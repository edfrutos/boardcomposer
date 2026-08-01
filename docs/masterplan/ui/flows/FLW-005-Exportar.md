# FLW-005 — Exportar Solución

**Módulo:** BoardComposer Studio

**Código:** FLW-005  
**Versión:** 1.2.0  
**Estado:** Alineado con Studio  
**Última revisión:** 01/08/2026

---

## Objetivo

Describir cómo el usuario exporta la **solución seleccionada** (o, aparte, el
historial del Timeline) a un archivo. Detalle de UI: SCR-007.

---

## Actor principal

- Usuario.

---

## Precondiciones (solución)

- Hay una candidata seleccionada en el servicio de layout (tras FLW-003 /
  FLW-004). Sin ella, el tip de estado pide calcular layout primero.
- Ruta de destino con permisos de escritura (el diálogo de guardar lo valida).

---

## Trigger

| Acción | Atajo / menú |
|--------|----------------|
| Exportar solución seleccionada… | **Ctrl+Shift+E** · menú Exportar · toolbar |
| Exportar historial del Timeline… | **Ctrl+Shift+L** · menú Exportar · Timeline |

Defaults de formato/flags: Preferencias (SCR-006) → `preferences.json`.

---

## Flujo principal — solución

1. El usuario tiene una candidata activa (Comparador / Re-Av Pág / post-cálculo).
2. Dispara **Exportar solución seleccionada…** (**Ctrl+Shift+E**).
3. Se abre `ExportDialog` (SCR-007) con última elección o defaults.
4. Elige formato: SVG / DXF / PDF / JSON / CSV.
5. Ajusta opciones: métricas y explicación (solo JSON), retales (todos).
6. Opcional: aplica o guarda una plantilla / perfil por cliente.
7. Revisa la vista previa (SVG + texto/resumen).
8. Confirma y elige ruta en el diálogo de archivo.
9. Studio escribe el archivo; emite eventos Timeline; ofrece **Abrir archivo**
   o **Mostrar en carpeta**.
10. Persiste formato + flags en `preferences.json`.

---

## Flujo alternativo A — Cancelación

1. Cancelar en el diálogo de opciones o en el de guardar.
2. No se genera archivo; prefs de última elección no se actualizan.

---

## Flujo alternativo B — Error de escritura / export

1. Fallo al generar o guardar.
2. Evento `ExportFailed` (cuando aplique) y mensaje al usuario.
3. Puede reintentar con otra ruta u opciones.

---

## Flujo alternativo C — Sin solución

1. No hay `selected_solution`.
2. No se abre un export útil; tip/status indica calcular layout primero.

---

## Flujo paralelo — Timeline

1. **Ctrl+Shift+L** (no usa `ExportDialog`).
2. `QFileDialog` → JSON o CSV del historial filtrado del Timeline.
3. Código: `studio/timeline/export.py`.

---

## Validaciones (Studio actual)

- Formato ∈ {svg, dxf, pdf, json, csv}.
- Solución seleccionada presente para el flujo principal.
- Diálogo de sistema para ruta/permisos.
- Opciones inconsistentes con el formato: métricas/explicación deshabilitadas
  fuera de JSON.

---

## Eventos relevantes

- `ExportStarted`
- `ExportCompleted`
- `ExportFailed`

(No hay `ExportPreviewGenerated` ni registro aparte de «historial de proyecto»
más allá del Timeline.)

---

## Resultado esperado

Archivo fiel a la candidata seleccionada (o al Timeline filtrado), con
posibilidad de abrir/revelar al terminar y de reutilizar plantillas/defaults.

---

## Criterios de aceptación

- Exporta la candidata activa, no otra.
- Vista previa antes de confirmar la ruta.
- Plantillas y última elección persistentes.
- Post-export: abrir archivo o carpeta.
- Timeline exportable sin mezclarse con el diálogo de solución.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-006 — Preferencias.
- SCR-007 — Exportación.
- FLW-003 — Generar.
- FLW-004 — Comparar.
- ADR-016 — Retales.

---

## Límites conocidos

- PNG/JPEG/PDF/DXF/SVG/JSON/CSV vía diálogo de export (SCR-007).
- Opciones de papel/escala/márgenes limitadas (defaults del exportador).
- CSV solo placements.
- Sin lotes ni publicación a la nube.
