# EP003 图像资产清单

## 人类审阅资产

| 类型 | 资产 | 状态 | 用途 |
| --- | --- | --- | --- |
| 风格 | `assets/style/user-anime-style-reference.png` | 已有 | 暗黑都市幻想动漫总风格 |
| 角色 | `assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png` | 已有 | 顾沉人脸与工装锁定 |
| 角色 | `assets/characters/SMA_ZHAO_TIANLIN_001/canonical-turnaround.png` | 已有 | 赵天麟人脸、黑金礼服与腕环锁定 |
| 角色 | `assets/characters/SMA_GU_XIAOMAN_001/canonical-turnaround.png` | 已有 | 病房通话镜头锁定 |
| 场景 | `assets/scenes/SCENE_TIANYAO_GALA_SERVICE_CORRIDOR_001/canonical-concept.png` | 已生成并目检 | Segment 02-04 宴会后勤空间 |
| 道具 | `assets/props/PROP_MEDICAL_FUND_WINE_CRATE_001/canonical-concept.png` | 已生成并目检 | 酒箱、三瓶酒与医疗封签尺度 |

## 本集首尾帧

| 段落 | 首帧 | 尾帧 | 状态 |
| --- | --- | --- | --- |
| Segment 01 | `segment_01_00-15s/frames/first-frame.png` | `segment_01_00-15s/frames/last-frame.png` | 已生成并目检 |
| Segment 02 | `segment_02_15-30s/frames/first-frame.png` | `segment_02_15-30s/frames/last-frame.png` | 已生成并目检 |
| Segment 03 | `segment_03_30-45s/frames/first-frame.png` | `segment_03_30-45s/frames/last-frame.png` | 已生成并目检 |
| Segment 04 | `segment_04_45-60s/frames/first-frame.png` | `segment_04_45-60s/frames/last-frame.png` | 已生成并目检 |

## 连续性复用

- Segment 02 首帧继承 Segment 01 尾帧中的酒箱和抱姿，但地点切到财团塔后勤闸机。
- Segment 03 首帧复用 Segment 02 尾帧。
- Segment 04 首帧使用 Segment 03 尾帧的顾沉、酒箱与资金链视觉状态生成后勤门抵达画面。
- 每段默认上传首尾帧，并按人物漂移风险追加顾沉、赵天麟或酒箱 canonical 图。

## 生成记录

- 2026-08-01：所有新增图片均使用本地内置 ImageGen 生成，未调用豆包图片模型。
- 2026-08-01：宴会后勤走廊母版、酒箱母版与本集关键帧已落位。
- 2026-08-01：后勤闸机帧已重绘为双臂抱箱；尾帧酒瓶数量已修正为一瓶已开、两瓶未开，总数三瓶。
