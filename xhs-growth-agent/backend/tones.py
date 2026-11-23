"""Trusted, composable editorial tones; no extra model calls."""
from typing import Literal

ToneName = Literal['natural', 'critical', 'objective', 'subjective', 'sharp', 'gentle', 'humorous', 'empathetic']
TONES = {
    'natural': ('自然', '像平常跟人聊天，词语日常、句子有长有短，表达直接，不刻意煽情或评价。'),
    'critical': ('批判', '找具体问题、规则或利益矛盾，说明谁承担代价、哪里不合理，给批判理由；不默认所有事情都值得骂。'),
    'objective': ('客观', '克制陈述事实和适用条件，把事实、判断、未知分开，证据不够不下断言，不预设赞扬或批判立场，也不强凑双方观点。'),
    'subjective': ('主观', '从个人看法、偏好和感受切入，明确这是观点，不代表所有人；第一人称用于看法，不能虚构亲历。'),
    'sharp': ('犀利', '判断直接，抓住核心矛盾，用简短有力的句子说透；不靠脏话、羞辱或夸张事实撑气势。'),
    'gentle': ('温和', '措辞平和、留有余地，不训读者、不拱火；可以明确不同意，但说明理由而不是逼人站队。'),
    'humorous': ('幽默', '用少量贴切比喻、轻松吐槽或反差表达，不硬塞段子和表情，不拿伤害与灾难开玩笑。'),
    'empathetic': ('共情', '先看普通人的具体处境、预算、压力和感受，用细节让人觉得被理解，不代替所有人宣布情绪。'),
}


def normalize_tones(values=None):
    if values is None:
        return ['natural']
    if not isinstance(values, (list, tuple)) or any(not isinstance(value, str) or value not in TONES for value in values):
        raise ValueError('请选择内置语气标签')
    selected = list(dict.fromkeys(values))
    if len(selected) > 4:
        raise ValueError('每次最多选择 4 个语气标签')
    return selected or ['natural']


def tone_prompt(values=None):
    selected = normalize_tones(values)
    lines = ['本次语气：' + '＋'.join(TONES[key][0] for key in selected)]
    lines.extend(f'{TONES[key][0]}：{TONES[key][1]}' for key in selected)
    lines.append('组合标签共同生效，不随机挑一个。不论标签如何，都保持自然表达；没有选择批判时，不自动套用愤世嫉俗的人设。')
    if 'objective' in selected and ('subjective' in selected or 'critical' in selected):
        lines.append('组合方式：客观约束事实与证据，主观或批判只作用于有理由的判断；正文自然地区分事实和看法，不写标签说明。')
    if 'gentle' in selected and ('sharp' in selected or 'critical' in selected):
        lines.append('组合方式：观点可以直接、批判可以明确，但措辞温和，不人身攻击。')
    return '\n'.join(lines)
