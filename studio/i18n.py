"""UI language catalog for Studio (SCR-006)."""

from __future__ import annotations

VALID_LANGUAGES = ("es", "en")
DEFAULT_LANGUAGE = "es"

_STRINGS: dict[str, dict[str, str]] = {
    "es": {
        "language.es": "Español",
        "language.en": "English",
        "units.mm": "Milímetros (mm)",
        "units.cm": "Centímetros (cm)",
        "units.in": "Pulgadas (in)",
        "prefs.title": "Preferencias",
        "prefs.intro": (
            "Estas opciones se aplican a todos los proyectos y no forman "
            "parte del fichero `.bcproj`."
        ),
        "prefs.general": "General",
        "prefs.workspace": "Workspace",
        "prefs.algorithms": "Algoritmos",
        "prefs.export": "Exportación",
        "prefs.advanced": "Avanzado / rendimiento",
        "prefs.language": "Idioma:",
        "prefs.theme": "Tema:",
        "prefs.units": "Unidades:",
        "prefs.show_grid": "Mostrar cuadrícula",
        "prefs.grid_size": "Tamaño de cuadrícula:",
        "prefs.strategy": "Estrategia:",
        "prefs.use_custom_weights": "Usar pesos personalizados",
        "prefs.weight_material": "Aprovechamiento de material:",
        "prefs.weight_placed": "Piezas colocadas:",
        "prefs.weight_compactness": "Compacidad:",
        "prefs.weight_rotation": "Penalización por rotación:",
        "prefs.export_format": "Formato por defecto:",
        "prefs.export_metrics": "Incluir métricas (JSON)",
        "prefs.export_explanation": "Incluir explicación (JSON)",
        "prefs.export_offcuts": "Incluir retales",
        "prefs.max_solutions": "Máx. soluciones a conservar:",
        "prefs.open_config_folder": "Abrir carpeta de configuración…",
        "tip.open_config_folder": (
            "Abrir la carpeta de preferences.json en el explorador de archivos"
        ),
        "tip.template_rename": (
            "Renombrar la plantilla seleccionada; pide el nuevo nombre"
        ),
        "tip.template_delete": (
            "Eliminar la plantilla seleccionada del catálogo; pide confirmación"
        ),
        "prefs.restore_defaults": "Restaurar valores",
        "theme.system": "Sistema",
        "theme.light": "Claro",
        "theme.dark": "Oscuro",
        "strategy.balanced": "Equilibrada",
        "strategy.material": "Material primero",
        "strategy.compact": "Compacta primero",
        "strategy.exact": "Exacta (MaxRects + CP-SAT)",
        "welcome.tagline": (
            "Optimiza el corte de tableros. Crea un proyecto, abre uno reciente "
            "o importa piezas para empezar."
        ),
        "welcome.recent": "Proyectos recientes",
        "welcome.clear_recent": "Vaciar lista",
        "welcome.new": "Nuevo proyecto",
        "welcome.open": "Abrir proyecto…",
        "welcome.import": "Importar piezas (CSV/Excel)…",
        "welcome.demo": "Proyecto de ejemplo",
        "welcome.from_template": "Desde plantilla…",
        "welcome.docs": "Documentación…",
        "welcome.whats_new": "Novedades…",
        "welcome.preferences": "Preferencias…",
        "welcome.shortcuts": "Atajos…",
        "welcome.about": "Acerca de…",
        "welcome.remove_recent": "Quitar de recientes",
        "welcome.pin_recent": "Anclar",
        "welcome.unpin_recent": "Desanclar",
        "welcome.reveal_folder": "Mostrar en carpeta",
        "welcome.empty_recent": "Sin proyectos recientes",
        "menu.file": "Archivo",
        "menu.edit": "Editar",
        "menu.view": "Ver",
        "toolbar.main": "Barra principal",
        "action.toggle_toolbar": "Barra de herramientas",
        "tip.toggle_toolbar": "Mostrar u ocultar la barra de herramientas (Ctrl+Shift+K)",
        "tip.toggle_toolbar_show": "Mostrar la barra de herramientas (Ctrl+Shift+K)",
        "tip.toggle_toolbar_hide": "Ocultar la barra de herramientas (Ctrl+Shift+K)",
        "status.toolbar_shown": "Barra de herramientas visible",
        "status.toolbar_hidden": "Barra de herramientas oculta",
        "action.toggle_explorer": "Explorador",
        "tip.toggle_explorer": "Mostrar u ocultar el Explorador (Ctrl+1)",
        "tip.toggle_explorer_show": "Mostrar el Explorador (Ctrl+1)",
        "tip.toggle_explorer_hide": "Ocultar el Explorador (Ctrl+1)",
        "action.toggle_inspector": "Inspector",
        "tip.toggle_inspector": "Mostrar u ocultar el Inspector (Ctrl+2)",
        "tip.toggle_inspector_show": "Mostrar el Inspector (Ctrl+2)",
        "tip.toggle_inspector_hide": "Ocultar el Inspector (Ctrl+2)",
        "action.toggle_timeline": "Timeline",
        "tip.toggle_timeline": "Mostrar u ocultar el Timeline (Ctrl+3)",
        "tip.toggle_timeline_show": "Mostrar el Timeline (Ctrl+3)",
        "tip.toggle_timeline_hide": "Ocultar el Timeline (Ctrl+3)",
        "action.toggle_comparator": "Comparador de soluciones",
        "tip.toggle_comparator": "Mostrar u ocultar el Comparador de soluciones (Ctrl+4)",
        "tip.toggle_comparator_show": "Mostrar el Comparador de soluciones (Ctrl+4)",
        "tip.toggle_comparator_hide": "Ocultar el Comparador de soluciones (Ctrl+4)",
        "status.dock_shown": "{name} visible",
        "status.dock_hidden": "{name} oculto",
        "menu.project": "Proyecto",
        "menu.generate": "Generar",
        "menu.compare": "Comparar",
        "menu.export": "Exportar",
        "menu.help": "Ayuda",
        "menu.recent": "Abrir recientes",
        "action.new_project": "Nuevo proyecto",
        "action.new_demo_project": "Nuevo proyecto demo",
        "action.new_from_template": "Nuevo desde plantilla…",
        "action.save_as_template": "Guardar como plantilla…",
        "action.show_welcome": "Pantalla de inicio",
        "action.open": "Abrir…",
        "action.open_recent": "Abrir",
        "action.save": "Guardar",
        "action.save_as": "Guardar como…",
        "action.rename_project": "Renombrar proyecto…",
        "action.reveal_project_folder": "Abrir carpeta del proyecto",
        "action.diff_bcproj": "Comparar revisiones .bcproj…",
        "action.restore_local_revision": "Restaurar última revisión local…",
        "action.export_revision_backup": "Exportar backup de revisiones…",
        "action.add_board": "Añadir tablero…",
        "action.add_piece": "Añadir pieza…",
        "action.import_boards_csv": "Importar inventario de tableros (CSV/Excel)…",
        "action.import_pieces_csv": "Importar piezas (CSV/Excel)…",
        "diff_bcproj.title": "Comparar revisiones .bcproj",
        "diff_bcproj.intro": (
            "Diff estructural (meta, tableros, piezas, colocaciones). "
            "Al guardar se conserva un anillo de revisiones locales "
            "(carpeta oculta junto al .bcproj). Puedes restaurar una "
            "revisión del anillo en memoria (queda pendiente de Guardar)."
        ),
        "diff_bcproj.left": "Izquierda (antes)",
        "diff_bcproj.right": "Derecha (después)",
        "diff_bcproj.browse": "Examinar…",
        "diff_bcproj.browse_tip": "Elegir un archivo .bcproj en disco",
        "diff_bcproj.use_current": "Usar proyecto abierto como izquierda",
        "diff_bcproj.use_current_right": "Usar proyecto abierto como derecha",
        "diff_bcproj.revision": "Revisión guardada (izquierda)",
        "diff_bcproj.revision_none": "— (elegir archivo)",
        "diff_bcproj.current_project": "(proyecto abierto)",
        "diff_bcproj.compare": "Comparar",
        "diff_bcproj.compare_tip": (
            "Calcular el diff estructural entre izquierda y derecha"
        ),
        "diff_bcproj.restore": "Restaurar esta revisión…",
        "diff_bcproj.restore_tip": (
            "Cargar la revisión seleccionada en memoria (misma ruta; Guardar "
            "para escribir en disco)"
        ),
        "diff_bcproj.restore_idle": "Elige una revisión del anillo local",
        "diff_bcproj.restore_confirm_title": "Restaurar revisión local",
        "diff_bcproj.restore_confirm": (
            "¿Cargar la revisión «{name}» en el proyecto abierto?\n\n"
            "Se reemplaza el inventario en memoria. La ruta del archivo "
            "sigue siendo:\n{path}\n\n"
            "Los cambios sin guardar se pierden. Usa Guardar para escribir "
            "esta revisión en disco (el anillo conservará el archivo actual)."
        ),
        "diff_bcproj.restore_error_title": "No se pudo restaurar",
        "diff_bcproj.restore_not_in_ring": (
            "Solo se pueden restaurar snapshots del anillo local de este proyecto."
        ),
        "diff_bcproj.placeholder": "El resultado del diff aparecerá aquí.",
        "diff_bcproj.open_title": "Abrir .bcproj",
        "diff_bcproj.file_filter": "Proyectos BoardComposer (*.bcproj);;Todos (*.*)",
        "diff_bcproj.need_left": "Elige el .bcproj de la izquierda.",
        "diff_bcproj.need_right": "Elige el .bcproj de la derecha.",
        "diff_bcproj.error_title": "No se pudo comparar",
        "status.revision_restored": (
            "Revisión «{name}» cargada en memoria (pendiente de Guardar)"
        ),
        "status.revision_restore_no_file": (
            "Guarda el proyecto antes de restaurar una revisión local"
        ),
        "status.revision_restore_empty": (
            "No hay revisiones locales; guarda el proyecto al menos una vez "
            "más para crear el anillo"
        ),
        "status.revision_restore_failed": "No se pudo restaurar la revisión: {error}",
        "action.export_selected": "Exportar solución seleccionada…",
        "action.export_timeline": "Exportar historial del Timeline…",
        "action.exit": "Salir",
        "action.undo": "Deshacer",
        "action.redo": "Rehacer",
        "action.rotate_piece": "Rotar 90°",
        "action.rename_selection": "Renombrar…",
        "action.edit_selection": "Editar…",
        "action.copy_selection_id": "Copiar ID",
        "action.duplicate_piece": "Duplicar",
        "action.delete_piece": "Eliminar",
        "action.select_all_pieces": "Seleccionar todas las piezas",
        "action.deselect_pieces": "Deseleccionar piezas",
        "action.invert_selection": "Invertir selección",
        "action.preferences": "Preferencias…",
        "action.fit_board": "Ajustar al tablero",
        "action.fit_selection": "Ajustar a la selección",
        "action.zoom_in": "Acercar",
        "action.zoom_out": "Alejar",
        "action.toggle_grid": "Mostrar cuadrícula",
        "action.reset_window_layout": "Restablecer disposición de ventana",
        "action.solve_layout": "Calcular layout",
        "action.previous_solution": "Solución anterior",
        "action.next_solution": "Solución siguiente",
        "action.apply_layout": "Aplicar layout calculado",
        "action.no_recent": "Sin archivos recientes",
        "action.clear_recent": "Vaciar lista de recientes",
        "action.whats_new": "Novedades…",
        "dialog.clear_recent_title": "Vaciar recientes",
        "dialog.clear_recent_body": (
            "¿Vaciar la lista de proyectos recientes?\n"
            "Los archivos del disco no se eliminan."
        ),
        "status.recent_cleared": "Lista de recientes vaciada",
        "status.recent_removed": "Quitado de recientes: {path}",
        "status.recent_pinned": "Anclado en recientes: {path}",
        "status.recent_unpinned": "Desanclado de recientes: {path}",
        "action.explain_solution": "Explicar candidata…",
        "action.shortcuts": "Atajos de teclado…",
        "action.open_docs": "Documentación…",
        "action.about": "Acerca de BoardComposer…",
        "tip.new_project": (
            "Crear un proyecto vacío (Ctrl+N); pide nombre/unidades y "
            "confirmación si hay cambios sin guardar"
        ),
        "tip.new_demo_project": (
            "Abrir el proyecto de ejemplo con tableros, piezas y colocaciones "
            "(Ctrl+Shift+D); pide confirmación si hay cambios sin guardar"
        ),
        "tip.new_from_template": (
            "Elegir una plantilla guardada y crear un proyecto "
            "(Ctrl+Shift+N); pide confirmación si hay cambios sin guardar"
        ),
        "tip.save_as_template": (
            "Guardar el proyecto actual como plantilla (Ctrl+Shift+M); "
            "pide nombre y, si hay, si incluir colocaciones"
        ),
        "tip.show_welcome": (
            "Volver a la pantalla de inicio sin cerrar el proyecto (Ctrl+Shift+H)"
        ),
        "status.already_on_welcome": "Ya estás en la pantalla de inicio",
        "tip.open": (
            "Abrir un proyecto .bcproj (Ctrl+O); recuerda la última carpeta; "
            "pide confirmación si hay cambios sin guardar"
        ),
        "tip.save": (
            "Guardar el proyecto actual (Ctrl+S); si aún no tiene archivo, "
            "pide ruta (como Guardar como); si ya existe, deja revisión en el anillo"
        ),
        "tip.save_as": (
            "Guardar el proyecto con otro nombre o ruta (Ctrl+Shift+S); "
            "pasa a ser el archivo actual; si existe, deja revisión en el anillo; "
            "recuerda la última carpeta"
        ),
        "tip.rename_project": (
            "Cambiar el nombre del proyecto (Ctrl+Shift+F2); pide el nuevo nombre"
        ),
        "tip.reveal_project_folder": "Abrir la carpeta del archivo .bcproj (Ctrl+Shift+R)",
        "tip.status_project_path": (
            "{path}\nClic para abrir la carpeta (Ctrl+Shift+R)"
        ),
        "tip.status_project_unsaved": (
            "Guarda el proyecto (Ctrl+S) para abrir su carpeta"
        ),
        "tip.diff_bcproj": (
            "Comparar dos revisiones .bcproj o el proyecto abierto vs un archivo "
            "(Ctrl+Shift+Y); abre el diálogo; puede restaurar una revisión del anillo; "
            "recuerda la última carpeta"
        ),
        "tip.restore_local_revision": (
            "Cargar la última revisión del anillo local en memoria "
            "(Ctrl+Alt+Y); pide confirmación · Guardar para escribir en disco"
        ),
        "tip.export_revision_backup": (
            "Copia el .bcproj y el anillo .revs/ a una carpeta de backup "
            "(Ctrl+Alt+B); ofrece abrir esa carpeta; "
            "recuerda la última carpeta"
        ),
        "status.revision_backup_no_file": (
            "Guarda el proyecto en disco para exportar un backup de revisiones"
        ),
        "status.revision_backup_done": "Backup de revisiones exportado: {path}",
        "status.revision_backup_failed": "No se pudo exportar el backup: {error}",
        "dialog.export_revision_backup": "Carpeta de backup de revisiones",
        "tip.add_board": (
            "Añadir un tablero al inventario (Ctrl+Shift+B); "
            "abre el diálogo de ID y dimensiones"
        ),
        "tip.add_piece": (
            "Añadir una pieza al proyecto (Ctrl+Shift+P); "
            "abre el diálogo de ID, dimensiones y cantidad"
        ),
        "tip.import_boards_csv": (
            "Importar inventario de tableros desde CSV o Excel (Ctrl+Shift+T); "
            "recuerda la última carpeta; abre mapeo de columnas y vista previa"
        ),
        "tip.import_pieces_csv": (
            "Importar piezas desde CSV o Excel (Ctrl+Shift+O); "
            "recuerda la última carpeta; abre mapeo de columnas y vista previa"
        ),
        "tip.export_selected": (
            "Exportar la solución del Comparador (Ctrl+Shift+E); "
            "abre opciones de formato y vista previa "
            "(SVG/PNG/JPEG/PDF/DXF/JSON/CSV); "
            "ofrece abrir el archivo; "
            "recuerda la última carpeta"
        ),
        "tip.export_selected_outdated": (
            "Soluciones desactualizadas: al exportar (Ctrl+Shift+E) "
            "pide confirmar recalcular / exportar de todos modos / cancelar"
        ),
        "tip.export_timeline": (
            "Exportar el historial del Timeline (Ctrl+Shift+L): "
            "JSON o CSV según los filtros actuales; "
            "ofrece abrir el archivo; "
            "recuerda la última carpeta"
        ),
        "tip.exit": (
            "Cerrar BoardComposer Studio (Ctrl+Q); "
            "pide confirmación si hay cambios sin guardar"
        ),
        "tip.undo": "Deshacer la última acción (Ctrl+Z)",
        "tip.redo": "Rehacer la última acción deshecha (Ctrl+Shift+Z)",
        "tip.rotate_piece": (
            "Rotar 90° la pieza seleccionada en el lienzo (R); "
            "debe estar colocada en un tablero"
        ),
        "tip.rename_selection": (
            "Renombrar la pieza, el tablero o el proyecto seleccionado (F2); "
            "pide el nuevo nombre o ID"
        ),
        "tip.edit_selection": (
            "Editar la pieza o el tablero seleccionado (Return); "
            "abre el diálogo de ID y dimensiones"
        ),
        "tip.copy_selection_id": (
            "Copiar al portapapeles el ID de la pieza o tablero (Ctrl+Shift+C): "
            "Explorador, selección única o tablero enfocado"
        ),
        "tip.duplicate_piece": (
            "Duplicar la pieza o el tablero seleccionado (Ctrl+D); asigna un ID único"
        ),
        "tip.delete_piece": (
            "Eliminar la pieza o el tablero seleccionado (Backspace o Delete); "
            "pide confirmación"
        ),
        "tip.select_all_pieces": "Seleccionar todas las piezas del canvas (Ctrl+A)",
        "tip.deselect_pieces": "Quitar la selección de piezas del canvas (Escape)",
        "tip.invert_selection": "Invertir la selección de piezas del canvas (Ctrl+Shift+I)",
        "tip.preferences": (
            "Abrir preferencias globales: idioma, tema, unidades, cuadrícula, "
            "algoritmos y exportación (Ctrl+,); se aplican al aceptar"
        ),
        "status.pieces_selected": "{n} piezas seleccionadas",
        "status.no_pieces_to_select": "No hay piezas para seleccionar",
        "status.nothing_to_deselect": "No hay piezas seleccionadas",
        "status.selection_cleared": "Selección eliminada",
        "status.nothing_to_fit_selection": (
            "Selecciona una pieza o un tablero para ajustar la vista"
        ),
        "status.nothing_to_fit_board": "No hay tableros para ajustar la vista",
        "tip.fit_board": (
            "Ajustar el zoom para ver todos los tableros (Ctrl+0); ignora la selección"
        ),
        "tip.fit_selection": (
            "Ajustar el zoom a las piezas seleccionadas o al tablero enfocado "
            "(Ctrl+Shift+0)"
        ),
        "tip.zoom_in": "Acercar el Workspace (rueda, Ctrl+=)",
        "tip.zoom_out": "Alejar el Workspace (rueda, Ctrl+-)",
        "status.zoom_at_maximum": "Zoom al máximo",
        "status.zoom_at_minimum": "Zoom al mínimo",
        "tip.toggle_grid": "Mostrar u ocultar la cuadrícula del canvas (Ctrl+G)",
        "tip.toggle_grid_show": "Mostrar la cuadrícula del canvas (Ctrl+G)",
        "tip.toggle_grid_hide": "Ocultar la cuadrícula del canvas (Ctrl+G)",
        "status.grid_shown": "Cuadrícula visible",
        "status.grid_hidden": "Cuadrícula oculta",
        "tip.reset_window_layout": (
            "Volver a la disposición inicial de docks, toolbar y tamaño de ventana "
            "(Ctrl+Shift+W); guarda esa disposición"
        ),
        "status.window_layout_reset": "Disposición de ventana restablecida",
        "tip.solve_layout": (
            "Calcular soluciones de layout (Ctrl+Return); "
            "hace falta inventario de tableros y piezas"
        ),
        "tip.solve_layout_outdated": (
            "Soluciones desactualizadas: recalcula ahora (Ctrl+Return)"
        ),
        "tip.previous_solution": "Seleccionar la solución anterior (Re Pág)",
        "tip.previous_solution_outdated": (
            "Soluciones desactualizadas: navegas candidatas viejas (Re Pág); "
            "recalcula con el CTA del Comparador o Ctrl+Return"
        ),
        "tip.next_solution": "Seleccionar la solución siguiente (Av Pág)",
        "tip.next_solution_outdated": (
            "Soluciones desactualizadas: navegas candidatas viejas (Av Pág); "
            "recalcula con el CTA del Comparador o Ctrl+Return"
        ),
        "tip.apply_layout": (
            "Aplicar la solución seleccionada al proyecto (Ctrl+Shift+Return); "
            "sustituye las colocaciones actuales"
        ),
        "tip.apply_layout_outdated": (
            "Soluciones desactualizadas: al aplicar (Ctrl+Shift+Return) "
            "pide confirmar recalcular / aplicar de todos modos / cancelar"
        ),
        "tip.whats_new": (
            "Mostrar un resumen reciente del CHANGELOG en un diálogo (Ctrl+Shift+U)"
        ),
        "tip.explain_solution": (
            "Mostrar fortalezas, debilidades y notas de la candidata "
            "(Ctrl+Alt+E); en el diálogo podés Copiar al portapapeles"
        ),
        "tip.explain_solution_outdated": (
            "Soluciones desactualizadas: la explicación describe la candidata "
            "vieja; recalcula con el CTA del Comparador o Ctrl+Return "
            "(Ctrl+Alt+E)"
        ),
        "help.explain_solution_title": "Explicar candidata",
        "help.explain_solution_heading": (
            "Explicación determinista (sin IA en red). IDE-0007 MVP."
        ),
        "help.explain_solution_outdated_heading": (
            "Soluciones desactualizadas: esta explicación describe la "
            "candidata calculada antes de editar el proyecto. "
            "Explicación determinista (sin IA en red). IDE-0007 MVP."
        ),
        "help.explain_strengths": "Fortalezas",
        "help.explain_weaknesses": "Debilidades",
        "help.explain_notes": "Notas",
        "help.explain_empty": "Sin explicación disponible para esta candidata.",
        "help.explain_copy": "Copiar",
        "tip.explain_copy": "Copiar toda la explicación al portapapeles",
        "status.explain_copied": "Explicación copiada al portapapeles",
        "tip.shortcuts": (
            "Abrir el diálogo de atajos activos (F1); "
            "incluye filas contextuales del Timeline"
        ),
        "tip.open_docs": (
            "Abrir la guía rápida local en la app del sistema (Shift+F1)"
        ),
        "tip.about": (
            "Abrir Acerca de con la versión de BoardComposer Studio (Ctrl+Shift+A)"
        ),
        "tip.clear_recent": (
            "Vaciar la lista de proyectos recientes (Ctrl+Shift+X); "
            "pide confirmación (no borra archivos del disco)"
        ),
        "tip.remove_recent": (
            "Quitar este proyecto de la lista (Delete o Backspace); "
            "no borra el archivo del disco"
        ),
        "tip.pin_recent": "Anclar este proyecto arriba en la lista de recientes",
        "tip.unpin_recent": "Quitar el anclaje de este proyecto reciente",
        "tip.reveal_recent": "Mostrar el archivo .bcproj en el explorador de archivos",
        "tip.recent_row": (
            "{path}\nClic abre; pide confirmación si hay cambios sin guardar · "
            "menú: anclar / Mostrar en carpeta / quitar"
        ),
        "tip.recent_row_pinned": (
            "{path}\nClic abre; pide confirmación si hay cambios sin guardar · "
            "menú: desanclar / Mostrar en carpeta / quitar"
        ),
        "tip.recent_menu": ("{path} — Abrir · anclar · carpeta · quitar"),
        "tip.recent_menu_pinned": (
            "{path} (anclado) — Abrir · desanclar · carpeta · quitar"
        ),
        "tip.recent_menu_open": (
            "Abrir {path}; pide confirmación si hay cambios sin guardar"
        ),
        "tip.recent_menu_pin": "Anclar {path} arriba en recientes",
        "tip.recent_menu_unpin": "Quitar el anclaje de {path}",
        "tip.recent_menu_reveal": "Mostrar {path} en el explorador de archivos",
        "tip.recent_menu_remove": (
            "Quitar {path} de recientes; no borra el archivo del disco"
        ),
        "help.whats_new_title": "Novedades",
        "help.whats_new_heading": "Cambios recientes ({section})",
        "help.whats_new_unavailable": "No hay notas de versión disponibles.",
        "help.whats_new_read_error": "No se pudo leer CHANGELOG.md.",
        "help.whats_new_see_changelog": (
            "Consulta CHANGELOG.md para el detalle completo de la versión."
        ),
        "help.about_title": "Acerca de",
        "help.about_version": "Versión {version}",
        "help.about_blurb": (
            "Studio para optimizar el corte de tableros. "
            "Consulta la documentación local y el CHANGELOG del repositorio."
        ),
        "help.shortcuts_title": "Atajos de teclado",
        "help.shortcuts_intro": (
            "Atajos activos en BoardComposer Studio. "
            "Los mismos valores se aplican desde el menú y el teclado. "
            "En macOS, ⌘ (Command) es el modificador principal "
            "(no la tecla Control ⌃). "
            "En el Workspace: Espacio+arrastre, botón medio o derecho para "
            "desplazar; flechas (Shift = tamaño de cuadrícula) para mover "
            "la pieza; rueda para zoom. "
            "En el Timeline (lista enfocada): Espacio play/pausa, Inicio "
            "reinicia, ← / → paso a paso; Ctrl+C copia la línea del evento."
        ),
        "help.shortcuts_col_action": "Acción",
        "help.shortcuts_col_keys": "Atajo",
        "action.timeline_replay_play": "Timeline — Play / Pausa (lista enfocada)",
        "action.timeline_replay_reset": "Timeline — Inicio replay (lista enfocada)",
        "action.timeline_replay_back": "Timeline — Paso atrás (lista enfocada)",
        "action.timeline_replay_forward": ("Timeline — Paso adelante (lista enfocada)"),
        "action.timeline_copy_line": (
            "Timeline — Copiar línea de evento (lista enfocada)"
        ),
        "help.docs_missing": "No se encontró la documentación en:\n{path}",
        "status.docs_opened": "Guía rápida abierta",
        "dock.explorer": "Explorador",
        "dock.inspector": "Inspector",
        "dock.timeline": "Timeline",
        "dock.comparator": "Comparador de soluciones",
        "timeline.placeholder": "Timeline / Consola / Eventos",
        "timeline.filter": "Filtro:",
        "timeline.filter_all": "Todos los eventos",
        "timeline.filter_algorithm": "Algoritmo:",
        "timeline.filter_algorithm_all": "Todos los algoritmos",
        "timeline.filter_period": "Periodo:",
        "timeline.filter_period_all": "Todo el historial",
        "timeline.filter_period_1m": "Último minuto",
        "timeline.filter_period_5m": "Últimos 5 min",
        "timeline.filter_period_15m": "Últimos 15 min",
        "timeline.filter_period_1h": "Última hora",
        "timeline.filter_piece_moves": "Solo movimientos",
        "timeline.filter_markers": "Solo marcadores",
        "timeline.follow_latest": "Seguir",
        "timeline.clear_filters": "Limpiar filtros",
        "timeline.count_empty": "0 eventos",
        "timeline.count_all": "{n} eventos",
        "timeline.count_filtered": "{visible} de {total} eventos",
        "timeline.detail.duration_ms": "{n} ms",
        "timeline.clear": "Vaciar",
        "timeline.clear_confirm_title": "Vaciar Timeline",
        "timeline.clear_confirm": (
            "¿Vaciar el historial del Timeline ({n} eventos)? Esta acción no se puede deshacer."
        ),
        "timeline.copy_line": "Copiar línea",
        "timeline.copy_payload": "Copiar payload JSON",
        "status.timeline_copied": "Evento del Timeline copiado al portapapeles",
        "tip.timeline_clear": ("Vaciar el historial del Timeline (pide confirmación)"),
        "tip.timeline_clear_filters": "Quitar filtros de evento, algoritmo y periodo",
        "tip.timeline_follow": ("Mantener la vista en el último evento del Timeline"),
        "tip.timeline_filter_piece_moves": (
            "Mostrar solo movimientos de piezas (desactivar = todos)"
        ),
        "tip.timeline_filter_markers": ("Mostrar solo marcadores (desactivar = todos)"),
        "tip.timeline_filter_event": (
            "Limitar el historial a un tipo de evento concreto"
        ),
        "tip.timeline_filter_algorithm": (
            "Mostrar solo eventos de un algoritmo de cálculo"
        ),
        "tip.timeline_filter_period": ("Limitar el historial a un periodo reciente"),
        "tip.timeline_replay_mode": (
            "Reproducir colocaciones de la solución o las fases del solver"
        ),
        "tip.timeline_replay_speed": (
            "Velocidad de la reproducción automática en el Timeline"
        ),
        "tip.timeline_list": (
            "Lista enfocada: Espacio play/pausa, Inicio, ← / →, "
            "Ctrl+C copia la línea; menú contextual = payload JSON"
        ),
        "tip.timeline_copy_line": "Copiar la línea visible del evento (Ctrl+C)",
        "tip.timeline_copy_payload": "Copiar el payload JSON del evento",
        "status.timeline_clear_filters_idle": "No hay filtros activos",
        "status.timeline_filters_cleared": "Filtros del Timeline limpiados",
        "tip.timeline_replay_reset": "Inicio de la reproducción (Inicio)",
        "tip.timeline_replay_back": "Paso atrás (←)",
        "tip.timeline_replay_forward": "Paso adelante (→)",
        "tip.timeline_replay_play": "Play / Pausa (Espacio)",
        "status.timeline_replay_idle": (
            "Calcula un layout para reproducir la solución en el Timeline"
        ),
        "tip.timeline_mark": (
            "Añadir un marcador con nota (diálogo); opcional paso/algoritmo "
            "del replay activo"
        ),
        "timeline.export": "Exportar…",
        "timeline.mark": "Marcador…",
        "timeline.mark_dialog_title": "Añadir marcador",
        "timeline.mark_dialog_label": "Nota:",
        "timeline.detail.step": "paso {n}",
        "dialog.export_timeline": "Exportar historial del Timeline",
        "dialog.filter_timeline": "JSON (*.json);;CSV (*.csv)",
        "status.timeline_exported": "Historial del Timeline exportado: {path}",
        "status.timeline_export_empty": ("No hay eventos en el Timeline para exportar"),
        "status.timeline_clear_empty": ("No hay eventos en el Timeline para vaciar"),
        "status.timeline_export_failed": "No se pudo exportar el Timeline: {error}",
        "timeline.empty": "Sin eventos todavía. Las acciones del Studio aparecerán aquí.",
        "timeline.detail.count": "{n} ítem(s)",
        "timeline.detail.index": "#{n}",
        "timeline.event.ProjectCreated": "Proyecto creado",
        "timeline.event.ProjectModified": "Proyecto modificado",
        "timeline.event.ProjectSaved": "Proyecto guardado",
        "timeline.event.ProjectOpened": "Proyecto abierto",
        "timeline.event.CsvImported": "CSV importado",
        "timeline.event.PieceMoved": "Pieza movida",
        "timeline.event.SolutionGenerationStarted": "Cálculo iniciado",
        "timeline.event.SolutionGenerated": "Cálculo finalizado",
        "timeline.event.SolutionSelected": "Solución seleccionada",
        "timeline.event.SolutionsMarkedOutdated": "Soluciones desactualizadas",
        "timeline.event.ExportCompleted": "Exportación completada",
        "timeline.event.WorkspaceUpdated": "Workspace actualizado",
        "timeline.event.TimelineMarked": "Marcador",
        "comparator.solutions_outdated": (
            "Soluciones desactualizadas: el proyecto cambió. "
            "Vuelve a generar el layout para actualizarlas."
        ),
        "comparator.recalculate_layout": "Calcular layout",
        "inspector.solutions_outdated": (
            "⚠ Soluciones pendientes de regeneración (proyecto modificado)."
        ),
        "status.solutions_outdated": "Soluciones marcadas como desactualizadas",
        "dialog.outdated_solutions_title": "Soluciones desactualizadas",
        "dialog.outdated_solutions_apply": (
            "Las soluciones ya no coinciden con el proyecto actual. "
            "Recalcular es la opción segura; aplicar usa la candidata vieja."
        ),
        "dialog.outdated_solutions_apply_anyway": "Aplicar de todos modos",
        "dialog.outdated_solutions_export": (
            "Las soluciones ya no coinciden con el proyecto actual. "
            "Recalcular es la opción segura; exportar usa la candidata vieja."
        ),
        "dialog.outdated_solutions_export_anyway": "Exportar de todos modos",
        "timeline.replay_none": "Reproducción: sin solución",
        "timeline.replay_mode": "Modo:",
        "timeline.replay_mode_placements": "Colocaciones",
        "timeline.replay_mode_phases": "Fases del solver",
        "timeline.replay_speed": "Velocidad:",
        "timeline.replay_speed_slow": "Lenta",
        "timeline.replay_speed_normal": "Normal",
        "timeline.replay_speed_fast": "Rápida",
        "timeline.phase_none": "Sin traza de fases. Calcula un layout primero.",
        "timeline.phase_progress_idle": "Fases · 0/{total}",
        "timeline.phase_progress": "{kind} · {current}/{total}",
        "timeline.phase_progress_algo": ("{kind} · {algorithm} · {current}/{total}"),
        "timeline.phase_idle_detail": "inicio",
        "timeline.phase.generator_started": "Inicio algoritmo",
        "timeline.phase.generator_finished": "Fin algoritmo",
        "timeline.phase.placement_failures_summary": "Resumen fallos",
        "timeline.phase.placement_failed": "Fallo colocación",
        "timeline.phase.evaluation_started": "Inicio evaluación",
        "timeline.phase.evaluation_finished": "Fin evaluación",
        "timeline.phase.build_order": "Orden de construcción",
        "timeline.phase.cancelled": "Cancelado",
        "timeline.replay_progress": "Reproducción: {current}/{total} piezas",
        "timeline.replay_progress_algo": (
            "Algoritmo {algorithm} · {current}/{total} piezas"
        ),
        "timeline.replay_progress_algo_piece": (
            "Algoritmo {algorithm} · {piece} · {current}/{total}"
        ),
        "timeline.replay_algorithm_unknown": "desconocido",
        "timeline.detail.accepted": "aceptadas {n}",
        "timeline.detail.rejected": "rechazadas {n}",
        "timeline.detail.total": "total {n}",
        "timeline.detail.no_fit": "sin hueco {n}",
        "timeline.detail.incompatible": "incompatibles {n}",
        "timeline.reason.incompatible": "material/espesor incompatible",
        "timeline.reason.no_fit": "sin hueco",
        "timeline.event.AlgorithmStarted": "Algoritmo iniciado",
        "timeline.event.AlgorithmFinished": "Algoritmo finalizado",
        "timeline.event.EvaluationFinished": "Evaluación finalizada",
        "timeline.event.PlacementFailed": "Colocación fallida",
        "timeline.event.PlacementFailuresSummary": "Resumen de fallos de colocación",
        "timeline.replay_reset": "Inicio",
        "timeline.replay_back": "◀",
        "timeline.replay_forward": "▶",
        "timeline.replay_play": "Play",
        "timeline.replay_pause": "Pausa",
        "status.timeline_replay": "Reproducción {current}/{total}",
        "status.timeline_phase": "Fase {current}/{total}: {detail}",
        "status.timeline_seek": "Timeline: {detail}",
        "explorer.boards": "Tableros ({n})",
        "explorer.pieces": "Piezas ({n})",
        "explorer.solutions": "Soluciones ({n})",
        "explorer.units": "ud.",
        "explorer.solution": "Solución {n} — {pieces} piezas — {waste} huecos",
        "explorer.context.rename": "Renombrar…",
        "explorer.context.reveal_folder": "Abrir carpeta…",
        "explorer.context.edit": "Editar…",
        "explorer.context.duplicate": "Duplicar",
        "explorer.context.copy_id": "Copiar ID",
        "explorer.context.delete": "Eliminar",
        "explorer.context.add_board": "Añadir tablero…",
        "explorer.context.add_piece": "Añadir pieza…",
        "explorer.context.preview_solution": "Vista previa",
        "explorer.context.place_on_board": "Colocar en tablero enfocado",
        "tip.preview_solution": (
            "Mostrar la solución en el Workspace sin aplicarla; "
            "para conservarla usa Aplicar layout (Ctrl+Shift+Return)"
        ),
        "tip.preview_solution_outdated": (
            "Soluciones desactualizadas: la vista previa muestra una candidata "
            "vieja; recalcula con el CTA del Comparador o Ctrl+Return"
        ),
        "explorer.unplaced_mark": "sin colocar",
        "inspector.title": "Inspector",
        "inspector.none": "Sin selección",
        "inspector.board": "Tablero",
        "inspector.piece": "Pieza",
        "inspector.dimensions": "Dimensiones",
        "inspector.thickness": "Espesor",
        "inspector.quantity": "Cantidad",
        "inspector.material": "Material",
        "inspector.position": "Posición",
        "inspector.unplaced": "Sin colocar en el Workspace",
        "inspector.place_hint": (
            "Consejo: enfoca un tablero en el Explorador y usa "
            "«Colocar en tablero enfocado» (o doble clic)."
        ),
        "inspector.no_panel": "Sin tablero asignado",
        "inspector.panel_instance": "{board} · instancia {instance}/{quantity}",
        "inspector.layout_title": "Layout calculado",
        "inspector.solution": "Solución: {current} / {total}",
        "inspector.strategy": "Estrategia: {name}",
        "inspector.placed": "Piezas colocadas: {n}",
        "inspector.total_length": "Largo total: {value} mm",
        "inspector.total_width": "Ancho total: {value} mm",
        "inspector.internal_waste": "Huecos internos: {value}",
        "inspector.free_material": "Material libre: {value}",
        "inspector.omitted": "Piezas omitidas: {ids}",
        "inspector.offcuts": ("Retales aprovechables: {n} (área total {area} mm²)"),
        "inspector.highlights": "Puntos clave: {items}",
        "inspector.no_solution": "Sin solución",
        "inspector.layout_cancelled": "Cálculo cancelado",
        "inspector.strategy_unknown": "desconocida",
        "comparator.pieces": "Piezas",
        "comparator.waste": "Huecos",
        "comparator.board_free": "Tablero libre",
        "comparator.length": "Largo",
        "comparator.width": "Ancho",
        "comparator.score": "Score",
        "comparator.sort_by": "Ordenar por:",
        "comparator.complete_only": "Solo soluciones completas",
        "comparator.pin_reference": "Fijar como referencia",
        "tip.pin_reference": (
            "Fija la candidata seleccionada como referencia del diff "
            "(hace falta ≥2 soluciones)"
        ),
        "tip.pin_reference_outdated": (
            "Soluciones desactualizadas: el diff usa candidatas viejas; "
            "recalcula con el CTA del Comparador o Ctrl+Return"
        ),
        "tip.comparator_sort": (
            "Ordena las candidatas: ranking del solver, piezas, huecos, "
            "tablero libre o puntuación (solo esta sesión)"
        ),
        "tip.comparator_complete_only": (
            "Mostrar solo candidatas completas (sin piezas omitidas); "
            "desactivar = también las parciales"
        ),
        "comparator.reference_mark": "Ref {n}",
        "comparator.reference_thumb": "#{n} · ref",
        "comparator.reference_tooltip": "Referencia fijada (solución {n})",
        "comparator.diff_title": "Diferencias vs referencia",
        "comparator.diff_placeholder": (
            "Diferencias respecto a la solución de referencia"
        ),
        "comparator.best_in": "Mejor en: {items}",
        "comparator.unplaced_suffix": " ({n} sin colocar)",
        "sort.ranking": "Orden del solver",
        "sort.pieces": "Piezas colocadas",
        "sort.waste": "Huecos internos",
        "sort.board_waste": "Tablero libre",
        "sort.score": "Puntuación",
        "highlight.pieces": "Piezas colocadas",
        "highlight.waste": "Menos huecos internos",
        "highlight.score": "Mejor puntuación",
        "highlight.board_free": "Menos tablero libre",
        "highlight.length": "Menor largo",
        "highlight.width": "Menor ancho",
        "diag.title": "Diagnóstico del cálculo",
        "diag.cancelled": "Cancelado por el usuario",
        "diag.generated": "Candidatas generadas: {n}",
        "diag.unique": "Candidatas únicas: {n}",
        "diag.accepted": "Aceptadas: {n}",
        "diag.rejected": "Rechazadas: {n}",
        "diag.reasons": "Motivos de rechazo:",
        "diag.missing_board": "Piezas omitidas",
        "diag.duplicate_board": "Piezas duplicadas",
        "diag.unknown_board": "Piezas desconocidas",
        "diag.overlap": "Solapes",
        "diag.exceeds_constraints": "Fuera del tablero",
        "diag.unassigned_stock_panel": "Sin tablero asignado",
        "diag.unknown_stock_panel": "Tablero desconocido",
        "diag.exceeds_stock_panel": "Fuera del tablero físico",
        "diag.panel_thickness_mismatch": "Espesor incompatible",
        "diag.panel_material_mismatch": "Material incompatible",
        "workspace.empty_title": "Empieza tu proyecto",
        "workspace.empty_blurb": (
            "Añade tableros y piezas, o impórtalos desde CSV/Excel "
            "para comenzar a componer."
        ),
        "status.ready": "BoardComposer Studio listo",
        "status.project_unsaved": "Proyecto aún no guardado",
        "status.zoom": "{n}%",
        "tip.zoom_status": (
            "Nivel de zoom del Workspace (rueda, Ctrl+= / Ctrl+-, Ctrl+0)"
        ),
        "status.project_folder_unavailable": "Guarda el proyecto para abrir su carpeta",
        "status.project_folder_failed": "No se pudo abrir la carpeta del proyecto",
        "status.project_folder_opened": "Carpeta del proyecto abierta",
        "status.welcome": "Pantalla de inicio",
        "status.new_empty": "Nuevo proyecto vacío creado",
        "status.new_project_created": "Proyecto «{name}» creado",
        "project.untitled": "Proyecto sin título",
        "status.demo_created": "Proyecto demo creado — Ctrl+Return calcula varias candidatas",
        "status.demo_created_max_solutions_raised": (
            "Proyecto demo creado — Máx. soluciones era 1; restaurado a {n} "
            "para el Comparador (Ctrl+Return)"
        ),
        "status.template_saved": "Plantilla «{name}» guardada",
        "status.template_loaded": "Proyecto creado desde «{name}»",
        "status.template_empty": "No hay plantillas de proyecto guardadas",
        "status.template_missing_project": "No hay un proyecto abierto para guardar como plantilla",
        "template.pick_title": "Nuevo desde plantilla",
        "template.pick_intro": (
            "Elige una plantilla. Se creará un proyecto nuevo con sus "
            "tableros y piezas; si guarda colocaciones, podrás restaurarlas."
        ),
        "template.pick_item": "{name} — {boards} tablero(s), {pieces} pieza(s)",
        "template.pick_item_with_placements": (
            "{name} — {boards} tablero(s), {pieces} pieza(s), "
            "{placements} colocación(es)"
        ),
        "template.load_placements": "¿Restaurar también las colocaciones de la plantilla?",
        "template.rename": "Renombrar…",
        "template.rename_title": "Renombrar plantilla",
        "template.rename_prompt": "Nuevo nombre:",
        "template.rename_failed": "No se pudo renombrar a «{name}».",
        "template.delete": "Eliminar…",
        "template.delete_title": "Eliminar plantilla",
        "template.delete_confirm": "¿Eliminar la plantilla «{name}»?",
        "template.delete_failed": "No se pudo eliminar «{name}».",
        "template.save_title": "Guardar como plantilla",
        "template.save_prompt": "Nombre de la plantilla:",
        "template.save_placements": "¿Incluir también las colocaciones actuales?",
        "template.empty_name": "El nombre de la plantilla no puede estar vacío.",
        "status.board_id_exists": "Ya existe un tablero con id {id}",
        "status.board_id_empty": "El identificador del tablero no puede estar vacío",
        "status.board_added": "Tablero añadido",
        "status.boards_imported": "{n} tablero(s) importado(s)",
        "status.pieces_imported": "{n} pieza(s) importada(s)",
        "status.import_template_applied": "Mapeo aplicado desde plantilla «{name}»",
        "status.import_template_saved": "Plantilla de importación «{name}» guardada",
        "status.piece_id_empty": "El identificador de la pieza no puede estar vacío",
        "status.piece_id_exists": "Ya existe una pieza con id {id}",
        "status.pieces_added": "{n} piezas añadidas",
        "status.piece_added": "Pieza añadida",
        "status.piece_duplicated": "Pieza duplicada: {id}",
        "status.board_duplicated": "Tablero duplicado: {id}",
        "status.id_copied": "ID copiado: {id}",
        "status.select_piece_first": "Selecciona una pieza primero",
        "status.place_piece_before_rotate": (
            "Coloca la pieza en un tablero antes de rotarla"
        ),
        "status.nothing_to_duplicate": (
            "Selecciona una pieza o un tablero para duplicar"
        ),
        "status.nothing_to_delete": ("Selecciona una pieza o un tablero para eliminar"),
        "status.cannot_rotate": "La pieza no puede rotarse en esa posición",
        "status.piece_rotated": "Pieza rotada 90°",
        "status.piece_placed": "Pieza {piece} colocada en {board}",
        "status.piece_already_placed": "La pieza {id} ya está colocada",
        "status.place_needs_board_focus": (
            "Selecciona un tablero en el Explorador para colocar la pieza"
        ),
        "status.place_piece_missing": "No se encuentra la pieza «{id}»",
        "status.place_board_missing": "No se encuentra el tablero «{id}»",
        "status.rename_unchanged": "El nombre no cambió",
        "status.edit_unchanged": "Sin cambios que aplicar",
        "status.place_no_space": "No cabe {piece} en {board}",
        "status.place_incompatible_thickness": (
            "Espesor incompatible: {piece} ({piece_thickness}) ≠ "
            "{board} ({board_thickness}). Edita la pieza o el tablero."
        ),
        "status.place_incompatible_material": (
            "Material incompatible: {piece} («{piece_material}») ≠ "
            "{board} («{board_material}»). Edita la pieza o el tablero."
        ),
        "status.place_incompatible_both": (
            "Material/espesor incompatibles: {piece} "
            "({piece_thickness}, «{piece_material}») ≠ {board} "
            "({board_thickness}, «{board_material}»)."
        ),
        "status.prefs_saved": "Preferencias guardadas",
        "status.nothing_to_solve": "No hay proyecto para calcular layout",
        "status.solve_needs_inventory": (
            "Añade al menos un tablero y una pieza antes de calcular layout"
        ),
        "status.solve_needs_boards": (
            "Añade al menos un tablero antes de calcular layout"
        ),
        "status.solve_needs_pieces": (
            "Añade al menos una pieza antes de calcular layout"
        ),
        "status.layout_failed": "No se pudo calcular layout",
        "status.layout_partial": "Layout parcial: {omitted} pieza(s) sin colocar de {total} soluciones",
        "status.layout_ok": (
            "Layout calculado: {n} soluciones — Re/Av Pág · "
            "Fijar referencia · Exportar Ctrl+Shift+E"
        ),
        "status.layout_ok_single": (
            "Layout calculado: 1 única candidata (no hay más distintas; "
            "generadas {generated}, únicas {unique}). "
            "Varias candidatas: demo Ctrl+Shift+D → Calcular · Exportar Ctrl+Shift+E"
        ),
        "status.layout_truncated_by_limit": (
            "Mostrando {shown}/{accepted} soluciones (límite en Preferencias: {limit}). "
            "Re/Av Pág recorre las visibles."
        ),
        "status.layout_computing": "Calculando layout…",
        "status.layout_cancelled": "Cálculo de layout cancelado",
        "status.layout_error": "Error al calcular layout: {error}",
        "progress.layout_title": "Generar soluciones",
        "progress.layout_label": "Ejecutando algoritmos de empaquetado…",
        "progress.layout_cancel": "Cancelar",
        "status.select_solution_first": "Primero selecciona una solución",
        "status.reference_pinned": "Referencia fijada en solución #{n}",
        "status.calculate_layout_first": (
            "Primero calcula un layout (Ctrl+Return). "
            "Luego Exportar (Ctrl+Shift+E) o Aplicar (Ctrl+Shift+Return)"
        ),
        "status.solution_applied": "Solución {current}/{total} aplicada al proyecto",
        "status.no_solutions": "No hay soluciones calculadas",
        "status.no_solutions_match_filter": (
            "Ninguna candidata coincide con el filtro del Comparador "
            "(quita «solo completas» o cambia el orden)"
        ),
        "status.only_one_visible_solution": (
            "Solo hay 1 candidata visible — Re Pág / Av Pág no tienen otra a la que ir"
        ),
        "status.only_one_visible_truncated": (
            "Solo 1 visible de {accepted} aceptadas (límite Preferencias: {limit}). "
            "Sube «Máx. soluciones» para recorrer más con Re/Av Pág"
        ),
        "status.previewing_solution": "Previsualizando solución {current}/{total}. Pulsa 'Aplicar layout calculado' para conservarla.",
        "status.export_failed": "No se pudo exportar {format}: {error}",
        "status.exported": "{format} exportado: {path}",
        "status.export_open_failed": "No se pudo abrir el archivo: {path}",
        "status.export_reveal_failed": "No se pudo abrir la carpeta de: {path}",
        "status.nothing_to_undo": "No hay acciones para deshacer",
        "status.nothing_to_redo": "No hay acciones para rehacer",
        "status.undone": "Acción deshecha",
        "status.redone": "Acción rehecha",
        "status.nothing_to_save": "No hay proyecto para guardar",
        "status.nothing_to_rename": "No hay proyecto para renombrar",
        "status.nothing_to_rename_selection": (
            "Selecciona una pieza, un tablero o el proyecto para renombrar"
        ),
        "status.nothing_to_edit_selection": (
            "Selecciona una pieza o un tablero para editar"
        ),
        "status.nothing_to_copy_id": (
            "Selecciona una pieza o un tablero para copiar su ID"
        ),
        "status.no_recent_to_clear": "No hay proyectos recientes para vaciar",
        "status.save_failed": "No se pudo guardar: {error}",
        "status.project_renamed": "Proyecto renombrado: {name}",
        "status.piece_renamed": "Pieza renombrada: {id}",
        "status.board_renamed": "Tablero renombrado: {id}",
        "status.project_saved": "Proyecto guardado: {path}",
        "status.project_saved_with_revision": (
            "Proyecto guardado: {path} (revisión anterior: {revision})"
        ),
        "status.project_opened": "Proyecto abierto: {path}",
        "status.board_updated": "Tablero actualizado",
        "status.board_deleted": "Tablero eliminado: {id}",
        "status.piece_deleted": "Pieza eliminada: {id}",
        "status.piece_updated": "Pieza actualizada",
        "dialog.open_project": "Abrir proyecto",
        "dialog.save_project": "Guardar proyecto",
        "dialog.unsaved_title": "Cambios sin guardar",
        "dialog.unsaved_body": (
            "El proyecto «{name}» tiene cambios sin guardar.\n"
            "{location}\n\n"
            "¿Quieres guardarlos antes de continuar?"
        ),
        "dialog.unsaved_unnamed": "Sin nombre",
        "dialog.unsaved_location_file": "Archivo: {path}",
        "dialog.unsaved_location_new": "Todavía no se ha guardado en un archivo.",
        "dialog.unsaved_save": "Guardar",
        "dialog.unsaved_discard": "Descartar",
        "dialog.unsaved_cancel": "Cancelar",
        "dialog.save_failed_title": "No se pudo guardar",
        "dialog.import_boards": "Importar inventario de tableros (CSV/Excel)",
        "dialog.import_boards_short": "Importar inventario de tableros",
        "dialog.import_pieces": "Importar piezas (CSV/Excel)",
        "dialog.import_pieces_short": "Importar piezas",
        "dialog.export_selected": "Exportar solución seleccionada",
        "dialog.filter_csv_excel": "CSV / Excel (*.csv *.xlsx);;CSV (*.csv);;Excel (*.xlsx);;Todos los archivos (*)",
        "dialog.filter_bcproj": "BoardComposer Project (*.bcproj)",
        "dialog.edit_board": "Editar tablero",
        "dialog.edit_piece": "Editar pieza",
        "dialog.rename_project_title": "Renombrar proyecto",
        "dialog.rename_piece_title": "Renombrar pieza",
        "dialog.rename_board_title": "Renombrar tablero",
        "dialog.delete_board_title": "Eliminar tablero",
        "dialog.delete_board_confirm": "¿Eliminar el tablero «{id}»?",
        "dialog.delete_board_confirm_placements": (
            "¿Eliminar el tablero «{id}»?\n\n"
            "Se quitarán {n} colocación(es) de ese tablero; las piezas se conservan."
        ),
        "dialog.delete_piece_title": "Eliminar pieza",
        "dialog.delete_piece_confirm": "¿Eliminar la pieza «{id}»?",
        "dialog.delete_piece_confirm_placed": (
            "¿Eliminar la pieza «{id}»?\n\n"
            "También se quitará su colocación en el Workspace."
        ),
        "export.title": "Exportar solución",
        "export.intro": "Elige el formato y el contenido. La vista previa refleja las opciones seleccionadas.",
        "export.template": "Plantilla:",
        "export.no_template": "(sin plantilla)",
        "export.save": "Guardar…",
        "export.delete": "Eliminar",
        "tip.export_save_template": (
            "Guardar la configuración actual como plantilla de exportación; "
            "pide el nombre"
        ),
        "tip.export_delete_template": (
            "Eliminar la plantilla de exportación seleccionada; pide confirmación"
        ),
        "tip.export_share_export": (
            "Exportar el catálogo de plantillas a un pack JSON; "
            "respeta el filtro de cliente actual; "
            "recuerda la última carpeta"
        ),
        "tip.export_share_import": (
            "Importar un pack de plantillas de exportación; "
            "recuerda la última carpeta; pide fusionar o reemplazar el catálogo"
        ),
        "export.format": "Formato:",
        "export.metrics": "Incluir métricas (JSON)",
        "export.explanation": "Incluir explicación (JSON)",
        "export.offcuts": "Incluir retales",
        "export.graphic": "Vista previa gráfica",
        "export.summary": "Resumen / contenido",
        "export.export_btn": "Exportar…",
        "export.save_template_title": "Guardar plantilla",
        "export.save_template_prompt": "Nombre de la plantilla:",
        "export.empty_name": "El nombre de la plantilla no puede estar vacío.",
        "export.delete_title": "Eliminar plantilla",
        "export.delete_confirm": "¿Eliminar la plantilla «{name}»?",
        "export.no_preview": "Sin vista previa",
        "export.client": "Cliente:",
        "export.client_all": "(todos los clientes)",
        "export.client_general": "(general)",
        "export.client_prompt": "Cliente (opcional):",
        "export.share_export": "Exportar pack…",
        "export.share_import": "Importar pack…",
        "export.share_export_title": "Exportar plantillas",
        "export.share_import_title": "Importar plantillas",
        "export.share_filter": "Plantillas BoardComposer (*.json)",
        "export.share_export_done": "Se exportaron {count} plantilla(s).",
        "export.share_import_mode": (
            "¿Fusionar con las plantillas existentes?\n\n"
            "Sí = fusionar (sustituye homónimas)\n"
            "No = reemplazar todo el catálogo\n"
            "Cancelar = no importar"
        ),
        "export.share_import_done": (
            "Importadas {imported} plantilla(s) ({mode}). Catálogo actual: {total}."
        ),
        "export.share_mode_merge": "fusión",
        "export.share_mode_replace": "reemplazo",
        "export.share_error": "No se pudo completar la operación:\n{error}",
        "export.done_title": "Exportación completada",
        "export.done_message": "Archivo guardado:\n{path}",
        "export.done_message_folder": "Carpeta creada:\n{path}",
        "export.open_file": "Abrir archivo",
        "export.open_folder": "Abrir carpeta",
        "export.reveal_folder": "Mostrar en carpeta",
        "import.boards_title": "Importar inventario de tableros (CSV)",
        "import.pieces_title": "Importar piezas (CSV)",
        "import.file_error_header": "No se pudo procesar el archivo:",
        "import.file_failed": "El archivo no se pudo importar.",
        "import.boards_summary": "{valid} tablero(s) válido(s), {invalid} fila(s) con errores.",
        "import.pieces_summary": "{pieces} pieza(s) válida(s) en {rows} fila(s); {invalid} fila(s) con errores.",
        "import.col.row": "Fila",
        "import.col.id": "Id",
        "import.col.base_id": "Id base",
        "import.col.quantity": "Cantidad",
        "import.col.generated_ids": "Ids generados",
        "import.col.length": "Largo",
        "import.col.width": "Ancho",
        "import.col.thickness": "Espesor",
        "import.col.material": "Material",
        "import.col.status": "Estado",
        "import.mapping_title": "Asignar columnas",
        "import.mapping_intro": (
            "No se reconocieron columnas obligatorias ({fields}). "
            "Asigna cada campo a una columna del archivo:"
        ),
        "import.mapping_none": "(ninguna)",
        "import.mapping_incomplete": (
            "Siguen faltando columnas obligatorias: {fields}"
        ),
        "import.mapping_template": "Plantilla:",
        "import.mapping_delete": "Eliminar…",
        "tip.import_mapping_delete": (
            "Eliminar la plantilla de mapeo seleccionada; pide confirmación"
        ),
        "import.mapping_delete_title": "Eliminar plantilla de importación",
        "import.mapping_delete_confirm": "¿Eliminar la plantilla «{name}»?",
        "import.mapping_save_title": "Guardar plantilla de importación",
        "import.mapping_save_prompt": (
            "¿Guardar este mapeo de columnas como plantilla reutilizable?"
        ),
        "import.mapping_save_name": "Nombre de la plantilla:",
        "import.mapping.field.board_id": "Id tablero",
        "import.mapping.field.piece_id": "Id pieza",
        "import.mapping.field.length_mm": "Largo",
        "import.mapping.field.width_mm": "Ancho",
        "import.mapping.field.thickness_mm": "Espesor",
        "import.mapping.field.quantity": "Cantidad",
        "import.mapping.field.material": "Material",
        "import.sheet_title": "Seleccionar hoja",
        "import.sheet_label": "Hoja del libro Excel:",
        "form.new_project": "Nuevo proyecto",
        "form.project_name": "Nombre del proyecto:",
        "form.project_name_placeholder": "Ej. Cocina Nordik",
        "dialog.project_name_required": "El nombre del proyecto no puede estar vacío.",
        "form.new_board": "Nuevo tablero",
        "form.new_piece": "Nueva pieza",
        "form.id": "Identificador:",
        "form.length": "Largo ({unit}):",
        "form.width": "Ancho ({unit}):",
        "form.thickness": "Espesor ({unit}):",
        "form.quantity": "Cantidad:",
        "form.material": "Material:",
        "form.allow_rotation": "Permitir rotación:",
        "diff.title": "Diferencias",
        "diff.identical": "Solución #{candidate} es idéntica a la referencia #{reference}.",
        "diff.header": "Diferencias de #{candidate} respecto a la referencia #{reference}",
        "diff.sync_header": (
            "Reproducción sincronizada · paso {step}/{total} "
            "(#{candidate} vs ref. #{reference})"
        ),
        "diff.sync_empty": "Sin piezas reveladas todavía. Pulsa ▶ o Play.",
        "diff.sync_same_solution": (
            "La referencia es la solución en reproducción "
            "({revealed}/{total} piezas visibles)."
        ),
        "diff.sync_matched": (
            "Hasta el paso {step}, candidato y referencia coinciden "
            "en las piezas reveladas."
        ),
        "diff.metrics": "Métricas",
        "diff.placements": "Colocaciones",
        "diff.none": "Sin diferencias relevantes en métricas ni colocaciones.",
        "diff.better_here": "  ↑ mejor aquí",
        "diff.better_reference": "  ↑ mejor en referencia",
        "diff.need_two": (
            "Se necesitan ≥2 soluciones para el diff. "
            "Prueba demo Ctrl+Shift+D → Calcular layout."
        ),
        "diff.select_solution": "Selecciona una solución en el Comparador.",
        "diff.metric.pieces": "Piezas colocadas",
        "diff.metric.omitted": "Piezas omitidas",
        "diff.metric.waste": "Huecos internos",
        "diff.metric.board_free": "Material libre",
        "diff.metric.length": "Largo total (mm)",
        "diff.metric.width": "Ancho total (mm)",
        "diff.metric.panels": "Paneles usados",
        "diff.metric.offcuts": "Retales",
        "diff.metric.score": "Puntuación",
        "diff.metric.completeness": "Completitud",
        "diff.complete": "completa",
        "diff.partial": "parcial",
        "diff.no_panel": "sin panel",
        "diff.panel": "panel {stock}.{instance}",
        "diff.rotated": " rotada",
        "diff.only_reference": "solo en referencia ({placement})",
        "diff.only_candidate": "solo aquí ({placement})",
    },
    "en": {
        "language.es": "Spanish",
        "language.en": "English",
        "units.mm": "Millimetres (mm)",
        "units.cm": "Centimetres (cm)",
        "units.in": "Inches (in)",
        "prefs.title": "Preferences",
        "prefs.intro": (
            "These options apply to all projects and are not part of "
            "the `.bcproj` file."
        ),
        "prefs.general": "General",
        "prefs.workspace": "Workspace",
        "prefs.algorithms": "Algorithms",
        "prefs.export": "Export",
        "prefs.advanced": "Advanced / performance",
        "prefs.language": "Language:",
        "prefs.theme": "Theme:",
        "prefs.units": "Units:",
        "prefs.show_grid": "Show grid",
        "prefs.grid_size": "Grid size:",
        "prefs.strategy": "Strategy:",
        "prefs.use_custom_weights": "Use custom weights",
        "prefs.weight_material": "Material utilization:",
        "prefs.weight_placed": "Pieces placed:",
        "prefs.weight_compactness": "Compactness:",
        "prefs.weight_rotation": "Rotation penalty:",
        "prefs.export_format": "Default format:",
        "prefs.export_metrics": "Include metrics (JSON)",
        "prefs.export_explanation": "Include explanation (JSON)",
        "prefs.export_offcuts": "Include offcuts",
        "prefs.max_solutions": "Max solutions to keep:",
        "prefs.open_config_folder": "Open settings folder…",
        "tip.open_config_folder": (
            "Open the preferences.json folder in the file manager"
        ),
        "tip.template_rename": ("Rename the selected template; asks for the new name"),
        "tip.template_delete": (
            "Delete the selected template from the catalog; asks for confirmation"
        ),
        "prefs.restore_defaults": "Restore defaults",
        "theme.system": "System",
        "theme.light": "Light",
        "theme.dark": "Dark",
        "strategy.balanced": "Balanced",
        "strategy.material": "Material first",
        "strategy.compact": "Compact first",
        "strategy.exact": "Exact (MaxRects + CP-SAT)",
        "welcome.tagline": (
            "Optimise panel cutting. Create a project, open a recent one, "
            "or import pieces to get started."
        ),
        "welcome.recent": "Recent projects",
        "welcome.clear_recent": "Clear list",
        "welcome.new": "New project",
        "welcome.open": "Open project…",
        "welcome.import": "Import pieces (CSV/Excel)…",
        "welcome.demo": "Sample project",
        "welcome.from_template": "From template…",
        "welcome.docs": "Documentation…",
        "welcome.whats_new": "What’s new…",
        "welcome.preferences": "Preferences…",
        "welcome.shortcuts": "Shortcuts…",
        "welcome.about": "About…",
        "welcome.remove_recent": "Remove from recent",
        "welcome.pin_recent": "Pin",
        "welcome.unpin_recent": "Unpin",
        "welcome.reveal_folder": "Show in folder",
        "welcome.empty_recent": "No recent projects",
        "menu.file": "File",
        "menu.edit": "Edit",
        "menu.view": "View",
        "toolbar.main": "Main toolbar",
        "action.toggle_toolbar": "Toolbar",
        "tip.toggle_toolbar": "Show or hide the main toolbar (Ctrl+Shift+K)",
        "tip.toggle_toolbar_show": "Show the main toolbar (Ctrl+Shift+K)",
        "tip.toggle_toolbar_hide": "Hide the main toolbar (Ctrl+Shift+K)",
        "status.toolbar_shown": "Toolbar visible",
        "status.toolbar_hidden": "Toolbar hidden",
        "action.toggle_explorer": "Explorer",
        "tip.toggle_explorer": "Show or hide the Explorer (Ctrl+1)",
        "tip.toggle_explorer_show": "Show the Explorer (Ctrl+1)",
        "tip.toggle_explorer_hide": "Hide the Explorer (Ctrl+1)",
        "action.toggle_inspector": "Inspector",
        "tip.toggle_inspector": "Show or hide the Inspector (Ctrl+2)",
        "tip.toggle_inspector_show": "Show the Inspector (Ctrl+2)",
        "tip.toggle_inspector_hide": "Hide the Inspector (Ctrl+2)",
        "action.toggle_timeline": "Timeline",
        "tip.toggle_timeline": "Show or hide the Timeline (Ctrl+3)",
        "tip.toggle_timeline_show": "Show the Timeline (Ctrl+3)",
        "tip.toggle_timeline_hide": "Hide the Timeline (Ctrl+3)",
        "action.toggle_comparator": "Solution comparator",
        "tip.toggle_comparator": "Show or hide the solution comparator (Ctrl+4)",
        "tip.toggle_comparator_show": "Show the solution comparator (Ctrl+4)",
        "tip.toggle_comparator_hide": "Hide the solution comparator (Ctrl+4)",
        "status.dock_shown": "{name} visible",
        "status.dock_hidden": "{name} hidden",
        "menu.project": "Project",
        "menu.generate": "Generate",
        "menu.compare": "Compare",
        "menu.export": "Export",
        "menu.help": "Help",
        "menu.recent": "Open recent",
        "action.new_project": "New project",
        "action.new_demo_project": "New demo project",
        "action.new_from_template": "New from template…",
        "action.save_as_template": "Save as template…",
        "action.show_welcome": "Home screen",
        "action.open": "Open…",
        "action.open_recent": "Open",
        "action.save": "Save",
        "action.save_as": "Save as…",
        "action.rename_project": "Rename project…",
        "action.reveal_project_folder": "Open project folder",
        "action.diff_bcproj": "Compare .bcproj revisions…",
        "action.restore_local_revision": "Restore latest local revision…",
        "action.export_revision_backup": "Export revisions backup…",
        "action.add_board": "Add board…",
        "action.add_piece": "Add piece…",
        "action.import_boards_csv": "Import board inventory (CSV/Excel)…",
        "action.import_pieces_csv": "Import pieces (CSV/Excel)…",
        "diff_bcproj.title": "Compare .bcproj revisions",
        "diff_bcproj.intro": (
            "Structural diff (meta, boards, pieces, placements). "
            "Saving keeps a local revision ring (hidden folder next to the "
            ".bcproj). You can restore a ring revision into memory (Save to "
            "write it to disk)."
        ),
        "diff_bcproj.left": "Left (before)",
        "diff_bcproj.right": "Right (after)",
        "diff_bcproj.browse": "Browse…",
        "diff_bcproj.browse_tip": "Choose a .bcproj file on disk",
        "diff_bcproj.use_current": "Use open project as left",
        "diff_bcproj.use_current_right": "Use open project as right",
        "diff_bcproj.revision": "Saved revision (left)",
        "diff_bcproj.revision_none": "— (pick a file)",
        "diff_bcproj.current_project": "(open project)",
        "diff_bcproj.compare": "Compare",
        "diff_bcproj.compare_tip": (
            "Compute the structural diff between left and right"
        ),
        "diff_bcproj.restore": "Restore this revision…",
        "diff_bcproj.restore_tip": (
            "Load the selected revision into memory (same path; Save to write to disk)"
        ),
        "diff_bcproj.restore_idle": "Pick a revision from the local ring",
        "diff_bcproj.restore_confirm_title": "Restore local revision",
        "diff_bcproj.restore_confirm": (
            "Load revision “{name}” into the open project?\n\n"
            "Inventory in memory will be replaced. The file path stays:\n"
            "{path}\n\n"
            "Unsaved changes are discarded. Use Save to write this revision "
            "to disk (the ring will keep the current file)."
        ),
        "diff_bcproj.restore_error_title": "Could not restore",
        "diff_bcproj.restore_not_in_ring": (
            "Only snapshots from this project’s local revision ring can be restored."
        ),
        "diff_bcproj.placeholder": "Diff output will appear here.",
        "diff_bcproj.open_title": "Open .bcproj",
        "diff_bcproj.file_filter": "BoardComposer projects (*.bcproj);;All (*.*)",
        "diff_bcproj.need_left": "Choose the left .bcproj.",
        "diff_bcproj.need_right": "Choose the right .bcproj.",
        "diff_bcproj.error_title": "Could not compare",
        "status.revision_restored": (
            "Revision “{name}” loaded into memory (pending Save)"
        ),
        "status.revision_restore_no_file": (
            "Save the project before restoring a local revision"
        ),
        "status.revision_restore_empty": (
            "No local revisions yet; save the project at least once more to "
            "create the ring"
        ),
        "status.revision_restore_failed": "Could not restore revision: {error}",
        "action.export_selected": "Export selected solution…",
        "action.export_timeline": "Export Timeline history…",
        "action.exit": "Quit",
        "action.undo": "Undo",
        "action.redo": "Redo",
        "action.rotate_piece": "Rotate 90°",
        "action.rename_selection": "Rename…",
        "action.edit_selection": "Edit…",
        "action.copy_selection_id": "Copy ID",
        "action.duplicate_piece": "Duplicate",
        "action.delete_piece": "Delete",
        "action.select_all_pieces": "Select all pieces",
        "action.deselect_pieces": "Deselect pieces",
        "action.invert_selection": "Invert selection",
        "action.preferences": "Preferences…",
        "action.fit_board": "Fit to board",
        "action.fit_selection": "Fit to selection",
        "action.zoom_in": "Zoom in",
        "action.zoom_out": "Zoom out",
        "action.toggle_grid": "Show grid",
        "action.reset_window_layout": "Reset window layout",
        "action.solve_layout": "Calculate layout",
        "action.previous_solution": "Previous solution",
        "action.next_solution": "Next solution",
        "action.apply_layout": "Apply calculated layout",
        "action.no_recent": "No recent files",
        "action.clear_recent": "Clear recent list",
        "action.whats_new": "What’s new…",
        "dialog.clear_recent_title": "Clear recent",
        "dialog.clear_recent_body": (
            "Clear the list of recent projects?\nFiles on disk are not deleted."
        ),
        "status.recent_cleared": "Recent list cleared",
        "status.recent_removed": "Removed from recent: {path}",
        "status.recent_pinned": "Pinned in recent: {path}",
        "status.recent_unpinned": "Unpinned from recent: {path}",
        "action.explain_solution": "Explain candidate…",
        "action.shortcuts": "Keyboard shortcuts…",
        "action.open_docs": "Documentation…",
        "action.about": "About BoardComposer…",
        "tip.new_project": (
            "Create an empty project (Ctrl+N); asks for name/units and "
            "confirms if there are unsaved changes"
        ),
        "tip.new_demo_project": (
            "Open the sample project with boards, pieces, and placements "
            "(Ctrl+Shift+D); asks to confirm if there are unsaved changes"
        ),
        "tip.new_from_template": (
            "Pick a saved template and create a project "
            "(Ctrl+Shift+N); asks to confirm if there are unsaved changes"
        ),
        "tip.save_as_template": (
            "Save the current project as a template (Ctrl+Shift+M); "
            "asks for a name and, if any, whether to include placements"
        ),
        "tip.show_welcome": (
            "Return to the home screen without closing the project (Ctrl+Shift+H)"
        ),
        "status.already_on_welcome": "You are already on the home screen",
        "tip.open": (
            "Open a .bcproj project (Ctrl+O); remembers the last folder; "
            "asks to confirm if there are unsaved changes"
        ),
        "tip.save": (
            "Save the current project (Ctrl+S); if it has no file yet, "
            "asks for a path (like Save As); if the file exists, stores a ring revision"
        ),
        "tip.save_as": (
            "Save the project under another name or path (Ctrl+Shift+S); "
            "becomes the current file; if the file exists, stores a ring revision; "
            "remembers the last folder"
        ),
        "tip.rename_project": (
            "Rename the current project (Ctrl+Shift+F2); asks for the new name"
        ),
        "tip.reveal_project_folder": "Open the folder that contains the .bcproj file (Ctrl+Shift+R)",
        "tip.status_project_path": ("{path}\nClick to open the folder (Ctrl+Shift+R)"),
        "tip.status_project_unsaved": ("Save the project (Ctrl+S) to open its folder"),
        "tip.diff_bcproj": (
            "Compare two .bcproj revisions or the open project vs a file "
            "(Ctrl+Shift+Y); opens the dialog; can restore a ring revision; "
            "remembers the last folder"
        ),
        "tip.restore_local_revision": (
            "Load the latest local ring revision into memory (Ctrl+Alt+Y); "
            "prompts for confirmation · Save to write to disk"
        ),
        "tip.export_revision_backup": (
            "Copy the .bcproj and .revs/ ring to a backup folder (Ctrl+Alt+B); "
            "offers to open that folder; "
            "remembers the last folder"
        ),
        "status.revision_backup_no_file": (
            "Save the project to disk to export a revisions backup"
        ),
        "status.revision_backup_done": "Revisions backup exported: {path}",
        "status.revision_backup_failed": "Could not export backup: {error}",
        "dialog.export_revision_backup": "Revisions backup folder",
        "tip.add_board": (
            "Add a board to the inventory (Ctrl+Shift+B); "
            "opens the ID and dimensions dialog"
        ),
        "tip.add_piece": (
            "Add a piece to the project (Ctrl+Shift+P); "
            "opens the ID, dimensions, and quantity dialog"
        ),
        "tip.import_boards_csv": (
            "Import board inventory from CSV or Excel (Ctrl+Shift+T); "
            "remembers the last folder; opens column mapping and a preview"
        ),
        "tip.import_pieces_csv": (
            "Import pieces from CSV or Excel (Ctrl+Shift+O); "
            "remembers the last folder; opens column mapping and a preview"
        ),
        "tip.export_selected": (
            "Export the Comparator solution (Ctrl+Shift+E); "
            "opens format options and a preview "
            "(SVG/PNG/JPEG/PDF/DXF/JSON/CSV); "
            "offers to open the file; "
            "remembers the last folder"
        ),
        "tip.export_selected_outdated": (
            "Solutions outdated: when exporting (Ctrl+Shift+E) "
            "prompts to recalculate / export anyway / cancel"
        ),
        "tip.export_timeline": (
            "Export the Timeline history (Ctrl+Shift+L): "
            "JSON or CSV matching current filters; "
            "offers to open the file; "
            "remembers the last folder"
        ),
        "tip.exit": (
            "Quit BoardComposer Studio (Ctrl+Q); "
            "asks to confirm if there are unsaved changes"
        ),
        "tip.undo": "Undo the last action (Ctrl+Z)",
        "tip.redo": "Redo the last undone action (Ctrl+Shift+Z)",
        "tip.rotate_piece": (
            "Rotate the selected piece by 90° (R); the piece must be placed on a board"
        ),
        "tip.rename_selection": (
            "Rename the selected piece, board, or project (F2); "
            "asks for the new name or ID"
        ),
        "tip.edit_selection": (
            "Edit the selected piece or board (Return); "
            "opens the ID and dimensions dialog"
        ),
        "tip.copy_selection_id": (
            "Copy the piece or board ID to the clipboard (Ctrl+Shift+C): "
            "Explorer, single selection, or focused board"
        ),
        "tip.duplicate_piece": (
            "Duplicate the selected piece or board (Ctrl+D); assigns a unique ID"
        ),
        "tip.delete_piece": (
            "Delete the selected piece or board (Backspace or Delete); "
            "asks for confirmation"
        ),
        "tip.select_all_pieces": "Select every piece on the canvas (Ctrl+A)",
        "tip.deselect_pieces": "Clear the piece selection on the canvas (Escape)",
        "tip.invert_selection": "Invert the piece selection on the canvas (Ctrl+Shift+I)",
        "tip.preferences": (
            "Open global preferences: language, theme, units, grid, "
            "algorithms, and export (Ctrl+,); applied when you accept"
        ),
        "status.pieces_selected": "{n} pieces selected",
        "status.no_pieces_to_select": "No pieces to select",
        "status.nothing_to_deselect": "No pieces are selected",
        "status.selection_cleared": "Selection cleared",
        "status.nothing_to_fit_selection": ("Select a piece or board to fit the view"),
        "status.nothing_to_fit_board": "No boards to fit the view",
        "tip.fit_board": "Zoom to fit all boards (Ctrl+0); ignores the selection",
        "tip.fit_selection": (
            "Zoom to fit the selected pieces or the focused board (Ctrl+Shift+0)"
        ),
        "tip.zoom_in": "Zoom in on the Workspace (wheel, Ctrl+=)",
        "tip.zoom_out": "Zoom out on the Workspace (wheel, Ctrl+-)",
        "status.zoom_at_maximum": "Already at maximum zoom",
        "status.zoom_at_minimum": "Already at minimum zoom",
        "tip.toggle_grid": "Show or hide the canvas grid (Ctrl+G)",
        "tip.toggle_grid_show": "Show the canvas grid (Ctrl+G)",
        "tip.toggle_grid_hide": "Hide the canvas grid (Ctrl+G)",
        "status.grid_shown": "Grid visible",
        "status.grid_hidden": "Grid hidden",
        "tip.reset_window_layout": (
            "Restore the default dock, toolbar and window size layout "
            "(Ctrl+Shift+W); saves that layout"
        ),
        "status.window_layout_reset": "Window layout reset",
        "tip.solve_layout": (
            "Calculate layout solutions (Ctrl+Return); needs board and piece inventory"
        ),
        "tip.solve_layout_outdated": (
            "Solutions outdated: recalculate now (Ctrl+Return)"
        ),
        "tip.previous_solution": "Select the previous solution (Page Up)",
        "tip.previous_solution_outdated": (
            "Solutions outdated: browsing stale candidates (Page Up); "
            "recalculate via the Comparator banner CTA or Ctrl+Return"
        ),
        "tip.next_solution": "Select the next solution (Page Down)",
        "tip.next_solution_outdated": (
            "Solutions outdated: browsing stale candidates (Page Down); "
            "recalculate via the Comparator banner CTA or Ctrl+Return"
        ),
        "tip.apply_layout": (
            "Apply the selected solution to the project (Ctrl+Shift+Return); "
            "replaces current placements"
        ),
        "tip.apply_layout_outdated": (
            "Solutions outdated: when applying (Ctrl+Shift+Return) "
            "prompts to recalculate / apply anyway / cancel"
        ),
        "tip.whats_new": (
            "Show recent CHANGELOG highlights in a dialog (Ctrl+Shift+U)"
        ),
        "tip.explain_solution": (
            "Show strengths, weaknesses, and notes for the selected candidate "
            "(Ctrl+Alt+E); Copy is available in the dialog"
        ),
        "tip.explain_solution_outdated": (
            "Solutions outdated: explanation describes the stale candidate; "
            "recalculate via the Comparator banner CTA or Ctrl+Return "
            "(Ctrl+Alt+E)"
        ),
        "help.explain_solution_title": "Explain candidate",
        "help.explain_solution_heading": (
            "Deterministic explanation (no cloud AI). IDE-0007 MVP."
        ),
        "help.explain_solution_outdated_heading": (
            "Solutions outdated: this explanation describes the candidate "
            "computed before the project edit. "
            "Deterministic explanation (no cloud AI). IDE-0007 MVP."
        ),
        "help.explain_strengths": "Strengths",
        "help.explain_weaknesses": "Weaknesses",
        "help.explain_notes": "Notes",
        "help.explain_empty": "No explanation available for this candidate.",
        "help.explain_copy": "Copy",
        "tip.explain_copy": "Copy the full explanation to the clipboard",
        "status.explain_copied": "Explanation copied to the clipboard",
        "tip.shortcuts": (
            "Open the active shortcuts dialog (F1); includes contextual Timeline rows"
        ),
        "tip.open_docs": (
            "Open the local end-user quick guide in the system app (Shift+F1)"
        ),
        "tip.about": (
            "Open About with the BoardComposer Studio version (Ctrl+Shift+A)"
        ),
        "tip.clear_recent": (
            "Clear the list of recent projects (Ctrl+Shift+X); "
            "asks for confirmation (does not delete files on disk)"
        ),
        "tip.remove_recent": (
            "Remove this project from the list (Delete or Backspace); "
            "does not delete the file on disk"
        ),
        "tip.pin_recent": "Pin this project to the top of the recent list",
        "tip.unpin_recent": "Unpin this recent project",
        "tip.reveal_recent": "Show the .bcproj file in the file manager",
        "tip.recent_row": (
            "{path}\nClick opens; asks to confirm unsaved changes · "
            "menu: pin / Show in folder / remove"
        ),
        "tip.recent_row_pinned": (
            "{path}\nClick opens; asks to confirm unsaved changes · "
            "menu: unpin / Show in folder / remove"
        ),
        "tip.recent_menu": "{path} — Open · pin · folder · remove",
        "tip.recent_menu_pinned": ("{path} (pinned) — Open · unpin · folder · remove"),
        "tip.recent_menu_open": (
            "Open {path}; asks to confirm if there are unsaved changes"
        ),
        "tip.recent_menu_pin": "Pin {path} to the top of recent projects",
        "tip.recent_menu_unpin": "Unpin {path}",
        "tip.recent_menu_reveal": "Show {path} in the file manager",
        "tip.recent_menu_remove": (
            "Remove {path} from recent projects; does not delete the file on disk"
        ),
        "help.whats_new_title": "What’s new",
        "help.whats_new_heading": "Recent changes ({section})",
        "help.whats_new_unavailable": "No release notes available.",
        "help.whats_new_read_error": "Could not read CHANGELOG.md.",
        "help.whats_new_see_changelog": (
            "See CHANGELOG.md for the full version details."
        ),
        "help.about_title": "About",
        "help.about_version": "Version {version}",
        "help.about_blurb": (
            "Studio for optimizing board cutting. "
            "See the local documentation and the repository CHANGELOG."
        ),
        "help.shortcuts_title": "Keyboard shortcuts",
        "help.shortcuts_intro": (
            "Active shortcuts in BoardComposer Studio. "
            "The same bindings apply from the menu and the keyboard. "
            "On macOS, ⌘ (Command) is the primary modifier "
            "(not the Control ⌃ key). "
            "In the Workspace: Space+drag, middle or right button to pan; "
            "arrow keys (Shift = grid size) to nudge a piece; "
            "mouse wheel to zoom. "
            "In the Timeline (list focused): Space play/pause, Home "
            "restarts, ← / → step; Ctrl+C copies the event line."
        ),
        "help.shortcuts_col_action": "Action",
        "help.shortcuts_col_keys": "Shortcut",
        "action.timeline_replay_play": "Timeline — Play / Pause (list focused)",
        "action.timeline_replay_reset": "Timeline — Restart replay (list focused)",
        "action.timeline_replay_back": "Timeline — Step back (list focused)",
        "action.timeline_replay_forward": ("Timeline — Step forward (list focused)"),
        "action.timeline_copy_line": ("Timeline — Copy event line (list focused)"),
        "help.docs_missing": "Documentation not found at:\n{path}",
        "status.docs_opened": "Quick guide opened",
        "dock.explorer": "Explorer",
        "dock.inspector": "Inspector",
        "dock.timeline": "Timeline",
        "dock.comparator": "Solution comparator",
        "timeline.placeholder": "Timeline / Console / Events",
        "timeline.filter": "Filter:",
        "timeline.filter_all": "All events",
        "timeline.filter_algorithm": "Algorithm:",
        "timeline.filter_algorithm_all": "All algorithms",
        "timeline.filter_period": "Period:",
        "timeline.filter_period_all": "Full history",
        "timeline.filter_period_1m": "Last minute",
        "timeline.filter_period_5m": "Last 5 min",
        "timeline.filter_period_15m": "Last 15 min",
        "timeline.filter_period_1h": "Last hour",
        "timeline.filter_piece_moves": "Only moves",
        "timeline.filter_markers": "Only markers",
        "timeline.follow_latest": "Follow",
        "timeline.clear_filters": "Clear filters",
        "timeline.count_empty": "0 events",
        "timeline.count_all": "{n} events",
        "timeline.count_filtered": "{visible} of {total} events",
        "timeline.detail.duration_ms": "{n} ms",
        "timeline.clear": "Clear",
        "timeline.clear_confirm_title": "Clear Timeline",
        "timeline.clear_confirm": (
            "Clear the Timeline history ({n} events)? This cannot be undone."
        ),
        "timeline.copy_line": "Copy line",
        "timeline.copy_payload": "Copy payload JSON",
        "status.timeline_copied": "Timeline event copied to clipboard",
        "tip.timeline_clear": ("Clear the Timeline history (asks for confirmation)"),
        "tip.timeline_clear_filters": "Clear event, algorithm, and period filters",
        "tip.timeline_follow": "Keep the view on the latest Timeline event",
        "tip.timeline_filter_piece_moves": (
            "Show only piece moves (turn off = all events)"
        ),
        "tip.timeline_filter_markers": ("Show only markers (turn off = all events)"),
        "tip.timeline_filter_event": "Limit the history to one event type",
        "tip.timeline_filter_algorithm": ("Show only events from one solve algorithm"),
        "tip.timeline_filter_period": "Limit the history to a recent period",
        "tip.timeline_replay_mode": ("Replay solution placements or solver phases"),
        "tip.timeline_replay_speed": ("Speed of automatic Timeline replay"),
        "tip.timeline_list": (
            "List focused: Space play/pause, Home, ← / →, "
            "Ctrl+C copies the line; context menu = JSON payload"
        ),
        "tip.timeline_copy_line": "Copy the visible event line (Ctrl+C)",
        "tip.timeline_copy_payload": "Copy the event JSON payload",
        "status.timeline_clear_filters_idle": "No filters active",
        "status.timeline_filters_cleared": "Timeline filters cleared",
        "tip.timeline_replay_reset": "Restart replay (Home)",
        "tip.timeline_replay_back": "Step back (←)",
        "tip.timeline_replay_forward": "Step forward (→)",
        "tip.timeline_replay_play": "Play / Pause (Space)",
        "status.timeline_replay_idle": (
            "Calculate a layout to replay the solution in the Timeline"
        ),
        "tip.timeline_mark": (
            "Add a marker with a note (dialog); optional step/algorithm "
            "from the active replay"
        ),
        "timeline.export": "Export…",
        "timeline.mark": "Marker…",
        "timeline.mark_dialog_title": "Add marker",
        "timeline.mark_dialog_label": "Note:",
        "timeline.detail.step": "step {n}",
        "dialog.export_timeline": "Export Timeline history",
        "dialog.filter_timeline": "JSON (*.json);;CSV (*.csv)",
        "status.timeline_exported": "Timeline history exported: {path}",
        "status.timeline_export_empty": ("No Timeline events to export"),
        "status.timeline_clear_empty": ("No Timeline events to clear"),
        "status.timeline_export_failed": "Could not export Timeline: {error}",
        "timeline.empty": "No events yet. Studio actions will appear here.",
        "timeline.detail.count": "{n} item(s)",
        "timeline.detail.index": "#{n}",
        "timeline.event.ProjectCreated": "Project created",
        "timeline.event.ProjectModified": "Project modified",
        "timeline.event.ProjectSaved": "Project saved",
        "timeline.event.ProjectOpened": "Project opened",
        "timeline.event.CsvImported": "CSV imported",
        "timeline.event.PieceMoved": "Piece moved",
        "timeline.event.SolutionGenerationStarted": "Solve started",
        "timeline.event.SolutionGenerated": "Solve finished",
        "timeline.event.SolutionSelected": "Solution selected",
        "timeline.event.SolutionsMarkedOutdated": "Solutions marked outdated",
        "timeline.event.ExportCompleted": "Export completed",
        "timeline.event.WorkspaceUpdated": "Workspace updated",
        "timeline.event.TimelineMarked": "Marker",
        "comparator.solutions_outdated": (
            "Outdated solutions: the project changed. "
            "Regenerate the layout to refresh them."
        ),
        "comparator.recalculate_layout": "Calculate layout",
        "inspector.solutions_outdated": (
            "⚠ Solutions pending regeneration (project modified)."
        ),
        "status.solutions_outdated": "Solutions marked as outdated",
        "dialog.outdated_solutions_title": "Outdated solutions",
        "dialog.outdated_solutions_apply": (
            "Solutions no longer match the current project. "
            "Recalculating is the safe option; apply uses the stale candidate."
        ),
        "dialog.outdated_solutions_apply_anyway": "Apply anyway",
        "dialog.outdated_solutions_export": (
            "Solutions no longer match the current project. "
            "Recalculating is the safe option; export uses the stale candidate."
        ),
        "dialog.outdated_solutions_export_anyway": "Export anyway",
        "timeline.replay_none": "Replay: no solution",
        "timeline.replay_mode": "Mode:",
        "timeline.replay_mode_placements": "Placements",
        "timeline.replay_mode_phases": "Solver phases",
        "timeline.replay_speed": "Speed:",
        "timeline.replay_speed_slow": "Slow",
        "timeline.replay_speed_normal": "Normal",
        "timeline.replay_speed_fast": "Fast",
        "timeline.phase_none": "No phase trace. Calculate a layout first.",
        "timeline.phase_progress_idle": "Phases · 0/{total}",
        "timeline.phase_progress": "{kind} · {current}/{total}",
        "timeline.phase_progress_algo": ("{kind} · {algorithm} · {current}/{total}"),
        "timeline.phase_idle_detail": "start",
        "timeline.phase.generator_started": "Algorithm start",
        "timeline.phase.generator_finished": "Algorithm end",
        "timeline.phase.placement_failures_summary": "Failures summary",
        "timeline.phase.placement_failed": "Placement failure",
        "timeline.phase.evaluation_started": "Evaluation start",
        "timeline.phase.evaluation_finished": "Evaluation end",
        "timeline.phase.build_order": "Build order",
        "timeline.phase.cancelled": "Cancelled",
        "timeline.replay_progress": "Replay: {current}/{total} pieces",
        "timeline.replay_progress_algo": (
            "Algorithm {algorithm} · {current}/{total} pieces"
        ),
        "timeline.replay_progress_algo_piece": (
            "Algorithm {algorithm} · {piece} · {current}/{total}"
        ),
        "timeline.replay_algorithm_unknown": "unknown",
        "timeline.detail.accepted": "accepted {n}",
        "timeline.detail.rejected": "rejected {n}",
        "timeline.detail.total": "total {n}",
        "timeline.detail.no_fit": "no fit {n}",
        "timeline.detail.incompatible": "incompatible {n}",
        "timeline.reason.incompatible": "incompatible material/thickness",
        "timeline.reason.no_fit": "no fit",
        "timeline.event.AlgorithmStarted": "Algorithm started",
        "timeline.event.AlgorithmFinished": "Algorithm finished",
        "timeline.event.EvaluationFinished": "Evaluation finished",
        "timeline.event.PlacementFailed": "Placement failed",
        "timeline.event.PlacementFailuresSummary": "Placement failures summary",
        "timeline.replay_reset": "Start",
        "timeline.replay_back": "◀",
        "timeline.replay_forward": "▶",
        "timeline.replay_play": "Play",
        "timeline.replay_pause": "Pause",
        "status.timeline_replay": "Replay {current}/{total}",
        "status.timeline_phase": "Phase {current}/{total}: {detail}",
        "status.timeline_seek": "Timeline: {detail}",
        "explorer.boards": "Boards ({n})",
        "explorer.pieces": "Pieces ({n})",
        "explorer.solutions": "Solutions ({n})",
        "explorer.units": "pcs",
        "explorer.solution": "Solution {n} — {pieces} pieces — {waste} gaps",
        "explorer.context.rename": "Rename…",
        "explorer.context.reveal_folder": "Open folder…",
        "explorer.context.edit": "Edit…",
        "explorer.context.duplicate": "Duplicate",
        "explorer.context.copy_id": "Copy ID",
        "explorer.context.delete": "Delete",
        "explorer.context.add_board": "Add board…",
        "explorer.context.add_piece": "Add piece…",
        "explorer.context.preview_solution": "Preview",
        "explorer.context.place_on_board": "Place on focused board",
        "tip.preview_solution": (
            "Show the solution in the Workspace without applying it; "
            "to keep it use Apply layout (Ctrl+Shift+Return)"
        ),
        "tip.preview_solution_outdated": (
            "Solutions outdated: preview shows a stale candidate; "
            "recalculate via the Comparator banner CTA or Ctrl+Return"
        ),
        "explorer.unplaced_mark": "unplaced",
        "inspector.title": "Inspector",
        "inspector.none": "No selection",
        "inspector.board": "Board",
        "inspector.piece": "Piece",
        "inspector.dimensions": "Dimensions",
        "inspector.thickness": "Thickness",
        "inspector.quantity": "Quantity",
        "inspector.material": "Material",
        "inspector.position": "Position",
        "inspector.unplaced": "Not placed in the Workspace",
        "inspector.place_hint": (
            "Tip: focus a board in the Explorer, then use "
            "“Place on focused board” (or double-click)."
        ),
        "inspector.no_panel": "No board assigned",
        "inspector.panel_instance": "{board} · instance {instance}/{quantity}",
        "inspector.layout_title": "Calculated layout",
        "inspector.solution": "Solution: {current} / {total}",
        "inspector.strategy": "Strategy: {name}",
        "inspector.placed": "Pieces placed: {n}",
        "inspector.total_length": "Total length: {value} mm",
        "inspector.total_width": "Total width: {value} mm",
        "inspector.internal_waste": "Internal gaps: {value}",
        "inspector.free_material": "Free material: {value}",
        "inspector.omitted": "Omitted pieces: {ids}",
        "inspector.offcuts": ("Usable offcuts: {n} (total area {area} mm²)"),
        "inspector.highlights": "Key points: {items}",
        "inspector.no_solution": "No solution",
        "inspector.layout_cancelled": "Calculation cancelled",
        "inspector.strategy_unknown": "unknown",
        "comparator.pieces": "Pieces",
        "comparator.waste": "Gaps",
        "comparator.board_free": "Free board",
        "comparator.length": "Length",
        "comparator.width": "Width",
        "comparator.score": "Score",
        "comparator.sort_by": "Sort by:",
        "comparator.complete_only": "Complete solutions only",
        "comparator.pin_reference": "Pin as reference",
        "tip.pin_reference": (
            "Pin the selected candidate as the diff reference (needs ≥2 solutions)"
        ),
        "tip.pin_reference_outdated": (
            "Solutions outdated: the diff uses stale candidates; "
            "recalculate via the Comparator banner CTA or Ctrl+Return"
        ),
        "tip.comparator_sort": (
            "Sort candidates by solver ranking, pieces, gaps, free board, or score "
            "(this session only)"
        ),
        "tip.comparator_complete_only": (
            "Show only complete candidates (no omitted pieces); "
            "turn off = include partial ones too"
        ),
        "comparator.reference_mark": "Ref {n}",
        "comparator.reference_thumb": "#{n} · ref",
        "comparator.reference_tooltip": "Pinned reference (solution {n})",
        "comparator.diff_title": "Differences vs reference",
        "comparator.diff_placeholder": (
            "Differences relative to the reference solution"
        ),
        "comparator.best_in": "Best at: {items}",
        "comparator.unplaced_suffix": " ({n} unplaced)",
        "sort.ranking": "Solver order",
        "sort.pieces": "Pieces placed",
        "sort.waste": "Internal gaps",
        "sort.board_waste": "Free board",
        "sort.score": "Score",
        "highlight.pieces": "Pieces placed",
        "highlight.waste": "Fewer internal gaps",
        "highlight.score": "Best score",
        "highlight.board_free": "Less free board",
        "highlight.length": "Shorter length",
        "highlight.width": "Narrower width",
        "diag.title": "Solver diagnosis",
        "diag.cancelled": "Cancelled by the user",
        "diag.generated": "Candidates generated: {n}",
        "diag.unique": "Unique candidates: {n}",
        "diag.accepted": "Accepted: {n}",
        "diag.rejected": "Rejected: {n}",
        "diag.reasons": "Rejection reasons:",
        "diag.missing_board": "Omitted pieces",
        "diag.duplicate_board": "Duplicate pieces",
        "diag.unknown_board": "Unknown pieces",
        "diag.overlap": "Overlaps",
        "diag.exceeds_constraints": "Outside board",
        "diag.unassigned_stock_panel": "No board assigned",
        "diag.unknown_stock_panel": "Unknown board",
        "diag.exceeds_stock_panel": "Outside physical board",
        "diag.panel_thickness_mismatch": "Incompatible thickness",
        "diag.panel_material_mismatch": "Incompatible material",
        "workspace.empty_title": "Start your project",
        "workspace.empty_blurb": (
            "Add boards and pieces, or import them from CSV/Excel to begin composing."
        ),
        "status.ready": "BoardComposer Studio ready",
        "status.project_unsaved": "Project not saved yet",
        "status.zoom": "{n}%",
        "tip.zoom_status": ("Workspace zoom level (wheel, Ctrl+= / Ctrl+-, Ctrl+0)"),
        "status.project_folder_unavailable": "Save the project to open its folder",
        "status.project_folder_failed": "Could not open the project folder",
        "status.project_folder_opened": "Project folder opened",
        "status.welcome": "Home screen",
        "status.new_empty": "Empty project created",
        "status.new_project_created": "Project “{name}” created",
        "project.untitled": "Untitled project",
        "status.demo_created": "Demo project created — Ctrl+Return computes several candidates",
        "status.demo_created_max_solutions_raised": (
            "Demo project created — Max solutions was 1; restored to {n} "
            "for the Comparator (Ctrl+Return)"
        ),
        "status.template_saved": "Template “{name}” saved",
        "status.template_loaded": "Project created from “{name}”",
        "status.template_empty": "No project templates saved yet",
        "status.template_missing_project": "No open project to save as a template",
        "template.pick_title": "New from template",
        "template.pick_intro": (
            "Choose a template. A new project will be created with its boards "
            "and pieces; if it stores placements, you can restore them."
        ),
        "template.pick_item": "{name} — {boards} board(s), {pieces} piece(s)",
        "template.pick_item_with_placements": (
            "{name} — {boards} board(s), {pieces} piece(s), {placements} placement(s)"
        ),
        "template.load_placements": "Also restore the template placements?",
        "template.rename": "Rename…",
        "template.rename_title": "Rename template",
        "template.rename_prompt": "New name:",
        "template.rename_failed": "Could not rename to “{name}”.",
        "template.delete": "Delete…",
        "template.delete_title": "Delete template",
        "template.delete_confirm": "Delete template “{name}”?",
        "template.delete_failed": "Could not delete “{name}”.",
        "template.save_title": "Save as template",
        "template.save_prompt": "Template name:",
        "template.save_placements": "Also include the current placements?",
        "template.empty_name": "Template name cannot be empty.",
        "status.board_id_exists": "A board with id {id} already exists",
        "status.board_id_empty": "The board id cannot be empty",
        "status.board_added": "Board added",
        "status.boards_imported": "{n} board(s) imported",
        "status.pieces_imported": "{n} piece(s) imported",
        "status.import_template_applied": "Mapping applied from template “{name}”",
        "status.import_template_saved": "Import template “{name}” saved",
        "status.piece_id_empty": "The piece id cannot be empty",
        "status.piece_id_exists": "A piece with id {id} already exists",
        "status.pieces_added": "{n} pieces added",
        "status.piece_added": "Piece added",
        "status.piece_duplicated": "Piece duplicated: {id}",
        "status.board_duplicated": "Board duplicated: {id}",
        "status.id_copied": "ID copied: {id}",
        "status.select_piece_first": "Select a piece first",
        "status.place_piece_before_rotate": (
            "Place the piece on a board before rotating it"
        ),
        "status.nothing_to_duplicate": "Select a piece or board to duplicate",
        "status.nothing_to_delete": "Select a piece or board to delete",
        "status.cannot_rotate": "The piece cannot be rotated in that position",
        "status.piece_rotated": "Piece rotated 90°",
        "status.piece_placed": "Piece {piece} placed on {board}",
        "status.piece_already_placed": "Piece {id} is already placed",
        "status.place_needs_board_focus": (
            "Select a board in the Explorer to place the piece"
        ),
        "status.place_piece_missing": "Piece “{id}” was not found",
        "status.place_board_missing": "Board “{id}” was not found",
        "status.rename_unchanged": "Name unchanged",
        "status.edit_unchanged": "No changes to apply",
        "status.place_no_space": "{piece} does not fit on {board}",
        "status.place_incompatible_thickness": (
            "Incompatible thickness: {piece} ({piece_thickness}) ≠ "
            "{board} ({board_thickness}). Edit the piece or board."
        ),
        "status.place_incompatible_material": (
            "Incompatible material: {piece} (“{piece_material}”) ≠ "
            "{board} (“{board_material}”). Edit the piece or board."
        ),
        "status.place_incompatible_both": (
            "Incompatible material/thickness: {piece} "
            "({piece_thickness}, “{piece_material}”) ≠ {board} "
            "({board_thickness}, “{board_material}”)."
        ),
        "status.prefs_saved": "Preferences saved",
        "status.nothing_to_solve": "No project to calculate layout",
        "status.solve_needs_inventory": (
            "Add at least one board and one piece before calculating layout"
        ),
        "status.solve_needs_boards": (
            "Add at least one board before calculating layout"
        ),
        "status.solve_needs_pieces": (
            "Add at least one piece before calculating layout"
        ),
        "status.layout_failed": "Could not calculate layout",
        "status.layout_partial": "Partial layout: {omitted} unplaced piece(s) across {total} solutions",
        "status.layout_ok": (
            "Layout calculated: {n} solutions — Page Up/Down · "
            "Pin reference · Export Ctrl+Shift+E"
        ),
        "status.layout_ok_single": (
            "Layout calculated: 1 unique candidate (no more distinct ones; "
            "generated {generated}, unique {unique}). "
            "Multiple candidates: demo Ctrl+Shift+D → Calculate · Export Ctrl+Shift+E"
        ),
        "status.layout_truncated_by_limit": (
            "Showing {shown}/{accepted} solutions (Preferences limit: {limit}). "
            "Page Up/Down browse the visible ones."
        ),
        "status.layout_computing": "Calculating layout…",
        "status.layout_cancelled": "Layout calculation cancelled",
        "status.layout_error": "Layout calculation error: {error}",
        "progress.layout_title": "Generate solutions",
        "progress.layout_label": "Running packing algorithms…",
        "progress.layout_cancel": "Cancel",
        "status.select_solution_first": "Select a solution first",
        "status.reference_pinned": "Reference pinned to solution #{n}",
        "status.calculate_layout_first": (
            "Calculate a layout first (Ctrl+Return). "
            "Then Export (Ctrl+Shift+E) or Apply (Ctrl+Shift+Return)"
        ),
        "status.solution_applied": "Solution {current}/{total} applied to the project",
        "status.no_solutions": "No calculated solutions",
        "status.no_solutions_match_filter": (
            "No candidates match the Comparator filter "
            "(clear “complete only” or change the sort)"
        ),
        "status.only_one_visible_solution": (
            "Only 1 visible candidate — Page Up / Page Down have nowhere else to go"
        ),
        "status.only_one_visible_truncated": (
            "Only 1 visible of {accepted} accepted (Preferences limit: {limit}). "
            "Raise “Max solutions” to browse more with Page Up/Down"
        ),
        "status.previewing_solution": "Previewing solution {current}/{total}. Press 'Apply calculated layout' to keep it.",
        "status.export_failed": "Could not export {format}: {error}",
        "status.exported": "{format} exported: {path}",
        "status.export_open_failed": "Could not open the file: {path}",
        "status.export_reveal_failed": "Could not open the folder for: {path}",
        "status.nothing_to_undo": "No actions to undo",
        "status.nothing_to_redo": "No actions to redo",
        "status.undone": "Undone",
        "status.redone": "Redone",
        "status.nothing_to_save": "No project to save",
        "status.nothing_to_rename": "No project to rename",
        "status.nothing_to_rename_selection": (
            "Select a piece, board, or the project to rename"
        ),
        "status.nothing_to_edit_selection": "Select a piece or board to edit",
        "status.nothing_to_copy_id": "Select a piece or board to copy its ID",
        "status.no_recent_to_clear": "No recent projects to clear",
        "status.save_failed": "Could not save: {error}",
        "status.project_renamed": "Project renamed: {name}",
        "status.piece_renamed": "Piece renamed: {id}",
        "status.board_renamed": "Board renamed: {id}",
        "status.project_saved": "Project saved: {path}",
        "status.project_saved_with_revision": (
            "Project saved: {path} (previous revision: {revision})"
        ),
        "status.project_opened": "Project opened: {path}",
        "status.board_updated": "Board updated",
        "status.board_deleted": "Board deleted: {id}",
        "status.piece_deleted": "Piece deleted: {id}",
        "status.piece_updated": "Piece updated",
        "dialog.open_project": "Open project",
        "dialog.save_project": "Save project",
        "dialog.unsaved_title": "Unsaved changes",
        "dialog.unsaved_body": (
            "The project “{name}” has unsaved changes.\n"
            "{location}\n\n"
            "Do you want to save them before continuing?"
        ),
        "dialog.unsaved_unnamed": "Untitled",
        "dialog.unsaved_location_file": "File: {path}",
        "dialog.unsaved_location_new": "It has not been saved to a file yet.",
        "dialog.unsaved_save": "Save",
        "dialog.unsaved_discard": "Discard",
        "dialog.unsaved_cancel": "Cancel",
        "dialog.save_failed_title": "Could not save",
        "dialog.import_boards": "Import board inventory (CSV/Excel)",
        "dialog.import_boards_short": "Import board inventory",
        "dialog.import_pieces": "Import pieces (CSV/Excel)",
        "dialog.import_pieces_short": "Import pieces",
        "dialog.export_selected": "Export selected solution",
        "dialog.filter_csv_excel": "CSV / Excel (*.csv *.xlsx);;CSV (*.csv);;Excel (*.xlsx);;All files (*)",
        "dialog.filter_bcproj": "BoardComposer Project (*.bcproj)",
        "dialog.edit_board": "Edit board",
        "dialog.edit_piece": "Edit piece",
        "dialog.rename_project_title": "Rename project",
        "dialog.rename_piece_title": "Rename piece",
        "dialog.rename_board_title": "Rename board",
        "dialog.delete_board_title": "Delete board",
        "dialog.delete_board_confirm": "Delete board “{id}”?",
        "dialog.delete_board_confirm_placements": (
            "Delete board “{id}”?\n\n"
            "{n} placement(s) on that board will be removed; pieces are kept."
        ),
        "dialog.delete_piece_title": "Delete piece",
        "dialog.delete_piece_confirm": "Delete piece “{id}”?",
        "dialog.delete_piece_confirm_placed": (
            "Delete piece “{id}”?\n\n"
            "Its placement on the Workspace will also be removed."
        ),
        "export.title": "Export solution",
        "export.intro": "Choose the format and content. The preview reflects the selected options.",
        "export.template": "Template:",
        "export.no_template": "(no template)",
        "export.save": "Save…",
        "export.delete": "Delete",
        "tip.export_save_template": (
            "Save the current options as an export template; asks for the name"
        ),
        "tip.export_delete_template": (
            "Delete the selected export template; asks for confirmation"
        ),
        "tip.export_share_export": (
            "Export the template catalog to a JSON pack; "
            "respects the current client filter; "
            "remembers the last folder"
        ),
        "tip.export_share_import": (
            "Import an export-templates pack; remembers the last folder; "
            "asks to merge or replace the catalog"
        ),
        "export.format": "Format:",
        "export.metrics": "Include metrics (JSON)",
        "export.explanation": "Include explanation (JSON)",
        "export.offcuts": "Include offcuts",
        "export.graphic": "Graphic preview",
        "export.summary": "Summary / content",
        "export.export_btn": "Export…",
        "export.save_template_title": "Save template",
        "export.save_template_prompt": "Template name:",
        "export.empty_name": "The template name cannot be empty.",
        "export.delete_title": "Delete template",
        "export.delete_confirm": "Delete template “{name}”?",
        "export.no_preview": "No preview",
        "export.client": "Client:",
        "export.client_all": "(all clients)",
        "export.client_general": "(general)",
        "export.client_prompt": "Client (optional):",
        "export.share_export": "Export pack…",
        "export.share_import": "Import pack…",
        "export.share_export_title": "Export templates",
        "export.share_import_title": "Import templates",
        "export.share_filter": "BoardComposer templates (*.json)",
        "export.share_export_done": "Exported {count} template(s).",
        "export.share_import_mode": (
            "Merge with existing templates?\n\n"
            "Yes = merge (overwrite same client+name)\n"
            "No = replace the whole catalog\n"
            "Cancel = do not import"
        ),
        "export.share_import_done": (
            "Imported {imported} template(s) ({mode}). Current catalog: {total}."
        ),
        "export.share_mode_merge": "merge",
        "export.share_mode_replace": "replace",
        "export.share_error": "Could not complete the operation:\n{error}",
        "export.done_title": "Export completed",
        "export.done_message": "File saved:\n{path}",
        "export.done_message_folder": "Folder created:\n{path}",
        "export.open_file": "Open file",
        "export.open_folder": "Open folder",
        "export.reveal_folder": "Show in folder",
        "import.boards_title": "Import board inventory (CSV)",
        "import.pieces_title": "Import pieces (CSV)",
        "import.file_error_header": "Could not process the file:",
        "import.file_failed": "The file could not be imported.",
        "import.boards_summary": "{valid} valid board(s), {invalid} row(s) with errors.",
        "import.pieces_summary": "{pieces} valid piece(s) in {rows} row(s); {invalid} row(s) with errors.",
        "import.col.row": "Row",
        "import.col.id": "Id",
        "import.col.base_id": "Base id",
        "import.col.quantity": "Quantity",
        "import.col.generated_ids": "Generated ids",
        "import.col.length": "Length",
        "import.col.width": "Width",
        "import.col.thickness": "Thickness",
        "import.col.material": "Material",
        "import.col.status": "Status",
        "import.mapping_title": "Map columns",
        "import.mapping_intro": (
            "Required columns were not recognized ({fields}). "
            "Assign each field to a column from the file:"
        ),
        "import.mapping_none": "(none)",
        "import.mapping_incomplete": ("Required columns are still missing: {fields}"),
        "import.mapping_template": "Template:",
        "import.mapping_delete": "Delete…",
        "tip.import_mapping_delete": (
            "Delete the selected mapping template; prompts for confirmation"
        ),
        "import.mapping_delete_title": "Delete import template",
        "import.mapping_delete_confirm": "Delete template “{name}”?",
        "import.mapping_save_title": "Save import template",
        "import.mapping_save_prompt": (
            "Save this column mapping as a reusable template?"
        ),
        "import.mapping_save_name": "Template name:",
        "import.mapping.field.board_id": "Board id",
        "import.mapping.field.piece_id": "Piece id",
        "import.mapping.field.length_mm": "Length",
        "import.mapping.field.width_mm": "Width",
        "import.mapping.field.thickness_mm": "Thickness",
        "import.mapping.field.quantity": "Quantity",
        "import.mapping.field.material": "Material",
        "import.sheet_title": "Select sheet",
        "import.sheet_label": "Worksheet:",
        "form.new_project": "New project",
        "form.project_name": "Project name:",
        "form.project_name_placeholder": "E.g. Nordik kitchen",
        "dialog.project_name_required": "The project name cannot be empty.",
        "form.new_board": "New board",
        "form.new_piece": "New piece",
        "form.id": "Identifier:",
        "form.length": "Length ({unit}):",
        "form.width": "Width ({unit}):",
        "form.thickness": "Thickness ({unit}):",
        "form.quantity": "Quantity:",
        "form.material": "Material:",
        "form.allow_rotation": "Allow rotation:",
        "diff.title": "Differences",
        "diff.identical": "Solution #{candidate} is identical to reference #{reference}.",
        "diff.header": "Differences of #{candidate} vs reference #{reference}",
        "diff.sync_header": (
            "Synced replay · step {step}/{total} (#{candidate} vs ref. #{reference})"
        ),
        "diff.sync_empty": "No pieces revealed yet. Press ▶ or Play.",
        "diff.sync_same_solution": (
            "Reference is the solution being replayed "
            "({revealed}/{total} pieces visible)."
        ),
        "diff.sync_matched": (
            "Up to step {step}, candidate and reference match on the revealed pieces."
        ),
        "diff.metrics": "Metrics",
        "diff.placements": "Placements",
        "diff.none": "No relevant differences in metrics or placements.",
        "diff.better_here": "  ↑ better here",
        "diff.better_reference": "  ↑ better in reference",
        "diff.need_two": (
            "At least 2 solutions are needed for the diff. "
            "Try demo Ctrl+Shift+D → Calculate layout."
        ),
        "diff.select_solution": "Select a solution in the Comparator.",
        "diff.metric.pieces": "Pieces placed",
        "diff.metric.omitted": "Omitted pieces",
        "diff.metric.waste": "Internal gaps",
        "diff.metric.board_free": "Free material",
        "diff.metric.length": "Total length (mm)",
        "diff.metric.width": "Total width (mm)",
        "diff.metric.panels": "Panels used",
        "diff.metric.offcuts": "Offcuts",
        "diff.metric.score": "Score",
        "diff.metric.completeness": "Completeness",
        "diff.complete": "complete",
        "diff.partial": "partial",
        "diff.no_panel": "no panel",
        "diff.panel": "panel {stock}.{instance}",
        "diff.rotated": " rotated",
        "diff.only_reference": "only in reference ({placement})",
        "diff.only_candidate": "only here ({placement})",
    },
}

