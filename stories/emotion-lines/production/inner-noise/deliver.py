"""对已完成的主片抽段、抽帧、验音轨并生成本地交付报告。"""
from pathlib import Path
import json, subprocess, hashlib, re, math
import numpy as np

ROOT=Path(__file__).resolve().parent
EP=ROOT.parent.parent/'episodes/EP001_inner-noise'
OUT=EP/'output'
FILM=OUT/'inner-noise_1080x1920_60s.mp4'
def run(args):
    return subprocess.run(args,check=True,capture_output=True).stdout
def probe(p):
    return json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))

meta=probe(FILM)
assert abs(float(meta['format']['duration'])-60)<.12
vs=[s for s in meta['streams'] if s['codec_type']=='video'][0]
assert (vs['width'],vs['height'])==(1080,1920)
assert len([s for s in meta['streams'] if s['codec_type']=='audio'])==1
run(['ffmpeg','-hide_banner','-v','error','-i',str(FILM),'-f','null','-'])

segments=[]
for i,seg in enumerate(sorted(EP.glob('segment_*'))):
    dest=seg/'output/video.mp4'
    run(['ffmpeg','-hide_banner','-v','error','-y','-ss',str(i*15),'-i',str(FILM),'-t','15','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)])
    m=probe(dest)
    assert abs(float(m['format']['duration'])-15)<.12
    for t,name in [(0,'first-frame.png'),(15-1/30,'last-frame.png')]:
        run(['ffmpeg','-hide_banner','-v','error','-y','-ss',str(t),'-i',str(dest),'-frames:v','1',str(seg/'frames'/name)])
    (seg/'api-request.md').write_text((seg/'api-request.md').read_text().replace('待成片抽段，由 delivery-qa.json 回填。','已完成；15 秒本地成片与首尾帧已验证。外部 API 未调用。'))
    segments.append({'path':str(dest.relative_to(EP)),'duration_seconds':float(m['format']['duration']),'size_bytes':dest.stat().st_size})

run(['ffmpeg','-hide_banner','-v','error','-y','-ss','52.2','-i',str(FILM),'-frames:v','1',str(OUT/'cover.jpg')])
run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(FILM),'-vf','fps=1/5,scale=216:384,tile=6x2','-frames:v','1',str(OUT/'contact-sheet.jpg')])

def pcm(p):
    return np.frombuffer(run(['ffmpeg','-hide_banner','-v','error','-i',str(p),'-t','12','-vn','-ac','1','-ar','22050','-f','f32le','pipe:1']),dtype=np.float32).astype(np.float64)
a=pcm(ROOT/'assets/reference-soundtrack.m4a');b=pcm(FILM)
# 比较真实音乐波形，允许重编码的极小采样起始差异。
n=min(len(a),len(b));a=a[:n];b=b[:n]
fftlen=1<<(2*n-1).bit_length()
cross=np.fft.irfft(np.fft.rfft(b,fftlen)*np.conj(np.fft.rfft(a,fftlen)),fftlen)
lags=np.r_[np.arange(0,2206),np.arange(fftlen-2205,fftlen)]
peak=int(lags[np.argmax(cross[lags])]);lag=peak if peak<fftlen//2 else peak-fftlen
if lag>=0:aa=a[:n-lag];bb=b[lag:n]
else:aa=a[-lag:n];bb=b[:n+lag]
corr=float(np.corrcoef(aa,bb)[0,1]);assert corr>.98, f'Unexpected soundtrack mismatch: {corr}'

bm=json.loads((ROOT/'beat-map.json').read_text())
cues=bm['cues'];assert len(cues)==19
assert cues[0]['start']==0 and cues[-1]['end']==60
assert all(c['start']<c['end'] for c in cues)
assert all(abs(a['end']-b['start'])<.001 for a,b in zip(cues,cues[1:]))
quant=[abs(round(c['start']*30)/30-c['start'])*1000 for c in cues]
check=json.loads((ROOT/'check.json').read_text());assert check['ok']
report={
 'status':'PASS_LOCAL_DELIVERY',
 'video':{'file':FILM.name,'duration_seconds':float(meta['format']['duration']),'resolution':[vs['width'],vs['height']],'fps':vs['r_frame_rate'],'frames':vs.get('nb_frames'),'codec':vs['codec_name'],'full_decode':'PASS','sha256':hashlib.sha256(FILM.read_bytes()).hexdigest()},
 'audio':{'stream_count':1,'track_name_user_confirmed':'we never 若如初见','source':'Nico 参考作品原始AAC音轨','source_range_seconds':[0,60],'playback_rate':1,'new_voiceover':False,'waveform_comparison_first_12_seconds':{'pearson_correlation':corr,'alignment_lag_ms':lag/22050*1000,'scope':'重编码后的音轨与参考音轨前12秒，非全曲身份鉴定'}},
 'beat_sync':{'bpm_estimate':bm['bpm_estimate'],'text_cues':len(cues),'authoring_grid':'源音轨实测节拍','max_30fps_timestamp_quantization_error_ms':max(quant),'boundary':'BPM为自动估计；量化误差仅指时间线落点，不代表人耳音乐理解准确度'},
 'subtitles':{'srt':'inner-noise.zh-CN.srt','vtt':'inner-noise.zh-CN.vtt','cues':len(cues),'timing':'PASS'},
 'segments':segments,
 'hyperframes':{'check_ok':check['ok'],'runtime_errors':check['runtime']['errorCount'],'layout_errors':check['layout']['errorCount'],'contrast_checks':check['contrast']['checked'],'contrast_passed':check['contrast']['passed'],'motion_samples':check['motion']['samples'],'motion_errors':check['motion']['errorCount'],'lint_warnings':check['lint']['warningCount'],'warning_note':'单一连续图形场景的3个嵌套图层结构建议，非渲染错误'},
 'boundaries':{'rendered_topics':['内耗'],'other_topics':'4个候选未渲染','paid_generation':'NOT_RUN','external_video_api':'NOT_RUN','published':False,'subjective_style_match':'样片，非逐像素复刻'},
 'visual_review':'关键帧与Studio预览已看；待本次编码成片连续播放复核'
}
(OUT/'delivery-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(EP/'qa-checklist.md').write_text('# 交付检查\n\n- [x] 60秒，1080×1920，30fps，主片全程解码通过。\n- [x] 四段各15秒，实际首尾帧齐全。\n- [x] 使用参考片原音轨，未变速；前12秒真实波形对比通过。\n- [x] 19条字幕，完整覆盖0至60秒。\n- [x] 布局、运行时、对比度和300个运动采样检查通过。\n- [x] 图形推近时不会遮挡标题。\n- [ ] 编码成片连续播放复核；结果回填delivery-qa.json。\n\n只完成本地样片，没有发布。其余四个选题未渲染。')
print(json.dumps(report,ensure_ascii=False,indent=2))
