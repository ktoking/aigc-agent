#!/usr/bin/env python3
"""Plan, render and verify portable, caption-detached silent still-image films."""
import argparse
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for part in iter(lambda: source.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def positive_int(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f'{label} must be a positive integer')
    return value


def number(value, label, allow_zero=False):
    if isinstance(value, bool):
        raise ValueError(f'{label} must be numeric')
    try:
        d = Decimal(str(value))
    except Exception as exc:
        raise ValueError(f'{label} must be numeric') from exc
    if not d.is_finite() or (d < 0 if allow_zero else d <= 0):
        raise ValueError(f'{label} must be finite and {"nonnegative" if allow_zero else "positive"}')
    return d


def quantize(seconds, fps):
    return int((seconds * fps).to_integral_value(rounding=ROUND_HALF_UP))


def timestamp(frame, fps, decimal=','):
    ms = int((Decimal(frame) * 1000 / fps).to_integral_value(rounding=ROUND_HALF_UP))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d}{decimal}{ms:03d}'


def caption_files(timeline):
    srt, vtt = [], []
    fps = timeline['fps']
    for i, cue in enumerate(timeline['cues'], 1):
        a, b = cue['start_frame'], cue['end_frame_exclusive']
        srt.append(f"{i}\n{timestamp(a, fps)} --> {timestamp(b, fps)}\n{cue['text']}")
        vtt.append(f"{timestamp(a, fps, '.')} --> {timestamp(b, fps, '.')}\n{cue['text']}")
    return '\n\n'.join(srt) + '\n', 'WEBVTT\n\n' + '\n\n'.join(vtt) + '\n'


def make_plan(project_path):
    project_path = project_path.resolve()
    spec = json.loads(project_path.read_text(encoding='utf-8'))
    fps = positive_int(spec.get('fps', 30), 'fps')
    width = positive_int(spec.get('width', 1920), 'width')
    height = positive_int(spec.get('height', 1080), 'height')
    if width % 2 or height % 2:
        raise ValueError('H.264 yuv420p requires even width and height')
    gap_requested = number(spec.get('gap_seconds', 0.1), 'gap_seconds', True)
    dissolve_requested = number(spec.get('dissolve_seconds', 0.1), 'dissolve_seconds', True)
    gap, dissolve = quantize(gap_requested, fps), quantize(dissolve_requested, fps)
    if dissolve > gap:
        raise ValueError('Dissolve must fit inside the inter-cue gap; change parameters explicitly')
    cps = number(spec.get('characters_per_second', 7.5), 'characters_per_second')
    assets = spec.get('assets')
    if not isinstance(assets, dict) or not assets:
        raise ValueError('assets must be a nonempty id-to-file object')
    for key, value in assets.items():
        if not isinstance(key, str) or not isinstance(value, str) or not value:
            raise ValueError('Asset ids and file paths must be nonempty strings')
    episodes = spec.get('episodes')
    if not isinstance(episodes, list) or not episodes:
        raise ValueError('episodes must be a nonempty list')
    cues, chapters, seen_ids = [], [], set()
    cursor = 0
    for ei, episode in enumerate(episodes, 1):
        eid = str(episode.get('id', f'EP{ei:03d}'))
        if eid in seen_ids:
            raise ValueError(f'Duplicate episode id: {eid}')
        seen_ids.add(eid)
        authored = episode.get('cues')
        if not isinstance(authored, list) or not authored:
            raise ValueError(f'{eid} has no cues')
        chapter_start = None
        for ci, item in enumerate(authored, 1):
            text = item.get('text')
            if not isinstance(text, str) or not text.strip() or '\n\n' in text:
                raise ValueError(f'{eid} cue {ci}: nonempty text required; split blank lines into separate cues')
            key = item.get('asset')
            if key not in assets:
                raise ValueError(f'{eid} cue {ci}: unknown asset {key}')
            if 'duration_frames' in item and 'duration_seconds' in item:
                raise ValueError(f'{eid} cue {ci}: specify frames OR seconds, not both')
            if 'duration_frames' in item:
                frames = positive_int(item['duration_frames'], 'duration_frames')
                basis = item.get('timing_basis', 'provided_duration')
            elif 'duration_seconds' in item:
                frames = max(1, quantize(number(item['duration_seconds'], 'duration_seconds'), fps))
                basis = item.get('timing_basis', 'provided_duration')
            else:
                spoken = item.get('spoken_text', text)
                if not isinstance(spoken, str):
                    raise ValueError('spoken_text must be a string')
                units = number(item['spoken_units'], 'spoken_units') if 'spoken_units' in item else Decimal(sum(c.isalnum() for c in spoken))
                if units <= 0:
                    raise ValueError('Text-only timing needs spoken letters/digits or positive spoken_units')
                frames = max(1, quantize(units / cps, fps))
                basis = 'text_estimate_not_audio_aligned'
            if cues:
                cursor += gap
            if chapter_start is None:
                chapter_start = cursor
            cues.append({'index': len(cues) + 1, 'episode': eid, 'episode_cue': ci,
                         'text': text, 'asset': key, 'duration_frames': frames,
                         'start_frame': cursor, 'end_frame_exclusive': cursor + frames,
                         'timing_basis': basis})
            cursor += frames
        chapters.append({'episode': eid, 'title': str(episode.get('title', eid)),
                         'start_frame': chapter_start, 'end_frame_exclusive': cursor})
    transitions = []
    for a, b in zip(cues, cues[1:]):
        if a['asset'] != b['asset'] and dissolve:
            transitions.append({'start_frame': b['start_frame'] - dissolve,
                                'end_frame_exclusive': b['start_frame'],
                                'old_asset': a['asset'], 'new_asset': b['asset']})
    for i, chapter in enumerate(chapters):
        if i + 1 < len(chapters):
            chapter['end_frame_exclusive'] = chapters[i + 1]['start_frame']
        chapter['start_seconds'] = chapter['start_frame'] / fps
        chapter['end_seconds'] = chapter['end_frame_exclusive'] / fps
    return {'schema_version': 1, 'name': str(spec.get('name', project_path.stem)),
            'project_file': project_path.name, 'project_sha256': digest(project_path),
            'fps': fps, 'width': width, 'height': height,
            'gap_requested_seconds': str(gap_requested), 'gap_frames': gap,
            'gap_actual_seconds': gap / fps,
            'dissolve_requested_seconds': str(dissolve_requested), 'dissolve_frames': dissolve,
            'dissolve_actual_seconds': dissolve / fps,
            'frame_count': cursor, 'duration_seconds': cursor / fps,
            'gap_count': len(cues) - 1, 'audio': False,
            'subtitles_burned': False, 'subtitles_embedded': False,
            'assets': assets, 'cues': cues, 'chapters': chapters, 'transitions': transitions}


