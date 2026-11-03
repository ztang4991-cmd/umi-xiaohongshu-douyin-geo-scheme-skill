"""Build a structured proposal: Markdown + JSON component blocks -> HTML -> PDF.

Usage:
    python build.py 源稿.md                 # HTML + PDF next to the source
    python build.py 源稿.md --preview       # also write per-page PNGs to <源稿>_preview/
    python build.py 源稿.md --html-only     # skip PDF
See ../../references/output-components.md for the component catalogue.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import helpers  # noqa: E402
from components_a import REGISTRY as REG_A  # noqa: E402
from components_b import REGISTRY as REG_B  # noqa: E402

REGISTRY = {**REG_A, **REG_B}
FENCE = re.compile(r'^```(' + '|'.join(REGISTRY) + r')[ \t]*\n(.*?)\n```[ \t]*$', re.S | re.M)
ERRORS = []


def front_matter(text):
    meta = {}
    if text.startswith('---'):
        head, _, text = text[3:].partition('\n---')
        for line in head.strip().splitlines():
            key, sep, value = line.partition(':')
            if sep:
                meta[key.strip()] = value.strip()
        text = text.lstrip('-').lstrip('\n')
    return meta, text


def md(text):
    """Render Markdown, replacing component fences with their HTML."""
    blocks = []

    def swap(m):
        name, body = m.group(1), m.group(2)
        try:
            out = REGISTRY[name](json.loads(body))
        except Exception as exc:  # surface bad JSON or missing fields in the page and the exit code
            ERRORS.append(f'{name}: {exc}')
            out = f'<div class="comp-error">组件 {name} 渲染失败：{helpers.esc(exc)}</div>'
        blocks.append(out)
        return f'\n\n@@COMP{len(blocks) - 1}@@\n\n'

    text = re.sub(r'^- \[ \] ', '- <span class="box"></span> ', text, flags=re.M)
    text = re.sub(r'^- \[x\] ', '- <span class="box on"></span> ', text, flags=re.M)
    rendered = helpers.MD.render(FENCE.sub(swap, text))
    for n, block in enumerate(blocks):
        rendered = rendered.replace(f'<p>@@COMP{n}@@</p>', block).replace(f'@@COMP{n}@@', block)
    return rendered


def columns(text):
    """:::cols / :::col / ::: -> side-by-side grid."""
    out, cols, buf, inside = [], [], [], False
    for line in text.splitlines():
        tag = line.strip()
        if tag == ':::cols' and not inside:
            out.append(md('\n'.join(buf))); buf, cols, inside = [], [], True
        elif tag == ':::col' and inside:
            cols.append(md('\n'.join(buf))); buf = []
        elif tag == ':::' and inside:
            cols.append(md('\n'.join(buf))); buf, inside = [], False
            out.append('<div class="cols">' + ''.join(f'<div class="col">{c}</div>' for c in cols) + '</div>')
        else:
            buf.append(line)
    out.append(md('\n'.join(buf)))
    return ''.join(out)


def split_pages(text):
    pages, cur = [], []
    for line in text.splitlines():
        if line.startswith('# ') and cur:
            pages.append('\n'.join(cur)); cur = []
        cur.append(line)
    if cur:
        pages.append('\n'.join(cur))
    return [p for p in pages if p.strip()]


def page_html(chunk, n, meta):
    first, _, body = chunk.partition('\n')
    heading = first[2:].strip() if first.startswith('# ') else ''
    if not first.startswith('# '):
        body = chunk
    inner = helpers.style_tags(columns(body))
    if '```cover' in chunk:
        return f'<section class="page cover">{inner}</section>'
    m = re.match(r'^(\d{1,2})\s*[｜|·.、]?\s*(.+)$', heading)
    no, title = (m.group(1), m.group(2)) if m else ('', heading)
    top = (f'<header class="topbar"><span>{helpers.esc(meta.get("client", ""))} / {helpers.esc(meta.get("title", ""))}</span>'
           f'<span class="disc">{helpers.esc(meta.get("disclaimer", ""))}</span><b>{n:02d}</b></header>')
    h1 = f'<h1 class="sec"><span class="sec-no">{helpers.esc(no)}</span>{helpers.style_tags(helpers.il(title))}</h1>'
    return f'<section class="page">{top}{h1}<div class="body">{inner}</div></section>'


def build_html(meta, text):
    css = (HERE / 'theme.css').read_text(encoding='utf-8')
    pages = ''.join(page_html(c, i + 1, meta) for i, c in enumerate(split_pages(text)))
    return (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            f'<title>{helpers.esc(meta.get("title", "proposal"))}</title><style>{css}</style></head><body>{pages}</body></html>')


def export(html_path, pdf_path, preview_dir, chrome):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
        page = browser.new_page(viewport={'width': 1123, 'height': 794})
        page.goto(html_path.resolve().as_uri(), wait_until='load')
        page.evaluate('document.fonts.ready')
        overflow = page.evaluate("""() => [...document.querySelectorAll('.page')].map((p, i) => {
            const b = p.querySelector('.body'); return b && b.scrollHeight > b.clientHeight + 1 ? i + 1 : 0
        }).filter(Boolean)""")
        page.pdf(path=str(pdf_path), print_background=True, prefer_css_page_size=True)
        if preview_dir:
            preview_dir.mkdir(exist_ok=True)
            for i, el in enumerate(page.locator('.page').all(), 1):
                el.screenshot(path=str(preview_dir / f'page-{i:02d}.png'))
        browser.close()
    return overflow


def main():
    ap = argparse.ArgumentParser(description='Markdown + JSON components -> proposal PDF')
    ap.add_argument('source')
    ap.add_argument('--pdf', help='PDF output path (default: next to source)')
    ap.add_argument('--html-only', action='store_true')
    ap.add_argument('--preview', action='store_true', help='write per-page PNG previews')
    ap.add_argument('--chrome', help='Chrome/Edge executable if Playwright Chromium is not installed')
    args = ap.parse_args()

    source = Path(args.source).resolve()
    helpers.BASE_DIR = source.parent
    meta, text = front_matter(source.read_text(encoding='utf-8'))
    html_path = source.with_suffix('.html')
    html_path.write_text(build_html(meta, text), encoding='utf-8')
    print(f'HTML: {html_path}')
    if ERRORS:
        print('组件错误：\n  ' + '\n  '.join(ERRORS)); sys.exit(2)
    if args.html_only:
        return
    pdf_path = Path(args.pdf).resolve() if args.pdf else source.with_suffix('.pdf')
    preview = source.parent / f'{source.stem}_preview' if args.preview else None
    overflow = export(html_path, pdf_path, preview, args.chrome)
    print(f'PDF:  {pdf_path}')
    if overflow:
        print(f'内容溢出（被裁切）的页：{overflow}。请拆页或删减后重建。'); sys.exit(3)
    print('溢出检查：通过')


if __name__ == '__main__':
    main()
