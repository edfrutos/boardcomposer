# BoardComposer — MASTERPLAN

Última revisión: 2026-10-29.

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
- Snapshot de planificación: `REVIEW-2026-10-29-planificacion.md`.

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
- Perfiles nombrados de preferencias, locales (IDE-0054 `#672`). Sin nube.
- Inspector de pieza: área L×A (IDE-0055 `#673`).
- Zoom del Workspace al 100% (**Ctrl+Alt+0**, IDE-0056 `#675`).
- Copiar texto del Inspector (**Ctrl+Alt+I**, IDE-0057 `#676`).
- Marca ● de sin guardar en la barra de ruta (IDE-0058 `#678`).
- Inspector de tablero: área de una hoja (IDE-0059 `#680`).
- Barra de estado: piezas colocadas / total (IDE-0060 `#682`).
- Copiar ruta del `.bcproj` (**Ctrl+Alt+Shift+C**, IDE-0061 `#683`).
- Clic en la etiqueta de zoom vuelve al 100% (IDE-0062 `#684`).
- Barra de estado: piezas seleccionadas (IDE-0063 `#686`).
- Copiar medidas L×A de una pieza (**Ctrl+Alt+Shift+D**, IDE-0064).
- Copiar medidas L×A de un tablero (**Ctrl+Alt+Shift+B**, IDE-0068).
- Barra de estado: tableros físicos (IDE-0069 `#692`).
- Barra de estado: kerf del proyecto (IDE-0065).
- Clic en `n sel.` ajusta el encuadre (IDE-0066).
- Clic en el kerf de la barra abre el espesor de sierra (IDE-0067).
- Clic en colocadas/total encuadra las piezas colocadas (IDE-0070).
- Clic en `n tab.` encuadra todos los tableros (IDE-0071).
- Copiar el espesor de sierra del proyecto (IDE-0072).
- Barra de estado: espesor del tablero enfocado (IDE-0073).
- Clic en el espesor del tablero abre su edición (IDE-0074).
- Copiar el espesor del tablero de la barra (IDE-0075).
- Barra de estado: material del tablero (IDE-0076).
- Copiar el material del tablero de la barra (IDE-0077).
- Clic en el material del tablero abre su edición (IDE-0078).
- Barra de estado: piezas omitidas (IDE-0079 `#706`).
- Clic en las piezas omitidas (IDE-0080 `#707`).
- Barra de estado: aprovechamiento del tablero enfocado (IDE-0081).
- Clic en el aprovechamiento selecciona ese tablero (IDE-0082).
- Copiar el aprovechamiento del tablero de la barra (IDE-0083).
- Barra de estado: material libre del tablero enfocado (IDE-0084).
- Copiar el material libre del tablero de la barra (IDE-0085).
- Clic en el material libre selecciona ese tablero (IDE-0086).
- Copiar las piezas colocadas de la barra (IDE-0087 `#715`).
- Copiar las piezas omitidas de la barra (IDE-0088 `#716`).
- Copiar los tableros físicos de la barra (IDE-0089 `#718`).
- Copiar la selección de la barra (IDE-0090).
- Copiar el zoom de la barra (IDE-0091).
- Barra de estado: retales de la solución seleccionada (IDE-0092 `#724`).
- Copiar los retales de la barra (**Ctrl+Alt+Shift+R**, IDE-0093 `#725`).
- Clic en los retales selecciona su tablero (IDE-0094).
- Barra de estado: índice de la solución seleccionada (IDE-0095).
- Copiar el índice de la solución (**Ctrl+Alt+Shift+L**, IDE-0096).
- Clic en el índice de la solución pasa a la siguiente (IDE-0097).
- Barra de estado: huecos internos de la solución seleccionada (IDE-0098).
- Copiar los huecos internos de la barra (IDE-0099; Ctrl+Alt+Shift+G).
- Clic en los huecos internos selecciona esa solución (IDE-0100).
- Barra de estado: estrategia de la solución seleccionada (IDE-0103).
- Copiar la estrategia de la barra (IDE-0104; Ctrl+Alt+Shift+Y).
- Clic en la estrategia selecciona esa solución (IDE-0105 `#742`).
- Barra de estado: piezas de la solución seleccionada (IDE-0106 `#743`).
- Copiar las piezas de la solución (IDE-0107; Ctrl+Alt+Shift+J).
- Clic en las piezas selecciona esa solución (IDE-0108).
- Barra de estado: omitidas de la solución seleccionada (IDE-0109).
- Copiar las omitidas de la solución (IDE-0110; Ctrl+Alt+Shift+Q).
- Clic en las omitidas selecciona esa solución (IDE-0111).
- Barra de estado: tableros de la solución seleccionada (IDE-0112).
- Copiar los tableros de la solución (IDE-0113; Ctrl+Alt+Shift+W).
- Clic en los tableros selecciona esa solución (IDE-0114).
- Barra de estado: puntuación de la solución seleccionada (IDE-0115).
- Copiar la puntuación de la solución (IDE-0116; Ctrl+Alt+Shift+V).
- Clic en la puntuación selecciona esa solución (IDE-0117).
- Barra de estado: tablero libre de la solución seleccionada (IDE-0118).
- Copiar el tablero libre de la solución (IDE-0119; Ctrl+Alt+Shift+E).
- Clic en el tablero libre selecciona esa solución (IDE-0120).
- Barra de estado: largo total de la solución seleccionada (IDE-0121).
- Copiar el largo total de la solución (IDE-0122; Ctrl+Alt+Shift+H).
- Clic en el largo total selecciona esa solución (IDE-0123).
- Barra de estado: ancho total de la solución seleccionada (IDE-0124).
- Copiar el ancho total de la solución (IDE-0125; Ctrl+Alt+Shift+X).
- Clic en el ancho total selecciona esa solución (IDE-0126).
- Barra de estado: área usada de la solución seleccionada (IDE-0127).
- Copiar el área usada de la solución (IDE-0128; Ctrl+Alt+Shift+A).
- Clic en el área usada selecciona esa solución (IDE-0129).
- Barra de estado: área de retales de la solución seleccionada (IDE-0130).
- Copiar el área de retales de la solución (IDE-0131; Ctrl+Alt+Shift+I).
- Clic en el área de retales selecciona esa solución (IDE-0132).
- Barra de estado: área envolvente de la solución seleccionada (IDE-0133).
- Copiar el área envolvente de la solución (IDE-0134; Ctrl+Alt+Shift+1).
- Clic en el área envolvente selecciona esa solución (IDE-0135).
- Barra de estado: área de huecos internos de la solución seleccionada
  (IDE-0136).
