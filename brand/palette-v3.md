# Paleta v3 · Almud Bar

Esta paleta reemplaza a la v1 (`brand/palette.md`), que tenía 12 colores vivos y una franja arcoíris. La v3 parte de la noche cálida del local. Sobre ella van dos acentos que salen de lo más reconocible de Almud: el **muro rosa** de la barra y el **letrero ALMUD BAR** azul y blanco. Hay además tres fondos planos de sección.

- **Tokens:** `css/v3/tokens.css`.
- **Lámina:** `_plan/v3/04-paleta.jpg` (colores, recortes de las fotos de origen y 5 pantallas tipo).

## Método

Usé k-means con k=7 en sklearn, sobre píxeles muestreados (miniaturas de 160 px y hasta 6.000 píxeles por imagen). También corrí un k=5 extra solo con los píxeles saturados (S>0,5 y V>0,35).

| Grupo | Material | Clusters k=7 (por peso) | Saturados |
|---|---|---|---|
| Noche cálida | 27 de las 30 mejores fotos (`ranking.csv`, luz "noche cálida") | #1f0f0e 22% · #4e2b23 20% · #8d3821 14% · #e29b75 13% · #926b5b 12% · #d5593a 11% · #eecebf 8% | #d56c46, #f19e62, #c92e23 |
| Muro rosa | P362 `Dbok2NyFNdb_05`, P184 `DM_Ih5dyVKH_02` (mitad superior) | #210d09 · **#f24350** 17% · #f39977 · #612a1d · #bb6941 · **#ac2527** · #fcdec8 | #f3414f, #b7202b |
| Letrero | frame `V031_letrero_0.87s` (recorte central) | #050307 81% · **#f9f8f9** · **#2aa1f8** · #2a2b39 · … · #225aa5 | #1a9dfc, #20549e, **#15316e** |
| Afiches | 21 filas `kind=afiche` de `catalogo.csv` | #090808 41% · #2b2420 25% · #505458 · #892f1e · #f2ebe2 · #959590 · #d18a39 | #c8382e, **#d59f31** (dorado), #1f8a79 |
| Carta | `carta_2_Cocteleria_De_La_Casa.pdf`, pág. 1 | papel #ececed/#fbfbfb · tinta de nombres #4346db–#6a6cdc · precios #db67b2 | — |

Lo que mostró el análisis:

- El 60% de la luz de las fotos es una noche marrón y cálida, no negra ni violeta.
- El único color saturado que es *del lugar* (no de un afiche puntual) es el rojo-rosa del muro.
- El azul solo existe en el letrero y en la carta.
- Los afiches son negros con un acento dorado o rojo.

Por eso la v3 deja fuera el violeta, el verde cinta, el cielo y el magenta.

## Tokens

