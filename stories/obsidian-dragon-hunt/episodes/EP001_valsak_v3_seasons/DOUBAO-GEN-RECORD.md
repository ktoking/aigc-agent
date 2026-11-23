# EP001 视频生成记录

## 生成时间
- 首轮：2026-11-04（segment_01 成功，seg02-04 因额度阻塞）
- 第二轮：2026-11-04 11:12（seg02 成功，seg03/04 仍因额度阻塞）
- 第三轮：2026-11-04（seg03 因参考图人脸合规拦截；seg04 因豆包订阅专属能力拦截；均未生成）
- 第四轮：2026-11-04（用户处理后重试：seg03 人脸合规已通过，但 seg03 仍被"豆包订阅专属能力"拦截，禁止自动重试；seg04 同功能门槛，未重复提交）
- 第五轮：2026-11-04 16:10（seg03 与 seg04 并行提交；seg03 成功，seg04 返回"近 7 天额度已用完"）
- 第六轮：2026-11-04 16:14（用户要求继续，seg04 复用同方案与已上传 URL 重提，仍为同一额度拦截，已停止不再重试）

## 模型与参数
- 实际使用：seedance_2.5 / 30s / 16:9
- 回退：seedance_2.0_fast / 15s（未授权降级，不使用）

## 各段状态

| Segment | 时间段 | 模型 | 状态 | 产物路径 |
|---------|--------|------|------|----------|
| segment_01 | 00-30s | seedance_2.5 / 30s | ✅ 已完成 | output/video.mp4 (5.5MB) |
| segment_02 | 30-60s | seedance_2.5 / 30s | ✅ 已完成 | output/video.mp4 (5.1MB / 5,326,954 bytes) |
| segment_03 | 60-90s | seedance_2.5 / 30s | ✅ 已完成 | output/video.mp4 (5,446,519 bytes) |
| segment_04 | 90-120s | seedance_2.5 / 30s | ❌ 视频额度不足 | 待额度恢复后复用已备方案生成 |

## Segment 01 详情
- 原始URL：https://aka.doubaocdn.com/s/AFOBiDrT9y
- 参考图：10张（current-references-v2/ref-01~10.png）
- 本地路径：segment_01_00-30s/output/video.mp4

## Segment 02 详情（2026-11-04 11:12 生成）
- 原始URL：https://aka.doubaocdn.com/s/Nh7XZ8R5lv
- 参考图：10张（current-references-v2/ref-01~10.png，已排除 discarded-v1）
- Prompt：director-promt.txt 完整原文（8155 字节），未精简
- 本地路径：segment_02_30-60s/output/video.mp4
- 分辨率：1280×720，30s，16:9
- 一次性生成成功，无审核拦截

## Segment 03 详情（2026-11-04 16:10 生成）
- 原始URL：https://aka.doubaocdn.com/s/3VxNZnW3ER
- 参考图：10张（current-references-v2/ref-01~10.png，已排除 discarded-v1），上传后逐张核验与本地一致
- Prompt：director-promt.txt 全文 + `<图片1>`—`<图片10>` 顺序绑定，去掉制作备注
- 本地路径：segment_03_60-90s/output/video.mp4
- 规格：1280×720、30.048s、24fps、AAC 44.1kHz 双声道
- 抽帧核验：石环陨石、三头龙、机械体四弹、藤束与烧断、龙裔变装、刺客与支援者协商均在位；无字幕、无可见水印
- 与 seg04 同轮并行提交，seg03 抢到当轮最后一条额度

## Segment 04 阻塞
- 16:10 与 seg03 并行提交：返回"近 7 天额度已用完"，无 task 返回
- 16:14 用户要求继续：复用同方案与同一批参考图 URL（已验证 302 跳转正常）再次提交，仍为同一提示，工具明确要求不自动重试，已停止
- 方案与素材已完全就绪：director-promt.txt 全文、10 张 v6 关键帧、URL 列表见 segment_04_90-120s/api-request.md
- 额度恢复后可直接提交，无需重传参考图

## 当前进度
- EP001 四段：3/4 已完成（seg01 + seg02 + seg03）
- 待办：segment_04 待视频额度恢复后提交
