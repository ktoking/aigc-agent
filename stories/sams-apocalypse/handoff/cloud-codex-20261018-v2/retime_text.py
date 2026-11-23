"""Create continuous, text-estimated captions; no audio synthesis or audio alignment."""
from pathlib import Path
import argparse
import hashlib
import json
import re


def units(text):
    return len(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]', text))


def stamp_ms(ms, sep=','):
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path(__file__).with_name('scripts-and-shots.json'))
    parser.add_argument('--out', type=Path, default=Path(__file__).with_name('estimated-timing'))
    parser.add_argument('--cps', type=float, default=5.0)
    parser.add_argument('--fps', type=int, default=30)
    args = parser.parse_args()
    if not 0 < args.cps <= 30 or args.fps < 1:
        parser.error('cps must be in (0,30] and fps positive')
    source = json.loads(args.source.read_text())
    args.out.mkdir(parents=True, exist_ok=True)
    all_episodes = []
    compilation = []
    offset = 0
    for ep in source['episodes']:
        cues = []
        segments = []
        cumulative_units = 0
        previous_end = 0
        for seg in ep['segments']:
            segment_start = previous_end
            for text in seg['narration']:
                count = units(text)
                if count == 0:
                    raise ValueError(f'Cue has no spoken units: {text!r}')
                cumulative_units += count
                # Round a cumulative boundary, rather than adding rounded cue durations.
                end = round(cumulative_units / args.cps * args.fps)
                if end <= previous_end:
                    raise ValueError('Cue is too short for the selected frame rate')
                cues.append({'index': len(cues)+1, 'segment': seg['segment'], 'text': text,
                             'characters': count, 'start_frame': previous_end,
                             'end_frame_exclusive': end, 'gap_after_frames': 0,
                             'timing_basis': 'text_estimate_not_audio_aligned'})
                previous_end = end
            segments.append({'segment': seg['segment'], 'start_frame': segment_start,
                             'end_frame_exclusive': previous_end,
                             'directory': f"segment_{seg['segment']:02d}_{segment_start/args.fps:.2f}-{previous_end/args.fps:.2f}s"})
        approved = ''.join(t for s in ep['segments'] for t in s['narration'])
        assert ''.join(c['text'] for c in cues) == approved
        assert cues[0]['start_frame'] == 0
        assert all(a['end_frame_exclusive'] == b['start_frame'] for a,b in zip(cues,cues[1:]))
        record = {'episode':ep['episode'], 'title':ep['title'], 'fps':args.fps,
                  'characters':cumulative_units, 'frame_count':previous_end,
                  'duration_seconds':previous_end/args.fps, 'segments':segments, 'cues':cues,
                  'script_sha256':hashlib.sha256(approved.encode()).hexdigest()}
        all_episodes.append(record)
        for c in cues:
            compilation.append({**c, 'episode':ep['episode'], 'start_frame':c['start_frame']+offset,
                                'end_frame_exclusive':c['end_frame_exclusive']+offset})
        offset += previous_end
        write_captions(args.out/f"EP{ep['episode']:03d}_text-estimate", cues, args.fps)
        (args.out/f"EP{ep['episode']:03d}_narration.txt").write_text('\n'.join(c['text'] for c in cues)+'\n')
    write_captions(args.out/'EP001-EP008_text-estimate', compilation, args.fps)
    result={'status':'estimated_only_not_rendered_or_audio_aligned','cps':args.cps,'fps':args.fps,
            'punctuation_padding_seconds':0,'inter_cue_gap_frames':0,'head_padding_frames':0,
            'tail_padding_frames':0,'frame_count':offset,'duration_seconds':offset/args.fps,
            'episodes':all_episodes}
    (args.out/'timing-plan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cps':args.cps,'episode_seconds':[x['duration_seconds'] for x in all_episodes],
                      'compilation_seconds':offset/args.fps,'gap_frames':0,'status':result['status']},ensure_ascii=False))


def write_captions(base, cues, fps):
    def ms(frame): return round(frame * 1000 / fps)
    srt=[];vtt=[]
    for i,c in enumerate(cues,1):
        a,b=ms(c['start_frame']),ms(c['end_frame_exclusive'])
        # Presentation line wrapping may be applied later without changing timings or text.
        srt.append(f"{i}\n{stamp_ms(a)} --> {stamp_ms(b)}\n{c['text']}")
        vtt.append(f"{stamp_ms(a,'.')} --> {stamp_ms(b,'.')}\n{c['text']}")
    base.with_suffix('.srt').write_text('\n\n'.join(srt)+'\n',encoding='utf-8')
    base.with_suffix('.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(vtt)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
