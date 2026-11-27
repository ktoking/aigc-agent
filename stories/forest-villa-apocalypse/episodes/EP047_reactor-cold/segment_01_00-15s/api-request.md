# EP047 Segment 1 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-ep005-director-layout-v2；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=eb06b2932e466a48d6257f291514ed0634d476899236a8a16db2caa54c144130；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词49个有效字；4字/秒粗估12.25秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 沈知夏 | asset://asset-20260310030618-88hlb | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 现代客厅地暖空间 | assets/scenes/SCENE_FOREST_VILLA_001/references/villa-ground-floor-self-built-radiant-heating-16x9.png | 原现代客厅、稳定照明、地暖分水器、厚毯与暖桌；只锁空间，不靠图片断言温度；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 独立能源棚外观 | assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-energy-shed-cooling-loop-16x9.png | 原围墙内独立能源棚、密封发电模块外壳与外部供暖柜，生活区距离服从canonical；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 6 | 外部供暖支路柜 | assets/production/ep044-050-seedance25/references/heatingBranch-16x9.png | 密封核能主机之外的独立供暖柜，源侧与回屋侧管路、外接阀件可区分；无人物，无主机内部；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 外部执行件一次检查 | assets/production/ep044-050-seedance25/references/valveCheck-16x9.png | 同一外部传感器与两只小执行件，其中一只卡住；手持终端仅外观，不画内部电路；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 知夏暗酒红医护工装 | assets/characters/FVA_SHEN_ZHIXIA_001/references/shen-zhixia-medical-outfit-flatlay-16x9.png | 沈知夏无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
