export const ep044ReferenceRevision = '2026-11-23-ep044-team-fight-v6';

const archive = 'docs/revisions/2026-11-12-pre-15s/episodes/EP044_afterglow';
const keyframes = 'assets/production/ep044-named-references';
const turnarounds = {
  许砚: `${archive}/segment_01_00-30s/frames/参考图01_人物三视图_许砚.png`,
  白棠: `${archive}/segment_01_00-30s/frames/参考图02_人物三视图_白棠.png`,
  冬狼: `${archive}/segment_02_30-60s/frames/参考图02_人物三视图_冬狼.png`,
  叶凝霜: `${archive}/segment_02_30-60s/frames/参考图01_人物三视图_叶凝霜.png`,
  沈知夏: `${archive}/segment_01_00-30s/frames/参考图04_人物三视图_沈知夏.png`,
};

const scene = (key, label, scope, shots) => ({ key, label, scope, shots, kind: 'scene_or_prop' });
const keyframe = (name, label, scope, shot) => ({
  key: name, label, scope, shots: [shot], kind: 'action_keyframe',
  file: `${keyframes}/${name}-16x9.png`, status: 'imagegen_visually_checked',
});
const villa = (...shots) => scene('villa', '场景雪中别墅', '只锁同一栋现代三层别墅、阳台、围墙及黑门相对位置，不复制画中机位', shots);
const gate = (...shots) => scene('gate', '场景闭合黑门', '只锁同一扇双扇黑门、灰墙和门柱位置；门全程闭合，不能从图中继承完好锁座', shots);

const backgroundsAndKeyframes = {
  'segment_01_00-15s': [
    villa('L01'),
    scene('control', '场景别墅控制室', '只锁控制台、屏幕和房间格局，屏幕内容按本镜重绘', ['L04']),
    keyframe('gate-held-shut', '关键帧护臂抵门', '只参考院内护臂抵门与受撞但仍扣住的锁座，不锁人物脸，不把门拍开', 'L02'),
  ],
  'segment_02_15-30s': [
    scene('control', '场景别墅控制室', '只锁控制台与屏幕边框；屏内人物只为远景无脸轮廓', ['L02']),
    scene('turret', '道具唯一阳台炮台', '只参考外壳形状，仍在原二楼阳台，不复制第二座，不展示内部', ['L01']),
    keyframe('brace-overheat', '关键帧护臂过热', '只参考同一护臂、外门和单枚暖色过热灯；警示亮后护臂下沉，知夏让它重新撑住，不复刻静态姿势', 'L03'),
  ],
  'segment_03_30-45s': [
    gate('L01', 'L02', 'L03', 'L04'),
    keyframe('boots-frozen-gate', '关键帧门外雪靴结冰', '只用于门外靴边浅冰；冰只到脚踝，不提前封住身体，也不让凝霜出院', 'L03'),
  ],
  'segment_04_45-60s': [
    gate('L01', 'L02'),
    villa('L04'),
    keyframe('ice-outside-closed-gate', '关键帧冰体倒在门外', '只锁L01倒下后的半透明无脸冰体、扬雪和门外位置；开镜从脚踝起冰，不定格、不复制这张图的结束姿势到院内', 'L01'),
  ],
};

export function ep044LocalReferences(master, segment) {
  const portraits = segment.cast.map(name => ({
    key: `turnaround_${name}`, name, label: `人物三视图_${name}`, kind: 'character_turnaround',
    file: turnarounds[name], scope: `正侧背只参考${name}的冬装、发型和体态；本人容貌以对应数字人为准，不生成并排人影`,
    shots: segment.shots.flatMap((s, i) => s.faces.includes(name) ? [`L0${i + 1}`] : []),
    status: 'existing_turnaround_visually_checked',
  }));
  const production = backgroundsAndKeyframes[segment.directory].map(ref => ({
    ...ref, file: ref.file || master.assets[ref.key].file,
    status: ref.status || 'existing_scene_or_prop_visually_checked',
  }));
  return [...portraits, ...production];
}
