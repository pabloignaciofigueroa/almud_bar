// Capturas del dossier: computador 1440x900 y celular 390x844 de /nueva_v6/
const {chromium}=require('playwright');
const OUT=__dirname+'/shots/'; const U='http://localhost:8765/nueva_v6/';
// [clave, selector, modo, x]
const S=[
 ['hero','.hero','top'],
 ['lugar-a','.lugar','top'],['lugar-b','.lleno','center'],['lugar-c','.rincones','center'],
 ['tragos-a','.tragos','top'],['tragos-b','.tragos__band','offset',0.35],['tragos-c','.tragos__named','center'],
 ['comida-a','.comida','top'],['comida-b','.co__more','center'],
 ['quien-a','.quien','top'],['quien-b','.qz','center'],
 ['eventos-a','.eventos','top'],['eventos-b','.ev__mas','center'],['eventos-c','.cal','center'],
 ['equipo','.equipo','center'],
 ['resenas','.resenas','center'],
 ['donde','.donde','center'],
 ['pie','.pie','bottom'],
];
async function shoot(p,vh,prefix,list){
  for(const [k,sel,mode,x] of list){
    const y=await p.evaluate(([sel,mode,x,vh])=>{const e=document.querySelector(sel); if(!e) return -1;
      const top=e.getBoundingClientRect().top+scrollY, h=e.offsetHeight;
      if(mode==='top')return top; if(mode==='frac')return top+(h-vh)*x;
      if(mode==='offset')return top+h*x; if(mode==='bottom')return top+h-vh; return top+(h-vh)/2;},[sel,mode,x,vh]);
    if(y<0){console.log('no',sel);continue}
    // bajar por etapas para disparar las entradas
    const cur=await p.evaluate(()=>scrollY);
    for(let s=cur;s<y;s+=vh*0.6){await p.evaluate(s=>scrollTo(0,s),s);await p.waitForTimeout(120)}
    await p.evaluate(y=>scrollTo(0,y),Math.max(0,y)); await p.waitForTimeout(400);
    await p.evaluate(y=>scrollTo(0,y),Math.max(0,y)+1); await p.waitForTimeout(2600);
    await p.screenshot({path:`${OUT}${prefix}-${k}.jpg`,type:'jpeg',quality:84});
  }
}
(async()=>{const b=await chromium.launch();
  const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});
  const p=await c.newPage(); await p.goto(U);
  for(const t of [350,900,1500]){await p.waitForTimeout(t-(t===350?0:t===900?350:900));await p.screenshot({path:OUT+`d-intro-${t}.jpg`,type:'jpeg',quality:84});}
  await p.waitForTimeout(3500); await p.screenshot({path:OUT+'d-hero0.jpg',type:'jpeg',quality:84});
  await shoot(p,900,'d',S); await c.close();
  const m=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2.5,isMobile:true,hasTouch:true,locale:'es-CL'});
  const q=await m.newPage(); await q.goto(U); await q.waitForTimeout(4000);
  await q.screenshot({path:OUT+'m-hero0.jpg',type:'jpeg',quality:84});
  await shoot(q,844,'m',S); await b.close();})();
