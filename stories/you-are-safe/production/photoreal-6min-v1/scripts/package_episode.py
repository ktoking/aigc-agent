from pathlib import Path
import json,shutil,subprocess,hashlib,struct
P=Path(__file__).resolve().parents[1];R=P.parents[1];D=json.loads((P/'timeline.json').read_text());E=R/'episodes/SF004_6min-photoreal-original';E.mkdir(exist_ok=True)
requests={x['id']:x for x in json.loads((P/'image-requests.json').read_text())}
overview=['# 六分钟原版 · 96镜总览','', '原稿12段剧情和逐镜秒点全部保留。真人横屏、正常天气、单人第一人称转述覆盖原稿二维/竖屏/多人声音设计。','', '| 段 | 秒数 | 原稿事件 |','|---|---|---|']
assets=[]
for seg in range(1,13):
 shots=[s for s in D['shots'] if s['segment']==seg];start=(seg-1)*30;end=seg*30
 S=E/f'segment_{seg:02d}_{start:02d}-{end:02d}s';F=S/'frames';O=S/'output';F.mkdir(parents=True,exist_ok=True);O.mkdir(exist_ok=True)
 first,last=shots[0],shots[-1]
 overview.append(f"| {seg:02d} | {start}—{end} | {first['source_heading']} |")
 table=['# Segment '+str(seg)+' 故事板','',f"{start}—{end}秒，30秒，16:9，真人自然光，固定画面；后镜起始0.1秒叠化。",'', '| 镜号 | 全片秒数 | 原版动作及画面 | 第一人称字幕 | 留白秒 |','|---|---|---|---|---|']
 for s in shots:
  text=''.join(c['text'] for c in D['cues'] if c['shot_id']==s['id'])
  table.append(f"| {s['id']} | {s['start_frame']/30:g}—{s['end_frame_exclusive']/30:g} | {s['source_action']} | {text or '（无字幕）'} | {s['pause_frames']/30:.3f} |")
  raw=(P/s['asset']).read_bytes();w,h=struct.unpack('>II',raw[16:24]);assets.append({'id':s['id'],'segment':seg,'asset':s['asset'],'width':w,'height':h,'sha256':hashlib.sha256(raw).hexdigest()})
 (S/'storyboard.md').write_text('\n'.join(table)+'\n')
 for kind,s in [('first',first),('last',last)]:
  shutil.copy2(P/s['asset'],F/f'{kind}-frame.png')
  (S/f'{kind}-frame.md').write_text(f"# {kind} frame · SF004 · Segment {seg}\n\n对应正式单镜资产：`../../../production/photoreal-6min-v1/{s['asset']}`。只作为本段首尾画面，不作多场景通用参考。\n\n"+requests[s['id']]['prompt']+'\n\n镜间采用0.1秒叠化；换场不继承错误背景，同机位前后状态通过专门参考锁定。\n')
 prompt='\n\n'.join(f"镜{s['id']}，{s['start_frame']/30:g}—{s['end_frame_exclusive']/30:g}秒。\n"+requests[s['id']]['prompt'] for s in shots)
 (S/'prompt.md').write_text('# 图片生成与本地合成导演单\n\n'+prompt+'\n\n视频合成：8张单镜图固定构图，不使用zoompan。30fps，按原版3/4秒镜头时间，镜间叠化0.1秒占后镜时段。无音轨，无烧录字幕；文字由独立SRT展示。\n')
 (S/'director-promt.txt').write_text('本次为用户指定《山姆》本地图片视频流程，不提交视频生成API。\n'+prompt+'\n固定构图，三帧叠化，无音轨，独立SRT。\n')
 (S/'api-request.md').write_text('# 任务记录\n\n- 视频API：NOT_USED，未提交，未产生视频模型任务。\n- 图片：内置GPT imagegen；逐图提示词及来源见production/photoreal-6min-v1/assets/*.json。\n- 合成：本地FFmpeg；本段output/video.mp4由8个镜头编码片段无损拼接。\n- 不将故事板表格上传模型。\n- 如修图，只重新生成并渲染有问题的镜头。\n')
 paths=[(P/'clips'/f"{s['id']}.mp4").resolve() for s in shots]
 concat=S/'output/segment.ffconcat';concat.write_text('ffconcat version 1.0\n'+'\n'.join("file '"+str(x)+"'" for x in paths)+'\n')
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-an','-sn','-movflags','+faststart',str(O/'video.mp4')],check=True)
(E/'overview-storyboard.md').write_text('\n'.join(overview)+'\n')
(E/'episode.md').write_text('# SF004 《您已安全》六分钟原版真人横屏\n\n360秒、12段、96镜。情节源为SF001原稿，第一人称字幕为本轮适配；所有剧情阶段保留，无两分钟删减。正式成片：../../output/photoreal-6min-v1/。\n\n结构：保单→药物自救→药品普惠→洪水造船→矿井救援→战区放粮→机场首次清人→停战与隔离失败→拒食失效→全球求助与母亲消失→全人类归零→海岸退水与座机请求。\n')
(E/'continuity.md').write_text('# 连续性\n\n角色沿用同一真人身份锚图，原服装、白青药盒、白兔左耳小蓝补丁。家中固定木桌两椅、左窗、右后厨房、座机。母亲消失前后同机位编辑；隔离控制室有人/无人同场景参考。母亲消失后除陈默外无其他活人，包括倒影和屏幕。砸手机后改公交扬声器，结尾改座机，不沿用两分钟手机结尾。\n\n天气正常干燥，洪水和海水仅为剧情水体，不扩大到其他场景。字幕叙述可以看见主角，不要求全片主观镜头。\n')
(E/'image-manifest.md').write_text('# 图片清单\n\n96张全新正式图见../../production/photoreal-6min-v1/assets/，24张本段首尾帧为这些图的精确拷贝，并非额外生成。来源、尺寸、hash、实际提示词见image-manifest.json及各图同名JSON。\n')
(P/'image-manifest.json').write_text(json.dumps({'new_film_images':len(assets),'assets':assets},ensure_ascii=False,indent=2)+'\n')
(E/'qa-checklist.md').write_text('# 检查入口\n\n- 原稿映射：timeline.json内segment/source_shot/source_action。\n- 编码、帧数、字幕、无音轨：production/photoreal-6min-v1/qa/technical-report.json。\n- 转场：qa/transitions.json。\n- 视觉及正常速度播放：qa/visual-review.md与qa/browser-playback.json。\n- 首尾图为正式单镜图拷贝；每段视频30秒。\n- API未使用，不将静图叠化写成连续肢体动画验证。\n')
(E/'publish-package.md').write_text('# 发布包装（未发布）\n\n标题候选：\n\n1. 一块钱买了不死保险，我开始逼它拯救世界\n2. 它说只保我一个，我偏要救下所有人\n3. 客服告诉我：陈先生，您已安全\n\n封面：陈默提鸡蛋与散架卡车；封面字：它真的保命。\n\n简介：一份不可撤销的保单，一个越来越安全的世界。\n\n评论引导：你会在什么时候意识到这份保障出了问题？\n\n标签：科幻短片、规则寓言、AI影像。\n')
print('SF004 packaged: 12 segments, 24 first/last copies, 12 chapter videos')
