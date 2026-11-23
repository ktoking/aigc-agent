from pathlib import Path
import json,re,hashlib,math
R=Path(__file__).resolve().parents[1]
# 与用户稿原段落一一对应，只写画面，不改旁白。
visuals={
1:'''CORRIDOR|WANG|冷红光下，王大富一手攥装金条的小布袋，一手拍101闭门，手背有限干燥血迹，无伤口特写
HOME2|CHEN|暖色餐桌中近景，陈屿以筷子夹一片毛肚在红汤上方，远处门口暗红光，衣袖与食材清楚
HOME2|无|火锅和两副碗筷的静物近景，旁有牛肉蔬菜，远处闭合门框，门内暖黄门外冷红
OFFICE|CHEN,MA|九十天前办公室，马主任把一张签收单推到陈屿面前，桌面仅单据和工牌
OFFICE|CHEN,MA|近景，陈屿伸手拿签收单，马主任掌心压住纸页，双方手腕姿态自然
OFFICE|CHEN|工牌落在桌面的近景，陈屿的手刚松开卡片，胸前挂绳已摘掉
OLDHOME|CHEN|深夜旧客厅，陈屿坐在木桌边，只有手机光映着疲惫脸部，客厅灯未开
OLDHOME|CHEN|过肩手机，显示抽象红色倒计时光块与绑定信息布局但无可读字，陈屿保持警惕
OLDHOME|CHEN|低机位，卧室门自己打开细缝，一线白光照到陈屿干燥鞋尖
HALL1|CHEN|从正常卧室门框过肩看200㎡白色空厅，陈屿抛入半包泡面，包装在离地低处定格
HALL1|CHEN|中景，陈屿持手机对照空厅，墙边只有小块警示红光，怪物尚未出现在现实
OLDHOME|CHEN|桌面近景，陈屿指尖握手机，屏幕简洁金融余额布局无可读字，另一边采购本空白页
OLDHOME|CHEN|俯拍两盒完整干燥草莓摆在卧室门槛两侧，陈屿分别推入一盒，手机购物页虚焦
OLDHOME|CHEN|次日陈屿读手机群聊，气泡及笑脸形状表达嘲笑但无可读文字，货架商品照片在旁
OLDHOME|CHEN|近景陈屿按灭群聊屏幕，嘴角克制，手旁采购本已打开
HALL1|CHEN|当晚空厅白墙浮现一小块红色警示光，陈屿抬头看，门后房间空着
OLDHOME|CHEN|从白色门洞反打旧客厅，陈屿猛回头，客厅没有第二个人，冷白门光勾出轮廓''',
2:'''OLDHOME|CHEN|客厅桌面草莓盒局部果蒂灰白小霉点，陈屿将盒封袋，其余家具干燥整洁
HALL1|CHEN|俯拍同批完好草莓，手机支架录延时，陈屿用洁净小刀切一颗，果肉紧实
HALL1|CHEN|陈屿将完好草莓盒放在待装食品位置，身旁米袋采购图片和空货架，表现储备计划
HALL1|CHEN|门边中景，陈屿点手机演示区域，身后留出可走的门口
SIM|无|隔离展示窗外一个青灰成年轮廓扑近，红眼但脸部不作裂伤特写，窗内大厅无怪物
SIM|CHEN|展示窗隔离面亮红光阻住外侧手掌，陈屿在内侧后退，双方空间边界明确
OLDHOME|CHEN|手部近景陈屿在小采购本抄下三行条目，不生成可读汉字，旁边手电商品图
OLDHOME|CHEN|陈屿用计算器合计采购清单，账本一页多行，手机余额布局在旁
OLDHOME|CHEN|账本俯拍，仅一个姓名栏填入短笔画，两栏空白，陈屿笔尖停住
OLDHOME|CHEN|近景陈屿看父母小相框，照片里一对成年夫妇，旁边旧手机屏幕熄灭
OLDHOME|CHEN|陈屿扶正父母相框，手停在相框底边，采购本摊在前方，表情克制
OLDHOME|CHEN|借款额度手机过肩，陈屿看着屏幕略微笑，屏幕只保留抽象数值块
OLDHOME|CHEN|桌上纸币和贷款手机，陈屿手收起纸币，视线留在倒计时手机，物件清楚
OLDHOME|CHEN|指尖按申请按钮区域，屏幕一个简洁转圈图标，陈屿另一手压住采购本''',
3:'''CARLOT|CHEN,DEALER|车行旧灰轿车旁，陈屿翻开保养记录给车贩看，双方各自站在车侧
CARLOT|CHEN,DEALER|近景陈屿在购车合同落笔，车贩递来签字位置，旧车钥匙放桌上
OLDHOME|CHEN|傍晚陈屿核对到账手机和采购本，车钥匙已不在手中，账本三笔收入相加
RESTAURANT|CHEN,UNCLE|家族饭桌，表叔放下筷子问陈屿，背景几位成年亲戚虚焦微笑，主角端碗
RESTAURANT|CHEN,UNCLE|表叔手掌落在饭桌旁，陈屿镇定夹菜，其他成年人在画外
MALL|CHEN,MA|商场门口马主任一臂搭着一位无名成年男主管肩，陈屿持文件袋与他相遇，三人
MALL|CHEN|陈屿带文件袋从商场门口走开，侧后方马主任为虚焦小轮廓，不新增情节
GATE|无|八辆厢式货车按次序停在小区入口外等卸货，高位全景，留旁侧应急通道
GATE|CHEN,WANG|王大富拎一只小鸟笼围观，陈屿握手推车对他简短回应，背景只有两辆近车其余远景
HALL1|CHEN|夜里陈屿把箱装水和罐头推进正常卧室门框，空厅内已有整齐密集货垛
HALL1|CHEN|六车货量已形成高密度纸箱货架，入口留出单人通路，陈屿查看容量提示抽象光条
OLDHOME|CHEN|陈屿在窗边扶腰喘气，窗外仅两辆满载厢式车仍停在路边，车数必须两辆''',
4:'''WAREHOUSE|CHEN|天亮前两辆厢式车在B7中转库开门卸货，陈屿拿租约站库外，车辆恰好两辆
MARKET|CHEN,LI|清晨粮油摊老李拍一袋米报价，陈屿蹲身查看，米袋按批次分垛
MARKET|CHEN|手部近景陈屿抓一小把米在掌心捻开闻看，旁是米袋口和批次标签形状
MARKET|CHEN,LI|老李拿烟在一侧停住与陈屿握手成交，米袋和单据在中间，烟不形成雨雾
WAREHOUSE|CHEN|俯拍采购本不断划勾，旁边代表性少量米面水盐油罐头种子和羽绒服，燃料不在食物堆里
MARKET|CHEN,LI|老李指一台大功率探照灯，陈屿手掌压着记录本，桌上配套备用电源
WAREHOUSE|CHEN|陈屿蹲在货车后厢教一位成年工人交错码袋，垫板与脱氧剂可见，两人
FUEL|无|物流园独立燃料储位，封口柴油桶与气罐有序分区，住宅绝不出现
OLDHOME|CHEN|陈屿在手机看王大富发来的聊天截图样式，无可读文字，脸色平静
GATE|CHEN|陈屿提一袋面粉经过楼门，远处两名穿正常衣服的儿童追着喊但不接近危险，主体仍陈屿
OLDHOME|CHEN|手机近景陈屿仅发送单个简短气泡，不要求生成汉字，手和键盘自然
GATE|CHEN|单元门新贴物业通知版面无可读字，陈屿看一眼准备离开，面粉袋已收好
WAREHOUSE|CHEN|夜间B7库门半拉开，陈屿拿合同刚进入，一束手电照到他脸侧，持灯者在画外''',
5:'''WAREHOUSE|XIA|手电照住叉车轮子，夏凛从侧前方抬手喊停，短棍挂腰，叉车已经停稳
WAREHOUSE|XIA|夏凛侧后转脸中近景，左耳后浅疤可见，右手贴腰，另一手持检查夹板
WAREHOUSE|CHEN,XIA|夏凛看过陈屿合同后用美工刀仅划箱口胶带，刀远离身体，陈屿站旁，两人
WAREHOUSE|CHEN,XIA|分区验货宽景，饼干种子灯具在近处，后方隔离的密封柴油储位通过门可见，夏凛问话
WAREHOUSE|CHEN,XIA|陈屿指水粮灯认真回答，夏凛停下开箱动作，双方站在货垛两侧
WAREHOUSE|XIA|特写夏凛握刀的手停在已开胶带上方，神情从冷淡变成短暂疑惑
WAREHOUSE|XIA|夏凛把美工刀收回安全鞘，抬眼盯陈屿，衣领内藏狗牌链
WAREHOUSE|XIA|手部近景夏凛用力在回执签字，无可读字，指节清楚，旁放报备资料
WAREHOUSE|XIA|夏凛站在停稳叉车与工人路线之间指示安全间隔，陈屿在远处货垛边观察
GUARD|CHEN,XIA|凌晨岗亭窗口，陈屿递副本，夏凛合上旧本子，纸页角露转账表格布局但无真实号码
GUARD|XIA|夏凛把报备单压在窗口下，旧本新一页只落一笔，脸不看镜头
GUARD|XIA|近景夏凛握笔指节发白，旧狗牌从领口微露，未交给陈屿''',
6:'''PARKOFFICE|MA|马主任将一张解聘通知拍在办公桌上，陈屿只从门口观察不入镜
PARKOFFICE|MA,XIA|办公室双人对峙，马主任指桌上通知，夏凛站直平视，没有退缩
PARKOFFICE|CHEN,XIA|走廊陈屿等夏凛出来，她抱纸箱，箱内只有水杯夹板旧本三样物件
PARKGATE|CHEN,XIA|陈屿递名片给抱纸箱的夏凛，双人平视中景，入口栏杆在后方
PARKGATE|CHEN,XIA|双人近景陈屿说明报酬，夏凛目光转冷，一手抱箱，一手按住本子
PARKGATE|XIA|夏凛戒备看陈屿画外，沉默后点向路口准备看屋，无威胁肢体接触
COURTYARD|CHEN,XIA|一楼小院夏凛查看低窗，陈屿从旧客厅推开通向白厅的卧室门
HALL1|XIA|夏凛右手按收起的短棍，另一手摸白墙，脚尖探地，货架满但保持通道
HALL1|CHEN,XIA|夏凛停在本该外墙的位置，回望普通门框，陈屿站在入口，空间尺度可读
HALL1|CHEN,XIA|陈屿递手机给夏凛查看，屏幕抽象绑定计时布局，无可读字
HALL1|CHEN,XIA|双人对话近景，夏凛警觉扫大厅，陈屿平静等她判断
OLDHOME|CHEN,XIA|桌面合同与三条分行屋规，手机到账图标，夏凛签字，所有小文字不可读
HALL1|XIA|夏凛抬头看墙上小块红色倒计时光，指尖收紧，门前仍未放下纸箱''',
7:'''OLDHOME|CHEN,XIA|晚间陈屿在旧客厅门边回应夏凛，她正拿垫子走向沙发旁，尚无新卧室出现
OLDHOME|CHEN,XIA|夏凛坐沙发旁垫子握短棍，陈屿递热面，双方保持自然距离
OLDHOME|XIA|夏凛把面吃完放下空碗，筷子平放，陈屿画外货架整理声由旁白承担
OLDHOME|CHEN,XIA|半夜夏凛靠墙睡着，短棍落垫子边，陈屿俯身给她盖毯子
OLDHOME|CHEN|陈屿看手机睡眠奖励抽象提示，夏凛睡眠只在远背景虚焦，无新人物
OLDHOME|CHEN,XIA|清晨夏凛惊醒握短棍坐起，陈屿站在桌旁回答，两人没有攻击行为
OLDHOME|CHEN,XIA|陈屿把热豆浆推到夏凛面前，她双手接杯低头，毯子仍搭肩
HALL1|CHEN|陈屿按手机升级确认，建材包独立摆一侧，食品储备不消失
HOME2|CHEN,XIA|升级刚完成的空间大全景，厨房台面、浴室闭门、四扇卧室门和新木地板，夏凛短棍举起又停住
BATH2|无|浴室龙头往浴缸放热水，少量蒸气局限缸口，环境其余干燥，无裸体无人
HOME2|XIA|夏凛抱臂站在浴室闭门外，嘴角一瞬轻笑，声音来自门内的陈屿画外
HOME2|CHEN|陈屿穿完整干净灰T恤长裤拿毛巾，看手机下一等级抽象条件，头发微整齐不湿透
HOME2|CHEN,XIA|陈屿用毛巾擦头发，夏凛在厨房边问话，两人自然日常站位
HOME2|CHEN|陈屿俯看空医疗箱，内衬格子可见，旁边水粮灯整齐摆好''',
8:'''HOME2|CHEN|医疗箱空格特写，陈屿手停在箱沿，远处仓储区水粮齐备
PHARMACY|CHEN,CLERK|药店店员将长清单推还陈屿并指门外义诊台，两人，柜台无杂乱药品
CLINIC|XU|许知意穿白大褂擦白桌布台面，医用夹板在旁，胸牌只是空白标牌不生成字
CLINIC|CHEN,XU|许知意用纸巾隔着捏陈屿清单皱眉看，陈屿坐桌对面，桌上止血带纱布碘伏少量
CLINIC|CHEN,XU|许知意抬眼指清单数量，陈屿话到嘴边停住，双人近景
CLINIC|CHEN,XU|两人安静问答，陈屿在清单人数栏旁握笔，许知意看他，不添加旁人
CLINIC|XU|许知意把药品清单折到背面，指向基础耗材列，桌上没有整箱处方药
CLINIC|XU|许知意将几盒纱布按大小摆齐，陈屿仅边缘一只拿清单的手
CLINIC|CHEN,XU|陈屿起身道谢，许知意扶夹板认真回应，两人视线平齐
CLINIC|XU|许知意在名片背面写联系方式，手部近景，不生成真实号码
HOME2|XIA|夏凛把纱布和碘伏按数量放入医疗箱，盒盖打开，整洁日常光
HOME2|CHEN|采购本近景，陈屿把普通名片夹在两栏空白姓名旁，页面只画栏线与笔迹形状''',
9:'''COURTYARD|无|住宅楼下成年家犬拉紧固定链条朝西边低吼，姿态不受伤，天空暗红前兆，地面干燥
OLDHOME|XIA|夏凛留一指窗帘缝观察，电视无字新闻播红云与动物剪影，室内简洁
OLDHOME|CHEN,XIA|夏凛从窗口转身回应陈屿，他手拿倒计时手机，两人看向彼此
CORRIDOR|无|两盏固定外置探照灯亮起照明台阶和楼梯转角，电源线规范走线，无人物无激光
SUPERMARKET|CHEN|陈屿停在超市入口，近景空水盐货架，远处两名成年顾客各抓一侧箱水，无暴力
HOSPITAL|CHEN,XU|急诊接收台陈屿放一箱纱布和消毒耗材，票据夹在箱顶，许知意接收
HOSPITAL|CHEN,XU|陈屿展示倒计时手机并递普通纸卡，许知意看手机，医院正常走廊
HOSPITAL|CHEN,XU|双人走廊中景陈屿郑重邀请，许知意手里夹着值班表，画外病区有灯
HOSPITAL|CHEN,XU|许知意神情警惕反问，陈屿把地址卡留在她手边，不强行塞入衣袋
HOSPITAL|XU|许知意把纸卡收白大褂口袋，露出一角，目光停在陈屿离开的方向
OLDHOME|CHEN|手机显示王大富烧烤照片：新炉旁半开小柜内一排金条，画面无聊天文字
OLDHOME|XIA|夏凛持短棍站外门旁等陈屿回来，窗外红色天光未退
OLDHOME|CHEN|陈屿关外门，把院灯控制器放到手边，内侧线缆连备用电源，无其他人''',
10:'''OLDHOME|无|从旧客厅窗看整排住宅熄灯与红月在楼缝出现，前景桌椅影子，所有地面干燥
OLDHOME|XIA|近景夏凛拉外门门链确认，转头望向通往厨房的白色卧室门框
HOME2|CHEN,XIA|陈屿在厨房将卡式炉火调旺，红汤火锅与毛肚牛肉蔬菜齐备，夏凛站门框问话
CORRIDOR|WANG|王大富满手有限干燥血迹攥金条袋拍101门，无开放伤口不溅血，冷红月光
HOME2|CHEN|中近景陈屿夹毛肚在红汤上方，与EP001相同服装餐具但新机位和新生成图，神情冷静
CORRIDOR|WANG|王大富背抵门惊惧，远处转角一个青灰成人形轮廓出现，不表现咬伤或撕裂
OLDHOME|CHEN|陈屿从餐桌走来放下筷子到小碟，手伸向控制器，门仍锁着
OLDHOME|CHEN|陈屿按控制器开关，备用电源在桌边，另一手离开门锁，无猫眼光束
CORRIDOR|无|外置灯白光照住转角，一个青灰成人形轮廓抬手遮眼后退，无面部裂伤特写
CORRIDOR|WANG|王大富趁白光逃回对门，门扇正要闭合，金条小袋仍在手中，无死亡场面
OLDHOME|CHEN|陈屿靠观察口听到女人呼喊，面部从冷静转紧张，院灯控制器仍在手边
CORRIDOR|XU|许知意白大褂破裂且有干燥深红血迹，扶墙攥地址纸卡，身后三道人影只在远端转角，无血腥伤口
OLDHOME|CHEN|陈屿隔观察口朝门外说话，面向灯照亮的区域，手掌贴外门内侧
OLDHOME|CHEN|手机手部近景抽象幸存者入住确认红色区域，门锁同框，画面不生成汉字字幕
OLDHOME|CHEN,XIA|夏凛在陈屿身后举短棍待接应，陈屿一手按门锁，门仍闭合，门外许知意不实体进入'''
}
oldcards=R/'assets/characters'
actors={}
for p in oldcards.glob('*/00-character-card.md'):
 s=p.read_text();actors[p.parent.name]=s.split('本版外貌设计（原稿未给处由本次补定，待审美确认）：')[-1].split('。\n\n同人脸')[0]
