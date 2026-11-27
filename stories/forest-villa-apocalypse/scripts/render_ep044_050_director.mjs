import { cameraPlan, directorRevision } from './ep044-050-camera-plan.mjs';

const fmt = time => (time / 100).toFixed(2).replace(/\.?0+$/, '');
const spokenCount = text => (text.match(/[\p{Script=Han}\p{N}]/gu) || []).length;
const lineNumber = (prefix, index) => `${prefix}${String(index + 1).padStart(2, '0')}`;

const rhythm = {
  EP044: [
    '冬狼先说要谁，同伙即跑向黑门；门一撞就切歪锁和护臂。许砚不交人，白棠看到他顶住门后立即还手；在她手还没落定时过段。',
    '白棠用最后一轮让随从离门，却看见冬狼反向冲回。重撞后护臂立刻失力，酒红色袖口接下一镜。知夏接触时才出现一次微光；门重新抵稳，但过热灯不能熄灭。',
    '接门板顶退冬狼，他冲不开才换旧命令。凝霜认得那种口气，压住怒意只回一句。接两只靴先后冻住，再看她收指，厚冰声出时立即过段。',
    '冰层上升、倒下扬雪、后方转身而逃连续发生。许砚看到凝霜手滑时就伸手，同一动作接下个镜头。答完话马上转肩、搀扶、迈步，收尾时人物仍在往主楼走。',
  ],
  EP045: [
    '先拍一次推门失败，再把门板重量交给撑杆。旧件与新件做动作匹配，直接省略加工和安装等待；完整保留试推发生在「锁住了」之前。',
    '由上一段的膜响进入温室，先看落雪砸到苗，再搬第一盘。用许砚暂时扣住旧膜隔开两次搬运，最后看到两盘苗都在暖台上。',
    '三张卡先显形，白棠看过苗才给选择。点选后只实体化一卷膜；末镜展开一小截又收好，保温膜还没用到院里。',
    '开画就是清晨，两人从相反一端扶同一片膜。扣合、松手、放回苗盘按顺序发生，末镜留出工具车上的剩膜。',
  ],
  EP046: [
    '一粒冰落进空盘，让观众先看懂缺水。冻壶由人接走，工具车在有薄冰的鱼池旁停下；凝霜扶稳原架，接后续施工。',
    '先给禽舍迎风面和上沿的通气口，再沿剩膜递出的方向去鱼池。最后透过水汽看见鱼影，水一直在原池循环。',
    '饮水器恢复供水后，切相邻窝箱。把一枚蛋留在白棠手里，再由凝霜看向饲料勺，自然进入照看的分工。',
    '从室内落稳的一枚蛋切到许砚例行巡查，再用远景交代树林中的细烟。回终端只记下位置，情绪不抬成作战警报。',
  ],
  EP047: [
    '先给亮灯和冰冷地面的反差。许砚起身、知夏跟上后就硬切能源棚，从可见的冷热差异结束，不重复介绍供电。',
    '知夏的手碰到外部传感器，紧接同框两件反应不同；许砚打开盒子只剩一只，结尾由她让出位置决定更换。',
    '旧件落盘，接新件已经就位。让设备轻响向下一镜过渡；回客厅前省略升温等待，听白棠说话时毯子才折好。',
    '终端已经稳定，知夏仍不肯立刻走。许砚接过终端，硬切回屋把空盒搁下；关手电后留一拍让对话自然结束。',
  ],
  EP048: [
    '空盒和旧件是开场问题；许砚手指在两种材料之间做区别。出件镜只看有限的实物，白棠分格装好，留下一些原料。',
    '从人手托住的同一块护板开始，白棠撤手后板才算装稳。硬切窗边苗架，看清一端没光，许砚才拿起手机。',
    '罐头和育苗灯同框给出取舍。投影变实物后，跳过搬运等待直接到灯架旁；结尾只见灯已固定，仍不亮。',
    '苗盘先落稳，灯才亮。用对讲提示音把工作间接到门口，让住户先完整说明来意；许砚听完再应声。',
  ],
  EP049: [
    '先留自用、再给出愿意交换的份量；门外举盐后，许砚才报价。尾镜收到答应，但两样货还在各自一侧。',
    '按上一段的成交直接交接，不重念价格。盐收好才切来客放下小泵；许砚只答应检查，泵还没进工作间。',
    '旧泵放台后晃了一下，白棠看向余料。许砚询问、来客发照片；段尾只能看见手机上的包装，实物还没到。',
    '先约明天验料，再留下待修的泵。白棠的玩笑和许砚的回复都对着同一台泵，最后只用脚步送走来客。',
  ],
  EP050: [
    '对照新旧支架后看同一台泵试转，水起泡再到流稳。硬切到温室两盘不同阶段的菜，白棠在片尾选定一盘。',
    '先用一镜看掌下那盘叶片展开，邻盘不变。剪下一把菜才分装，两份分清后回工作间接许砚抱泵去门口。',
    '先给试水结果，再略去试打时间看合格试片。手提旧泵交代交货已经完成，最后把话落在苗长稳后再联系。',
    '碗先落桌，终端随后扣下。凝霜吃一口、咽下、抬眼才开口；许砚说完再拿筷子，留在热饭和窗边小苗上。',
  ],
};

