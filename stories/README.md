# Stories 目录

每个剧本一个独立 story 包，目录名使用稳定英文 slug。

## 当前 story

- `twin-dawn/`：《末日重生：双生曙光 / 末日降临：我和闺蜜觉醒双SSS异能》
- `last-mile-robot/`：《请不要攻击送餐机器人》
- `robot-dream-ban/`：《机器人禁止做梦》
- `hunt-yesterday-self/`：《猎杀昨日的我》

## 新增 story

1. 从 `templates/story-package/` 复制基础结构。
2. 填写 `README.md` 和 `AGENTS.md`。
3. 完成 `docs/story-memory.md`、`docs/production-rules.md`、`docs/audience-strategy.md`、`docs/season-arc.md`。
4. 补角色、场景、道具、风格资产卡。
5. 使用根目录 skill 生成 EP001。

默认所有 story 的 episode 都是一集 60 秒、四段、每段 15 秒以内，并且每段包含故事板、首帧、尾帧和视频 prompt。
