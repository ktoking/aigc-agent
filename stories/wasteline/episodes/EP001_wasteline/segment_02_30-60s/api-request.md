# Segment 02 API 请求（30-60s，30s）

## 模型与参数
- model_version: seedance_2.5
- duration: 30
- ratio: 16:9
- 参考图：图生视频（本段首帧 + 核心资产图，URL 待 P2/P3 回填）

## 请求体模板
{
  "prompt": "<读取 director-promt.txt 全文>",
  "image_reference_url_list": ["<首帧图URL>", "<核心资产图URL>"],
  "ratio": "16:9",
  "duration": "30",
  "model_version": "seedance_2.5"
}

## 提交与重试策略
- 提交后记录 task_id → output/。
- 连续 2 次失败：调整描述措辞（保留总控前缀），不换模型。
- 成功标准：角色一致、镜头顺序正确、无水印残留、无 AI 伪影。

## 状态
- [ ] 待提交（P3）

## 本轮提示词交付说明

- 审阅版：`prompt.md`；纯文本版：`director-promt.txt`；以 `storyboard.md` 的段内时间为准。
- 上述 model_version / duration 为原故事包规划，未在本轮验证真实API能力，未提交、未产生任务ID。
- 图片尚未生成；不得直接提交模板占位符。实际提交时在正文前补充参考图编号与用途，对应真实上传顺序；不得把设定卡Markdown当图片。
- 30秒是剪辑段长；若所选真实接口不支持，应按本段L镜头组拆成受支持的短片后组装，保持240秒成片时间线。

## 已准备参考图（按上传顺序）

1. `frames/first-frame.png` — 本段首帧，锁定0秒状态
2. `frames/last-frame.png` — 本段尾帧，锁定30秒状态
3. `frames/ref-core-cradle.png` — 剧情补充参考资产；用途由文件名及本段prompt.md确定
4. `frames/ref-core-portable.png` — 剧情补充参考资产；用途由文件名及本段prompt.md确定
5. `frames/ref-dry-settlement.png` — 剧情补充参考资产；用途由文件名及本段prompt.md确定
6. `frames/ref-dry-wasteland.png` — 剧情补充参考资产；用途由文件名及本段prompt.md确定
7. `frames/ref-original-armored-train.png` — 用户提供的原始关键帧，仅按README指定职责使用
8. `frames/ref-original-lead-sniper.png` — 用户提供的原始关键帧，仅按README指定职责使用
9. `frames/ref-original-purification-chamber.png` — 用户提供的原始关键帧，仅按README指定职责使用
10. `frames/ref-train-coupler.png` — 剧情补充参考资产；用途由文件名及本段prompt.md确定
