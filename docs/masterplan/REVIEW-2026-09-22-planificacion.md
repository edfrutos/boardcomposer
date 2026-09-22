# Revisión de planificación — 2026-09-22

**Origen:** cron diario; reconciliar snapshot `REVIEW-2026-09-21` (PR `#656`
mergeado) con producto en `main`: `#655` (IDE-0042), `#657` (IDE-0043),
`#658` (IDE-0044), `#659` (IDE-0045).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-09-21`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#655`…`#659` **mergeados**; sin PRs abiertos.
**Planning mergeado previo:** `#656` (2026-09-21) — se pliega como histórico.

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
| IDE-0024 metadatos proyecto (cliente / ref. / notas; Ctrl+Alt+M; v3) | 🟢 (#617) |
| IDE-0019 intercambiar dos piezas colocadas (Ctrl+Alt+X) | 🟢 (#618) |
| IDE-0020 kerf / espesor de sierra (Ctrl+Alt+K; `.bcproj` v4) | 🟢 (#619) |
| IDE-0023 lista de corte / informe taller (Ctrl+Alt+C; CSV/PDF) | 🟢 (#621) |
| IDE-0021 veta / orientación de fibra (`.bcproj` v5; no rotar si fija) | 🟢 (#622) |
| IDE-0022 packing multipanel Skyline | 🟢 (#623) |
| IDE-0025 retales a inventario remnant (Ctrl+Alt+R; `.bcproj` v6) | 🟢 (#636) |
| IDE-0026 etiquetas de piezas en plano (SVG/PDF/DXF) | 🟢 (#631) |
| IDE-0027 secuencia de corte por panel | 🟢 (#632) |
| IDE-0030 congelar colocaciones / re-pack omitidas (Ctrl+Alt+F) | 🟢 (#634) |
| IDE-0028 catálogo materiales / espesores (Ctrl+Alt+T) | 🟢 (#637) |
| IDE-0029 coste estimado de material (€/m² catálogo) | 🟢 (#638) |
| IDE-0031 medidas típicas de tablero en catálogo (L×A) | 🟢 (#640) |
| IDE-0032 presupuesto de material PDF (Ctrl+Alt+Q) | 🟢 (#642) |
| IDE-0033 etiquetas de retales en plano (LxW SVG/PDF/DXF) | 🟢 (#641) |
| IDE-0034 papel / márgenes / escala en PDF de plano | 🟢 (#643) |
| IDE-0035 exportar soluciones en lote | 🟢 (#644) |
| IDE-0036 colocación manual asistida (sugerir hueco) | 🟢 (#645) |
| IDE-0037 cotas L×A del tablero en plano | 🟢 (#647) |
| IDE-0038 calidad raster PNG/JPEG (DPI) | 🟢 (#649) |
| IDE-0039 trazabilidad en plano (versión, algoritmo, fecha) | 🟢 (#651) |
| IDE-0040 unidades Inspector (mm/cm/in) | 🟢 (#653) |
| IDE-0041 capas DXF por rol (marco/pieza/retal/cota) | 🟢 (#654) |
| IDE-0042 exportar/importar catálogo de materiales | 🟢 (#655) |
| IDE-0043 trazabilidad lista de corte / presupuesto PDF | 🟢 (#657) |
| IDE-0044 unidades prefs en plano / etiquetas export | 🟢 (#658) |
| IDE-0045 mano de obra en presupuesto | 🟢 (#659) |
| IDE-0046 Inspector espesor / rotación / veta de pieza | 🟢 (#661) |
| IDE-0047 unidades prefs en Comparador | 🟢 (#662) |
| IDE-0048 unidades prefs en lista de corte / presupuesto | 🟢 (#663) |
| IDE-0049 exportar/importar preferencias JSON | 🟢 (#664) |
| IDE-0050 Inspector resumen rico proyecto/categoría | 🟢 (#665) |
| IDE-0051 Inspector aprovechamiento de tablero | 🟢 |
| IDE-0052 preview canvas al terminar el solve | ⚪ |
| IDE-0053 material por defecto de proyecto | ⚪ |
| IDE-0054 perfiles nombrados de preferencias | ⚪ |
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
producto IDE-0019…0024 **cerrada** en `0.4.3`; primera ola `0.4.4.dev0`
(0025…0030) **cerrada**; segunda ola 0031…0036 **cerrada** (`#640`…`#645`);
IDE-0037…0049 **entregadas** (`#647`…`#663` + 0049); quinta ola
0050 abierta.

Desde la revisión 2026-09-21, en `main` entraron `#655` (0042), `#657`
(0043), `#658` (0044) y `#659` (0045). Planning `#656` queda histórico.

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
- Workspace: sugerir hueco para colocación manual (IDE-0036; SCR-002).
- Inspector: unidades prefs mm/cm/in (IDE-0040 `#653`); disco sigue mm.
  Pieza muestra espesor, rotación 0°/90° (— si no colocada) y veta
  (IDE-0046 `#661`). Comparador Largo/Ancho y diffs (IDE-0047 `#662`).
  Lista de corte / presupuesto PDF TEXT siguen `prefs.units` (IDE-0048);
  CSV/JSON y área m² siguen mm.
  Prefs: export/import JSON de taller (IDE-0049 `#664`); sin rutas
  locales ni ventana. Inspector de raíz/categoría: conteos, materiales
  y área (IDE-0050 `#665`). Tablero: aprovechamiento (IDE-0051).

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` sexta ola** — IDE-0052 (0051 entregada; abre 0052…0054).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0052…0054. Residual bloqueado: piloto DT-0006 D (operativo) +
IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → **sí se añaden IDE-0051…0054**
(ancladas a SCR-004 tablero, FLW-003 preview, FLW-001 material,
SCR-006 perfiles).

| ID | Título | Estado |
|----|--------|--------|
| IDE-0042 | Exportar/importar catálogo de materiales | Entregado (#655) |
| IDE-0043 | Trazabilidad en lista de corte / presupuesto | Entregado (#657) |
| IDE-0044 | Unidades prefs en plano y etiquetas de export | Entregado (#658) |
| IDE-0045 | Mano de obra en presupuesto | Entregado (#659) |
| IDE-0046 | Inspector: espesor / rotación / veta de pieza | Entregado (#661) |
| IDE-0047 | Unidades prefs en Comparador | Entregado (#662) |
| IDE-0048 | Unidades prefs en lista de corte / presupuesto | Entregado (#663) |
| IDE-0049 | Exportar/importar preferencias JSON | Entregado (#664) |
| IDE-0050 | Inspector: resumen rico de proyecto/categoría | Entregado (#665) |
| IDE-0051 | Inspector: aprovechamiento de tablero | Entregado |
| IDE-0052 | Preview canvas al terminar el solve | Idea |
| IDE-0053 | Material por defecto de proyecto | Idea |
| IDE-0054 | Perfiles nombrados de preferencias | Idea |

Prioridad de ataque: **IDE-0052** (preview canvas post-solve).

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0050;
IDE-0051 en esta rama.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- Alinear `#665` 🟢; entregar IDE-0051; cola 0052…0054.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
