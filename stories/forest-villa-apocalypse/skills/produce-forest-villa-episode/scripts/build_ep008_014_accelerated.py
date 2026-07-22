#!/usr/bin/env python3
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[5]
STORY = ROOT / "stories/forest-villa-apocalypse"
EPISODES = STORY / "episodes"

XU = "asset://asset-20260320075237-29hdx"
BAI = "asset://asset-20260320075131-k78qt"
SHEN = "asset://asset-20260310030618-88hlb"
RAIDER_LEADER = "asset://asset-20260310022222-kjz8z"

XU_OUTFIT = "许砚穿FVA_XU_YAN_OUTFIT_001：炭灰防水工装夹克、深灰内搭、黑灰工装裤、深棕高帮登山靴。"
BAI_OUTFIT = "白棠穿FVA_BAI_TANG_OUTFIT_001：鼠尾草绿工装外套、浅灰内搭、深灰工装裤、黑色工作靴，发型沿用数字人资产。"
SHEN_OUTFIT = "沈知夏穿FVA_SHEN_ZHIXIA_OUTFIT_001：深栗色微卷长发、发长过肩、侧分；暗酒红医护工装外套、黑色刷手服内搭、炭灰工装裤、黑色防滑短靴。她是成熟冷静的急诊医生，表情克制，与白棠明确区分。"
RAIDER_LEADER_OUTFIT = "罗彪穿FVA_RAIDER_LEADER_OUTFIT_001：旧黑色皮夹克、深灰圆领衫、黑色工装裤、棕黑作战靴，右臂系暗红布条；发型和脸完全沿用数字人资产。"

ASSETS = {
    "villa": "assets/scenes/SCENE_FOREST_VILLA_001/references/villa-courtyard-after-siege-corrected-16x9.png",
    "villa_perimeter_electric": "assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-structure-three-view-perimeter-electric-v2-16x9.png",
    "storage": "assets/scenes/SCENE_FOREST_VILLA_001/references/basement-storage-function-test-high-tech-v3-16x9.png",
    "low_storage": "assets/scenes/SCENE_FOREST_VILLA_001/references/basement-canned-food-low-stock-16x9.png",
    "rod": "assets/props/references/daily-draw-fishing-rod-kit-16x9.png",
    "fish_plan": "assets/props/references/fish-aquaponics-blueprint-kit-16x9.png",
    "river": "assets/scenes/SCENE_FOREST_VILLA_001/references/mountain-river-fishing-site-16x9.png",
    "pickup": "assets/vehicles/references/diesel-pickup-supply-truck-16x9.png",
    "drone": "assets/vehicles/references/heavy-lift-agricultural-cargo-drone-16x9.png",
    "road": "assets/scenes/SCENE_FOREST_VILLA_001/references/mountain-road-zombie-aerial-survey-16x9.png",
    "road_obstacle": "assets/scenes/SCENE_FOREST_VILLA_001/references/mountain-road-abandoned-car-narrow-gap-16x9.png",
    "villa_gate": "assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-exterior-day-16x9.png",
    "night_villa": "assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-exterior-night-16x9.png",
    "zombie": "assets/zombies/references/ordinary-infected-canonical-trio-16x9.png",
    "fish_tanks": "assets/water/references/basement-aquaponics-two-tank-system-16x9.png",
    "fish_tanks_18": "assets/water/references/basement-two-tanks-exact-18-fish-16x9.png",
    "empty_fish_tanks": "assets/water/references/basement-empty-two-tank-fish-system-16x9.png",
    "river_catch": "assets/scenes/SCENE_FOREST_VILLA_001/references/river-two-live-fish-buckets-catch-16x9.png",
    "filter": "assets/water/references/water-filtration-storage-system-16x9.png",
    "battery": "assets/scenes/SCENE_FOREST_VILLA_001/references/backup-battery-system-16x9.png",
    "water_kit": "assets/water/references/water-quality-startup-kit-16x9.png",
    "poultry": "assets/scenes/SCENE_FOREST_VILLA_001/references/villa-poultry-pen-first-egg-16x9.png",
    "seed": "assets/props/references/daily-draw-seeds-filter-card-16x9.png",
    "fish_veg_draw": "assets/props/references/daily-draw-fish-feed-vegetable-test-kit-16x9.png",
    "hotpot_draw": "assets/props/references/daily-draw-copper-hotpot-kit-16x9.png",
    "hotpot_harvest": "assets/interiors/references/villa-kitchen-copper-hotpot-harvest-16x9.png",
    "electric_fence": "assets/props/references/villa-low-voltage-perimeter-fence-kit-16x9.png",
    "crop": "assets/scenes/SCENE_FOREST_VILLA_001/references/villa-soy-pea-growing-zones-16x9.png",
    "radio": "assets/scenes/SCENE_FOREST_VILLA_001/references/villa-tool-room-drone-radio-map-16x9.png",
    "clinic": "assets/scenes/SCENE_FOREST_VILLA_001/references/mountain-clinic-exterior-16x9.png",
    "clinic_alley": "assets/scenes/SCENE_FOREST_VILLA_001/references/mountain-clinic-rear-alley-rescue-route-16x9.png",
    "crossbow": "assets/props/references/compact-crossbow-twelve-bolts-16x9.png",
    "quarantine": "assets/scenes/SCENE_FOREST_VILLA_001/references/garage-quarantine-medical-bay-16x9.png",
    "medical_bay": "assets/scenes/SCENE_FOREST_VILLA_001/references/garage-quarantine-medical-bay-16x9.png",
    "contract": "assets/props/references/cooperation-contract-phone-ui-16x9.png",
    "low_oxygen": "assets/water/references/aquaponics-low-oxygen-emergency-16x9.png",
    "raider_gear": "assets/raiders/references/raider-faction-vehicles-equipment-16x9.png",
    "raider_assault_gear": "assets/raiders/references/raider-night-assault-ladder-kit-16x9.png",
    "raider_camp": "assets/raiders/references/raider-quarry-camp-16x9.png",
    "raider_trace": "assets/scenes/SCENE_FOREST_VILLA_001/references/raider-scout-evidence-outside-villa-16x9.png",
    "raider_hotpot_watch": "assets/raiders/references/raider-dry-rations-villa-watch-16x9.png",
    "raider_failed_tunnel": "assets/raiders/references/raider-failed-tunnel-perimeter-alert-16x9.png",
    "mushroom": "assets/scenes/SCENE_FOREST_VILLA_001/references/underground-mushroom-harvest-room-16x9.png",
}

