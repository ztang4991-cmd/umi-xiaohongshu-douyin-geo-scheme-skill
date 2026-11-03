const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const outDir = __dirname;
const htmlPath = path.join(outDir, '牧云台·三圣乡小红书账号诊断方案.html');
const pdfPath = path.join(outDir, '牧云台·三圣乡小红书账号诊断方案.pdf');

const html = String.raw`<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>牧云台·三圣乡小红书账号诊断方案</title>
<style>
@page { size: A4; margin: 17mm 14mm 18mm; }
* { box-sizing: border-box; }
:root {
  --ink:#1f2924; --green:#29483b; --green2:#416456; --gold:#ad8350;
  --terracotta:#a85f4b; --sand:#f4efe5; --cream:#fbf9f4; --line:#d9d1c2;
  --muted:#69736e; --white:#fff;
}
html,body { margin:0; padding:0; }
body {
  color:var(--ink); background:#fff;
  font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",Arial,sans-serif;
  font-size:11.5px; line-height:1.58;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
h1,h2,h3,h4,p { margin-top:0; }
.cover {
  height:260mm; position:relative; page-break-after:always; overflow:hidden;
  padding:43mm 12mm 20mm; background:linear-gradient(145deg,#fbfaf6 0%,#f4efe5 58%,#e7eee9 100%);
}
.cover:before { content:""; position:absolute; left:-25mm; top:-20mm; width:100mm; height:100mm; border-radius:50%; border:18mm solid rgba(41,72,59,.08); }
.cover:after { content:""; position:absolute; right:-30mm; bottom:-35mm; width:120mm; height:120mm; border-radius:50%; background:rgba(173,131,80,.10); }
.cover-line { height:2mm; width:48mm; background:linear-gradient(90deg,var(--green),var(--gold),var(--terracotta)); margin:0 auto 14mm; }
.brand { text-align:center; color:var(--green2); font-size:12px; letter-spacing:2px; margin-bottom:8mm; }
.cover h1 { position:relative; z-index:1; text-align:center; font-size:30px; line-height:1.25; color:#18261f; margin:0 auto 7mm; max-width:155mm; }
.cover .sub { text-align:center; color:var(--gold); font-size:18px; font-weight:700; letter-spacing:1px; }
.cover .verdict { position:relative; z-index:1; margin:25mm auto 0; max-width:145mm; padding:8mm 9mm; border-top:1px solid #b8aa90; border-bottom:1px solid #b8aa90; text-align:center; font-size:14px; line-height:1.75; color:#34453c; background:rgba(255,255,255,.42); }
.cover-meta { position:absolute; z-index:1; left:27mm; right:27mm; bottom:28mm; display:grid; grid-template-columns:1fr 1fr; border-top:1px solid #cabfae; padding-top:5mm; color:#5f665f; font-size:11px; }
.cover-meta div:nth-child(even){text-align:right;}
.page { page-break-after:auto; }
.page:last-child { page-break-after:auto; }
.kicker { color:var(--gold); font-weight:700; letter-spacing:1.2px; font-size:10px; margin-bottom:2mm; page-break-after:avoid; break-after:avoid; }
h2 { font-size:20px; line-height:1.3; color:var(--green); margin:0 0 5mm; padding-bottom:2mm; border-bottom:1.5px solid var(--gold); page-break-after:avoid; }
h3 { font-size:14px; color:#76542e; margin:5mm 0 2mm; page-break-after:avoid; }
h4 { font-size:12px; color:var(--green); margin:0 0 1.6mm; }
p { margin-bottom:2.5mm; }
.lead { padding:5mm 5.5mm; border-left:4px solid var(--green); background:#f2f6f3; font-size:13px; line-height:1.7; margin-bottom:4mm; }
.quote { position:relative; padding:7mm 8mm 6mm 12mm; background:var(--green); color:#fff; font-size:16px; line-height:1.7; margin:4mm 0 6mm; }
.quote:before { content:"“"; position:absolute; left:4mm; top:0; color:#d5c09f; font-size:38px; font-family:Georgia,serif; }
.note { padding:3.5mm 4mm; border:1px solid var(--line); background:#fffdf8; color:#555f5a; font-size:10.5px; }
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:4mm; margin:3mm 0 5mm; }
.grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:3mm; margin:3mm 0 5mm; }
.grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:3mm; margin:3mm 0 5mm; }
.card { border:1px solid var(--line); background:var(--cream); padding:4mm; page-break-inside:avoid; }
.card strong { display:block; color:var(--green); font-size:13px; margin-bottom:1.4mm; }
.metric { text-align:center; border-top:3px solid var(--gold); background:#faf8f2; padding:4mm 2mm; }
.metric .num { font-size:24px; font-weight:800; color:var(--green); line-height:1.1; }
.metric .label { margin-top:1.5mm; color:var(--muted); font-size:10.5px; }
.badge { display:inline-block; padding:1mm 2.3mm; margin:.6mm 1mm .6mm 0; border-radius:10mm; background:#e7eee9; color:var(--green); font-size:10px; }
.badge.gold { background:#f2e7d5; color:#76542e; }
.badge.red { background:#f3e4df; color:#844636; }
.swot { border-top:4px solid var(--green); }
.swot.opp { border-top-color:var(--gold); }
.swot.risk { border-top-color:var(--terracotta); }
ul { margin:0 0 3mm 4mm; padding-left:4mm; }
li { margin-bottom:1.2mm; }
table { width:100%; border-collapse:collapse; margin:2.5mm 0 5mm; page-break-inside:avoid; }
th,td { border:1px solid var(--line); padding:2.4mm 2.3mm; vertical-align:top; line-height:1.45; }
th { background:var(--green); color:#fff; font-weight:700; text-align:center; }
tbody tr:nth-child(odd) td { background:#fbfaf6; }
.diagnosis th:nth-child(1){width:17%;}.diagnosis th:nth-child(2){width:29%;}.diagnosis th:nth-child(3){width:25%;}.diagnosis th:nth-child(4){width:29%;}
.compact { font-size:10px; }
.compact th,.compact td { padding:2mm 1.8mm; }
.competitor th:nth-child(1){width:9%;}.competitor th:nth-child(2){width:17%;}.competitor th:nth-child(3){width:19%;}.competitor th:nth-child(4){width:20%;}.competitor th:nth-child(5){width:17%;}.competitor th:nth-child(6){width:18%;}
.section-number { display:inline-flex; align-items:center; justify-content:center; width:8mm; height:8mm; border-radius:50%; background:var(--gold); color:white; margin-right:2mm; font-size:11px; }
.timeline { display:grid; grid-template-columns:33mm 1fr; gap:0; margin-top:3mm; }
.timeline .phase { padding:3mm; color:#fff; font-weight:700; background:var(--green); border-bottom:1px solid #587064; }
.timeline .detail { padding:3mm 4mm; background:#f8f6f0; border-right:1px solid var(--line); border-bottom:1px solid var(--line); }
.mix { margin:4mm 0; }
.mix-row { display:grid; grid-template-columns:38mm 1fr 13mm; gap:3mm; align-items:center; margin:2.5mm 0; }
.bar { height:8mm; background:#ebe7dd; position:relative; overflow:hidden; border-radius:1mm; }
.bar > span { display:block; height:100%; background:linear-gradient(90deg,var(--green),var(--green2)); }
.mix-row:nth-child(2) .bar>span{background:linear-gradient(90deg,#76542e,var(--gold));}
.mix-row:nth-child(3) .bar>span{background:linear-gradient(90deg,#8c5948,var(--terracotta));}
.mix-row:nth-child(4) .bar>span{background:linear-gradient(90deg,#69736e,#94a29b);}
.keyword { border:1px solid var(--line); padding:3mm; min-height:28mm; background:#fff; }
.keyword strong{color:var(--green);display:block;margin-bottom:1mm;}
.callout { border:1px solid #c9b89f; background:linear-gradient(135deg,#fffdf8,#f4efe5); padding:5mm; margin:4mm 0; }
.priority { display:grid; grid-template-columns:12mm 1fr; gap:3mm; margin:2.5mm 0; align-items:start; }
.priority .n { width:9mm; height:9mm; border-radius:50%; background:var(--terracotta); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700; }
.small { font-size:10px; color:var(--muted); }
.center { text-align:center; }
.no-break { page-break-inside:avoid; }
.end { margin-top:10mm; padding:7mm; text-align:center; background:var(--green); color:#fff; font-size:13px; }
</style>
</head>
<body>

<section class="cover">
  <div class="cover-line"></div>
  <div class="brand">聚光米 UMI 运营团队 · 本地生活内容运营</div>
  <h1>牧云台·三圣乡<br>小红书账号诊断方案</h1>
  <div class="sub">从“漂亮场地展示”升级为“宴会决策入口”</div>
  <div class="verdict">牧云台不缺场地质感和内容素材。当前关键不是继续堆叠婚礼画面，而是把已有的建筑、草坪、夜间派对和复合业态，转化为用户能够搜索、比较与判断的结构化内容资产。</div>
  <div class="cover-meta">
    <div>诊断对象：牧云台蓝V账号</div><div>小红书号：27760215304</div>
    <div>账号查看日期：2026年7月22日</div><div>用途：门店经营与运营决策参考</div>
  </div>
</section>

<section class="page">
  <div class="kicker">01 / EXECUTIVE SUMMARY</div>
  <h2>项目概况与核心诊断</h2>
  <div class="lead"><strong>一句话诊断：</strong>门店已有较强视觉资产和外部UGC基础，但蓝V目前尚未形成明确的业务主次、稳定的搜索占位和完整的宴会决策信息，导致“有人看过场地”与“能够理解产品”之间存在断层。</div>
  <div class="grid-4">
    <div class="metric"><div class="num">62</div><div class="label">关注</div></div>
    <div class="metric"><div class="num">69</div><div class="label">粉丝</div></div>
    <div class="metric"><div class="num">360</div><div class="label">获赞与收藏</div></div>
    <div class="metric"><div class="num">4.5</div><div class="label">POI评分</div></div>
  </div>
  <div class="grid-3">
    <div class="card"><strong>18条</strong>POI公开评价，正向反馈集中在草坪、建筑、天台、布置和拍照体验。</div>
    <div class="card"><strong>约919</strong>POI收藏，说明门店具备一定被发现、被记录和被再次查看的基础。</div>
    <div class="card"><strong>30条样本</strong>近期公开笔记累计约74赞，平均约2.47赞，最高约6赞。</div>
  </div>
  <h3>数据口径说明</h3>
  <p>本诊断依据2026年7月22日蓝V主页公开可见信息、门店POI页面及用户提供的评价与笔记截图形成。账号与平台数据会持续变化，公开互动仅作为内容表现样本，不等同于完整后台数据。</p>
  <div class="grid-2">
    <div class="card swot"><strong>现有基础</strong><ul><li>设计师建筑、草坪、天台及夜景具有识别度</li><li>已有婚礼、求婚、派对等真实场景素材</li><li>外部UGC曾形成较高互动内容</li><li>餐饮、茶空间、精酿、窑烤可拓展日常消费</li></ul></div>
    <div class="card swot risk"><strong>当前制约</strong><ul><li>业务标签多，但首屏没有清晰主次</li><li>婚礼画面重复，决策型信息不足</li><li>更新节奏存在明显断层</li><li>UGC、POI与蓝V尚未形成统一叙事</li></ul></div>
  </div>
  <div class="note">判断原则：低互动不能简单归因于场地缺乏吸引力，更合理的解释是账号定位、标题封面、信息结构、更新稳定性和用户意图匹配仍有改善空间。</div>
</section>

<section class="page">
  <div class="kicker">02 / MARKET LANDSCAPE</div>
  <h2>三圣乡市场：竞争已经进入“决策内容”阶段</h2>
  <div class="quote">三圣乡不缺自然流量，也不缺漂亮院子；真正稀缺的是能在用户搜索和比较阶段，把场地、人数、预算、菜单、雨备、停车和真实案例讲清楚的专业账号。</div>
  <div class="grid-2">
    <div class="card"><strong>区域成熟度高</strong>三圣乡长期承接周末休闲、家庭聚会、花园餐饮、婚礼宴会和企业活动需求，用户已形成跨店比较习惯。</div>
    <div class="card"><strong>内容竞争主体多</strong>门店蓝V之外，婚礼策划师、摄影师、探店达人、新人与消费者都在争夺同一批搜索结果。</div>
    <div class="card"><strong>审美表达同质化</strong>“浪漫、出片、小众、氛围感、治愈”等描述高度重复，单纯展示漂亮画面难以支持最终判断。</div>
    <div class="card"><strong>决策链路较长</strong>婚礼和宴会用户会反复对比人数、餐标、菜单、档期、停车、雨备、私密性和真实案例。</div>
  </div>
  <h3>竞争强度判断：中高至高</h3>
  <table>
    <thead><tr><th>竞争维度</th><th>市场现状</th><th>对牧云台的要求</th></tr></thead>
    <tbody>
      <tr><td><strong>场景审美</strong></td><td>花园、草坪、法式、森系、独栋等供给密集。</td><td>不能只说环境好，需要建立设计师庭院与夜间派对的辨识度。</td></tr>
      <tr><td><strong>搜索占位</strong></td><td>用户会搜索成都/三圣乡＋婚礼、商务宴、聚会、下午茶等组合词。</td><td>按真实搜索意图设置标题、正文、合集与POI关联。</td></tr>
      <tr><td><strong>信任证明</strong></td><td>真实新人、第三方策划师与消费者内容影响决策。</td><td>把外部UGC转化为可验证的案例库和品牌资产。</td></tr>
      <tr><td><strong>咨询承接</strong></td><td>用户需要快速获得价格、人数、场地和看场信息。</td><td>用结构化资料降低反复沟通成本，提高咨询有效性。</td></tr>
    </tbody>
  </table>
  <div class="callout"><strong>相对机会：</strong>草坪婚礼是高竞争词，但“三圣乡商务宴请、庭院客户接待、企业小型晚宴、会议＋茶空间＋用餐”等内容供给相对分散。牧云台可将商务宴作为第二增长线，而不是继续与所有门店只争同一种婚礼画面。</div>
</section>

<section class="page">
  <div class="kicker">03 / ACCOUNT DIAGNOSIS</div>
  <h2>账号现状诊断（上）</h2>
  <table class="diagnosis compact">
    <thead><tr><th>现状</th><th>诊断依据</th><th>可能影响</th><th>优化建议</th></tr></thead>
    <tbody>
      <tr><td><strong>定位信息分散</strong></td><td>简介同时罗列民宿、餐厅、下午茶、茶空间、棋牌、窑烤、精酿和小型宴会。</td><td>用户进入主页后难以在几秒内判断核心业务；不同人群标签可能互相稀释。</td><td>确立“庭院宴会”为核心，婚礼为第一主线、商务宴为第二主线，下午茶和餐饮承担高频入口。</td></tr>
      <tr><td><strong>内容集中在婚礼</strong></td><td>近期内容主要围绕草坪婚礼、求婚、户外婚礼和现场片段。</td><td>账号名称中的商务宴、下午茶、民宿、团建与餐饮价值没有被持续证明。</td><td>按业务目标建立栏目比例，避免所有内容都使用相似婚礼镜头。</td></tr>
      <tr><td><strong>标题偏氛围化</strong></td><td>可见《热闹的婚礼》《婚礼进行式》《户外婚礼》《夜晚热情不减》等泛化标题。</td><td>缺少成都、三圣乡、人数、预算和人群词，搜索入口与点击理由不足。</td><td>标题优先回答“在哪里、适合谁、什么场景、有什么差异”，再补充情绪表达。</td></tr>
      <tr><td><strong>产品信息未体系化</strong></td><td>内容已出现1688—4288元/桌、三个户外仪式场地、一站式配套等信息，但分散在个别正文中。</td><td>有价值的信息未成为稳定卖点，用户仍需反复询问基本问题。</td><td>建立场地、人数、桌数、餐标、菜单、停车、雨备、档期和预约流程模板。</td></tr>
    </tbody>
  </table>
  <h3>标题优化示例</h3>
  <div class="grid-2">
    <div class="card"><strong>原表达：夜晚的草坪派对如此迷人</strong><span class="small">信息偏情绪化，搜索和筛选信息较少。</span><br><br><strong>优化方向</strong>成都三圣乡草坪Afterparty｜3个户外仪式区，晚宴餐标1688元/桌起</div>
    <div class="card"><strong>原表达：成都三圣乡求婚场地</strong><span class="small">已有区域词，但缺少容量、服务与场景答案。</span><br><br><strong>优化方向</strong>三圣乡庭院求婚怎么选？人数、花墙布置、雨天方案一次讲清</div>
  </div>
  <div class="note">示例用于说明信息结构，具体标题需结合门店已确认的价格、容量、服务边界及当期素材后发布。</div>
</section>

<section class="page">
  <div class="kicker">03 / ACCOUNT DIAGNOSIS</div>
  <h2>账号现状诊断（下）</h2>
  <table class="diagnosis compact">
    <thead><tr><th>现状</th><th>诊断依据</th><th>可能影响</th><th>优化建议</th></tr></thead>
    <tbody>
      <tr><td><strong>更新节奏断层</strong></td><td>可见内容存在短期集中发布后停更数周的情况；2026年6月6日至7月18日前后存在较长空档。</td><td>不利于持续建立账号标签，也使新案例、档期和产品信息无法稳定触达。</td><td>建立月度选题、集中拍摄、素材归档和固定发布节奏，保留临时热点弹性。</td></tr>
      <tr><td><strong>UGC未回流蓝V</strong></td><td>POI笔记中可见多条数百至两千赞以上的外部内容，主题集中于建筑、人像、度假感和拍照出片。</td><td>门店已有关注度没有转化为官方案例、宴会能力和品牌信任资产。</td><td>合规联动消费者、摄影师与策划师；通过官方合集、案例复盘和POI关联形成统一认知。</td></tr>
      <tr><td><strong>POI资产承接不足</strong></td><td>POI公开评分4.5、评价18条、收藏约919；评价提及草坪婚礼、Afterparty、精酿、天台和布置。</td><td>用户看到环境优势后，仍可能缺少进入蓝V继续了解产品的完整路径。</td><td>让置顶内容承接POI高频关注点，并持续回答看场前的关键问题。</td></tr>
    </tbody>
  </table>
  <h3>内容链路的核心断点</h3>
  <div class="timeline no-break">
    <div class="phase">被看见</div><div class="detail"><strong>已有基础：</strong>建筑、草坪、人像、夜景和派对内容具备视觉吸引力，外部UGC证明场地具有传播素材。</div>
    <div class="phase">被理解</div><div class="detail"><strong>当前薄弱：</strong>用户难以快速理解婚礼、商务宴、下午茶各自适合谁，以及人数、预算和服务边界。</div>
    <div class="phase">被比较</div><div class="detail"><strong>当前薄弱：</strong>缺少停车、雨备、菜单、桌数、私密性、日夜场景和案例复盘等横向对比信息。</div>
    <div class="phase">被咨询</div><div class="detail"><strong>需要建立：</strong>用分类资料、统一问题清单和看场预约路径，提高咨询信息完整度。</div>
  </div>
  <div class="callout"><strong>核心任务不是单纯增加内容数量，而是补齐“被看见—被理解—被比较—被咨询”的完整链路。</strong></div>
</section>

<section class="page">
  <div class="kicker">04 / BRAND ASSETS</div>
  <h2>账号优势与潜在机会</h2>
  <div class="grid-2">
    <div class="card swot"><strong>01 视觉辨识度</strong>建筑、草坪、天台、木质元素和夜间灯光可形成从日景到夜景的完整内容资产，不必只依赖单一婚礼布置。</div>
    <div class="card swot"><strong>02 场景延展性</strong>可承接草坪婚礼、求婚、订婚宴、Afterparty、小型宴会等多个相邻场景，具备案例系列化条件。</div>
    <div class="card swot opp"><strong>03 复合消费能力</strong>商务宴、茶空间、精酿、窑烤、下午茶等业态可填补工作日和非婚礼档期内容，增强日常到店理由。</div>
    <div class="card swot opp"><strong>04 已有口碑素材</strong>公开评价中存在对面积、建筑、布置、拍照和聚会体验的正向描述，可进一步整理为信任证明。</div>
    <div class="card swot"><strong>05 UGC传播基础</strong>POI下已有多条较高互动的外部笔记，说明门店并非缺乏内容吸引力，而是需要将关注沉淀到官方叙事。</div>
    <div class="card swot opp"><strong>06 商务宴空位</strong>相比高度拥挤的草坪婚礼表达，庭院客户接待、企业小型晚宴和会议用餐更有机会形成差异化。</div>
  </div>
  <h3>建议建立的品牌表达</h3>
  <div class="quote">设计师庭院，不只适合拍照；也能够承接一场从白天到夜晚、从仪式到用餐、从社交到深度交流的完整聚会。</div>
  <div class="grid-3">
    <div class="card center"><strong>日景</strong>建筑、草坪、下午茶<br>适合踩点与轻社交</div>
    <div class="card center"><strong>宴席</strong>婚礼、商务宴、家庭宴<br>突出菜单与服务</div>
    <div class="card center"><strong>夜场</strong>灯光、精酿、窑烤、派对<br>强化Afterparty</div>
  </div>
  <div class="note">复合业态不等于所有业务平均传播。对外必须形成主次，避免再次回到“什么都有，但用户记不住什么最强”的状态。</div>
</section>

<section class="page">
  <div class="kicker">05 / COMPETITOR REVIEW</div>
  <h2>同区域竞品对比</h2>
  <table class="competitor compact">
    <thead><tr><th>竞品</th><th>核心定位</th><th>内容心智</th><th>主要优势</th><th>可改善点</th><th>对牧云台的启示</th></tr></thead>
    <tbody>
      <tr><td><strong>悦哉</strong></td><td>独栋庭院、民宿、小型婚礼</td><td>树下婚礼、清迈感、私密性、Afterparty</td><td>日夜场景和独栋私密心智明确；第三方内容共同占位。</td><td>悦哉/乐哉名称存在搜索分流可能；价格、人数、雨备仍可更完整。</td><td>牧云台应强化夜场，但要用产品参数和商务场景形成不同心智。</td></tr>
      <tr><td><strong>可悦</strong></td><td>私房菜＋庭院聚会＋草坪婚礼</td><td>摩洛哥风、三层院子、聚餐与宴会</td><td>账号内容存量和更新频率领先；餐饮为宴会补充高频入口。</td><td>临餐、家庭宴与婚礼内容集中于同一账号时，标签可能分散。</td><td>复合业务要有明确栏目与内容比例，不能只追求发布数量。</td></tr>
      <tr><td><strong>春生花园</strong></td><td>小而美户外婚礼、泳池、性价比</td><td>户外婚礼案例、踩点、餐标比较</td><td>历史案例和第三方UGC基础较深，容易进入场地比较搜索。</td><td>官方搜索存在感相对有限；历史内容与改造后产品需重新衔接。</td><td>牧云台应尽早沉淀官方案例，不让关键解释长期掌握在第三方手中。</td></tr>
      <tr><td><strong>祥和花园</strong></td><td>一站式婚礼堂、室内主题厅</td><td>法式宫殿、标准化婚礼、省心承接</td><td>室内场景和雨天承接能力强，适配较大规模标准化宴会。</td><td>婚礼堂同质化较强；自然庭院和私密感相对不是主优势。</td><td>牧云台可用自然庭院、私密小型宴会和日夜联动形成区隔。</td></tr>
    </tbody>
  </table>
  <div class="note">春生花园说明：根据项目内执行资料，2026年7—9月处于装修改造及开业预热阶段，历史内容与后续产品之间可能存在更新衔接需求。</div>
  <h3>竞品结论</h3>
  <div class="grid-2">
    <div class="card"><strong>不建议复制</strong>继续堆叠草坪、花墙、森系、法式等泛审美内容，会使牧云台进入高度同质化竞争。</div>
    <div class="card"><strong>建议建立</strong>“设计师庭院＋草坪宴会＋夜间派对＋商务宴请”的复合差异化，并以参数与案例证明。</div>
  </div>
  <p class="small">竞品判断来自公开可见内容样本与项目内既有研究，主要用于识别定位差异，不构成对其经营结果的评价。</p>
</section>

<section class="page">
  <div class="kicker">06 / POSITIONING</div>
  <h2>推荐定位与账号结构</h2>
  <div class="quote center">三圣乡设计师庭院宴会目的地</div>
  <div class="grid-3">
    <div class="card"><strong>第一主线</strong>小型草坪婚礼<br>求婚、订婚宴<br>Afterparty</div>
    <div class="card"><strong>第二主线</strong>商务宴、客户接待<br>企业晚宴、团建<br>会议＋用餐</div>
    <div class="card"><strong>高频入口</strong>下午茶、窑烤<br>精酿、茶空间<br>工作日消费</div>
  </div>
  <h3>主页信息建议</h3>
  <table>
    <thead><tr><th>模块</th><th>建议方向</th></tr></thead>
    <tbody>
      <tr><td><strong>昵称</strong></td><td>牧云台｜三圣乡庭院宴会；或牧云台｜三圣乡草坪婚礼·商务宴。</td></tr>
      <tr><td><strong>简介</strong></td><td>先讲核心场景和区域，再讲关键能力。示例结构：三圣乡设计师庭院｜草坪婚礼·商务宴·Afterparty｜下午茶与茶空间｜预约看场。</td></tr>
      <tr><td><strong>置顶一</strong></td><td>第一次了解牧云台：空间、场地、容量、停车、交通和适合场景总览。</td></tr>
      <tr><td><strong>置顶二</strong></td><td>婚礼与求婚方案：仪式区、餐标、布置边界、雨备和真实案例。</td></tr>
      <tr><td><strong>置顶三</strong></td><td>商务宴与企业聚会：包场方式、会议茶歇、菜单、私密性和预约流程。</td></tr>
      <tr><td><strong>合集</strong></td><td>草坪婚礼｜求婚订婚｜商务宴请｜下午茶餐饮｜看场指南｜真实案例。</td></tr>
    </tbody>
  </table>
  <h3>搜索关键词分组</h3>
  <div class="grid-3">
    <div class="keyword"><strong>婚礼宴会</strong>成都草坪婚礼<br>三圣乡婚礼场地<br>小型户外婚礼<br>成都订婚宴<br>草坪Afterparty</div>
    <div class="keyword"><strong>商务企业</strong>三圣乡商务宴<br>成都庭院商务餐<br>客户接待餐厅<br>企业小型晚宴<br>成都团建场地</div>
    <div class="keyword"><strong>日常消费</strong>三圣乡下午茶<br>三圣乡庭院餐厅<br>成都精酿花园<br>三圣乡窑烤<br>成都茶空间</div>
  </div>
</section>

<section class="page">
  <div class="kicker">07 / CONTENT SYSTEM</div>
  <h2>内容架构与标题封面原则</h2>
  <div class="mix">
    <div class="mix-row"><strong>婚礼/求婚/派对</strong><div class="bar"><span style="width:40%"></span></div><strong>40%</strong></div>
    <div class="mix-row"><strong>商务宴/团建/家庭宴</strong><div class="bar"><span style="width:25%"></span></div><strong>25%</strong></div>
    <div class="mix-row"><strong>下午茶/餐饮/工作日</strong><div class="bar"><span style="width:20%"></span></div><strong>20%</strong></div>
    <div class="mix-row"><strong>路线/雨备/流程/幕后</strong><div class="bar"><span style="width:15%"></span></div><strong>15%</strong></div>
  </div>
  <h3>内容栏目示例</h3>
  <div class="grid-2">
    <div class="card"><strong>场地答案</strong>多少人合适、草坪与餐区如何连接、三个户外仪式区分别适合什么、停车与路线如何安排。</div>
    <div class="card"><strong>预算答案</strong>餐标包含什么、布置与场地如何计算、不同人数如何选、预算容易遗漏哪些项目。</div>
    <div class="card"><strong>真实案例</strong>从需求、人数、场景、执行难点到最终效果，建立可被比较的案例档案。</div>
    <div class="card"><strong>商务场景</strong>客户接待、企业晚宴、团建、会议茶歇与晚餐组合，突出私密性与服务流程。</div>
    <div class="card"><strong>日夜体验</strong>下午茶—晚宴—精酿派对的时间线内容，强化全天候复合空间。</div>
    <div class="card"><strong>信任幕后</strong>雨备演练、草坪维护、摆台、厨房备餐、服务准备和活动撤场。</div>
  </div>
  <h3>标题与封面原则</h3>
  <table class="compact">
    <thead><tr><th>要素</th><th>建议</th><th>避免</th></tr></thead>
    <tbody>
      <tr><td>标题</td><td>区域词＋场景词＋关键答案/差异点。</td><td>只写“氛围感、太美了、婚礼进行式”等泛表达。</td></tr>
      <tr><td>封面</td><td>一个主画面＋一个核心决策信息；全景、人物和细节有稳定比例。</td><td>同一场景连续使用相似远景，或文字过多遮挡主体。</td></tr>
      <tr><td>正文</td><td>先回答适合谁，再给人数、预算、服务、雨备、停车和预约信息。</td><td>只有情绪描写、装饰风格和无边界的产品描述。</td></tr>
    </tbody>
  </table>
</section>

<section class="page">
  <div class="kicker">08 / OPERATING UPGRADE</div>
  <h2>运营接手后的改善方向</h2>
  <div class="priority"><div class="n">1</div><div><h4>统一账号定位与主页表达</h4>统一昵称、简介、置顶、合集、封面和视觉语言，让用户进入主页后快速识别核心业务。</div></div>
  <div class="priority"><div class="n">2</div><div><h4>建立三类搜索内容矩阵</h4>围绕婚礼宴会、商务企业、下午茶餐饮分别规划关键词、选题和案例，避免内容标签相互干扰。</div></div>
  <div class="priority"><div class="n">3</div><div><h4>完成产品信息结构化</h4>统一收集人数、桌数、餐标、菜单、场地、停车、雨备、档期和预约流程，形成可复用内容模板。</div></div>
  <div class="priority"><div class="n">4</div><div><h4>建立稳定生产机制</h4>按月完成选题规划、集中拍摄、素材归档、发布排期和数据复盘，减少集中连发后长期停更。</div></div>
  <div class="priority"><div class="n">5</div><div><h4>推动UGC资产回流</h4>合规联动真实消费者、新人、策划师、摄影师和企业客户，让第三方内容与官方案例形成相互验证。</div></div>
  <div class="priority"><div class="n">6</div><div><h4>打通蓝V、POI与咨询链路</h4>让POI评价、高频问题、官方笔记和预约看场形成一致路径，降低用户获取信息的成本。</div></div>
  <div class="priority"><div class="n">7</div><div><h4>以数据持续迭代</h4>根据搜索收录、主页访问、收藏、咨询问题和看场来源，持续调整内容主题与表达方式。</div></div>
  <div class="callout"><strong>可交付的核心价值：</strong>建立更清晰的账号定位、更完整的产品表达、更稳定的内容机制和更可复盘的用户路径。实际市场表现仍会受到门店产品、价格、服务、档期、投放与市场环境等多重因素影响。</div>
</section>

<section class="page">
  <div class="kicker">09 / MEASUREMENT</div>
  <h2>建议考核指标与阶段重点</h2>
  <table>
    <thead><tr><th>指标层级</th><th>建议观察项</th><th>用途</th></tr></thead>
    <tbody>
      <tr><td><strong>内容执行</strong></td><td>月度选题完成率、拍摄完成率、发布稳定性、栏目覆盖情况。</td><td>判断运营机制是否稳定落地。</td></tr>
      <tr><td><strong>搜索能力</strong></td><td>核心关键词覆盖、收录位置、搜索来源占比、长尾词新增情况。</td><td>判断账号是否进入用户主动比较链路。</td></tr>
      <tr><td><strong>内容质量</strong></td><td>封面点击表现、阅读/观看完成度、收藏率、评论问题质量。</td><td>识别哪些主题真正帮助用户决策。</td></tr>
      <tr><td><strong>主页承接</strong></td><td>主页访问、置顶内容访问、合集浏览、POI关联表现。</td><td>判断单篇内容能否带动进一步了解。</td></tr>
      <tr><td><strong>有效咨询</strong></td><td>咨询场景、人数、预算、档期、看场意向及高频问题。</td><td>判断信息是否匹配目标客群，并反哺选题。</td></tr>
      <tr><td><strong>线下反馈</strong></td><td>看场预约、到店来源记录、未继续推进原因、门店服务反馈。</td><td>连接线上内容与线下经营，形成复盘闭环。</td></tr>
    </tbody>
  </table>
  <h3>建议阶段顺序</h3>
  <div class="timeline">
    <div class="phase">阶段一</div><div class="detail"><strong>定位与基建：</strong>完成主页改造、产品资料盘点、置顶内容和关键词库。</div>
    <div class="phase">阶段二</div><div class="detail"><strong>栏目验证：</strong>持续测试婚礼、商务宴和日常消费三类内容，识别高质量主题。</div>
    <div class="phase">阶段三</div><div class="detail"><strong>案例沉淀：</strong>建立真实活动档案，推动UGC、POI和蓝V协同。</div>
    <div class="phase">阶段四</div><div class="detail"><strong>数据优化：</strong>围绕搜索、主页、咨询和看场反馈迭代选题及表达。</div>
  </div>
  <div class="end">最终目标：让牧云台在三圣乡同类竞争中，不只被看见，更能被理解、被比较，并形成持续积累的官方内容资产。</div>
  <p class="small center" style="margin-top:6mm;">本方案为账号公开信息诊断与运营建议，具体执行需结合门店最新产品资料、场地容量、价格体系、档期和服务流程进一步校准。</p>
</section>

</body>
</html>`;

