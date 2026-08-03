# SCR-005 — Gestión del Proyecto

**Módulo:** BoardComposer Studio

**Código:** SCR-005  
**Versión:** 1.2.0  
**Estado:** Alineado con Studio  
**Última revisión:** 02/08/2026

---

## Objetivo

La gestión del proyecto cubre el ciclo de vida del `.bcproj`: crear, abrir,
guardar, renombrar, plantillas, inventario de tableros/piezas (manual o
CSV/Excel) y el Explorador como árbol del trabajo en curso. No es una pantalla
única: se reparte entre menús **Archivo** / **Proyecto**, la pantalla de inicio
(SCR-001) y el dock Explorador.

---

## Filosofía

Un proyecto es una unidad reproducible en disco (`.bcproj` v2, con migraciones).
El usuario debe poder retomarlo meses después con el mismo inventario,
colocaciones y contexto. La configuración de solver/tema vive en Preferencias
(SCR-006), no en un formulario monolítico de «Proyecto».

---

## Dónde vive en Studio

```text
Archivo          Proyecto              Explorador (Ctrl+1)
────────         ────────              ────────────────────
Nuevo            Renombrar…            Raíz: nombre proyecto
Desde plantilla  Abrir carpeta         ├ Tableros (n)
Demo             Comparar revisiones…  ├ Piezas (n)
Inicio           Restaurar revisión…   └ Soluciones (n)
Abrir / Recientes Añadir tablero…
Guardar / Como   Añadir pieza…
Plantilla…       Importar tableros…
Salir            Importar piezas…
```

La barra de estado muestra la ruta del `.bcproj` cuando el proyecto está
guardado.

---

## Flujos implementados

### Ciclo de archivo

| Acción | Atajo | Notas |
|--------|-------|--------|
| Nuevo | **Ctrl+N** | Diálogo nombre + unidades; untitled |
| Abrir | **Ctrl+O** | `.bcproj`; migra v1→v2; rechaza versión futura; recuerda carpeta |
| Guardar | **Ctrl+S** | Si no hay ruta → Guardar como |
| Guardar como | **Ctrl+Shift+S** | Filtro `.bcproj`; recuerda carpeta (`last_project_directory`) |
| Salir | **Ctrl+Q** | Diálogo si hay cambios sin guardar |
| Recientes | menú / inicio | Máx. 10; poda fantasmas |
| Vaciar recientes | **Ctrl+Shift+X** | Confirmación |

### Identidad y ubicación

| Acción | Atajo | Notas |
|--------|-------|--------|
| Renombrar proyecto | **Ctrl+Shift+F2** (también **F2** en raíz) | Undoable; menú y ctx Explorador |
| Abrir carpeta | **Ctrl+Shift+R** | Solo si hay archivo en disco |
| Comparar revisiones | **Ctrl+Shift+Y** | Diff vs anillo local / archivos; recuerda carpeta (`last_diff_directory`) |
| Restaurar última revisión | **Ctrl+Alt+Y** | Snapshot más reciente del anillo; dirty hasta Guardar; vacía undo |
| Exportar backup de revisiones | **Ctrl+Alt+B** | Copia `.bcproj` + anillo a carpeta; diálogo Abrir carpeta; recuerda destino |

### Plantillas y demo

| Acción | Atajo | Notas |
|--------|-------|--------|
| Guardar como plantilla | **Ctrl+Shift+M** | `~/.boardcomposer/project_templates/`; opcional incluir placements |
| Nuevo desde plantilla | **Ctrl+Shift+N** | Instancia **sin** placements |
| Proyecto demo | **Ctrl+Shift+D** | Inventario de ejemplo; untitled modificado |
| Pantalla de inicio | **Ctrl+Shift+H** | SCR-001 |

### Inventario

| Acción | Atajo | Notas |
|--------|-------|--------|
| Añadir tablero | **Ctrl+Shift+B** | Diálogo; `AddBoardCommand` (undo) |
| Añadir pieza | **Ctrl+Shift+P** | Qty → varios IDs; `AddPieceCommand` (undo) |
| Importar tableros CSV/Excel | **Ctrl+Shift+T** | Preview + mapeo; con undo |
| Importar piezas CSV/Excel | **Ctrl+Shift+O** | Preview; qty expandida; con undo |

Entradas alternativas: menú contextual del Explorador, CTAs del canvas vacío,
botones de la pantalla de inicio (piezas / plantilla / demo).

---

## Explorador

- Árbol: proyecto → Tableros / Piezas / Soluciones (conteos).
- Clic pieza → Inspector + selección en Workspace.
- Clic tablero → centra/resalta paneles.
- Doble clic / ctx solución → preview de candidata.
- Ctx pieza/tablero: editar, renombrar, duplicar, copiar ID, eliminar.

---

## Flujo principal recomendado

1. Nuevo, demo, plantilla o abrir reciente.
2. Añadir o importar tableros y piezas.
3. Guardar `.bcproj`.
4. Calcular layout (flujo Generar / SCR-002 / SCR-003).
5. Aplicar, ajustar en Workspace, exportar (SCR-007).

---

## Criterios de aceptación

- Crear / abrir / guardar / guardar como un `.bcproj` sin perder inventario.
- Renombrar y revelar carpeta cuando el archivo existe en disco.
- Importar CSV/Excel de tableros y piezas con vista previa.
- El Explorador refleja conteos y permite editar elementos.
- Cambios sin guardar bloquean el cierre con diálogo claro.

---

## Relación con otras pantallas

- SCR-001 — Inicio (CTAs y recientes).
- SCR-002 — Workspace.
- SCR-003 — Comparador (nodo Soluciones).
- SCR-004 — Inspector.
- SCR-006 — Preferencias (estrategia, idioma, tema; no sustituye al `.bcproj`).
- SCR-007 — Exportación.
- FLW-002 — Importar CSV/Excel.

---

## Límites conocidos (Studio actual)

- No existe aún un formulario único con cliente/kerf/vetas como en la visión
  antigua de esta pantalla; esos datos viven en piezas/tableros y preferencias.

---

## Evolución prevista

- Formulario de metadatos de proyecto (cliente, referencia, notas).
- Historial cloud / multi-usuario (DT-0006; esperar piloto).