LABELS = {
    "villa": "现代三层林中别墅和高墙院落，只锁定单栋建筑与院内农业区",
    "villa_perimeter_electric": "现代三层林中别墅加固完成版三视图，只锁定同一栋别墅、高围墙、电动铁门、院内菜地鸡鸭棚、围墙顶部内侧整圈三道低压警戒线和墙内控制箱；不单独立栅栏",
    "storage": "现代地下储藏区，只锁定罐头货架、清点桌和通道",
    "low_storage": "现代地下低库存储藏区，只锁定稀疏罐头、空货架、干粮盒和清点桌",
    "rod": "鱼竿抽卡工具包，只锁定鱼竿、线轮、活鱼桶和简洁手机卡面",
    "fish_plan": "鱼池施工图，只锁定双水箱、过滤桶、管路和空池结构",
    "river": "无人机发现的山间河湾，只锁定浅滩、旧桥、停车区和撤离方向",
    "pickup": "柴油皮卡，只锁定深色现代皮卡外形和货斗结构",
    "drone": "重载农业无人机，只锁定机体、吊篮和监控视角",
    "road": "山路侦察图，只锁定弯道、障碍物与返回别墅的路线",
    "road_obstacle": "山路废车障碍，只锁定左侧斜停废车、右侧窄缝和连续弯道",
    "villa_gate": "现代三层林中别墅正门，只锁定单栋建筑、高墙和黑色铁门",
    "night_villa": "现代三层林中别墅夜景，只锁定夜色、高墙、黑色铁门、监控与建筑轮廓",
    "zombie": "三只普通感染体锚点，只锁定群体轮廓和移动姿态",
    "fish_tanks": "地下双水箱鱼池，只锁定两箱、过滤桶、水泵和管路",
    "fish_tanks_18": "地下双水箱十八尾鱼状态，只锁定两池各九尾、过滤桶、水泵、气泵和空运输桶",
    "empty_fish_tanks": "地下双水箱施工态，只锁定两个空池、过滤桶、水泵、气泵和未连接管件",
    "river_catch": "河岸捕鱼收获状态，只锁定两只增氧活鱼桶、有限小鲫鱼、鱼竿、抄网和同一辆皮卡",
    "filter": "井水过滤储水系统，只锁定过滤桶、净水箱和管线",
    "battery": "备用储能系统，只锁定电池柜、回路和现代控制屏",
    "water_kit": "水质启动包，只锁定试纸、温度计、取样杯和有限耗材",
    "poultry": "现代鸡鸭棚，只锁定五只禽类、饮水槽和饲料槽",
    "seed": "黄豆豌豆抽卡资产，只锁定有限种子包和简洁卡面",
    "fish_veg_draw": "鱼菜循环日常抽卡测试包，只锁定鱼饲料启动包、水质试纸、叶菜种子、量勺、记录卡和简洁手机卡面",
    "hotpot_draw": "铜锅火锅日常抽卡包，只锁定黄铜铜锅、火锅底料、芝麻酱、便携燃气炉、记事本和简洁手机卡面",
    "hotpot_harvest": "现代别墅室内铜锅火锅收获台，只锁定黄铜铜锅、小鲫鱼鱼片、叶菜、三枚鸡蛋、平菇、少量主食和暖黄厨房灯光",
    "electric_fence": "围墙顶部内侧低压警戒电网套件，只锁定三道绝缘钢丝、黑色绝缘支架、低压脉冲主机、备用电池与施工工具；不单独立栅栏",
    "crop": "院内豆类种植区，只锁定育苗盘、菜床、滴灌和网架",
    "radio": "无线电工具间，只锁定电台、地图桌和设备布局",
    "clinic": "山下卫生院，只锁定现代小诊所、侧门和后巷路线",
    "clinic_alley": "卫生院后巷撤离路线，只锁定侧门、单车道、装卸台和山路转角；图中没有人物",
    "crossbow": "紧凑弩和有限箭矢，只锁定武器比例与箭矢数量",
    "quarantine": "车库隔离医疗区，只锁定隔离窗、传递箱和医疗台",
    "medical_bay": "现代车库医疗区，只锁定医疗台、药品柜、照明和器械布局；图中没有人物",
    "contract": "协作契约手机界面，只锁定权限、任务和退出条款布局",
    "low_oxygen": "鱼池缺氧状态，只锁定浮头鱼群、停泵水面和备用气泵",
    "raider_gear": "强盗势力车辆装备，只锁定旧越野车、摩托、油桶、无线电和暗红布条标识，不锁人物",
    "raider_assault_gear": "强盗夜袭装备，只锁定折叠梯、绳索、断线钳、对讲机、工具包和暗红布条，不锁人物",
    "raider_camp": "废弃采石场强盗营地，只锁定帐篷、车辆、瞭望塔、物资笼和暗红布条标识，不锁人物",
    "raider_trace": "别墅外围踩点痕迹，只锁定林边车辙、藏匿摄像头和暗红布条标记，不锁人物",
    "raider_hotpot_watch": "采石场边缘强盗观察点，只锁定望远镜、压缩饼干、冷罐头水、干硬馒头、旧对讲机、暗红布条和远处暖光别墅；不锁人物",
    "raider_failed_tunnel": "围墙外失败地道现场，只锁定浅挖土沟、埋地警戒线、铲子、折叠梯、绝缘手套、暗红布条和围墙顶部内侧电网；不锁人物",
    "mushroom": "现代地下室菌菇收获室，只锁定平菇种植架、收获篮、除湿灯和清洁操作台；图中没有人物",
}


def shot(title, framing, composition, camera, content, speaker, dialogue):
    return {
        "title": title,
        "framing": framing,
        "composition": composition,
        "camera": camera,
        "content": content,
        "speaker": speaker,
        "dialogue": dialogue,
    }


