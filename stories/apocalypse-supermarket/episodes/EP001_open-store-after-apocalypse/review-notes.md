# EP001 生成前审查记录

## 结构检查

- 4 个 15 秒 segment 已生成文档包：
  - `segment_01_00-15s`
  - `segment_02_15-30s`
  - `segment_03_30-45s`
  - `segment_04_45-60s`
- 每段都包含：
  - `storyboard.md`
  - `first-frame.md`
  - `last-frame.md`
  - `prompt.md`
  - `director-promt.txt`
  - `api-request.md`
  - `frames/`
  - `output/`

## 当前状态

- 4 段首帧/尾帧图片已按 AMG 横屏 16:9 重新生成并通过脚本校验。
- Segment 02/03/04 的首帧已继承上一段尾帧，继承哈希记录在 `frame-inheritance-manifest.json`。
- 帧图总览已生成：`EP001-frames-contact-sheet.png`。
- 4 段视频尚未提交 API，`output/` 目录没有 `.mp4`。
- 当前阶段是“文字、资产、首尾帧生产包已就绪”，不是“视频已生成”。

## 已有基础资产

- `assets/characters/AS_LIN_QIAO_001/turnaround.png`：林乔三视图。
- `assets/characters/AS_SECURITY_DRONE_001/turnaround.png`：小秤无人机三视图。
- `assets/scenes/SCENE_FORTIFIED_SUPERMARKET/scene-reference.png`：16:9 横屏末世超市场景参考。
- `assets/props/restock-vfx-reference.png`：16:9 横屏补货特效参考。
- `assets/props/member-card-reference.png`：16:9 横屏旧会员卡和门禁参考。

## 剧情与分镜逻辑

整体逻辑成立：

1. Segment 01：灰雨危机 + 林乔反常开门，5 秒内有钩子。
2. Segment 02：抢货男暴力拿水失败，证明“抢货不算交易”。
3. Segment 03：林乔完成一笔示范交易，货架补满，释放爽点。
4. Segment 04：林乔救老人孩子入店，立规矩，并用旧会员卡抛出父亲线索。

本次已修正：

- Segment 03 原本写“把水推给门口老人”，但 Segment 04 才开门救人，已改成“推到收银台取货区，完成示范交易”。
- Segment 03 尾帧和 Segment 04 首帧已统一为“众人开始排队，林乔抬手准备开门”。
- Segment 04 的“手写店规”已改成“无字图标店规牌”，避免生成可读文字。
- 旧会员卡参考图已补齐，Segment 04 不再只引用文字道具说明。

## 视频提示词风险审查

已按之前经验处理：

- 避免一段塞过多动作，每段只承担一个戏剧任务。
- `director-promt.txt` 已改为横屏 16:9，并按 0-4 / 4-8 / 8-12 / 12-15 秒拆动作；每个时间块内部继续拆到 0.6-0.8 秒级动作因果。
- 每段都补充了运镜、声音、台词落点、移动路线、受力/命中点和尾段推进。
- 补货特效写成“沿价签和货架推进”，避免凭空爆炸或游戏 UI。
- 店规、会员卡、灯箱均要求不出现可读文字和真实品牌。
- 尾段保留开门、贴牌、刷卡、回头动作，不做画面停留。

仍需注意：

- Segment 03 的“整排水补满”是核心爽点，建议正式视频先拆成 5 秒小样验证货架补货是否能读懂。
- Segment 04 的旧会员卡钩子不要让模型生成可读姓名，只保留旧卡、橙色边缘光和林乔反应。
- 如果用 Seedance mini，建议不要一次性连发四段，先生成 Segment 01 或 Segment 03 小样看可读性。

## 推荐下一步

1. 优先用 mini 生成 Segment 03 的 5 秒补货小样，验证爽点。
2. 再按 01 -> 02 -> 03 -> 04 的顺序单段生成，不要一次性连发。
3. 每次重生成某段尾帧后，重新执行 `scripts/link_segment_frames.py` 更新下一段首帧。
4. 正式提交视频时必须使用 `--ratio 16:9 --generate-audio`。
