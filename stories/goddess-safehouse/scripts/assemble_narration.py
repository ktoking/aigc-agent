from pathlib import Path
import json,subprocess,wave,array,hashlib
R=Path(__file__).resolve().parents[1];SR=48000;FPS=30
results=[]
for p in sorted((R/'episodes').glob('EP*/timeline.json')):
 d=p.parent;t=json.loads(p.read_text());n=t['frames']*(SR//FPS);pcm=array.array('h',[0])*n
 for c in t['cues']:
  raw=subprocess.run(['ffmpeg','-v','error','-i',str(R/c['audio_path']),'-ac','1','-ar',str(SR),'-f','s16le','-'],capture_output=True,check=True).stdout
  a=array.array('h');a.frombytes(raw);start=c['start_frame']*(SR//FPS);allocated=(c['end_frame']-c['start_frame'])*(SR//FPS)
  assert len(a)<=allocated,(c['cue_id'],len(a),allocated)
  assert start+len(a)<=n
  pcm[start:start+len(a)]=a
 work=d/'render';work.mkdir(exist_ok=True);out=work/'narration.wav'
 with wave.open(str(out),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
 o=d/'output';o.mkdir(exist_ok=True);mp3=o/f'{d.name}_Chinese_worker_male.mp3'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-codec:a','libmp3lame','-b:a','128k',str(mp3)],check=True)
 peak=max(abs(i) for i in pcm);clipped=sum(abs(i)>=32767 for i in pcm)
 r={'episode':d.name,'master_wave':str(out.relative_to(R)),'standalone_mp3':str(mp3.relative_to(R)),'frames':t['frames'],'duration_seconds':t['frames']/FPS,'sample_count':len(pcm),'peak_pcm16':peak,'clipped_samples':clipped,'all_cue_tails_fit':True,'voice_id':'Chinese_worker_male','human_listening':'NOT_RUN','sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
 assert clipped==0
 (o/'audio-manifest.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));results.append(r);print(d.name,'audio assembled',r['duration_seconds'],flush=True)
(R/'production/user-script-v2/audio-master-summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
