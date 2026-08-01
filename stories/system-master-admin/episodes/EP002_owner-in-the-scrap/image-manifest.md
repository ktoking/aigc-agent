# EP002 图像资产清单

## 人类审阅资产

| 类型 | 资产 | 状态 | 用途 |
| --- | --- | --- | --- |
| 风格 | `assets/style/user-anime-style-reference.png` | 已有 | 暗黑都市幻想动漫总风格 |
| 角色 | `assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png` | 已有 | 顾沉脸与服装锁定 |
| 角色 | `assets/characters/SMA_GU_XIAOMAN_001/canonical-turnaround.png` | 已有 | 顾小满黑发病号服锁定 |
| 场景 | `assets/scenes/SCENE_LOW_PERMISSION_CLINIC_001/canonical-concept.png` | 已有 | Segment 01 病房 |
| 场景 | `assets/scenes/SCENE_SYSTEM_RECYCLE_STATION_001/canonical-concept.png` | 已生成并目检 | Segment 01 尾部至 Segment 04 主空间 |
| 道具 | `assets/props/PROP_DISCARDED_SYSTEM_CORE_001/canonical-concept.png` | 已生成并目检 | 废核心外观与尺度锁定；已移除设计稿文字版 |

## 本集首尾帧

| 段落 | 首帧 | 尾帧 | 状态 |
| --- | --- | --- | --- |
| Segment 01 | `segment_01_00-15s/frames/first-frame.png` | `segment_01_00-15s/frames/last-frame.png` | 已生成并目检 |
| Segment 02 | `segment_02_15-30s/frames/first-frame.png` | `segment_02_15-30s/frames/last-frame.png` | 已生成并目检 |
| Segment 03 | `segment_03_30-45s/frames/first-frame.png` | `segment_03_30-45s/frames/last-frame.png` | 已生成并目检 |
| Segment 04 | `segment_04_45-60s/frames/first-frame.png` | `segment_04_45-60s/frames/last-frame.png` | 已生成并目检 |

## 连续性复用

- Segment 02 首帧复用 Segment 01 尾帧。
- Segment 03 首帧复用 Segment 02 尾帧。
- Segment 04 首帧复用 Segment 03 尾帧。
- 每段视频默认上传该段首尾帧，再按漂移风险追加顾沉、场景或废核心 canonical 图。

## 生成记录

- 2026-08-01：所有新增图片均使用本地内置 ImageGen 生成，未调用豆包图片模型。
- 2026-08-01：回收站母版、废核心母版与五张独立边界关键帧已落位；三处跨段首帧复用上一段尾帧。
- 2026-08-01：回收站门牌英文已通过局部重绘移除；废核心第一版文字设计稿未落入项目。
