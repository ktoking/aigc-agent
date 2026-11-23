"""保留供应商原文件，实测保音调加速后的cue并建立独立版本。"""
from pathlib import Path
import array, copy, hashlib, json, math, subprocess, wave

R = Path(__file__).resolve().parents[1]
V = R / 'production/user-script-v2'
FPS, SR, SPEED = 30, 48000, 1.3
TAG = 'speed1p3'

def run(args, **kwargs):
    return subprocess.run(list(map(str, args)), check=True, **kwargs)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    queue = {s['shot_id']: s for s in json.loads((V / 'image-queue.json').read_text())}
    results = []
    for source in sorted((R / 'episodes').glob('EP*/timeline.json')):
        d = source.parent
        t = json.loads(source.read_text())
        assert not t.get('tempo_multiplier'), '输入必须是原始1.0时间线'
        out = copy.deepcopy(t)
        out.update(tempo_multiplier=SPEED, provider_speed=1.0, variant=TAG,
                   source_timeline=str(source.relative_to(R)), cues=[], shots=[])
        audio = d / 'audio' / TAG
        audio.mkdir(exist_ok=True)
        cursor = 0
        cue_pcm = []
        original_hash = sha(d / 'narration.txt')
        for ci, original in enumerate(t['cues']):
            c = copy.deepcopy(original)
            src = R / c['audio_path']
            target = audio / (c['cue_id'] + '.wav')
            # 音频正文与供应商metadata不改；每个cue只加速一次。
            meta = target.with_suffix('.tempo.json')
            key = {'source_sha256': sha(src), 'tempo_multiplier': SPEED, 'sample_rate': SR}
            cached = json.loads(meta.read_text()) if meta.exists() else {}
            if not target.exists() or any(cached.get(k) != v for k, v in key.items()):
                run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', f'atempo={SPEED}',
                     '-ac', '1', '-ar', SR, '-c:a', 'pcm_s16le', target])
            with wave.open(str(target), 'rb') as wav:
                assert wav.getframerate() == SR and wav.getnchannels() == 1
                samples = wav.getnframes()
                raw = wav.readframes(samples)
            save(meta, {**key, 'source_audio_path': str(src.relative_to(R)),
                        'source_provider_speed': 1.0, 'preserve_pitch': True,
                        'samples': samples, 'actual_duration_seconds': samples / SR,
                        'audio_sha256': sha(target), 'full_decode': 'PASS'})
            gap = 3 if ci else 0
            frames = math.ceil(samples * FPS / SR)
            total = frames + gap
            c.update(source_audio_path=original['audio_path'],
                     source_audio_sha256=original['audio_sha256'],
                     source_duration_seconds=original['actual_duration_seconds'],
                     audio_path=str(target.relative_to(R)), audio_sha256=sha(target),
                     actual_duration_seconds=samples / SR, sample_count=samples,
                     start_frame=cursor + gap, end_frame=cursor + total,
                     external_gap_before_frames=gap)
            out['cues'].append(c)
            cue_pcm.append((c, raw))
            candidates = [copy.deepcopy(queue[s['shot_id']]) for s in t['shots']
                          if c['cue_id'] in s['cue_ids']]
            # 短于约7.5秒时保留一张主事件图，长段采用两张，避免全部旧镜机械缩短。
            n = min(len(candidates), max(1, math.floor(total / (FPS * 5) + .5)))
            selected = candidates[:n]
            for k, s in enumerate(selected):
                start = cursor + total * k // n
                end = cursor + total * (k + 1) // n
                seconds = (end - start) / FPS
                s.update(start_frame=start, end_frame=end, display_seconds=seconds,
                         transition_frames=gap if k == 0 else 0,
                         timing_status='MEASURED_POSTPROCESSED_AUDIO_INTEGER_FRAMES',
                         final_timing_locked=True,
                         duration_exception_reason=None if 4 <= seconds <= 6 else
                         '原句事件边界保留；短回应或完整句群随实测1.3倍音频呈现，不截词、不延长音轨')
                out['shots'].append(s)
            cursor += total
        out.update(frames=cursor, duration_seconds=cursor / FPS,
                   timing_note='135段原声逐段atempo=1.3，按PCM实测采样数向上取整到帧；外部空档仍为3帧且只计一次。原始1.0时间线与文件保留。')
        pcm = array.array('h', [0]) * (cursor * (SR // FPS))
        for c, raw in cue_pcm:
            chunk = array.array('h')
            chunk.frombytes(raw)
            pos = c['start_frame'] * (SR // FPS)
            assert len(chunk) <= (c['end_frame'] - c['start_frame']) * (SR // FPS)
            pcm[pos:pos + len(chunk)] = chunk
        work = d / 'render' / TAG
        work.mkdir(parents=True, exist_ok=True)
        master = work / 'narration.wav'
        with wave.open(str(master), 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(SR)
            wav.writeframes(pcm.tobytes())
        mp3 = d / 'output' / f'{d.name}_Chinese_worker_male_{TAG}.mp3'
        run(['ffmpeg', '-v', 'error', '-y', '-i', master, '-c:a', 'libmp3lame', '-b:a', '128k', mp3])
        run(['ffmpeg', '-v', 'error', '-i', mp3, '-f', 'null', '-'], capture_output=True)
        assert sha(d / 'narration.txt') == original_hash
        assert ''.join(c['text'] for c in out['cues']) == ''.join(c['text'] for c in t['cues'])
        clipped = sum(abs(x) >= 32767 for x in pcm)
        assert clipped == 0
        out['audio_master_path'] = str(master.relative_to(R))
        save(d / f'timeline-{TAG}.json', out)
        rows = ['# ' + d.name + ' · 1.3倍实测镜头表', '',
                '正文零改写，原声保留；供应商speed=1.0，后期保音调atempo=1.3。', '',
                '|镜头|帧区间|秒|原cue|事件|', '|---|---|---:|---|---|']
        for s in out['shots']:
            rows.append(f"|{s['shot_id']}|{s['start_frame']}—{s['end_frame']}|{s['display_seconds']:.2f}|{','.join(s['cue_ids'])}|{s['unique_event']}|")
        (d / f'storyboard-{TAG}.md').write_text('\n'.join(rows) + '\n')
        result = dict(episode=d.name, variant=TAG, voice_id='Chinese_worker_male',
                      provider_speed=1.0, tempo_multiplier=SPEED, preserve_pitch=True,
                      original_duration_seconds=t['duration_seconds'], duration_seconds=cursor / FPS,
                      standalone_mp3=str(mp3.relative_to(R)), master_wave=str(master.relative_to(R)),
                      timeline=str((d / f'timeline-{TAG}.json').relative_to(R)),
                      shots=len(out['shots']), range_4_6=sum(4 <= s['display_seconds'] <= 6 for s in out['shots']),
                      images_ready=sum(bool(s.get('image_path')) for s in out['shots']),
                      all_cue_tails_fit=True, clipped_samples=clipped, full_decode='PASS',
                      script_sha256=original_hash, text_changes=0, human_listening='NOT_RUN',
                      sha256=sha(mp3))
        save(d / 'output' / f'audio-manifest-{TAG}.json', result)
        results.append(result)
        print(d.name, result['original_duration_seconds'], '→', result['duration_seconds'],
              'seconds;', len(out['shots']), 'shots', flush=True)
    save(V / f'audio-master-summary-{TAG}.json', results)
    save(V / f'image-queue-{TAG}.json', [s for r in results
         for s in json.loads((R / r['timeline']).read_text())['shots']])

if __name__ == '__main__':
    main()
