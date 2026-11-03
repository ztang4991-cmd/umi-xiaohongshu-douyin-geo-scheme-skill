from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from pathlib import Path

OUT = Path(r"C:\Users\EDY\mslearn-ai-agents\deliverables\福气东来酒店新都大丰门店小红书诊断与90天落地运营方案.docx")

NAVY = "17324D"
RED = "B33A3A"
GOLD = "B88746"
LIGHT = "F5F1EA"
PALE_BLUE = "EAF1F7"
GRAY = "5F6873"
DARK = "24313D"

def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:fill'), fill)

def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in('w:tcBorders')
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        if edge in kwargs:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ['val', 'sz', 'space', 'color']:
                if key in kwargs[edge]:
                    element.set(qn('w:{}'.format(key)), str(kwargs[edge][key]))

def set_cell_margins(cell, top=90, start=110, bottom=90, end=110):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in('w:tcMar')
    if tcMar is None:
        tcMar = OxmlElement('w:tcMar')
        tcPr.append(tcMar)
    for m, v in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = tcMar.find(qn('w:' + m))
        if node is None:
            node = OxmlElement('w:' + m)
            tcMar.append(node)
        node.set(qn('w:w'), str(v))
        node.set(qn('w:type'), 'dxa')

def set_run_font(run, name='Microsoft YaHei', size=10.5, color=DARK, bold=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:ascii'), name)
    run._element.rPr.rFonts.set(qn('w:hAnsi'), name)
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)

def style_paragraph(p, before=0, after=6, line=1.25, keep=False):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if keep:
        pf.keep_with_next = True

def add_text(p, text, bold=False, color=DARK, size=10.5):
    r = p.add_run(text)
    set_run_font(r, size=size, color=color, bold=bold)
    return r

def add_para(doc, text='', style=None, before=0, after=6, line=1.25, color=DARK, size=10.5, bold=False, align=None):
    p = doc.add_paragraph(style=style)
    if text:
        add_text(p, text, bold=bold, color=color, size=size)
    style_paragraph(p, before=before, after=after, line=line)
    if align is not None:
        p.alignment = align
    return p

def add_bullet(doc, label, text, level=0):
    p = doc.add_paragraph(style='List Bullet' if level == 0 else 'List Bullet 2')
    add_text(p, label, bold=True, color=NAVY)
    add_text(p, text)
    style_paragraph(p, after=3, line=1.18)
    return p

def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f'Heading {level}')
    add_text(p, text, bold=True, color=NAVY if level == 1 else RED, size=15 if level == 1 else 11.5)
    style_paragraph(p, before=12 if level == 1 else 7, after=5, line=1.1, keep=True)
    return p

def add_callout(doc, title, text, fill=PALE_BLUE):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.cell(0,0)
    set_cell_shading(cell, fill)
    set_cell_margins(cell, top=130, start=170, bottom=130, end=170)
    set_cell_border(cell, top={'val':'single','sz':'6','color':GOLD}, bottom={'val':'single','sz':'6','color':GOLD}, left={'val':'single','sz':'6','color':GOLD}, right={'val':'single','sz':'6','color':GOLD})
    p = cell.paragraphs[0]
    add_text(p, title + '  ', bold=True, color=RED, size=10.5)
    add_text(p, text, size=10.5)
    style_paragraph(p, after=0, line=1.18)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)

def add_table(doc, headers, rows, widths=None, font_size=8.8):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    # Repeat the header when a long table flows onto another page.
    trPr = t.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        set_cell_shading(hdr[i], NAVY)
        set_cell_margins(hdr[i], top=100, start=90, bottom=100, end=90)
        set_cell_border(hdr[i], top={'val':'single','sz':'4','color':'FFFFFF'}, bottom={'val':'single','sz':'4','color':'FFFFFF'}, left={'val':'single','sz':'4','color':'FFFFFF'}, right={'val':'single','sz':'4','color':'FFFFFF'})
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_text(p, h, bold=True, color='FFFFFF', size=font_size)
        style_paragraph(p, after=0, line=1.05)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        rowPr = t.rows[-1]._tr.get_or_add_trPr()
        cantSplit = OxmlElement('w:cantSplit')
        rowPr.append(cantSplit)
        for ci, value in enumerate(row):
            cells[ci].text = ''
            set_cell_margins(cells[ci], top=85, start=90, bottom=85, end=90)
            set_cell_shading(cells[ci], 'FFFFFF' if ri % 2 == 0 else LIGHT)
            set_cell_border(cells[ci], top={'val':'single','sz':'3','color':'D6DCE2'}, bottom={'val':'single','sz':'3','color':'D6DCE2'}, left={'val':'single','sz':'3','color':'D6DCE2'}, right={'val':'single','sz':'3','color':'D6DCE2'})
            cells[ci].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cells[ci].paragraphs[0]
            add_text(p, str(value), size=font_size, color=DARK)
            style_paragraph(p, after=0, line=1.08)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return t

