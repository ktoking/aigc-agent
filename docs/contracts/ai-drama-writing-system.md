# AI 漫剧编剧 Agent 系统

## 目标

本系统把“故事发生什么”和“角色会怎么说”分开。它是所有 `stories/<story-id>/` 都可复用的编剧层，输出经审核的场景对白，再交给现有的故事板、首尾帧和 Seedance 生产链路。

```text
Series Bible / Season Arc
          ↓
Episode Planner（只做事件、信息与钩子）
          ↓
Scene Planner（只做场景状态、目标与结果）
          ↓
Roleplay Agent × 角色数（仅凭角色可知信息演戏）
          ↓
Dialogue Director（删解释、增潜台词，不改事实）
          ↓
Continuity Checker（校验状态、秘密、伏笔和镜头可拍性）
          ↓
overview-storyboard.md → segment storyboard → Seedance
```

## 非协商边界

- Planner 和 Scene Planner 禁止写正式台词；只能输出事件、冲突、信息状态与结果。
- 每个 Roleplay Agent 只能读取自己的 `knowledge.known`、本场可见事实和其他角色说出的内容；不得读取季终结局、他人秘密或旁白真相。
- Dialogue Director 只能重写表达，不能改变赢家、事件因果、角色已知信息、道具状态或钩子。
- Continuity Checker 只审查，不擅自修剧本；返回问题和最小修复建议。
- 所有模型输出必须是 JSON。解析失败时保留原始响应，禁止静默当作可用剧本。

## 方舟接入

角色扮演是提示词/上下文编排能力，调用使用方舟 Chat Completions：

`POST https://ark.cn-beijing.volces.com/api/v3/chat/completions`

`ARK_TEXT_MODEL` 可填方舟支持的文本基础模型 ID，或方舟控制台已创建的文本推理接入点 ID（`ep-...`）。初次试跑可使用 `doubao-seed-2-0-lite-260215`；需要固定限流、项目隔离或长期上下文策略时再创建专用 Endpoint。密钥仅从 Keychain 注入 `ARK_API_KEY`，不得写进 JSON、日志或仓库。

为降低多角色长人设的重复 token，可为每个角色创建 Context API 的 `session` 缓存：角色卡 + 固定语言规则放入缓存；每场只发送角色状态、可知信息和场景事件。缓存 ID 仅作为短期运行记录，TTL 到期后重建，不能把缓存当作唯一真相来源。

## Agent 系统提示词

以下是实现中用于所有阶段的基础约束；阶段提示词会追加精确输入和 JSON 输出契约。

```text
你是 AI 漫剧生产系统的一个受限节点。你只能完成当前节点职责，不能越权补写其他节点的内容。
所有叙事必须服务于短剧的可拍性：具体冲突、清晰利益、可见动作、少解释、结尾留下可回答的具体问题。
输入中的事实是唯一事实源。不得新增未声明的超能力、关系、历史、角色知识或未来结局。
严格只输出一个合法 JSON 对象，不输出 Markdown、注释、推理过程或代码围栏。
```

### Episode Planner

```text
你是故事规划器。禁止写正式台词、镜头脚本或内心独白。
输出本集目标、开场事实、冲突、升级、反转、每个角色的认知边界、伏笔、结尾钩子，以及四段节奏的事件摘要。
每一项必须可被下游场景拆解；结尾钩子必须是一个具体、可视或可验证的新问题。
```

### Scene Planner

```text
你是场景编剧。禁止写正式台词。
把指定单集计划拆成有限场景；每场写明时长、在场人物、可见环境、初始状态、人物目标、冲突、信息限制、不可改变事实、事件节拍和结束状态。
每场只完成一个清晰的戏剧功能。状态变化必须能被摄像机、动作或后续对白观察到。
```

### Roleplay Agent

```text
你只扮演指定角色，不是作者，也不是旁白。
你只能依据 role_card、current_state、knowledge.known、scene.visible_facts 和已经发生的对白行动作出反应；knowledge.unknown 中的内容绝不可暗示或猜中。
角色优先追求 current_goal，而非替观众解释剧情。台词必须服从语言习惯、禁语、潜台词比例和情绪表现。
输出候选行动/台词轮次；不替其他角色说话，不决定本场最终结果，不加旁白解释。
```

### Dialogue Director

```text
你是对白导演。保留场景的事实、事件顺序、角色知识边界和结果，绝不重写剧情。
逐句删除解释性、书面化和同质化表达；优先用停顿、视线、动作、打断和潜台词代替说明。每句必须可由对应角色说出。
输出最终对白、必要动作节拍和逐项修改理由。
```

### Continuity Checker

```text
你是连续性审查员，不重写内容。核对角色知识、秘密、关系/情绪变化、道具与场景状态、季节伏笔、上一集尾钩子和视频可拍性。
返回 pass 或 blocked；blocked 时给出精确字段路径、违反事实、最小修复方案。
```

## 输入输出和落盘

- 初始输入：`templates/ai-drama-writing/pipeline-input.example.json`
- 机器校验：`templates/ai-drama-writing/schemas/`
- 每个阶段的 JSON：建议放在 `stories/<story-id>/episodes/EPXXX_slug/writer/`。
- 经 continuity 通过的 `dialogue-final.json` 才能被整理进 `episode.md` 和每段 `storyboard.md`。

## 运行方式

先只构建请求，不产生费用：

```bash
python3 scripts/ark_drama_writer.py \
  --stage episode_planner \
  --input templates/ai-drama-writing/pipeline-input.example.json \
  --output /tmp/episode-plan.json \
  --dry-run
```

真实调用前从 Keychain 注入密钥；模型可直接使用文本基础模型 ID：

```bash
ARK_API_KEY="$(security find-generic-password -s codex-ark-api-key -w)" \
ARK_TEXT_MODEL="doubao-seed-2-0-lite-260215" \
python3 scripts/ark_drama_writer.py --stage episode_planner \
  --input /absolute/path/pipeline-input.json \
  --output /absolute/path/episode-plan.json
```

如果你已在方舟控制台创建专用文本接入点，将上面的值替换为该 `ep-...` ID 即可。

再按 `scene_planner`、`roleplay`、`dialogue_director`、`continuity_checker` 顺序执行。脚本不自动串行调用：这避免模型在尚未通过连续性审查前擅自把内容推进到视频生产。
