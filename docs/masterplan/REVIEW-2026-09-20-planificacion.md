# Revisión de planificación — 2026-09-20

**Origen:** cron diario; reconciliar snapshot `REVIEW-2026-09-19` (PR `#650`
mergeado) con PR de producto `#651` (IDE-0039), ahora en `main`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-09-19`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#651` (IDE-0039) **mergeado**.
**Planning mergeado previo:** `#650` (2026-09-19) — se pliega como histórico.

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
| IDE-0040 unidades Inspector (mm/cm/in) | 🟢 |
| IDE-0041 capas DXF por rol (marco/pieza/retal/cota) | 🟢 |
| IDE-0042 exportar/importar catálogo de materiales | 🟢 |
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
IDE-0037, IDE-0038 e IDE-0039 **entregadas** (`#647`, `#649`, `#651`);
tercera ola 0040…0042 **cerrada**.

Desde la revisión 2026-09-19, en `main` entró `#651` (IDE-0039
trazabilidad: pie `BoardComposer {version} · {algorithm} · fecha` en
SVG/PDF/DXF; casilla Exportar/Preferencias). Planning `#650` queda
histórico.

Límites conocidos (no son bugs; son alcance):

- Retales se reportan (ADR-016) y se pueden promover a inventario del
  mismo `.bcproj` (IDE-0025); no hay librería compartida entre proyectos.
- Catálogo de usuario (IDE-0028/0031) guarda nombre / espesor / €/m² /
  L×A; export/import JSON entre PCs (IDE-0042). Sin nube.
- CP-SAT exacto sigue siendo un solo panel (opcional).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.
- Etiquetas de plano cubren piezas (IDE-0026), retales LxW (IDE-0033) y
  cotas L×A del tablero (IDE-0037) y pie de trazabilidad (IDE-0039).
- Coste (IDE-0029) y presupuesto PDF (IDE-0032) cubren material de
  tableros físicos; no hay mano de obra.
- Export PDF: papel/márgenes/escala en plano (IDE-0034); lote de
  candidatas Studio (IDE-0035). Raster PNG/JPEG: DPI y calidad JPEG
  (IDE-0038). Capas DXF por rol (IDE-0041). Sin nube.
- Workspace: sugerir hueco para colocación manual (IDE-0036; SCR-002).
- Inspector: unidades prefs mm/cm/in (IDE-0040); disco sigue mm.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` tercera ola** — **cerrada** (0037…0042). Residual
   implementable vacío.
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
vacía. Residual bloqueado: piloto DT-0006 D (operativo) + IDE-0008 /
LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → cola implementable vacía;
bloqueados no cuentan como desarrollo pendiente de producto.

| ID | Título | Estado |
|----|--------|--------|
| IDE-0039 | Trazabilidad en plano (versión, algoritmo, fecha) | Entregado (#651) |
| IDE-0040 | Unidades Inspector (mm/cm/in) | Entregado |
| IDE-0041 | Capas DXF por rol (marco/pieza/retal/cota) | Entregado |
| IDE-0042 | Exportar/importar catálogo de materiales | Entregado |

Prioridad de ataque: residual bloqueado (no IDE nuevas aquí).

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0042.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- Alinear docs con IDE-0042 🟢; cola implementable vacía.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
