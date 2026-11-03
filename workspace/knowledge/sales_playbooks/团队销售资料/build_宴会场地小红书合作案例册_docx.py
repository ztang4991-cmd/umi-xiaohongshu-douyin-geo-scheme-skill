from pathlib import Path
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(r"C:\Users\EDY\mslearn-ai-agents")
ASSETS = ROOT / "UMI项目整理" / "02_客户数据与素材" / "素材" / "团队案例素材库_20260908"
OUTPUT = ROOT / "UMI项目整理" / "01_方案成品" / "output" / "docx" / "宴会场地小红书运营合作案例册_20260924.docx"
INK, TEAL, CORAL = "19342F", "236B61", "E56B56"
PALE, MUTED, WHITE = "EAF2EF", "5A6B6D", "FFFFFF"

def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)

def no_cell_border(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:val"), "nil")
        borders.append(el)

def set_font(run, size=None, color=INK, bold=False):
    name = "Microsoft YaHei"
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rpr.rFonts.set(qn("w:ascii"), name)
    rpr.rFonts.set(qn("w:hAnsi"), name)
    rpr.rFonts.set(qn("w:eastAsia"), name)
    if size is not None:
        run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    run.bold = bold

def fmt(p, before=0, after=6, line=1.15, align=None):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if align is not None:
        p.alignment = align

def text(doc, value, size=10.5, color=INK, bold=False, before=0, after=6, line=1.15, align=None):
    p = doc.add_paragraph()
    fmt(p, before, after, line, align)
    set_font(p.add_run(value), size, color, bold)
    return p

def label(doc, value):
    p = doc.add_paragraph(); fmt(p, after=5); set_font(p.add_run(value.upper()), 8.5, CORAL, True)

def heading(doc, number, title, subtitle):
    label(doc, f"{number} / CASE BOOK")
    p = doc.add_paragraph(); fmt(p, after=5); set_font(p.add_run(title), 23, INK, True)
    text(doc, subtitle, 10.5, MUTED, after=12, line=1.25)

def callout(doc, value, fill=PALE, color=TEAL):
    table = doc.add_table(rows=1, cols=1); table.alignment = WD_TABLE_ALIGNMENT.CENTER; table.autofit = False
    cell = table.cell(0, 0); cell.width = Inches(6.65); set_cell_shading(cell, fill); no_cell_border(cell)
    p = cell.paragraphs[0]; fmt(p, before=6, after=6, line=1.2); set_font(p.add_run(value), 9.5, color)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)

def cell_bullets(cell, items):
    for item in items:
        p = cell.add_paragraph(style="List Bullet"); fmt(p, after=4, line=1.15); set_font(p.add_run(item), 9.5, INK)

def case_page(doc, number, title, account, image_path, note, visible, discussion):
    doc.add_page_break(); heading(doc, number, title, account)
    table = doc.add_table(rows=1, cols=2); table.alignment = WD_TABLE_ALIGNMENT.CENTER; table.autofit = False
    left, right = table.rows[0].cells; left.width, right.width = Inches(3.45), Inches(3.0)
    for cell in (left, right): cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP; no_cell_border(cell)
    p = left.paragraphs[0]; fmt(p, after=4, align=WD_ALIGN_PARAGRAPH.CENTER); p.add_run().add_picture(str(image_path), width=Inches(3.05))
    p2 = left.add_paragraph(); fmt(p2, after=0, line=1.1, align=WD_ALIGN_PARAGRAPH.CENTER); set_font(p2.add_run(note), 8, MUTED)
    rp = right.paragraphs[0]; fmt(rp, after=4); set_font(rp.add_run("截图可直接支持"), 10.5, TEAL, True)
    cell_bullets(right, visible)
    rp2 = right.add_paragraph(); fmt(rp2, before=9, after=4); set_font(rp2.add_run("合作讨论切入"), 10.5, CORAL, True)
    rp3 = right.add_paragraph(); fmt(rp3, line=1.2); set_font(rp3.add_run(discussion), 10, INK)

def header_footer(section):
    hp = section.header.paragraphs[0]; fmt(hp, after=0, align=WD_ALIGN_PARAGRAPH.RIGHT); set_font(hp.add_run("宴会场地小红书运营合作案例 | 对外沟通版"), 8, MUTED)
    fp = section.footer.paragraphs[0]; fmt(fp, after=0, align=WD_ALIGN_PARAGRAPH.CENTER); set_font(fp.add_run("UMI  |  2026年9月24日  |  "), 8, MUTED)
    fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE"); fp._p.append(fld)

