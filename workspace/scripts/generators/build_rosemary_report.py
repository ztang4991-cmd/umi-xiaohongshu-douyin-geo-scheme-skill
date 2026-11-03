from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
from pathlib import Path

OUT = Path('迷迭香农庄_小红书账号诊断与运营建议_客户沟通版_20260817.pdf')
ASSET = Path('_merchant_assets')
CASE = Path('_case_assets')
pdfmetrics.registerFont(TTFont('Deng', r'C:\Windows\Fonts\Deng.ttf'))
pdfmetrics.registerFont(TTFont('Deng-Bold', r'C:\Windows\Fonts\Dengb.ttf'))

TEAL = HexColor('#0F6577')
TEAL_D = HexColor('#0B5060')
ORANGE = HexColor('#C67643')
CREAM = HexColor('#F7F2EA')
PALE = HexColor('#EDF5F4')
INK = HexColor('#24323A')
MUTED = HexColor('#66747A')
LINE = HexColor('#D9D0C3')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', fontName='Deng-Bold', fontSize=24, leading=33, textColor=TEAL_D, spaceAfter=6))
styles.add(ParagraphStyle(name='CoverSub', fontName='Deng', fontSize=12, leading=19, textColor=INK))
styles.add(ParagraphStyle(name='Kicker', fontName='Deng-Bold', fontSize=9, leading=13, textColor=ORANGE, spaceAfter=5))
styles.add(ParagraphStyle(name='H1x', fontName='Deng-Bold', fontSize=18, leading=25, textColor=TEAL_D, spaceAfter=8))
styles.add(ParagraphStyle(name='H2x', fontName='Deng-Bold', fontSize=12.2, leading=17, textColor=TEAL_D, spaceBefore=6, spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx', fontName='Deng', fontSize=9.2, leading=15, textColor=INK, spaceAfter=4))
styles.add(ParagraphStyle(name='Smallx', fontName='Deng', fontSize=8.1, leading=12.5, textColor=MUTED, spaceAfter=3))
styles.add(ParagraphStyle(name='Tinyx', fontName='Deng', fontSize=7.1, leading=10, textColor=MUTED))
styles.add(ParagraphStyle(name='Cell', fontName='Deng', fontSize=8, leading=11.7, textColor=INK))
styles.add(ParagraphStyle(name='CellW', fontName='Deng-Bold', fontSize=8, leading=11.7, textColor=colors.white))
styles.add(ParagraphStyle(name='Quote', fontName='Deng-Bold', fontSize=10.5, leading=17, textColor=TEAL_D))
styles.add(ParagraphStyle(name='CaseTitle', fontName='Deng-Bold', fontSize=10, leading=14, textColor=TEAL_D))
styles.add(ParagraphStyle(name='CaseBody', fontName='Deng', fontSize=8, leading=12, textColor=INK))

def P(s, name='Bodyx'): return Paragraph(s, styles[name])
def section(kicker, title): return [P(kicker, 'Kicker'), P(title, 'H1x'), HRFlowable(width='100%', thickness=1.2, color=ORANGE, spaceAfter=8)]
def box(text, bg=PALE, style='Bodyx', pad=10):
    t=Table([[P(text,style)]], colWidths=[174*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),0.5,bg),('LEFTPADDING',(0,0),(-1,-1),pad),('RIGHTPADDING',(0,0),(-1,-1),pad),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return t
def table(data, widths, header=True):
    rows=[]
    for i,row in enumerate(data): rows.append([P(str(c),'CellW' if header and i==0 else 'Cell') for c in row])
    t=Table(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign='LEFT')
    cmds=[('GRID',(0,0),(-1,-1),0.45,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    if header: cmds += [('BACKGROUND',(0,0),(-1,0),TEAL),('TEXTCOLOR',(0,0),(-1,0),colors.white)]
    for i in range(1 if header else 0,len(data)): cmds.append(('BACKGROUND',(0,i),(-1,i),colors.white if i%2 else CREAM))
    t.setStyle(TableStyle(cmds)); return t
def bullets(items): return [P('• '+x,'Bodyx') for x in items]
def footer(canvas, doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(LINE); canvas.setLineWidth(.5); canvas.line(18*mm,14*mm,w-18*mm,14*mm)
    canvas.setFont('Deng',7.3); canvas.setFillColor(MUTED)
    canvas.drawString(18*mm,9*mm,'迷迭香农庄｜小红书账号诊断与运营建议｜客户沟通版')
    canvas.drawRightString(w-18*mm,9*mm,str(doc.page)); canvas.restoreState()

doc=SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=20*mm, title='迷迭香农庄小红书账号诊断与运营建议')
story=[]

# 01 Cover
story += [Spacer(1,17*mm), P('小红书账号诊断与运营建议','CoverTitle'), P('迷迭香农庄','CoverTitle'), Spacer(1,3*mm), P('客户沟通版｜仅讨论小红书运营','CoverSub'), Spacer(1,16*mm)]
story.append(box('<b>核心判断</b><br/>迷迭香农庄已拥有“新派乡村园林美学、红砖拱门、大草坪、意式窑炉披萨、预约制私域场所”等鲜明资产。账号下一步不应继续只发氛围图，而要把这些资产整理成用户能快速判断、愿意收藏并主动咨询的<b>目的地场景答案</b>。', PALE, 'Quote', 12))
story += [Spacer(1,10*mm), P('本次诊断口径','H2x')]
story.append(table([
 ['项目','信息'],
 ['账号主体','迷迭香农庄｜小红书号：538177362｜IP属地：四川'],
 ['主页公开信息','73关注｜3,543粉丝｜1.7万获赞与收藏（以客户提供截图为准）'],
 ['商家属性','原住民私域场所／新派乡村园林美学空间／预约制接待'],
 ['地址','都江堰市玉沿路桃花岛内（客户提供）'],
 ['重点业务','团建｜窑烤／披萨体验｜求婚｜草坪婚礼｜品牌发布会'],
 ['资料边界','本稿仅讨论小红书；附件《卡萨四季…》仅作为案例素材参考，不作为本商家诊断依据。'],
 ],[35*mm,139*mm]))
story += [Spacer(1,8*mm), P('关键校正说明：本报告的诊断对象为“迷迭香农庄”，不是卡萨四季。账号公开主页数据、简介与笔记样本来自客户提供的迷迭香农庄主页截图。', 'Smallx'), PageBreak()]

# 02 Snapshot
story += section('01 / ACCOUNT SNAPSHOT','账号不是从零开始：已有明确审美资产，但业务表达仍不够完整')
story.append(Image(str(ASSET/'profile_overview.png'), width=174*mm, height=60.5*mm))
story += [Spacer(1,5*mm), P('主页公开信息解读','H2x')]
story.append(table([
 ['维度','当前信号','诊断结论'],
 ['品牌名','迷迭香农庄','名称有记忆点，但没有前置“都江堰／桃花岛／婚礼／团建／窑烤”等高意图场景词。'],
 ['简介','原住民私域场所、新派乡村园林美学空间、预约制、10:00-19:00','调性清晰，但用户仍不知道：适合多少人、可办什么活动、如何预约、距离和停车如何处理。'],
 ['粉丝与互动','3,543粉丝、1.7万获赞与收藏','账号已有内容基础和审美吸引力，重点应放在把已有注意力转成搜索、收藏和有效咨询。'],
 ['可见内容','窑炉披萨、红砖拱门、大草坪、夏日庭院、新景预告','空间与产品都具备内容性，但主线仍偏“好看”，业务板块与转化信息不足。'],
 ],[28*mm,60*mm,86*mm]))
story += [Spacer(1,6*mm), box('<b>一句话定位建议</b><br/>都江堰桃花岛内的预约制乡村园林美学农庄：可以吃一顿窑炉披萨，也可以完成一次求婚、草坪婚礼、团建或品牌活动。', CREAM, 'Quote', 12), PageBreak()]

# 03 Diagnosis
story += section('02 / BUSINESS DIAGNOSIS','五大业务板块诊断：优势很具体，线上必须“产品化”')
story.append(table([
 ['板块','已有优势','当前线上短板','小红书优化重点'],
 ['团建','预约制私域感、大草坪、红砖庭院、餐饮与体验可组合。','看不出适合多少人、活动时长、组织者要准备什么、雨天是否可执行。','把团建写成方案：人数+时长+餐饮+活动+场地分区+雨天预案，降低企业HR和行政的组织成本。'],
 ['窑烤／披萨','“600℃窑炉、90秒披萨”是明确记忆点，制作过程具备强视觉与互动。','目前更像单品展示，缺少“谁适合来体验、怎么预约、多人怎么玩、价格口径”等决策信息。','从菜品图升级为体验产品：窑炉过程、食材、多人分享、亲友／团建版本、预约规则与到店路线。'],
 ['求婚','红砖拱门、草坪、乡村园林、预约制私密感，天然适合仪式感内容。','若没有真实案例、布置前后、隐私性、服务边界和天气预案，用户不敢咨询。','用真实案例与流程证明确定性：动线、布置、摄影位、餐饮、备用空间、咨询入口。'],
 ['草坪婚礼','草坪与庭院构成差异化视觉资产，适合目的地婚礼和小型仪式。','用户关心人数、档期、餐饮、雨天、交通、过夜与执行能力，空镜无法回答。','持续输出“真实婚礼方案”，按规模／需求拆分；把动线、时间、雨天和服务边界讲透。'],
 ['品牌发布会','空间风格强、场景新、适合审美型品牌活动与客户答谢。','没有形成B端案例证明：面积、分区、设备、餐饮、接待与执行能力。','建立发布会案例模版：客户类型+人数+布置+流程+现场效果+复盘，不只发现场照片。'],
 ],[22*mm,41*mm,52*mm,59*mm]))
story += [Spacer(1,6*mm), P('优先级建议','H2x')]
story.append(table([
 ['优先级','业务','原因'],
 ['A','窑烤／披萨 + 团建','现有内容与空间最容易形成“看得懂、愿意分享”的周末及多人消费理由。'],
 ['A','求婚 + 草坪婚礼','最能体现私域感、草坪和红砖空间差异，应尽快用真实案例建立高客单信任。'],
 ['B','品牌发布会','价值高但决策链更长，需等案例与场地参数内容同步补齐后重点放大。'],
 ],[22*mm,48*mm,104*mm]))
story.append(PageBreak())

# 04 Location
story += section('03 / LOCATION & COMPETITION','离城区约70公里：不做“顺路消费”，而做“值得专程去”的目的地')
story += [P('都江堰玉沿路桃花岛内的地理位置，决定迷迭香农庄的用户不是三圣乡那种“下班后临时吃饭、拍照”的近场用户，而是需要提前规划一次出行的人。距离不是天然劣势，前提是账号要让用户相信：这一趟有足够的体验密度与仪式价值。','Bodyx'), P('与三圣乡用户画像的关键差异','H2x')]
story.append(table([
 ['人群','核心动机','账号需要补齐的信息'],
 ['都江堰／周边本地人','生日、求婚、家庭聚会、朋友聚餐','路线、停车、营业时段、预约方式、雨天可用空间'],
 ['成都周末目的地人群','团建、拍照、体验型餐饮、亲友聚会','车程值不值、半日怎么玩、多人如何安排、披萨／草坪／庭院组合体验'],
 ['婚嫁人群','求婚、草坪婚礼、小型仪式','档期、人数、预算口径、动线、布置、餐饮、雨天预案'],
 ['企业／品牌客户','团建、发布会、客户答谢','面积、分区、设备、流程、接待能力、往期案例'],
 ],[34*mm,61*mm,79*mm]))
story += [Spacer(1,6*mm), P('竞对不应只看“附近哪家餐厅”，而要看用户会拿什么替代方案比较','H2x')]
story.append(table([
 ['竞对层级','用户比较什么','迷迭香农庄的差异化表达'],
 ['都江堰／青城山目的地餐厅、民宿、庭院场地','出片、体验、停车、周末活动、住宿／一站式','新派乡村园林美学、红砖草坪、预约制私域、窑炉披萨体验与仪式场景组合'],
 ['都江堰宴会中心与酒店婚宴','交通、人数、标准化、价格、婚宴服务','不直接拼“离城区近”，突出户外草坪与私密感、审美场景、可定制体验与真实案例'],
 ['三圣乡／成都近郊庭院场地','即时聚餐、拍照打卡、短途活动','把“远”翻译为目的地价值：专程来一次，能完成吃、玩、拍、聚会、仪式的组合体验'],
 ['农家乐、露营、烧烤与团建基地','价格、人数、活动自由度','用更高的审美、窑炉体验、服务流程、布置能力和案例品质拉开差距'],
 ],[43*mm,62*mm,69*mm]))
story += [Spacer(1,6*mm), box('<b>地理策略结论</b><br/>每条笔记至少要回答五个问题：<b>适合谁、能做什么、几个人、怎么去、为什么值得专程来</b>。尤其是团建、求婚、草坪婚礼与品牌活动，要把“预约制”“私密性”“距离”“停车”“雨天方案”写进内容，而不是留给用户私信反复问。', PALE, 'Bodyx', 10), PageBreak()]

# 05 Framework
story += section('04 / OPTIMIZATION FRAMEWORK','优化方向框架：让用户在5秒内看懂“这里能帮我完成什么”')
story += [P('主页重构框架','H2x')]
story.append(table([
 ['模块','建议框架'],
 ['昵称','迷迭香农庄｜都江堰桃花岛庭院婚礼团建（示例）——品牌名+地域+高意图场景。'],
 ['简介','四行表达：在哪里｜空间特色｜可承接的五类场景｜预约方式与营业信息。把“预约制私域场所”翻译成用户听得懂的消费理由。'],
 ['置顶三篇','01 第一次来：路线、停车、预约、能玩什么；02 窑炉披萨／团建：人数、流程与体验；03 求婚／草坪婚礼：真实案例与雨天预案。'],
 ['合集','第一次来迷迭香｜窑炉披萨体验｜团建与聚会｜求婚与草坪婚礼｜品牌活动｜农庄四季。'],
 ],[34*mm,140*mm]))
story += [Spacer(1,5*mm), P('内容矩阵建议（只展示合作框架）','H2x')]
story.append(table([
 ['内容支柱','建议占比','内容作用','示例'],
 ['到店决策','30%','降低70公里目的地决策成本','成都出发攻略、停车、预约、适合人数、半日行程'],
 ['窑炉与餐饮体验','25%','建立可记住、可分享的产品钩子','600℃窑炉、90秒披萨、多人分享、制作体验'],
 ['婚嫁与仪式案例','25%','证明私密性与高客单承接力','求婚、草坪婚礼、布置前后、雨天预案、真实故事'],
 ['团建／品牌活动','15%','建立B端需求入口','人数、场地分区、流程、餐饮与现场效果'],
 ['农庄美学与幕后','5%','维持调性、补充信任','四季景观、备餐、布置、服务准备'],
 ],[28*mm,22*mm,50*mm,74*mm]))
story += [Spacer(1,6*mm), P('内容表达标准','H2x')]
story += bullets(['封面不只放空镜，必须让用户知道：这是都江堰哪里、是什么场景、适合谁。','标题从“氛围感”升级为“人群+场景+结果”，例如“成都周边20人团建怎么选”“都江堰草坪求婚场地怎么安排”。','正文固定补齐：时间、人数、路线、停车、预约、餐饮／活动、雨天预案；没有价格时至少给出预算或询价口径。','把披萨、红砖、草坪、庭院从零散素材串成一个统一叙事：在迷迭香农庄，完成一场有美感的相聚或仪式。'])
story.append(PageBreak())

# 06 Team + conversion
story += section('05 / TEAM & HANDOVER','我们的角色：把审美空间变成可经营的线上账号资产')
story.append(box('我们来自婚嫁垂直领域与运营领域的头部公司，专注于商家的线上账号运营。我们不把小红书当成只做曝光的渠道，而是围绕场地、产品、案例和服务能力，搭建用户看得懂、愿意咨询、能回流门店的内容系统。', CREAM, 'Quote', 12))
story += [Spacer(1,6*mm), P('接手后的运营动作框架（不展开SOP）','H2x')]
story.append(table([
 ['阶段','框架动作','本阶段目的'],
 ['接手与校准','核验五类业务的可承接能力、现有内容资产、线索来源、用户问题与竞对。','确认账号承诺与线下接待能力一致，避免内容“好看但接不住”。'],
 ['账号重建','统一昵称、简介、置顶、合集、封面、标题与五大场景栏目。','让用户进入主页后能立刻完成基本判断。'],
 ['内容验证','围绕窑炉、团建、求婚、草坪婚礼、发布会做首批场景内容验证。','验证哪类内容最能带来收藏、搜索与有效咨询。'],
 ['持续运营','内容生产、发布、评论／私信承接、案例回流与数据复盘。','把一次内容表现变成可复制的长期资产。'],
 ['专项放大','对表现和成交更好的业务板块做专题内容与案例包装。','将经营资源集中在高价值、可转化场景。'],
 ],[31*mm,88*mm,55*mm]))
story += [Spacer(1,6*mm), P('复盘不只看点赞','H2x')]
story.append(table([
 ['指标层','重点观察'],
 ['搜索','地域词与场景词覆盖、主页访问、收藏／点赞比'],
 ['咨询','有效私信、人数、日期、预算、业务板块与到店意向'],
 ['经营','看场、订位、到店、成交及未成交原因'],
 ['口碑','真实客户反馈、授权UGC、复购与转介绍'],
 ],[35*mm,139*mm]))
story += [Spacer(1,7*mm), box('<b>本版本不公开展开</b><br/>月度选题库、脚本与分镜、拍摄清单、发布节奏、私信话术、投放测试、数据看板与项目SOP，将在合作启动后的专属项目方案中结合迷迭香农庄的真实业务与素材确定。', PALE, 'Bodyx', 10), PageBreak()]

# 07 cases
story += section('06 / CASE DISPLAY','案例展示：方法可借鉴，但迷迭香农庄需要自己的起号路径')
story.append(P('以下案例来自客户提供的参考 PDF，用于说明我们在庭院餐饮、婚嫁宴会与复合场景账号建设上的方法。案例截图不是迷迭香农庄自身数据或项目成果；具体案例数据与素材资产，在“余生项目方案”中对应展开。','Smallx'))
case_items=[
 ('siyuezai.png','四悦哉账号｜成熟账号结构与持续运营协同','通过统一主页、场景化内容和咨询入口，让婚礼、聚会等业务拥有清晰表达与承接路径。'),
 ('sichunsheng.png','四春生账号｜0-1起号与流量信号验证','当前处于0-1起号阶段，已出现两个流量爆贴，验证“有场地”到“有人看”的第一轮信号；下一步是稳定栏目与补齐转化。'),
 ('liuxianghe.png','六祥和账号｜复合场景与宴会产品包装','把宴会、场地服务与日常内容连接起来，让用户理解能办什么、适合谁、怎样咨询。'),
 ('muyuntai.png','牧云台账号｜接手后的冷启动建设','刚接手账号，处于冷启动建设期；围绕婚宴、商务、民宿、下午茶做内容分层和品牌认知，具体运营情况在余生项目方案中展开。'),
]
rows=[]
for i in range(0,4,2):
    row=[]
    for j in range(i,i+2):
        f,title,desc=case_items[j]
        cell=Table([[[Image(str(CASE/f),width=82*mm,height=29*mm), Spacer(1,2*mm), P(title,'CaseTitle'), Spacer(1,1*mm), P(desc,'CaseBody')]]],colWidths=[82*mm])
        cell.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CREAM),('BOX',(0,0),(-1,-1),.5,LINE),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
        row.append(cell)
    rows.append(row)
ct=Table(rows,colWidths=[87*mm,87*mm])
ct.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
story.append(ct)
story += [Spacer(1,7*mm), box('<b>对迷迭香农庄的借鉴重点</b><br/>不复制别人的封面或选题，而是借鉴共同逻辑：<b>定位清晰、场景分层、冷启动验证、案例沉淀、咨询承接</b>。迷迭香农庄最应先放大的，是“窑炉披萨体验＋私密草坪庭院＋仪式/团建场景”的独有组合。', PALE, 'Bodyx', 10), PageBreak()]

# 08 Closing
story += section('07 / NEXT STEP','最终建议：先让“迷迭香农庄值得专程来”成为用户共识')
story.append(box('迷迭香农庄的增长重点不是重复输出“很有氛围”，而是把新派乡村园林、红砖草坪、窑炉披萨和预约制私域体验，变成用户能理解并行动的五类答案：<br/><br/><b>来这里吃什么？适合和谁来？能完成什么仪式/活动？离城区70公里为什么值得？怎么预约？</b>', CREAM, 'Quote', 12))
story += [Spacer(1,8*mm), P('合作后首轮需要确认的资料','H2x')]
story += bullets(['五个业务板块真实可承接的产品、人群、人数、预算／价格口径和预约规则。','近半年求婚、婚礼、团建、品牌活动及窑炉体验的真实素材与客户授权。','路线、停车、天气预案、场地分区、设备与服务边界。','小红书后台数据、私信问题、到店与成交记录。','门店拍摄、审核、接待、素材回流的责任人和响应机制。'])
story += [Spacer(1,8*mm), P('结论','H2x'), P('建议以“账号主页重建＋五大场景内容矩阵＋目的地距离转化＋真实案例资产沉淀”为合作主线。先让用户看懂迷迭香农庄，再根据搜索、收藏、咨询与成交信号，集中放大窑烤／团建、求婚／草坪婚礼或品牌发布会等高价值场景。','Bodyx'), Spacer(1,8*mm), P('谢谢｜期待与迷迭香农庄一起，把桃花岛内的乡村园林美学空间做成用户愿意专程前往的目的地。','Quote'), Spacer(1,14*mm), P('附：本稿为客户沟通版框架，不包含完整执行方案、脚本、选题库、SOP、投放计划及数据承诺。','Smallx')]

doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT.resolve())
