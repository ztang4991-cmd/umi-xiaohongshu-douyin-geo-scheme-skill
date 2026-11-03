from __future__ import annotations

import subprocess
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r"C:\Users\EDY\Desktop\米兰素材\春生最新素材")
ASSET_DIR = ROOT / "tmp" / "pdfs" / "chunsheng_toc_assets"
OUT_DIR = ROOT / "output" / "pdf"
W, H, M = 960, 540, 52
FONT, BOLD = "Deng", "DengBold"
INK = HexColor("#1E2926"); GREEN = HexColor("#4D6756"); RUST = HexColor("#B65D42")
GOLD = HexColor("#C79A42"); SKY = HexColor("#A9D2D4"); PAPER = HexColor("#F4F6F2")
MIST = HexColor("#E6ECE6"); LINE = HexColor("#CBD5CA"); MUTED = HexColor("#607069"); WHITE = HexColor("#FFFFFF")

FRAMES = {
    "aisle":"IMG_0767", "wedding":"IMG_0768", "install":"IMG_0769", "garden":"IMG_0770", "detail":"IMG_0771",
    "pergola":"IMG_0772", "arch":"IMG_0773", "archfront":"IMG_0774", "sign":"IMG_0776", "wall":"IMG_0778",
    "fountain":"IMG_0779", "hall":"IMG_0784", "hallwide":"IMG_0785", "room":"IMG_0792", "gardenwall":"IMG_0798",
    "archdetail":"IMG_0805", "snacks":"IMG_0812"
}

def prepare():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    result = {}
    for key, stem in FRAMES.items():
        target = ASSET_DIR / f"{stem}.jpg"
        if not target.exists():
            source = SOURCE / f"{stem}.HEIC.mov"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "00:00:00.5", "-i", str(source), "-frames:v", "1", str(target)], check=True)
        result[key] = target
    return result

def setup_fonts():
    pdfmetrics.registerFont(TTFont(FONT, r"C:\Windows\Fonts\Deng.ttf"))
    pdfmetrics.registerFont(TTFont(BOLD, r"C:\Windows\Fonts\Dengb.ttf"))

def txt(c, s, x, y, size, color=INK, font=FONT):
    c.setFillColor(color); c.setFont(font, size); c.drawString(x, y, s)

def rtxt(c, s, x, y, size, color=INK, font=FONT):
    c.setFillColor(color); c.setFont(font, size); c.drawRightString(x, y, s)

def wrap(c, s, x, y, width, size=11, leading=18, color=MUTED, font=FONT):
    c.setFillColor(color); c.setFont(font, size); line = ""
    for ch in s:
        maybe = line + ch
        if c.stringWidth(maybe, font, size) > width and line:
            c.drawString(x, y, line); y -= leading; line = ch
        else: line = maybe
    if line: c.drawString(x, y, line); y -= leading
    return y

def img(c, p, x, y, w, h):
    im = ImageReader(str(p)); iw, ih = im.getSize(); scale = max(w/iw, h/ih); dw, dh = iw*scale, ih*scale
    c.saveState(); path = c.beginPath(); path.rect(x,y,w,h); c.clipPath(path, stroke=0, fill=0)
    c.drawImage(im, x+(w-dw)/2, y+(h-dh)/2, dw, dh); c.restoreState()

def veil(c, x, y, w, h, color, alpha):
    c.saveState(); c.setFillColor(color); c.setFillAlpha(alpha); c.rect(x,y,w,h, fill=1, stroke=0); c.restoreState()

def base(c, n, section, audience):
    c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColor(LINE); c.line(M,H-38,W-M,H-38)
    txt(c, f"CHUNSHENG | {audience.upper()}", M,H-29,8.5,GREEN,BOLD); rtxt(c,section,W-M,H-29,8.5,MUTED,BOLD)
    txt(c,"春生线下销售工具 | TOC 场景框架",M,24,8.5,MUTED); rtxt(c,f"{n:02d}",W-M,24,8.5,MUTED,BOLD)

def note(c, message):
    c.setFillColor(MIST); c.roundRect(M,55,W-M*2,32,4,fill=1,stroke=0)
    txt(c,"销售提示",M+14,74,8.5,RUST,BOLD); txt(c,message,M+69,72,9.3,MUTED)

def card(c, x, y, w, h, title, body, accent):
    c.setFillColor(WHITE); c.roundRect(x,y,w,h,5,fill=1,stroke=0); c.setFillColor(accent); c.rect(x,y+h-5,w,5,fill=1,stroke=0)
    txt(c,title,x+16,y+h-29,12,INK,BOLD); wrap(c,body,x+16,y+h-51,w-32,9.2,15)

