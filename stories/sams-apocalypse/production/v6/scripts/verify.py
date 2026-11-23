from pathlib import Path
import json,re,subprocess,math
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[1];R=P.parents[1];O=R/'output/EP001-EP008-v6';Q=P/'qa';Q.mkdir(exist_ok=True)
T=json.loads((P/'timeline.json').read_text());NAME='EP001-EP008_sams_apocalypse_v6_silent';VIDEO=O/f'{NAME}.mp4'
def output(args):return subprocess.check_output(list(map(str,args)))

def main():
    probe=json.loads(output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',VIDEO]));(Q/'ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n')
    assert len(probe['streams'])==1 and probe['streams'][0]['codec_type']=='video'
    v=probe['streams'][0];assert [v['width'],v['height']]==[1920,1080] and v['r_frame_rate']=='30/1' and int(v['nb_read_frames'])==7730
    assert all(b['start_frame']-a['end_frame_exclusive']==3 for a,b in zip(T['cues'],T['cues'][1:]))
    assert all(c['end_frame_exclusive']-c['start_frame']==c['source_end_frame_exclusive']-c['source_start_frame'] for c in T['cues'])
    old=json.loads((R/'production/v5/timeline.json').read_text())
    assert [c['text'] for c in T['cues']]==[c['text'] for c in old['cues']]
    srt=(O/f'{NAME}.zh-CN.srt').read_text();blocks=srt.strip().split('\n\n');assert len(blocks)==130
    def milliseconds(s):
        h,m,sec,ms=map(int,re.split('[:,]',s));return ((h*60+m)*60+sec)*1000+ms
    parsed=[]
    for block,c in zip(blocks,T['cues']):
        lines=block.splitlines();a,b=lines[1].split(' --> ');assert '\n'.join(lines[2:])==c['text'];parsed.append((milliseconds(a),milliseconds(b)))
    assert all(b[0]-a[1]==100 for a,b in zip(parsed,parsed[1:]))
    assert parsed[0][0]==0 and abs(parsed[-1][1]-T['frames']*1000/30)<1
    # Full decode, with actual per-frame stability and dissolve-weight checks.
    raw=output(['ffmpeg','-v','error','-i',VIDEO,'-an','-vf','scale=96:54','-pix_fmt','gray','-f','rawvideo','-'])
    frames=np.frombuffer(raw,np.uint8).reshape(-1,54,96).astype(np.float32);assert len(frames)==7730
    changes=np.mean(np.abs(frames[1:]-frames[:-1]),axis=(1,2));mask=np.ones(len(changes),bool)
    transition_errors=[]
    for t in T['transitions']:
        a,b=t['start_frame'],t['end_frame_exclusive'];assert b-a==3
        assert any(c['end_frame_exclusive']==a and c['gap_after_frames']==3 for c in T['cues'])
        before,after=frames[a-1],frames[b]
        for k in range(3):
            expected=before*(1-(k+1)/3)+after*((k+1)/3)
            transition_errors.append(float(np.mean(np.abs(frames[a+k]-expected))))
        mask[max(0,a-2):min(len(mask),b+2)]=False
    assert max(transition_errors)<2.5,max(transition_errors)
    assert float(changes[mask].max())<1.0
    assert float(frames.mean(axis=(1,2)).min())>2
    # Sample actual encoded frames across every visual event, without drawing captions.
    mids=[];last=None
    for c in T['cues']:
        if c['asset']!=last:mids.append({'frame':(c['start_frame']+c['end_frame_exclusive'])//2,'asset':c['asset']});last=c['asset']
    assert len(mids)==69
    select='+'.join(f"eq(n\\,{x['frame']})" for x in mids)
    data=output(['ffmpeg','-v','error','-i',VIDEO,'-vf',f'select={select},scale=480:270','-fps_mode','vfr','-pix_fmt','rgb24','-f','rawvideo','-'])
    pics=np.frombuffer(data,np.uint8).reshape(-1,270,480,3);assert len(pics)==69
    for page in range(math.ceil(len(pics)/12)):
        canvas=Image.new('RGB',(1440,1200),'#141a21');draw=ImageDraw.Draw(canvas)
        for j,pic in enumerate(pics[page*12:(page+1)*12]):
            x=(j%3)*480;y=(j//3)*300;idx=page*12+j;canvas.paste(Image.fromarray(pic),(x,y));draw.text((x+8,y+275),f"{mids[idx]['asset']} / {mids[idx]['frame']/30:.2f}s",fill='white')
        canvas.save(Q/f'contact-{page+1:02d}.jpg')
    for j,idx in enumerate([0,29,61],1):
        t=T['transitions'][idx];a=t['start_frame'];data=output(['ffmpeg','-v','error','-i',VIDEO,'-vf',f'select=between(n\\,{a-1}\\,{a+3}),scale=480:270','-fps_mode','vfr','-pix_fmt','rgb24','-f','rawvideo','-']);pics=np.frombuffer(data,np.uint8).reshape(-1,270,480,3);assert len(pics)==5
        canvas=Image.new('RGB',(1440,580),'#141a21');draw=ImageDraw.Draw(canvas)
        for k,pic in enumerate(pics):
            x=k%3*480;y=k//3*290;canvas.paste(Image.fromarray(pic),(x,y));draw.text((x+8,y+274),f'frame {a-1+k}',fill='white')
        canvas.save(Q/f'transition-{j:02d}.jpg')
    qa={'status':'automated_passed_visual_review_pending','full_decode':'passed','frames':7730,'fps':30,'resolution':[1920,1080],'audio_streams':0,'embedded_subtitle_streams':0,'subtitle_cues':130,'subtitle_text_exact':True,'cue_durations_preserved':True,'gap_count':129,'all_srt_gaps_ms':100,'dissolve_count':68,'all_dissolves_frames':3,'max_dissolve_weight_mean_luma_error':max(transition_errors),'max_static_mean_luma_change':float(changes[mask].max()),'visual_review':'pending'}
    (Q/'automated.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');f=O/'delivery-manifest.json';m=json.loads(f.read_text());m['qa']=qa;f.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
