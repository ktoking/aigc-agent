# 《裂界行者 / Rift Breakers》OP 生产交接文档

> 本文档供另一个 AI/人工接手时快速了解项目状态、已完成工作和后续步骤。
> 最后更新：2026-09-19（v2 合成）

## 项目一句话

90秒日式热血都市异能动画OP，30个镜头，16:9横屏，Blue Lock（ブルーロック）画风，195BPM女声嘶吼版J-Rock BGM。无对白无字幕，全靠画面卡点。

## 项目根路径

```
/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rift-breakers/
```

---

## 当前进度总览

| 阶段 | 状态 | 说明 |
|---|---|---|
| P0 骨架 + director prompt | ✅ 完成 | 3个segment的逐镜头导演prompt已写好 |
| P1 角色资产图 | ✅ 完成 | 每segment 6张角色立绘（共18张） |
| P2 关键帧图 | ✅ 完成 | 30个镜头全覆盖（每segment 10张） |
| P3 视频生成 | ✅ 完成 | Seg01/Seg02/Seg03 三段720p成片齐 |
| P4 后期拼接+卡点 | ✅ 完成 | 三段升频1080p硬切拼接+BGM+标题落版，精确90.000s |
| P5 交付 | ✅ 完成 | `episodes/OP00_opening/output/OP00_rift-breakers_90s_1080p.mp4`（v2 成片） |

### 迭代记录

- **v2（2026-09-19）**：三段整段用 seedance_2.5 重做后重新合成。三段均为 721 帧，统一 `select='lt(n,720)'` 裁到 720 帧=30.000s，硬切 concat 后 2160 帧=精确 90.000s；BGM `atrim=0:90` 锁定，0:30 / 1:00 边界对齐 BGM 段落切换。复用 `title_card.png`，标题 86.0s 起 0.2s 淡入至 90.0s。v1 成片保留为 `.v1-backup`（勿动）。
- **已知偏差（v2 直接用，不重做）**：L25 六格群像 montage 被模型跳过，Seg03 约 13.5s 处重复了夜臣斩击镜头；另新段背景模型自行烧入若干环境霓虹招牌/竖排日文文字（画面内景，非叠加字幕）。

---

## 已完成产物明细

### 关键帧图 — 30/30 全覆盖 ✅

每个segment的 `frame/` 目录下有10张关键帧（命名格式：`序号_镜头号_描述.png`）：

**Segment 01 (00-30s) — 路径：`episodes/OP00_opening/segment_01_00-30s/frame/`**
| 文件 | 镜头 | 内容 |
|---|---|---|
| 01_l01_aerial-rift.png | L01 | 高空俯冲俯瞰黄昏都市+天空裂缝 |
| 02_l02_train-reflection.png | L02 | 地铁车窗映出男主侧脸+蓝火眼 |
| 03_l03_against-the-crowd.png | L03 | 男主低机位逆人潮行走 |
| 04_l04_sky-anomaly.png | L04 | 男主抬头天空扭曲异象 |
| 05_l05_mio-rooftop.png | L05 | 女主天台夕阳回头亮相 |
| 06_l06_mio-barrier.png | L06 | 女主指尖展开透明几何结界 |
| 07_l07_hayato-landing.png | L07 | 赤城高架桥跃下橙红能量喷射 |
| 08_l08_yakumo-draw.png | L08 | 夜臣暴雨巷口拔刀白色裂纹 |
| 09_l09_makoto-command.png | L09 | 雾原监控室关屏反光 |
| 10_l10_kokuyou-rooftop.png | L10 | 黑曜背对镜头摩天楼顶黑紫核心 |

**Segment 02 (30-60s) — 路径：`episodes/OP00_opening/segment_02_30-60s/frame/`**
| 文件 | 镜头 | 内容 |
|---|---|---|
| 01_l11_six-beat-montage.png | L11 | 六格闪切montage |
| 02_l12_bridge-team.png | L12 | 天桥四人并肩夕阳行走 |
| 03_l13_classroom-glance.png | L13 | 教室澪看书男主回头 |
| 04_l14_training-spar.png | L14 | 训练场赤城冲拳男主闪避 |
| 05_l15_yakumo-rooftop.png | L15 | 夜臣楼顶风衣飘扬扶刀远望 |
| 06_l16_badge-clue.png | L16 | 桌面徽章俯拍悬念 |
| 07_l17_kokuyou-smile.png | L17 | 黑曜侧脸微笑裂界怪物红眼 |
| 08_l18_frozen-crossing.png | L18 | 时间冻结十字路口 |
| 09_l19_inverted-monster.png | L19 | 天空碎裂怪物倒挂俯冲 |
| 10_l20_mio-shield.png | L20 | 澪半球结界挡怪物 |

