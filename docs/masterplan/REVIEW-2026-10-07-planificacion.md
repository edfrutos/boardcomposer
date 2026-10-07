# Revisión de planificación — 2026-10-07

**Origen:** cron diario; corte tras `#721` (IDE-0091) en `main`; planning
`#722` (2026-10-06) sigue **draft** sin mergear.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-10-06-planificacion.md` (desde `#722`), PRs
`#718`…`#722`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#718`…`#721` **mergeados**
(IDE-0089…0091). Sin PR de producto abierto. Residual implementable:
IDE-0092…0094 🔵. Residual bloqueado: piloto DT-0006 D + IDE-0008 /
LLM / DT-0006 C.
**Planning previo:** `#722` (2026-10-06, draft) — se pliega aquí como
histórico `REVIEW-2026-10-06-planificacion.md` (superseded; misma cola
residual 0092…0094). También histórico: `#719` / `REVIEW-2026-10-05`.

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
| IDE-0019…0078 (swap, kerf, grain, cut list, catalog, quote, status QoL…) | 🟢 en `main` |
| IDE-0079 barra de estado: piezas omitidas | 🟢 (#706) |
| IDE-0080 clic en omitidas selecciona y encuadra las omitidas | 🟢 (#707) |
| IDE-0081 barra de estado: aprovechamiento del tablero enfocado | 🟢 (#709) |
| IDE-0082 clic en el aprovechamiento selecciona ese tablero | 🟢 (#710) |
| IDE-0083 copiar el aprovechamiento del tablero de la barra | 🟢 (#711) |
| IDE-0084 barra de estado: material libre del tablero enfocado | 🟢 (#712) |
| IDE-0085 copiar el material libre del tablero | 🟢 (#713) |
| IDE-0086 clic en el material libre selecciona ese tablero | 🟢 (#714) |
| IDE-0087 copiar piezas colocadas/total de la barra | 🟢 (#715) |
| IDE-0088 copiar las piezas omitidas de la barra | 🟢 (#716) |
| IDE-0089 copiar los tableros físicos de la barra | 🟢 (#718) |
| IDE-0090 copiar la selección de la barra | 🟢 (#720) |
| IDE-0091 copiar el zoom de la barra | 🟢 (#721) |
| IDE-0092 barra de estado: retales de la solución seleccionada | 🔵 |
| IDE-0093 copiar los retales de la barra | 🔵 |
| IDE-0094 clic en retales selecciona su tablero | 🔵 |
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
0025…0091 **cerradas** en `main` (`#631`…`#721`).

Desde la revisión 2026-10-06 (PR `#722` draft), **sin merge de producto**:
sigue vigente `#721` (IDE-0091). IDE-0092…0094 siguen 🔵 sin PR. Planning
`#722` / `REVIEW-2026-10-06` y `#719` / `REVIEW-2026-10-05` se pliegan
como histórico.

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
  enfocado, zoom, con clics y copias simétricas hasta IDE-0091.
  Decimosexta ola residual: retales de la solución (IDE-0092…0094).
- Inspector: unidades prefs mm/cm/in; disco sigue mm. Prefs:
  export/import JSON; perfiles nombrados locales; sin nube.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` decimosexta ola residual** — IDE-0092 🔵 (siguiente:
   IDE-0093 copiar retales; IDE-0094 clic en retales).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0079…0091: **cerrada** en `main` (`#706`…`#721`). Residual abierto
implementable: **IDE-0092…0094** 🔵. Residual bloqueado: piloto DT-0006 D
(operativo) + IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → decimosexta ola residual
IDE-0092…0094 abierta; **no se añaden IDE nuevas** hasta cerrarla.

Decimosexta ola (no renumerar):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0091 | Copiar el zoom de la barra | 🟢 `#721` |
| IDE-0092 | Barra de estado: retales de la solución seleccionada | 🔵 |
| IDE-0093 | Copiar los retales de la barra | 🔵 |
| IDE-0094 | Clic en retales selecciona su tablero | 🔵 |

Prioridad de ataque: **abrir IDE-0092** (barra `n ret.`); luego 0093 / 0094.

Decimoquinta ola ya registrada (no renumerar):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0087…0090 | (ver DOC-004) | 🟢 en `main` |

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0091.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).
En desarrollo / planificadas (decimosexta ola residual): IDE-0092…0094.

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; confirmar IDE-0091 🟢 (`#721`) e IDE-0092…0094 🔵.
  `#722` / `REVIEW-2026-10-06` y `#719` / `REVIEW-2026-10-05` quedan
  histórico.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0092…0094 mergean y la cola queda vacía → proponer nueva ola IDE.