const specialSound = {
  'EP044/3': '冰只从门外雪地与脚边出现，院内叶凝霜只有按柱动作与呼吸。门内外声场硬切，冰层尚未升到躯干。',
  'EP044/4': '接门外同一冰层的虚构异能效果。碎雪闷声先落，再收回门内；冰不穿墙，院内的对白不配给墙外轮廓。',
  'EP045/3': '手机只以三张图形投影交代选项，选中一张后才出现实物。投影声消退，卷材落台是单独一次实声。',
  'EP047/2': '短促微光只属于知夏接触外部传感器这一刻。靠两个外部件一动一停交代排查结果，不给主机内景。',
  'EP048/3': '卡牌只在同一部手机上出现。中选项先投影，再落成有限实物；跳到安装镜后无投影，灯不提前亮。',
  'EP050/2': '白棠掌下微光只照一盘。叶面变化结束后才给剪菜声与落篮声，邻盘保持此前的幼苗状态。',
};

// Lines that explicitly follow an action are held back within their shot.
const leadIn = {
  EP044: [[.45, 0, .50, 0], [0, .50, 0, .60], [.95, .60, 0, 0], [0, 0, 1.35, .45]],
  EP045: [[.40, .45, .30, .25], [.35, .40, .30, .35], [.30, .25, .35, .25], [.35, .45, .55, .35]],
  EP046: [[.35, .30, .35, .60], [.35, .35, .40, .70], [.45, .45, .30, .55], [.35, .25, .65, .50]],
  EP047: [[.25, .45, .35, .40], [.25, .60, .35, .30], [.30, .35, .30, .40], [.35, .30, .25, .30]],
  EP048: [[.25, .30, .40, .35], [.25, .50, .40, .35], [.35, .30, .30, .35], [.30, .30, .35, .30]],
  EP049: [[.25, .40, .35, .35], [.25, .25, .25, .30], [.35, .35, .25, .25], [.30, .30, .30, .40]],
  EP050: [[.30, .40, .35, .35], [1.30, .35, .30, .30], [.40, .35, .30, .35], [.30, .40, 1.35, .45]],
};

