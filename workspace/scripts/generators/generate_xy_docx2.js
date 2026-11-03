const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageBreak
} = require("docx");

const mdPath = "C:/Users/EDY/mslearn-ai-agents/新都喜遇言庭宴会中心_小红书+美团运营简案.md";
const mdContent = fs.readFileSync(mdPath, "utf-8");

const BRAND_DARK = "1a1a2e";
const BRAND_ACCENT = "c9a96e";
const BRAND_MID = "4a3728";

function parseTableRow(line) {
  return line.split("|").filter((_, i, arr) => i > 0 && i < arr.length - 1).map(c => c.trim());
}

function createStyledTable(headers, rows) {
  const colWidth = Math.floor(9020 / headers.length);
  const headerCells = headers.map(h => new TableCell({
    children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20, color: "FFFFFF" })], alignment: AlignmentType.CENTER, spacing: { before: 60, after: 60 } })],
    shading: { type: ShadingType.SOLID, color: BRAND_DARK },
    width: { size: colWidth, type: WidthType.DXA },
  }));
  const dataRows = rows.map((row, ri) => {
    const cells = row.map(cell => new TableCell({
      children: [new Paragraph({ text: cell || "", spacing: { before: 40, after: 40 }, alignment: AlignmentType.LEFT, size: 20 })],
      shading: ri % 2 === 0 ? { type: ShadingType.SOLID, color: "faf8f5" } : undefined,
      width: { size: colWidth, type: WidthType.DXA },
    }));
    return new TableRow({ children: cells });
  });
  return new Table({
    rows: [new TableRow({ children: headerCells }), ...dataRows],
    width: { size: 9020, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: "cccccc" },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: "cccccc" },
      left: { style: BorderStyle.SINGLE, size: 1, color: "cccccc" },
      right: { style: BorderStyle.SINGLE, size: 1, color: "cccccc" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: "cccccc" },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: "cccccc" },
    },
  });
}

const children = [];

// Cover
children.push(new Paragraph({ spacing: { before: 2200 } }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "聚光米 UMI", size: 48, bold: true, color: BRAND_DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: "×  新都喜遇言庭宴会中心", size: 36, bold: true, color: BRAND_ACCENT })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60 }, children: [new TextRun({ text: "小红书 + 美团 运营合作简案", size: 28, color: BRAND_MID })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 300, after: 60 }, children: [new TextRun({ text: "汇报对象：宴会酒店 / 婚礼堂负责人", size: 22, color: "6c757d" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: "2026年7月1日", size: 22, color: "6c757d" })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 400 }, children: [new TextRun({ text: "—— 专业 · 独家 · 婚嫁垂类 ——", size: 20, color: "adb5bd", italics: true })] }));
children.push(new Paragraph({ children: [new PageBreak()] }));

