# 工作流 - Foreign Rights

## 单集生产流程

1. **剧本确认**：剧情梗概 + 人物小传 + 场景清单 + 完整剧本
2. **分镜切分**：4章 × 15秒片段，每段6-10个镜头
3. **资产设定**：角色设定图（主角→配角→反派）、场景参考图、道具参考图
4. **关键帧生成**：每段1-2张决定性瞬间关键帧
5. **视频生成**：4段 × 15秒，图生视频（参考关键帧）
6. **后期制作**：拼接转场 + TTS配音 + 混音 + 字幕压制
7. **质检交付**：抽帧验证 + 音量检测 + 交付

## 每集目录结构

```
episodes/EP001_foreign-rights/
├── overview-storyboard.md      # 60秒总览故事板
├── segment_01_00-15s/
│   ├── storyboard.md           # 分段故事板和镜头表
│   ├── first-frame.md          # 首帧图提示词
│   ├── last-frame.md           # 尾帧图提示词
│   ├── prompt.md               # 视频API提示词
│   ├── api-request.md          # API参数和返回记录
│   ├── frames/                 # 首尾帧、关键帧图
│   └── output/                 # 视频生成产物
├── segment_02_15-30s/
├── segment_03_30-45s/
├── segment_04_45-60s/
├── qa-checklist.md             # 质检清单
└── publish-package.md          # 发布包（标题、封面、标签）
```

## 资产目录结构

```
assets/
├── characters/   # 角色设定图（含正脸特写+三视图）
├── scenes/       # 场景参考图（全景+各视角）
├── props/        # 道具参考图
└── style/        # 风格参考（色调、光影、质感）
```
