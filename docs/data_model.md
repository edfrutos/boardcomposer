# Modelo de datos

Última revisión: 2026-07-16.

## Entidades principales

### Board

Pieza rectangular que debe colocarse. Contiene largo, ancho, espesor e ID.

### StockPanel

Tipo de tablero disponible: dimensiones, espesor, ID opcional y `quantity`.
Una cantidad mayor que uno representa varias unidades físicas equivalentes.

### PanelReference

Referencia interna estable a una unidad física:

- `stock_panel_index`: índice en `Project.stock_panels`;
- `instance_index`: unidad dentro de `StockPanel.quantity`.

Los índices comienzan en cero. Los IDs de usuario no actúan como clave interna.

### Project

Agrupa piezas, inventario de paneles y restricciones. Expone las instancias
físicas mediante `stock_panel_instances()` y resuelve referencias con
`stock_panel_for()`.

### BoardPlacement

Posición, dimensiones efectivas y rotación de una pieza. `panel_reference` es
opcional para compatibilidad legacy. En multipanel, sus coordenadas son locales
al panel físico.

### AssemblySolution

Colección de colocaciones con score y explicación. Expone:

- área usada y bounding area;
- paneles consumidos;
- área usada/desperdicio por panel;
- desperdicio total sobre paneles consumidos.

### ValidationResult

Separa dos conceptos:

- `complete`: todas las piezas esperadas aparecen exactamente una vez;
- `valid`: además cumple geometría, inventario, espesor y límites.

## Compatibilidad

Sin `StockPanel`, el modelo usa el plano único y `ProjectConstraints`. Con
inventario, las dimensiones físicas de cada panel sustituyen los límites
globales como frontera de colocación.

Consulta ADR-014 para el contrato normativo.
