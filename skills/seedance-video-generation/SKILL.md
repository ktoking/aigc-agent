---
name: seedance-video-generation
description: Use when generating, polling, downloading, retrying, or writing prompts for AI short-drama segment videos with VolcEngine Ark Seedance, especially from story-package segment folders with first/last frames, storyboard directions, character references, scene assets, and audio requirements.
---

# Seedance 视频生成

## 目的

用于把 `stories/<story-id>/episodes/<episode>/segment_XX_xx-xxs/` 里的首帧、尾帧、故事板文字、按段选择的角色/动作/场景/道具参考资产和 `director-promt.txt` 提交给火山 Ark Seedance，生成 15 秒竖屏短剧视频。若旧 segment 缺少 `director-promt.txt`，再回退使用 `prompt.md`。

Seedance 2.0/2.0 Fast 不要直接上传本地含人脸参考图。需要人脸一致性时，先用 Seedream 5.0 lite 文生图生成平台信任产物，再把 Seedream 返回的 URL 传给 Seedance。

## 必须遵守

- 不把 Ark key 写入任何仓库文件；只从当前 shell 的 `ARK_API_KEY` 读取。
- 正式分段默认 `duration=15`、`ratio=9:16`、`resolution=720p`。
- 本仓库默认以 Seedance 2.0-mini `doubao-seedance-2-0-mini-260615` 作为低成本草稿主力；标准 Seedance 2.0/2.0 Fast 只用于动作逻辑验证后的定稿镜头。
- 视频生成是高成本操作；默认先做提交前门禁检查和 dry-run 计划，除非用户明确说“直接生成/立即提交/可以烧”，否则不要提交正式视频任务。
- 动作戏默认先生成 4-5 秒 mini 小样，每条只验证一个动作任务；不要直接用高价模型抽 15 秒复杂正片。
- 必须优先使用本段 `frames/first-frame.png` 和 `frames/last-frame.png`；角色一致性优先用角色三视图、定妆图或尾帧。
- `scripts/ark_video.py` 的自动参考图只应依赖首帧和尾帧；故事板图只能显式 `--include-storyboard` 才传。
- 故事板表格图主要给人审阅，不默认作为视频参考图上传；把故事板内容转写进 prompt，避免模型把表格当静态图片拉伸。
- 背景/场景资产要来自当前 story 的 `assets/scenes/`，不可用错误人物图或无关场景图兜底。
- 输入人物图必须声明为 AI 生成的虚拟角色，不包含真人身份、肖像或隐私信息。
- 含人脸参考优先使用 Seedream 5.0 lite 文生图返回的 URL；不要下载后再作为本地图片 base64 上传给 Seedance。
- 若用户明确要求“直接拿本地图生成”，允许使用本地图片；若隐私审核拦截，立即停止并汇报，不自动换错图。
- 如果火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，默认立即停止，不要自动换图、空镜兜底或继续强行提交。
- 只有用户明确要求再次尝试时，才允许追加/加强虚拟人物隐私说明后进行有限重试。
- `output/` 下的 API 返回、视频、任务 id 是本地运行产物，默认不入库。

## 生成前检查

1. 确认 segment 目录存在。
2. 读取 segment 的 `director-promt.txt`、`prompt.md`、`storyboard.md`、`first-frame.md`、`last-frame.md`。正式提交优先使用 `director-promt.txt`。
3. 确认图片存在：
   - `frames/first-frame.png`
   - `frames/last-frame.png`
   - 角色三视图/定妆图，如 `frames/**/character-turnaround.png`
   - 故事板表格图仅用于人工核对，不默认上传。
4. 按本段最容易漂移的问题选择相关背景/场景、角色、动作、道具资产，例如 `stories/<story-id>/assets/scenes/<SCENE_ID>/*.png`。
5. 确认 `scripts/ark_video.py` 存在，并优先使用该脚本提交、轮询、下载。
6. 如果本地参考图被隐私审核拦截，优先停止；只有用户确认继续时，才改走 Seedream 5.0 lite 信任图片 URL。

## 参考图选择协议

参考图不是素材越多越好；每张图必须有明确职责，并在 `director-promt.txt` 中按 API 输入顺序写成“参考图1/参考图2/参考图3”。API 没有真正的 `@图片` 语法，`@` 只会变成普通文本；靠图片输入顺序和文字说明建立对应关系。

默认策略：

