# CHANGELOG — BoardComposer

## Unreleased — 0.4.0.dev0 — 2026-07-16

### Añadido

- `StockPanel.quantity` como inventario de unidades físicas.
- `PanelReference` para asignar colocaciones a tipo e instancia de panel.
- Packing MaxRects sobre múltiples paneles y tipos de espesor compatible.
- Validación de referencia, límites, espesor y solapes por panel físico.
- Estado completo/parcial en `ValidationResult`.
- Métricas de área usada y desperdicio por panel consumido.
- Persistencia Studio versión 2 compatible con proyectos versión 1.
- Cantidad y espesor editables en tableros y piezas de Studio.
- Disposición visual y exportación SVG de paneles lado a lado.
- ADR-014 con el contrato multipanel.
- Compatibilidad de **material** (además de espesor) entre pieza y panel,
  validada en el solver y enrutada por `multi_panel_maxrects`.
- Búsqueda de órdenes de panel (`panel_ordering.py`) como eje adicional del
  generador MaxRects, junto a heurísticas y órdenes de pieza.
- **Retales aprovechables** (`Offcut`) reportados de forma informativa por
  panel consumido, en Inspector, SVG y presentadores JSON/texto (ADR-016).
- Soluciones **parciales**: piezas que no caben se reportan como
  `omitted_piece_ids` en vez de descartar toda la solución.
- Migraciones explícitas y versionadas de `.bcproj`, con
  `UnsupportedProjectVersionError` para ficheros de una versión futura
  desconocida (ADR-015).
- Importación de inventario de tableros desde CSV
  (`Proyecto → Importar inventario de tableros (CSV)…`), con vista previa,
  validación por fila y detección de duplicados.
- Campo de cantidad al crear una pieza nueva, generando varios ids
  correlativos de una sola vez.
- Movimiento y reasignación interactiva de piezas entre paneles físicos
  distintos desde el Workspace, arrastrando la pieza sobre el panel destino.
- Identificador e instancia de panel físico visibles en el Inspector de
  pieza.
- Resaltado de "puntos clave" (mejor solución por métrica) en el comparador
  de soluciones de Studio (SCR-003).
- Diagnóstico con estadísticas del solver cuando no se encuentra ninguna
  solución.
- Suite de pruebas de interacción Qt para el Workspace (arrastre,
  reasignación de panel, selección, reversión de movimientos inválidos).
- Script de benchmarks reproducibles para `multi_panel_maxrects`
  (`scripts/benchmark_multipanel_maxrects.py`).
- Generador exacto CP-SAT de un solo panel (opcional,
  `pip install 'boardcomposer[cp_sat]'`, estrategia `exact`, ADR-017).
- Comparador: ordenar por métrica y filtrar «solo completas» (SCR-003).
- Exportación DXF y PDF de la solución seleccionada (además de SVG).
- Importación de piezas desde CSV (`Proyecto → Importar piezas (CSV)…`).
- Revisión UI `docs/masterplan/ui/REVIEW-2026-07-17.md`.
- Preferencias de Studio (SCR-006): estrategia y pesos de scoring en
  `~/.boardcomposer/preferences.json` (`Editar → Preferencias…`).
- Miniaturas SVG sincronizadas en el comparador de soluciones (misma escala).
- Importación CSV/Excel (`.xlsx`) de tableros y piezas (FLW-002), sin
  dependencias extra (lector OOXML mínimo).
- Panel de diferencias del comparador (SCR-003): métricas y colocaciones
  respecto a una solución de referencia fijable.
- Exportación JSON y CSV de la solución seleccionada (SCR-007).
- Preferencias ampliadas SCR-006: tema (sistema/claro/oscuro), mostrar
  cuadrícula y tamaño de grid persistidos en `preferences.json`.
- Pantalla de inicio SCR-001 con acciones principales, recientes
  persistidos y acceso a preferencias/ejemplo.
- Diálogo de exportación SCR-007 con formato, opciones (métricas,
  explicación, retales), vista previa y recuerdo de la última elección.
- Preferencias SCR-006: idioma (es/en), unidades (mm/cm/in) aplicadas a
  inspector, explorador y formularios; defaults de exportación editables.
- Miniaturas reales de proyectos recientes en la pantalla de inicio
  (SCR-001): SVG del layout del `.bcproj` más fecha de modificación.
- Vista previa gráfica SVG embebida en el diálogo de exportación
  (SCR-007), actualizada al cambiar formato u opciones.
- Idioma es/en aplicado a menús, docks, Inspector y comparador (SCR-006).
- Plantillas de exportación nombradas en el diálogo SCR-007
  (`~/.boardcomposer/export_templates.json`).
