# Segment03当前状态｜v7重做

旧视频：提交成功，但2026-11-04按用户反馈及连续抽帧判为QUALITY_REJECTED。output/video.mp4保留原文件，不作为通过样片。

新版：导演提示、分镜、5张角色/结构输入和动作首帧已更新；尚未提交新版视频。正式输入顺序见../../../production/v7/segment03-rework/input-map.json。不得把旧版SUBMITTED_SUCCESS作为新版通过状态。

## 原提交记录（保留原文）

# 当前第03段请求状态

SUBMITTED_SUCCESS。2026-11-04 16:10 提交豆包图生视频（image_to_video），模型 Seedance 2.5，30秒、16:9，全片60—90秒，v4-in-place。

- 提示词：director-promt.txt 全文（图像锁v6 + 七名角色定义 + 八段导演正文 + 禁止项），前置补充 `<图片1>`—`<图片10>` 顺序绑定说明；去掉“输入职责计划／当前不提交API”等制作备注。
- 参考输入：10 张 v6 关键帧（current-references-v2/ref-01～ref-10，排除 discarded-v1），上传后逐张核验与本地文件一致（像素差 0.0）。
- 生成结果：https://aka.doubaocdn.com/s/3VxNZnW3ER
- 本地产物：output/video.mp4（5,446,519 字节）
- 实测规格：1280×720、30.048s、24fps、AAC 44.1kHz 双声道。
- 抽帧核验（1/4/7/11/17/21/25/29.5s）：石环与陨石、三头龙、机器人体四弹、藤束与烧断、龙裔变装、刺客与支援者协商均在位；画面无字幕与水印。
- 定额消耗：本轮成功占用 1 条视频额度。