def add_source(doc, label, url, note):
    p = doc.add_paragraph()
    add_text(p, label + '：', bold=True, color=NAVY, size=8.5)
    add_text(p, note + ' ', size=8.5, color=GRAY)
    add_text(p, url, size=8.2, color='2E6A99')
    style_paragraph(p, after=3, line=1.08)

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.65)
sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.7)
sec.right_margin = Inches(0.7)
sec.header_distance = Inches(0.3)
sec.footer_distance = Inches(0.3)

styles = doc.styles
styles['Normal'].font.name = 'Microsoft YaHei'
styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
styles['Normal'].font.size = Pt(10.5)
for name in ['Heading 1','Heading 2']:
    styles[name].font.name = 'Microsoft YaHei'
    styles[name]._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    styles[name].font.color.rgb = RGBColor.from_string(NAVY)
    styles[name].paragraph_format.keep_with_next = True

# Header and footer
header = sec.header.paragraphs[0]
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
add_text(header, '聚尤米 UMI  |  婚嫁垂类线上运营', color=GRAY, size=8.2)
style_paragraph(header, after=0, line=1.0)
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_text(footer, '福气东来酒店新都大丰门店  |  小红书落地运营方案  |  2026年9月4日', color=GRAY, size=8.2)
style_paragraph(footer, after=0, line=1.0)

# Cover
p = doc.add_paragraph()
style_paragraph(p, before=38, after=8, line=1.0)
add_text(p, '福气东来酒店', bold=True, color=RED, size=16)
p = doc.add_paragraph()
style_paragraph(p, after=10, line=1.0)
add_text(p, '新都大丰门店小红书诊断与90天落地运营方案', bold=True, color=NAVY, size=24)
p = doc.add_paragraph()
style_paragraph(p, after=24, line=1.2)
add_text(p, '从账号体检到新都市场破局的执行方案', color=GRAY, size=12)
add_callout(doc, '本方案先给结论', '福气东来当前的核心问题不是“没有卖点”，而是卖点没有被稳定、具体、可搜索地表达。90天工作重点是把账号从零散宣传号，做成“新都大丰婚宴决策入口”：用户能搜到、看懂、比较、咨询，并且有人及时跟进。', fill='F8F0E8')
add_para(doc, '汇报对象：福气东来酒店新都大丰门店负责人', color=GRAY, size=9.5, after=2)
add_para(doc, '方案日期：2026年9月4日', color=GRAY, size=9.5, after=2)
add_para(doc, '服务范围：小红书账号诊断、内容运营、私信承接、数据复盘；本版不含美团执行。', color=GRAY, size=9.5, after=20)
doc.add_page_break()

add_heading(doc, '一 项目范围与判断', 1)
add_para(doc, '本方案服务对象为福气东来酒店新都大丰门店，重点解决“账号现在是什么状态、市场上谁在抢同一批新人、我们如何在新都变得更容易被选择、接下来每周具体做什么”。公开平台数据只代表可见样本，不等于门店后台经营数据；涉及餐标、地址、厅型、桌数、套餐包含项目的内容，必须经门店负责人确认后再公开发布。', after=8)
add_callout(doc, '白话解释：GEO', 'GEO（让 AI 搜索更容易理解和引用品牌内容）在本项目中不另起炉灶，先通过清晰的标题、问答、地点、桌数、预算和服务信息，把门店内容整理成搜索引擎和用户都能读懂的结构。')
add_heading(doc, '1.1 当前结论', 2)
add_bullet(doc, '账号基础：', '账号名为“福气东来酒店”，公开主页可见 3 条视频笔记；可见互动为 0-1 赞，当前没有形成连续的内容资产。')
add_bullet(doc, '定位线索：', '已公开出现“成都新开新中式庭院宴会酒店”“超私密高奢”“新鲜食材、锅气十足”等表达，说明门店具备新中式庭院和宴席品质两条可发展的卖点。')
add_bullet(doc, '最大短板：', '没有把用户最先要问的地址、交通、能办多少桌、餐标区间、是否一站式、看场怎么预约写清楚。')
add_bullet(doc, '竞争态势：', '新都公开内容中，缤纷盛宴、艾悦映江南、恒杏花园艺术酒店、顺庭等都在用“新开、主题厅、预算、桌数、全包、出片”抢搜索注意力；至臻盛宴也已公开预售。')
add_bullet(doc, '破局方向：', '不和新场地只比“谁更漂亮”，而是建立“新中式庭院私密感 + 大丰近场便利 + 真实宴席品质 + 顾问式选择服务”的组合认知。')

