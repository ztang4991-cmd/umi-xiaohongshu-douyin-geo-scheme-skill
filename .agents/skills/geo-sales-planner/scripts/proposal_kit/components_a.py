"""Layout and evidence components: cover, outline, kpi, cards, decision, steps, compare, formula, case."""
from helpers import esc, il, items, src


def cover(d):
    stats = ''.join(
        f'<div class="cv-stat"><b>{esc(s.get("value"))}</b><span>{il(s.get("label"))}</span></div>'
        for s in items(d, 'stats'))
    return (f'<div class="cover-wrap"><div class="cv-eyebrow">{esc(d.get("eyebrow", ""))}</div>'
            f'<h1 class="cv-title">{esc(d.get("title", ""))}</h1>'
            f'<div class="cv-sub">{il(d.get("subtitle", ""))}</div>'
            f'<div class="cv-chain">{il(d.get("chain", ""))}</div>'
            f'<div class="cv-note">{il(d.get("note", ""))}</div>'
            f'<div class="cv-stats">{stats}</div>'
            f'<div class="cv-foot">{esc(d.get("footer", ""))}</div></div>')


def outline(d):
    rows = ''.join(
        f'<div class="ol-row"><span class="ol-no">{esc(i.get("no"))}</span>'
        f'<b>{il(i.get("title"))}</b><span class="ol-pt">{il(i.get("point"))}</span></div>'
        for i in items(d))
    return f'<div class="outline">{rows}</div>'


def kpi(d):
    cols = int(d.get('cols', len(items(d)) or 4))
    tiles = ''.join(
        f'<div class="kpi-tile"><div class="kpi-v">{esc(i.get("value"))}</div>'
        f'<div class="kpi-l">{il(i.get("label"))}</div>'
        f'<div class="kpi-n">{il(i.get("note", ""))}</div></div>'
        for i in items(d))
    return f'<div class="kpi" style="grid-template-columns:repeat({cols},1fr)">{tiles}</div>'


def cards(d):
    cols = int(d.get('cols', 3))
    out = []
    for n, i in enumerate(items(d), 1):
        num = f'<span class="cd-no">{n}</span>' if d.get('numbered') else ''
        tag = f'<span class="cd-tag">{esc(i["tag"])}</span>' if i.get('tag') else ''
        out.append(f'<div class="card {esc(i.get("level", ""))}">{num}{tag}'
                   f'<div class="cd-t">{il(i.get("title"))}</div>'
                   f'<div class="cd-b">{il(i.get("body", ""))}</div></div>')
    return f'<div class="cards" style="grid-template-columns:repeat({cols},1fr)">{"".join(out)}</div>'


def decision(d):
    checks = ''.join(f'<li>{il(c)}</li>' for c in items(d, 'checklist'))
    checks = f'<div class="dc-sub">{esc(d.get("checklist_title", "店方提供"))}</div><ul class="dc-list">{checks}</ul>' if checks else ''
    note = f'<div class="dc-note">{il(d["note"])}</div>' if d.get('note') else ''
    return (f'<div class="decision"><div class="dc-t">{il(d.get("title", "今天想和您定下来的事"))}</div>'
            f'<div class="dc-b">{il(d.get("body", ""))}</div>{checks}{note}</div>')


def steps(d):
    cols = int(d.get('cols', len(items(d)) or 4))
    out = ''.join(
        f'<div class="step"><span class="st-no">{n}</span><div class="st-t">{il(i.get("title"))}</div>'
        f'<div class="st-b">{il(i.get("body", ""))}</div></div>'
        for n, i in enumerate(items(d), 1))
    return f'<div class="steps" style="grid-template-columns:repeat({cols},1fr)">{out}</div>'


def compare(d):
    def side(s, cls):
        chips = ''.join(f'<span class="chip">{il(x)}</span>' for x in s.get('items', []))
        return f'<div class="cp-side {cls}"><div class="cp-l">{il(s.get("label", ""))}</div><div class="chips">{chips}</div></div>'
    return (f'<div class="compare">{side(d.get("from", {}), "from")}'
            f'<div class="cp-arrow">↓ {il(d.get("arrow", "换成能拍、能核实的证据"))}</div>'
            f'{side(d.get("to", {}), "to")}</div>')


def formula(d):
    terms = '<span class="fx-op">×</span>'.join(f'<span class="fx-term">{il(t)}</span>' for t in items(d, 'terms'))
    note = f'<div class="fx-note">{il(d["note"])}</div>' if d.get('note') else ''
    return (f'<div class="formula"><div class="fx-row">{terms}<span class="fx-op">=</span>'
            f'<span class="fx-term result">{il(d.get("result", ""))}</span></div>{note}</div>')


def case(d):
    cols = int(d.get('cols', min(len(items(d)) or 1, 3)))
    out = []
    for i in items(d):
        uri = src(i.get('image', ''))
        img = f'<img src="{uri}">' if uri else f'<div class="missing">图片未找到：{esc(i.get("image", ""))}</div>'
        out.append(f'<div class="case-card">{img}<div class="cs-t">{il(i.get("title"))}</div>'
                   f'<div class="cs-c">{il(i.get("caption", ""))}</div></div>')
    return f'<div class="cases" style="grid-template-columns:repeat({cols},1fr)">{"".join(out)}</div>'


REGISTRY = {'cover': cover, 'outline': outline, 'kpi': kpi, 'cards': cards, 'decision': decision,
            'steps': steps, 'compare': compare, 'formula': formula, 'case': case}
