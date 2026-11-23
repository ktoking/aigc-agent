from pathlib import Path
import json,subprocess,concurrent.futures
P=Path(__file__).resolve().parents[1];R=P.parents[1];D=json.loads((P/'timeline.json').read_text());V=R/'output/photoreal-v1/you-are-safe-photoreal-v1.mp4';Q=P/'qa';F=Q/'frames';F.mkdir(exist_ok=True)
def work(pair):
 i,s=pair;mid=(s['start_frame']+s['end_frame_exclusive'])/60
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(mid),'-i',str(V),'-frames:v','1',str(F/f'frame-{i:02d}.png')],check=True)
 n=s['end_frame_exclusive']-s['start_frame'];clip=P/'clips'/(s['id']+'.mp4')
 vf=f"select='eq(n,20)+eq(n,{n-8})',scale=320:180"
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(clip),'-vf',vf,'-fps_mode','passthrough','-pix_fmt','gray','-f','rawvideo','-'])
 size=320*180;assert len(raw)==2*size,(s['id'],len(raw));a,b=raw[:size],raw[size:];mean=sum(abs(x-y) for x,y in zip(a,b))/size
 return {'id':s['id'],'sample_frames':[20,n-8],'gray_pixel_mean_abs_diff':mean,'note':'像素差只支持静帧稳定性检查，不单独证明几何无抖动'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(work,enumerate(D['shots'],1)))
subprocess.run(['ffmpeg','-v','error','-y','-framerate','1','-i',str(F/'frame-%02d.png'),'-vf','scale=480:270,tile=5x4','-frames:v','1',str(Q/'encoded-overview.png')],check=True)
(Q/'stability-samples.json').write_text(json.dumps({'shots':results,'max_mean_difference':max(x['gray_pixel_mean_abs_diff'] for x in results)},ensure_ascii=False,indent=2)+'\n')
print('encoded overview complete; max gray pixel mean difference',max(x['gray_pixel_mean_abs_diff'] for x in results))
