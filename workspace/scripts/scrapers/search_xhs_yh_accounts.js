const fs=require('fs');
const out='C:/Users/EDY/mslearn-ai-agents/xhs_yh_capture'; fs.mkdirSync(out,{recursive:true});
const queries=['63082574980','成都雅盉雅禾婚礼','成都雅禾婚礼'];
async function httpJson(url,opts){const r=await fetch(url,opts); if(!r.ok) throw new Error(r.status+' '+url); return r.json();}
async function connect(wsUrl){const ws=new WebSocket(wsUrl); await new Promise((res,rej)=>{ws.onopen=res; ws.onerror=()=>rej(new Error('ws error'));}); let id=0; const pending=new Map(); ws.onmessage=ev=>{const m=JSON.parse(ev.data); if(m.id&&pending.has(m.id)){const p=pending.get(m.id); pending.delete(m.id); m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result)}}; return {send(method,params={}){const mid=++id; ws.send(JSON.stringify({id:mid,method,params})); return new Promise((resolve,reject)=>{const t=setTimeout(()=>{pending.delete(mid);reject(new Error('timeout '+method));},30000); pending.set(mid,{resolve:v=>{clearTimeout(t);resolve(v)},reject:e=>{clearTimeout(t);reject(e)}})})}, close(){ws.close()}}}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const results=[];
 for(const q of queries){
  const url='https://www.xiaohongshu.com/search_result?keyword='+encodeURIComponent(q)+'&source=web_search_result_notes';
  const target=await httpJson('http://127.0.0.1:9222/json/new?'+encodeURIComponent(url),{method:'PUT'});
  const c=await connect(target.webSocketDebuggerUrl); await c.send('Runtime.enable'); await c.send('Page.enable'); await sleep(7000);
  for(let i=0;i<4;i++){await c.send('Runtime.evaluate',{expression:`window.scrollTo(0,${900*(i+1)}); true`,returnByValue:true}); await sleep(1200);}
  const r=await c.send('Runtime.evaluate',{returnByValue:true, awaitPromise:true, expression:`(()=>{const clean=s=>(s||'').replace(/\\s+/g,' ').trim(); const as=[...document.querySelectorAll('a')].map(a=>({href:a.href,text:clean(a.innerText||a.title||a.ariaLabel||''),title:a.title||'',aria:a.ariaLabel||''})).filter(x=>x.href||x.text); const body=clean(document.body.innerText).slice(0,30000); return {q:${JSON.stringify(q)},title:document.title,url:location.href,body,links:as.slice(0,300)}})()`});
  fs.writeFileSync(`${out}/search_${q}.json`.replace(/[\\/:*?"<>|]/g,'_'), JSON.stringify(r.result.value,null,2),'utf8');
  fs.writeFileSync(`${out}/search_${q}.txt`.replace(/[\\/:*?"<>|]/g,'_'), r.result.value.body,'utf8');
  console.log('QUERY',q,'TITLE',r.result.value.title,'LEN',r.result.value.body.length);
  console.log(r.result.value.body.slice(0,2000));
  results.push(r.result.value);
  try{await httpJson('http://127.0.0.1:9222/json/close/'+target.id)}catch(e){}
  c.close(); await sleep(1500);
 }
 fs.writeFileSync(`${out}/search_accounts_summary.json`, JSON.stringify(results,null,2),'utf8');
})();
