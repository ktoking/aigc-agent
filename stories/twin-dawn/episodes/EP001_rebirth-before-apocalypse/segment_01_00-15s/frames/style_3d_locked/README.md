# EP001 Segment 01 3D 锁定风格资产

本目录用于 EP001 Segment 01 的 3D 非真人风格重制。生成顺序为：先固定双女主人物风格，再生成首尾帧和故事板图，避免每张图重新随机角色脸。

## 角色锁定

- 林晚：黑色超长直发，左眼下小痣，黑色破损战术夹克，冷感、疲惫但强撑。
- 沈清雪：齐肩短发，空气刘海，白色战术服，苍白、克制、坚定。
- 风格：3D 动画电影感，明显非真人，不使用真人照片质感。

## 主要产物

- `clean_v2/character-style-reference.png`：双女主人物风格母版。
- `clean_v2/first-frame.png`：Segment 01 首帧。
- `clean_v2/last-frame.png`：Segment 01 尾帧。
- `shots/clean_v2/shot-01.png` 至 `shots/clean_v2/shot-04.png`：四个故事板镜头图。
- `storyboard-table.png`：按参考图格式制作的整张分镜表。
- `storyboard-table.svg`：分镜表源文件，可继续替换镜头图或文字。

## 后续视频生成提示

生成 Seedance / 可灵 / 即梦视频时，优先引用 `clean_v2` 和 `shots/clean_v2` 下的图片，并在提示词中保留：

> 画面中的所有人物都是 AI 生成的虚构 3D 动画短剧角色，不对应、不冒充、不还原任何真实人物，不包含真人隐私信息。

