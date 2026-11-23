# EP045 Segment 1 视频交接

版本：2026-11-12-four-15s。导演稿：2026-11-23-cinematic-director-v1；时码为文字预排，未生成视频。

- model=doubao-seedance-2-5-260628（沿用既定目标；本次未验证账号或服务端参数）。
- duration=15，ratio=16:9，resolution=480p，generate_audio=true。
- prompt_file=director-promt.txt；SHA256=849b3e4e8de5393523a92957a303e2b6f89061d2da097e3278364e6bcdb39ab7；prompt.md逐字一致。
- first_frame=null，last_frame=null，auto_images=false。
- 台词39个有效字；4字/秒粗估9.75秒，非实测语音。
- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。
- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。

| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |
| --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 2 | 白棠 | asset://asset-20260320075131-k78qt | 只锁本人身份与脸；基础服装和发型服从本段完整描述 |
| 3 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 4 | 旧锁板变形 | assets/production/ep042-044-reference-refresh/references/black-gate-center-latch-strain-16x9.png | 门内旧锁板歪斜、中央锁舌错位，门本体没有被打穿；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 5 | 新锁板装回原门 | assets/production/ep045-rebuild-reference-refresh/references/black-gate-replaced-center-latch-16x9.png | 同一黑门装回一块新锁板的局部，旧划痕保留，不新增外侧护板；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 6 | 打印仓单块锁板成品 | assets/production/ep045-rebuild-reference-refresh/references/industrial-printer-single-gate-latch-plate-16x9.png | 原打印仓输出托盘里的一块新锁板与旁边旧件，有限材料，人工安装；无人物；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 7 | 原现代工作间 | assets/production/ep042-044-reference-refresh/references/industrial-metal-printer-winter-workshop-16x9.png | 原现代灰白工作间、打印仓和金属台面，窗外冬雪；只锁空间与机器，不锁台上新道具；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 8 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |
| 9 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果 |

本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。