**Segment 03 (60-90s) — 路径：`episodes/OP00_opening/segment_03_60-90s/frame/`**
| 文件 | 镜头 | 内容 |
|---|---|---|
| 01_l21_hayato-charge.png | L21 | 赤城橙红能量冲锋撞怪 |
| 02_l22_yakumo-spatial-cut.png | L22 | 夜臣横斩刀光空间切开 |
| 03_l23_rinto-awakening.png | L23 | 男主觉醒界焰+黑裂纹蔓延 |
| 04_l24_rinto-sprint.png | L24 | 男主超低机位高速冲刺 |
| 05_l25_chorus-montage.png | L25 | 副歌群像快切montage |
| 06_l26_destiny-clash.png | L26 | 男主vs黑曜宿命对冲 |
| 07_l27_memory-shards.png | L27 | 记忆碎片闪回montage |
| 08_l28_rift-gate.png | L28 | 巨大裂界之门男主背影 |
| 09_l29_team-assembly.png | L29 | 五人群像裂界之门前集结 |
| 10_l30_final-charge.png | L30 | 全员冲锋男主回头定格 |

### 角色资产图 — 每segment 6张
每segment的 `frame/` 目录下另有6张角色立绘（`character_*.png`），用于角色一致性参考。

### 视频产物

| Segment | 视频文件 | 规格 | 状态 |
|---|---|---|---|
| 01 (00-30s) | `segment_01_00-30s/output/video-30s.mp4` | 1280×720 24fps HEVC 30s ~11.3MB（v2 seedance_2.5） | ✅ 已完成 |
| 02 (30-60s) | `segment_02_30-60s/output/video-30s.mp4` | 1280×720 24fps HEVC 30s ~10.4MB（v2 seedance_2.5） | ✅ 已完成 |
| 03 (60-90s) | `segment_03_60-90s/output/video-30s.mp4` | 1280×720 24fps HEVC 30s ~13.0MB（v2 seedance_2.5，含 L25 偏差） | ✅ 已完成 |
| **最终成片** | `OP00_opening/output/OP00_rift-breakers_90s_1080p.mp4` | 1920×1080 24fps H.264 90s + AAC BGM ~87.7MB（v2） | ✅ 已交付 |

### BGM

- **文件**：`assets/audio/bgm-v3.wav`
- **规格**：WAV, 90.0秒（精确1:30），13.7MB
- **版本**：V3 高速女声嘶吼版，195BPM J-Rock
- **卡点结构**：
  - 0:00-0:10 前奏（失真吉他riff+双踩鼓点炸入）
  - 0:10-0:30 A段（女声"いつもの帰り道…"）
  - 0:30-0:48 B段（鼓组double time，群像快闪）
  - 0:48-1:08 预副歌（配器收窄→心跳底鼓→上升白噪音）
  - 1:08-1:26 副歌爆发（女声嘶吼"裂けた空の向こうへ…"）
  - 1:26-1:30 尾奏（撕裂高音"Rift Breakers!"硬切）

---

## 关键文件位置（接手必读）

| 文件 | 作用 |
|---|---|
| `AGENTS.md` | 剧本专属规则（硬约束、BGM卡点表、目录结构） |
| `assets/style/global-style-prefix.txt` | **全局风格总控**，含6角色完整锚定描述+负面词 |
| `assets/audio/bgm-v3.wav` | **BGM**，90秒完整版 |
| `episodes/OP00_opening/segment_01_00-30s/director-promt.txt` | L01-L10 逐镜头导演prompt |
| `episodes/OP00_opening/segment_02_30-60s/director-promt.txt` | L11-L20 逐镜头导演prompt |
| `episodes/OP00_opening/segment_03_60-90s/director-promt.txt` | L21-L30 逐镜头导演prompt |

