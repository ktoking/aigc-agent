# 工具安装与验证

日期：2026-10-16。

## 已完成

- 官方 Hypit Skill：`/Users/kaiyi.wang/.codex/skills/hypit`。
- 通过 skill-installer 的 GitHub 安装脚本，从 `hypit-ai/hypit` 的 `skills/hypit` 安装。
- 全局执行程序：`@hypit/hypit 0.3.1`。
- Distribution：`/opt/homebrew/lib/node_modules/@hypit/hypit`。
- Launcher：`/opt/homebrew/lib/node_modules/@hypit/hypit/bin/hypit.mjs`。
- `hypit version`、`hypit --help` 返回成功。
- Node：v26.0.0；FFmpeg：8.0.1；uv 已存在。

最终执行的 npm 安装命令：

```bash
npm install --global @hypit/hypit --registry=https://registry.npmjs.org/ --ignore-scripts --legacy-peer-deps --no-audit --no-fund
```

首次安装出现额外 peer 依赖解析与内部镜像等待，停止该次安装后用上述选项成功安装 116 个包。没有运行仓库 Git/Cursor hooks 或 Skynet。

Node 26 下 CLI 有 `module.register()` 弃用提示，命令仍返回成功；尚不能据此保证所有渲染依赖均兼容。

## 验证边界

仅验证 Skill 落盘、执行程序安装和 CLI 启动。尚未初始化生产 Runtime、准备浏览器渲染程序、构建或导出视频；不宣称成片渲染通过。

后续 GPT 生图使用会话工具生成本地文件，不必先连接 HypiHub 或其他图片服务。图片以本地素材导入 Hypit，再验证本地渲染。

新装 Skill 会在下一轮可用，本轮已读取其落盘说明继续分析。
