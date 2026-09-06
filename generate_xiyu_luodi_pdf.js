const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const base = "C:/Users/EDY/mslearn-ai-agents";
const mdPath = path.join(base, "新都喜遇言庭宴会中心_小红书美团落地运营方案.md");
const htmlPath = path.join(base, "新都喜遇言庭宴会中心_小红书美团落地运营方案.html");
const pdfPath = path.join(base, "新都喜遇言庭宴会中心_小红书美团落地运营方案.pdf");

function esc(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function inline(text) {
  return esc(text).replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
}

function parseRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => inline(cell.trim()));
}

function isTableSep(line) {
  return /^\|\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?$/.test(line.trim());
}

function renderTable(lines) {
  const headers = parseRow(lines[0]);
  const rows = lines.slice(2).map(parseRow);
  const th = headers.map((h) => `<th>${h}</th>`).join("");
  const tr = rows
    .map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`)
    .join("\n");
  return `<table><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>`;
}

function mdToHtml(md) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    if (line.trim().startsWith("|")) {
      const tableLines = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        tableLines.push(lines[i]);
        i += 1;
      }
      if (tableLines.length >= 3 && isTableSep(tableLines[1])) {
        out.push(renderTable(tableLines));
      }
      continue;
    }

    if (line.startsWith("# ")) out.push(`<h1>${inline(line.replace(/^#\s*/, ""))}</h1>`);
    else if (line.startsWith("## ")) out.push(`<h2>${inline(line.replace(/^##\s*/, ""))}</h2>`);
    else if (line.startsWith("### ")) out.push(`<h3>${inline(line.replace(/^###\s*/, ""))}</h3>`);
    else if (/^\s*-\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*-\s+/.test(lines[i])) {
        items.push(`<li>${inline(lines[i].replace(/^\s*-\s+/, ""))}</li>`);
        i += 1;
      }
      out.push(`<ul>${items.join("")}</ul>`);
      continue;
    } else if (line.trim() === "---") out.push("<hr>");
    else if (line.trim() === "") out.push("");
    else out.push(`<p>${inline(line)}</p>`);
    i += 1;
  }
  return out.join("\n");
}

const md = fs.readFileSync(mdPath, "utf8");
const body = mdToHtml(md);
const html = `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>新都喜遇言庭宴会中心_小红书美团落地运营方案</title>
<style>
@page { size: A4; margin: 16mm 15mm; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif;
  color: #222831;
  line-height: 1.56;
  font-size: 12.5px;
  background: #ffffff;
}
h1 {
  text-align: center;
  margin: 84mm 0 5mm;
  font-size: 30px;
  letter-spacing: 0;
  color: #222831;
}
h1 + h2 {
  text-align: center;
  border: 0;
  margin-top: 0;
  font-size: 21px;
  color: #b48a4a;
  page-break-after: always;
}
h2 {
  margin: 8mm 0 3.5mm;
  padding-bottom: 1.6mm;
  border-bottom: 1.5px solid #b48a4a;
  font-size: 18px;
  color: #222831;
  page-break-after: avoid;
}
h3 {
  margin: 5mm 0 2mm;
  font-size: 14px;
  color: #9b7138;
  page-break-after: avoid;
}
p { margin: 0 0 3mm; }
ul { margin: 0 0 3.5mm 5mm; padding-left: 4mm; }
li { margin: 0 0 1.4mm; }
strong { font-weight: 700; }
hr { border: 0; height: 3mm; margin: 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 2.5mm 0 4mm;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #d7d0c4;
  padding: 2.1mm 2.2mm;
  vertical-align: top;
  line-height: 1.45;
}
th {
  background: #222831;
  color: #fff;
  font-weight: 700;
  text-align: center;
}
tbody tr:nth-child(odd) td { background: #fcfaf7; }
a { color: #8a612b; text-decoration: none; }
</style>
</head>
<body>
${body}
</body>
</html>`;

fs.writeFileSync(htmlPath, html, "utf8");

const chromeCandidates = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
];
const chrome = chromeCandidates.find((candidate) => fs.existsSync(candidate));
if (!chrome) {
  throw new Error("Chrome/Edge executable not found");
}

const result = spawnSync(
  chrome,
  [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--disable-extensions",
    `--print-to-pdf=${pdfPath}`,
    `file:///${htmlPath.replace(/\\/g, "/")}`,
  ],
  { encoding: "utf8" }
);

if (result.status !== 0) {
  console.error(result.stdout);
  console.error(result.stderr);
  process.exit(result.status || 1);
}

const stat = fs.statSync(pdfPath);
console.log(`OK ${pdfPath} ${(stat.size / 1024).toFixed(1)} KB`);
