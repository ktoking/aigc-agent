# 第1集 · 1.3倍版本验证

- PASS：确认稿正文逐字未改，原音频和原成片保留。
- PASS：Chinese_worker_male；供应商原请求speed=1.0，后期atempo=1.3保音调。
- PASS：135段加速音频完整解码，无削波；10集全部尾音可容纳于新时间线。
- PASS：第1集102秒、3060帧、1920×1080/30fps、21张独立图片hash；1路音频、0字幕流，完整解码。
- PASS：浏览器实际播放加速后的文件，播放器rate=1、未静音、已正常播放至102秒结尾、ended=true、无媒体错误。
- NOT_RUN：完整人工听音、全片人工观看和用户节奏审美验收；自动播放不替代听音。

后续图片使用production/user-script-v2/image-queue-speed1p3.json，按实测新音轨排时。
