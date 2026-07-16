# UAT multipanel — checklist

**Fecha:** 2026-07-16  
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
- [x] Persistencia `.bcproj` v2 y carga de proyectos v1.

## Regresión automatizada

- `tests/test_workspace_qt_interaction.py` (Qt offscreen).
- `tests/test_multi_panel_validation.py`, `tests/test_maxrects_generator.py`.
- `scripts/benchmark_multipanel_maxrects.py`.

## Pendiente de UAT futuro

- Ordenar / filtrar soluciones en el comparador (SCR-003).
- Importación de piezas (no solo tableros) y Excel.
