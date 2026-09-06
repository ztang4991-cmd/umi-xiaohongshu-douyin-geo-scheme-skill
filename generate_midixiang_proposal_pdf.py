# -*- coding: utf-8 -*-
"""
迷迭香农庄 - 小红书账号诊断与运营提案 PDF生成器
基于真实账号数据生成专业提案文档
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# 注册中文字体
font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('msyh', font_path))
    font_name = 'msyh'
else:
    font_name = 'Helvetica'

def create_styles():
    """创建样式"""
    styles = getSampleStyleSheet()

    # 标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        leading=36
    )

    # 一级标题
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=18,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=20,
        leading=28
    )

    # 二级标题
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        textColor=colors.HexColor('#5D6D7E'),
        spaceAfter=10,
        spaceBefore=15,
        leading=22
    )

    # 三级标题
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=12,
        textColor=colors.HexColor('#7F8C8D'),
        spaceAfter=8,
        spaceBefore=12,
        leading=18
    )

    # 正文样式
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=8,
        leading=16,
        alignment=TA_JUSTIFY
    )

    # 要点样式
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        textColor=colors.HexColor('#2C3E50'),
        leftIndent=20,
        spaceAfter=6,
        leading=16
    )

    return {
        'title': title_style,
        'h1': h1_style,
        'h2': h2_style,
        'h3': h3_style,
        'body': body_style,
        'bullet': bullet_style
    }

def create_cover_page(styles):
    """创建封面"""
    story = []

    story.append(Spacer(1, 3*cm))

    # 主标题
    title = Paragraph("迷迭香农庄", styles['title'])
    story.append(title)
    story.append(Spacer(1, 0.5*cm))

    subtitle = Paragraph("小红书账号诊断与运营提案", styles['h1'])
    story.append(subtitle)
    story.append(Spacer(1, 3*cm))

    # 账号信息表格
    account_data = [
        ['账号名称', '迷迭香农庄'],
        ['小红书ID', '538177362'],
        ['粉丝数', '3,543'],
        ['获赞收藏', '17,000'],
        ['IP属地', '四川成都'],
        ['提案日期', '2026年8月17日']
    ]

    account_table = Table(account_data, colWidths=[5*cm, 8*cm])
    account_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 11),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    story.append(account_table)
    story.append(PageBreak())

    return story

def create_executive_summary(styles):
    """创建执行摘要"""
    story = []

    story.append(Paragraph("执行摘要", styles['h1']))
    story.append(Spacer(1, 0.3*cm))

    # 账号现状
    story.append(Paragraph("账号现状", styles['h2']))
    summary_points = [
        "• <b>粉丝基数</b>：3,543粉丝，1.7万获赞收藏，处于初期成长阶段",
        "• <b>内容产出</b>：61篇可见笔记，内容稳定但爆款率低（<2%）",
        "• <b>唯一爆款</b>："一场非常哇塞的婚礼"（1,225赞），证明婚礼内容是流量密码",
        "• <b>核心问题</b>：定位模糊、转化链条断裂、商业化效率低"
    ]
    for point in summary_points:
        story.append(Paragraph(point, styles['bullet']))

    story.append(Spacer(1, 0.5*cm))

    # 三大致命问题
    story.append(Paragraph("三大致命问题", styles['h2']))

    problems_data = [
        ['问题层级', '具体表现', '影响'],
        ['战略层：定位模糊',
         '窑烤+婚礼+亲子+团建混杂，用户不知道你是什么',
         '品牌认知混乱，流量分散'],
        ['内容层：转化弱',
         '标题信息密度低，缺价格/位置/预约方式，无CTA',
         '流量有但留资少，看完不知道怎么约'],
        ['转化层：闭环缺失',
         '笔记→私信→留资→成交链条断裂',
         '估算转化损失70%+']
    ]

    problems_table = Table(problems_data, colWidths=[4*cm, 6*cm, 4.5*cm])
    problems_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(problems_table)
    story.append(Spacer(1, 0.5*cm))

    # 核心策略
    story.append(Paragraph("核心优化策略", styles['h2']))

    strategy_points = [
        "• <b>重新定位</b>：成都托斯卡纳式户外生活场景专家 —— "在成都，过一天意式田园生活"",
        "• <b>内容升级</b>：从"记录型"转向"解决方案型"，标题加价格/位置/场景信息",
        "• <b>流量策略</b>：聚光投放 + KOC矩阵 + UGC激励，提升爆款率至10%+",
        "• <b>转化优化</b>：笔记CTA + 私信SOP + 企微承接，留资率提升至5%+"
    ]
    for point in strategy_points:
        story.append(Paragraph(point, styles['bullet']))

    story.append(Spacer(1, 0.5*cm))

    # 预期成果
    story.append(Paragraph("预期成果（6个月）", styles['h2']))

    results_data = [
        ['指标', '第1个月', '第2-3个月', '第4-6个月'],
        ['粉丝增长', '+500-800', '+1,500/月', '累计5,000+'],
        ['月均曝光', '8-10万', '15-20万', '25-30万'],
        ['有效留资', '20-30', '80-100/月', '150+/月'],
        ['预估ROI', '测试期', '1:4-1:7', '1:7-1:12']
    ]

    results_table = Table(results_data, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    results_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(results_table)
    story.append(PageBreak())

    return story

def create_content_analysis(styles):
    """创建内容板块分析"""
    story = []

    story.append(Paragraph("一、内容板块诊断（基于61篇真实笔记）", styles['h1']))
    story.append(Spacer(1, 0.3*cm))

    # 板块概览
    story.append(Paragraph("1.1 内容板块概览", styles['h2']))

    overview_data = [
        ['板块', '占比', '互动表现', '核心问题', '优化优先级'],
        ['窑烤披萨', '25%', '置顶66赞，其余5-18赞', '转化引导缺失', '★★★★'],
        ['草坪婚礼', '10%', '爆款1,225赞，其余7-19赞', '内容占比过低', '★★★★★'],
        ['亲子遛娃', '20%', '5-13赞', '价格信息模糊', '★★★★'],
        ['氛围打卡', '40%', '5-26赞', '纯氛围无转化', '★★'],
        ['团建活动', '5%', '5-10赞', '平台用户错位', '★']
    ]

    overview_table = Table(overview_data, colWidths=[2.8*cm, 2*cm, 3*cm, 3.5*cm, 2.5*cm])
    overview_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 8),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(overview_table)
    story.append(Spacer(1, 0.5*cm))

    # 窑烤披萨板块
    story.append(Paragraph("1.2 窑烤披萨板块", styles['h2']))
    story.append(Paragraph("<b>✅ 优势</b>", styles['h3']))
    advantages = [
        "• 差异化强：意式窑炉披萨是核心记忆点，"600℃高温90秒"具象化专业度",
        "• 视觉吸引力：置顶笔记（66赞）火焰、烟雾、出炉瞬间有冲击力",
        "• 重复强化：多篇笔记提及窑烤，形成符号"
    ]
    for adv in advantages:
        story.append(Paragraph(adv, styles['bullet']))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>⚠️ 劣势与问题</b>", styles['h3']))
    problems = [
        "• 转化引导缺失：笔记未说明"如何预约""团队套餐价格""是否可单点"",
        "• 场景单一：只展示"做披萨"，未关联"亲子DIY""团建活动""婚礼晚宴"",
        "• 与竞品区隔不清：你的独特性（托斯卡纳环境+窑烤）未被强化"
    ]
    for prob in problems:
        story.append(Paragraph(prob, styles['bullet']))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>优化建议</b>", styles['h3']))

    optimization_data = [
        ['现状标题❌', '优化后标题✅'],
        ['"窑烤披萨🍕一炉烟火气"', '"成都周边｜DIY窑烤披萨198元/人｜托斯卡纳农庄包场攻略"'],
        ['"意式窑炉披萨"', '"成都窑烤披萨｜600℃意式窑炉｜亲子团建婚礼可定制"']
    ]

    opt_table = Table(optimization_data, colWidths=[7*cm, 7*cm])
    opt_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#95A5A6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(opt_table)
    story.append(Spacer(1, 0.5*cm))

    # 草坪婚礼板块
    story.append(Paragraph("1.3 草坪婚礼板块（核心重点）", styles['h2']))
    story.append(Paragraph("<b>✅ 优势</b>", styles['h3']))
    wedding_advantages = [
        "• 爆款验证："一场非常哇塞的婚礼💒"（1,225赞）证明婚礼内容是流量密码",
        "• 场地视觉优势：草坪、丝柏道、红砖拱门、白纱元素符合小红书婚礼审美",
        "• 情绪共鸣强："在这里，每一个重要时刻都值得被完美铭记"戳中新人心智"
    ]
    for adv in wedding_advantages:
        story.append(Paragraph(adv, styles['bullet']))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>⚠️ 致命问题</b>", styles['h3']))
    wedding_problems = [
        "• <b>婚礼笔记占比过低</b>：61篇笔记中仅5-6篇提及婚礼（应占30%+）",
        "• <b>核心痛点未解答</b>：能办多少桌？雨天怎么办？价格区间？包含哪些服务？",
        "• <b>搜索关键词缺失</b>：未覆盖"成都草坪婚礼""成都户外婚礼场地"等高搜索词",
        "• <b>用户UGC未激活</b>：办过婚礼的新人是最佳代言人，但未系统化引导发笔记"
    ]
    for prob in wedding_problems:
        story.append(Paragraph(prob, styles['bullet']))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("<b>优化方向</b>", styles['h3']))
    story.append(Paragraph("• 婚礼内容占比提升至30%，每月产出4-5篇婚礼相关内容", styles['bullet']))
    story.append(Paragraph("• 覆盖高搜索关键词："成都草坪婚礼""成都户外婚礼场地""托斯卡纳风格婚礼"", styles['bullet']))
    story.append(Paragraph("• 每篇笔记必须包含：桌数、价格区间、雨天方案、服务清单", styles['bullet']))

    story.append(PageBreak())

    return story

def create_strategy_framework(styles):
    """创建策略框架"""
    story = []

    story.append(Paragraph("二、优化策略框架", styles['h1']))
    story.append(Spacer(1, 0.3*cm))

    # 战略层
    story.append(Paragraph("2.1 战略层：重新定义账号人设", styles['h2']))

    positioning_text = """
    <b>核心定位</b>：成都托斯卡纳式户外生活场景专家<br/>
    <b>Slogan</b>：在成都，过一天意式田园生活<br/><br/>

    <b>内容逻辑重构</b>：<br/>
    不是"我们有5种服务"，而是"托斯卡纳场景下的5种生活方式"<br/>
    • 草坪婚礼 = 托斯卡纳式浪漫仪式<br/>
    • 窑烤披萨 = 托斯卡纳式美食体验<br/>
    • 亲子活动 = 托斯卡纳式自然教育<br/>
    • 丝柏道打卡 = 托斯卡纳式美学空间
    """

    story.append(Paragraph(positioning_text, styles['body']))
    story.append(Spacer(1, 0.5*cm))

    # 内容层
    story.append(Paragraph("2.2 内容层：场景化选题矩阵", styles['h2']))

    content_matrix_data = [
        ['场景', '痛点型', '攻略型', '案例型'],
        ['草坪婚礼',
         '草坪婚礼5大翻车现场',
         '成都草坪婚礼场地测评TOP5',
         '60桌草坪婚礼全流程复盘'],
        ['窑烤披萨',
         '为什么窑烤比烤箱好吃10倍',
         '成都哪里能DIY窑烤披萨',
         '20人团建窑烤趴人均198'],
        ['亲子遛娃',
         '成都周边遛娃避坑指南',
         '托斯卡纳农庄遛娃攻略',
         '我们在农庄过了一天'],
        ['打卡拍照',
         '成都小托斯卡纳怎么拍出大片',
         '10个机位实测攻略',
         '闺蜜局拍照圣地人均180']
    ]

    matrix_table = Table(content_matrix_data, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 4*cm])
    matrix_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 8),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9B59B6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(matrix_table)
    story.append(Spacer(1, 0.5*cm))

    # 标题公式
    story.append(Paragraph("2.3 标题优化公式", styles['h2']))

    title_formula = """
    <b>标题公式</b>：成都/周边 + 核心卖点 + 价格/数字 + 场景/人群<br/><br/>

    <b>✅ 好标题示例</b>：<br/>
    • "成都草坪婚礼｜60桌托斯卡纳农庄｜2999元/桌含窑烤晚宴"<br/>
    • "成都周边遛娃｜人均128玩一天｜挖沙+戏水+DIY披萨"<br/>
    • "成都小托斯卡纳｜丝柏道拍照攻略｜10个机位实测"<br/><br/>

    <b>❌ 差标题示例</b>：<br/>
    • "暑气漫溢的夏日，被阳光揉成温柔滤镜"（文艺但无用）<br/>
    • "把时间浪费在美好事物上"（无信息量）<br/>
    • "一步一景，走进电影画面"（泛泛而谈）
    """

    story.append(Paragraph(title_formula, styles['body']))
    story.append(Spacer(1, 0.5*cm))

    # 转化层
    story.append(Paragraph("2.4 转化层：CTA优化", styles['h2']))

    cta_data = [
        ['现状❌', '优化后✅'],
        ['笔记结尾无引导或"欢迎来玩"', '"评论区扣【婚礼】，发你60桌方案报价"'],
        ['简介规则太多无吸引力', '"私信回复【预约】获取套餐价格+实景视频"'],
        ['私信回复慢话术不专业', '自动回复+10分钟内人工跟进+引导加企微']
    ]

    cta_table = Table(cta_data, colWidths=[7*cm, 7*cm])
    cta_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E67E22')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(cta_table)
    story.append(PageBreak())

    return story

def create_roadmap(styles):
    """创建执行路线图"""
    story = []

    story.append(Paragraph("三、执行路线图（3阶段6个月）", styles['h1']))
    story.append(Spacer(1, 0.3*cm))

    # 第一阶段
    story.append(Paragraph("阶段一：诊断与筑基（第1个月）", styles['h2']))

    phase1_tasks = [
        "• 优化账号首页（简介/头像/置顶笔记/精选合集）",
        "• 生产12篇"解决方案型"内容（草坪婚礼×4、窑烤×4、亲子×4）",
        "• 建立私信话术SOP + 企微承接流程",
        "• 启动第一轮UGC激励计划"
    ]
    for task in phase1_tasks:
        story.append(Paragraph(task, styles['bullet']))

    story.append(Spacer(1, 0.3*cm))

    phase1_results_data = [
        ['指标', '目标', '投入预算'],
        ['粉丝增长', '+500-800', '¥21,000'],
        ['爆文产出', '1-2篇（互动率>5%）', '（内容6k+投放3k+'],
        ['有效私信', '50+', 'KOC 4k+服务费8k）'],
        ['企微留资', '20-30', '']
    ]

    phase1_table = Table(phase1_results_data, colWidths=[3.5*cm, 4*cm, 6*cm])
    phase1_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1ABC9C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(phase1_table)
    story.append(Spacer(1, 0.5*cm))

    # 第二阶段
    story.append(Paragraph("阶段二：放量与转化（第2-3个月）", styles['h2']))

    phase2_tasks = [
        "• 内容批量生产（每周4-5篇，建立1个爆款带3个长尾策略）",
        "• 启动付费投流（聚光信息流+搜索广告，每个场景跑3-5条素材）",
        "• KOC矩阵合作（婚礼博主×2、亲子博主×2、探店博主×1）",
        "• 私信转化SOP落地（回复及时率>90%）"
    ]
    for task in phase2_tasks:
        story.append(Paragraph(task, styles['bullet']))

    story.append(Spacer(1, 0.3*cm))

    phase2_results_data = [
        ['指标', '目标', '月均投入'],
        ['粉丝增长', '+1,500-2,000/月', '¥34,000/月'],
        ['月均曝光', '15-20万', '（内容8k+投放8k+'],
        ['有效留资', '80-100/月', 'KOC 8k+服务费10k）'],
        ['高意向（婚礼）', '15-20/月', '预期ROI 1:4-1:7']
    ]

    phase2_table = Table(phase2_results_data, colWidths=[3.5*cm, 4*cm, 6*cm])
    phase2_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(phase2_table)
    story.append(Spacer(1, 0.5*cm))

    # 第三阶段
    story.append(Paragraph("阶段三：规模化与口碑裂变（第4-6个月）", styles['h2']))

    phase3_tasks = [
        "• 内容IP化（孵化固定栏目："成都草坪婚礼避坑指南"系列）",
        "• UGC规模化激活（每月产出10+条客户真实分享）",
        "• 数据驱动迭代（月度复盘：内容TOP10、投放ROI、转化漏斗）",
        "• 考虑孵化个人IP号（主理人出镜，增强信任感）"
    ]
    for task in phase3_tasks:
        story.append(Paragraph(task, styles['bullet']))

    story.append(Spacer(1, 0.3*cm))

    phase3_results_data = [
        ['指标', '目标', '说明'],
        ['累计粉丝', '5,000+', '形成自然流量为主结构'],
        ['月均曝光', '25-30万', '付费流量为辅'],
        ['月均留资', '150+', '小红书渠道营收'],
        ['ROI', '1:7-1:12', '≥运营投入3-5倍']
    ]

    phase3_table = Table(phase3_results_data, colWidths=[3.5*cm, 4*cm, 6*cm])
    phase3_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9B59B6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(phase3_table)
    story.append(PageBreak())

    return story

def create_case_studies(styles):
    """创建案例展示"""
    story = []

    story.append(Paragraph("四、案例展示", styles['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("以下案例涵盖不同阶段账号（成熟账号优化、0-1冷启动），证明我们的方法论在不同场景下均可落地。", styles['body']))
    story.append(Spacer(1, 0.3*cm))

    # 案例对比表
    cases_data = [
        ['案例', '类型', '核心策略', '关键成果'],
        ['四悦哉婚礼',
         '成熟账号优化',
         '内容转型+付费投放+私信SOP',
         '3个月粉丝+50%，留资率×4'],
        ['四春生场地',
         '0-1冷启动',
         '精准定位+爆款打造+投放加速',
         '2个月2000粉，2篇爆文'],
        ['祥和餐饮',
         '本地生活',
         '场景化内容+团购+达人矩阵',
         '团购核销×4，营收占比30%'],
        ['牧云台民宿',
         '冷启动中',
         '视觉升级+场景聚焦+测试迭代',
         '1个月480粉，已成交2单']
    ]

    cases_table = Table(cases_data, colWidths=[2.5*cm, 2.5*cm, 4*cm, 4.5*cm])
    cases_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 8),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(cases_table)
    story.append(Spacer(1, 0.5*cm))

    # 详细案例
    story.append(Paragraph("案例一：四春生 —— 0到1冷启动典范", styles['h2']))

    chunsheng_text = """
    <b>📊 账号情况（接手时）</b>：新账号，粉丝<200，无系统化内容规划<br/><br/>

    <b>🎯 我们做了什么</b>：<br/>
    • 精准定位：聚焦"成都小众婚礼场地"差异化标签<br/>
    • 爆款打造：<br/>
      - 第1篇爆文："成都婚礼｜2999元/桌｜这个草坪场地藏不住了"（曝光12万，涨粉800+）<br/>
      - 第2篇爆文："婚礼预算5万和50万的区别｜真实对比"（曝光8万，收藏/点赞比38%）<br/>
    • 冷启动破圈：前10篇内容精打细磨，确保质量，同步聚光小额投放（每篇200-500元）<br/><br/>

    <b>✅ 运营成果（2个月）</b>：<br/>
    • 粉丝突破2000，产出2篇爆款（曝光8万+）<br/>
    • 已进入自然流量正循环，月均留资15+，成交3单
    """

    story.append(Paragraph(chunsheng_text, styles['body']))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("案例二：牧云台 —— 正在进行的冷启动项目", styles['h2']))

    muyuntai_text = """
    <b>📊 账号情况（接手1个月）</b>：新账号，粉丝<500，定位高端民宿+活动场地，挑战客单价高（人均800+）<br/><br/>

    <b>🎯 我们正在做的事</b>：<br/>
    • 内容策略：聚焦"成都周边团建/公司年会/小型婚礼"三大场景<br/>
    • 视觉升级：统一视觉风格（自然系+高级感），每篇笔记至少9图，确保"氛围感拉满"<br/>
    • 冷启动策略：前期每周3-4篇内容，聚光小额投放测试（单篇500-1000元）<br/><br/>

    <b>✅ 阶段性成果（1个月）</b>：<br/>
    • 粉丝增长至480，产出8篇内容，平均互动率6.2%<br/>
    • 有效咨询12组，其中2组已签约（团建+小型婚礼），正在进入流量爬坡期
    """

    story.append(Paragraph(muyuntai_text, styles['body']))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("<b>共同点</b>：不盲目追求粉丝量，聚焦精准流量+高转化；内容策略基于用户决策路径；数据驱动迭代。", styles['body']))

    story.append(PageBreak())

    return story

def create_team_intro(styles):
    """创建团队介绍"""
    story = []

    story.append(Paragraph("五、团队介绍", styles['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("我们是一支<b>垂直于婚嫁与本地生活赛道的小红书运营团队</b>", styles['body']))
    story.append(Spacer(1, 0.3*cm))

    team_advantages = [
        "• <b>行业经验</b>：核心成员来自婚嫁垂直领域头部公司，操盘过10+本地生活商家从0到1冷启动",
        "• <b>运营能力</b>：擅长"内容-投放-转化"全链路，自研《小红书本地生活商家运营SOP》",
        "• <b>专注方向</b>：不做泛流量，只做高转化的精准流量；不做代运营外包，做陪跑式深度合作"
    ]
    for adv in team_advantages:
        story.append(Paragraph(adv, styles['bullet']))

    story.append(Spacer(1, 0.5*cm))

    # 差异化对比
    story.append(Paragraph("我们的差异化", styles['h2']))

    diff_data = [
        ['维度', '传统代运营', '我们的模式'],
        ['服务深度', '按月交付内容数量', '深度陪跑，目标=生意增长'],
        ['内容质量', '批量生产，模板化', '定制化策略，每篇都是作品'],
        ['数据透明', '只给阅读/点赞数据', '全链路数据看板，从曝光到成交可追踪'],
        ['转化能力', '只管涨粉，不管转化', '以留资率和ROI为核心考核指标'],
        ['行业理解', '泛运营团队', '深耕婚嫁与本地生活赛道']
    ]

    diff_table = Table(diff_data, colWidths=[3*cm, 5*cm, 5.5*cm])
    diff_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(diff_table)
    story.append(PageBreak())

    return story

def create_next_steps(styles):
    """创建下一步行动"""
    story = []

    story.append(Paragraph("六、下一步行动", styles['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("如果您对我们的服务感兴趣，欢迎：", styles['body']))
    story.append(Spacer(1, 0.3*cm))

    steps = [
        "<b>Step 1：预约深度沟通（1小时线上会议）</b><br/>我们会深入了解您的业务目标、现状、预算，给出初步诊断和建议",
        "<b>Step 2：获取详细方案</b><br/>基于沟通结果，我们会定制专属方案，包含执行排期、预算拆解、预期ROI",
        "<b>Step 3：小范围测试合作（可选）</b><br/>可先从1个月试运营开始，用数据说话，效果好再深度合作"
    ]

    for i, step in enumerate(steps, 1):
        story.append(Paragraph(f"{step}", styles['body']))
        story.append(Spacer(1, 0.3*cm))

    story.append(Spacer(1, 0.5*cm))

    # 联系方式
    contact_data = [
        ['联系方式', '[此处填写联系方式]'],
        ['提案有效期', '30天'],
        ['文档版本', 'V1.0 | 2026年8月17日']
    ]

    contact_table = Table(contact_data, colWidths=[4*cm, 9*cm])
    contact_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), font_name, 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    story.append(contact_table)
    story.append(Spacer(1, 1*cm))

    # 底部说明
    footer_text = """
    <i>* 本提案基于2026年8月17日抓取的真实账号数据（迷迭香农庄，小红书ID 538177362），<br/>
    诊断结论和优化方案均基于实际情况制定。</i>
    """
    story.append(Paragraph(footer_text, styles['body']))

    return story

def main():
    """主函数"""
    output_path = "C:/Users/EDY/mslearn-ai-agents/deliverables/迷迭香农庄_小红书账号诊断与运营提案.pdf"

    # 创建PDF文档
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # 创建样式
    styles = create_styles()

    # 构建文档内容
    story = []

    # 1. 封面
    story.extend(create_cover_page(styles))

    # 2. 执行摘要
    story.extend(create_executive_summary(styles))

    # 3. 内容板块分析
    story.extend(create_content_analysis(styles))

    # 4. 策略框架
    story.extend(create_strategy_framework(styles))

    # 5. 执行路线图
    story.extend(create_roadmap(styles))

    # 6. 案例展示
    story.extend(create_case_studies(styles))

    # 7. 团队介绍
    story.extend(create_team_intro(styles))

    # 8. 下一步行动
    story.extend(create_next_steps(styles))

    # 生成PDF
    doc.build(story)

    print(f"✅ PDF提案已生成：{output_path}")
    print(f"📄 文件大小：{os.path.getsize(output_path) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
