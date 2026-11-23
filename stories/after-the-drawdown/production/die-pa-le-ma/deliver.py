"""验证真实编码文件，拆四段，核对字幕与原音乐，生成交付台账。"""
from pathlib import Path
import subprocess,json,hashlib,re
import numpy as np
P=Path(__file__).resolve().parent
EP=P.parent.parent/'episodes/EP001_die-pa-le-ma'
OUT=EP/'output'
FILM=OUT/'die-pa-le-ma_1080x1920_60s.mp4'
def run(a):return subprocess.run(a,check=True,capture_output=True).stdout
def probe(p):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
m=probe(FILM);video=next(s for s in m['streams']if s['codec_type']=='video')
assert (video['width'],video['height'],video['r_frame_rate'])==(1080,1920,'30/1')
assert abs(float(m['format']['duration'])-60)<.08
assert len([s for s in m['streams']if s['codec_type']=='audio'])==1
run(['ffmpeg','-v','error','-i',str(FILM),'-f','null','-'])
bm=json.loads((P/'beat-map.json').read_text());cues=bm['cues']
assert len(cues)==16 and cues[0]['start']==0 and cues[-1]['end']==60
assert all(c['start']<c['end']for c in cues)
assert all(abs(a['end']-b['start'])<1e-8 for a,b in zip(cues,cues[1:]))
assert (OUT/'die-pa-le-ma.zh-CN.srt').read_text().count(' --> ')==len(cues)
assert (OUT/'die-pa-le-ma.zh-CN.vtt').read_text().count(' --> ')==len(cues)
segments=[]
for i,seg in enumerate(sorted(EP.glob('segment_*'))):
 dest=seg/'output/video.mp4'
 run(['ffmpeg','-v','error','-y','-ss',str(i*15),'-i',str(FILM),'-t','15','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)])
 sm=probe(dest);assert abs(float(sm['format']['duration'])-15)<.08
 for t,n in [(0,'first'),(15-1/30,'last')]:run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(dest),'-frames:v','1',str(seg/f'frames/{n}-frame.png')])
 ap=seg/'api-request.md';ap.write_text(ap.read_text().replace('等待主片渲染后抽段验证。','已完成主片抽段与首尾帧验证。'))
 segments.append({'file':str(dest.relative_to(EP)),'duration':float(sm['format']['duration'])})
run(['ffmpeg','-v','error','-y','-ss','5','-i',str(FILM),'-frames:v','1',str(OUT/'cover.jpg')])
run(['ffmpeg','-v','error','-y','-i',str(FILM),'-vf','fps=1/5,scale=216:384,tile=6x2','-frames:v','1',str(OUT/'contact-sheet.jpg')])
def pcm(p):return np.frombuffer(run(['ffmpeg','-v','error','-i',str(p),'-t','12','-vn','-ac','1','-ar','22050','-f','f32le','pipe:1']),dtype=np.float32).astype(np.float64)
a=pcm(P/'assets/reference-soundtrack.m4a');b=pcm(FILM);n=min(len(a),len(b));a=a[:n];b=b[:n]
nfft=1<<(2*n-1).bit_length();cross=np.fft.irfft(np.fft.rfft(b,nfft)*np.conj(np.fft.rfft(a,nfft)),nfft)
lags=np.r_[np.arange(2206),np.arange(nfft-2205,nfft)];peak=int(lags[np.argmax(cross[lags])]);lag=peak if peak<nfft//2 else peak-nfft
aa=a[:n-lag]if lag>=0 else a[-lag:n];bb=b[lag:n]if lag>=0 else b[:n+lag]
corr=float(np.corrcoef(aa,bb)[0,1]);assert corr>.98
check=json.loads((P/'check.json').read_text());assert check['ok']
qa={'status':'PASS_LOCAL_DELIVERY','video':{'file':FILM.name,'duration':float(m['format']['duration']),'resolution':[1080,1920],'fps':30,'frames':video.get('nb_frames'),'full_decode':'PASS','bytes':FILM.stat().st_size,'sha256':hashlib.sha256(FILM.read_bytes()).hexdigest()},'audio':{'music_user_confirmed':'we never 若如初见','range':[0,60],'rate':1,'new_voiceover':False,'first_12_seconds_waveform':{'correlation':corr,'lag_ms':lag/22050*1000,'boundary':'与参考AAC的前12秒波形比较；非全曲版权或曲名鉴定'}},'beat_sync':{'bpm_estimate':112.9,'scene_boundaries':[s['start']for s in bm['scenes']],'max_frame_quantization_ms':max(abs(round(c['start']*30)/30-c['start'])*1000 for c in cues),'scope':'同一实测节拍表驱动场景、文案与主要物体动作；BPM为估计值'},'subtitles':{'cues':len(cues),'srt':'die-pa-le-ma.zh-CN.srt','vtt':'die-pa-le-ma.zh-CN.vtt','continuous_timing':'PASS'},'segments':segments,'hyperframes':{'ok':check['ok'],'runtime_errors':check['runtime']['errorCount'],'layout_errors':check['layout']['errorCount'],'motion_samples':check['motion']['samples'],'motion_errors':check['motion']['errorCount'],'contrast_checked':check['contrast']['checked'],'contrast_passed':check['contrast']['passed'],'lint_warnings':check['lint']['warningCount']},'intro10':{'file':'intro10.mp4','duration':float(probe(OUT/'intro10.mp4')['format']['duration']),'gate':'已检查实际编码逐秒联系表及本地播放器'},'browser_playback':{'played_from_start_to_end':False,'status':'PENDING'},'boundaries':{'market_data':'未使用真实行情；全部金融物体为隐喻','external_video_api':'NOT_RUN','social_publication':'NOT_RUN','cloudflare':'PENDING'}}
(OUT/'delivery-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(EP/'qa-checklist.md').write_text('# 交付检查\n\n- [x] 六幕原创视觉、无分支连线；分镜与来源台账齐全。\n- [x] 先导出10秒试片并检查实际编码帧。\n- [x] 60秒、1080×1920、30fps，完整解码通过。\n- [x] 四段各15秒、实际首尾帧齐全。\n- [x] 16条字幕连续覆盖全片。\n- [x] 原音轨原速，真实编码前12秒波形比对通过。\n- [x] HyperFrames运行、布局、动效和对比度检查通过。\n- [ ] 主片浏览器连续播放与Cloudflare链接，见delivery-qa.json后续回填。\n')
print(json.dumps(qa,ensure_ascii=False,indent=2))