add_heading(doc, '1.2 需要门店在启动前确认的事实', 2)
add_table(doc, ['信息项','必须确认的内容','用于哪些动作'], [
    ['门店地址','完整地址、导航关键词、停车入口、地铁/公交、周边地标','主页简介、路线笔记、评论回复'],
    ['厅型与容量','厅名、层高、面积、柱体情况、舞台、迎宾区、独立卫生间；每厅可接桌数','厅型对比、用户匹配、首图排序'],
    ['价格口径','婚宴餐标、最低桌数、旺淡季、是否含服务费/婚庆/四大金刚/布置','标题、私信报价、活动内容'],
    ['餐饮证据','菜单版本、菜品照片、出品流程、试菜政策、儿童/老人友好菜品','菜品实拍、试菜内容、信任建设'],
    ['服务与档期','婚礼管家、婚庆合作边界、可预约看场时段、近期空档','私信承接、预约表、档期内容'],
    ['案例授权','近三个月婚礼、寿宴、宝宝宴、企业宴会的照片/视频和肖像授权','真实案例、客户口碑、复盘素材'],
], widths=[1.2,3.0,2.5], font_size=8.7)
add_callout(doc, '执行纪律', '未确认的数字不写进标题，未获得授权的客片不公开发布；所有“起”“全包”“送”“限时”等词，先由门店确认适用条件。')

add_heading(doc, '二 福气东来小红书账号诊断', 1)
add_para(doc, '诊断时间：2026年9月4日。方法是查看公开主页、检索账号名和逐条读取可见笔记；未登录商家后台，因此不对粉丝画像、曝光、收藏、私信和历史删除内容做推断。', after=8)
add_table(doc, ['诊断维度','公开可见情况','判断','优先级'], [
    ['内容数量','主页可见 3 条视频笔记','账号仍处于内容冷启动阶段','P0（马上做）'],
    ['内容主题','宴席口碑、食材出品、新婚祝福','主题过散，用户无法快速判断“适不适合我”','P0'],
    ['信息完整度','未见地址、厅型、桌数、餐标、预约路径的成套说明','搜索用户无法完成比较，容易转去看竞品','P0'],
    ['标题表达','有“成都酒店/宴会厅”“新中式庭院”“高奢”等词，但没有具体场景和决策信息','有方向，没有搜索落点','P1（两周内）'],
    ['互动表现','公开可见笔记互动 0-1 赞，未见稳定评论讨论','当前不能证明内容已形成有效获客','P1'],
    ['信任证据','暂未形成连续客片、菜单、服务流程、客户评价系列','缺少“看完就敢咨询”的证据链','P1'],
], widths=[1.15,2.4,2.9,0.8], font_size=8.5)
add_heading(doc, '2.1 账号问题拆解', 2)
add_bullet(doc, '主页没有第一眼答案：', '简介要在一行内说清“在哪、办什么宴、有什么特色、怎么预约”，而不是只留形容词。')
add_bullet(doc, '笔记像单点宣传：', '用户需要的是“我有 18/25/35 桌，预算多少，选哪个厅，怎么到店”，而不是只看一句祝福或一句口号。')
add_bullet(doc, '没有内容分工：', '后续用“场地搜索、宴席品质、预算答疑、真实案例、顾问邀约”五类栏目固定输出。')
add_bullet(doc, '没有承接动作：', '每篇笔记只设置一个动作，例如“评论区留下桌数和日期，发你匹配建议”，避免多个电话、二维码、私信口径互相冲突。')
add_bullet(doc, '没有复盘基线：', '首周先记录曝光、点击主页、收藏、评论、私信、有效线索（有日期/桌数/预算三项中的两项以上）和到店预约，第二周再设提升目标。')

