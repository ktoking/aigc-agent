# EP001 图像资产清单

## 生成基线

- 生成方式：Codex 内置 `image_gen`。
- 画幅：16:9 横屏。
- 风格：原创日式古风动漫赛璐璐；清晰黑色描线、平涂高对比大色块。
- 人物锁：成年玄夜 / 成年凌尘 / 少年玄夜 / 少年凌尘。
- 场景锁：冷灰蓝虚空裂隙 / 暖金竹林 / 橙红山门废墟。
- 通用负面约束：无水印、无平台 Logo、无游戏 UI；不复刻既有动漫角色；非写实、非 3D、非 Q 版；避免过度锐化、鱼鳞网格和密集微纹理。
- 参考策略：先生成角色与场景母资产，再将母资产作为后续关键帧参考图输入。

## Segment 01｜少年日常 → 虚空初战

目录：`segment_01_00-30s/frames/`

1. `01-asset-adult-duo.png`：成年玄夜 / 凌尘双人定妆。
2. `02-asset-youth-duo.png`：少年玄夜 / 凌尘双人定妆。
3. `03-asset-void-rift.png`：虚空裂隙无人场景。
4. `04-asset-bamboo-grove.png`：竹林练剑场无人场景。
5. `05-l01-shimen-four.png`：师门四人竹林日常。
6. `06-l02-sword-eye.png`：少年凌尘剑瞳特写。
7. `07-l03-close-fist.png`：成年双人近身对拳。
8. `08-l04-youth-jump-kick.png`：少年玄夜跳踢。
9. `09-l06-down-kick-block.png`：成年玄夜下踢 / 凌尘格挡。
10. `10-l07-impact-freeze.png`：蓝色冲击波段尾定格。

## Segment 02｜连续格斗 → 回忆穿插

目录：`segment_02_30-60s/frames/`

1. `01-asset-blue-spirit.png`：蓝色灵力效果资产。
2. `02-asset-youth-training-pose.png`：少年徒手对练姿势资产。
3. `03-l08-side-kick.png`：凌尘侧踢 / 玄夜反击。
4. `04-l08-demon-eye-smirk.png`：成年玄夜魔瞳冷笑。
5. `05-l09-youth-combo.png`：少年直拳 / 侧闪 / 回蹴。
6. `06-l10-pillar-leap.png`：石碑间跃迁换位。
7. `07-l10-air-flip-punch.png`：空翻闪避 / 滑步直拳。
8. `08-l11-youth-golden-clash.png`：少年金色灵力碰拳。
9. `09-l12-elbow-counter.png`：凌尘肘击反制。
10. `10-l13-angry-charge.png`：剑瞳前景 / 玄夜怒冲段尾。

## Segment 03｜结印 → 山门崩塌 → 凌尘被打

目录：`segment_03_60-90s/frames/`

1. `01-asset-mountain-gate-ruins.png`：山门废墟无人场景。
2. `02-asset-genya-seal.png`：成年玄夜结印动作资产。
3. `03-l14-hand-seal-closeup.png`：结印手部特写。
4. `04-l14-eye-reflection.png`：魔瞳倒映结印。
5. `05-l15-time-overlap.png`：少年 / 成年玄夜双时空叠化。
6. `06-l16-pinned-under-rubble.png`：少年玄夜被压瓦砾。
7. `07-l17-fire-engulf-hand.png`：火焰吞没 / 手臂伸出。
8. `08-l18-chest-punch.png`：玄夜击中凌尘胸口。
9. `09-l18-pillar-impact.png`：凌尘撞碎石碑。
10. `10-l19-wounded-approach.png`：凌尘负伤 / 玄夜逼近段尾。

## Segment 04｜时空交错 → 最终碰撞 → 对峙

目录：`segment_04_90-120s/frames/`

1. `01-asset-golden-blaze.png`：金色剑辉效果资产。
2. `02-asset-wounded-adult-duo.png`：受伤成年双人一致性资产。
3. `03-l20-collar-grab.png`：玄夜抓起凌尘。
4. `04-l20-face-punch.png`：面门重拳命中。
5. `05-l21-youth-smile.png`：少年玄夜指向前方。
6. `06-l22-golden-time-overlap.png`：金色剑辉双时空叠化。
7. `07-l23-full-speed-charge.png`：成年双人全速冲刺。
8. `08-l23-final-collision.png`：蓝金最终碰撞。
9. `09-l24-distant-standoff.png`：冲击后远距对峙。
10. `10-l25-tears-pullback.png`：泪血 / 清泪终局特写。

## 预览

四个 segment 的 5×2 接触表位于 `previews/`，仅供人工审阅，不计入每段 10 张交付数量。
