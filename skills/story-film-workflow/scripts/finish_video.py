"""Add a quiet looping music bed, endpoint fades and an unchanged cover image.

Requires ffmpeg/ffprobe. Does not regenerate TTS, shift captions or insert a cover card.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import shutil
import subprocess


def run(args):
    subprocess.run(args, check=True)


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)
    ]))


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def loudness(path):
    result = subprocess.run([
        'ffmpeg', '-hide_banner', '-nostats', '-i', str(path),
        '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'
    ], check=True, capture_output=True, text=True).stderr
    return json.loads(result[result.rfind('{'):result.rfind('}') + 1])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['video', 'narration', 'bgm', 'cover', 'output', 'work-dir']:
        ap.add_argument('--' + name, type=Path, required=True)
    ap.add_argument('--bgm-gain-db', type=float)
    ap.add_argument('--music-margin-db', type=float, default=14)
    ap.add_argument('--music-peak-db', type=float, default=-22)
    ap.add_argument('--music-fade', type=float, default=.5)
    ap.add_argument('--video-fade', type=float, default=.3)
    ap.add_argument('--duck-music', action='store_true',
                    help='Opt in only when requested; default is a constant quiet music gain.')
    args = ap.parse_args()
    for name in ['video', 'narration', 'bgm', 'cover']:
        setattr(args, name, getattr(args, name).resolve(strict=True))
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing output; choose a new version.')
    if not all(math.isfinite(v) and v >= 0 for v in [
        args.music_margin_db, args.music_fade, args.video_fade
    ]):
        raise SystemExit('Fade durations and music margin must be finite and nonnegative.')
    args.output = args.output.resolve()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    info = probe(args.video)
    track = next(s for s in info['streams'] if s['codec_type'] == 'video'
                 and not s.get('disposition', {}).get('attached_pic'))
    duration = float(track.get('duration', info['format']['duration']))
    fps_a, fps_b = map(int, track['r_frame_rate'].split('/'))
    fps = fps_a / fps_b
    frames = int(track.get('nb_frames') or round(duration * fps))
    duration = frames / fps
    if max(args.music_fade, args.video_fade) * 2 > duration:
        raise SystemExit('Endpoint fades would overlap.')
    speech_duration = float(probe(args.narration)['format']['duration'])
    if abs(speech_duration - duration) > 1 / fps:
        raise SystemExit('Narration does not match video duration; resolve timing first.')
    gain = args.bgm_gain_db
    measurements = None
    if gain is None:
        voice, music = loudness(args.narration), loudness(args.bgm)
        measurements = {'voice': voice, 'music': music}
        gain = min(float(voice['input_i']) - args.music_margin_db - float(music['input_i']),
                   args.music_peak_db - float(music['input_tp']))
    if not math.isfinite(gain):
        raise SystemExit('Invalid music gain; check source audio.')
    raw_bed = args.work_dir / 'bgm-loop.wav'
    bed = args.work_dir / 'bgm-bed.wav'
    mix = args.work_dir / 'mix.wav'
    # Loop without adding a separate pause. Trim once, then apply endpoint fades once.
    samples = round(duration * 48000)
    run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-stream_loop', '-1', '-i', str(args.bgm),
         '-af', f'aresample=48000,asetpts=PTS-STARTPTS,apad=whole_len={samples},'
                f'atrim=end_sample={samples},'
                f'volume={gain:.9f}dB,afade=t=in:st=0:d={args.music_fade},'
                f'afade=t=out:st={duration-args.music_fade:.9f}:d={args.music_fade}',
         '-ar', '48000', '-ac', '2', '-c:a', 'pcm_f32le', str(raw_bed)])
    if args.duck_music:
        run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', str(raw_bed),
             '-i', str(args.narration), '-filter_complex',
             '[0:a][1:a]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=250:makeup=1[out]',
             '-map', '[out]', '-t', f'{duration:.9f}', '-ar', '48000', '-ac', '2',
             '-c:a', 'pcm_f32le', str(bed)])
    else:
        shutil.copy2(raw_bed, bed)
    run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', str(args.narration), '-i', str(bed),
         '-filter_complex',
         '[0:a]aformat=channel_layouts=stereo[voice];'
         '[voice][1:a]amix=inputs=2:duration=first:normalize=0[out]',
         '-map', '[out]', '-t', f'{duration:.9f}', '-ar', '48000', '-ac', '2',
         '-c:a', 'pcm_f32le', str(mix)])
    poster = args.output.parent / ('cover' + args.cover.suffix.lower())
    if poster.resolve() != args.cover:
        shutil.copy2(args.cover, poster)
    fade_frames = round(args.video_fade * fps)
    fade_steps = max(1, fade_frames - 1)
    vf = (f'fade=t=in:s=0:n={fade_steps},'
          f'fade=t=out:s={frames-fade_frames}:n={fade_steps}') if fade_frames else 'null'
    cmd = ['ffmpeg', '-v', 'error', '-nostdin', '-n', '-i', str(args.video),
           '-i', str(mix), '-i', str(poster), '-map', f"0:{track['index']}",
           '-map', '1:a:0', '-map', '2:v:0', '-filter:v:0', vf,
           '-c:v:0', 'libx264', '-crf', '18', '-preset', 'veryfast', '-threads', '4',
           '-pix_fmt:v:0', 'yuv420p', '-bf', '0', '-c:a', 'aac', '-b:a', '256k',
           '-c:v:1', 'copy', '-disposition:v:0', 'default',
           '-disposition:v:1', 'attached_pic', '-metadata:s:v:1', 'title=Cover',
           '-metadata:s:v:1', 'comment=Cover (front)', '-map_metadata', '-1',
           '-t', f'{duration:.9f}', '-movflags', '+faststart', str(args.output)]
    # No output-global -frames:v: it can truncate cover or audio streams.
    run(cmd)
    report = {
        'status': 'RENDERED_QA_PENDING', 'video': str(args.output),
        'duration_seconds': duration, 'frames': frames, 'fps': fps,
        'music_gain_db': gain, 'music_fade_seconds': args.music_fade,
        'video_fade_seconds': fade_frames/fps, 'video_fade_frames': fade_frames,
        'narration_gain_changed': False, 'music_ducking': args.duck_music,
        'music_gain_mode': 'sidechain' if args.duck_music else 'constant_except_endpoint_fades',
        'cover_mode': 'attached_pic_and_external_poster_no_timeline_insert',
        'sources': {name: {'path': str(getattr(args, name)), 'sha256': digest(getattr(args, name))}
                    for name in ['video', 'narration', 'bgm', 'cover']},
        'loudness_measurements': measurements, 'output_sha256': digest(args.output),
        'render_command': cmd,
    }
    args.output.with_suffix('.manifest.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
