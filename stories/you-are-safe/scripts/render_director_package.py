#!/usr/bin/env python3
"""从两分钟详细时间线同步导演包；不触碰六分钟原稿，不调用模型。"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes/SF002_2min-adaptation"


def write(path, text):
    path.write_text(text.strip() + "\n", encoding="utf-8")


def section(text, heading):
    match = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match[1].strip() if match else ""


def render():
    data = json.loads((EP / "timeline.json").read_text())
    full_book = [
        "# 《您已安全》两分钟｜八段详细导演提示词 v2",
        "2026-10-21。120秒，8段各15秒，32镜。参照六分钟第二版的逐镜导演字段重写；"
        "本次压缩剧情长度，恢复拍摄说明的详细程度。旧简版已归档，六分钟原稿保持不变。",
        "以下每段A均为完整独立导演稿；代码块与对应segment/director-promt.txt一致。"
        "局部秒点均在0—15秒内。尚未生成、试听或验证成片。",
        "角色、场景与动作细节服务于同一个主要行动，不代表在四秒内增加多条剧情。"
        "实际入口的长提示词、图像模式和镜头执行能力仍需试片核验。",
    ]
    reading = ["# 《您已安全》两分钟完整阅读稿", "导演详细版v2；120秒、8段、32镜。"
               "本文件便于连贯阅读；完整构图、对焦、灯光和动作节拍见two-minute-detailed-director-prompts-v2.md。"]
    metrics = []
    for seg in data["segments"]:
        n, folder = seg["id"], EP / seg["directory"]
        role_text = []
        for cid in seg["character_ids"]:
            card = (ROOT / "assets/characters" / cid / "00-character-card.md").read_text()
            role_text.append(card.splitlines()[0][2:] + "：" + section(card, "可见特征与服装")
                             + " 表演：" + section(card, "性格与表演"))
        scene_text = []
        for sid in seg["scene_ids"]:
            card = (ROOT / "assets/scenes" / sid / "scene-card.md").read_text()
            scene_text.append(card.splitlines()[0][2:] + "：" + section(card, "视觉锚点"))
        intro = [
            "生成一段十五秒、九比十六竖屏叙事动画，成人向二维半国漫，清楚轮廓、克制赛璐璐阴影、"
            "真实空间透视和电影布光。建议草稿清晰度为720p。它是按顺序切换的四个剧情镜头，"
            "不是一镜到底、四宫格、静态翻页或一次只画首镜。时间标签均是本段局部时间，十五秒到点结束。",
            "本段任务：" + seg["task"],
            "情绪与叙事：" + seg["emotional_task"],
            "人物固定：\n" + "\n".join(role_text),
            "空间关系：\n" + "\n".join(scene_text),
            "造型与材质：同一部动画的脸型、头身比例、发缝与服装版型不可改变，"
            "皮肤简洁平涂加少量渐变，不变真人摄影或塑料三维脸。衣褶随动作变化，"
            "不能用过量细节、鱼鳞网格或高锐化代替质感。金属、纸盒、玻璃、布料各自保有体积，"
            "毛绒只表现清楚轮廓与蓝补丁，不堆满屏细毛。参考焦距只是透视意图，不是真实相机元数据。",
            "参考约束：本次没有实际上传图片，不假设存在图片编号、角色URL或素材文件。"
            "后续如上传真实参考，角色图只锁身份与服装，场景图只锁空间与材质，"
            "首尾帧只锁时间端点；不得从场景图复制陌生人物。实际输入清单按真实顺序另行绑定，"
            "故事板表格、箭头、时间码与说明文字不画入视频。",
            "道具与左右：手机正常由陈默右手操作，白兔按本段交接后的位置出现，"
            "兔子左耳蓝补丁以玩偶自身左右为准，左眉缺口以陈默自身左右为准。"
            "交接物必须先由原持有者释放再由接收者托稳，不凭空复制、穿过手指或在切镜后换手。"
            "药盒白底青横条；合同与风险处置界面沿用白底青线，所有可读文字后期添加。",
            "逐镜导演时间线：",
        ]
        outro = [
            "全段声音与连续性：",
            "声音执行：只说每镜声音与台词标出的内容，其余镜头说明、结果和修复策略都不能读出。"
            "陈默始终同一自然中低男声，前半带普通人的自嘲与认真，后半疲惫；客服同一平稳中性女声，"
            "永远礼貌，不邪笑、发怒或戏剧性变声。朵朵是自然童声，母亲温和稍慢；"
            "画外声不驱动画内人物嘴部。对白按正常语速轮流说，不能二倍速、同句叠说或自动重复。"
            "本段保留环境声与对白，不生成背景配乐，配乐由后期统一；指定静默必须留出来，"
            "不要用自动音乐填满每一秒。",
            "文字与后期：屏幕、合同、金额、报告、评论、时间卡、字幕与片名全部后期叠加，"
            "生成画面只留平稳贴图面，不尝试书写汉字、不生品牌与水印。"
            "文字不能遮住递药接触点、兔子交接、人物眼睛或母亲消失的关键空位。",
            "前后段衔接：" + seg["bridge"],
            "首帧状态：" + seg["first_frame_exact"],
            "尾帧状态：" + seg["last_frame_exact"],
            "验收重点：观众不看制作说明也应看懂“" + seg["task"] + "”。"
            "逐镜核对动作开始、接触或转移、完成后的结果，不能只还原气氛。"
            "先修人脸与人数，再修因果动作、说话者和道具归属，最后修材质细节。"
            "漏镜时按对应镜头补拍或合成并回拼原时段，不自动加长旁白、延长到三十秒或追加支线。",
            "禁止偏差：不生成客服实体、施法手势、能量罩、法阵、反派头像、传送光圈、"
            "真实机构标志或血肉残片，不随机闪白、乱换场景、加片头广告和关注提示。"
            "母亲消失以后，现场、玻璃倒影、车厢和实时屏幕里都不得出现另一个活人，"
            "也不能用人形阴影暗示幸存者。只在明确换地、回忆或跨日时硬切，"
            "同场保持轴线与门窗方向。所有镜头仍属于本段十五秒，不把补拍建议演成新的剧情。",
        ]
        prompt = "\n\n".join(intro + [shot["full_text"] for shot in seg["shots"]] + outro)
        write(folder / "director-promt.txt", prompt)
        han, chars = len(re.findall(r"[\u4e00-\u9fff]", prompt)), len(prompt)
        metrics.append(dict(segment=n, han=han, chars=chars))
        asset_note = "角色：" + "、".join(seg["character_ids"]) + "；场景：" + "、".join(seg["scene_ids"]) + "。资产图像均未生成。"
        write(folder / "prompt.md", f"# Segment {n:02d}｜{seg['title']}｜详细导演版v2\n\n"
              f"## 规格与状态\n\n15秒、9:16、4镜。完整导演稿{han}个汉字。仅文字设计，"
              "没有生成或试听；长文接受程度和四镜执行待试片。\n\n"
              f"## 资产与端点\n\n{asset_note}\n\n首尾帧文字见first-frame.md、last-frame.md。"
              "图像尚未存在；换景不能强行继承同一帧。\n\n"
              f"## 完整导演提示词\n\n```text\n{prompt}\n```\n\n## 后期\n\n{seg['post']}")
        table = ["| 镜 | 局部时间 | 任务 | 画面与人物 | 运镜 | 声音 | 结果 |",
                 "| --- | --- | --- | --- | --- | --- | --- |"]
        for s in seg["shots"]:
            values = [s["id"], f"{s['start']}—{s['end']}秒", s["title"], s["action"], s["camera"], s["sound"], s["result"]]
            table.append("| " + " | ".join(str(v).replace("|", "／").replace("\n", " ") for v in values) + " |")
        source_map = "\n".join(f"- 镜{s['id']}：" + "、".join(f"六分钟第{ref['segment']:02d}段镜{ref['shot']}" for ref in s['source_refs']) for s in seg['shots'])
        write(folder / "storyboard.md", f"# Segment {n:02d} 故事板｜{seg['title']}\n\n"
              f"## 分段信息\n\n全片{seg['start']}—{seg['end']}秒，局部0—15秒。{seg['task']}\n\n"
              f"{asset_note}\n\n" + "\n".join(table) + "\n\n## 逐镜导演详表\n\n"
              + "\n\n".join(s['full_text'] for s in seg['shots'])
              + f"\n\n## 原稿参考\n\n{source_map}\n\n## 首尾帧与连续性\n\n首帧：{seg['first_frame_exact']}\n\n"
              f"尾帧：{seg['last_frame_exact']}\n\n{seg['bridge']}\n\n## 后期\n\n{seg['post']}\n\n"
              "## 优化后提示词\n\n完整执行稿见director-promt.txt；故事板含生产标注，只供审阅，不默认上传给视频模型。")
        for filename, exact, endshot in [("first-frame.md", seg["first_frame_exact"], seg["shots"][0]),
                                         ("last-frame.md", seg["last_frame_exact"], seg["shots"][-1])]:
            is_black = n == 8 and filename == "last-frame.md"
            frame_text = ("纯黑，不渲染人物、厨房和文字；片名后期添加。" if is_black
                          else f"景别与机位：{endshot['lens']}\n\n构图参考：{endshot['composition']}\n\n"
                          f"光线：{endshot['light']}\n\n质感与焦点：{endshot['focus']}")
            write(folder / filename, f"# Segment {n:02d} {'首帧' if filename.startswith('first') else '尾帧'}｜详细版v2\n\n"
                  "Story：you-are-safe；SF002；9:16，二维半国漫。状态：文字设计，图片待生成。\n\n"
                  f"## 精确瞬间\n\n{exact}\n\n## 机位、构图与光线\n\n{frame_text}\n\n"
                  f"## 身份锁\n\n" + "\n\n".join(role_text) + f"\n\n## 桥接\n\n{seg['bridge']}\n\n"
                  "## 禁止项\n\n只画一个明确瞬间，不把动作全过程、多个人物状态或四格时间线画进一张图。"
                  "不换脸、不镜像眉缺口与兔耳补丁、不复制物件、不画汉字水印，不以一张首帧冒充身份图。"
                  "母亲消失后的帧没有第二个活人，黑场帧不混入任何场景。")
        # 保留API未提交状态，只更新输入稿版本与长度，避免把导演重写升级成能力验证。
        ap = folder / "api-request.md"
        original = ap.read_text()
        original = re.sub(r"\n## 本轮导演稿版本\n.*?(?=\n## |\Z)", "", original, flags=re.S)
        original += (f"\n## 本轮导演稿版本\n\n2026-10-21详细版v2；{han}个汉字、{chars}个字符，4镜/15秒。"
                     "Prompt仍为director-promt.txt。该长度是写作结果，不是已验证的入口上限。"
                     "若实际入口截断或漏镜，先按完整长稿对应单镜补拍并拼回十五秒，"
                     "不要静默截掉后三镜，也不自动改模型、提交或扩时。\n")
        write(ap, original)
        full_book += [f"## 第{n:02d}段：{seg['title']}",
                      f"全片{seg['start']//60:02d}:{seg['start']%60:02d}—{seg['end']//60:02d}:{seg['end']%60:02d}；"
                      f"局部0—15秒；4镜；导演正文{han}个汉字。",
                      "### A. 完整导演提示词", f"```text\n{prompt}\n```",
                      "### B. 后期与段间衔接", seg["post"], seg["bridge"]]
        reading.append(f"## {seg['start']//60:02d}:{seg['start']%60:02d}—{seg['end']//60:02d}:{seg['end']%60:02d}｜{seg['title']}")
        for s in seg['shots']:
            a, b = seg['start'] + s['start'], seg['start'] + s['end']
            reading.append(f"**{a//60:02d}:{a%60:02d}—{b//60:02d}:{b%60:02d} {s['title']}**\n\n画面：{s['action']}\n\n声音：{s['sound']}")
        reading.append("后期：" + seg['post'])
    write(ROOT / "docs/two-minute-detailed-director-prompts-v2.md", "\n\n".join(full_book))
    write(ROOT / "docs/two-minute-reading-script.md", "\n\n".join(reading))
    print(json.dumps(metrics, ensure_ascii=False))


if __name__ == "__main__":
    render()
