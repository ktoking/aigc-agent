from pathlib import Path
import json,subprocess,concurrent.futures
P=Path(__file__).resolve().parents[1];R=P.parents[1];D=json.loads((P/'timeline.json').read_text());V=R/'output/photoreal-6min-v1/you-are-safe-photoreal-6min-v1.mp4';Q=P/'qa';F=Q/'frames';F.mkdir(exist_ok=True)
def work(pair):
 i,s=pair;mid=(s['start_frame']+s['end_frame_exclusive'])/60
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(mid),'-i',str(V),'-frames:v','1','-vf','scale=480:270',str(F/f'frame-{i:03d}.png')],check=True)
 return s['id']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(work,enumerate(D['shots'],1)))
for seg in range(12):
 subprocess.run(['ffmpeg','-v','error','-y','-start_number',str(seg*8+1),'-i',str(F/'frame-%03d.png'),'-vf','tile=4x2','-frames:v','1',str(Q/f'segment-{seg+1:02d}.png')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','1','-i',str(Q/'segment-%02d.png'),'-vf','scale=960:270,tile=2x6','-frames:v','1',str(Q/'film-overview.png')],check=True)
print('96 encoded frames, 12 chapter grids and film overview ready')
