import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { episodes as oldMetadata } from './ep044-050-seedance25-plan.mjs';
import { revision, directories, timelines, additions, layouts, languageEvidence } from './ep044-050-15s-layout.mjs';
import { directorRevision } from './ep044-050-camera-plan.mjs';
import { renderDirector } from './render_ep044_050_director.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const oldDirs = ['segment_01_00-30s', 'segment_02_30-60s'];
const archive = 'docs/revisions/2026-11-12-pre-15s';
const masterFile = 'scripts/ep044-050-15s-plan.json';
const absolute = file => path.join(root, file);
const read = file => fs.readFileSync(absolute(file), 'utf8');
const readJson = file => JSON.parse(read(file));
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const count = text => (text.match(/[\p{Script=Han}\p{N}]/gu) || []).length;
const write = (file, text) => {
  fs.mkdirSync(path.dirname(absolute(file)), { recursive: true });
  fs.writeFileSync(absolute(file), text);
};
const writeJson = (file, value) => write(file, `${JSON.stringify(value, null, 2)}\n`);
const table = text => String(text).replaceAll('|', '／').replaceAll('\n', ' ');
const model = 'doubao-seedance-2-5-260628';
const voices = { 许砚: '成年男性中低声，平稳清楚，临战果断', 白棠: '成年女性自然中声，利落，情绪有起伏但不尖叫',
  沈知夏: '成年女性偏低声，成熟克制，与白棠音色区分', 叶凝霜: '成年女性清冷中低声，稳，不甜腻',
  冬狼: '成年男性偏低声，命令口吻，受困后才提高音量', 泵房住户: '门柱对讲中的成年男性声音，礼貌拘谨，有轻微通道底噪' };
const building = '同一栋现代三层主楼、连续阳台、灰色高围墙、黑色双扇外门和墙顶电网；屋顶与建筑比例服从既定别墅参考。唯一炮台仍在二楼阳台，EP044打空后不凭空补弹。温室、禽舍、鱼池、能源棚均在围墙内，主路塌方未恢复。';

function writeDirectorFiles(dir, episode, segment, index, director, roles) {
  const formatWindow = times => times.map(t => t / 100).join('–');
  const rows = director.shots.map((shot, i) => {
    const speaker = `${shot.speaker}${shot.mode === 'voiceover' ? '（画外音）' : ''}`;
    return `| ${i + 1} ${table(shot.title)} | ${formatWindow(shot.time)} | ${shot.lens_mm}mm；${table(shot.size)} | ${table(shot.position)}；${table(shot.composition)} | ${table(shot.camera)}；${table(shot.focus)} | ${table(shot.action)} | ${formatWindow(shot.speech_window)}：${speaker}：${table(shot.dialogue)}；${table(shot.sound)} | ${table(shot.transition)} |`;
  });
  write(`${dir}/director-promt.txt`, director.text);
  write(`${dir}/prompt.md`, director.text);
  writeJson(`${dir}/storyboard-source.json`, { revision, director_revision: directorRevision, episode, segment: segment.directory, ...segment, shots: director.shots });
  write(`${dir}/storyboard.md`, `# ${episode.slice(0, 5)} Segment ${index + 1}：${segment.title}\n\n导演版本：${directorRevision}。15秒、四镜、16:9真人。时码与对白窗口为预排，不是实测。\n\n首状态：${segment.opening}\n\n尾状态：${segment.ending}\n\n清晰人物及完整服装：\n${segment.cast.map(n => `- ${n}：${roles[n].description}`).join('\n')}\n\n| 镜头 | 段内秒 | 焦段及景别 | 机位与构图 | 运镜及焦点 | 动作 | 对白窗口与声音 | 剪辑衔接 |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n${rows.join('\n')}\n\n跨段衔接：${segment.bridge}\n`);
}

function outputInventory() {
  const files = [];
  function walk(dir) {
    if (!fs.existsSync(absolute(dir))) return;
    for (const item of fs.readdirSync(absolute(dir), { withFileTypes: true })) {
      const file = `${dir}/${item.name}`;
      if (item.isDirectory()) walk(file);
      else {
        const stat = fs.statSync(absolute(file));
        files.push({ file, bytes: stat.size, mtime: stat.mtimeMs });
      }
    }
  }
  for (const e of oldMetadata) for (const dir of oldDirs) walk(`episodes/${e.dir}/${dir}/output`);
  return files;
}

