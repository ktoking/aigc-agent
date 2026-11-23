from pathlib import Path
import json,collections
P=Path(__file__).resolve().parents[1]
cues=json.loads((P/'voice-plan.json').read_text());old={int(r['id']):r for r in json.loads((P.parent/'long-ep02-v1/storyboard.json').read_text())}
cursor=0
for c in cues:
    c['planning_start']=cursor;c['planning_end']=cursor+c['units']*4+round(c['breath_seconds']*30)
    cursor=c['planning_end']+3
total=cursor-3;images=[]
for i in range(120):
    a=round(i*total/120);b=round((i+1)*total/120)
    group=[c for c in cues if min(b,c['planning_end'])-max(a,c['planning_start'])>=12]
    if not group:group=[min(cues,key=lambda c:abs(c['planning_start']-(a+b)/2))]
    weights=collections.Counter()
    for c in group:weights[c['old_shot']]+=max(0,min(b,c['planning_end'])-max(a,c['planning_start']))
    sid=weights.most_common(1)[0][0];row=old[sid]
    light='停电深夜，窗外漆黑，卖场顶灯全关，头灯和低亮工作灯照亮主体' if sid<=6 or sid in [30,31,32] or 63<=sid<=67 else '天亮前暗蓝清晨，顶灯全关，头灯/手电与微弱工作灯照亮主体' if sid>=68 else '天刚亮的柔和冷色天光' if sid==7 else '傍晚金橙色余晖，外面逐渐变暗' if 57<=sid<=62 else '正常白昼，室内主要靠高窗自然天光、局部便携工作灯，卖场顶灯关闭'
    roles='MF' if sid==51 else row['roles']
    images.append(dict(id=f'p{i+1:03d}',chapter=group[0]['chapter'],cue_ids=[c['id'] for c in group],text=''.join(c['source_text'] for c in group),old_shot=sid,roles=roles,scene_hint=row['scene'],light=light,planning_start_frame=a,planning_end_frame=b,planning_seconds=(b-a)/30))
(P/'image-plan.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n')
print(dict(images=len(images),min_seconds=min(x['planning_seconds'] for x in images),max_seconds=max(x['planning_seconds'] for x in images),planning_total_seconds=total/30))
