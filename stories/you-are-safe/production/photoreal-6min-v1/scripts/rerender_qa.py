from pathlib import Path
import json,subprocess,concurrent.futures
import render_film as film
P=Path(__file__).resolve().parents[1];R=P.parents[1]
ids=['006','008','014','018','020','021','023','026','027','028','031','032','034','035','036','037','045','047','053','054','055','056','058','065','066','070','074','088','090','092']
# 镜头开头使用前镜图片，修图后必须同时更新下一镜的三帧叠化。
indices=sorted({i for ident in ids for i in [int(ident)-1,int(ident)] if i<96})
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(film.render,indices):print('QA rerendered',result['id'],flush=True)
video=R/'output/photoreal-6min-v1/you-are-safe-photoreal-6min-v1.mp4'
film.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',P/'clips.ffconcat','-map','0:v:0','-c:v','copy','-an','-sn','-dn','-movflags','+faststart',video],P/'logs/qa-concat.log')
m=json.loads((P/'render-manifest.json').read_text());m.update(qa_revised_images=ids,qa_rerendered_clips=[f'{i+1:03d}' for i in indices],transition_frames=3,transition_seconds=.1)
(P/'render-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('QA export complete: 10800 frames, 360 seconds')