function captureSource() {
  const snapshotFile = `${archive}/source.json`;
  if (fs.existsSync(absolute(snapshotFile))) return readJson(snapshotFile);
  const source = { captured: '2026-11-12', revision, episodes: [], roles: {}, assets: {}, outputs: outputInventory() };
  for (const e of oldMetadata) {
    const entry = { ...e, sources: [] };
    for (const directory of oldDirs) {
      const base = `episodes/${e.dir}/${directory}`;
      const shotSource = readJson(`${base}/storyboard-source.json`);
      const prompt = read(`${base}/director-promt.txt`);
      const references = readJson(`${base}/reference-assets.json`);
      if (prompt !== read(`${base}/prompt.md`)) throw new Error(`Prompt copies disagree: ${base}`);
      if (!shotSource.shots.every(s => prompt.includes(`{${s.dialogue}}`))) throw new Error(`Shot source is stale: ${base}`);
      const sounds = [...prompt.matchAll(/^声音：(<.+>)$/gm)].map(m => m[1]);
      if (sounds.length !== 8 || shotSource.shots.length !== 8) throw new Error(`Expected eight source shots: ${base}`);
      for (const ref of references.references) {
        if (ref.kind === 'digital_human') {
          const line = prompt.split('\n').find(l => l.startsWith(`参考图${ref.number}：${ref.name}，`));
          if (!line) throw new Error(`Missing role description: ${ref.name}`);
          const description = line.slice(line.indexOf('；') + 1);
          source.roles[ref.name] = { name: ref.name, asset: ref.asset, uri: ref.uri, description };
        } else {
          const key = ref.key === 'clean_detail' ? path.basename(ref.file).replace(/-16x9\.png$/, '') : ref.key;
          source.assets[key] = { ...ref, key };
        }
      }
      entry.sources.push({ directory, shotSource, references, prompt_sha256: sha(prompt), sounds });
    }
    source.episodes.push(entry);
  }
  for (const [key, asset] of Object.entries(additions)) source.assets[key] = { ...asset, key, kind: 'scene_or_prop', status: 'existing_candidate_pending_new_shot_review' };
  writeJson(snapshotFile, source);
  return source;
}

function makeMaster(source) {
  return {
    revision, format: { episode_duration: 60, segments: 4, segment_duration: 15, shots_per_segment: 4,
      ratio: '16:9', resolution: '480p', generate_audio: true, first_last_frames: false, model },
    source_snapshot: `${archive}/source.json`, roles: source.roles, assets: source.assets,
    episodes: source.episodes.map((e, ei) => ({ ...Object.fromEntries(Object.entries(e).filter(([k]) => !['sources', 'segments'].includes(k))),
      language_evidence: languageEvidence[ei],
      segments: layouts[ei].map(([title, faces, refs, opening, ending, bridge], si) => {
        const sourceSegment = e.sources[Math.floor(si / 2)];
        const offset = (si % 2) * 4;
        const shots = structuredClone(sourceSegment.shotSource.shots.slice(offset, offset + 4));
        shots.forEach((s, i) => { s.faces = faces[i]; s.sound = sourceSegment.sounds[offset + i]; s.source_shot = offset + i + 1; });
        const cast = [...new Set(faces.flat())];
        const offscreen = [...new Set(shots.filter(s => !cast.includes(s.speaker)).map(s => s.speaker))];
        return { title, directory: directories[si], duration: 15, time: sourceSegment.shotSource.time,
          source_segment: sourceSegment.directory, source_shots: [offset + 1, offset + 4],
          cast, offscreen, refs, opening, ending, bridge, shots };
      }) })) };
}

