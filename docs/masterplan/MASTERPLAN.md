# BoardComposer — MASTERPLAN

Última revisión: 2026-09-24.

## Estado actual

- Fase de producto: **Fase 2 — BoardComposer Studio** (núcleo usable;
  Fase 3 plataforma entregada).
- Versión de desarrollo: `0.4.4.dev0` (última estable: `0.4.3` /
  `v0.4.3` publicada).
- Core base consolidado y cubierto por tests (incluye kerf IDE-0020,
  veta IDE-0021, Skyline multipanel IDE-0022 y freeze/re-pack IDE-0030).
- Studio dispone de flujo funcional de proyecto, edición, cálculo y exportación
  (lista de corte IDE-0023; swap IDE-0019; metadatos IDE-0024;
  etiquetas IDE-0026; secuencia IDE-0027).
- Vertical multipanel MaxRects **y** Skyline, con compatibilidad de material
  y espesor, Workspace interactivo y suite Qt de arrastre/reasignación.
- Snapshot de planificación: `REVIEW-2026-09-24-planificacion.md`.

## Último bloque consolidado

### Packing multipanel

- `StockPanel` con cantidad.
- `PanelReference` por tipo e instancia física.
- MaxRects multipanel con compatibilidad de **espesor y material**.
- Validación, completitud, deduplicación y scoring por panel.
- Persistencia Studio versionada (migraciones ADR-015; v3 metadatos, v4 kerf,
  v5 grain, v6 remnant).
- Workspace y SVG con paneles físicos lado a lado.
- Movimiento y reasignación interactiva de piezas entre paneles (arrastre en
  Workspace, con undo; incompatibilidad revierte; solape ajusta al hueco).
- Intercambio de dos piezas colocadas (**Ctrl+Alt+X**, IDE-0019).
- Colocación manual asistida / sugerir hueco (**Ctrl+Alt+G**, IDE-0036).
- Kerf / espesor de sierra en packing (**Ctrl+Alt+K**, IDE-0020).
- Veta fija por pieza (**Permitir rotación**, IDE-0021).
- Lista de corte / informe taller (**Ctrl+Alt+C**, IDE-0023).
- Etiquetas de piezas en plano SVG/PDF/DXF (IDE-0026).
- Etiquetas de retales (LxW mm) en plano SVG/PDF/DXF (IDE-0033).
- Cotas L×A del tablero en plano SVG/PDF/DXF (IDE-0037).
- Calidad raster PNG/JPEG (DPI y calidad JPEG, IDE-0038).
- Trazabilidad en plano (versión, algoritmo, fecha; IDE-0039) y en
  lista de corte / presupuesto PDF (IDE-0043).
- Unidades de display en Inspector mm/cm/in (IDE-0040 `#653`; disco sigue mm),
  etiquetas de plano / Workspace (IDE-0044), Comparador (IDE-0047) y
  lista de corte / presupuesto PDF (IDE-0048).
- Inspector de pieza: espesor, rotación y veta (IDE-0046).
- Inspector de raíz/categoría: conteos, materiales y área (IDE-0050).
- Inspector de tablero: aprovechamiento de panel (IDE-0051).
- Preview del Workspace al terminar Calcular layout, sin aplicar
  (IDE-0052 `#667`).
- Material por defecto de taller para tableros y piezas nuevos
  (IDE-0053 `#671`). Preferencias; no va en el `.bcproj`.
- Perfiles nombrados de preferencias, locales (IDE-0054). Sin nube.
- Inspector de pieza: área L×A (IDE-0055).
- Capas DXF por rol PANELS/PIECES/OFFCUTS/DIMS (IDE-0041 `#654`).
- Secuencia de corte por panel (IDE-0027; orden de sierra en CSV/PDF y números en plano).
- Congelar layout OK y re-empaquetar omitidas (**Ctrl+Alt+F**, IDE-0030).
- Retales a inventario del mismo proyecto (**Ctrl+Alt+R**, IDE-0025).
- Catálogo de materiales / espesores / L×A de usuario (**Ctrl+Alt+T**,
  IDE-0028/0031); export/import JSON (IDE-0042). Preferencias de taller
  también export/import JSON (IDE-0049).
- Coste estimado de material (precio €/m² del catálogo; IDE-0029).
- Presupuesto de material PDF (**Ctrl+Alt+Q**, IDE-0032) con mano de
  obra opcional (IDE-0045; EUR/h × min/pieza en Preferencias).
- Packing Skyline multipanel (IDE-0022; junto a MaxRects).
- ADR-014 / ADR-016 y documentación técnica alineada en README, backlog y UAT.

## Próxima tarea única

1. Ciclo `0.4.4` séptima ola: IDE-0056 (0055 entregada; quedan 0056…0058).
2. Mantener piloto DT-0006 D; no abrir C sin multi-usuario.
3. Backlog grande bloqueado hasta demanda real:
   - DT-0006 **C** (API revisiones + ACL) — solo multi-usuario real + DOC-010.
   - IDE-0007 LLM opt-in — tras política de datos (eval cerrada; DEC-0011).
   - IDE-0008 plugins — XL; no priorizar sin ADR-004 operativo.

## Criterio de finalización del próximo bloque

- Docs de pantalla (SCR) no contradicen el Studio implementado.
- El flujo UAT se completa sin errores ni pérdida de asignación física.
- Inspector y Workspace identifican correctamente panel e instancia.
- Defectos encontrados tienen test de regresión cuando sea viable.
- Ruff y Pytest limpios en CI.

## Límites conocidos

- MaxRects y Skyline implementan el contrato multipanel completo
  (CP-SAT exacto sigue siendo un solo panel, opcional).
- Una sola candidata tras «Calcular layout» es válida: el pipeline puede
  deduplicar a una solución única según inventario y heurísticas.
- Retales (ADR-016) se reportan y, con **Ctrl+Alt+R**, pueden pasar a
  inventario remnant del mismo `.bcproj` (IDE-0025). Sin librería entre
  proyectos.
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
