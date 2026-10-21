import json, csv, re, collections, sys
ROOT = '/home/claude/almud_bar'
posts = {p['id']: p for p in json.load(open(f'{ROOT}/content/ig_posts.json'))}
cat = list(csv.DictReader(open(f'{ROOT}/_plan/diag/catalogo.csv')))
bypost = collections.defaultdict(list)
for r in cat:
    bypost[r['post_id']].append(r)

# ---------- emoji handling ----------
EMO = ('[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿‼⁉™ℹ'
       '↔-↪〰〽㊗㊙️‍\U0001F1E6-\U0001F1FF\U0001F3FB-\U0001F3FF⃣]+')
EMO_RUN = re.compile(r'([ \t]*)(' + EMO + r')([ \t]*)')
PUNCT = set(',.!?;:)]…')

def strip_emoji(s):
    removed = []
    out = []
    pos = 0
    for m in EMO_RUN.finditer(s):
        removed.append(m.group(2))
        out.append(s[pos:m.start()])
        nxt = s[m.end():m.end() + 1]
        prev = s[m.start() - 1:m.start()] if m.start() > 0 else ''
        if nxt == '' or nxt in PUNCT or nxt == '\n' or prev == '' or prev == '\n':
            rep = ''
        else:
            rep = ' '
        out.append(rep)
        pos = m.end()
    out.append(s[pos:])
    t = ''.join(out)
    t = re.sub(r'[ \t]{3,}', '  ', t)
    return t, removed

def frag(pid, start, end=None):
    cap = posts[pid]['caption']
    i = cap.find(start)
    if i < 0:
        sys.exit(f'START NOT FOUND {pid}: {start!r}')
    if end is None:
        j = i + len(start)
    else:
        j = cap.find(end, i)
        if j < 0:
            sys.exit(f'END NOT FOUND {pid}: {end!r}')
        j += len(end)
    raw = cap[i:j]
    if '\n.\n' in raw:
        sys.exit(f'SPANS PARAGRAPH {pid}: {raw!r}')
    txt, rem = strip_emoji(raw)
    txt = txt.replace('\n', ' / ').strip()
    return raw, txt, rem

def quote(pid, start, end=None, voz=None, nota=None):
    raw, txt, rem = frag(pid, start, end)
    d = {'text': txt, 'source': pid}
    if nota:
        d['nota'] = nota
    if rem:
        d['emoji_removed'] = rem
    if voz:
        d['voz'] = voz
    return d

def title(pid, start, end=None, voz=None):
    d = quote(pid, start, end, voz)
    d['chars'] = len(d['text'])
    if d['chars'] > 32:
        sys.exit(f'TITLE TOO LONG {pid}: {d["text"]!r} {d["chars"]}')
    return d

THIRD = {'IG-007': 'tercero: creadores de contenido (post colaborativo)',
         'IG-028': 'tercero: banda Isleños (post colaborativo)',
         'IG-029': 'tercero: banda Isleños (post colaborativo)',
         'IG-056': 'tercero: @mediskin (post colaborativo)',
         'IG-033': 'tercero: fotógrafa @mariannefuentealba (post colaborativo)'}