// Parse
const lines = mdContent.split("\n");
let inTable = false, tableLines = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (i < 6) continue;

  if (line.startsWith("|") && line.endsWith("|") && !line.match(/^\|[\s\-:]+\|/)) {
    if (!inTable) { inTable = true; tableLines = []; }
    tableLines.push(line);
    if (i + 1 < lines.length && lines[i + 1].startsWith("|") && lines[i + 1].endsWith("|") && !lines[i + 1].match(/^\|[\s\-:]+\|/)) continue;
    if (tableLines.length >= 2) {
      children.push(createStyledTable(parseTableRow(tableLines[0]), tableLines.slice(1).map(parseTableRow)));
      children.push(new Paragraph({ spacing: { after: 200 }, text: "" }));
    }
    inTable = false; tableLines = [];
    continue;
  }
  if (line.match(/^\|[\s\-:]+\|/)) continue;

  // Image placeholder
  if (line.includes("[ 插图：小红书运营产品清单 ]")) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 200, after: 200 },
      border: { top: { style: BorderStyle.DASHED, size: 2, color: "c9a96e" }, bottom: { style: BorderStyle.DASHED, size: 2, color: "c9a96e" }, left: { style: BorderStyle.DASHED, size: 2, color: "c9a96e" }, right: { style: BorderStyle.DASHED, size: 2, color: "c9a96e" } },
      children: [new TextRun({ text: "[ 此处插入：小红书运营产品清单图片 ]", size: 22, color: "999999", italics: true })],
    }));
    continue;
  }

  if (line.startsWith("# ")) {
    children.push(new Paragraph({ spacing: { before: 200, after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BRAND_ACCENT } }, text: "" }));
    children.push(new Paragraph({ heading: "Heading1", text: line.replace(/^#\s*/, ""), spacing: { before: 360, after: 120 } }));
  } else if (line.startsWith("## ")) {
    children.push(new Paragraph({ heading: "Heading2", text: line.replace(/^##\s*/, ""), spacing: { before: 280, after: 120 } }));
  } else if (line.startsWith("### ")) {
    children.push(new Paragraph({ heading: "Heading3", text: line.replace(/^###\s*/, ""), spacing: { before: 200, after: 100 } }));
  } else if (line.match(/^[\s]*\-\s/)) {
    const indent = line.match(/^(\s*)/)[0].length;
    const level = Math.floor(indent / 2);
    const text = line.replace(/^[\s]*\-\s*/, "");
    children.push(new Paragraph({ text, spacing: { after: 100 }, bullet: { level } }));
  } else if (line.trim() === "---") {
    children.push(new Paragraph({ spacing: { before: 160, after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: BRAND_ACCENT } }, text: "" }));
  } else if (line.trim() !== "") {
    if (line.includes("**")) {
      const parts = line.split(/(\*\*.*?\*\*)/g);
      const runs = parts.map(p => p.startsWith("**") && p.endsWith("**") ? new TextRun({ text: p.replace(/^\*\*|\*\*$/g, ""), bold: true, size: 22 }) : new TextRun({ text: p, size: 22 }));
      children.push(new Paragraph({ spacing: { after: 120 }, children: runs }));
    } else if (line.startsWith(">")) {
      children.push(new Paragraph({ children: [new TextRun({ text: line.replace(/^>\s*/, ""), italics: true, color: "6c757d", size: 22 })], spacing: { before: 80, after: 80 } }));
    } else {
      children.push(new Paragraph({ text: line, spacing: { after: 120 } }));
    }
  } else {
    children.push(new Paragraph({ spacing: { after: 60 }, text: "" }));
  }
}

children.push(new Paragraph({ spacing: { before: 300, after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BRAND_ACCENT } }, text: "" }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200 }, children: [new TextRun({ text: "聚光米 UMI  ——  婚嫁垂类线上运营", size: 20, color: "adb5bd", italics: true })] }));

const doc = new Document({
  styles: {
    default: { document: { run: { size: 22, font: "Microsoft YaHei" } }, heading1: { run: { size: 32, bold: true, color: BRAND_DARK, font: "Microsoft YaHei" } }, heading2: { run: { size: 28, bold: true, color: BRAND_MID, font: "Microsoft YaHei" } }, heading3: { run: { size: 24, bold: true, color: BRAND_ACCENT, font: "Microsoft YaHei" } } },
  },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }],
});

const tmpPath = "C:/Users/EDY/mslearn-ai-agents/_tmp_xy.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(tmpPath, buffer);
  console.log("OK:", tmpPath, (buffer.length / 1024).toFixed(1), "KB");

  // Overwrite target
  const target = "C:/Users/EDY/mslearn-ai-agents/新都喜遇言庭宴会中心_小红书+美团运营简案.docx";
  try { fs.unlinkSync(target); } catch(e) {}
  fs.copyFileSync(tmpPath, target);
  fs.unlinkSync(tmpPath);
  console.log("OK:", target);
}).catch(err => console.error("ERR:", err));
