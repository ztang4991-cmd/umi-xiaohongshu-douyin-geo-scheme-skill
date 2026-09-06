const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageBreak, NumberProperties
} = require("docx");

const mdPath = "C:/Users/EDY/mslearn-ai-agents/东莞美集婚纱摄影_小红书运营方案.md";
const mdContent = fs.readFileSync(mdPath, "utf-8");

// ── Helpers ──────────────────────────────────────────────

function createHeading(text, level) {
  const sizes = { 1: 36, 2: 30, 3: 26, 4: 24, 5: 22 };
  const colors = { 1: "1a1a2e", 2: "16213e", 3: "0f3460", 4: "e63946", 5: "333333" };
  return new Paragraph({
    heading: level <= 5 ? `Heading${level}` : "Heading5",
    text: text.replace(/^#+\s*/, ""),
    spacing: { before: level === 1 ? 400 : level === 2 ? 300 : 200, after: 150 },
  });
}

function createBodyText(text) {
  if (!text || text.trim() === "") {
    return new Paragraph({ spacing: { after: 100 }, text: "" });
  }
  return new Paragraph({
    text: text,
    spacing: { after: 120 },
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
    shading: { type: ShadingType.SOLID, color: "1a1a2e" },
    width: { size: colWidth, type: WidthType.DXA },
  }));

  const dataRows = rows.map((row, ri) => {
    const cells = row.map(cell => new TableCell({
      children: [new Paragraph({
        text: cell || "",
        spacing: { before: 40, after: 40 },
        size: 20,
      })],
      shading: ri % 2 === 0 ? { type: ShadingType.SOLID, color: "f8f9fa" } : undefined,
      width: { size: colWidth, type: WidthType.DXA },
    }));
    return new TableRow({ children: cells });
  });

  return new Table({
    rows: [new TableRow({ children: headerCells }), ...dataRows],
    width: { size: 9020, type: WidthType.DXA },
  });
}

function addDivider() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "e63946" } },
  });
}

// ── Build document ───────────────────────────────────────

const children = [];

// Cover page
children.push(new Paragraph({ spacing: { before: 2200 } }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "东莞美集婚纱摄影", size: 56, bold: true, color: "1a1a2e" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: "小红书运营方案", size: 44, bold: true, color: "e63946" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 300 },
  children: [new TextRun({ text: "法式轻奢，记录真实的你", size: 28, color: "6c757d" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "GEO + 内容 + 投放  三合一增长策略", size: 28, color: "6c757d" })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 600 },
  children: [new TextRun({ text: "方案版本：V1.0    制定日期：2026年6月24日", size: 22, color: "999999" })],
}));

children.push(new Paragraph({ children: [new PageBreak()] }));

// ── Parse markdown ───────────────────────────────────────

const lines = mdContent.split("\n");
let inTable = false;
let tableLines = [];

// collect second-pass table: consecutive |…| lines
const tableBlocks = [];
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.startsWith("|") && line.endsWith("|") && !line.match(/^\|[\s\-:]+\|/)) {
    if (!inTable) { inTable = true; tableLines = []; }
    tableLines.push(line);
  } else {
    if (inTable) {
      if (tableLines.length >= 2) tableBlocks.push({ start: i - tableLines.length, end: i - 1, lines: [...tableLines] });
      inTable = false;
      tableLines = [];
    }
  }
}
if (inTable && tableLines.length >= 2) {
  tableBlocks.push({ start: lines.length - tableLines.length, end: lines.length - 1, lines: [...tableLines] });
}
const tableStartLines = new Set(tableBlocks.map(b => b.start));
const tableEndLines = new Set(tableBlocks.map(b => b.end));

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // skip lines belonging to tables (processed when block starts)
  if (tableStartLines.has(i)) {
    const block = tableBlocks.find(b => b.start === i);
    const headers = parseTableRow(block.lines[0]);
    const rows = block.lines.slice(1).map(parseTableRow);
    children.push(createStyledTable(headers, rows));
    children.push(new Paragraph({ spacing: { after: 200 }, text: "" }));
    i = block.end;
    continue;
  }
  if (tableEndLines.has(i) && !tableStartLines.has(i)) continue;

  // skip separator lines inside tables
  if (line.match(/^\|[\s\-:]+\|/)) continue;

  // headings
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
  // bullet items (including ✅)
  else if (line.match(/^[\s]*[-*✅⚡⭐️✔️☑️✓]\s/)) {
    const text = line.replace(/^[\s]*[-*✅⚡⭐️✔️☑️✓]\s*/, "");
    if (text.includes("**")) {
      const parts = text.split(/(\*\*.*?\*\*)/g);
      const runs = parts.map(p => {
        if (p.startsWith("**") && p.endsWith("**")) {
          return new TextRun({ text: p.replace(/^\*\*|\*\*$/g, ""), bold: true, size: 22 });
        }
        return new TextRun({ text: p, size: 22 });
      });
      children.push(new Paragraph({
        spacing: { after: 100 },
        bullet: { level: 0 },
        children: runs,
      }));
    } else {
      children.push(new Paragraph({
        text,
        spacing: { after: 100 },
        bullet: { level: 0 },
      }));
    }
  }
  // numbered list items
  else if (line.match(/^\d+\.\s/)) {
    const text = line.replace(/^\d+\.\s*/, "");
    if (text.includes("**")) {
      const parts = text.split(/(\*\*.*?\*\*)/g);
      const runs = parts.map(p => {
        if (p.startsWith("**") && p.endsWith("**")) {
          return new TextRun({ text: p.replace(/^\*\*|\*\*$/g, ""), bold: true, size: 22 });
        }
        return new TextRun({ text: p, size: 22 });
      });
      children.push(new Paragraph({
        spacing: { after: 100 },
        numbering: { reference: "numberedList", level: 0 },
        children: runs,
      }));
    } else {
      children.push(new Paragraph({
        text,
        spacing: { after: 100 },
        numbering: { reference: "numberedList", level: 0 },
      }));
    }
  }
  // dividers
  else if (line.trim() === "---") {
    children.push(addDivider());
  }
  // regular text (possibly with bold)
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
      children.push(createBodyText(line));
    }
  } else {
    children.push(new Paragraph({ spacing: { after: 60 }, text: "" }));
  }
}

// ── Create Document ──────────────────────────────────────

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { size: 22, font: "Microsoft YaHei" },
      },
      heading1: { run: { size: 36, bold: true, color: "1a1a2e", font: "Microsoft YaHei" } },
      heading2: { run: { size: 30, bold: true, color: "16213e", font: "Microsoft YaHei" } },
      heading3: { run: { size: 26, bold: true, color: "0f3460", font: "Microsoft YaHei" } },
      heading4: { run: { size: 24, bold: true, color: "e63946", font: "Microsoft YaHei" } },
    },
  },
  numbering: {
    config: [
      {
        reference: "numberedList",
        levels: [{
          level: 0,
          format: "decimal",
          text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
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

// ── Save ─────────────────────────────────────────────────

Packer.toBuffer(doc).then(buffer => {
  const outputPath = "C:/Users/EDY/mslearn-ai-agents/东莞美集婚纱摄影_小红书运营方案.docx";
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ DOCX saved: ${outputPath}`);
  console.log(`   Size: ${(buffer.length / 1024).toFixed(1)} KB`);
  console.log(`   Paragraphs: ${children.length}`);
}).catch(err => {
  console.error("Error:", err);
});