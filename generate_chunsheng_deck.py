# -*- coding: utf-8 -*-
"""Generate a projection-friendly client deck for Chunsheng Garden."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output" / "pdf"
ASCII_OUTPUT = OUTPUT_DIR / "chunsheng_garden_account_growth_meeting.pdf"
CHINESE_OUTPUT = OUTPUT_DIR / "春生花园_账号矩阵与内容增长沟通方案.pdf"

PAGE_W, PAGE_H = landscape(A4)

FONT_REGULAR = "YaHei"
FONT_BOLD = "YaHeiBold"

INK = HexColor("#17352F")
GREEN = HexColor("#1F6A55")
GREEN_DARK = HexColor("#13483B")
MINT = HexColor("#E7F1EC")
MINT_LIGHT = HexColor("#F3F8F5")
CORAL = HexColor("#D96C50")
CORAL_LIGHT = HexColor("#F8EAE5")
GOLD = HexColor("#B88A3B")
GOLD_LIGHT = HexColor("#F6F0E4")
TEXT = HexColor("#24302D")
MUTED = HexColor("#66736F")
LINE = HexColor("#D9E1DE")
PAPER = HexColor("#FAFBF9")
WHITE = HexColor("#FFFFFF")

MARGIN_X = 48
CONTENT_W = PAGE_W - MARGIN_X * 2


def register_fonts():
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, r"C:\Windows\Fonts\msyh.ttc"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, r"C:\Windows\Fonts\msyhbd.ttc"))


def rounded_box(c, x, y, w, h, fill, stroke=None, radius=7, line_width=0.8):
    c.setLineWidth(line_width)
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)


def draw_text(c, text, x, y, size=12, color=TEXT, font=FONT_REGULAR):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def draw_right(c, text, x, y, size=10, color=MUTED, font=FONT_REGULAR):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawRightString(x, y, text)


def wrap_text(text, max_width, size, font=FONT_REGULAR):
    """Wrap Chinese and mixed text by rendered width."""
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and pdfmetrics.stringWidth(candidate, font, size) > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, max_width, size=12, leading=None, color=TEXT,
                 font=FONT_REGULAR, max_lines=None):
    leading = leading or size * 1.55
    lines = wrap_text(text, max_width, size, font)
    if max_lines:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        draw_text(c, line, x, y - i * leading, size, color, font)
    return y - len(lines) * leading


def draw_bullet(c, text, x, y, max_width, size=10.5, color=TEXT,
                dot_color=GREEN, leading=16):
    c.setFillColor(dot_color)
    c.circle(x + 3, y + 4, 2.3, fill=1, stroke=0)
    lines = wrap_text(text, max_width - 16, size, FONT_REGULAR)
    for i, line in enumerate(lines):
        draw_text(c, line, x + 14, y - i * leading, size, color)
    return y - max(1, len(lines)) * leading


def page_chrome(c, page_no, section):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_text(c, "CHUNSHENG GARDEN", MARGIN_X, PAGE_H - 27, 7.5, GREEN, FONT_BOLD)
    draw_right(c, section, PAGE_W - MARGIN_X, PAGE_H - 27, 8, MUTED)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN_X, 29, PAGE_W - MARGIN_X, 29)
    draw_text(c, "春生花园｜账号矩阵与内容增长沟通方案", MARGIN_X, 14, 7.5, MUTED)
    draw_right(c, f"{page_no:02d} / 07", PAGE_W - MARGIN_X, 14, 7.5, MUTED, FONT_BOLD)


def title_block(c, kicker, title, subtitle=None):
    draw_text(c, kicker, MARGIN_X, PAGE_H - 66, 9, CORAL, FONT_BOLD)
    draw_text(c, title, MARGIN_X, PAGE_H - 101, 23, INK, FONT_BOLD)
    if subtitle:
        draw_text(c, subtitle, MARGIN_X, PAGE_H - 125, 10.5, MUTED)


def number_badge(c, x, y, number, fill=GREEN):
    c.setFillColor(fill)
    c.circle(x, y, 13, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 10)
    c.setFillColor(WHITE)
    c.drawCentredString(x, y - 3.5, str(number))


def page_cover(c):
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#2E5148"))
    c.setLineWidth(0.5)
    for x in range(0, int(PAGE_W), 52):
        c.line(x, 0, x, PAGE_H)
    for y in range(0, int(PAGE_H), 52):
        c.line(0, y, PAGE_W, y)
    c.setFillColor(GREEN_DARK)
    c.circle(PAGE_W - 80, PAGE_H - 58, 145, fill=1, stroke=0)
    c.setFillColor(CORAL)
    c.rect(PAGE_W - 154, 0, 154, 12, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(PAGE_W - 174, 12, 20, 86, fill=1, stroke=0)
    draw_text(c, "CHUNSHENG GARDEN", 60, PAGE_H - 62, 10, HexColor("#A7CABB"), FONT_BOLD)
    draw_text(c, "春生花园", 60, PAGE_H - 184, 38, WHITE, FONT_BOLD)
    draw_text(c, "账号矩阵与内容增长沟通方案", 60, PAGE_H - 232, 25, WHITE, FONT_BOLD)
    c.setFillColor(CORAL)
    c.rect(60, PAGE_H - 257, 54, 4, fill=1, stroke=0)
    draw_wrapped(c, "围绕企业号认证、账号分工、内容供给与冷启动投入，\n明确从基础建设到稳定获客的协同路径。", 60, PAGE_H - 300, 520, 12.5, 23, HexColor("#D9E8E1"))
    rounded_box(c, 60, 62, 238, 34, HexColor("#24483E"), HexColor("#3E655A"), 5)
    draw_text(c, "客户沟通会版本  ·  2026.08", 76, 73, 9.5, WHITE, FONT_BOLD)
    draw_right(c, "账号基础建设｜内容增长｜获客转化", PAGE_W - 58, 32, 8.5, HexColor("#A7CABB"))


def page_meeting_goal(c):
    page_chrome(c, 2, "MEETING OBJECTIVE")
    title_block(c, "01｜本次会议目标", "先统一关键决策，再进入执行", "围绕三个前置条件达成一致，确保账号运营具备持续性与转化基础。")
    card_y, card_h, gap = 250, 172, 16
    card_w = (CONTENT_W - gap * 2) / 3
    cards = [
        ("01", "账号基础建设", "确认企业号认证路径、现有账号归属及管理员权限。", GREEN, MINT),
        ("02", "内容生产机制", "确认素材来源、拍摄配合与日常更新的责任分工。", CORAL, CORAL_LIGHT),
        ("03", "首月冷启动投入", "确认种草频次、预算区间及首月重点验证指标。", GOLD, GOLD_LIGHT),
    ]
    for i, (num, head, body, accent, fill) in enumerate(cards):
        x = MARGIN_X + i * (card_w + gap)
        rounded_box(c, x, card_y, card_w, card_h, fill, LINE, 7)
        draw_text(c, num, x + 18, card_y + card_h - 31, 10, accent, FONT_BOLD)
        draw_text(c, head, x + 18, card_y + card_h - 69, 16, INK, FONT_BOLD)
        draw_wrapped(c, body, x + 18, card_y + card_h - 103, card_w - 36, 10.5, 18, TEXT)
        c.setFillColor(accent)
        c.rect(x, card_y, card_w, 5, fill=1, stroke=0)
    rounded_box(c, MARGIN_X, 145, CONTENT_W, 75, INK, None, 7)
    draw_text(c, "共识原则", MARGIN_X + 20, 194, 9, HexColor("#A7CABB"), FONT_BOLD)
    draw_text(c, "认证、内容与种草同步推进", MARGIN_X + 20, 165, 16, WHITE, FONT_BOLD)
    draw_right(c, "先建立可持续运营能力，再逐步放大投放与转化。", PAGE_W - MARGIN_X - 20, 169, 11, HexColor("#D9E8E1"))


def page_certification(c):
    page_chrome(c, 3, "ENTERPRISE VERIFICATION")
    title_block(c, "02｜企业号认证", "认证可执行，建议与内容建设同步启动", "法人年龄不构成平台限制，关键在于完成微信扫码、身份核验与人脸识别。")
    rounded_box(c, MARGIN_X, 384, CONTENT_W, 55, MINT, GREEN, 7)
    draw_text(c, "结论", MARGIN_X + 18, 406, 9, GREEN, FONT_BOLD)
    draw_text(c, "当前认证路径清晰，可在法人可配合时间内一次完成。", MARGIN_X + 74, 403, 14, INK, FONT_BOLD)
    draw_text(c, "认证流程", MARGIN_X, 352, 11, INK, FONT_BOLD)
    flow_y = 292
    labels = [("后台发起", "生成企业认证二维码"), ("法人核验", "微信扫码并确认身份"), ("人脸识别", "按页面指引完成核验"), ("账号完善", "绑定管理员并补齐资料")]
    flow_w, flow_gap = 162, 28
    for i, (head, body) in enumerate(labels):
        x = MARGIN_X + i * (flow_w + flow_gap)
        rounded_box(c, x, flow_y, flow_w, 78, WHITE, LINE, 6)
        number_badge(c, x + 21, flow_y + 56, i + 1, GREEN if i < 3 else CORAL)
        draw_text(c, head, x + 43, flow_y + 53, 11.5, INK, FONT_BOLD)
        draw_wrapped(c, body, x + 16, flow_y + 25, flow_w - 32, 8.8, 13, MUTED)
        if i < len(labels) - 1:
            c.setStrokeColor(GREEN)
            c.setLineWidth(1.2)
            c.line(x + flow_w + 7, flow_y + 39, x + flow_w + flow_gap - 7, flow_y + 39)
            c.setFillColor(GREEN)
            c.wedge(x + flow_w + flow_gap - 13, flow_y + 35, x + flow_w + flow_gap - 5, flow_y + 43, 270, 180, fill=1, stroke=0)
    left_w = 465
    rounded_box(c, MARGIN_X, 113, left_w, 142, WHITE, LINE, 7)
    draw_text(c, "认证前建议准备", MARGIN_X + 18, 229, 11, INK, FONT_BOLD)
    y = 202
    y = draw_bullet(c, "6-10 条基础内容：店铺介绍、婚宴服务、案例与空间卖点", MARGIN_X + 18, y, left_w - 36)
    y = draw_bullet(c, "统一头像、简介、联系方式和私信承接口径", MARGIN_X + 18, y - 3, left_w - 36)
    draw_bullet(c, "明确认证后持续供材与内容更新机制", MARGIN_X + 18, y - 3, left_w - 36)
    right_x = MARGIN_X + left_w + 16
    right_w = CONTENT_W - left_w - 16
    rounded_box(c, right_x, 113, right_w, 142, INK, None, 7)
    draw_text(c, "本次需确认", right_x + 18, 229, 10, HexColor("#A7CABB"), FONT_BOLD)
    for i, item in enumerate(["法人可配合时间", "账号管理员权限", "认证后供材意愿"]):
        yy = 198 - i * 34
        c.setStrokeColor(HexColor("#6D9186"))
        c.setLineWidth(1)
        c.rect(right_x + 18, yy - 2, 12, 12, fill=0, stroke=1)
        draw_text(c, item, right_x + 42, yy, 10.5, WHITE, FONT_BOLD)


def page_matrix(c):
    page_chrome(c, 4, "ACCOUNT MATRIX")
    title_block(c, "03｜账号矩阵", "不同账号承担不同任务，形成协同获客", "避免账号内容同质化，让每个账号都对应明确的人群、内容与转化任务。")
    x0, y_top = MARGIN_X, 425
    col_widths = [150, 151, 286, 156]
    headers = ["账号角色", "核心任务", "重点内容", "转化承接"]
    row_h, header_h = 63, 36
    c.setFillColor(INK)
    c.roundRect(x0, y_top - header_h, CONTENT_W, header_h, 6, fill=1, stroke=0)
    x = x0
    for title, width in zip(headers, col_widths):
        draw_text(c, title, x + 14, y_top - 24, 9, WHITE, FONT_BOLD)
        x += width
    rows = [
        ("婚宴主账号 / 企业号", "官方信任与婚宴获客", "品牌介绍、婚宴案例、套餐权益、服务能力", "咨询 / 到店 / 预约"),
        ("备婚获客号", "覆盖搜索与决策场景", "选址攻略、预算避坑、备婚清单、案例拆解", "私信 / 线索收集"),
        ("素材 / 素人内容号", "持续种草与氛围传播", "探店体验、活动花絮、员工日常、现场记录", "互动 / 引流主号"),
        ("餐厅账号", "餐饮场景与业务联动", "漂亮饭、聚会、商拍、打卡场景、特色菜品", "团购 / 到店消费"),
    ]
    for r, row in enumerate(rows):
        y = y_top - header_h - (r + 1) * row_h
        c.setFillColor(WHITE if r % 2 == 0 else MINT_LIGHT)
        c.setStrokeColor(LINE)
        c.rect(x0, y, CONTENT_W, row_h, fill=1, stroke=1)
        x = x0
        for col, (value, width) in enumerate(zip(row, col_widths)):
            color = GREEN if col == 0 else TEXT
            font = FONT_BOLD if col in (0, 1) else FONT_REGULAR
            size = 9.2 if col != 2 else 8.8
            draw_wrapped(c, value, x + 14, y + 39, width - 26, size, 14, color, font, 2)
            x += width
    rounded_box(c, MARGIN_X, 103, CONTENT_W, 50, CORAL_LIGHT, None, 6)
    draw_text(c, "现有两个小号建议分工：", MARGIN_X + 18, 121, 10, CORAL, FONT_BOLD)
    draw_text(c, "1 个承担备婚获客与搜索种草，1 个承担日常素材更新与内容分发。", MARGIN_X + 160, 121, 11.5, INK, FONT_BOLD)


def page_content(c):
    page_chrome(c, 5, "CONTENT SYSTEM")
    title_block(c, "04｜内容与素材", "先建立持续供给，再放大内容效果", "装修期与开业后的内容任务不同，应分阶段建设素材资产和用户信任。")
    half_w = (CONTENT_W - 16) / 2
    y, h = 290, 145
    stages = [
        ("阶段 1｜装修 / 筹备期", "建立期待与专业认知", ["装修进度与空间规划", "过往婚宴案例与服务流程", "套餐能力、选址攻略与备婚知识"], MINT, GREEN),
        ("阶段 2｜装修完成 / 开业后", "集中形成视觉说服力", ["空间全景、宴会场景与菜品", "真实婚礼记录与客户评价", "漂亮饭、商拍、打卡与活动联动"], CORAL_LIGHT, CORAL),
    ]
    for i, (head, sub, bullets, fill, accent) in enumerate(stages):
        x = MARGIN_X + i * (half_w + 16)
        rounded_box(c, x, y, half_w, h, fill, None, 7)
        draw_text(c, head, x + 18, y + h - 28, 11.5, accent, FONT_BOLD)
        draw_text(c, sub, x + 18, y + h - 54, 15, INK, FONT_BOLD)
        yy = y + h - 83
        for bullet in bullets:
            yy = draw_bullet(c, bullet, x + 18, yy, half_w - 36, 9.5, TEXT, accent, 15)
    draw_text(c, "首批素材库", MARGIN_X, 257, 11, INK, FONT_BOLD)
    assets = ["空间环境", "婚礼案例", "宴席菜品", "套餐权益", "服务流程", "商拍场景", "装修过程", "团队日常"]
    gap = 8
    pill_w = (CONTENT_W - gap * 7) / 8
    for i, asset in enumerate(assets):
        x = MARGIN_X + i * (pill_w + gap)
        rounded_box(c, x, 210, pill_w, 32, WHITE, LINE, 5)
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(GREEN if i < 5 else CORAL)
        c.drawCentredString(x + pill_w / 2, 221, asset)
    rounded_box(c, MARGIN_X, 103, CONTENT_W, 84, INK, None, 7)
    draw_text(c, "建议的内容生产机制", MARGIN_X + 18, 160, 9, HexColor("#A7CABB"), FONT_BOLD)
    mechanisms = [("每月选题", "确定主题与发布节奏"), ("集中拍摄", "固定半天建立素材库存"), ("日常补充", "员工花絮与现场轻量记录"), ("数据复盘", "按咨询与到店线索优化内容")]
    item_w = (CONTENT_W - 36) / 4
    for i, (head, body) in enumerate(mechanisms):
        x = MARGIN_X + 18 + i * item_w
        draw_text(c, f"0{i + 1}", x, 126, 9, CORAL, FONT_BOLD)
        draw_text(c, head, x + 26, 126, 10.5, WHITE, FONT_BOLD)
        draw_text(c, body, x, 109, 8.5, HexColor("#BCD2C9"))


def page_budget(c):
    page_chrome(c, 6, "COLD START BUDGET")
    title_block(c, "05｜冷启动投入", "用真实内容积累初期信任，再逐步放大", "首月重点不是追求单篇爆量，而是建立搜索可见度、口碑密度和咨询承接链路。")
    left_w = 490
    rounded_box(c, MARGIN_X, 194, left_w, 232, WHITE, LINE, 7)
    draw_text(c, "建议预算档位", MARGIN_X + 20, 399, 11, INK, FONT_BOLD)
    rows = [
        ("基础档", "900-1,000 元 / 月", "约 30 篇", "平均每天 1 篇", GREEN, MINT),
        ("高频档", "1,800 元 / 月起", "约 60 篇", "每天约 2 篇 + 互动维护", CORAL, CORAL_LIGHT),
    ]
    for i, (tier, budget, volume, cadence, accent, fill) in enumerate(rows):
        yy = 303 - i * 88
        rounded_box(c, MARGIN_X + 20, yy, left_w - 40, 72, fill, None, 6)
        rounded_box(c, MARGIN_X + 34, yy + 17, 70, 38, accent, None, 5)
        c.setFont(FONT_BOLD, 10)
        c.setFillColor(WHITE)
        c.drawCentredString(MARGIN_X + 69, yy + 31, tier)
        draw_text(c, budget, MARGIN_X + 122, yy + 39, 13, INK, FONT_BOLD)
        draw_text(c, f"{volume}  ·  {cadence}", MARGIN_X + 122, yy + 18, 9.5, MUTED)
    right_x = MARGIN_X + left_w + 16
    right_w = CONTENT_W - left_w - 16
    rounded_box(c, right_x, 194, right_w, 232, INK, None, 7)
    draw_text(c, "首月重点验证", right_x + 20, 399, 11, HexColor("#A7CABB"), FONT_BOLD)
    metrics = [("内容表现", "曝光、点击、收藏与互动"), ("线索质量", "私信、咨询、到店意向"), ("承接效率", "回复速度与有效留资率"), ("方向迭代", "高表现选题与人群偏好")]
    for i, (head, body) in enumerate(metrics):
        yy = 352 - i * 47
        number_badge(c, right_x + 30, yy + 1, i + 1, CORAL if i == 1 else GREEN)
        draw_text(c, head, right_x + 54, yy + 3, 10.5, WHITE, FONT_BOLD)
        draw_text(c, body, right_x + 54, yy - 14, 8.5, HexColor("#BCD2C9"))
    rounded_box(c, MARGIN_X, 112, CONTENT_W, 56, GOLD_LIGHT, None, 6)
    draw_text(c, "执行原则", MARGIN_X + 18, 133, 9, GOLD, FONT_BOLD)
    draw_text(c, "先测试内容与承接链路，再根据咨询质量、到店线索和内容表现逐步优化预算。", MARGIN_X + 84, 131, 11.5, INK, FONT_BOLD)
    draw_text(c, "注：以上为素人种草内容预算测算，不含平台广告投放、专业拍摄及第三方达人费用。", MARGIN_X, 88, 8, MUTED)


def page_confirmation(c):
    page_chrome(c, 7, "NEXT ACTION")
    title_block(c, "06｜会议确认清单", "今天明确 6 件事，项目即可进入执行", "以下事项确认后，运营方可完成账号规划、内容筹备与首月排期。")
    items = [
        ("认证配合", "法人时间、扫码方式、管理员"),
        ("账号归属", "现有账号持有人与运营权限"),
        ("品牌定位", "主营优先级、客群与差异化"),
        ("素材机制", "拍摄配合、日常供材与审核"),
        ("内容分工", "主号、小号与餐厅号边界"),
        ("首月预算", "种草档位、频次与验证指标"),
    ]
    card_w = (CONTENT_W - 16 * 2) / 3
    card_h = 92
    for i, (head, body) in enumerate(items):
        col, row = i % 3, i // 3
        x = MARGIN_X + col * (card_w + 16)
        y = 324 - row * (card_h + 14)
        rounded_box(c, x, y, card_w, card_h, WHITE, LINE, 7)
        c.setStrokeColor(GREEN if i < 4 else CORAL)
        c.setLineWidth(1.2)
        c.rect(x + 18, y + 57, 14, 14, fill=0, stroke=1)
        draw_text(c, f"0{i + 1}", x + card_w - 40, y + 61, 9, MUTED, FONT_BOLD)
        draw_text(c, head, x + 44, y + 59, 12, INK, FONT_BOLD)
        draw_wrapped(c, body, x + 18, y + 29, card_w - 36, 9.3, 14, MUTED)
    rounded_box(c, MARGIN_X, 93, CONTENT_W, 100, INK, None, 7)
    draw_text(c, "会后输出", MARGIN_X + 20, 165, 9, HexColor("#A7CABB"), FONT_BOLD)
    outputs = ["账号定位与资料清单", "首批选题与脚本", "探店 / 拍摄计划", "种草预算与执行排期"]
    segment_w = (CONTENT_W - 40) / 4
    for i, output in enumerate(outputs):
        x = MARGIN_X + 20 + i * segment_w
        if i:
            c.setStrokeColor(HexColor("#41685E"))
            c.line(x - 14, 112, x - 14, 160)
        draw_text(c, f"0{i + 1}", x, 136, 9, CORAL, FONT_BOLD)
        draw_text(c, output, x + 25, 136, 10.5, WHITE, FONT_BOLD)
        draw_text(c, "确认后进入执行", x + 25, 116, 8.5, HexColor("#BCD2C9"))


def build_pdf(path):
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("春生花园｜账号矩阵与内容增长沟通方案")
    c.setAuthor("运营项目组")
    c.setSubject("企业号认证、账号矩阵、内容供给与冷启动沟通方案")
    for page in [page_cover, page_meeting_goal, page_certification, page_matrix, page_content, page_budget, page_confirmation]:
        page(c)
        c.showPage()
    c.save()


if __name__ == "__main__":
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_pdf(ASCII_OUTPUT)
    CHINESE_OUTPUT.write_bytes(ASCII_OUTPUT.read_bytes())
    print(ASCII_OUTPUT)
    print(CHINESE_OUTPUT)