const effects = {
  'EP045/1/4': {
    composition: '白棠的手在门侧，许砚站在中央锁舌的另一侧，两人不挡住门缝。',
    camera: '固定内侧双人机位，安装时间已经在上一个切镜省略；本镜始终看同一次试门。',
    action: '开镜新锁板已经装好，撑杆刚被白棠撤开。许砚说前半句，她轻推门一次；锁舌入位，门不再晃。许砚看清结果再说后半句。',
  },
  'EP045/3/3': { action: '指尖点选保温膜，另两张先变暗并退去。空台上出现卷材的投影轮廓，硬切到同一轮廓凝成实物并落台；留一声落台重音，不追加其他物资。' },
  'EP046/4/2': { action: '许砚放下手套，确认终端的例行巡查画面已亮起，回应厨房那边的白棠。起飞过程省略，下镜直接到已经飞行一段时间的远视角。' },
  'EP047/1/4': { action: '硬切到能源棚，外部支路已停机隔离。镜头只给柜外两根管与终端上的热冷差异，不展示机组内部或操作步骤。许砚看见差别，才从画外指出。' },
  'EP047/3/1': { action: '原外部供暖支路已隔离。许砚把卡住的旧件搁上托盘，开口让同伴先别扔。借落盘声切到新件已回原位的画面；只展示摆放和结果，不展开接线或开机步骤。' },
  'EP048/3/4': { action: '从空台组件硬切同物已到原架边。许砚扶着灯件核对就位，白棠的手只在画边抵稳另一端。定在单层灯条装好但还不亮，省略重复紧固。' },
};

