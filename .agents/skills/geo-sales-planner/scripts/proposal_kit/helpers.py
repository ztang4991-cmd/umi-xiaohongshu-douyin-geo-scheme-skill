"""Shared helpers for proposal_kit components."""
import html
import re
from pathlib import Path

from markdown_it import MarkdownIt

MD = MarkdownIt('commonmark', {'html': True}).enable('table').enable('strikethrough')

# Set by build.py to the source Markdown's folder so relative image paths resolve.
BASE_DIR = Path('.')

# Evidence labels from references/team-profile.md “证据等级约定”, plus a few writing labels.
TAGS = {
    '公开抽样': 'sample', 'OTA公开快照': 'sample', '公开快照': 'sample', '坐标直线距离': 'sample',
    '现场核实': 'fact', '事实': 'fact', '推断': 'infer',
    '客户提供': 'verify', '待核实': 'verify', '待确认': 'verify',
    '建议': 'advice', '示例': 'demo', '风险': 'risk',
}
TAG_RE = re.compile(r'\[(' + '|'.join(sorted(TAGS, key=len, reverse=True)) + r')([^\]]*)\]')


def esc(text):
    return html.escape(str(text if text is not None else ''))


def il(text):
    """Render inline Markdown (bold, code, links) inside component strings."""
    if text is None:
        return ''
    return MD.renderInline(str(text))


def src(path):
    """Return a file:// URI for an image, or None if it does not exist."""
    p = Path(path)
    if not p.is_absolute():
        p = (BASE_DIR / p).resolve()
    return p.as_uri() if p.exists() else None


def style_tags(fragment):
    """Turn [事实] / [推断·2026-10-28] style labels into coloured pills."""
    return TAG_RE.sub(
        lambda m: f'<span class="tag {TAGS[m.group(1)]}">{m.group(1)}{m.group(2)}</span>',
        fragment)


def items(data, key='items'):
    value = data.get(key, [])
    return value if isinstance(value, list) else []
