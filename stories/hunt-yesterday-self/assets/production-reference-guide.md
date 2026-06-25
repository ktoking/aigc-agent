# 制作参考使用指南

## 分镜前

1. 先从 `asset-manifest.md` 选角色身份、三视图、动作、道具和场景资产。
2. 米拉与猎手同框时，额外引用对应 `CHOREO_EP001_*` 编排图。
3. 在分镜中写明屏幕方向、左右站位、持械手、怀表所在手和动作结束姿态。

## 首尾帧

- 首帧继承上一段尾帧时，不只写“同一角色”，还要逐项继承站位、朝向、重心、手部、武器、怀表、服装损伤和光线。
- 三视图负责解决背面、侧面和衣服结构；动作表负责解决姿态；概念海报只负责气质和总体美术。
- 少年出现时必须标注年龄阶段 1-4，并引用 `boy-age-progression.png`。

## 视频 prompt

每个动作镜头使用“准备 → 发力 → 接触/避让 → 收势”的连续描述。禁止只写“激烈打斗”“高速交锋”等无法约束动作前后状态的空泛词。

猎手攻击必须写出具体目标，例如“刀锋从米拉左肩外侧掠过并切断表链”，不能只写“猎手刺向米拉”。

## 画质

统一附加：

```text
Avoid fish scale texture, grid patterns, plastic skin, grid-like artifacts, aliasing, over-processed appearance, visible grains, repetitive scales, plastic texture, moire, crunchy outlines and excessive sharpening. Smooth even skin texture, soft lighting transitions, uniform matte surfaces.
```

服装材质使用“plain smooth matte fabric”，避免 quilted、diamond stitching、mesh、scales 等会诱发网状纹理的词。
