# AI Context

Nombre del proyecto: BoardComposer.

## Propósito

Generar, validar, puntuar, comparar y explicar composiciones de corte 2D sobre
material disponible. BoardComposer no impone una única respuesta: presenta
alternativas comprensibles para que el usuario decida.

## Estado actual — 2026-09-17

- Fase de producto: Fase 2 Studio (núcleo usable) + Fase 3 plataforma
  entregada (EP-001…003).
- Core base completado y en evolución controlada (kerf IDE-0020; grain
  IDE-0021; Skyline multipanel IDE-0022; freeze/re-pack IDE-0030).
- Vertical multipanel MaxRects **y** Skyline, con compatibilidad de material
  y espesor, órdenes de panel, retales (ADR-016; inventario IDE-0025) y soluciones
  parciales (piezas omitidas en vez de "sin solución").
- Studio funcional con persistencia versionada y migraciones explícitas
  (ADR-015; v3 metadatos, v4 kerf, v5 grain, v6 remnant), importación de inventario,
  movimiento entre paneles, swap (IDE-0019), lista de corte (IDE-0023),
  etiquetas en plano (IDE-0026), secuencia de sierra (IDE-0027),
  freeze/re-pack (IDE-0030), retales a inventario (IDE-0025) y etiquetas
  de retal (IDE-0033).
- Catálogo de materiales / espesores / precio €/m² / medidas L×A
  (IDE-0028/0029/0031; `~/.boardcomposer/material_catalog.json`;
  **Ctrl+Alt+T**). Coste = tableros físicos × precio; no puntúa el solver.
- PDF de plano: papel / márgenes / escala (IDE-0034); default ajustar al
  dibujo. Lista de corte y presupuesto siguen A4.
- Docs: mapa en `docs/README.md`; guía usuario `docs/user/GUIA-RAPIDA.md`;
  UAT visual `uat/studio/CHECKLIST-VISUAL.md`; planificación
  `docs/masterplan/REVIEW-2026-09-17-planificacion.md`.
- Versión de desarrollo: `0.4.4.dev0` (última estable: `0.4.3` /
  `v0.4.3` publicada).
- Próximo: cerrar IDE-0036 (`#645`) → IDE-0035; piloto
  DT-0006 D; Issues = 0; eval IDE-0007 cerrada; LLM / plugins / C bloqueados.
  Sin IDE nuevas (cola implementable aún abierta).

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
