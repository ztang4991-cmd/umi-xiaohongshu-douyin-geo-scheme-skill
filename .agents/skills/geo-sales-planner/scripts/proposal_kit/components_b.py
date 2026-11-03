"""Data and process components: hbar, funnel, journey, timeline, calendar, checkpoints, rules, tiers."""
from helpers import esc, il, items


def _num(v):
    return f'{v:g}' if isinstance(v, (int, float)) else esc(v)


def hbar(d):
    rows = items(d)
    vals = [r.get('value', 0) for r in rows if isinstance(r.get('value'), (int, float))]
    top = d.get('max') or (max(vals) if vals else 1) or 1
    unit = esc(d.get('unit', ''))
    out = ''.join(
        f'<div class="hb-row"><span class="hb-l">{il(r.get("label"))}</span>'
        f'<span class="hb-track"><span class="hb-fill" style="width:{100 * r.get("value", 0) / top:.1f}%"></span></span>'
        f'<span class="hb-v">{_num(r.get("value"))}{unit}</span></div>'
        for r in rows)
    title = f'<div class="hb-title">{il(d["title"])}</div>' if d.get('title') else ''
    note = f'<div class="hb-note">{il(d["note"])}</div>' if d.get('note') else ''
    return f'<div class="hbar">{title}{out}{note}</div>'


def _chain(labels, cls, highlight=()):
    parts = []
    for n, s in enumerate(labels):
        hl = ' hl' if s in highlight else ''
        parts.append(f'<div class="{cls}{hl}"><span class="fn-i">{n + 1}</span>{il(s)}</div>')
    return '<span class="fn-arrow">→</span>'.join(parts)


def funnel(d):
    defs = ''.join(f'<div class="fn-def"><b>{il(x.get("term"))}</b><span>{il(x.get("def"))}</span></div>'
                   for x in items(d, 'defs'))
    defs = f'<div class="fn-defs">{defs}</div>' if defs else ''
    return (f'<div class="funnel"><div class="fn-chain">{_chain(items(d, "stages"), "fn-stage", d.get("highlight", []))}</div>'
            f'{defs}</div>')


def journey(d):
    note = f'<div class="jr-note">{il(d["note"])}</div>' if d.get('note') else ''
    return f'<div class="journey"><div class="fn-chain">{_chain(items(d, "steps"), "jr-step")}</div>{note}</div>'


def timeline(d):
    total = float(d.get('total', 90))
    bars = ''.join(
        f'<div class="tl-phase p{n % 3}" style="left:{100 * (p.get("start", 1) - 1) / total:.2f}%;'
        f'width:{100 * (p.get("end", total) - p.get("start", 1) + 1) / total:.2f}%">{il(p.get("label"))}</div>'
        for n, p in enumerate(items(d, 'phases')))
    def mark(m):
        pct = 100 * m.get('day', 0) / total
        edge = ' end' if pct > 90 else (' start' if pct < 10 else '')  # keep edge labels inside the page
        return f'<div class="tl-ms{edge}" style="left:{pct:.2f}%"><i></i><span>{il(m.get("label"))}</span></div>'
    marks = ''.join(mark(m) for m in items(d, 'milestones'))
    lanes = ''.join(
        f'<div class="tl-lane"><div class="tl-when">{il(l.get("when"))}</div>'
        f'<div class="tl-lt">{il(l.get("title"))}</div><div class="tl-lb">{il(l.get("body", ""))}</div></div>'
        for l in items(d, 'lanes'))
    lanes = f'<div class="tl-lanes" style="grid-template-columns:repeat({len(items(d, "lanes")) or 1},1fr)">{lanes}</div>' if lanes else ''
    return f'<div class="timeline"><div class="tl-track">{bars}</div><div class="tl-marks">{marks}</div>{lanes}</div>'


def calendar(d):
    weeks = items(d, 'weeks')
    cells = []
    for w in weeks:
        rows = ''.join(
            f'<li><div class="ca-t">{il(i.get("title"))}</div>'
            f'<div class="ca-m"><span class="ca-f">{esc(i.get("format", ""))}</span>{il(i.get("source", ""))}</div></li>'
            for i in w.get('items', []))
        cells.append(f'<div class="ca-week"><div class="ca-w">{il(w.get("week"))}</div><ol>{rows}</ol></div>')
    foot = f'<div class="ca-foot">{il(d["foot"])}</div>' if d.get('foot') else ''
    return f'<div class="calendar" style="grid-template-columns:repeat({len(weeks) or 1},1fr)">{"".join(cells)}</div>{foot}'


def checkpoints(d):
    out = ''.join(
        f'<div class="ck"><div class="ck-day">◆ {il(i.get("day"))}</div>'
        f'<div class="ck-k">看</div><div class="ck-v">{il(i.get("look"))}</div>'
        f'<div class="ck-k">定</div><div class="ck-v">{il(i.get("decide"))}</div></div>'
        for i in items(d))
    return f'<div class="checkpoints">{out}</div>'


def rules(d):
    out = ''.join(
        f'<div class="rule {esc(i.get("key", "go"))}"><b>● {il(i.get("label"))}</b><span>{il(i.get("body"))}</span></div>'
        for i in items(d))
    return f'<div class="rules">{out}</div>'


def tiers(d):
    out = []
    for t in items(d):
        rec = '<span class="ti-rec">推荐</span>' if t.get('recommended') else ''
        rows = ''.join(f'<div class="ti-k">{k}</div><div class="ti-v">{il(t[f])}</div>'
                       for k, f in (('适合', 'fit'), ('做什么', 'scope'), ('不含', 'exclude'), ('费用', 'fee')) if t.get(f))
        out.append(f'<div class="tier{" rec" if t.get("recommended") else ""}">'
                   f'<div class="ti-n">{il(t.get("name"))}{rec}</div><div class="ti-grid">{rows}</div></div>')
    return f'<div class="tiers" style="grid-template-columns:repeat({len(out) or 1},1fr)">{"".join(out)}</div>'


REGISTRY = {'hbar': hbar, 'funnel': funnel, 'journey': journey, 'timeline': timeline, 'calendar': calendar,
            'checkpoints': checkpoints, 'rules': rules, 'tiers': tiers}
