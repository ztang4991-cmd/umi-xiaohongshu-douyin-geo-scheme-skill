from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, Image, HRFlowable)
from reportlab.lib.utils import ImageReader
from pathlib import Path
from datetime import date

OUT = Path('卡萨四季庭院餐厅_小红书账号诊断与运营建议_客户沟通版_20260817.pdf')
ASSET = Path('_case_assets')
FONT = r'C:\Windows\Fonts\Deng.ttf'
FONT_B = r'C:\Windows\Fonts\Dengb.ttf'
pdfmetrics.registerFont(TTFont('Deng', FONT))
pdfmetrics.registerFont(TTFont('Deng-Bold', FONT_B))

TEAL = HexColor('#0F6577')
TEAL_D = HexColor('#0B5060')
ORANGE = HexColor('#C67643')
CREAM = HexColor('#F7F2EA')
PALE = HexColor('#EDF5F4')
INK = HexColor('#24323A')
MUTED = HexColor('#66747A')
LINE = HexColor('#D9D0C3')
GREEN = HexColor('#5C7D67')
RED = HexColor('#B85D47')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', fontName='Deng-Bold', fontSize=24, leading=33, textColor=TEAL_D, alignment=TA_LEFT, spaceAfter=6))
styles.add(ParagraphStyle(name='CoverSub', fontName='Deng', fontSize=12, leading=19, textColor=INK, alignment=TA_LEFT))
styles.add(ParagraphStyle(name='Kicker', fontName='Deng-Bold', fontSize=9, leading=13, textColor=ORANGE, tracking=1.4, spaceAfter=5))
styles.add(ParagraphStyle(name='H1x', fontName='Deng-Bold', fontSize=18, leading=25, textColor=TEAL_D, spaceBefore=2, spaceAfter=8))
styles.add(ParagraphStyle(name='H2x', fontName='Deng-Bold', fontSize=12.5, leading=18, textColor=TEAL_D, spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx', fontName='Deng', fontSize=9.5, leading=16, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name='Smallx', fontName='Deng', fontSize=8.2, leading=13, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle(name='Tinyx', fontName='Deng', fontSize=7.2, leading=10, textColor=MUTED))
styles.add(ParagraphStyle(name='Cell', fontName='Deng', fontSize=8.1, leading=12, textColor=INK))
styles.add(ParagraphStyle(name='CellB', fontName='Deng-Bold', fontSize=8.2, leading=12, textColor=TEAL_D))
styles.add(ParagraphStyle(name='CellW', fontName='Deng-Bold', fontSize=8.2, leading=12, textColor=colors.white))
styles.add(ParagraphStyle(name='Quote', fontName='Deng-Bold', fontSize=11, leading=18, textColor=TEAL_D, spaceBefore=5, spaceAfter=5))
styles.add(ParagraphStyle(name='CaseTitle', fontName='Deng-Bold', fontSize=10.5, leading=15, textColor=TEAL_D))
styles.add(ParagraphStyle(name='CaseBody', fontName='Deng', fontSize=8.3, leading=12.5, textColor=INK))


def P(text, style='Bodyx'):
    return Paragraph(text, styles[style])

def bullet(items, style='Bodyx'):
    return [P('• ' + x, style) for x in items]

def section(kicker, title):
    return [P(kicker, 'Kicker'), P(title, 'H1x'), HRFlowable(width='100%', thickness=1.2, color=ORANGE, spaceBefore=0, spaceAfter=9)]

def box(text, bg=PALE, style='Bodyx', pad=10):
    t=Table([[P(text, style)]], colWidths=[174*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),0.5,bg),('LEFTPADDING',(0,0),(-1,-1),pad),('RIGHTPADDING',(0,0),(-1,-1),pad),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return t

def data_table(data, widths, header=True, font=8.1, row_bgs=None):
    rows=[]
    for r, row in enumerate(data):
        rows.append([P(str(c), 'CellW' if header and r==0 else 'Cell') for c in row])
    t=Table(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign='LEFT')
    cmds=[('GRID',(0,0),(-1,-1),0.45,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]
    if header:
        cmds += [('BACKGROUND',(0,0),(-1,0),TEAL),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    for i in range(1 if header else 0, len(data)):
        cmds.append(('BACKGROUND',(0,i),(-1,i), colors.white if i%2 else CREAM))
    if row_bgs:
        for i,c in row_bgs.items(): cmds.append(('BACKGROUND',(0,i),(-1,i),c))
    t.setStyle(TableStyle(cmds))
    return t

def card_grid(cards, cols=2, widths=None):
    if widths is None: widths=[85*mm]*cols
    rows=[]
    for i in range(0,len(cards),cols):
        row=cards[i:i+cols]
        while len(row)<cols: row.append('')
        rows.append([P(c,'Bodyx') if c else '' for c in row])
    t=Table(rows, colWidths=widths, hAlign='LEFT')
    t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.5,LINE),('INNERGRID',(0,0),(-1,-1),0.5,LINE),('BACKGROUND',(0,0),(-1,-1),CREAM),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    w,h=A4
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.5); canvas.line(18*mm, 14*mm, w-18*mm,14*mm)
    canvas.setFont('Deng',7.5); canvas.setFillColor(MUTED)
    canvas.drawString(18*mm, 9*mm, '卡萨四季庭院餐厅｜小红书账号诊断与运营建议｜客户沟通版')
    canvas.drawRightString(w-18*mm, 9*mm, f'{doc.page}')
    canvas.restoreState()

doc=SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=20*mm, title='卡萨四季庭院餐厅小红书账号诊断与运营建议')
story=[]

# Cover
story += [Spacer(1,17*mm), P('小红书账号诊断与运营建议', 'CoverTitle'), P('卡萨四季庭院餐厅', 'CoverTitle'), Spacer(1,3*mm), P('客户沟通版｜仅讨论小红书运营', 'CoverSub'), Spacer(1,16*mm)]
story.append(box('<b>核心判断</b><br/>卡萨四季的优势不是“再证明一次环境很美”，而是把都江堰玉沿路·桃花岛内的目的地空间，包装成用户愿意专程前往、愿意提前咨询、愿意带人来完成一件事的场景产品。', PALE, 'Quote', 12))
story += [Spacer(1,11*mm), P('本次诊断范围', 'H2x'), data_table([
    ['账号', '账号ID：538177362｜主页链接：客户提供的小红书主页'],
    ['商家地址', '四川省成都市都江堰市玉沿路·桃花岛内'],
    ['重点业务', '团建｜窑烤｜求婚｜草坪婚礼｜品牌发布会'],
    ['参考材料', '客户提供《卡萨四季庭院餐厅_小红书账号诊断与抖音诊断_客户沟通版_20260812(2).pdf》'],
    ['版本说明', '本版本不涉及GEO、不展开抖音，仅作为小红书合作沟通框架。'],
], [30*mm,144*mm], header=False), Spacer(1,10*mm), P('资料口径：附件公开数据抓取日为2026年8月12日；本次账号ID与地址以客户本次提供的信息为准。周边竞对部分采用公开检索与场景分类判断，具体店名、价格、投放及排名建议在合作后用平台后台与实地走访复核。', 'Smallx')]
story.append(PageBreak())

# Executive summary
story += section('01 / EXECUTIVE SUMMARY','先给结论：卡萨四季要做“目的地场景账号”，而不是普通餐厅账号')
story.append(box('一句话定位建议：<b>都江堰桃花岛内·摩洛哥风情庭院目的地</b>，承接团建、窑烤、求婚、草坪婚礼与品牌活动，让用户先理解“为什么值得来”，再进入“怎么预约”。', CREAM, 'Quote', 12))
story += [Spacer(1,5*mm), P('账号现状的核心矛盾', 'H2x')]
story.append(data_table([
 ['现状', '对经营的影响', '优化方向'],
 ['线下空间体量与辨识度强，但线上账号信息量不足', '用户看到“好看”后，仍不清楚适合谁、能做什么、要提前多久约', '从空间展示转向“场景+人群+方案+预约”'],
 ['历史知名度与明星打卡是资产，但更新断续、内容标签分散', '平台难以稳定识别账号主题，用户也难以形成近期消费理由', '建立稳定栏目与业务板块，持续重复核心关键词'],
 ['地址离成都城区约70公里，不能套用三圣乡的近场消费逻辑', '用户决策成本更高，单纯“环境很美”不足以支撑专程出发', '围绕目的地价值设计车程、路线、活动与套餐表达'],
 ['团建、窑烤、求婚、草坪婚礼、发布会均有机会', '业务多而杂，若无分层，主页会像“什么都能做”的场地广告', '以五大场景做内容矩阵，以高客单场景做转化抓手'],
], [38*mm,65*mm,71*mm]))
story += [Spacer(1,7*mm), P('建议优先级', 'H2x')]
story.append(data_table([
 ['优先级', '业务板块', '原因'],
 ['A', '团建 + 窑烤', '适合周末/工作日组织，需求频次和人数场景更容易形成内容；可承接多人、套餐和活动咨询。'],
 ['A', '求婚 + 草坪婚礼', '空间差异化最强，适合打造高收藏、高分享案例；但需要真实案例与预约信息承接。'],
 ['B', '品牌发布会', '客单与品牌背书价值高，但决策链更长，需用案例、场地参数、执行能力建立信任。'],
], [22*mm,42*mm,110*mm]))
story.append(PageBreak())

# Location research
story += section('02 / LOCATION & COMPETITION','地址不是短板本身，真正的短板是没有把“远”解释成值得')
story += [P('用户地理半径判断', 'H2x'), P('商家位于都江堰市玉沿路桃花岛内，距离成都城区约70公里。与三圣乡相比，用户不是“下班后顺路吃饭”或“城市内临时聚会”，而是需要完成一次更高成本的出行决策：谁来、怎么去、活动多长、能不能一站式解决、值不值得带人一起去。', 'Bodyx')]
story.append(data_table([
 ['人群层级', '典型动机', '小红书需要回答的问题', '适合内容'],
 ['都江堰及周边本地人', '生日、求婚、家庭聚餐、朋友聚会', '离我多远？停车方便吗？雨天能不能用？', '路线/停车/场景实拍/套餐/真实评价'],
 ['成都周边周末目的地人群', '周末出游、团建、拍照、聚会、体验型消费', '专程来一趟能玩什么？几个人合适？', '半日/一日体验、团建流程、窑烤、庭院氛围'],
 ['婚嫁决策人群', '求婚、草坪婚礼、婚礼宴会、仪式感场地', '是否适合我的人数和预算？雨天预案？能否落地？', '真实案例、动线、布置前后、档期/预约须知'],
 ['企业/品牌活动决策者', '发布会、团建、客户答谢、团队活动', '场地规格、设备、接待与执行能力如何？', '案例复盘、场地参数、分区图、服务流程'],
], [28*mm,40*mm,48*mm,58*mm]))
story += [Spacer(1,7*mm), P('周边竞对应按“用户替代方案”看，而不只按行政区看', 'H2x')]
story.append(data_table([
 ['竞对层级', '用户在比较什么', '卡萨四季应突出什么'],
 ['第一层：都江堰/青城山目的地型餐厅、民宿、庭院场地', '环境、出片、周末体验、停车与一站式活动', '5000㎡级庭院体量、摩洛哥风情、室内外复合空间、团建/婚嫁/活动承接能力'],
 ['第二层：都江堰城区宴会中心、婚宴酒店', '交通、价格、宴会标准化、接待人数', '不拼“离家近”，强调目的地仪式感、草坪与庭院独特性、可定制体验'],
 ['第三层：成都三圣乡、近郊庭院餐厅与活动空间', '即时聚餐、拍照打卡、朋友聚会、短途出行', '不直接复制三圣乡打法，转向“值得专程到都江堰完成一件事”'],
 ['第四层：农家乐/露营/烧烤/团建基地', '价格、人数、活动丰富度、自由度', '用更强的视觉资产、服务流程、场景方案和高质量案例拉开差距'],
], [43*mm,63*mm,68*mm]))
story += [Spacer(1,4*mm), P('公开检索到的区域可比样本（非完整名单、非实时排名）', 'H2x')]
story.append(box('<b>样本：</b>鑫和祥瑞禧宴中心、外滩宴会中心、东顺宴会中心、岷江新濠酒店及宏达桥农家乐等。<br/><b>判断：</b>前两类覆盖婚宴/酒店式接待，后者覆盖聚餐、团年与团建。卡萨四季要避免只拼距离与价格，应重点突出草坪庭院、窑烤体验、室内外动线、雨天预案与高质量案例。', CREAM, 'Smallx', 8))
story.append(P('公开资料参考：都江堰文旅行业页面、搜狐婚礼场地报道、风雨网婚宴场地页面、百度百科等；检索日期：2026年8月17日。合作后建议用小红书/地图平台后台与实地走访复核距离、价格、档期和内容表现。', 'Tinyx'))
story += [Spacer(1,5*mm), box('<b>地理策略结论</b><br/>不建议把账号做成“成都哪里吃饭”的泛餐饮号；建议做成“成都周边值得专程去的庭院活动目的地”。每条内容都要降低一次出行决策成本，至少回答：<b>适合谁、能做什么、几个人、怎么去、要不要预约、遇到下雨怎么办</b>。', PALE, 'Bodyx', 10)]
story.append(PageBreak())

# Module diagnosis
story += section('03 / BUSINESS MODULES','五大业务板块诊断：空间优势强，线上需要产品化与证据化')
story.append(P('以下为客户沟通层面的框架诊断，重点指出“可放大资产”和“需要补齐的线上信息”，不替代合作后的完整内容规划、脚本与拍摄清单。', 'Smallx'))
module_data=[
 ['板块','可放大的优势','当前可能的短板','建议优化抓手'],
 ['团建','庭院空间大、室内外可组合；窑烤/餐饮/活动天然适配多人场景。','若只发环境和菜品，用户不知道适合多少人、能玩多久、组织者要准备什么。','做“人数+时长+流程+预算区间+雨天预案”表达；用团建案例证明组织成本可控。'],
 ['窑烤','有记忆点、有参与感，适合周末、朋友聚会、团队活动；内容视觉强。','容易被平台归类为普通烧烤/农家乐，距离远时性价比疑问更强。','从“吃什么”升级为“来这里完成一次窑烤体验”；展示准备、过程、成品、适合人数和预约规则。'],
 ['求婚','环境与仪式感空间有差异化，适合高收藏与转发；决策者愿意为确定性付费。','缺少真实案例、流程、布置档位、隐私性与天气预案时，用户不敢私信。','用真实求婚故事、动线、布置前后、摄影位、服务边界建立信任；主页设置明确咨询入口。'],
 ['草坪婚礼','庭院、草坪、室内备选空间适合做目的地婚礼；视觉资产强。','用户最关心的不是“有没有草坪”，而是人数、档期、雨天、动线、餐饮和执行。','内容用“婚礼方案”而非单图；按小型/中型/定制型拆分，持续发布真实案例和场地参数。'],
 ['品牌发布会','空间可做品牌活动、客户答谢、团队活动，具备视觉记忆点。','企业决策者需要案例与执行能力证据，单纯氛围图很难转化。','建立案例模板：客户类型/人数/分区/流程/现场效果/复盘；用“场地能解决什么问题”替代泛宣传。'],
]
story.append(data_table(module_data,[24*mm,48*mm,49*mm,53*mm]))
story += [Spacer(1,7*mm), P('五个板块的内容分工建议', 'H2x')]
story.append(data_table([
 ['内容目标', '主攻板块', '用户动作'],
 ['扩大搜索与收藏', '窑烤、团建、草坪婚礼', '收藏路线、套餐、场地与活动灵感'],
 ['建立信任与高客单咨询', '求婚、草坪婚礼、品牌发布会', '私信人数/日期/预算/场景，进入预约沟通'],
 ['持续经营与口碑', '日常庭院、季节活动、真实客人、幕后准备', '复访、转发、带朋友到店、产生第三方内容'],
], [42*mm,58*mm,74*mm]))
story.append(PageBreak())

# Optimization framework
story += section('04 / OPTIMIZATION FRAMEWORK','优化方向框架：先重建“被看懂”，再重建“被预约”')
story += [P('A. 账号定位与主页重构', 'H2x')]
story.append(data_table([
 ['模块', '建议框架'],
 ['昵称', '卡萨四季｜都江堰桃花岛庭院餐厅（示例）——品牌名 + 地域 + 场景，不只保留品牌名。'],
 ['简介', '用四行说明：在哪里｜空间/风格｜能承接什么｜如何咨询。避免只写明星打卡与形容词。'],
 ['置顶三篇', '01 品牌总览：为什么值得专程来；02 到店决策：路线/停车/人数/餐饮；03 高客单案例：求婚/婚礼/发布会怎么落地。'],
 ['合集', '第一次来卡萨｜窑烤与团建｜求婚与婚礼｜品牌活动｜四季庭院日记｜真实客人案例。'],
], [33*mm,141*mm]))
story += [Spacer(1,6*mm), P('B. 内容矩阵建议（只给框架，不展开执行细节）', 'H2x')]
story.append(data_table([
 ['内容支柱', '建议占比', '内容角色', '示例方向'],
 ['到店决策', '35%', '解决远距离用户“值不值得来”', '成都出发怎么走、停车、适合几个人、半日怎么玩、预约前要问什么'],
 ['空间体验', '25%', '建立视觉记忆与场景想象', '庭院动线、摩洛哥风情、室内外切换、白天/夜晚/雨天差异'],
 ['活动案例', '25%', '证明能承接真实需求', '团建、窑烤、求婚、草坪婚礼、品牌发布会案例'],
 ['品牌幕后', '15%', '建立信任与持续更新理由', '备餐、布置、服务准备、四季变化、主理人和团队'],
], [31*mm,21*mm,50*mm,72*mm]))
story += [Spacer(1,6*mm), P('C. 小红书表达原则', 'H2x')]
story.extend(bullet([
 '标题从“环境很美”转为“人群+场景+结果”：例如“都江堰求婚场地怎么选”“20人团建怎样安排不尴尬”。',
 '封面要让用户一眼看懂：这是哪里、适合什么、为什么值得去；减少只有空镜的封面。',
 '正文采用“问题—现场—方案—预约信息”结构，统一补齐车程、停车、人数、时段、价格/预算口径与雨天预案。',
 '同一素材不直接搬运：小红书版本补充参数、路线、攻略与决策信息，建立收藏价值。',
], 'Bodyx'))
story.append(PageBreak())

# Conversion and metrics
story += section('05 / CONVERSION & METRICS','从“种草”到“预约”：把账号变成可测量的线索入口')
story.append(box('小红书运营的目标不是只把笔记做得好看，而是让用户在看完后知道下一步怎么做：<b>看懂场景 → 判断适配 → 私信咨询 → 到店/签单 → 真实反馈回流</b>。', CREAM, 'Quote', 12))
story += [Spacer(1,5*mm), P('建议建立四层指标，不只看点赞', 'H2x')]
story.append(data_table([
 ['指标层', '重点观察', '判断意义'],
 ['搜索', '地域词、场景词覆盖；主页访问；收藏/点赞比', '内容是否进入用户主动决策路径'],
 ['咨询', '有效私信、到店咨询、团建/婚礼/求婚/发布会需求结构', '账号是否吸引真实消费意向'],
 ['经营', '留资、到店、订位、看场、成交原因与未成交原因', '是否把线上内容与线下经营连起来'],
 ['口碑', '客户评价、授权UGC、复购与转介绍、第三方内容', '知名度是否转化为持续信任'],
], [26*mm,80*mm,68*mm]))
story += [Spacer(1,7*mm), P('合作后运营动作框架', 'H2x')]
story.append(data_table([
 ['阶段', '动作框架', '交付口径'],
 ['阶段一：接手与校准', '资料盘点、账号权限与资产梳理、业务目标确认、用户与竞对复核、主页诊断。', '形成账号定位、栏目结构、内容资产清单与优先级。'],
 ['阶段二：主页与内容重建', '主页信息重构、封面与标题方向统一、五大场景栏目建立、首批内容验证。', '形成可持续的内容框架，不公开展开具体脚本与选题库。'],
 ['阶段三：持续运营', '按栏目生产与发布、评论/私信承接、案例素材回流、数据周复盘。', '围绕搜索、咨询、到店与口碑四层指标优化。'],
 ['阶段四：专项放大', '针对团建、婚礼/求婚、品牌活动等高价值场景做专题内容与案例包装。', '按经营目标配置专项方案，具体动作在合作后项目方案中展开。'],
], [31*mm,86*mm,57*mm]))
story += [Spacer(1,7*mm), P('本版本刻意不展开的内容', 'H2x')]
story.extend(bullet(['具体月度选题库、脚本、拍摄分镜与模版', '账号发布频次、人员分工、素材管理和审核SOP', '竞品逐店数据、投放测试、预算与阶段目标', '私信话术、线索表单、复盘表及项目管理流程'], 'Bodyx'))
story.append(PageBreak())

# Team
story += section('06 / TEAM & HANDOVER','我们团队：懂婚嫁行业，也懂商家账号运营')
story.append(box('我们来自婚嫁垂直领域与运营领域的头部公司，长期服务商家的线上账号运营。我们关注的不只是内容曝光，而是把场地、产品、案例、服务能力整理成用户看得懂、愿意咨询、能落地成交的内容资产。', PALE, 'Quote', 12))
story += [Spacer(1,6*mm), P('团队能力框架', 'H2x')]
story.append(data_table([
 ['能力方向', '我们能解决的问题'],
 ['婚嫁垂直理解', '理解求婚、婚礼、宴会等业务的决策链、信任门槛、档期与现场执行要求。'],
 ['账号运营', '从定位、主页、内容、互动、数据到案例沉淀，建立持续经营的账号结构。'],
 ['场景产品化', '把“一个好看的场地”拆成适合谁、做什么、多少人、什么流程、如何预约。'],
 ['内容与经营协同', '把线上用户问题回流到门店产品、接待流程与案例采集，减少只追求表面数据。'],
], [40*mm,134*mm]))
story += [Spacer(1,7*mm), P('如果接手卡萨四季，小红书运营动作会围绕以下框架展开', 'H2x')]
story.append(data_table([
 ['动作层', '框架'],
 ['1. 重新定义账号', '明确“都江堰桃花岛目的地庭院”心智；统一地域、场景、视觉和咨询入口。'],
 ['2. 重建内容结构', '以团建、窑烤、求婚、草坪婚礼、品牌发布会为主业务栏目，辅以到店决策和品牌幕后。'],
 ['3. 建立案例资产', '持续沉淀人数、预算、流程、布置、动线、雨天预案和客户反馈等可复用信息。'],
 ['4. 做距离转化', '用路线、停车、时间成本、半日/一日体验和组合套餐，回应“离城区远”的真实顾虑。'],
 ['5. 用数据复盘', '从搜索、收藏、咨询、到店、成交、口碑六个环节判断内容是否有效。'],
], [40*mm,134*mm]))
story += [Spacer(1,7*mm), box('合作后，我们会根据卡萨四季的经营目标、真实素材、可承接产品与团队配合方式，输出专属项目方案。客户沟通版只展示方法论与执行边界，不公开完整选题库、脚本库与运营SOP。', CREAM, 'Bodyx', 10)]
story.append(PageBreak())

# Cases
story += section('07 / CASE DISPLAY','案例展示：四个项目打包看，重点看“冷启动如何建立信号”')
story.append(P('以下为团队过往在庭院餐饮、婚嫁宴会、复合场景与本地生活账号建设上的案例素材展示。案例用于说明方法与结果信号，不等同于对卡萨四季的最终结果承诺；具体数据与素材资产在“余生项目方案”中对应展开。', 'Smallx'))
case_specs=[
 ('siyuezai.png','四悦哉账号｜成熟账号结构与持续运营协同','通过统一主页视觉、场景化内容和咨询入口，让婚礼、聚会等高价值业务拥有更清晰的表达与承接路径。'),
 ('sichunsheng.png','四春生账号｜0-1起号与流量信号验证','当前处于0-1冷启动阶段，已出现两个流量爆贴，说明空间特征与用户兴趣之间已经出现有效连接；下一阶段重点是稳定栏目、复用信号、补齐转化。'),
 ('liuxianghe.png','六祥和账号｜复合场景与宴会产品包装','将宴会、场地服务与日常内容结合，帮助用户理解“能办什么、适合谁、如何咨询”，让内容从展示走向产品表达。'),
 ('muyuntai.png','牧云台账号｜接手后的冷启动建设','刚接手账号，当前处于冷启动建设期；围绕婚宴、商务、民宿、下午茶等多业态做内容分层和品牌认知建立，具体运营情况与素材在余生项目方案中展开。'),
]
# render 2x2 case cards
case_rows=[]
for i in range(0,4,2):
    row=[]
    for j in range(i,i+2):
        img=Image(str(ASSET/case_specs[j][0]), width=82*mm, height=29*mm)
        content=[img, Spacer(1,2*mm), P(case_specs[j][1],'CaseTitle'), Spacer(1,1*mm), P(case_specs[j][2],'CaseBody')]
        cell=Table([[content]], colWidths=[82*mm])
        cell.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CREAM),('BOX',(0,0),(-1,-1),0.5,LINE),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
        row.append(cell)
    case_rows.append(row)
