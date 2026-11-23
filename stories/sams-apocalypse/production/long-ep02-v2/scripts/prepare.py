from pathlib import Path
import json,re,shutil
P=Path(__file__).resolve().parents[1];V1=P.parent/'long-ep02-v1'
old=json.loads((V1/'project.json').read_text());rows=json.loads((V1/'storyboard.json').read_text())
presets={}
for sid in range(1,73):
    if sid<=3 or sid==7:preset='suspense'
    elif sid in [35,36,37,38,39,40,41,49,50,51,69,70,71]:preset='fear'
    elif sid in [8,9,10,11,12,13,29,42,57,58,59,60,61,62]:preset='resolve'
    elif sid in [30,56,63,64,65,66,67,72]:preset='healing'
    elif sid==68:preset='reveal'
    elif sid in list(range(4,7))+list(range(15,24))+list(range(31,35))+[52,53,54,55]:preset='documentary'
    else:preset='natural'
    presets[sid]=preset
breaths={7:'(inhale)',40:'(gasps)',56:'(exhale)',69:'(inhale)',72:'(exhale)'}
cues=[];seen=set()
for ep in old['episodes']:
    for c in ep['cues']:
        sid=int(c['asset'][1:]);source=c['text'];tag=breaths.get(sid,'') if sid not in seen else ''
        seen.add(sid);tts=source
        # Sparse performance tags are kept separate from the original words and captions.
        if tag:tts=tag+tts
        cue=dict(id=f'c{len(cues)+1:03d}',index=len(cues)+1,old_shot=sid,chapter=ep['title'],source_text=source,tts_text=tts,preset=presets[sid],direction='克制讲述，紧凑清晰；危险用恐惧；末段轻声收束，原文悬念不改',units=sum(x.isalnum() for x in source),breath_seconds=.2 if tag else 0,model='speech-2.8-turbo',voice_id='Chinese_calm_streamer_nv1',api_speed=1.85)
        assert re.sub(r'\([^)]*\)|<#.*?#>','',tts)==source
        (P/'audio'/(cue['id']+'.txt')).write_text(tts)
        cues.append(cue)
(P/'voice-plan.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n')
for name in ['male-neutral.png','female-neutral.png','outsiders-identity.png']:
    shutil.copy2(V1/'references'/name,P/'references'/name)
shutil.copy2(V1/'assets/s23-v2.png',P/'references/hatch.png')
shutil.copy2(V1/'script.md',P/'script.md');shutil.copy2(V1/'narration.txt',P/'narration.txt')
print(dict(cues=len(cues),units=sum(c['units'] for c in cues),breaths=sum(bool(c['breath_seconds']) for c in cues)))
