from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

W, H = 3840, 2160
img = Image.new('RGB', (W,H), '#ffffff')
d = ImageDraw.Draw(img)

# Palette closely follows the supplied Xiaohongshu template.
maroon = '#a71938'
red = '#bd2f4d'
red2 = '#d14563'
red_soft = '#f8eeee'
red_border = '#ead7db'
green = '#2e6f59'
green2 = '#3e8068'
green_soft = '#f0f5f1'
green_border = '#d7e2dc'
purple = '#6d3b64'
purple2 = '#805274'
purple_soft = '#f2f1f4'
purple_border = '#ddd6df'
gold = '#c99a3b'
text = '#353535'
muted = '#6d6d6d'
box = '#eeeae6'
box_green = '#e6eeea'
box_purple = '#e9e7eb'

font_dir = Path('C:/Windows/Fonts')
def F(size, bold=False):
    path = font_dir / ('Dengb.ttf' if bold else 'Deng.ttf')
    return ImageFont.truetype(str(path), size)

f_title = F(84, True)
f_badge = F(42, True)
f_section = F(46, True)
f_num = F(34, True)
f_label = F(38, True)
f_body = F(30, False)
f_body_b = F(34, True)
f_footer = F(34, True)
f_footer2 = F(30, False)

# helpers
def rr(xy, radius, fill, outline=None, width=1):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def fit_text(text, font, max_width):
    # Return lines split by explicit slash separators and width.
    parts = text.split('\n')
    lines=[]
    for part in parts:
        if not part:
            lines.append(''); continue
        cur=''
        for ch in part:
            test=cur+ch
            if d.textbbox((0,0), test, font=font)[2] <= max_width:
                cur=test
            else:
                if cur: lines.append(cur)
                cur=ch
        if cur: lines.append(cur)
    return lines

def draw_centered_text(xy, s, font, fill, max_width=None, line_gap=8):
    x1,y1,x2,y2=xy
    if max_width is None: max_width=x2-x1
    lines=fit_text(s,font,max_width)
    bbox=d.textbbox((0,0),'Ag',font=font)
    lh=bbox[3]-bbox[1]
    total=len(lines)*lh+(len(lines)-1)*line_gap
    y=y1+(y2-y1-total)/2-bbox[1]
    for line in lines:
        bb=d.textbbox((0,0), line, font=font)
        d.text((x1+(x2-x1-(bb[2]-bb[0]))/2,y), line, font=font, fill=fill)
        y += lh+line_gap

def draw_left_text(x, y, s, font, fill, max_width, line_gap=8, max_lines=None):
    lines=fit_text(s,font,max_width)
    if max_lines and len(lines)>max_lines:
        lines=lines[:max_lines]
        if lines[-1]: lines[-1]=lines[-1][:-1]+'…'
    bb=d.textbbox((0,0),'Ag',font=font)
    lh=bb[3]-bb[1]
    for line in lines:
        d.text((x,y),line,font=font,fill=fill)
        y += lh+line_gap
    return y

def section(x,y,w,h,num,title,theme='red',rows=[]):
    if theme=='red':
        head, soft, border, label_fill, body_fill = red, red_soft, red_border, red2, box
    elif theme=='green':
        head, soft, border, label_fill, body_fill = green, green_soft, green_border, green, box_green
    else:
        head, soft, border, label_fill, body_fill = purple, purple_soft, purple_border, purple2, box_purple
    rr((x,y,x+w,y+h), 24, soft, border, 3)
    rr((x+40,y+36,x+w-40,y+158), 14, head)
    rr((x+74,y+68,x+188,y+126), 10, '#d98ba0')
    draw_centered_text((x+74,y+68,x+188,y+126), f'{num:02d}', f_num, '#ffffff', 114, 0)
    d.text((x+218,y+61), title, font=f_section, fill='#ffffff')
    inner_y=y+188
    label_w=250
    row_gap=20
    body_x=x+315
    for label, value, rh in rows:
        rr((x+40,inner_y,x+40+label_w,inner_y+rh), 12, label_fill)
        draw_centered_text((x+40,inner_y,x+40+label_w,inner_y+rh), label, f_label, '#ffffff', label_w-25, 4)
        rr((body_x,inner_y,x+w-40,inner_y+rh), 12, body_fill)
        draw_left_text(body_x+30, inner_y+18, value, f_body, text, w-(body_x-x)-100, 5)
        inner_y += rh+row_gap

