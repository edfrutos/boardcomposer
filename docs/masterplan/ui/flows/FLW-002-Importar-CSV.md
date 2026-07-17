# FLW-002 — Importar CSV

**Módulo:** BoardComposer Studio

**Código:** FLW-002
**Versión:** 1.0.0
**Estado:** En revisión
**Última revisión:** 01/07/2026

---

## Objetivo

Describir el flujo completo para importar piezas desde un archivo CSV, validando su contenido antes de incorporarlo al proyecto y garantizando la trazabilidad del proceso.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Existe un proyecto abierto.
- El usuario dispone de un archivo CSV compatible.

---

## Flujo principal

1. El usuario selecciona **Importar CSV**.
2. Studio abre el selector de archivos.
3. Se elige el archivo CSV.
4. Studio analiza automáticamente su estructura.
5. Se muestra una vista previa de los datos.
6. El usuario confirma la importación.
7. Las piezas se incorporan al proyecto.
8. El Workspace se actualiza automáticamente.

---

## Flujo alternativo A — Archivo inválido

1. El formato no puede interpretarse.
2. Studio informa del problema indicando la causa.
3. El usuario puede seleccionar otro archivo.

---

## Flujo alternativo B — Errores en los datos

1. Se detectan filas con errores.
2. Studio resalta únicamente las filas afectadas.
3. El usuario decide continuar, corregir o cancelar.

---

## Validaciones

- Cabeceras reconocidas.
- Campos obligatorios presentes.
- Valores numéricos válidos.
- Dimensiones positivas.
- Referencias duplicadas.
- Compatibilidad con la unidad del proyecto.

---

## Resultado esperado

Las piezas válidas quedan incorporadas al proyecto sin alterar la información existente y con un registro completo de la operación.

---

## Eventos generados

- CsvImported
- PiecesValidated
- PiecesAdded
- WorkspaceUpdated

---

## Criterios de aceptación

- Vista previa antes de importar.
- Mensajes de error claros y accionables.
- Posibilidad de cancelar en cualquier momento.
- Importación reproducible y registrada.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-005 — Proyecto.

---

## Observaciones

En futuras versiones se admitirán plantillas de importación, formatos de
terceros adicionales y reglas de validación configurables por el usuario.
Excel `.xlsx` (primera hoja) ya está soportado. Si el auto-match de
cabeceras falla, Studio ofrece un asistente de mapeo de columnas.

---

## Estado de implementación (2026-07-17)

- Inventario de tableros: `Proyecto → Importar inventario de tableros (CSV/Excel)…`
  (`studio/board_csv_importer.py`, `ImportBoardsPreviewDialog`).
- Piezas: `Proyecto → Importar piezas (CSV/Excel)…`
  (`studio/piece_csv_importer.py`, `ImportPiecesPreviewDialog`), con
  expansión de cantidad a ids correlativos y colocación inicial en el
  Workspace.
- Formatos: CSV y Excel `.xlsx` (primera hoja) vía `studio/tabular_file.py`.
  Samples: `data/samples/studio_*.csv` y `data/samples/studio_*.xlsx`.
- Asistente de mapeo de columnas cuando fallan las obligatorias
  (`ImportColumnMappingDialog`, `studio/import_headers.py`).