add_heading(doc, '2.2 主页改造清单', 2)
add_table(doc, ['位置','建议改法','验收标准'], [
    ['昵称','福气东来酒店｜新都大丰婚宴（以平台可用字符为准）','包含品牌、区域、核心场景'],
    ['简介','新都大丰新中式庭院宴会酒店｜婚宴/寿宴/宝宝宴/商务宴｜支持预约看场｜私信“桌数+日期”获取匹配建议','用户读完知道做什么、在哪、怎么问'],
    ['头像与封面','使用门店识别度高的门头或庭院主景，避免模糊合成图','缩小后仍能识别品牌'],
    ['置顶 1','门店总览：地址、交通、庭院、厅型、可办场景','新访客 30 秒了解门店'],
    ['置顶 2','宴席品质：菜单、热菜出品、试菜、服务流程','回答“菜好不好、服务稳不稳”'],
    ['置顶 3','预算与预约：餐标口径、桌数匹配、看场流程','回答“要花多少、如何开始”'],
], widths=[1.0,4.0,2.2], font_size=8.7)

add_heading(doc, '三 成都新都婚宴市场理解', 1)
add_para(doc, '本节的市场判断来自 2026 年公开小红书检索样本和竞品官方笔记，不把平台结果当作完整市场统计。样本显示，新都婚宴竞争已经从“有没有场地”进入“谁能在用户搜索和比较阶段先建立信任”的阶段。', after=8)
add_table(doc, ['公开观察','证据表现','对福气东来的含义'], [
    ['新场地密集出现','2026 年公开内容中，缤纷盛宴、艾悦映江南、恒杏花园艺术酒店、至臻盛宴均有新开/预售/新厅传播','新品会持续吸走平台注意力，必须建立稳定更新而非一次开业宣传'],
    ['价格成为点击入口','缤纷公开笔记出现 899、1299；艾悦、恒杏公开内容多次出现 1 万出头或 2 万预算表达','不能回避预算问题，但要把“价格 + 包含内容 + 适用桌数”一起说明'],
    ['桌数与厅型是核心比较项','顺庭公开笔记直接给出 7 厅、15-80 桌、层高、面积和风格','福气东来需要尽快完成自己的厅型资料卡，否则用户会默认竞品更专业'],
    ['用户看重“好看”也看重“好办”','公开标题集中在出片、全包、停车、地铁、庭院、花园、食材、无柱等词','内容必须同时拍氛围和动线，把审美转成可执行的选择依据'],
    ['新都与大丰是近场决策','公开搜索中反复出现“新都备婚”“新都大丰”“斑竹园”等区域词','区域词要进入昵称、标题、正文、话题和评论，而不是只写“成都酒店”'],
], widths=[1.35,3.2,2.6], font_size=8.6)
add_heading(doc, '3.1 用户决策链路', 2)
add_para(doc, '用户通常先在小红书用区域词和场景词找灵感，再用桌数、预算、风格和交通筛选，最后通过私信、电话或预约看场确认。运营要做的是把每一个“还没决定”的问题，提前变成一篇能收藏的答案。', after=6)
add_table(doc, ['阶段','用户心里在问什么','福气东来要给出的内容'], [
    ['发现','新都/大丰有没有新中式庭院婚宴？','庭院主景、门店氛围、短视频动线'],
    ['比较','25 桌、35 桌、50 桌分别适合什么？','厅型与桌数对比卡，明确适合人群'],
    ['核实','餐标包含什么？菜品是否现做？停车方便吗？','菜单、出品、停车入口、服务流程'],
    ['咨询','我的日期还有档期吗？预算能不能做？','私信收集表：日期、桌数、预算、偏好'],
    ['到店','看场要看哪些细节？','看场清单、路线、接待人、试菜说明'],
], widths=[1.0,2.7,3.4], font_size=8.8)

