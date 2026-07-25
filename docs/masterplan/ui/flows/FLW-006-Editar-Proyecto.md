# FLW-006 — Editar Proyecto

**Módulo:** BoardComposer Studio

**Código:** FLW-006  
**Versión:** 1.2.0  
**Estado:** Alineado con Studio  
**Última revisión:** 25/07/2026

---

## Objetivo

Describir cómo el usuario **modifica** un proyecto abierto (inventario,
colocaciones, nombre) con dirty flag, undo donde aplica, y marcado de
soluciones desactualizadas cuando el cambio afecta al layout.

Crear proyecto: FLW-001. Import CSV/Excel: FLW-002. Abrir/guardar: SCR-005.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Hay un proyecto en memoria (abierto, nuevo o creado al añadir/importar).
- Sin asistente modal bloqueante.

---

## Trigger (edición habitual)

| Acción | Atajo / UI |
|--------|------------|
| Añadir tablero | **Ctrl+Shift+B** · Proyecto · overlay vacío |
| Añadir pieza | **Ctrl+Shift+P** · Proyecto · overlay vacío |
| Editar selección | **Return** · doble clic canvas/Explorer · contexto |
| Renombrar selección | **F2** |
| Duplicar pieza | **Ctrl+D** |
| Eliminar pieza | **Backspace** / **Delete** |
| Copiar ID | **Ctrl+Shift+C** |
| Renombrar proyecto | **Ctrl+Shift+F2** · Proyecto · raíz Explorer |
| Deshacer / Rehacer | **Ctrl+Z** / **Ctrl+Shift+Z** |
| Mover pieza (panel) | Arrastre en Workspace · flechas (nudge) |

Inspector (SCR-004) refleja selección; edición de dims/material suele ir por
diálogos `NewBoardDialog` / `NewPieceDialog` (modo add vs edit).

---

## Flujo principal — editar inventario / colocación

1. Usuario elige elemento (Explorer, canvas o menú).
2. Abre diálogo o mueve en el Workspace.
3. Studio valida campos del formulario (dims positivas, ids, etc.).
4. Aplica el cambio (comando undoable cuando existe; ver límites).
5. `mark_project_modified(affects_layout=…)`:
   - siempre → dirty + evento `ProjectModified`
   - si `affects_layout` → flag `solutions_outdated` + `SolutionsMarkedOutdated`
     (banner Comparador; aviso al aplicar layout)
6. Usuario guarda (**Ctrl+S**) o sigue; al salir/reemplazar proyecto → diálogo
   unsaved (`unsaved_changes_message`: nombre, ruta o «aún no guardado»).

Regenerar layout (FLW-003) limpia el aviso outdated.

---

## Operaciones concretas

### Tableros

- Añadir: `NewBoardDialog` (id, largo, ancho, espesor, material, cantidad).
- Editar: mismo diálogo; `EditBoardCommand` (undo; renombre id actualiza
  colocaciones).
- Eliminar: `DeleteBoardCommand` desde Explorer; piezas se conservan;
  colocaciones de ese tablero se quitan.
- Duplicar tablero: acción Explorer / handler `_duplicate_board`.

### Piezas

- Añadir: `NewPieceDialog` con cantidad → ids correlativos + placements
  iniciales.
- Editar: diálogo sin campo cantidad; `EditPieceCommand`.
- Duplicar: `DuplicatePieceCommand` — id `*-copy`, offset ~20 mm.
- Eliminar: selección / id.
- Mover entre paneles físicos: drag-drop en Workspace; material/espesor deben
  compatir; drop inválido revierte; `MovePieceCommand` (también nudge).
  No hay botón «swap».

### Proyecto

- Renombrar: `RenameProjectCommand` con `affects_layout=False` (no marca
  outdated).
- Revelar carpeta `.bcproj`: **Ctrl+Shift+R** (no edita datos).

---

## Flujo alternativo A — Validación de formulario

1. Campos inválidos en diálogo add/edit.
2. Warning / no se acepta; proyecto intacto.

---

## Flujo alternativo B — Descartar / guardar al cambiar de contexto

1. Nuevo / abrir / demo / plantilla / cerrar app con dirty.
2. Diálogo Guardar / Descartar / Cancelar.
3. Fallo al guardar → mensaje; no continúa la acción destructiva.
4. Cancelar «Guardar como» → no continúa.

---

## Dirty y soluciones outdated

| Cambio típico | Dirty | Outdated |
|---------------|-------|----------|
| Add/edit/delete board/piece, move, import, duplicate | Sí | Sí |
| Rename project | Sí | No |
| Preferencias UI sin tocar inventario | No (vía prefs) | No |

Banner en Comparador mientras `solutions_outdated`. Apply (FLW-004) avisa si
está outdated.

---

## Undo / redo

Pila `CommandManager`. Comandos: `AddBoardCommand` / `AddPieceCommand`,
edit/delete/duplicate board|piece, `MovePieceCommand`,
`RenameProjectCommand`, imports (FLW-002).

---

## Eventos relevantes

- `ProjectModified`
- `SolutionsMarkedOutdated`
- `ProjectSaved` (al persistir; SCR-005)

No existen en el catálogo actual: `ProjectValidated`, `ProjectHistoryUpdated`,
ni un evento bus `PieceMoved` (solo reason/`piece_moved` interno + comando).

Timeline refleja hechos publicados en el Event Bus (ADR-005); no es un
historial de revisiones del `.bcproj`.

---

## Resultado esperado

Proyecto dirty coherente; soluciones marcadas stale si el layout puede
cambiar; undo en las ops con comando; regeneración (FLW-003) para volver a
candidatas válidas.

---

## Criterios de aceptación

- Edición de tableros/piezas desde menú, Explorer y canvas.
- Drag entre paneles con validación material/espesor.
- Outdated automático en cambios de layout; rename no invalida.
- Diálogo unsaved claro al salir/reemplazar.
- Undo/redo en ops con comando.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-003 — Comparador (banner outdated).
- SCR-004 — Inspector.
- SCR-005 — Proyecto.
- FLW-001 — Crear.
- FLW-002 — Importar.
- FLW-003 — Generar.
- FLW-004 — Comparar / apply.

---

## Límites conocidos

- Sin control de versiones / diffs entre revisiones del `.bcproj`.
- Sin edición colaborativa ni bloqueo de recursos.
- Sin evento bus `PieceMoved` / `ProjectValidated` / `ProjectHistoryUpdated`.
- Historial = Timeline de eventos + pila undo de sesión, no auditoría
  persistente de revisiones.
