# 当前制作状态

EP001当前采用v3台词修订r2，第8段为白璃爆气与元神法相v2，两张关键帧及导演文本已同步。小说正文、对白、8段分镜与导演文本已按全新人物和实际图片适配。

图片已完成16张剧情关键帧与6张人物资产图，覆盖7人。每段frames含2张选定关键帧与本段出场人物三视图，reference-plan.json记录有序输入。image-manifest.json是本集图片入口，参考图总览.html可浏览全部选定素材。

完整生成提示词、引用图、输出源路径、hash与目视检查记录保存在production/images-v1/image-jobs.json。重绘淘汰稿与旧人物输入归入独立生产归档。

下一阶段可按本段director-promt.txt与有序参考输入制作视频。配音和视频阶段状态在各段api-request.md与output中维护。

EP002《本座只是皱了个眉》已完成60秒、四段剧本与导演文本，主线为霸体误会、白发师傅驾鹤请罪并邀主角离场。新角色C07与第二集剧情关键帧待生成，文本检查见该集qa-checklist.md。

## EP003现行v2与后续规格

用户新剧情已写成《本座一句都没说》v2，120秒、8×15秒、49镜。正文为story-v2.md，对白为dialogue-v2.md，完整入口为完整剧本与15秒分段-v2.md。各段storyboard、首尾帧提示词、prompt、director-promt、api-request和reference-plan均同步v2。

开头15秒先交代落地冷场，谢无咎开口追问，裴长庚才当面说明方才用了传音。一个时辰沉默以日影、计时香和长老对白压缩呈现，画面无字幕。第二个核心误会为仙丹换清汤面，末尾长老下令仙宴改素面，肉片被收回。

每段两张剧情关键帧，共16张。C01与C07沿用前集基准，新增C08执礼长老、C09厨子、BG02讲道弟子组。各段按实际出演人物整理到frames，编号见分段reference-plan.json。

原八段剧本与关键帧留作制作依据。会盟广场、石壁龙椅和贵客膳轩已同步至导演提示词。成片以源片实际对白定字幕时间。查看[EP003参考图总览](../episodes/EP003_speak_out_loud/参考图总览.html)。

v1整体归档在production/EP003-revisions/v1-before-user-lecture-20261117，版本入口以README及本集revision-history.md为准。后续按prompt-writing-standard.md与story-local模板写作。


2026-11-17 EP002台词r1及图片适配1已完成。裴长庚心声改为气息敛得如此干净……大尊者又精进了。选定剧情帧11张，各段2、3、3、3；裴长庚和独立车夫人物图已生成。按实际出镜名单，第一段5张人物图、第二段6张、第三四段各3张，搬货弟子与其余未入镜人物图归档到production/EP002-images-v1/excluded-inputs。当前图片入口为EP002/image-manifest.json与参考图总览.html。


2026-11-17用户确认后期剪辑固定规范。BGM在上一版0.238基础上再降50%，现为0.119，正片恒定电平，Groovy Hammond循环到剧情结束。片头使用Create By／西瓜终结者AIGC／AI-GENERATED CINEMA细宋体与衬线英文白字设计，黑屏静音，片尾收至纯黑，图像及音乐起止0.3秒渐显渐隐，段间0.2秒叠化，成片加入对白字幕。固定入口为docs/editing-standard.md与templates/editing-profile.json。

EP001八段用户提供4K视频已合成为122.9秒、4K30fps成片，文件episodes/EP001_today-we-walk/output/EP001_本座今日不飞_4K.mp4。60组字幕、七处叠化、接环、黑帧及完整解码检查通过，BGM固定系数实测0.11867–0.11900。末段原片错误烧录字幕已局部清理，声音未经人工试听。

2026-11-18，EP002将四份用户源片剪成4K30fps正片，含三处0.2秒叠化和24条对白与内心字幕。使用用户指定的备选配乐《Groovy Hammond》，增益0.119。第一段末的原片烧录字幕已局部清理，字幕使用苹方简体 Regular。

用户指定从第二集起先播署名片头，再复用第一集的穿越自述。EP002按2.1秒署名片头、5.3秒自述、60.4秒当集正片剪辑，成片67.8秒，27条字幕。后续成片使用相同顺序和字幕时间轴。[第二集输出](../episodes/EP002_just_a_frown/output/) · [核验记录](../production/EP002-final-cut-v1/REVIEW.md) · [固定自述规范](editing-standard.md)

用户要求自述切入正片时配乐连续。EP002已将《Groovy Hammond》设为一条65.7秒音轨，成片2.1秒开始，7.4秒切入正片时歌曲已播放5.3秒。已核对切点前后音乐波形，后续成片按同一混音规则执行。

2026-11-18，原EP003八段用户源片分为EP003《本座一句都没说》和EP004《本座只想吃碗面》，每集67.8秒、4K30fps。第三集按实际对白将“一个时辰”放在“满场悟道”之前，第四集承接火锅、仙丹、清汤面与改素宴。两集各三处0.2秒叠化，BGM从2.1秒开始，跨7.4秒正片切点连续播放。[第三集核验](../production/EP003-final-cut-v1/REVIEW.md) · [第四集核验](../production/EP004-final-cut-v1/REVIEW.md)
