# AI Context

Nombre del proyecto: BoardComposer.

## Propósito

Generar, validar, puntuar, comparar y explicar composiciones de corte 2D sobre
material disponible. BoardComposer no impone una única respuesta: presenta
alternativas comprensibles para que el usuario decida.

## Estado actual — 2026-07-16

- Fase de producto: Fase 2, BoardComposer Studio.
- Core base completado y en evolución controlada.
- Vertical multipanel MaxRects implementada.
- Studio funcional con persistencia versión 2 y compatibilidad versión 1.
- Versión de desarrollo: `0.4.0.dev0`.

## Fuentes de verdad

1. Código y tests vigentes.
2. `docs/masterplan/MASTERPLAN.md`.
3. ADR aceptados en `docs/masterplan/adr/`.
4. Roadmap y backlog del masterplan.
5. Documentación técnica de `docs/`.

## Reglas

- El Core no depende de Studio, Qt, Flask ni IA.
- Toda colocación multipanel usa coordenadas locales y `PanelReference`.
- Mantener compatibilidad de proyectos y formatos cuando sea posible.
- Añadir tests en interfaces públicas antes de ampliar comportamiento.
- Registrar decisiones relevantes mediante ADR/DECISIONS.
- Actualizar CHANGELOG, MASTERPLAN y documentación con cada hito.
- Ejecutar Ruff, type checking y Pytest antes de cerrar un bloque.