| Token | Hex | Rol | De dónde sale |
|---|---|---|---|
| `--noche` | `#160d0b` | **Fondo principal** | sombra dominante de las fotos de noche (#1f0f0e, 22%) llevada a fondo de pantalla |
| `--noche-2` | `#22140f` | Superficie (tarjetas, carta) | madera y penumbra del salón (#4e2b23) oscurecida |
| `--noche-3` | `#3a2219` | Superficie elevada, bordes | mismo cluster #4e2b23 |
| `--papel` | `#f5e9db` | **Texto principal**, fondo de pantalla clara | luz sobre la piel (#eecebf), crema de afiches (#f2ebe2), papel de la carta |
| `--papel-2` | `#c8af9c` | **Texto secundario** | marrón claro de las fotos (#926b5b) aclarado |
| `--letrero-blanco` | `#f9f8f9` | Logo "ALMUD" | blanco del letrero |
| `--muro-rosa` | `#f24350` | **ACENTO PRINCIPAL**: CTA, enlaces sobre noche | muro rosa de la barra (#f24350, 17% del grupo) |
| `--muro-rosa-tinta` | `#c41e34` | el mismo acento sobre papel | muro rosa en sombra (#b7202b) |
| `--letrero-azul` | `#2aa1f8` | **Acento secundario**: enlaces, foco, "BAR" | letrero ALMUD BAR (#2aa1f8 / #1a9dfc) |
| `--letrero-azul-tinta` | `#1d5fae` | el acento 2 sobre papel | letrero (#225aa5) y nombres de la carta |
| `--muro` | `#a8222d` | **Sección Tragos** (fondo plano) | sombra del muro rosa (#ac2527) |
| `--muro-2` | `#f7cfc4` | texto secundario en Tragos | rosa claro del muro iluminado (#fcdec8) |
| `--ambar` | `#e5a05c` | **Sección Comida** (fondo plano) | lámparas de mimbre, tragos (#e29b75, #f19e62) y dorado de afiches (#d59f31) |
| `--ambar-2` | `#4d2a1c` | texto secundario en Comida y en papel | madera (#4e2b23) |
| `--tinta` | `#142a5c` | **Sección Eventos** (fondo plano) | azul hondo del letrero (#15316e) y tinta de la carta |
| `--tinta-2` | `#b9c9ea` | texto secundario en Eventos | azul del letrero aclarado |

**Con quién** va sobre `--noche`, con fotos a sangre. Las pantallas de Portada, El lugar, Equipo, Reseñas y Dónde también usan `--noche` o `--noche-2`. **La carta** puede usar la pantalla clara: fondo `--papel` y texto `--noche`.

Alias semánticos en `tokens.css`: `--bg`, `--surface`, `--surface-2`, `--text`, `--text-2`, `--accent`, `--on-accent`, `--accent-2` y `--focus`.

## Reglas de uso (1–2 acentos por pantalla)

| Pantalla | Fondo | Texto / secundario | CTA (botón) | Enlaces y foco |
|---|---|---|---|---|
| Portada, Lugar, Con quién, Equipo, Dónde | `noche` | `papel` / `papel-2` | `muro-rosa` con texto `noche` | `letrero-azul` |
| Tragos | `muro` | `papel` / `muro-2` | `papel` con texto `noche` | `papel` subrayado; foco `papel` |
| Comida | `ambar` | `noche` / `ambar-2` | `noche` con texto `papel` | `noche` subrayado; foco `noche` |
| Eventos | `tinta` | `papel` / `tinta-2` | `muro-rosa` con texto `noche` | `papel`; foco `papel`; "próximo" en `muro-rosa` ≥24px |
| Carta / pantalla clara | `papel` | `noche` / `ambar-2` | `muro-rosa-tinta` con texto `papel` | `letrero-azul-tinta` |

- No se usan degradés arcoíris ni la franja `--rib`. Los colores de los banderines ya están en las fotos y no hace falta repetirlos en la interfaz.
- En una pantalla de sección, el color de sección **es** el acento: no se le suma el rosa, salvo en Eventos, donde el rosa marca el próximo evento.
- `--letrero-azul` va solo sobre `noche` o `noche-2`.

## Contraste WCAG 2.x, calculado con un script

El mínimo exigido es 4,5:1 para texto normal y 3:1 para texto ≥24px o para elementos que no son texto (anillo de foco).

| Texto | Fondo | Ratio | Mín. | Estado | Uso |
|---|---|---|---|---|---|
| `papel` | `noche` | 16.02 | 4.5 | OK | cuerpo |
| `papel` | `noche-2` | 14.95 | 4.5 | OK | cuerpo en superficie |
| `papel` | `noche-3` | 12.34 | 4.5 | OK | superficie elevada |
| `papel-2` | `noche` | 9.18 | 4.5 | OK | secundario |
| `papel-2` | `noche-2` | 8.57 | 4.5 | OK | secundario en superficie |
| `muro-rosa` | `noche` | 5.19 | 4.5 | OK | acento / enlace |
| `noche` | `muro-rosa` | 5.19 | 4.5 | OK | texto del botón CTA |
| `muro-rosa` | `noche-2` | 4.85 | 4.5 | OK | acento en superficie |
| `letrero-azul` | `noche` | 6.89 | 4.5 | OK | acento 2 / enlace / foco |
| `letrero-azul` | `noche-2` | 6.43 | 4.5 | OK | acento 2 en superficie |
| `letrero-blanco` | `noche` | 18.08 | 4.5 | OK | logo |
| `noche` | `papel` | 16.02 | 4.5 | OK | pantalla clara, botón papel |
| `ambar-2` | `papel` | 10.56 | 4.5 | OK | secundario en papel |
| `muro-rosa-tinta` | `papel` | 4.90 | 4.5 | OK | acento sobre papel |
| `papel` | `muro-rosa-tinta` | 4.90 | 4.5 | OK | CTA en pantalla clara |
| `letrero-azul-tinta` | `papel` | 5.32 | 4.5 | OK | enlace sobre papel |
| `papel` | `muro` | 5.99 | 4.5 | OK | Tragos: texto y foco |
| `muro-2` | `muro` | 5.01 | 4.5 | OK | Tragos: secundario |
| `noche` | `ambar` | 8.68 | 4.5 | OK | Comida: texto y foco |
| `ambar-2` | `ambar` | 5.72 | 4.5 | OK | Comida: secundario |
| `papel` | `tinta` | 11.59 | 4.5 | OK | Eventos: texto y foco |
| `tinta-2` | `tinta` | 8.32 | 4.5 | OK | Eventos: secundario |
| `muro-rosa` | `tinta` | 3.76 | 3.0 | OK solo ≥24px | Eventos: marca "próximo" |

**Pares que fallaron y se corrigieron**

| Par | Ratio | Corrección |
|---|---|---|
| `papel` sobre `muro-rosa` | 3.08 | El texto del CTA es `noche` (5.19). |
| `letrero-azul` sobre `papel` | 2.33 | Se creó `letrero-azul-tinta` #1d5fae (5.32). |
| `muro-rosa` como texto sobre `papel` | 3.08 | Se creó `muro-rosa-tinta` #c41e34 (4.90). |
| `noche` sobre `muro` | 2.67 | En Tragos el texto es `papel` (5.99). |
| `letrero-azul` sobre `muro` y sobre `ambar` | 2.58 / 1.26 | El foco en esas secciones usa `papel` y `noche`. |

## Equivalencias con la v1

| v1 | v3 |
|---|---|
| `--noche` #150b12 (violáceo) | `--noche` #160d0b (marrón cálido, el de las fotos) |
| `--barra` #ff3f6c | `--muro-rosa` #f24350 (el valor medido en el muro) |
| `--guinda` | `--muro` |
| `--pisco` y `--brasa` | `--ambar` |
| `--azul` y `--cielo` | `--letrero-azul` y `--tinta` |
| `--violeta`, `--magenta`, `--cinta`, `--rib` | se eliminan |


## Cambios de Carmen Paz (validación fases 3-4)
Ver `_plan/v3/03-04-validacion-carmen.md`. Aplicados en `css/v3/tokens.css`: papel-2 #d8c2b0; Comida sobre noche-2 con ámbar solo de acento; Eventos en tinta solo con foto o afiche; nuevo `--dorado` #d9a441 para "próximo"; azul solo en "BAR", foco y enlaces chicos; precios en papel; botones radio 4 px, 600, ≥48 px; sin "Reservar" (los botones son Ver la carta, Escríbenos por DM, Cómo llegar).
