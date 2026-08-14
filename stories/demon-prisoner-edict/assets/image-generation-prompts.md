# 图像生成提示词

## 共用风格前缀

Use case: stylized-concept. Asset type: 16:9 landscape cinematic frame for an original motion comic. Original characters, semi-realistic 3D Eastern fantasy animated film, ancient demon-disaster world, cinematic physically based materials, natural skin and fabric, clean large shapes, clear silhouettes, cold desaturated gray-blue grade, volumetric fog, atmospheric perspective, restrained detail, shallow depth of field, realistic weight, no resemblance to an existing franchise.

## 共用负面约束

No text, subtitles, speech bubbles, watermark, logo, border, arrows, diagram, red targeting circle or game UI. Avoid live-action photography, flat 2D anime, plastic-doll skin, excessive sharpening, fish-scale mesh, dense microtexture, neon rainbow particles, malformed hands, extra people, duplicate bodies and identity drift.

## 角色锚点（3 张）

### A01 沈烬

- 输出：`assets/characters/DPE_SHEN_JIN_001/references/shen-jin-character-anchor-16x9.png`
- Prompt：16:9 landscape character anchor. Shen Jin, 24-year-old lean East Asian man, long narrow face, high straight nose, thin lips, gray-brown eyes, shoulder-length damp messy black hair, torn dark-gray cross-collar prison robe, coarse linen, dried blood at left lip, dark-red restraint burns on neck and wrists. Chest-up three-quarter pose, guarded exhausted expression, character centered slightly right, cold mist negative space left, cloudy side light.

### A02 阿璃

- 输出：`assets/characters/DPE_A_LI_001/references/a-li-character-anchor-16x9.png`
- Prompt：16:9 landscape character anchor. A-Li, 20-year-old slender East Asian woman, soft oval face, straight fine eyebrows, deep-brown almond eyes, small straight nose, black long hair tied in a simple high ponytail, one short matte ivory bone needle hidden horizontally in her hair, worn blue-white cross-collar dress and deep teal cloth belt, tiny mole below right ear. Half-body cautious backward glance, centered slightly left, fog negative space right, no demon features.

### A03 韩枭

- 输出：`assets/characters/DPE_HAN_XIAO_001/references/han-xiao-character-anchor-16x9.png`
- Prompt：16:9 landscape character anchor. Han Xiao, 36-year-old tall strong East Asian man, square-long face, narrow eyes, diagonal scar from right eyebrow toward temple, short black hair in low knot, matte black iron scale armor over black robe, old leather bracers, dark-red waist badge, right hand resting on a sheathed black straight blade. Three-quarter intimidating pose, uncovered face, blurred fog-valley road.

## 角色三视图补充（3 张）

角色三视图均以对应定妆图作为身份、脸型、发型、服装和伤痕参考，生成 16:9 横屏无字资产面板；正面、严格左侧面、背面三个人体等比例并列，中性 A-pose，中性灰摄影棚背景，明确为原创成年半写实 3D 动画电影角色，不复刻现实人物。

- 沈烬：`assets/characters/DPE_SHEN_JIN_001/references/shen-jin-turnaround-front-side-back-16x9.png`
- 阿璃：`assets/characters/DPE_A_LI_001/references/a-li-turnaround-front-side-back-16x9.png`
- 韩枭：`assets/characters/DPE_HAN_XIAO_001/references/han-xiao-turnaround-front-side-back-16x9.png`

## 场景锚点（3 张）

### A04 雾谷囚车外景

- 输出：`assets/scenes/DPE_FOG_VALLEY_CART_001/references/fog-valley-prison-cart-16x9.png`
- Prompt：16:9 landscape environment anchor, no close character. Narrow mountain valley before a storm, black pines and cliff on left, muddy road through center, deep gorge on right, battered wooden cage cart with iron-cornered wheels and wet black canopy moving toward distant stone steps, sparse armored escorts as tiny silhouettes, thick cloud light and volumetric mist, readable foreground-middle-background layers.

