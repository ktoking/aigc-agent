# EP046 Segment 3 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-cinematic-director-v1；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=b99a7065069426a68f4034f3cae1174e8da94c489538713fdaf7bc352a402dd1；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词37个有效字；4字/秒粗估9.25秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 叶凝霜 | asset://asset-20260720212023-wwndz | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 白棠 | asset://asset-20260320075131-k78qt | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 禽舍修后通风与饮水 | assets/production/ep044-050-seedance25/references/coopWarm-16x9.png | 同一现代禽舍完成单侧挡风、原饮水器解冻后有水，保留通风口；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 窝箱单枚鸡蛋 | assets/scenes/SCENE_FOREST_VILLA_001/references/villa-poultry-pen-first-egg-16x9.png | 同一禽舍窝箱内仅一枚蛋与垫草的近景，不锁背景建筑或人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果；发现和带回的鸡蛋都只有一枚，不能加第二枚 |
| 6 | 原禽舍饮水器冻住 | assets/scenes/SCENE_FOREST_VILLA_001/references/villa-poultry-pen-empty-modern-16x9.png | 只锁原金属禽舍、原银色饮水器结构；时令必须冬雪，不能复制原夏季绿树林；冻结或解冻按本镜 |
| 7 | 凝霜银白长发无脸头模 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-silver-white-hair-reference-16x9.png | 只锁叶凝霜银白长发的长度、发色和发尾；假发头模不进入正片，不绑定脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 凝霜白色冬装 | assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
