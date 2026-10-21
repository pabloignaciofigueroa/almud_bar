"""Contraste WCAG 2.x de cada par tinta/fondo del sistema v2 (fase 8).
Uso: python3 _plan/direccion/contraste.py  -> tabla markdown."""
def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    c = [x/12.92 if x <= 0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la+0.05)/(lb+0.05)

T = {  # tokens
 'noche': '#170e0b', 'noche-alta': '#2a1a14', 'papel': '#f6ecdc', 'papel-suave': '#cbb9a5',
 'barra': '#ff3f6c',
 'coral': '#f26343', 'turquesa': '#40b9c2', 'fucsia': '#cd0b61', 'amarillo': '#fac307', 'verde': '#06aa6b',
 'carta-azul': '#2023e4', 'carta-magenta-impreso': '#ec008c', 'carta-magenta': '#cd007a',
 'noche-neutra': '#171515',
}
PAIRS = [  # (tinta, fondo, uso, mínimo)
 ('papel', 'noche', 'cuerpo y titulares sobre noche', 4.5),
 ('papel-suave', 'noche', 'texto secundario sobre noche', 4.5),
 ('papel', 'noche-alta', 'texto en la hoja del menú', 4.5),
 ('papel-suave', 'noche-alta', 'secundario en la hoja del menú', 4.5),
 ('barra', 'noche', 'acento como texto/foco sobre noche', 4.5),
 ('noche', 'barra', 'texto del botón primario', 4.5),
 ('papel', 'barra', 'RECHAZADO: papel en botón', 4.5),
 ('noche', 'coral', 'tinta en campo coral', 4.5),
 ('papel', 'coral', 'RECHAZADO: papel en coral', 4.5),
 ('noche', 'turquesa', 'tinta en campo turquesa', 4.5),
 ('papel', 'turquesa', 'RECHAZADO: papel en turquesa', 4.5),
 ('papel', 'fucsia', 'tinta en campo fucsia', 4.5),
 ('noche', 'fucsia', 'RECHAZADO: noche en fucsia', 4.5),
 ('noche', 'amarillo', 'tinta en campo amarillo', 4.5),
 ('papel', 'amarillo', 'RECHAZADO: papel en amarillo', 4.5),
 ('noche', 'verde', 'tinta en campo verde', 4.5),
 ('papel', 'verde', 'RECHAZADO: papel en verde', 4.5),
 ('carta-azul', 'papel', 'nombres de la carta', 4.5),
 ('carta-magenta-impreso', 'papel', 'RECHAZADO en pantalla: magenta impreso', 4.5),
 ('carta-magenta', 'papel', 'precios en la web (cualquier tamaño)', 4.5),
 ('noche', 'papel', 'descripciones de la carta', 4.5),
 ('papel', 'carta-azul', 'botón sobre papel (azul)', 4.5),
 ('barra', 'fucsia', 'RECHAZADO: acento sobre fucsia (se confunden)', 3.0),
]
if __name__ == '__main__':
    print('| Tinta | Fondo | Uso | Ratio | Mín. | Resultado |\n|---|---|---|---|---|---|')
    for a, b, u, m in PAIRS:
        r = ratio(T[a], T[b]); ok = r >= m
        print(f"| `{a}` {T[a]} | `{b}` {T[b]} | {u} | {r:.2f}:1 | {m} | {'pasa' if ok else 'NO'} |")
