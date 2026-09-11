# 冬狼与炎魁数字人登记

用户本次指定，不是本地图片路径。

- 炎魁：asset://asset-20260804202241-z9zcp。
- 冬狼：asset://asset-20260720205729-l4dfh。

## 人物设定图（2026-09-08 用户确认）

两张图已存入 `assets/characters/FVA_DONG_LANG_001/` 与 `assets/characters/FVA_YAN_KUI_001/`，作为脸/气质/轮廓参考；**穿着（服装）以各集 director-promt 剧情提示词为准，不沿用人物图自带服装**。

- 冬狼：`assets/characters/FVA_DONG_LANG_001/donglang-character-sheet.png`（URL `https://aka.doubaocdn.com/s/7QwKTbF3TG`）。深蓝色带暗纹的立领传统服饰（古风立领）、棕色皮质腰带配雕花金属带扣、利落黑色短发、沉稳直视镜头，半身定妆质感。
- 炎魁：`assets/characters/FVA_YAN_KUI_001/yanquei-character-sheet.png`（URL `https://aka.doubaocdn.com/s/JHLrOsAqV3`）。东亚男性、正面、深蓝色休闲西装外套、浅灰圆领T恤、纯色浅灰背景、神情沉稳。

剧情中的实际造型：冬狼按剧情为雪原武装组织头领（阵中背光/侧影，不露正脸），炎魁为被打上印记火系异能者（放火时眼神空洞）。视频生成时可用上述人物图作参考输入，但服装、姿态按对应 director-promt 锁定。

人物脸只绑定本人ID，不借用许砚或其他角色。ID不放入背景图编号；API提交时作为独立数字人image_url输入。仅在需要正脸且本段数字人数不超过三人时加入。远景和背影未列身份锁的段落不得自行生成人脸。

当前正脸段落：
- 炎魁：EP042 segment03、segment04；EP044 segment03。
- 冬狼：EP043 segment04。

其他出镜保持原远景/背影，不增加第四个人脸。台词不变。服装沿用该角色已有确认画面；本次未读取数字资产原始图像，不将资产默认衣服视为剧情定装。生成前仍须核验服装与实际输入。