- Copiar el área de huecos internos de la solución (IDE-0137;
  Ctrl+Alt+Shift+2).
- Clic en el área de huecos internos selecciona esa solución
  (IDE-0138).
- Barra de estado: área de tablero libre de la solución seleccionada
  (IDE-0139).
- Copiar el área de tablero libre de la solución (IDE-0140;
  Ctrl+Alt+Shift+3).
- Clic en el área de tablero libre selecciona esa solución
  (IDE-0141).
- Barra de estado: área de tableros consumidos de la solución seleccionada
  (IDE-0142).
- Copiar el área de tableros consumidos de la solución (IDE-0143;
  Ctrl+Alt+Shift+4).
- Clic en el área de tableros consumidos selecciona esa solución
  (IDE-0144).
- Barra de estado: aprovechamiento de tableros de la solución seleccionada
  (IDE-0145).
- Copiar el aprovechamiento de tableros de la solución (IDE-0146;
  Ctrl+Alt+Shift+5).
- Clic en el aprovechamiento de tableros selecciona esa solución
  (IDE-0147).
- Barra de estado: piezas rotadas de la solución seleccionada
  (IDE-0148).
- Copiar las piezas rotadas de la solución (IDE-0149;
  Ctrl+Alt+Shift+6).
- Clic en las piezas rotadas selecciona esa solución (IDE-0150).
- Barra de estado: piezas sin rotar de la solución seleccionada
  (IDE-0151).
- Copiar las piezas sin rotar de la solución (IDE-0152;
  Ctrl+Alt+Shift+7).
- Clic en las piezas sin rotar selecciona esa solución (IDE-0153).
- Barra de estado: porcentaje de piezas rotadas de la solución
  seleccionada (IDE-0154).
