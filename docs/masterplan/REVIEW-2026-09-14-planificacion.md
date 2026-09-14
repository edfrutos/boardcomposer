# Revisión de planificación — 2026-09-14

**Origen:** automatización periódica (cron) de documentación y planificación.  
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` ciclo `0.4.3.dev0`, UAT release smoke,
revisión `REVIEW-2026-09-13-planificacion.md` (PR #620 mergeado).  
**Issues GitHub:** `gh issue list --state open` → **vacío** (sin bugs abiertos
visibles en el repo). **PRs abiertos al corte:** 1 (`#623` IDE-0022 Skyline
multipanel; CI verde, mergeable).

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| Core 2D (modelos, geometría, pipeline, Skyline/MaxRects, Beam Search) | 🟢 Base Fase 1 |
| Multipanel MaxRects (material + espesor, retales, parciales) | 🟢 |
| CP-SAT un panel (opcional) | 🟢 Explorado |
| Studio: Workspace, Inspector, comandos, persistencia `.bcproj` | 🟢 Núcleo usable |
| Comparador SCR-003, Timeline, Preferencias, Welcome | 🟢 |
| Welcome / Archivo → Recientes (pin, quitar, carpeta, submenú gestión) | 🟢 QoL `0.4.3.dev0` |
| Barra de estado: basename, clic → carpeta, tips zoom / sin guardar | 🟢 QoL `0.4.3.dev0` |
| Timeline: tips honestos + F1 replay/Ctrl+C | 🟢 QoL `0.4.3.dev0` |
| Tips honesty menús + plantillas + outdated/confirmaciones + import/export | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Vista / Comparar / Guardar / zoom / Explicar / selección | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Importar / Añadir / Duplicar / stock paneles (#614) | 🟢 QoL `0.4.3.dev0` |
| IDE-0024 metadatos proyecto (cliente / ref. / notas; Ctrl+Alt+M; v3) | 🟢 (#617) |
| IDE-0019 intercambiar dos piezas colocadas (Ctrl+Alt+X) | 🟢 (#618) |
| IDE-0020 kerf / espesor de sierra (Ctrl+Alt+K; `.bcproj` v4) | 🟢 (#619 + fixes) |
| IDE-0023 lista de corte / informe taller (Ctrl+Alt+C; CSV/PDF) | 🟢 (#621) |
| IDE-0021 veta / orientación de fibra (`.bcproj` v5; no rotar si fija) | 🟢 (#622) |
| IDE-0022 packing multipanel Skyline | 🟡 En PR `#623` |
| Guía rápida: Welcome…Explorador + Disposición (docks/toolbar/reset) | 🟢 Docs `0.4.3.dev0` |
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
| 1 Core 2D | 🟢 Base | Extensiones controladas (kerf, grain) |
| 2 Studio | 🟡 En curso | Núcleo usable; pulido continuo |
| 3 Plataforma | 🟢 | EP-001…003 cerradas (corte 2026-07) |
| 4 Inteligencia | ⚪ | IDE-0007 MVP+eval; LLM bajo política |
| 5 Ecosistema | ⚪ | Plugins / marketplace |

Versión: desarrollo `0.4.3.dev0` · estable `0.4.2` (2026-08-02).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; ciclo
abierto = **IDE-0022** (PR `#623` en curso) + piloto DT-0006 D.

Desde la revisión 2026-09-13 (#620 mergeado), en `main` entró producto real:
#621 lista de corte (IDE-0023) y #622 veta (IDE-0021). Planning #615/#616
también cerrados. Al corte 09-14: **Issues abiertos = 0**; **PRs abiertos = 1**
(`#623` Skyline multipanel).

Límites conocidos (no son bugs; son alcance):

- Solo MaxRects cumple el contrato multipanel completo en `main`
  (Skyline multipanel pendiente de merge `#623`).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`, corte `0.4.2`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cerrar IDE-0022** — revisar/mergear `#623` (CI verde; Skyline multipanel
   ADR-014) cuando el gate humano lo apruebe.
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **Tras merge `#623`** — alinear docs (DOC-004 🟢, límites MASTERPLAN) y
   evaluar si la cola implementable queda vacía → entonces sí IDE-0025+.
5. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata (sin ideas nuevas en este pase)

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Queda **una idea abierta
implementable** (IDE-0022, en PR) + residual piloto DT-0006 D. Criterio del
cron: *solo proponer nuevas funcionalidades si no queda desarrollo pendiente
y bugs cerrados*.

Cola implementable **no vacía** → **no se añaden IDE-0025+** en este pase.

Cola vigente:

| ID | Título | Por qué |
|----|--------|---------|
| IDE-0022 | Multipanel Skyline | PR `#623` abierto; hoy solo MaxRects en `main` |

Cerradas desde 2026-09-12: IDE-0024 (#617), IDE-0019 (#618), IDE-0020 (#619),
eval IDE-0007. Cerradas 2026-09-13: IDE-0023 (#621), IDE-0021 (#622).

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs y
  snapshot con merges #621/#622 y PR abierto #623.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
