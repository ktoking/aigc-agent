from pathlib import Path
import subprocess,time,json
P=Path(__file__).resolve().parent
REPO=P.parents[3]
items=[('XU','female-chengshu'),('QIAO','female-tianmei'),('GU','Chinese (Mandarin)_Soft_Girl')]
text='门关好了。先坐下，把手给我，别动。剩下的事，等你休息好了再说。'
results=[]
for role,voice in items:
    out=P/'voice-tests'/f'{role}.mp3'
    if not out.exists():
        time.sleep(8)
        r=subprocess.run(['python3',str(REPO/'scripts/minimax_tts.py'),'--voice',voice,'--preset','natural','--emotion','calm','--speed','1.0','--text',text,'--output',str(out)],capture_output=True,text=True)
        if r.returncode:
            results.append({'role':role,'status':'FAILED_NO_AUTO_RETRY','error':r.stderr.strip()})
            break
    results.append({'role':role,'status':'GENERATED_LISTENING_NOT_RUN','path':str(out)})
    print(json.dumps(results[-1],ensure_ascii=False),flush=True)
(P/'voice-tests/status.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
