# Revisión de planificación — 2026-08-13

**Origen:** automatización periódica (cron) de documentación y planificación.  
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` ciclo `0.4.3.dev0`, UAT release smoke,
revisión previa `REVIEW-2026-08-12-planificacion.md`.  
**Issues GitHub:** API no accesible desde esta automatización (403); no se
listan bugs abiertos en la documentación de producto. PRs abiertos vía
`gh pr list`: ninguno al momento del snapshot.

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
| Tips honesty menú Archivo/Edición/Ayuda + plantillas + outdated/confirmaciones | 🟢 QoL `0.4.3.dev0` |
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

Desde la revisión 2026-08-12 el ciclo `0.4.3.dev0` cerró la cola de tips
pendiente (#474 Rename template) y amplió la ola honesty (PRs #476…#490
mergeados): rotate (placement + EN board), export save/delete template,
rename selection, restore local revision, import mapping delete,
apply/export outdated (diálogo de opciones), solve-layout (inventario),
remove-recent (no borra disco). Snapshot planificación 08-12 mergeado
(#475). Sin PRs abiertos al corte de este pase.

Límites conocidos (no son bugs; son alcance):

- Solo MaxRects cumple el contrato multipanel completo.
- Sin acción «intercambiar dos piezas» (solo arrastre entre paneles).
- Sin formulario único cliente/kerf/vetas en Proyecto (SCR-005).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`, corte `0.4.2`).

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

**No se añaden IDE-0025+** en este pase: la cola implementable no está vacía
y Issues GitHub no son consultables aquí (403).

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
- Bugs: sin evidencia en docs; Issues GitHub no consultables aquí (403).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
