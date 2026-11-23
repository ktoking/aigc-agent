# 静态图片视频的 MiniMax 场景配音

2026-10-22 核对[官方同步语音接口](https://platform.minimax.cn/docs/api-reference/speech-t2a-http)及其`.md` OpenAPI。参数范围来自文档；场景预设是创作起点，不是官方预设或效果保证。

本仓库约定：`speech-2.8-turbo` + `Chinese_calm_streamer_nv1`，默认有声无字，不生成独立字幕。遵循目标项目和用户当前约定，不把静音项目擅自改成配音版。

目录：参数限制 → 场景预设 → 文本/提示词 → CLI → 时间线/验收。

## 常用请求设置

|字段|官方范围/行为|静帧视频用法|
|---|---|---|
|`voice_setting.emotion`|通用值`happy/sad/angry/fearful/disgusted/surprised/calm`；省略则按文本自动匹配|每个请求选一种情绪；明显转折拆请求，不用未定义的括号标签冒充情绪参数|
|`voice_setting.speed`|`[0.5,2]`，默认1|多数旁白从0.88–1.08试起，先保可懂度；不是精确时长控制|
|`voice_setting.vol`|`(0,10]`，默认1|从0.9–1.05试起；不是dB/LUFS，不表示数值加倍听感就加倍，也不能代替最终混音|
|`voice_setting.pitch`|整数`[-12,12]`，默认0|原音色优先，小幅±1试状态，避免每句改变人设音色|
|`text`内`<#0.35#>`|停顿秒数`[0.01,99.99]`，最多2位小数|仅在可朗读文本之间使用，不能连续用或放首尾；已经包含在音频时长中|
|`pronunciation_dict.tone`|`原文/替换内容`数组，可用汉字展开、带数字声调拼音、IPA等|处理人名、多音字、缩写和数字；如`处理/(chu3)(li3)`|
|`text_normalization_mode`|basic/quality；quality对2.8/2.6的hd/turbo且非流式生效，其他情况按basic处理|数字/日期/金额多时可用quality，有额外延迟，仍要试听；不用已废弃的`voice_setting.text_normalization`|
|`language_boost`|Chinese、Chinese,Yue、English、auto及其他官方语种|普通话用Chinese；粤语需相应音色与Chinese,Yue，单改此项不保证方言能力|
|`audio_setting`|sample_rate：8000/16000/22050/24000/32000/44100；channel：1或2；MP3 bitrate：32000/64000/128000/256000|默认MP3/32000/128000/单声道；剪辑中间件可WAV/FLAC，最终视频可转48kHz AAC|
|`subtitle_enable`|默认false|保持false，不请求或下载字幕文件|
|`stream/output_format`|非流式hex/url；流式仅hex；url有效24小时|离线视频默认false + hex，落地后再剪辑；HTTP流式传输不等于视频流剪辑|

文档情绪描述写“8种”但枚举列9项，以明确枚举和模型限制为准：`fluent`、`whisper`仅支持2.6-hd/turbo，当前2.8不要使用。不能为耳语擅自切模型/音色；低音量、慢语速只是轻声创作尝试，不是耳语能力。没有独立“情绪强度”字段，不编造`emotion_strength`。

### 语气与声音效果

- 仅2.8-hd/turbo支持：`(laughs)`笑、`(chuckle)`轻笑、`(coughs)`咳嗽、`(clear-throat)`清嗓、`(groans)`呻吟、`(breath)`换气、`(pant)`喘气、`(inhale)`吸气、`(exhale)`呼气、`(gasps)`倒吸气、`(sniffs)`吸鼻、`(sighs)`叹气、`(snorts)`喷鼻息、`(burps)`打嗝、`(lip-smacking)`咂嘴、`(humming)`哼唱、`(hissing)`嘶声、`(emm)`嗯、`(sneezes)`喷嚏。只选剧情需要的少数，不每句都加。标签会占时长，试听是否自然、是否误读。
- `voice_modify.pitch`：整数[-100,100]，负低沉、正明亮；效果器与普通`voice_setting.pitch`不同。
- `voice_modify.intensity`：整数[-100,100]，**负值更刚劲，正值更轻柔**，不是音量。
- `voice_modify.timbre`：整数[-100,100]，负浑厚、正清脆。
- `voice_modify.sound_effects`：一次一种，`spacious_echo`空旷回音、`auditorium_echo`礼堂广播、`lofi_telephone`电话失真、`robotic`电音。非流式支持mp3/wav/flac，流式仅mp3。
- 效果器不默认叠加，先保住已选音色。多角色分角色生成；`timbre_weights`最多4种音色按权重混为**一种声音**，不是多角色轮流说话，当前脚本未开放混音色。
- 官方另有公式朗读、流式CBR、水印、PCM/Opus等；脚本只开放静帧配音常用项，不声称覆盖全部API。

## 场景预设

优先级：基础模型/音色 → `--preset` → 显式CLI覆盖。准确值由[tts-presets.json](tts-presets.json)维护；下表用于创作选择。每个预设仍须结合台词试听。

|预设|适用画面/情绪|emotion|speed|vol|pitch|表演设计|
|---|---|---|---|---|---|---|
|natural|日常、自然旁白|省略/自动|1.00|1.00|0|先保原音色，根据正文自动匹配|
|healing|窗边、归途、释然|calm|0.92|0.90|0|陪伴朋友，不拖尾；靠措辞与留白|
|suspense|空走廊、门后异响|calm|0.92|0.95|-1|克制陈述，揭示前停0.25–0.45秒|
|fear|近身危险、突然发现|fearful|1.06|1.00|0|短句，可单次吸气，不全程喘息|
|grief|旧物、离别、回忆|sad|0.88|0.90|-1|物件后留白，不整段哭腔|
|resolve|立场冲突、反抗决断|angry|1.05|1.05|0|落字稳、短句推进，不靠音量拉满|
|reveal|真相、身份揭晓|surprised|1.02|1.00|1|只用于反转句，之后回正常旁白|
|joy|团聚、成功、轻喜剧|happy|1.08|1.00|1|带笑意，正文需要时才加轻笑|
|documentary|科普、规则、信息卡|calm|1.00|1.00|0|先处理术语数字，可选quality归一化|
|phone|电话来声|calm|1.00|0.95|0|仅电话台词用lofi_telephone|
|broadcast|场内广播、通知|calm|0.96|1.00|0|仅通知用auditorium_echo|

同一角色保持voice_id；多数场景只改emotion和小幅speed，固定采样率并统一最终响度。电话/广播需有画面空间关系，场外旁白不随意加混响。画面已强烈时配音可克制，别让每句都成为峰值。

## 三层文本与制作提示词

接口没有自由的`prompt`/`instruction`导演字段。制作提示词交给创作Agent，由它输出真实参数与朗读文本。`direction`留制作清单，绝不拼进`text`朗读。

每段保存：cue_id、角色/voice_id、图像asset_id、已确认原文source_text、带合法标签的tts_text、预设、direction、最终参数、音频路径/hash、实测秒数和首尾帧。原文与发音展开分开；不能为表演偷偷改已确认台词。

可复用提示词：

```text
使用 $story-film-workflow 制作这段静态图片视频的配音设计。
模型固定 speech-2.8-turbo，音色固定 Chinese_calm_streamer_nv1。
保留已确认正文，按角色、场景和情绪转折划分cue。
每段给出画面事件、角色、表演意图、预设、emotion/speed/vol/pitch、
可直接朗读的tts_text、必要发音词典和前后停顿关系。
只用官方停顿/语气标签；不用whisper/fluent，不编造情绪强度字段。
导演说明不放入tts_text。先输出参数设计和dry-run；实际生成按本次任务授权执行。
生产时按最终语音实测时长排画面，不烧录/内嵌字幕，不生成SRT/VTT。
```

按场景补一句：

- 治愈：“黄昏窗边的静态人物，用healing陪朋友说话；保留呼吸，避免字字重读和拖尾。”
- 悬疑：“先用suspense克制交代异常，揭示前一次0.35秒停顿；危险贴近的短句用fear，之后恢复克制。”
- 悲伤：“用grief，重点落在旧物；正文允许时在一处叹气，不让全段哭腔盖过信息。”
- 决断：“用resolve说立场句，短而落稳；冲突结束回natural，保持同一音色与整体响度。”
- 科普：“用documentary，展开人名、缩写、金额和单位；quality仅辅助，保留关键读音核对项。”

朗读文本演示，不带入其他故事的已确认剧情：

```text
悬疑：门外的脚步停了。<#0.35#>可门把手，还在慢慢转动。
恐惧：(inhale)别开门。<#0.20#>外面那个声音，不是他。
悲伤：我把钥匙放回原处。(sighs)这一次，再也没有人来开门。
治愈：先别着急。<#0.25#>你可以慢一点，故事还没有结束。
```

上面的“悬疑：”等是说明，真实tts_text只含后面的正文。停顿/语气按内容减法使用；写`[愤怒]`、`[耳语]`或“用悲伤语气朗读”不能可靠切换情绪。

## 脚本调用

不需第三方Python包。仓库入口`scripts/minimax_tts.py`；独立包用`<skill目录>/scripts/minimax_tts.py`。先取`MINIMAX_API_KEY`，macOS再读Keychain service `codex-minimax-api-key`。不落密钥/请求头；云端由运行环境供密钥，不能打包本机Keychain。

```bash
python3 <skill目录>/scripts/minimax_tts.py --list-presets
python3 <skill目录>/scripts/minimax_tts.py \
  --preset suspense --text '门外的脚步停了。<#0.35#>可门把手，还在慢慢转动。' --dry-run
python3 <skill目录>/scripts/minimax_tts.py \
  --preset grief --text-file <该段tts文本.txt> --output <该段output/narration.mp3>
python3 <skill目录>/scripts/minimax_tts.py \
  --preset documentary --speed 0.98 --vol 0.95 --pitch 0 \
  --normalization quality --tone '处理/(chu3)(li3)' \
  --text-file <该段tts文本.txt> --output <该段output/narration.wav>
```

`--emotion auto`移除情绪；`--sound-effect none`移除效果。`--modify-pitch/--intensity/--timbre`对应效果器；`--sample-rate/--channel/--bitrate`对应规格，bitrate仅MP3生效。`--dry-run`只打印参数，不取密钥、不收费。脚本不自动换模型/音色，失败不自动重试，不覆盖已有文件。

首次选风格，用相同短文本比较少量候选，模型/音色一致，优先一次只改一项。已授权正式生产可延用已选预设，无须每句反复审批。失败保留状态和trace_id，鉴权/余额/非法参数先解决原因，不循环收费重试。

## 接入静帧时间线

1. 按角色、情绪连续性和画面事件分段。跨图连续旁白可共用一段音频，不必每张图重配；图片按约5秒一张独立新图规划，不能把音频共用误解成重复回放旧图。精确句级换图可逐句生成，长句群需人工或用可用对齐工具确认内部边界。
2. 先生成并ffprobe实测，再向上量化为整数帧：`ceil(duration_seconds * fps)`。不用计费字数估时。API audio_length作记录，最终以落地文件为准；MP3编解码延迟可造成小差异。
3. 音频内停顿、换气、尾音已经占时长，不按标点/段尾重复加。独立cue间如约定0.1秒，只补一次；换图叠化仍放空档内。可按听感调整外部gap，不能裁词头尾压时长。
4. 音轨与图像起止帧写入同一时间线。逐cue音轨按start_frame/fps放置，补齐量化余量与空档，再合成总音轨；不裸拼MP3或只给第一张图配音。
5. 优先复用故事工程渲染器。旧`story_video.py`仍是静音/字幕模式，不能传不存在的audio字段后声称已自动配音；有声版需故事工程编辑器或ffmpeg合轨并验最终MP4。未要求字幕时不调用旧脚本的字幕输出路径。
6. 单图单段最小合成（多图按统一时间线扩展）：

```bash
ffmpeg -n -loop 1 -framerate 30 -i <image.png> -i <narration.mp3> \
  -map 0:v:0 -map 1:a:0 -c:v libx264 -tune stillimage -pix_fmt yuv420p \
  -c:a aac -ar 48000 -shortest -movflags +faststart <scene.mp4>
```

此处`-shortest`仅适用于无限循环静图配完整音频，不能套用有限视频和更长旁白而截尾。合轨后检查末句，不凭命令成功判断完整。

## 混音与验收

- `vol`控制请求；跨段响度与BGM比例在后期统一。先测再调，不把每段拉最大，避免削波、保留峰值余量。叙事片可从约-16 LUFS/-1 dBTP试混，平台规范和听感优先；这是后期目标，不是MiniMax参数或所有题材的强制标准。
- 默认只合成所需配音，不自动加音乐；要BGM时给人声留空间，电话/广播仅覆盖相应场内声音。
- API需HTTP成功、base_resp.status_code=0、非空audio、完成状态2。完整解码与实际试听分开记录。
- 最终MP4检查预期音频流、分辨率/fps/帧数、末句完整；无非预期字幕流或SRT/VTT；源图与编码帧无烧录字。
- 试听检查身份、情绪、停顿/标签、人名/数字/缩写、跨段响度、词头尾和音画对应。未试听记NOT_RUN；返回0/完整解码都不能代替美学验收。
