from pathlib import Path
import json,shutil,hashlib

P=Path(__file__).resolve().parents[1];R=P.parents[1]
T=json.loads((P/'timeline.json').read_text());jobs={j['id']:j for j in T['jobs']}
old=json.loads((R/'handoff/cloud-codex-20261018-v2/scripts-and-shots.json').read_text())
records=[]
for j in jobs.values():
    corrections=sorted((P/'assets').glob(f"{j['id']}.correction*.json"))
    side=corrections[-1] if corrections else P/'assets'/f"{j['id']}.json"
    record=json.loads(side.read_text())
    assert record and (P/j['path']).exists(),j['id']
    record['sha256']=hashlib.sha256((P/j['path']).read_bytes()).hexdigest()
    records.append(record)
(P/'image-prompts.json').write_text(json.dumps({'provider':'GPT built-in imagegen','items':records},ensure_ascii=False,indent=2)+'\n')
for ep in old['episodes']:
    n=ep['episode'];folder=R/'episodes'/f"EP{n:03d}_{ep['slug']}"/'v5';folder.mkdir(parents=True,exist_ok=True)
    cues=[c for c in T['cues'] if c['episode']==n];start=cues[0]['output_start_frame'];end=cues[-1]['output_end_frame_exclusive']
    shots=[s for s in T['shots'] if s['episode']==n]
    (folder/'overview-storyboard.md').write_text(f"# EP{n:03d} 真人末日电影风v5\n\n时长{(end-start)/30:.3f}秒。原配音与BGM，固定构图，4帧短叠化。灾难初期，地面干燥、环境完整整洁。\n\n|镜头|本集秒数|事件图|\n|---|---|---|\n"+'\n'.join(f"|{s['id']}|{(s['start_frame']-start)/30:.3f}—{(s['end_frame_exclusive']-start)/30:.3f}|{s['asset']}|" for s in shots)+'\n')
    for segment in range(1,5):
        cc=[c for c in cues if c['segment']==segment];a=cc[0]['output_start_frame'];b=cc[-1]['output_end_frame_exclusive']
        selected=[s for s in shots if s['start_frame']<b and s['end_frame_exclusive']>a]
        d=folder/f'segment_{segment:02d}_{(a-start)/30:.2f}-{(b-start)/30:.2f}s';(d/'frames').mkdir(parents=True,exist_ok=True);(d/'output').mkdir(exist_ok=True)
        first,last=jobs[selected[0]['asset']],jobs[selected[-1]['asset']]
        shutil.copy2(P/first['path'],d/'frames/first-frame.png');shutil.copy2(P/last['path'],d/'frames/last-frame.png')
        rows='\n'.join(f"- {s['id']}：合集{s['start_frame']/30:.3f}—{s['end_frame_exclusive']/30:.3f}s；{s['asset']}；{jobs[s['asset']]['description']}" for s in selected)
        (d/'storyboard.md').write_text('# 分段故事板\n\n'+rows+'\n')
        (d/'first-frame.md').write_text('# 首帧\n\n采用frames/first-frame.png，对应'+first['id']+'。完整生图提示词见production/v5/image-prompts.json。\n')
        (d/'last-frame.md').write_text('# 尾帧\n\n采用frames/last-frame.png，对应'+last['id']+'。下一画面按合集时间线4帧短叠化，不增加秒数。\n')
        body=f"# 本段本地视频合成指令\n\n16:9，1920×1080，30fps，{(b-a)/30:.3f}秒。真人末日电影静帧，正常完整超市、干燥地面。人物、场景、门边界按各事件图锁定。首尾帧见frames/。固定位置与缩放，不摇晃、不zoompan、不逐句重置。相邻事件图4帧短叠化，声音与字幕不重影；无片头片尾等待。读取production/v5/timeline.json的同一帧时间线，音轨复用v4完整混音。\n\n镜头：\n{rows}\n\n台词：\n"+'\n'.join(c['text'] for c in cc)+'\n'
        (d/'prompt.md').write_text(body);(d/'director-promt.txt').write_text(body)
        (d/'api-request.md').write_text('# 生成与合成记录\n\n图像：GPT内置imagegen，来源与提示词见production/v5/assets/*.json。视频：本地FFmpeg固定帧合成，不调用付费视频API、不生成肢体动画、不新生成语音。合成脚本：production/v5/scripts/render.py。参数与实际完成状态见合集delivery-manifest.json。\n')
print('Packaged 8 episode storyboards and 32 segment source folders')
