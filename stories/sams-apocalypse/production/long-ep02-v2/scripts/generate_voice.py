from pathlib import Path
import concurrent.futures as cf
import subprocess,json,threading,time,sys
P=Path(__file__).resolve().parents[1]
SKILL=P.parents[3]/'skills/story-film-workflow/scripts/minimax_tts.py'
plan=json.loads((P/'voice-plan.json').read_text())
lock=threading.Lock();stopped=threading.Event();last=[0.0];completed=[0]
def one(c):
    path=P/'audio/raw'/(c['id']+'.wav')
    if path.exists() and path.with_suffix('.metadata.json').exists():return c['id']
    if stopped.is_set():return None
    with lock:
        time.sleep(max(0,8.0-(time.monotonic()-last[0])));last[0]=time.monotonic()
    if stopped.is_set():return None
    cmd=[sys.executable,str(SKILL),'--model',c['model'],'--voice',c['voice_id'],'--preset',c['preset'],'--speed',str(c['api_speed']),'--text-file',str(P/'audio'/(c['id']+'.txt')),'--output',str(path),'--format','wav','--sample-rate','32000','--tone','许棠/(xu3)(tang2)','--tone','林岚/(lin2)(lan2)','--tone','周强/(zhou1)(qiang2)']
    result=subprocess.run(cmd,capture_output=True,text=True)
    if result.returncode:
        stopped.set();(P/'audio'/f"{c['id']}-failure.txt").write_text(result.stderr)
        raise RuntimeError(f"{c['id']}: {result.stderr.strip()}")
    with lock:
        completed[0]+=1
        if completed[0]%12==0:print(f'TTS generated {completed[0]}/{len(plan)}',flush=True)
    return c['id']
with cf.ThreadPoolExecutor(max_workers=2) as executor:
    futures=[executor.submit(one,c) for c in plan]
    for f in cf.as_completed(futures):
        try:f.result()
        except Exception as e:
            print(str(e),flush=True)
            for other in futures:other.cancel()
            raise
print('TTS complete',flush=True)
