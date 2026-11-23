from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=R/'output/photoreal-6min-v1';D=json.loads((P/'timeline.json').read_text())
def wrap(text):
 if len(text)<=24:return text
 candidates=[i+1 for i,c in enumerate(text) if c in '，。；！？' and 6<=i+1<=len(text)-6]
 cut=min(candidates,key=lambda i:abs(i-len(text)/2)) if candidates else len(text)//2
 return text[:cut]+'\n'+text[cut:]
def stamp(f,sep=','):
 ms=round(f/D['fps']*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'
srt='\n\n'.join(f"{i}\n{stamp(c['start_frame'])} --> {stamp(c['end_frame_exclusive'])}\n{wrap(c['text'])}" for i,c in enumerate(D['cues'],1))+'\n'
vtt='WEBVTT\n\n'+'\n\n'.join(f"{stamp(c['start_frame'],'.')} --> {stamp(c['end_frame_exclusive'],'.')}\n{wrap(c['text'])}" for c in D['cues'])+'\n'
for folder in [P,O]:
 (folder/'you-are-safe.zh-CN.srt').write_text(srt,encoding='utf-8');(folder/'you-are-safe.zh-CN.vtt').write_text(vtt,encoding='utf-8')
print('subtitle line breaks updated, text and timings unchanged')
