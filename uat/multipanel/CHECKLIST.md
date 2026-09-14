# UAT multipanel — checklist

**Fecha:** 2026-07-28  
**Estado:** Completado (sesión Studio + reconstrucción verificada en tests)

## Escenarios cubiertos

- [x] Varios tipos de tablero, cantidades e instancias físicas.
- [x] Compatibilidad de espesor y material entre pieza y panel.
- [x] Solución parcial cuando el inventario o el material no alcanza.
- [x] Movimiento / reasignación de piezas entre paneles desde el Workspace.
- [x] Inspector muestra identificador e instancia de panel.
- [x] Comparador resalta la mejor solución por métrica.
- [x] Retales visibles en Inspector / SVG.
- [x] Importación de inventario CSV con vista previa.
- [x] Persistencia `.bcproj` (v5 actual; carga v1…v4 vía ADR-015).
- [x] Skyline y MaxRects cumplen el contrato multipanel (IDE-0022).

## Cubierto también en UAT Studio

- Ordenar / filtrar soluciones en el Comparador (SCR-003) — ver
  `uat/studio/CHECKLIST-FUNCIONAL.md` §4 + `tests/test_uat_multi_candidate_flow.py`.
- Importación de piezas CSV/Excel — ver §5 del checklist Studio.

## Regresión automatizada

- `tests/test_workspace_qt_interaction.py` (Qt offscreen).
- `tests/test_multi_panel_validation.py`, `tests/test_maxrects_generator.py`,
  `tests/test_multi_panel_skyline.py`.
- `scripts/benchmark_multipanel_maxrects.py`.
- `tests/test_uat_multi_candidate_flow.py` (Comparador multi-candidata).
