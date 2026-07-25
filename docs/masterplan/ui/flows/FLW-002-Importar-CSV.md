# FLW-002 — Importar CSV/Excel

**Módulo:** BoardComposer Studio

**Código:** FLW-002  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 25/07/2026

---

## Objetivo

Describir cómo el usuario importa **inventario de tableros** o **piezas**
desde CSV o Excel (`.xlsx` / `.xlsm`), con resolución de cabeceras,
plantillas de mapeo, vista previa y commit deshacible.

---

## Actor principal

- Usuario.

---

## Precondiciones

- No hace falta proyecto previo: si no hay uno abierto, Studio crea un
  proyecto vacío al iniciar la importación.
- Archivo CSV o Excel con al menos las columnas obligatorias (o un mapeo /
  plantilla que las cubra).

---

## Trigger

| Acción | Atajo / menú / CTA |
|--------|---------------------|
| Importar inventario de tableros (CSV/Excel)… | **Ctrl+Shift+T** · menú Proyecto · overlay vacío Workspace |
| Importar piezas (CSV/Excel)… | **Ctrl+Shift+O** · menú Proyecto · overlay vacío · Welcome |

Filtro de archivo: CSV y Excel (`dialog.filter_csv_excel`).

---

## Flujo principal — tableros o piezas

1. El usuario dispara la acción correspondiente (menú, atajo o CTA).
2. Si no hay proyecto, Studio carga uno vacío.
3. Selector de archivo (CSV / `.xlsx` / `.xlsm`).
4. Si es Excel con **más de una hoja**, Studio pide cuál usar
   (`_prompt_xlsx_sheet`); una sola hoja → primera por defecto.
5. `load_tabular_file` lee cabeceras y filas (`studio/tabular_file.py`).
6. Auto-match de cabeceras (`resolve_header_map` + aliases en
   `studio/import_headers.py`).
7. Si faltan obligatorias: intenta plantilla guardada
   (`ImportTemplatesManager`, `~/.boardcomposer/import_templates.json`);
   si sigue faltando → `ImportColumnMappingDialog` (guardar / reutilizar /
   eliminar plantilla).
8. Parseo por filas: `import_boards_from_rows` o `import_pieces_from_rows`.
9. Vista previa modal (`ImportBoardsPreviewDialog` /
   `ImportPiecesPreviewDialog`): filas válidas + errores por fila.
10. Al confirmar: comando undoable (`ImportBoardsCommand` /
    `ImportPiecesCommand`), reload Workspace/Explorer, tip de estado,
    evento Timeline `CsvImported` (`kind` + `count`).

Piezas: `quantity` > 1 expande a ids correlativos; cada pieza nueva recibe
placement inicial en el primer tablero (si existe) vía
`_find_free_piece_position`. La importación de piezas fuerza mostrar el
Workspace.

---

## Flujo alternativo A — Cancelación

1. Cancelar en selector, hoja Excel, mapeo o vista previa.
2. No se modifica el proyecto.

---

## Flujo alternativo B — Archivo ilegible / errores de archivo

1. `load_tabular_file` o `file_errors` del importer fallan.
2. `QMessageBox.warning` con el mensaje; no se abre la vista previa.

---

## Flujo alternativo C — Filas inválidas en vista previa

1. Algunas filas fallan (dims, duplicados, ids ya en proyecto, etc.).
2. Preview resalta errores; el usuario puede **aceptar** solo las válidas
   o cancelar. Cero válidas → status con `n=0`, sin comando.

---

## Columnas

| Kind | Obligatorias | Opcionales |
|------|--------------|------------|
| Tableros | `board_id`, `length_mm`, `width_mm` | `thickness_mm`, `quantity`, `material` |
| Piezas | `piece_id`, `length_mm`, `width_mm` | `thickness_mm`, `quantity`, `material` |

Aliases aceptados (p. ej. `id`, `largo`, `ancho`, `cantidad`) en
`BOARD_HEADER_ALIASES` / `PIECE_HEADER_ALIASES`.

Samples: `data/samples/studio_boards_inventory.{csv,xlsx}`,
`data/samples/studio_pieces.{csv,xlsx}`, `data/samples/basic_boards.csv`.

---

## Validaciones (Studio actual)

- Cabeceras vía aliases o mapeo/plantilla.
- Campos obligatorios presentes tras el mapeo.
- Valores numéricos y dimensiones positivas.
- Ids duplicados dentro del CSV y contra el inventario actual
  (`existing_ids`, casefold).
- Excel: hoja elegida o primera.

---

## Eventos relevantes

- `CsvImported` (`kind=boards|pieces`, `count=N`)

(No hay eventos separados `PiecesValidated` / `PiecesAdded` /
`WorkspaceUpdated` en el catálogo actual; el reload de UI es efecto
directo del comando + `_mark_project_modified`.)

---

## Resultado esperado

Tableros o piezas válidos **añadidos** al proyecto (append, no reemplazo),
con undo (Ctrl+Z), Workspace/Explorer actualizados y registro en Timeline.

---

## Criterios de aceptación

- Dos entradas claras: tableros vs piezas.
- CSV y Excel (`.xlsx` / `.xlsm`).
- Vista previa antes de confirmar.
- Mapeo + plantillas cuando falla el auto-match.
- Errores por fila visibles; cancelable en cada paso.
- Importación deshacible.
- Samples reproducibles en `data/samples/`.

---

## Pantallas implicadas

- SCR-001 — Pantalla de inicio (CTA piezas).
- SCR-002 — Workspace (overlay vacío + canvas tras import).
- SCR-005 — Proyecto (menú).
- FLW-001 — Crear proyecto (proyecto vacío si no había uno).
- FLW-006 — Editar proyecto (modificación / soluciones outdated).

---

## Límites conocidos

- Sin `.xls` legacy ni CSV con delimitadores no detectados de forma
  configurable por el usuario.
- Welcome solo ofrece import de **piezas** (tableros: menú / atajo /
  overlay).
- Sin reglas de validación custom por usuario más allá de aliases +
  plantillas de mapeo.
- No sustituye inventario existente; solo añade.