scenes={p.parent.name:p.read_text().split('\n\n')[1] for p in (R/'assets/scenes').glob('*/scene-card.md')}
assets=json.loads((R/'assets/manifest.json').read_text());refs={a['asset_id']:str(R/a['path']) for a in assets if a['type']=='character_identity'}
allshots=[]
for n,raw in visuals.items():
 eid=f'EP{n:03d}';d=R/'episodes'/eid
 cues=json.loads((d/'voice-plan.json').read_text());lines=raw.splitlines();assert len(cues)==len(lines),(eid,len(cues),len(lines))
 shots=[];t=0
 for j,(c,line) in enumerate(zip(cues,lines),1):
  sid,charids,visual=line.split('|');ids=[] if charids=='无' else charids.split(',')
  count=len(re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]','',c['source_text']));dur=count/7.5
  # 只估预算，不擅自声称已按实测4—6秒完成排时。
  p=f'''真人写实电影静帧，横向16:9，单张全画幅，固定构图，不是拼贴，不要文字、字幕或水印。\n本镜唯一事件：{visual}。\n角色身份：{';'.join(actors.get(a,a) for a in ids) if ids else '本镜无主角实体，远景对象仅按上述事件出现'}。\n场景布局：{scenes[sid]}\n输入角色参考仅锁对应人物脸、年龄、发型和服装，不复制参考的背景姿势和镜头；未列的演员不能出现。场景与人物的具体状态以上述事件为准，场景卡中通用描述不覆盖当前剧情。例如Lv1空厅在EP001—2为空，EP003起才逐渐满仓；EP007升级后才有厨房浴室。\n自然皮肤与衣服质感，主体轮廓清楚、干净大形、适度细节，不锐化、不鳞片网格、不满屏微纹理。布景简洁有秩序、地墙衣物干燥哑光；血月原稿明确的干燥血迹与浴室局部热水保留在需要的物件上，不加入其他湿反光、雨雾、垃圾、重污渍。\n本镜不在图中排旁白文字；手机屏幕信息只用抽象光块/图形表达，关键信息由配音传达。独立生成新图片，不以旧图裁切调色冒充。\n'''
  shot_id=f'{eid}-S{j:02d}';pp=d/'image-prompts'/f'{shot_id}.txt';pp.parent.mkdir(exist_ok=True);pp.write_text(p)
  sh={'shot_id':shot_id,'episode':eid,'cue_ids':[c['cue_id']],'source_text':c['source_text'],'scene_id':sid,'character_ids':ids,'unique_event':visual,'prompt_path':str(pp.relative_to(R)),'reference_paths':[refs[a] for a in ids if a in refs],'timing_status':'TEXT_ESTIMATE_IMAGE_FIRST_USER_REQUEST','estimated_start_seconds':round(t,3),'estimated_duration_seconds':round(dur,3),'start_frame':None,'end_frame':None,'image_path':None,'image_sha256':None,'generation_status':'PLANNED','final_timing_locked':False,'timing_note':'用户要求先出图，当前一段一候选图；实际配音后沿语义边界拆/并，必要时另生成新图，不靠复用图凑时长。'}
  shots.append(sh);allshots.append(sh);t+=dur+(0.1 if j<len(cues) else 0)
 (d/'shots.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
 table=['# 确认稿画面拆解（图片优先）','','以下画面逐段对应原句；不改旁白。时长为文字预算，未实测，后续以真实配音调整4—6秒主节奏。','','|镜头|原段落|人物/场景|唯一画面|','|---|---|---|---|']
 for s in shots:table.append(f"|{s['shot_id']}|{s['cue_ids'][0]}|{','.join(s['character_ids'])} / {s['scene_id']}|{s['unique_event']}|")
 (d/'storyboard.md').write_text('\n'.join(table)+'\n')
(R/'production/user-script-v2/image-queue.json').write_text(json.dumps(allshots,ensure_ascii=False,indent=2))
print('new confirmed-text shot candidates:',len(allshots))
