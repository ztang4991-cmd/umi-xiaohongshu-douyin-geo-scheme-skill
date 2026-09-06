const fs = require("fs");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  AlignmentType,
  BorderStyle,
  WidthType,
  ShadingType,
  PageBreak,
} = require("docx");

const base = "C:/Users/EDY/mslearn-ai-agents";
const mdPath = `${base}/新都喜遇言庭宴会中心_小红书美团落地运营方案.md`;
const outPath = `${base}/新都喜遇言庭宴会中心_小红书美团落地运营方案.docx`;

const md = fs.readFileSync(mdPath, "utf8");

const COLORS = {
  dark: "222831",
  accent: "B48A4A",
  muted: "6B7280",
  light: "F7F3EC",
  border: "D7D0C4",
};

function cleanInline(text) {
  return text.replace(/\*\*/g, "").trim();
}

function inlineRuns(text, opts = {}) {
  const runs = [];
  const parts = text.split(/(\*\*.*?\*\*)/g);
  for (const part of parts) {
    if (!part) continue;
    const bold = part.startsWith("**") && part.endsWith("**");
    runs.push(
      new TextRun({
        text: bold ? part.slice(2, -2) : part,
        bold: bold || opts.bold,
        size: opts.size || 21,
        color: opts.color || COLORS.dark,
        italics: opts.italics,
        font: "Microsoft YaHei",
      })
    );
  }
  return runs;
}

function para(text = "", options = {}) {
  return new Paragraph({
    children: inlineRuns(text, options),
    alignment: options.alignment || AlignmentType.LEFT,
    spacing: {
      before: options.before || 0,
      after: options.after ?? 120,
      line: options.line || 320,
    },
    bullet: options.bullet,
    indent: options.indent,
    border: options.border,
    shading: options.shading,
  });
}

function parseRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cleanInline(cell));
}

function isSeparator(line) {
  return /^\|\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?$/.test(line.trim());
}

function tableFrom(lines) {
  const headers = parseRow(lines[0]);
  const rows = lines.slice(2).map(parseRow);
  const colWidth = Math.floor(9020 / headers.length);
  const headerCells = headers.map(
    (h) =>
      new TableCell({
        children: [
          new Paragraph({
            children: [
              new TextRun({
                text: h,
                bold: true,
                size: 19,
                color: "FFFFFF",
                font: "Microsoft YaHei",
              }),
            ],
            alignment: AlignmentType.CENTER,
            spacing: { before: 90, after: 90 },
          }),
        ],
        shading: { type: ShadingType.SOLID, color: COLORS.dark },
        width: { size: colWidth, type: WidthType.DXA },
      })
  );

  const bodyRows = rows.map((row, idx) => {
    const cells = headers.map((_, ci) => {
      const text = row[ci] || "";
      return new TableCell({
        children: [
          new Paragraph({
            children: inlineRuns(text, { size: 18 }),
            spacing: { before: 70, after: 70, line: 285 },
          }),
        ],
        shading: idx % 2 === 0 ? { type: ShadingType.SOLID, color: "FCFAF7" } : undefined,
        width: { size: colWidth, type: WidthType.DXA },
      });
    });
    return new TableRow({ children: cells });
  });

  return new Table({
    rows: [new TableRow({ children: headerCells }), ...bodyRows],
    width: { size: 9020, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border },
      left: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border },
      right: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: COLORS.border },
    },
  });
}

const children = [];

children.push(new Paragraph({ spacing: { before: 1800, after: 180 } }));
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({ text: "聚光米 UMI", bold: true, size: 44, color: COLORS.dark, font: "Microsoft YaHei" }),
    ],
  })
);
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 140, after: 80 },
    children: [
      new TextRun({
        text: "× 新都喜遇言庭宴会中心",
        bold: true,
        size: 32,
        color: COLORS.accent,
        font: "Microsoft YaHei",
      }),
    ],
  })
);
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 220, after: 60 },
    children: [
      new TextRun({
        text: "小红书 + 美团落地运营方案",
        size: 30,
        color: COLORS.dark,
        font: "Microsoft YaHei",
      }),
    ],
  })
);
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 280, after: 60 },
    children: [
      new TextRun({
        text: "明日到店沟通版  |  2026年7月3日",
        size: 21,
        color: COLORS.muted,
        font: "Microsoft YaHei",
      }),
    ],
  })
);
children.push(new Paragraph({ children: [new PageBreak()] }));

const lines = md.split(/\r?\n/);
let i = 0;
while (i < lines.length) {
  const line = lines[i];

  if (i < 2) {
    i += 1;
    continue;
  }

  if (line.trim().startsWith("|")) {
    const tableLines = [];
    while (i < lines.length && lines[i].trim().startsWith("|")) {
      tableLines.push(lines[i]);
      i += 1;
    }
    if (tableLines.length >= 3 && isSeparator(tableLines[1])) {
      children.push(tableFrom(tableLines));
      children.push(para("", { after: 160 }));
    }
    continue;
  }

  if (line.startsWith("## ")) {
    children.push(
      new Paragraph({
        children: [
          new TextRun({
            text: line.replace(/^##\s*/, ""),
            bold: true,
            size: 28,
            color: COLORS.dark,
            font: "Microsoft YaHei",
          }),
        ],
        spacing: { before: 320, after: 130 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: COLORS.accent } },
      })
    );
  } else if (line.startsWith("### ")) {
    children.push(
      new Paragraph({
        children: [
          new TextRun({
            text: line.replace(/^###\s*/, ""),
            bold: true,
            size: 23,
            color: COLORS.accent,
            font: "Microsoft YaHei",
          }),
        ],
        spacing: { before: 220, after: 100 },
      })
    );
  } else if (/^\s*-\s+/.test(line)) {
    children.push(
      para(line.replace(/^\s*-\s+/, ""), {
        bullet: { level: 0 },
        after: 80,
        indent: { left: 360 },
      })
    );
  } else if (line.trim() === "---") {
    children.push(para("", { after: 160 }));
  } else if (line.trim() === "") {
    children.push(para("", { after: 40 }));
  } else if (!line.startsWith("# ")) {
    const isMeta = /^(汇报对象|方案日期|方案定位)/.test(line);
    children.push(
      para(line, {
        size: isMeta ? 20 : 21,
        color: isMeta ? COLORS.muted : COLORS.dark,
        after: isMeta ? 70 : 120,
      })
    );
  }
  i += 1;
}

children.push(para("", { before: 260, border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: COLORS.accent } } }));
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 180 },
    children: [
      new TextRun({
        text: "聚光米 UMI  |  婚嫁垂类线上运营",
        size: 18,
        color: COLORS.muted,
        font: "Microsoft YaHei",
      }),
    ],
  })
);

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Microsoft YaHei", size: 21, color: COLORS.dark },
        paragraph: { spacing: { line: 320 } },
      },
    },
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1180, bottom: 1180, left: 1180, right: 1180 },
        },
      },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.log(`OK ${outPath} ${(buffer.length / 1024).toFixed(1)} KB`);
});
