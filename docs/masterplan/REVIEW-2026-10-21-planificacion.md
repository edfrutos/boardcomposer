# Revisión de planificación — 2026-10-21

**Origen:** cron diario; corte tras `#777` (IDE-0134) en `main`.
Sin PRs de producto abiertos. Planning `#774` /
`REVIEW-2026-10-20-planificacion.md` **mergeado** (histórico;
residual entonces 0132…0134 🔵; ahora 0132…0134 🟢).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-10-20-planificacion.md`, PRs `#774`…`#777`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#775`…`#777` **mergeados**
(IDE-0132…0134). Cola implementable **vacía**.
Residual diferido (no cola): IDE-0101/0102 ⚪ (sin costes).
Residual bloqueado: piloto DT-0006 D + IDE-0008 / LLM / DT-0006 C.
**Planning previo:** `#774` / `REVIEW-2026-10-20` queda histórico
(superseded).

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
| IDE-0019…0134 (swap, kerf, grain, cut list, catalog, quote, status QoL…) | 🟢 en `main` |
| IDE-0132 clic en el área de retales selecciona su solución | 🟢 (#775) |
| IDE-0133 barra: área envolvente de la solución seleccionada | 🟢 (#776) |
| IDE-0134 copiar el área envolvente de la solución | 🟢 (#777) |
| IDE-0135 clic en el área envolvente selecciona su solución | 🔵 |
| IDE-0136 barra: área de huecos internos de la solución seleccionada | 🔵 |
| IDE-0137 copiar el área de huecos internos de la solución | 🔵 |
| IDE-0138 clic en el área de huecos internos selecciona su solución | 🔵 |
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
0025…0134 **cerradas** en `main` (`#631`…`#777`; IDE-0101/0102
diferidas ⚪). Vigesimosexta ola 0131…0134 **cerrada**; cola
implementable vacía → **vigesimoséptima ola** IDE-0135…0138 🔵.

Desde la revisión 2026-10-20 (PR `#774`): mergeados `#775`…`#777`
(IDE-0132…0134). Issues = 0. Criterio del cron cumplido → se registran
IDE nuevas.

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
  (`retár. …`, IDE-0130…0132), área envolvente (`env. …`, IDE-0133…0134;
  clic IDE-0135 🔵). Vigesimoséptima ola: área de huecos internos
  (`hueár. …`, IDE-0136…0138; complemento absoluto a `hueco n%`).
- Inspector: unidades prefs mm/cm/in; disco sigue mm. Prefs:
  export/import JSON; perfiles nombrados locales; sin nube.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` vigesimoséptima ola** — abrir/cerrar IDE-0135 🔵
   (clic en el área envolvente selecciona su solución); luego IDE-0136
   (barra: área de huecos internos), IDE-0137 (copiar) e IDE-0138 (clic).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C / IDE-0101–0102 sin ADR
   o decisión vigente (eval IDE-0007 ya cerrada; LLM sigue diferido
   DEC-0011; coste por solución diferido).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0131…0134: **cerrada** en `main` (`#772`, `#775`…`#777`). En cola sin PR:
IDE-0135…0138 🔵 (vigesimoséptima ola, **nueva**). Diferidas (fuera de
cola): IDE-0101/0102 ⚪. Residual bloqueado: piloto DT-0006 D
(operativo) + IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → cola vacía + Issues = 0 →
**sí se añaden IDE-0135…0138**. Ancladas a límites ya escritos: el área
envolvente (`env.`, IDE-0133/0134) aún no tiene clic simétrico; el
porcentaje de huecos (`hueco n%`, `waste_ratio`) aún no muestra su área
absoluta (`waste_area_mm2`, ya en el modelo).

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0135 | Clic en el área envolvente selecciona su solución | Simetría click → `solution:{index}` tras copy 0134 |
| IDE-0136 | Barra: área de huecos internos de la solución seleccionada | Complemento a `hueco n%`; `_format_area(waste_area_mm2)` |
| IDE-0137 | Copiar el área de huecos internos de la solución | Simetría copy; área con unidad, sin prefijo |
| IDE-0138 | Clic en el área de huecos internos selecciona su solución | Simetría click → `solution:{index}` |

Prioridad de ataque: **IDE-0135** (luego 0136 → 0137 → 0138).

Vigesimoséptima ola (no renumerar):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0135 | Clic en el área envolvente selecciona su solución | 🔵 |
| IDE-0136 | Barra: área de huecos internos de la solución seleccionada | 🔵 |
| IDE-0137 | Copiar el área de huecos internos de la solución | 🔵 |
| IDE-0138 | Clic en el área de huecos internos selecciona su solución | 🔵 |

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

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0100,
IDE-0103…0134.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).
Planificadas (vigesimoséptima ola): IDE-0135…0138.

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; confirmar IDE-0132…0134 🟢 (`#775`…`#777`) y
  abrir IDE-0135…0138 🔵. `#774` / `REVIEW-2026-10-20` queda histórico.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0135…0138 mergean y la cola queda vacía → proponer nueva ola IDE.
