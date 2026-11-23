# Toonflow视频provider接入

这是给后续编码任务的接入指南，不代表已经修改或验证过用户本地Toonflow。文件名、扩展接口和状态枚举以目标仓库实际代码为准。

## 先定位扩展点

在用户指定的Toonflow仓库查找现有视频模型/provider注册、create/generate与query/poll适配接口、数据库任务模型、后台调度器、文件存储和模型配置UI。优先复制现有同类异步视频provider的组织方式；不要引入新的队列体系或同步长连接等待。

豆包账号池不是OpenAI兼容接口；不能只把OpenAI baseURL改成17888就宣称接通。如果当前Toonflow只接受固定供应商协议，新增小型provider适配层；确需独立bridge才实现，沿用已有项目栈和任务持久化。

## 后端配置

配置名沿用Toonflow习惯。语义上需要：本机base URL（默认http://127.0.0.1:17888）、后端Bearer密钥、模型ID、HTTP短超时、受支持画幅及真实输入能力。密钥从本机环境或私有配置读取，不返回给浏览器；默认不让前端直接连账号池。

后端在Docker或另一台机器时，127.0.0.1指向其自身；先核对网络拓扑、认证与共享文件可达性。不得把本机绝对图片路径当成跨容器自动可读，也不能把服务直接无认证暴露到公网。

## 创建任务

```http
POST /api/generate
Authorization: Bearer <server-side-key>
Content-Type: application/json
```

```json
{
  "model": "seedance_2_0_mini",
  "aspectRatio": "16:9",
  "prompt": "已审读的动作导演稿；当前接口时长自动，不承诺15秒。",
  "referenceImagePaths": ["/absolute/path/readable-by-account-pool/a.png", "/absolute/path/readable-by-account-pool/b.png"],
  "source": "toonflow-job-unique-id-take-01"
}
```

正常返回HTTP202，顶层含requestId、status、message等。将requestId作为provider任务ID保存，并立即返回Toonflow的排队/处理中结构，不能把message当视频地址。

- referenceImagePaths中的每个路径均要求账号池服务进程可读。不同文件系统时，使用重复referenceImages文件part的multipart上传，或referenceImageUrls数组（服务可访问的图片URL），择一；保留顺序，保护签名参数，不记录到日志。旧单图字段仍兼容，但不能混用。
- 自动换号模式省略accountId，交给账号池调度；不要将Toonflow旧配置中的账号编号继续传入。只有用户明确锁号时才传正整数accountId，该模式不可用会返回409。前台不需要Cookie或账号partition。
- source只是来源标签，**服务不会把它当幂等键**。调用方必须对Toonflow job/take加唯一约束并保存提交意图；同一job重入应读已有requestId。
- 先GET /api/capabilities确认多图修复版；旧版404时仅视为单图，不发送多图继续消费。新版本回执referenceImageCount应等于请求数；选定账号先做只上传、不生成的多图preflight。
- 不发送duration、durationSeconds等猜测字段；当前固定时长仍不支持，旧JSON接口可能忽略它们而仍消耗额度。
- removeWatermark=false不能当作已实现的跳过去水印开关：当前生成入口强制最终MP4验证，源码会保存removeWatermark=true。未配置Token的取片能力要单独处理。

## 查询与状态映射

`GET /api/requests/:requestId`，使用相同Bearer。按照实际Toonflow枚举映射以下语义，不虚构它的字段名：

|账号池status|Toonflow语义|处理|
|---|---|---|
|accepted|queued/pending|服务已建任务；不再次生成|
|running|running/processing|准备、提交或等待视频；不能当已生成|
|success|先校验输出，再completed|使用有效cleanVideoUrl或实际outputVideoPath|
|failed|failed，保留错误|保留error.stage/code/title/detail；不得自动重提|
|stopped|cancelled/stopped|本地停止不代表已撤销豆包端生成|

保留原始provider status，避免适配过程丢失真实边界。错误恢复时不把旧失败回调覆盖后续确认成功；使用updatedAt和当前任务状态处理乱序，沿用Toonflow既有防重方式。

回调callbackUrl是可选能力。只有明确配置了本机可达接收端才传，按requestId防重；回调结构/认证方式核对当前实现，不能臆造签名头。不能信任未经验证的回调直接完成任务；必要时使用原requestId的GET结果确认。

## 返回视频

success只可包含已经验证的MP4输出。cleanVideoUrl若是签名媒体地址，及时通过Toonflow现有媒体存储流程保存，保留资源引用，不把会过期的URL写进可公开的静态导演稿。outputVideoPath是账号池机器上的本地路径，需要服务端可读或受认证文件传输；不能直接把它当浏览器URL。

分享页、聊天页、HTML、空路径和不存在的MP4都不能转成Toonflow完成态。下载HTTP成功也要核对内容类型、MP4特征/媒体流，避免把错误页面保存为.mp4。

watermark/token_missing可能发生在视频已生成之后。UI明确显示取片/解析失败；若要保留官方水印的原片方案，在后端增加已验证的官方原片导出能力，再接入正常媒体存储；不伪造cleanVideoUrl，不向远程资源携带本机Bearer。没有原片下载能力时如实报输出恢复待处理，不能声称端到端可用。

## 并发、恢复与验证

沿用Toonflow持久化任务队列，保存job ID→requestId。每段/take独立任务；调用端不直接操纵账号窗口、剪贴板或Cookie，也不让所有任务抢同一对话。

预算来自选中任务数×当前本地模型单价，限制一次提交任务数和并发。不擅自改账号池余额、账号并发或平台限制。读取账号登录标记不等于完成视频能力验证。

至少覆盖：两条并发任务ID各自映射；同job重复调用只POST一次；POST超时后保持未知提交状态；HTTP500可能已有任务；重启后继续查原任务；HTTP409不当作受理成功；watermark失败不重新生成；HTML/分享链接拒绝作为MP4；旧版多图/当前固定15秒请求在调用前明确拒绝；新版有序数组、multipart多文件、数量回执、附件缺失不发出均覆盖。使用项目已有验证方式，优先必要的聚焦测试。

未授权生成时，只做代码/模拟及health、账号、无生成预检，报告真实视频E2E为NOT_RUN。接入完成后也不默认扣额度跑一条视频。


## 已安装本机适配的业务开关修复（1.1.0）

本机doubaoLocal曾额外要求config.allowAutoDuration===true，而UI默认false；对话授权不会修改该配置。这是接入层业务开关，不是豆包OAuth或API权限。供应商1.1.0已移除该rule及判断，正常生成自动时长模型不再重复询问；仍保留实际API认证和固定时长/声音开关等未支持参数的拒绝。

缺少第三方去水印Token不应在有官方原片恢复路径时阻止生成。本机转接1.1.0会在同一requestId的watermark失败后取回官方带水印MP4，保留poolStatus/poolError，验证文件后才向Toonflow返回完成；未就绪继续查原任务，不重生成。此机制保留原音轨，但不证明指定对白/音效质量已通过。
