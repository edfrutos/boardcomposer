# Revisión de planificación — 2026-09-19

**Origen:** cron diario; reconciliar merge `#647` (IDE-0037), `#649`
(IDE-0038) y snapshot histórico `REVIEW-2026-09-18` (PR `#648` abierto).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisiones `REVIEW-2026-09-17` / `REVIEW-2026-09-18`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#647` y `#649` **mergeados** en `main`.
**Planning abierto previo:** `#648` (2026-09-18) — se pliega como histórico.

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
| IDE-0039 trazabilidad en plano (versión, algoritmo, fecha) | 🟢 |
| IDE-0040 unidades Inspector (mm/cm/in) | ⚪ |
| IDE-0041 capas DXF por rol (marco/pieza/retal/cota) | ⚪ |
| IDE-0042 exportar/importar catálogo de materiales | ⚪ |
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
IDE-0037, IDE-0038 e IDE-0039 **entregadas**; restante tercera ola
0040…0042.

Desde la revisión 2026-09-18, en `main` entró: `#647` (IDE-0037 cotas) y
`#649` (IDE-0038 raster). El snapshot 2026-09-18 (PR `#648`) proponía la
tercera ola IDE-0037…0042; este corte confirma 0037/0038 🟢 y retiene
0041/0042 en backlog.

Límites conocidos (no son bugs; son alcance):

- Retales se reportan (ADR-016) y se pueden promover a inventario del
  mismo `.bcproj` (IDE-0025); no hay librería compartida entre proyectos
  (IDE-0042 propuesto).
- CP-SAT exacto sigue siendo un solo panel (opcional).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.
- Catálogo de usuario (IDE-0028/0031) guarda nombre / espesor / €/m² /
  L×A de tablero.
- Etiquetas de plano cubren piezas (IDE-0026), retales LxW (IDE-0033) y
  cotas L×A del tablero (IDE-0037).
- Coste (IDE-0029) y presupuesto PDF (IDE-0032) cubren material de
  tableros físicos; no hay mano de obra.
- Export PDF: papel/márgenes/escala en plano (IDE-0034); lote de
  candidatas Studio (IDE-0035). Raster PNG/JPEG: DPI y calidad JPEG
  (IDE-0038). Pie de trazabilidad en plano (IDE-0039). Capas DXF por
  rol aún no (IDE-0041). Sin nube.
- Workspace: sugerir hueco para colocación manual (IDE-0036; SCR-002).

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` tercera ola** — IDE-0040…0042 (0037…0039 entregadas).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0040…0042. Residual bloqueado: piloto DT-0006 D (operativo)
+ IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → **no** se proponen IDE nuevas
(0040…0042 siguen abiertas; 0041/0042 vienen del snapshot 2026-09-18).

| ID | Título | Estado |
|----|--------|--------|
| IDE-0037 | Cotas L×A del tablero en plano | Entregado (#647) |
| IDE-0038 | Calidad raster PNG/JPEG (DPI) | Entregado (#649) |
| IDE-0039 | Trazabilidad en plano (versión, algoritmo, fecha) | Entregado |
| IDE-0040 | Unidades Inspector (mm/cm/in) | Idea |
| IDE-0041 | Capas DXF por rol (marco/pieza/retal/cota) | Idea |
| IDE-0042 | Exportar/importar catálogo de materiales | Idea |

Prioridad de ataque: **IDE-0040** (unidades Inspector).

Cerradas en este ciclo `0.4.4.dev0`: IDE-0025…0039.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- No se implementa código de producto: alinear docs con `#647`/`#649`,
  plegar histórico 2026-09-18 y retener IDE-0041/0042 en DOC-004.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
