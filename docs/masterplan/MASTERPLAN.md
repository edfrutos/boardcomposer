# BoardComposer — MASTERPLAN

Última revisión: 2026-08-01.

## Estado actual

- Fase de producto: **Fase 2 — BoardComposer Studio**.
- Versión de desarrollo: `0.4.2.dev0` (última estable: `0.4.1`).
- Core base consolidado y cubierto por tests.
- Studio dispone de flujo funcional de proyecto, edición, cálculo y exportación.
- Vertical multipanel MaxRects con material + espesor, Workspace interactivo y
  suite Qt de arrastre/reasignación.

## Último bloque consolidado

### Packing multipanel

- `StockPanel` con cantidad.
- `PanelReference` por tipo e instancia física.
- MaxRects multipanel con compatibilidad de **espesor y material**.
- Validación, completitud, deduplicación y scoring por panel.
- Persistencia Studio versionada (migraciones ADR-015).
- Workspace y SVG con paneles físicos lado a lado.
- Movimiento y reasignación interactiva de piezas entre paneles (arrastre en
  Workspace, con undo; solape o incompatibilidad revierten el movimiento).
- ADR-014 / ADR-016 y documentación técnica alineada en README, backlog y UAT.

## Próxima tarea única

Ciclo `0.4.2.dev0`: pulido QoL bajo demanda. Backlog grande bloqueado hasta
demanda real:

- DT-0006 historial cloud — esperar piloto (`spikes/SPIKE-DT-0006-historial-cloud.md`).
- IDE-0007 IA — L–XL, solo bajo demanda.
- IDE-0008 plugins — XL; no priorizar sin ADR-004 operativo.

## Criterio de finalización del próximo bloque

- Docs de pantalla (SCR) no contradicen el Studio implementado.
- El flujo UAT se completa sin errores ni pérdida de asignación física.
- Inspector y Workspace identifican correctamente panel e instancia.
- Defectos encontrados tienen test de regresión cuando sea viable.
- Ruff y Pytest limpios en CI.

## Límites conocidos

- Solo MaxRects implementa por ahora el contrato multipanel completo
  (CP-SAT exacto sigue siendo un solo panel, opcional).
- Una sola candidata tras «Calcular layout» es válida: el pipeline puede
  deduplicar a una solución única según inventario y heurísticas.
- No hay acción «intercambiar dos piezas»; la reasignación es arrastrar y
  soltar sobre otro panel físico compatible.
- Guía de usuario final: [`docs/user/GUIA-RAPIDA.md`](../user/GUIA-RAPIDA.md)
  (también **Ayuda → Documentación**, Shift+F1). UAT y masterplan complementan.

## Normas de trabajo

1. No añadir funcionalidad sin bloque definido.
2. No introducir dependencias de interfaz en el Core.
3. No duplicar reglas geométricas o de validación.
4. Mantener coordenadas multipanel locales al panel físico.
5. Trabajar desde interfaces públicas con tests de comportamiento.
6. Actualizar ADR, CHANGELOG y MASTERPLAN al cerrar un hito.
7. Ejecutar Ruff, type checking, Pytest y smoke test de Studio antes del commit.
