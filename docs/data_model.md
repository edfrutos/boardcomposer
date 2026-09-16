# Modelo de datos

Última revisión: 2026-09-16.

## Entidades principales

### Board

Pieza rectangular que debe colocarse. Contiene largo, ancho, espesor, ID,
`material` (por defecto `"Generico"`) y `grain` (`none` o `locked`;
IDE-0021). `material_key` normaliza mayúsculas y espacios para comparar
compatibilidad con un panel. `locked` impide rotar en packing y en Studio
(**R**).

### StockPanel

Tipo de tablero disponible: dimensiones, espesor, ID opcional, `quantity` y
`material` (mismas reglas de normalización que `Board`). Una cantidad mayor
que uno representa varias unidades físicas equivalentes. En Studio, un
tablero puede marcarse `remnant` (IDE-0025 / `.bcproj` v6) si nació de un
retal promovido; el Core lo trata como stock normal.

### PanelReference

Referencia interna estable a una unidad física:

- `stock_panel_index`: índice en `Project.stock_panels`;
- `instance_index`: unidad dentro de `StockPanel.quantity`.

Los índices comienzan en cero. Los IDs de usuario no actúan como clave interna.

### Project

Agrupa piezas, inventario de paneles y restricciones. `kerf_mm` (IDE-0020)
es el hueco de sierra. Expone las instancias físicas mediante
`stock_panel_instances()` y resuelve referencias con `stock_panel_for()`.

### BoardPlacement

Posición, dimensiones efectivas y rotación de una pieza. `panel_reference` es
opcional para compatibilidad legacy. En multipanel, sus coordenadas son locales
al panel físico.

### Offcut

Región rectangular sobrante en un panel físico consumido: `panel_reference`,
posición y dimensiones locales al panel, y `area_mm2`. El reporte es
informativo (ADR-016). IDE-0025 puede promoverlos a tableros `remnant` del
mismo `.bcproj` (**Ctrl+Alt+R**).

### AssemblySolution

Colección de colocaciones con score y explicación. Expone:

- área usada y bounding area;
- paneles consumidos;
- área usada/desperdicio por panel;
- desperdicio total sobre paneles consumidos;
- `omitted_piece_ids`: piezas que no pudieron colocarse (solución parcial);
- `is_complete`: `True` cuando `omitted_piece_ids` está vacío;
- `offcuts` y `total_offcut_area_mm2`: retales reportados y su área total.

### ValidationResult

Separa dos conceptos:

- `complete`: todas las piezas esperadas aparecen exactamente una vez;
- `valid`: cumple geometría, espesor, material, veta y límites. Una pieza sin
  colocar (`missing_board_ids`) ya **no** invalida la solución por sí sola:
  se trata como un motivo "blando" que produce una solución parcial válida,
  a diferencia de solapes, límites excedidos o incompatibilidad de
  espesor/material entre pieza y panel, que sí son motivos "duros".

## Compatibilidad

Sin `StockPanel`, el modelo usa el plano único y `ProjectConstraints`. Con
inventario, las dimensiones físicas de cada panel sustituyen los límites
globales como frontera de colocación, y espesor **y material** deben
coincidir entre pieza y panel.

Consulta ADR-014 (contrato multipanel), ADR-015 (migraciones de `.bcproj`,
hoy `CURRENT_VERSION` 6) y ADR-016 (retales) para el detalle normativo.
