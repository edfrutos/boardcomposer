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
