# Revisión de planificación — 2026-10-16

**Origen:** cron diario; corte tras `#747` (IDE-0109) en `main`;
`#748` (IDE-0110) **abierto** (CI verde al corte; mergeable).
Planning `#744` (2026-10-15) ya mergeado. Planning `#739`
(2026-10-14) sigue **open/conflicting** sin mergear — se pliega como
histórico `REVIEW-2026-10-14-planificacion.md` / `REVIEW-2026-10-15`
(superseded).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-10-15-planificacion.md` (desde `#744`), PRs
`#743`…`#748`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#743`…`#747` **mergeados**
(IDE-0106…0109). `#748` **abierto** (IDE-0110; CI test OK).
Residual implementable: IDE-0110 🟡. Residual diferido (no cola):
IDE-0101/0102 ⚪ (sin costes). Residual bloqueado: piloto DT-0006 D +
IDE-0008 / LLM / DT-0006 C.
**Planning previo:** `#744` / `REVIEW-2026-10-15` mergeado (cola entonces
0106 🟡; ahora 0110 🟡). `#739` / `REVIEW-2026-10-14` sigue
open/conflicting → histórico.

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
| IDE-0019…0100 (swap, kerf, grain, cut list, catalog, quote, status QoL…) | 🟢 en `main` |
| IDE-0101 barra: coste de la solución seleccionada | ⚪ Diferido (sin costes) |
| IDE-0102 copiar el coste de la solución | ⚪ Diferido (sin costes) |
| IDE-0103 barra: estrategia de la solución seleccionada | 🟢 (#740) |
| IDE-0104 copiar la estrategia | 🟢 (#741) |
| IDE-0105 clic en la estrategia selecciona su solución | 🟢 (#742) |
| IDE-0106 barra: piezas de la solución seleccionada | 🟢 (#743) |
| IDE-0107 copiar las piezas de la solución | 🟢 (#745) |
| IDE-0108 clic en las piezas selecciona su solución | 🟢 (#746) |
| IDE-0109 barra: omitidas de la solución seleccionada | 🟢 (#747) |
| IDE-0110 copiar las omitidas de la solución | 🟡 (#748) |
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
0025…0109 **cerradas** en `main` (`#631`…`#747`; IDE-0101/0102
diferidas ⚪).

Desde la revisión 2026-10-15 (PR `#744` mergeado): **`#743`…`#747`
mergeados** (IDE-0106…0109); **`#748` abierto** (IDE-0110).
Planning `#739` / `REVIEW-2026-10-14` sigue open/conflicting → histórico
(superseded; cola residual entonces 0100; ahora 0110 🟡).
`REVIEW-2026-10-15` queda histórico (superseded; cola entonces 0106).

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
  0100), estrategia (`est. …`, IDE-0103…0105), piezas de la solución
  (`n pza`, IDE-0106…0108), omitidas de la solución (`fuera n`,
  IDE-0109). Vigésima ola residual: copiar omitidas (IDE-0110 `#748`).
- Inspector: unidades prefs mm/cm/in; disco sigue mm. Prefs:
  export/import JSON; perfiles nombrados locales; sin nube.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` vigésima ola residual** — cerrar IDE-0110 🟡 `#748`
   (copiar omitidas de la solución; Ctrl+Alt+Shift+Q; CI ya verde).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C / IDE-0101–0102 sin ADR
   o decisión vigente (eval IDE-0007 ya cerrada; LLM sigue diferido
   DEC-0011; coste por solución diferido).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0106…0109: **cerrada** en `main` (`#743`…`#747`). En curso:
IDE-0110 🟡 `#748`. Diferidas (fuera de cola): IDE-0101/0102 ⚪.
Residual bloqueado: piloto DT-0006 D (operativo) + IDE-0008 / LLM /
DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → vigésima ola residual
IDE-0110 abierta; **no se añaden IDE nuevas** hasta cerrarla.

Vigésima ola (no renumerar):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0107 | Copiar las piezas de la solución | 🟢 `#745` |
| IDE-0108 | Clic en las piezas selecciona su solución | 🟢 `#746` |
| IDE-0109 | Barra: omitidas de la solución seleccionada | 🟢 `#747` |
| IDE-0110 | Copiar las omitidas de la solución | 🟡 `#748` |

Prioridad de ataque: **cerrar IDE-0110** (`#748`; CI verde).

Decimonovena ola ya registrada (no renumerar):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0103…0106 | (ver DOC-004) | 🟢 en `main` |
| IDE-0101…0102 | Coste en barra | ⚪ Diferidas |

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0100,
IDE-0103…0109.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).
En desarrollo (vigésima ola residual): IDE-0110.

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; confirmar IDE-0106…0109 🟢 (`#743`…`#747`) e
  IDE-0110 🟡 (`#748`). `#744` / `REVIEW-2026-10-15`, `#739` /
  `REVIEW-2026-10-14` quedan histórico.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0110 mergea y la cola queda vacía → proponer nueva ola IDE.
