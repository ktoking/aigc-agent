# EP050 Segment 2 视频交接

版本：2026-11-12-four-15s。这是重做后的15秒段，没有提交视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=835b76858366c24c7a3062cd730852e9fb78607e33f58b4b970d2d47033f7c5b；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词39个有效字；4字/秒粗估9.75秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 白棠 | asset://asset-20260320075131-k78qt | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 3 | 原温室补膜后结构 | assets/production/ep045-rebuild-reference-refresh/references/courtyard-greenhouse-film-repaired-16x9.png | 只锁完整黑棚架和透明补膜连接关系；苗盘数量、成熟程度与灯具按本镜，不复制满棚成熟菜；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 单盘叶菜与邻盘幼苗 | assets/production/ep044-050-seedance25/references/growthTray-16x9.png | 温室中一盘接近采收的叶菜与邻盘刚播小苗，前者展开到成熟、后者不变；仅提供作物状态，不锁人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 自用与交换的有限收成 | assets/production/ep044-050-seedance25/references/eggAndGreens-16x9.png | 当晚自用碗与少量交换菜分别放，库存鸡蛋和有限青菜，不虚构满仓收获；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 6 | 一层育苗灯架 | assets/production/ep044-050-seedance25/references/seedlingRack-16x9.png | 原工作间一层旧金属架安装有限育苗灯、控制组件与一盘刚播种的苗盘；无人物，不生成多层工厂；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 同一旧泵修后试水 | assets/production/ep044-050-seedance25/references/repairedPump-16x9.png | 同一旧泵装上新外部支架，防溅台上试转、管口回到同一水桶；电气部分不浸水，无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 有限种子与空育苗盘 | assets/production/ep044-050-seedance25/references/seedTray-16x9.png | 原工作间旧架、空育苗盘与有限种子袋，接近窗口光照不均；无人物，不画成熟蔬菜；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
