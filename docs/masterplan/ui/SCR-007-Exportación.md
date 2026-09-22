# SCR-007 — Exportación

**Módulo:** BoardComposer Studio

**Código:** SCR-007  
**Versión:** 1.13.0  
**Estado:** Alineado con Studio  
**Última revisión:** 22/09/2026

---

## Objetivo

Exportar la **solución seleccionada** (candidata activa del layout) a un
archivo útil para fabricación, documentación o intercambio, con opciones de
contenido, vista previa y plantillas reutilizables.

---

## Filosofía

Exportar no es solo «guardar». Es transformar la candidata elegida en un
artefacto reproducible. La solución de origen es la del Comparador /
servicio de layout (`selected_solution`), no un snapshot arbitrario del
canvas sin calcular.

---

## Acceso

| Acción | Atajo / menú |
|--------|----------------|
| Exportar solución seleccionada… | **Ctrl+Shift+E** · Exportar · toolbar |
| Exportar lista de corte… | **Ctrl+Alt+C** · Exportar (flujo aparte; CSV/PDF) |
| Exportar presupuesto… | **Ctrl+Alt+Q** · Exportar (flujo aparte; PDF) |
| Exportar historial del Timeline… | **Ctrl+Shift+L** · Exportar · Timeline (flujo aparte) |

Sin solución calculada/seleccionada: el tip de estado pide calcular layout
antes. Si `solutions_outdated`, tip/diálogo priorizan **Calcular layout**
antes de abrir este diálogo.

Defaults de formato y flags: SCR-006 → `preferences.json`.

---

## Distribución actual (solución)

```text
┌────────────────────────────────────────────────────────────────────┐
│ Exportar solución seleccionada                                     │
├────────────────────┬───────────────────────────────────────────────┤
│ Formato            │ SVG │ PNG │ JPEG │ DXF │ PDF │ JSON │ CSV     │
│ Opciones           │ ☐ Métricas  ☐ Explicación  ☐ Retales          │
│                    │ ☐ Etiquetas de piezas (id y LxW mm)           │
│                    │ ☐ Etiquetas de retales (LxW mm)               │
│                    │ ☐ Cotas L×A del tablero                       │
│                    │ ☐ Trazabilidad (versión, algoritmo, fecha)    │
│ PDF plano          │ papel (dibujo/A4/A3/Letter) · orientación     │
│                    │ escala (fit / 1:n) · márgenes mm              │
│ Raster PNG/JPEG    │ DPI (36–300) · calidad JPEG (1–100)           │
│ Lote               │ ☐ Todas las candidatas del ranking            │
│ Plantillas         │ cliente · guardar/aplicar/borrar · pack JSON  │
├────────────────────┴───────────────────────────────────────────────┤
│ Vista previa (SVG/raster + texto/resumen según formato)            │
├────────────────────────────────────────────────────────────────────┤
│                         [Cancelar]  [Exportar…]                    │
└────────────────────────────────────────────────────────────────────┘
```

Tras exportar OK: opción de abrir el archivo o revelar la carpeta.

---

## Formatos

| Formato | Contenido principal |
|--------|---------------------|
| PNG / JPEG | Raster del layout (misma geometría que SVG preview) |
| SVG / DXF / PDF | Planos de paneles; retales opcionales |
| JSON | Documento estructurado; métricas / explicación / retales opcionales; Studio añade `estimated_material_cost` si el catálogo tiene €/m² |
| CSV | Filas de placements (sin omitted/metrics/explanation) |

No implementados: más formatos de imagen (WebP, TIFF).

### Opciones de contenido

- **Métricas / explicación:** solo activas para **JSON** (UI deshabilitada
  en el resto).
- **Retales:** aplican a todos los formatos vía preparación de la solución
  (omiten `offcuts` cuando están desmarcados).
