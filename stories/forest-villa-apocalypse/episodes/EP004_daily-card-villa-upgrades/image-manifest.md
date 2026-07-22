# EP004 图像资产清单

## 角色资产

- 许砚：`asset://asset-20260320075237-29hdx`。
- 白棠：`asset://asset-20260320075131-k78qt`。

## 场景/道具参考

| 资产 | 路径 | 用途 |
| --- | --- | --- |
| 铁门与加固材料 | `assets/props/references/draw-card-gate-reinforcement-materials-16x9.png` | Segment 01，锁定钢板、螺栓和门锁 |
| 别墅外门结构 | `assets/props/references/outer-gate-trade-intercom-box-16x9.png` | Segment 01，锁定高墙和黑色铁门 |
| EP003 外门交易尾帧 | `episodes/EP003_mountain-road-car-outer-gate-trade/segment_04_45-60s/output/last-frame-generated.png` | Segment 01，承接实际铁门内侧和夜间院落状态 |
| 现代围墙人工施工背景 V2 | `assets/scenes/SCENE_FOREST_VILLA_001/references/wall-manual-construction-background-modern-v2-16x9.png` | Segment 02，锁定与别墅三视图一致的冷灰墙面、深灰压顶、砌块、砂浆和脚手架，不锁人物 |
| 现代无线绊线安装背景 V2 | `assets/props/references/wireless-tripwire-installation-background-modern-v2-16x9.png` | Segment 03，锁定现代门区、感应器、防水盒、备用铃铛和接线工具，不锁人物 |
| 别墅铁门夜景 | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-gate-generator-night-16x9.png` | Segment 03，锁定夜间铁门、监控和山林光线，不锁人物 |
| 地下室改造前 | `assets/scenes/SCENE_FOREST_VILLA_001/references/basement-storage-16x9.png` | Segment 04，锁定潮湿空置储藏间 |
| 现代地下室储存测试 V3 | `assets/scenes/SCENE_FOREST_VILLA_001/references/basement-storage-function-test-high-tech-v3-16x9.png` | Segment 04，锁定现代墙板、新风除湿、环境监测、配电柜、分区货架和测试物资，不锁人物 |

## 连续性限制

- 全部画面为真人写实、现代中国山区环境、横屏 `16:9`。
- 场景资产不得包含任何人物；许砚和白棠只由视频 API 的两个 `asset://` 数字人资产生成。
- 抽卡只提供材料、设备或图纸，所有改变都由人物施工完成。
- Segment 01 的加固过程只保留安装钢板、拧紧螺栓、落锁测试三个明确动作。
- Segment 02 用搬砖、拌砂浆和砌筑蒙太奇加高一段约十二米长的围墙；不出现蓝光、扫描线或墙体自动生长。
- Segment 03 是预警装置，不出现自动攻击、爆炸或伤人画面。
- Segment 04 只改造一间地下储藏室，通过温湿度和隔夜储物测试验证功能；不出现任何暗门或新通道。
- 室外建筑色调统一为冷白、浅灰和深灰金属；室内设备保持现代实用，不做复古仓库或科幻基地。
