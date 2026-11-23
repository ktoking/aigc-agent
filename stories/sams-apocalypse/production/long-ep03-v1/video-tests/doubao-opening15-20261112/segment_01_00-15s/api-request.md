# 首次图生视频测试

用户授权：2026-11-12，指定 long-ep03-v1 开头15秒。

本机账号池 API，Mini，16:9，p001/p002/p003 分镜各自单图，提示词时长6/6/4秒，计划剪至15秒。当前无独立 duration 或多图参数；模型实际时长需测。

先提交p001，具体受理/状态见 `output/p001/api-submit.json` 与 `api-result.json`。不记录API密钥、Cookie、Token或临时远程媒体URL。不存在去水印Token，生成和取片分别验收，平台失败时不盲目重复消耗额度。

## 实测结论

四次本地请求未通过平台提交前门禁，均已退回本地预扣；尚无视频产物。具体见 `../RESULT.md`、`../manifest.json` 及各 `output/p001/attempt-*` 记录。重启修复了本次主窗口销毁导致的HTTP500，但网页视频模式识别仍失败；未改动服务源码。

## 2026-11-13 真实测试

账号001，Mini，16:9，p001单图。requestId：doubao-20c8a98dc1234677。第五次本地提交已受理，已到上传参考图、填写提示词和触发发送；截至本记录尚未确认平台视频任务启动。记录见output/p001/attempt-05。只跟踪同一任务，不重复生成。

## 2026-11-13 最终结论（覆盖前文待验证状态）

三镜均已真实生成并下载官方原始MP4：

- p001：doubao-20c8a98dc1234677，output/p001/attempt-05/。
- p002：doubao-317a073325a34a1d，output/p002/。
- p003：doubao-d0a6d888fe7743fe，output/p003/。

均为账号001、Mini、16:9。API本地受理/上传参考图/填写提示词/网页生成/官方分享已完成，最终API错误统一为watermark/token_missing；api-result.json真实保留failed，不伪改为成功。本地额度未退款。本次未验证多账号轮换。

save_official_video.py从官方分享页提取官方导出资源，无第三方解析，无水印处理。各原片10.08秒、1280×720、24fps，三段完整解码通过。模型没有真实duration参数，本次原生时长未按提示词6/6/4秒执行。assemble_test.py剪成15秒、30fps、450帧，复用原旁白与烧录中文字幕，成片output/video-test-15s.mp4。无新配音调用，不重复提交。最终QA和媒体摘要见../qa/final-summary.json、../RESULT.md。
