# Checklist humana — funcionalidad Studio

**Fecha:** 2026-07-25 (taller 0019–0024: 2026-09-14)  
**Base:** `main` tras IDE-0019…0024 + guía rápida  
**Versión:** `0.4.3`  
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
- [x] **Guardar** (**Ctrl+S**) / **Guardar como** (**Ctrl+Shift+S**) / **Abrir** (**Ctrl+O**) `.bcproj` (tips de estado); basename en barra de estado (tooltip = ruta; clic abre carpeta); **Ctrl+Shift+R** abre la carpeta (tip de estado); recuerda carpeta (`last_project_directory`).
- [ ] Barra de ruta: `●` delante del nombre si hay cambios sin guardar (IDE-0058).
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
- [ ] Inspector raíz/categoría: conteos, materiales y área (prefs);
  soluciones candidatas/seleccionada; sin edición inline (IDE-0050).
- [x] Clic en **pieza** → Inspector completo + selección en canvas.
- [x] Inspector de pieza: espesor (prefs), rotación 0°/90° (— si no
  colocada) y veta libre/fija; rotar (R) actualiza el ángulo.
- [ ] Preferencias unidades cm/in: Inspector de pieza/tablero y de layout
  muestra cm o in (área de retales incluida); Workspace, plano
  SVG/PDF/DXF y Comparador (Largo/Ancho + diffs) usan las mismas
  unidades; `.bcproj` / JSON siguen mm.
- [x] Clic en **tablero** → centra cámara y resalta en Workspace.
- [ ] Inspector tablero: instancias usadas, aprovechamiento y retales
  si hay layout; «sin layout» si no (IDE-0051).
- [x] Inspector pieza: área L×A (IDE-0055).
- [x] **Ctrl+Alt+I** copia el texto del Inspector (IDE-0057).
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
- [ ] **Ctrl+Alt+0** vuelve el zoom al 100% (IDE-0056).
- [x] Pan: botón medio, botón derecho, **Espacio + arrastre**.
- [x] Clic en vacío deselecciona; **Ctrl+A** / **Esc** / **Ctrl+Shift+I** (tips de estado en selección).
- [x] **Flechas** mueven 1 mm; **Shift+flechas** = tamaño de cuadrícula (prefs).
- [x] **R** rota si cabe (tip de estado); si no, se rechaza. Con **veta
  fija** la acción queda deshabilitada (`status.cannot_rotate_grain`).
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
- [ ] Tras **Calcular layout**, el canvas muestra preview de la mejor
  candidata sin aplicar `placements` (IDE-0052).
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
- [ ] Pack catálogo materiales recuerda carpeta (`last_material_catalog_directory`).
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
- [ ] Preferencias: export/import JSON de taller (fusionar / reemplazar);
  rutas locales y ventana no viajan; OK persiste (IDE-0049).
- [ ] Preferencias Avanzado: material por defecto; tablero y pieza nuevos
  lo heredan; editar conserva el del ítem (IDE-0053).
- [ ] Preferencias Avanzado: guardar / aplicar / eliminar perfil de taller
  (IDE-0054). OK persiste. Sin nube.
- [x] Geometría de ventana/docks se recuerda al reiniciar.
- [x] **Ayuda → Atajos de teclado…** (**F1**; tip de estado) lista el catálogo
  (incl. PgUp/PgDown, Ctrl+Shift+Return/E, Ctrl+Alt+B/E/M/K/X/C/T).
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

## 9. Taller 0.4.3 (IDE-0019…0024)

Regresión auto: `tests/test_grain.py`, `tests/test_kerf.py`,
`tests/test_cut_list.py`, `tests/test_multi_panel_skyline.py`,
`tests/test_project_serializer.py`. Guía: `docs/user/GUIA-RAPIDA.md`.

- [x] **Ctrl+Alt+M** metadatos (cliente / referencia / notas); Inspector en
  raíz del Explorador; `.bcproj` v3+.
- [x] **Ctrl+Alt+K** espesor de sierra; 0 mm = sin hueco; recalcular tras
  cambiar kerf marca soluciones desactualizadas.
- [x] Pieza: desmarcar «Permitir rotación» → veta fija; Calcular y **R** no
  giran; Inspector muestra veta.
- [x] **Ctrl+Alt+X** intercambia dos piezas colocadas; no-op si no caben o
  material/espesor no coinciden; se puede deshacer.
