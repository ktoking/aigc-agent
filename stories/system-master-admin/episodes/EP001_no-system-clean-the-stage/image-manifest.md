# EP001 图像资产清单

## 人类审阅资产

| 类型 | 资产 | 状态 | 用途 |
| --- | --- | --- | --- |
| 角色 | `assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png` | 已生成 | 顾沉人脸与磨损哑黑暗金长工装 |
| 角色 | `assets/characters/SMA_GU_XIAOMAN_001/canonical-turnaround.png` | 已重制 | 唯一有效的暗色冷蓝动漫版顾小满；浅米色旧版已移出项目 |
| 角色 | `assets/characters/SMA_ZHAO_TIANLIN_001/canonical-turnaround.png` | 已生成 | 赵天麟人脸与黑金财团礼服 |
| 场景 | `assets/scenes/SCENE_SYSTEM_WORLD_MONTAGE_001/canonical-concept.png` | 已生成 | 五类系统文明开场 |
| 场景 | `assets/scenes/SCENE_AWAKENING_HALL_001/canonical-concept.png` | 已生成 | Segment 01 顾沉阶级落差收束 |
| 场景 | `assets/scenes/SCENE_LOW_PERMISSION_CLINIC_001/canonical-concept.png` | 已生成 | Segment 02-04 病房主空间 |
| 道具 | 黑金付款卡 | 待定义参考图 | 神豪借款与管理员觉醒媒介 |
| 道具 | `assets/props/PROP_HOST_GOLD_WRISTBAND_001/prop-card.md` | 已定义，参考图待生成 | SSS 宿主锚点 |
| 道具 | 系统稳定剂、缴费屏与拒贷界面 | 待定义参考图 | 顾小满治疗目标与顾沉绝境 |

## 本集首尾帧

| 段落 | 首帧 | 尾帧 | 图片状态 |
| --- | --- | --- | --- |
| Segment 01 | `segment_01_00-15s/frames/first-frame.png` | `segment_01_00-15s/frames/last-frame.png` | 已生成并提交 |
| Segment 02 | `segment_02_15-30s/frames/first-frame.png` | `segment_02_15-30s/frames/last-frame.png` | 已生成并提交 |
| Segment 03 | `segment_03_30-45s/frames/first-frame.png` | `segment_03_30-45s/frames/last-frame.png` | 已生成并提交 |
| Segment 04 | `segment_04_45-60s/frames/first-frame.png` | `segment_04_45-60s/frames/last-frame.png` | 已生成并提交 |

## 视频 API 上传原则

- 每段默认上传该段 `frames/first-frame.png` 和 `frames/last-frame.png`。
- 角色参考图生成后，涉及顾沉和赵天麟的段落追加相应 canonical 角色图。
- Segment 01 追加系统文明蒙太奇参考图，五类宿主只保留剪影。
- Segment 04 复用 Segment 01 五类系统画面做“全部标红”闪回，并追加破损终端参考图。
- 不上传 `frames/storyboard-sheet.png`，避免文字、箭头和表格污染视频。

## 缺失项

- 黑金付款卡、系统稳定剂、缴费屏和金色腕环尚无独立道具图；当前关键帧与视频内已有可用视觉锚点。

## 生成记录

- 顾沉、顾小满、赵天麟 canonical 人物三视图已落位。
- 2026-07-31：Segment 01 首帧、尾帧、系统文明场景与觉醒礼堂场景均已用内置 imagegen 生成并落位，统一采用用户指定的暗黑都市幻想动漫风格。
- 2026-07-31：Segment 01 已按 `director-promt.txt` 提交 Seedance 2.0 Mini，480p、15 秒、9:16、有声音；任务 ID 仅保留于已忽略的 `output/`。
- 2026-07-31：删除浅米色旧版顾小满三视图，重制并落位暗色冷蓝动漫版 `SMA_GU_XIAOMAN_001/canonical-turnaround.png`，旧版不再参与任何视频参考。
- 2026-07-31：低权限病房母版与 Segment 02-04 全部首尾关键帧已生成；错误银发顾小满中间图已作废且未落入项目。
- 2026-07-31：Segment 02 已生成成功；实测 496×864、15.104 秒、H.264、AAC 双声道；任务 ID 仅保留于已忽略的 `output/`。
- 2026-07-31：Segment 03 已生成成功；实测 496×864、15.104 秒、H.264、AAC 双声道；任务 ID 仅保留于已忽略的 `output/`。
- 2026-07-31：Segment 04 参数与五张参考图预检通过，首次提交因账户计费状态被平台拒绝，未创建视频任务。
- 2026-07-31：账户恢复后重新提交 Segment 04 成功；实测 496×864、15.104 秒、H.264、AAC 双声道。所有参考资产图均来自本地内置 ImageGen，Seedance 仅用于视频生成；任务 ID 仅保留于已忽略的 `output/`。
- 2026-07-31：Segment 01-04 已无损拼接为 `output/EP001-complete-01-04.mp4`；总时长 60.448 秒，文件大小 29,421,226 字节，SHA-256：`20e94381f691d7b4acf9fa6a2899dfc57ec2bd126f55cb519b7a4c4aa3a6f9bd`。
