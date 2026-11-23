# EP044 Segment 3 视频交接

版本：2026-11-12-four-15s。这是重做后的15秒段，没有提交视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=29420ec61e6a563858b7aed4dd93c441cb9bf548693bc4fd69ecb61d862474ff；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词36个有效字；4字/秒粗估9秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 冬狼 | asset://asset-20260720205729-l4dfh | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 叶凝霜 | asset://asset-20260720212023-wwndz | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 同一关闭黑门 | assets/production/ep042-044-reference-refresh/references/canonical-gate-closed-winter-16x9.png | 原黑门门柱、内外侧与关闭状态，不改变canonical建筑；冻结发生墙外；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 墙外冰封倒地轮廓 | assets/production/ep042-044-reference-refresh/references/ice-covered-faceless-silhouette-snow-16x9.png | 只锁冬狼靴边的冰层材质；本段只冻住双脚，不提前封住全身或倒地，不从图中生成另一张脸 |
| 6 | 凝霜银白长发无脸头模 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-silver-white-hair-reference-16x9.png | 只锁叶凝霜银白长发的长度、发色和发尾；假发头模不进入正片，不绑定脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 凝霜白色冬装 | assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 冬狼现代黑色冬装 | assets/production/ep042-044-reference-refresh/references/wolf-winter-long-coat-flatlay-16x9.png | 冬狼无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 原双门人工交易槽 | assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-gate-transfer-hatch-16x9.png | 原黑门上的双门交易槽、托盘与内外门关系，主门关闭，箱子需人手推动；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