EPISODES_DATA = [
    {
        "dir": "EP008_cans-low-river-fishing",
        "title": "EP008：罐头只够九天，抽到鱼竿直奔河边",
        "summary": "两人清点后发现罐头只够九天。零点抽到鱼竿和活鱼桶，他们当天清出双水箱池位，次日趁白天普通丧尸活动少，开柴油皮卡前往无人机发现的河湾取活鱼。",
        "segments": [
            ("罐头只够九天", ["low_storage", "rod"], [
                shot("清点最后几箱罐头", "储藏室双人中景", "稀疏罐头架在后，两人把剩余食物放上清点桌", "从空货架横移到账本", "白棠直接计算两人每天的最低消耗，不反复询问常识。", "白棠", "按最低消耗算，罐头只够我们吃九天。"),
                shot("停止继续消耗肉罐头", "账本与罐头近景", "肉罐头、鸡蛋和粮食余量分栏摆放", "固定近景", "许砚把肉罐头移入应急栏，日常改吃干粮和现有蔬菜。", "许砚", "肉罐头封存，九天内必须找到新的蛋白质。"),
                shot("午夜抽到鱼竿套装", "手机与工具桌近景", "简洁卡面、鱼竿、线轮和两个折叠活鱼桶同框", "从零点时钟移到工具", "系统只给捕鱼工具，不直接变出鱼。", "白棠", "抽到鱼竿、线轮和两个活鱼桶，没有鱼苗。"),
                shot("地图锁定山间河湾", "地图桌双人中景", "无人机旧航拍里的河湾、旧桥和撤离路线清楚", "沿地图路线移到两人", "两人决定先搭空池，再在白天出发。", "许砚", "先把池位搭好，明早开皮卡去这条河。"),
            ]),
            ("当天搭好空鱼池", ["fish_plan", "empty_fish_tanks", "battery"], [
                shot("清出两只旧水箱", "地下设备区大全景", "两只旧水箱、过滤桶和空施工位同框", "稳定横移", "人物手动清洗水箱，不自动施工。", "白棠", "两只水箱没有裂，清洗后都能继续用。"),
                shot("接好过滤回水管", "管路操作中景", "许砚连接过滤桶和回水管，白棠固定卡箍", "跟随双手完成连接", "本段只完成空池框架，不放鱼、不注满水。", "许砚", "过滤桶先接上，鱼回来再启动整套循环。"),
                shot("给水泵留独立电路", "储能柜中近景", "鱼泵回路从备用储能柜单独引出", "从电池柜移到水泵插座", "人物实际接线并测试指示灯。", "白棠", "鱼泵走独立回路，晚上断别的电也不影响它。"),
                shot("两个空池等待活鱼", "双水箱远景", "空池、过滤桶、氧气泵和带盖活鱼桶排列清楚", "缓慢后拉", "施工结果可见，第二天路线板放在门边。", "许砚", "池子准备好了，明天只带活鱼回来。"),
            ]),
            ("白天开皮卡去河边", ["pickup", "river", "drone"], [
                shot("无人机先飞过山路", "无人机航拍大全景", "河湾和沿途山路处于白天，路面暂时没有丧尸", "低速前推", "无人机先侦察，不让皮卡盲目出门。", "白棠画外音", "沿路暂时没人影，河湾附近也没有聚集。"),
                shot("皮卡驶出高墙", "别墅外门全景", "深色柴油皮卡驶出，铁门在车后立即关闭", "低机位跟车后拉", "白棠带活鱼桶，许砚驾驶，院内设施不出墙。", "许砚", "四十分钟内回来，太阳偏西就直接撤。"),
                shot("抵达旧桥下浅滩", "河湾大全景", "皮卡停在撤离方向，浅滩和旧桥在前", "从皮卡横移到水面", "车辆不熄火太久，车头朝返程方向。", "白棠", "车头已经调好，鱼桶和增氧泵都在岸边。"),
                shot("下竿寻找小鱼群", "河岸双人中景", "鱼漂进入缓流，透明水面能看到小鱼群", "跟随抛竿落水", "两人只在可见浅滩活动，不走入深水。", "许砚", "先钓小鲫鱼，能活着带回去比大小重要。"),
            ]),
            ("活鱼到手，林中出现动静", ["river", "river_catch", "pickup"], [
                shot("第一尾小鲫鱼入桶", "鱼竿与活鱼桶近景", "一尾小鲫鱼由抄网进入带增氧的活鱼桶", "跟随抄网移动", "鱼由人物取钩放桶，不自行飞入。", "白棠", "第一尾状态正常，水温也和河里一样。"),
                shot("两只桶逐渐有鱼", "河岸双人中景", "两只活鱼桶内只有有限小鱼，皮卡在身后", "从桶横移到继续收竿的两人", "用短蒙太奇表现数次收获，不瞬间装满。", "许砚", "够起一池种鱼就停，不能为了多几尾拖时间。"),
                shot("无人机发现林边移动", "无人机监控近景", "林缘出现三个模糊移动目标，距离河湾仍远", "从河面抬升到林缘", "只让观众看懂有东西接近，不做血腥特写。", "白棠", "林边有三个目标，正在往河道方向移动。"),
                shot("收竿准备撤离", "河岸双人全景", "许砚收竿，白棠提桶上货斗，皮卡车门打开", "手持跟随快速装车", "两人停止捕鱼，结尾远处树丛继续晃动。", "许砚", "不等它们靠近，装鱼，现在就走。"),
            ]),
        ],
    },
    {
        "dir": "EP009_river-zombie-pickup-escape",
        "title": "EP009：河边丧尸越聚越多，皮卡冲回高墙",
        "summary": "装鱼时，普通丧尸从林边、旧桥和下游同时靠近。无人机在前方找路，许砚驾驶皮卡穿过山路障碍，白棠保护活鱼桶并远程开门，两人惊险冲回别墅。",
        "segments": [
            ("三个目标变成一群", ["river", "zombie", "drone"], [
                shot("林边丧尸进入河滩", "河湾大全景", "三只普通型从林缘走上碎石滩，皮卡在右侧", "从林边快速横移到皮卡", "两人继续装最后一个活鱼桶。", "白棠", "不止三个，旧桥后面还有一批在往这边走。"),
                shot("无人机升高确认包围", "无人机俯拍大全景", "旧桥、下游和林边三股目标逐渐合拢", "垂直升高后俯拍", "丧尸数量增加但不瞬移。", "许砚画外音", "河滩会被堵死，先走上游土路。"),
                shot("固定活鱼桶", "皮卡货斗近景", "白棠用绑带固定两个活鱼桶和增氧泵", "跟随绑带收紧", "鱼桶不翻倒，气管保持连接。", "白棠", "两个桶都固定了，增氧泵还在工作。"),
                shot("皮卡冲出河湾", "低机位车辆全景", "皮卡从碎石滩加速驶向上游土路，丧尸在后方追来", "低机位跟车转向", "车辆不撞人群，依靠提前撤离拉开距离。", "许砚", "坐稳，我们走没被堵住的上游路。"),
            ]),
            ("山路连续躲避", ["pickup", "road", "drone"], [
                shot("无人机标出前方障碍", "无人机航拍大全景", "弯道停着废车，另一侧留有窄缝", "从障碍后退到皮卡", "无人机低音量回传路线。", "白棠", "前面废车挡了半条路，右侧还能过。"),
                shot("皮卡贴右侧通过", "车外侧跟拍中景", "皮卡减速贴右侧越过废车，车身不穿模", "平行跟车", "后方普通丧尸刚进入弯道。", "许砚", "我减速过缝，你盯住鱼桶和后面。"),
                shot("落枝挡住下一弯", "驾驶室主观中景", "前方落枝占据一侧车道，山坡边缘可通行", "轻微手持前推", "许砚转向避开，不突然飞车。", "白棠", "左边有空位，转过去就是回别墅的主路。"),
                shot("无人机把追兵带偏", "山路远景", "无人机飞向支路发出短促机械声，部分丧尸转向", "从无人机移到远离的皮卡", "无人机不无限吸引，只争取短暂距离。", "许砚", "无人机带偏一部分，我们直接回家。"),
            ]),
            ("远程开门冲进院内", ["pickup", "villa", "drone"], [
                shot("高墙出现在弯道尽头", "皮卡前方大全景", "现代高墙铁门位于道路尽头，后方山路有零散追兵", "车头低机位前推", "白棠提前操作门禁。", "白棠", "外门已经解锁，进院以后我马上关门。"),
                shot("铁门只开一辆车宽", "门口固定全景", "铁门开启有限宽度，皮卡保持直线驶入", "固定镜头看清车辆通过", "不让丧尸与车辆同时进门。", "许砚", "别全开，够车进去就行。"),
                shot("皮卡冲入后立即关门", "院内中远景", "皮卡越过安全线，白棠按下关闭按钮", "跟车进院后回转看铁门", "铁门在追兵到达前合拢。", "白棠", "车进来了，关门，落锁。"),
                shot("丧尸撞在高墙外", "监控屏与双人中景", "门外少量普通型拍门，院内皮卡和鱼桶完整", "从监控移到两人", "高墙和门没有立即损坏。", "许砚", "先别管外面，活鱼必须马上入池。"),
            ]),
            ("活鱼和剩余物资清点", ["fish_tanks", "storage", "battery"], [
                shot("检查活鱼数量", "活鱼桶俯拍近景", "有限小鲫鱼仍在游动，增氧泵持续冒泡", "固定俯拍", "白棠逐桶检查，没有突然增减。", "白棠", "两桶一共十八尾，路上没有死鱼。"),
                shot("核对现有设备", "设备清单中景", "两只水箱、过滤桶、水泵、气泵和储能回路逐项摆开", "从左到右横移", "所有设备来自旧库存和前一集施工。", "许砚", "设备够用，缺的是稳定水质和长期饲料。"),
                shot("把鱼桶放入池水缓温", "双水箱中景", "封闭鱼桶浮在池水中缓慢适应温度", "从温度计移到鱼桶", "不直接把河水倒进主池。", "白棠", "先缓温，再分批兑水，河水不能进过滤系统。"),
                shot("启动内循环倒计时", "控制屏双人中景", "水泵测试、过滤桶和储能曲线同时可见", "从控制屏后拉到两人", "结尾明确下一集正式接通鱼池。", "许砚", "今晚先增氧，明天把整个循环跑起来。"),
            ]),
        ],
    },
    {
        "dir": "EP010_aquaponics-internal-loop",
        "title": "EP010：复用旧设备，十八尾鱼进入内循环",
        "summary": "两人复用旧水箱、过滤桶、井水和储能系统，完成双池内循环。河鱼经过缓温、兑水和观察后分批入池，鱼泵被列为夜间不断电负载。",
        "segments": [
            ("过滤系统先空转", ["fish_tanks", "filter", "battery"], [
                shot("过滤井水注入双池", "双水箱大全景", "过滤井水分别注入两只水箱，水位线一致", "沿进水管横移", "不使用河水直接灌池。", "白棠", "两只池都用过滤井水，河水一滴也没倒进来。"),
                shot("启动过滤桶和回水", "设备中景", "水泵启动，回水形成稳定水流", "从水泵跟到回水口", "所有部件由人物开启，不自行运转。", "许砚", "先空转一小时，确认管路不漏再放鱼。"),
                shot("储能回路单独标记", "电池控制屏近景", "鱼泵和气泵处于优先供电栏", "从回路移到备用插座", "夜间保留最低增氧。", "白棠", "鱼泵和气泵已经列进夜间保电回路。"),
                shot("检查无漏水", "地下设备区双人中景", "两人用干布检查接头，地面保持干燥", "平稳横移管路接点", "结果明确，无夸张成功特效。", "许砚", "接头都干的，可以开始给鱼兑水。"),
            ]),
            ("缓温兑水再入池", ["water_kit", "fish_tanks"], [
                shot("测温差", "温度计近景", "鱼桶与主池温度计并排，差值逐渐缩小", "固定近景", "不依赖小字表达。", "白棠", "温差已经不到一度，可以开始少量兑水。"),
                shot("每次加入少量池水", "鱼桶操作中景", "许砚用量杯向鱼桶缓慢加入池水", "跟随量杯移动", "连续三次少量兑水用短蒙太奇表达。", "许砚", "每隔五分钟加一点，让它们慢慢适应。"),
                shot("九尾鱼进入第一池", "第一水箱中景", "抄网把九尾鱼分批移入左池", "跟随抄网入水", "只用专用抄网，不倒入河水。", "白棠", "左池九尾都在游，没有浮头。"),
                shot("剩余九尾进入第二池", "双水箱大全景", "两池各九尾，回水和气泡稳定", "从左池横移到右池", "固定十八尾总数。", "许砚", "两池分开养，一边出问题还能保住另一边。"),
            ]),
            ("鱼池开始闭环运行", ["fish_tanks", "filter", "battery"], [
                shot("鱼粪水进入过滤桶", "管路与过滤桶近景", "回流水经过沉淀和过滤再返回水箱", "沿透明观察管移动", "只表现机械过滤，不夸张净化。", "白棠", "脏水先沉淀过滤，再回到鱼池。"),
                shot("过滤水进入育苗槽", "鱼池与空育苗槽中景", "少量过滤水支路流向尚未播种的育苗槽", "从分流阀移到育苗槽", "为豆类种植预留接口。", "许砚", "这条支路留给育苗，暂时只开最低流量。"),
                shot("太阳能给储能补电", "控制屏近景", "白天太阳能输入高于鱼泵消耗", "固定屏幕后移到设备", "不显示无限电量。", "白棠", "白天太阳能能盖住鱼泵用电，还能补一点储能。"),
                shot("夜间切换最低负载", "地下室双人中景", "非必要照明关闭，气泵和鱼泵保留", "灯光分区依次熄灭", "明确夜间运行边界。", "许砚", "晚上只保鱼池、监控和冰箱，其他设备停掉。"),
            ]),
            ("第一晚鱼群稳定", ["fish_tanks", "poultry", "villa"], [
                shot("鱼群正常抢食", "双鱼池中景", "十八尾鱼分两池靠近少量饵料", "从饵料移到鱼群", "投喂量有限，不让水体浑浊。", "白棠", "两池都肯吃，说明运输应激正在过去。"),
                shot("计算鱼饲料缺口", "饲料与账本近景", "有限鱼料、鸡鸭饲料和消耗表并列", "平稳横移", "同一批粮食不能无限喂两套养殖。", "许砚", "现有饲料撑不了多久，下一步必须自己种。"),
                shot("查看空育苗槽", "育苗槽双人中景", "空槽与鱼池支路相连，补光灯尚未开启", "从鱼池移到空槽", "不提前出现植物。", "白棠", "育苗槽已经接好，只差能做饲料的种子。"),
                shot("等待零点抽卡", "手机与双人中近景", "零点倒计时、饲料余量和空育苗盘同框", "从账本移到手机", "下一集由真实缺口触发抽卡。", "许砚", "今晚抽到什么，优先解决饲料和蛋白质。"),
            ]),
        ],
    },
    {
        "dir": "EP011_protein-seeds-clinic-sos",
        "title": "EP011：抽到黄豆豌豆，卫生院突然求救",
        "summary": "每日抽到有限黄豆和豌豆种子。两人把种子分为芽菜、留种和饲料三部分，刚完成播种，无线电便收到山下卫生院女医生的求救。",
        "segments": [
            ("饲料和蛋白质同时告急", ["storage", "poultry", "fish_tanks"], [
                shot("核算两套养殖消耗", "账本双人中景", "鸡鸭和鱼池饲料余量并列", "从两栏移到白棠", "白棠主动完成计算。", "白棠", "鸡鸭和鱼一起喂，现有饲料最多撑二十天。"),
                shot("鸡蛋产量仍有限", "鸡鸭棚近景", "五只禽类和当天一枚鸡蛋同框", "从鸡蛋移到鸡群", "鸡蛋不能覆盖两人长期需求。", "许砚", "鸡蛋只能补一点，不能解决长期蛋白质。"),
                shot("鱼苗仍不能食用", "双鱼池中景", "小鲫鱼在两池正常游动", "平稳横移两池", "明确不能提前捕捞种鱼。", "白棠", "这批鱼要先长大繁殖，现在一尾也不能吃。"),
                shot("零点抽卡刷新", "手机与空育苗盘近景", "简洁卡槽刷新，育苗盘在旁", "轻推手机", "不提前出现大量成品粮。", "许砚", "缺口很清楚，抽卡只看能不能持续生产。"),
            ]),
            ("抽到黄豆和豌豆种子", ["seed", "crop"], [
                shot("两包有限种子出现", "手机与种子包近景", "黄豆、豌豆种子各一小包", "从卡面移到种子", "数量有限，不铺满桌面。", "白棠", "黄豆两斤、豌豆一斤，数量不多但能留种。"),
                shot("分成三种用途", "工作台俯拍近景", "芽菜、留种、饲料三只盒子清楚分开", "依次横移三盒", "白棠直接分配，不问常识问题。", "许砚", "三成发芽吃，四成留种，剩下试种饲料区。"),
                shot("检查发芽率", "湿布与种子近景", "少量种子放入湿布测试盘", "固定俯拍", "不让种子瞬间发芽。", "白棠", "先测发芽率，坏种不能占菜床。"),
                shot("院内划出豆类区", "院内菜床大全景", "三个小区仍在高墙内，滴灌和网架清楚", "稳定横移", "只划区整地，不出现成熟作物。", "许砚", "明天播种，鱼池水只给育苗槽少量分流。"),
            ]),
            ("种子进入育苗和菜床", ["crop", "fish_tanks", "villa"], [
                shot("黄豆进入育苗盘", "育苗盘双人中景", "白棠按固定间距点播黄豆", "沿育苗格横移", "人物手动播种。", "白棠", "黄豆先育苗，出芽后再移进院内菜床。"),
                shot("豌豆沿网架点播", "院内菜床中景", "许砚在网架下点播豌豆，滴灌管在侧", "跟随点播动作", "不出现快速生长。", "许砚", "豌豆靠网架种，后面嫩梢和豆荚都能吃。"),
                shot("鱼池水少量灌入育苗槽", "管路近景", "分流阀打开最低档，水缓慢流入育苗槽", "沿水流移动", "不淹没种子。", "白棠", "流量刚好，育苗槽不会积水。"),
                shot("写下二十天目标", "计划板双人中景", "出芽、移栽、留种和饲料试验四项排列", "从计划板后拉", "种植结果需要时间兑现。", "许砚", "二十天先保住饲料，蛋白质还要继续找。"),
            ]),
            ("卫生院女医生求救", ["radio", "clinic", "drone"], [
                shot("电台收到断续呼叫", "无线电工具间中景", "电台红灯闪烁，两人停止手中工作", "从电台移到两人", "呼叫音量克制，不向山谷广播。", "女医生画外音", "这里是山下卫生院，我被困在二楼药房。"),
                shot("对方说明门外情况", "电台与地图近景", "卫生院位置被标在旧地图上", "沿路线移到诊所位置", "对方先说明身份和威胁。", "女医生画外音", "一楼有六只丧尸，我的水只够撑到明天。"),
                shot("无人机准备侦察", "车库双人中景", "无人机、电池、柴油皮卡和弓弩柜同框", "从无人机横移到皮卡", "先侦察，不立即盲目出发。", "白棠", "无人机满电，卫生院往返路线还能飞一趟。"),
                shot("许砚建立救援底线", "地图桌双人中景", "侧门、后巷和撤离路线清楚", "轻推路线图", "结尾确定次日白天行动。", "许砚", "先确认她没被咬，天亮后再决定怎么进去。"),
            ]),
        ],
    },
    {
        "dir": "EP012_pickup-rescues-doctor",
        "title": "EP012：无人机引开尸群，最后关头救出沈知夏",
        "summary": "无人机确认卫生院侧门仍可用。许砚驾驶柴油皮卡，白棠留守远程操控无人机，用机械声引开大部分普通型；许砚以有限弩箭清除侧门阻挡，最后关头救出急诊医生沈知夏。",
        "segments": [
            ("无人机确认救援路线", ["drone", "clinic", "radio"], [
                shot("无人机抵达卫生院上空", "无人机航拍大全景", "诊所、侧门、后巷和六只普通型位置清楚", "低速环绕半圈", "不贴近人物正脸。", "白棠画外音", "正门堵死，侧门外只有两只，后巷能停车。"),
                shot("窗边确认沈知夏", "无人机中远景", "二楼窗边出现暗酒红医护工装身影", "稳定悬停", "沈知夏固定数字人首次作为远距离身份锚点。", "沈知夏画外音", "我没有被咬，左臂是药柜砸伤。"),
                shot("标出无人机诱导路线", "地图桌双人中景", "正门到停车场的诱导路线与皮卡后巷路线分开", "沿两条路线横移", "白棠负责无人机，许砚负责接人。", "许砚", "你把正门的引去停车场，我从后巷接她。"),
                shot("救援装备装车", "车库中景", "弓弩、六支箭、急救包和皮卡同框", "从箭盒移到车门", "有限武器数量清楚。", "白棠", "六支箭、半箱柴油、急救包，全部装好了。"),
            ]),
            ("皮卡和无人机同时行动", ["pickup", "drone", "clinic"], [
                shot("无人机掠过诊所正门", "正门全景", "无人机发出短促机械声后飞向停车场", "低空侧向移动", "四只普通型转向追逐，无人机保持安全高度。", "白棠画外音", "四只已经跟走，侧门还剩两只。"),
                shot("皮卡进入后巷", "后巷低机位全景", "皮卡倒车贴近侧门，车头朝撤离方向", "低机位跟车停稳", "车辆不撞墙，不熄火。", "许砚", "我到侧门了，你让她现在下楼。"),
                shot("沈知夏从楼梯撤离", "诊所内部中景", "沈知夏背医疗包快速下楼，左臂简单包扎", "手持跟随下楼", "她独立行动，不等待英雄抱走。", "沈知夏", "药品和器械都在包里，我一分钟到侧门。"),
                shot("许砚举弩守住侧门", "侧门外中景", "许砚靠皮卡车门稳定瞄准，两只普通型接近", "从弩箭移到目标路线", "不连续乱射。", "许砚", "门一开就上车，不要停下来解释。"),
            ]),
            ("最后十秒救出沈知夏", ["clinic", "crossbow", "pickup"], [
                shot("第一箭阻断最近目标", "侧门动作中景", "箭命中最近丧尸肩颈区域使其倒向一侧", "短促跟箭后回到许砚", "非血腥，不穿模。", "许砚", "左边倒了，右边那只正在靠近车门。"),
                shot("沈知夏推门冲出", "侧门全身中景", "沈知夏推门后直接跑向皮卡后座", "侧向跟随她的完整步伐", "人物腿部始终完整可见。", "沈知夏", "我出来了，医疗包和急救器械都在。"),
                shot("第二只丧尸抓住车门边缘", "皮卡侧面中景", "普通型伸手碰到外侧门框，许砚用弩托推开", "近距离跟随受力点", "不让手臂穿过车门。", "许砚", "上车，门关好。"),
                shot("皮卡在尸群回流前离开", "后巷大全景", "沈知夏进入后座，皮卡加速驶离，无人机从停车场返回", "后拉展示撤离方向", "最后关头完成救援，不在原地对话。", "白棠画外音", "正门尸群在回头，直接按原路撤。"),
            ]),
            ("回到别墅先隔离", ["quarantine", "pickup", "villa"], [
                shot("皮卡进入车库隔离线", "车库大全景", "皮卡停在黄色隔离线内，主楼内门关闭", "跟车进入后固定", "不直接进入生活区。", "许砚", "欢迎先放一放，七十二小时隔离不能省。"),
                shot("沈知夏主动交出医疗包", "传递箱中景", "沈知夏把医疗包放进双门传递箱", "跟随包进入箱体", "物资不瞬移。", "沈知夏", "可以，药品清单和使用方法都在最上面。"),
                shot("白棠远程测温登记", "隔离窗双人中景", "白棠在窗外操作测温仪并记录", "固定中景", "两人不直接接触。", "白棠", "体温正常，左臂划伤需要继续观察。"),
                shot("沈知夏进入独立隔离间", "隔离医疗区全景", "沈知夏走进有床、洗手台和监控的隔离间", "完整全身跟随", "固定服装和腿部完整，门在身后关闭。", "沈知夏", "先给我消毒工具，伤口我自己处理。"),
            ]),
        ],
    },
    {
        "dir": "EP013_quarantine-ability-contract",
        "title": "EP013：隔离七十二小时，女医生命状态感知觉醒",
        "summary": "沈知夏完成七十二小时隔离。她在检查鱼池时短暂感知到缺氧鱼群，随后用现实检测验证能力边界；系统发放协作契约，她自愿签约加入。",
        "segments": [
            ("隔离七十二小时不走捷径", ["quarantine", "clinic"], [
                shot("第三天完成体征记录", "隔离窗中景", "体温、血氧和伤口记录摆在传递台", "逐项横移", "白棠主动核对三天记录。", "白棠", "七十二小时体温正常，伤口也没有感染。"),
                shot("沈知夏完成最后检查", "医疗台中景", "沈知夏自行检查瞳孔、血氧和手臂活动", "稳定横移", "不靠系统直接放行。", "沈知夏", "没有抽搐和攻击冲动，划伤也已经结痂。"),
                shot("开放有限区域权限", "门禁屏中景", "医疗间、农业区亮起，主控室仍关闭", "从权限屏移到门卡", "权限有限。", "许砚", "你能进医疗和农业区，主控室暂时不开。"),
                shot("沈知夏开始整理药品", "医疗间全身中景", "她完整走入医疗间，把药包放上隔离架", "侧向全身跟随", "人物腿部完整，服装固定。", "沈知夏", "够了，我先把救回来的药重新分类。"),
            ]),
            ("生命状态感知第一次出现", ["fish_tanks", "low_oxygen", "quarantine"], [
                shot("沈知夏靠近右侧鱼池", "地下鱼池三人中景", "她在右池五米内停步，轻按太阳穴", "缓慢推近", "异能视觉极轻。", "沈知夏", "右边那池有一片生命状态在往下掉。"),
                shot("白棠先看鱼群表现", "右池近景", "几尾鱼靠近水面，回水比左池弱", "从水面移到回水口", "白棠主动发现现实异常。", "白棠", "右池回水变小，已经有鱼开始浮头。"),
                shot("许砚限制使用时间", "设备区中景", "许砚关闭非必要负载并看计时器", "从计时器移到沈知夏", "能力不无限使用。", "许砚", "二十秒就停，后面靠设备检查。"),
                shot("沈知夏出现头痛", "医疗台中景", "她坐下按住太阳穴，白棠递水", "轻微失焦后恢复", "不夸张晕倒。", "沈知夏", "最多半分钟，用久了会头痛、看不清。"),
            ]),
            ("现实检测验证能力", ["water_kit", "fish_tanks", "battery"], [
                shot("检查右池气泵", "设备近景", "右池气管松脱，气泡明显变少", "从接头移到水面", "异常原因可见。", "白棠", "右池气管松了，气泡只有左边一半。"),
                shot("重新固定气管", "操作中景", "许砚卡紧接头，气泡逐渐恢复", "跟随手部操作", "不自动修复。", "许砚", "接头固定好了，先看鱼群能不能缓过来。"),
                shot("试纸排除水质突变", "水样近景", "两池水样与试纸并排", "固定俯拍", "检测结果支撑判断。", "沈知夏", "水质没有突变，主要问题就是短时缺氧。"),
                shot("能力边界写入记录", "医疗间三人中景", "五米、三次、三十秒和副作用用图标记录", "沿记录板横移", "不依赖小字。", "白棠", "一天最多三次，只用来找异常范围。"),
            ]),
            ("自愿签下协作契约", ["contract", "quarantine", "radio"], [
                shot("里程碑契约出现", "手机与三人中景", "协作契约卡简洁显示权限、任务和退出条款", "从手机移到三人", "不是奴役契约。", "白棠", "系统奖励协作契约，签不签由你决定。"),
                shot("沈知夏核对医疗自主", "手机与沈知夏中近景", "她主动查看医疗权限栏", "缓慢推近", "不秒签。", "沈知夏", "安全行动听指挥，医疗判断必须由我负责。"),
                shot("许砚确认边界", "三人对话中景", "许砚站在桌对面，不控制她的动作", "固定中景", "契约不控制思想。", "许砚", "安全规则必须执行，专业问题你说了算。"),
                shot("沈知夏按下确认", "手部与门卡近景", "她主动按下确认并拿到医疗门卡", "固定近景后上移", "不出现锁链或洗脑光效。", "沈知夏", "成交，我先把医疗间和检疫流程建起来。"),
            ]),
        ],
    },
    {
        "dir": "EP014_night-pump-failure-three-person-team",
        "title": "EP014：鱼泵夜间停转，三个人第一次协同救池",
        "summary": "夜间储能保护切断鱼泵，白棠发现浮头，沈知夏用有限感知判断右池更危险，许砚重排供电并接上备用气泵。三人第一次形成生产、医疗与工程协同。",
        "segments": [
            ("鱼泵夜间突然停了", ["low_oxygen", "battery", "fish_tanks"], [
                shot("白棠听见设备安静", "地下鱼池中景", "回水停止，鱼群靠近水面", "从静止水面移到白棠", "她主动发现异常。", "白棠", "回水声没了，右池已经有鱼浮头。"),
                shot("储能柜触发保护", "控制屏近景", "低电量保护切断鱼泵回路", "从报警灯移到断开回路", "停电原因明确。", "许砚画外音", "储能触发保护，先关掉非必要负载。"),
                shot("沈知夏判断右池更急", "双鱼池三人中景", "沈知夏只感知十秒后停止", "缓慢推近右池", "能力有限且立即停用。", "沈知夏", "右池下降得更快，先给右边增氧。"),
                shot("白棠拿出备用气泵", "设备柜中景", "白棠取出旧备用气泵和两根气管", "跟随设备到鱼池", "旧资产重新利用。", "白棠", "备用气泵在这里，我先接右池。"),
            ]),
            ("三人分工救鱼", ["low_oxygen", "battery", "fish_tanks"], [
                shot("白棠接上右池气泵", "右池操作中景", "气管入水后气泡恢复", "跟随气管入水", "人物手动完成。", "白棠", "右池气泡恢复了，鱼还没有继续翻身。"),
                shot("许砚切断非必要电路", "储能柜中景", "景观灯、工具充电和部分照明依次关闭", "沿回路逐项横移", "为鱼泵腾出电量。", "许砚", "关掉照明和充电，鱼泵先恢复最低流量。"),
                shot("沈知夏观察呼吸变化", "鱼池近景", "鱼群逐渐离开水面恢复游动", "从鱼鳃移到水下", "不用异能宣布治愈。", "沈知夏", "呼吸在恢复，继续增氧，不要马上喂食。"),
                shot("左池也接上分气管", "双池大全景", "一台气泵通过分气阀给两池供气", "从右池横移到左池", "应急方案可持续一晚。", "白棠", "两池都接上了，今晚轮流检查。"),
            ]),
            ("重排全屋供电优先级", ["battery", "fish_tanks", "quarantine"], [
                shot("列出一级负载", "计划板三人中景", "鱼泵、监控、冰箱和医疗设备列在一级", "依次横移", "优先级明确。", "许砚", "鱼泵、监控、冰箱和医疗设备列为一级。"),
                shot("列出可延后负载", "控制屏近景", "工具充电、景观灯和热水器进入白天栏", "固定近景", "不无限用电。", "白棠", "工具和热水器改到白天太阳能有余量再开。"),
                shot("医疗设备保留独立插座", "医疗间中景", "沈知夏给制氧机和小冰箱贴上独立回路标记", "从插座移到设备", "医疗不挤占鱼池应急电。", "沈知夏", "药品冰箱不能断，制氧机平时保持关闭。"),
                shot("完成夜间自动切换", "储能柜三人中景", "许砚设定低电量时只保一级负载", "从控制屏后拉", "规则由设备执行但由人物设定。", "许砚", "下次电量下降，系统只保这四项。"),
            ]),
            ("第一次三人协同成功", ["fish_tanks", "radio", "villa"], [
                shot("天亮鱼群恢复", "双鱼池中景", "十八尾鱼分两池正常游动", "稳定横移", "数量不变，不宣布无损奇迹。", "白棠", "十八尾都活着，昨晚的处理有效。"),
                shot("复盘异常顺序", "计划板三人中景", "发现、判断、供电、增氧四步用图标表达", "沿四步横移", "三人职责互补。", "沈知夏", "先看表现，再找范围，最后才决定处理。"),
                shot("备用电量仍然有限", "储能屏近景", "剩余电量和柴油库存都下降", "固定屏幕后移", "保留资源压力。", "许砚", "救回来了，但储能和柴油都不是无限的。"),
                shot("三人回到各自岗位", "院内农业区大全景", "白棠去菜地、沈知夏去医疗间、许砚检查太阳能", "稳定后拉", "自然衔接EP015一个月生产。", "白棠", "鱼池稳定了，今天继续种豆和照看鸡鸭。"),
            ]),
        ],
    },
]


