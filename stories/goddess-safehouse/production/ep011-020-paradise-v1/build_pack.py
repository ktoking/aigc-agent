from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent
R=P.parents[1]
data=json.loads((P/'episode-source.json').read_text())
cast=json.loads((P/'voice-cast.json').read_text())['characters']
allc=[];combined=[]
for ep in data:
    eid=ep['episode'];D=R/'episodes'/eid
    for sub in ['text-cues','audio','audio-speed1p3','frames','image-prompts','output']: (D/sub).mkdir(parents=True,exist_ok=True)
    cues=[];novel=[];readable=[]
    for i,(role,txt,scene,people,events) in enumerate(ep['cues'],1):
        cid=f'{eid}-C{i:02d}'
        (D/'text-cues'/f'{cid}.txt').write_text(txt+'\n')
        c={'cue_id':cid,'episode':eid,'speaker':role,'speaker_name':cast[role]['name'],'voice_id':cast[role]['voice_id'],'pitch':cast[role]['pitch'],'source_text':txt,'tts_text':txt,'scene':scene,'character_ids':people,'events':events,'text_path':str((D/'text-cues'/f'{cid}.txt').relative_to(R)),'status':'PENDING','direction':cast[role]['direction']}
        # 与实际空间对应：本批只有两段电话、最后一个无线电来声需要轻度电话空间效果。
        c['sound_effect']='lofi_telephone' if (role=='GU' or (role=='QIAO' and eid=='EP014')) else 'none'
        cues.append(c);allc.append(c)
        novel.append(txt if role=='N' else '“'+txt+'”')
        readable.append(f'**{cast[role]["name"]}**\n\n{txt}')
    title=f'{eid}《{ep["title"]}》'
    (D/'novel.md').write_text('# '+title+'\n\n'+'\n\n'.join(novel)+'\n')
    (D/'narration.md').write_text('# '+title+' · 分角色朗读稿\n\n角色名只用于路由，不朗读。\n\n'+'\n\n'.join(readable)+'\n')
    (D/'narration.txt').write_text('\n\n'.join(c['source_text'] for c in cues)+'\n')
    (D/'cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n')
    (D/'qa-checklist.md').write_text(f'# {title} 检查\n\n稿件版本：paradise-v1。正文/旁白/对白语义审读见production/ep011-020-paradise-v1/script-review.md，L01—L06、S01—S06均PASS。\n\n音频、图像、成片验证独立记录，当前尚未生成；人工完整听看NOT_RUN。\n')
    combined.append('# '+title+'\n\n'+'\n\n'.join(readable))
(P/'全部剧本_11-20集_多角色配音稿.md').write_text('\n\n---\n\n'.join(combined)+'\n')
(P/'voice-queue.json').write_text(json.dumps(allc,ensure_ascii=False,indent=2)+'\n')
manifest={'version':'paradise-v1','episodes':10,'cues':len(allc),'characters':{k:sum(len(c['source_text']) for c in allc if c['speaker']==k) for k in cast},'episode_files':[{ 'episode':e['episode'],'title':e['title'],'sha256':hashlib.sha256((R/'episodes'/e['episode']/'narration.txt').read_bytes()).hexdigest(),'cues':len(e['cues']),'characters':sum(len(c[1]) for c in e['cues'])} for e in data]}
(P/'script-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(P/'status.json').write_text(json.dumps({'version':'paradise-v1','scripts_complete':10,'scripts_review':'PASS_TEXT_ONLY','voice_complete':0,'voice_total':len(allc),'images_complete':0,'images_total':None,'timing':'WAITING_MEASURED_AUDIO','videos':'NOT_REQUESTED_THIS_TURN','human_full_listening':'NOT_RUN'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
