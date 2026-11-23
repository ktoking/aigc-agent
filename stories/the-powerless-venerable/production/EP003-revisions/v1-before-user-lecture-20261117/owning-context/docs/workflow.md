# 当前制作状态

EP001当前采用v3台词修订r2，第8段为白璃爆气与元神法相v2，两张关键帧及导演文本已同步。小说正文、对白、8段分镜与导演文本已按全新人物和实际图片适配。

图片已完成16张剧情关键帧与6张人物资产图，覆盖7人。每段frames含2张选定关键帧与本段出场人物三视图，reference-plan.json记录有序输入。image-manifest.json是本集图片入口，参考图总览.html可浏览全部选定素材。

完整生成提示词、引用图、输出源路径、hash与目视检查记录保存在production/images-v1/image-jobs.json。重绘淘汰稿与旧人物输入归入独立生产归档。

下一阶段可按本段director-promt.txt与有序参考输入制作视频。配音和视频阶段状态在各段api-request.md与output中维护。

EP002《本座只是皱了个眉》已完成60秒、四段剧本与导演文本，主线为霸体误会、白发师傅驾鹤请罪并邀主角离场。新角色C07与第二集剧情关键帧待生成，文本检查见该集qa-checklist.md。

## EP003与后续规格

用户2026-11-17确定后续每集120秒、8×15秒，EP003为首个按该规格新增的后续剧集。五阶段方向见series-progression.md。

EP003《你倒是开口啊》v1已经补齐小说正文、对白、8段故事板、首尾帧提示词、视频提示词、director-promt.txt、api-request.md与episode-plan.json。每段规划两张剧情关键帧，当前尚待生成。各段frames已复用C01、C07现有人物三视图并记录hash。

声音窗口为文字估排。第8段远景群演BG01的造型文字已完成，参考图片待制作。本轮制作状态为SCRIPT_DESIGN_MEDIA_PENDING，配音、关键帧和视频尚待制作。文字与结构核验分别见该集qa-checklist.md和text-validation.json。

EP003当前文本修订为r1-prompt-completeness-20261117。8段共48镜，每镜已填写焦段、景别、机位构图、运镜、焦点、动作、声音和衔接，导演提示词每段约3279—3718个非空白字符。新增规范与模板见prompt-writing-standard.md及templates/segment-director-prompt-template.md。画面采用无字幕规格，本轮交付为文本。


2026-11-17 EP002台词r1及图片适配1已完成。裴长庚心声改为气息敛得如此干净……大尊者又精进了。选定剧情帧11张，各段2、3、3、3；裴长庚和独立车夫人物图已生成。按实际出镜名单，第一段5张人物图、第二段6张、第三四段各3张，搬货弟子与其余未入镜人物图归档到production/EP002-images-v1/excluded-inputs。当前图片入口为EP002/image-manifest.json与参考图总览.html。
