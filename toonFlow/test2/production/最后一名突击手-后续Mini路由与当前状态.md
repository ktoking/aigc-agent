# 《最后一名突击手》后续Mini路由

用户最新要求：“用Mini 模型生成吧 其他的”。解释为后续未提交的视频改用本机豆包Studio Seedance 2.0 Mini，不切换到Toonflow或其他供应商，不取消已运行的Fast任务，不自动重生成已有视频。

## 已完成配置修改
第02段节点75b53b3b-15a2-4595-b132-0a304f711980已通过实际setConfig改为providerId=doubaoLocal、modelId=seedance_2_0_mini、ratio=16:9、mode=singleImage，实际时长自动、分辨率未声明。完整提示词仅将模型名Fast改为Mini，保留单张02-A参考、连续动作、原稿无线电与声音要求，其余内容不变；未提交Mini任务。
第03、04、06—11段后续方案使用本机Mini，但这些视频尚未逐批确认真实参考、完整执行方案与具体次数，未提交。

## 当前真实任务状态
- G05：节点798d0ba6-889f-4fa7-85ee-6e5bca7c6f6f，任务be5f2796-846f-48e0-b81a-8f61038a2022，Fast，最新running、resumable=true、outputs为空。保持原任务，不取消、不重复提交。
- G12：节点e1aa26b0-688d-464c-bd29-9785a23c50dd，任务327cd213-c763-4853-b506-a241aa6b9ea4，Fast，最新status=failed、task.state=interrupted、resumable=true；错误“所选账号未就绪、正忙或本地额度不足；未提交，不自动换号”。保留原任务，不擅自换号或改模型恢复。
- G02原Fast任务d409a14d-0e37-4de1-a5c3-c53fd7ba132f：failed、not_started、未确认视频启动，工具说明已退回预扣额度。Mini尚未启动。

## 执行边界
本机账号的未就绪/忙/额度不足具体原因没有被工具区分，不能断言是额度耗尽。Mini同样走本机Studio，切模型不保证解决账号阻碍。当前先保留配置，不盲目批量提交。
换模型本身不是视频成功结果，不追加未确认的重试或无限生成。新增Mini生成前展示实际方案、次数、参考及算力消耗未知；沿用仍有效的内容确认，不逐工具审批。
