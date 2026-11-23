from pathlib import Path
import json,hashlib,os,shutil,unicodedata,fcntl
P=Path(__file__).resolve().parent;R=P.parents[1];D=R/'delivery/后10集_世外桃源_剧本图片多角色配音'
q=json.loads((P/'image-queue.json').read_text());src=json.loads((P/'episode-source.json').read_text());manifest=json.loads((P/'script-manifest.json').read_text());aud=json.loads((P/'audio-master-summary.json').read_text())
assert len(aud)==10
assert len(q)==132 and all(s.get('image_path') for s in q),'图片未齐，不得虚报完成'
assert len({s['image_sha256'] for s in q})==len(q),'成片图片重复'
assert all(4<=s['display_seconds']<=6 for s in q)
assert all(s.get('visual_review')=='PASS_MODEL_VISUAL_REVIEW' for s in q),'图片尚未逐镜审读'
for m in manifest['episode_files']:
 p=R/'episodes'/m['episode']/'narration.txt';assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
for sub in ['剧本','分镜','图片','图片总览']: (D/sub).mkdir(parents=True,exist_ok=True)
def copy(f,t):
 t.parent.mkdir(parents=True,exist_ok=True)
 if t.exists():
  if hashlib.sha256(t.read_bytes()).hexdigest()==hashlib.sha256(f.read_bytes()).hexdigest():return
  raise ValueError('交付目录已存在不同文件，保留现有版本：'+str(t))
 try:os.link(f,t)
 except OSError:shutil.copy2(f,t)
for e in src:
 eid=e['episode'];ep=R/'episodes'/eid
 copy(ep/'narration.md',D/'剧本'/f'{eid}_{e["title"]}.md')
 copy(ep/'novel.md',D/'剧本'/f'{eid}_小说正文.md')
 copy(ep/'storyboard.md',D/'分镜'/f'{eid}.md')
 sheet=P/'contacts'/f'{eid}.jpg'
 if sheet.exists():copy(sheet,D/'图片总览'/f'{eid}.jpg')
 timeline=json.loads((ep/'timeline-speed1p3.json').read_text())
 for c in timeline['cues']:
  c['display_text']=' '.join(''.join(' ' if unicodedata.category(ch).startswith('P') else ch for ch in c['source_text']).split())
 (ep/'timeline-speed1p3.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
for s in q:
 f=R/s['image_path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==s['image_sha256']
 copy(f,D/'图片'/s['episode']/f'{s["shot_id"]}.png')
# 通用资产索引保留旧记录，只追加本批图与新身份/空间基准。
index=R/'assets/manifest.json';assets=json.loads(index.read_text());newids={s['shot_id'] for s in q}|{'QIAO-v1','PARADISE-v1','BONE-v1'}
assets=[a for a in assets if a.get('asset_id') not in newids]
for s in q:assets.append({'asset_id':s['shot_id'],'path':s['image_path'],'sha256':s['image_sha256'],'native_dimensions':s['native_dimensions'],'generator':'built-in image_gen','type':'event_image','prompt_path':s['request_path'],'status':'PASS_MODEL_VISUAL_REVIEW','selected_for_production':True})
for aid,kind in [('QIAO-v1','character_baseline'),('PARADISE-v1','scene_baseline'),('BONE-v1','creature_identity_reference')]:
 p=R/'assets/baselines'/f'{aid}.png'
 assets.append({'asset_id':aid,'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'generator':'built-in image_gen','type':kind,'selected_for_production':False,'reference_only':True})
index.write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
copy(P/'全部剧本_11-20集_多角色配音稿.md',D/'全部剧本_11-20集_多角色配音稿.md')
copy(P/'voice-cast.json',D/'固定音色.json')
copy(P/'script-review.md',D/'剧本审读.md')
copy(P/'image-review.md',D/'图片复核.md')
rows=['# 后10集：世外桃源 · 剧本、图片与多角色配音','',f'EP011—EP020，十集正文，95段MiniMax多角色配音，132张独立新图。1.3倍音轨合计{sum(a["duration_seconds"] for a in aud):.3f}秒。','',
'- 剧本：小说正文、分角色朗读稿与合稿。角色名不朗读。','- 声音：陈屿保留Chinese_worker_male；夏凛冷御姐、许知意温柔成熟、乔星野成年元气傲娇、顾南枝温软暖声，voice_id见固定音色.json。','- 图片：每集分目录，全部独立新图，约5秒一张，原生尺寸如交付清单所记；前十集图未重制。','- 房屋：持续安居推动扩建，当前解锁恒温、40㎡耕地、诊疗室、工作区与第五卧室；花园、浴池、训练室等留待后续进度。','- 本轮交付剧本、图片与已配音音轨。完整视频尚未渲染；实际完整人工听看NOT_RUN，模型看图与自动解码不能替代用户审美。','',
'|集|剧本|配音|图片总览|','|---|---|---|---|']
for e,a in zip(src,aud):rows.append(f'|{e["episode"]}|[{e["title"]}](剧本/{e["episode"]}_{e["title"]}.md)|[{a["duration_seconds"]:.2f}秒]({e["episode"]}_多角色_1.3倍.mp3)|[{sum(s["episode"]==e["episode"] for s in q)}张](图片总览/{e["episode"]}.jpg)|')
(D/'README.md').write_text('\n'.join(rows)+'\n')
report={'version':'paradise-v1','script_episodes':10,'voice_cues':95,'voice_decode':'PASS','post_atempo':1.3,'duration_seconds':sum(a['duration_seconds'] for a in aud),'images':len(q),'unique_image_hashes':len({s['image_sha256'] for s in q}),'all_shots_4_6_seconds':True,'model_visual_review':'PASS_MODEL_VISUAL_REVIEW','human_full_listening':'NOT_RUN','user_aesthetic_acceptance':'NOT_RUN','video_render':'NOT_RUN_NOT_REQUESTED_THIS_TURN','episodes':aud,'shots':q,'baseline_images':['assets/baselines/QIAO-v1.png','assets/baselines/PARADISE-v1.png']}
(D/'delivery-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with (P/'.image.lock').open('w') as f:
 fcntl.flock(f,fcntl.LOCK_EX);s=json.loads((P/'status.json').read_text());s.update(scripts_complete=10,voice_complete=95,images_complete=132,images_total=132,timing='MEASURED_AUDIO_1P3_LOCKED',image_visual_review='PASS_MODEL_VISUAL_REVIEW',delivery_path=str(D.resolve()),production_status='REQUESTED_SCRIPT_IMAGE_AUDIO_DELIVERABLES_COMPLETE');(P/'status.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'delivery':str(D.resolve()),'scripts':10,'voice_cues':95,'images':132,'seconds':report['duration_seconds']},ensure_ascii=False))