1. 参考图1：`frames/first-frame.png`，锁定 0 秒桥接画面和人物站位。
2. 参考图2：`frames/last-frame.png`，锁定 15 秒收束画面和下一段衔接。
3. 参考图3：本段最容易漂移的一张资产，如角色脸/三视图、场景路线、动作编排或关键道具。
4. 参考图4-5：只在复杂打斗、精确空间路线、道具数量或身份反转证据确有必要时追加。

优先选择能解决“本段最大风险”的图：

| 风险 | 追加图 |
| --- | --- |
| 脸或服装漂移 | 角色脸部参考、三视图、定妆图 |
| 路线和空间跳变 | 场景路线图、空间关系图 |
| 打斗动作乱 | 动作编排图、角色 action poses |
| 道具数量/比例错 | 道具比例图、关键道具图 |
| 风格偏移 | 风格 key art，仅在首尾帧风格不足时追加 |

如果参考图是路线图、动作图、比例图或带标注生产图，必须写清：只用于理解空间/动作/比例，不要把箭头、文字、网格、标注画进最终视频。

不要默认上传 `storyboard-sheet.png`：它适合人审阅和 prompt 转写，直接上传容易带来文字污染、表格污染和静态拉图。确实要上传时，命令必须显式加 `--include-storyboard`，并在计划里解释原因。

## 提交前门禁

在任何正式 `submit` 之前，必须先给出或保存一份“视频提交计划”，并逐项检查：

- **参考图数量**：默认 3-5 张；自动默认只有首帧和尾帧，其他资产必须按段显式追加；不上传整张故事板表格。
- **角色锁定**：列出每个角色的不可变特征；对特殊标记（例如“林晚左眼角下一颗痣”）单独标成 QA 项。
- **首尾帧一致**：首帧负责开场环境，尾帧负责收束构图；不要用错误角色或旧版本尾帧。
- **时间轴完整**：15 秒必须拆成明确时间段，不能只写一段泛泛描述。
- **运镜明确**：每段必须写景别、镜头运动和主体动作，避免只做静态拉图。
- **声音开关**：需要声音时命令必须包含 `--generate-audio`；不需要声音时明确写“无声样片”。
- **剧情短剧默认有声**：豪门复仇、丧尸清道夫、追逐、打斗、反转、悬疑揭示等可观看样片默认加 `--generate-audio`。只有用户明确要“无声样片/只测画面/不烧音频”时才关闭声音。
- **原生音频边界**：Seedance 原生音频优先当作环境声、动作声、群体反应声使用。不要在一个 15 秒任务里依赖多角色精准对白和精确说话人归属；如果台词归属很重要，优先后期配音/剪辑，或只保留一个可见说话人、一句短台词，并明确其他角色全程不说话。
- **合规说明**：本地人物图必须包含“AI 虚构角色，不含真人隐私信息”说明。
- **失败停止线**：隐私拦截、角色错脸、参考图缺失、参数 400 时停止，不自动换图重试。

只有当以上门禁都通过，且用户已经明确授权生成，才提交正式视频任务。若用户已经明确说“用这些图生成视频”，视为授权一次提交；失败后仍需再次确认才可重试或换平台。

门禁计划格式：

```text
提交前计划
- 模型/时长/画幅/分辨率：
- 是否生成声音：
- 参考图：
- 不上传的图：
- 每张图用途：
- 角色 QA：
- 时间轴：
- 风险与停止线：
- 输出文件名：
```

## 提示词写法

项目中 `prompt.md` 是可读维护版视频提示词，`director-promt.txt` 是 API 直投版导演提示词。正式提交给 `scripts/ark_video.py --prompt-file` 时优先使用 `director-promt.txt`；文件名沿用项目既有拼写 `promt`。

Seedance 2.0 支持文字、图片、音频、视频等多模态参考输入；提示词不要写成散文，要写成导演执行指令。官方和实践指南的共同结论是：参考素材负责“长相/构图/风格”，文本负责“动作/运镜/时间轴/约束”。

### 通用逐秒结构

适合动作因果很强、需要严格控制每几秒发生什么的片段。

```text
全局规格：9:16，15秒，720p，3D动画电影风，非真人，生成声音。
参考图用途：按 API 输入顺序写“参考图1/2/3/4”，每张图只负责一个主要约束；不要笼统说“参考所有图片”。
角色锁定：姓名、发型、服装、面部特征、禁止变化项。
时间轴镜头：0-4s / 4-8s / 8-11s / 11-15s，每段写主体动作、场景变化、镜头运动。
音效/声音：需要声音时写风声、警报、人声、能量声，并在命令中加 `--generate-audio`。
负面约束：不要字幕、水印、logo；不要静态拉图、不要图片变形过渡、不要新增角色脸。
```

