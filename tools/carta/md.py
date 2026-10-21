import json
R='/home/claude/almud_bar/content/'
d=json.load(open(R+'carta-v2.json'))
L=['# Carta Almud Bar — v2 (para revisión)','',
   'Generado desde `content/carta-v2.json`. Texto literal de los 7 PDFs oficiales (`assets/raw/carta/`). Validar con `python3 tools/validate_carta.py`.','',
   '**Íconos → tags:** 🌿 = veggie · ✦vegan = vegan · 🌶 = picante · ★ = NUEVO','']
ico={'veggie':'🌿','vegan':'✦vegan','picante':'🌶','nuevo':'★ NUEVO'}
L.append('## Índice'); L.append('')
for s in d['secciones']:
    n=sum(len(g['items']) for g in s['grupos'])
    L.append(f"- [{s['titulo']}](#{s['id']}) — {s['fuente']} — {n} ítems")
L.append('')
for s in d['secciones']:
    L.append(f"<a id=\"{s['id']}\"></a>"); L.append(f"## {s['titulo']}  ·  {s['fuente']}"); L.append('')
    if s.get('intro'): L.append(f"_{s['intro']}_"); L.append('')
    for g in s['grupos']:
        if g.get('titulo'):
            t=g['titulo'] if not g.get('padre') else f"{g['padre']} › {g['titulo']}"
            L.append(f"### {t}"); L.append('')
        if g.get('nota'):
            for ln in g['nota'].split('\n'): L.append(f"> {ln}")
            L.append('')
        cols=g.get('columnas')
        if cols:
            L.append('| Nombre | Detalle | '+' | '.join(cols)+' |'); L.append('|---|---|'+'---:|'*len(cols))
            for i in g['items']:
                det=' '.join(x for x in (i.get('desc'),i.get('nota')) if x)
                L.append(f"| **{i['nombre']}** | {det} | "+' | '.join(i['precios'][c] for c in cols)+' |')
            L.append('')
        else:
            for i in g['items']:
                tags=' '.join(ico.get(t,t) for t in i.get('tags',[]))
                head=f"- **{i['nombre']}**" + (f" {tags}" if tags else '') + f" — {i['precio']}"
                if i.get('dia'): head=f"- **{i['dia']}:** {i['nombre']} — {i['precio']}" + (f"  (impreso: “{i['texto']}”)" if i.get('texto') else '')
                if i.get('bodega'): head=f"- **{i['nombre']}** _{i['bodega']}_ {i.get('nota','')} — {i['precio']}"
                L.append(head)
                if i.get('desc'): L.append(f"  {i['desc']}")
                if i.get('nota') and not i.get('bodega'): L.append(f"  _{i['nota']}_")
            L.append('')
        if g.get('nota_pie'): L.append(f"> 📝 {g['nota_pie']}"); L.append('')
L.append('---'); L.append('## Correcciones aplicadas'); L.append('')
for c in d['_correcciones']: L.append(f"- {c['fuente']} · {c['item']} · {c['campo']}: “{c['antes']}” → “{c['despues']}” — {c['motivo']}")
L.append(''); L.append('## Emoji omitidos'); L.append('')
for e in d['_emoji_omitidos']: L.append(f"- {e['fuente']} · {e['item']}: {e['aspecto']} (glifo `{e['glifo_pdf']}`) tras “{e['tras']}”")
L.append(''); L.append('## Diferencias con carta.json (se conservó el texto de carta.json)'); L.append('')
for x in d['_diferencias_con_carta_json']: L.append(f"- {x['item']} · {x['campo']}: PDF “{x.get('pdf_v2_transcripcion', x.get('pdf',''))}” / carta.json “{x.get('carta.json','')}”")
L.append(''); L.append('## Dudas'); L.append('')
for x in d['_dudas']: L.append(f"- {x}")
open(R+'carta-v2.md','w').write('\n'.join(L)+'\n')
