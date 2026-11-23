# 人生容错率 · V2

当前版本：六组独立路网、持续前进、真实回退、逐级分叉与点亮。原片《we never（若如初见）》音轨0至60秒不变速，无新增配音。

- [新版播放器](player-v2.html)
- 主片：episodes/EP002_fault-tolerance-v2/output/fault-tolerance-v2_1080x1920_60s.mp4
- 工程：production/fault-tolerance-v2/index.html
- 图形与行程源数据：production/fault-tolerance-v2/journey-data.json
- 可逆行程引擎：production/fault-tolerance-v2/engine.js
- 节拍动作表：production/fault-tolerance-v2/beat-actions.csv
- QA：episodes/EP002_fault-tolerance-v2/output/delivery-qa.json

旧版内耗样片保留在EP001，已被本次容错率V2取代。其他选题不作为本轮制作目标。

运行 production/fault-tolerance-v2/build.py 会重建HTML和分段制作包；直接手工编辑HTML的改动会被生成器覆盖。npm run dev 打开可编辑工程。修改几何/事件使用build.py，修改描绘/回退/运镜使用engine.js。
