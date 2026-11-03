from __future__ import annotations

import os
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
MD_PATH = ROOT / "三圣乡.余生_小红书账号诊断与运营合作方案_20260810.md"
DOCX_PATH = ROOT / "三圣乡.余生_小红书账号诊断与运营合作方案_20260810.docx"

FONT_LATIN = "Calibri"
FONT_CJK = "Microsoft YaHei"
BLUE = RGBColor(46, 116, 181)
DARK_BLUE = RGBColor(31, 77, 120)
NAVY = RGBColor(11, 37, 69)
GRAY = RGBColor(88, 88, 88)
MUTED = RGBColor(105, 105, 105)
LIGHT_FILL = "F4F6F9"
TABLE_FILL = "F2F4F7"
GOLD_FILL = "FFF8E8"


def set_run_font(run, size=11, color=None, bold=None, italic=None, name=FONT_LATIN):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), FONT_CJK)
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.first_child_found_in("w:shd")
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")


def set_table_borders(table, color="D7DBE2", size="6"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        node = borders.find(tag)
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)


def set_table_geometry(table, widths, indent=120):
    widths = [int(w) for w in widths]
    total = sum(widths)
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    tbl_w = tbl_pr.first_child_found_in("w:tblW")
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(total))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = tbl_pr.first_child_found_in("w:tblInd")
    if tbl_ind is None:
        tbl_ind = OxmlElement("w:tblInd")
        tbl_pr.append(tbl_ind)
    tbl_ind.set(qn("w:w"), str(indent))
    tbl_ind.set(qn("w:type"), "dxa")
    layout = tbl_pr.first_child_found_in("w:tblLayout")
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")

    grid = tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for w in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(w))
        grid.append(col)

    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            cell.width = Inches(widths[idx] / 1440)
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.first_child_found_in("w:tcW")
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:w"), str(widths[idx]))
            tc_w.set(qn("w:type"), "dxa")
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cell)


def add_page_number(paragraph):
    run = paragraph.add_run("第 ")
    set_run_font(run, 9, color=MUTED)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)
    run = paragraph.add_run(" 页")
    set_run_font(run, 9, color=MUTED)


def configure_document(doc):
    section = doc.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.right_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)

    normal = doc.styles["Normal"]
    normal.font.name = FONT_LATIN
    normal._element.rPr.rFonts.set(qn("w:ascii"), FONT_LATIN)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), FONT_LATIN)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CJK)
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(35, 35, 35)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.333
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    for name, size, color, before, after in (
        ("Heading 1", 16, BLUE, 18, 10),
        ("Heading 2", 13, BLUE, 12, 6),
        ("Heading 3", 12, DARK_BLUE, 8, 4),
    ):
        style = doc.styles[name]
        style.font.name = FONT_LATIN
        style._element.rPr.rFonts.set(qn("w:ascii"), FONT_LATIN)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), FONT_LATIN)
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CJK)
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = color
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    for style_name in ("List Bullet", "List Number"):
        style = doc.styles[style_name]
        style.font.name = FONT_LATIN
        style._element.rPr.rFonts.set(qn("w:ascii"), FONT_LATIN)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), FONT_LATIN)
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CJK)
        style.font.size = Pt(11)
        style.paragraph_format.left_indent = Inches(0.375)
        style.paragraph_format.first_line_indent = Inches(-0.194)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.line_spacing = 1.208

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hrun = header.add_run("UMI / 聚光米运营团队  |  三圣乡.余生小红书运营方案")
    set_run_font(hrun, 9, color=MUTED)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_page_number(footer)


def add_rich_text(paragraph, text, default_color=None, size=11):
    text = re.sub(r"<https?://([^>]+)>", r"https://\1", text)
    text = text.replace("`", "")
    pos = 0
    pattern = re.compile(r"(\*\*[^*]+\*\*|\[[^\]]+\]\([^\)]+\))")
    for match in pattern.finditer(text):
        if match.start() > pos:
            run = paragraph.add_run(text[pos:match.start()])
            set_run_font(run, size, color=default_color)
        token = match.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            set_run_font(run, size, color=default_color, bold=True)
        else:
            label, url = re.match(r"\[([^\]]+)\]\(([^\)]+)\)", token).groups()
            run = paragraph.add_run(label)
            set_run_font(run, size, color=RGBColor(35, 91, 145), bold=True)
        pos = match.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        set_run_font(run, size, color=default_color)


def clean_cell(value):
    value = value.strip()
    value = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", value)
    value = value.replace("**", "").replace("`", "")
    return value


