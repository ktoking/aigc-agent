import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const activeFormatFile = path.join(root, 'docs/ep044-050-production-format.json');
if (fs.existsSync(activeFormatFile) && JSON.parse(fs.readFileSync(activeFormatFile, 'utf8')).segment_duration === 15) {
  throw new Error('此同步器仅适用于历史30秒稿。当前15秒资产由build_ep044_050_15s.mjs统一构建与复核。');
}
const recordPath = 'assets/production/ep044-050-seedance25/generation-record.json';
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const json = file => JSON.parse(read(file));
const write = (file, value) => fs.writeFileSync(path.join(root, file), value);
const writeJson = (file, value) => write(file, `${JSON.stringify(value, null, 2)}\n`);
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const record = json(recordPath);
const generated = new Map(record.generated.map(item => [item.key, item]));
if (generated.size !== 27 || record.pending.length) throw new Error('Expected 27 completed assets');
const report = { scope: 'EP044-EP050', generator: record.tool, final_assets: 27,
  image_tool_calls: record.image_tool_calls, video_submitted: false,
  prompt_and_dialogue_changed: false, segments: [], missing: [], raster_files: [] };

for (const item of generated.values()) {
  const data = fs.readFileSync(item.file);
  if (!data.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) {
    throw new Error(`Invalid PNG: ${item.file}`);
  }
  const width = data.readUInt32BE(16), height = data.readUInt32BE(20);
  if (Math.abs(width / height - 16 / 9) > 0.003) throw new Error(`Not landscape 16:9: ${item.file}`);
  report.raster_files.push({ key: item.key, file: path.relative(root, item.file),
    width, height, bytes: data.length, sha256: sha(data) });
}

const validationFile = 'docs/ep044-050-seedance25-validation.json';
const validation = json(validationFile);
const imageRows = refs => refs.map(r => `| ${r.number} | ${r.label} | ${r.uri || r.file} | ${r.scope} | ${r.status} |`).join('\n');

