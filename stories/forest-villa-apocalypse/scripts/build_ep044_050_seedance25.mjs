import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { episodes } from './ep044-050-seedance25-plan.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const activeFormatFile = path.join(root, 'docs/ep044-050-production-format.json');
if (fs.existsSync(activeFormatFile) && JSON.parse(fs.readFileSync(activeFormatFile, 'utf8')).segment_duration === 15) {
  throw new Error('EP044-EP050已切换四段15秒。请运行build_ep044_050_15s.mjs；禁止旧构建器覆盖当前稿件。');
}
const revision = '2026-10-21-seedance25-story-rebuild';
const snapshot = path.join(root, 'docs/revisions/2026-10-21-pre-seedance25');
const segmentDirs = ['segment_01_00-30s', 'segment_02_30-60s'];
const nums = ['一', '二', '三', '四', '五', '六', '七', '八'];
const countSpeech = text => (text.match(/[\p{Script=Han}\p{N}]/gu) || []).length;
const sha = text => crypto.createHash('sha256').update(text).digest('hex');
const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const json = object => `${JSON.stringify(object, null, 2)}\n`;
const tab = value => String(value).replaceAll('|', '／').replaceAll('\n', ' ');
const bullets = list => list.map(item => `- ${item}`).join('\n');
const cast = {
  许砚: { asset: 'asset-20260320075237-29hdx', outfit: '黑色短发；炭灰防水工装夹克、黑肩拼片、深灰上衣、黑灰直筒工装裤、深棕高帮登山靴、黑色电子表', acting: '沉着实干，判断在观察之后；日常关心用实际行动表达', voice: '成年男性中低声，清楚平稳，临战果断，生活中不过度压嗓' },
  白棠: { asset: 'asset-20260320075131-k78qt', outfit: '利落低马尾；鼠尾草绿短款工装外套、浅灰圆领上衣、深灰直筒工装裤、黑色防滑工作靴', acting: '能独立判断生产与库存，有心疼劳动、期待收成和熟人间的幽默', voice: '成年女性自然中声，利落清楚，紧张时仍有完整语句' },
  沈知夏: { asset: 'asset-20260310030618-88hlb', outfit: '深栗色侧分微卷长发过肩；暗酒红医护工装外套、黑色刷手服内搭、炭灰工装裤、黑色防滑短靴', acting: '成熟克制，专业意见独立；会坚持休息与复核，不无条件附和', voice: '成年女性偏低声，语气稳，有关心但不甜腻' },
  叶凝霜: { asset: 'asset-20260720212023-wwndz', outfit: '银白色长发；白色修身长款防寒风衣、冰灰高领内搭、白灰战术长裤、白色雪地靴', acting: '清冷有主见，怒意用目光与停顿，疲劳按剧情发生；生活戏不改成撒娇少女', voice: '成年女性清冷中低声，咬字清楚，少修饰，不拖腔' },
  冬狼: { asset: 'asset-20260720205729-l4dfh', outfit: '利落黑短发；黑色厚防风长外套、深灰高领内搭、黑色工装长裤、黑色防滑雪地靴', acting: '习惯控制别人，听见停火才敢靠近；失去优势后情绪变化可见，不狂笑', voice: '成年男性偏低声，命令口吻，失势时才抬高音量' },
};
const canonical = 'assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png';
const building = '同一栋现代三层主楼、连续阳台、灰色高围墙与黑色双扇外门，屋顶逐项服从canonical锚图。菜园、温室、禽舍、鱼池、独立能源棚均在围墙内；唯一炮台固定二楼阳台。塌方主路未恢复，来客只能走原步行路线。';
const constraints = '不生成字幕、水印、logo、可读坐标、陌生清晰人脸、人物分身、换脸换衣、第二栋主楼或第二座炮台。人手接触实物、搬运和受力连续；结果不早于动作。不得给未发声角色补口型。';
const labels = {
  villa: '正确别墅冬季总景', gateStrain: '受撞锁座', turret: '唯一阳台炮台', armorDefense: '外骨骼抵门受力', gate: '同一关闭黑门', wolfFrozen: '墙外冰封倒地轮廓', armorCooling: '外骨骼过热停用',
  gateDamage: '旧锁板变形', gateRepaired: '新锁板装回原门', metalPrinter: '打印仓单块锁板成品', greenhouseLeak: '温室旧膜漏雪', seedlingRescue: '室内两盘受冻苗', filmCards: '保温膜三选一与有限卷材',
  coopCold: '原禽舍饮水器冻住', pondCover: '原鱼池局部保温罩', shelterBuild: '有限膜材分配与旧架', coopWarm: '禽舍修后通风与饮水', firstEgg: '窝箱单枚鸡蛋', pondWarm: '保温罩内循环水和鱼影', pumpHouseSmoke: '山谷旧泵房炊烟',
  energyShed: '独立能源棚外观', heatingBranch: '外部供暖支路柜', valveCheck: '外部执行件一次检查', livingWarm: '现代客厅地暖空间', spareTray: '旧件与最后一个备用件', printer: '原工业打印仓', mechanicalParts: '有限机械小件与护板', gateRepair: '外门新增外侧防撞板', seedTray: '有限种子与空育苗盘',
  workshop: '原现代工作间', growLightCards: '罐头与育苗灯三选一', seedlingRack: '一层育苗灯架', radio: '原门柱对讲设备', tradeHatch: '原双门人工交易槽', saltTrade: '盐包与有限菜蛋', brokenPump: '旧泵变形支架', feedstockLabel: '待验原料包装照片', saltShelf: '收到的盐包储位', repairedPump: '同一旧泵修后试水', growthTray: '单盘叶菜与邻盘幼苗', eggAndGreens: '自用与交换的有限收成', feedstockCheck: '原料包装与合格试件', dining: '现代别墅暖色餐区', noodles: '青菜鸡蛋面',
  'outfit_冬狼': '冬狼现代黑色冬装', 'outfit_白棠': '白棠鼠尾草绿工装', 'outfit_许砚': '许砚炭灰工装', 'outfit_沈知夏': '知夏暗酒红医护工装', 'outfit_叶凝霜': '凝霜白色冬装', clean_detail: '本段物件收束局部',
};
const segmentLimits = [
  '本段只发生最后短射、门锁受力和护臂过热。门关闭，叶凝霜还未出手；最后枪声后不能继续射击。',
  '炮台已经空仓，外骨骼仍过热。冻结从墙外冬狼靴周连续升起，仅一次；冬狼倒下后不开口、不复活。',
  '只修原门锁板、搬两盘苗和用旧夹子临时挡风。本段不抽卡，没有新膜卷，外骨骼停用、炮台无弹。',
  'D2仅领取一卷保温膜。选择前桌上无实体；夜里只领取，清晨才人工安装，苗不瞬间复活或成熟。',
  '使用前集剩膜，只改原禽舍和鱼池，通风、过滤与增氧保持。饮水器先进屋解冻；不抽卡，不催鱼催蛋。',
  '鸡蛋正常产出，凝霜只做轻劳动。无人机是例行巡查，炊烟只证明可能有人，不断言人数或敌意。',
  '主机发电正常，只检查隔离后的外部支路。知夏一次短时校准只定位；备用件尚未装上，反应堆不拆壳。',
  '本段人工用掉最后一个现有备件，知夏不再次发功。热传到室内需要时间省略，空盒与旧件分别留下。',
  '只打印机械支架与外门护板，电子件仍做不了、原料下降。本段未领取新卡，门沿用EP045新锁板。',
  'D3当天首次领取，只选灯板组件，另两张失效。人手搭一层灯架，种子不因灯亮立刻长成菜。',
  '自用粮与药保留，只交换小筐菜与两枚库存蛋。外门主门关闭，箱由人手推动；泵只留下待检。',
  '泵仍在待检状态，不承诺已修好。原料只有照片，不计入库存，来客不进入院内。',
  '只给原泵换外部支架再试水。白棠D4只催一盘接近采收叶菜，邻盘小苗不变；未收到或验收交易原料。',
  '同一修好泵换一小袋匹配且经试件确认的料，先验后收。晚饭使用已有主粮与当天收获，窗外仍是冬季。',
];