def cover(c, audience, desc, p, accent):
    img(c,p,0,0,W,H); veil(c,0,0,W,H,INK,.56)
    txt(c,"CHUNSHENG",M,H-58,11,WHITE,BOLD); c.setFillColor(accent); c.rect(M,H-78,80,4,fill=1,stroke=0)
    txt(c,"春生",M,250,46,WHITE,BOLD); txt(c,"线下销售工具",M+3,214,20,WHITE,BOLD); txt(c,audience,M+3,180,18,accent,BOLD)
    wrap(c,desc,M+3,146,360,11.2,18,WHITE); txt(c,"TOC 场景框架 | 基于现有场地素材",M,64,10,WHITE,BOLD)
    rtxt(c,"供销售人员当面讲解与后续完善使用",W-M,64,9.5,WHITE); c.showPage()

def contents(c, audience, accent, entries):
    base(c,2,"CONTENTS",audience); txt(c,"从客户关心的问题开始翻",M,434,26,INK,BOLD)
    wrap(c,"本版是线下销售讲解框架。照片用于让客户先看见场景，方括号内容由销售在正式对外前补齐。",M,402,540)
    for i,(h,s) in enumerate(entries):
        col,row=i%2,i//2; x,y=M+col*420,338-row*74
        c.setFillColor(WHITE); c.roundRect(x,y,392,54,4,fill=1,stroke=0); c.setFillColor(accent); c.circle(x+23,y+27,12,fill=1,stroke=0)
        txt(c,f"{i+1:02d}",x+16,y+23,7.8,WHITE,BOLD); txt(c,h,x+48,y+30,12,INK,BOLD); txt(c,s,x+48,y+14,8.8,MUTED)
    note(c,"不在本版填入未经确认的桌数、人数、套餐价格、交通时长或服务承诺。"); c.showPage()

def intro(c, audience, n, section, heading, desc, p, box_title, box_body, accent):
    base(c,n,section,audience); img(c,p,0,0,482,H); veil(c,0,0,482,H,INK,.12); txt(c,"场景照片",M,70,8.5,WHITE,BOLD)
    txt(c,heading,522,416,26,INK,BOLD); wrap(c,desc,522,382,365)
    card(c,522,192,360,136,box_title,box_body,accent); card(c,522,106,174,64,"需要补齐","[具体位置] [开放时间]",RUST); card(c,708,106,174,64,"销售动作","先问需求，再翻对应案例",accent); c.showPage()

def gallery(c, audience, n, section, heading, desc, photos, labels, accent):
    base(c,n,section,audience); txt(c,heading,M,434,26,INK,BOLD); wrap(c,desc,M,402,470)
    slots=[(M,178,258,180),(326,178,258,180),(600,178,308,180)]
    for p,lab,(x,y,w,h) in zip(photos,labels,slots):
        img(c,p,x,y,w,h); veil(c,x,y,w,34,INK,.62); txt(c,lab,x+14,y+12,9.8,WHITE,BOLD)
    for lab,(x,_,_,_) in zip(labels,slots):
        txt(c,lab,x,142,11,INK,BOLD); txt(c,"对应区域的看点",x,123,8.8,MUTED)
    note(c,"讲解时不要只说“好看”：结合客户当天的流程，说明这里在何时被使用、由谁体验。"); c.showPage()

def brief(c, audience, n, section, heading, left_title, left_items, right_title, right_items, p, accent):
    base(c,n,section,audience); txt(c,heading,M,434,26,INK,BOLD); img(c,p,594,104,314,320); veil(c,594,104,314,44,INK,.66); txt(c,"以现场确认信息为准",610,121,9.5,WHITE,BOLD)
    for x,title,items,color in [(M,left_title,left_items,accent),(306,right_title,right_items,RUST)]:
        c.setFillColor(WHITE); c.roundRect(x,136,224,236,5,fill=1,stroke=0); c.setFillColor(color); c.rect(x,365,224,7,fill=1,stroke=0); txt(c,title,x+18,334,14,INK,BOLD)
        y=293
        for item in items:
            c.setFillColor(color); c.circle(x+22,y+3,3,fill=1,stroke=0); wrap(c,item,x+34,y,170,9.5,17); y-=46
    note(c,"本页用于帮助客户把“我想办什么”转换成销售可确认的筹备清单。"); c.showPage()