---

## 6角色外观锚点（每次生成必须复述）

- **神崎凛斗（男主）**：17岁，黑色略乱短发，冷静倔强眼神，深色高中制服外套半敞内搭浅色上衣，蓝白色界焰能量，失控时半边手臂黑色裂纹
- **天野澪（女主）**：17岁，黑色长直发及腰，红色瞳孔，清冷五官，深色校服小耳坠，透明几何结界
- **赤城隼（搭档）**：18岁，红色短刺猬发，狂放笑容，运动型身材，深色战斗服，橙红推进能量
- **白峰夜臣（强者）**：20岁，白色中长发及肩，冷淡锐利，黑色长风衣及膝，长刀，白色空间裂纹斩击
- **雾原真琴（导师）**：28岁，短深色发，深色长外套手套，沉稳
- **黑曜（反派）**：黑衣金纹，黑色长发金色眼瞳，优雅危险，黑紫色裂界能量

---

## Blue Lock 画风关键词（每张prompt必带）

**开头英文前缀**：
```
Blue Lock anime style, ブルーロック animation art, Japanese TV anime cel shading, sharp clean lineart, cold blue-grey palette, hand-drawn feel
```

**画风特征**：
- 日式TV动画赛璐璐风格，线条清晰利落
- 人物五官偏锐利狭长，眼睛细长有棱角，眉毛锋利
- 面部光影硬朗，明暗交界线清晰，皮肤不光滑油亮
- 整体偏冷调，大面积深蓝/黑/灰，高饱和电光蓝作为主能量色
- 背景现代都市/废墟，笔触有手绘感，非照片写实
- 前倾透视、速度线、飞溅粒子，保持动画手绘质感

**结尾负面词（每条必带）**：
```
no plastic skin, no 3D render, no over-sharpen, no mesh texture, no AI artifacts, no chibi, no deformed face, no extra fingers, no oversaturated, no HDR, no figurine look, no smooth plastic texture, no mesh grid texture
```

---

## 下一步要做什么

### 1. 生成 Segment 02 视频（30-60s）

- 输入：`segment_02_30-60s/frame/` 下的10张关键帧
- 用 Seedance 图生视频，每张关键帧生成对应时长的动态片段
- 视频 prompt 从 `segment_02_30-60s/director-promt.txt` 提取镜头描述
- 输出到 `segment_02_30-60s/output/`（需创建目录）
- 参考 Seg01 已完成的 `video-30s.mp4` 作为风格和时长基准

### 2. 生成 Segment 03 视频（60-90s）

- 输入：`segment_03_60-90s/frame/` 下的10张关键帧
- 同上流程，输出到 `segment_03_60-90s/output/`

### 3. 后期拼接 + BGM 卡点

- 三段视频拼接成90秒完整OP
- 用 `assets/audio/bgm-v3.wav` 作为音轨
- 按BGM卡点表对齐镜头切换时间点：
  - 0:00 / 0:10 / 0:30 / 0:48 / 1:08 / 1:26 / 1:30 为段落切换点
  - 段内每2.5-3秒一个镜头切换（卡鼓点）
- 尾帧加标题落版《裂界行者》
- 输出最终 1080p 版本

### API 调用备注

- 模型：Seedance 2.0-mini `doubao-seedance-2-0-mini-260615`（草稿主力）
- 定稿镜头可用标准 Seedance 2.0 / 2.0 Fast
- API key：从 macOS Keychain `codex-ark-api-key` 读取，注入 `ARK_API_KEY`
- 可用 `ARK_VIDEO_MODEL` 环境变量临时覆盖默认模型

---

## 硬约束速查

1. 90秒OP，30镜头，16:9横屏，2D赛璐璐
2. BGM 195BPM 女声嘶吼版，所有切镜卡鼓点
3. 无对白无旁白无字幕
4. 角色跨镜头长相服装发色瞳色必须稳定
5. 能力配色固定：界焰=蓝白、结界=透明几何、赤城=橙红、夜臣=白色裂纹、黑曜=黑紫
6. 图片生成避免过度锐化/鱼鳞网格/满屏微纹理/塑料质感
7. 不接Skynet统计，git commit用 --no-verify