- **Etiquetas de piezas (id y LxW):** SVG, PNG, JPEG, DXF y PDF
  (mismo dibujo que Workspace). Texto según `prefs.units` (IDE-0044).
  Deshabilitada en JSON/CSV. Default: sí.
- **Etiquetas de retales (LxW):** mismos formatos de plano. Requiere
  retales incluidos. PDF dibuja el retal punteado. Default: sí.
  Deshabilitada en JSON/CSV. Área mm² sigue en JSON; Inspector usa
  prefs.units (IDE-0040).
- **Cotas L×A del tablero (IDE-0037):** mismos formatos de plano.
  Líneas de dimensión overall (largo abajo, ancho a la izquierda).
  Valor según `prefs.units` (IDE-0044). Default: sí. Deshabilitada en
  JSON/CSV. Sin bump `.bcproj`. No son etiquetas de pieza/retal
  (0026/0033).
- **Unidades de plano (IDE-0044):** sin casilla. `prefs.units` mm/cm/in
  en TEXT de pieza/retal/cota. mm omite sufijo (`A 400x300`); cm/in
  lo añaden (`A 40x30 cm`). Geometría, JSON/CSV y `$INSUNITS` siguen
  mm.
- **Unidades de informes (IDE-0048):** sin casilla. `prefs.units` en
  TEXT de lista de corte PDF y presupuesto PDF (LxW, espesor, kerf,
  posición, pasos de sierra). Default mm no cambia el texto. CSV de
  corte, JSON y área m² siguen mm.
- **Trazabilidad (IDE-0039 / IDE-0043):** pie
  `BoardComposer {versión} · {algoritmo o "-"} · YYYY-MM-DD HH:MM`.
  Plano SVG/PDF/DXF (0039) y PDF de lista de corte / presupuesto (0043).
  Default: sí (casilla Preferencias / Exportar plano). JSON/CSV y CSV
  de corte no. Capa DXF `META`. Sin bump `.bcproj`.
- **Mano de obra (IDE-0045):** solo presupuesto PDF (**Ctrl+Alt+Q**).
  Preferencias: EUR/h (0–999) y minutos por pieza colocada (0–180).
  Default 0 omite la línea. Total = material (catálogo EUR/m²) + labor.
  JSON de métricas y lista de corte no. Sin herrajes. Sin bump `.bcproj`.
- **Capas DXF por rol (IDE-0041):** solo **DXF**. Tabla LAYER con
  `PANELS` (marco), `PIECES`, `OFFCUTS`, `DIMS` (cotas), `SEQ`, `META`.
  `$INSUNITS` = mm. LibreCAD / QCAD / CAM pueden ocultar capas. SVG/PDF
  no. Sin checkbox extra.
- **Números de secuencia (IDE-0027):** siempre en SVG/PDF/DXF (paso de
  pieza en su panel). La lista de corte (Ctrl+Alt+C) añade el orden de
  sierra (guillotina o por posición) en CSV y PDF.
- **Papel / orientación / escala / márgenes (IDE-0034):** solo formato
  **PDF** de plano. Papel: ajustar al dibujo (default, 1:1, página a
  medida) o A4/A3/Letter. Escala fit o 1:1 / 1:2 / 1:5 / 1:10 y
  orientación auto/vertical/apaisado cuando el papel es ISO. Márgenes
  0–50 mm (default 12,7 mm). Lista de corte y presupuesto siguen A4
  aparte. SVG/DXF/raster no usan estos controles.
- **Calidad raster (IDE-0038):** solo **PNG** y **JPEG**. DPI 36–300
  (default 96; 1 mm ≈ DPI/25,4 px). JPEG calidad 1–100 (default 90;
  deshabilitada en PNG). El lado mayor se recorta a 16384 px si el
  dibujo × DPI lo supera. Vista previa del diálogo sigue en miniatura;
  el archivo usa DPI. Plantillas y Preferencias recuerdan ambos valores.
  `boardcomposer-batch` no exporta PNG/JPEG.