add_heading(doc, '四 新都重点竞品核验与应对', 1)
add_para(doc, '以下事实均来自小红书公开搜索与笔记详情的两轮核验。价格和宣传卖点可能随活动变化，方案只用来判断竞争方向，不建议直接照抄竞品的价格话术。', after=8)
add_table(doc, ['场地','已核验公开信息','竞争强项','福气东来应对'], [
    ['缤纷盛宴','官方笔记：餐标 1299 起；大宴会厅 50-75 桌、小宴会厅 5-10 桌、星河厅 50-70 桌、莫奈花园厅 30-46 桌；无柱；棋牌室、茶室、休息区；另有公开笔记出现 899 起/70 桌表达','低价入口、大桌数、花园与新店话题','不跟随“最低价”单点竞争，强化新中式庭院私密感、宴席品质和近场到店体验；所有价格以真实口径为准'],
    ['艾悦婚礼艺术中心（映江南店）','官方笔记：歌剧魅影/琉金厅 30 桌、挑高 7.2 米；coco 香奈儿/水晶厅 50 桌、挑高 5 米；森爱厅 30 桌、挑高 7.2 米；浮光厅 20 桌、挑高 5 米；均强调无柱与主题设计','主题厅命名强、风格细分、预算内容高频','福气东来要做“庭院风格 + 桌数 + 预算 + 适合人群”四项合一的选择卡，避免只发空镜'],
    ['恒杏花园艺术酒店','官方笔记：斥资 6000 万、32 亩独立花园、3 大户外婚礼区、4 大艺术主题厅、4 大仪式堂、6 个小宴厅、千平棋牌室等；公开笔记还有 2 万全包表达','大体量、艺术花园、全场景宴会、投资故事','不在体量上硬碰，建立“更私密、更适合近场家庭宴请、顾问更细致”的差异；用真实服务细节证明高质感'],
    ['至臻盛宴','官方账号公开笔记：2026 年全新打造宴会中心，3 大流行元素主题婚礼堂，档期开启预售；未核验到稳定地址、价格、厅型硬数据','新开预售和新鲜感','列入每周监测，不引用未核验数据；提前抢占“新都新中式庭院/大丰宴会”相关内容'],
    ['顺庭宴会中心（隔壁，最大竞争对手）','官方两条笔记相互印证：7 大宴会厅；中庭 A 30-80 桌、9.8 米、约 1300 平；中庭 B 15-40 桌、9.8 米、约 600 平；韩式厅 20-50 桌、8 米、约 700 平；另有云锦、锦华、臻爱、幸福厅；强调一站式、停车、厨房鲜制','厅型资料完整、桌数覆盖广、内容更新持续、邻近比较优势','不回避邻近竞争，改打“庭院私密宴 + 菜品真实体验 + 预约顾问服务”；每周监测其新厅、价格、客片和评论问题'],
], widths=[1.25,3.15,1.45,2.0], font_size=7.8)
add_callout(doc, '市场破局句', '让用户在“新都大丰婚宴怎么选”这个问题里，先想到福气东来的不是某个最低餐标，而是一家有新中式庭院氛围、宴席品质说得清、桌数匹配有人帮、到店体验不折腾的酒店。', fill='F8F0E8')

add_heading(doc, '4.1 竞品监测表', 2)
add_table(doc, ['每周监测项','记录方式','触发动作'], [
    ['新笔记与新厅','记录标题、发布日期、主题、互动、是否官方账号','发现同类卖点被重复使用时，调整福气东来选题角度'],
    ['价格与活动','只记录公开出现的价格和适用条件，截图留档','门店确认后再决定是否跟价或做价值解释'],
    ['评论问题','整理用户反复问的桌数、交通、餐标、档期、菜品','在福气东来主页和笔记中提前回答'],
    ['客片与口碑','区分官方、达人、真实客人内容','寻找可合作达人和可授权客户案例'],
], widths=[1.5,3.4,2.8], font_size=8.6)

add_heading(doc, '五 账号定位与内容架构', 1)
add_para(doc, '账号定位建议：官方品牌号 + 新都大丰婚宴顾问入口。品牌号负责让人看懂场地与宴席，评论和私信负责把具体需求接住。后续如门店有真实顾问，可开设个人顾问号，但不建议在基础账号尚未稳定前盲目扩号。', after=8)
add_table(doc, ['栏目','白话解释','用户问题','首批选题示例'], [
    ['庭院实景','把场地走一遍给用户看','这里到底好不好看、私不私密？','新都大丰新中式庭院婚宴，白天和夜晚一次看完'],
    ['桌数匹配','按人数帮用户选厅','我有 18/25/35 桌，怎么选？','25 桌婚宴怎么选厅？看这张福气东来匹配表'],
    ['预算拆解','把钱花在哪里说清楚','预算够不够、有没有隐形项？','2 万预算办婚宴，先问清这 6 项'],
    ['宴席品质','让用户看到菜和出品过程','菜好不好、是不是预制？','一桌宴席从厨房到上桌，真实记录'],
    ['真实案例','用真实客户证明服务','别人办完感觉怎么样？','一场 26 桌婚礼的布置、上菜与宾客动线'],
    ['顾问答疑','把咨询变成有人帮助的过程','我该什么时候看场、怎么预约？','发我日期+桌数+预算，帮你做第一轮匹配'],
], widths=[1.05,1.55,2.0,3.0], font_size=8.3)
add_heading(doc, '5.1 内容标准', 2)
add_bullet(doc, '标题：', '区域词 + 场景词 + 一个具体问题；例如“新都大丰婚宴｜25 桌怎么选厅？先看这 4 个细节”。')
add_bullet(doc, '封面：', '一张真实场景图 + 8-14 字核心信息；不把文字堆满，不用过度磨皮或与现场不一致的效果图。')
add_bullet(doc, '正文：', '先给结论，再给 3-5 个证据，最后只留一个咨询动作。')
add_bullet(doc, '评论：', '首条评论补充地址/适用条件；对桌数、预算、日期问题 2 小时内响应，营业时段尽量 30 分钟内响应。')
add_bullet(doc, '标签：', '优先使用“新都婚宴、新都大丰婚宴、成都北门婚宴、新都婚礼堂、新中式婚礼、庭院婚宴、宝宝宴/寿宴”等与内容一致的词。')

