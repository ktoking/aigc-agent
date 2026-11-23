# 输入合同与脚本

本页只描述旧`story_video.py`的**静音＋独立字幕模式**。配音生产使用[场景配音](minimax-tts.md)，按真实音轨排画面并在故事工程中合轨；不要将本页静音项目JSON误当成已经支持自动合轨的schema。

`project.json`和所引用图片共同组成一个项目。相对路径以project.json所在目录为基准，不依赖当前工作目录；尽量把资产放在项目内，云端移交时必须如此。

```json
{
  "name": "new-story",
  "fps": 30,
  "width": 1920,
  "height": 1080,
  "gap_seconds": 0.1,
  "dissolve_seconds": 0.1,
  "characters_per_second": 7.5,
  "assets": {
    "opening": "assets/opening.png",
    "reveal": "assets/reveal.png"
  },
  "episodes": [
    {
      "id": "EP001",
      "title": "本集标题",
      "cues": [
        {"text": "第一句已经确认的台词。", "asset": "opening", "duration_frames": 72},
        {"text": "第二句台词。", "asset": "opening", "duration_seconds": 1.5},
        {"text": "第三句暂时只有文字。", "asset": "reveal"}
      ]
    }
  ]
}
```

## 排时规则

- `duration_frames`和`duration_seconds`只能选一个，两者都省略时按文字估时；显式帧数优先不是静默覆盖冲突输入。
- 实际音频得到的时长可填`duration_frames`，并用`timing_basis`记录来源，如`measured_from_supplied_audio`。显式时长但无来源只标`provided_duration`，不自动声称实测。
- 只有文字时按`spoken_text`（可选读音展开）或text里的非标点字母数字计数；可用`spoken_units`提供明确读音单位数。中文初稿默认7.5字/秒，英文或其他语言应选合适参数或显式时长，不能套中文速度声称语音对齐。
- 所有秒数用十进制转换成整数帧。0.1秒在30fps为3帧；24fps下不能精确表示，脚本会记录实际量化后的时长，不虚报0.1秒。要求精确100ms时使用30/60fps。
- 每两个cue之间添加一次gap，包括跨集；首尾不补gap。单句时长不变。
- 仅不同事件图之间叠化，放在gap末端，结束时恰好到下一cue开始。同图连续使用保持完全相同构图。
- 辅助脚本要求量化后的叠化不长于gap；不满足时拒绝输入，交由创作者选择更长gap、短叠化或其他明确转场策略，不擅自切掉台词。设置gap和dissolve为0即可跳切。
- 不设置固定总时长。若用户明确要求固定总长，先修改剧本或明确的单句时长并检查能否实现，再调用脚本。

## 命令与文件

plan写入`timeline.json`、`captions.srt`、`captions.vtt`和`chapters.json`。render先重新plan，再从源图固定缩放/裁切到目标画幅，输出`video.mp4`和`render-manifest.json`；全程无音频和文字绘制。已有video.mp4默认不覆盖，明确需要时加`--overwrite`。

verify对照时间线与字幕，检查原文、单句帧数、间隔、章节边界、实际帧数、分辨率、帧率、零音轨/零内嵌字幕及完整解码，写`qa.json`。它不自动证明人脸/美术/剧情正确，也不把零字幕流当作烧录文字检测。检查失败以非零状态退出。

`python3 <skill目录>/scripts/story_video.py --help`查看子命令。脚本不负责声音/VAD/ASR、生图、动态视频生成或上传；用户需要这些能力时在生产流程中用当前可用工具处理，不能凭辅助脚本已通过而宣称全流程已完成。