- i18n es/en de diálogos (export/import) y mensajes de la barra de estado.
- i18n es/en de formularios Nuevo/Editar tablero y pieza.
- i18n es/en del panel de diferencias del comparador (SCR-003).
- Perfiles de exportación por cliente (plantillas SCR-007 con campo
  `client` y filtro en el diálogo).
- Tema visual «Industrial madera»: tokens + QSS (claro/oscuro), fuentes
  Archivo / Source Sans 3, y pantalla de inicio brand-first (`docs/DESIGN.md`).
- Colores del canvas/workspace alineados al tema (tablero, pieza, selección,
  validación y grid).
- Paleta SVG Industrial madera en exportación y miniaturas (inicio,
  comparador, vista previa de export).
- Compartir plantillas de exportación entre equipos (pack JSON).
- Plantillas de proyecto (guardar / nuevo desde plantilla).
- Accesos a documentación y novedades (menú Ayuda + pantalla de inicio).
- Preferencias avanzadas: tope de soluciones y progreso al calcular layout
  (FLW-003 / SCR-006).
- Cancelación cooperativa del solver (`CancellationToken`) con botón
  Cancelar en el diálogo de progreso de layout (FLW-003).
- Timeline MVP (ADR-005): dock alimentado por el Event Bus (ADR-003) con
  filtro por tipo de evento y vaciado; publicación de hechos clave
  (proyecto, CSV, cálculo, selección, export, workspace).
- Reproducción paso a paso de colocaciones de la solución seleccionada
  en el Timeline (Inicio / ◀ / ▶ / Play), sin mutar el proyecto.
- Detección de soluciones desactualizadas al editar el proyecto (FLW-006):
  banner en el Comparador, aviso al aplicar y eventos `ProjectModified` /
  `SolutionsMarkedOutdated`.
- Comparador sincronizado con la reproducción del Timeline: el panel de
  diferencias muestra el divergencia paso a paso vs la referencia (SCR-003).
- Trazas de algoritmo del solver (`SolveTrace`): el Timeline registra
  `AlgorithmStarted` / `AlgorithmFinished` / `EvaluationFinished`, y el
  replay etiqueta el generador y la pieza actual (ADR-005).
- Exportación del historial del Timeline a JSON/CSV (menú Exportar y botón
  en el dock) respetando el filtro activo.
- Instrumentación de fallos de colocación MaxRects (`incompatible` / `no_fit`)
  en la traza del solver y el Timeline (`PlacementFailed` + resumen).
- Filtro del Timeline por algoritmo y métricas temporales (`duration_ms`) en
  `AlgorithmFinished` / `EvaluationFinished` (ADR-005).
- Marcadores/anotaciones de usuario en el Timeline (`TimelineMarked`) con
  nota libre y contexto opcional del replay (algoritmo, pieza, paso).
- Filtro del Timeline por intervalo temporal (presets 1/5/15 min y 1 h),
  respetado también al exportar (`since` / `period_seconds`).
- Instrumentación de fallos de colocación Skyline (`no_fit`) en la traza
  y el Timeline; captura activa para todos los generadores instrumentados.
- Reproducción de fases del solver en el Timeline (modo Colocaciones /
  Fases): recorre `SolveTrace` y sincroniza solución/pieza cuando aplica.
- Clic en un hecho del Timeline para buscar contexto (algoritmo → solución,
  pieza fallida, índice de solución, nota de marcador).
- Asistente de mapeo de columnas al importar CSV/Excel cuando no se
  reconocen cabeceras obligatorias (FLW-002).
- Selector de hoja al importar libros Excel con varias hojas; el preview
  muestra el id aunque la fila sea inválida.
- Importación CSV/Excel de tableros y piezas deshacible (Ctrl+Z) con
  `ImportBoardsCommand` / `ImportPiecesCommand`.
- Plantillas de mapeo de columnas al importar CSV/Excel: se guardan y
  reaplican automáticamente cuando el archivo trae las mismas cabeceras.
- Tras exportar una solución, diálogo para abrir el archivo o mostrar su
  carpeta; eventos `ExportStarted` / `ExportFailed` en el Timeline (FLW-005).
- Eliminar plantillas de mapeo de columnas desde el asistente de
  importación CSV/Excel.
- Duplicar la pieza seleccionada (`Editar → Duplicar pieza`, Ctrl+D) con
  undo/redo.
- Diálogo de cambios sin guardar con nombre del proyecto, ruta o aviso de
  «aún no guardado», botones traducidos y error explícito si falla el
  guardado.
- Diálogo «Nuevo proyecto» con nombre y unidades; `project_id` único y
  evento `WorkspaceOpened` al abrir el Workspace (FLW-001).
