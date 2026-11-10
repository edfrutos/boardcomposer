# Revisión de planificación — 2026-11-10

**Origen:** cron diario; corte tras `#880` (IDE-0218) en `main`.
PRs de producto abiertos: **0**. Issues abiertos: **0**.
Planning `#877` / `REVIEW-2026-11-09-planificacion.md` **mergeado**
(histórico; entonces residual ola 47: 0216…0218 🔵; ahora ola 47 🟢
`#878`/`#879`/`#880`, cola implementable vacía).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-11-09-planificacion.md`, PRs `#877`…`#880`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#878`/`#879`/`#880` **mergeados**
(IDE-0216…0218). Planning `#877` mergeado. Sin PRs abiertos.
Cola implementable residual: **vacía**.
Residual diferido (no cola): IDE-0101/0102 ⚪ (sin costes).
Residual bloqueado: piloto DT-0006 D + IDE-0008 / LLM / DT-0006 C.
**Planning previo:** `#877` / `REVIEW-2026-11-09` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| Core 2D (modelos, geometría, pipeline, Skyline/MaxRects, Beam Search) | 🟢 Base Fase 1 |
| Multipanel MaxRects **y** Skyline (material + espesor, retales, parciales) | 🟢 (#623) |
| CP-SAT un panel (opcional) | 🟢 Explorado |
| Studio: Workspace, Inspector, comandos, persistencia `.bcproj` | 🟢 Núcleo usable |
| Comparador SCR-003, Timeline, Preferencias, Welcome | 🟢 |
| QoL tips honesty / Welcome / barra estado / Timeline (ciclo `0.4.3`) | 🟢 |
| IDE-0019…0218 (swap, kerf, grain, cut list, catalog, quote, status QoL…) | 🟢 en `main` |
| IDE-0215 copiar la cuota del menor retal | 🟢 (#876) |
| IDE-0216 clic en la cuota del menor retal selecciona su solución | 🟢 (#878) |
| IDE-0217 barra: relación de forma del mayor retal (`relr.` / `aspr`) | 🟢 (#879) |
| IDE-0218 copiar la relación de forma del mayor retal | 🟢 (#880) |
| IDE-0219 clic en la relación de forma del mayor retal selecciona su solución | 🔵 |
| IDE-0220 barra: relación de forma del menor retal (`relm.` / `asps`) | 🔵 |
| IDE-0221 copiar la relación de forma del menor retal | 🔵 |
| IDE-0222 clic en la relación de forma del menor retal selecciona su solución | 🔵 |
| IDE-0101 barra: coste de la solución seleccionada | ⚪ Diferido (sin costes) |
| IDE-0102 copiar el coste de la solución | ⚪ Diferido (sin costes) |
| Import CSV/Excel; export SVG/DXF/PDF/JSON/CSV + plantillas | 🟢 |
| Fase 3: EP-001 API `v1`, EP-002 batch, EP-003 HTTP/Docker | 🟢 Entregada |
| IDE-0007 explicación local (sin LLM) | 🟢 MVP + eval humana (2026-09-12) |
| IDE-0008 plugins | ⚪ Visión Fase 5 |
| DT-0006 historial cloud | 🟡 Piloto D (backup); C diferida |

Detalle de ideas: `DOC-004-Backlog.md`.

---

## 2. Planificación de construcción

| Fase | Estado | Notas |
|------|--------|-------|
| 0 Fundamentos | 🟢 | Repo, CI, ADR |
| 1 Core 2D | 🟢 Base | Extensiones controladas (kerf, grain, Skyline MP, freeze) |
| 2 Studio | 🟡 En curso | Núcleo usable; pulido continuo |
| 3 Plataforma | 🟢 | EP-001…003 cerradas (corte 2026-07) |
| 4 Inteligencia | ⚪ | IDE-0007 MVP+eval; LLM bajo política |
| 5 Ecosistema | ⚪ | Plugins / marketplace |

Versión: desarrollo `0.4.4.dev0` · estable `0.4.3` (2026-09-14;
etiqueta `v0.4.3` **publicada** 2026-09-16 — latest GitHub Releases).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; cola
producto IDE-0019…0024 **cerrada** en `0.4.3`; olas `0.4.4.dev0`
0025…0218 **cerradas** en `main` (`#631`…`#880`; IDE-0101/0102
diferidas ⚪). Cuadragésima séptima ola 0215…0218 **cerrada**
(`#876`/`#878`/`#879`/`#880`). Cuadragésima octava ola 0219…0222
**planificada** (nueva; 🔵).

Desde la revisión 2026-11-09 (PR `#877`, mergeado): mergeados `#878`/
`#879`/`#880` (IDE-0216…0218). Sin PRs de producto abiertos.
Issues = 0. Criterio del cron **cumplido** para nuevas IDE: cola
implementable vacía + bugs cerrados → **sí se añaden IDE-0219…0222**.

Límites conocidos (no son bugs; son alcance):

- Retales se reportan (ADR-016) y se pueden promover a inventario del
  mismo `.bcproj` (IDE-0025); no hay librería de retales entre proyectos.
- CP-SAT exacto sigue siendo un solo panel (opcional).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.
- Catálogo de usuario (IDE-0028/0031) guarda nombre / espesor / €/m² /
  L×A; export/import JSON (IDE-0042 `#655`). Sin nube.
- Etiquetas de plano cubren piezas (IDE-0026), retales LxW (IDE-0033) y
  cotas L×A del tablero (IDE-0037) y pie de trazabilidad (IDE-0039);
  lista de corte / presupuesto PDF (IDE-0043). Etiquetas de plano siguen
  `prefs.units` (IDE-0044); geometría / JSON / `$INSUNITS` en mm.
- Coste (IDE-0029) y presupuesto PDF (IDE-0032) cubren material de
  tableros físicos; mano de obra opcional (IDE-0045 `#659`) vía EUR/h y
  minutos/pieza en Preferencias. Sigue sin herrajes. Coste *por
  solución* en barra (IDE-0101/0102) diferido.
- Export PDF: papel/márgenes/escala en plano (IDE-0034); lote de
  candidatas Studio (IDE-0035). Raster PNG/JPEG: DPI y calidad JPEG
  (IDE-0038). Capas DXF por rol (IDE-0041 `#654`). Sin nube.
- Workspace: sugerir hueco (IDE-0036); preview al terminar solve
  (IDE-0052); zoom 100% / clic zoom (IDE-0056/0062); copiar zoom
  (IDE-0091).
- Barra de estado (SCR-005): colocadas/total, omitidas, selección, kerf,
  tableros físicos, espesor/material/aprovechamiento/libre del tablero
  enfocado, zoom, retales (`n ret.`, IDE-0092…0094), índice de solución
  (`1/2 sol.`, IDE-0095…0097), huecos internos (`hueco n%`, IDE-0098…
  0100), estrategia (`est. …`, IDE-0103…0105), piezas (`n pza`,
  IDE-0106…0108), omitidas de solución (`fuera n`, IDE-0109…0111),
  tableros de solución (`pan. n`, IDE-0112…0114), puntuación
  (`pts. …`, IDE-0115…0117), tablero libre (`sbr. …`, IDE-0118…0120),
  largo total (`lrg. …`, IDE-0121…0123), ancho total (`anc. …`,
  IDE-0124…0126), área usada (`ár. …`, IDE-0127…0129), área de retales
  (`retár. …`, IDE-0130…0132), área envolvente (`env. …`, IDE-0133…
  0135), área de huecos internos (`hueár. …`, IDE-0136…0138), área de
  tablero libre (`sbrár. …`, IDE-0139…0141), área de tableros consumidos
  (`panár. …`, IDE-0142…0144), aprovechamiento (`aprv. …`,
  IDE-0145…0147), piezas rotadas (`rot. …`, IDE-0148…0150), piezas sin
  rotar (`nrot. …`, IDE-0151…0153), porcentaje rotadas (`rot% …`,
  IDE-0154…0156), porcentaje sin rotar (`nrot% …`, IDE-0157…0159),
  aprovechamiento envolvente (`env% …`, IDE-0160…0162), porcentaje de
  retales (`ret% …`, IDE-0163…0165), puntuación de desperdicio
  (`ptsh. …`, IDE-0166…0168), puntuación de uso de material
  (`ptsu. …`, IDE-0169…0171), puntuación de cortes (`ptsc. …`,
  IDE-0172…0174), puntuación de regularidad (`ptsr. …`,
  IDE-0175…0177), puntuación de veta (`ptsv. …`, IDE-0178…0180),
  completitud (`comp. sí`/`comp. no`, IDE-0181…0183), área del mayor
  retal (`maxr. {area}` / `maxo {area}`, IDE-0184…0186 🟢), área del
  menor retal (`minr. {area}` / `mino {area}`, IDE-0187…0189 🟢),
  dimensiones del mayor retal (`maxd. {size}` / `maxd {size}`,
  IDE-0190…0192 🟢), dimensiones del menor retal (`mind. {size}` /
  `mind {size}`, IDE-0193…0195 🟢), área media de retales
  (`medr. {area}` / `avgo {area}`, IDE-0196…0198 🟢), área mediana
  (`mdnr. {area}` / `medo {area}`, IDE-0199…0201 🟢 `#857`…`#859`),
  dimensiones del retal de área mediana (`mdnd. {size}` / `medd {size}`,
  IDE-0202…0204 🟢 `#860`…`#862`), dimensiones del retal de área media
  (`mdds. {size}` / `avgd {size}`, IDE-0205…0207 🟢 `#863`…`#865`),
  amplitud de áreas de retales (`ampr. {area}` / `spno {area}`,
  IDE-0208…0210 🟢 `#866`/`#868`/`#869`), cuota del mayor retal
  (`cmay. {value}` / `lsh {value}`, IDE-0211…0213 🟢 `#870`/`#872`/
  `#874`), cuota del menor retal (`cmen. {value}` / `ssh {value}`,
  IDE-0214…0216 🟢 `#875`/`#876`/`#878`), relación de forma del mayor
  retal (`relr. {value}` / `aspr {value}`, IDE-0217…0218 🟢 `#879`/
  `#880`; clic IDE-0219 🔵; relación del menor `relm.`/`asps`
  IDE-0220…0222 🔵).
- Inspector: unidades prefs mm/cm/in; disco sigue mm. Prefs:
  export/import JSON; perfiles nombrados locales; sin nube.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` cuadragésima octava ola** — implementar IDE-0219
   (clic en `relr.` / `aspr` selecciona su solución); luego IDE-0220
   (barra: relación de forma del menor retal `relm.` / `asps`); luego
   IDE-0221 (copiar relación; Ctrl+Alt+Shift+\`); luego IDE-0222
   (clic en `relm.` / `asps` selecciona su solución).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C / IDE-0101–0102 sin ADR
   o decisión vigente (eval IDE-0007 ya cerrada; LLM sigue diferido
   DEC-0011; coste por solución diferido).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0215…0218: **cerrada** en `main` (`#876`/`#878`/`#879`/`#880`).
En cola (nueva): IDE-0219…0222 🔵 (cuadragésima octava ola). Diferidas
(fuera de cola): IDE-0101/0102 ⚪. Residual bloqueado: piloto DT-0006 D
(operativo) + IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → cola vacía + Issues = 0 →
**sí se añaden IDE-0219…0222**. Ancladas a límites ya escritos:
`relr.` click cierra el trío show/copy/click del mayor; `relm.`/`asps`
= max(L,A)/min(L,A) del retal de menor área (empate como `mind.`;
distinta de `mind.` y de `relr.`); copy sin prefijo.

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0219 | Clic en la relación de forma del mayor retal selecciona su solución | Cierra trío `relr.`/`aspr`; click → `solution:{index}`; arrastre no |
| IDE-0220 | Barra: relación de forma del menor retal | `relm. {value}` / `asps {value}`; simetría de `relr.` |
| IDE-0221 | Copiar la relación de forma del menor retal | Valor sin `relm.`; Ctrl+Alt+Shift+\` |
| IDE-0222 | Clic en la relación de forma del menor retal selecciona su solución | Simetría click → `solution:{index}`; arrastre no |

Prioridad de ataque: **IDE-0219** → 0220 → 0221 → 0222.

Cuadragésima octava ola (no renumerar; **nueva**):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0219 | Clic en la relación de forma del mayor retal selecciona su solución | 🔵 |
| IDE-0220 | Barra: relación de forma del menor retal | 🔵 |
| IDE-0221 | Copiar la relación de forma del menor retal | 🔵 |
| IDE-0222 | Clic en la relación de forma del menor retal selecciona su solución | 🔵 |

Olas ya cerradas en este ciclo (no renumerar):

| Ola | IDs | Estado |
|-----|-----|--------|
| Decimoctava | 0099…0100 (+ 0101/0102 diferidas) | 🟢 / ⚪ |
| Decimonovena | 0103…0106 | 🟢 |
| Vigésima | 0107…0110 | 🟢 |
| Vigesimoprimera | 0111…0114 | 🟢 |
| Vigesimosegunda | 0115…0118 | 🟢 |
| Vigesimotercera | 0119…0122 | 🟢 |
| Vigesimocuarta | 0123…0126 | 🟢 |
| Vigesimoquinta | 0127…0130 | 🟢 |
| Vigesimosexta | 0131…0134 | 🟢 |
| Vigesimoséptima | 0135…0138 | 🟢 |
| Vigesimoctava | 0139…0142 | 🟢 |
| Vigesimonovena | 0143…0146 | 🟢 |
| Trigésima | 0147…0150 | 🟢 |
| Trigésima primera | 0151…0154 | 🟢 |
| Trigésima segunda | 0155…0158 | 🟢 |
| Trigésima tercera | 0159…0162 | 🟢 |
| Trigésima cuarta | 0163…0166 | 🟢 |
| Trigésima quinta | 0167…0170 | 🟢 |
| Trigésima sexta | 0171…0174 | 🟢 |
| Trigésima séptima | 0175…0178 | 🟢 |
| Trigésima octava | 0179…0182 | 🟢 |
| Trigésima novena | 0183…0186 | 🟢 |
| Cuadragésima | 0187…0190 | 🟢 |
| Cuadragésima primera | 0191…0194 | 🟢 |
| Cuadragésima segunda | 0195…0198 | 🟢 |
| Cuadragésima tercera | 0199…0202 | 🟢 |
| Cuadragésima cuarta | 0203…0206 | 🟢 |
| Cuadragésima quinta | 0207…0210 | 🟢 |
| Cuadragésima sexta | 0211…0214 | 🟢 |
| Cuadragésima séptima | 0215…0218 | 🟢 |

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0100,
IDE-0103…0218.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).
Planificadas (cuadragésima octava ola): IDE-0219…0222.

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; confirmar IDE-0216…0218 🟢 (`#878`/`#879`/`#880`)
  y abrir IDE-0219…0222 🔵. `#877` / `REVIEW-2026-11-09` queda histórico.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0219…0222 mergean y la cola queda vacía → proponer nueva ola IDE.
