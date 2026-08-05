# Checklist humana — funcionalidad Studio

**Fecha:** 2026-07-25  
**Base:** `main` tras sync docs SCR-001…007 + FLW-001…006  
**Versión:** `0.4.2`  
**Cómo arrancar:** `make run` o `.venv/bin/python -m studio.app`

> Pasada visual cerrada (2026-07-28): [`CHECKLIST-VISUAL.md`](CHECKLIST-VISUAL.md).
> Índice UAT: [`../README.md`](../README.md).

Marca cada ítem al comprobarlo. Objetivo: ver **qué hay implementado y usable**, no buscar bugs de borde.

Flujos de referencia: FLW-001…006 y pantallas SCR-001…007 en
`docs/masterplan/ui/`.

---

## 0. Arranque y entorno

- [x] La app abre con icono propio (no el genérico de Python).
- [x] Pantalla de inicio (SCR-001): hero, CTAs, recientes, plantilla, docs/novedades/atajos/acerca; volver con **Ctrl+Shift+H** (tip de estado); demo con **Ctrl+Shift+D** (tip de estado).
- [x] Tema «Industrial madera» se ve coherente (claro/oscuro vía Preferencias).
- [x] Idioma es/en cambia menús y tip de estado (`Editar → Preferencias…`, **Ctrl+,**).

---

## 1. Proyecto (SCR-005 / FLW-001)

- [x] **Nuevo proyecto** (**Ctrl+N**, tip de estado) pide nombre y unidades; aparece workspace vacío con CTAs.
- [x] **Añadir tablero** (**Ctrl+Shift+B**; tip de estado) y **añadir pieza** (**Ctrl+Shift+P**; tip de estado) (menú / Explorador / CTA vacío).
- [x] **Guardar** (**Ctrl+S**) / **Guardar como** (**Ctrl+Shift+S**) / **Abrir** (**Ctrl+O**) `.bcproj` (tips de estado); ruta visible en la barra de estado; **Ctrl+Shift+R** abre la carpeta (tip de estado); recuerda carpeta (`last_project_directory`).
- [x] **Recientes** en inicio y menú: clic / Enter abre; anclar / desanclar vía menú contextual; Delete / menú quita uno; vaciar lista (**Ctrl+Shift+X**; tip de estado) si aplica.
- [x] **Plantilla de proyecto**: guardar (**Ctrl+Shift+M**; tip de estado) y crear desde plantilla (**Ctrl+Shift+N**; tip de estado).
- [x] Cerrar / **Salir** (**Ctrl+Q**; tip de estado) con cambios sin guardar → diálogo claro (nombre/ruta/botones).
- [x] **Renombrar proyecto** (menú, clic derecho en raíz del Explorador, **F2** o **Ctrl+Shift+F2**; tip de estado).
- [x] **Comparar revisiones `.bcproj`** (**Ctrl+Shift+Y**; tip de estado): tras guardar varias veces, abre diff con cambios estructurales legibles (`diff:` / `changes:`); recuerda carpeta examinada (`last_diff_directory`).
- [x] **Restaurar última revisión local** (**Ctrl+Alt+Y** / menú Proyecto; tip idle si no hay anillo): tras ≥2 guardados, confirma → inventario en memoria vuelve al snapshot; título dirty; Guardar escribe en disco.
- [x] **Exportar backup de revisiones…** (**Ctrl+Alt+B**; tip idle sin archivo): elige carpeta → copia `.bcproj` + anillo; diálogo «Carpeta creada» / **Abrir carpeta**; recuerda destino (`last_backup_directory`).

---

## 2. Explorador e Inspector

- [x] Contadores `Tableros (n)`, `Piezas (n)`, `Soluciones (n)`.
- [x] Clic en **pieza** → Inspector completo + selección en canvas.
- [x] Clic en **tablero** → centra cámara y resalta en Workspace.
- [x] Menú contextual pieza: editar / duplicar / eliminar / copiar ID / renombrar.
- [x] Menú contextual tablero: editar / duplicar / eliminar / copiar ID / renombrar.
- [x] Clic / doble clic / Enter en **solución** del Explorador → vista previa
  (tip de estado con índice).