for (const episode of fs.readdirSync(path.join(root, 'episodes')).filter(n => /^EP0(44|45|46|47|48|49|50)_/.test(n)).sort()) {
  const episodeDir = `episodes/${episode}`;
  const episodeManifests = [];
  for (const segment of ['segment_01_00-30s', 'segment_02_30-60s']) {
    const dir = `${episodeDir}/${segment}`;
    const immutable = ['director-promt.txt', 'prompt.md', 'dialogue.txt', 'storyboard.md', 'storyboard-source.json'];
    const hashes = new Map(immutable.map(file => [file, sha(read(`${dir}/${file}`))]));
    const manifest = json(`${dir}/reference-assets.json`);
    const changed = [];
    for (const ref of manifest.references) {
      if (ref.kind === 'digital_human') continue;
      const planned = ref.planned_file;
      if (!ref.file && planned) {
        const key = path.basename(planned).replace(/-16x9\.png$/, '');
        const item = generated.get(key);
        if (!item) throw new Error(`No generated record for ${planned}`);
        ref.file = path.relative(root, item.file);
        ref.generation_plan_file = planned;
        ref.planned_file = null;
        ref.status = 'generated_builtin_basic_visual_review';
        ref.generation_record = recordPath;
        changed.push(ref.number);
      }
      if (!ref.file || !fs.existsSync(path.join(root, ref.file))) {
        report.missing.push({ episode, segment, number: ref.number });
        continue;
      }
      const relativeCopy = `frames/参考图${ref.number}.png`;
      fs.mkdirSync(path.join(root, dir, 'frames'), { recursive: true });
      const target = path.join(root, dir, relativeCopy);
      if (fs.existsSync(target) && sha(fs.readFileSync(target)) !== sha(fs.readFileSync(path.join(root, ref.file)))) {
        throw new Error(`Existing numbered reference differs; preserve and review: ${target}`);
      }
      fs.copyFileSync(path.join(root, ref.file), target);
      ref.segment_file = relativeCopy;
    }
    manifest.api_submission.status = 'needs_visual_review';
    manifest.api_submission.local_reference_files_complete = true;
    manifest.api_submission.note = '九项含数字人，编号以本清单为准；本地图已补齐，旧候选状态仍需逐镜复核。禁止扫描frames自动上传，不传首尾帧；未提交视频，账号能力未验证。';
    writeJson(`${dir}/reference-assets.json`, manifest);
    const handoff = json(`${dir}/seedance25-handoff.json`);
    handoff.missing_reference_numbers = [];
    handoff.readiness = 'needs_visual_review';
    handoff.local_reference_files_complete = true;
    writeJson(`${dir}/seedance25-handoff.json`, handoff);
    let api = read(`${dir}/api-request.md`);
    for (const n of changed) {
      const ref = manifest.references.find(r => r.number === n);
      api = api.replace(`待补：${ref.generation_plan_file}`, ref.file);
    }
    api = api.replaceAll('needs_generation_for_rewritten_shots', 'generated_builtin_basic_visual_review');
    api = api.replace(/仍缺\d+张新稿对应图，详见asset-image-prompts\.md；缺图补齐前不提交。/, '本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。');
    write(`${dir}/api-request.md`, api);
    const scenes = manifest.references.filter(r => r.kind !== 'digital_human');
    const blocks = scenes.map(ref => {
      const item = record.generated.find(g => path.relative(root, g.file) === ref.file);
      return `## 参考图${ref.number}：${ref.label}\n\n状态：${ref.status}\n\n资产：${ref.file}\n\n本段副本：${ref.segment_file}\n\n用途：${ref.scope}\n\n${item ? `实际生图提示词：${item.prompt}\n\n输入参考：${item.references.map(f => path.relative(root, f)).join('；')}` : '沿用既有资产；未重新生成，旧候选状态与机位仍须按本镜头复核。'}\n`;
    });
    write(`${dir}/asset-image-prompts.md`, `# 参考图资产与生成记录\n\n本段${scenes.length}张非人物图片均有本地文件；数字人只用asset URI，不另生人脸。不传首尾帧。\n\n${blocks.join('\n')}\n`);
    write(`${dir}/frames/本版参考图说明.md`, `# 本版参考图\n\n仅按../reference-assets.json选择图片。文件名参考图N.png的N与本版提示词和实际请求统一编号一致。\n数字人占用前面的编号，但由asset URI提供，不以旧人物三视图替代。\n本目录其他带旧标题、旧人物三视图或关键帧的文件仅为历史材料，不自动上传、不当首尾帧。\n\n${manifest.references.map(r => `${r.number}：${r.label} → ${r.uri || r.segment_file}`).join('\n')}\n`);
    const row = validation.segments_detail.find(r => r.episode === episode && r.segment === segment);
    row.missing_reference_numbers = [];
    row.generated_reference_slots = manifest.references.filter(r => r.generation_record).length;
    row.new_reference_slots = 0;
    row.local_reference_files_complete = true;
    row.submission_status = 'needs_visual_review';
    if (hashes.get('director-promt.txt') !== row.prompt_sha256) throw new Error(`Prompt hash drift: ${dir}`);
    for (const [file, hash] of hashes) if (sha(read(`${dir}/${file}`)) !== hash) throw new Error(`Story changed: ${dir}/${file}`);
    report.segments.push({ episode, segment, planned_references: manifest.references.length,
      digital_humans: manifest.digital_humans.length, local_images: scenes.length, newly_linked: changed,
      missing_reference_numbers: [], prompt_sha256: hashes.get('director-promt.txt') });
    episodeManifests.push(`## ${segment}\n\n9项输入含数字人；本地场景道具${scenes.length}张，缺图0张。旧候选图仍需新镜头复核。\n\n| 输入顺序 | 标签 | 来源 | 职责 | 状态 |\n| --- | --- | --- | --- | --- |\n${imageRows(manifest.references)}\n`);
  }
  write(`${episodeDir}/image-manifest.md`, `# ${episode.slice(0, 5)} 资产清单\n\n图片补齐日期：2026-10-21。未生成视频，不扫描旧frames，不传首尾帧。\n\n${episodeManifests.join('\n')}\n`);
  const qaFile = `${episodeDir}/qa-checklist.md`;
  let qa = read(qaFile).replace(/缺参考图\d+张/g, '缺参考图0张');
  qa = qa.replace('- [ ] 缺图补齐，候选图逐张确认建筑、物件、服装与机位。', '- [x] 本版清单对应本地图片已补齐，编号副本已归入frames。\n- [ ] 旧候选图仍需逐镜确认建筑、物件、服装与机位。');
  write(qaFile, qa);
}
if (report.missing.length) throw new Error(JSON.stringify(report.missing));
validation.unique_missing_reference_files = 0;
validation.reference_images_generated_this_run = 27;
validation.asset_generation_record = recordPath;
validation.checks = 'text_and_paths_static_plus_new_asset_basic_visual_review';
writeJson(validationFile, validation);
const planFile = 'docs/ep044-050-seedance25-asset-plan.json';
const plan = json(planFile);
for (const asset of plan.assets) {
  const key = path.basename(asset.planned_file).replace(/-16x9\.png$/, '');
  asset.file = path.relative(root, generated.get(key).file);
  asset.status = 'generated_builtin_basic_visual_review';
}
plan.unique_missing_files = 0;
plan.images_generated_this_run = 27;
plan.generation_record = recordPath;
writeJson(planFile, plan);
record.status = 'complete_local_assets_linked';
record.validation_report = 'docs/ep044-050-reference-completion.json';
writeJson(recordPath, record);
report.result = 'local_reference_files_complete';
report.visual_review = 'New image outputs reviewed for basic subject, no people, modern style and approximate 16:9; existing candidates retain review status. Not a video or API quality pass.';
writeJson(record.validation_report, report);
console.log(JSON.stringify({ final_assets: 27, missing: report.missing.length, segments: report.segments.length,
  local_reference_slots: report.segments.reduce((n, s) => n + s.local_images, 0), prompt_changed: false }));
