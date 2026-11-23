from pathlib import Path
import hashlib,json,re,shutil

P=Path(__file__).resolve().parents[1]
STORY=P.parents[1]
ROOT=P.parents[3]
for folder in ['audio/text','audio/raw','audio/final','assets','prompts','references','qa']:
    (P/folder).mkdir(parents=True,exist_ok=True)
src=STORY/'drafts/LONG-EP04-hold-the-warehouse-v2-narration.txt'
text=src.read_text();digest=hashlib.sha256(src.read_bytes()).hexdigest()
review=STORY/'reviews/2026-11-11-ep04-hold-the-warehouse-v2-review.md'
assert digest in review.read_text()
(P/'narration.txt').write_text(text)
shutil.copy2(STORY/'docs/voice-profile.json',P/'voice-profile.json')
for name in ['male-neutral.png','female-neutral.png']:
    shutil.copy2(STORY/'production/long-ep03-v1/references'/name,P/'references'/name)
def units(s):return len(re.findall(r'[\w\u4e00-\u9fff]',s))
plan=[]
for pn,para in enumerate(text.strip().split('\n\n'),1):
    sentences=[x for x in re.split(r'(?<=[。！？])',para) if x]
    parts=[]
    for sentence in sentences:
        if units(sentence)<=42:parts.append(sentence);continue
        buf=''
        for clause in re.split(r'(?<=[，；])',sentence):
            if units(buf+clause)>42 and buf:parts.append(buf);buf=''
            buf+=clause
        if buf:parts.append(buf)
    merged=[];buf=''
    for part in parts:
        if units(buf+part)>34 and buf:merged.append(buf);buf=''
        buf+=part
    if buf:merged.append(buf)
    assert ''.join(merged)==para
    for spoken in merged:
        assert units(spoken)<=52,spoken
        cid=f'c{len(plan)+1:03}'
        c=dict(id=cid,paragraph=pn,source_text=spoken,tts_text=spoken,model='speech-2.8-turbo',voice_id='Chinese (Mandarin)_Gentleman',api_speed=1.2,preset='documentary',emotion='calm',vol=1.0,pitch=0,units=units(spoken))
        plan.append(c);(P/'audio/text'/f'{cid}.txt').write_text(spoken)
(P/'voice-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
for name in ['generate_voice.py','process_voice.py','check_voice.py','build_shots.py','render.py']:
    s=(STORY/'production/long-ep03-v1/scripts'/name).read_text()
    s=s.replace('山姆第三集 白光之后','山姆第四集 守住这座仓库').replace('LONG-EP03-v1','LONG-EP04-v1')
    s=s.replace("initial_prompt='许棠，山姆，林岚，周强。'","initial_prompt='许棠，山姆，霰弹枪，收货亭，机房。'")
    (P/'scripts'/name).write_text(s)
manifest=dict(status='IN_PRODUCTION',authorized='user requested images + MiniMax TTS + render after v2 script review',skill=str((ROOT/'skills/story-film-workflow/SKILL.md').resolve()),script=str(src.relative_to(STORY)),script_sha256=digest,script_approved_for_production=True,voice_cues=len(plan),voice='speech-2.8-turbo / Chinese (Mandarin)_Gentleman / speed1.2 / calm',cue_gap_seconds=.1,dissolve_seconds=.1,subtitles_burned=True,independent_subtitles=False,fixed_camera=True,reuse_images=False,music='Audiomachine Tempt Scandal fixed quiet loop; no ducking',qa={'tts':'PENDING','images':'PENDING','render':'PENDING','playback':'PENDING'},hyperframes_usage='UNKNOWN: CLI not installed; continuing established story FFmpeg engine')
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(P/'brief.md').write_text('# 第四集生产合同\n\n以v2原文和该版审读为输入，用户本轮已授权图片、MiniMax TTS和渲染。保留旧稿旧片；使用原角色参考和现有FFmpeg渲染器。约5秒独立新图、固定构图、干净干燥写实、外景黄色尘土；字幕逗号空格句号删除。警报与火光仅表现虚构事件，不绘制燃烧瓶制作、机关结构或枪械操作。背景音乐沿用Tempt Scandal、固定低音量、首尾0.5s；画面首尾0.3s。无独立字幕。按实际语音决定时长，不加空镜凑十分钟。\n')
print(json.dumps(dict(cues=len(plan),paragraphs=pn,script_sha256=digest),ensure_ascii=False))
