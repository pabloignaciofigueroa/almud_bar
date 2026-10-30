// Carta de envío: PDF, PNG de control, chequeos (desbordes y alineación de pies) y PDF para anillar (carta + brochure).
// Uso: python3 dossier/build_carta.py && NODE_PATH=$(npm root -g) node dossier/render_carta.js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1248, height: 816 } });
  await p.goto('file://' + __dirname + '/almud-carta-regalo.html', { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => {
    const out = [];
    for (const s of document.querySelectorAll('.izq,.der')) {
      const S = s.getBoundingClientRect();
      s.querySelectorAll('*').forEach(e => { const q = e.getBoundingClientRect(); if (q.height && (q.bottom > S.bottom + .5 || q.right > S.right + .5)) out.push(e.className || e.tagName); });
    }
    // aire entre el último párrafo y la firma
    const ps = [...document.querySelectorAll('.der .p')]; const last = ps[ps.length - 1].getBoundingClientRect();
    const firma = document.querySelector('.firma').getBoundingClientRect();
    const h1 = document.querySelector('h1'); const lh = parseFloat(getComputedStyle(h1).lineHeight);
    return { desbordes: out, pieFirma: document.querySelector('.firma .rol').getBoundingClientRect().bottom,
             pieIzq: document.querySelector('.base').getBoundingClientRect().bottom, aireFirma_in: (firma.top - last.bottom) / 96,
             lineasTitular: Math.round(h1.getBoundingClientRect().height / lh) };
  });
  console.log(JSON.stringify(r));
  await p.pdf({ path: __dirname + '/almud-carta-regalo.pdf', width: '13in', height: '8.5in', printBackground: true });
  await p.screenshot({ path: __dirname + '/pages/carta.png' });
  await b.close();
  require('child_process').execFileSync('qpdf', ['--empty', '--pages', __dirname + '/almud-carta-regalo.pdf', __dirname + '/almud-dossier-diseno.pdf', '--', __dirname + '/almud-brochure-imprimir.pdf']);
})();
