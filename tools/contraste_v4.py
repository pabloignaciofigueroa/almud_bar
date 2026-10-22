"""Mide el contraste de cada texto visible de /nueva/ y /nueva/carta/ (ES y EN, 390 y 1440). Uso: python3 tools/contraste_v4.py [base_url]"""
import asyncio,sys,json
from playwright.async_api import async_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8892'
JS=r"""()=>{
const lum=c=>{const a=c.map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2]};
const parse=s=>{const k=s.match(/color\(srgb ([^)]+)\)/);if(k){const q=k[1].split(/[ /]+/).filter(Boolean).map(Number);return [q[0]*255,q[1]*255,q[2]*255,q[3]===undefined?1:q[3]]}const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(/[ ,/]+/).filter(Boolean).map(Number);return [p[0],p[1],p[2],p[3]===undefined?1:p[3]]};
const out=[];const seen=new Set();
const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){const t=n.textContent.trim();if(!t)continue;const el=n.parentElement;if(seen.has(el))continue;seen.add(el);
 const cs=getComputedStyle(el);if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0)continue;
 const r=el.getBoundingClientRect();if(r.width<2||r.height<2)continue;
 if(el.closest('[aria-hidden="true"]')&&!el.closest('.hero'))continue;
 let fg=parse(cs.color);let bg=null,over=false,e=el;
 while(e){const s=getComputedStyle(e);const b=parse(s.backgroundColor);
   if(s.backgroundImage!=='none'&&!s.backgroundImage.includes('gradient'))over=true;
   if(b&&b[3]>0.5){bg=b;break} e=e.parentElement}
 // texto sobre foto/video (hermano medio debajo)
 const sec=el.closest('section,header,footer,figure,a');if(sec&&sec.querySelector('img,video')&&getComputedStyle(el).position==='absolute')over=true;
 if(!bg)bg=[255,255,255,1];
 const l1=lum(fg),l2=lum(bg);const ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
 const fs=parseFloat(cs.fontSize),fw=+cs.fontWeight;const big=fs>=24||(fs>=18.66&&fw>=700);
 const min=big?3:4.5;
 out.push({t:t.slice(0,40),sec:(el.closest('section,header,footer,nav')||{}).className||'',fg:cs.color,bg:`rgb(${bg.slice(0,3)})`,ratio:+ratio.toFixed(2),min,fs,over});
}
return out}"""
async def main():
  res=[]
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for path in ['/nueva/','/nueva/carta/']:
      for w,h in [(390,844),(1440,900)]:
        for lang in ['es','en']:
          ctx=await b.new_context(viewport={'width':w,'height':h})
          pg=await ctx.new_page()
          if lang=='en': await pg.add_init_script("try{localStorage.setItem('almud-idioma','en')}catch(e){}")
          await pg.goto(BASE+path);await pg.wait_for_timeout(4500)
          await pg.evaluate("document.querySelectorAll('.reveal,[class*=reveal]').forEach(e=>{e.style.opacity=1;e.style.transform='none'})")
          r=await pg.evaluate(JS)
          for x in r: x.update(page=path,w=w,lang=lang)
          res+=r;await ctx.close()
    await b.close()
  bad=[x for x in res if x['ratio']<x['min'] and not x['over']]
  json.dump(res,open('_plan/v4/contraste.json','w'),ensure_ascii=False,indent=0)
  uniq={}
  for x in bad: uniq.setdefault((x['page'],x['sec'],x['fg'],x['bg']),x)
  print('textos medidos',len(res),'· bajo el mínimo',len(bad),'· casos únicos',len(uniq))
  for k,x in uniq.items(): print(f"{x['ratio']:5} <{x['min']} {x['page']} [{x['sec'][:22]}] '{x['t']}' {x['fg']} sobre {x['bg']} {x['fs']}px")
asyncio.run(main())
