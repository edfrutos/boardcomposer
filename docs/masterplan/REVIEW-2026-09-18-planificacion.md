# Revisión de planificación — 2026-09-18

**Origen:** cron diario; cola implementable vacía en `main` tras
`#644`/`#645`/`#646`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión previa `REVIEW-2026-09-17-planificacion.md`, PR abierto `#647`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#647` **abierto** (IDE-0037 cotas L×A).

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
| IDE-0037 cotas L×A del tablero en plano | 🟡 PR `#647` |
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
(0025…0030) **cerrada**; segunda ola 0031…0036 **cerrada** en `main`
(`#640`…`#645`).

Desde la revisión 2026-09-17 no hay merges de producto en `main`. PR abierto
`#647` (IDE-0037 cotas L×A) aún fuera de `main`.

Límites conocidos (no son bugs; son alcance):

- Retales se reportan (ADR-016) y se pueden promover a inventario del
  mismo `.bcproj` (IDE-0025); no hay librería compartida entre proyectos.
- CP-SAT exacto sigue siendo un solo panel (opcional).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.
- Catálogo de usuario (IDE-0028/0031) guarda nombre / espesor / €/m² /
  L×A de tablero; sin export/import entre equipos (IDE-0042 propuesto).
- Etiquetas de plano cubren piezas (IDE-0026) y retales LxW (IDE-0033);
  cotas overall de tablero en curso (IDE-0037).
- Coste (IDE-0029) y presupuesto PDF (IDE-0032) cubren material de
  tableros físicos; no hay mano de obra.
- Export PDF: papel/márgenes/escala en plano (IDE-0034); lote de
  candidatas Studio (IDE-0035). Sin publicación a la nube.
- Workspace: sugerir hueco para colocación manual (IDE-0036; SCR-002).

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cerrar `#647` (IDE-0037)** — cotas L×A del tablero en plano; merge a
   `main` antes de arrancar 0038.
2. **Cola `0.4.4` tercera ola** — IDE-0038…0042 (tras merge 0037).
3. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
4. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
5. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0031…0036: **vacía** en `main`. Residual bloqueado: piloto DT-0006 D
(operativo) + IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → **sí se añaden IDE-0037…0042**.

Ancladas a límites ya escritos (SCR-007 cotas/DPI/trazabilidad; SCR-004
unidades; DXF CNC; catálogo IDE-0028 sin compartir entre equipos):

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0037 | Cotas L×A del tablero en plano | Taller lee tamaño físico; `#647` 🟡 |
| IDE-0038 | Calidad raster PNG/JPEG (DPI) | Export taller/impresión; sin solver |
| IDE-0039 | Trazabilidad en plano (versión, algoritmo, fecha) | Auditoría de candidata exportada |
| IDE-0040 | Unidades en Inspector (mm/cm/in) | Prefs.units → display; mm en disco |
| IDE-0041 | Capas DXF por rol (marco/pieza/retal/cota) | Import CAD/CNC limpio |
| IDE-0042 | Exportar/importar catálogo de materiales | Compartir IDE-0028 entre PCs; sin nube |

Prioridad de ataque: **cerrar `#647` (0037) → IDE-0038**.

Cerradas en este ciclo `0.4.4.dev0`: IDE-0025…0036.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; registrar tercera ola IDE-0037…0042 y el PR `#647`.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