# ---------- lexicon ----------
LEX = [
 ('ito ito / ita ita (diminutivo en cascada)', r'\b\w+(it[oa]s?|iñ[oa]s?)\s+(ito|ita|itos|itas)\b'),
 ('ona ona / ucho ucho / lín lín (eco)', r'\b(ona ona|ucho ucho|lín lín)\b'),
 ('-eichon', r'\w+eichons?\b'),
 ('Almudcito', r'almudcit[oa]s?|almuddddcitooo'),
 ('barsucho', r'barsucho'),
 ('guarisnaque(arse)', r'guarisnaque\w*'),
 ('güergüero', r'güergüer\w*'),
 ('buche', r'\bbuche\b'),
 ('empinar el codo / empinación / codein', r'empin\w+|codein|codazo'),
 ('comilona', r'comilona'),
 ('menjunje', r'menjunje\w*'),
 ('ñam ñam / glup glup / chin chin', r'ñam ñam|glup glup|chin chin'),
 ('parroquian@s', r'parroquian\w*'),
 ('jornada recreativa', r'jornadas? recreativas?'),
 ('delichus', r'delichu\w*'),
 ('macanúo', r'macanú\w*'),
 ('picho caluga', r'p[is]sho caluga|picho caluga'),
 ('choriflai', r'choriflai\w*'),
 ('mortal kombat', r'mortal kombat'),
 ('el descueve', r'descueve\w*'),
 ('chanchulín / shanshulín / chanchi / tchantcho', r'chanchul\w+|shanshul\w+|\bchanchi\b|tchantcho|chancho'),
 ('tikitikití', r'tiki ?tiki ?t\w*'),
 ('japi berdey / japi niu yiar', r'japi \w+'),
 ('guanderful', r'guanderful\w*'),
 ('tumorrou / tudei / siyuleiter', r'tumorrou|tudei\w*|siyuleiter'),
 ('of corsss', r'of cors\w*'),
 ('usté', r'\busté\b'),
 ('con tuti', r'con tuti\w*|tuti el|tuti '),
 ('colors / colorsss', r'\bcolors+\w*|colorc[ií]n'),
 ('mundo mundial', r'mundo mundial'),
 ('llenifer', r'llenifer'),
 ('beio/beia', r'\bbei[oa]s?\b|beiooo|beiiii\w*'),
 ('-eli (tinteli, bigoteli, pisqueli, concurseli)', r'\b\w+eli(s|ss|iii\w*)?\b'),
 ('onfaya / on faia', r'on ?fa[yi]a+\w*|faia'),
 ('ponerle wendy / güendi', r'wendy\w*|güendi'),
 ('queridis / amiguis / toditis / todis', r'queridi\w*|amiguis|toditi\w*|todis\b|cuerpis|parejis|hermanis'),
 ('corasound', r'corasound\w*'),
 ('helao Juan', r'helao juan\w*|frío juan'),
 ('perro con dos colas', r'perro con dos colas'),
 ('maldición gitana', r'maldici[oó]n gitana'),
 ('lucrecias / lucas', r'lucrecias|\blucas\b'),
 ('besi', r'\bbesi\w*'),
 ('salucita', r'saluc\w*|\bsalú+\b'),
 ('güen/güena/güeno', r'\bgüen\w*'),
 ('-ein (piscolein, tranquilein, rapidein, cerradein)', r'\b\w+ein(n+)?\b'),
 ('dentrar pa dentro', r'dentr\w+ pa dentro|dentrada pa dentro'),
 ('nanai', r'nanai'),
 ('cachilupi', r'cachilupi\w*'),
 ('endieciochar(se)', r'endieciocha\w*|dieciosho+|dieciotcho'),
]
LEXC = [(n, re.compile(rx, re.I)) for n, rx in LEX]

def lexicon(pids):
    c = collections.Counter(); ex = {}
    for pid in pids:
        cap = posts[pid]['caption']
        if pid in THIRD:
            continue
        for n, rx in LEXC:
            ms = rx.findall(cap)
            found = [m.group(0) for m in rx.finditer(cap)]
            if found:
                c[n] += len(found)
                ex.setdefault(n, [])
                for f in found:
                    if f not in ex[n] and len(ex[n]) < 4:
                        ex[n].append(f)
    return [{'term': n, 'count': c[n], 'examples': ex[n]} for n, _ in c.most_common()]

HANDLE = re.compile(r'(?<![\w@])@[A-Za-z0-9_][\w.]*\w')

def people(pids, extra):
    seen = []
    for pid in pids:
        for h in HANDLE.findall(posts[pid]['caption']):
            if h.lower() == '@almud_bar':
                continue
            if h not in seen:
                seen.append(h)
    return seen + [e for e in extra if e not in seen]

SPACEMAP = {'rincón sillones': 'sofás', 'salón interior': 'mesas interiores', 'barra': 'barra',
            'terraza techada': 'patio techado', 'terraza abierta': 'terraza descubierta',
            'cuadros/arte': 'cuadros', 'equipo': 'personal', 'dueños': 'personal'}

def fnum(x, d=None):
    try:
        return float(x)
    except Exception:
        return d

def files_for(pid):
    return [r for r in bypost.get(pid, []) if r['kind'] != 'portada-video']