# Header
d.rectangle((0,0,W,300), fill=maroon)
d.text((96,94), '聚尤米 UMI · 抖音运营服务方案', font=f_title, fill='#ffffff')
rr((3135,52,3738,250), 0, gold)
d.text((3288,84), '全包服务', font=F(52,True), fill='#ffffff')
d.text((3238,171), '按季度签约 · 全程托管', font=F(28,False), fill='#ffffff')

# Card layout
x1,x2,x3=96,1330,2564
w1,w2,w3=1180,1180,1180
top_y=350
section(x1,top_y,w1,700,1,'账号搭建','red',[
    ('准备工作','客户提供可接收验证码、已退出抖音的手机',128),
    ('账号创建','确认主体名称，运营专员完成抖音账号创建',104),
    ('基础搭建','头像 · 昵称 · 简介 · 背景图 · 企业号基础设置',104),
    ('验收方式','提供官方账号和密码，客户可登录查看（尽量减少账号切换登录频次）',128),
])
section(x2,top_y,w2,700,2,'企业认证','red',[
    ('所需资料','运营者姓名/手机号/企业资质表/注册文件（加盖公章）',128),
    ('Logo注意','使用公司Logo须提前确认商标注册情况',104),
    ('企业号','建议开通企业号及团购/门店功能（费用客户自理，我方全程协助）',128),
    ('验收方式','主页头像下方出现企业认证标识，团购/门店功能可正常使用',104),
])
section(x3,top_y,w3,700,3,'内容策划','red',[
    ('数量标准','短视频每周最低4条；月度内容不少于16条',112),
    ('内容方向','场景展示 → 婚礼案例 → 价格对比 → 干货避坑 → 客户见证',128),
    ('策划流程','账号分析→选题提炼→脚本撰写→拍摄剪辑→发布优化→数据复盘',128),
    ('验收方式','提交客户审核，可小范围修改1次（方向不可改）',104),
])

bottom_y=1110
section(x1,bottom_y,w1,700,4,'短视频发布','green',[
    ('素材准备','客户提供场地、产品、服务、客户案例等基础素材；我方负责补拍/剪辑',128),
    ('发布标准','每周最低4条；覆盖成都本地、婚宴/商拍、户外场地等精准标签',112),
    ('团购植入','视频挂载商拍场地券、试餐/到店咨询、婚宴套餐等转化入口',128),
    ('验收方式','发布后实时分享视频链接，客户可自行查看数据与评论',104),
])
section(x2,bottom_y,w2,700,5,'账号维护','green',[
    ('在线时段','工作日09:00-23:00保持在线，及时处理账号消息与客户咨询',112),
    ('评论回复','品牌账号评论2小时内回复，维护互动体验与咨询承接',112),
    ('主动互动','主动私信关注/收藏/评论用户，维护账号活跃度与内容互动',112),
    ('验收方式','账号24h登录监控，运营日志客户可随时查阅',112),
])
section(x3,bottom_y,w3,700,6,'运营总结','purple',[
    ('月度报表','输出曝光量 · 播放量 · 完播率 · 互动 · 粉丝 · 线索数据分析1次/月',128),
    ('活动策划','线上热点/主题活动/本地生活团购策划1次/月',104),
    ('季度汇报','电话/视频会议：汇报+规划+优化3次/季度',104),
    ('验收方式','以文档/Excel形式交付，每月2号（遇假日顺延）',104),
])

# Footer
d.rectangle((0,2025,W,H), fill='#86152b')
# bullets and text
items=[('合作方式：按季度签约', 560),('客户需配合提供：场地素材/产品介绍/价格信息', 1190),('抖音广告费、认证费、团购/门店相关费用由客户自行缴纳', 2520)]
for s,x in items:
    d.ellipse((x-38,2073,x+2,2113), fill=gold)
    d.text((x+28,2062),s,font=f_footer,fill='#ffffff')

out=Path('C:/Users/EDY/mslearn-ai-agents/output/聚尤米UMI_抖音运营服务方案.png')
img.save(out, quality=95)
print(out)


