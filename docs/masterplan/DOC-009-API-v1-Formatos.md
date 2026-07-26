# BoardComposer

## Documento 9 — Formatos de intercambio API `v1`

**Código:** DOC-009  
**Versión:** 1.0.0  
**Estado:** En revisión  
**Fecha de creación:** 26/07/2026  
**Última revisión:** 26/07/2026  
**Épica / sprint:** EP-001 / SPR-002  
**API:** `boardcomposer.api.v1` (`API_VERSION = 1.0.0`)

---

## Objetivo

Documentar los **payloads estables** que un integrador usa con la API Python
`v1` sin Studio ni Qt: entrada de proyecto (CSV) y salida de solución
(JSON / CSV / SVG).

Fuente de verdad del comportamiento: código en `src/boardcomposer/` y tests
`tests/test_api_v1_contract.py`, `tests/test_csv_json_exporters.py`.

---

## Superficie relacionada

| Función `v1` | Formato |
|--------------|---------|
| `load_project(path)` | CSV de piezas → `Project` |
| `solve` / `run` | — (objetos Core en memoria) |
| `export_json` | documento JSON de una solución |
| `export_csv` | tabla CSV de placements |
| `export_svg` | documento SVG |

Tipos de dominio: `boardcomposer` / `boardcomposer.domain` (`Project`,
`AssemblySolution`, …). Modelo conceptual: `docs/data_model.md`.

---

## 1. Proyecto de entrada — CSV de piezas

Usado por `load_project` (mismo loader que el CLI `--csv`).

### Ubicación de ejemplo

`data/samples/basic_boards.csv`

### Columnas

| Columna | Tipo | Obligatoria | Notas |
|--------|------|-------------|-------|
| `id` | string | no | Si falta, el Core asigna id automático |
| `length_mm` | float | sí | Largo de la pieza (mm) |
| `width_mm` | float | sí | Ancho (mm) |
| `thickness_mm` | float | sí | Espesor (mm) |

Encoding: UTF-8. Cabecera en la primera fila. Separador: `,`.

### Ejemplo

```csv
id,length_mm,width_mm,thickness_mm
A,2000,300,20
B,1000,300,20
C,800,250,20
```

### Límites del corte `v1` (SPR-001/002)

- Este CSV describe **piezas a colocar** (`Board` en Core), no inventario
  de tableros stock.
- Inventario multipanel / `.bcproj` **no** entra por `load_project` aún
  (SPR-003).
- Restricciones (`ProjectConstraints`: rotación, máximos, …) se fijan en
  código sobre el `Project` cargado, no en el CSV.

---

## 2. Solución — JSON (`export_json`)

Serializa **una** `AssemblySolution` (opcionalmente con `Project` para
enriquecer métricas e inventario referenciado).

### Campos raíz

| Campo | Tipo | Siempre | Descripción |
|-------|------|---------|-------------|
| `solution_index` | int \| null | sí | Índice en el ranking (si se pasa) |
| `strategy` | string \| null | sí | Nombre de estrategia (`balanced`, …) |
| `complete` | bool | sí | Todas las piezas colocadas |
| `score` | number | sí | Score total de la solución |
| `omitted_piece_ids` | string[] | sí | Piezas no colocadas (parcial) |
| `placements` | object[] | sí | Colocaciones |
| `metrics` | object | por defecto | Métricas agregadas |
| `notes` | string[] | por defecto | Notas de explicación |
| `strengths` | string[] | por defecto | Fortalezas |
| `weaknesses` | string[] | por defecto | Debilidades |
| `offcuts` | object[] | por defecto | Retales informativos (ADR-016) |
| `stock_panels` | object[] | si hay `project` | Inventario stock del proyecto |

### `placements[]`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `piece_id` | string | Id de pieza |
| `x_mm`, `y_mm` | number | Origen local al panel (mm) |
| `length_mm`, `width_mm` | number | Dimensiones efectivas tras rotación |
| `rotated` | bool | Pieza rotada 90° |
| `panel_reference` | object \| null | `{ stock_panel_index, instance_index }` |