def cover(doc):
    p = doc.add_paragraph(); fmt(p, before=100, after=12); set_font(p.add_run("宴会场地"), 15, CORAL, True)
    p = doc.add_paragraph(); fmt(p, after=4, line=1.0); set_font(p.add_run("小红书运营"), 33, INK, True)
    p = doc.add_paragraph(); fmt(p, after=22, line=1.0); set_font(p.add_run("合作案例"), 33, TEAL, True)
    text(doc, "从账号呈现到客户咨询承接", 14, INK, True, after=8)
    text(doc, "用已留档的项目页面与协作记录，介绍我们如何理解宴会场地线上获客。", 11, MUTED, after=30, line=1.35)
    table = doc.add_table(rows=1, cols=1); table.autofit = False; table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0); cell.width = Inches(6.65); set_cell_shading(cell, TEAL); no_cell_border(cell)
    p = cell.paragraphs[0]; fmt(p, before=10, after=10); set_font(p.add_run("团队案例简册  |  对外沟通版  |  2026年9月"), 10.5, WHITE, True)
    callout(doc, "适用对象：正在评估线上获客、咨询承接与销售协同的宴会场地负责人。")
    text(doc, "本册不承诺平台排名、线索数量或成交结果；案例页只描述截图和已留档资料能够直接支持的事实。", 9, MUTED, before=170, after=0, line=1.25)

def chain_page(doc):
    doc.add_page_break(); heading(doc, "01", "账号之外，重视咨询承接", "让意向客户更快理解场地，也让场地知道询问从哪里来、该由谁接。")
    steps = [("被发现", "清楚展示地区、场地与可承接场景"), ("被理解", "通过真实内容回答空间、人数、价格等问题"), ("被咨询", "把档期、预算和服务需求导向明确入口"), ("被承接", "客资报备、责任人响应与线下沟通"), ("被复盘", "统一记录预约、报价与成交，判断下一步")]
    table = doc.add_table(rows=len(steps), cols=2); table.autofit = False; table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (title, desc) in enumerate(steps):
        c1, c2 = table.rows[i].cells; c1.width, c2.width = Inches(1.15), Inches(5.5)
        for c in (c1, c2): set_cell_shading(c, PALE if i % 2 == 0 else WHITE); no_cell_border(c); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c1.paragraphs[0]; fmt(p, before=7, after=7, align=WD_ALIGN_PARAGRAPH.CENTER); set_font(p.add_run(f"{i + 1:02d}"), 15, TEAL, True)
        p = c2.paragraphs[0]; fmt(p, before=7, after=1); set_font(p.add_run(title), 12.5, INK, True)
        p2 = c2.add_paragraph(); fmt(p2, after=7); set_font(p2.add_run(desc), 9.7, MUTED)
    text(doc, "团队负责人具有宴会垂直平台、OTA 酒店平台及线上运营平台相关经验，聚焦宴会场地线上获客、咨询承接和线下销售衔接。我们希望与具备承接能力、愿意协同复盘的场地合作。", 10.2, INK, after=9, line=1.28)
    callout(doc, "证据边界：主页说明账号呈现，工作群说明协作记录；均不能单独证明线索增量、到店率或成交额。")

