// Carta y modo inglés
const {chromium}=require('playwright');
const OUT=__dirname+'/shots/';
(async()=>{const b=await chromium.launch();
 const m=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2.5,isMobile:true,hasTouch:true,locale:'es-CL'});
 const q=await m.newPage(); await q.goto('http://localhost:8765/nueva/carta/'); await q.waitForTimeout(3000);
 await q.screenshot({path:OUT+'m-carta.jpg',type:'jpeg',quality:84});
 await q.evaluate(()=>scrollTo(0,900)); await q.waitForTimeout(1500); await q.screenshot({path:OUT+'m-carta2.jpg',type:'jpeg',quality:84});
 const q2=await m.newPage(); await q2.goto('http://localhost:8765/nueva_v6/'); await q2.waitForTimeout(4000);
 await q2.click('[data-lang]'); await q2.waitForTimeout(800);
 const y=await q2.evaluate(()=>document.querySelector('.lugar').getBoundingClientRect().top+scrollY);
 for(let s=0;s<y;s+=400){await q2.evaluate(s=>scrollTo(0,s),s);await q2.waitForTimeout(120)}
 await q2.evaluate(y=>scrollTo(0,y),y);await q2.waitForTimeout(2800); await q2.screenshot({path:OUT+'m-en-lugar.jpg',type:'jpeg',quality:84});
 await q2.evaluate(()=>{try{localStorage.removeItem('almud-idioma')}catch(e){}});
 const d=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1.5,locale:'es-CL'});
 const p=await d.newPage(); await p.goto('http://localhost:8765/nueva/carta/'); await p.waitForTimeout(3000);
 await p.screenshot({path:OUT+'d-carta.jpg',type:'jpeg',quality:84});
 await b.close()})();
