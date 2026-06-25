# SF001 图片资产清单

## 生成基准

- 清理范围: 已清空各段 `frames/` 目录下旧版图片，再重新生成本清单中的故事板图。
- 角色主参考: `../../assets/characters/LMR_COURIER_BOT_001/01-locked-reference/main-reference.png`
- 角色三视图: `../../assets/characters/LMR_COURIER_BOT_001/02-turnaround/turnaround-sheet.png`
- 角色动作表: `../../assets/characters/LMR_COURIER_BOT_001/03-action-sheet/action-sheet.png`
- 场景锚点图: `../../assets/scenes/SCENE_RUINED_DELIVERY_CITY/scene-anchor-sheet.png`
- 统一要求: 后续所有图必须使用同一个小型白橙送餐机器人、同一个橙色记忆餐箱、同一套湿冷夜晚废墟配送城。

## 分段故事板图

| 段落 | 图片 | Prompt 记录 |
| --- | --- | --- |
| 01 | `segment_01_00-15s/frames/storyboard.png` | `segment_01_00-15s/frames/storyboard.prompt.txt` |
| 02 | `segment_02_15-30s/frames/storyboard.png` | `segment_02_15-30s/frames/storyboard.prompt.txt` |
| 03 | `segment_03_30-45s/frames/storyboard.png` | `segment_03_30-45s/frames/storyboard.prompt.txt` |
| 04 | `segment_04_45-60s/frames/storyboard.png` | `segment_04_45-60s/frames/storyboard.prompt.txt` |
| 05 | `segment_05_60-75s/frames/storyboard.png` | `segment_05_60-75s/frames/storyboard.prompt.txt` |
| 06 | `segment_06_75-90s/frames/storyboard.png` | `segment_06_75-90s/frames/storyboard.prompt.txt` |
| 07 | `segment_07_90-105s/frames/storyboard.png` | `segment_07_90-105s/frames/storyboard.prompt.txt` |
| 08 | `segment_08_105-120s/frames/storyboard.png` | `segment_08_105-120s/frames/storyboard.prompt.txt` |
| 09 | `segment_09_120-135s/frames/storyboard.png` | `segment_09_120-135s/frames/storyboard.prompt.txt` |
| 10 | `segment_10_135-150s/frames/storyboard.png` | `segment_10_135-150s/frames/storyboard.prompt.txt` |

## 验收记录

- 图片数量: 10 张分段故事板图。
- 首尾帧数量: 20 张，覆盖 10 个 segment 的 `first-frame.png` 和 `last-frame.png`。
- 图片尺寸: 全部为 1672x941，横屏 16:9。
- 连续性抽查: 主角外形、蓝色眼灯、白橙涂装、橙色记忆餐箱、湿冷废墟城场景基调保持一致。


## 动作指导建议图

| 段落 | 图片 | 源文件 | 说明 |
| --- | --- | --- | --- |
| 01 | `segment_01_00-15s/frames/action-guide.png` | `segment_01_00-15s/frames/action-guide.svg` | 用于打斗/运动方向、爆点和镜头调度参考，不作为首尾帧 |
| 02 | `segment_02_15-30s/frames/action-guide.png` | `segment_02_15-30s/frames/action-guide.svg` | 用于打斗/运动方向、爆点和镜头调度参考，不作为首尾帧 |
| 03 | `segment_03_30-45s/frames/action-guide.png` | `segment_03_30-45s/frames/action-guide.svg` | 用于打斗/运动方向、爆点和镜头调度参考，不作为首尾帧 |
| 05 | `segment_05_60-75s/frames/action-guide.png` | `segment_05_60-75s/frames/action-guide.svg` | 用于打斗/运动方向、爆点和镜头调度参考，不作为首尾帧 |
| 06 | `segment_06_75-90s/frames/action-guide.png` | `segment_06_75-90s/frames/action-guide.svg` | 用于打斗/运动方向、爆点和镜头调度参考，不作为首尾帧 |
| 07 | `segment_07_90-105s/frames/action-guide.png` | `segment_07_90-105s/frames/action-guide.svg` | 用于打斗/运动方向、爆点和镜头调度参考，不作为首尾帧 |
| 08 | `segment_08_105-120s/frames/action-guide.png` | `segment_08_105-120s/frames/action-guide.svg` | 用于打斗/运动方向、爆点和镜头调度参考，不作为首尾帧 |

## 清理记录

- 已移除上一版由 `storyboard.png` 裁切派生的错误首尾帧；现已使用内置 image 模型重新生成与 `storyboard.png` 同画风同质量的正式首尾帧。

## 分段首尾帧图

| 段落 | 首帧 | 尾帧 | Prompt 记录 | 状态 |
| --- | --- | --- | --- | --- |
| 01 | `segment_01_00-15s/frames/first-frame.png` | `segment_01_00-15s/frames/last-frame.png` | `segment_01_00-15s/frames/first-frame.prompt.txt`, `segment_01_00-15s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 02 | `segment_02_15-30s/frames/first-frame.png` | `segment_02_15-30s/frames/last-frame.png` | `segment_02_15-30s/frames/first-frame.prompt.txt`, `segment_02_15-30s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 03 | `segment_03_30-45s/frames/first-frame.png` | `segment_03_30-45s/frames/last-frame.png` | `segment_03_30-45s/frames/first-frame.prompt.txt`, `segment_03_30-45s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 04 | `segment_04_45-60s/frames/first-frame.png` | `segment_04_45-60s/frames/last-frame.png` | `segment_04_45-60s/frames/first-frame.prompt.txt`, `segment_04_45-60s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 05 | `segment_05_60-75s/frames/first-frame.png` | `segment_05_60-75s/frames/last-frame.png` | `segment_05_60-75s/frames/first-frame.prompt.txt`, `segment_05_60-75s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 06 | `segment_06_75-90s/frames/first-frame.png` | `segment_06_75-90s/frames/last-frame.png` | `segment_06_75-90s/frames/first-frame.prompt.txt`, `segment_06_75-90s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 07 | `segment_07_90-105s/frames/first-frame.png` | `segment_07_90-105s/frames/last-frame.png` | `segment_07_90-105s/frames/first-frame.prompt.txt`, `segment_07_90-105s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 08 | `segment_08_105-120s/frames/first-frame.png` | `segment_08_105-120s/frames/last-frame.png` | `segment_08_105-120s/frames/first-frame.prompt.txt`, `segment_08_105-120s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 09 | `segment_09_120-135s/frames/first-frame.png` | `segment_09_120-135s/frames/last-frame.png` | `segment_09_120-135s/frames/first-frame.prompt.txt`, `segment_09_120-135s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
| 10 | `segment_10_135-150s/frames/first-frame.png` | `segment_10_135-150s/frames/last-frame.png` | `segment_10_135-150s/frames/first-frame.prompt.txt`, `segment_10_135-150s/frames/last-frame.prompt.txt` | 已使用内置 image 模型正式生成；与 `storyboard.png` 同画风同质量，不是示意图或裁切图 |
