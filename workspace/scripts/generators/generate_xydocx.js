const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType
} = require("docx");

const mdPath = "C:/Users/EDY/mslearn-ai-agents/新都喜遇言庭宴会中心_小红书+美团运营简案.md";
const mdContent = fs.readFileSync(mdPath, "utf-8");

const BRAND_RED = "9e1f34";
const BRAND_GOLD = "cda349";
const BRAND_GREEN = "2f6f5e";
const BRAND_PURPLE = "6b3f6d";
const LIGHT_BG = "f7f4f2";

function createHeading(text, level) {
  return new Paragraph({
    heading: level <= 5 ? `Heading${level}` : "Heading5",
    text: text.replace(/^#+\s*/, ""),
    spacing: { before: level === 1 ? 240 : 180, after: 120 },
  });
}

function createBody(text, opts = {}) {
  return new Paragraph({
    text,
    spacing: { after: opts.after || 100 },
    bullet: opts.bullet ? { level: 0 } : undefined,
    alignment: opts.alignment || AlignmentType.LEFT,
  });
}

function parseTableRow(line) {
  return line
    .split("|")
    .filter((_, i, arr) => i > 0 && i < arr.length - 1)
    .map((c) => c.trim());
}

function createTable(headers, rows) {
  const width = Math.floor(9020 / headers.length);
  const headerCells = headers.map((h) =>
    new TableCell({
      children: [
        new Paragraph({
          children: [new TextRun({ text: h, bold: true, color: "FFFFFF", size: 22 })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 50, after: 50 },
        }),
      ],
      shading: { type: ShadingType.SOLID, color: BRAND_RED },
      width: { size: width, type: WidthType.DXA },
    })
  );

  const bodyRows = rows.map((row, idx) =>
    new TableRow({
      children: row.map((cell) =>
        new TableCell({
          children: [
            new Paragraph({
              text: cell || "",
              spacing: { before: 40, after: 40 },
            }),
          ],
          shading: idx % 2 === 0 ? { type: ShadingType.SOLID, color: "fbf8f6" } : undefined,
          width: { size: width, type: WidthType.DXA },
        })
      ),
    })
  );

  return new Table({
    rows: [new TableRow({ children: headerCells }), ...bodyRows],
    width: { size: 9020, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: "d9d9d9" },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: "d9d9d9" },
      left: { style: BorderStyle.SINGLE, size: 1, color: "d9d9d9" },
      right: { style: BorderStyle.SINGLE, size: 1, color: "d9d9d9" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: "d9d9d9" },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: "d9d9d9" },
    },
  });
}

function divider(color = BRAND_GOLD) {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color } },
  });
}

const children = [];

children.push(
  new Paragraph({
    shading: { type: ShadingType.SOLID, color: BRAND_RED },
    spacing: { before: 160, after: 220 },
    children: [
      new TextRun({ text: "聚光米 UMI", bold: true, size: 38, color: "FFFFFF" }),
      new TextRun({ text: "  |  新都喜遇言庭宴会中心", bold: true, size: 38, color: "FFFFFF" }),
    ],
  })
);

children.push(
  new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({ text: "小红书 + 美团运营合作简案", bold: true, size: 32, color: BRAND_RED })],
  })
);
children.push(createBody("汇报对象：宴会酒店 / 婚礼堂负责人"));
children.push(createBody("方案日期：2026年7月1日"));
children.push(createBody("合作目标：提升品牌曝光、增加线上咨询、提高婚宴到店转化", { after: 140 }));

const lines = mdContent.split("\n");
let tableLines = [];
let inTable = false;

for (const rawLine of lines) {
  const line = rawLine.trimEnd();

  if (
    line.startsWith("|") &&
    line.endsWith("|") &&
    !line.match(/^\|[\s\-:]+\|/)
  ) {
    inTable = true;
    tableLines.push(line);
    continue;
  }

  if (inTable && line.match(/^\|[\s\-:]+\|/)) {
    continue;
  }

  if (inTable && (!line.startsWith("|") || !line.endsWith("|"))) {
    const headers = parseTableRow(tableLines[0]);
    const rows = tableLines.slice(1).map(parseTableRow);
    children.push(createTable(headers, rows));
    children.push(new Paragraph({ spacing: { after: 120 } }));
    tableLines = [];
    inTable = false;
  }

  if (!line || line.startsWith("> **汇报对象**") || line.startsWith("> **方案日期**") || line.startsWith("> **合作目标**")) {
    continue;
  }

  if (line === "---") {
    children.push(divider());
  } else if (line.startsWith("# ")) {
    continue;
  } else if (line.startsWith("## ")) {
    children.push(createHeading(line, 2));
  } else if (line.startsWith("### ")) {
    children.push(createHeading(line, 3));
  } else if (line.match(/^- /)) {
    children.push(createBody(line.replace(/^- /, ""), { bullet: true }));
  } else {
    const parts = line.split(/(\*\*.*?\*\*)/g).filter(Boolean);
    const runs = parts.map((part) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return new TextRun({
          text: part.replace(/^\*\*|\*\*$/g, ""),
          bold: true,
          color: BRAND_GREEN,
        });
      }
      return new TextRun({ text: part });
    });
    children.push(new Paragraph({ children: runs, spacing: { after: 100 } }));
  }
}

if (inTable && tableLines.length) {
  const headers = parseTableRow(tableLines[0]);
  const rows = tableLines.slice(1).map(parseTableRow);
  children.push(createTable(headers, rows));
}

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Microsoft YaHei", size: 22 },
        paragraph: { spacing: { after: 80 } },
      },
      heading2: {
        run: { font: "Microsoft YaHei", size: 28, bold: true, color: BRAND_RED },
      },
      heading3: {
        run: { font: "Microsoft YaHei", size: 24, bold: true, color: BRAND_PURPLE },
      },
    },
  },
  sections: [
    {
      properties: {
        page: {
          margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 },
        },
      },
      children,
    },
  ],
});

Packer.toBuffer(doc)
  .then((buffer) => {
    const outputPath = "C:/Users/EDY/mslearn-ai-agents/新都喜遇言庭宴会中心_小红书+美团运营简案.docx";
    fs.writeFileSync(outputPath, buffer);
    console.log(`DOCX saved: ${outputPath}`);
    console.log(`Size: ${(buffer.length / 1024).toFixed(1)} KB`);
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
