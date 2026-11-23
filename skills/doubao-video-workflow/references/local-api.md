# 本机账号池接口（已核对0.1.76修复版）

默认地址`http://127.0.0.1:17888`。该服务将HTTP请求转为账号隔离的豆包网页DOM操作，不是豆包官方视频API；截图仅辅助排错。

## 当前真实能力

|接口/能力|已实现|边界|
|---|---|---|
|GET /health|是|无认证，不证明实际生成|
|GET /api/accounts|是|Bearer认证，本地账号/额度/任务数|
|GET /api/accounts/:id/editor-status|是|只读已打开唯一窗口；没有窗口不会打开|
|POST /api/accounts/:id/preflight|是|默认只检查model/aspectRatio；可传referenceImagePaths上传并核对数量，不发送生成、不扣点；不检查15秒|
|POST /api/generate|是|prompt/model/aspectRatio/accountId/referenceImagePaths或referenceImageUrls/source/callbackUrl；旧单图兼容|
|GET /api/requests/:id|是|单个任务状态|
|POST /api/requests/:id/retry-result|是|恢复已有结果，不是重新生成；仅准备流程时不调用|
|独立时长参数|否|prompt写15秒会被模型当文本；不能保证实际时长|
|原生多图数组|本机修复版已实现|有序数组，上传后及发送前核对数量；账号001实测3张上传就绪|
|GET /api/capabilities|已实现|本地最多9张，真实账号上限需preflight；固定时长未实现|
|异步并发|是（实现存在）|每条任务独立requestId/窗口；实际跨账号生成质量另验|

代码核对点：electron/reference-images.ts负责校验，database.ts保存完整数组并兼容旧单图，main.ts解析JSON/multipart及preflight，executor.ts通过CDP批量或逐张上传，video-attachments.ts检查当前输入区图片数量和加载状态。修复标识20261113-readiness-routing-v3；部署状态以运行服务/health为准。

多图选择referenceImagePaths（本机绝对路径数组）或referenceImageUrls（HTTP/HTTPS数组），与旧单图字段四选一；不混用，不丢图。multipart重复referenceImages字段，保留part顺序。请求本地上限9张，真实账号001只验证过3张；需要上传验证但不生成时，POST /api/accounts/:id/preflight传referenceImagePaths，返回requestedCount/attachedCount/readyCount。

参考图尽力上传策略（2026-11-13用户授权）：上传等待最多30秒；缺图、零张或部分未就绪不再作为生成任务失败条件，记录实际数量与警告后继续尝试发送。隐藏进度元素不算上传中。`referenceUpload.complete`说明是否全部就绪，`warning`说明降级情况；预检的`ready`只表示模型与画幅就绪，不代表参考图完整。请求回执`referenceImageCount`仍是请求张数，不能冒充实际使用张数。未知额外附件仍停止以免串图；不存在的本机文件、格式错误等输入校验保持有效。旧运行服务未升级前仍可能执行严格检查，部署受活动任务保护。

固定15秒仍未实现：durationSeconds不是受支持参数。先核对网页真实时长控件，再在明确范围内扩展时长选择及无生成校验；不能只在prompt写15秒。多图上传预检通过不代表视频质量或实际多图生成已通过。

## 预算与并发

以当前本地miniCost/fastCost计算，不硬编码为官方价格。公开账号接口未返回单价时，不猜价格；在授权范围内查本机配置的非敏感字段。账号池的quotaRemaining、dailyQuotaExhausted、runningTaskCount和queuedTaskCount都要核对。自动换号模式不传accountId，由账号池按可用额度与现有队列选择；执行器在每次实际发送前核验页面、模型、画幅及附件。只登录过不代表适合立即使用，失败不能跳过校验继续发出。

并发请求由服务接管后，创建请求不等待视频、不刷新额度、不自行重置账号，也不通过切账号绕过平台明确限制。命名用项目+段号+take+内容指纹，记录每段requestId。

## 授权和去重

后端可使用DOUBAO_API_KEY环境变量保存本地密钥，配置名遵循Toonflow实际约定；排查时可在授权范围内只读本机SQLite的settings.apiKey。不得打印密钥或读取Cookie。不要在shell命令里直接写Bearer。Mac默认数据库位于~/Library/Application Support/doubao-account-manager/doubao-manager.sqlite3；实际使用前核对，不复制数据库到仓库。

提交意图持久化后，即使无响应也标记UNKNOWN_SUBMISSION，需要核对SQLite任务source或原日志再决定。只有明确未发出才可另开take；已经提交不能靠删除本地标记再次生成。source不是账号池服务幂等键，去重由Toonflow的job/take映射负责。

会话中用户要求“不要等”时，只返回受理快照和任务号；后续查询做一次GET快照。Toonflow自身可沿用已有后台状态查询机制。返回failed且error.stage=watermark、code=token_missing时，任务可能已有视频；若有官方原片恢复能力则恢复同一任务并保留水印，不能因为API failed重新生成。

## 视频入口就绪与安全换号

GET /api/accounts返回videoReadiness数组，按model保存ready/reason/checkedAt。未知状态仍可调度，但执行器发送前必须核验；明确未通过视频入口/模型校验的账号对该模型暂停自动调度。账号本地额度保持原值，不伪装成官方额度耗尽。状态跨重启、登录/额度重置持久保存，只有对应模型页面校验成功后恢复。

只对自动分配、无submissionSentAt、无generationAcceptedAt的活动任务沿用同一个requestId换号，原子退还旧预扣并预扣新账号；不先回调failed，模型和输入保持原样。全部账号不可用时明确失败并退回持有的预扣；固定账号请求不暗换，历史失败任务不自动重提。

GET /api/accounts/selection?model=seedance_2_0_fast可在不创建任务/不扣额度下检查真实分配函数；可带accountId检查指定账号是否符合条件，返回accountId或null。该接口同样要求Bearer。它证明调度选择行为，不证明视频成功生成。
