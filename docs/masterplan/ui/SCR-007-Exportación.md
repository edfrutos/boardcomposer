# SCR-007 — Exportación

**Módulo:** BoardComposer Studio

**Código:** SCR-007  
**Versión:** 1.2.0  
**Estado:** Alineado con Studio  
**Última revisión:** 02/08/2026

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
| JSON | Documento estructurado; métricas / explicación / retales opcionales |
| CSV | Filas de placements (sin omitted/metrics/explanation) |

No implementados: escala, márgenes, papel, calidad, cotas como opciones del
diálogo.

### Opciones de contenido

- **Métricas / explicación:** solo activas para **JSON** (UI deshabilitada
  en el resto).
- **Retales:** aplican a todos los formatos vía preparación de la solución
  (omiten `offcuts` cuando están desmarcados).

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
- incluir métricas / explicación / retales
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
- Vista previa coherente con retales y formato.
- Plantillas y última elección persistentes.
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

- Sin controles de papel/escala/márgenes.
- Métricas/explicación solo en JSON.
- CSV limitado a placements.
- Sin exportación por lotes ni publicación a la nube.

---

## Evolución prevista

- Más formatos de imagen y opciones de página.
- Lotes / perfiles CAD-CAM avanzados.
- Trazabilidad explícita (versión app, algoritmo, fecha) en más formatos.
