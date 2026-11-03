from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.colors import HexColor
from xml.sax.saxutils import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "pdf" / "都江堰明智上春假日酒店_GEO+小红书3个月运营方案.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT = r"C:\Windows\Fonts\simhei.ttf"
FONT_B = r"C:\Windows\Fonts\simhei.ttf"
pdfmetrics.registerFont(TTFont("CN", FONT))
pdfmetrics.registerFont(TTFont("CN-B", FONT_B))

NAVY = HexColor("#16324F")
TEAL = HexColor("#087E8B")
GOLD = HexColor("#C8943E")
INK = HexColor("#22313F")
MUTED = HexColor("#667788")
PALE = HexColor("#F4F7F8")
PALE_BLUE = HexColor("#EAF3F5")
LINE = HexColor("#D8E0E5")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverKicker", fontName="CN-B", fontSize=11, leading=16, textColor=TEAL, spaceAfter=8))
styles.add(ParagraphStyle(name="CoverTitle", fontName="CN-B", fontSize=27, leading=36, textColor=NAVY, spaceAfter=11))
styles.add(ParagraphStyle(name="CoverSub", fontName="CN", fontSize=13, leading=21, textColor=INK, spaceAfter=18))
styles.add(ParagraphStyle(name="H1CN", fontName="CN-B", fontSize=17, leading=25, textColor=NAVY, spaceBefore=12, spaceAfter=9, keepWithNext=True))
styles.add(ParagraphStyle(name="H2CN", fontName="CN-B", fontSize=12.5, leading=19, textColor=TEAL, spaceBefore=8, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyCN", fontName="CN", fontSize=9.2, leading=15, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="SmallCN", fontName="CN", fontSize=7.7, leading=11.5, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle(name="TinyCN", fontName="CN", fontSize=6.7, leading=9.2, textColor=MUTED))
styles.add(ParagraphStyle(name="TableCN", fontName="CN", fontSize=7.1, leading=10.2, textColor=INK))
styles.add(ParagraphStyle(name="TableHead", fontName="CN-B", fontSize=7.3, leading=10.5, textColor=WHITE, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Callout", fontName="CN-B", fontSize=10, leading=16, textColor=NAVY, backColor=PALE_BLUE, borderColor=TEAL, borderWidth=0.6, borderPadding=8, spaceBefore=6, spaceAfter=8))
styles.add(ParagraphStyle(name="Quote", fontName="CN-B", fontSize=11.5, leading=18, textColor=NAVY, leftIndent=8, borderColor=GOLD, borderWidth=2, borderPadding=7, spaceBefore=5, spaceAfter=8))

def P(txt, style="BodyCN"):
    return Paragraph(escape(str(txt)).replace("\n", "<br/>").replace("  ", "&nbsp;&nbsp;"), styles[style])

def rich(txt, style="BodyCN"):
    return Paragraph(txt, styles[style])

def table(data, widths, header=True, small=False, repeat=1):
    conv = []
    for r, row in enumerate(data):
        conv.append([rich(str(c), "TableHead" if header and r == 0 else ("TinyCN" if small else "TableCN")) for c in row])
    t = Table(conv, colWidths=widths, repeatRows=repeat if header else 0, hAlign="LEFT")
    cmds = [
        ("GRID", (0,0), (-1,-1), 0.35, LINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]
    if header:
        cmds += [("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), WHITE)]
        for i in range(1, len(data)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0,i), (-1,i), PALE))
    t.setStyle(TableStyle(cmds))
    return t

def bullet(text):
    return rich("<font color='#087E8B'>●</font>&nbsp;" + escape(text), "BodyCN")

def section(title):
    return [P(title, "H1CN"), HRFlowable(width="100%", thickness=0.8, color=TEAL, spaceAfter=6)]

def footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.4)
    canvas.line(16*mm, 13*mm, w-16*mm, 13*mm)
    canvas.setFont("CN", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(16*mm, 8*mm, "明智上春假日酒店 | GEO + 小红书 3 个月运营方案")
    canvas.drawRightString(w-16*mm, 8*mm, f"{doc.page}")
    canvas.restoreState()

class Doc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=15*mm, bottomMargin=18*mm, title="都江堰明智上春假日酒店 GEO+小红书3个月运营方案", author="GEO+新媒体运营团队")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=footer)])

story = []

# Cover
story += [Spacer(1, 23*mm), P("GEO + 小红书运营提案", "CoverKicker"), P("都江堰明智上春假日酒店", "CoverTitle"), P("国内 GEO 布局 + 小红书免费运营 3 个月", "CoverSub"), HRFlowable(width="100%", thickness=2, color=GOLD, spaceBefore=3, spaceAfter=15)]
story += [P("让酒店在 AI 问答、小红书搜索和本地决策场景中，被看见、被理解、被选择。", "Quote")]
cover_meta = [["项目费用", "19,800 元"], ["运营周期", "小红书 3 个月 + GEO 长期内容资产"], ["服务对象", "都江堰明智上春假日酒店（熊猫谷店）"], ["方案日期", "2026 年 8 月 24 日"]]
story += [table(cover_meta, [30*mm, 130*mm], header=False), Spacer(1, 14*mm), P("本提案以高德地图、小红书官方账号及客户提供的宴会清单为基础，竞对部分采用公开可检索信息形成初步判断，签约前建议进行一次现场和平台复核。", "SmallCN"), PageBreak()]

# Executive summary
story += section("一、先给酒店老板看的结论")
story += [rich("<b>一句话定位：</b>明智上春不是单一住宿酒店，而是“熊猫谷亲子度假 + 165 间客房承接 + 600 人宴会会议 + 汤池棋牌配套”的都江堰北部综合接待节点。", "Callout")]
for x in [
    "当前线上最大问题不是没有产品，而是产品没有被结构化表达。高德页面已经有 4.8 分和真实亲子、自驾、熊猫谷近距离等证据，小红书官方号也有 10 条笔记，但账号只有 16 粉丝，且公开内容未形成稳定栏目。",
    "本项目的核心不是简单发笔记，而是把酒店的客房、宴会、会议、亲子和交通优势，改写成 AI 能读懂、小红书用户愿意收藏、销售人员能够直接报价的内容资产。",
    "3 个月以自然内容和账号基础建设为主，不含聚光、达人、摄影、认证等第三方费用；成交线索由酒店承接，所有效果以可追踪的私信、电话、到店和订单数据复盘。",
]: story.append(bullet(x))
story += [P("建议优先抢占的 3 个心智位", "H2CN")]
story += [table([
    ["心智位", "用户问题", "酒店应该被记住的答案"],
    ["熊猫谷亲子住宿", "带孩子去熊猫谷住哪里？", "离熊猫谷近，自驾友好，家庭房、戏水/汤池、停车和早餐一站解决"],
    ["都江堰团队会议/团建", "50-600 人会议住哪里？", "6 个会议宴会空间，最大剧院式 600 人，165 间客房可承接住宿与用餐"],
    ["都江堰婚宴/家宴", "婚宴或家宴如何选酒店？", "明智厅、上春厅、明智上春厅可按桌数和舞台需求组合，兼顾宾客住宿"],
], [34*mm, 53*mm, 73*mm])]

# Research facts
story += section("二、已核实的酒店现状")
story += [P("2.1 小红书账号诊断", "H2CN")]
story += [table([
    ["项目", "已核实信息", "判断"],
    ["账号", "明智上春假日酒店；小红书号 26253920250", "可作为官方品牌号继续运营"],
    ["主页数据", "16 粉丝、10 笔记、10 关注；获赞与收藏 33", "账号资产尚小，适合重做定位和内容基建"],
    ["主页简介", "165 间客房；满足 600 人用餐；会议室、棋牌茶室、汤池、健身房、停车场", "产品卖点齐全，但目前没有按需求场景拆解"],
    ["可见内容", "避暑玩水、亲子/旅游住宿、熊猫谷、智能客房、酒店开业等", "已有亲子和旅游素材，可延展到会议、婚宴和团队接待"],
], [31*mm, 88*mm, 41*mm])]
story += [P("2.2 高德地图公开信息", "H2CN")]
story += [table([
    ["项目", "高德页面显示"],
    ["名称与地址", "明智上春假日酒店（都江堰熊猫谷店）；赵公路 126 号"],
    ["评分与价格", "4.8 分；14 条评价；页面显示约 ¥336/人；高档型"],
    ["联系方式", "028-87261666；028-87298999"],
    ["设施标签", "亲子房、山景房、花园景、充电桩、客房 WIFI、早餐、健身房、全屋智能、亲子温泉等"],
    ["评价证据", "自驾停车方便、充电桩、家庭房 50 多平方米、全屋智能、戏水池/汤池、开车约 5 分钟到熊猫谷、十几分钟到都江堰景区等"],
], [37*mm, 123*mm])]
story += [P("2.3 客户提供的宴会与会议能力", "H2CN")]
story += [P("以下数据来自酒店宴会清单，建议作为后续所有小红书笔记、AI 话料、销售报价单的统一口径。", "SmallCN")]
story += [table([
    ["空间", "面积", "类型/屏幕", "剧院式", "课桌式", "适合销售的场景"],
    ["行政会议室", "51㎡", "无柱；智能 100 寸会议电视", "-", "-", "董事会、访谈、小型培训"],
    ["多功能会议室 C", "160㎡", "凸柱；LED 3.84×1.92m，1920×960", "100", "90", "培训、发布会、团队会议"],
    ["四季厅 BC", "317㎡", "有柱", "120", "120", "中小型会议、家宴"],
    ["明智厅 A", "336㎡", "无柱；LED 6.4×3.04m，3200×1520", "250", "200", "婚宴、论坛、企业年会"],
    ["上春厅 AB", "493㎡", "有柱；LED 6.4×3.04m", "350", "240", "中大型婚宴、团队宴请"],
    ["明智上春厅 ABC", "653㎡", "有柱；LED 6.4×3.04m", "600", "360", "大型会议、年会、婚宴"],
], [30*mm, 16*mm, 46*mm, 17*mm, 17*mm, 40*mm], small=True)]
story += [rich("<b>产品化结论：</b>酒店需要把“600 人用餐”改写成可购买的组合，例如“会议 2 天 1 夜”“婚宴 + 住宿”“熊猫谷团队接待”“企业年会包场”，而不是只在简介里罗列设施。", "Callout")]

# GEO explanation
story += section("三、GEO 是什么，以及它如何影响酒店决策")
story += [P("3.1 用酒店经营者听得懂的话解释", "H2CN")]
story += [P("GEO（Generative Engine Optimization，生成式引擎优化）是针对豆包、DeepSeek、文心、通义、夸克、Kimi、ChatGPT 等 AI 问答入口的内容优化。SEO 争取的是搜索结果页面的排名；GEO 争取的是 AI 在回答“我该选哪家”时，能准确理解酒店并把它列入建议。", "BodyCN")]
story += [P("例如，客人不一定搜索酒店名字，而是问：‘都江堰熊猫谷亲子住宿怎么选？’‘都江堰 200 人会议酒店推荐？’‘都江堰婚宴能不能同时安排宾客住宿？’ GEO 要做的，就是让公开内容中持续出现清晰、可验证、可引用的答案。", "BodyCN")]
story += [P("3.2 它对线上用户决策的作用", "H2CN")]
story += [table([
    ["决策阶段", "传统方式", "加入 GEO 后的酒店机会"],
    ["产生需求", "朋友推荐、旅行平台榜单、广告", "AI 先给出场景化清单，酒店进入候选池"],
    ["筛选比较", "用户逐个平台看价格和评价", "AI 将距离、设施、人数、场景和口碑做摘要，酒店的差异点更容易被看见"],
    ["验证信任", "看高德/点评评分和照片", "GEO 内容把评分之外的证据讲清楚：165 间房、会议容量、LED、停车、亲子配套"],
    ["咨询成交", "电话、平台客服、到店考察", "AI 或小红书内容引导用户按场景咨询，销售更容易承接"],
], [30*mm, 65*mm, 75*mm])]
story += [P("3.3 GEO 是替代旧链路，还是增加链路？", "H2CN")]
story += [rich("<b>结论：是增加一个“AI 决策入口”，不是替代高德、点评、携程或线下销售。</b>", "Callout")]
story += [P("酒店原有链路仍然重要：小红书种草/搜索 -> 高德或点评确认位置和评价 -> 电话或平台预订 -> 到店体验。GEO 增加的是上游的“问 AI”入口，并把公开信息重新组织成一个可被 AI 摘要的品牌答案。最终要形成：AI 发现 -> 小红书理解场景 -> 高德验证口碑与路线 -> 电话/私信询价 -> 到店或下单。", "BodyCN")]
story += [P("3.4 GEO 能给酒店带来的价值", "H2CN")]
for x in [
    "获得非品牌搜索流量：用户未必知道“明智上春”，但会搜索熊猫谷亲子酒店、都江堰会议酒店、都江堰婚宴酒店。",
    "提升客单价解释能力：把房间、会议室、宴会厅、汤池、停车和旅游动线组合成方案，减少只比房价。",
    "减少销售重复沟通：统一的 FAQ、容量表、套餐说明和交通说明，可以成为客服、销售和 AI 的共同话料。",
    "沉淀长期资产：高质量公开内容不会随着一次投放结束而消失，后续可继续被小红书搜索、地图和 AI 引用。",
]: story.append(bullet(x))

# Competitive landscape
story += section("四、5-8 公里竞对研究与酒店差异化")
story += [P("4.1 竞对范围与说明", "H2CN")]
story += [P("本次竞对按赵公路 126 号、熊猫谷和都江堰北部自驾动线筛选，重点看“婚宴、会议、旅游住宿”三类承接能力。由于平台的 POI、房价和营业状态会动态变化，以下为公开信息形成的首轮销售策略矩阵，不把未完成二次核验的字段当作硬承诺。", "BodyCN")]
story += [table([
    ["竞对/参照对象", "主要心智", "对明智上的威胁", "建议应对"],
    ["都江堰智选假日酒店", "连锁、商务、标准化住宿", "品牌认知和商务客信任更强", "用熊猫谷亲子、汤池、宴会会议一体化和大容量承接做差异"],
    ["都江堰青城豪生国际酒店", "高端度假、会议、团建", "高端会议与度假预算客被吸走", "不做同质化高端，强调 165 房、600 人宴会、交通与性价比"],
    ["都江堰百伦国际酒店", "城区商务、宴会、婚宴", "城市宴会和本地婚宴心智成熟", "抢“旅游住宿 + 宴会住宿联动”，突出熊猫谷动线与停车充电"],
    ["都江堰万达/城区连锁酒店群", "位置便利、平台价格透明", "OTA 比价和短住订单分流", "小红书做场景内容，不与单晚房价硬拼"],
    ["青城山及熊猫谷周边民宿/精品酒店", "景观、轻度假、亲子打卡", "亲子旅游内容更灵活、视觉更强", "用酒店级客房数量、宴会会议、早餐停车和全屋智能做稳定性"],
], [38*mm, 36*mm, 52*mm, 44*mm], small=True)]
story += [P("4.2 明智上的可防守优势", "H2CN")]
story += [table([
    ["维度", "明智上春的证据", "应转成的传播话术"],
    ["住宿规模", "165 间客房", "团队、婚宴宾客和亲子家庭可以集中入住"],
    ["宴会会议", "6 个空间；最大 653㎡；剧院式 600 人", "从 16 人董事会到 600 人年会，一家酒店完成"],
    ["技术设施", "3.84m 和 6.4m LED；会议电视", "发布会、培训、年会能直接展示大屏和会场效果"],
    ["亲子旅游", "亲子房、亲子温泉/戏水、熊猫谷近", "熊猫谷家庭出游，住得下、玩得到、停车方便"],
    ["交通与服务", "赵公路 126 号；停车、充电桩；高德 4.8 分", "自驾到店不绕路，新能源车也方便"],
], [31*mm, 64*mm, 75*mm])]
story += [rich("<b>竞争策略不是“证明我们比所有酒店都好”，而是让不同客群在不同问题下都能迅速知道：明智上春在哪个场景更合适。</b>", "Quote")]

# Product strategy
story += section("五、把酒店产品卖成三条线")
story += [P("5.1 旅游住宿线：熊猫谷亲子与自驾", "H2CN")]
story += [table([
    ["产品包", "内容", "主推关键词/标题"],
    ["熊猫谷亲子住", "家庭房/亲子房 + 早餐 + 停车 + 熊猫谷路线说明", "都江堰熊猫谷亲子酒店、带娃住哪里"],
    ["自驾友好住", "免费停车/充电桩 + 近景区动线 + 24 小时前台信息", "都江堰自驾住宿、熊猫谷附近停车方便的酒店"],
    ["避暑汤池住", "戏水/汤池、健身、棋牌茶室等设施组合", "都江堰避暑酒店、亲子温泉酒店"],
], [34*mm, 83*mm, 53*mm])]
story += [P("5.2 会议与团建线：从 16 人到 600 人", "H2CN")]
story += [P("对外报价建议按“人数 + 会场 + 屏幕 + 住宿 + 用餐 + 茶歇 + 交通”打包，避免只卖会议室面积。首批内容优先展示 C 会议室、明智厅 A、上春厅 AB、明智上春厅 ABC 的实景和摆台。", "BodyCN")]
story += [table([
    ["场景", "建议组合", "销售动作"],
    ["企业培训/发布会", "C 会议室或明智厅 + LED + 茶歇 + 住宿", "发布会场地实拍、屏幕尺寸和停车说明"],
    ["团队年会", "上春厅/明智上春厅 + 舞台 LED + 宴会 + 住宿", "按 200/350/600 人做三档方案"],
    ["旅行团接待", "客房 + 团队用餐 + 景区动线 + 大巴停车", "把熊猫谷、都江堰景区、青城山路线写成攻略"],
], [34*mm, 82*mm, 54*mm])]
story += [P("5.3 婚宴与家宴线：把厅型变成选择题", "H2CN")]
story += [P("婚宴客户最关心桌数、层高、柱子、LED、住宿和交通。建议每篇内容只解决一个问题，例如“20 桌婚宴选明智厅还是上春厅”“600 人婚宴如何安排宾客住宿”，避免只发空厅照片。", "BodyCN")]

# GEO implementation
story += section("六、国内 GEO 执行方案")
story += [P("6.1 关键词与用户提问矩阵", "H2CN")]
story += [table([
    ["需求主题", "AI/用户可能的真实提问", "内容载体"],
    ["亲子住宿", "都江堰熊猫谷附近亲子酒店推荐？带孩子住哪里方便？", "小红书攻略、高德简介、FAQ"],
    ["会议酒店", "都江堰 100 人培训在哪里办？600 人年会有哪些酒店？", "会议厅容量表、会议案例、长图"],
    ["婚宴家宴", "都江堰婚宴酒店怎么选？有住宿和大屏的宴会厅吗？", "厅型对比、婚宴流程、宴会清单"],
    ["避坑决策", "熊猫谷附近酒店如何选？自驾停车、早餐、汤池重要吗？", "实测攻略、服务清单、评价回应"],
    ["品牌词", "明智上春假日酒店怎么样？电话多少？离熊猫谷多远？", "高德一致信息、小红书置顶笔记、品牌 FAQ"],
], [30*mm, 88*mm, 52*mm], small=True)]
story += [P("6.2 话料资产清单", "H2CN")]
story += [table([
    ["资产", "首期交付", "用途"],
    ["品牌标准介绍", "1 套 300 字短介绍 + 1 套 800 字长介绍", "小红书主页、高德、官网/公众号、AI 读取"],
    ["酒店 FAQ", "不少于 30 问", "电话客服、私信、AI 问答、销售培训"],
    ["会议宴会能力表", "6 个厅型、面积、容量、屏幕、柱型", "会议/婚宴报价和搜索卡位"],
    ["场景攻略", "熊猫谷亲子、自驾、会议、婚宴各 2 篇", "小红书收藏与 AI 引用"],
    ["口碑证据库", "高德评价中可公开使用的服务关键词", "亲子、停车、智能、汤池、位置、服务"],
], [36*mm, 58*mm, 76*mm])]
story += [P("6.3 监测方式", "H2CN")]
for x in [
    "每月固定抽测 20-30 个问题，记录 AI 是否提及酒店、提及的卖点是否准确、是否出现竞品。",
    "每周记录小红书品牌词、熊猫谷亲子酒店、都江堰会议酒店、都江堰婚宴酒店等搜索结果中的内容表现。",
    "所有电话、私信和到店客户使用来源标签：GEO、XHS-住宿、XHS-会议、XHS-婚宴、高德、转介绍。",
]: story.append(bullet(x))

# XHS plan
story += section("七、小红书免费运营 3 个月方案")
story += [P("账号策略：继续使用官方账号 26253920250，账号定位从“酒店宣传号”改为“都江堰熊猫谷住宿 + 会议宴会解决方案”。主页简介建议：165 间客房｜熊猫谷附近自驾友好｜600 人宴会会议｜亲子房/汤池/停车充电｜会议婚宴咨询。", "Callout")]
story += [P("7.1 四大内容栏目", "H2CN")]
story += [table([
    ["栏目", "内容比例", "示例标题", "目标"],
    ["亲子旅游住宿", "35%", "都江堰熊猫谷带娃住哪里？这家酒店停车和戏水都省心", "抢住宿搜索和收藏"],
    ["会议团建", "25%", "都江堰 200 人培训场地怎么选？明智厅实景和容量表", "获取企业询盘"],
    ["婚宴家宴", "25%", "20 桌婚宴选哪个厅？明智厅/上春厅一次看懂", "获取婚宴到店"],
    ["酒店服务口碑", "15%", "住客说停车、智能客房和汤池到底好不好用", "建立信任"],
], [32*mm, 18*mm, 78*mm, 42*mm])]
story += [P("7.2 三个月排期", "H2CN")]
story += [table([
    ["阶段", "重点", "发布建议", "验收"],
    ["第 1 月：重启与基建", "重做主页、统一视觉、补齐酒店/房型/厅型素材", "每周 3 条，至少 12 条；置顶 3 条：酒店总览、亲子住宿、会议宴会", "账号资料完整；建立素材库和线索表"],
    ["第 2 月：场景卡位", "围绕熊猫谷、自驾、会议、婚宴做问答型内容", "每周 3-4 条，至少 14 条；每周 1 条厅型/容量内容", "搜索词覆盖；私信问题沉淀为 FAQ"],
    ["第 3 月：案例转化", "发布真实入住、会议摆台、宴会案例和路线攻略", "每周 4 条，至少 16 条；加强评论区和私信承接", "形成住宿/会议/婚宴三类线索看板"],
], [30*mm, 48*mm, 63*mm, 29*mm], small=True)]
story += [P("7.3 首月可直接执行的 12 个选题", "H2CN")]
topics = [
    "酒店总览：165 间客房 + 600 人宴会会议，适合哪几类客人？", "熊猫谷亲子住宿：家庭房、早餐、停车、戏水/汤池一次讲清", "都江堰自驾住宿：有停车和充电桩的酒店怎么选？", "熊猫谷一日游路线：住明智上春怎么安排时间？", "明智厅 A 实景：336㎡、剧院式 250 人、LED 6.4m", "上春厅 AB 实景：493㎡、剧院式 350 人、课桌式 240 人", "明智上春厅 ABC：600 人年会怎么摆台？", "16 人董事会到 600 人年会，厅型怎么选？", "20 桌婚宴选哪个厅：柱型、屏幕、宾客住宿对比", "都江堰婚宴酒店避坑：问清桌数、柱子、LED、住宿和停车", "住客评价拆解：停车、智能客房、汤池、熊猫谷距离", "酒店周边旅游住宿清单：熊猫谷、都江堰景区、青城山如何组合",
]
story += [table([["序号", "选题"]] + [[str(i+1), t] for i,t in enumerate(topics)], [16*mm, 154*mm], header=True, small=True)]
story += [P("7.4 内容制作模板", "H2CN")]
story += [table([
    ["模块", "写法"],
    ["封面", "地点 + 人群 + 一个明确利益点，例如“熊猫谷亲子住｜停车/汤池/早餐”"],
    ["开头 3 行", "先给结论，再给适用人群，不用酒店宣传腔"],
    ["正文", "实景证据 + 参数 + 体验细节 + 适用场景 + 交通/咨询方式"],
    ["结尾", "引导用户留言人数、日期、用途，分别承接住宿/会议/婚宴"],
    ["评论区", "置顶容量表、电话、地址和“可帮你按人数推荐厅型”"],
], [32*mm, 138*mm])]

# Case and fee
story += section("八、案例、费用与合作边界")
story += [P("8.1 案例说明", "H2CN")]
story += [P("案例：郫县臻里八号宴会中心。该案例用于证明我们对宴会类客户的内容结构、场景拆解和本地用户决策逻辑有经验。明智上春与特色场地不同，不能照搬“出片/婚礼风格”模板，必须把住宿、会议、宴会、旅游动线放在同一个酒店产品逻辑里。其他案例可沿用既有方案中的三圣乡/婚宴/本地生活案例，但本项目交付以可核验数据和酒店实际素材为准，不承诺复制案例结果。", "BodyCN")]
story += [P("8.2 19,800 元服务内容", "H2CN")]
story += [table([
    ["模块", "包含内容"],
    ["GEO 基础建设", "酒店品牌诊断、关键词和提问矩阵、核心话料、FAQ、会议宴会能力结构化、公开平台信息一致性建议"],
    ["小红书免费运营 3 个月", "官方账号定位、主页优化、内容策划、图文发布、标题/标签优化、评论区基础维护、月度复盘"],
    ["内容资产", "住宿、会议、婚宴、亲子旅游四类模板；首期 30+ 个选题；宴会能力表和销售可用话术"],
    ["数据与复盘", "周度发布记录；月度数据报告；线索来源标记；第 1 月和第 3 月复盘会议"],
], [39*mm, 131*mm])]
story += [P("8.3 不包含与酒店需配合", "H2CN")]
for x in [
    "不包含聚光投放、达人探店、摄影摄像、平台认证费、第三方平台佣金和酒店优惠成本。",
    "酒店需提供可公开使用的房型、价格区间、宴会菜单/套餐、会议报价、停车/早餐/汤池规则和最新素材。",
    "酒店需指定 1 位线索承接人，住宿咨询建议 10 分钟内响应，会议/婚宴询盘建议 30 分钟内响应。",
    "平台规则、AI 推荐和自然流量存在波动，方案提供内容建设和过程指标，不承诺固定曝光、排名或成交量。",
]: story.append(bullet(x))

# KPI and next steps
story += section("九、目标、KPI 与启动清单")
story += [P("9.1 三个月建议目标（过程型 + 结果型）", "H2CN")]
story += [table([
    ["指标", "第 1 月", "第 2 月", "第 3 月"],
    ["发布量", "12 条", "14 条", "16 条"],
    ["账号基础", "主页/置顶/素材库完成", "搜索词和 FAQ 完善", "三类线索看板稳定"],
    ["有效咨询", "建立基线", "住宿/会议/婚宴均有记录", "以第 2 月为基线持续提升"],
    ["AI 监测", "建立 20-30 个问题基线", "复测并修正错误信息", "形成季度报告"],
    ["销售闭环", "来源标签上线", "记录电话、到店、报价", "复盘成交和未成交原因"],
], [44*mm, 43*mm, 43*mm, 40*mm])]
story += [P("9.2 启动前 7 天清单", "H2CN")]
for x in [
    "酒店确认账号授权、联系人和内容审核时限。",
    "提供宴会厅、房型、公共区域、停车、充电桩、汤池、早餐的高清照片和短视频。",
    "确认会议/婚宴最新报价口径，以及哪些内容可以公开发布。",
    "补拍 6 个厅型的空场、摆台、LED、入口、动线和停车场素材。",
    "建立线索表：日期、人数、用途、预算、来源、跟进人、结果。",
    "首周发布 3 条：酒店总览、熊猫谷亲子住宿、会议宴会能力。",
]: story.append(bullet(x))
story += [rich("<b>最终建议：</b>先用 3 个月把“明智上春是什么、适合谁、能承接多大规模、为什么比周边竞品更适合”讲清楚，再根据线索成本决定是否追加投放和达人合作。", "Quote")]

# Sources / caveats
story += section("附录：公开来源与核验边界")
story += [P("本方案使用的公开信息与内部材料：", "BodyCN")]
sources = [
    "小红书官方账号主页：明智上春假日酒店，小红书号 26253920250（账号数据、简介、公开笔记）。",
    "高德地图 POI：明智上春假日酒店（都江堰熊猫谷店），B0KU36ET43；地址赵公路 126 号，页面评分、电话、设施标签及评价。",
    "客户提供的宴会清单截图：6 个会议/宴会空间、面积、厅型、LED 与容量数据。",
    "竞对候选：都江堰智选假日酒店、都江堰青城豪生国际酒店、都江堰百伦国际酒店、城区连锁酒店群、青城山/熊猫谷周边民宿与精品酒店。",
]
for s in sources: story.append(bullet(s))
story += [P("核验提示：酒店房价、房态、平台评分、竞对距离和宴会承接状态会随时间变化。正式签约和对外发布前，应由酒店确认最新价格、营业状态、可公开素材及竞对 5-8 公里实测距离。", "SmallCN")]

Doc(str(OUT)).build(story)
print(OUT)
