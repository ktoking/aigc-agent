# XHS Growth Agent

本机小红书图文运营 MVP，覆盖研究、策划、内容生成、封面配图、人工审核、发布队列和复盘。内容方向由每次输入决定，支持生活、旅行、美食、职场等任意领域。界面、数据库和运行进程独立于 Codex 对话存活。

后端 FastAPI + SQLite，前端 React + TypeScript + Vite。真实选题、策划、写稿与修改统一调用本机 Codex CLI，模型固定 `gpt-6.1-sol`，推理强度固定 `high`。默认 Live；Mock 可单独用于隔离流程和容量验证。

## 启动

需要 macOS arm64、`uv`、Node.js/npm、已安装并登录的 Codex CLI 和普通 Google Chrome。首次构建 MCP 另需 Git 与 Go 1.24+。Python 由 `uv` 建立项目专用 3.12 虚拟环境。

```bash
cd /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent
make setup
make dev
make doctor
```

后台：[http://127.0.0.1:18761](http://127.0.0.1:18761)。API：[http://127.0.0.1:18760/docs](http://127.0.0.1:18760/docs)。MCP 仅监听 `127.0.0.1:18060`。

`make dev` 脱离当前终端启动，日志在 `.runtime/logs/`、进程记录在 `.runtime/run/`。`make stop` 只停止当前路径创建且 PID 启动时间匹配的服务；端口被其他进程占用时拒绝启动，拒绝接管或终止占用者。项目路径带空格也可直接运行。

MCP 构建基于官方 `xiaohongshu-mcp` v2.5.5，用户要求使用普通 Chrome，故适配该版本默认的指纹浏览器依赖，使用标准浏览器路径。已审查构建置于 `.runtime/bin/xiaohongshu-mcp`，启动参数固定 `-port 127.0.0.1:18060`；Cookie 路径固定 `.runtime/mcp/cookies.json`。安装脚本不会自动下载新版覆盖此适配，也不修改其他 MCP 配置。

`make setup` 在二进制缺失或构建证明不匹配时执行源码构建；`make setup-mcp` 可显式重建。脚本克隆官方 tag `v2.5.5`，核验 commit `a5c8f7799980ba1fdd501999843eb2d17e4c9a9f`，应用 [普通 Chrome 补丁](docs/mcp-standard-browser.patch) 后用 Go 编译，生成 `.runtime/bin/mcp-build.json`（源码 commit、补丁及二进制哈希）。`python3 scripts/setup_mcp.py --check` 可复核，启动脚本也会校验。构建失败记录 BLOCKED，不会退回执行原始 Release。浏览器缺失时请安装普通 Chrome，或配置 `XHS_CHROME_PATH`。

仅启动应用、不启动 MCP：

```bash
make dev ARGS="--services backend frontend"
```

## 日常使用

1. 点击“准备内容”，先填写本次方向；可补充自己的经历、要点或素材，组合语气并预览写法模板，默认生成 1 篇。
2. 提交后立即进入审核中心，文案与配图在后台准备。页面可继续浏览，每篇完成即出现，不必等整批完成。
3. 在“本次创作”里修改或过滤，确认满意后批准。启用审批即队列时，批准直接排队发布，不再输入授权字符串。
4. 没有灵感时打开“选题雷达”：查看多来源近期热榜与新闻，或输入旅游、美食等方向查询，再用选中的话题写草稿。

热点默认最多 20 条，15 分钟缓存；网络并发读取，单源 5 秒、总上限 12 秒。新闻限定最近 24/72 小时并保留时间和出处，热榜仅注明获取时间，不把热榜时间伪装为新闻发布时间。来源读取不等于新闻事实核验。

准备内容接口快速返回后台任务；默认每次 1 篇、最多 3 篇，单篇 Codex 调用上限 120 秒，不自动换模型或重试。普通操作不经过旧的“研究 100 → 策划 50 → 批量生成”链条，旧诊断/Mock 功能收在高级设置中。新生成不会自动审批；质检退回也可以在审核中心修正，人工过滤后退出待审列表并保留历史。

历史三篇技术示例和实际发布证据见 [2026-10-12 验收](docs/acceptance.md)，本次流程复盘与实际验证见 [2026-10-13 流程复盘](docs/flow-review.md)。

审批入队策略启用时，后台把审批操作作为执行授权，并绑定版本、正文/图片哈希和实际账号。标题、正文、标签、图片顺序、信息卡或封面模板的修改会使之前的审批与授权失效；涉及视觉的修改会生成新图片版本，后台保留旧版快照。账号变更会阻止消费旧账号授权。真实发布结果不确定时进入 `VERIFY_REQUIRED`，需要人工核实；核实动作仅通过读取账号笔记比对，不会再次提交。暂停、每日上限、内容质量、重复发布检查均在服务端执行。

```bash
# 以下为高级诊断/历史示例入口，正常使用网页的“准备内容”
make demo
make review
# 完整预览后批准文章；启用审批入队策略时会直接入真实发布队列。
make review ARGS="--ids ARTICLE_ID --decision approve"
# 默认只模拟，未登录也能检验队列；不会标记为真实 PUBLISHED。
make publish-approved
make report
```

`make publish-approved ARGS="--mode live"` 只调用一次 `/api/publishing/enqueue-approved`，把历史已批准内容补入启用的审批队列并快速返回；常驻 worker 串行执行。默认处理全部已批准内容，可用 `--ids ARTICLE_ID` 限定范围。登录、账号绑定、版本/哈希、每日额度、暂停或质量条件不满足时会明确阻塞；未知提交不会自动重试。用户已经批准的当前版本可以直接入队，无需重复授权问答。

首次真实发布实际耗时约 2 分 9 秒。`.env` 的 `XHS_PUBLISH_TIMEOUT_SECONDS=600` 为一次 MCP 写请求留出等待时间，`XHS_CLI_HTTP_TIMEOUT_SECONDS=1800`（最低 900）用于本机 CLI 请求；延长等待不增加提交次数。生产 worker 独立于研究/生成调度开关运行，暂停会阻止后续写操作。停用审批入队策略会暂停后续提交、取消尚未提交的自动队列并撤销其执行授权，保留审计记录；已经开始的写请求不重试或强制中断。

## 写作学习与本地记忆

准备内容时展示语气对应的结构、开头示例与真实样本出处。展开“学习高赞写法”可后台读取20篇完整正文，按标题、开头、内容组织、收尾和语气提炼成Harness。生成直接读已保存结果，模板版本与任务绑定，人工采用或过滤会逐步影响推荐。

规则入口见 [写作 Harness](harness/writing/README.md)，当前真实学习结果导出到 `data/writing-harness/current.md`。图文正文学习与图片视觉学习分开；封面仍由本地HTML/CSS通过Chrome渲染一张图。

## 研究和容量验证

```bash
make research ARGS="--mode live"       # 真实来源与 Codex CLI 选题，默认 100 个候选
make plan ARGS="--mode live"           # 最多策划 50 个选题，使用 Codex CLI
make generate ARGS="--mode mock --count 50" # 隔离 Mock 容量验证
make research ARGS="--mode live --count 10 --keywords Codex MCP"
make generate ARGS="--mode live --count 3"
```

真实研究需要 MCP 登录或已配置的公开来源，真实选题与创作需要本机 Codex CLI 及有效登录。缺少这些条件会记录 BLOCKED，不会把演示数据伪装成平台搜索、个人实测或真实 LLM 产物。系统不会自动点赞、关注、评论或绕过平台限制。Mock 50 篇测试仅证明本机持久化、评分、媒体和工作流容量，不能证明真实模型日产 50 篇的质量、成本或小红书发布能力。

在终端运行 `codex login` 完成 Codex 账户登录，后台优先使用 Codex App 内置 CLI，随后尝试 PATH 中的 `codex`，通过 `codex exec` 调用；不需要为此系统接入其他模型服务。模型与推理强度固定，界面只提供 Live / Mock 创作模式。`.env` 的 `XHS_CODEX_TIMEOUT_SECONDS=600` 控制单次模型调用等待（范围 30–1800 秒）。CLI 安装检查仅证明可找到程序，登录与模型权限以真实调用结果为准；认证、超时或结构错误会明确记录 BLOCKED，不自动切换模型或服务。调用可能需要数分钟，正常准备内容接口立即返回后台任务，审核中心显示进度；真实发布保持单次请求，不自动重试。账户用量受 Codex 额度约束，系统不把未知美元费用填成已知 API 账单。每日发布上限、质量阈值和调度开关仍在后台设置。客户端接口见 [API 契约](docs/api-contract.md)。

## 测试与运行状态

```bash
make test      # 控制脚本安全检查、后端测试、前端生产构建
make doctor    # 本机工具、监听端口、MCP 连接/登录、Codex CLI 安装状态
make stop
make dev       # SQLite 保存的内容、授权状态、队列与运行记录可恢复
```

测试不会进行真实平台发布。真实 MCP 连接、搜索、登录和实际发布证据与 Mock 测试分开记录在 [验收报告](docs/acceptance.md)。真实发布正在执行时，不重启 server 或安装/替换 launchd；完成或未知结果安全收口后再安排维护。SQLite 与生成图片位于 `data/`，二进制、Cookie、日志位于 `.runtime/`，均应保持本地忽略。

## 持续运行

当前机器已经安装并实际核验用户级 launchd：MCP、API、Web 三个服务均为 running，退出 Codex 后继续运行，登录后可以恢复；不是云服务，Mac 关机时不能运行。服务 labels 为 `local.xhs-growth-agent.2748411da7.{mcp,backend,frontend}`，配置仅属于本项目路径。运行证据见 `.runtime/daemon-evidence.json`。

其他机器使用普通 `make dev` 时，Web、API 与发布进程不依赖 Codex 对话或终端保持打开；创作时会单独启动本机 Codex CLI。退出登录或重启后需重新启动。可在没有真实发布进行中时安装用户级 launchd：

```bash
make stop
make install-service
make doctor
# 删除本项目用户服务：
make uninstall-service
```

launchd 安装仅创建当前用户 `~/Library/LaunchAgents/local.xhs-growth-agent.<项目路径哈希>.*.plist`，分别启动 MCP、后端和前端。可在登录后自动恢复，不是云服务，也不能在 Mac 关机时运行；不会运行 Git hooks 或 Skynet 上报。数据及凭证仍留在本机。重新执行 `make dev` 前卸载 launchd 服务，避免两套启动方式竞争端口。

## 目录

```text
xhs-growth-agent/
  backend/           API、SQLite、Agent、发布保护、测试
  frontend/          中文运营后台
  scripts/           环境安装、生命周期、API CLI、安全检查
  docs/              需求、接口契约、实际验收
  data/              本地数据库与生成图片（忽略）
  .runtime/          MCP 二进制、Cookie、PID、日志（忽略）
  .venv/             专用 Python 环境（忽略）
```

当前版本是本机 MVP。平台登录、真实指标与搜索依赖账号状态；真实创作依赖 Codex CLI 登录、账户额度与模型输出质量。完整可用性以验收报告中的实际证据为准。

## 尚未完成的原始需求

- 当前质量评分是规则预检，完整事实核查、来源交叉验证和复杂语义质量评估未实现。
- 现有文本指纹与图片哈希可以拦截重复，完整语义去重与历史内容相似度检索未实现。
- 仅使用公开来源和已准备的演示资料，用户授权目录资料的完整导入、过滤和增量索引未实现。
- 保留 CLI 调用与用量记录；完整账户预算限制、美元费用换算及评分失败后的自动一次重写未实现。
- 首图已有六种不同版式，写法已有五种内置结构及真实样本提炼；图片像素的视觉风格学习尚未实现。
- 写作 Harness 已支持版本保存、生成冻结与有效审核反馈推荐；曝光校正、多变量实验与可信因果归因未实现。

已经验证的 50 篇容量为 Mock 内容配合真实图片渲染；今天真实平台发布与逐篇只读核实单独记录。不能把该容量结果或第一篇成功扩展为上述功能全部完成。