- Copiar el porcentaje de piezas rotadas de la solución (IDE-0155;
  Ctrl+Alt+Shift+8).
- Clic en el porcentaje de piezas rotadas selecciona esa solución
  (IDE-0156).
- Barra de estado: porcentaje de piezas sin rotar de la solución
  seleccionada (IDE-0157).
- Copiar el porcentaje de piezas sin rotar de la solución (IDE-0158;
  Ctrl+Alt+Shift+9).
- Clic en el porcentaje de piezas sin rotar selecciona esa solución
  (IDE-0159).
- Barra de estado: aprovechamiento envolvente de la solución
  seleccionada (IDE-0160).
- Copiar el aprovechamiento envolvente de la solución (IDE-0161;
  Ctrl+Alt+Shift+0).
- Clic en el aprovechamiento envolvente selecciona esa solución
  (IDE-0162).
- Barra de estado: porcentaje de retales de la solución seleccionada
  (IDE-0163).
- Copiar el porcentaje de retales de la solución (IDE-0164;
  Ctrl+Alt+Shift+F1).
- Clic en el porcentaje de retales selecciona esa solución
  (IDE-0165).
- Barra de estado: puntuación de desperdicio de la solución
  seleccionada (IDE-0166).
- Copiar la puntuación de desperdicio de la solución (IDE-0167;
  Ctrl+Alt+Shift+F2).
- Clic en la puntuación de desperdicio selecciona esa solución
  (IDE-0168).
- Barra de estado: puntuación de uso de material de la solución
  seleccionada (IDE-0169).
- Copiar la puntuación de uso de material de la solución (IDE-0170;
  Ctrl+Alt+Shift+F3).
- Clic en la puntuación de uso de material selecciona esa solución
  (IDE-0171).
- Barra de estado: puntuación de cortes de la solución
  seleccionada (IDE-0172).
- Copiar la puntuación de cortes de la solución (IDE-0173;
  Ctrl+Alt+Shift+F4).
- Clic en la puntuación de cortes selecciona esa solución
  (IDE-0174).
- Barra de estado: puntuación de regularidad de la solución
  seleccionada (IDE-0175).
- Copiar la puntuación de regularidad de la solución (IDE-0176;
  Ctrl+Alt+Shift+F5).
- Clic en la puntuación de regularidad selecciona esa solución
  (IDE-0177).
- Barra de estado: puntuación de veta de la solución
  seleccionada (IDE-0178).
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

1. Ciclo `0.4.4`: duodécima ola cerrada (0078 `#702`); IDE-0079 `#706`;
   IDE-0080 `#707`. Decimotercera ola cerrada (0082 entregada). Decimocuarta
   ola cerrada (0086 entregada). IDE-0087 `#715`; IDE-0088 `#716`;
   IDE-0089 `#718`. Decimoquinta ola cerrada (0090 `#720`).
   Decimosexta ola cerrada (0094 entregada). Decimoséptima ola cerrada
   (0098 entregada).    Decimoctava ola: 0100 entregada. IDE-0101 e
   IDE-0102 diferidas (sin costes). Decimonovena ola cerrada (0106 `#743`).
   Vigésima ola cerrada (0110 entregada). Vigesimoprimera ola cerrada
   (0114 entregada). Vigesimosegunda ola cerrada (0118 entregada).
   Vigesimotercera ola cerrada (0122 entregada).    Vigesimocuarta ola
   cerrada (0126 `#766`). Vigesimoquinta ola cerrada (0130 `#771`).
   Vigesimosexta ola cerrada (0134 `#777`). Vigesimoséptima ola
   cerrada (0138 entregada). Vigesimoctava ola cerrada (0142
   entregada). Vigesimonovena ola cerrada (0146 entregada).
   Trigésima ola cerrada (0150 entregada). Trigésima primera ola
   cerrada (0154 entregada `#802`). Trigésima segunda ola cerrada
   (0158 entregada `#807`). Trigésima tercera ola cerrada (0162
   entregada). Trigésima cuarta ola cerrada (0166 entregada).
   Trigésima quinta ola cerrada (0170 entregada).
   Trigésima sexta ola cerrada (0174 entregada).
   Trigésima séptima ola cerrada (0178 entregada).
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
