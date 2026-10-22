
() => {
  const vw = innerWidth, out = [], issues = [];
  const vis = el => { const s = getComputedStyle(el); if (s.display==='none'||s.visibility==='hidden'||+s.opacity===0) return false;
    let p = el; while (p) { const cs = getComputedStyle(p); if (cs.display==='none'||cs.visibility==='hidden') return false; p = p.parentElement; } return true; };
  const sel = el => { let s = el.tagName.toLowerCase(); if (el.className && typeof el.className==='string') s += '.' + el.className.trim().split(/\s+/).join('.'); return s; };
  const seen = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue;
    const el = n.parentElement; if (!el || ['SCRIPT','STYLE','NOSCRIPT'].includes(el.tagName)) continue;
    if (!vis(el)) continue;
    if (el.closest('.sr-only')) continue;
    const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    const cs = getComputedStyle(el);
    out.push({sel: sel(el), t, tt: cs.textTransform, fs: cs.fontSize, lang: el.closest('[lang]')?.getAttribute('lang')});
    if (!seen.has(el)) { seen.add(el);
      if (el.scrollWidth > el.clientWidth + 1 && cs.overflow !== 'visible') issues.push({k:'overflow-clip', sel: sel(el), t, sw: el.scrollWidth, cw: el.clientWidth});
      if (cs.textOverflow === 'ellipsis' || cs.webkitLineClamp !== 'none') issues.push({k:'ellipsis/clamp', sel: sel(el), t});
      // horizontal: outside viewport and not in a horizontal track/carousel
      const inTrack = el.closest('[data-track],[data-swipe],.rincones,.eq,.rs');
      if (!inTrack && (r.right > vw + 1 || r.left < -1)) issues.push({k:'offscreen-x', sel: sel(el), t, l: Math.round(r.left), r: Math.round(r.right)});
      // word broken mid-word? range rects per word
      const rg = document.createRange(); const words = [...n.textContent.matchAll(/\S+/g)];
      for (const m of words) { rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length); const rs = rg.getClientRects();
        if (rs.length > 1) { const tops = new Set([...rs].map(x => Math.round(x.top))); if (tops.size > 1) issues.push({k:'word-split', sel: sel(el), w: m[0]}); } }
    }
  }
  return {out, issues, sw: document.documentElement.scrollWidth, vw};
}