def add_table(doc, rows):
    cols = len(rows[0])
    table = doc.add_table(rows=1, cols=cols)
    table.style = "Table Grid"
    widths_by_cols = {
        2: [2700, 6660],
        3: [1800, 3300, 4260],
        4: [1750, 2500, 2500, 2610],
        5: [1200, 2050, 1900, 2150, 2060],
        6: [1050, 1700, 1600, 1700, 1650, 1660],
    }
    widths = widths_by_cols.get(cols, [9360 // cols] * cols)
    set_table_geometry(table, widths)
    set_table_borders(table)
    for idx, value in enumerate(rows[0]):
        cell = table.rows[0].cells[idx]
        set_cell_shading(cell, TABLE_FILL)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_rich_text(p, clean_cell(value), size=9.5)
        for run in p.runs:
            run.bold = True
    for row_values in rows[1:]:
        cells = table.add_row().cells
        for idx, value in enumerate(row_values):
            p = cells[idx].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            add_rich_text(p, clean_cell(value), size=9.2)
    set_table_geometry(table, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_callout(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    set_table_geometry(table, [9360])
    set_table_borders(table, color="D7DBE2", size="4")
    cell = table.cell(0, 0)
    set_cell_shading(cell, LIGHT_FILL)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    add_rich_text(p, text.lstrip("> "), default_color=RGBColor(55, 55, 55), size=10.2)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_title_block(doc, lines):
    kicker = doc.add_paragraph()
    kicker.alignment = WD_ALIGN_PARAGRAPH.CENTER
    kicker.paragraph_format.space_after = Pt(8)
    run = kicker.add_run("UMI / 聚光米运营团队  |  本地生活内容运营")
    set_run_font(run, 10, color=GRAY, bold=True)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(4)
    title.paragraph_format.keep_with_next = True
    r = title.add_run(lines[0].lstrip("# "))
    set_run_font(r, 24, color=NAVY, bold=True, name=FONT_CJK)

    if len(lines) > 1:
        subtitle = doc.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle.paragraph_format.space_after = Pt(14)
        sr = subtitle.add_run(lines[1].lstrip("# "))
        set_run_font(sr, 13, color=GRAY, name=FONT_CJK)

    meta = doc.add_table(rows=4, cols=2)
    meta.style = "Table Grid"
    set_table_geometry(meta, [2100, 7260])
    set_table_borders(meta, color="D7DBE2", size="4")
    meta_rows = [
        ("商家名", "三圣乡.余生"),
        ("小红书号", "63025500881"),
        ("方案范围", "账号诊断、运营方向、团队介绍、四个案例和90天执行"),
        ("数据日期", "2026年8月10日；公开主页与项目内资料口径"),
    ]
    for row, (label, value) in zip(meta.rows, meta_rows):
        set_cell_shading(row.cells[0], TABLE_FILL)
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        add_rich_text(p0, label, size=9.5)
        for run in p0.runs:
            run.bold = True
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        add_rich_text(p1, value, size=9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def parse_markdown(doc, path):
    lines = path.read_text(encoding="utf-8").splitlines()
    title_lines = []
    idx = 0
    while idx < len(lines) and lines[idx].startswith("# "):
        title_lines.append(lines[idx])
        idx += 1
    add_title_block(doc, title_lines[:2])
    in_table = False
    table_rows = []
    i = idx
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped == "":
            if in_table:
                add_table(doc, table_rows)
                in_table = False
                table_rows = []
            i += 1
            continue
        if stripped == "---":
            if in_table:
                add_table(doc, table_rows)
                in_table = False
                table_rows = []
            i += 1
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                i += 1
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        if in_table:
            add_table(doc, table_rows)
            in_table = False
            table_rows = []
        if stripped.startswith(">"):
            add_callout(doc, stripped)
            i += 1
            continue
        m = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1)) - 1
            p = doc.add_paragraph(style=f"Heading {level}")
            add_rich_text(p, m.group(2), size={1: 16, 2: 13, 3: 12}[level])
            i += 1
            continue
        if re.match(r"^[-*]\s+", stripped):
            p = doc.add_paragraph(style="List Bullet")
            add_rich_text(p, re.sub(r"^[-*]\s+", "", stripped))
            i += 1
            continue
        if re.match(r"^\d+\.\s+", stripped):
            p = doc.add_paragraph(style="List Number")
            add_rich_text(p, re.sub(r"^\d+\.\s+", "", stripped))
            i += 1
            continue
        p = doc.add_paragraph()
        add_rich_text(p, stripped)
        i += 1
    if in_table:
        add_table(doc, table_rows)


def add_screenshot_appendix(doc):
    images = [
        ("图1  悦哉运营群：项目群协同与素材归档", Path(r"C:\Users\EDY\AppData\Local\Temp\codex-clipboard-cd4a008f-4fcc-4cbe-b0f2-569cab337901.png")),
        ("图2  春生花园运营群：内容数据反馈与选题复用", Path(r"C:\Users\EDY\AppData\Local\Temp\codex-clipboard-845b2dd8-3cfa-4413-a494-706a16900492.jpg")),
        ("图3  牧云台运营群：平台审核与账号处理", Path(r"C:\Users\EDY\AppData\Local\Temp\codex-clipboard-1b35d51c-f0b5-42c3-b05c-b3ea70ac37af.jpg")),
        ("图4  祥和花园运营群：场地方对接与素材沟通", Path(r"C:\Users\EDY\AppData\Local\Temp\codex-clipboard-268a875a-cbf9-4112-97eb-c3a02619df5c.jpg")),
    ]
    doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    add_rich_text(p, "附录B：运营群协同截图（用户提供）", size=16)
    p = doc.add_paragraph()
    add_rich_text(p, "以下截图用于说明项目协同方式和执行过程，不作为单独的流量或成交证明。", default_color=GRAY, size=10)
    for caption, image in images:
        if not image.exists():
            continue
        cp = doc.add_paragraph()
        cp.paragraph_format.space_before = Pt(8)
        cp.paragraph_format.space_after = Pt(4)
        run = cp.add_run(caption)
        set_run_font(run, 10, color=DARK_BLUE, bold=True)
        ip = doc.add_paragraph()
        ip.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ip.paragraph_format.space_after = Pt(8)
        ip.add_run().add_picture(str(image), width=Inches(6.2))


def main():
    doc = Document()
    configure_document(doc)
    parse_markdown(doc, MD_PATH)
    add_screenshot_appendix(doc)
    doc.save(DOCX_PATH)
    print(DOCX_PATH)


if __name__ == "__main__":
    main()
