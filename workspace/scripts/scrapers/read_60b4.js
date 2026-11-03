const fs=require('fs');
const out='C:/Users/EDY/mslearn-ai-agents/xhs_yh_capture'; fs.mkdirSync(out,{recursive:true});
const url='https://www.xiaohongshu.com/user/profile/60b4e1f200000000010033a7?xsec_token=ABZgWUUEuSwKteHuG017lsa-0BbcdAFedbU28G2AhKAa0%3D&xsec_source=pc_search';
async function httpJson(url,opts){const r=await fetch(url,opts); if(!r.ok) throw new Error(r.status+' '+url); return r.json();}
async function connect(wsUrl){const ws=new WebSocket(wsUrl); await new Promise((res,rej)=>{ws.onopen=res; ws.onerror=()=>rej(new Error('ws error'));}); let id=0; const pending=new Map(); ws.onmessage=ev=>{const m=JSON.parse(ev.data); if(m.id&&pending.has(m.id)){const p=pending.get(m.id); pending.delete(m.id); m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result)}}; return {send(method,params={}){const mid=++id; ws.send(JSON.stringify({id:mid,method,params})); return new Promise((resolve,reject)=>{const t=setTimeout(()=>{pending.delete(mid);reject(new Error('timeout '+method));},30000); pending.set(mid,{resolve:v=>{clearTimeout(t);resolve(v)},reject:e=>{clearTimeout(t);reject(e)}})})}, close(){ws.close()}}}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const target=await httpJson('http://127.0.0.1:9222/json/new?'+encodeURIComponent(url),{method:'PUT'});
 const c=await connect(target.webSocketDebuggerUrl); await c.send('Runtime.enable'); await c.send('Page.enable'); await sleep(8000);
 for(let i=0;i<5;i++){await c.send('Runtime.evaluate',{expression:`window.scrollTo(0,${900*(i+1)}); true`,returnByValue:true}); await sleep(1200);}
 await c.send('Runtime.evaluate',{expression:'window.scrollTo(0,0); true',returnByValue:true}); await sleep(1000);
 const r=await c.send('Runtime.evaluate',{returnByValue:true, awaitPromise:true, expression:`(()=>{const clean=s=>(s||'').replace(/\\s+/g,' ').trim(); return {title:document.title,url:location.href,body:clean(document.body.innerText).slice(0,50000), cards:[...document.querySelectorAll('a[href*=\"/explore/\"]')].map(a=>a.href).slice(0,100)}})()`});
 fs.writeFileSync(out+'/60b4_profile.json', JSON.stringify(r.result.value,null,2),'utf8');
 fs.writeFileSync(out+'/60b4_profile.txt', r.result.value.body,'utf8');
 console.log(r.result.value.title, r.result.value.body.slice(0,1000));
 try{await httpJson('http://127.0.0.1:9222/json/close/'+target.id)}catch(e){}
 c.close();
})();
