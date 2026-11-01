# Revisión de planificación — 2026-11-01

**Origen:** cron diario; corte tras `#841` (IDE-0187) en `main`.
PRs de producto abiertos: **`#842`** (IDE-0188). Issues abiertos: **0**.
Planning `#839` / `REVIEW-2026-10-31-planificacion.md` **mergeado**
(histórico; entonces 0185 🟡 `#838` + 0186 🔵; ahora
0185…0187 🟢 `#838`/`#840`/`#841`, cuadragésima ola 0187…0190: 0187
🟢; 0188 🟡 `#842`; 0189…0190 🔵).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-10-31-planificacion.md`, PRs `#838`…`#842`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#838`/`#840`/`#841` **mergeados**
(IDE-0185…0187). Abierto: `#842` (IDE-0188).
Cola implementable residual: IDE-0188 🟡 + IDE-0189…0190 🔵.
Residual diferido (no cola): IDE-0101/0102 ⚪ (sin costes).
Residual bloqueado: piloto DT-0006 D + IDE-0008 / LLM / DT-0006 C.
**Planning previo:** `#839` / `REVIEW-2026-10-31` queda histórico.

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
| IDE-0019…0187 (swap, kerf, grain, cut list, catalog, quote, status QoL…) | 🟢 en `main` |
| IDE-0185 copiar el área del mayor retal de la solución | 🟢 (#838) |
| IDE-0186 clic en el área del mayor retal selecciona su solución | 🟢 (#840) |
| IDE-0187 barra: área del menor retal de la solución seleccionada | 🟢 (#841) |
| IDE-0188 copiar el área del menor retal de la solución | 🟡 (#842) |
| IDE-0189 clic en el área del menor retal selecciona su solución | 🔵 |
| IDE-0190 barra: dimensiones del mayor retal de la solución | 🔵 |
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
0025…0187 **cerradas** en `main` (`#631`…`#841`; IDE-0101/0102
diferidas ⚪). Trigésima novena ola 0183…0186 **cerrada**
(`#836`…`#840`). Cuadragésima ola 0187…0190 **abierta**
(0187 🟢 `#841`; 0188 🟡 `#842`; 0189…0190 🔵).

Desde la revisión 2026-10-31 (PR `#839`, mergeado): mergeados
`#838`/`#840`/`#841` (IDE-0185…0187). Issues = 0. PR abierto = `#842`.
Criterio del cron **no** cumplido para nuevas IDE fuera de esa ola:
queda cola implementable residual (0188…0190). IDs ya fijados por
producto (`#841` abrió 0187…0190) — **no renumerar**.

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
  menor retal (`minr. {area}` / `mino {area}`, IDE-0187 🟢 `#841`;
  copiar IDE-0188 🟡 `#842`; clic IDE-0189 🔵; dimensiones mayor
  retal IDE-0190 🔵).
- Inspector: unidades prefs mm/cm/in; disco sigue mm. Prefs:
  export/import JSON; perfiles nombrados locales; sin nube.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` cuadragésima ola** — cerrar IDE-0188 🟡 `#842`
   (copiar área menor retal; Ctrl+Alt+Shift+F9; valor sin `minr.`);
   luego IDE-0189 (clic en `minr.` selecciona su solución); luego
   IDE-0190 (barra: dimensiones L×A del mayor retal).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C / IDE-0101–0102 sin ADR
   o decisión vigente (eval IDE-0007 ya cerrada; LLM sigue diferido
   DEC-0011; coste por solución diferido).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0185…0187: **cerrada** en `main` (`#838`/`#840`/`#841`). En cola
(producto `#842`): IDE-0188 🟡 + IDE-0189…0190 🔵 (cuadragésima ola).
Diferidas (fuera de cola): IDE-0101/0102 ⚪. Residual bloqueado: piloto
DT-0006 D (operativo) + IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → residual implementable **no**
vacío → **sin IDE nuevas del cron**. IDs 0187…0190 ya fijados por
producto (`#841`) — no renumerar. Ancladas a límites ya escritos:
`minr.` (IDE-0187) cerrado en `main`; falta copy/click simétricos
(IDE-0188/0189) y dimensiones del mayor retal (IDE-0190).

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0188 | Copiar el área del menor retal de la solución | Valor sin prefijo `minr.`; Ctrl+Alt+Shift+F9 (`#842`) |
| IDE-0189 | Clic en el área del menor retal selecciona su solución | Simetría click → `solution:{index}`; arrastre no |
| IDE-0190 | Barra: dimensiones del mayor retal de la solución | `maxd. {L}×{A}` / `maxd {L}×{W}`; distinta de `maxr.` |

Prioridad de ataque: **IDE-0188** (luego 0189, luego 0190).

Cuadragésima ola (no renumerar; **abierta**; 0187 ya 🟢):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0187 | Barra: área del menor retal de la solución seleccionada | 🟢 (#841) |
| IDE-0188 | Copiar el área del menor retal de la solución | 🟡 (#842) |
| IDE-0189 | Clic en el área del menor retal selecciona su solución | 🔵 |
| IDE-0190 | Barra: dimensiones del mayor retal de la solución | 🔵 |

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

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0100,
IDE-0103…0187.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).
En curso (cuadragésima ola): IDE-0188…0190 (0187 ya 🟢).

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; confirmar IDE-0185…0187 🟢 (`#838`/`#840`/`#841`)
  y alinear residual IDE-0188 🟡 `#842` + IDE-0189…0190 🔵 (IDs del
  producto; sin inventar ola nueva). `#839` / `REVIEW-2026-10-31`
  queda histórico.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0188…0190 mergean y la cola queda vacía → proponer nueva ola IDE.
