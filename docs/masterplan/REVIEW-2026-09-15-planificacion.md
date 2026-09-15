# Revisión de planificación — 2026-09-15

**Origen:** automatización periódica (cron) de documentación y planificación.  
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` ciclo `0.4.4.dev0`, UAT release smoke,
revisión `REVIEW-2026-09-14-planificacion.md` (PR #624 mergeado).  
**Issues GitHub:** `gh issue list --state open` → **vacío** (sin bugs abiertos
visibles en el repo). **PRs abiertos al corte:** 1 (`#628` bump
`0.4.4.dev0`; CI según estado del PR).

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
| IDE-0022 packing multipanel Skyline | 🟢 (#623 mergeado 2026-09-14) |
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
| 1 Core 2D | 🟢 Base | Extensiones controladas (kerf, grain, Skyline MP) |
| 2 Studio | 🟡 En curso | Núcleo usable; pulido continuo |
| 3 Plataforma | 🟢 | EP-001…003 cerradas (corte 2026-07) |
| 4 Inteligencia | ⚪ | IDE-0007 MVP+eval; LLM bajo política |
| 5 Ecosistema | ⚪ | Plugins / marketplace |

Versión: desarrollo `0.4.4.dev0` · estable `0.4.3` (2026-09-14; etiqueta
`v0.4.3` pendiente de publicar en GitHub Releases).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; cola
producto IDE-0019…0024 **cerrada** en el corte `0.4.3` (Skyline `#623`
incluido).

Desde la revisión 2026-09-14 (#624 mergeado), en `main` entró: merge `#623`
(IDE-0022), release `#627` (`0.4.3`). Al corte 09-15: **Issues abiertos = 0**;
**PRs abiertos = 1** (`#628` abrir ciclo `0.4.4.dev0`).

Límites conocidos (no son bugs; son alcance):

- Retales informativos (ADR-016); **no** son inventario reutilizable todavía.
- CP-SAT exacto sigue siendo un solo panel (opcional).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`, corte `0.4.3`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cerrar ciclo paquete** — mergear `#628` (o equivalente) para dejar
   `pyproject` / Studio en `0.4.4.dev0`; publicar etiqueta `v0.4.3` si falta.
2. **Cola `0.4.4`** — atacar IDE-0025…0030 (abajo) por prioridad sugerida.
3. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
4. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
5. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata (ciclo `0.4.4` / nuevas ideas)

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
IDE-0019…0024: **vacía** (IDE-0022 mergeado). Residual: piloto DT-0006 D
(operativo, no feature de producto) + backlog grande bloqueado.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → **sí se añaden IDE-0025…0030**.

Ancladas a límites ya escritos (ADR-016 retales; taller post lista de corte;
soluciones parciales; usuarios N1–N2):

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0025 | Retales como inventario reutilizable | ADR-016 difería inventario; retales solo informativos hoy |
| IDE-0026 | Etiquetas de piezas en plano (SVG/PDF) | Taller N1 tras lista de corte IDE-0023 |
| IDE-0027 | Secuencia de corte por panel | Orden de sierra; complementa informe taller |
| IDE-0028 | Catálogo de materiales / espesores | Reutilizar stock tipificado entre proyectos |
| IDE-0029 | Coste estimado de material | Decisión junto a desperdicio / retales |
| IDE-0030 | Congelar colocaciones / re-pack omitidas | Flujo soluciones parciales sin romper layout OK |

Prioridad sugerida de ataque si se abre capacidad: **0026 → 0027 → 0030 →
0025 → 0028 → 0029** (etiquetas y secuencia antes de inventario de retales;
coste al final).

Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog con merges `#623`/`#627` y cola vacía.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
