from pathlib import Path
import json, re, hashlib, math
R=Path(__file__).resolve().parents[1]
V=R/'production/script-v1'
eps=json.loads((V/'episode-data.json').read_text())
def write(p,s):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n')
actors={
'CHEN':('陈屿','26岁中国成年男性，短黑发自然侧分，长方脸、清晰下颌、深棕眼，干净无胡须，中等偏瘦体格；炭灰色轻薄工装外套、素色灰T恤、深色长裤，无首饰','前物流仓储主管；负责采购、核算、准入；不获得格斗能力'),
'XIA':('夏凛','28岁中国成年女性，结实匀称体格，轮廓利落，黑色低马尾、平直浓眉、深棕眼，左耳后一道浅小旧疤；前期藏青保安制服无标志，入住后同色实用上衣、黑长裤；狗牌放衣领内、短棍挂腰侧','退役侦察兵；警戒与防御；初登场EP005；未通过陈屿所见得到的私事不由旁白揭示'),
'XU':('许知意','27岁中国成年女性，椭圆脸、柔和但清醒的眼神，黑发整齐挽低髻，深棕眼，无浓妆；白大褂、浅蓝内衫、深长裤、平底鞋；血月夜只有袖口轻微裂开、脸色苍白','市一院急诊医生；EP008登场；EP010只到门外，未入住'),
'WANG':('王大富','45岁中国成年男性，略胖圆脸、短黑发、身材矮壮；酒红Polo衫、深裤；初期一只小鸟笼，血月夜小布袋装十根金条，外观不大量堆金','邻居，群聊嘲讽者；EP010受灯光掩护逃回对门，未死亡'),
'MA':('马主任','48岁中国成年男性，偏瘦长脸、后梳短发、灰色衬衫、深色西裤、细框眼镜','陈屿前上司，同一物流园管理者；将货损责任推给陈屿，并因投诉解聘夏凛'),
'LI':('老李','50岁中国成年男性，短寸头、藏青夹克、棕围裙','粮油批发商；见批次核验后换合格货，不把返潮米换名出售给主角'),
'DEALER':('车贩','40岁中国成年男性，短发、浅灰衬衫、黑长裤','二手车商，先压价后六万成交'),
'UNCLE':('表叔','52岁中国成年男性，稀短黑发、棕色针织衫','质疑借贷与囤货的亲戚；前十集不登门求救'),
'DRIVER':('司机','38岁中国成年男性，寸头、浅蓝工作外套','货运司机；按主角调度分流车辆'),
'CLERK':('药店店员','32岁中国成年女性，短黑发、浅绿药店工作服','按处方规则拒绝大批量购药')}
scenes={
'OLDHOME':'梧桐里3栋101外层旧客厅：一楼小院入户，普通尺寸防盗外门朝楼道，外门有观察口、门链；客厅暖灰墙、旧木桌和沙发；右后卧室门通折叠空间。没有大开间落地窗，陈屿能从内侧观察口看见门前。',
'HALL1':'Lv1折叠大厅：约200平方米，入口是普通卧室门框，哑光暖白墙、浅灰干燥地坪；初期空旷，EP003起货架与纸箱较满但保持入口通道；尚无系统厨房浴室。',
'HOME2':'Lv2折叠安全屋：入口接一条宽约1.2米的清楚通道，左侧紧凑厨房与四人餐桌，后方走廊连接四间卧室，浴室邻厨房但不敞开；仓储区在通道右侧。哑光木地板、暖白墙、暖色生活照明；保留有限物资，不画豪华无边宫殿。',
'ROOM2':'Lv2靠入口的夏凛卧室：一张单人床、一张小桌、素色衣柜，门锁为普通室内锁；浅木哑光地面，整齐但非空无一物。',
'BATH2':'Lv2浴室：浅灰瓷砖、普通浴缸和金属龙头，热水仅在浴缸内部；镜头不含裸体，房间外围保持干燥。',
'CORRIDOR':'101门外公共走廊及入户台阶：101深灰外门，与王大富家对门，短段楼梯转角在侧前方；两盏外置探照灯固定在101入口上方并覆盖台阶与转角，控制线从规范走线孔进入客厅。血月时冷红环境光、灯开时局部白光。',
'COURTYARD':'101一楼小院：低矮窗台、单扇入户门、简洁步道和少量绿植，无杂物，日常光线自然。',
'OFFICE':'物流园仓储办公室：普通办公桌、电脑、纸质签收单、金属文件柜，夜间仅一盏工作灯。',
'PARKOFFICE':'同一物流园办公楼管理办公室与走廊：浅灰墙、木门、普通办公桌，白天平光。',
'PARKGATE':'物流园出口：岗亭、栏杆、干燥水泥路面；人物能在门外停留交谈，不挡车。',
'WAREHOUSE':'物流园B7中转库：普通高顶仓库、食品与建材明确分区，几排金属货架、托盘、黄线通道；叉车工作时与人保持安全距离。燃油不在此库。',
'FUEL':'物流园独立燃料储位：隔离围栏与少量密封桶，有合规管理标识的形状但不生成字；与食品库为不同场所。',
'GUARD':'物流园岗亭：窗口、监控桌、工作椅、旧笔记本，凌晨冷白灯，监控屏不添加无关人物。',
'MARKET':'粮油批发市场室内摊位：大米袋按批次整齐分垛、木台面、少量检验单，清晨平光，未合格米仅袋内局部异常，不渲染潮湿环境。',
'GATE':'梧桐里小区门口与单元门：正常城市住宅，消防通道通畅；送货时车辆待调度，不能画八车堵死救援通路。',
'CARLOT':'城市二手车行：一辆无品牌旧灰色轿车为主，停车位和小办公桌，白日干燥。',
'RESTAURANT':'普通中餐厅包间：圆桌、少量菜碗，主要人物陈屿和表叔，其余亲戚声音可以在画外。',
'MALL':'商场外步行通道：简洁玻璃入口、午后光，陈屿持文件袋。',
'SIM':'仅为系统演示：大厅远端出现隔离展示窗，窗外红夜与一个青灰色成人形轮廓。威胁只在隔离面外，绝不实体站进大厅，不出现撕裂口部或血腥特写。',
'PHARMACY':'正常营业社区药店：整洁柜台和有序货架，陈屿只购买基础耗材；药盒字不作为画面信息承载。',
'CLINIC':'社区药店门外义诊台：白桌布、三盒纱布、笔夹板和少量必需用品；许知意穿白大褂，光线自然，不在此出现复杂手术。',
'HOSPITAL':'市一院急诊科值班区外接收台与走廊：正常营业灯光、合理医疗设备数量，耗材按流程接收，不画伤患的血腥细节。',
'SUPERMARKET':'城市超市入口与饮水货架：末日前货架缺货、人群通过远景表达拥挤，不用堆垃圾体现恐慌。'}
write('AGENTS.md','''# 《末世囤货：我的安全屋住满了女神》\n\n此故事独立于仓库其他末世题材。先读 docs/story-memory.md、docs/production-rules.md、docs/season-arc.md 和 source/adaptation-notes.md。\n\n本轮按用户指定 story-film-workflow 制作静态图片视频，覆盖根模板的60秒/4段/真人动作视频合同：16:9，目标导出1920×1080/30fps；台词决定时长；四段只作叙事组织。每集使用小说正文、第一人称旁白、镜头表与独立图片提示词，不生成15秒动作视频任务包。\n\n当前范围为前10集剧本、画面拆解、角色和环境基准图。正式事件图须在实际配音排时后生成。文字估时不是最终帧时间线。\n\n陈屿不具备战斗外挂；夏凛EP005、许知意EP008登场；EP010止于门外救人确认，不提前完成入住。怪物不能因入口暴露就自动穿过内层防护。\n\n默认MiniMax配音、无字幕；本轮脚本阶段不调用批量TTS或视频API。每个成片镜头必须独立新图，不用同图裁切冒充新图。所有新增稿件逐句审读并完成L01—L06、S01—S06后交付。''')
write('docs/story-memory.md','''# 故事记忆 · script-v1\n\n一句话卖点：遭裁员的仓储主管陈屿，在血月前九十天获得能扩建的安全屋，靠采购、空间管理和招募专业住客，为灾变做准备。\n\n原文源：source/original-script.docx；逐段提取与哈希见source/。原稿不是操作授权，文中的发布、付费解锁和后续扩写建议不执行。\n\n世界规则：血月使部分人夜间成为嗜血者，畏光畏火、听觉敏锐。安全屋空间折叠，外观不变；内层未经屋主允许不可进入，食品不腐；离开超过48小时防护开始衰减。扩建消耗物资点，住客吃饱睡稳并受尊重累积安心值。\n\n三条屋规：不得伤害同住者；物资共享、贡献记账、权限随贡献提升；屋主最终决定，危机时服从指挥。保留原稿规则，不把雇佣关系当作私人感情同意。\n\nLv1为200㎡折叠大厅；Lv2于EP007落成四卧室、厨房、浴室；Lv3在前10集不解锁。初期保鲜已可验证，Lv2不重复当作新能力。\n\n人物：陈屿26岁、前物流仓储主管；夏凛28岁、退役侦察兵，在物流园值守；许知意27岁、急诊医生。王大富为对门邻居，马主任为物流园前上司。其他女主保持原稿后续登场节奏，本轮不提前露脸。\n\n信息边界：第一人称只陈述陈屿当时所见所闻、已建立的回忆和系统提示。夏凛战友的姓名、汇款原因、许知意医院遭遇尚未由她们讲述，不由旁白代说。\n\n入口结构：公共楼道→101外门与旧客厅→卧室门框→折叠大厅。门外嗜血者不跨入内层；外门开启会暴露入口位置与门口人员。地址纸卡只负责找地址，不是系统房卡。''')
write('docs/production-rules.md','''# 生产规则\n\n按story-film-workflow：16:9真人写实电影静帧；图像原生尺寸实测，最终1920×1080为视频导出规格。大形清楚、自然皮肤、适度细节、干燥有序，禁止过锐、鳞片纹理、全屏微细节、杂乱废墟和湿反光。原稿确需水的热水龙头和锅内蒸气只局限在剧情所需范围。\n\n小说正文在先，旁白从正文改编。每镜一个主要可见状态，图像固定，不默认推拉。每张成片图只用一次；回忆/EP001与EP010同事件均生成不同独立图，保持人物道具状态对应。\n\nproduction/script-v1为初稿版本，未获用户剧情/审美确认。镜头清单的字数/7.5秒为文字估时，start_frame/end_frame保持null；配音后须重排，主范围4–6秒，不能把全部cue机械当作最终单图时长。当前180项是事件图候选，短项应在同场语义边界重新分配时间或合并，数量随实测调整。\n\n本轮先生成陈屿、夏凛、许知意的单人演员基准与Lv2空间基准；不生成180张无音频排时的最终事件图。基准图不可直接反复拿去拼成片。\n\n声音默认speech-2.8-turbo/Chinese_calm_streamer_nv1；单叙述者复述必要对白，不用同音色伪装已锁定多演员。情绪与语速须先试听，voice-plan.json只记录建议。无字幕，不生成SRT/VTT。\n\nsource/adaptation-notes.md是原文差异记录；source/原稿保持不变。assets/manifest.json记录基准图prompt、来源、hash与选用状态。''')
write('docs/workflow.md','''# 本故事工作流\n\n1. 原稿归档、提取、核对前十集及规则。\n2. 小说正文→陈屿第一人称旁白，逐集执行12项语义审读，记录稿件hash。\n3. 给出事件图候选与独立prompt；文字估时不冒充实测。\n4. 生成三名主角与Lv2空间基准；视觉选择为待用户审美确认。\n5. 后续制作时先短段试听，再逐cue生成MiniMax配音；ffprobe测时并核对句群内部边界，按4–6秒主范围重排镜头。\n6. 每镜生成独立新图，绑定参考职责/hash，检查近重复、人数和状态；不复制基准图代替事件图。\n7. 本地合成有声无字视频，统一整数帧时间线，0.1秒外部空档与叠化只计一次。\n8. 分开记录完整解码、正常速度播放、观看和审美意见。\n\n本轮不调用视频API；视频API交付合同只作为后续用户另行选择真人动作视频路线时的参考，不在静帧工程创建空提交记录。''')
write('docs/audience-strategy.md','''# 观众与表现\n\n题材承诺为囤货、经营升级、门内门外反差、专业成员入队和信任积累。前十集的具体回报依次为折叠空间、保鲜验证、筹钱和首批库存、仓储管理、守卫亮相、签约入屋、厨房浴室、医疗联系、灯具备防、灯光救援。\n\n开场用正在发生的损失/限制/异常，结尾用当前事件的具体后果续接；不反复宣布主角觉悟，不用一句讽刺替代实际回报。每集有冲突、选择、结果。\n\n标题中的“女神”沿用原稿名称；成员靠专业能力和共同生活推进，不把女性当物资展示。前十集只建立夏凛与许知意的关系，不增艳遇或争宠。\n\n借鉴仓库抖音方法的钩子—加压—变化—后果，不沿用其固定60秒、9:16和视频API动作要求。文案审读通过不等于平台表现得到验证。''')
write('source/adaptation-notes.md','''# 原稿与script-v1改编记录\n\n保留：标题、人物姓名年龄身份、血月前90天、41.2万存款、78万贷款、6万卖车、空间200㎡、前10集主线、夏凛EP005及许知意EP008登场、EP010开门确认卡点。原稿本身已有前10集分集，当前是静帧/旁白适配，不宣称补写了原稿缺失的十集。\n\n|原稿问题/表达|本版处理及理由|\n|---|---|\n|第1集已全额信用卡套现，第2集又78万借款，后文总债务口径不同|本版只保留一次78万借款，EP002申请，EP003到账；信用卡不重复计资|\n|118万一人清单与后续15万预付冲突|118万是最初计划；签约前削减两项设备，新现金上限125.2万，工资15万、备用8万、采购及运输102.2万；不声称所有原计划已采购|\n|八车已到、Lv1满仓，后续继续大采购|EP003分流六车，EP004租B7并卸货；后续为分批订单，燃料独立储位，至EP007仅逐批调入，不凭空扩容|\n|老米砍价后直接当新米交易|明确拒绝异常批次，换有检测单的合格批次后另谈三千二；原稿砍价四成不作为实证|\n|月薪五万、日结、一次付三个月混用|统一三个月合同、15万预付；先现场查验后到账签字|\n|男主全知夏凛战友汇款、独立岗亭内心戏|只写陈屿看到狗牌、浅疤和合本子时的一笔8000；不给出未听说的战友姓名与原因|\n|半空泡面、比刚买更甜容易引出未定义能力|以实体落地和保鲜对照表现空间；不新增悬浮、食物增甜|\n|药店凭备货清单大量开处方，次集来源不明药品捐赠|只购买基础耗材；处方按具体诊疗；医院捐赠为有票据耗材并登记|\n|大功率灯通过猫眼照退怪物，照射路径不成立|EP004采购灯电源，EP009测试两盏外置灯、内侧控制、备用电源，EP010兑现；不是从猫眼射激光|\n|第1集惨叫暗示邻居死亡，第10集逃回对门|冷开场只预告求救，EP010明确王大富逃回对门；不写死亡假象|\n|第9集24小时与今晚邀请容易错一天|EP009约明晚烧烤，EP010明示第二天晚上归零|\n|绝对安全与开门暴露看似矛盾|保留原系统提示：暴露是入口可被定位，未开放准入不使怪物自动穿过内层，门外接应仍有风险；不增防护失效|\n|字幕、黑屏付费及视频拍摄提示|只作原稿资料；本版无字幕，EP010悬念保留，不替用户发布收费内容|\n\n这些为本次未确认初稿的适配选择，后续可依据用户意见修订；原文件完整保留。''')
arc=['# 前10集与后续衔接 · script-v1','','|集|标题|时间|本集兑现|结尾续接|','|---|---|---|---|---|']
for e in eps:arc.append(f"|{e['episode']}|{e['title']}|{e['day']}|{e['payoff']}|{e['hook']}|")
arc.extend(['','EP011从是否开门及接应许知意开始，本轮不提前写成入住。后续乔星野EP014、顾南枝EP020、岑月EP028、宋清晏EP052按原文角色专节与登场节奏保留；原文其他概要对岑月登场有23—26集版本，待扩写相应章节再确认，不本轮擅自改为提前出场。','后续等级/人员上限/终局依原文，前10集不提前引入同类持有者身份；EP001仅埋信号。'])
write('docs/season-arc.md','\n'.join(arc))
write('production/script-v1/brief.md','''# script-v1制作简报\n\n片名：《末世囤货：我的安全屋住满了女神》。本轮交付前10集小说式正文、陈屿第一人称旁白、逐镜事件候选、完整生图提示词、连续性和语义审读记录，以及角色/场景基准图。\n\n16:9真人写实静帧；最终导出目标1920×1080/30fps；原稿约90秒仅作量级参考，当前按每秒7.5个非标点字估时，最终以配音为准，不强凑90秒。\n\n当前无TTS，无最终音轨时间线，无成片，未获剧情或画风审美认可。前置图片为三名演员和Lv2空间，正式事件图待实测排时后逐镜生成。\n\n可读总稿：前10集剧本.md。机器源：episode-data.json。每集episodes/EPxxx含novel.md、narration.md、narration.txt、storyboard.md、shots.json、image-prompts/、qa-checklist.md及voice-plan.json。''')
for aid,(name,description,role) in actors.items():
 write(f'assets/characters/{aid}/00-character-card.md',f'# {name} · {aid}\n\n身份与叙事：{role}。\n\n本版外貌设计（原稿未给处由本次补定，待审美确认）：{description}。\n\n同人脸、年龄、发型与体格保持一致；当镜头无此人不加载此角色参考。参考只锁身份服装，不复制参考的姿态、构图或背景。')