case_table=Table(case_rows, colWidths=[87*mm,87*mm], hAlign='LEFT')
case_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story.append(case_table)
story += [Spacer(1,7*mm), box('<b>本次沟通建议</b><br/>卡萨四季不需要先复制某个案例，而是要借鉴这四类项目的共同方法：<b>明确定位、分层场景、建立信号、沉淀案例、连接咨询</b>。其中，四春生与牧云台对卡萨四季最有参考价值：一个验证冷启动起量，一个验证复合业态账号如何从“有场地”走向“有认知”。', PALE, 'Bodyx', 10)]
story.append(PageBreak())

# Closing
story += section('08 / NEXT STEP','建议的合作起点：先把账号做成“能被用户理解的目的地”')
story.append(box('卡萨四季的线上增量，不在于继续堆叠“环境很美”的照片，而在于把用户的五个问题回答清楚：<br/><br/><b>我为什么要来？我适合做什么？要带多少人？怎么预约和执行？离城区这么远，值不值得专程来？</b>', CREAM, 'Quote', 12))
story += [Spacer(1,9*mm), P('合作后首轮会优先确认的资料', 'H2x')]
story.extend(bullet(['五大业务板块当前可承接的真实产品、人数、价格/预算口径与预约方式', '近半年真实案例、客户授权、现场照片/视频、雨天与设备预案', '从成都、都江堰及周边到店的路线、停车、营业时段与接待限制', '现有账号后台数据、私信线索、到店与成交记录', '门店配合拍摄、审核、接待与素材回流的责任边界'], 'Bodyx'))
story += [Spacer(1,9*mm), P('最终建议', 'H2x'), P('以“小红书账号重建 + 五大场景内容矩阵 + 距离转化 + 案例资产沉淀”为合作主线，先建立账号的可识别性与可咨询性，再根据数据决定重点放大团建、窑烤、求婚、草坪婚礼或品牌发布会。', 'Bodyx'), Spacer(1,9*mm), P('谢谢｜期待与卡萨四季一起，把桃花岛内这座庭院做成用户愿意专程去完成一件事的目的地。', 'Quote'), Spacer(1,16*mm), P('附：本稿仅作为客户沟通版框架，不包含完整执行方案、脚本、选题库、SOP、投放计划及数据承诺。', 'Smallx')]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT.resolve())

