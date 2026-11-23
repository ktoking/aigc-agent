# 《跌怕了吗》可编辑工程

- 入口：index.html；六幕在compositions/。
- 本地预览：http://localhost:5205/#project/die-pa-le-ma
- 文案、动作与分段文档生成器：build.py。
- 来源：sources.md；三案比选和avoid：frame.md；分镜：STORYBOARD.md。
- 导出：`npx hyperframes render --quality looks --fps 30 --output ../../episodes/EP001_die-pa-le-ma/output/die-pa-le-ma_1080x1920_60s.mp4`
- 检查：`npx hyperframes check --json`；交付验证：使用带numpy的Python运行deliver.py。
- CLI0.8.171；GSAP3.14.2；字体、音乐本地打包；无外部视频API。

原音轨0—60秒，未变速。字幕和六幕关键点来自beat-map.json同一实测节拍表。不要把估计BPM或帧量化精度当作听觉质量证明。

重新运行build.py会按当前代码重写文档、场景和字幕，故手工编辑HTML后先同步回生成器再重建。