function write(relative, content) {
  const target = path.join(root, relative);
  const previous = path.join(snapshot, relative);
  if (fs.existsSync(target) && !fs.existsSync(previous)) {
    fs.mkdirSync(path.dirname(previous), { recursive: true });
    fs.copyFileSync(target, previous);
  }
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${content.trimEnd()}\n`);
}

// Read all reference plans before writing any of them, so reruns do not lose candidates.
const prior = new Map();
const pool = new Map();
for (const e of episodes) {
  for (const directory of segmentDirs) {
    const relative = `episodes/${e.dir}/${directory}/reference-assets.json`;
    const snapshotPath = path.join(snapshot, relative);
    const originalPath = fs.existsSync(snapshotPath) ? snapshotPath : path.join(root, relative);
    const plan = readJson(originalPath);
    prior.set(`${e.dir}/${directory}`, plan);
    for (const ref of plan.references) if (ref.key && !pool.has(ref.key)) pool.set(ref.key, ref);
  }
}

const specs = {
  villa: { file: canonical, scope: '正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物' },
  gateStrain: { scope: '原黑门中央锁座受撞变形，门板主体仍完整；只锁旧状态，不把结果提前修好' },
  turret: { scope: '唯一自动炮台外形；安装位置在二楼阳台，弹药状态严格按当镜，不能复制第二座' },
  armorDefense: { scope: '同一防护外骨骼护臂抵住黑门的接触与受力；测试架不出现在正片，角色身份只用数字人' },
  gate: { scope: '原黑门门柱、内外侧与关闭状态，不改变canonical建筑；冻结发生墙外' },
  wolfFrozen: { scope: '墙外单个无脸冰封轮廓与倒地冰层质感；不锁新面孔，不出现碎尸' },
  armorCooling: { scope: '外骨骼同款关节、过热警示与停用状态；不锁新人物或新装甲' },
  gateDamage: { scope: '门内旧锁板歪斜、中央锁舌错位，门本体没有被打穿；无人物' },
  gateRepaired: { scope: '同一黑门装回一块新锁板的局部，旧划痕保留，不新增外侧护板；无人物' },
  metalPrinter: { scope: '原打印仓输出托盘里的一块新锁板与旁边旧件，有限材料，人工安装；无人物' },
  greenhouseLeak: { scope: '院内同一现代温室旧膜一处接缝掀起，下面两盘苗落雪，黑色棚架完整；无人物' },
  seedlingRescue: { scope: '现代工作台上两盘受冻但尚存活的小苗，坏叶分开放，不是成熟菜；无人物' },
  filmCards: { scope: '原手机零点三选一：保温膜、便携灯、未知；选中后一卷有限膜材。只锁选项与材料，不把膜提前安装；无人物' },
  coopCold: { scope: '原院内现代金属禽舍结构、旧饮水器出水口冻住的局部，少量鸡，不出现陌生房屋或人' },
  pondCover: { scope: '原循环鱼池边缘薄冰，局部透明保温罩留通气与检修口，过滤桶仍在旧位置；无人物' },
  shelterBuild: { scope: '同一院内原禽舍单侧挡风膜与相邻鱼池罩，有限膜材在旧架上，通风口留出；无人物' },
  coopWarm: { scope: '同一现代禽舍完成单侧挡风、原饮水器解冻后有水，保留通风口；无人物' },
  firstEgg: { scope: '同一禽舍窝箱内仅一枚蛋与垫草的近景，不锁背景建筑或人物' },
  pondWarm: { scope: '同一透明罩下鱼影、气泡与正常循环水，鱼大小不被异能放大；无人物' },
  pumpHouseSmoke: { scope: '南侧山谷旧泵房远景，一缕炊烟，树林遮挡；没有人物脸、尸潮、可读坐标或新别墅' },
  energyShed: { scope: '原围墙内独立能源棚、密封发电模块外壳与外部供暖柜，生活区距离服从canonical；无人物' },
  heatingBranch: { alias: 'heatBranch', scope: '密封核能主机之外的独立供暖柜，源侧与回屋侧管路、外接阀件可区分；无人物，无主机内部' },
  valveCheck: { alias: 'sensorCheck', scope: '同一外部传感器与两只小执行件，其中一只卡住；手持终端仅外观，不画内部电路；无人物' },
  livingWarm: { scope: '原现代客厅、稳定照明、地暖分水器、厚毯与暖桌；只锁空间，不靠图片断言温度' },
  spareTray: { scope: '旧外接执行件、仅一只备用件与空格备件盒，分开摆放；换件后盒子为空，无人物' },
  printer: { scope: '既有单台炭灰封闭工业金属打印仓、原料盒、输出托盘与工作间；不锁时间或人物' },
  mechanicalParts: { scope: '少量机械支架、单块外门防撞护板与有限原料并列，电子封装件单独放；无人物' },
  gateRepair: { scope: '沿用EP045已修好的黑门内锁板，新增外侧同色防撞护板；灰墙、电网、屋顶不变，无人物' },
  seedTray: { scope: '原工作间旧架、空育苗盘与有限种子袋，接近窗口光照不均；无人物，不画成熟蔬菜' },
  workshop: { file: 'assets/production/ep042-044-reference-refresh/references/industrial-metal-printer-winter-workshop-16x9.png', scope: '原现代灰白工作间、打印仓和金属台面，窗外冬雪；只锁空间与机器，不锁台上新道具' },
  growLightCards: { scope: '白天原手机三选一：一箱罐头、有限育苗灯组件、未知；只能选灯，组件投影落在空台；无人物' },
  seedlingRack: { scope: '原工作间一层旧金属架安装有限育苗灯、控制组件与一盘刚播种的苗盘；无人物，不生成多层工厂' },
  radio: { scope: '原门柱对讲设备及呼叫灯，关闭黑门与灰门柱；只锁对讲外观，不能添大喇叭或人物脸' },
  tradeHatch: { scope: '原黑门上的双门交易槽、托盘与内外门关系，主门关闭，箱子需人手推动；无人物' },
  saltTrade: { scope: '封口盐包、小筐青菜与两枚垫好的鸡蛋分开放，交易量有限；无人物，无药品交易' },
  brokenPump: { scope: '一台小型旧水泵、明显歪斜的外部安装支架，保留完整原外壳；无人物，不拆复杂内部' },
  feedstockLabel: { scope: '手机上的旧仓库原料包装照片，与本机原包装标签并列；只锁包装外观，不把照片变为已收到实物；无人物' },
  saltShelf: { scope: '现代干燥储架里刚收好的一包盐，自用食品储位保留，不出现无限物资；无人物' },
  repairedPump: { scope: '同一旧泵装上新外部支架，防溅台上试转、管口回到同一水桶；电气部分不浸水，无人物' },
  growthTray: { scope: '温室中一盘接近采收的叶菜与邻盘刚播小苗，前者展开到成熟、后者不变；仅提供作物状态，不锁人物' },
  eggAndGreens: { scope: '当晚自用碗与少量交换菜分别放，库存鸡蛋和有限青菜，不虚构满仓收获；无人物' },
  feedstockCheck: { scope: '匹配本机包装的一小袋原料、同批小试件、旧机型标签并列，有限数量；无人物，无制造参数' },
  dining: { scope: 'canonical现代别墅暖色餐区、普通碗筷、窗外冬雪；四把椅子可见但没有人物，不画四人合照' },
  noodles: { scope: '普通陶瓷碗中的青菜鸡蛋面，少量真实热气，现代餐桌，无火锅、宴席、人物和文字' },
};

const details = {
  'EP045_snow-greenhouse/0': { alias: 'greenhouseLeak', file: pool.get('greenhouseLeak')?.file, scope: specs.greenhouseLeak.scope },
  'EP045_snow-greenhouse/1': { file: 'assets/production/ep045-rebuild-reference-refresh/references/courtyard-greenhouse-film-repaired-16x9.png', scope: '同一温室新膜补住局部接缝，旧黑架完整，一盘苗归位，剩余膜有限；无人物' },
  'EP047_reactor-cold/1': { scope: '外部供暖柜修后关闭，原管路、便携监测终端与厚毯保持位置；无人物，不含主机内部' },
  'EP048_printer-parts/0': { scope: '原打印仓有限剩余料、已分格机械备件与单独旧电子件，不把电子件打印出来；无人物' },
  'EP048_printer-parts/1': { alias: 'seedTray', scope: '同一育苗架下单盘刚播种的湿土、封好的剩余种子与原门柱手持对讲；无人物' },
  'EP049_outside-trade/0': { scope: '原门外对讲与小物资箱的位置关系，关闭主门、双门交易托盘，不画人或自动推出的箱子' },
  'EP049_outside-trade/1': { scope: '原工作间独立待修架上仅同一故障泵、旧件与有限工具，旁边盐包已收好；无人物' },
};

const cueSets = [
  ['<远处稀疏枪声，雪地风声>', '<门板钝响，伺服承力声>', '<控制室轻底噪，内线按键>', '<炮台转向马达，尚未射击>', '<门内金属受力，衣料摩擦>', '<最后一轮短射，随即空仓一响>', '<单次低声温度提示，撞击仍在>', '<靴底踩雪，枪被收起>'],
  ['<门柱对讲轻电噪，踩雪声停住>', '<衣袖碰门柱，近处呼吸>', '<雪面冻结与靴底受阻>', '<细碎结冰由近及远>', '<冰层变厚，冰体仅一次倒地闷响>', '<撞击已停，伺服卸力>', '<衣料摩擦和变弱的呼吸>', '<停用提示一响，脚步向主楼移动>'],
  ['<锁舌松动金属响>', '<撑杆落地，工具箱提手轻碰>', '<打印仓停机，托盘滑出>', '<工具拧紧，锁舌咬合>', '<旧膜被风扯动，少量雪落>', '<盘底接触临时台>', '<普通夹子扣合，拍膜声变小>', '<坏叶落台，覆盖布轻响>'],
  ['<手机一次短提示，工作灯底噪>', '<覆盖布与苗盘轻碰>', '<一次选择提示，卷材落台轻响>', '<束带解开，薄膜轻摩擦>', '<清晨风声与卷材展开>', '<扣件合拢，话后松手>', '<棚外风声仍在，棚内不拍膜>', '<苗盘落架，原灌溉点轻滴水>'],
  ['<饮水器轻碰，一粒冰落>', '<水壶交接，脚步向主楼>', '<薄冰轻碰，循环水声>', '<轻铲浮雪，棚架接触>', '<薄膜与旧扣件摩擦>', '<收卷轻响，棚外风声>', '<原过滤泵持续低噪>', '<少量气泡，鱼游过水面>'],
  ['<出水口轻滴，鸡喝水>', '<垫草轻响，鸡低鸣>', '<量勺挂回栏边>', '<饲料入勺，料盒扣好>', '<托盘落台，不加庆祝音效>', '<终端按键，起飞声短暂>', '<远处风声与无人机低嗡>', '<操纵杆回中，记录笔轻响>'],
  ['<客厅电器低噪，拖鞋摩擦>', '<衣料与手电轻碰>', '<抽屉合上，外套拉链>', '<外部供暖柜打开，主机低噪稳定>', '<指尖接触，极轻弱光声>', '<一次测试，卡住部件轻响>', '<备件盒打开，一件被取出>', '<手收回，柜边工具轻碰>'],
  ['<旧件落盘，普通工具接触>', '<终端按键一次>', '<支路恢复运行，水流低声>', '<对讲反馈，厚毯折起>', '<柜门闭合，轻呼吸>', '<便携终端被接过>', '<空盒落台，旧件另放>', '<手电关闭，室内轻底噪>'],
  ['<旧件落台，料盒轻碰>', '<部件分开放置，衣袖摩擦>', '<一轮打印停机，托盘出件>', '<机械小件依次入盒>', '<护板落在门外固定位置>', '<普通紧固工具轻响>', '<空盘落架，种子袋摩擦>', '<手机被拿起，工作间底噪>'],
  ['<手机一次短提示>', '<种子袋放下，轻呼吸>', '<选择提示一次，组件落台>', '<灯板贴合旧架，扣件固定>', '<苗盘落架，种子袋封好>', '<电源开关，灯板稳定低噪>', '<门柱呼叫提示，对讲轻电噪>', '<工具放下，对讲按键>'],
  ['<食品箱轻响，蛋落软垫>', '<盐包接触外侧台面>', '<对讲按键，内侧箱落盘>', '<门外靴底退半步>', '<双门交易槽按顺序开合，箱由手推>', '<盐包封口轻响>', '<小泵有重量地落入外侧箱>', '<对讲轻电噪，门保持关闭>'],
  ['<旧泵落台轻晃>', '<记录卡与原料盒接触>', '<工具放稳，对讲按键>', '<手机收到照片一声轻提示>', '<按键说完后静下>', '<小泵放到待修架>', '<普通工具取出>', '<脚步沿原雪路逐渐远去>'],
  ['<新支架贴合，普通工具固定>', '<泵启动，水流由断续转稳定>', '<稳定运行，不额外报警>', '<小苗盘移开，温室底噪>', '<极轻能力声，叶片自然展开>', '<一次采收，菜落小篮>', '<叶菜分别入碗入篮>', '<工具收好，泵由人手抱起>'],
  ['<短时试转，稳定出水后断电>', '<小试件与包装轻碰，不加打印大场面>', '<交易槽开合，泵由人提走>', '<对讲按键，工具车移动>', '<面碗落桌，厨房轻响>', '<终端扣下，椅子移近>', '<筷子轻放碗沿，留咀嚼停顿>', '<筷子与碗轻碰，屋外风雪渐低>'],
];

const checks = [];
const allReadthrough = [];
const outlineRows = [];
const missingAssets = new Map();
const generatedRecordPath = path.join(root, 'assets/production/ep044-050-seedance25/generation-record.json');
const generatedAssets = new Map(fs.existsSync(generatedRecordPath)
  ? readJson(generatedRecordPath).generated.map(item => [item.key, path.relative(root, item.file)]) : []);

function referencePlan(e, s, index) {
  const old = prior.get(`${e.dir}/${segmentDirs[index]}`);
  const references = s.cast.map((name, i) => ({ number: i + 1, kind: 'digital_human', name, asset: cast[name].asset, uri: `asset://${cast[name].asset}`, label: name, scope: `只绑定${name}本人脸与身份；服装和表演以正文为准`, status: 'user_registered_identity' }));
  for (const key of s.refs) {
    const original = old.references.find(ref => ref.key === key) || pool.get(key);
    let spec = key === 'clean_detail' ? details[`${e.dir}/${index}`] : specs[key];
    spec ||= {};
    const candidate = spec.alias ? pool.get(spec.alias) : original;
    let file = spec.file || candidate?.file || null;
    if (key === 'outfit_叶凝霜') file = 'assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png';
    const number = references.length + 1;
    if (file && !fs.existsSync(path.join(root, file))) file = null;
    const scope = spec.scope || candidate?.scope || `${key}的无人物外观与物件状态，服从本段剧情`;
    const slug = key === 'clean_detail' ? `${e.dir.slice(0, 5).toLowerCase()}-s${index + 1}-detail` : key.replaceAll('_', '-').replace(/[^a-zA-Z0-9-]/g, 'outfit');
    const planned_file = `assets/production/ep044-050-seedance25/references/${slug}-16x9.png`;
    const generatedFile = generatedAssets.get(slug);
    if (generatedFile && fs.existsSync(path.join(root, generatedFile))) file = generatedFile;
    else if (!file && fs.existsSync(path.join(root, planned_file))) file = planned_file;
    references.push({ number, key, kind: key.startsWith('outfit_') ? 'outfit' : 'scene_or_prop', label: labels[key] || key, file, planned_file: file ? null : planned_file, scope, status: file ? 'existing_candidate_pending_new_shot_review' : 'needs_generation_for_rewritten_shots' });
  }
  if (references.length !== 9) throw new Error(`${e.dir} S${index + 1}: expected 9 references`);
  return { revision, numbering: 'exact_api_image_order_including_digital_humans', first_last_frames: false,
    digital_humans: s.cast.map(name => ({ name, asset: cast[name].asset })),
    api_submission: { status: references.some(r => !r.uri && !r.file) ? 'needs_reference_images' : 'needs_visual_review', model: 'doubao-seedance-2-5-260628', duration: 30, ratio: '16:9', resolution: '480p', generate_audio: true, max_total_images: 9, planned_total_images: 9, auto_images: false, note: '九项为本批制作规划，非模型官方上限；不扫描旧frames，不传首尾帧。本轮未提交视频。' },
    references, exclusions: ['不上传未出场角色或历史人物三视图', '不上传旧首尾帧与旧output视频', '不把待补图当已存在，不把候选图当已通过新镜头视觉验收'] };
}