### `metrics` (cuando se incluyen)

| Campo | Descripción |
|-------|-------------|
| `placed_pieces` | Nº de placements |
| `omitted_pieces` | Nº omitidas |
| `total_length_mm` / `total_width_mm` | Bounding box de la solución |
| `waste_ratio` | Ratio de desperdicio (modelo solución) |
| `used_area_mm2` | Área usada |
| `offcut_area_mm2` | Área de retales informativos |
| `panels_used` | Paneles físicos referenciados |
| `panel_waste_ratio` | Solo si hay `project` y paneles usados |

### `offcuts[]` (informativos; no son inventario)

| Campo | Descripción |
|-------|-------------|
| `panel_reference` | Panel físico del retal |
| `x_mm`, `y_mm`, `length_mm`, `width_mm` | Geometría |
| `area_mm2` | Área |

### `stock_panels[]` (si se pasa `project`)

| Campo | Descripción |
|-------|-------------|
| `id` | Id del tipo de panel |
| `length_mm`, `width_mm`, `thickness_mm` | Dimensiones |
| `quantity` | Unidades físicas |
| `material` | Material |

### Ejemplo mínimo (forma)

```json
{
  "solution_index": 0,
  "strategy": "balanced",
  "complete": true,
  "score": 80.17,
  "omitted_piece_ids": [],
  "placements": [
    {
      "piece_id": "A",
      "x_mm": 0,
      "y_mm": 0,
      "length_mm": 2000,
      "width_mm": 300,
      "rotated": false,
      "panel_reference": null
    }
  ],
  "metrics": {
    "placed_pieces": 1,
    "omitted_pieces": 0,
    "waste_ratio": 0.0,
    "panels_used": 0
  },
  "notes": [],
  "strengths": [],
  "weaknesses": [],
  "offcuts": []
}
```

Implementación: `boardcomposer.export.solution_to_json` /
`boardcomposer.api.v1.export_json`.

---

## 3. Solución — CSV de placements (`export_csv`)

Una fila por placement. **No** incluye piezas omitidas ni métricas (usar JSON).

| Columna | Descripción |
|---------|-------------|
| `piece_id` | Id de pieza |
| `x_mm`, `y_mm` | Origen (mm) |
| `length_mm`, `width_mm` | Dimensiones efectivas |
| `rotated` | `true` / `false` |
| `stock_panel_index` | Vacío si no hay referencia |
| `instance_index` | Vacío si no hay referencia |

---

## 4. Solución — SVG (`export_svg`)

Documento SVG con paneles lado a lado (si hay referencias), piezas como
rectángulos, retales con trazo discontinuo y leyenda de omitidas si aplica.
Contrato visual, no schema JSON; estable en el sentido de «documento SVG
válido», no pixel-perfect entre versiones menores.

---

## Versionado y breaking changes

- Contrato empaquetado: `boardcomposer.api.v1` + este DOC.
- Renombrar/eliminar campos JSON/CSV de solución o columnas CSV de entrada
  sin ruta de compatibilidad → bump a `v2` + DOC nuevo.
- Añadir campos opcionales en JSON es compatible hacia adelante dentro de `v1`.

---

## Fuera de alcance (siguientes sprints)

| Tema | Sprint / épica |
|------|----------------|
| Carga `.bcproj` / stock multipanel vía API | SPR-003 |
| HTTP / OpenAPI | EP-003 |
| Guía larga de integrador (más allá del ejemplo) | evolución DOC-008 |

Ejemplo mínimo de código: `examples/api_v1_minimal.py`.

---

## Relación con otros documentos

- [DOC-008](DOC-008-API.md) — visión API.
- [EP-001](epics/EP-001-API-Publica-Contratos.md) — épica y sprints.
- `docs/data_model.md` — entidades Core.
- ADR-014 (multipanel), ADR-016 (retales informativos).
