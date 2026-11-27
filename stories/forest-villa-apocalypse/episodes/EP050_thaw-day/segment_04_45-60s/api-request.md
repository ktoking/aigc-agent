# EP050 Segment 4 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-ep005-director-layout-v2；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=66b49450ca0ab9a066127e642e1f86e1501233522f5c193dbb155cdc0ae906da；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词39个有效字；4字/秒粗估9.75秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 沈知夏 | asset://asset-20260310030618-88hlb | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 叶凝霜 | asset://asset-20260720212023-wwndz | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 许砚 | asset://asset-20260320075237-29hdx | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 4 | 现代别墅暖色餐区 | assets/production/ep044-050-seedance25/references/dining-16x9.png | canonical现代别墅暖色餐区、普通碗筷、窗外冬雪；四把椅子可见但没有人物，不画四人合照；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 青菜鸡蛋面 | assets/production/ep044-050-seedance25/references/noodles-16x9.png | 普通陶瓷碗中的青菜鸡蛋面，少量真实热气，现代餐桌，无火锅、宴席、人物和文字；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 6 | 凝霜银白长发无脸头模 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-silver-white-hair-reference-16x9.png | 只锁叶凝霜银白长发的长度、发色和发尾；假发头模不进入正片，不绑定脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 知夏暗酒红医护工装 | assets/characters/FVA_SHEN_ZHIXIA_001/references/shen-zhixia-medical-outfit-flatlay-16x9.png | 沈知夏无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 凝霜白色冬装 | assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