### 五段式按镜头切片结构

适合豪门复仇、丧尸清道夫、怪谈反转、宴会/室内调度等更看重“气质 + 场景反差 + 镜头设计”的片段。选了按镜头切片，就不要再混用 `0-3 秒 / 3-7 秒` 这类按秒切片；每个分镜只写“景别、构图、运镜手法、画面内容”。

按镜头切片不是少写。每个分镜内部必须包含足够撑时长的连续动作点，避免变成静态图慢推。参考《丧尸清道夫》的写法：一个分镜里通常有“主体进入/姿态变化 -> 环境声音或物体触发 -> 角色反应 -> 视线方向或情绪变化 -> 场景细节回应”。15 秒四镜头时，每个镜头至少写 4-6 个可见动作或环境变化。

```text
核心主题：<题材> | <场景反差> | 电影级质感 | <美学定调> | <情绪> | 杜绝游戏 CG 感

参考图1：首帧图，锁定起始构图、人物站位和场景空间。
参考图2：尾帧图，锁定结束构图、道具状态和下一段衔接。
参考图3：本段最容易漂移的资产，例如角色定妆、动作路线、关键道具或场景比例。

〖人物与基础设定〗
面部：参照对应参考图，五官、脸型、发型、表情保持一致，杜绝随意美化和换脸。
服装：写材质和不可变特征，例如湿感蕾丝、哑光皮革、金属腰带、破损边缘。
场景：写空间、天气、光线和动态环境，例如雨夜落地窗、黑色大理石反射、吊灯轻晃。
声音：默认不配乐，仅保留同期声；列出环境声、动作声、台词落点，并在命令中加 `--generate-audio`。
对白：如果使用原生音频，优先写“无清晰对白，只要环境声/群体反应”。需要清晰台词时，一个片段最多保留一句短台词，并让说话人在画面中近景可见；同时写清其他角色不说话。不要把广播、同学、老师、主角多方台词塞进同一段。

〖氛围与画质〗
风格核心：<电影级质感/高端短剧/超写实或明显非真人>，强调场景反差，不要写成普通说明文。
视觉基调：模拟电影摄影机 + 镜头，写色彩、影调、光源和材质差异。
质感要求：写真实瑕疵和材质区别，避免过度锐化、鱼鳞状网格、满屏微纹理。

〖运镜规则〗
单镜头倾向：说明少切镜、一镜到底倾向或允许的少量镜头切换。
角度：写开场景别、关键横移/推进/低角度跟随/后拉构图。
呼吸感：轻微手持呼吸感，镜头稳定克制，不要快速乱切。

〖分镜（按镜头切片）〗
分镜一：<镜头名>
景别：<中广角/近景/低角度中景/特写>。
构图：<主体、前景、后景、关键道具的空间关系>。
运镜手法：<极缓推进/平稳横移/固定机位/低角度跟随/轻微后拉>。
画面内容：<至少 4-6 个连续可见动作点：主体动作、道具变化、环境反应、旁人反应、视线/表情变化、同期声触发；不写秒数>。

分镜二：...

负面约束：不要字幕、水印、logo、可读文字；不要人物瞬移、换房间、多个主角；不要把参考图做成静态拉伸。
```

按镜头切片的参考图顺序默认是“首帧 -> 尾帧 -> 角色/动作/道具”。如果把角色定妆图放在参考图1，Seedance 容易把角色图当成主锚点，结尾漂回定妆照而不是尾帧构图。只有当用户明确说“优先测脸”时，才把角色参考图放到首位。

按镜头切片 QA：

- 每个分镜是否至少有 4 个连续动作点，而不是一句剧情概括。
- 每个分镜是否有一个声音触发或环境反馈，例如玻璃声、雨声变化、电流、脚步、水花。
- 每个分镜是否写了角色的姿态/视线/表情变化。
- 画面是否形成“主体 + 道具 + 环境 + 旁人反应”的闭环。
- 结尾分镜是否推进剧情或抛钩子，而不是只停在情绪特写。
- 原生音频是否只承担环境声/群体反应，或者是否只有一个明确可见说话人和一句短台词。

