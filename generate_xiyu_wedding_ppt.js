const pptxgen = require("pptxgenjs");
const fs = require("fs");

const base = "C:/Users/EDY/mslearn-ai-agents";
const out = `${base}/新都喜遇言庭宴会中心_婚宴类目小红书美团运营方案.pptx`;

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "聚光米 UMI";
pptx.subject = "婚宴类目小红书美团运营方案";
pptx.title = "新都喜遇言庭宴会中心_婚宴类目运营方案";
pptx.company = "聚光米 UMI";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};
pptx.defineLayout({ name: "CUSTOM_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "CUSTOM_WIDE";

const C = {
  ink: "1F2328",
  sub: "5C5E66",
  gold: "B78A45",
  deepGold: "8A642E",
  ivory: "FBF7EF",
  paper: "FFFDFC",
  line: "DDD2BF",
  rose: "B85C65",
  green: "556B5A",
  blue: "526D82",
  white: "FFFFFF",
};

function addBg(slide) {
  slide.background = { color: C.paper };
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.paper }, line: { color: C.paper } });
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 0.13, fill: { color: C.gold }, line: { color: C.gold } });
  slide.addShape(pptx.ShapeType.line, { x: 0.72, y: 6.95, w: 11.9, h: 0, line: { color: C.line, width: 0.8 } });
  slide.addText("聚光米 UMI · 婚嫁垂类线上运营", { x: 0.72, y: 7.05, w: 5.8, h: 0.22, fontFace: "Microsoft YaHei", fontSize: 7.5, color: "8A8F98" });
}

function title(slide, t, st) {
  slide.addText(t, { x: 0.72, y: 0.52, w: 8.8, h: 0.45, fontFace: "Microsoft YaHei", fontSize: 22, bold: true, color: C.ink, margin: 0 });
  if (st) slide.addText(st, { x: 0.75, y: 1.02, w: 9.7, h: 0.28, fontFace: "Microsoft YaHei", fontSize: 9.5, color: C.sub, margin: 0 });
}

function pageNo(slide, n) {
  slide.addText(String(n).padStart(2, "0"), { x: 12.35, y: 7.03, w: 0.35, h: 0.2, fontSize: 7.5, color: "8A8F98", align: "right", margin: 0 });
}

function chip(slide, text, x, y, w, color = C.gold) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.32, rectRadius: 0.04, fill: { color }, line: { color } });
  slide.addText(text, { x: x + 0.12, y: y + 0.075, w: w - 0.24, h: 0.14, fontSize: 7.5, bold: true, color: C.white, align: "center", margin: 0 });
}

function card(slide, x, y, w, h, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.05,
    fill: { color: opts.fill || C.white },
    line: { color: opts.line || C.line, width: opts.width || 0.8 },
  });
}

function bullet(slide, lines, x, y, w, opts = {}) {
  let cy = y;
  lines.forEach((line) => {
    slide.addShape(pptx.ShapeType.ellipse, { x, y: cy + 0.07, w: 0.07, h: 0.07, fill: { color: opts.color || C.gold }, line: { color: opts.color || C.gold } });
    slide.addText(line, { x: x + 0.16, y: cy, w, h: 0.32, fontSize: opts.size || 10.2, color: opts.textColor || C.ink, breakLine: false, fit: "shrink", margin: 0 });
    cy += opts.gap || 0.42;
  });
}

function metric(slide, num, label, x, y, w, color = C.gold) {
  card(slide, x, y, w, 1.05, { fill: "FFFCF7" });
  slide.addText(num, { x: x + 0.15, y: y + 0.16, w: w - 0.3, h: 0.28, fontSize: 21, bold: true, color, align: "center", margin: 0 });
  slide.addText(label, { x: x + 0.15, y: y + 0.63, w: w - 0.3, h: 0.18, fontSize: 8.2, color: C.sub, align: "center", margin: 0 });
}

function table(slide, rows, x, y, w, h, widths) {
  const rowH = h / rows.length;
  rows.forEach((row, r) => {
    let cx = x;
    row.forEach((cell, c) => {
      const cw = w * (widths ? widths[c] : 1 / row.length);
      const head = r === 0;
      slide.addShape(pptx.ShapeType.rect, {
        x: cx, y: y + r * rowH, w: cw, h: rowH,
        fill: { color: head ? C.ink : (r % 2 ? "FFFCF8" : C.white) },
        line: { color: C.line, width: 0.55 },
      });
      slide.addText(cell, {
        x: cx + 0.08, y: y + r * rowH + 0.07, w: cw - 0.16, h: rowH - 0.12,
        fontSize: head ? 8.6 : 7.7,
        bold: head,
        color: head ? C.white : C.ink,
        valign: "mid",
        fit: "shrink",
        margin: 0,
      });
      cx += cw;
    });
  });
}