def write_plan(project, out, allow_rendered=False):
    if (out / 'video.mp4').exists() and not allow_rendered:
        raise ValueError('Output contains a rendered video; plan in a new version directory')
    timeline = make_plan(project)
    out.mkdir(parents=True, exist_ok=True)
    save(out / 'timeline.json', timeline)
    save(out / 'chapters.json', timeline['chapters'])
    srt, vtt = caption_files(timeline)
    (out / 'captions.srt').write_text(srt, encoding='utf-8')
    (out / 'captions.vtt').write_text(vtt, encoding='utf-8')
    return timeline


def render(project, out, overwrite=False):
    video = out / 'video.mp4'
    if video.exists() and not overwrite:
        raise ValueError('video.mp4 exists; use a new output directory or explicit --overwrite')
    if not shutil.which('ffmpeg'):
        raise ValueError('ffmpeg is required')
    from PIL import Image, ImageOps
    timeline = make_plan(project)
    source_dir = project.resolve().parent
    paths = {key: (source_dir / value).resolve() for key, value in timeline['assets'].items()}
    used = {c['asset'] for c in timeline['cues']}
    for key in used:
        if not paths[key].is_file():
            raise ValueError(f'Missing image: {key} -> {paths[key]}')
        with Image.open(paths[key]) as im:
            im.verify()
    timeline = write_plan(project, out, allow_rendered=overwrite)
    size = (timeline['width'], timeline['height'])
    cached_key, cached_im = None, None
    def picture(key):
        nonlocal cached_key, cached_im
        if key != cached_key:
            with Image.open(paths[key]) as im:
                cached_im = ImageOps.fit(im.convert('RGB'), size, method=Image.Resampling.LANCZOS)
            cached_key = key
        return cached_im
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{size[0]}x{size[1]}', '-r', str(timeline['fps']), '-i', '-',
           '-map', '0:v:0', '-an', '-sn', '-dn', '-c:v', 'libx264', '-preset', 'veryfast',
           '-tune', 'stillimage', '-crf', '18', '-bf', '0', '-threads', '4',
           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(video)]
    written, current = 0, None
    with (out / 'render.log').open('w') as log:
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=log)
        try:
            for i, cue in enumerate(timeline['cues']):
                incoming = picture(cue['asset'])
                if i:
                    changed = timeline['cues'][i - 1]['asset'] != cue['asset']
                    d = timeline['dissolve_frames'] if changed else 0
                    old_raw = current.tobytes()
                    for k in range(timeline['gap_frames']):
                        fade_index = k - (timeline['gap_frames'] - d)
                        raw = Image.blend(current, incoming, (fade_index + 1) / d).tobytes() if d and fade_index >= 0 else old_raw
                        enc.stdin.write(raw)
                        written += 1
                if written != cue['start_frame']:
                    raise ValueError('Render cursor drift')
                raw = incoming.tobytes()
                for _ in range(cue['duration_frames']):
                    enc.stdin.write(raw)
                    written += 1
                current = incoming
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError('Encoding failed; see render.log')
        except BaseException:
            if enc.poll() is None:
                enc.terminate()
                enc.wait()
            raise
    if written != timeline['frame_count']:
        raise ValueError('Incorrect frame count written')
    manifest = {'status': 'rendered_pending_verification', 'frames_written': written,
                'timeline_sha256': digest(out / 'timeline.json'), 'video_sha256': digest(video),
                'source_assets': {key: {'file': timeline['assets'][key], 'sha256': digest(paths[key])} for key in sorted(used)},
                'renderer': 'fixed source images and gap-contained dissolves; no text drawing; no audio input',
                'manual_visual_review': 'NOT_RUN', 'actual_browser_playback': 'NOT_RUN'}
    save(out / 'render-manifest.json', manifest)
    return {'video': str(video.resolve()), 'duration_seconds': timeline['duration_seconds'], 'frames': written}


