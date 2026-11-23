from pathlib import Path
import subprocess,json,numpy as np
P=Path(__file__).resolve().parent;O=P.parent.parent/'episodes/EP002_hold-yourself/output';F=O/'hold-yourself_1920x1080_60s.mp4'
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-t','60','-vn','-ac','1','-ar','8000','-f','f32le','pipe:1']),dtype=np.float32)
a=pcm(P/'assets/bgm.wav');b=pcm(F);n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.98
q=json.load(open(O/'delivery-qa.json'));q['audio']['full_60s_waveform_correlation']=corr;q['audio']['comparison']='same-time 8kHz mono decoded PCM';q['beat_sync']={'canonical':'audiomap.json','bpm_estimate':112.3,'render_quantization_max_ms':8.334,'scope':'main entrances and scene transitions mapped to measured anchors; no subjective listening certification'};(O/'delivery-qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2));print(corr)
