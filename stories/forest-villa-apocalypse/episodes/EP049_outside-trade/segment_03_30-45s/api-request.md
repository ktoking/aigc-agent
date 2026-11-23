# EP049 Segment 3 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-cinematic-director-v1；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=836bf78f0a47eb9d0cf39d4502d570008efb3ce294ac7fce606a737fc478fd9a；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词46个有效字；4字/秒粗估11.5秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 白棠 | asset://asset-20260320075131-k78qt | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 原现代工作间 | assets/production/ep042-044-reference-refresh/references/industrial-metal-printer-winter-workshop-16x9.png | 原现代灰白工作间、打印仓和金属台面，窗外冬雪；只锁空间与机器，不锁台上新道具；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 原工业打印仓 | assets/props/FVA_INDUSTRIAL_METAL_PRINTER_001/references/industrial-metal-printer-installed-utilities-16x9.png | 既有单台炭灰封闭工业金属打印仓、原料盒、输出托盘与工作间；不锁时间或人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 旧泵变形支架 | assets/production/ep044-050-seedance25/references/brokenPump-16x9.png | 一台小型旧水泵、明显歪斜的外部安装支架，保留完整原外壳；无人物，不拆复杂内部；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 6 | 待验原料包装照片 | assets/production/ep044-050-seedance25/references/feedstockLabel-16x9.png | 手机上的旧仓库原料包装照片，与本机原包装标签并列；只锁包装外观，不把照片变为已收到实物；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 收到的盐包储位 | assets/production/ep044-050-seedance25/references/saltShelf-16x9.png | 现代干燥储架里刚收好的一包盐，自用食品储位保留，不出现无限物资；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