def build_prompt(number, title, refs, shots, include_shen, include_raider_leader):
    wardrobe = XU_OUTFIT + BAI_OUTFIT + (SHEN_OUTFIT if include_shen else "") + (RAIDER_LEADER_OUTFIT if include_raider_leader else "")
    character_distinction = "角色区分：白棠是年轻利落的建造搭档，鼠尾草绿工装、轻快执行和记录习惯。"
    if include_shen:
        character_distinction += "沈知夏是深栗色微卷长发、暗酒红医护工装的成熟急诊医生，沉稳专业、心地善良但不软弱；禁止两人同发型、同服装、互换功能位或使用相同少女化表情。"
    lines = [
        "16:9横屏，15秒，720p，真人末日生存短剧。" + wardrobe,
        character_distinction + "人物对白克制，动作镜头不强制口型；禁止数字人原始服装和随机换装。",
        "",
    ]
    for index, key in enumerate(refs, 1):
        lines.append(f"参考图{index}：{LABELS[key]}；图中没有人物，不锁人物脸和服装。")
    lines.extend(["", f"Segment {number:02d}：{title}", "", "四个镜头连续推进，同一物体的位置和数量保持稳定。", ""])
    names = "一二三四"
    for index, item in enumerate(shots):
        lines.extend([
            f"镜头{names[index]}｜{item['title']}",
            f"景别：{item['framing']}。",
            f"构图：{item['composition']}。",
            f"运镜手法：{item['camera']}。",
            f"画面内容：{item['content']}",
            f"说话者绑定：本镜头仅{item['speaker'].replace('画外音', '').replace('通过对讲', '').replace('低声', '')}开口；若为画外音或对讲声，则画面中所有人物保持闭嘴。普通对白必须给说话者未遮挡的正面嘴部，其他人物不在画面、侧背对镜头或闭嘴。",
            f"{item['speaker']}：",
            f"“{item['dialogue']}”",
            "",
        ])
    lines.extend([
        "声音：保留环境声、设备声和动作声；每个镜头最多一句对白，说完再执行关键动作。禁止字幕、水印、logo。",
        "禁止：人物连续说话、多人同时开口、嘴穿口罩、物体瞬移、自动施工、数量漂移、人物换脸、人物换装、数字人原始服装、第二栋别墅、农业区出现在围墙外、二次元、游戏CG。",
    ])
    return "\n".join(lines) + "\n"


