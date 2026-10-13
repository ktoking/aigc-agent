# 2026-10-12 三篇小红书测试笔记 · 修订版

账号：momo。每篇 1 张封面＋3 张原创信息卡。以下内容尚未公开发布。

文案已根据“不要 AI 味道太重”改写。规则评分只做格式与重复预检，事实和表达仍需人工审核。批准内容后，执行发布还需要绑定当前版本、图片及账号的明确授权。

## 1. Codex跑偏？先把验收写清楚

文章 ID：`9d1e1f5a5ef64a4ebe646bcacaab7dd8`；版本：2；状态：APPROVED。

“帮我加个筛选功能。”
这句话交给 Codex，能写出代码，但写出来的东西未必就是你想要的。

拿一个很小的后台需求举例：筛选待审核的笔记。除了“加筛选”，其实还有几件事没说清——刷新后要不要保留？没有结果时显示什么？网络出错怎么办？

可以把任务改成这样：

“在笔记列表加状态筛选。选‘待审核’时，只显示待审核笔记；清空后恢复全部。刷新页面保留筛选条件。没有结果显示空状态，请求失败显示错误提示。先读这个目录适用的 AGENTS.md，再修改现有列表与查询接口。”

最后再加一句：
“请实际运行检查，交付时列出改了哪些文件、哪些场景验证过，还有什么没验证。”

这段话没有特别的提示词技巧，只是把原本藏在脑子里的判断写了出来。尤其是你已经知道答案的那些小细节，别留给工具猜。

项目比较大时，可以先让它指出需求里缺的条件。边界没聊清楚，代码写得越快，后面返工越容易。

参考：OpenAI Codex 官方文档。

你遇到过“代码能跑，但不是我要的”吗？

话题：#Codex #AI编程 #开发效率 #Agent #实操教程

引用：
- [OpenAI Codex 官方文档](https://developers.openai.com/codex/mcp)

封面与配图（按下列顺序发布）：

![第1张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/9d1e1f5a5ef64a4ebe646bcacaab7dd8/478043b83f8e/01.png)

![第2张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/9d1e1f5a5ef64a4ebe646bcacaab7dd8/478043b83f8e/02.png)

![第3张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/9d1e1f5a5ef64a4ebe646bcacaab7dd8/478043b83f8e/03.png)

![第4张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/9d1e1f5a5ef64a4ebe646bcacaab7dd8/478043b83f8e/04.png)

## 2. MCP接通后，别急着点发布

文章 ID：`18a17672c30b4300a3d3c6aba986a340`；版本：2；状态：APPROVED。

MCP 控制台亮了绿灯，就能开始发笔记了吗？
先别急。绿灯说明服务连上了，账号登录和发布权限还要另外检查。

比如接小红书 MCP，可以先看它实际返回了哪些工具。工具名和参数以当前版本为准，旧教程里的截图不一定还适用。

接着查登录状态。服务能运行，但账号没登录，这种情况很正常。二维码由账号本人用 App 扫，不需要把登录资料贴给别人。

登录后，先搜一个关键词，看看能不能真的拿到结果。这样至少知道读取这条路是通的。至于发布，还得单独确认文案、图片、可见范围，以及这篇内容有没有得到授权。

最容易误判的是最后一步：工具返回“发布完成”，但没给笔记 ID 或链接。这个返回值得记录，却还缺一次结果核实——去账号里找，确认实际出现的是刚才那篇内容。

如果请求超时，也先别马上再点一遍。它可能已经发出去，只是结果没回来。

所以，一个实用的接入顺序是：看工具 → 查登录 → 试读取 → 确认具体内容 → 发布后核实。每一步都留一份结果，比只保存一张“连接成功”的截图更有用。

参考：xiaohongshu-mcp 官方仓库与接口说明。

你接工具时，卡得最多的是登录还是权限？

话题：#MCP #AI工具 #Agent #小红书运营 #技术避坑

引用：
- [xiaohongshu-mcp 官方 README 与源码 v2.5.5](https://github.com/xpzouying/xiaohongshu-mcp/tree/v2.5.5)

封面与配图（按下列顺序发布）：

![第1张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/18a17672c30b4300a3d3c6aba986a340/d1c42f1277b8/01.png)

![第2张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/18a17672c30b4300a3d3c6aba986a340/d1c42f1277b8/02.png)

![第3张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/18a17672c30b4300a3d3c6aba986a340/d1c42f1277b8/03.png)

![第4张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/18a17672c30b4300a3d3c6aba986a340/d1c42f1277b8/04.png)

## 3. 自动发布，超时后先别重试

文章 ID：`559ffd1eb2b54668a8dd13ecf437ff5b`；版本：2；状态：PUBLISHING。

自动发布里，有一种报错特别容易让人手快：请求超时。

假设笔记已经提交，平台也接收了，但返回结果的那段网络断了。此时再点“重试”，就有可能把同一篇发两次。

这是一个假设场景，提醒的却是很具体的设计问题：系统不能把“没收到结果”直接翻译成“没有发布”。

做发布队列时，可以先把任务记进数据库：发哪篇、哪个版本、哪几张图，什么时候开始提交。提交中和结果待确认的任务，先拦住重复发送。重启后也要接着看这份记录，不能当成一切没发生过。

审核也是一样。文案通过了，后来又换了封面，原来的确认就不该继续沿用。批准什么，就发什么；修改了内容，再确认一次。

再放一个随时能找到的停止开关。它能拦住后续任务，但已经提交到平台的请求，未必能撤回来。界面最好把这点直接说清楚。

这些功能看起来没有自动生成封面那么亮眼，但遇到异常时，能让人知道发生了什么、下一步该查哪里。

最后别把生产量当成发布量。稿子可以多准备，发多少还是看账号状态、平台规则和内容质量。

参考：xiaohongshu-mcp 公开发布接口；文中设计建议供开发时参考。

如果请求一直转圈，你会先检查结果，还是先点重试？

话题：#Agent #自动化 #AI开发 #内容运营 #系统设计

引用：
- [xiaohongshu-mcp 发布接口源码](https://github.com/xpzouying/xiaohongshu-mcp/blob/v2.5.5/service.go)

封面与配图（按下列顺序发布）：

![第1张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/559ffd1eb2b54668a8dd13ecf437ff5b/f706c03aa612/01.png)

![第2张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/559ffd1eb2b54668a8dd13ecf437ff5b/f706c03aa612/02.png)

![第3张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/559ffd1eb2b54668a8dd13ecf437ff5b/f706c03aa612/03.png)

![第4张](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/xhs-growth-agent/data/media/559ffd1eb2b54668a8dd13ecf437ff5b/f706c03aa612/04.png)