### A05 囚车内部

- 输出：`assets/scenes/DPE_CART_INTERIOR_001/references/prison-cart-interior-16x9.png`
- Prompt：16:9 landscape environment anchor, empty prison-cart interior, cramped rough wooden bars on both sides, wet straw and mud on floor, rusted floor ring and black rune shackles, translucent black rear curtain, thin cold daylight entering through slats, droplets and wood splinters, no people, no readable symbols.

### A06 祭坛山道

- 输出：`assets/scenes/DPE_ALTAR_ROAD_001/references/altar-mountain-road-16x9.png`
- Prompt：16:9 landscape environment anchor, broken stone mountain road at end of a fog valley during first rain, muddy foreground, ruined blank sacrificial stele in middle ground, black pines and broken stone lamps, distant steps rising into cloud-hidden altar, gorge as negative space, cold gray-blue light, no palace, no legible writing.

## 道具锚点（3 张）

### A07 骨针

- 输出：`assets/props/DPE_BONE_NEEDLE_001/references/bone-needle-16x9.png`
- Prompt：16:9 landscape cinematic prop study, one 12cm matte ivory bone needle on dark wet cloth, sharp tip and tiny crescent grip, subtle natural bone grain, scale readable beside two fingertips, soft cold side light, minimal uncluttered composition, no jewelry, no glow.

### A08 符文锁链

- 输出：`assets/props/DPE_RUNE_SHACKLE_001/references/rune-shackle-16x9.png`
- Prompt：16:9 landscape cinematic prop study, one 4cm-wide black iron wrist shackle attached to heavy chain, worn edges reveal dark silver, three shallow non-letter grooves, faint dark-red burn residue on inner rim, resting on wet wooden floor, realistic scale and weight, no bright magic.

### A09 镇妖刀

- 输出：`assets/props/DPE_DEMON_BLADE_001/references/demon-blade-16x9.png`
- Prompt：16:9 landscape cinematic prop study, single 85cm one-handed straight demon-suppressing blade, light-absorbing black steel, narrow dark-silver cutting edge, small oval guard, dark leather grip, three abstract grooves along spine, placed diagonally on damp stone, restrained cold light, no glow and no blood.

## EP001 Segment 01（3 张）

### EP001-S01-01 雾谷囚车

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_01_00-15s/frames/shot-01.png`
- Prompt：16:9 landscape wide establishing frame. The battered prison cage cart crosses the fog valley before a storm; black pines, cliff, muddy wheel tracks and distant stone steps. The cart is small in the middle ground, heavy cloud and mist dominate, sparse escorts only as distant silhouettes, ominous restrained composition.

### EP001-S01-02 囚徒细节

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_01_00-15s/frames/shot-02.png`
- Prompt：16:9 landscape interior cinematic close detail. Shen Jin sits collapsed in the right rear corner of the cramped wooden cart, torn dark-gray robe, bare muddy foot, black shackle and chain in sharp foreground, dried blood at left lip and damp hair partly hiding his closed eyes; A-Li is only a soft out-of-focus blue-white silhouette on the left. Cold light through bars.

### EP001-S01-03 睁眼与门影

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_01_00-15s/frames/shot-03.png`
- Prompt：16:9 landscape extreme close-up. Shen Jin's gray-brown eye snaps open beneath wet black strands, restrained alarm; in the far blurred background the black rear curtain carries the broad silhouette of a man who has stopped outside. A-Li's two fingers hover near Shen Jin's sleeve, cold low light, strong negative space.

## EP001 Segment 02（3 张）

### EP001-S02-01 骨针开锁

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_02_15-30s/frames/shot-01.png`
- Prompt：16:9 landscape macro close-up inside the cart. A-Li's right fingers hold the short ivory bone needle inside the outer lock of Shen Jin's black iron wrist shackle; her worn blue-white sleeve and his dark-gray sleeve clearly differ, realistic hand anatomy, damp wood and chain, focused quiet tension.

