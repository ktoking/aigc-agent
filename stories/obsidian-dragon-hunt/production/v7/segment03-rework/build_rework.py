"""在原EP001同步segment03的30秒对抗改稿，不调用生成服务。"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]
EP = ROOT/'episodes/EP001_valsak_v3_seasons'
SEG = EP/'segment_03_60-90s'
HERE = Path(__file__).resolve().parent
shots = [
 dict(id='SH22', start=0, end=4, title='龙先抢攻，法师在压力下落石',
      event='龙撤回被斧击的西前爪，中央首压低横咬，逼兽人侧跨撤斧；后足蹬地，胸躯向南抢进约两米。西首盯住法师开始吸气。法师后脚踩实、转髋稳杖，抬眼确认高空落点，掌心只下压一次；一块不规则陨石从云后开始陡直下坠。',
      camera='东南侧35mm中广景保留兽人侧步、龙前后足与法师承重；短上摇揭出高空落石，不把杖尖连到陨石。',
      weight='龙的后足先推、肩胸后移；法师有后撤半步和衣摆受风，龙没有停下来等法师表演。',
      expression='兽人盯咬击方向、咬牙侧撤；法师冷脸判断而非摆展示姿势。',
      sound='爪刮岩、斧柄抽离、近处咬合与高空落石低频。',
      state='龙主动抢攻；陨石已离开云层，之后沿重力轨迹完成下坠。'),
 dict(id='SH23', start=4, end=8, title='负重闪避，陨石落地碎裂',
      event='中央首发现落石，龙以后足为支点向西跨步，肩胸外转并向北撤回；三条颈因惯性先滞后再回摆。陨石从高处陡角下坠，擦开东侧共用颈根的外甲，继续向下砸进北后侧空地，当场碎裂成坠石和短促尘浪。龙落足稳住后立刻转眼寻找法师。',
      camera='东侧低广景连续读清来石、负重跨步、擦甲与北后方落地；落地后才短震，不跟着石头横向飞。',
      weight='完整落体：高空下坠→擦甲→地面撞击→碎裂散落。陨石无持续推进火口，不回升、不拐弯追踪；主体残块留在落点。',
      expression='龙侧首收颈避让，中央首立刻找施法者；法师追随落点而非继续遥控。',
      sound='护甲钝裂、陨石撞地、重块滚停；先接触后声浪。',
      state='龙收回中央偏北，体位目标约(0,81)；东侧同一外甲初裂，内膜完整；北后侧形成陨石坑。'),
 dict(id='SH24', start=8, end=12, title='四弹离舱，侧首主动截击',
      event='机器人在南岩后跨步站稳，身体跟着移动中的裂甲转向，每肩各两枚、总共四枚导弹短间隔交替离舱。龙西首追着弹道甩颈，短喷火在空中引爆其中两枚；另外两枚从东侧空隙继续接近原裂甲。龙的前足持续调整支撑，中央首转向机器人的掩体。',
      camera='机器人肩舱近中景交代四次离舱和每肩剩一枚，接同轴东侧广景看两次空爆与两条仍在接近的弹道。',
      weight='发射先点火再离管，机身有短反冲；同一枚弹不复制。四枚分别结束于两处空爆与两处甲上爆炸，空爆的弹体立即销毁。',
      expression='机器人锁定环跟随龙身修正；西首目光真实追弹并提前迎击。',
      sound='四次短发射，两次分开的空爆，机足摩擦岩面。',
      state='累计发四枚，剩两枚；两枚已空爆，另两枚尚未命中，龙继续进攻。'),
 dict(id='SH25', start=12, end=15, title='命中完结，龙用扫火迫退机器人',
      event='余下两枚先后撞进同一东侧裂甲，触发引信后立即爆开，完整弹体消失，短碎片向下落。龙东侧胸肩被震偏，前足补一步支撑，中央首随即向南横扫一道短火流。机器人已经发完首轮，立刻低头、重步退到原南岩背后，火流擦过岩顶。',
      camera='同一东侧裂甲中景读清两次命中，再顺龙首视线切机器人退入掩体；两张画面方向一致。',
      weight='每枚撞击到弹体销毁只占瞬间，爆后不再保留完整导弹、推进尾焰或连回发射器的烟线；导弹不钉在甲片或脚上。龙以承重补步承受爆压，随后反击。',
      expression='龙因命中短促偏头，迅速反抢；机器人主动避火，不原地看命中。',
      sound='两次相隔短拍的闷爆、碎甲落地、扫火和两步沉重机械脚步。',
      state='同一外甲扩大破损，内膜完整；导弹首轮已全部销毁，机器人移到原南岩背后，剩两枚。'),
 dict(id='SH26', start=15, end=19, title='藤蔓截住换脚，双方互相拖动',
      event='龙抬前爪准备再进，瑟琳压掌催根。第一道藤掠过抬起的爪尖扑空；她立即转腕，根束贴地回卷，在另一前足落地承重时扣住脚踝，第二路根同时绕住后踝、咬进两侧基岩。龙想继续迈步，后踝被绷紧的藤束拉住，肩身失衡半拍，展翼找回支撑。拉力沿根束传回，瑟琳前滑约半米，以膝抵岩、另一手撑住裂缝。',
      camera='东侧低位跟脚与根的先后接触，再沿绷紧根束回到精灵被拖动的手和膝，动作不断因果。',
      weight='藤扑空一次再成功截步；先接触、绕踝、扎根，最后张紧。脚在活动，藤也随脚受力，精灵实受反冲。',
      expression='精灵从判断落足转为吃力，手背绷白；龙立即补足撑身，不静止配合缠绕。',
      sound='爪尖刮石、根入岩、藤束骤绷、膝甲碰岩和短吸气。',
      state='精灵争得一次短暂绊步窗口，龙颈和翼仍自由；部分前足和后足根束受力，精灵保持原东南施法位。'),
 dict(id='SH27', start=19, end=22, title='烧藤再扯断，后足束缚仍有效',
      event='中央首俯下短喷火，前圈藤皮先焦黑。龙压肩扭爪猛拽，烧弱的纤维才逐股断开，断端沿张力回弹。它再向前抢半步，后足根束骤然绷直，把后踝拉回，龙胸下沉、三首分别收颈找平衡。瑟琳被带低后迅速压住另一束根，仍拦着它的第二步。',
      camera='东侧中广景保留龙口—火—前足藤束，随后不切断地面锚点便读到后踝受阻；短切精灵反冲。',
      weight='火烧弱后靠爪力扯断，后足根不凭空消失；有效束缚表现为打断一步，持续对抗而非整龙定身。',
      expression='龙有明确挣脱意图；瑟琳痛吸气仍改抓另一束根，没有站着旁观。',
      sound='短龙息、焦藤纤维断裂、断端抽岩、后足再次压地。',
      state='前圈已断且残根在地；后足根束仍有效，龙胸和三颈在活动；给刺客绕行留下短窗。'),
 dict(id='SH28', start=22, end=26, title='刺客边跑变装，东首追踪反咬',
      event='烬趁龙与藤根拉扯已经沿东壁起跑，手触晶扣后衣甲贴身收束，兜帽半面罩在跑动中扣合，右腕刃仍折叠贴臂。东首发现侧边运动，目光先转、颈根再带动下压探咬；烬低身借岩壁遮挡继续前进，衣摆延迟掠过石角。',
      camera='东侧沿墙平移跟同一个人，从触扣到装备扣合均在连续跑动中；画面远处保留龙东首转向作为追击来源。',
      weight='变装不停止脚步，头脸角和体型不变；龙眼—颈—头依次追踪，颈部有惯性，角色靠脚步与掩体避开。',
      expression='刺客专注判断咬击角度，目光先扫掩体；东首主动捕捉他，不等他靠近。',
      sound='连续落足、衣甲扣合、近处吸气、颈部掠风；无语言。',
      state='A1已完成，右腕刃仍折叠；沿东壁路线连续，未隐形或传送。'),
 dict(id='SH29', start=26, end=30, title='咬击擦过岩沿，小队抢下一拍',
      event='烬在东侧低骨坡急停压身，东首咬击擦过他身前岩沿，咬下一角碎石，巨颈因惯性越过后再拉回。烬贴掩体稳住脚，回看裂甲。兽人借龙重心拉扯向西前爪推进，瑟琳补紧后足根束，机器人从同一南岩探出肩舱，剩两枚仍在。龙后躯再次收压准备展翼，中央首仍威胁前沿。',
      camera='东侧跟到低骨坡，以岩沿和龙首咬合交代险距，再小拉开看西前爪、南岩和东南根锚；不跳到全队并排站姿。',
      weight='人先刹步再借掩体避咬，龙头有过冲回收；尾帧双方都在持续准备和承重，不做胜利摆拍。',
      expression='刺客短喘后看准裂口，支援者持续吃力；龙是仍在反扑的威胁。',
      sound='爪步、咬石钝响、局部碎石、紧绷根声与两枚舱锁开声。',
      state='90秒：龙体回到中央偏北约(0,81)，朝南，东侧旧裂口仍在；后足束缚、前圈断根、陨石坑保留。刺客到东侧(10,70)低骨坡后，机器人仍南岩且剩两枚。接segment04钩爪/补根/末轮破甲。')
]
assert sum(s['end']-s['start'] for s in shots)==30

refs = [
 ('动作预备首帧：仅图1决定0秒构图；法师、兽人及三头龙已在相互威胁', SEG/'frames/motion-v7/first-frame.png'),
 ('三头龙身份与结构：同一龙的三视图，只取模型，不复制视图或站姿', ROOT/'assets/characters/VALSAK/three-head-v6/three-view.png'),
 ('机器人身份与肩舱：每肩三管，初始全装，首轮4枚后每肩剩1枚', ROOT/'assets/characters/ROBOT/combat-v6/three-view.png'),
 ('精灵身份：同一瑟琳的三视图，只取脸、银发和月白靛蓝袍', ROOT/'assets/characters/ELF/turnaround-v1/three-view.png'),
 ('刺客A1身份：同一烬的三视图，只取脸、角、装备和右腕挂点；先跑动后变装', ROOT/'assets/characters/DRAGONBORN/assassin-a1-v4/three-view-v2.png'),
]
for _, p in refs: assert p.is_file(), p
refmap = [{'index':i,'path':str(p.resolve()),'purpose':label,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
          for i,(label,p) in enumerate(refs,1)]
(HERE/'input-map.json').write_text(json.dumps({'version':'v7','duration':30,'ratio':'16:9','references':refmap,
  'excluded':['旧十张近似站姿关键帧不作时间顺序约束','含完整导弹抵住皮肤的命中静帧不作持续状态','不把中途的烧藤或命中图指定为首帧'],
  'submit_status':'NOT_SUBMITTED'},ensure_ascii=False,indent=2)+'\n')

head = '''30秒，16:9，欧美奇幻电影级写实CG。六位成年虚构角色身份沿资产；同一山谷连续作战，无对白、旁白、字幕或歌词。
重点是双方抢攻、反制与被迫调整：巨龙在接触前主动移动，命中后承重失衡并反击；人类与机械体也有闪避、拖步、痛感和重新支撑。角色不能在技能之间回到统一的展示站姿。
三头三颈共用一个胸躯，四足、双翼、单尾；中央首压前沿，西首截弹，东首看侧翼。三颈有独立视线和惯性，不能把三头复制成三条龙。身体负重步态参考大型猛兽，颈部追击有蛇类式过冲回收，翼只助力与平衡。
摄影机保持战斗轴东侧。北洞与陨石落点在龙后，南岩为机器人掩体，法师西南、精灵东南、兽人西前沿、刺客沿东壁，游侠留东高台。本段机器人仅退到原南岩后，段尾再探出，不换掩体。体位数字仅供预演，画面优先保持这些地标和双方距离。
'''
bindings='\n'.join(f'<图片{i}>：{label}。' for i,(label,_) in enumerate(refs,1))
body=[]
for s in shots:
    body.append(f"{s['start']}—{s['end']}秒：{s['event']} 摄影：{s['camera']}")
ending='''
投射物必须完结：陨石沿陡直重力轨迹向下，擦肩后撞地碎裂并留坑；不能从法杖发射、悬停、回升或转弯。四枚导弹分为两枚空爆、两枚甲上爆炸；触发即销毁完整弹体，碎片落下，禁止钉在龙脚/皮肤上继续燃烧、持续连着尾烟、复制新弹。
藤根必须有双方受力：移动脚先让藤扑空或受拉，再形成有限绊步；龙烧前圈再用爪力扯断，后足根仍绷紧，精灵被反拖、跪撑后再加力。嘴和翼可继续攻击，不能整龙定住配合缠绕。
全速为主，只在真正接触瞬间短促停顿，随后立即失衡和恢复。保留爪、脚、武器、地面接触与撤离过程；烟火不遮盖所有命中点。绝不出现完整导弹挂脚、陨石反弹飞走、滑行代替迈步、刺客瞬移、全员等候摆拍。右腕刃本段始终折叠，segment04落稳后才展开。段尾龙仍危险、队员仍用力，6枚弹剩2枚，同一颈根伤口、断藤、原掩体保留。'''
director=head+'\n'+bindings+'\n\n'+'\n\n'.join(body)+'\n'+ending+'\n'
(SEG/'director-promt.txt').write_text(director)
(SEG/'prompt.md').write_text('# Segment03 v7｜30秒双向对抗导演提示\n\n'+director)

board=['# Segment03 v7｜陨石、导弹与束足的双向对抗','','全片60—90秒，仍为一个30秒segment。八个镜头节拍，不拆成15秒目录。','']
for s in shots:
    board += [f"## {s['id']}｜局部{s['start']}—{s['end']}秒／全片{60+s['start']}—{60+s['end']}秒｜{s['title']}",'']
    for label,key in [('事件','event'),('摄影','camera'),('受力与生命周期','weight'),('表演','expression'),('声音','sound'),('镜末状态','state')]:
        board += [f'- {label}：{s[key]}']
    board += ['']
(SEG/'storyboard.md').write_text('\n'.join(board))
(SEG/'first-frame.md').write_text('# Segment03首帧｜v7\n\n当前文件：frames/motion-v7/first-frame.png。\n\n三头龙正撤回受伤西前爪并抢攻兽人，法师在西南承重预备下压手势；陨石尚未出现。此图只锁0秒构图和身份，后续必须有移足、侧撤、俯首和重心转移。不得把首帧龙姿当作30秒站姿。\n')
(SEG/'last-frame.md').write_text('# Segment03尾帧目标｜v7\n\n30秒／全片90秒：'+shots[-1]['state']+'\n\n三首仍追踪对手，后足根束张紧、胸部随呼吸和挣脱移动。刺客贴低骨坡喘息，兽人与精灵持续承重，机器人从原掩体探出。不是全队列阵或巨龙定身。当前为尾帧文字目标，尚无新版视频实测尾帧。\n')

tp=EP/'timeline.json';t=json.loads(tp.read_text());by={s['id']:s for s in shots}
for sh in t['shots']:
    if sh['id'] in by:
        s=by[sh['id']]
        for k in ['event','camera','expression','sound','state']:sh[k]=s[k]
        sh['weight']=s['weight'];sh['motion_version']='v7-contested'
t['segment03_motion_version']='v7-contested';t['version']='v7-segment03-motion-in-place'
tp.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
eptext=(EP/'episode.md').read_text();a=eptext.index('## 第三段');b=eptext.index('## 第四段',a)
prose='## 第三段 60—90秒｜落石逼位、截弹反击与束足抢窗\n\n'+'\n\n'.join(s['event'] for s in shots)+'\n\n'
eptext=eptext[:a]+prose+eptext[b:]
eptext=eptext.replace('EP001｜v6 三头龙当前稿','EP001｜v7 第三段对抗改稿')
(EP/'episode.md').write_text(eptext)
overview=EP/'overview-storyboard.md';lines=overview.read_text().splitlines()
for i,line in enumerate(lines):
    for s in shots:
        if line.startswith('| '+s['id']+' |'):
            lines[i]=f"| {s['id']} | {60+s['start']}—{60+s['end']}s／{s['start']}—{s['end']}s | {s['event']} | {s['camera']} | {s['weight']} | {s['expression']} | {s['sound']} | {s['state']} |"
overview.write_text('\n'.join(lines)+'\n')

api=(HERE/'before-v7/api-request.md').read_text()
(SEG/'api-request.md').write_text('# Segment03当前状态｜v7重做\n\n旧视频：提交成功，但2026-11-04按用户反馈及连续抽帧判为QUALITY_REJECTED。output/video.mp4保留原文件，不作为通过样片。\n\n新版：导演提示、分镜、5张角色/结构输入和动作首帧已更新；尚未提交新版视频。正式输入顺序见../../../production/v7/segment03-rework/input-map.json。不得把旧版SUBMITTED_SUCCESS作为新版通过状态。\n\n## 原提交记录（保留原文）\n\n'+api)

qa='''# Segment03 v7复核\n\n稿件：当前episode.md第三段、storyboard.md及director-promt.txt；原片为output/video.mp4。\n\n原片判定REJECTED：30秒连续抽帧显示躯干主动位移不足；4—8秒落石横向飞离；约13—15秒甲上命中与尾烟持续。导弹挂脚另按用户反馈列为必修，未把用户反馈冒充本次抽帧已完全验证的现象。\n\n新稿逐句语义审读：\n\n| 条目 | 结果 | 证据 |\n| --- | --- | --- |\n| L01 | PASS | 每句新增攻击、躲避、接触或身体后果，无顿悟报幕。 |\n| L02 | PASS | 无对白和说教，技术禁止项留在导演规格。 |\n| L03 | PASS | 无抽象升华，结尾落在咬击擦岩与队员争下一拍。 |\n| L04 | PASS | 正文只写可见事件；左右腕/引信/镜头/人数要求在制作说明。 |\n| L05 | PASS | 危险中无插科打诨，性格以法师冷静、兽人踏实、精灵硬撑呈现。 |\n| L06 | PASS | 每枚弹的终点、原掩体、同一裂口和剩余根束均有具体指代。 |\n| S01 | PASS | 0秒承接龙主动抢攻、兽人侧撤，威胁持续。 |\n| S02 | PASS | 保住前沿、扩大同一裂甲并给刺客造近身窗口；施法者承受代价。 |\n| S03 | PASS | 龙闪避/截弹/扫火/烧藤/追咬，队员主动择隙、改根、借掩体。 |\n| S04 | PASS | 一次动作迫使对方改变下一步，完整串起陨石逼位→四弹两被拦→扫火迫退→根绊承重脚→烧断前圈→刺客绕行。 |\n| S05 | PASS | 陨石确实破甲，导弹扩口，根束打断一步，刺客取得东侧近身位。 |\n| S06 | PASS | 八节拍各改变局面，90秒接原segment04末轮协同，无新敌人或新装备。 |\n\n未处理文案项：无。新视频动作验收NOT_RUN；不将文案PASS当作成片通过。\n\n生成后必验：每段动作必须包含预备、启动、接触、后果、恢复；检查重心和脚掌承重。陨石完整下坠碎裂、4枚导弹生命周期结束、龙主动挣脱/精灵反拖必须逐事件完整观看，不能只在几张图上数技能。三头/四足/两翼、4+2弹药、右腕折刃和同一伤口连续。\n'''
qa+='\n当前episode.md SHA256：`'+hashlib.sha256((EP/'episode.md').read_bytes()).hexdigest()+'`\n'
(HERE/'qa-review.md').write_text(qa)
(EP/'qa-checklist.md').write_text('# 当前增量复核｜v7第三段\n\n第三段已按双向对抗改写，L01—L06与S01—S06逐项PASS，未处理文案项无；原视频REJECTED，新视频NOT_RUN。详见../../production/v7/segment03-rework/qa-review.md。\n\n'+(HERE/'before-v7/qa-checklist.md').read_text())
record=json.loads((HERE/'source-review.json').read_text())
(SEG/'output/video-qa.json').write_text(json.dumps({'status':'rejected','checked_at':'2026-11-04','video':record['source_video'],'video_sha256':record['source_sha256'],'notes':'用户拒绝且连续抽帧确认对抗不足、陨石轨迹错误、投射物命中后未完结。新稿通过不等于新视频通过。','evidence':str((SEG/'output/review-v7').resolve())},ensure_ascii=False,indent=2)+'\n')
(SEG/'motion-rework-v7.md').write_text('''# Segment03对抗重做｜v7\n\n可以参考《英雄联盟》电影短片的动作设计：预备、启动、接触、失衡、反制和恢复，由对手的行动触发下一动作。此处没有取得或调用官方骨骼/动作捕捉文件，也未将作品名当作可执行动作数据。\n\n本次保留原segment03的30秒、三头龙、6人身份、同一谷地、4+2弹药和既有破甲链。重写的是龙与队员持续争主动权的动作。\n\n- 原片完整抽帧与定点密集序列：output/review-v7/。\n- 原片问题与来源：../../../production/v7/segment03-rework/source-review.json。\n- 新30秒导演提示：director-promt.txt；新版分镜：storyboard.md。\n- 新动作首帧：frames/motion-v7/first-frame.png。\n- 新输入：共5图，图1动作预备、图2龙结构、图3机器人、图4精灵、图5刺客；旧10张站姿图仍保留但不批量喂作时间目标。\n- 原片已判不通过，下一次生成另存take-v7-motion.mp4，完整检查后才能替换当前video.mp4。\n\n动作参考入口：[Riot 2019赛季／Awaken](https://na.leagueoflegends.com/en/featured/events/season-start-2019)、[Riot Warriors CG资料](https://www.leagueoflegends.com/en-us/news/community/warriors-cinematic-season-2020-asset-pack/)。以上只标识参考作品；本次对原片的判断来自本地视频抽帧，未声称已逐帧分析这两部官方短片。\n''')
(HERE/'shots.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2)+'\n')
report={'version':'v7-contested','seconds':30,'shots':len(shots),'episode_seconds':t['total_seconds'],'episode_segments':t['total_segments'],'language_qa':'PASS','new_video_qa':'NOT_RUN','new_video_submitted':False,'director_characters':len(director),'input_images':5}
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