add_heading(doc, '六 90天落地动作', 1)
add_heading(doc, '6.1 第一阶段 0-7天 先把基础补齐', 2)
add_table(doc, ['动作','具体做法','交付/验收'], [
    ['资料盘点','门店现场拍摄；核对地址、厅型、桌数、价格、菜单、服务、档期','1 份门店事实表；所有数字有负责人签字确认'],
    ['主页改造','昵称、简介、头像、封面、置顶三篇重做','用户从主页能知道在哪、办什么、如何咨询'],
    ['内容资产','拍庭院全景、厅内动线、厨房/菜品、停车、卫生间、迎宾和新娘房（如有）','建立 100 张以上可用照片和 10 条以上短视频素材'],
    ['私信承接','统一问询表和回复话术，记录日期、桌数、预算、偏好、来源','每条有效咨询有编号、有跟进人、有下一步'],
    ['首批选题','按五大栏目排出 20 个标题，先做 6 篇基础内容','首周至少上线 4 篇，避免连续同一模板'],
], widths=[1.15,3.6,2.4], font_size=8.5)
add_heading(doc, '6.2 第二阶段 8-30天 建立搜索入口', 2)
add_bullet(doc, '每周发布 4-5 篇：', '2 篇场地/厅型，1 篇宴席品质，1 篇预算或避坑，1 篇真实案例/顾问答疑。')
add_bullet(doc, '做 3 个系列：', '“新都大丰婚宴怎么选厅”“福气东来一桌宴席记录”“看场前先问这 6 件事”。系列名固定，方便收藏和持续追更。')
add_bullet(doc, '建立评论词库：', '把用户常问的地址、停车、桌数、餐标、档期、试菜、宝宝宴、寿宴问题，整理成可快速调用的白话回复。')
add_bullet(doc, '做一次小预算测试：', '只推广已经有自然收藏/评论的 1-2 篇内容，测试不同封面和标题，不在冷启动期盲目放大低质量内容。')
add_heading(doc, '6.3 第三阶段 31-60天 让内容变成信任', 2)
add_bullet(doc, '真实案例连续化：', '每场案例拆成“准备日、布置、迎宾、宴席、结束复盘”多篇，避免只发一张大合照。')
add_bullet(doc, '顾问出镜：', '用固定人物回答预算、日期和桌数问题，展示真实接待过程，不把个人号做成重复广告号。')
add_bullet(doc, '达人与客户共创：', '优先邀请本地婚嫁、备婚、家庭宴请类小体量创作者到店体验；合作内容必须标明合作关系，客片先取得授权。')
add_bullet(doc, '月度复盘：', '按“曝光→主页点击→收藏/评论→私信→有效线索→预约到店”逐层判断问题，调整下一月栏目配比。')
add_heading(doc, '6.4 第四阶段 61-90天 做区域心智', 2)
add_bullet(doc, '形成年度内容节点：', '围绕国庆、年底宴会、春节前家庭宴请、2027 好日子等节点提前 4-6 周准备内容。')
add_bullet(doc, '做比较型内容：', '不点名贬低竞品，围绕“庭院/室内、20/30/50 桌、婚宴/宝宝宴/商务宴”给出选择方法。')
add_bullet(doc, '沉淀可复用资产：', '形成门店介绍页、厅型卡、菜单卡、看场清单、私信话术、月报模板，后续由门店持续使用。')

