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
- [ ] UAT visual multipanel completo.
- [ ] Movimiento interactivo de piezas entre paneles.
- [ ] Comparador visual avanzado conforme a SCR-003.
- [ ] Importación de inventario multipanel desde CSV/Excel.

## Fase 3 — Plataforma — Planificada

- API pública y contratos versionados.
- Automatización e integraciones.
- Exportadores avanzados y servicios remotos.

## Fase 4 — Inteligencia — Visión

- Asistencia y explicaciones mediante IA.
- Recomendación de estrategias y análisis avanzado.

## Fase 5 — Ecosistema — Visión futura

- Plugins, marketplace, biblioteca de materiales y comunidad.
