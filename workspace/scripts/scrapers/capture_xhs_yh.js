const fs = require('fs');
const path = require('path');

const outDir = 'C:/Users/EDY/mslearn-ai-agents/xhs_yh_capture';
fs.mkdirSync(outDir, { recursive: true });

const accounts = [
  { key: '63082574980', name: '成都雅盉雅禾婚礼', url: 'https://www.xiaohongshu.com/user/profile/5e3f9f6000000000010051c9?xsec_token=ABkQgAx1bA1k6p79sSKF_p9-qFq4JL0rnmraJVBaEwVSw%3D&xsec_source=pc_search' },
  { key: '49988072972', name: 'A雅禾婚礼', url: 'https://www.xiaohongshu.com/user/profile/60b4e1f200000000010033a7?xsec_token=ABZgWUUEuSwKteHuG017lsa-0BbcdAFedbU28G2AhKAa0%3D&xsec_source=pc_search' },
  { key: '633073288', name: '雅禾婚礼维维', url: 'https://www.xiaohongshu.com/user/profile/5ae9c9ea4eacab1a73fefd46?xsec_token=ABPp7CPpGnfS-JwPxgsBvUeT-WMmVfEaXnW3DggAEXlhI%3D&xsec_source=pc_search' },
  { key: '27234178083', name: 'A雅禾婚礼工作室', url: 'https://www.xiaohongshu.com/user/profile/60b4e1f200000000010033a7?xsec_token=ABZgWUUEuSwKteHuG017lsa-0BbcdAFedbU28G2AhKAa0%3D&xsec_source=pc_search' },
];

async function httpJson(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} ${url}`);
  return res.json();
}

async function cdp(wsUrl) {
  const WebSocket = global.WebSocket;
  const ws = new WebSocket(wsUrl);
  await new Promise((resolve, reject) => {
    ws.addEventListener('open', resolve, { once: true });
    ws.addEventListener('error', reject, { once: true });
  });
  let id = 0;
  const pending = new Map();
  ws.addEventListener('message', ev => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    }
  });
  return {
    send(method, params = {}) {
      const mid = ++id;
      ws.send(JSON.stringify({ id: mid, method, params }));
      return new Promise((resolve, reject) => pending.set(mid, { resolve, reject }));
    },
    close() { ws.close(); }
  };
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function waitForLoad(client, timeoutMs = 25000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const r = await client.send('Runtime.evaluate', { expression: 'document.readyState', returnByValue: true });
      if (r.result.value === 'complete' || r.result.value === 'interactive') return;
    } catch (e) {}
    await sleep(500);
  }
}

async function evalText(client, expression) {
  const r = await client.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  return r.result.value;
}

async function captureAccount(browserWs, account, index) {
  const target = await httpJson(`http://127.0.0.1:9222/json/new?${encodeURIComponent(account.url)}`, { method: 'PUT' });
  const client = await cdp(target.webSocketDebuggerUrl);
  await client.send('Page.enable');
  await client.send('Runtime.enable');
  await client.send('Network.enable');
  await client.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1600, deviceScaleFactor: 1, mobile: false });
  await waitForLoad(client);
  await sleep(6000);

  // Scroll to trigger note loading.
  for (let i = 0; i < 5; i++) {
    await evalText(client, `window.scrollTo(0, document.body.scrollHeight * ${(i + 1) / 5}); true`);
    await sleep(1800);
  }
  await evalText(client, `window.scrollTo(0,0); true`);
  await sleep(1000);

  const visible = await evalText(client, `(() => {
    const clean = s => (s || '').replace(/\s+/g, ' ').trim();
    return clean(document.body.innerText).slice(0, 20000);
  })()`);

  const data = await evalText(client, `(() => {
    const clean = s => (s || '').replace(/\s+/g, ' ').trim();
    const cards = [...document.querySelectorAll('a[href*="/explore/"], a[href*="/discovery/item/"]')].slice(0, 60).map(a => {
      const rect = a.getBoundingClientRect();
      const txt = clean(a.innerText || a.getAttribute('title') || a.getAttribute('aria-label') || '');
      return { href: a.href, text: txt, x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) };
    });
    const imgs = [...document.images].slice(0, 120).map(img => ({ alt: img.alt || '', src: img.currentSrc || img.src, w: img.naturalWidth, h: img.naturalHeight }));
    const metas = [...document.querySelectorAll('meta')].map(m => ({ name: m.getAttribute('name') || m.getAttribute('property') || '', content: m.getAttribute('content') || '' })).filter(x => x.content);
    return { title: document.title, url: location.href, visibleText: clean(document.body.innerText).slice(0,20000), cards, imgs, metas };
  })()`);

  const shot = await client.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  const safe = `${index}_${account.key}_${account.name}`.replace(/[\\/:*?"<>|]/g, '_');
  fs.writeFileSync(path.join(outDir, `${safe}.png`), Buffer.from(shot.data, 'base64'));
  fs.writeFileSync(path.join(outDir, `${safe}.json`), JSON.stringify({ account, data }, null, 2), 'utf8');
  fs.writeFileSync(path.join(outDir, `${safe}.txt`), visible, 'utf8');
  await client.close();
  try { await httpJson(`http://127.0.0.1:9222/json/close/${target.id}`); } catch(e) {}
  return { account, title: data.title, textLen: visible.length, cards: data.cards.length, file: safe };
}

(async () => {
  const version = await httpJson('http://127.0.0.1:9222/json/version');
  const results = [];
  for (let i = 0; i < accounts.length; i++) {
    console.log('CAPTURE', accounts[i].name, accounts[i].url);
    try {
      results.push(await captureAccount(version.webSocketDebuggerUrl, accounts[i], i + 1));
    } catch (e) {
      console.error('ERR', accounts[i].name, e.stack || e.message);
      results.push({ account: accounts[i], error: e.message });
    }
    await sleep(2500);
  }
  fs.writeFileSync(path.join(outDir, 'summary.json'), JSON.stringify(results, null, 2), 'utf8');
  console.log(JSON.stringify(results, null, 2));
})();
