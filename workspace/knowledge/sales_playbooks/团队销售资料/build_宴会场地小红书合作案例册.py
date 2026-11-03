from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

HERE = Path(__file__).resolve().parent
UMI = HERE.parents[1]
SOURCE = HERE / '宴会场地小红书合作案例册_20260924.md'
OUTPUT = HERE.parent / 'output' / 'pdf' / '宴会场地小红书运营合作案例册_20260924.pdf'
ASSETS = UMI / '02_客户数据与素材' / '素材' / '团队案例素材库_20260908'
W, H = A4
LEFT, RIGHT = 48, W - 48
WIDTH = RIGHT - LEFT
FONT, BOLD = 'Case-YaHei', 'Case-YaHei-Bold'
INK = colors.HexColor('#162B2B')
TEAL = colors.HexColor('#196761')
CORAL = colors.HexColor('#DD6B57')
MUTED = colors.HexColor('#526366')
PALE = colors.HexColor('#F1F6F4')
LINE = colors.HexColor('#D7E2E0')

def sections():
    result, key = {}, None
    for raw in SOURCE.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if line.startswith('### '):
            key = line[4:6]
            result[key] = {'title': line[7:], 'body': []}
        elif line.startswith('## '):
            key = None
        elif key and line:
            result[key]['body'].append(line)
    return result

def text(c, value, x, y, size=11, color=INK, bold=False):
    c.setFont(BOLD if bold else FONT, size)
    c.setFillColor(color)
    c.drawString(x, y, value)

def para(c, value, x, y, width=WIDTH, size=10.5, leading=17, color=INK, bold=False):
    style = ParagraphStyle('p', fontName=BOLD if bold else FONT, fontSize=size, leading=leading, textColor=color, wordWrap='CJK')
    p = Paragraph(value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), style)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, y - height)
    return y - height

def frame(c, page, label):
    c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL); c.rect(0, H - 9, W, 9, fill=1, stroke=0)
    text(c, 'UMI  /  宴会场地合作案例', LEFT, H - 39, 9.5, TEAL, True)
    text(c, label, RIGHT - pdfmetrics.stringWidth(label, FONT, 9), H - 39, 9, MUTED)
    c.setStrokeColor(LINE); c.line(LEFT, H - 51, RIGHT, H - 51); c.line(LEFT, 48, RIGHT, 48)
    text(c, '对外沟通版  ·  2026.09', LEFT, 29, 8.5, MUTED)
    text(c, f'{page:02d} / 07', RIGHT - 38, 29, 8.5, MUTED)

def header(c, number, title, deck):
    text(c, number, LEFT, 743, 12, CORAL, True)
    text(c, title, LEFT, 704, 24, INK, True)
    para(c, deck, LEFT, 675, size=10.5, color=MUTED)

def cover(c, s):
    c.setFillColor(INK); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL); c.rect(0, H - 12, W, 12, fill=1, stroke=0)
    text(c, 'UMI  /  TEAM CASES', LEFT, 765, 12, colors.HexColor('#84D1C4'), True)
    c.setFillColor(CORAL); c.rect(LEFT, 548, 49, 5, fill=1, stroke=0)
    text(c, '宴会场地', LEFT, 663, 35, colors.white, True)
    text(c, '小红书运营', LEFT, 607, 35, colors.white, True)
    text(c, '合作案例', LEFT, 487, 40, colors.white, True)
    para(c, s['body'][1], LEFT, 441, 430, 13, 23, colors.HexColor('#D7E6E2'))
    c.setStrokeColor(colors.HexColor('#4D6868')); c.line(LEFT, 249, RIGHT, 249)
    text(c, '祥和花园  /  悦哉（乐哉餐饮）  /  牧云台', LEFT, 214, 10.5, colors.white)
    text(c, '春生  /  介个院子  /  麓山宴  /  可悦  /  臻里八号', LEFT, 187, 10.5, colors.white)
    text(c, s['body'][2], LEFT, 80, 9, colors.HexColor('#B8CBC7'))
    c.showPage()


def image_fit(c, path, x, y, max_width, max_height):
    image = ImageReader(str(path)); iw, ih = image.getSize()
    scale = min(max_width / iw, max_height / ih); dw, dh = iw * scale, ih * scale
    ix, iy = x + (max_width - dw) / 2, y + (max_height - dh) / 2
    c.setFillColor(PALE); c.roundRect(x - 5, y - 5, max_width + 10, max_height + 10, 5, fill=1, stroke=0)
    c.drawImage(image, ix, iy, width=dw, height=dh, mask='auto')

def case(c, page, s, image_path, note, fact_label):
    frame(c, page, '账号案例')
    header(c, f'{page - 1:02d}', s['title'], '以下为留档主页截图，展示页面可见信息，不代表当前实时状态。')
    image_fit(c, image_path, LEFT, 371, WIDTH, 244)
    text(c, fact_label, LEFT, 341, 9, TEAL, True)
    y = 315
    for line in s['body']:
        y = para(c, line, LEFT, y, size=10.6, leading=18); y -= 18
    text(c, note, LEFT, 74, 8.1, MUTED)
    c.showPage()

