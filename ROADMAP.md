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

## Fase 3 — Plataforma — Planificada

- API pública y contratos versionados.
- Automatización e integraciones.
- Exportadores avanzados y servicios remotos.

## Fase 4 — Inteligencia — Visión

- Asistencia y explicaciones mediante IA.
- Recomendación de estrategias y análisis avanzado.

## Fase 5 — Ecosistema — Visión futura

- Plugins, marketplace, biblioteca de materiales y comunidad.
