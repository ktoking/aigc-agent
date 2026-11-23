# EP046 Segment 4 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-cinematic-director-v1；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=d8f1edef7e298fc7fb89431f90d66f6aebb9c9c78def2334a92c5e7343705633；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词37个有效字；4字/秒粗估9.25秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 3 | 窝箱单枚鸡蛋 | assets/scenes/SCENE_FOREST_VILLA_001/references/villa-poultry-pen-first-egg-16x9.png | 同一禽舍窝箱内仅一枚蛋与垫草的近景，不锁背景建筑或人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果；发现和带回的鸡蛋都只有一枚，不能加第二枚 |
| 4 | 保温罩内循环水和鱼影 | assets/production/ep044-050-seedance25/references/pondWarm-16x9.png | 同一透明罩下鱼影、气泡与正常循环水，鱼大小不被异能放大；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 禽舍修后通风与饮水 | assets/production/ep044-050-seedance25/references/coopWarm-16x9.png | 同一现代禽舍完成单侧挡风、原饮水器解冻后有水，保留通风口；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 6 | 原现代控制室机位 | assets/production/ep036-defrost-and-intel/references/modern-winter-intel-control-room-16x9.png | 只锁原监控台、屏幕边框和室内布局；屏幕内容依本镜重绘，不继承图上其他建筑或车辆；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 无人机观察终端外壳 | assets/production/ep036-defrost-and-intel/references/drone-monitor-camp-verification-16x9.png | 只锁显示器黑色边框、终端材质；图上敌营、帐篷、装甲车、地图一律不复制，屏幕只显示本镜泵房远景；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 山谷旧泵房炊烟 | assets/production/ep044-050-seedance25/references/pumpHouseSmoke-16x9.png | 南侧山谷旧泵房远景，一缕炊烟，树林遮挡；没有人物脸、尸潮、可读坐标或新别墅；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