add_heading(doc, '七 私信与到店转化流程', 1)
add_para(doc, '白话解释：转化率就是“看到内容的人里，有多少人真正咨询、到店或下单”。我们不只看点赞，而是把每一条有效咨询都接住并能追踪下一步。', after=8)
add_table(doc, ['节点','标准动作','记录字段'], [
    ['评论/私信进入','先回答问题，再追问 3 项：日期、桌数、预算；不要一上来只发电话','来源笔记、时间、用户昵称、需求摘要'],
    ['初步匹配','按桌数与预算给 1-2 个适合方向，说明仍需现场确认','推荐厅型、价格口径、待确认项'],
    ['预约看场','给可选时段、地址、停车说明、接待人姓名和电话','预约时间、到店人数、负责人'],
    ['到店接待','按“环境→厅型→菜品→服务→费用”顺序讲解，现场不临时改变口径','到店结果、异议、下一步'],
    ['跟进与复盘','24 小时内发资料，3 天内一次轻提醒；拒绝骚扰式频繁追问','状态：待定/已定/暂缓/无效；失单原因'],
], widths=[1.25,4.0,2.25], font_size=8.5)
add_callout(doc, '建议的私信首句', '“可以的，我先按你的情况帮你匹配。方便告诉我婚期、预计桌数和大概预算吗？如果日期还没定，也可以先发桌数和喜欢的风格。”', fill='F8F0E8')

add_heading(doc, '八 数据指标与复盘机制', 1)
add_para(doc, '以下是运营目标值，不是平台承诺；首月以真实基线校准。重点看“有效线索和到店”，不以虚假互动、刷量或违规导流作为手段。', after=8)
add_table(doc, ['层级','指标','首月建议目标','复盘动作'], [
    ['内容质量','收藏率、评论率、主页点击率','以首周基线为准，第二周起逐周提升 20%','保留高收藏选题，重做低点击封面'],
    ['线索质量','有效私信数（日期/桌数/预算至少两项）','每周形成可追踪的有效线索清单','检查标题、评论钩子和回复速度'],
    ['到店转化','预约看场数、到店率','以门店接待能力设月度上限，避免过度承诺','分析失约、暂缓和失单原因'],
    ['服务效率','工作时段首响、跟进完成率','首响 30 分钟内；24 小时跟进率 100%','超时记录责任和原因'],
    ['品牌资产','可授权客片、真实评价、可复用素材量','每月沉淀至少 2 个完整案例包','检查授权、拍摄和归档'],
], widths=[1.15,2.2,2.2,2.8], font_size=8.4)
add_heading(doc, '8.1 周报内容', 2)
add_para(doc, '每周一页即可：本周发布清单、最高/最低表现内容、用户高频问题、有效线索与预约、竞品新动态、下周调整。月报增加“内容投入与到店结果”的关联说明，避免只报曝光。', after=8)

add_heading(doc, '九 服务内容与合作边界', 1)
add_table(doc, ['服务模块','我们负责','门店需要配合'], [
    ['策略与策划','账号定位、栏目、关键词、月度选题和排期','确认事实口径、活动和主推方向'],
    ['内容生产','脚本、拍摄规划、图文/视频编辑、发布与基础评论维护','提供拍摄场地、人员、菜品、案例和授权'],
    ['线索承接','统一私信话术、线索表、预约提醒、周度复盘','指定接待负责人，保证到店体验和报价一致'],
    ['数据与优化','周报、月报、竞品监测、标题/封面测试','提供后台数据与成交/失单反馈'],
], widths=[1.35,3.55,3.0], font_size=8.5)
add_para(doc, '运营费用在整体合作中按双方确认的月度服务范围执行，方案不展开报价表。投放、达人合作、额外拍摄和大规模活动，须在测试目标、素材授权和预算上单独确认。任何“保曝光、保成交、保 ROI”的承诺均不属于本方案。', after=8)
add_callout(doc, '合规边界', '不刷量、不买虚假评价、不冒充客户、不隐瞒商业合作、不发布未经授权的肖像和菜单信息；价格、档期、赠品和“全包”必须写清适用条件。')

add_heading(doc, '十 启动清单', 1)
add_table(doc, ['启动前 3 个工作日内完成','负责人','完成标志'], [
    ['确认地址、厅型、桌数、餐标、菜单和包含项目','门店负责人','事实表签字/微信确认'],
    ['确定 1 个主推厅/主推宴会场景和 1 个辅助场景','门店负责人+运营','写入首月内容排期'],
    ['安排半天门店拍摄与一场真实案例拍摄','门店+运营','素材清单完成并归档'],
    ['指定 1 名私信和到店负责人','门店负责人','工作时间和联系方式明确'],
    ['开通/确认后台数据查看权限','门店负责人','可查看笔记和私信数据'],
    ['确认价格、赠品、肖像授权和发布审核流程','双方','形成一页审核规则'],
], widths=[4.35,1.35,2.2], font_size=8.5)