for (const [ei, e] of episodes.entries()) {
  const episodePath = `episodes/${e.dir}`;
  const episodeRows = [];
  const summaries = [];
  const manifest = [];
  const readthrough = [`# ${e.dir.slice(0, 5)} 台词通读：${e.title}`, '', `版本：${revision}。先只读角色对白，检查是否像一轮交流。`, '', `承接：${e.premise}`, ''];
  for (const [si, s] of e.segments.entries()) {
    if (s.shots.length !== 8 || s.cast.length > 3) throw new Error(`Invalid shot/cast count: ${e.dir}`);
    const d = `${episodePath}/${segmentDirs[si]}`;
    const plan = referencePlan(e, s, si);
    const scenes = plan.references.filter(r => r.kind !== 'digital_human');
    const offscreen = [...new Set(s.shots.filter(x => !s.cast.includes(x.speaker)).map(x => x.speaker))];
    const speakers = [...new Set(s.shots.map(x => x.speaker))];
    const spoken = countSpeech(s.shots.map(x => x.dialogue).join(''));
    if (spoken > 105 || s.shots.some(x => !x.dialogue.trim())) throw new Error(`Dialogue overload: ${e.dir} S${si + 1}: ${spoken}`);
    for (const sh of s.shots) if (sh.mode === 'onscreen' && !s.cast.includes(sh.speaker)) throw new Error(`Unbound face: ${sh.speaker}`);
    const format = [
      `16:9横屏，30秒，8个实际镜头，有声音，真人电影实拍质感。${e.dir.slice(0, 5)} Segment ${si + 1}：${s.title}。`,
      `生成目标：${s.opening} 本段结束：${s.ending}`,
      '', '数字人身份锁（按首次清晰露脸顺序传入，编号与实际图片输入一致）：',
      ...plan.references.filter(r => r.kind === 'digital_human').map(r => `参考图${r.number}：${r.label}，数字人身份锁=${r.uri}；${cast[r.name].outfit}。${cast[r.name].acting}。只锁本人脸与身份，不沿用资产原衣。`),
      `清晰出镜仅${s.cast.join('、')}，单机位最多两张清晰脸。${offscreen.length ? `仅声音、不露脸：${offscreen.join('、')}。` : ''}`,
      '', '场景与道具参考（下面的数字继续沿用实际请求顺序）：',
      ...scenes.map(r => `参考图${r.number}：${r.label}；${r.scope}。`),
      '', `空间与承接：${building} ${s.time}。`,
      '摄影：自然肤色，冷灰雪光与室内暖功能灯形成真实对比，现代灰石与金属保持干净大形。人物反应以目光、停顿、呼吸和手部动作呈现。各镜按动作与表演分配时长，不机械平分；用动作匹配或明确硬切，不用融化转场。',
      '声音：中文自然交流。对白只说本镜列出的内容，单镜一个说话人；画外音对应原现场或同一对讲通道。音效跟动作发生，音乐极轻，不盖词。', '',
      `声音角色：${speakers.map(name => `${name}为${cast[name]?.voice || '隔着门柱对讲的成年男性声音，礼貌拘谨，与主角音色分开'}`).join('；')}。`, '',
    ];
    const table = [];
    readthrough.push(`## Segment ${si + 1}：${s.title}`, '', `情境：${s.time}`, '');
    for (const [i, sh] of s.shots.entries()) {
      const bound = sh.mode === 'voiceover'
        ? `仅${sh.speaker}按上述来源作画外音，画面内人物闭口；器械、动物和冰封轮廓不配口型。`
        : `仅${sh.speaker}开口，给其正面或四分之三侧面清楚口型；其他人物闭口，用眼神和动作回应。`;
      const cue = cueSets[ei * 2 + si][i];
      format.push(`镜头${nums[i]}｜${sh.title}`, `景别：${sh.size}。`, `构图：${sh.composition}`, `运镜手法：${sh.camera}`, `画面内容：${sh.action}`, `表演：${sh.delivery}`, `说话者绑定：${bound}`, `${sh.speaker}台词${sh.mode === 'voiceover' ? '（画外音）' : ''}：{${sh.dialogue}}`, `声音：${cue}`, '');
      const who = `${sh.speaker}${sh.mode === 'voiceover' ? '（画外音）' : ''}`;
      table.push(`| ${i + 1} ${sh.title} | ${tab(sh.size)}；${tab(sh.composition)} | ${tab(sh.camera)} | ${tab(sh.action)} | ${who}：${sh.dialogue} |`);
      episodeRows.push(`| ${si + 1} | ${i + 1} | ${who} | ${tab(sh.dialogue)} |`);
      readthrough.push(`${i + 1}. ${who}：${sh.dialogue}`);
    }
    format.push(`收束状态：${s.ending}`, '声音与表演连续：台词不在动作说明里复述。实际语音快慢、呼吸与切镜按自然交流安排，画面里没有字幕。', `保持一致：${segmentLimits[ei * 2 + si]}`, `排除内容：${constraints}`, '');
    const prompt = format.join('\n');
    const hash = sha(prompt);
    write(`${d}/director-promt.txt`, prompt);
    write(`${d}/prompt.md`, prompt);
    write(`${d}/storyboard.md`, `# ${e.dir.slice(0, 5)} Segment ${si + 1}：${s.title}\n\n版本：${revision}。30秒，16:9，真人；8镜，每镜一句具名发声，时间随动作分配。\n\n首状态：${s.opening}\n\n尾状态：${s.ending}\n\n| 镜头 | 景别与构图 | 运镜 | 动作与结果 | 发声 |\n| --- | --- | --- | --- | --- |\n${table.join('\n')}\n\n完整表演与声画绑定见director-promt.txt。台词与episode、prompt均来自同一母版。\n`);
    write(`${d}/storyboard-source.json`, json({ revision, episode: e.dir, segment: segmentDirs[si], duration: 30, time: s.time, cast: s.cast, offscreen, opening: s.opening, ending: s.ending, shots: s.shots }));
    write(`${d}/first-frame.md`, `# 首状态说明：${s.title}\n\n无首尾帧提交。本文件只记录剪辑和连续性，不触发首帧图片生成或上传。\n\n${s.opening}\n\n首个实际镜头：${s.shots[0].size}；${s.shots[0].composition}\n\n人物：${s.cast.join('、')}；建筑与物件服从本段reference-assets.json。\n`);
    write(`${d}/last-frame.md`, `# 尾状态说明：${s.title}\n\n无首尾帧提交。本文件只记录剪辑和连续性，不触发尾帧图片生成或上传。\n\n${s.ending}\n\n末个实际镜头：${s.shots[7].size}；${s.shots[7].composition}\n\n后续继续承接这个状态，不拿旧视频尾帧覆盖新稿。\n`);
    write(`${d}/reference-assets.json`, json(plan));
    const missing = scenes.filter(r => !r.file);
    for (const r of missing) {
      const asset = missingAssets.get(r.planned_file) || { planned_file: r.planned_file, label: r.label, scope: r.scope, used_by: [] };
      asset.used_by.push({ episode: e.dir, segment: segmentDirs[si], reference_number: r.number });
      missingAssets.set(r.planned_file, asset);
    }
    const rows = plan.references.map(r => `| ${r.number} | ${r.label} | ${r.uri || r.file || `待补：${r.planned_file}`} | ${tab(r.scope)} | ${r.status} |`);
    const handoff = `# ${e.dir.slice(0, 5)} Segment ${si + 1} 视频交接\n\n版本：${revision}\n\n状态：提示词已重写；本轮未提交视频。旧output为历史记录。\n\n## 参数\n- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。\n- duration=30，ratio=16:9，resolution=480p，generate_audio=true。\n- 参考生视频；无首尾帧；auto_images=false。\n- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。\n- SHA256：${hash}\n- 台词有效字数：${spoken}；按每秒4字仅粗估${(spoken / 4).toFixed(1)}秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。\n\n## 精确输入顺序\n数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。\n\n| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |\n| --- | --- | --- | --- | --- |\n${rows.join('\n')}\n\n## 下一步\n${missing.length ? `仍缺${missing.length}张新稿对应图，详见asset-image-prompts.md；缺图补齐前不提交。` : '本地候选图齐全；提交前须逐图确认新镜头的建筑、服装、状态和机位，再核对实际请求映射。'}\n\n不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。\n\n提交记录：无。任务ID：无。\n`;
    write(`${d}/api-request.md`, handoff);
    write(`${d}/seedance25-handoff.json`, json({ revision, submitted: false, model: plan.api_submission.model, duration: 30, ratio: '16:9', resolution: '480p', generate_audio: true, prompt_file: 'director-promt.txt', prompt_sha256: hash, first_frame: null, last_frame: null, auto_images: false, references_file: 'reference-assets.json', readiness: plan.api_submission.status, missing_reference_numbers: missing.map(r => r.number) }));
    const imagePrompts = scenes.map(r => `## 参考图${r.number}：${r.label}\n\n状态：${r.status}\n\n${r.file ? `候选：${r.file}` : `计划输出：${r.planned_file}`}\n\n用途：${r.scope}\n\n生图提示词：16:9横屏，真人实拍电影道具或场景参考，无人物、无人手、无人脸、无文字水印。${r.scope}。现代灰石、灰白金属与真实材质，冬季自然光或对应工作灯，画面主体清楚；干净大形、适度细节，不锐化、不堆网格微纹理。只给场景和物件，动作人物与口型由视频数字人负责。\n\n建筑编辑依据：${canonical}；若已有同一物件候选图，编辑时以它锁定形状。此图只供参考，不作为首尾帧；新旧状态按本段对应镜头使用。`);
    write(`${d}/asset-image-prompts.md`, `# ${s.title} 参考图复核与补图\n\n版本：${revision}。本文件提供生图需求，本轮没有调用生图接口。数字人不在这里生成。共有${scenes.length}项非人物规划，${missing.length}项当前缺文件。\n\n${imagePrompts.join('\n\n')}\n`);
    write(`${d}/dialogue.txt`, `${s.shots.map((sh, i) => `${i + 1}. ${sh.speaker}${sh.mode === 'voiceover' ? '（画外音）' : ''}：${sh.dialogue}`).join('\n')}\n`);
    summaries.push(`| ${si + 1} | ${s.title} | ${tab(s.opening)} | ${tab(s.ending)} | ${spoken} |`);
    manifest.push(`## Segment ${si + 1}：${s.title}\n\n规划9项（数字人${s.cast.length}、场景道具${scenes.length}）；现有候选${scenes.length - missing.length}张，缺${missing.length}张。\n\n| 输入顺序 | 标签 | 来源 | 职责 | 状态 |\n| --- | --- | --- | --- | --- |\n${rows.join('\n')}\n`);
    readthrough.push('');
    checks.push({ episode: e.dir, segment: segmentDirs[si], duration: 30, shots: 8, visible_cast: s.cast, offscreen, dialogue_chars: spoken, estimated_speech_seconds_at_4cps: Number((spoken / 4).toFixed(1)), prompt_characters: prompt.length, prompt_sha256: hash, prompt_copy_equal: true, planned_references: 9, existing_candidates: scenes.length - missing.length, new_reference_slots: missing.length, missing_reference_numbers: missing.map(r => r.number), submission_status: plan.api_submission.status, video_submitted: false, video_reviewed: false });
  }
  write(`${episodePath}/episode.md`, `# ${e.dir.slice(0, 5)}：${e.title}\n\n版本：${revision}\n\n## 基本信息\n60秒，2段×30秒，每段8镜，16:9真人短剧。时间：${e.time}。目标模型Seedance 2.5。\n\n## 上集承接\n${e.premise}\n\n## 本集人物要什么\n${e.want}\n\n## 冲突、变化与回报\n${e.turn}\n\n${e.payoff}\n\n## 分段与台词预算\n| 段 | 内容 | 首状态 | 尾状态 | 有效台词字数 |\n| --- | --- | --- | --- | --- |\n${summaries.join('\n')}\n\n## 完整发声台词\n| 段 | 镜头 | 发声者 | 台词 |\n| --- | --- | --- | --- |\n${episodeRows.join('\n')}\n\n## 资源与能力\n${bullets(e.resource)}\n\n## 下集动力\n${e.hook}\n\n## 制作状态\n全部文字来自同一母版并同步。参考图重做语义分配，缺图与候选分别记录，见image-manifest.md。本轮未生成图片、未提交或覆盖视频。\n`);
  write(`${episodePath}/dialogue-readthrough.md`, readthrough.join('\n'));
  allReadthrough.push(readthrough.join('\n'));
  write(`${episodePath}/overview-storyboard.md`, `# ${e.dir.slice(0, 5)} 故事板总览\n\n${e.premise}\n\n人物目标：${e.want}\n\n转折：${e.turn}\n\n回报：${e.payoff}\n\n| 段 | 内容 | 开始 | 结束 | 发声字数 |\n| --- | --- | --- | --- | --- |\n${summaries.join('\n')}\n\n后续：${e.hook}\n`);
  write(`${episodePath}/continuity.md`, `# ${e.dir.slice(0, 5)} 连续性\n\n版本：${revision}\n\n时间：${e.time}\n\n承接：${e.premise}\n\n空间：${building}\n\n${e.segments.map((s, i) => `## Segment ${i + 1}\n\n清晰人物：${s.cast.join('、')}。\n\n首状态：${s.opening}\n\n尾状态：${s.ending}\n\n转场时间：${s.time}`).join('\n\n')}\n\n## 不可回退的资源状态\n${bullets(e.resource)}\n\n## 下一集\n${e.hook}\n`);
  write(`${episodePath}/image-manifest.md`, `# ${e.dir.slice(0, 5)} 新稿参考图清单\n\n版本：${revision}。参考图编号为真实API图片输入顺序，数字人计入规划9项。文件存在仅为候选，本轮尚未逐图重新视觉验收；缺图提示词已写到各段asset-image-prompts.md。\n\n旧frames与output是历史记录，不自动上传；无首尾帧。不把另一机位的场景图替代人物脸，不把旧图的状态倒灌到新剧情。\n\n${manifest.join('\n')}\n`);
  const ec = checks.filter(c => c.episode === e.dir);
  write(`${episodePath}/qa-checklist.md`, `# ${e.dir.slice(0, 5)} 制作检查\n\n版本：${revision}\n\n## 已核对的文本\n- [x] 两段各八镜，每镜有具体行动、发现、反应或结果，并有一句具名发声。\n- [x] 单段最多三名清晰角色；每镜单一发声者，纯物件机位明确画外音。\n- [x] director-promt.txt和prompt.md逐字一致，故事板与episode对白由同一母版生成。\n- [x] 参考图按真实请求顺序共9项，身份与场景职责分开。\n- [x] 抽卡日期、选择代价、有限材料、唯一炮台及既有物件结果衔接。\n\n## 台词与生成状态\n${ec.map((c, i) => `- Segment ${i + 1}：${c.dialogue_chars}个有效字，按4字/秒粗估${c.estimated_speech_seconds_at_4cps}秒；缺参考图${c.new_reference_slots}张。`).join('\n')}\n\n## 尚待实物与成片核对\n- [ ] 缺图补齐，候选图逐张确认建筑、物件、服装与机位。\n- [ ] 提交前回读真实请求的数字人、图像标签、顺序、模型参数与提示词哈希。\n- [ ] 成片检查切镜、脸、衣服、手、动作起止、口型归属及对白听感。\n- [ ] 字幕逐字取本地剧本，并实际对齐声音。\n\n本次文本静态检查不代表视频质量PASS；没有提交新视频。\n`);
  write(`${episodePath}/publish-package.md`, `# ${e.dir.slice(0, 5)} 发布草案\n\n版本：${revision}\n\n标题候选：\n${bullets([e.title, e.payoff, e.hook])}\n\n封面画面：${e.dir.startsWith('EP044') ? '关闭黑门在后景，许砚抵门护臂与门外结冰形成同一防线的反差，不做血腥近景。' : `${e.payoff}选择一项能看懂的实物结果做画面主体；人物仅按该镜登记身份。`}\n\n评论方向：围绕本集取舍或劳动回报提问，不虚构播放量、官方推荐或爆款保证。\n\n标签方向：末日建家、抽卡生存、真人AI短剧。\n`);
  outlineRows.push(`| ${e.dir.slice(0, 5)} ${e.title} | ${e.time} | ${tab(e.want)} | ${tab(e.turn)} | ${tab(e.payoff)} | ${tab(e.hook)} |`);
}

write('docs/ep044-050-seedance25-outline.md', `# EP044–EP050 新版剧情\n\n版本：${revision}。连续性从未修改的EP043接起。\n\n| 集 | 时间 | 人物目标 | 转折 | 本集兑现 | 后续动力 |\n| --- | --- | --- | --- | --- | --- |\n${outlineRows.join('\n')}\n\n创作依据与平台核查见seedance25-story-writing-method.md。所有对白与分镜母版位于scripts/ep044-050-seedance25-plan.mjs。\n`);
write('docs/ep044-050-seedance25-dialogue-readthrough.md', allReadthrough.join('\n\n'));
write('docs/ep044-050-seedance25-validation.json', json({ revision, scope: 'EP044-EP050', checks: 'text_and_paths_static_only', episodes: 7, segments: 14, total_shots: 112, unique_missing_reference_files: missingAssets.size, reference_images_generated_this_run: 0, video_submitted: false, segments_detail: checks }));
write('docs/ep044-050-seedance25-asset-plan.json', json({ revision, images_generated_this_run: 0, unique_missing_files: missingAssets.size, assets: [...missingAssets.values()] }));

const legacyValidation = path.join(root, 'docs/ep041-050-rewrite-validation.json');
if (fs.existsSync(legacyValidation)) {
  const original = readJson(legacyValidation);
  original.revision = revision;
  original.note = 'EP041-EP043保留原记录；EP044-EP050更新为Seedance2.5新稿静态数据。';
  original.segments_detail = original.segments_detail.map(old => {
    const next = checks.find(c => c.episode === old.episode && c.segment === old.segment);
    return next ? { ...old, ...next, estimated_speech_seconds: next.estimated_speech_seconds_at_4cps, dialogue_revision: revision } : old;
  });
  write('docs/ep041-050-rewrite-validation.json', json(original));
}

const legacyRead = path.join(root, 'docs/ep041-050-dialogue-readthrough.md');
if (fs.existsSync(legacyRead)) {
  const old = fs.readFileSync(legacyRead, 'utf8');
  const boundary = old.search(/^# EP044\b/m);
  if (boundary >= 0) write('docs/ep041-050-dialogue-readthrough.md', `${old.slice(0, boundary)}${allReadthrough.join('\n\n')}\n`);
}

const legacyOutline = path.join(root, 'docs/ep041-050-rebuild-outline.md');
if (fs.existsSync(legacyOutline)) {
  let text = fs.readFileSync(legacyOutline, 'utf8');
  for (const e of episodes) {
    const number = e.dir.slice(0, 5);
    const row = `| ${number} ${e.title} | ${e.time} | ${tab(`${e.premise} ${e.turn} ${e.payoff}`)} | ${tab(e.hook)} |`;
    text = text.replace(new RegExp(`^\\| ${number} .+$`, 'm'), row);
  }
  text = text.replace(/^版本：.+$/m, `版本：${revision}。EP041–EP043保留原承接，EP044–EP050采用新的剧本与导演稿；详细创作依据见seedance25-story-writing-method.md。`);
  write('docs/ep041-050-rebuild-outline.md', text);
}

for (const c of checks) console.log(`${c.episode} ${c.segment}: 8 shots, ${c.dialogue_chars} spoken chars, ${c.prompt_characters} prompt chars, ${c.new_reference_slots} missing reference files`);
console.log('Built 7 episodes / 14 segments / 112 shots. No external calls.');
