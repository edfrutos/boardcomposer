# FLW-001 — Crear Proyecto

**Módulo:** BoardComposer Studio

**Código:** FLW-001  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 25/07/2026

---

## Objetivo

Describir cómo el usuario **crea** un proyecto en Studio (vacío con diálogo,
demo o plantilla) y pasa al Workspace listo para editar / importar.

Abrir y guardar `.bcproj` viven en SCR-005; editar inventario en FLW-006.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Studio iniciado; sin diálogo modal bloqueante.
- Si hay cambios sin guardar, Studio pide Guardar / Descartar / Cancelar
  antes de reemplazar el proyecto (`_confirm_discard_unsaved_changes`).

---

## Trigger

| Acción | Atajo / menú / CTA |
|--------|---------------------|
| Nuevo proyecto… | **Ctrl+N** · Archivo · Welcome |
| Nuevo desde plantilla… | **Ctrl+Shift+N** · Archivo · Welcome |
| Proyecto demo | **Ctrl+Shift+D** · Archivo · Welcome |
| Guardar como plantilla… | **Ctrl+Shift+M** · Archivo (proyecto actual) |

---

## Flujo principal — vacío (`NewProjectDialog`)

1. El usuario dispara **Nuevo proyecto** (**Ctrl+N**).
2. Confirmación de cambios sin guardar (si aplica).
3. Se abre `NewProjectDialog`: nombre (obligatorio) + unidades
   (defaults desde Preferencias SCR-006).
4. Cancelar → no se crea proyecto; se permanece en la pantalla actual.
5. Aceptar con nombre vacío → warning; no se crea.
6. Si las unidades del diálogo ≠ prefs → se actualizan prefs y se aplican.
7. `_load_empty_project(name=…)`: `StudioProject` sin tableros/piezas,
   `project_id` = `PRJ-` + 8 hex (`new_project_id`, ADR-006).
8. Se limpia el layout/soluciones; se muestra Workspace (`WorkspaceOpened`).
9. Evento `ProjectCreated` (`kind=empty`, `name=…`) + tip de estado.

El proyecto queda **sin guardar** hasta Ctrl+S / Guardar como (`.bcproj` v2).

---

## Flujo paralelo A — Demo

1. **Ctrl+Shift+D** (o CTA Welcome).
2. Confirmación unsaved.
3. `_load_demo_project`: tablero + 3 piezas + placements fijos
   (`project_id=PRJ-DEMO-001`).
4. `ProjectCreated` (`kind=demo`) → Workspace.

---

## Flujo paralelo B — Desde plantilla

1. **Ctrl+Shift+N**.
2. Confirmación unsaved.
3. Si no hay plantillas → info + status; no se crea.
4. `ProjectTemplatePickerDialog` → `instantiate(name, include_placements=False)`.
5. Nuevo `project_id` vía `new_project_id`; inventario de la plantilla sin
   placements.
6. `ProjectCreated` (`kind=template`, `name=…`) → Workspace.

---

## Flujo paralelo C — Guardar como plantilla

1. Hay proyecto actual; **Ctrl+Shift+M**.
2. `save_from_project` en el gestor de plantillas.
3. No crea un proyecto nuevo; solo persiste plantilla reutilizable.

---

## Creación implícita

Si no hay proyecto y el usuario añade tablero/pieza o importa CSV (FLW-002),
Studio llama `_load_empty_project()` con nombre «Sin título» y luego continúa
la acción. Eso **no** emite `ProjectCreated` en esos caminos (solo deja un
proyecto en memoria).

---

## Datos del diálogo principal

| Campo | Obligatorio | Notas |
|-------|-------------|--------|
| Nombre | Sí | Default i18n `project.untitled`; trim |
| Unidades | Sí | `mm` / prefs; puede actualizar Preferencias |

No se pide material por defecto a nivel de proyecto.

---

## Eventos relevantes

- `ProjectCreated` (`kind=empty|demo|template`)
- `WorkspaceOpened` (al mostrar el Workspace)

(Open/save usan `ProjectOpened` / `ProjectSaved` — SCR-005.)

---

## Resultado esperado

Proyecto en memoria con id único, Workspace visible, listo para FLW-002 /
FLW-006. Persistencia opcional posterior en `.bcproj` (versión 2, ADR-015).

---

## Criterios de aceptación

- Crear vacío en un paso (nombre + unidades).
- Demo y plantilla como atajos paralelos.
- Confirmación si hay cambios sin guardar.
- Apertura automática del Workspace tras crear.
- Id `PRJ-…` único (excepto demo fijo).

---

## Pantallas implicadas

- SCR-001 — Pantalla de inicio.
- SCR-002 — Workspace.
- SCR-005 — Proyecto (abrir/guardar/recientes).
- SCR-006 — Preferencias (unidades default).
- FLW-002 — Importar CSV/Excel.
- FLW-006 — Editar proyecto.
- ADR-006 — Identificadores.
- ADR-015 — Migraciones `.bcproj`.

---

## Límites conocidos

- Sin wizard multi-paso ni material por defecto de proyecto.
- Plantilla no incluye placements al instanciar.
- Demo con datos fijos en código (`_load_demo_project`).
- «Nuevo» no pide ruta de archivo; el `.bcproj` aparece al guardar.
