#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迷迭香农庄 - 小红书账号诊断与运营提案 PDF生成器
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('msyh', 'C:/Windows/Fonts/msyh.ttc'))
    CN_FONT = 'msyh'
except:
    CN_FONT = 'Helvetica'

def make_styles():
    styles = getSampleStyleSheet()

    return {
        'title': ParagraphStyle('title', parent=styles['Heading1'], fontName=CN_FONT, fontSize=24,
                               textColor=colors.HexColor('#2C3E50'), spaceAfter=30, alignment=TA_CENTER, leading=36),
        'h1': ParagraphStyle('h1', parent=styles['Heading1'], fontName=CN_FONT, fontSize=18,
                            textColor=colors.HexColor('#34495E'), spaceAfter=12, spaceBefore=20, leading=28),
        'h2': ParagraphStyle('h2', parent=styles['Heading2'], fontName=CN_FONT, fontSize=14,
                            textColor=colors.HexColor('#5D6D7E'), spaceAfter=10, spaceBefore=15, leading=22),
        'h3': ParagraphStyle('h3', parent=styles['Heading3'], fontName=CN_FONT, fontSize=12,
                            textColor=colors.HexColor('#7F8C8D'), spaceAfter=8, spaceBefore=12, leading=18),
        'body': ParagraphStyle('body', parent=styles['BodyText'], fontName=CN_FONT, fontSize=10,
                              textColor=colors.HexColor('#2C3E50'), spaceAfter=8, leading=16, alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet', parent=styles['BodyText'], fontName=CN_FONT, fontSize=10,
                                textColor=colors.HexColor('#2C3E50'), leftIndent=20, spaceAfter=6, leading=16)
    }

