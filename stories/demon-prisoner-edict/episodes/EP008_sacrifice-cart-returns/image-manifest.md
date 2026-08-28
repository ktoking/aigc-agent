# EP008 图片资产清单

## 新锚点

- [x] `assets/characters/DPE_LU_YAN_001/references/lu-yan-turnaround-16x9.png`：辘魇三视图。
- [x] `assets/scenes/DPE_BROKEN_SACRIFICE_ROAD_001/references/broken-sacrifice-road-16x9.png`：运输祭道场景锚点。
- [x] `assets/props/DPE_SACRIFICE_CART_001/references/sacrifice-cart-16x9.png`：六名成年祭品的封闭祭车与四根主锁。
- [x] `assets/props/DPE_EDICT_SWORD_001/references/edict-sword-16x9.png`：无字克妖剑常驻形态，复用已存在资产。

## 分镜图

生成后每段将 `first-frame.png` 同步复制为 `shot-01.png`，将 `last-frame.png` 同步复制为 `shot-03.png`；`shot-02.png` 独立生成。

- [x] `segment_01_00-15s/frames/first-frame.png`
- [x] `segment_01_00-15s/frames/shot-02.png`
- [x] `segment_01_00-15s/frames/last-frame.png`
- [x] `segment_02_15-30s/frames/first-frame.png`
- [x] `segment_02_15-30s/frames/shot-02.png`
- [x] `segment_02_15-30s/frames/last-frame.png`
- [x] `segment_03_30-45s/frames/first-frame.png`
- [x] `segment_03_30-45s/frames/shot-02.png`
- [x] `segment_03_30-45s/frames/last-frame.png`
- [x] `segment_04_45-60s/frames/first-frame.png`
- [x] `segment_04_45-60s/frames/shot-02.png`
- [x] `segment_04_45-60s/frames/last-frame.png`

状态：角色、场景、祭车与克妖剑锚点已齐全；四段共 12 张独立分镜原图已生成，每段 `shot-01.png` 已同步为 `first-frame.png`，`shot-03.png` 已同步为 `last-frame.png`。