for sid,desc in scenes.items():write(f'assets/scenes/{sid}/scene-card.md',f'# {sid}\n\n{desc}\n\n只锁空间，不自动添加全部角色。画面保持干净、干燥、有秩序，危险用距离、表演和光线承载。')
props={
'P_LEDGER':'采购本与资金本，EP002开始记录；不可每张图强求所有数字准确，关键信息靠旁白。',
'P_ADDRESS':'EP009写给许知意的普通地址纸卡；不发光、不具备系统开门权限；EP010仍在她手中。',
'P_ROOM_KEY':'EP007夏凛卧室普通钥匙，只开卧室；不等于安全屋授权房卡。',
'P_LAMPS':'EP004采购灯具和匹配电源；EP009固定两盏到101入口上方，照射台阶和转角，控制器与备用电源在客厅；EP010门闭合时可用。',
'P_DOGTAG':'夏凛的旧狗牌，通常衣领内；本轮不交给陈屿，不凭此揭露战友隐情。',
'P_MEDKIT':'EP007为空；EP008放入基础耗材，处方项未凭空补满。',
'P_GOLD':'王大富称有十根金条，使用小布袋拿在手里；不新增主角抢夺或收走金条。'}
for pid,desc in props.items():write(f'assets/props/{pid}/prop-card.md',f'# {pid}\n\n{desc}')
style='真人写实电影静帧，横向16:9构图；自然肤质和衣物材质，主体轮廓清楚，适度细节，不过度锐化；背景有秩序，干燥哑光地面、墙面与衣物；除本镜明确需要的局部物件外，不加水珠、雨雾、湿反光、重污渍、垃圾、密集微纹理；无字幕、无标题、无水印、无分镜拼贴、无游戏UI。'
write('assets/style/global-style.md','# 视觉风格\n\n'+style+'\n\n家中暖白/琥珀，外部血月冷红；对比来自实物和光线，不依赖满地血或破败。')
write('assets/style/camera-language.md','''# 机位\n\n第一人称为陈屿的叙述身份，并非全部主观摄影。允许正面、侧面、过肩、手部、门框与环境。每图固定构图，一个可读事件。人物/道具细节与空间全景交替，避免连续十张同一张脸。''' )
write('assets/style/negative-prompts.md','''# 相关限制\n\n只添加本镜需要的角色参考。监控人物、演示怪物与现实演员不混入同一房间；无未授权角色、无跨空间门框变形、无湿反光、无血腥伤口特写、无满屏文本、无拼图。不要用长负面词表覆盖具体事件。''')
combined=['# 《末世囤货：我的安全屋住满了女神》\n\n前10集 · script-v1\n\n小说式正文＋陈屿第一人称旁白。按原稿改编，时间为文字估算，尚未配音。每集都有独立画面拆解文件。']
index=['# 前10集交付索引','','|集|标题|旁白字数|文字估时秒|候选画面|','|---|---|---:|---:|---:|']
manifest=[]
for e in eps:
 eid=e['episode'];d=R/'episodes'/eid;d.mkdir(parents=True,exist_ok=True)
 write(f'episodes/{eid}/novel.md',f"# {eid}《{e['title']}》·小说式正文\n\n版本script-v1；剧情时间：{e['day']}。\n\n{e['novel']}")
 narr='\n\n'.join(s['narration'] for s in e['shots'])
 write(f'episodes/{eid}/narration.md',f"# {eid}《{e['title']}》·第一人称旁白\n\n陈屿单叙述者版，角色对白由他转述；导演说明不进朗读文本。\n\n{narr}")
 write(f'episodes/{eid}/narration.txt',narr)
 rows=['# 画面拆解（文字预排）','','时长按非标点字数/7.5估算，外部cue空档0.1秒，仅加一次。当前为事件图候选：短项待实际配音后在同场语义边界合并或移动图像切点，不照搬cue边界；最终主范围4–6秒，start_frame/end_frame尚未锁定。无最终事件图。','','|镜头/旁白cue|估计音频范围（秒）|估计画面秒|人物/场景|唯一事件与构图|','|---|---|---:|---|---|']
 elapsed=0;voice=[]
 for i,s in enumerate(e['shots']):
  c=len(re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]','',s['narration']))
  dur=c/7.5;gap=.1 if i<len(e['shots'])-1 else 0
  s.update(dict(audio_estimate_seconds=round(dur,3),estimate_start_seconds=round(elapsed,3),estimate_end_seconds=round(elapsed+dur,3),estimated_display_seconds=round(dur+gap,3),external_gap_seconds=gap,timing_status='TEXT_ESTIMATE_ONLY',start_frame=None,end_frame=None,image_path=None,image_sha256=None,reference_paths=[],reference_status='BIND_AFTER_BASELINE_SELECTION',image_status='NOT_GENERATED',duration_exception_reason='文字估时短于4秒，实测后优先调整同场图像切点或合并；不得照此固化最终短镜' if dur+gap<4 else None))
  names='、'.join(actors[a][0] for a in s['character_ids']) or '无实体角色'
  desc='\n'.join(f'{a} {actors[a][1]}' for a in s['character_ids']) or '没有可见的主角实体；按事件描述决定是否有远景威胁轮廓。'
  prompt=f"{style}\n\n人物与参考职责：\n{desc}\n仅出现本镜描述人数；演员图只锁身份，不把参考背景搬入。本镜不加载其他人物图。\n\n地点/时刻：{scenes[s['scene_id']]} 剧情时间：{e['day']}。\n本镜唯一状态与构图：{s['visual']}。\n旁白语境（不是画中文字）：{s['narration']}\n场景参考只负责布局，风格参考只负责色光。本镜生成一张全画幅独立新图，不能以既有成片图的裁切、缩放或调色冒充。文字与数字均由旁白传达，不要求画中生成可读汉字。\n"
  s['prompt']=prompt
  write(f'episodes/{eid}/image-prompts/{s["shot_id"]}.txt',prompt)
  rows.append(f"|{s['shot_id']} / {s['cue_id']}|{elapsed:.2f}–{elapsed+dur:.2f}|{dur+gap:.2f}|{names} / {s['scene_id']}|{s['visual']}|")
  preset='suspense' if e['episode'] in ['EP001','EP002','EP009','EP010'] else 'documentary'
  voice.append(dict(cue_id=s['cue_id'],speaker='陈屿（含对白转述）',model='speech-2.8-turbo',voice_id='Chinese_calm_streamer_nv1',emotion='calm',speed=.98,vol=1,pitch=0,preset_hint=preset,source_text=s['narration'],tts_text=s['narration'],direction='克制、口语、句群推进；对白转述保留语义，不表演成另一个固定演员。实际语速须先短段试听；此处参数未提交。',subtitle_enable=False,audio_path=None,audio_duration_seconds=None,audio_sha256=None,status='NOT_RUN'))
  elapsed+=dur+gap
 write(f'episodes/{eid}/storyboard.md','\n'.join(rows))
 write(f'episodes/{eid}/shots.json',json.dumps(e['shots'],ensure_ascii=False,indent=2))
 write(f'episodes/{eid}/voice-plan.json',json.dumps(voice,ensure_ascii=False,indent=2))
 index.append(f"|{eid}|{e['title']}|{sum(len(re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]','',s['narration'])) for s in e['shots'])}|{elapsed:.1f}|{len(e['shots'])}|")
 combined.extend([f"\n## {eid}《{e['title']}》\n\n时间：{e['day']}\n\n### 小说式正文\n\n{e['novel']}\n\n### 第一人称旁白\n\n{narr}"])
 manifest.append(dict(episode=eid,title=e['title'],script_version='script-v1',novel_sha256=hashlib.sha256((d/'novel.md').read_bytes()).hexdigest(),narration_sha256=hashlib.sha256((d/'narration.txt').read_bytes()).hexdigest(),shot_candidates=len(e['shots']),text_estimate_seconds=round(elapsed,3),actual_audio_seconds=None,final_image_count=0,status='SCRIPT_READY_BASELINES_PENDING'))
write('production/script-v1/前10集剧本.md','\n'.join(combined))
write('production/script-v1/index.md','\n'.join(index))
write('production/script-v1/script-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
write('README.md','''# 末世囤货：我的安全屋住满了女神\n\n独立Story ID：goddess-safehouse。采用story-film-workflow静态图片视频路线。\n\n- 前10集总稿：production/script-v1/前10集剧本.md\n- 分集索引与文字估时：production/script-v1/index.md\n- 每集正文、旁白、镜头、prompt与审读：episodes/EP001—EP010/\n- 原稿与适配说明：source/\n- 人物/场景/道具卡及基准图片：assets/\n- 规则与时间线：docs/\n\n当前为script-v1初稿与基准图阶段；无配音、无最终镜头时间线、无成片。180个画面候选不是180张已生成图片。\n\n每个正式镜头约5秒，实际配音后以4–6秒为主重新定图像切点和数量；同一成片不重复用图。''')
print('built',len(eps),'episodes;',sum(len(e['shots']) for e in eps),'image prompts')
