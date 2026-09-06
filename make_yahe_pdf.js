const fs = require("fs");
const path = require("path");

const src = "C:/Users/EDY/mslearn-ai-agents/雅禾婚礼_小红书运营方案_初版.md";
const out = "C:/Users/EDY/mslearn-ai-agents/雅禾婚礼_小红书运营方案_初版.html";

function esc(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function inline(s) {
  return esc(s).replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
}

const lines = fs.readFileSync(src, "utf8").split(/\r?\n/);
const html = [];
let inList = false;
let inTable = false;
let tableRows = [];

function closeList() {
  if (inList) {
    html.push("</ul>");
    inList = false;
  }
}

function flushTable() {
  if (!inTable) return;
  html.push("<table>");
  tableRows.forEach((row, idx) => {
    if (/^\|[\s\-:|]+\|$/.test(row)) return;
    const cells = row.split("|").slice(1, -1).map(c => inline(c.trim()));
    html.push("<tr>");
    cells.forEach(c => html.push(idx === 0 ? `<th>${c}</th>` : `<td>${c}</td>`));
    html.push("</tr>");
  });
  html.push("</table>");
  tableRows = [];
  inTable = false;
}

for (const raw of lines) {
  const line = raw.trimEnd();
  if (line.startsWith("|") && line.endsWith("|")) {
    closeList();
    inTable = true;
    tableRows.push(line);
    continue;
  }
  flushTable();

  if (!line.trim()) {
    closeList();
    html.push("");
  } else if (line === "---") {
    closeList();
    html.push("<hr>");
  } else if (line.startsWith("# ")) {
    closeList();
    html.push(`<h1>${inline(line.replace(/^#\s*/, ""))}</h1>`);
  } else if (line.startsWith("## ")) {
    closeList();
    html.push(`<h2>${inline(line.replace(/^##\s*/, ""))}</h2>`);
  } else if (line.startsWith("### ")) {
    closeList();
    html.push(`<h3>${inline(line.replace(/^###\s*/, ""))}</h3>`);
  } else if (line.startsWith(">")) {
    closeList();
    html.push(`<blockquote>${inline(line.replace(/^>\s*/, ""))}</blockquote>`);
  } else if (/^\s*-\s+/.test(line)) {
    if (!inList) {
      html.push("<ul>");
      inList = true;
    }
    html.push(`<li>${inline(line.replace(/^\s*-\s+/, ""))}</li>`);
  } else {
    closeList();
    html.push(`<p>${inline(line)}</p>`);
  }
}
closeList();
flushTable();

const doc = `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>雅禾婚礼_小红书运营方案_初版</title>
<style>
  @page { size: A4; margin: 18mm 16mm; }
  body {
    font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif;
    color: #2d2220;
    font-size: 14px;
    line-height: 1.75;
  }
  h1 {
    text-align: center;
    font-size: 30px;
    color: #2d2220;
    margin: 42px 0 8px;
  }
  h2 {
    font-size: 20px;
    color: #9e1f34;
    border-left: 5px solid #cda349;
    padding-left: 10px;
    margin: 28px 0 12px;
    break-after: avoid;
  }
  h3 {
    font-size: 16px;
    color: #7b5a28;
    margin: 18px 0 8px;
    break-after: avoid;
  }
  p { margin: 0 0 8px; }
  ul { margin: 0 0 10px 22px; padding: 0; }
  li { margin: 0 0 4px; }
  blockquote {
    color: #666;
    background: #faf8f6;
    border-left: 4px solid #cda349;
    margin: 12px 0;
    padding: 8px 12px;
  }
  hr {
    border: none;
    border-top: 1px solid #e7d7b4;
    margin: 18px 0;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px;
    font-size: 13px;
    break-inside: avoid;
  }
  th {
    background: #9e1f34;
    color: #fff;
    font-weight: 700;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 7px 8px;
    vertical-align: top;
  }
  tr:nth-child(even) td { background: #fbf8f6; }
  strong { color: #2f6f5e; }
</style>
</head>
<body>
${html.join("\n")}
</body>
</html>`;

fs.writeFileSync(out, doc, "utf8");
console.log(out);