## 动作短剧提示词规范

当生成追逐、打斗、逃亡、反制、交付悬疑等短剧片段时，优先使用“逐秒动作因果”写法。这个写法已在 `last-mile-robot` 的 Seedance 2.0 片段中验证，比泛泛镜头表更容易得到连贯、可读、不卡顿的动作视频。

核心原则：

- **每段都写动作因果**：不要只写“敌人开火、主角躲避、继续前进”。要写清“攻击从哪里来、打向哪里、命中哪里、主角为什么这样躲、躲完后产生什么新局面”。
- **先锁移动结构**：如果角色是轮式、履带式、漂浮式、四足式或固定底盘，必须在角色锁定和每个相关动作里用一致动词描述，例如“轮式底盘贴地滑行、急刹、漂移”。不要混用“奔跑、迈步、半跪、脚步、收脚”等会把模型带成人形运动的词。
- **每个攻击都有命中点**：枪、电磁网、激光、扫描线、钩索都必须写明确目标和命中点，例如地面积水、路障边缘、护盾边缘、机械臂外壳、广告屏边框、门板、墙面。避免无目标乱扫射。
- **每个反应都有受力点**：拉扯、撞击、格挡、攀爬、横摆要写清受力点，例如餐箱提手、墙边管道、广告屏支架、电梯井墙沿、配送柜底部、脚轮水痕。
- **躲避必须有路径**：不要用“绕圈、画圈、寻找出口、原地防御”撑时长。要写成“从入口玻璃门滑到左侧承重柱后、再贴着收银台外沿滑向后门光缝”，让模型知道角色从 A 点到 B 点。
- **穿模高风险动作要降级**：摆荡、飞跃、掠过、撞屏、穿门等动作容易穿墙或穿过物体。写成“在广告屏前方半米处摆过、撞在广告屏金属外框、无人机砸进外框而不是穿过屏幕、角色始终在墙面/屏幕前方可见”。
- **道具意图必须明确**：如果主角是在保护道具，不要写“举起/递向/送到敌人面前”。应写“道具贴胸/贴身，主角身体或机械臂位于敌方火线和道具之间，攻击先命中外壳/机械臂/护盾边缘”。否则模型容易把防御动作误解成交付动作。
- **台词必须有触发条件**：不要让角色在仍被直接攻击时突然说话。写成“躲到柜后并切断火线后，才说……”“挡住第一束激光后，才说……”。
- **尾段继续推进剧情**：11-15 秒不要只停在情绪特写。可以给 1 秒情绪钩子，然后立刻加入下一步行动、下一段威胁或转场衔接。
- **声音用正向锁定**：需要固定音色时，只写正向约束，例如“固定使用低沉、清晰、克制的男性机器人合成音，音色一致，语速稳定”。避免在 prompt 里反复写“女声、童声”等不想要的词。
- **减少反向污染词**：避免写“慢动作、停顿、静止、定格、静态、PPT、长时间停在……”等词，即使是禁止项也尽量改成正向动作要求。

推荐时间块仍保持 4 段，但每段内部要拆成子节拍：

```text
0-3 秒：第 0-0.8 秒 <承接上一段 + 主体进入>；第 0.8-1.4 秒 <威胁出现或武器预备>；第 1.4-2.1 秒 <攻击/钩索/扫描准确命中某个目标>；第 2.1-3 秒 <主角即时反应 + 受力痕迹>。运镜：<必须看清哪些因果点>。声音：<动作声和环境声>。

3-7 秒：第 3-4 秒 <第一动作>；第 4-5 秒 <攻击命中点或受力点>；第 5-6 秒 <躲避/格挡/反制>；第 6-7 秒 <造成新局面>。台词落点：<动作条件成立后才说>。运镜：<主体、威胁、命中点同框或连续可读>。

7-11 秒：第 7-8 秒 <新威胁出现>；第 8-9 秒 <目标锁定/命中/受力>；第 9-10 秒 <主角反制动作>；第 10-11 秒 <威胁被阻断或转入下一动作>。不要让敌人突然停止攻击；必须给停止、后退、迟疑或火线中断的原因。

11-15 秒：第 11-12 秒 <上一动作结果>；第 12-13 秒 <短促情绪钩子或信息揭示>；第 13-14 秒 <新的威胁/下一步动作>；第 14-15 秒 <冲向下一场景或留下清楚的下一段钩子>。避免只做餐箱、脸、门缝、光效特写。
```