(async () => {
  fs.writeFileSync(htmlPath, html, 'utf8');
  const candidates = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
  ];
  const executablePath = candidates.find(fs.existsSync);
  const browser = await chromium.launch(executablePath ? { executablePath, headless:true } : { headless:true });
  const page = await browser.newPage({ viewport:{ width:1240, height:1754 }, deviceScaleFactor:1 });
  await page.goto('file:///' + htmlPath.replace(/\\/g,'/'), { waitUntil:'networkidle' });
  await page.emulateMedia({ media:'print' });
  await page.pdf({
    path: pdfPath,
    format:'A4',
    printBackground:true,
    preferCSSPageSize:true,
    displayHeaderFooter:true,
    headerTemplate:`<div style="font-size:8px;color:#758079;width:100%;padding:0 14mm;font-family:Microsoft YaHei,Arial,sans-serif;display:flex;justify-content:space-between;"><span>牧云台·三圣乡小红书账号诊断方案</span><span>聚光米 UMI</span></div>`,
    footerTemplate:`<div style="font-size:8px;color:#758079;width:100%;padding:0 14mm;font-family:Microsoft YaHei,Arial,sans-serif;display:flex;justify-content:space-between;"><span>数据查看日期：2026年7月22日</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
    margin:{ top:'17mm', right:'14mm', bottom:'18mm', left:'14mm' }
  });
  await browser.close();

  const forbidden = ['首次联系','微信沟通','销售异议'];
  for (const term of forbidden) {
    if (html.includes(term)) throw new Error('正文包含不应出现的内容：' + term);
  }
  console.log(JSON.stringify({ htmlPath, pdfPath, bytes:fs.statSync(pdfPath).size }, null, 2));
})().catch(err => { console.error(err); process.exit(1); });


