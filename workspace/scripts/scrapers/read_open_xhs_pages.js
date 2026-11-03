const fs = require('fs');
const out = 'C:/Users/EDY/mslearn-ai-agents/xhs_yh_capture';
fs.mkdirSync(out, {recursive:true});

async function httpJson(url){ const r=await fetch(url); if(!r.ok) throw new Error(`${r.status} ${url}`); return r.json(); }
function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
async function connect(wsUrl){
  const ws = new WebSocket(wsUrl);
  await new Promise((res,rej)=>{ const t=setTimeout(()=>rej(new Error('ws open timeout')),10000); ws.onopen=()=>{clearTimeout(t);res();}; ws.onerror=e=>{clearTimeout(t);rej(new Error('ws error'))}; });
  let id=0; const pending=new Map();
  ws.onmessage = ev => { const msg=JSON.parse(ev.data); if(msg.id && pending.has(msg.id)){ const p=pending.get(msg.id); pending.delete(msg.id); msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result); } };
  return { send(method, params={}){ const mid=++id; ws.send(JSON.stringify({id:mid,method,params})); return new Promise((resolve,reject)=>{ const t=setTimeout(()=>{pending.delete(mid); reject(new Error('timeout '+method));},20000); pending.set(mid,{resolve:(v)=>{clearTimeout(t);resolve(v);}, reject:(e)=>{clearTimeout(t);reject(e);}}); });}, close(){ws.close();} };
}

(async()=>{
  const pages = await httpJson('http://127.0.0.1:9222/json/list');
  const targets = pages.filter(p => p.type==='page' && p.url.includes('xiaohongshu.com') && p.url.includes('/user/profile/'));
  console.log('targets', targets.map(t=>({title:t.title,url:t.url,id:t.id})));
  const summaries=[];
  for(const [idx,t] of targets.entries()){
    console.log('read', idx+1, t.title);
    const c = await connect(t.webSocketDebuggerUrl);
    await c.send('Runtime.enable');
    await c.send('Page.enable');
    try { await c.send('Page.bringToFront'); } catch(e) {}
    await sleep(1000);
    // Scroll a little on profile/search pages to load notes.
    for(let i=0;i<4;i++){
      await c.send('Runtime.evaluate',{expression:`window.scrollTo(0, ${800*(i+1)}); true`, returnByValue:true});
      await sleep(1000);
    }
    await c.send('Runtime.evaluate',{expression:`window.scrollTo(0,0); true`, returnByValue:true});
    await sleep(800);
    const result = await c.send('Runtime.evaluate',{returnByValue:true, awaitPromise:true, expression:`(() => {
      const clean = s => (s||'').replace(/\\s+/g,' ').trim();
      const cards=[...document.querySelectorAll('a[href*="/explore/"], a[href*="/discovery/item/"]')].slice(0,80).map(a=>({href:a.href,text:clean(a.innerText||a.title||a.ariaLabel||''), aria:a.getAttribute('aria-label')||'', title:a.getAttribute('title')||''}));
      const els=[...document.querySelectorAll('div,span,p,a')].map(e=>clean(e.innerText||e.textContent||'')).filter(Boolean);
      const uniq=[...new Set(els)].filter(x=>x.length>1).slice(0,600);
      const profile={title:document.title,url:location.href,body:clean(document.body.innerText).slice(0,50000),cards,uniq};
      return profile;
    })()`});
    const data = result.result.value;
    const safe = `${idx+1}_${t.title}`.replace(/[\\/:*?"<>|]/g,'_');
    fs.writeFileSync(`${out}/${safe}.json`, JSON.stringify({target:t,data}, null, 2), 'utf8');
    fs.writeFileSync(`${out}/${safe}.txt`, data.body || '', 'utf8');
    try {
      const shot = await c.send('Page.captureScreenshot',{format:'png', captureBeyondViewport:true});
      fs.writeFileSync(`${out}/${safe}.png`, Buffer.from(shot.data,'base64'));
    } catch(e) { console.error('screenshot fail', e.message); }
    summaries.push({title:t.title,url:t.url,textLen:(data.body||'').length,cards:data.cards?.length||0,file:safe, sample:(data.body||'').slice(0,500)});
    c.close();
  }
  fs.writeFileSync(`${out}/dom_summary.json`, JSON.stringify(summaries,null,2),'utf8');
  console.log(JSON.stringify(summaries,null,2));
})();