def write_episode(data):
    episode = EPISODES / data["dir"]
    episode.mkdir(parents=True, exist_ok=True)
    segment_dirs = ["segment_01_00-15s", "segment_02_15-30s", "segment_03_30-45s", "segment_04_45-60s"]
    overview = [f"# {data['title']}", "", data["summary"], "", "| Segment | 核心任务 |", "| --- | --- |"]
    all_refs = []
    episode_has_shen = False
    for number, ((title, refs, shots), dirname) in enumerate(zip(data["segments"], segment_dirs), 1):
        segment = episode / dirname
        (segment / "frames").mkdir(parents=True, exist_ok=True)
        (segment / "output").mkdir(parents=True, exist_ok=True)
        include_shen = "沈知夏" in str(shots)
        include_raider_leader = "罗彪" in str(shots)
        episode_has_shen = episode_has_shen or include_shen
        prompt = build_prompt(number, title, refs, shots, include_shen, include_raider_leader)
        for filename in ("director-promt.txt", "prompt.md", "storyboard.md"):
            (segment / filename).write_text(prompt, encoding="utf-8")
        (segment / "first-frame.md").write_text(f"# 首帧\n{shots[0]['content']}\n", encoding="utf-8")
        (segment / "last-frame.md").write_text(f"# 尾帧\n{shots[-1]['content']}\n", encoding="utf-8")
        humans = [XU, BAI] + ([SHEN] if include_shen else []) + ([RAIDER_LEADER] if include_raider_leader else [])
        api = [f"# Segment {number:02d} API 请求", "", "- 数字人：" + "、".join(f"`{human}`" for human in humans)]
        api.append("- 生成策略：先生成真实首尾帧，再按 Segment 顺序串行提交；禁止四段并发直出")
        api.append("- 服装：按导演提示词固定 Outfit ID，数字人原始服装不参与生成")
        for key in refs:
            api.append(f"- 参考图：`stories/forest-villa-apocalypse/{ASSETS[key]}`")
        api.extend(["- 参数：`doubao-seedance-2-0-mini-260615`、15s、16:9、720p、audio", "- 状态：剧本与资产已准备，尚未提交付费视频任务"])
        (segment / "api-request.md").write_text("\n".join(api) + "\n", encoding="utf-8")
        overview.append(f"| {number:02d} | {title} |")
        all_refs.extend(refs)

    (episode / "episode.md").write_text("\n".join(overview) + "\n", encoding="utf-8")
    (episode / "overview-storyboard.md").write_text("# 总览故事板\n\n" + "\n".join(overview[4:]) + "\n", encoding="utf-8")
    continuity = [
        "# 连续性", "",
        "- EP007及其已生成视频保持不变，本集从现有鸡鸭、菜地、高墙、皮卡、无人机和弓弩状态继续。",
        "- 一集四段，每段十五秒、四镜头、四句关键对白；动作镜头不安排连续口型。",
        "- 别墅始终只有一栋现代三层建筑，所有生产设施均在高墙内。",
        "- 抽卡只给有限工具、种子或方法，施工、捕鱼、运输、检测和救援均由人物完成。",
        "- 许砚和白棠固定数字人、固定服装；视频生成必须串行并使用真实首尾帧衔接。",
    ]
    if episode_has_shen:
        continuity.append("- 沈知夏固定使用 `asset-20260310030618-88hlb` 和 `FVA_SHEN_ZHIXIA_OUTFIT_001`；EP010 救援后直接接手车库医疗区，医疗、隔离和用药流程由她负责。")
    (episode / "continuity.md").write_text("\n".join(continuity) + "\n", encoding="utf-8")
    unique_refs = list(dict.fromkeys(all_refs))
    manifest = ["# 图片清单", ""] + [f"- `stories/forest-villa-apocalypse/{ASSETS[key]}`" for key in unique_refs]
    (episode / "image-manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    qa = [
        "# QA Checklist", "",
        "- [ ] 四个 Segment 均为四镜头和四句关键对白，总口播适合十五秒。",
        "- [ ] 戴口罩、高速驾驶、奔跑、吊装等动作中不强制人物持续说话。",
        "- [ ] 数字人资产独立传入，固定服装没有被原始服装覆盖。",
        "- [ ] 生成视频前补齐真实16:9首尾帧，并按顺序串行生成。",
        "- [ ] 所有参考资产存在，不上传无关人物图或错误车型图片。",
        "- [ ] 尚未提交付费视频任务。",
    ]
    (episode / "qa-checklist.md").write_text("\n".join(qa) + "\n", encoding="utf-8")
    publish = [
        "# 发布包", "",
        f"- 标题：{data['title'].split('：', 1)[1]}",
        "- 封面：本集最清楚的资源结果或动作危机，16:9真人实景，主体居中。",
        "- 评论引导：如果是你，会继续冒险找资源，还是先守住现有生产？",
        "- 标签：末日种田、别墅生存、抽卡系统、丧尸逃生、真人短剧",
    ]
    (episode / "publish-package.md").write_text("\n".join(publish) + "\n", encoding="utf-8")


