# ROADMAP — BoardComposer

Resumen operativo. El roadmap detallado vive en
`docs/masterplan/DOC-003-Roadmap.md`.

## Fase 0 — Fundamentos — Completada

- [x] Repositorio, packaging y CI.
- [x] Documentación fundacional y ADR.
- [x] Estructura modular Core/Studio.

## Fase 1 — Core 2D — Base completada

- [x] Modelos de proyecto, piezas, restricciones y soluciones.
- [x] Geometría, colisiones y espacios libres.
- [x] Pipeline de candidatos, validación, evaluación y ranking.
- [x] Horizontal, vertical, free-space, Skyline y MaxRects.
- [x] Beam Search, heurísticas adaptativas y diagnósticos.
- [x] CLI, CSV, texto, JSON y SVG.
- [x] Inventario `StockPanel` y primera vertical multipanel MaxRects.

El Core permanece abierto a extensiones; “completada” significa que la base
arquitectónica y funcional está consolidada.

## Fase 2 — BoardComposer Studio — En curso

- [x] Workspace gráfico y cámara.
- [x] Inspector y selección centralizada.
- [x] Comandos de mover, rotar y eliminar con undo/redo.
- [x] Creación y edición de proyectos, tableros y piezas.
- [x] Persistencia, archivos recientes y exportación SVG.
- [x] Exploración de varias soluciones y diagnósticos del solver.
- [x] Modelo, persistencia y representación básica multipanel.
- [x] UAT visual multipanel completo.
- [x] Movimiento interactivo de piezas entre paneles.
- [x] Comparador visual SCR-003 (resaltado, ordenar/filtrar, miniaturas, diff).
- [x] Importación tableros/piezas CSV y Excel (`.xlsx`), con mapeo y plantillas.
- [x] Exportación SVG/DXF/PDF/JSON/CSV con diálogo, preview y plantillas.
- [x] Preferencias (tema, idioma, unidades, grid, estrategia, export defaults).
- [x] Pantalla de inicio / bienvenida (SCR-001).
- [x] Docs UI SCR-001…007 y FLW-001…006 alineados con Studio
      (`docs/masterplan/ui/REVIEW-2026-07-17.md`).
- [x] Timeline (ADR-005): filtros, replay, export, preferencias de UI.

Núcleo usable; evolución continua (pulido tips/enablement, deuda DT-0006).

## Fase 3 — Plataforma — Entregada

Detalle: `docs/masterplan/epics/` (EP-001 → EP-002 → EP-003). Alineado con
`DOC-003` / `DOC-004` (corte 2026-07).

- [x] EP-001 API pública y contratos `v1`.
- [x] EP-002 Automatización y batch (CLI/lotes).
- [x] EP-003 Integraciones / servicios remotos.

Post-corte (solo con piloto): rate-limit / mTLS — ver `DOC-010`.
Historial cloud `.bcproj`: spike `docs/masterplan/spikes/SPIKE-DT-0006-historial-cloud.md`.

## Fase 4 — Inteligencia — Visión

- Asistencia y explicaciones mediante IA (IDE-0007).
- Recomendación de estrategias y análisis avanzado.

## Fase 5 — Ecosistema — Visión futura

- Plugins (IDE-0008), marketplace, biblioteca de materiales y comunidad.

## Próximo foco (operativo)

Revisión: `docs/masterplan/REVIEW-2026-09-06-planificacion.md`.

1. Release **`0.4.2`** cortado (`v0.4.2`, 2026-08-02) — hecho.
2. Ciclo `0.4.3.dev0` abierto — ola tips honesty Archivo/Edición/Ayuda/
   plantillas/outdated/confirmaciones/import·export + Timeline/Vista/docks/
   comparador + Calcular layout + Abrir carpeta/barra estado + Comparar
   ant./sig. + Timeline Play/Reset/←/→/lista + Guardar/zoom/Explicar/
   Seleccionar todas/Quitar/Invertir + demo Máx. soluciones + Nuevo
   proyecto/export selección/Timeline + Importar piezas/tableros +
   Añadir tablero (PRs ~457–599; Issues = 0; PRs abiertos = 0 al corte
   09-06; planning #594/#595/#598 + tip #599 en `main`); candidatos
   IDE-0019…0024 aún sin implementar (bajo demanda).
3. IDE-0007: MVP local en `0.4.2`; **eval humana** aún abierta
   (`uat/studio/CHECKLIST-EXPLAIN-EVAL.md`).
4. Piloto DT-0006 D activo; opción C diferida (demanda multi-usuario + DOC-010).
5. Gate demo/release (`uat/RELEASE-SMOKE.md`) — activo en cada corte.
6. IDE-0007 LLM opt-in — tras eval/política (DEC-0011).
7. Plugins (IDE-0008) — no priorizar sin ADR-004 operativo.
