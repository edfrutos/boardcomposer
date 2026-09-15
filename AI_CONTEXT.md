# AI Context

Nombre del proyecto: BoardComposer.

## Propósito

Generar, validar, puntuar, comparar y explicar composiciones de corte 2D sobre
material disponible. BoardComposer no impone una única respuesta: presenta
alternativas comprensibles para que el usuario decida.

## Estado actual — 2026-09-15

- Fase de producto: Fase 2 Studio (núcleo usable) + Fase 3 plataforma
  entregada (EP-001…003).
- Core base completado y en evolución controlada (kerf IDE-0020; grain
  IDE-0021; Skyline multipanel IDE-0022).
- Vertical multipanel MaxRects **y** Skyline, con compatibilidad de material
  y espesor, órdenes de panel, retales informativos (ADR-016) y soluciones
  parciales (piezas omitidas en vez de "sin solución").
- Studio funcional con persistencia versionada y migraciones explícitas
  (ADR-015; v3 metadatos, v4 kerf, v5 grain), importación de inventario,
  movimiento entre paneles, swap (IDE-0019) y lista de corte (IDE-0023).
- Docs: mapa en `docs/README.md`; guía usuario `docs/user/GUIA-RAPIDA.md`;
  UAT visual `uat/studio/CHECKLIST-VISUAL.md`; planificación
  `docs/masterplan/REVIEW-2026-09-15-planificacion.md`.
- Versión de desarrollo: `0.4.4.dev0` (última estable: `0.4.3`).
- Próximo: cola IDE-0026 → 0027 → 0030 → 0025 → 0028 → 0029; piloto
  DT-0006 D; Issues = 0; eval IDE-0007 cerrada; LLM / plugins / C bloqueados.

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
