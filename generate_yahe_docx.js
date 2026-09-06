const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageBreak
} = require('docx');

const mdPath = 'C:/Users/EDY/mslearn-ai-agents/雅禾婚礼_小红书运营方案_初版.md';
const mdContent = fs.readFileSync(mdPath, 'utf-8');

const RED = '9e1f34';
const GOLD = 'cda349';
const DARK = '2d2220';
const GREEN = '2f6f5e';

function heading(text, level) {
  return new Paragraph({
    heading: level <= 5 ? `Heading${level}` : 'Heading5',
    text: text.replace(/^#+\s*/, ''),
    spacing: { before: level === 1 ? 360 : level === 2 ? 260 : 180, after: 120 },
  });
}
function parseRow(line) {
  return line.split('|').filter((_, i, arr) => i > 0 && i < arr.length - 1).map(c => c.trim());
}
function table(headers, rows) {
  const w = Math.floor(9020 / headers.length);
  const head = headers.map(h => new TableCell({
    children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: 'FFFFFF', size: 20 })], alignment: AlignmentType.CENTER, spacing: { before: 60, after: 60 } })],
    shading: { type: ShadingType.SOLID, color: RED },
    width: { size: w, type: WidthType.DXA },
  }));
  const body = rows.map((r, idx) => new TableRow({
    children: r.map(c => new TableCell({
      children: [new Paragraph({ text: c || '', spacing: { before: 40, after: 40 } })],
      shading: idx % 2 === 0 ? { type: ShadingType.SOLID, color: 'fbf8f6' } : undefined,
      width: { size: w, type: WidthType.DXA },
    }))
  }));
  return new Table({
    rows: [new TableRow({ children: head }), ...body],
    width: { size: 9020, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: 'd9d9d9' },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: 'd9d9d9' },
      left: { style: BorderStyle.SINGLE, size: 1, color: 'd9d9d9' },
      right: { style: BorderStyle.SINGLE, size: 1, color: 'd9d9d9' },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: 'd9d9d9' },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: 'd9d9d9' },
    },
  });
}
function divider() {
  return new Paragraph({ spacing: { before: 120, after: 120 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: GOLD } } });
}

const children = [];
children.push(new Paragraph({ spacing: { before: 2200 } }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: '雅禾婚礼', size: 52, bold: true, color: DARK })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: '小红书运营方案（初版）', size: 38, bold: true, color: RED })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 220, after: 80 }, children: [new TextRun({ text: '户外打包价婚庆为主 · 室内酒店布置为辅', size: 24, color: '6c757d' })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: '2026年7月1日', size: 22, color: '6c757d' })] }));
children.push(new Paragraph({ children: [new PageBreak()] }));

const lines = mdContent.split('\n');
let inTable = false;
let tlines = [];
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (i < 6) continue;
  if (line.startsWith('|') && line.endsWith('|') && !line.match(/^\|[\s\-:]+\|/)) {
    if (!inTable) { inTable = true; tlines = []; }
    tlines.push(line);
    if (i + 1 < lines.length && lines[i + 1].startsWith('|') && lines[i + 1].endsWith('|') && !lines[i + 1].match(/^\|[\s\-:]+\|/)) continue;
    if (tlines.length >= 2) {
      children.push(table(parseRow(tlines[0]), tlines.slice(1).map(parseRow)));
      children.push(new Paragraph({ spacing: { after: 160 }, text: '' }));
    }
    inTable = false; tlines = [];
    continue;
  }
  if (line.match(/^\|[\s\-:]+\|/)) continue;
  if (line.startsWith('# ')) { children.push(divider()); children.push(heading(line, 1)); }
  else if (line.startsWith('## ')) children.push(heading(line, 2));
  else if (line.startsWith('### ')) children.push(heading(line, 3));
  else if (line.trim() === '---') children.push(divider());
  else if (/^\s*-\s/.test(line)) children.push(new Paragraph({ text: line.replace(/^\s*-\s/, ''), bullet: { level: 0 }, spacing: { after: 80 } }));
  else if (line.trim()) {
    if (line.includes('**')) {
      const parts = line.split(/(\*\*.*?\*\*)/g).filter(Boolean).map(p => p.startsWith('**') && p.endsWith('**') ? new TextRun({ text: p.replace(/^\*\*|\*\*$/g, ''), bold: true, color: GREEN }) : new TextRun({ text: p }));
      children.push(new Paragraph({ children: parts, spacing: { after: 100 } }));
    } else if (line.startsWith('>')) children.push(new Paragraph({ children: [new TextRun({ text: line.replace(/^>\s*/, ''), italics: true, color: '666666' })], spacing: { after: 100 } }));
    else children.push(new Paragraph({ text: line, spacing: { after: 100 } }));
  } else children.push(new Paragraph({ spacing: { after: 60 }, text: '' }));
}

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: 'Microsoft YaHei', size: 22 } },
      heading1: { run: { font: 'Microsoft YaHei', size: 34, bold: true, color: DARK } },
      heading2: { run: { font: 'Microsoft YaHei', size: 28, bold: true, color: RED } },
      heading3: { run: { font: 'Microsoft YaHei', size: 24, bold: true, color: GOLD } },
    }
  },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children }]
});

Packer.toBuffer(doc).then(buf => {
  const out = 'C:/Users/EDY/mslearn-ai-agents/雅禾婚礼_小红书运营方案_初版.docx';
  fs.writeFileSync(out, buf);
  console.log('OK', out, (buf.length/1024).toFixed(1),'KB');
});
