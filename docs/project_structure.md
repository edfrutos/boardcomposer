# Estructura del proyecto

## Raíz

- `pyproject.toml`: configuración Python.
- `Makefile`: comandos frecuentes.
- `README.md`: descripción general.
- `TODO.md`: tareas pendientes.
- `CHANGELOG.md`: historial de cambios.

## Código

- `src/boardcomposer/domain/`: modelos principales.
- `src/boardcomposer/domain/panel_reference.py`: identidad de panel físico.
- `src/boardcomposer/domain/offcut.py`: retal informativo por panel (ADR-016).
- `src/boardcomposer/layout/`: geometría y colocación.
- `src/boardcomposer/solver/`: generación, validación y evaluación.
- `src/boardcomposer/solver/multi_panel_maxrects.py`: packing MaxRects
  multipanel (material, órdenes de panel, retales, soluciones parciales).
- `src/boardcomposer/solver/panel_ordering.py`: órdenes de panel candidatos.
- `src/boardcomposer/solver/cp_sat_runner.py`: generador exacto CP-SAT
  (exploratorio, un solo panel).
- `src/boardcomposer/io/`: entrada/salida de datos.
- `src/boardcomposer/cli.py`: interfaz de línea de comandos.

## Studio

- `studio/models/`: modelos persistentes de la aplicación.
- `studio/layout_service.py`: adaptador Studio → Core.
- `studio/project_serializer.py`: persistencia `.bcproj` y migraciones de
  versión (ADR-015).
- `studio/board_csv_importer.py`: importación de inventario de tableros
  desde CSV.
- `studio/solution_highlights.py`: mejor solución por métrica para el
  comparador (SCR-003).
- `studio/workspace/`: vista, controladores y disposición multipanel
  (incluye movimiento/reasignación de piezas entre paneles físicos).
- `studio/dialogs/`: diálogos (nuevo tablero/pieza, vista previa de
  importación CSV).

## Pruebas

- `tests/`: tests unitarios.
- `tests/conftest.py`: fixture de `QApplication` para pruebas Qt offscreen.
- `tests/test_workspace_qt_interaction.py`: pruebas de interacción Qt del
  Workspace (DT-0004).

## Datos

- `data/samples/`: CSV de ejemplo (piezas para la CLI, inventario de
  tableros para Studio).

## Scripts

- `scripts/check_project.py`: validación básica del proyecto.
- `scripts/benchmark_multipanel_maxrects.py`: benchmarks reproducibles del
  packing multipanel.

## UAT

- `uat/multipanel/CHECKLIST.md`: checklist del UAT visual multipanel.