function referencesFor(master, e, segment) {
  const refs = segment.cast.map(name => ({ ...master.roles[name], kind: 'digital_human', label: name,
    scope: '只锁本人身份与脸；基础服装和发型服从本段完整描述', status: 'user_registered_identity' }));
  for (const key of segment.refs) {
    const candidate = master.assets[key];
    if (!candidate?.file || !fs.existsSync(absolute(candidate.file))) throw new Error(`Missing ${e.dir}/${segment.directory}: ${key}`);
    const ref = structuredClone(candidate);
    delete ref.number;
    delete ref.segment_file;
    ref.scope += '；只取外观与对应局部，破损、成熟程度、通电和物资数量严格按本镜，不能提前套用后期结果';
    if (key === 'filmCards' && segment.directory === directories[3]) ref.scope = '只锁单卷膜材的材质与宽度；本段不再显示手机卡片，不再次抽卡，不复制便携灯或未知奖励';
    if (key === 'wolfFrozen' && segment.directory === directories[2]) ref.scope = '只锁冬狼靴边的冰层材质；本段只冻住双脚，不提前封住全身或倒地，不从图中生成另一张脸';
    if (key === 'spareTray') ref.scope += '；EP047换件后盒里必须为空，EP048空盒状态继续承接，不能恢复一只备用件';
    if (key === 'coopCold') ref.scope = '只锁原金属禽舍、原银色饮水器结构；时令必须冬雪，不能复制原夏季绿树林；冻结或解冻按本镜';
    if (key === 'gateRepair') ref.scope += '；只有一块新外侧护板，不能每扇门各一块';
    if (key === 'firstEgg') ref.scope += '；发现和带回的鸡蛋都只有一枚，不能加第二枚';
    refs.push(ref);
  }
  refs.forEach((r, i) => { r.number = i + 1; if (r.kind !== 'digital_human') r.segment_file = `frames/参考图${i + 1}.png`; });
  if (refs.length !== 9 || new Set(refs.map(r => r.file || r.uri)).size !== 9) throw new Error(`Need nine distinct inputs: ${e.dir} ${segment.title}`);
  return { revision, numbering: 'exact_api_image_order_including_digital_humans', first_last_frames: false,
    digital_humans: segment.cast.map(name => ({ name, asset: master.roles[name].asset })),
    api_submission: { status: 'needs_visual_review', model, duration: 15, ratio: '16:9', resolution: '480p',
      generate_audio: true, max_total_images: 9, planned_total_images: 9, auto_images: false,
      local_reference_files_complete: true, note: '九项为本项目规划，不代表已验证模型上限或账号权限。仅按清单取图，不扫描历史目录，不传首尾帧，尚未提交。' },
    references: refs, exclusions: ['不上传未出场角色', '不上传旧三视图、旧关键帧或历史output', '不把本地文件存在视为视频人物一致性通过'] };
}

function validateMaster(master) {
  if (master.episodes.length !== 7) throw new Error('Expected seven episodes');
  for (const e of master.episodes) {
    if (e.segments.length !== 4) throw new Error(`Wrong segment count: ${e.dir}`);
    for (const [i, s] of e.segments.entries()) {
      if (s.directory !== directories[i] || s.duration !== 15 || s.shots.length !== 4 || s.cast.length > 3) throw new Error(`Wrong layout: ${e.dir} ${i}`);
      if (count(s.shots.map(x => x.dialogue).join('')) > 55) throw new Error(`Speech overload: ${e.dir} ${i}`);
      for (const shot of s.shots) {
        if (!shot.dialogue.trim() || shot.faces.length > 2 || shot.faces.some(n => !s.cast.includes(n))) throw new Error(`Invalid faces/dialogue: ${shot.title}`);
        if (shot.mode === 'onscreen' && !shot.faces.includes(shot.speaker)) throw new Error(`Unbound speaker: ${shot.title}`);
      }
      referencesFor(master, e, s);
    }
  }
}

function archiveOld(source) {
  for (const e of source.episodes) {
    const episodeDir = `episodes/${e.dir}`;
    for (const name of ['episode.md', 'overview-storyboard.md', 'dialogue-readthrough.md', 'continuity.md', 'image-manifest.md', 'qa-checklist.md', 'publish-package.md']) {
      const dest = `${archive}/${episodeDir}/${name}`;
      if (fs.existsSync(absolute(`${episodeDir}/${name}`)) && !fs.existsSync(absolute(dest))) {
        fs.mkdirSync(path.dirname(absolute(dest)), { recursive: true });
        fs.copyFileSync(absolute(`${episodeDir}/${name}`), absolute(dest));
      }
    }
    for (const s of e.sources) {
      const dir = `${episodeDir}/${s.directory}`;
      if (!fs.existsSync(absolute(`${dir}/director-promt.txt`))) continue;
      if (sha(read(`${dir}/director-promt.txt`)) !== s.prompt_sha256) throw new Error(`Source changed since capture: ${dir}`);
      const dest = `${archive}/${dir}`;
      fs.mkdirSync(absolute(dest), { recursive: true });
      for (const item of fs.readdirSync(absolute(dir))) {
        if (item === 'output' || item === 'ARCHIVED.md') continue;
        if (fs.existsSync(absolute(`${dest}/${item}`))) throw new Error(`Archive collision: ${dest}/${item}`);
        fs.renameSync(absolute(`${dir}/${item}`), absolute(`${dest}/${item}`));
      }
      write(`${dir}/ARCHIVED.md`, `# 历史30秒任务目录\n\n此段不再制作。提示词、故事板与frames已归档至story根目录下${dest}。\n本目录output历史视频和任务记录原路径保留，不移动、不覆盖。\n当前使用本集production-manifest.json列出的四个15秒目录。\n`);
    }
  }
}

