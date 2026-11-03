const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageBreak
} = require('docx');

// Read markdown file
const mdPath = 'C:/Users/EDY/mslearn-ai-agents/玛瑞莎摄影_GEO产品方案_完整版.md';
const mdContent = fs.readFileSync(mdPath, 'utf-8');

// Helper functions (same as before)
function createHeading(text, level) {
  return new Paragraph({
    heading: level <= 5 ? `Heading${level}` : 'Heading5',
    text: text.replace(/^#+\s*/, ''),
    spacing: { before: level === 1 ? 400 : level === 2 ? 300 : 200, after: 150 },
  });
}

function createBodyText(text) {
  if (!text || text.trim() === '') {
    return new Paragraph({ spacing: { after: 100 }, text: '' });
  }
  return new Paragraph({
    text: text,
    spacing: { after: 120 },
  });
}

function parseTableRow(line) {
  const cells = line.split('|').filter((_, i, arr) => i > 0 && i < arr.length - 1).map(c => c.trim());
  return cells;
}

function createStyledTable(headers, rows) {
  const headerCells = headers.map(h => new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text: h, bold: true, size: 20, color: 'FFFFFF' })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 60, after: 60 },
    })],
    shading: { type: ShadingType.SOLID, color: '1a1a2e' },
    width: { size: Math.floor(9020 / headers.length), type: WidthType.DXA },
  }));

  const dataRows = rows.map((row, ri) => {
    const cells = row.map(cell => new TableCell({
      children: [new Paragraph({
        text: cell || '',
        spacing: { before: 40, after: 40 },
        size: 20,
      })],
      shading: ri % 2 === 0 ? { type: ShadingType.SOLID, color: 'f8f9fa' } : undefined,
      width: { size: Math.floor(9020 / headers.length), type: WidthType.DXA },
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
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'e63946' } },
  });
}

// Build document
const children = [];

// Cover page
children.push(new Paragraph({ spacing: { before: 2500 } }));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: '成都玛瑞莎孕婴摄影工作室', size: 56, bold: true, color: '1a1a2e' })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: 'GEO生成式引擎优化产品方案', size: 44, bold: true, color: 'e63946' })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 300 },
  children: [new TextRun({ text: '让AI搜索主动推荐玛瑞莎', size: 28, color: '6c757d' })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: '抢占"成都孕照/新生儿摄影"第一认知', size: 28, color: '6c757d' })],
}));

children.push(new Paragraph({ children: [new PageBreak()] }));

// Parse markdown
const lines = mdContent.split('\n');
let inTable = false;
let tableLines = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  if (i < 10) continue;

  // Table handling
  if (line.startsWith('|') && line.endsWith('|') && !line.match(/^\|[\s\-:]+\|/)) {
    if (!inTable) {
      inTable = true;
      tableLines = [];
    }
    tableLines.push(line);
    if (i + 1 < lines.length && lines[i + 1].startsWith('|') && lines[i + 1].endsWith('|') && !lines[i + 1].match(/^\|[\s\-:]+\|/)) {
      continue;
    }
    if (tableLines.length >= 2) {
      const headers = parseTableRow(tableLines[0]);
      const rows = tableLines.slice(1).map(parseTableRow);
      children.push(createStyledTable(headers, rows));
      children.push(new Paragraph({ spacing: { after: 200 }, text: '' }));
    }
    inTable = false;
    tableLines = [];
    continue;
  }

  if (line.match(/^\|[\s\-:]+\|/)) continue;

  if (line.startsWith('# ')) {
    children.push(addDivider());
    children.push(createHeading(line, 1));
  } else if (line.startsWith('## ')) {
    children.push(createHeading(line, 2));
  } else if (line.startsWith('### ')) {
    children.push(createHeading(line, 3));
  } else if (line.startsWith('#### ')) {
    children.push(createHeading(line, 4));
  } else if (line.match(/^[\s]*[-*✅❌✓⚠️]\s/)) {
    const text = line.replace(/^[\s]*[-*✅❌✓⚠️]\s*/, '');
    children.push(new Paragraph({
      text,
      spacing: { after: 100 },
      bullet: { level: 0 },
    }));
  } else if (line.trim() === '---') {
    children.push(addDivider());
  } else if (line.trim() !== '') {
    if (line.includes('**')) {
      const parts = line.split(/(\*\*.*?\*\*)/g);
      const runs = parts.map(p => {
        if (p.startsWith('**') && p.endsWith('**')) {
          return new TextRun({ text: p.replace(/^\*\*|\*\*$/g, ''), bold: true, size: 22 });
        }
        return new TextRun({ text: p, size: 22 });
      });
      children.push(new Paragraph({ spacing: { after: 120 }, children: runs }));
    } else {
      children.push(createBodyText(line));
    }
  } else {
    children.push(new Paragraph({ spacing: { after: 60 }, text: '' }));
  }
}

// Create document
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { size: 22, font: 'Microsoft YaHei' },
      },
      heading1: { run: { size: 36, bold: true, color: '1a1a2e', font: 'Microsoft YaHei' } },
      heading2: { run: { size: 30, bold: true, color: '16213e', font: 'Microsoft YaHei' } },
      heading3: { run: { size: 26, bold: true, color: '0f3460', font: 'Microsoft YaHei' } },
      heading4: { run: { size: 24, bold: true, color: 'e63946', font: 'Microsoft YaHei' } },
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

// Save
Packer.toBuffer(doc).then(buffer => {
  const outputPath = 'C:/Users/EDY/mslearn-ai-agents/玛瑞莎摄影_GEO产品方案.docx';
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ DOCX saved: ${outputPath}`);
  console.log(`   Size: ${(buffer.length / 1024).toFixed(1)} KB`);
}).catch(err => {
  console.error('Error:', err);
});