---

## 3. Workspace (SCR-002)

- [x] Paneles físicos lado a lado (cantidad > 1 en un tablero).
- [x] Arrastrar pieza dentro del panel; soltar en **otro panel** reasigna instancia.
- [x] Solape inválido revierte el movimiento.
- [x] Zoom: rueda / **Ctrl+=** / **Ctrl+-** (tips de estado); % en barra de estado.
- [x] **Ctrl+0** ajusta a todos los tableros (tip de estado); **Ctrl+Shift+0** a la selección (tip de estado).
- [x] Pan: botón medio, botón derecho, **Espacio + arrastre**.
- [x] Clic en vacío deselecciona; **Ctrl+A** / **Esc** / **Ctrl+Shift+I** (tips de estado en selección).
- [x] **Flechas** mueven 1 mm; **Shift+flechas** = tamaño de cuadrícula (prefs).
- [x] **R** rota si cabe (tip de estado); si no, se rechaza.
- [x] Doble clic pieza/tablero → editar; vacío → ajustar vista.
- [x] **Enter/Return** edita selección (tip de estado); **F2** renombra (tip de estado); **Ctrl+Shift+C** copia ID (tip de estado).
- [x] **Ctrl+D** duplica pieza o tablero enfocado (tip de estado).
- [x] **Delete/Backspace** elimina pieza o tablero enfocado (con confirmación; tip de estado).
- [x] **Ctrl+G** muestra/oculta cuadrícula (tip de estado menciona el atajo).
- [x] Docks: Ver → Explorador (**Ctrl+1**; tip de estado) / Inspector (**Ctrl+2**; tip de estado) / Timeline (**Ctrl+3**; tip de estado) / Comparador (**Ctrl+4**; tip de estado); barra de herramientas (**Ctrl+Shift+K**; tip de estado); restablecer disposición (**Ctrl+Shift+W**; tip de estado).

---

## 4. Layout / Comparar / Exportar (flujo estrella)

Precondición para checks de comparador multi-candidata:

- En Preferencias, `Máx. soluciones a conservar` > 1 (recomendado 20).
- Atajo rápido: **Ctrl+Shift+D** (proyecto demo). Si el máx. era 1, Studio
  lo restaura a 20 y el tip de estado lo dice. Luego **Ctrl+Return**.
- Dataset que produzca >=2 candidatas únicas/aceptadas (el demo basta).
- Si tras Calcular solo hay 1, el tip de estado dirá «única candidata… no
  hay más distintas» (no es fallo del límite).
- Confirmar en Inspector diagnóstico: `Candidatas únicas` y `Aceptadas`.
- Regresión auto: `pytest tests/test_uat_multi_candidate_flow.py`
  (demo→solve≥2, Re/Av Pág, pin/diff, export+open-after).

- [x] **Ctrl+Return** calcula layout (progreso + Cancelar funcionan; tip de estado menciona el atajo).
- [x] Aparecen >=2 soluciones en Comparador + Explorador (si el dataset y preferencias lo permiten).
- [x] **Re Pág** / **Av Pág** (tips de estado) recorren candidatas (preview + status) cuando hay >=2 visibles; con 1 quedan deshabilitados.
- [x] **Ctrl+Shift+Return** aplica la solución al proyecto (tip de estado).
- [x] Editar pieza tras aplicar → aviso de soluciones **desactualizadas**
  (banner Comparador + CTA **Calcular layout**).
- [x] Aplicar / Exportar con outdated: tip honesto + diálogo **Calcular layout**
  / continuar de todos modos / Cancelar.
- [x] Calcular layout / CTA banner con outdated: tip honesto
  (`tip.solve_layout_outdated`).
- [x] Explicar candidata con outdated: tip + cabecera avisan (sin bloquear).
- [x] Re/Av Pág y Fijar referencia con outdated: tips avisan candidatas viejas.
- [x] Vista previa Explorador con outdated: tip honesto
  (`tip.preview_solution_outdated`).