- **Lote de candidatas (IDE-0035):** casilla «Exportar las N candidatas
  del ranking». Deshabilitada si hay menos de 2. Elige carpeta y escribe
  `boardcomposer-solution-01.{ext}` … en orden del Comparador. Vista
  previa sigue siendo la candidata seleccionada. No sustituye
  `boardcomposer-batch` (EP-002, carpetas de proyectos).

---

## Vista previa

- Gráfica: SVG de la solución (misma lógica de retales que el export).
- Texto: resumen y, según formato, payload truncado (JSON/CSV) o notas de
  tamaño (SVG/DXF/PDF).
- Se refresca al cambiar formato u opciones.

---

## Plantillas y perfiles por cliente

- Plantillas nombradas en `~/.boardcomposer/export_templates.json`.
- Campo **cliente** + filtro (todos / general / cliente).
- Guardar / aplicar / eliminar plantilla.
- Compartir: exportar/importar pack JSON (fusión o reemplazo).

---

## Memoria de última elección

Tras un export correcto se guardan en `preferences.json`:

- formato
- incluir métricas / explicación / retales / etiquetas de piezas / etiquetas
  de retales
- papel / orientación / escala / márgenes del PDF de plano
- lote de candidatas del ranking
- carpeta de destino (`last_export_directory`) — sin UI en Preferencias;
  el siguiente `QFileDialog` (solución **o** Timeline) abre ahí si sigue
  existiendo
- carpeta del pack de plantillas (`last_export_templates_directory`) — al
  exportar/importar el JSON compartido desde `ExportDialog`

También editables en Preferencias (SCR-006), salvo las carpetas (solo
persistencia silenciosa).

**Backup de revisiones** (menú Proyecto / **Ctrl+Alt+B**, no `ExportDialog`)
usa `last_backup_directory` por separado: mismo patrón silencioso; tras éxito
ofrece Abrir carpeta. Detalle operativo: `docs/ops/PILOT-DT-0006-backup.md`.

---

## Exportación del Timeline (aparte)

No usa `ExportDialog`. Flujo propio:

1. **Ctrl+Shift+L** (o menú / botón Timeline).
2. `QFileDialog` → JSON o CSV del historial filtrado del Timeline.
3. Código: `studio/timeline/export.py`.

---

## Flujo principal (solución)

1. Calcular layout y seleccionar candidata (SCR-003).
2. **Ctrl+Shift+E** (si outdated: confirmar recalcular / exportar / cancelar).
3. Elegir formato / opciones / plantilla.
4. Revisar vista previa.
5. Exportar y, si se desea, abrir o revelar el archivo.

---

## Criterios de aceptación

- Exporta la candidata seleccionada, no otra.
- SVG/DXF/PDF/JSON/CSV cubiertos desde el mismo diálogo.
- Vista previa coherente con retales, etiquetas de piezas/retales y formato.
- PDF de plano respeta papel/escala/márgenes; lista de corte y presupuesto
  no cambian de página.
- Plantillas y última elección persistentes.
- Lote: N archivos en carpeta, nombres numerados, misma opciones.
- Timeline exportable sin mezclarse con el diálogo de solución.

---

## Relación con otras pantallas

- SCR-002 — Workspace (contexto visual).
- SCR-003 — Comparador (selección de candidata).
- SCR-005 — Proyecto.
- SCR-006 — Preferencias (defaults).
- FLW-005 — Exportar (flujo).
- ADR-016 — Retales informativos.

---

## Límites conocidos (Studio actual)

- Métricas/explicación solo en JSON.
- CSV del diálogo limitado a placements; lista de corte (Ctrl+Alt+C)
  cubre piezas/tableros/cortes y secuencia de sierra en CSV o PDF.
- Sin publicación a la nube.

---

## Evolución prevista

- Más formatos de imagen (WebP, TIFF).
- Perfiles CAD-CAM avanzados (más allá de capas DXF IDE-0041).