def other_projects(c, s):
    frame(c, 6, '其他项目')
    header(c, '05', '项目覆盖与协作记录', '除三组账号页面外，以下项目有名单、工作产物或企业微信协作记录留档。')
    titles = ['春生花园', '介个院子', '麓山宴', '可悦私房菜三圣乡店', '臻里八号']
    summaries = ['客资群截图显示客户需求报备与内部协作；原图不对外展示。', '客资群截图显示报备记录；另有账号诊断及旺季方案留档。', '运营群截图显示内容沟通与协作；不据此推断平台效果。', '小红书运营方案及行动清单留档；执行范围和结果待核。', '团队正式项目名单列示；账号与结果素材待补。']
    for idx, (title, summary) in enumerate(zip(titles, summaries)):
        y = 624 - idx * 100
        c.setFillColor(PALE if idx % 2 == 0 else colors.white); c.roundRect(LEFT, y - 73, WIDTH, 83, 5, fill=1, stroke=0)
        text(c, f'{idx + 1:02d}', LEFT + 16, y - 22, 13, CORAL, True)
        text(c, title, LEFT + 57, y - 19, 13, INK, True)
        para(c, summary, LEFT + 57, y - 33, WIDTH - 75, 9.5, 15, MUTED)
    para(c, '这些项目并非同一服务范围或同一业绩口径。企业微信原图不附在本册中，任何客资记录均不等于成交结果。', LEFT, 112, size=9.3, leading=15, color=TEAL)
    c.showPage()

def close(c, s):
    frame(c, 7, '合作洽谈')
    header(c, '06', '先聊一次场地现状', '合作前先确认目标客户、现有内容素材和销售承接能力。')
    questions = ['目前最希望获得哪类宴会客户？', '场地有哪些可直接展示的真实空间与服务证据？', '谁负责回复咨询、安排到场和记录报价？']
    for idx, item in enumerate(questions):
        y = 606 - idx * 93
        c.setFillColor(PALE); c.roundRect(LEFT, y - 56, WIDTH, 71, 5, fill=1, stroke=0)
        text(c, f'0{idx + 1}', LEFT + 18, y - 16, 15, TEAL, True)
        para(c, item, LEFT + 68, y - 11, WIDTH - 91, 12, 19, bold=True)
    c.setStrokeColor(LINE); c.line(LEFT, 320, RIGHT, 320)
    text(c, '建议的第一步', LEFT, 287, 13, INK, True)
    para(c, s['body'][1], LEFT, 269, size=10.2, leading=17)
    text(c, '外发与试运行前核对', LEFT, 186, 12, INK, True)
    para(c, '项目名称与截图授权；各项目实际服务范围；现有咨询、预约、报价和成交数据的统一口径。', LEFT, 168, size=9.7, leading=16, color=MUTED)
    c.setFillColor(TEAL); c.roundRect(LEFT, 76, WIDTH, 48, 5, fill=1, stroke=0)
    text(c, '欢迎联系发送本资料的团队成员，约一次针对场地的沟通。', LEFT + 17, 94, 10.8, colors.white, True)
    c.showPage()

def approach(c, s):
    frame(c, 2, '合作链路')
    header(c, '01', '账号之外，重视咨询承接', '让意向客户更快理解场地，也让场地知道询问从哪里来、该由谁接。')
    steps = [('被发现', '清楚展示地区、场地与可承接场景'), ('被理解', '通过真实内容回答空间、人数、价格等问题'), ('被咨询', '把档期、预算和服务需求导向明确入口'), ('被承接', '客资报备、责任人响应与线下沟通'), ('被复盘', '统一记录预约、报价与成交，判断下一步')]
    for idx, (title, desc) in enumerate(steps):
        top = 620 - idx * 84
        c.setFillColor(PALE if idx % 2 == 0 else colors.white); c.roundRect(LEFT, top - 58, WIDTH, 66, 5, fill=1, stroke=0)
        text(c, f'{idx + 1:02}', LEFT + 18, top - 17, 15, TEAL, True)
        text(c, title, LEFT + 72, top - 13, 13, INK, True); text(c, desc, LEFT + 72, top - 39, 9.6, MUTED)
    para(c, s['body'][1], LEFT, 190, size=10, leading=17)
    c.setFillColor(colors.HexColor('#E7F0EE')); c.roundRect(LEFT, 76, WIDTH, 65, 5, fill=1, stroke=0)
    para(c, '证据边界：主页说明账号呈现，工作群说明协作记录；均不能单独证明线索增量、到店率或成交额。', LEFT + 16, 128, WIDTH - 32, 9.4, 15, TEAL)
    c.showPage()

def main():
    pdfmetrics.registerFont(TTFont(FONT, 'C:/Windows/Fonts/msyh.ttc', subfontIndex=0))
    pdfmetrics.registerFont(TTFont(BOLD, 'C:/Windows/Fonts/msyhbd.ttc', subfontIndex=0))
    s = sections(); OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    c.setTitle('宴会场地小红书运营合作案例册'); c.setAuthor('UMI')
    cover(c, s['01']); approach(c, s['02'])
    cases = [
        (3, '03', ASSETS / '02_祥和' / '02_小红书主页_祥和花园.png', '素材：团队案例库 / 祥和主页；企业微信信息仅作脱敏提炼。', '截图可见：账号定位、宴会空间、咨询导向内容'),
        (4, '04', ASSETS / '03_悦哉' / '02_小红书主页_乐哉餐饮.png', '素材：团队案例库 / 乐哉餐饮主页；项目名称口径待确认。', '截图可见：户外婚礼、草坪婚礼、私宴等场景'),
        (5, '05', ASSETS / '04_牧云台' / '02_小红书主页_牧云台.png', '素材：团队案例库 / 牧云台主页；未核实截图拍摄日期。', '截图可见：婚宴、商宴、民宿、庭院下午茶等场景'),
    ]
    for page, key, path, note, label in cases:
        if not path.is_file(): raise FileNotFoundError(path)
        case(c, page, s[key], path, note, label)
    other_projects(c, s['06']); close(c, s['07']); c.save()
    print(OUTPUT)

if __name__ == '__main__':
    main()