### EP001-S02-02 活祭石碑

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_02_15-30s/frames/shot-02.png`
- Prompt：16:9 landscape over-shoulder from behind Shen Jin. Through a narrow curtain gap he sees a ruined blank sacrificial stele and stone steps in rain; his damp black hair and dark robe frame the right foreground, A-Li's worried half-face is blurred left, no legible text carved on the stone.

### EP001-S02-03 校尉拔刀

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_02_15-30s/frames/shot-03.png`
- Prompt：16:9 landscape tense over-shoulder confrontation. Han Xiao has lifted the rear curtain and draws his black straight blade, right-brow scar visible; Shen Jin rises between him and A-Li, dark-gray back in foreground, A-Li behind in blue-white, cramped cart geometry, cold rain light, blade points toward frame center.

## EP001 Segment 03（3 张）

### EP001-S03-01 刀锋抵近

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_03_30-45s/frames/shot-01.png`
- Prompt：16:9 landscape tight side composition on the mountain road. Han Xiao's black blade is held a finger-width from A-Li's neck without cutting; A-Li remains calm but tense, blue-white collar and high ponytail exact, Shen Jin enters from right foreground with restrained anger, rain beginning, archers blurred behind.

### EP001-S03-02 放箭抬眼

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_03_30-45s/frames/shot-02.png`
- Prompt：16:9 landscape dynamic medium close frame. Several arrows have just left bows in the misty background and fly toward the cart; Shen Jin raises his head in foreground, gray-brown eyes focused, wet shoulder-length black hair, torn dark-gray robe and restraint burns exact; A-Li and Han Xiao hold their positions. No magic visible yet.

### EP001-S03-03 万物凝固

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_03_30-45s/frames/shot-03.png`
- Prompt：16:9 landscape hero frame. Shen Jin stands centered in the fog-valley road after saying stop; dozens of arrows, individual rain droplets and Han Xiao's black blade are perfectly suspended in space. Only a tiny dark-gold ancient glyph reflection appears deep in Shen Jin's pupils, subtle transparent air refraction and hairline spatial cracks, A-Li behind him, restrained premium supernatural effect, no UI.

## EP001 Segment 04（3 张）

### EP001-S04-01 穿过箭雨

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_04_45-60s/frames/shot-01.png`
- Prompt：16:9 landscape tracking-style frame. Shen Jin holds A-Li's hand and guides her between perfectly suspended arrows and rain droplets, his dark-gray robe and her blue-white dress flowing only slightly, fog valley layers behind, Han Xiao frozen farther back, quiet impossible stillness.

### EP001-S04-02 反噬与坠箭

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_04_45-60s/frames/shot-02.png`
- Prompt：16:9 landscape medium close frame. A thin line of fresh blood runs from Shen Jin's eye as time resumes; arrows strike and scatter across muddy ground around his bare feet without hitting him or A-Li, Han Xiao falls to one knee in shock, rain moves again, supernatural glow almost gone.

### EP001-S04-03 妖王影子

- 输出：`episodes/EP001_a-word-stops-the-arrows/segment_04_45-60s/frames/shot-03.png`
- Prompt：16:9 landscape final cliffhanger. Shen Jin turns in right foreground, blood at one eye, looking toward A-Li standing left-middle ground with her normal human face and blue-white dress; behind her, the valley fog forms one enormous long-horned demon-king silhouette covering the distant cliff, only a silhouette with no detailed monster face, cold gray-blue grade, huge negative space, ominous restraint.

## 发布封面（1 张）

### A22 无字封面

- 输出：`episodes/EP001_a-word-stops-the-arrows/cover-assets/cover-clean.png`
- Prompt：16:9 landscape cinematic thumbnail base with no text. Shen Jin occupies the right third in a strong three-quarter close pose, injured but calm, dozens of suspended arrows create diagonal depth across the center; A-Li stands on the left third with a faint giant horned shadow hidden in fog behind her, cold gray-blue palette with one restrained dark-gold reflection in Shen Jin's eye, clean silhouettes and readable faces.
