# EP048 Segment 1 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-ep005-director-layout-v2；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=47f00c3e4393d63388fc36352f613f82076b0480ca502dc0a47f9e8ecce40c10；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词46个有效字；4字/秒粗估11.5秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 白棠 | asset://asset-20260320075131-k78qt | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 许砚 | asset://asset-20260320075237-29hdx | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 原现代工作间 | assets/production/ep042-044-reference-refresh/references/industrial-metal-printer-winter-workshop-16x9.png | 原现代灰白工作间、打印仓和金属台面，窗外冬雪；只锁空间与机器，不锁台上新道具；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 原工业打印仓 | assets/props/FVA_INDUSTRIAL_METAL_PRINTER_001/references/industrial-metal-printer-installed-utilities-16x9.png | 既有单台炭灰封闭工业金属打印仓、原料盒、输出托盘与工作间；不锁时间或人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 旧件与最后一个备用件 | assets/production/ep044-050-seedance25/references/spareTray-16x9.png | 旧外接执行件、仅一只备用件与空格备件盒，分开摆放；换件后盒子为空，无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果；EP047换件后盒里必须为空，EP048空盒状态继续承接，不能恢复一只备用件 |
| 6 | 有限机械小件与护板 | assets/production/ep044-050-seedance25/references/mechanicalParts-16x9.png | 少量机械支架、单块外门防撞护板与有限原料并列，电子封装件单独放；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 本段物件收束局部 | assets/production/ep044-050-seedance25/references/ep048-s1-detail-16x9.png | 原打印仓有限剩余料、已分格机械备件与单独旧电子件，不把电子件打印出来；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
