# 今日 MVP API 契约

FastAPI 127.0.0.1:18760，前端 127.0.0.1:18761。JSON API 前缀 /api，媒体 /media/{path}。SQLite 位于 data/，亚洲上海时区。

GET /api/dashboard -> {counts: {articles, pending_review, approved, published, verify_required, topics}, agents: [{name,status,last_run}], mcp: {connected,logged_in,detail}, model: {mode,configured,name:"gpt-6.1-sol",provider:"codex_cli",reasoning_effort:"high",detail}, paused: bool, daily_limit: int, recent_runs: [], metrics: {likes,saves,comments,views:null}, costs: {calls,cost_usd}}
GET /api/articles -> [{id,title,title_candidates,body,tags,status,category,style,ai_assisted,sources:[{title,url,verified}],media:[{id,url,path,sha256}],quality:{score,reasons,risks},version,created_at,comment_prompt}]
GET /api/articles/{id} -> 同上
PATCH /api/articles/{id} {title?,body?,tags?,media_order?,cards?:[{title,body}],template?} -> article；编辑使审批及授权失效；title/cards/template 变动重新绘制首图并保存新版本实际媒体。新模板 auto/bold/sticky/editorial/receipt/split/ink；旧模板名保持兼容，映射到新布局。cards 输入兼容1至5个对象，新模型只返回1个封面对象，实际只渲染1张首图，完整内容放在body。单图可通过规则质检。
POST /api/articles/{id}/review {decision:approve|reject,reviewer:string} -> article；approval_to_queue=true 时，approve 即为当前版本/图片和绑定实际账号的执行授权，同步生成 live QUEUED job 后快速返回，不要求逐篇输入确认字符串。策略未启用时只审批。
POST /api/articles/{id}/revise {instruction:string,tones?:最多4个内置语气标签} -> article；标题、正文、封面与评论引导一起按标签改写。
POST /api/articles/{id}/cover {template?:string} -> article
POST /api/articles/{id}/authorize {confirmation:string,visibility:string} -> 兼容旧客户端的手动授权接口；审批入队策略启用后无需调用此接口，也不要求用户输入确认字符串。任何授权仍绑定版本、图片哈希及当前 MCP 核实的实际账号，客户端不能自由指定授权账号。
POST /api/articles/{id}/publish {mode:mock|live,visibility?:string} -> job；mock 不改变真实 PUBLISHED 或消耗授权
GET /api/jobs -> [{id,article_id,title,status,mode,error,created_at,response}]
POST /api/jobs/{id}/verify -> job；仅只读核实 VERIFY_REQUIRED，不重新提交，不自动解除发布暂停。
POST /api/jobs/{id}/resolve-not-submitted {log_line,operator,explanation} -> job；仅暂停时由操作者提供与任务时间匹配的精确原生创作者登录初始化错误日志，核实为 NO_SUBMISSION，保存原尝试与源码解释。超时及主页未找到笔记不能据此解除未知结果。
POST /api/jobs/{id}/retry-pre-submit -> job；仅暂停时对有审计证据的 NO_SUBMISSION 原版本创建最多一个恢复任务；重新核实当前账号、原审批、版本、图片哈希与审批入队策略，保持暂停。仅 NO_SUBMISSION 不占真实提交额度。
POST /api/publishing/pause {paused:bool} -> {paused}
POST /api/publishing/enqueue-approved {article_ids?:string[]} -> {count,enqueued:[{job_id,article_id,status}],blocked:[]}；空 body 默认全部 APPROVED，可指定 ID 范围。审批入队策略启用时，将历史已批准且未成功发布的有效版本补入 live 队列，快速返回，不等待平台完成。后台常驻单独串行 worker 执行，独立于生产 scheduler；不会再次提交已发布/已有提交尝试/未知结果内容。
GET /api/topics -> [{id,title,category,score,reasons,sources,status}]
POST /api/research {mode:mock|live,count?:100,keywords?:[]} -> {count,mode,blocked?,run_id}
POST /api/plan {limit?:50,mode?:mock|live} -> {count,mode}
POST /api/generate {count?:3,mode:mock|live} -> {count,mode,article_ids}
POST /api/demo -> {article_ids}；创建今天准备好的 3 篇原创技术内容，不伪造个人体验
GET /api/settings -> {daily_limit,quality_threshold,account_positioning,model_mode,model_configured,mcp_url,paused,scheduler_enabled,production_target,keywords,rss_urls,user_id,model_name:"gpt-6.1-sol",model_provider:"codex_cli",model_reasoning_effort:"high",model_detail,approval_to_queue,approved_account_id,approved_account_name}
PATCH /api/settings -> 支持以上非密钥字段；approval_to_queue=true 时服务端实时读取当前 MCP profile 后绑定实际账号，approved_account_id/name 为只读，不接受客户端指定。false 停用新自动入队、暂停后续提交、取消未提交的自动 QUEUED job 并撤销对应 auth，保留审计。只有 CANCELLED 且无 PublishAttempt 的同版本任务可在重新启用后用同一个 job/idempotency key 重新绑定授权激活，已提交或未知结果任务绝不自动重试。
GET /api/mcp/status -> {connected,logged_in,detail,tools:[]}
POST /api/mcp/qrcode -> {image_url,detail}；二维码可由本地图片返回
GET /api/report -> {date,production,approvals,published,blocked,insights,uncertainty,metrics,experiments}
POST /api/metrics/collect -> {collected,blocked}
GET /api/runs -> 最近 AgentRun
POST /api/scheduler/{task}/run -> 研究/策划/生成/质检/队列/采集/复盘；真实执行只消费有效的账号/版本/图片授权。approval_to_queue 启用时批准即生成该授权，不增加逐篇确认步骤。