const source = captureSource();
if (!fs.existsSync(absolute(masterFile))) writeJson(masterFile, makeMaster(source));
const master = readJson(masterFile);
master.episodes.forEach((e, ei) => e.segments.forEach((s, si) => { s.time = timelines[ei][si]; }));
validateMaster(master);
const checkOnly = process.argv.includes('--check');
const promptsOnly = process.argv.includes('--prompts-only');
if (checkOnly && promptsOnly) throw new Error('Choose either --check or --prompts-only');
const render = (e, s, si, refs) => renderDirector(e.dir, s, si, refs, master.roles, voices, building);

if (promptsOnly) {
  // Validate every current input before changing the first file.
  const pending = master.episodes.flatMap(e => e.segments.map((s, si) => {
    const dir = `episodes/${e.dir}/${s.directory}`;
    const refs = readJson(`${dir}/reference-assets.json`);
    const handoff = readJson(`${dir}/seedance25-handoff.json`);
    const inputOrder = refs.references.map(r => [r.number, r.uri || r.file]);
    if (JSON.stringify(inputOrder) !== JSON.stringify(referencesFor(master, e, s).references.map(r => [r.number, r.uri || r.file]))) throw new Error(`Reference order drift: ${dir}`);
    const oldPrompt = read(`${dir}/director-promt.txt`);
    const api = read(`${dir}/api-request.md`);
    if (oldPrompt !== read(`${dir}/prompt.md`) || sha(oldPrompt) !== handoff.prompt_sha256 ||
        !api.includes(`SHA256=${handoff.prompt_sha256}`) || handoff.submitted) throw new Error(`Prompt or handoff drift: ${dir}`);
    const currentShots = readJson(`${dir}/storyboard-source.json`).shots;
    if (JSON.stringify(currentShots.map(x => [x.speaker, x.mode, x.dialogue])) !== JSON.stringify(s.shots.map(x => [x.speaker, x.mode, x.dialogue]))) {
      throw new Error(`Dialogue source drift: ${dir}`);
    }
    return { e, s, si, dir, api, handoff, director: render(e, s, si, refs) };
  }));
  const hashes = new Map();
  for (const { e, s, si, dir, api, handoff, director } of pending) {
    const hash = sha(director.text);
    writeDirectorFiles(dir, e.dir, s, si, director, master.roles);
    write(`${dir}/api-request.md`, api
      .replace(`SHA256=${handoff.prompt_sha256}`, `SHA256=${hash}`)
      .replace(/^版本：.*$/m, `版本：${revision}。导演稿：${directorRevision}；时码为文字预排，未生成视频。`));
    writeJson(`${dir}/seedance25-handoff.json`, { ...handoff, director_revision: directorRevision, prompt_sha256: hash });
    hashes.set(`${e.dir}/${s.directory}`, hash);
  }
  for (const file of ['docs/ep044-050-15s-validation.json', 'docs/ep044-050-seedance25-validation.json', 'docs/ep041-050-rewrite-validation.json']) {
    const report = readJson(file);
    for (const item of report.segments_detail) {
      const hash = hashes.get(`${item.episode}/${item.segment}`);
      if (hash) Object.assign(item, { director_revision: directorRevision, prompt_sha256: hash });
    }
    writeJson(file, report);
  }
} else if (!checkOnly) {
  writeJson(masterFile, master);
  archiveOld(source);
  const checks = [], allReadthrough = [], outline = [], uses = new Map();
  for (const e of master.episodes) {
    const ep = `episodes/${e.dir}`;
    const episodeRows = [], summaries = [], continuity = [], imageSections = [], readthrough = [];
    for (const [si, s] of e.segments.entries()) {
      const dir = `${ep}/${s.directory}`, refs = referencesFor(master, e, s);
      const spoken = count(s.shots.map(x => x.dialogue).join(''));
      const director = render(e, s, si, refs);
      const hash = sha(director.text);
      for (const [i, shot] of director.shots.entries()) {
        const who = `${shot.speaker}${shot.mode === 'voiceover' ? '（画外音）' : ''}`;
        episodeRows.push(`| ${si + 1} | ${i + 1} | ${who} | ${table(shot.dialogue)} |`);
      }
      writeDirectorFiles(dir, e.dir, s, si, director, master.roles);
      write(`${dir}/dialogue.txt`, `${s.shots.map((x, i) => `${i + 1}. ${x.speaker}${x.mode === 'voiceover' ? '（画外音）' : ''}：${x.dialogue}`).join('\n')}\n`);
      write(`${dir}/first-frame.md`, `# 首状态（不生首帧、不上传）\n\n${s.opening}\n\n首镜：${s.shots[0].size}；${s.shots[0].composition}\n\n仅文字连续性记录；不能据此传旧视频帧。\n`);
      write(`${dir}/last-frame.md`, `# 尾状态（不生尾帧、不上传）\n\n${s.ending}\n\n衔接：${s.bridge}\n\n末镜：${s.shots[3].size}；${s.shots[3].composition}\n`);
      writeJson(`${dir}/reference-assets.json`, refs);
      for (const ref of refs.references.filter(r => r.file)) {
        fs.mkdirSync(absolute(`${dir}/frames`), { recursive: true });
        fs.copyFileSync(absolute(ref.file), absolute(`${dir}/${ref.segment_file}`));
        const entries = uses.get(ref.file) || [];
        entries.push({ episode: e.dir, segment: s.directory, reference_number: ref.number }); uses.set(ref.file, entries);
      }
      writeJson(`${dir}/frames/reference-manifest.json`, { revision, source: '../reference-assets.json', first_last_frames: false,
        references: refs.references.map(r => ({ number: r.number, label: r.label, kind: r.kind, file: r.segment_file ? path.basename(r.segment_file) : null, uri: r.uri || null })) });
      write(`${dir}/frames/参考图顺序.md`, `# 本段实际输入顺序\n\n数字人通过asset URI提供，没有对应本地PNG；其余文件按同一编号命名。只按清单上传，不遍历目录。\n\n${refs.references.map(r => `${r.number}：${r.label} → ${r.uri || path.basename(r.segment_file)}`).join('\n')}\n\n原30秒段的三视图和关键帧均不进入本段。\n`);
      const imageTable = refs.references.map(r => `| ${r.number} | ${r.label} | ${r.uri || r.file} | ${table(r.scope)} |`).join('\n');
      write(`${dir}/api-request.md`, `# ${e.dir.slice(0, 5)} Segment ${si + 1} 视频交接\n\n版本：${revision}。这是重做后的15秒段，没有提交视频。\n\n- model=${model}（沿用既定目标；本次未验证账号或服务端参数）。\n- duration=15，ratio=16:9，resolution=480p，generate_audio=true。\n- prompt_file=director-promt.txt；SHA256=${hash}；prompt.md逐字一致。\n- first_frame=null，last_frame=null，auto_images=false。\n- 台词${spoken}个有效字；4字/秒粗估${spoken / 4}秒，非实测语音。\n- 只按reference-assets.json上传具名数字人和图片；九项包括人物，无旧首尾帧。\n- 整集四段串行，前一段完成、下载并验收后再提交下一段；发现问题停止，不自动重试。\n\n| 实际输入序号 | 标签 | story根目录来源或asset URI | 职责 |\n| --- | --- | --- | --- |\n${imageTable}\n\n本地文件齐全不代表身份、服装、动作或语音已通过生成验证。正式提交前核对实际payload的角色名、URI、图片标签、编号和prompt哈希。任务ID：无。\n`);
      writeJson(`${dir}/seedance25-handoff.json`, { revision, director_revision: directorRevision, submitted: false, model, duration: 15, ratio: '16:9', resolution: '480p',
        generate_audio: true, prompt_file: 'director-promt.txt', prompt_sha256: hash, first_frame: null, last_frame: null,
        auto_images: false, references_file: 'reference-assets.json', readiness: 'needs_visual_review', missing_reference_numbers: [],
        sequence: si + 1, previous_segment: si ? directories[si - 1] : null, generation_policy: 'sequential_wait_download_review_stop_on_error' });
      write(`${dir}/asset-image-prompts.md`, `# 本段资产引用\n\n本次拆段不新增图像内容，沿用已经生成的场景与道具；缺图0张。人物只用数字人URI。\n原生图记录见assets/production/ep044-050-seedance25/generation-record.json；不把它当成本次新生图记录。\n\n${refs.references.filter(r => r.file).map(r => `## 参考图${r.number}：${r.label}\n\n资产：${r.file}\n\n本段副本：${r.segment_file}\n\n用途：${r.scope}\n\n状态：${r.status}；拆段后的使用时点仍须在实际视频生成前复核。`).join('\n\n')}\n`);
      fs.mkdirSync(absolute(`${dir}/output`), { recursive: true });
      write(`${dir}/output/README.md`, '# 本段输出\n\n尚未提交视频；本目录只接收本段15秒任务结果。旧30秒视频不搬到这里，不冒充新成片。\n');
      summaries.push(`| ${si + 1} | ${si * 15}-${(si + 1) * 15}s | ${s.title} | ${table(s.opening)} | ${table(s.ending)} | ${spoken} |`);
      readthrough.push(`## Segment ${si + 1}：${s.title}\n\n${s.shots.map((x, i) => `${i + 1}. ${x.speaker}${x.mode === 'voiceover' ? '（画外音）' : ''}：${x.dialogue}`).join('\n')}\n`);
      continuity.push(`## Segment ${si + 1}\n\n清晰人物：${s.cast.join('、')}。仅声音：${s.offscreen.join('、') || '无'}。\n\n开始：${s.opening}\n\n结束：${s.ending}\n\n衔接：${s.bridge}\n`);
      imageSections.push(`## Segment ${si + 1}：${s.title}\n\n数字人${s.cast.length}项＋本地图${9 - s.cast.length}张＝9项，无缺失。\n\n| 输入 | 标签 | 来源 | 职责 |\n| --- | --- | --- | --- |\n${imageTable}\n`);
      checks.push({ episode: e.dir, segment: s.directory, director_revision: directorRevision, title: s.title, duration: 15, shots: 4, visible_cast: s.cast, offscreen: s.offscreen,
        dialogue_chars: spoken, estimated_speech_seconds_at_4cps: spoken / 4, prompt_sha256: hash, prompt_copy_equal: true,
        planned_references: 9, local_images: 9 - s.cast.length, missing_reference_numbers: [], submission_status: 'needs_visual_review',
        video_submitted: false, video_reviewed: false });
    }
    write(`${ep}/episode.md`, `# ${e.dir.slice(0, 5)}：${e.title}\n\n版本：${revision}。60秒＝四段15秒，每段四镜；16:9、真人、有声音。\n\n## 上集承接\n${e.premise}\n\n## 人物目标\n${e.want}\n\n## 转折与回报\n${e.turn}\n\n${e.payoff}\n\n## 四段推进\n| 段 | 时长 | 本段任务 | 开始 | 结束 | 台词字数 |\n| --- | --- | --- | --- | --- | --- |\n${summaries.join('\n')}\n\n## 完整对白\n| 段 | 镜头 | 发声者 | 台词 |\n| --- | --- | --- | --- |\n${episodeRows.join('\n')}\n\n## 资源承接\n${e.resource.map(x => `- ${x}`).join('\n')}\n\n## 下一集\n${e.hook}\n\n重做仅调整拆段、镜头衔接和参考输入；既有16镜对白保留，原视频不移动、不覆盖。\n`);
    const speechDoc = `# ${e.dir.slice(0, 5)} 台词通读：${e.title}\n\n版本：${revision}。四段连续读，不在段头重念上一句。\n\n${readthrough.join('\n')}\n`;
    write(`${ep}/dialogue-readthrough.md`, speechDoc); allReadthrough.push(speechDoc);
    write(`${ep}/overview-storyboard.md`, `# ${e.dir.slice(0, 5)} 四段总览\n\n版本：${revision}\n\n| 段 | 时长 | 任务 | 开始 | 结束 | 台词字数 |\n| --- | --- | --- | --- | --- | --- |\n${summaries.join('\n')}\n`);
    write(`${ep}/continuity.md`, `# ${e.dir.slice(0, 5)} 连续性\n\n版本：${revision}。${e.time}\n\n${building}\n\n承接：${e.premise}\n\n${continuity.join('\n')}\n## 资源不可回退\n${e.resource.map(x => `- ${x}`).join('\n')}\n\n下一集：${e.hook}\n`);
    write(`${ep}/image-manifest.md`, `# ${e.dir.slice(0, 5)} 当前15秒段资产清单\n\n版本：${revision}。按本集production-manifest.json选段，数字人计入每段九项。场景图都在各段frames，不传旧首尾帧。\n\n${imageSections.join('\n')}\n`);
    writeJson(`${ep}/production-manifest.json`, { revision, active: true, episode_duration: 60, segment_duration: 15,
      segments: e.segments.map((s, i) => ({ sequence: i + 1, directory: s.directory, duration: 15, shots: 4 })),
      historical_30s_text: `${archive}/${ep}`, historical_outputs_unchanged: oldDirs.map(d => `${d}/output`),
      source_plan: masterFile, first_last_frames: false });
    const evidence = e.language_evidence;
    const languageRows = [
      ['L01', '反复顿悟', '对白按看见、决定、行动和回应顺序推进，没有反复宣布领悟。'],
      ['L02', '对照说教', evidence[1]], ['L03', '金句升华', evidence[2]],
      ['L04', '创作约束外露', '数字人、模型限制与分段约束只写导演制作区，不进入角色实际发声。'],
      ['L05', '硬拗幽默', evidence[2]], ['L06', '空泛汇报与悬念占位', evidence[0]],
      ['S01', '开场冲突', evidence[0]], ['S02', '目标与代价', evidence[1]],
      ['S03', '主动选择', `${e.want}；${e.turn}`], ['S04', '因果', evidence[1]],
      ['S05', '题材兑现', e.payoff], ['S06', '推进与具体结果', e.hook],
    ];
    write(`${ep}/qa-checklist.md`, `# ${e.dir.slice(0, 5)} 制作与文案检查\n\n稿件版本：${revision}；范围：整集16镜对白、段落衔接与动作。沿用拆段前112句中的本集16句，不改对白，审读不由关键词扫描代替。\n\n## 本地结构\n- [x] 四段各15秒、各四镜，每镜一句具名发声；不强行四等分镜长。\n- [x] 每段最多三张清晰脸、每镜最多两张；数字人按首次露脸排序，声音角色单列。\n- [x] director-promt与prompt一致；故事板、台词表、输入顺序一致。\n- [x] 每段九项含数字人，本地图已按号复制，无首尾帧。\n- [x] 原30秒文字归档，旧output路径保持；没有生成新视频。\n\n## 文案逐句审读\n结论：PASS；未处理项：无。PASS只表示本次编辑审读，不代表用户认可或平台效果。\n\n| 项 | 检查 | 结果 | 复核证据 |\n| --- | --- | --- | --- |\n${languageRows.map(([id, label, note]) => `| ${id} | ${label} | PASS | ${table(note)} |`).join('\n')}\n\n修改记录：对白保留；本次新写每段开始/结束状态与跨段接法，人物发声顺序未调换。第一人称信息边界不适用于本剧多机位对话；各人物的判断仍只使用本镜或已听到的信息。\n\n## 未执行的制作验证\n- [ ] 实际账号模型、参数与付费请求dry-run。\n- [ ] 视频人物、服装、动作、切镜与口型。\n- [ ] 实际音频是否清楚、台词是否自然说完。\n\n台词时长仅按4字/秒估算，不是实际配音或视频时长证明。\n`);
    outline.push(`| ${e.dir.slice(0, 5)} | ${e.title} | ${e.segments.map(s => s.title).join(' → ')} | ${table(e.payoff)} |`);
  }
  const report = { revision, scope: 'EP044-EP050', episodes: 7, segments: 28, segment_duration: 15, episode_duration: 60,
    shots_per_segment: 4, total_shots: 112, dialogue_changed: false, unique_missing_reference_files: 0,
    reference_images_generated_this_run: 0, first_last_frames: false, video_submitted: false, video_reviewed: false,
    language_review: { version: revision, L01_L06: 'PASS', S01_S06: 'PASS', unresolved: [], method: 'editorial_readthrough_recorded_per_episode_not_keyword_scan' },
    segments_detail: checks };
  writeJson('docs/ep044-050-15s-validation.json', report);
  writeJson('docs/ep044-050-seedance25-validation.json', report);
  write('docs/ep044-050-seedance25-dialogue-readthrough.md', allReadthrough.join('\n\n'));
  write('docs/ep044-050-15s-outline.md', `# EP044–EP050 四段15秒版\n\n版本：${revision}。每集60秒、四段15秒、每段四镜。沿用现有剧情和对白，不自动提交图片或视频。\n\n| 集 | 集名 | 四段推进 | 本集结果 |\n| --- | --- | --- | --- |\n${outline.join('\n')}\n\n母版：${masterFile}；构建：scripts/build_ep044_050_15s.mjs。\n旧30秒文稿与frames：${archive}；历史视频仍在原output路径，不能当作新15秒结果。\n`);
  const outlineFile = 'docs/ep044-050-seedance25-outline.md';
  const priorOutline = read(outlineFile);
  if (!priorOutline.includes('当前制作分段：')) write(outlineFile, `${priorOutline}\n当前制作分段：2026-11-12起改为四段15秒，详见ep044-050-15s-outline.md；剧情表不变。\n`);
  writeJson('docs/ep044-050-production-format.json', { revision, ...master.format, active_directories: directories,
    source_plan: masterFile, builder: 'scripts/build_ep044_050_15s.mjs', validation: 'docs/ep044-050-15s-validation.json' });
  const assetFile = 'docs/ep044-050-seedance25-asset-plan.json';
  const assetPlan = readJson(assetFile);
  assetPlan.revision = revision;
  assetPlan.unique_missing_files = 0;
  assetPlan.images_generated_in_current_resegment_run = 0;
  for (const a of assetPlan.assets) a.used_by = uses.get(a.file || a.planned_file) || [];
  writeJson(assetFile, assetPlan);
  const legacyRead = 'docs/ep041-050-dialogue-readthrough.md';
  if (fs.existsSync(absolute(legacyRead))) {
    const text = read(legacyRead), boundary = text.search(/^# EP044\b/m);
    if (boundary >= 0) write(legacyRead, `${text.slice(0, boundary)}${allReadthrough.join('\n\n')}\n`);
  }
  const legacyValidation = 'docs/ep041-050-rewrite-validation.json';
  if (fs.existsSync(absolute(legacyValidation))) {
    const old = readJson(legacyValidation);
    old.segments_detail = [...old.segments_detail.filter(x => !/^EP0(44|45|46|47|48|49|50)_/.test(x.episode)), ...checks];
    old.note = 'EP041-EP043保留原记录；EP044-EP050以2026-11-12四段15秒记录为准。';
    writeJson(legacyValidation, old);
  }
}

const verification = { revision, director_revision: directorRevision, editorial_timing_only: true, segments: 0, shots: 0, digital_human_inputs: 0, local_reference_slots: 0,
  dialogue_min: Infinity, dialogue_max: 0, missing: [], errors: [], video_submitted: false };
for (const e of master.episodes) {
  const oldSpeech = source.episodes.find(x => x.dir === e.dir).sources.flatMap(x => x.shotSource.shots.map(s => s.dialogue));
  const newSpeech = e.segments.flatMap(s => s.shots.map(x => x.dialogue));
  if (JSON.stringify(oldSpeech) !== JSON.stringify(newSpeech)) verification.errors.push(`${e.dir}: dialogue changed`);
  for (const [si, s] of e.segments.entries()) {
    const dir = `episodes/${e.dir}/${s.directory}`, prompt = read(`${dir}/director-promt.txt`);
    const manifest = readJson(`${dir}/reference-assets.json`), handoff = readJson(`${dir}/seedance25-handoff.json`);
    const expected = render(e, s, si, manifest);
    verification.segments++; verification.shots += s.shots.length;
    const chars = count(s.shots.map(x => x.dialogue).join(''));
    verification.dialogue_min = Math.min(verification.dialogue_min, chars); verification.dialogue_max = Math.max(verification.dialogue_max, chars);
    if (prompt !== read(`${dir}/prompt.md`) || sha(prompt) !== handoff.prompt_sha256) verification.errors.push(`${dir}: hash/copy`);
    if (prompt !== expected.text || handoff.director_revision !== directorRevision ||
        !read(`${dir}/api-request.md`).includes(`SHA256=${handoff.prompt_sha256}`) ||
        JSON.stringify(readJson(`${dir}/storyboard-source.json`).shots) !== JSON.stringify(expected.shots)) verification.errors.push(`${dir}: timed director/storyboard drift`);
    if (!prompt.startsWith('16:9横屏，15秒，4个实际镜头') || [...prompt.matchAll(/^镜头[一二三四]｜/gm)].length !== 4) verification.errors.push(`${dir}: format`);
    if (s.shots.some(x => !prompt.includes(`{${x.dialogue}}`)) || [...prompt.matchAll(/台词(?:（画外音）)?：\{/g)].length !== 4) verification.errors.push(`${dir}: dialogue`);
    for (const ref of manifest.references) {
      if (ref.uri) { verification.digital_human_inputs++; continue; }
      verification.local_reference_slots++;
      if (!fs.existsSync(absolute(ref.file)) || !fs.existsSync(absolute(`${dir}/${ref.segment_file}`))) verification.missing.push({ dir, number: ref.number });
      else if (sha(fs.readFileSync(absolute(ref.file))) !== sha(fs.readFileSync(absolute(`${dir}/${ref.segment_file}`)))) verification.errors.push(`${dir}: image copy ${ref.number}`);
    }
  }
}
if (JSON.stringify(source.outputs) !== JSON.stringify(outputInventory())) verification.errors.push('Historical output inventory changed');
if (verification.errors.length || verification.missing.length) throw new Error(JSON.stringify(verification));
if (!checkOnly) writeJson('docs/ep044-050-15s-files-verified.json', verification);
console.log(JSON.stringify(verification, null, 2));