def other_page(doc):
    doc.add_page_break(); heading(doc, "05", "其他项目与协作证据", "项目被列示，不等于每个项目具有相同服务范围或效果口径。")
    rows = [("春生花园", "幸福梅林", "企业微信客资群截图可见客户需求和内部协作信息；不对外附原图，未据此推断成交。"), ("介个院子", "三圣乡", "企业微信客资群截图可见客资报备及内部协作；已有账号诊断和旺季执行方案文件留档，不能据此认定已执行全部动作或取得结果。"), ("麓山宴", "双流", "企业微信运营群截图可见内容沟通及协作；不对外附原图，未据此推断平台效果。"), ("可悦私房菜", "三圣乡", "已有小红书运营方案和行动清单文件留档；项目实际执行范围和效果待补证据。"), ("臻里八号", "郫县", "团队正式项目名单中列示；尚缺可对外展示的账号页面和结果材料。")]
    table = doc.add_table(rows=1, cols=3); table.autofit = False; table.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths, headers = [1.25, 0.95, 4.45], ["项目", "区域", "当前可说明的事实"]
    for j, value in enumerate(headers):
        cell = table.rows[0].cells[j]; cell.width = Inches(widths[j]); set_cell_shading(cell, TEAL); no_cell_border(cell)
        p = cell.paragraphs[0]; fmt(p, before=7, after=7); set_font(p.add_run(value), 9.3, WHITE, True)
    for i, row in enumerate(rows):
        cells = table.add_row().cells
        for j, value in enumerate(row):
            cells[j].width = Inches(widths[j]); set_cell_shading(cells[j], PALE if i % 2 == 0 else WHITE); no_cell_border(cells[j]); cells[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cells[j].paragraphs[0]; fmt(p, before=6, after=6, line=1.15); set_font(p.add_run(value), 8.7 if j == 2 else 9.2, INK if j < 2 else MUTED, j < 2)
    callout(doc, "企业微信原图不附在本册中。任何客资报备记录均不等于成交结果，正式外发前仍需核对项目名称、授权、实际服务范围和可公开数据。", "FFF3EF", CORAL)

def close_page(doc):
    doc.add_page_break(); heading(doc, "06", "先聊一次场地现状", "合作前先确认目标客户、现有内容素材和销售承接能力。")
    questions = ["目前最希望获得哪类宴会客户？", "场地有哪些可直接展示的真实空间与服务证据？", "谁负责回复咨询、安排到场和记录报价？"]
    table = doc.add_table(rows=3, cols=2); table.autofit = False; table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, q in enumerate(questions):
        c1, c2 = table.rows[i].cells; c1.width, c2.width = Inches(0.75), Inches(5.9)
        for c in (c1, c2): set_cell_shading(c, PALE); no_cell_border(c)
        p = c1.paragraphs[0]; fmt(p, before=8, after=8, align=WD_ALIGN_PARAGRAPH.CENTER); set_font(p.add_run(f"0{i + 1}"), 14, TEAL, True)
        p = c2.paragraphs[0]; fmt(p, before=8, after=8); set_font(p.add_run(q), 11, INK, True)
    text(doc, "建议的第一步", 12, INK, True, before=24, after=6)
    text(doc, "先做一次资料核对与账号诊断：明确目标客群、场景素材、咨询入口和承接责任人，再决定内容生产、账号优化和销售协同的优先级。", 10.5, INK, after=18, line=1.3)
    text(doc, "外发与试运行前核对", 11, INK, True, after=5)
    text(doc, "项目名称与截图授权；各项目实际服务范围；现有咨询、预约、报价和成交数据的统一口径。", 9.8, MUTED, after=26, line=1.25)
    callout(doc, "欢迎联系发送本资料的团队成员，约一次针对场地的沟通。", TEAL, WHITE)
    text(doc, "当前仍缺的外发素材：对外联系方式或二维码、项目授权、更多项目主页/笔记截图、服务范围与合作时间、可公开的咨询/到店/报价/成交数据、客户评价或合作方确认语。", 9, MUTED, before=115, after=0, line=1.25)

def main():
    doc = Document(); section = doc.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.top_margin, section.bottom_margin = Inches(0.65), Inches(0.55)
    section.left_margin, section.right_margin = Inches(0.75), Inches(0.75)
    header_footer(section)
    normal = doc.styles["Normal"]; normal.font.name = "Microsoft YaHei"; normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei"); normal.font.size = Pt(10.5)
    doc.styles["List Bullet"].font.name = "Microsoft YaHei"; doc.styles["List Bullet"]._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    cover(doc); chain_page(doc)
    case_page(doc, "02", "祥和花园", "账号页面：祥和花园一站式宴会艺术中心", ASSETS / "02_祥和" / "02_小红书主页_祥和花园.png", "团队案例库 / 祥和主页", ["账号定位与宴会空间呈现", "场地图片及内容栏目", "了解场地、档期、套餐及价格等咨询导向"], "场景呈现之后，如何把档期、价格、人数等询问准确转交给场地销售？")
    case_page(doc, "03", "悦哉", "截图账号原名：乐哉餐饮；项目名称口径待客户确认", ASSETS / "03_悦哉" / "02_小红书主页_乐哉餐饮.png", "团队案例库 / 乐哉餐饮主页", ["户外婚礼场地", "草坪婚礼", "私宴聚餐等内容场景"], "不同宴会场景在账号主页如何被清晰区分，方便客户快速判断是否适合？")
    case_page(doc, "04", "牧云台", "账号页面：三圣乡牧云台", ASSETS / "04_牧云台" / "02_小红书主页_牧云台.png", "团队案例库 / 牧云台主页", ["婚宴、商宴、民宿等业务场景", "庭院下午茶与活动内容", "多业务场地的统一账号呈现"], "多业务场地如何让目标客户在同一账号里迅速找到相关场景和咨询入口？")
    other_page(doc); close_page(doc)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.core_properties.title = "宴会场地小红书运营合作案例册"; doc.core_properties.subject = "ToB合作沟通材料"; doc.core_properties.author = "UMI"
    doc.save(str(OUTPUT)); print(OUTPUT)

if __name__ == "__main__": main()