- [x] **Ctrl+Alt+C** lista de corte CSV/PDF (flujo aparte de Exportar
  solución); pide recalcular si outdated.
- [x] Varios tableros físicos: pipeline MaxRects **y** Skyline; Inspector
  panel + instancia.

---

## 10. Taller 0.4.4 (IDE-0026…)

Regresión auto: `tests/test_svg_exporter.py`, `tests/test_dxf_pdf_exporters.py`,
`tests/test_export_options.py`, `tests/test_pdf_page.py`,
`tests/test_cut_sequence.py`, `tests/test_material_catalog.py`,
`tests/test_material_cost.py`, `tests/test_quote.py`,
`tests/test_export_batch.py`,
`tests/test_suggest_gap.py`.

- [ ] **Ctrl+Shift+E** plano SVG/PDF: piezas muestran id y LxW según
  unidades de Preferencias (mm: `A 400x300`; cm: `A 40x30 cm`); retales
  y cotas L×A del tablero igual; desmarcar «Etiquetas de
  piezas», «Etiquetas de retales», «Cotas L×A del tablero» o
  «Trazabilidad (versión, algoritmo, fecha)» deja el plano sin ese
  texto; Workspace sigue mostrando solo piezas. El pie muestra
  versión, algoritmo y fecha; JSON/CSV no activan la casilla.
- [ ] **Ctrl+Shift+E** PDF de plano: papel A4/A3/Letter o ajustar al
  dibujo; escala fit o 1:n; márgenes mm. Lista de corte y presupuesto
  PDF no cambian de página.
- [ ] **Ctrl+Shift+E** PNG/JPEG: DPI 36–300 cambia el tamaño del archivo;
  JPEG calidad baja el peso; deshabilitado en SVG/PDF/DXF. Preferencias
  recuerdan DPI y calidad.
- [ ] **Ctrl+Shift+E** DXF: LibreCAD/QCAD lista capas PANELS / PIECES /
  OFFCUTS / DIMS / SEQ / META; ocultar DIMS o META no quita geometría.
- [ ] **Ctrl+Shift+E** lote: con ≥2 candidatas, marca «Exportar las N
  candidatas del ranking»; elige carpeta; aparecen
  `boardcomposer-solution-01` y siguientes. Con 1 candidata la casilla
  está deshabilitada. No usa `boardcomposer-batch`.
- [ ] **Ctrl+Alt+Q** presupuesto PDF: total material = tableros físicos
  × €/m²; si Preferencias tiene EUR/h y min/pieza > 0, suma mano de obra;
  0 omite labor; materiales sin precio aparecen como «-»; pie de
  versión/algoritmo/fecha; desmarcar trazabilidad en Preferencias lo
  quita; LxW/espesor siguen prefs.units; área m²; no cambia el `.bcproj`.
- [ ] **Ctrl+Alt+C** lista de corte: CSV/PDF con `sequence` y pasos de
  sierra (`saw`); el PDF incluye pie de trazabilidad y prefs.units; el
  CSV sigue mm y no lleva pie; el plano muestra el número de orden por
  panel.
- [ ] **Ctrl+Alt+F** en candidata parcial: piezas OK no se mueven;
  omitidas caben en retales o tablero libre; acción deshabilitada si la
  solución es completa.
- [ ] **Ctrl+Alt+R** con retales ≥ 50 mm: Explorer muestra tableros
  remnant; segundo disparo no duplica; undo los quita; origen no baja solo.
- [ ] **Ctrl+Alt+T** catálogo de materiales: añade un nombre/espesor/medida
  L×A; al añadir tablero el combo ofrece el nombre y la medida típica
  (`2800×2070`); el `.bcproj` no cambia de versión. **Exportar** genera
  JSON; **Importar** fusiona o reemplaza; no usa nube.
- [ ] **Ctrl+Alt+G** con una pieza: colocada → mismo panel al hueco
  MaxRects; sin colocar → tablero enfocado. Drop que solapa ajusta al
  hueco más cercano; material/espesor incompatible sigue revirtiendo.
  Veta fija no rota. Se puede deshacer.

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
| 9 Taller 0019–0024 | OK | Guía + tests grano/kerf/corte/Skyline |

**Veredicto:** x Listo para uso diario de estudio  □ Faltan huecos (anotar arriba)  □ Solo regresión automatizada

**Regresión auto (opcional):** `make test` → 1180+ passed; multi-candidata:
`pytest tests/test_uat_multi_candidate_flow.py`.