def route(c, audience, n, heading, p, accent):
    base(c,n,"VISIT & ROUTE",audience); txt(c,heading,M,434,26,INK,BOLD)
    wrap(c,"路线、停车、预约与到场提示是临门一脚的信息。本页预留为场地确认后的最终版，不以当前素材推断具体地址或出行时长。",M,402,480)
    img(c,p,612,120,296,282); veil(c,612,120,296,282,INK,.2); txt(c,"路线图 / 停车说明预留区",633,146,13,WHITE,BOLD)
    y=335
    for field in ["[场地详细地址]","[导航关键词 / 定位点]","[停车安排与收费口径]","[预约联系人与联系电话]","[到店前需确认的事项]"]:
        c.setFillColor(WHITE); c.roundRect(M,y-15,500,34,4,fill=1,stroke=0); txt(c,field,M+16,y-3,10,MUTED); y-=47
    c.setFillColor(accent); c.roundRect(M,84,500,32,4,fill=1,stroke=0); txt(c,"建议：发给客户前，将本页替换为真实导航截图或简明手绘路线图。",M+16,96,9.4,WHITE,BOLD); c.showPage()

def close(c, p, accent):
    img(c,p,0,0,W,H); veil(c,0,0,W,H,INK,.65); txt(c,"NEXT STEP",M,H-86,8.5,accent,BOLD)
    txt(c,"把今天的需求，",M,306,30,WHITE,BOLD); txt(c,"落到一份可确认的方案里。",M,264,30,WHITE,BOLD)
    wrap(c,"本框架适合首次到店、二次带家人考察及活动需求沟通。成交资料完成前，请补齐场地事实、可售产品与对外口径。",M,208,410,11,18,WHITE)
    c.setFillColor(accent); c.roundRect(M,94,286,42,4,fill=1,stroke=0); txt(c,"[预约方式 / 销售姓名 / 联系方式]",M+16,109,10,WHITE,BOLD); rtxt(c,"春生 | 线下销售工具 TOC 场景框架",W-M,64,9.5,WHITE); c.showPage()

def make_wedding(a):
    p=OUT_DIR/"春生线下销售TOC框架_备婚版.pdf"; c=canvas.Canvas(str(p),pagesize=(W,H),pageCompression=1)
    cover(c,"备婚用户版","把场地、仪式、宾客体验与预算沟通串成一条能被看见的婚礼筹备路径。",a["wedding"],GOLD)
    contents(c,"备婚用户版",GOLD,[("初见春生","先看场地气质与到店第一感受"),("婚礼动线","仪式、迎宾、合影与用餐如何连起来"),("出片与打卡","给新人和宾客的拍照记忆点"),("真实布置案例","用不同风格帮助客户表达偏好"),("婚宴与服务","把餐饮、流程、配置说清楚"),("档期、路线与预约","进入可执行的看场下一步")])
    intro(c,"备婚用户版",3,"FIRST IMPRESSION","第一次到场，要先让新人看到画面感","用现场空间和装置建立第一印象，再根据婚期、人数、风格偏好选择后续讲解路径。",a["wedding"],"建议讲解顺序","入口/第一眼空间 -> 仪式或迎宾区域 -> 宾客停留区 -> 餐饮与服务确认。",GOLD)
    gallery(c,"备婚用户版",4,"SPACE & FLOW","婚礼不是只看一个主背景","让新人理解，从抵达、迎宾、仪式、合影到开席，每一段都需要有顺畅的体验和可被拍下来的画面。",[a["pergola"],a["arch"],a["hall"]],["到场与迎宾","仪式 / 合影区域","宴会承接区域"],GOLD)
    gallery(c,"备婚用户版",5,"PHOTO MOMENTS","为照片留下可辨识的春生记忆点","此页只展示现有素材中可见的花园、喷泉、拱门与布置细节。销售可据此追问客户是否偏好自然感、花艺感或仪式感。",[a["fountain"],a["archdetail"],a["wall"]],["花园喷泉","白色拱门","定制化装置"],GOLD)
    gallery(c,"备婚用户版",6,"REAL SETUPS","用真实布置案例缩短“我想要什么”的沟通","案例用于帮助客户选择风格与重点区域，不对布置范围、供应商、费用或效果作未经确认的承诺。",[a["aisle"],a["install"],a["detail"]],["户外仪式通道","主视觉装置","宾客视角细节"],GOLD)
    brief(c,"备婚用户版",7,"WEDDING BRIEF","把审美偏好变成可确认的婚礼简报","新人需要先决定",["[婚期 / 午宴或晚宴]","[预计宾客人数与桌数]","[偏好的婚礼风格]","[最在意的一个体验点]"],"场地需要确认",["[可用时段与档期]","[仪式/宴会区域安排]","[餐标、酒水与服务口径]","[布置、音响、执行边界]"],a["garden"],GOLD)
    intro(c,"备婚用户版",8,"DINING","婚宴页面要回答：吃什么、怎么选、谁来服务","目前素材可见基础零售/餐饮陈列，正式客户版需替换为确认后的婚宴菜单、菜品实拍、套餐包含项与服务说明。",a["snacks"],"此页正式版建议放入","[套餐名称] [菜品图] [价格/桌] [酒水规则] [儿童/素食/忌口处理]。",RUST)
    route(c,"备婚用户版",9,"从心动到到店确认，把信息说完整",a["sign"],GOLD); close(c,a["install"],GOLD); c.save(); return p

