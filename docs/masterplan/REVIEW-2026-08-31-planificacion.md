# Revisión de planificación — 2026-08-31

**Origen:** automatización periódica (cron) de documentación y planificación.  
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` ciclo `0.4.3.dev0`, UAT release smoke,
revisión previa en `main` `REVIEW-2026-08-30-planificacion.md`.  
**Issues GitHub:** `gh issue list --state open` → **vacío** (sin bugs abiertos
visibles en el repo). **PRs abiertos al corte:** ninguno.

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
| Tips honesty Vista: rejilla / barra herramientas / docks (persisten) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Vista: comparador (persiste) + Calcular layout (reemplaza / no undo) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Abrir carpeta / barra estado / status sin `.bcproj` (explorador) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Comparar: solución ant./sig. + Timeline Play / Reset / ← / → / lista | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Guardar / zoom Ctrl+0 / Explicar (sin IA red) / Seleccionar todas | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Quitar selección + Invertir selección (conservan tablero) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Explicar (ES `puedes`) + Proyecto demo (Máx. soluciones) | 🟢 QoL `0.4.3.dev0` |
| Guía rápida: Welcome…Explorador + Disposición (docks/toolbar/reset) | 🟢 Docs `0.4.3.dev0` |
| Import CSV/Excel; export SVG/DXF/PDF/JSON/CSV + plantillas | 🟢 |
| Fase 3: EP-001 API `v1`, EP-002 batch, EP-003 HTTP/Docker | 🟢 Entregada |
| IDE-0007 explicación local (sin LLM) | 🟡 MVP código; eval humana abierta |
| IDE-0008 plugins | ⚪ Visión Fase 5 |
| DT-0006 historial cloud | 🟡 Piloto D (backup); C diferida |

Detalle de ideas: `DOC-004-Backlog.md`.

---

## 2. Planificación de construcción

| Fase | Estado | Notas |
|------|--------|-------|
| 0 Fundamentos | 🟢 | Repo, CI, ADR |
| 1 Core 2D | 🟢 Base | Extensiones controladas |
| 2 Studio | 🟡 En curso | Núcleo usable; pulido continuo |
| 3 Plataforma | 🟢 | EP-001…003 cerradas (corte 2026-07) |
| 4 Inteligencia | ⚪ | IDE-0007 MVP local; LLM bajo política |
| 5 Ecosistema | ⚪ | Plugins / marketplace |

Versión: desarrollo `0.4.3.dev0` · estable `0.4.2` (2026-08-02).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; ciclo
abierto = **QoL / tips honesty bajo demanda** + residuales (eval / piloto).

Desde la revisión 2026-08-30 en `main`, el ciclo `0.4.3.dev0` cerró en `main`
el tip Quitar selección (#583), Invertir selección (#585), locale Explicar
`puedes` (#586), tip demo Máx. soluciones (#587) y el snapshot 08-30 (#584;
#582 también mergeado). Al corte 08-31: **Issues abiertos = 0**; **PRs
abiertos = 0**.

Límites conocidos (no son bugs; son alcance):

- Solo MaxRects cumple el contrato multipanel completo.
- Sin acción «intercambiar dos piezas» (solo arrastre entre paneles).
- Sin formulario único cliente/kerf/vetas en Proyecto (SCR-005).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`, corte `0.4.2`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Eval humana IDE-0007** — completar
   `uat/studio/CHECKLIST-EXPLAIN-EVAL.md` (≥4/5 útil/mixto) antes de valorar
   LLM opt-in.
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **QoL / producto `0.4.3`** — atacar cola IDE-0019…0024 (DOC-004) cuando
   haya capacidad; la ola de tips/docs no vacía esa cola.
5. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente.

---

## 5. Cola candidata (sin ideas nuevas en este pase)

Hay pendiente residual (eval + piloto) y **seis ideas abiertas**
(IDE-0019…0024) añadidas el 2026-08-05. Criterio del cron: *solo proponer
nuevas funcionalidades si no queda desarrollo pendiente y bugs cerrados*.

Bugs abiertos: **0**. Aun así, la cola implementable **no está vacía**
(IDE-0019…0024 + residuales eval/piloto). **No se añaden IDE-0025+** en este
pase.

Cola vigente (orden sugerido sin cambios):

| ID | Título | Por qué |
|----|--------|---------|
| IDE-0024 | Metadatos de proyecto (cliente, ref., notas) | Evolución SCR-005; esfuerzo S |
| IDE-0019 | Intercambiar dos piezas | Límite Workspace documentado |
| IDE-0020 | Kerf / espesor de sierra | ADR-010 / SCR-005 |
| IDE-0023 | Lista de corte / informe taller | Valor taller N1–N2 |
| IDE-0021 | Restricción de veta | Metadatos pieza/proyecto |
| IDE-0022 | Multipanel Skyline | Solo MaxRects cumple contrato hoy |

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs y
  snapshot.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