动作类片段的 QA 清单：

- 4 个主时间块都存在，每个时间块至少 3 个子节拍。
- 攻击有命中点，反制有受力点，转场有方向。
- 主角、关键道具和威胁源的空间关系能看懂。
- 台词落点不打断动作，且音色要求用正向描述。
- 结尾仍有运动、威胁或下一段钩子，不靠长特写拖满时间。

短剧 15 秒建议：

- 一段 15 秒最多 4 个镜头；每个镜头写清楚时间点和镜头运动。
- 用“切到/推进/后拉/固定/低角度/中景/特写”等镜头语言，不只写剧情。
- 不要把整张故事板表格图作为参考图上传；它会增加“拉图感”和文字污染风险。
- 图生视频优先上传 3-5 张关键图：首帧、尾帧、本段最关键的角色/动作/场景/道具参考图。
- 如果画面像静态拉伸，下一次减少参考图数量，并把动作、景别变化、镜头切换写进 prompt。
- 如果没有声音，检查命令是否加了 `--generate-audio`；只在 prompt 写音效不会自动生成音频。

`director-promt.txt` 短剧模板：

```text
9:16竖屏AI漫剧视频，时长15秒，720p，3D动画电影风，明显非真人。
参考图按 API 输入顺序使用：参考图1 是本段首帧，锁定 0 秒桥接画面和人物站位；参考图2 是本段尾帧，锁定 15 秒收束画面和下一段衔接；参考图3 是本段关键资产参考图，只用于锁定本段最容易漂移的角色、动作、场景路线或关键道具；如参考图带路线箭头、文字、网格或标注，只用于理解空间/动作/比例，不要画进最终视频。不要把参考图做成静态拉伸，不要上传故事板表格图。

角色锁定：<角色A特征>；<角色B特征>。禁止变脸、换发型、换服装、添加多余面部标记。

0-3 秒：第 0-1 秒 <承接上一段和主体进入>；第 1-2 秒 <威胁出现并锁定目标>；第 2-3 秒 <命中点/受力点 + 主体即时反应>。运镜：<必须看清的因果点>。
3-7 秒：第 3-4 秒 <第一动作>；第 4-5 秒 <攻击命中或受力>；第 5-6 秒 <躲避/格挡/反制>；第 6-7 秒 <造成新局面>。台词落点：<动作条件成立后才说>。
7-11 秒：第 7-8 秒 <新威胁出现>；第 8-9 秒 <目标锁定/命中/受力>；第 9-10 秒 <反制动作>；第 10-11 秒 <威胁被阻断或转入下一动作>。
11-15 秒：第 11-12 秒 <上一动作结果>；第 12-13 秒 <短促情绪钩子或信息揭示>；第 13-14 秒 <新的动作/威胁>；第 14-15 秒 <下一段钩子或清楚转场>。

声音：<风声/环境声/动作声/台词或无台词>。
负面约束：不要字幕，不要水印，不要logo，不要静态图片变形过渡。
```

## 先生成信任图片资产

用 `first-frame.md`、`last-frame.md`、`storyboard.md` 分别生成 Seedream 5.0 lite 平台托管图。图片生成尺寸默认用 `1440x2560`，因为 Seedream 5.0 lite 要求图片面积不低于 3,686,400 像素。

```bash
python3 scripts/ark_image.py \
  --name first-frame-trusted \
  --output-dir stories/<story-id>/episodes/<episode>/segment_01_00-15s/output/trusted-assets \
  --prompt-file stories/<story-id>/episodes/<episode>/segment_01_00-15s/first-frame.md \
  --context-file stories/<story-id>/assets/scenes/<SCENE_ID>/scene-card.md \
  --quiet
```

生成后读取 `output/trusted-assets/trusted-assets.json` 里的 URL，后续传给 Seedance 的是 URL，不是本地下载图。

## 标准视频命令

不要在文档中保存 key。用户已在环境中设置 key 时：

```bash
python3 scripts/ark_video.py submit \
  --segment stories/<story-id>/episodes/<episode>/segment_01_00-15s \
  --model doubao-seedance-2-0-mini-260615 \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --image-url "<Seedream first-frame-trusted url>" \
  --image-url "<Seedream last-frame-trusted url>" \
  --image-url "<Seedream character-or-key-shot url>" \
  --image stories/<story-id>/assets/scenes/<SCENE_ID>/<scene-reference>.png \
  --video-name video-formal-frames-assets-15s.mp4 \
  --last-frame-name last-frame-formal-frames-assets-15s.png \
  --generate-audio \
  --privacy-retry 0 \
  --quiet
```

