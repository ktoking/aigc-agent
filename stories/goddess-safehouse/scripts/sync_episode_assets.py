from pathlib import Path
import json,sys,hashlib,argparse
a=argparse.ArgumentParser();a.add_argument('episode');a.add_argument('--variant',choices=['speed1p3']);args=a.parse_args();suffix=f'-{args.variant}' if args.variant else ''
R=Path(__file__).resolve().parents[1];eid=args.episode;p=R/'production/user-script-v2/image-queue.json';q=json.loads(p.read_text());byid={s['shot_id']:s for s in q};tp=R/'episodes'/eid/f'timeline{suffix}.json';t=json.loads(tp.read_text());missing=[]
for s in t['shots']:
 a=byid[s['shot_id']]
 if not a.get('image_path'):missing.append(s['shot_id']);continue
 for k in ['image_path','image_sha256','native_dimensions','generation_status','reference_paths']:s[k]=a.get(k)
 assert hashlib.sha256((R/s['image_path']).read_bytes()).hexdigest()==s['image_sha256']
assert not missing,missing
assert len({s['image_sha256'] for s in t['shots']})==len(t['shots'])
tp.write_text(json.dumps(t,ensure_ascii=False,indent=2))
rows=['# '+eid+' 实测音频镜头表','','配音固定Chinese_worker_male；原文未改。音频范围与换图共用30fps整数帧时间线。镜头内画面固定，3帧外部cue空档只计一次，叠化只在这些空档内发生。','','|镜头|帧区间（尾帧不含）|秒|原cue|事件|图像|','|---|---|---:|---|---|---|']
for s in t['shots']:rows.append(f"|{s['shot_id']}|{s['start_frame']}—{s['end_frame']}|{s['display_seconds']:.2f}|{','.join(s['cue_ids'])}|{s['unique_event']}|{s['image_path']}|")
(R/'episodes'/eid/f'storyboard{suffix}.md').write_text('\n'.join(rows)+'\n')
if args.variant:
 active=R/'production/user-script-v2'/f'image-queue{suffix}.json';items=json.loads(active.read_text());selected={s['shot_id']:s for s in t['shots']};items=[selected.get(s['shot_id'],s) for s in items];active.write_text(json.dumps(items,ensure_ascii=False,indent=2))
print(eid,'all',len(t['shots']),'unique image assets bound',t['frames'],'frames')