export function renderDirector(episode, segment, index, refs, roles, voices, building) {
  const ep = episode.slice(0, 5);
  const plan = cameraPlan[ep]?.[index];
  if (!plan || plan.length !== 5) throw new Error(`Missing director blocking: ${ep}/${index + 1}`);
  const [space, ...blocking] = plan;
  let start = 0;
  const shots = segment.shots.map((original, i) => {
    const shot = { ...original, ...effects[`${ep}/${index + 1}/${i + 1}`] };
    const [endSeconds, lens_mm, position, focus, transition] = blocking[i];
    const end = Math.round(endSeconds * 100);
    const speechStart = start + Math.round(leadIn[ep][index][i] * 100);
    const punctuationPause = ep === 'EP045' && index === 0 && i === 3
      ? 68 : (shot.dialogue.slice(0, -1).match(/[，。？！、]/g) || []).length * 12;
    const speechEnd = speechStart + Math.ceil(spokenCount(shot.dialogue) * 100 / 4.25) + punctuationPause;
    const speechWindow = shot.mode === 'silent' ? null : [speechStart, speechEnd];
    if (end <= start || (speechWindow && speechEnd > end - 5) || !lens_mm || !position || !focus || !transition) {
      throw new Error(`Invalid shot/speech timing ${ep}/${index + 1}/${i + 1}: ${start}-${end}, ${speechStart}-${speechEnd}`);
    }
    const out = { ...shot, time: [start, end], speech_window: speechWindow, lens_mm, position, focus, transition };
    start = end;
    return out;
  });
  if (start !== 1500) throw new Error(`Incomplete 15-second timeline: ${ep}/${index + 1}`);
  const spokenShots = shots.filter(s => s.speech_window);
  const speakers = [...new Set(spokenShots.map(s => s.speaker))];
  const scopedRefs = refs.references.some(r => r.shots);
  const mode = shot => shot.mode === 'voiceover' ? '画外音' : '外部对白';
  const referenceLine = r => {
    if (r.uri) return `参考图${r.number}＝${r.uri}，${r.name}，只锁脸与身份，服装见下文。`;
    const scope = r.scope.replace('；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果', '');
    return `参考图${r.number}＝${r.segment_file}，${r.label}，${scope}，文件已存在。`;
  };
  const lines = [
    `16:9横屏，15秒，480p草稿，电影感真人实拍，有声音。${ep}第${String(index + 1).padStart(2, '0')}段《${segment.title}》，全片${index * 15}–${(index + 1) * 15}秒，以下均为段内时间。`, '',
    '参考输入', '',
    ...refs.references.map(referenceLine), '',
    scopedRefs ? '数字人和本地图按上述顺序输入。数字人锁本人身份，三视图只锁服装、发型和体态，场景图只锁空间，动作关键帧仅用于指定镜头。关键帧不是首尾帧，不把参考图拼进视频。'
      : '数字人和本地图统一按上面的顺序输入。资产图只锁注明的对象；不上传首尾帧、不把原图拼入正片。', '',
    '人物与站位', '',
    ...segment.cast.flatMap(name => {
      const ref = refs.references.find(r => r.name === name);
      const appearance = shots.map((s, i) => s.faces.includes(name) ? lineNumber('L', i) : '').filter(Boolean).join('、');
      return [`${name}对应参考图${ref.number}，清晰露脸镜头为${appearance}。${roles[name].description}`, ''];
    }),
    ...segment.offscreen.flatMap(name => [`${name}只发声，不露脸。${roles[name] ? `仅在分镜明确写出时，手、袖口或肩背按原定装入画：${roles[name].description.split('。')[0]}。` : '仅保留分镜明确写出的手、衣袖或无脸背影。'}`, '']),
    '空间、道具与光线', '',
    `${segment.time}。${space}`, '',
    building, '',
    '特效路径与声画', '',
    specialSound[`${ep}/${index + 1}`] || '以实物触碰、人的动作和环境声交代变化。只保留本镜已经写出的设备或环境效果，不加界面特效。', '',
    `${speakers.map(name => `${name}为${voices[name]}`).join('；')}。对白音量高于音乐及底噪，画外音保留实际声源，不给画面里的人补口型。`, '',
    '起点与终点', '',
    `起点　${segment.opening}`, '',
    `终点　${segment.ending}`, '',
    '本段节奏', '',
    rhythm[ep][index], '',
    ...(ep === 'EP044' ? ['全段实时动作，不做慢动作、定格或停口等字幕。每镜第一拍从上一镜的声音或动作进入，台词说完人物继续做本镜动作；末尾在动作仍在进行时切走。', ''] : []),
    '逐镜导演设计', '',
  ];
  for (const [i, shot] of shots.entries()) {
    const shotId = lineNumber('L', i);
    const faces = shot.faces.map(n => `${n}（参考图${refs.references.find(r => r.uri && r.name === n).number}）`);
    const visualRefs = refs.references.filter(r => r.shots?.includes(shotId));
    const lips = shot.mode === 'voiceover' ? '镜内人物不补口型。' : `仅${shot.speaker}嘴部清楚并随对白开合，其他人闭口。`;
    const hold = ep === 'EP045' && index === 0 && i === 3 ? '前后两句之间留一次完整试推。' : '';
    const dialogueCue = shot.speech_window
      ? `${lineNumber('D', spokenShots.indexOf(shot))}由${shot.speaker}以${mode(shot)}发声。${shot.delivery}${lips}${hold}`
      : '无对白、旁白或可辨人声；不生成说话口型。';
    lines.push(`### ${shotId}｜${shot.time.map(fmt).join('–')}秒`, '',
      ...(visualRefs.length ? [`本镜参考　${visualRefs.map(r => `参考图${r.number}＝${r.segment_file}`).join('；')}。`, ''] : []),
      `焦段与景别　全画幅等效${shot.lens_mm}mm，${shot.size}。`, '',
      `机位与构图　${shot.position}。${shot.composition}${faces.length ? `清晰露脸仅${faces.join('、')}。` : '本镜不出现清晰人脸。'}`, '',
      `运镜路线　${shot.camera}`, '',
      `焦点与景深　${shot.focus}。`, '',
      `画面动作　${shot.action}`, '',
      `声音设计　${dialogueCue}现场声：${shot.sound.slice(1, -1)}。`, '',
      `镜头衔接　${shot.transition}。`, '');
  }
  lines.push('段内台词', '',
    ...spokenShots.flatMap((shot, i) => [`${lineNumber('D', i)}｜${shot.speech_window.map(fmt).join('–')}秒｜${shot.speaker}／${mode(shot)}｜“${shot.dialogue}”`, '']),
    '画面与连续性', '',
    `${segment.bridge}每句对白只发声一次。人物服装、建筑和道具外观沿用本段参考；物件位置、通电和物资数量以实际动作进度为准。画面无字幕、解释字卡、可读界面文字、坐标和水印。对白窗口为文字估排。`, '');
  return { revision: directorRevision, text: lines.join('\n'), shots };
}