def verify(out):
    save(out / 'qa.json', {'automated_checks': 'running'})
    for tool in ['ffmpeg', 'ffprobe']:
        if not shutil.which(tool):
            raise ValueError(f'{tool} is required')
    timeline_path, video = out / 'timeline.json', out / 'video.mp4'
    t = json.loads(timeline_path.read_text(encoding='utf-8'))
    manifest = json.loads((out / 'render-manifest.json').read_text(encoding='utf-8'))
    if digest(timeline_path) != manifest['timeline_sha256'] or digest(video) != manifest['video_sha256']:
        raise ValueError('Rendered video or timeline changed after rendering')
    cues = t['cues']
    if not cues or cues[0]['start_frame'] != 0 or cues[-1]['end_frame_exclusive'] != t['frame_count']:
        raise ValueError('Leading/trailing timing mismatch')
    for cue in cues:
        if cue['end_frame_exclusive'] - cue['start_frame'] != cue['duration_frames']:
            raise ValueError('Cue duration changed')
    for a, b in zip(cues, cues[1:]):
        if b['start_frame'] - a['end_frame_exclusive'] != t['gap_frames']:
            raise ValueError('Cue gap mismatch')
    expected_transitions = [{'start_frame': b['start_frame'] - t['dissolve_frames'],
                            'end_frame_exclusive': b['start_frame'],
                            'old_asset': a['asset'], 'new_asset': b['asset']}
                           for a, b in zip(cues, cues[1:]) if a['asset'] != b['asset'] and t['dissolve_frames']]
    if t['transitions'] != expected_transitions:
        raise ValueError('Dissolve timing mismatch')
    expected_srt, expected_vtt = caption_files(t)
    if (out / 'captions.srt').read_text(encoding='utf-8') != expected_srt or (out / 'captions.vtt').read_text(encoding='utf-8') != expected_vtt:
        raise ValueError('Subtitles do not match timeline')
    if json.loads((out / 'chapters.json').read_text(encoding='utf-8')) != t['chapters']:
        raise ValueError('Chapters do not match timeline')
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(video)]))
    streams = probe['streams']
    if len(streams) != 1 or streams[0]['codec_type'] != 'video':
        raise ValueError('Delivery must contain exactly one video stream and no audio/subtitle/data streams')
    v = streams[0]
    if (v['width'], v['height']) != (t['width'], t['height']) or Fraction(v['r_frame_rate']) != t['fps'] or int(v['nb_read_frames']) != t['frame_count']:
        raise ValueError('Encoded resolution, fps or frame count mismatch')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-f', 'null', '-'], check=True)
    report = {'automated_checks': 'passed', 'frames': t['frame_count'], 'duration_seconds': t['duration_seconds'],
              'fps': t['fps'], 'resolution': [t['width'], t['height']], 'cue_count': len(cues),
              'gap_count': len(cues) - 1, 'gap_frames': t['gap_frames'],
              'gap_actual_seconds': t['gap_actual_seconds'], 'dissolve_count': len(t['transitions']),
              'dissolve_frames': t['dissolve_frames'], 'audio_streams': 0, 'subtitle_streams': 0,
              'full_decode': 'passed', 'subtitle_text_and_timing_exact_to_plan': True,
              'visual_absence_of_burned_text': 'NOT_RUN; inspect encoded pictures; stream counts alone cannot prove this',
              'actual_browser_playback': 'NOT_RUN', 'full_human_watch': 'NOT_RUN'}
    save(out / 'ffprobe.json', probe)
    save(out / 'qa.json', report)
    manifest['status'] = 'automated_passed_manual_review_pending'
    save(out / 'render-manifest.json', manifest)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['plan', 'render', 'verify']:
        p = sub.add_parser(name)
        p.add_argument('--output', type=Path, required=True)
        if name != 'verify':
            p.add_argument('--project', type=Path, required=True)
        if name == 'render':
            p.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'plan':
            t = write_plan(args.project, args.output)
            result = {k: t[k] for k in ['frame_count', 'duration_seconds', 'gap_frames', 'gap_actual_seconds', 'dissolve_frames', 'dissolve_actual_seconds']}
        elif args.command == 'render':
            result = render(args.project, args.output, args.overwrite)
        else:
            result = verify(args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        if args.command == 'verify' and args.output.is_dir():
            save(args.output / 'qa.json', {'automated_checks': 'failed', 'error': str(exc)})
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
