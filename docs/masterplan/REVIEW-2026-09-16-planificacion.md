# Revisión de planificación — 2026-09-16

**Origen:** cron diario post-merge `#638` (ciclo `0.4.4.dev0`, segunda ola).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión previa del mismo día (cola 0025…0030 cerrada).
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs abiertos al corte:** ninguno.

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
| IDE-0033 etiquetas de retales en plano (LxW SVG/PDF/DXF) | 🟢 |
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

Versión: desarrollo `0.4.4.dev0` · estable `0.4.3` (2026-09-14; etiqueta
`v0.4.3` pendiente de publicar en GitHub Releases — latest sigue `v0.4.2`).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; cola
producto IDE-0019…0024 **cerrada** en `0.4.3`; primera ola `0.4.4.dev0`
(0025…0030) **cerrada** con `#638` (IDE-0029).

Desde la revisión 2026-09-15 (#630 mergeado), en `main` entró: `#631`
(IDE-0026), `#632` (IDE-0027), `#634` (IDE-0030), `#636` (IDE-0025),
`#637` (IDE-0028), `#638` (IDE-0029).

Límites conocidos (no son bugs; son alcance):

- Retales se reportan (ADR-016) y se pueden promover a inventario del
  mismo `.bcproj` (IDE-0025); no hay librería compartida entre proyectos.
- CP-SAT exacto sigue siendo un solo panel (opcional).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.
- Catálogo de usuario (IDE-0028/0031) guarda nombre / espesor / €/m² /
  L×A de tablero.
- Etiquetas de plano cubren piezas (IDE-0026) y retales LxW (IDE-0033).
- Coste (IDE-0029) vive en Comparador / Inspector / JSON, no en un
  documento de presupuesto.
- Export PDF: sin papel / márgenes / escala; sin lote de soluciones
  (SCR-007 / FLW-005).
- Workspace: sin sugerencias de hueco para colocación manual (SCR-002).

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` segunda ola** — atacar **IDE-0032 → 0034 →
   0035 → 0036** (0031 y 0033 entregadas).
2. **Etiqueta** — `v0.4.3` publicado.
3. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
4. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
5. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0025…0030: **vacía**. Residual: piloto DT-0006 D
(operativo, no feature de producto) + backlog grande bloqueado
(IDE-0008 / LLM / DT-0006 C).

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → **sí se añaden IDE-0031…0036**.

Ancladas a límites ya escritos (catálogo IDE-0028; etiquetas IDE-0026;
coste IDE-0029; SCR-007 papel/lotes; SCR-002 hueco; usuarios N1–N2):

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0031 | Medidas típicas de tablero en catálogo | Entregado; L×A; combo Nuevo tablero |
| IDE-0032 | Informe de presupuesto PDF | Coste IDE-0029 solo UI/JSON; taller necesita documento |
| IDE-0033 | Etiquetas de retales en plano | Entregado; LxW en plano; casilla export |
| IDE-0034 | Papel / márgenes / escala en PDF | Límite explícito SCR-007 / FLW-005 |
| IDE-0035 | Exportar soluciones en lote | SCR-007 «sin lotes»; EP-002 es CLI de proyectos |
| IDE-0036 | Colocación manual asistida (sugerir hueco) | Evolución prevista SCR-002 |

Prioridad sugerida de ataque: **0032 → 0034 → 0035 → 0036**
(presupuesto; página y lote después; asistida al final).

Cerradas en este ciclo `0.4.4.dev0`: IDE-0025…0030.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog con merge `#638` y cola vacía.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
