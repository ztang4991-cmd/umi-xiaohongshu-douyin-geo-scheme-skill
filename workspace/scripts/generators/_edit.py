from pathlib import Path
import re
p=Path(r'C:\Users\EDY\mslearn-ai-agents\create_douyin_service_plan_image.py')
s=p.read_text(encoding='utf-8-sig')
s=s.replace("('数量标准','短视频每周5-7条；直播每周1-2场；月度内容不少于20条',128),", "('数量标准','短视频每周最低4条；月度内容不少于16条',112),")
s=s.replace("('发布标准','每周5-7条；覆盖成都本地、婚宴/商拍、户外场地等精准标签',128),", "('发布标准','每周最低4条；覆盖成都本地、婚宴/商拍、户外场地等精准标签',112),")
pattern=r"section\(x2,bottom_y,w2,850,5,'直播运营','green',\[.*?\n\]\)\n"
replacement="""section(x2,bottom_y,w2,700,5,'账号维护','green',[
    ('在线时段','工作日09:00-23:00保持在线，及时处理账号消息与客户咨询',112),
    ('评论回复','品牌账号评论2小时内回复，维护互动体验与咨询承接',112),
    ('主动互动','主动私信关注/收藏/评论用户，维护账号活跃度与内容互动',112),
    ('验收方式','账号24h登录监控，运营日志客户可随时查阅',112),
])
"""
s,n=re.subn(pattern,replacement,s,flags=re.S)
if n!=1: raise SystemExit(f'section replace count={n}')
s=s.replace("('客户需配合提供：场地素材/产品介绍/价格信息/直播出镜人员', 1190)", "('客户需配合提供：场地素材/产品介绍/价格信息', 1190)")
p.write_text(s,encoding='utf-8')
print('updated', n)
