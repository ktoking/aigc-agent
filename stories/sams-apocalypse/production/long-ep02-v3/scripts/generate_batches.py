from pathlib import Path
import json,time,hashlib,urllib.request,urllib.error,importlib.util,argparse
P=Path(__file__).resolve().parents[1];D=P/'audio/batches';ERROR=P/'qa/tts-last-error.json'
spec=importlib.util.spec_from_file_location('tts',P.parents[3]/'skills/story-film-workflow/scripts/minimax_tts.py');client=importlib.util.module_from_spec(spec);spec.loader.exec_module(client)
batches=json.loads((D/'batch-plan.json').read_text());parser=argparse.ArgumentParser();parser.add_argument('--one',action='store_true');args=parser.parse_args()
def write(path,data):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)
for b in batches:
    wav=D/(b['id']+'.wav');meta=D/(b['id']+'.json')
    if wav.exists() and meta.exists():
        previous=json.loads(meta.read_text())
        if previous.get('alignment'):continue
        assert previous.get('alignment_url'),'Audio exists without resumable alignment reference; do not resynthesize'
        m=previous
    else:
        assert not wav.exists() and not meta.exists(),'Partial audio requires review before any paid retry'
        preset=client.presets()[b['preset']];voice={'voice_id':'Chinese (Mandarin)_Gentleman',**preset['voice_setting'],'speed':1.2,'vol':1.0,'pitch':0}
        payload={'model':'speech-2.8-turbo','text':b['text'],'stream':False,'voice_setting':voice,'audio_setting':{'sample_rate':32000,'format':'wav','channel':1},'language_boost':'Chinese','output_format':'hex','subtitle_enable':True,'subtitle_type':'word','pronunciation_dict':{'tone':['许棠/(xu3)(tang2)','林岚/(lin2)(lan2)','周强/(zhou1)(qiang2)']}}
        if preset.get('voice_modify'):payload['voice_modify']=preset['voice_modify']
        for attempt in range(3):
            latest=max([f.stat().st_mtime for f in (P/'audio/raw').glob('*.metadata.json')]+[f.stat().st_mtime for f in D.glob('b[0-9]*.json')],default=0)
            not_before=latest+65
            if ERROR.exists():not_before=max(not_before,json.loads(ERROR.read_text()).get('next_attempt_after',0))
            delay=max(0,not_before-time.time())
            if delay:print(json.dumps({'batch':b['id'],'wait_seconds':round(delay,1)}),flush=True);time.sleep(delay)
            key=client.api_key();req=urllib.request.Request(client.API_URL,data=json.dumps(payload,ensure_ascii=False).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
            # Transport/unknown failures stop, so an uncertain success is never billed a second time automatically.
            with urllib.request.urlopen(req,timeout=180) as response:result=json.load(response);status=response.status;trace=response.headers.get('Trace-Id')
            base=result.get('base_resp') or {};data=result.get('data') or {}
            if base.get('status_code')==0:break
            error={'batch':b['id'],'status_code':base.get('status_code'),'message':str(base.get('status_msg')).replace(key,'[REDACTED]'),'trace_id':trace,'time_epoch':time.time(),'attempt':attempt+1}
            if base.get('status_code')==1002 and not data.get('audio'):
                error['next_attempt_after']=time.time()+150*(attempt+1);write(ERROR,error);print(json.dumps(error),flush=True)
                if attempt<2:continue
            raise RuntimeError('TTS stopped: '+str(error['status_code'])+' '+error['message'])
        assert data.get('status')==2 and data.get('audio')
        with wav.open('xb') as f:f.write(bytes.fromhex(data['audio']))
        assert data.get('subtitle_file'),'Missing provider alignment reference'
        m={'http_status':status,'base_status_code':0,'trace_id':result.get('trace_id') or trace,'request':payload,'preset':b['preset'],'extra_info':result.get('extra_info'),'alignment_url':data['subtitle_file'],'cue_ranges':b['cues'],'sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),'note':'Provider word timing for internal sentence alignment only; no SRT/VTT generated or delivered.'};write(meta,m)
        if ERROR.exists():ERROR.unlink()
    with urllib.request.urlopen(m['alignment_url'],timeout=45) as response:alignment=json.load(response)
    m['alignment']=alignment;m.pop('alignment_url',None);write(meta,m)
    print(json.dumps({'batch':b['id'],'cues':[c['id'] for c in b['cues']],'alignment_type':type(alignment).__name__,'audio_bytes':wav.stat().st_size},ensure_ascii=False),flush=True)
    if args.one:break