add_heading(doc, '附录 调研来源与核验说明', 1)
add_para(doc, '核验时间：2026年9月4日。平台公开内容会更新或下架，以下链接用于保留本次判断的来源线索。竞品数据采用“官方账号笔记详情 + 同账号/同关键词二次检索”交叉核对；未能完成二次核验的信息不写入硬数据。', after=8)
add_source(doc, '福气东来账号主页', 'https://www.xiaohongshu.com/user/profile/6a5da6d90000000010001003?xsec_token=ABJumTg_Yd3HPzkBHWFPx6Tg7IuQvcsb-dIGrY20KxAKo%3D&xsec_source=pc_search', '公开主页可见 3 条笔记；账号诊断基于公开页面。')
add_source(doc, '福气东来可见笔记', 'https://www.xiaohongshu.com/user/profile/6a5da6d90000000010001003/6a6d52eb00000000280321e0?xsec_token=ABj1DAPZk04Wcz5ZIRkBE2heczPsrK--6sp7Jjn_Laew0%3D&xsec_source=pc_user', '笔记标题为“成都新开新中式庭院宴会酒店｜超私密高奢”，可见 1 赞、0 收藏、0 评论。')
add_source(doc, '缤纷盛宴官方笔记', 'https://www.xiaohongshu.com/search_result/69c621bf00000000220008f2?xsec_token=AB8gK48ETc_EpyFOlOn6rd8-lKDFVDdK5wVk2OkjvJSYg=&xsec_source=', '核验餐标、厅型桌数、无柱、棋牌室/茶室等公开表达。')
add_source(doc, '艾悦映江南官方笔记', 'https://www.xiaohongshu.com/search_result/6964660d000000001a033c5d?xsec_token=ABvj9VdHIpOM-yL8k5Lii3-nEOkziVFlF_QDIo9hpNLuQ=&xsec_source=', '核验四个主题厅、桌数、层高和无柱表达。')
add_source(doc, '恒杏花园艺术酒店官方笔记', 'https://www.xiaohongshu.com/search_result/698da9a7000000001600886b?xsec_token=ABPRLsvcParkuvyG_80OTC1t14Bir5PrrYp3lrdrpfreo=&xsec_source=', '核验 6000 万、32 亩、户外区、主题厅和全场景配套表达。')
add_source(doc, '顺庭宴会中心官方笔记一', 'https://www.xiaohongshu.com/search_result/698bef77000000000903b937?xsec_token=ABDKA3vJ_kTYixJmv4ebuzHwAoumMH-BvUaDUCE503fgs=&xsec_source=', '核验 7 大厅、桌数、层高、面积及一站式服务表达。')
add_source(doc, '顺庭宴会中心官方笔记二', 'https://www.xiaohongshu.com/search_result/697f1f78000000000b0093e9?xsec_token=ABAXSDKjjMSU46bZKag4EcfDpkL2vKSA5P6xs7qE5IvVU=&xsec_source=', '对照核验厅型和桌数，补充各厅面积与风格。')
add_source(doc, '至臻盛宴官方/经理账号笔记', 'https://www.xiaohongshu.com/search_result/6a47674d0000000022015ed7?xsec_token=ABvkrRQ_gS2Q2_2ugCPP0RybQ_GDoCNBbCGaF8oZvz0_g=&xsec_source=', '仅核验“2026 全新打造、3 大主题婚礼堂、预售开启”，未核验到稳定地址/价格/厅型。')

add_para(doc, '本方案的所有建议均建立在上述公开核验和门店待确认事实之上。正式发布前，以门店最新合同、菜单、价目表、现场实际和平台后台为最终依据。', color=GRAY, size=8.8, after=0)

doc.core_properties.title = '福气东来酒店新都大丰门店小红书诊断与90天落地运营方案'
doc.core_properties.subject = '小红书账号诊断、成都新都婚宴市场竞争与落地运营规划'
doc.core_properties.author = '聚尤米 UMI'
doc.core_properties.keywords = '小红书, 新都婚宴, 大丰, 福气东来酒店, 运营方案'
OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(OUT)
