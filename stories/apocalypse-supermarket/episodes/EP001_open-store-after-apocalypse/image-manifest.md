# EP001 图片资产清单

## 已生成基础资产

- `assets/characters/AS_LIN_QIAO_001/turnaround.png`：林乔三视图。
- `assets/characters/AS_SECURITY_DRONE_001/turnaround.png`：小秤三视图。
- `assets/scenes/SCENE_FORTIFIED_SUPERMARKET/scene-reference.png`：16:9 横屏超市场景。
- `assets/props/restock-vfx-reference.png`：16:9 横屏补货特效参考。
- `assets/props/member-card-reference.png`：16:9 横屏旧会员卡和门禁读卡器参考。

## EP001 首尾帧规则

- 每个 segment 必须有 `frames/first-frame.png` 和 `frames/last-frame.png`。
- 除 Segment 01 外，后续 segment 的首帧必须继承上一 segment 的尾帧。
- 执行脚本：`python3 scripts/link_segment_frames.py <episode_dir> --apply --overwrite`。
- 继承记录：`frame-inheritance-manifest.json`。
- 帧图校验：`frame-verification.json`。
- 总览图：`EP001-frames-contact-sheet.png`。
- AMG 横屏规范：所有首尾帧必须通过 `--aspect 16:9` 校验。

## EP001 已生成帧图

- Segment 00：灰雨街道失序 / 林乔准备开门。
- Segment 01：灰雨夜开门 / 抢货男冲向水架。
- Segment 02：抢货失败 / 林乔举扫码枪。
- Segment 03：扫码交易 / 货架补满。
- Segment 04：救人入店 / 父亲会员卡刷门。

## 继承关系

- `segment_01_00-15s/frames/last-frame.png` -> `segment_02_15-30s/frames/first-frame.png`
- `segment_02_15-30s/frames/last-frame.png` -> `segment_03_30-45s/frames/first-frame.png`
- `segment_03_30-45s/frames/last-frame.png` -> `segment_04_45-60s/frames/first-frame.png`
