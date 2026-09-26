# AI Context

Nombre del proyecto: BoardComposer.

## Propósito

Generar, validar, puntuar, comparar y explicar composiciones de corte 2D sobre
material disponible. BoardComposer no impone una única respuesta: presenta
alternativas comprensibles para que el usuario decida.

## Estado actual — 2026-09-26

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
  **Ctrl+Alt+T**). Export/import JSON (IDE-0042 `#655`); sin nube.
  Coste = tableros físicos × precio; no puntúa el solver.
- PDF de plano: papel / márgenes / escala (IDE-0034); default ajustar al
  dibujo. Lista de corte y presupuesto siguen A4.
- Exportar lote de candidatas del ranking (IDE-0035); carpeta con
  `boardcomposer-solution-01…`. EP-002 sigue siendo CLI de proyectos.
- Workspace: sugerir hueco (IDE-0036); **Ctrl+Alt+G**; drop inválido por
  solape ajusta al hueco más cercano.
- Exportar: cotas L×A del tablero en plano (IDE-0037; `#647`); SVG/PDF/DXF;
  casilla en diálogo y Preferencias. Default: sí.
- Exportar: calidad raster PNG/JPEG (IDE-0038; `#649`); DPI 36–300 (default 96)
  y calidad JPEG 1–100 (default 90).
- Exportar: trazabilidad en plano (IDE-0039; `#651`) y en lista de corte
  / presupuesto PDF (IDE-0043 `#657`); pie versión / algoritmo / fecha.
  CSV de corte no. Casilla Preferencias. Default: sí.
- Inspector: unidades de Preferencias mm/cm/in (IDE-0040 `#653`) en pieza,
  tablero y métricas de layout; disco / JSON siguen mm.
- Comparador: Largo/Ancho y diffs siguen `prefs.units` (IDE-0047 `#662`).
- Lista de corte / presupuesto PDF: TEXT sigue `prefs.units` (IDE-0048);
  CSV/JSON y área m² siguen mm.
- Inspector de pieza: espesor, rotación 0°/90° y veta (IDE-0046).
- Exportar / Workspace: etiquetas de plano usan `prefs.units` (IDE-0044 `#658`);
  geometría y `$INSUNITS` siguen mm.
- Presupuesto PDF: mano de obra opcional (IDE-0045 `#659`) EUR/h × min/pieza
  en Preferencias; 0 omite; material sigue catálogo EUR/m².
- Exportar DXF: capas por rol (IDE-0041 `#654`) PANELS/PIECES/OFFCUTS/DIMS/SEQ/META.
- Docs: mapa en `docs/README.md`; guía usuario `docs/user/GUIA-RAPIDA.md`;
  UAT visual `uat/studio/CHECKLIST-VISUAL.md`; planificación
  `docs/masterplan/REVIEW-2026-09-26-planificacion.md`.
- Versión de desarrollo: `0.4.4.dev0` (última estable: `0.4.3` /
  `v0.4.3` publicada).
- Preferencias: export/import JSON de taller (IDE-0049 `#664`); sin rutas
  locales ni ventana; fusionar o reemplazar; sin nube.
- Inspector raíz/categoría: conteos, materiales y área (IDE-0050 `#665`).
- Inspector tablero: aprovechamiento de panel (IDE-0051 `#666`).
- Preview canvas al terminar Calcular layout, sin aplicar (IDE-0052 `#667`).
- Material por defecto de taller (IDE-0053 `#671`): tableros y piezas nuevos;
  no va en el `.bcproj`.
- Perfiles nombrados de preferencias, locales (IDE-0054 `#672`).
- Inspector de pieza: área (IDE-0055 `#673`).
- Zoom del Workspace al 100% (IDE-0056 `#675`; Ctrl+Alt+0).
- Próximo: cerrar `#676` (IDE-0057) → IDE-0058; piloto DT-0006 D;
  Issues = 0; eval IDE-0007 cerrada; LLM / plugins / C bloqueados.

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
