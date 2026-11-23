from pathlib import Path
import subprocess,json,hashlib,math,time,sys
P=Path(__file__).resolve().parent;R=P.parents[1];REPO=R.parents[1]
q=json.loads((P/'voice-queue.json').read_text());results=[]
def save():
    (P/'voice-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    s=json.loads((P/'status.json').read_text());s['voice_complete']=sum(x['status']=='PASS' for x in results);s['voice_status']='IN_PROGRESS';s['voice_last']=results[-1] if results else None
    (P/'status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
def probe(path):
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)],capture_output=True,text=True,check=True)
    return float(json.loads(r.stdout)['format']['duration'])
for c in q:
    start=time.monotonic();cid=c['cue_id'];D=R/'episodes'/c['episode'];raw=D/'audio'/f'{cid}.mp3';out=D/'audio-speed1p3'/f'{cid}.wav';existed=raw.exists()
    if not existed:
        cmd=['python3',str(REPO/'scripts/minimax_tts.py'),'--voice',c['voice_id'],'--preset','natural','--emotion','calm','--speed','1.0','--vol','1.0','--pitch',str(c['pitch']),'--sound-effect',c['sound_effect'],'--text-file',str(R/c['text_path']),'--output',str(raw)]
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode:
            results.append({'cue_id':cid,'status':'FAILED_NO_AUTO_RETRY','error':r.stderr.strip()});save()
            s=json.loads((P/'status.json').read_text());s['voice_status']='FAILED_NO_AUTO_RETRY';(P/'status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
            print(json.dumps(results[-1],ensure_ascii=False),flush=True);sys.exit(1)
    m=json.loads(raw.with_suffix('.metadata.json').read_text())
    assert m['request']['voice_setting']['voice_id']==c['voice_id']
    assert m['request']['text'].strip()==c['tts_text'].strip()
    if not out.exists():
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-af','atempo=1.3','-ar','48000','-ac','1','-c:a','pcm_s16le',str(out)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
    sec=probe(out)
    res={'cue_id':cid,'status':'PASS','speaker':c['speaker'],'voice_id':c['voice_id'],'raw_audio_path':str(raw.relative_to(R)),'audio_path':str(out.relative_to(R)),'raw_duration_seconds':probe(raw),'actual_duration_seconds':sec,'audio_frames_30fps':math.ceil(sec*30),'audio_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_text':c['source_text'],'human_listening':'NOT_RUN'}
    results.append(res);save()
    print(json.dumps({'cue_id':cid,'speaker':c['speaker'],'seconds':round(sec,3),'done':len(results),'total':len(q)},ensure_ascii=False),flush=True)
    # 已生成成功文件不再请求；新请求按8秒间隔节流，不对错误自动收费重试。
    if not existed:
        delay=8-(time.monotonic()-start)
        if delay>0:time.sleep(delay)
s=json.loads((P/'status.json').read_text());s['voice_status']='PASS_GENERATED_DECODED';(P/'status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print('ALL_VOICE_COMPLETE',flush=True)
