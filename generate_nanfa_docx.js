const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageBreak, convertInchesToTwip
} = require('docx');

// Read markdown file
const mdPath = 'C:/Users/EDY/mslearn-ai-agents/那年花开南法庄园_GEO+小红书+抖音运营方案_初稿.md';
const mdContent = fs.readFileSync(mdPath, 'utf-8');

// Helper functions
function createHeading(text, level) {
  return new Paragraph({
    heading: level <= 5 ? `Heading${level}` : 'Heading5',
    text: text.replace(/^#+\s*/, ''),
    spacing: { before: level === 1 ? 400 : level === 2 ? 300 : 200, after: 150 },
  });
}

function createBodyText(text, opts = {}) {
  if (!text || text.trim() === '') {
    return new Paragraph({ spacing: { after: 100 }, text: '' });
  }
  return new Paragraph({
    text: text,
    spacing: { after: opts.after || 120 },
    alignment: opts.alignment || AlignmentType.LEFT,
    bullet: opts.bullet ? { level: opts.bulletLevel || 0 } : undefined,
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
    shading: { type: ShadingType.SOLID, color: '8b4789' },
    width: { size: Math.floor(9020 / headers.length), type: WidthType.DXA },
  }));

  const dataRows = rows.map((row, ri) => {
    const cells = row.map(cell => new TableCell({
      children: [new Paragraph({
        text: cell || '',
        spacing: { before: 40, after: 40 },
        alignment: AlignmentType.LEFT,
        size: 20,
      })],
      shading: ri % 2 === 0 ? { type: ShadingType.SOLID, color: 'f5f0f5' } : undefined,
      width: { size: Math.floor(9020 / headers.length), type: WidthType.DXA },
    }));
    return new TableRow({ children: cells });
  });

  return new Table({
    rows: [new TableRow({ children: headerCells }), ...dataRows],
    width: { size: 9020, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: 'cccccc' },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: 'cccccc' },
      left: { style: BorderStyle.SINGLE, size: 1, color: 'cccccc' },
      right: { style: BorderStyle.SINGLE, size: 1, color: 'cccccc' },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: 'cccccc' },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: 'cccccc' },
    },
  });
}

function addDivider() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '8b4789' } },
  });
}

// Parse markdown content
const lines = mdContent.split('\n');
const sections = [];
let currentSection = [];
let inTable = false;
let tableHeaders = [];
let tableRows = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // Headings
  if (line.startsWith('#')) {
    if (inTable && tableHeaders.length > 0) {
      currentSection.push(createStyledTable(tableHeaders, tableRows));
      tableHeaders = [];
      tableRows = [];
      inTable = false;
    }
    const level = line.match(/^#+/)[0].length;
    currentSection.push(createHeading(line, level));
    if (level === 1 || level === 2) {
      currentSection.push(addDivider());
    }
  }
  // Table detection
  else if (line.includes('|') && line.trim().startsWith('|')) {
    if (!inTable) {
      tableHeaders = parseTableRow(line);
      inTable = true;
    } else if (line.includes('---')) {
      // Skip separator line
      continue;
    } else {
      tableRows.push(parseTableRow(line));
    }
  }
  // End of table
  else if (inTable && !line.includes('|')) {
    if (tableHeaders.length > 0) {
      currentSection.push(createStyledTable(tableHeaders, tableRows));
      tableHeaders = [];
      tableRows = [];
    }
    inTable = false;
    if (line.trim()) {
      currentSection.push(createBodyText(line));
    }
  }
  // Blockquote
  else if (line.startsWith('>')) {
    currentSection.push(new Paragraph({
      children: [new TextRun({ text: line.replace(/^>\s*/, ''), italics: true, color: '666666' })],
      spacing: { before: 100, after: 100, left: 400 },
      border: { left: { style: BorderStyle.SINGLE, size: 12, color: '8b4789' } },
    }));
  }
  // List items
  else if (line.match(/^[\-\*]\s/) || line.match(/^\d+\.\s/)) {
    const isBullet = line.match(/^[\-\*]\s/);
    const text = line.replace(/^[\-\*\d]+\.\s*/, '');
    currentSection.push(createBodyText(text, { bullet: true, bulletLevel: 0 }));
  }
  // Checkbox items
  else if (line.match(/^- \[[ x]\]/)) {
    const checked = line.includes('[x]');
    const text = line.replace(/^- \[[ x]\]\s*/, '');
    currentSection.push(new Paragraph({
      children: [
        new TextRun({ text: checked ? '☑ ' : '☐ ', size: 24 }),
        new TextRun({ text: text })
      ],
      spacing: { after: 80 },
    }));
  }
  // Horizontal rule
  else if (line.match(/^---+$/)) {
    currentSection.push(addDivider());
  }
  // Regular text
  else if (line.trim()) {
    // Handle bold/checkmarks in text
    let children = [];
    const boldPattern = /\*\*(.+?)\*\*/g;
    const checkPattern = /[✅❌]/g;

    let lastIndex = 0;
    let match;
    const combinedPattern = /(\*\*(.+?)\*\*|[✅❌])/g;

    while ((match = combinedPattern.exec(line)) !== null) {
      if (match.index > lastIndex) {
        children.push(new TextRun({ text: line.substring(lastIndex, match.index) }));
      }
      if (match[0].startsWith('**')) {
        children.push(new TextRun({ text: match[2], bold: true }));
      } else {
        children.push(new TextRun({ text: match[0], size: 24 }));
      }
      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < line.length) {
      children.push(new TextRun({ text: line.substring(lastIndex) }));
    }

    if (children.length > 0) {
      currentSection.push(new Paragraph({
        children: children,
        spacing: { after: 120 },
      }));
    } else {
      currentSection.push(createBodyText(line));
    }
  }
  // Empty line
  else {
    currentSection.push(new Paragraph({ spacing: { after: 100 }, text: '' }));
  }
}

// Handle last table if exists
if (inTable && tableHeaders.length > 0) {
  currentSection.push(createStyledTable(tableHeaders, tableRows));
}

// Create document
const doc = new Document({
  sections: [{
    properties: {
      page: {
        margin: {
          top: convertInchesToTwip(1),
          right: convertInchesToTwip(1),
          bottom: convertInchesToTwip(1),
          left: convertInchesToTwip(1),
        },
      },
    },
    children: currentSection,
  }],
});

// Save document
const outputPath = 'C:/Users/EDY/mslearn-ai-agents/那年花开南法庄园_GEO+小红书+抖音运营方案_初稿.docx';
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ DOCX文件已生成: ${outputPath}`);
}).catch(err => {
  console.error('❌ 生成失败:', err);
});