def build(t):
    pids = [p for p in t['posts'] if p.startswith('IG-')]
    hls = [p for p in t['posts'] if p.startswith('HL-')]
    plist = []
    rows = []
    for pid in sorted(pids, key=lambda x: posts[x]['date']):
        p = posts[pid]
        fr = files_for(pid)
        ln = fnum(fr[0]['likes_norm_era']) if fr else None
        plist.append({'id': pid, 'date': p['date'], 'likes': p['likes'], 'likes_norm': ln,
                      'files': p['files']})
        rows += fr
    for hl in hls:
        fr = files_for(hl)
        dates = sorted(r['date'] for r in fr if r['date'])
        plist.append({'id': hl, 'date': f'{dates[0]}..{dates[-1]}' if dates else None, 'likes': None,
                      'likes_norm': None, 'files': [r['file'].split('/')[-1] for r in fr],
                      'nota': 'destacada (stories); sin caption ni likes'})
        rows += fr
    def score(r):
        ln = fnum(r['likes_norm_era'])
        return int(r['epica'] or 0) * int(r['q_tecnica'] or 0) * (ln if ln is not None else 1.0)
    best = []
    for r in sorted(rows, key=score, reverse=True)[:5]:
        b = {'file': r['file'], 'ref': r['ref'], 'post': r['post_id'], 'kind': r['kind'], 'space': r['space'],
             'light': r['light'], 'epica': int(r['epica']), 'calidad': int(r['q_tecnica']),
             'likes_norm': fnum(r['likes_norm_era']), 'score': round(score(r), 2), 'resolution': r['resolution'],
             'descripcion': r['descripcion']}
        if fnum(r['likes_norm_era']) is None:
            b['nota'] = 'likes_norm no disponible (story): se usó 1,0'
        best.append(b)
    sp = collections.Counter(); spg = collections.Counter()
    for r in rows:
        k = SPACEMAP.get(r['space'])
        if k:
            sp[k] += 1
            if int(r['epica'] or 0) >= 4 and int(r['q_tecnica'] or 0) >= 4:
                spg[k] += 1
    likes = [x['likes'] for x in plist if x['likes'] is not None]
    lns = [x['likes_norm'] for x in plist if x['likes_norm'] is not None]
    years = sorted({int(r['date'][:4]) for r in rows if r['date']} | {int(posts[p]['date'][:4]) for p in pids})
    top3 = sorted([int(r['epica']) * int(r['q_tecnica']) for r in rows], reverse=True)[:3]
    photo = round(sum(top3) / len(top3) / 25 * 5, 2) if top3 else 0
    lnm = round(sum(lns) / len(lns), 2) if lns else None
    eng = round(min(lnm, 3) / 3 * 5, 2) if lnm is not None else 1.0
    strength = {'engagement': eng, 'foto': photo, 'narrativa': t['N'], 'quien_es_almud': t['W']}
    strength['total_20'] = round(sum(strength.values()), 2)
    out = {
        'id': t['id'], 'name': t['name'], 'kind': t['kind'],
        'title_literal': t['titles'],
        'posts': plist,
        'key_quotes': t['quotes'],
        'people': people(pids, t.get('extra_people', [])),
        'lexicon': lexicon(pids),
        'carta_names': t.get('carta', []),
        'best_files': best,
        'spaces_carried': {k: {'files': sp[k], 'fuertes_e4q4': spg[k]} for k in
                           ['sofás', 'mesas interiores', 'barra', 'patio techado', 'terraza descubierta', 'cuadros', 'personal'] if sp[k]},
        'total_likes': sum(likes), 'n_posts': len(pids), 'likes_norm_mean': lnm,
        'recurrence': years,
        'strength': strength,
        'note': t['note'],
    }
    if t.get('see_also'):
        out['see_also'] = t['see_also']
    if t.get('series'):
        out['series'] = t['series']
    return out

exec(open('/tmp/claude-0/-home-claude/011b3bf8-fa11-50bd-ba3e-4cc567dfb832/scratchpad/tales.py').read())

res = [build(t) for t in TALES]
# coverage check
assigned = collections.Counter(p for t in TALES for p in t['posts'] if p.startswith('IG-'))
missing = [p for p in posts if p not in assigned]
dup = [p for p, c in assigned.items() if c > 1]
print('missing', missing, 'dup', dup)
res.sort(key=lambda x: -x['strength']['total_20'])
for i, r in enumerate(res, 1):
    r['rank'] = i
doc = {'_fuente': 'Fase 3 · inventario de historias. 180 posts de content/ig_posts.json (IG-001…IG-180) + destacadas de assets/raw/hl/highlights.json. Cada post IG está en exactamente un cuento (posts); los cruces van en see_also. Textos literales de las captions: solo se quitan glifos emoji (anotados en emoji_removed) y los saltos de línea se escriben " / ". Captions de posts colaborativos de terceros marcadas con "voz". best_files = top 5 por épica × calidad × likes normalizados por época (catalogo.csv). strength: engagement (likes_norm_mean, tope 3 → 0–5) + foto (promedio top-3 épica×calidad → 0–5) + narrativa (juicio 1–5) + quien_es_almud (juicio 1–5) = total sobre 20.',
       'generado': '2026-10-21', 'n_cuentos': len(res), 'tales': res}
json.dump(res, open(f'{ROOT}/content/historias.json', 'w'), ensure_ascii=False, indent=1)
for r in res:
    print(r['rank'], r['id'], r['n_posts'], r['total_likes'], r['likes_norm_mean'], r['strength'], r['recurrence'], [b['ref'] for b in r['best_files']], r['spaces_carried'])