def make_meeting(a):
    p=OUT_DIR/"春生线下销售TOC框架_团建会议版.pdf"; c=canvas.Canvas(str(p),pagesize=(W,H),pageCompression=1)
    cover(c,"团建 / 会议用户版","从到场、会议、活动、餐饮到返程，把组织者要协调的关键节点放在同一份销售工具里。",a["hallwide"],SKY)
    contents(c,"团建 / 会议用户版",SKY,[("场地总览","先看活动当天的整体体验与氛围"),("会议与用餐空间","会议、就餐、交流如何衔接"),("户外团建场景","让活动负责人看到可用的场景变化"),("活动组织清单","把客户需求拆成可执行的确认项"),("餐饮与茶歇","明确菜单、节奏和特殊需求"),("路线与预约","让参会者顺利抵达并减少临场问题")])
    intro(c,"团建 / 会议用户版",3,"VENUE OVERVIEW","一场顺利的活动，从抵达体验开始","先让组织者看到环境和空间氛围，再确认会议规模、活动形式、餐饮安排与当天时间表。",a["hallwide"],"建议讲解顺序","活动人数/时段 -> 会议桌型 -> 户外活动需求 -> 餐饮节奏 -> 交通和停车。",SKY)
    gallery(c,"团建 / 会议用户版",4,"MEETING & DINING","会议、交流、就餐应当顺着流程发生","展示室内桌椅、采光和就餐承接区。具体桌型、人数、设备、时段及使用限制必须在报价前确认。",[a["hall"],a["hallwide"],a["room"]],["室内活动区","就餐 / 交流承接","环境细节"],SKY)
    gallery(c,"团建 / 会议用户版",5,"OUTDOOR EXPERIENCE","户外空间让团建不止停留在会议室","用花园、拱门、绿植与装置区域帮助客户判断活动氛围；是否可用于具体游戏、搭建或设备摆放，应以现场勘察结果为准。",[a["garden"],a["fountain"],a["gardenwall"]],["花园活动视角","休憩与拍照点","空间氛围背景"],SKY)
    brief(c,"团建 / 会议用户版",6,"EVENT BRIEF","先把活动组织条件问清楚，再进入报价","客户需要确认",["[活动日期 / 时段]","[预计人数与人员构成]","[会议、团建、晚宴的优先级]","[是否需要主持、搭建、设备]"],"场地需要确认",["[可用区域与时间]","[桌型 / 座位 / 设备支持]","[餐饮、茶歇、酒水口径]","[天气预案与现场执行边界]"],a["pergola"],SKY)
    intro(c,"团建 / 会议用户版",7,"FOOD & BREAKS","餐饮与茶歇，是整场活动节奏的一部分","目前素材可见基础餐饮陈列；正式版请替换为经场地确认的团餐、桌餐、茶歇或定制菜单图，并注明适用人数、上餐节奏与特殊餐食处理。",a["snacks"],"此页正式版建议放入","[菜单/餐标] [茶歇组合] [上餐时间] [忌口处理] [酒水规则]。",RUST)
    gallery(c,"团建 / 会议用户版",8,"TEAM EXPERIENCE","客户也会在意：参会者能留下什么记忆","这是活动负责人向内部沟通的可视化素材页。用环境细节、拍照点和活动背景减少“场地只有功能、没有体验”的顾虑。",[a["archfront"],a["wall"],a["fountain"]],["团队合影背景","活动打卡装置","自然休憩角落"],SKY)
    route(c,"团建 / 会议用户版",9,"把抵达、停车与集合说在活动开始之前",a["sign"],SKY); close(c,a["hall"],SKY); c.save(); return p

def main():
    setup_fonts(); OUT_DIR.mkdir(parents=True,exist_ok=True); assets=prepare()
    for p in [make_wedding(assets),make_meeting(assets)]: print(p)
if __name__ == "__main__": main()