- [x] Comparador: ordenar, filtrar «solo completas», miniaturas, fijar referencia
  visible + diff (requiere >=2; botón pin deshabilitado con 1; tip post-solve).
- [x] **Ctrl+Shift+E** (menú **Exportar** / toolbar) abre exportar solución
  (SVG/PNG/JPEG/PDF/DXF/JSON/CSV + preview). Tras Calcular, el tip de estado
  lo recuerda; sin layout: tip pide Ctrl+Return primero.
- [x] Tras exportar OK (solución **o** Timeline): diálogo «Abrir archivo» /
  «Mostrar en carpeta».

---

## 5. Importación (FLW-002)

- [x] Importar **tableros** CSV/Excel (**Ctrl+Shift+T**; tip de estado) con vista previa.
- [x] Importar **piezas** CSV/Excel (**Ctrl+Shift+O**; tip de estado; cantidad expandida si aplica).
- [x] Import recuerda última carpeta (`last_import_directory`).
- [x] Diff `.bcproj` recuerda última carpeta (`last_diff_directory`).
- [x] Pack plantillas exportación recuerda carpeta (`last_export_templates_directory`).
- [x] Excel multi-hoja: selector de hoja.
- [x] Si fallan columnas: asistente de mapeo + guardar/reaplicar/eliminar plantilla.
- [x] Importación **deshacible** (**Ctrl+Z** / **Ctrl+Shift+Z**, tips de Deshacer/Rehacer).

---

## 6. Timeline (ADR-005)

- [x] Eventos del cálculo aparecen en el dock.
- [x] Replay colocaciones / fases (no muta el proyecto).
- [x] Filtros por algoritmo / periodo; marcador de usuario.
- [x] Clic en hecho → busca contexto.
- [x] Exportar historial Timeline JSON/CSV (**Ctrl+Shift+L**; tip de estado).

---

## 7. Preferencias y ayuda (SCR-006)

- [x] Tema, idioma, unidades, grid, estrategia/pesos, máx. soluciones, defaults export.
- [x] Geometría de ventana/docks se recuerda al reiniciar.
- [x] **Ayuda → Atajos de teclado…** (**F1**; tip de estado) lista el catálogo (incl. PgUp/PgDown, Ctrl+Shift+Return/E, Ctrl+Alt+B/E).
- [x] Ayuda → Novedades (**Ctrl+Shift+U**; tip de estado) / Documentación (**Shift+F1**; tip de estado) / Acerca de (**Ctrl+Shift+A**; tip de estado, icono correcto).
- [x] **Ayuda → Explicar candidata…** (**Ctrl+Alt+E**; tip idle sin layout): tras Calcular, diálogo con fortalezas/debilidades/notas + **Copiar** (status bar confirma).
  Eval humana 5 candidatas: [`CHECKLIST-EXPLAIN-EVAL.md`](CHECKLIST-EXPLAIN-EVAL.md).

---

## 8. Multipanel / Core (smoke)

- [x] Proyecto con 2+ tipos o cantidades: solver usa paneles físicos.
- [x] Material/espesor incompatible → pieza omitida o fallo visible (parcial).
- [x] Inspector muestra panel + instancia; retales informativos si hay.
- [x] Guardar/reabrir `.bcproj` conserva colocaciones e inventario.

---

## Resultado

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 0 Arranque | OK | Welcome + tip/gates |
| 1 Proyecto | OK | Save/reveal/template |
| 2 Explorador/Inspector | OK | Edit selection gates |
| 3 Workspace | OK | Zoom/grid/fit/rotate |
| 4 Layout→Export | OK | Regresión multi-candidata |
| 5 Importación | OK | CSV/Excel + undo |
| 6 Timeline | OK | Export/clear/filters |
| 7 Preferencias/Ayuda | OK | Atajos/docs/tema |
| 8 Multipanel | OK | Ver `uat/multipanel/` |

**Veredicto:** x Listo para uso diario de estudio  □ Faltan huecos (anotar arriba)  □ Solo regresión automatizada

**Regresión auto (opcional):** `make test` → 562+ passed; multi-candidata:
`pytest tests/test_uat_multi_candidate_flow.py`.
