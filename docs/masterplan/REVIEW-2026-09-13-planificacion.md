# Revisión de planificación — 2026-09-13

**Origen:** automatización periódica (cron) de documentación y planificación.  
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` ciclo `0.4.3.dev0`, UAT release smoke,
revisiones `REVIEW-2026-09-11` / `REVIEW-2026-09-12` (PRs #615 draft / #616
abiertos, plegados aquí como histórico; producto #617–#619 ya en `main`).  
**Issues GitHub:** `gh issue list --state open` → **vacío** (sin bugs abiertos
visibles en el repo). **PRs abiertos al corte:** 2 (`#615` planning 09-11
draft; `#616` planning 09-12 — ambos supersedidos por este sync).

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
| Tips honesty Nuevo proyecto (unidades) + Exportar selección + Export Timeline | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Importar piezas / Importar tableros (crean proyecto vacío) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Añadir tablero / Añadir pieza (crean proyecto vacío si no hay) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Duplicar (copia colocación) + pieza/copia sin colocar → 1.º tablero | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Añadir pieza / Importar piezas (colocan en el primer tablero) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Añadir pieza / Importar piezas (cantidad → ids únicos) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Importar piezas / tableros (plantilla de mapeo aplicable) | 🟢 QoL `0.4.3.dev0` |
| Tips honesty Añadir tablero (cantidad = stock paneles, no ids nuevos) | 🟢 QoL `0.4.3.dev0` (#614) |
| IDE-0024 metadatos proyecto (cliente / ref. / notas; Ctrl+Alt+M; `.bcproj` v3) | 🟢 (#617) |
| IDE-0019 intercambiar dos piezas colocadas (Ctrl+Alt+X) | 🟢 (#618) |
| IDE-0020 kerf / espesor de sierra (Ctrl+Alt+K; `.bcproj` v4) | 🟢 (#619 + fixes) |
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
| 1 Core 2D | 🟢 Base | Extensiones controladas (kerf en packing) |
| 2 Studio | 🟡 En curso | Núcleo usable; pulido continuo |
| 3 Plataforma | 🟢 | EP-001…003 cerradas (corte 2026-07) |
| 4 Inteligencia | ⚪ | IDE-0007 MVP+eval; LLM bajo política |
| 5 Ecosistema | ⚪ | Plugins / marketplace |

Versión: desarrollo `0.4.3.dev0` · estable `0.4.2` (2026-08-02).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; ciclo
abierto = **cola producto restante** (IDE-0023 / 0021 / 0022) + piloto DT-0006 D.

Desde la revisión 2026-09-12 (aún sin merge de planning), en `main` entró
producto real: #617 metadatos, #618 swap, #619 kerf (+ fixes selección/
solape), y tip #614. Planning #615/#616 siguen abiertos y se pliegan aquí.
Al corte 09-13: **Issues abiertos = 0**; **PRs abiertos = 2** (solo planning
supersedidos).

Límites conocidos (no son bugs; son alcance):

- Solo MaxRects cumple el contrato multipanel completo.
- Sin restricción de veta / orientación de fibra (IDE-0021).
- Sin lista de corte / informe de taller (IDE-0023).
- Sin multipanel Skyline (IDE-0022).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`, corte `0.4.2`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
2. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
3. **Producto `0.4.3`** — atacar cola restante IDE-0023 → 0021 → 0022
   (DOC-004) cuando haya capacidad.
4. **Cerrar/superseder** planning `#615` / `#616` tras merge de este snapshot.
5. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata (sin ideas nuevas en este pase)

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Quedan **tres ideas abiertas
implementables** (IDE-0021…0023) + residual piloto DT-0006 D. Criterio del
cron: *solo proponer nuevas funcionalidades si no queda desarrollo pendiente
y bugs cerrados*.

Cola implementable **no vacía** → **no se añaden IDE-0025+** en este pase.

Cola vigente (orden sugerido):

| ID | Título | Por qué |
|----|--------|---------|
| IDE-0023 | Lista de corte / informe taller | Valor taller N1–N2; export PDF/CSV |
| IDE-0021 | Restricción de veta | Metadatos pieza; afecta rotación |
| IDE-0022 | Multipanel Skyline | Solo MaxRects cumple contrato hoy |

Cerradas en `main` el 2026-09-12: IDE-0024 (#617), IDE-0019 (#618),
IDE-0020 (#619), eval IDE-0007.

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs y
  snapshot (incluye históricos 09-11 / 09-12 desde PRs #615 / #616).
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
