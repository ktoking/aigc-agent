from pathlib import Path
import json, subprocess, sys, time

P = Path(__file__).resolve().parents[1]
ROOT = P.parents[3]
PLAN = json.loads((P / 'voice-plan.json').read_text())
STATE = P / 'qa/tts-status.json'

def write_state(**extra):
    done = sum((P / 'audio/raw' / (c['id'] + '.metadata.json')).exists() for c in PLAN)
    state = dict(completed=done, total=len(PLAN), updated=time.time(), **extra)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(json.dumps(state, ensure_ascii=False), flush=True)

for cue in PLAN:
    cid = cue['id']
    target = P / 'audio/raw' / (cid + '.wav')
    if target.exists() and target.with_suffix('.metadata.json').exists():
        continue
    cmd = [sys.executable, str(ROOT / 'scripts/minimax_tts.py'), '--model', cue['model'],
           '--voice', cue['voice_id'], '--preset', 'documentary', '--speed', '1.2',
           '--emotion', 'calm', '--vol', '1', '--pitch', '0', '--format', 'wav',
           '--sample-rate', '32000', '--tone', '许棠/(xu3)(tang2)',
 '--text-file', str(P / 'audio/text' / (cid+'.txt')),
           '--output', str(target)]
    for attempt in range(8):
        started = time.monotonic()
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            write_state(status='RUNNING', last_completed=cid)
            time.sleep(max(0, 10 - (time.monotonic()-started)))
            break
        message = (r.stderr or r.stdout).strip()
        (P / 'qa' / (cid + '-failure.txt')).write_text(message)
        if '1002' in message and not target.exists() and attempt < 7:
            delay = min(60, 20 * (attempt+1))
            write_state(status='RATE_LIMIT_BACKOFF', cue=cid, backoff_seconds=delay)
            time.sleep(delay)
            continue
        write_state(status='FAILED', cue=cid, error=message[-1500:])
        sys.exit(1)
write_state(status='COMPLETE')
