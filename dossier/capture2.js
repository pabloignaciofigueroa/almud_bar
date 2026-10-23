// Ajustes finos de capturas de computador
const {chromium}=require('playwright');
const OUT=__dirname+'/shots/'; const U='http://localhost:8765/nueva_v6/';
const S=[['equipo','.equipo','top',0],['resenas','.resenas','top',-60],['eventos-b','.ev__mas','top',-200],['pie','.pie','end',0],['donde','.donde','top',0]];
(async()=>{const b=await chromium.launch();
  const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});
  const p=await c.newPage(); await p.goto(U); await p.waitForTimeout(4000);
  for(const [k,sel,mode,dy] of S){
    const y=await p.evaluate(([sel,mode])=>{const e=document.querySelector(sel);const top=e.getBoundingClientRect().top+scrollY;
      return mode==='end'?document.documentElement.scrollHeight:top},[sel,mode]);
    const cur=await p.evaluate(()=>scrollY);
    for(let s=cur;s<y+dy;s+=400){await p.evaluate(s=>scrollTo(0,s),s);await p.waitForTimeout(150)}
    await p.evaluate(y=>scrollTo(0,y),y+dy); await p.waitForTimeout(500);
    await p.mouse.wheel(0,2); await p.waitForTimeout(3200);
    await p.screenshot({path:`${OUT}d-${k}.jpg`,type:'jpeg',quality:84});
  }
  await b.close();})();
