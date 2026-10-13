# 实际验收报告

日期：2026-10-12，Asia/Shanghai。当前版本为本机 MVP；真实平台、Codex CLI、Mock 容量和自动化测试分别记录。

## 今日真实发布

momo 账号的 3 篇公开笔记均已 PUBLISHED。每篇通过 `get_my_profile + get_feed_detail` 独立比对新笔记 ID、实际作者、标题、正文、4 张图片及平台时间。

| 笔记 | 当前版本 | 平台发布时间 | 实际链接 |
| --- | --- | --- | --- |
| 自动发布，超时后先别重试 | v2 | 17:58:25 | https://www.xiaohongshu.com/explore/6accaf41000000001c00f70f |
| Codex跑偏？先把验收写清楚 | v3 | 19:12:51 | https://www.xiaohongshu.com/explore/6accc0b3000000001303e66f |
| MCP接通后，别急着点发布 | v3 | 19:15:45 | https://www.xiaohongshu.com/explore/6accc161000000001c01c974 |

用户先在界面批准三篇 v2，之后明确取消逐篇输入授权步骤，启用绑定 momo 的审批即队列策略。最新指令要求去除正文和配图的模板式制作声明，未发布两篇据此生成 v3 与实际新图片；以这次明确修改指令记录当前版本审批并入队，没有再次要求用户点击授权。已发布首篇保留原稿，内部创作来源字段如实保留；平台标识依据实际要求处理，不做审核规避。

首篇曾在旧 45 秒等待下进入未知结果，实际平台已发布；只读核实后恢复 PUBLISHED，没有重发。第二篇 v2 的原生日志 `18:30:18` 精确报创作者登录失效。固定 v2.5.5 源码证明该错误发生于 NewPublishImageAction 初始化、上传及 Publish 调用之前；操作者保存日志与源码解释，原尝试记为 NO_SUBMISSION，完整保留审计。后续用户明确修改生成新版本，原第三篇 v2 排队任务取消。未知超时和主页未找到笔记不能用于此恢复分类。

官方 MCP 普通 Chrome 补丁已加入创作者会话保存，并重新源码构建与校验哈希证明。用户正常扫码恢复登录后，主页核实账号一致；两篇 v3 串行发布并独立核实。NO_SUBMISSION 不占实际提交额度，今日实际提交 3 次，额度 3，无进行中、未知结果或待提交任务。

真实指标回读 `POST /api/metrics/collect`：HTTP 200，collected=3，blocked=[]。本次快照分别为点赞 0/1/0，收藏和评论均为平台返回的 0；浏览、曝光、分享、粉丝未取得可靠数据，保持 null。首篇发布时间已依据 `note.time` 从核实时间纠正为平台时间。刚发布的小样本不能用于增长归因。

证据：`.runtime/evidence/final-publication.json`、`.runtime/evidence/final-metrics-collect.json`、主 SQLite 的 PublishedPost/PublishAttempt/AuditLog。

## Codex CLI 实际验收

按照用户最新指令，选题评分、主编策划、写稿与改稿仅使用本机官方 Codex CLI `gpt-6.1-sol` / `high`，不接其他模型 API。运行配置及后台已切换 Live，UI 不提供外部 API Key/Base URL 或自由模型名。模型参数固定；Mock 仅供显式流程测试。

真实隔离验收 PASS：2 个候选评分 → 1 篇策划 → 1 篇 593 字成稿《交给Codex前，先写验收条件》 → make_article → 普通 Chrome 实际渲染 6 张 1080×1440 PNG → 规则质检 100 分、PENDING_REVIEW。未审批、平台调用 0，没有额外发布。三轮实际用量分别 input/output 11003/518、10954/453、11162/1499，美元费用未知为 null；工具调用均 0。

CLI 通过 stdin 和严格 JSON schema 返回内容，在独立临时工作目录执行，禁用用户配置、项目指令、hooks、MCP 与模型工具，不读取认证文件内容，不继承外部模型 API 环境变量。认证仍由 Codex 自身管理。缺少 CLI、认证失败、超时或结构不合法均阻塞，不自动切换模型。CLI 安装状态不等于真实调用成功；本次成功有实际调用证据。

证据：`.runtime/evidence/codex-cli-live.json`，含评分、策划、真实正文、逐轮实测用量与实际渲染路径。今日三篇已批准笔记为此前准备的成稿，不冒充本次 CLI 生成物。

## 自动化测试与运行

最终 `make test` 退出码 0：控制脚本 15 项、后端 69 项，共 84 项通过；TypeScript/Vite 生产构建通过，1580 模块、1.48 秒。涵盖审批入队、版本/图片/账号绑定、单次提交、未知恢复、精确未提交证据、一次恢复、配额、停止响应、CLI 隔离/固定模型/结构校验与 Live/Mock 分流。测试使用隔离数据库与发布替身，平台写入 0。测试证据 `.runtime/full-test-evidence.json` 保留历史。

MCP 18060、API 18760、Web 18761 仅 loopback。三个用户级 launchd 服务持续运行，退出 Codex 后仍工作；Mac 关机无法运行。发布进行中未重启服务；最终源码加载安排在三篇核实且指标采集结束后。当前 approval_to_queue=true、绑定 momo、每日上限 3、model_mode=live、生产调度默认关闭；发布 worker 独立运行。没有 Git hooks、Skynet 生成或上报流程。

## 其他已有验收及范围

- 真实来源研究：RSS 50、GitHub 30、XHS 20，共 100 候选，162.88 秒；后续部分 XHS 查询超时，保留阻塞证据，不推断全部查询可用。
- Mock 容量：隔离数据库 100 候选 → 50 篇 Mock → 200 张实际 1080×1440 图片，182.37 秒；真实模型及平台调用均为 0。不能据此声称真实 CLI 日产 50 篇已验收。
- 九个模板键目前为共享布局和配色变体；完整独立版式、语义去重、完整事实核查、授权目录增量导入、账户预算与费用换算、自动策略迭代尚未全部实现。详细范围见 README 的未完成清单。
- 原始完整需求保留于 `docs/original-requirements.md`，用户后续指令覆盖旧逐篇 typed 授权和模型接入方案。

工作台响应修复已实际部署：账号状态后台读取，dashboard 50ms、settings 22ms、jobs 3ms、report 8ms（一次实际快照），全部 HTTP 200，日报 published=3、blocked=[]。加载今日稿件会复用已修改版本，避免因正文变化再次生成旧副本；用户此前加载的重复草稿保留为 QUALITY_REJECTED，没有审批或发布。最终 UI 已验证无连接报错，发布页显示 3 项已发布、0 项待执行、momo 审批即队列和 gpt-6.1-sol/high；截图 `.runtime/screenshots/final-console.jpg`。
