from pathlib import Path
import json,time
from faster_whisper import WhisperModel
from faster_whisper.vad import VadOptions,get_speech_timestamps
import wave
import numpy as np
P=Path(__file__).resolve().parents[1]
with wave.open(str(P/'analysis/source.wav'),'rb') as f:
    assert f.getframerate()==16000 and f.getnchannels()==1
    audio=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.float32)/32768
t=time.time()
vad=get_speech_timestamps(audio,VadOptions(threshold=.5,min_speech_duration_ms=100,min_silence_duration_ms=140,speech_pad_ms=0),sampling_rate=16000)
(P/'analysis/vad.json').write_text(json.dumps([{'start':x['start']/16000,'end':x['end']/16000} for x in vad],indent=2)+'\n')
print('VAD',len(vad),'seconds',time.time()-t,flush=True)
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,num_workers=1,local_files_only=True)
segments,info=model.transcribe(audio,language='zh',beam_size=3,word_timestamps=True,vad_filter=True,vad_parameters={'min_silence_duration_ms':200},condition_on_previous_text=False,initial_prompt='丧尸爆发后，我住进了整座山姆。店长、许棠、冷链、备用发电机。')
result=[]
for seg in segments:
 d={'start':seg.start,'end':seg.end,'text':seg.text,'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in seg.words]}
 result.append(d);print(f'{seg.start:.2f}–{seg.end:.2f} {seg.text}',flush=True)
 (P/'analysis/asr.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('COMPLETE',time.time()-t,flush=True)