def build_pdf():
    output = "C:/Users/EDY/mslearn-ai-agents/deliverables/迷迭香农庄_小红书运营提案.pdf"
    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    s = make_styles()
    story = []

    # 封面
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("迷迭香农庄", s['title']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("小红书账号诊断与运营提案", s['h1']))
    story.append(Spacer(1, 3*cm))

    account_data = [
        ['账号名称', '迷迭香农庄'], ['小红书ID', '538177362'],
        ['粉丝数', '3,543'], ['获赞收藏', '17,000'],
        ['IP属地', '四川成都'], ['提案日期', '2026年8月17日']
    ]
    t = Table(account_data, colWidths=[5*cm, 8*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 11),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#ECF0F1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('PADDING', (0,0), (-1,-1), 10)
    ]))
    story.append(t)
    story.append(PageBreak())

    # 执行摘要
    story.append(Paragraph("执行摘要", s['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("账号现状", s['h2']))
    for txt in [
        "粉丝基数：3,543粉丝，1.7万获赞收藏，处于初期成长阶段",
        "内容产出：61篇可见笔记，内容稳定但爆款率低（小于2%）",
        "唯一爆款：一场非常哇塞的婚礼（1,225赞），证明婚礼内容是流量密码",
        "核心问题：定位模糊、转化链条断裂、商业化效率低"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("三大致命问题", s['h2']))
    problems = [
        ['问题层级', '具体表现', '影响'],
        ['战略层：定位模糊', '窑烤+婚礼+亲子+团建混杂', '品牌认知混乱，流量分散'],
        ['内容层：转化弱', '标题信息密度低，缺价格/位置/预约方式', '流量有但留资少'],
        ['转化层：闭环缺失', '笔记→私信→留资→成交链条断裂', '估算转化损失70%+']
    ]
    t = Table(problems, colWidths=[4*cm, 5.5*cm, 4.5*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 9),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("核心优化策略", s['h2']))
    for txt in [
        "重新定位：成都托斯卡纳式户外生活场景专家",
        "内容升级：从记录型转向解决方案型，标题加价格/位置/场景信息",
        "流量策略：聚光投放 + KOC矩阵 + UGC激励，提升爆款率至10%+",
        "转化优化：笔记CTA + 私信SOP + 企微承接，留资率提升至5%+"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("预期成果（6个月）", s['h2']))
    results = [
        ['指标', '第1个月', '第2-3个月', '第4-6个月'],
        ['粉丝增长', '+500-800', '+1,500/月', '累计5,000+'],
        ['月均曝光', '8-10万', '15-20万', '25-30万'],
        ['有效留资', '20-30', '80-100/月', '150+/月'],
        ['预估ROI', '测试期', '1:4-1:7', '1:7-1:12']
    ]
    t = Table(results, colWidths=[3.5*cm]*4)
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 9),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#27AE60')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t)
    story.append(PageBreak())

    # 内容板块诊断
    story.append(Paragraph("一、内容板块诊断（基于61篇真实笔记）", s['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("1.1 内容板块概览", s['h2']))
    overview = [
        ['板块', '占比', '互动表现', '核心问题', '优化优先级'],
        ['窑烤披萨', '25%', '置顶66赞，其余5-18赞', '转化引导缺失', '★★★★'],
        ['草坪婚礼', '10%', '爆款1,225赞', '内容占比过低', '★★★★★'],
        ['亲子遛娃', '20%', '5-13赞', '价格信息模糊', '★★★★'],
        ['氛围打卡', '40%', '5-26赞', '纯氛围无转化', '★★'],
        ['团建活动', '5%', '5-10赞', '平台用户错位', '★']
    ]
    t = Table(overview, colWidths=[2.8*cm, 2*cm, 3*cm, 3*cm, 2.5*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E74C3C')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("1.2 草坪婚礼板块（核心重点）", s['h2']))
    story.append(Paragraph("优势", s['h3']))
    for txt in [
        "爆款验证：一场非常哇塞的婚礼（1,225赞）证明婚礼内容是流量密码",
        "场地视觉优势：草坪、丝柏道、红砖拱门符合小红书婚礼审美",
        "情绪共鸣强：在这里，每一个重要时刻都值得被完美铭记"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("致命问题", s['h3']))
    for txt in [
        "婚礼笔记占比过低：61篇笔记中仅5-6篇提及婚礼（应占30%+）",
        "核心痛点未解答：能办多少桌？雨天怎么办？价格区间？",
        "搜索关键词缺失：未覆盖成都草坪婚礼等高搜索词",
        "用户UGC未激活：未系统化引导客户发笔记"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("标题优化示例", s['h3']))
    title_opt = [
        ['现状标题❌', '优化后标题✅'],
        ['把婚礼搬进大自然', '成都草坪婚礼｜60桌托斯卡纳农庄｜2999元/桌含窑烤晚宴'],
        ['草坪、阳光、白纱', '成都户外婚礼场地｜托斯卡纳风格｜雨天Plan B全攻略']
    ]
    t = Table(title_opt, colWidths=[6.5*cm, 7*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#95A5A6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t)
    story.append(PageBreak())

    # 策略框架
    story.append(Paragraph("二、优化策略框架", s['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("2.1 重新定位", s['h2']))
    story.append(Paragraph("核心定位：成都托斯卡纳式户外生活场景专家", s['body']))
    story.append(Paragraph("Slogan：在成都，过一天意式田园生活", s['body']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("内容逻辑重构", s['h3']))
    for txt in [
        "草坪婚礼 = 托斯卡纳式浪漫仪式",
        "窑烤披萨 = 托斯卡纳式美食体验",
        "亲子活动 = 托斯卡纳式自然教育",
        "丝柏道打卡 = 托斯卡纳式美学空间"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("2.2 场景化选题矩阵", s['h2']))
    matrix = [
        ['场景', '痛点型', '攻略型', '案例型'],
        ['草坪婚礼', '5大翻车现场', '场地测评TOP5', '60桌婚礼全流程'],
        ['窑烤披萨', '为什么比烤箱好吃10倍', '哪里能DIY窑烤', '20人团建窑烤趴'],
        ['亲子遛娃', '周边遛娃避坑指南', '农庄遛娃攻略', '我们在农庄过了一天']
    ]
    t = Table(matrix, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 4*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#9B59B6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("2.3 标题公式", s['h2']))
    story.append(Paragraph("成都/周边 + 核心卖点 + 价格/数字 + 场景/人群", s['body']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("好标题示例：", s['h3']))
    for txt in [
        "成都草坪婚礼｜60桌托斯卡纳农庄｜2999元/桌含窑烤晚宴",
        "成都周边遛娃｜人均128玩一天｜挖沙+戏水+DIY披萨",
        "成都小托斯卡纳｜丝柏道拍照攻略｜10个机位实测"
    ]:
        story.append(Paragraph(f"✅ {txt}", s['bullet']))
    story.append(PageBreak())

    # 执行路线图
    story.append(Paragraph("三、执行路线图（3阶段6个月）", s['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("阶段一：诊断与筑基（第1个月）", s['h2']))
    for txt in [
        "优化账号首页（简介/头像/置顶笔记）",
        "生产12篇解决方案型内容（草坪婚礼×4、窑烤×4、亲子×4）",
        "建立私信话术SOP + 企微承接流程",
        "启动第一轮UGC激励计划"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))
    story.append(Spacer(1, 0.3*cm))

    phase1 = [
        ['指标', '目标', '投入预算'],
        ['粉丝增长', '+500-800', '21,000元'],
        ['爆文产出', '1-2篇', '（内容6k+投放3k+'],
        ['有效私信', '50+', 'KOC 4k+服务费8k）'],
        ['企微留资', '20-30', '']
    ]
    t = Table(phase1, colWidths=[3.5*cm, 4*cm, 6*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 9),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1ABC9C')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("阶段二：放量与转化（第2-3个月）", s['h2']))
    for txt in [
        "内容批量生产（每周4-5篇）",
        "启动付费投流（聚光信息流+搜索广告）",
        "KOC矩阵合作（每月3-5个）",
        "私信转化SOP落地（回复及时率>90%）"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))
    story.append(Spacer(1, 0.3*cm))

    phase2 = [
        ['指标', '目标', '月均投入'],
        ['粉丝增长', '+1,500-2,000', '34,000元/月'],
        ['月均曝光', '15-20万', 'ROI 1:4-1:7']
    ]
    t = Table(phase2, colWidths=[3.5*cm, 4*cm, 6*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 9),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t)
    story.append(PageBreak())

    # 案例展示
    story.append(Paragraph("四、案例展示", s['h1']))
    story.append(Spacer(1, 0.3*cm))

    cases = [
        ['案例', '类型', '核心策略', '关键成果'],
        ['四悦哉婚礼', '成熟账号优化', '内容转型+付费投放+私信SOP', '3个月粉丝+50%，留资率×4'],
        ['四春生场地', '0-1冷启动', '精准定位+爆款打造+投放加速', '2个月2000粉，2篇爆文'],
        ['祥和餐饮', '本地生活', '场景化内容+团购+达人矩阵', '团购核销×4，营收占比30%'],
        ['牧云台民宿', '冷启动中', '视觉升级+场景聚焦+测试迭代', '1个月480粉，已成交2单']
    ]
    t = Table(cases, colWidths=[2.5*cm, 2.5*cm, 4*cm, 4.5*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E74C3C')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("案例详解：四春生 - 0到1冷启动典范", s['h2']))
    story.append(Paragraph("账号情况（接手时）：新账号，粉丝小于200，无系统化内容规划", s['body']))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("我们做了什么：", s['h3']))
    for txt in [
        "精准定位：聚焦成都小众婚礼场地差异化标签",
        "爆款打造：第1篇爆文曝光12万涨粉800+，第2篇爆文曝光8万",
        "冷启动破圈：前10篇内容精打细磨，同步聚光小额投放"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("运营成果（2个月）：粉丝突破2000，产出2篇爆款，月均留资15+，成交3单", s['body']))
    story.append(PageBreak())

    # 团队介绍
    story.append(Paragraph("五、团队介绍", s['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("我们是垂直于婚嫁与本地生活赛道的小红书运营团队", s['body']))
    story.append(Spacer(1, 0.3*cm))

    for txt in [
        "行业经验：核心成员来自婚嫁垂直领域头部公司，操盘过10+本地生活商家从0到1冷启动",
        "运营能力：擅长内容-投放-转化全链路，自研小红书本地生活商家运营SOP",
        "专注方向：不做泛流量，只做高转化的精准流量；不做代运营外包，做陪跑式深度合作"
    ]:
        story.append(Paragraph(f"• {txt}", s['bullet']))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("我们的差异化", s['h2']))
    diff = [
        ['维度', '传统代运营', '我们的模式'],
        ['服务深度', '按月交付内容数量', '深度陪跑，目标=生意增长'],
        ['内容质量', '批量生产，模板化', '定制化策略，每篇都是作品'],
        ['数据透明', '只给阅读/点赞数据', '全链路数据看板，从曝光到成交可追踪'],
        ['转化能力', '只管涨粉，不管转化', '以留资率和ROI为核心考核指标']
    ]
    t = Table(diff, colWidths=[3*cm, 5*cm, 5.5*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 9),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#34495E')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t)
    story.append(PageBreak())

    # 下一步
    story.append(Paragraph("六、下一步行动", s['h1']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("如果您对我们的服务感兴趣，欢迎：", s['body']))
    story.append(Spacer(1, 0.3*cm))

    for txt in [
        "Step 1：预约深度沟通（1小时线上会议）",
        "Step 2：获取详细方案（执行排期、预算拆解、预期ROI）",
        "Step 3：小范围测试合作（可先从1个月试运营开始）"
    ]:
        story.append(Paragraph(txt, s['body']))
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.5*cm))
    contact = [
        ['联系方式', '[此处填写联系方式]'],
        ['提案有效期', '30天'],
        ['文档版本', 'V1.0 | 2026年8月17日']
    ]
    t = Table(contact, colWidths=[4*cm, 9*cm])
    t.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), CN_FONT, 10),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#ECF0F1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('PADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(t)
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("本提案基于2026年8月17日抓取的真实账号数据，诊断结论和优化方案均基于实际情况制定。", s['body']))

    doc.build(story)
    print(f"PDF已生成：{output}")
    print(f"文件大小：{os.path.getsize(output)/1024:.1f} KB")

if __name__ == "__main__":
    build_pdf()
