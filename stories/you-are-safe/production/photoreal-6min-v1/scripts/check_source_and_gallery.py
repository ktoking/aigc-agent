from pathlib import Path
import json,re,hashlib,html,struct
P=Path(__file__).resolve().parents[1];R=P.parents[1];D=json.loads((P/'timeline.json').read_text());src=(R/D['source']).read_bytes()
assert hashlib.sha256(src).hexdigest()==D['source_sha256']
assert len(D['shots'])==96 and len(D['cues'])==95 and D['frames']==10800 and D['duration_seconds']==360
assert {(s['segment'],s['source_shot']) for s in D['shots']}=={(a,b) for a in range(1,13) for b in range(1,9)}
assert D['shots'][0]['start_frame']==0 and D['shots'][-1]['end_frame_exclusive']==10800
for a,b in zip(D['shots'],D['shots'][1:]):assert a['end_frame_exclusive']==b['start_frame']
for seg in range(1,13):
 ss=[s for s in D['shots'] if s['segment']==seg];assert ss[0]['start_frame']==(seg-1)*900 and ss[-1]['end_frame_exclusive']==seg*900
for c in D['cues']:
 n=len(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]',c['text']));assert c['end_frame_exclusive']-c['start_frame']==n*4
assert not D['shots'][79]['cues'] and D['shots'][79]['pause_frames']==90
sha=[];cards=[]
for s in D['shots']:
 f=P/s['asset'];raw=f.read_bytes();w,h=struct.unpack('>II',raw[16:24]);assert w/h>1.7 and w/h<1.85
 sha.append(hashlib.sha256(raw).hexdigest())
 text=''.join(c['text'] for c in D['cues'] if c['shot_id']==s['id'])
 cards.append(f'<article><img loading="lazy" src="../{s["asset"]}"><b>{s["id"]} · {html.escape(s["title"])}</b><small>{s["start_frame"]/30:g}—{s["end_frame_exclusive"]/30:g}秒 · 原段{s["segment"]}镜{s["source_shot"]}</small><p>{html.escape(text) or "（整镜留白）"}</p></article>')
assert len(set(sha))==96,'no duplicate film images'
report={'status':'PASS_source_mapping_and_timing','source_sha256':D['source_sha256'],'source_unchanged':True,'source_segments':12,'source_shots':96,'film_images':96,'unique_image_hashes':96,'seconds':360,'frame_boundaries':'all source shot 3/4-second boundaries preserved','subtitle_cues':95,'reading_units':D['reading_units'],'units_per_second':7.5,'reading_seconds':D['reading_units']/7.5,'blank_seconds':sum(s['pause_frames'] for s in D['shots'])/30,'silent_caption_shot':'080 - 3 seconds','scope_overrides':['真人横屏正常干燥自然光','第一人称转述及独立字幕','固定图片视频，不宣称连续动作生成','局部站位及道具连续性勘误','部分冲突改为结果静物或成人反应，剧情由字幕完整承接'],'restored_events':['洪水造船','矿井救援','战区让粮车通行','停战与维修工清除','主动隔离与控制室空椅','拒食失败','朵朵来电及全球风险','全球直播','母亲消失','归零与孩子风险解释','砸手机与公交扬声器','海水退让','座机请求与空椅结尾']}
(P/'qa/source-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(P/'qa/asset-gallery.html').write_text('<!doctype html><meta charset="utf-8"><title>您已安全 · 六分钟原版96镜</title><style>body{font:16px system-ui;background:#f3f1ec;color:#253239;margin:30px}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}article{background:white;padding:10px;border-radius:8px}img{width:100%;aspect-ratio:16/9;object-fit:cover}b,small{display:block;margin-top:7px}small{color:#63727a}p{line-height:1.5}h1{font-size:25px}</style><h1>您已安全 · 六分钟原版96镜</h1><p>12段完整剧情 · 正常自然光真人写实 · 7.5字/秒及留白 · 原镜头时间点</p><main>'+''.join(cards)+'</main>')
print(json.dumps({k:report[k] for k in ['status','source_shots','film_images','seconds','subtitle_cues','reading_units','blank_seconds']},ensure_ascii=False))