// 1 Cover
{
  const s = pptx.addSlide();
  s.background = { color: C.ivory };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.ivory }, line: { color: C.ivory } });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 4.65, h: 7.5, fill: { color: C.ink }, line: { color: C.ink } });
  s.addShape(pptx.ShapeType.line, { x: 5.25, y: 1.22, w: 6.9, h: 0, line: { color: C.gold, width: 1.4 } });
  s.addText("聚光米 UMI", { x: 0.72, y: 0.75, w: 2.4, h: 0.26, fontSize: 13, bold: true, color: C.gold, margin: 0 });
  s.addText("新都喜遇言庭宴会中心", { x: 5.25, y: 1.45, w: 6.8, h: 0.5, fontSize: 25, bold: true, color: C.ink, margin: 0 });
  s.addText("小红书 + 美团\n婚宴类目落地运营方案", { x: 5.25, y: 2.13, w: 6.9, h: 1.12, fontSize: 29, bold: true, color: C.deepGold, breakLine: false, fit: "shrink", margin: 0 });
  s.addText("明日到店沟通版 / 2026.07.03", { x: 5.28, y: 3.52, w: 4.1, h: 0.25, fontSize: 10.5, color: C.sub, margin: 0 });
  s.addText("让婚礼堂在线上被看见、被比较、被信任", { x: 5.28, y: 4.35, w: 5.7, h: 0.35, fontSize: 15, bold: true, color: C.ink, margin: 0 });
  s.addText("市场判断 / 账号诊断 / 内容打法 / 美团承接 / 90天动作", { x: 5.28, y: 4.82, w: 6.9, h: 0.25, fontSize: 10.5, color: C.sub, margin: 0 });
  s.addShape(pptx.ShapeType.rect, { x: 0.72, y: 5.78, w: 2.25, h: 0.02, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("婚嫁垂类线上运营", { x: 0.72, y: 6.0, w: 2.4, h: 0.25, fontSize: 11, color: C.white, margin: 0 });
  s.addText("小红书种草 · 美团承接 · 客资闭环", { x: 0.72, y: 6.35, w: 2.9, h: 0.25, fontSize: 8.6, color: "D7D0C4", margin: 0 });
}

// 2 Who we are
{
  const s = pptx.addSlide(); addBg(s); title(s, "我们是谁", "来自婚嫁垂类平台经验，做的是线上获客闭环，不只是发内容。"); pageNo(s, 2);
  card(s, 0.75, 1.72, 5.55, 4.35, { fill: C.white });
  s.addText("聚光米 UMI", { x: 1.05, y: 2.0, w: 2.2, h: 0.28, fontSize: 17, bold: true, color: C.ink, margin: 0 });
  bullet(s, [
    "核心团队来自婚礼纪平台，熟悉婚宴用户决策路径",
    "长期服务成都婚宴、婚礼堂、宴会酒店类商家",
    "能把内容种草、平台搜索、线索承接和到店转化串起来",
    "合作案例：麓山宴、祥合花园、春生花园、悦哉等"
  ], 1.08, 2.62, 4.75, { gap: 0.55, size: 10.4 });
  card(s, 6.75, 1.72, 5.75, 4.35, { fill: "FFFCF8", line: C.gold });
  chip(s, "核心承诺", 7.08, 2.0, 1.05, C.rose);
  s.addText("独家运营，客资不外泄", { x: 7.08, y: 2.52, w: 4.3, h: 0.35, fontSize: 18, bold: true, color: C.ink, margin: 0 });
  s.addText("通过我方小红书、美团运营产生的咨询、私信、电话、预约到店等线索，只服务于新都喜遇言庭宴会中心，不外发、不转售、不导流第三方。", {
    x: 7.08, y: 3.18, w: 4.65, h: 1.1, fontSize: 12, color: C.sub, fit: "shrink", breakLine: false, margin: 0,
  });
  s.addShape(pptx.ShapeType.line, { x: 7.08, y: 4.72, w: 4.7, h: 0, line: { color: C.line, width: 0.8 } });
  s.addText("交付目标：让酒店老板看到动作、看到专业、看到客资归属。", { x: 7.08, y: 5.02, w: 4.65, h: 0.33, fontSize: 10.5, color: C.ink, bold: true, margin: 0 });
}

// 3 Market
{
  const s = pptx.addSlide(); addBg(s); title(s, "新都婚宴市场判断", "今年的“卷”来自供给集中、价格下探、场地同质化和线上决策前置。"); pageNo(s, 3);
  metric(s, "新场地", "宴会中心集中入场", 0.8, 1.6, 2.25, C.gold);
  metric(s, "低门槛", "餐标/活动价更敏感", 3.4, 1.6, 2.25, C.rose);
  metric(s, "同质化", "无柱/草坪/主题厅都在讲", 6.0, 1.6, 2.25, C.green);
  metric(s, "线上化", "小红书种草，美团查证", 8.6, 1.6, 2.25, C.blue);
  card(s, 0.8, 3.18, 11.55, 2.55, { fill: "FFFCF8" });
  s.addText("破局关键词", { x: 1.12, y: 3.48, w: 1.6, h: 0.25, fontSize: 13, bold: true, color: C.deepGold, margin: 0 });
  s.addText("不只打价格战，而是打“可被看见、可被比较、可被信任”。", { x: 1.12, y: 3.92, w: 6.8, h: 0.33, fontSize: 16, bold: true, color: C.ink, margin: 0 });
  bullet(s, [
    "可被看见：抢占新都婚宴、新都婚礼堂、锦水河婚宴等搜索词",
    "可被比较：把七个厅、桌数、预算、套餐包含项讲清楚",
    "可被信任：小红书做种草，美团做地址、评价、电话和套餐承接"
  ], 1.15, 4.58, 9.9, { gap: 0.36, size: 9.8, color: C.deepGold });
}

// 4 Competitors
{
  const s = pptx.addSlide(); addBg(s); title(s, "竞品信号与应对", "只引用公开平台可核验信息；公开资料不足的，不写死硬数据。"); pageNo(s, 4);
  table(s, [
    ["场地", "公开信息", "对喜遇言庭的压力", "应对方向"],
    ["缤纷盛宴", "斑竹园竹韵大道369号；宴会帮显示1699-2999元/桌；大型厅、草坪、大厅无柱", "抢“城北大场地”和大桌数用户", "突出锦水河地铁口、七厅可选、20-34桌灵活匹配"],
    ["艾悦映江南", "映江南店；多主题厅+草坪；公开平台价格口径存在差异", "主题命名强，容易吸引拍照出片用户", "每个厅做成风格+桌数+预算+适合人群对比"],
    ["恒杏/至臻", "公开稳定商家页不足，暂不引用硬数据", "可能制造新场地讨论声量", "纳入每周监测，防守花园/户外/艺术感关键词"],
  ], 0.78, 1.55, 11.78, 4.65, [0.14, 0.34, 0.25, 0.27]);
  s.addText("喜遇言庭基础不弱：炬光路51号、近锦水河、七个主题厅、8米层高无柱、户外草坪等，需要重新包装成用户能搜索、能理解、能咨询的内容。", {
    x: 0.85, y: 6.42, w: 11.2, h: 0.28, fontSize: 9.5, bold: true, color: C.deepGold, fit: "shrink", margin: 0,
  });
}

// 5 Account diagnosis official
{
  const s = pptx.addSlide(); addBg(s); title(s, "小红书账号诊断 01", "喜遇言庭-宴会中心：已有内容基础，但需要从“好看广告”转成“新都搜索入口”。"); pageNo(s, 5);
  metric(s, "186", "粉丝", 0.9, 1.6, 1.55, C.gold);
  metric(s, "497", "获赞与收藏", 2.65, 1.6, 1.85, C.gold);
  metric(s, "七大", "主题宴会厅", 4.7, 1.6, 1.85, C.gold);
  card(s, 7.05, 1.42, 4.95, 1.75, { fill: "FFFCF8" });
  s.addText("当前定位", { x: 7.34, y: 1.72, w: 1.2, h: 0.2, fontSize: 10.5, bold: true, color: C.deepGold, margin: 0 });
  s.addText("成都新都区 / 一站式婚礼服务 / 沉浸式婚礼堂 / 七大主题厅 / 户外草坪", { x: 7.34, y: 2.1, w: 4.25, h: 0.46, fontSize: 9.8, color: C.sub, fit: "shrink", margin: 0 });
  card(s, 0.9, 3.45, 5.3, 2.2, { fill: C.white });
  s.addText("主要问题", { x: 1.18, y: 3.75, w: 1.2, h: 0.2, fontSize: 12.5, bold: true, color: C.rose, margin: 0 });
  bullet(s, [
    "大量笔记互动停留在1-6赞，点击钩子不稳定",
    "“被问爆/太绝/美到犯规/1k+”重复较多，广告感偏强",
    "1399、1699、1k+、2299等价格口径需统一"
  ], 1.18, 4.2, 4.45, { gap: 0.36, size: 9.2, color: C.rose });
  card(s, 6.65, 3.45, 5.35, 2.2, { fill: "FFFCF8", line: C.gold });
  s.addText("调整方向", { x: 6.95, y: 3.75, w: 1.2, h: 0.2, fontSize: 12.5, bold: true, color: C.deepGold, margin: 0 });
  bullet(s, [
    "做官方搜索号：七厅对比、桌数匹配、预算说明",
    "强化“新都/锦水河/北门婚宴”关键词覆盖",
    "每篇内容增加私信动作：发桌数和预算，帮你匹配厅型"
  ], 6.95, 4.2, 4.45, { gap: 0.36, size: 9.2, color: C.deepGold });
}

// 6 Account diagnosis personal
{
  const s = pptx.addSlide(); addBg(s); title(s, "小红书账号诊断 02", "喜遇言庭-杨佳：从混合内容号，调整为顾问信任与私信转化号。"); pageNo(s, 6);
  metric(s, "46", "粉丝", 0.9, 1.58, 1.55, C.rose);
  metric(s, "289", "获赞与收藏", 2.65, 1.58, 1.85, C.rose);
  metric(s, "顾问号", "承接私信与到店", 4.7, 1.58, 1.85, C.rose);
  card(s, 0.9, 3.18, 5.35, 2.48, { fill: C.white });
  s.addText("当前问题", { x: 1.18, y: 3.5, w: 1.2, h: 0.2, fontSize: 12.5, bold: true, color: C.rose, margin: 0 });
  bullet(s, [
    "“温江”内容较多，与新都门店获客目标混淆",
    "美食、聚会、宝宝宴、攻略混合，身份不够清晰",
    "个人号还没有承担答疑、邀约、跟进的转化职责"
  ], 1.18, 3.95, 4.45, { gap: 0.42, size: 9.4, color: C.rose });
  card(s, 6.72, 3.18, 5.35, 2.48, { fill: "FFFCF8", line: C.gold });
  s.addText("建议定位", { x: 7.0, y: 3.5, w: 1.2, h: 0.2, fontSize: 12.5, bold: true, color: C.deepGold, margin: 0 });
  bullet(s, [
    "顾问信任号：用人设承接新人的不确定感",
    "内容聚焦预算问答、看店路线、档期提醒、桌数匹配",
    "评论和私信统一收集：日期、桌数、预算、风格偏好"
  ], 7.0, 3.95, 4.45, { gap: 0.42, size: 9.4, color: C.deepGold });
}

// 7 Matrix
{
  const s = pptx.addSlide(); addBg(s); title(s, "账号矩阵打法", "两个账号不要互相复制，而是分别承担“搜索”和“转化”。"); pageNo(s, 7);
  card(s, 0.85, 1.65, 5.55, 4.52, { fill: C.white });
  chip(s, "官方号", 1.18, 1.98, 0.95, C.gold);
  s.addText("喜遇言庭-宴会中心", { x: 1.18, y: 2.5, w: 3.0, h: 0.28, fontSize: 17, bold: true, color: C.ink, margin: 0 });
  s.addText("负责品牌形象与本地搜索", { x: 1.18, y: 2.92, w: 3.0, h: 0.22, fontSize: 10.5, color: C.sub, margin: 0 });
  bullet(s, [
    "七厅总览、厅型对比、真实案例",
    "新都婚宴、锦水河、成都北门关键词",
    "活动信息、宝宝宴、年会会议内容沉淀"
  ], 1.2, 3.55, 4.35, { gap: 0.43, size: 10 });
  card(s, 6.9, 1.65, 5.55, 4.52, { fill: "FFFCF8", line: C.gold });
  chip(s, "顾问号", 7.22, 1.98, 0.95, C.rose);
  s.addText("喜遇言庭-杨佳", { x: 7.22, y: 2.5, w: 3.0, h: 0.28, fontSize: 17, bold: true, color: C.ink, margin: 0 });
  s.addText("负责信任建立与私信承接", { x: 7.22, y: 2.92, w: 3.0, h: 0.22, fontSize: 10.5, color: C.sub, margin: 0 });
  bullet(s, [
    "预算问答、桌数匹配、档期提醒",
    "看店路线、顾问视角、客户常问问题",
    "私信收集日期/桌数/预算，推动到店预约"
  ], 7.24, 3.55, 4.35, { gap: 0.43, size: 10, color: C.rose });
}

// 8 XHS content
{
  const s = pptx.addSlide(); addBg(s); title(s, "小红书内容怎么发", "从“形容词好看”改成“具体有用”，让用户看完愿意问。"); pageNo(s, 8);
  table(s, [
    ["栏目", "解决问题", "示例标题"],
    ["七厅怎么选", "不知道哪个厅适合桌数", "新都20桌婚礼怎么选厅？先看这张对比表"],
    ["预算怎么配", "怕超预算、怕隐形消费", "预算2万以内，餐标和布置怎么平衡？"],
    ["到店看什么", "看场地不知道问什么", "看婚礼堂别只拍照，这6件事要问清"],
    ["真实案例", "需要画面和信任", "26桌韩式婚礼实拍 / 宝宝宴海洋主题怎么布置"],
    ["本地搜索", "抢新都关键词", "锦水河地铁口婚礼堂，外地亲友来方便吗？"],
  ], 0.8, 1.48, 11.78, 4.75, [0.17, 0.25, 0.58]);
  s.addText("执行原则：每篇笔记都要有明确私信钩子，例如“发桌数和预算，帮你匹配厅型”。", {
    x: 0.85, y: 6.45, w: 10.6, h: 0.28, fontSize: 10, bold: true, color: C.deepGold, margin: 0,
  });
}

// 9 Meituan
{
  const s = pptx.addSlide(); addBg(s); title(s, "美团负责成交信任", "用户刷完小红书后，会到美团查地址、电话、套餐、评价和真实感。"); pageNo(s, 9);
  card(s, 0.85, 1.52, 3.65, 4.78, { fill: C.white });
  s.addText("门店装修", { x: 1.15, y: 1.88, w: 1.6, h: 0.25, fontSize: 15, bold: true, color: C.deepGold, margin: 0 });
  bullet(s, ["首图用最强厅", "图片分组：大厅/七厅/草坪/菜品/案例", "亮点统一：锦水河、七厅、8米无柱、草坪"], 1.16, 2.45, 2.75, { gap: 0.48, size: 9.3 });
  card(s, 4.85, 1.52, 3.65, 4.78, { fill: "FFFCF8", line: C.gold });
  s.addText("套餐包装", { x: 5.15, y: 1.88, w: 1.6, h: 0.25, fontSize: 15, bold: true, color: C.deepGold, margin: 0 });
  bullet(s, ["婚宴套餐写清包含项", "宝宝宴/寿宴单独包装", "年会会议突出LED、舞台、停车、用餐"], 5.16, 2.45, 2.75, { gap: 0.48, size: 9.3, color: C.rose });
  card(s, 8.85, 1.52, 3.65, 4.78, { fill: C.white });
  s.addText("搜索评价", { x: 9.15, y: 1.88, w: 1.6, h: 0.25, fontSize: 15, bold: true, color: C.deepGold, margin: 0 });
  bullet(s, ["搜索词：新都婚宴/婚礼堂/锦水河婚宴", "评价覆盖菜品、场地、停车、服务", "每周看曝光、点击、电话、收藏、到店"], 9.16, 2.45, 2.75, { gap: 0.48, size: 9.3, color: C.green });
}

// 10 Timeline
{
  const s = pptx.addSlide(); addBg(s); title(s, "90天推进节奏", "先统一口径，再稳定发布，最后通过数据放大有效内容。"); pageNo(s, 10);
  const xs = [0.8, 3.8, 6.8, 9.8];
  const heads = ["0-7天", "8-30天", "31-60天", "61-90天"];
  const bodies = [
    ["资料统一", "价格口径确认", "账号简介/置顶优化", "美团页面体检"],
    ["小红书稳定发布", "美团图片/套餐/问答更新", "建立私信跟进表", "首月复盘"],
    ["复制高点击选题", "增加真实案例", "强化顾问问答", "沉淀评价"],
    ["节假日活动", "好日子档期", "年会季内容", "形成月度看板"],
  ];
  xs.forEach((x, idx) => {
    card(s, x, 1.65, 2.55, 4.45, { fill: idx % 2 ? "FFFCF8" : C.white, line: idx % 2 ? C.gold : C.line });
    s.addText(heads[idx], { x: x + 0.22, y: 1.98, w: 1.55, h: 0.26, fontSize: 17, bold: true, color: idx === 0 ? C.rose : C.deepGold, margin: 0 });
    bullet(s, bodies[idx], x + 0.25, 2.66, 1.85, { gap: 0.47, size: 9.2, color: idx === 0 ? C.rose : C.gold });
  });
  s.addShape(pptx.ShapeType.line, { x: 1.35, y: 6.36, w: 9.45, h: 0, line: { color: C.gold, width: 1.2 } });
  s.addText("目标：把“小红书看见 → 美团查证 → 私信/电话咨询 → 到店成交”跑成固定动作。", { x: 0.86, y: 6.56, w: 11.1, h: 0.28, fontSize: 10, bold: true, color: C.ink, margin: 0 });
}

// 11 Meeting checklist
{
  const s = pptx.addSlide(); addBg(s); title(s, "明日到店要确认什么", "这些信息确认得越清楚，后面内容越不容易跑偏。"); pageNo(s, 11);
  const left = ["真实餐标、活动价、套餐包含项", "七个厅名称、桌数、层高、面积", "主推厅、利润厅、空档期厅", "草坪/停车/化妆间/茶坊等标准说法"];
  const right = ["主要客源来自哪些渠道", "咨询到到店、到店到成交转化", "近期重点档期和促销活动", "是否允许建立独家客户跟进表"];
  card(s, 0.9, 1.55, 5.45, 4.65, { fill: C.white });
  s.addText("产品与价格", { x: 1.18, y: 1.9, w: 1.8, h: 0.25, fontSize: 15, bold: true, color: C.deepGold, margin: 0 });
  bullet(s, left, 1.22, 2.55, 4.2, { gap: 0.55, size: 10 });
  card(s, 6.85, 1.55, 5.45, 4.65, { fill: "FFFCF8", line: C.gold });
  s.addText("获客与承接", { x: 7.13, y: 1.9, w: 1.8, h: 0.25, fontSize: 15, bold: true, color: C.deepGold, margin: 0 });
  bullet(s, right, 7.17, 2.55, 4.2, { gap: 0.55, size: 10, color: C.rose });
}

// 12 Fee
{
  const s = pptx.addSlide(); addBg(s); title(s, "费用与合作机制", "费用简单讲，重点放在线上链路和客资归属。"); pageNo(s, 12);
  table(s, [
    ["服务", "费用", "说明"],
    ["小红书代运营", "3500元/月，季度起签", "账号定位、内容策划、笔记发布、评论私信维护、数据复盘"],
    ["美团代运营", "2000元/月", "门店装修、套餐包装、搜索词优化、评价/问答维护、月度复盘"],
    ["正餐返佣", "6%", "按我方运营带来的实际正餐成交订单结算"],
  ], 1.0, 1.65, 11.25, 2.8, [0.22, 0.24, 0.54]);
  card(s, 1.0, 5.05, 11.25, 0.95, { fill: "FFFCF8", line: C.gold });
  s.addText("合作重点不是只发笔记，而是帮喜遇言庭把“小红书看见、美团查证、私信咨询、到店成交”这条链路跑起来。", {
    x: 1.28, y: 5.36, w: 10.55, h: 0.32, fontSize: 12, bold: true, color: C.deepGold, fit: "shrink", margin: 0,
  });
  s.addText("资料来源：GitHub 开源工具 PptxGenJS；方案信息来自公开婚宴平台、小红书公开主页抓取及本地方案整理。", {
    x: 1.02, y: 6.35, w: 10.8, h: 0.22, fontSize: 7.8, color: "8A8F98", margin: 0,
  });
}

pptx.writeFile({ fileName: out }).then(() => {
  const stat = fs.statSync(out);
  console.log(`OK ${out} ${(stat.size / 1024).toFixed(1)} KB`);
});