- Editar pieza o tablero con undo/redo (`EditPieceCommand` /
  `EditBoardCommand`), actualizando ids en colocaciones.
- Menú contextual en el Explorador: editar/duplicar/eliminar pieza,
  editar tablero, añadir en categorías y vista previa de solución.
- Eliminar tablero desde el Explorador con undo (`DeleteBoardCommand`);
  se quitan colocaciones del tablero y se conservan las piezas.
- Renombrar proyecto (`Proyecto → Renombrar…` o clic derecho en la raíz
  del Explorador) con undo, sin marcar soluciones como desactualizadas.
- Diálogo **Ayuda → Atajos de teclado…** con catálogo compartido
  (`studio/keyboard_shortcuts.py`); incluye atajos de archivo (Ctrl+N/O/S)
  y preferencias además de undo/redo/rotar/duplicar/eliminar.
- Menú **Ver**: Ajustar al tablero (Ctrl+0) y Mostrar cuadrícula (Ctrl+G),
  persistiendo `show_grid` sin resetear el zoom.
- Vaciar lista de proyectos recientes desde **Archivo → Abrir recientes**
  o la pantalla de bienvenida (confirma; no borra ficheros).
- Menús **Generar** y **Comparar** poblados (Calcular layout; navegar/aplicar
  solución); se elimina el menú Herramientas vacío.
- Menú **Ver**: Acercar / Alejar (Ctrl+= / Ctrl+-), además de ajustar y
  cuadrícula.
- Higiene de proyectos recientes: se podan rutas inexistentes al refrescar
  el menú/bienvenida, y se quita la entrada si falla al abrir.
- Tips en la barra de estado al pasar el ratón sobre las acciones de menú
  (`setStatusTip`, i18n es/en).
- Ruta del proyecto en la barra de estado (permanente) y
  **Proyecto → Abrir carpeta del proyecto** (también en el Explorador).
- **Editar → Seleccionar todas las piezas** (Ctrl+A) en el Workspace.
- **Editar → Deseleccionar piezas** (Escape) para limpiar la selección del
  canvas.
- **Editar → Invertir selección** (Ctrl+Shift+I) en el Workspace.
- CTA de primeros pasos en el Workspace cuando el proyecto no tiene
  tableros ni piezas (añadir/importar).
- Barra de herramientas principal (archivo, undo, zoom, generar, comparar,
  exportar) con toggle en **Ver**.
- Persistencia de geometría de ventana y disposición de docks/toolbar en
  preferencias (se restaura al reabrir Studio).
- Clic izquierdo en el canvas vacío (o fuera de una pieza) deselecciona.
- Duplicar tablero desde el menú contextual del Explorador (con undo).
- Contadores en cabeceras del Explorador: Tableros/Piezas/Soluciones `(n)`.
- Selección de pieza en el Workspace se refleja en el Explorador (y se limpia
  al deseleccionar).
- Selección desde el Explorador: Inspector de pieza completo (posición/panel) y
  al elegir un tablero se limpia la selección del canvas.
- Confirmación al eliminar una pieza (menú, Backspace o Explorador), alineada
  con la de tableros.
- Seleccionar un tablero en el Explorador lo resalta y centra en el Workspace.
- Clic en un tablero del canvas lo enfoca y sincroniza Explorador e Inspector.
- Menú Ver: mostrar/ocultar Explorador, Inspector, Timeline y Comparador.
- Nivel de zoom del Workspace como porcentaje en la barra de estado.
- Desplazar el Workspace con el botón medio del ratón (también sobre piezas).
- Doble clic en una solución del Explorador para verla en vista previa.
- Tecla Delete como atajo alternativo a Backspace para eliminar pieza;
  Ayuda → Atajos muestra también las secuencias alternativas.