发布等待：publish_content 单次等待默认 600 秒（XHS_PUBLISH_TIMEOUT_SECONDS）；无自动写重试。CLI 本机请求等待至少 900 秒。未知结果暂停并要求只读核实，不能因 HTTP 等待结束重复提交。

错误 {detail:string}。所有列表可增加 metadata 字段，但 UI 兼容此形状。

模型适配：Live 选题评分、策划、内容生成与修改仅调用本机 Codex CLI `gpt-6.1-sol`，推理强度 `high`；不提供其他模型服务切换。`model_configured` 只表示能找到 CLI，认证与权限以真实调用结果为准。`model_name` 固定，修改为其他名称会被拒绝。Mock 是单独测试模式，不调用真实模型。`POST /api/plan` 未指定 mode 时读取当前后台创作模式。模型单次等待 `XHS_CODEX_TIMEOUT_SECONDS` 默认 600 秒、范围 30–1800 秒。认证失败、超时、结构不合法时记录 BLOCKED，不自动改用其他模型。前端研究/策划/生成/修改/任务请求等待 1800 秒，无自动重试。


## 2026-10-13 正常创作入口

- POST /api/creation/tasks {direction:1-300字,count:1-3默认1,topic_ids?:最多5,material?:最多10000字,tones?:最多4个标签} ->202 {id,status,stage,direction,count,tones,completed,article_ids,error,created_at,updated_at,finished_at}。语气可组合，支持natural/critical/objective/subjective/sharp/gentle/humorous/empathetic；默认及空选择为natural，重复标签去重，未知标签拒绝。标签保存在任务记录并传给每篇写作请求，不额外调用模型；默认不固定批判，所有语气都自然具体、少套话。
- GET /api/creation/tasks/latest ->最近任务或null；GET /api/creation/tasks/{id} ->进度。RUNNING/COMPLETED/FAILED/INTERRUPTED，阶段QUEUED/WRITING/RENDERING/REVIEW_READY/DONE；每篇就绪即写入article_ids并进入待审，生成不审批或发布。后台会话独立于HTTP请求；重启保留已完成稿、中断任务不自动重试。
- POST /api/hotspots/refresh {direction?:最多150字} ->202后台任务；GET /api/hotspots/tasks/{id}读取状态。
- GET /api/hotspots?direction=... ->{items,updated_at,loading,sources,errors,task_id,status,cache_fresh}；按日期和领域隔离缓存，不混旧Mock或历史AI候选。最多20、缓存15分钟、公开网络读取总上限12秒。
- 人工reject将文章标为REJECTED并移出待审；规则预检未通过仍为QUALITY_REJECTED供修改。approve仅使用已有版本/账号/哈希/配额保护后入队。

旧research/plan/generate/demo端点为兼容和高级诊断保留，网页正常准备内容不调用这些旧批量接口。任意领域创作仍使用固定Codex CLI gpt-6.1-sol/high。


## 2026-10-14 写法与 Harness

- GET /api/writing/templates?tones=natural,subjective -> {items,learning,harness}。内置与真实学习结果分开；推荐联合语气与当前模板版本的有效审核反馈。
- POST /api/writing/learn {keywords?:1至4个非政治关键词,target_samples?:4至30默认20} ->202后台任务。最多50次详情读取，默认深入20篇；成功相同参数缓存6小时。
- GET /api/writing/learning/latest -> {id,status,stage,sample_count,target_samples,candidate_count,read_count,samples,template_ids,harness_version,harness_path,error,...} 或null。阶段SEARCHING/READING/ANALYZING/DONE/BLOCKED/INTERRUPTED。学习失败仍保留原模板。
- GET /api/writing/harness -> 当前标题、开头、正文、收尾、语气、封面建议和避免项，含版本与真实公开样本元数据；不包含原文或访问token。
- POST /api/creation/tasks 新增 template_id，默认auto。服务端冻结写法模板与Harness版本，后续任务使用新版本，进行中的任务保持原规则。响应增加writing_template与harness_version。

学习只调用本机Codex CLI gpt-6.1-sol/high。普通生成不临时搜索、无额外模型调用；先检查本次要求、重复套话和虚构经历。学习/生成不自动批准或发布，图片仍为本地单张封面渲染。