_MENU_KEYS = (
    "file",
    "edit",
    "view",
    "project",
    "generate",
    "compare",
    "export",
    "help",
)

_ACTION_KEYS = (
    "new_project",
    "new_demo_project",
    "new_from_template",
    "save_as_template",
    "show_welcome",
    "open",
    "save",
    "save_as",
    "rename_project",
    "reveal_project_folder",
    "diff_bcproj",
    "restore_local_revision",
    "export_revision_backup",
    "add_board",
    "add_piece",
    "import_boards_csv",
    "import_pieces_csv",
    "export_selected",
    "export_timeline",
    "exit",
    "clear_recent",
    "undo",
    "redo",
    "rotate_piece",
    "rename_selection",
    "edit_selection",
    "copy_selection_id",
    "duplicate_piece",
    "delete_piece",
    "select_all_pieces",
    "deselect_pieces",
    "invert_selection",
    "preferences",
    "fit_board",
    "fit_selection",
    "zoom_in",
    "zoom_out",
    "toggle_grid",
    "reset_window_layout",
    "solve_layout",
    "previous_solution",
    "next_solution",
    "apply_layout",
    "whats_new",
    "explain_solution",
    "shortcuts",
    "open_docs",
    "about",
)


def normalize_language(language: str) -> str:
    return language if language in VALID_LANGUAGES else DEFAULT_LANGUAGE


def tr(key: str, language: str = DEFAULT_LANGUAGE, **kwargs: object) -> str:
    """Translate `key` for the selected language, falling back to Spanish."""
    lang = normalize_language(language)
    template = _STRINGS.get(lang, _STRINGS[DEFAULT_LANGUAGE]).get(
        key, _STRINGS[DEFAULT_LANGUAGE].get(key, key)
    )
    if kwargs:
        return template.format(**kwargs)
    return template


def menu_keys() -> tuple[str, ...]:
    return _MENU_KEYS


def action_keys() -> tuple[str, ...]:
    return _ACTION_KEYS
