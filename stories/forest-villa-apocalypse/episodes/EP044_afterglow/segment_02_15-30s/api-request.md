# EP044 Segment 2 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-cinematic-director-v1；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=bd54daa8015d19f7ce71d16c35bfb89c2bf0d6e246c1d4e1ef9636fb4215bfe2；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词37个有效字；4字/秒粗估9.25秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 冬狼 | asset://asset-20260720205729-l4dfh | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 受撞锁座 | assets/production/ep042-044-reference-refresh/references/black-gate-center-latch-strain-16x9.png | 原黑门中央锁座受撞变形，门板主体仍完整；只锁旧状态，不把结果提前修好；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 唯一阳台炮台 | assets/production/ep042-044-reference-refresh/references/auto-turret-isolated-16x9.png | 唯一自动炮台外形；安装位置在二楼阳台，弹药状态严格按当镜，不能复制第二座；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 6 | 外骨骼抵门受力 | assets/production/ep042-044-reference-refresh/references/exoskeleton-forearm-brace-gate-16x9.png | 同一防护外骨骼护臂抵住黑门的接触与受力；测试架不出现在正片，角色身份只用数字人；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 外骨骼过热停用 | assets/production/ep042-044-reference-refresh/references/exoskeleton-overheat-joint-16x9.png | 外骨骼同款关节、过热警示与停用状态；不锁新人物或新装甲；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 冬狼现代黑色冬装 | assets/production/ep042-044-reference-refresh/references/wolf-winter-long-coat-flatlay-16x9.png | 冬狼无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
