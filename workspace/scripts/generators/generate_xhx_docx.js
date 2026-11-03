const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageBreak
} = require("docx");

const mdPath = "C:/Users/EDY/mslearn-ai-agents/羲和轩·拾光管家_GEO+小红书产品方案.md";
const mdContent = fs.readFileSync(mdPath, "utf-8");

// Brand colors for 羲和轩·拾光管家
const BRAND_DARK = "1a3a4a";
const BRAND_ACCENT = "00a896";
const BRAND_MID = "2d6a4f";

function createHeading(text, level) {
  return new Paragraph({
    heading: level <= 5 ? `Heading${level}` : "Heading5",
    text: text.replace(/^#+\s*/, ""),
    spacing: { before: level === 1 ? 400 : level === 2 ? 300 : 200, after: 150 },
  });
}

function parseTableRow(line) {
  return line.split("|").filter((_, i, arr) => i > 0 && i < arr.length - 1).map(c => c.trim());
}

function createStyledTable(headers, rows) {
  const colWidth = Math.floor(9020 / headers.length);
  const headerCells = headers.map(h => new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text: h, bold: true, size: 20, color: "FFFFFF" })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 60, after: 60 },
    })],
    shading: { type: ShadingType.SOLID, color: BRAND_DARK },
    width: { size: colWidth, type: WidthType.DXA },
  }));

  const dataRows = rows.map((row, ri) => {
    const cells = row.map(cell => new TableCell({
      children: [new Paragraph({
        text: cell || "",
        spacing: { before: 40, after: 40 },
        alignment: AlignmentType.LEFT,
        size: 20,
      })],
      shading: ri % 2 === 0 ? { type: ShadingType.SOLID, color: "f0f7f4" } : undefined,
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

function addDivider() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BRAND_ACCENT } },
  });
}

const children = [];

// Cover page
children.push(new Paragraph({ spacing: { before: 2500 } }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "羲和轩·拾光管家", size: 56, bold: true, color: BRAND_DARK })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: "GEO+小红书 线上获客解决方案", size: 44, bold: true, color: BRAND_ACCENT })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 300, after: 80 },
  children: [new TextRun({ text: "方案日期：2026年6月29日", size: 24, color: "6c757d" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 80 },
  children: [new TextRun({ text: "服务区域：成都市及周边核心城区", size: 24, color: "6c757d" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 80 },
  children: [new TextRun({ text: "核心目标：降低获客成本 · 提升品牌曝光 · 建立线上私域流量池", size: 24, color: "6c757d" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 600 },
  children: [new TextRun({ text: "—— 专业 · 落地 · 可量化 ——", size: 20, color: "adb5bd", italics: true })],
}));

children.push(new Paragraph({ children: [new PageBreak()] }));

// Parse markdown
const lines = mdContent.split("\n");
let inTable = false;
let tableLines = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // Skip cover content (first 10 lines of markdown)
  if (i < 10) continue;

  // Table handling
  if (line.startsWith("|") && line.endsWith("|") && !line.match(/^\|[\s\-:]+\|/)) {
    if (!inTable) {
      inTable = true;
      tableLines = [];
    }
    tableLines.push(line);
    if (i + 1 < lines.length && lines[i + 1].startsWith("|") && lines[i + 1].endsWith("|") && !lines[i + 1].match(/^\|[\s\-:]+\|/)) {
      continue;
    }
    if (tableLines.length >= 2) {
      const headers = parseTableRow(tableLines[0]);
      const rows = tableLines.slice(1).map(parseTableRow);
      children.push(createStyledTable(headers, rows));
      children.push(new Paragraph({ spacing: { after: 200 }, text: "" }));
    }
    inTable = false;
    tableLines = [];
    continue;
  }

  if (line.match(/^\|[\s\-:]+\|/)) continue;

  // Headings
  if (line.startsWith("# ")) {
    children.push(addDivider());
    children.push(createHeading(line, 1));
  } else if (line.startsWith("## ")) {
    children.push(createHeading(line, 2));
  } else if (line.startsWith("### ")) {
    children.push(createHeading(line, 3));
  } else if (line.startsWith("#### ")) {
    children.push(createHeading(line, 4));
  }
  // Bullet points
  else if (line.match(/^[\s]*[-*✅❌]\s/)) {
    const indent = line.match(/^(\s*)/)[0].length;
    const level = Math.floor(indent / 2);
    const text = line.replace(/^[\s]*[-*✅❌]\s*/, "");
    children.push(new Paragraph({
      text,
      spacing: { after: 100 },
      bullet: { level },
    }));
  }
  // Separator
  else if (line.trim() === "---") {
    children.push(addDivider());
  }
  // Regular text
  else if (line.trim() !== "") {
    if (line.includes("**")) {
      const parts = line.split(/(\*\*.*?\*\*)/g);
      const runs = parts.map(p => {
        if (p.startsWith("**") && p.endsWith("**")) {
          return new TextRun({ text: p.replace(/^\*\*|\*\*$/g, ""), bold: true, size: 22 });
        }
        return new TextRun({ text: p, size: 22 });
      });
      children.push(new Paragraph({ spacing: { after: 120 }, children: runs }));
    } else {
      children.push(new Paragraph({
        text: line,
        spacing: { after: 120 },
        alignment: AlignmentType.LEFT,
      }));
    }
  } else {
    children.push(new Paragraph({ spacing: { after: 60 }, text: "" }));
  }
}

// Final page
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({ spacing: { before: 2000 } }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "—— 方案结束 ——", size: 28, color: "6c757d", italics: true })],
}));

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { size: 22, font: "Microsoft YaHei" },
      },
      heading1: { run: { size: 36, bold: true, color: BRAND_DARK, font: "Microsoft YaHei" } },
      heading2: { run: { size: 30, bold: true, color: BRAND_MID, font: "Microsoft YaHei" } },
      heading3: { run: { size: 26, bold: true, color: "2d6a4f", font: "Microsoft YaHei" } },
      heading4: { run: { size: 24, bold: true, color: BRAND_ACCENT, font: "Microsoft YaHei" } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  const outputPath = "C:/Users/EDY/mslearn-ai-agents/羲和轩·拾光管家_GEO+小红书产品方案.docx";
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ DOCX saved: ${outputPath}`);
  console.log(`   Size: ${(buffer.length / 1024).toFixed(1)} KB`);
}).catch(err => {
  console.error("Error:", err);
});
