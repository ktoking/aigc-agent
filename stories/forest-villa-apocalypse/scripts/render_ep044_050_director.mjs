import { cameraPlan, directorRevision } from './ep044-050-camera-plan.mjs';

const nums = ['一', '二', '三', '四'];
const fmt = time => (time / 100).toFixed(2).replace(/\.?0+$/, '');
const spokenCount = text => (text.match(/[\p{Script=Han}\p{N}]/gu) || []).length;

// Lines that explicitly follow an action are held back within their shot.
const leadIn = {
  EP044: [[.30, .35, .45, .45], [.30, .85, .35, .50], [.40, .45, .35, .35], [.75, .40, .45, .30]],
  EP045: [[.40, .45, .30, .25], [.35, .40, .30, .35], [.30, .25, .35, .25], [.35, .45, .55, .35]],
  EP046: [[.35, .30, .35, .60], [.35, .35, .40, .70], [.45, .45, .30, .55], [.35, .25, .65, .50]],
  EP047: [[.25, .45, .35, .40], [.25, .60, .35, .30], [.30, .35, .30, .40], [.35, .30, .25, .30]],
  EP048: [[.25, .30, .40, .35], [.25, .50, .40, .35], [.35, .30, .30, .35], [.30, .30, .35, .30]],
  EP049: [[.25, .40, .35, .35], [.25, .25, .25, .30], [.35, .35, .25, .25], [.30, .30, .30, .40]],
  EP050: [[.30, .40, .35, .35], [1.30, .35, .30, .30], [.40, .35, .30, .35], [.30, .40, 1.35, .45]],
};

const effects = {
  'EP044/1/4': {
    composition: '侧面只见二楼阳台上唯一炮台和原栏杆，院外保持虚景。',
    camera: '固定侧面机位，设备仍处于等待；不追向院外，不展示操作。',
    action: '设备外壳只做一次短暂轻响，尚未开火。白棠的声音从控制室内线接进来。',
  },
  'EP044/2/2': {
    size: '阳台设备外壳近景',
    composition: '唯一炮台的外部轮廓与栏杆同框；不看供弹机构，也不切向墙外人物。',
    camera: '固定侧面，震动只在声音最响的一刻出现，随即回到完全静止。',
    action: '短促响声从阳台传来，门外的撞击也断掉。声音收住，设备外壳恢复静止，白棠从控制室确认弹药已经用完。',
    sound: '<一阵短促的剧情音效迅速消失，最后只剩院外风声>',
  },
  'EP044/2/4': {
    action: '停火后，冬狼从废车边站直。他朝后方摆手叫停，独自向关着的外门走。远处背影不跟到门前。',
    camera: '保持雪坡侧面，跟两步后停住，以冬狼走向门的背侧轮廓收束。',
    sound: '<靴底踩雪；枪声已经停，不用回放>',
  },
  'EP044/4/1': {
    action: '接上一段雪地已经结冰的画面。半透明霜层遮住冬狼轮廓，轮廓失去平衡倒到门外雪地，不再活动。后景余众后退，黑门始终关着。只用虚构异能特效，不拍伤口、面部或身体细节。',
  },
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
    if (end <= start || speechEnd > end - 5 || !lens_mm || !position || !focus || !transition) {
      throw new Error(`Invalid shot/speech timing ${ep}/${index + 1}/${i + 1}: ${start}-${end}, ${speechStart}-${speechEnd}`);
    }
    const out = { ...shot, time: [start, end], speech_window: [speechStart, speechEnd], lens_mm, position, focus, transition };
    start = end;
    return out;
  });
  if (start !== 1500) throw new Error(`Incomplete 15-second timeline: ${ep}/${index + 1}`);
  const speakers = [...new Set(shots.map(s => s.speaker))];
  const lines = [
    `16:9横屏，15秒，4个实际镜头，480p，有声音，真人电影实拍质感。${ep} Segment ${index + 1}《${segment.title}》，全片${index * 15}–${(index + 1) * 15}秒。`,
    '以下为段内0–15秒的导演预排。对白窗口是估算，拍摄时允许在本镜内微调，不加速抢词，不重念上一段的台词。', '',
    '参考输入与人物', '',
    ...refs.references.map(r => r.uri
      ? `参考图${r.number}：${r.name}，数字人身份锁=${r.uri}；${r.description}`
      : `参考图${r.number}：${r.label}；${r.scope.replace('；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果', '')}。`),
    `清晰出镜仅${segment.cast.join('、')}。${segment.offscreen.length ? `${segment.offscreen.join('、')}只发声、不露脸。` : ''}一镜最多两张清晰脸；只为明确入镜者锁脸。`,
    ...segment.offscreen.filter(n => roles[n]).map(n => `只有画面明确出现${n}的手、袖口或肩背时，按其原定装入画：${roles[n].description.split('。')[0]}。不补头部与正脸。`),
    '前后状态只由文字和剪辑承接；不传首尾帧，不从参考图直接拼贴成画面。', '',
    '空间、光线与道具', `本段场面：${space}`, `时间：${segment.time}。`, building,
    '以已有参考确定相对位置，景深服务动作；冬雪用冷灰自然光，室内沿用功能灯，不改变真人写实质感。道具受力、通电、成品与物资数量按本镜阶段。', '',
    '起点与终点', `起点：${segment.opening}`, `终点：${segment.ending}`, '',
    `声音角色：${speakers.map(n => `${n}为${voices[n]}`).join('；')}。音乐只留极轻底层，动作声、对讲和对白先后清楚。`, '',
    '逐镜导演设计', '',
  ];
  for (const [i, shot] of shots.entries()) {
    const faces = shot.faces.map(n => `${n}（参考图${refs.references.find(r => r.name === n).number}）`);
    const mode = shot.mode === 'voiceover' ? '画外音' : '现场对白';
    const lips = shot.mode === 'voiceover' ? `仅${shot.speaker}发画外音，镜内人物不补口型。` : `仅${shot.speaker}开口，其他人闭嘴用目光或动作回应。`;
    lines.push(`镜头${nums[i]}｜${shot.title}`, `段内时码：${shot.time.map(fmt).join('–')}秒`,
      `景别：全画幅等效${shot.lens_mm}mm，${shot.size}。`,
      `构图：${shot.position}。${shot.composition}`,
      `运镜手法：${shot.camera}`,
      `焦点与景深：${shot.focus}。`,
      `画面内容：${shot.action}`,
      `表演：${shot.delivery}`,
      `人物与参考绑定：${faces.length ? `清晰露脸仅${faces.join('、')}，其余只按正文出现局部` : '本镜不出现清晰人脸'}。`,
        `声画窗口：${shot.speech_window.map(fmt).join('–')}秒，${mode}。${ep === 'EP045' && index === 0 && i === 3 ? '前后两句之间留一次完整试推。' : ''}说话者绑定：${lips}`,
      `${shot.speaker}台词${shot.mode === 'voiceover' ? '（画外音）' : ''}：{${shot.dialogue}}`,
      `声音：${shot.sound}`,
      `镜头衔接：${shot.transition}。`, '');
  }
  lines.push(`跨段交接：${segment.bridge}`,
    '禁止：字幕、解释字卡、可读界面文字、坐标、水印。不能增人、替换脸或服装、重造别墅和道具。', '');
  return { revision: directorRevision, text: lines.join('\n'), shots };
}