def keep_one_dialogue_per_shot(episode_dir, choices):
    episode = EPISODES / episode_dir
    segment_dirs = ["segment_01_00-15s", "segment_02_15-30s", "segment_03_30-45s", "segment_04_45-60s"]
    dialogue_pattern = re.compile(r"^([^\n：]{1,12}(?:画外音)?)：\n([“\"][^”\"\n]+[”\"])(?:\n)?", re.MULTILINE)
    for segment_name, shot_choices in zip(segment_dirs, choices):
        segment = episode / segment_name
        director = segment / "director-promt.txt"
        if not director.exists():
            continue
        parts = re.split(r"(?=^镜头[一二三四]｜)", director.read_text(encoding="utf-8"), flags=re.MULTILINE)
        rewritten = [parts[0]]
        for block, keep_index in zip(parts[1:5], shot_choices):
            matches = list(dialogue_pattern.finditer(block))
            for index, match in reversed(list(enumerate(matches))):
                if index != keep_index:
                    block = block[:match.start()] + block[match.end():]
            rewritten.append(block)
        rewritten.extend(parts[5:])
        text = "".join(rewritten)
        for filename in ("director-promt.txt", "prompt.md", "storyboard.md"):
            (segment / filename).write_text(text, encoding="utf-8")


def main():
    write_episode(EPISODES_DATA[0])
    print("EP008 rebuilt. Use build_ep009_016_raider_arc.py for EP009-EP016.")


if __name__ == "__main__":
    main()