如果用户明确要求本地图片直传：

```bash
python3 scripts/ark_video.py submit \
  --segment stories/<story-id>/episodes/<episode>/segment_01_00-15s \
  --model doubao-seedance-2-0-mini-260615 \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file stories/<story-id>/episodes/<episode>/segment_01_00-15s/director-promt.txt \
  --image stories/<story-id>/episodes/<episode>/segment_01_00-15s/frames/first-frame.png \
  --image stories/<story-id>/episodes/<episode>/segment_01_00-15s/frames/last-frame.png \
  --image stories/<story-id>/assets/characters/<CHARACTER_ID>/03-360-turnaround/character-turnaround.png \
  --image stories/<story-id>/assets/scenes/<SCENE_ID>/<scene-reference>.png \
  --generate-audio \
  --privacy-retry 0 \
  --quiet
```

提交前可以先 dry-run，确认 payload 结构和参考图选择：

```bash
python3 scripts/ark_video.py submit \
  --segment stories/<story-id>/episodes/<episode>/segment_01_00-15s \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file stories/<story-id>/episodes/<episode>/segment_01_00-15s/director-promt.txt \
  --image <first-frame.png> \
  --image <last-frame.png> \
  --image <segment-critical-character-action-scene-or-prop-reference.png> \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```

按镜头切片的本地图片直传 dry-run 示例，默认首帧、尾帧在前，角色/动作/道具参考在后，并默认生成声音：

```bash
python3 scripts/ark_video.py submit \
  --segment stories/<story-id>/experiments/<episode>/<segment> \
  --model doubao-seedance-2-0-mini-260615 \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file stories/<story-id>/experiments/<episode>/<segment>/director-promt.txt \
  --image stories/<story-id>/experiments/<episode>/<segment>/frames/first-frame.png \
  --image stories/<story-id>/experiments/<episode>/<segment>/frames/last-frame.png \
  --image stories/<story-id>/experiments/<episode>/<segment>/frames/heroine-reference.png \
  --generate-audio \
  --require-images \
  --dry-run
```

如果只提交不轮询：

```bash
python3 scripts/ark_video.py submit \
  --segment stories/<story-id>/episodes/<episode>/segment_01_00-15s \
  --duration 15 \
  --no-poll
```

继续轮询：

```bash
python3 scripts/ark_video.py poll \
  --segment stories/<story-id>/episodes/<episode>/segment_01_00-15s \
  --quiet
```

## 输出位置

成功后重点汇报：

- `output/<video-name>.mp4`
- `output/<last-frame-name>`
- `output/task-id.txt`
- `output/api-submit.json`
- `output/api-result.json`

不要把 `output/` 里的 JSON、视频、签名 URL、任务返回信息加入 Git。

## 失败处理

- `privacy_review_blocked`：说明已被真人隐私审核拦截；立即停止，不要换错图、空镜图或继续重试，要求用户换用平台允许的虚拟角色素材或改模型/平台。
- 本地人脸图被拦截：改走 Seedream 5.0 lite 文生图信任资产 URL，再提交 Seedance。
- `ModelNotOpen`：提示用户在火山控制台开通模型后再试。
- 缺图片：先生成/补齐首帧、尾帧、故事板，再提交视频。
- 视频时长不是 15 秒：检查命令是否显式传入 `--duration 15`，不要把 5 秒 smoke test 当正片。
- 视频没有声音：检查是否传了 `--generate-audio`，并用 `ffprobe` 确认是否存在 audio stream。
- 视频像“拉图”：下一版不要上传故事板表格图；减少参考图到角色图+首帧+尾帧；把每段动作和镜头切换写进 prompt。

## 参考资料

- 火山引擎文档：`https://www.volcengine.com/docs/82379/2291680?lang=zh`
- 火山引擎文档：`https://www.volcengine.com/docs/82379/2222480?lang=zh`
- 火山引擎文档：`https://www.volcengine.com/docs/82379/2298881?lang=zh`

## 交付口径

最终回复必须说明：

- 是否成功生成视频。
- 视频绝对路径。
- 任务 id。
- 实际时长、分辨率、帧率，能用 `ffprobe` 验证时必须验证。
- 如果失败，说明失败类型和停止原因，不要声称已生成正片。
