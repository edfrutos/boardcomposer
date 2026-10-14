# Revisión de planificación — 2026-10-14

**Origen:** cron diario; corte tras `#737` (IDE-0099) en `main`;
`#738` (IDE-0100) **abierto** (CI en curso al corte). Planning `#732`
(2026-10-13) **mergeado**; no hay planning draft previo que plegar.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-10-13-planificacion.md`, PRs `#731`…`#738`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#731`…`#737` **mergeados**
(IDE-0094…0099). `#738` **abierto** (IDE-0100; CI in progress).
Residual implementable: IDE-0100 🟡 + IDE-0101/0102 🔵. Residual
bloqueado: piloto DT-0006 D + IDE-0008 / LLM / DT-0006 C.
**Planning previo:** `#732` (2026-10-13) mergeado — queda histórico
`REVIEW-2026-10-13-planificacion.md` (superseded; cola ahora 0100…0102).

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
| IDE-0019…0093 (swap, kerf, grain, cut list, catalog, quote, status QoL…) | 🟢 en `main` |
| IDE-0094 clic en retales selecciona su tablero | 🟢 (#731) |
| IDE-0095 barra: índice de la solución seleccionada | 🟢 (#733) |
| IDE-0096 copiar el índice de la solución | 🟢 (#734) |
| IDE-0097 clic en el índice pasa a la siguiente solución | 🟢 (#735) |
| IDE-0098 barra: huecos internos de la solución seleccionada | 🟢 (#736) |
| IDE-0099 copiar los huecos internos de la barra | 🟢 (#737) |
| IDE-0100 clic en huecos selecciona su solución | 🟡 (#738) |
| IDE-0101 barra: coste de la solución seleccionada | 🔵 |
| IDE-0102 copiar el coste de la solución | 🔵 |
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
0025…0099 **cerradas** en `main` (`#631`…`#737`).

Desde la revisión 2026-10-13 (PR `#732` mergeado): **`#731`…`#737`
mergeados** (IDE-0094…0099); **`#738` abierto** (IDE-0100). Snapshot
`REVIEW-2026-10-13` queda histórico (cola residual entonces 0094;
ahora 0100…0102).

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
  minutos/pieza en Preferencias. Sigue sin herrajes.
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
  0099). Decimoctava ola residual: clic en huecos (IDE-0100 `#738`) +
  coste de solución (IDE-0101/0102).
- Inspector: unidades prefs mm/cm/in; disco sigue mm. Prefs:
  export/import JSON; perfiles nombrados locales; sin nube.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` decimoctava ola residual** — cerrar IDE-0100 🟡 `#738`
   (clic en huecos selecciona su solución); luego IDE-0101 y IDE-0102.
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0094…0099: **cerrada** en `main` (`#731`…`#737`). En curso: IDE-0100 🟡
`#738`. Planificada: IDE-0101/0102 🔵. Residual bloqueado: piloto
DT-0006 D (operativo) + IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → decimoctava ola residual
IDE-0100…0102 abierta; **no se añaden IDE nuevas** hasta cerrarla.

Decimoctava ola (no renumerar):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0099 | Copiar los huecos internos de la barra | 🟢 `#737` |
| IDE-0100 | Clic en huecos selecciona su solución | 🟡 `#738` |
| IDE-0101 | Barra: coste de la solución seleccionada | 🔵 |
| IDE-0102 | Copiar el coste de la solución | 🔵 |

Prioridad de ataque: **cerrar IDE-0100** (`#738`); luego 0101 → 0102.

Decimoséptima ola ya registrada (no renumerar):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0095…0098 | (ver DOC-004) | 🟢 en `main` |

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0099.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).
En desarrollo (decimoctava ola residual): IDE-0100…0102.

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; confirmar IDE-0094…0099 🟢 (`#731`…`#737`) e
  IDE-0100 🟡 (`#738`); IDE-0101/0102 🔵. `#732` /
  `REVIEW-2026-10-13` queda histórico.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0100…0102 mergean y la cola queda vacía → proponer nueva ola IDE.