- Menú Ver → Restablecer disposición de ventana (docks, toolbar y tamaño).
- Copiar ID de pieza/tablero desde el menú contextual del Explorador.
- Renombrar pieza/tablero desde el menú contextual del Explorador (con undo).
- Desplazar el Workspace con Espacio + arrastre (además de botón medio/derecho).
- Centrar la cámara al seleccionar una pieza en el Explorador.
- Renombrar con F2 la pieza, tablero o proyecto seleccionado.
- Doble clic en pieza/tablero del canvas para editar (vacío ajusta la vista).
- Mover la pieza seleccionada con las flechas (Shift = 10 mm).
- Editar pieza/tablero seleccionado con Enter (Editar…).
- Icono propio de BoardComposer Studio (ventana / Acerca de).
- Ver → Ajustar a la selección (Ctrl+Shift+0).
- Copiar ID de la pieza/tablero seleccionado (Ctrl+Shift+C).
- Shift+flechas mueven la pieza según el tamaño de cuadrícula.
- Ctrl+D duplica la pieza o el tablero seleccionado/enfocado.
- Delete/Backspace elimina la pieza o el tablero seleccionado/enfocado.
- Re Pág / Av Pág navegan entre soluciones candidatas (Comparar).
- Ctrl+Shift+Return aplica la solución candidata al proyecto.
- Ctrl+Shift+E exporta la solución seleccionada.
- Ctrl+Shift+P abre el diálogo para añadir una pieza.
- Ctrl+Shift+B abre el diálogo para añadir un tablero.
- Ctrl+Shift+O importa piezas desde CSV o Excel.
- Ctrl+Shift+T importa inventario de tableros desde CSV o Excel.
- Ctrl+Shift+L exporta el historial del Timeline.
- Ctrl+Shift+H vuelve a la pantalla de inicio.
- Ctrl+Shift+R abre la carpeta del archivo `.bcproj`.
- F1 abre el catálogo de atajos de teclado.
- Ctrl+Shift+W restablece la disposición de docks, toolbar y ventana.
- Ctrl+Shift+N crea un proyecto desde una plantilla.
- Ctrl+Shift+M guarda el proyecto actual como plantilla.
- Ctrl+Shift+U abre las novedades del CHANGELOG.
- Ctrl+Shift+D abre el proyecto de ejemplo.
- Shift+F1 abre la documentación local.
- Ctrl+Shift+A abre Acerca de BoardComposer.
- Ctrl+Shift+F2 renombra el proyecto actual.
- Ctrl+Q cierra BoardComposer Studio.
- Ctrl+Shift+X vacía la lista de proyectos recientes.
- Ctrl+Shift+K muestra u oculta la barra de herramientas.
- Ctrl+1 muestra u oculta el Explorador.
- Ctrl+2 muestra u oculta el Inspector.
- Ctrl+3 muestra u oculta el Timeline.
- Ctrl+4 muestra u oculta el Comparador de soluciones.
- Tip de estado de Calcular layout incluye Ctrl+Return.
- Tip de estado de Guardar incluye Ctrl+S.
- Tip de estado de Mostrar cuadrícula incluye Ctrl+G.
- Tip de estado de Deshacer incluye Ctrl+Z.
- Tip de estado de Rehacer incluye Ctrl+Shift+Z.
- Tip de estado de Rotar pieza incluye R.
- Importación CSV de piezas ya no apila todas en la misma esquina.
- Tip de estado de Abrir incluye Ctrl+O.
- Cierre de Studio tolera Ctrl+C / SIGINT sin traceback en closeEvent.
- Tip de estado de Nuevo proyecto incluye Ctrl+N.
- Tip de estado de Guardar como incluye Ctrl+Shift+S.
- Tip de estado de Preferencias incluye Ctrl+,.
- Tip de estado de Ajustar al tablero incluye Ctrl+0.
- Tip de estado de Ajustar a la selección incluye Ctrl+Shift+0.
- Tip de estado de Acercar incluye Ctrl+=.
- Tip de estado de Alejar incluye Ctrl+-.

### Cambiado

- El pipeline utiliza MaxRects cuando el proyecto declara inventario físico.
- El scoring de aprovechamiento usa el área de panel consumida.
- La deduplicación incluye la asignación física de panel.
- README, contexto de IA, roadmap, backlog y documentación técnica alineados.
- Versión de paquete actualizada a `0.4.0.dev0`.

### Compatibilidad

- Los proyectos sin `StockPanel` conservan restricciones y coordenadas legacy.
- Los ficheros Studio versión 1 cargan espesor 19 mm, cantidad 1 y panel sin
  asignar como valores por defecto (ahora vía migración explícita v1→v2).

### Documentación y limpieza

- README, ROADMAP, TODO, AI_CONTEXT, DECISIONS y masterplan (INDEX,
  DOC-003/004/005/006) alineados con el estado post-PR #21.
- Checklist UAT multipanel en `uat/multipanel/CHECKLIST.md`.
- Eliminados prototipos obsoletos (`workbench/`, `tools/visualize_demo.py`,
  `out/demo.html`) y directorios vacíos.

## 0.3.0-stable — 2026-07-11

### Añadido-1

- Edición de proyectos, tableros y piezas en Studio.
- Generación, selección y aplicación de varias soluciones.
- Exportación SVG y persistencia de proyectos.
- Validación, evaluación y deduplicación centralizadas.

## 0.1-prototype — 2026-06-27

### Añadido-2

- Primer motor funcional con layouts básicos y free-space.
- CLI, CSV, presentadores y pruebas iniciales.

## 0.0.1 — 2026-06-26

### Añadido-3

- Documentación fundacional.
- Estructura base del proyecto.
- Backlog y decisiones iniciales.
