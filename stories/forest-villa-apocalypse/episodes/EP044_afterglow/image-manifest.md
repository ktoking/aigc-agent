# EP044 新稿参考图衔接清单

版本：2026-09-23-dialogue-rebuild-eight-shots
2026-10-08按最新剧本完成六段参考资产复核及补图。旧frames根目录保留为历史素材；当前可用图片按编号存入各段frames/current-references。数字人身份仍用用户资产ID，人物三视图只供人工复核。图片就绪不等于30秒视频API已验收。

## Segment 1：最后一轮子弹
本地历史图片10张；新请求规划9项，其中数字人3项。

| 请求编号 | 用途 | 已验收输入（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定冬狼本人脸和身份，服装按正文 | asset://asset-20260720205729-l4dfh | user_registered_identity |
| 2 | 只绑定白棠本人脸和身份，服装按正文 | asset://asset-20260320075131-k78qt | user_registered_identity |
| 3 | 只绑定许砚本人脸和身份，服装按正文 | asset://asset-20260320075237-29hdx | user_registered_identity |
| 4 | 既定别墅冬季结构，只锁同一栋现代三层主楼、连续阳台、高围墙、黑门与院内空间；屋顶形状逐项服从原图，不按文字另造 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | reviewed_existing_16x9 |
| 5 | 只锁原外门中央锁座受撞变形细节；铁门整体样式仍服从参考图4，不生成第二道门 | assets/production/ep042-044-reference-refresh/references/black-gate-center-latch-strain-16x9.png | generated_reviewed_16x9 |
| 6 | 只锁唯一FVA_AUTO_TURRET_001炮台的外形；安装位置只服从别墅锚图与剧情中的二楼阳台 | assets/production/ep042-044-reference-refresh/references/auto-turret-isolated-16x9.png | generated_reviewed_16x9 |
| 7 | 只锁护臂接触门板的受力角度；画面中的空置测试支架不得出现在正片 | assets/production/ep042-044-reference-refresh/references/exoskeleton-forearm-brace-gate-16x9.png | generated_reviewed_16x9 |
| 8 | 冬狼无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/production/ep042-044-reference-refresh/references/wolf-winter-long-coat-flatlay-16x9.png | generated_reviewed_16x9 |
| 9 | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | reviewed_existing_16x9 |

历史frames按文件名保留，编号不再等于新API顺序：
- segment_01_00-30s/frames/参考图01_人物三视图_许砚.png
- segment_01_00-30s/frames/参考图02_人物三视图_白棠.png
- segment_01_00-30s/frames/参考图03_人物三视图_叶凝霜.png
- segment_01_00-30s/frames/参考图04_人物三视图_沈知夏.png
- segment_01_00-30s/frames/参考图05_正确别墅雪景.png
- segment_01_00-30s/frames/参考图06_关键帧_黎明围攻.png
- segment_01_00-30s/frames/参考图07_唯一阳台炮台.png
- segment_01_00-30s/frames/参考图08_围墙冰层状态.png
- segment_01_00-30s/frames/参考图09_黎明暴雪天空.png
- segment_01_00-30s/frames/参考图10_控制室监控背景.png

## Segment 2：叶凝霜把力量留给他
本地历史图片10张；新请求规划9项，其中数字人3项。

| 请求编号 | 用途 | 已验收输入（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定冬狼本人脸和身份，服装按正文 | asset://asset-20260720205729-l4dfh | user_registered_identity |
| 2 | 只绑定叶凝霜本人脸和身份，服装按正文 | asset://asset-20260720212023-wwndz | user_registered_identity |
| 3 | 只绑定许砚本人脸和身份，服装按正文 | asset://asset-20260320075237-29hdx | user_registered_identity |
| 4 | 既定别墅冬季结构，只锁同一栋现代三层主楼、连续阳台、高围墙、黑门与院内空间；屋顶形状逐项服从原图，不按文字另造 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | reviewed_existing_16x9 |
| 5 | 只锁正确别墅原有黑色双扇铁门、灰墙和门柱；开闭按镜头变化，别墅全貌只服从参考图4 | assets/production/ep042-044-reference-refresh/references/canonical-gate-closed-winter-16x9.png | generated_reviewed_16x9 |
| 6 | 只锁门外单个冰封物倒地的冰层质感；冬狼身份与服装仍服从数字人和参考图8 | assets/production/ep042-044-reference-refresh/references/ice-covered-faceless-silhouette-snow-16x9.png | generated_reviewed_16x9 |
| 7 | 只锁外骨骼过热关节和熄灭状态灯，不锁背景或新增装备 | assets/production/ep042-044-reference-refresh/references/exoskeleton-overheat-joint-16x9.png | generated_reviewed_16x9 |
| 8 | 冬狼无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/production/ep042-044-reference-refresh/references/wolf-winter-long-coat-flatlay-16x9.png | generated_reviewed_16x9 |
| 9 | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png | generated_reviewed_16x9 |

历史frames按文件名保留，编号不再等于新API顺序：
- segment_02_30-60s/frames/参考图01_人物三视图_叶凝霜.png
- segment_02_30-60s/frames/参考图02_人物三视图_冬狼.png
- segment_02_30-60s/frames/参考图03_人物三视图_许砚.png
- segment_02_30-60s/frames/参考图04_人物三视图_沈知夏.png
- segment_02_30-60s/frames/参考图05_正确别墅雪景.png
- segment_02_30-60s/frames/参考图06_关键帧_冬狼冰封.png
- segment_02_30-60s/frames/参考图07_终结冰系效果.png
- segment_02_30-60s/frames/参考图08_围墙冰层状态.png
- segment_02_30-60s/frames/参考图09_医疗急救包.png
- segment_02_30-60s/frames/参考图10_唯一阳台炮台.png

## 本轮排除
- 不能用旧关键帧的错误人物脸、蓝西装炎魁、古风冬狼、旧黑丝袜凝霜来控制服装。
- 不能拿炸药卡、机械接线图、全棚坍塌图去代替本集不同功能。
- 不用首尾帧，不自动扫描整个frames上传；提交前必须完成每张图的用途和身份审查。
