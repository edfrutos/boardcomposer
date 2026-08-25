# CHANGELOG — BoardComposer

## Unreleased — 0.4.3.dev0 — 2026-08-02

### Añadido

- Docs planificación 2026-08-24: snapshot
  `docs/masterplan/REVIEW-2026-08-24-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto; tips
  #557–#560 mergeados; sin PRs abiertos).
- Docs planificación 2026-08-23: snapshot
  `docs/masterplan/REVIEW-2026-08-23-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto; tips
  Vista docks #554–#556 mergeados; sin PRs abiertos).
- Docs planificación 2026-08-22: snapshot
  `docs/masterplan/REVIEW-2026-08-22-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto; tips
  #548–#552 mergeados; sin PRs abiertos).
- Docs planificación 2026-08-21: snapshot
  `docs/masterplan/REVIEW-2026-08-21-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto; tips
  Timeline #539–#547; PR #548 abierto).
- Docs planificación 2026-08-20: snapshot
  `docs/masterplan/REVIEW-2026-08-20-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto; tips
  #537–#538; PR #539 abierto).
- Docs planificación 2026-08-19: snapshot
  `docs/masterplan/REVIEW-2026-08-19-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto; tips
  #519…#535).
- Docs planificación 2026-08-16: snapshot
  `docs/masterplan/REVIEW-2026-08-16-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto; tips
  #511…#517).
- Docs planificación 2026-08-15: snapshot
  `docs/masterplan/REVIEW-2026-08-15-planificacion.md`; cola IDE-0019…0024
  sin IDE nuevas (Issues abiertos = 0; residuales eval/piloto).
- Barra de estado: clic en el basename abre la carpeta del `.bcproj`
  (mismo flujo que Ctrl+Shift+R); tooltip con ruta + hint.
- Barra de estado: basename del `.bcproj` (tooltip = ruta completa).
- Archivo → Abrir recientes: tips del submenú (anclar / carpeta / quitar)
  incluyen la ruta completa.
- Archivo → Abrir recientes: submenú por proyecto (Abrir / anclar / carpeta /
  quitar); misma gestión que Welcome.
- Tema `system`: secundarios Welcome/empty/Explain sin `min-height`/`padding`
  en QSS (evita pisar alturas polish_* / regresión CI 42px).
- Archivo → Abrir recientes: etiqueta = basename (★ si pin); tip sigue con ruta.
- Archivo → Abrir recientes: statusTip/tooltip con ruta (y «anclado» si pin).
- Welcome: tooltip de fila reciente honesto (ruta + clic abre · menú
  anclar/carpeta/quitar).
- Welcome: menú contextual de recientes → **Mostrar en carpeta** (sin abrir
  el proyecto).
- Welcome: anclar / desanclar proyectos recientes (★ arriba; JSON v2
  `files` + `pinned`).
- Welcome: quitar un reciente (Delete / Backspace / menú contextual).
- Welcome: abrir proyecto reciente con un clic (Enter sigue activo).
- Welcome: CTAs **Atajos…** / **Acerca de…** (fila help; mismos flujos que F1 /
  Ctrl+Shift+A).
- Tras **Exportar backup de revisiones…**, diálogo Abrir / Mostrar en carpeta
  (mismo patrón que export solución y Timeline).
- Backup de revisiones recuerda la última carpeta de destino
  (`last_backup_directory`).
- Atajos **Ctrl+Alt+B** (Exportar backup de revisiones) y **Ctrl+Alt+E**
  (Explicar candidata).
- Explicar candidata: tip en botón **Copiar**.
- Comparador: banner de soluciones desactualizadas incluye CTA **Calcular
  layout** (mismo flujo que Ctrl+Return).
- UAT / FLW-006 / RELEASE-SMOKE alineados con CTA banner outdated y ciclo
  `0.4.3.dev0`.
- Aplicar layout con soluciones desactualizadas: tip y diálogo recomiendan
  recalcular (banner / Ctrl+Return); guía rápida documenta el banner.
- Diálogo Aplicar outdated: **Calcular layout** (default) / Aplicar de todos
  modos / Cancelar.
- Exportar solución con outdated: tip honesto + diálogo **Calcular layout**
  (default) / Exportar de todos modos / Cancelar (mismo patrón que Aplicar).
- Explicar candidata con outdated: tip honesto + cabecera del diálogo avisa
  que describe la candidata vieja (sin bloquear; solo lectura).
- Comparador con outdated: tips de Re/Av Pág y Fijar referencia avisan que
  se navega/diff sobre candidatas viejas.
- Tema `system`: conserva tipografía de marca Welcome/About (`#welcomeBrand`
  Archivo 42px) sin cargar el QSS Industrial completo.
- Tema `system`: también conserva tipografía del empty Workspace
  (`#workspaceEmptyTitle` / `#workspaceEmptyBlurb`).
- Tema `system`: empty Workspace usa superficie/tinta LIGHT (contraste OK
  sobre canvas taller aunque la OS sea dark).
- Tema `system`: banner outdated usa danger/window LIGHT (aviso visible sin
  QSS Industrial completo).
- Tema `system`: `#welcomeClearRecent` conserva hover/focus LIGHT (anillo
  acento + tipografía UI) sin QSS Industrial completo.
- Tema `system`: `#welcomeRecentList` usa superficie/borde LIGHT (misma
  columna recientes que Clear Recent, contraste OK si la OS es dark).
- Tema `system`: `#welcomeRecentLabel` conserva tipografía SemiBold + muted
  LIGHT (cabecera de la columna recientes).
- Tema `system`: `#welcomeRoot` usa ventana LIGHT; tinta brand/subtitle/tagline
  scoped al root (contraste OK si la OS es dark).
- Tema `system`: `#welcomeRecentList` usa tinta + selección LIGHT (filas
  legibles sobre superficie parchment si la OS es dark).
- Tema `system`: CTAs `#primaryButton` de Welcome/empty/About/WhatsNew/
  Shortcuts/Explain usan ámbar LIGHT scoped (sin chrome Industrial global).
- Tema `system`: botones secundarios de Welcome/empty/Explain usan panel/borde
  LIGHT scoped (Open/Import/demo… / Copiar; Clear Recent conserva reglas
  propias).
- Tema `system`: `#aboutRoot` usa ventana LIGHT + tinta brand scoped; OK
  (`#primaryButton`) ámbar LIGHT.
- Tema `system`: `#whatsNewRoot` / `#shortcutsRoot` usan ventana LIGHT +
  heading/body/tabla LIGHT; OK ámbar.
- Tema `system`: `#explainSolutionRoot` usa ventana LIGHT + heading/body
  LIGHT; OK ámbar y **Copiar** secondary panel LIGHT (Preferences sigue
  chrome OS).
- Explorador: columna estirada al ancho del dock (sin `resizeColumnToContents`
  que sacaba el hit-test fuera del viewport en docks estrechos / CI offscreen).
- Calcular layout / CTA banner outdated: tip honesto
  (`tip.solve_layout_outdated`; mismo atajo Ctrl+Return).
- Vista previa de solución (Explorador) con outdated: tip honesto
  (`tip.preview_solution_outdated`; candidata vieja, sin bloquear).
- About reusa `#welcomeSubtitle` / `#welcomeTagline` para versión y blurb
  (misma jerarquía tipográfica que Welcome bajo system/light/dark).
- Import CSV/Excel recuerda la última carpeta de origen
  (`last_import_directory`; mismo patrón silencioso que export/backup).
- Abrir / Guardar como / recientes recuerdan carpeta de proyecto
  (`last_project_directory`).
- Comparar revisiones `.bcproj` recuerda la última carpeta examinada
  (`last_diff_directory`; mismo patrón silencioso que import/proyecto).
- Pack de plantillas de exportación (exportar/importar JSON) recuerda la
  última carpeta (`last_export_templates_directory`).

### Cambiado

- Proyecto: status carpeta no disponible aclara que abre el explorador de archivos.
- Barra de estado: tip sin guardar aclara que abre el explorador de archivos.
- Barra de estado: tip del basename aclara que abre el explorador de archivos.
- Proyecto: tip Abrir carpeta aclara que abre el explorador de archivos.
- Calcular layout: tip aclara que la lista de candidatas no se puede deshacer.
- Calcular layout: tip aclara que sustituye las candidatas anteriores.
- Vista: tip Comparador aclara que se recuerda entre sesiones.
- Vista: tip Timeline aclara que se recuerda entre sesiones.
- Vista: tip Inspector aclara que se recuerda entre sesiones.
- Vista: tip Explorador aclara que se recuerda entre sesiones.
- Vista: tip barra de herramientas aclara que se recuerda entre sesiones.
- Vista: tip cuadrícula aclara que se recuerda entre sesiones.
- Recientes: tip Anclar aclara que se recuerda entre sesiones.
- Timeline: tip Limpiar filtros aclara que se recuerda entre sesiones.
- Timeline: tip velocidad replay aclara que se recuerda entre sesiones.
- Timeline: tip modo replay aclara que se recuerda entre sesiones.
- Timeline: tip Solo marcadores aclara que se recuerda entre sesiones.
- Timeline: tip Solo movimientos aclara que se recuerda entre sesiones.
- Timeline: tip Evento aclara que se recuerda entre sesiones.
- Timeline: tip Algoritmo aclara que se recuerda entre sesiones.
- Timeline: tip Periodo aclara que se recuerda entre sesiones.
- Timeline: tip Seguir aclara que se recuerda entre sesiones.
- Calcular layout: tip aclara que muestra progreso y se puede cancelar.
- CI: `apt-get` evita el mirror Azure (timeout; `archive.ubuntu.com`).
- Importar piezas: tip aclara que si Excel tiene varias hojas, pide cuál.
- Importar tableros: tip aclara que si Excel tiene varias hojas, pide cuál.
- Rehacer: tip aclara que cubre piezas, tableros o colocaciones.
- Deshacer: tip aclara que cubre piezas, tableros o colocaciones.
- Preferencias: tip Restaurar valores aclara que se aplica al aceptar.
- Importar piezas: tip aclara que ofrece guardar el mapeo como plantilla.
- Importar tableros: tip aclara que ofrece guardar el mapeo como plantilla.
- Eliminar: tip aclara que al borrar un tablero las piezas se conservan.
- Nuevo desde plantilla: tip aclara que pregunta si restaurar colocaciones.
- Aplicar layout: tip aclara que no se puede deshacer.
- Restaurar revisión: tip aclara que los cambios sin guardar se pierden.
- Timeline: tip Vaciar aclara que no se puede deshacer.
- Ayuda: tip Documentación aclara fallback a índice de docs o README.
- Preferencias: tip Abrir carpeta de configuración aclara que la crea si no existe.
- Ayuda: tip Novedades aclara que prioriza Añadido de Unreleased.
- Comparador: tip Fijar referencia aclara que se pierde al recalcular.
- Comparador: tip Solo completas aclara que el filtro es solo de esta sesión.
- Comparador: tip Ordenar aclara que el criterio es solo de esta sesión.
- Vista: tip Ajustar a tableros aclara que ignora la selección.
- Guardar como: tip aclara que si el archivo existe deja revisión en el anillo.
- Guardar: tip aclara que si el archivo existe deja revisión en el anillo.
- Timeline: tip Exportar historial aclara que ofrece abrir el archivo.
- Exportar: tip solución del Comparador aclara que ofrece abrir el archivo.
- Guardar como: tip aclara que pasa a ser el archivo actual.
- Preferencias: tip aclara que los cambios se aplican al aceptar.
- Backup de revisiones: tip aclara que ofrece abrir la carpeta exportada.
- Vista: tip Ajustar a selección aclara piezas seleccionadas o tablero enfocado.
- Exportar: tip pack de plantillas menciona JSON y filtro de cliente.
- Copiar ID: tip aclara Explorador, selección única o tablero enfocado.
- Diff .bcproj: tip menciona el diálogo y que puede restaurar una revisión del anillo.
- Timeline: tip Exportar historial menciona JSON/CSV y filtros actuales.
- Exportar: tip solución del Comparador menciona opciones de formato y vista previa.
- Importar piezas: tip menciona mapeo de columnas y vista previa.
- CI: cache de pip y cancela runs de PR supersedidos.
- Importar tableros: tip menciona mapeo de columnas y vista previa.
- Exportar: tip Importar pack menciona fusionar o reemplazar el catálogo.
- Ventana: tip Restablecer disposición aclara que guarda esa disposición.
- Recientes: tip fila Welcome anclada menciona confirmación si hay cambios sin guardar.
- Recientes: tip fila Welcome menciona confirmación si hay cambios sin guardar.
- Recientes: tip Quitar del menú aclara que no borra el archivo del disco.
- Recientes: tip Abrir menciona confirmación si hay cambios sin guardar.
- Abrir: tip Ctrl+O menciona confirmación si hay cambios sin guardar.
- Aplicar layout: tip aclara que sustituye las colocaciones actuales.
- Recientes: tip Quitar aclara que no borra el archivo del disco.
- Calcular layout: tip aclara que hace falta inventario de tableros y piezas.
- Aplicar layout: tip outdated menciona diálogo recalcular/aplicar/cancelar.
- Exportar solución: tip outdated menciona diálogo recalcular/exportar/cancelar.
- Restaurar revisión local: tip Ctrl+Alt+Y menciona confirmación.
- Renombrar selección: tip F2 menciona diálogo de nombre o ID.
- Importación: tip Eliminar plantilla de mapeo menciona confirmación.
- Exportar: tip Guardar plantilla menciona diálogo del nombre.
- Exportar: tip Eliminar plantilla menciona confirmación.
- Rotar: tip R aclara que la pieza debe estar colocada en un tablero.
- Plantilla: tip Renombrar menciona diálogo del nuevo nombre.
- Plantilla: tip Eliminar del catálogo menciona confirmación.
- Duplicar: tip aclara que asigna un ID único.
- Editar selección: tip menciona diálogo de ID y dimensiones.
- Añadir pieza: tip menciona diálogo de ID, dimensiones y cantidad.
- Añadir tablero: tip menciona diálogo de ID y dimensiones.
- Guardar: tip aclara que sin archivo en disco pide ruta (como Guardar como).
- Renombrar proyecto: tip menciona diálogo del nuevo nombre.
- Eliminar: tip menciona confirmación antes de borrar pieza o tablero.
- Preferencias: tip lista secciones globales (idioma/tema/unidades/cuadrícula/
  algoritmos/exportación).
- Pantalla de inicio: tip aclara que no cierra el proyecto abierto.
- Atajos: tip F1 menciona diálogo + filas contextuales del Timeline.
- Acerca de: tip menciona diálogo con la versión de Studio.
- Documentación: tip aclara guía rápida local abierta en la app del sistema.
- Novedades: tip aclara diálogo con highlights del CHANGELOG (no abre el archivo).
- Salir: tip menciona confirmación si hay cambios sin guardar.
- Recientes: tip Vaciar lista menciona confirmación (no borra archivos del disco).
- Plantilla: tip Guardar como plantilla menciona nombre + opción de colocaciones.
- Nuevo proyecto: tip menciona diálogo nombre/unidades + confirmación si hay
  cambios sin guardar.
- Plantilla: tip Nuevo desde plantilla menciona selector + confirmación si hay
  cambios sin guardar.
- Demo: tip menciona inventario de ejemplo + confirmación si hay cambios sin
  guardar.
- Comparador: tip «Solo soluciones completas» explica omitidas vs parciales.
- Guía rápida: sección Disposición (docks Ctrl+1…4, toolbar, restablecer
  Ctrl+Shift+W).
- Explorador / Comparador: tip Vista previa aclara que no aplica y apunta a
  Ctrl+Shift+Return para conservar.
- Comparador: tip Ordenar por lista criterios (ranking / piezas / huecos /
  tablero libre / puntuación).
- Timeline: tip Marcador menciona diálogo de nota (+ paso/algoritmo de replay);
  guía rápida documenta el botón.
- Guía rápida: sección Pantalla de inicio (CTAs, recientes, atajos Welcome).
- Guía rápida: sección Plantillas de proyecto (guardar / nuevo, colocaciones,
  vs plantillas de exportación).
- Guía rápida: sección Preferencias (pestañas globales, cuadrícula,
  carpeta de config); Consejos dejan de duplicar tema/idioma.
- Guía rápida: sección Exportar (formatos, plantillas, pack, abrir carpeta,
  banner desactualizado).
- Guía rápida: sección Workspace (overlay vacío, pan, zoom, nudge, selección);
  Consejos dejan de duplicar pan/nudge/selección.
- Guía rápida: sección Inspector (selección, métricas de layout, retales
  informativos, banner desactualizado).
- Guía rápida: sección Explorador (doble clic, menú contextual, colocar,
  vista previa).
- Guía rápida: sección Comparador (ordenar, completas, referencia, navigate,
  banner desactualizado, explicar).
- Timeline: tip Vaciar menciona confirmación; tip de lista (atajos + Ctrl+C)
  y tips del menú contextual copiar línea / payload.
- F1 Atajos: fila contextual Timeline Ctrl+C (copiar línea de evento) e intro;
  guía rápida alinea Ctrl+C = línea (payload vía menú contextual).
- F1 Atajos: filas contextuales de replay Timeline (Espacio / Inicio / ← / →)
  e intro que las menciona.
- Guía rápida: sección Timeline (Seguir, filtros, replay, export) y atajos
  contextuales de reproducción.
- Timeline: tips en combos de filtro (evento / algoritmo / periodo) y replay
  (modo / velocidad).
- Timeline: tips honestos en Seguir / Solo movimientos / Solo marcadores
  (ya no repiten solo la etiqueta).
- Barra de estado y tip Export del dock Timeline: atajos vía
  `with_native_shortcuts` (⌘ en macOS, no Ctrl+ literal).
- Guía rápida: **Ctrl+Shift+W** / **Ctrl+Shift+F2** / **Ctrl+Shift+L**,
  más **Acerca de** (**Ctrl+Shift+A**) y **Salir** (**Ctrl+Q**).
- Guía rápida: atajos de selección/edición (**Ctrl+A** / **Escape** /
  **Ctrl+Shift+I**, **Return**, **Ctrl+Shift+C**).
- Guía rápida: nudge de pieza con flechas / Shift+flechas; atajos de
  plantilla (**Ctrl+Shift+N** / **Ctrl+Shift+M**).
- Guía rápida: pan de cámara (medio / derecho / Espacio+arrastre) y Eliminar
  con Backspace o Delete.
- Tips Zoom +/− (menú/toolbar): mencionan rueda además del atajo
  (paridad con tip del % en barra).
- Guía rápida: barra de estado (basename, clic → carpeta, tip sin guardar,
  zoom) y atajo **Ctrl+Shift+R**.
- Tip del basename en barra de estado sin guardar: indica Guardar (Ctrl+S)
  para poder abrir la carpeta.
- Tip del % de zoom en barra de estado: incluye rueda y atajos
  (Ctrl+= / Ctrl+- / Ctrl+0).
- Docs: Preferencias bajo tema `system` = chrome OS (sin `#preferencesRoot`);
  DESIGN / SCR-006 / guía rápida + asserts.
- Docs planificación 2026-08-13: snapshot
  `docs/masterplan/REVIEW-2026-08-13-planificacion.md`; cola IDE-0019…0024
  vigente (sin IDE nuevas: residuales + backlog abierto; ola tips honesty
  Archivo/Edición/Ayuda/plantillas/outdated PRs ~457–490); ROADMAP /
  DOC-003 / DOC-004 / DOC-006 / MASTERPLAN / AI_CONTEXT / INDEX alineados.
- Docs planificación 2026-08-12: snapshot
  `docs/masterplan/REVIEW-2026-08-12-planificacion.md`; cola IDE-0019…0024
  vigente (sin IDE nuevas: residuales + backlog abierto; ola tips honesty
  Archivo/Edición/Ayuda/plantillas PRs ~457–473); ROADMAP / DOC-003 /
  DOC-004 / DOC-006 / MASTERPLAN / AI_CONTEXT / INDEX alineados.
- Docs planificación 2026-08-10: snapshot
  `docs/masterplan/REVIEW-2026-08-10-planificacion.md`; cola IDE-0019…0024
  vigente (sin IDE nuevas: residuales + backlog abierto; avance tips honesty
  Comparador/plantillas/demo + guía Disposición); ROADMAP / DOC-003 /
  DOC-004 / DOC-006 / MASTERPLAN / AI_CONTEXT / INDEX alineados.
- Docs planificación 2026-08-09: snapshot
  `docs/masterplan/REVIEW-2026-08-09-planificacion.md`; cola IDE-0019…0024
  vigente (sin IDE nuevas: residuales + backlog abierto; avance guía rápida
  Welcome…Explorador); ROADMAP / DOC-003 / DOC-004 / DOC-006 / MASTERPLAN /
  AI_CONTEXT / INDEX alineados.
- Docs planificación 2026-08-08: snapshot
  `docs/masterplan/REVIEW-2026-08-08-planificacion.md`; cola IDE-0019…0024
  vigente (sin IDE nuevas: residuales + backlog abierto; avance QoL Timeline/
  guía); ROADMAP / DOC-003 / DOC-004 / DOC-006 / MASTERPLAN / AI_CONTEXT /
  INDEX alineados.
- Docs planificación 2026-08-07: snapshot
  `docs/masterplan/REVIEW-2026-08-07-planificacion.md`; cola IDE-0019…0024
  vigente (sin IDE nuevas: residuales + backlog abierto); ROADMAP / DOC-003 /
  DOC-004 / DOC-006 / MASTERPLAN / AI_CONTEXT / INDEX alineados.
- Docs planificación 2026-08-06: snapshot
  `docs/masterplan/REVIEW-2026-08-06-planificacion.md`; cola IDE-0019…0024
  vigente (sin IDE nuevas: residuales + backlog abierto); ROADMAP / DOC-003 /
  DOC-004 / DOC-006 / MASTERPLAN / AI_CONTEXT / INDEX alineados.
- Docs planificación 2026-08-05: snapshot
  `docs/masterplan/REVIEW-2026-08-05-planificacion.md`; backlog IDE-0019…0024
  (swap, kerf, veta, Skyline multipanel, lista de corte, metadatos proyecto);
  ROADMAP / DOC-003 / DOC-004 / MASTERPLAN / AI_CONTEXT / INDEX alineados.
- Tips de Abrir / Guardar como / Import / Diff / Export solución·Timeline /
  pack plantillas avisan «recuerda la última carpeta» (mismo honesty que
  backup; prefs `last_*_directory` ya activas).
- Docs ciclo (`AI_CONTEXT`, MASTERPLAN, ROADMAP) alineados con `0.4.3.dev0`.
- Diálogo post-export: si destino es carpeta, copy «Carpeta creada» + **Abrir
  carpeta** (sin «Mostrar en carpeta» redundante).
- `make check` / `make lint` incluyen `ruff format --check` (mismo gate que CI).
- UAT / SCR-003 / SCR-005 / FLW-006 documentan backup (**Ctrl+Alt+B**) y
  Explicar candidata (**Ctrl+Alt+E**).
- Tip backup menciona carpeta recordada; piloto DT-0006 + SCR-007 alineados
  con open-after / `last_backup_directory`.
- Spike IDE-0007: MVP marca Copiar / atajo Ctrl+Alt+E.
- Diff `.bcproj`: botón **Comparar** como CTA primario (altura ≥36 + tip).
- Helper `polish_secondary_button`: Examinar (diff), carpeta de config (prefs),
  renombrar/eliminar plantilla (altura ≥36 + tip).
- Export / mapeo CSV: Guardar·Eliminar·pack plantillas e Eliminar mapeo con
  `polish_secondary_button`.
- Comparador: **Fijar como referencia** ≥36px; Explicar **Copiar** usa
  `polish_secondary_button`; DESIGN documenta el helper.
- Timeline: botones etiquetados de la fila de acciones ≥36 vía
  `polish_secondary_button` (transporte replay sigue compacto).
- Tras cambio de tema, `repolish_secondary_buttons` restaura alturas de
  secundarios (evita wipe light/dark → `system`).
- Welcome + empty Workspace: CTAs vía `polish_primary_button` /
  `polish_secondary_button` (sobreviven cambio de tema).
- Diff `.bcproj`: **Comparar** usa `polish_primary_button` (altura durable).
- UAT: checklist eval humana Explicar candidata (IDE-0007); DESIGN tipografía
  tabla corregida.

## 0.4.2 — 2026-08-02

### Añadido

- Ayuda → Novedades cae a highlights de la última release si Unreleased está vacío.
- Piloto **DT-0006 opción D**: `boardcomposer-backup` + Proyecto → Exportar backup
  de revisiones… (`docs/ops/PILOT-DT-0006-backup.md`, DEC-0010).
- IDE-0007 MVP: Ayuda → **Explicar candidata…** (explicación determinista; spike
  `SPIKE-IDE-0007`, DEC-0011).
- `boardcomposer-backup`: epilog venv, aviso `.bcstudio.json` → sibling `.bcproj`.
- Explicar candidata: botón **Copiar** al portapapeles; guía rápida documenta
  backup + explicar.
- Explicar candidata: tras Copiar, status bar confirma «copiada al portapapeles».
- Tip de Explicar candidata menciona Copiar; piloto DT-0006 D marcado validado.

### Cambiado

- Versión de Studio (Welcome / About) se lee de `pyproject.toml` — una sola fuente.
- Timeline: transport de replay y Marcador llevan statusTip (idle honesto sin solución).
- Fallbacks de Ayuda → Novedades (fichero ausente / vacío) respetan idioma UI.
- Docs ciclo (`AI_CONTEXT`, MASTERPLAN, SCR-001, ROADMAP) alineados con `0.4.2.dev0`.

## 0.4.1 — 2026-08-01

### Añadido

- Proyecto → **Restaurar última revisión local…** (`Ctrl+Alt+Y`): atajo y
  enablement honesto sobre el anillo `.bcproj.revs/`.

### Cambiado

- Anillo local `.bcproj.revs/`: `MAX_REVISIONS` 5 → **10**; FLW-005 deja de
  negar PNG/JPEG (ya soportados en export).
- Guía rápida alineada con atajos diarios (solve, export, import Excel, zoom,
  undo, docks) y nota ⌘ en macOS; MASTERPLAN apunta a la guía.
- Calcular layout exige ≥1 tablero y ≥1 pieza (tip/status honestos; no lanza
  solver vacío).
- Al abrir / nuevo / demo / plantilla / restaurar se vacía la pila undo/redo
  (evita deshacer comandos de otro proyecto).
- Guía rápida, FLW-006, SCR-005 y UAT documentan comparar/restaurar revisiones
  locales (`Ctrl+Shift+Y` / `Ctrl+Alt+Y`).

## 0.4.0 — 2026-07-31

### Añadido

- Restaurar revisión local desde Comparar revisiones (anillo `.bcproj.revs/`):
  carga en memoria, misma ruta, dirty hasta Guardar; vacía undo/redo.
- Gate corto demo/release: `uat/RELEASE-SMOKE.md`.
- Spike DT-0006 (`docs/masterplan/spikes/SPIKE-DT-0006-historial-cloud.md`):
  opciones Git / sync / API / export; **sin cloud** hasta piloto.
- Mapa docs (`docs/README.md`), guía rápida usuario (`docs/user/GUIA-RAPIDA.md`)
  y checklist visual UAT (`uat/studio/CHECKLIST-VISUAL.md`). Ayuda →
  Documentación abre la guía de usuario.
- Tip dinámico Mostrar/Ocultar + status al toggle de la barra (Ctrl+Shift+K).
- Tip dinámico Mostrar/Ocultar + status al toggle de docks (Ctrl+1…4).
- Regresión UAT multi-candidata: `tests/test_uat_multi_candidate_flow.py`
  (demo→≥2 en Comparador/Explorador, Re/Av Pág, pin/diff, export solución
  con open-after). Checklist §4 marcado con enlace a esa suite.
- UAT Studio/multipanel: Resultado § cerrado; pendiente multipanel absorbido
  por checklist Studio.
- Al guardar un `.bcproj` existente, la barra de estado anuncia la revisión
  anterior conservada en el anillo local (Comparar revisiones).
- Regresión UI importación: `tests/test_dialog_chrome.py` valida preview por
  fila (estado `OK` y error visible), cerrando hueco residual de checklist visual.

### Cambiado

- Overlay vacío del Workspace: tips/tooltips en CTAs (paridad con Welcome).
- Menú contextual Explorador: tips de status en Editar / Duplicar / Eliminar /
  Renombrar / Copiar ID / Añadir / Vista previa (además de Colocar / carpeta).
- Timeline «Limpiar filtros» anuncia status al vaciar filtros activos.
- Deshacer/Rehacer anuncian status (`status.undone` / `status.redone`); sin pila,
  reutilizan tips idle existentes.
- Editar tablero/pieza sin diffs anuncia status (`status.edit_unchanged`).
- Gate demo/release cerrado en `uat/RELEASE-SMOKE.md` (Studio manual OK).
- Welcome: tips/status en CTAs principales (nuevo, abrir, importar, demo, docs…).
- Explorador: tip honesto «Colocar» (ya colocada vs falta tablero); revelar
  carpeta usa `project_folder_unavailable`.
- Renombrar sin cambio de nombre anuncia status; colocar pieza sin returns mudos.
- Menú Recientes vacío muestra tip + Vaciar deshabilitado.
- DOC-006: métricas/umbrales por release; DOC-004: estimaciones IDE-0007/0008
  y DT-0006.
- `ROADMAP.md` raíz alineado con DOC-003/004: Fase 3 EP-001…003 marcadas
  entregadas; próximo foco DT-0006 / IA bajo demanda.
- UAT plataforma (`uat/plataforma/CHECKLIST.md`) marcado OK operativo
  (smoke batch+HTTP + 21 tests, 2026-07-30).
- Comparador: Re/Av Pág y Pin respetan el filtro visible (tips/enablement).
- Rotar: tip honesto si la pieza está seleccionada pero aún no colocada.
- Menú contextual Explorador: tip al deshabilitar Colocar / Abrir carpeta.
- DOC-010 / EP-003: rate-limit y mTLS diferidos hasta piloto nombrado.
- Raíz docs limpia: `TODO.md` / `DECISIONS.md` stubs → masterplan;
  `docs/estructura.md` redirige; `NOTEBOOK.md` marcado histórico.
  Ayuda → Documentación prioriza guía usuario sobre masterplan.
  Tip/status de docs habla de «guía rápida».
  UAT visual cerrado; DOC-003/DOC-006 alineados (revisiones ya entregadas).
- `DOC-006-DeudaTecnica` actualizado a `1.2.0` (29/07/2026): estado en verde,
  deuda abierta explícita `DT-0006` (historial cloud/multi-usuario) y próximos
  focos concretos por release.
- Sincronía UAT post-cierre: `CHECKLIST-FUNCIONAL` ya no describe la visual como
  «sin marcar», y `CHECKLIST-VISUAL` fija base en `main@3430698`.
- `uat/README.md`: separador de tabla en estilo markdownlint (`MD060`) para
  evitar ruido de lint en docs UAT.
- `DOC-004-Backlog` y comentario en `solution_validator.py` actualizados para
  reflejar estado post-Fase 3 y eliminar referencias al `TODO.md` ya stub.
- Tablas Markdown en `docs/` y `uat/`: eliminada línea vacía entre cabecera y
  separador (rompe render en GitHub/previewers).
- `board_ids` / `piece_ids` delegan en helper compartido `studio/unique_ids.py`
  (misma lógica casefold + sufijos `-2`, `-3`, …).
- Expansión por cantidad (`qty>1` → `base-1`…) unificada en
  `expand_ids_for_quantity`; diálogo Nuevo pieza e import CSV/XLSX la comparten.
  También reserva el id base tras expandir (evita colisión `LAT×3` + `LAT`).
- Strip de retales en export unificado: `prepare_solution_for_export` en Core;
  Studio y batch lo reutilizan (SCR-007 / EP-002).
- Parsers numéricos de import CSV/XLSX (`parse_positive_float` /
  `parse_positive_int`) compartidos en `studio/import_parse.py`.
- Campos opcionales de import (espesor / cantidad / material + defaults)
  unificados en `optional_positive_*` / `optional_string`.
- Resolución de cabeceras de import (`prepare_import_header_map` + mensaje
  de archivo vacío) compartida entre importers de tablero y pieza.
- Pipeline UI de import CSV/Excel en Studio: helpers compartidos para abrir
  archivo, resolver cabeceras (plantilla/mapeo) y refrescar tras importar.
- Export SVG reutiliza `panel_offsets` / `canvas_size_mm` de `export/common`
  (misma geometría que DXF/PDF); tests dedicados en `test_export_common.py`.
- Sets de IDs casefold (`casefolded_piece_ids` / `casefolded_board_ids`)
  compartidos entre commands y MainWindow.
- Test de contrato: `DEFAULT_SVG_PALETTE` refleja `LIGHT_CANVAS` (export /
  thumbnails alineados con el workspace claro).
- Colisión de IDs al renombrar/editar (`id_taken`) unificada en
  `studio/unique_ids.py` y usada desde MainWindow.
- Cobertura de revisiones `.bcproj`: checklist UAT funcional/visual ahora
  incluye `Ctrl+Shift+Y`, y test de integración valida que MainWindow abre
  `BcprojDiffDialog` con contexto de proyecto/ruta.
- Nuevo checklist UAT de plataforma (`uat/plataforma/CHECKLIST.md`) para
  operación sin UI: batch CLI, API HTTP, auth y smoke de regresión.
- Timeline registra `PieceMoved` con payload de movimiento/reasignación
  (pieza, origen/destino y panel) para trazabilidad de edición en Workspace.
- Timeline muestra `PieceMoved` en formato legible (`pieza: panel origen→destino,
  (x,y)→(x,y)`) y conserva metadatos adicionales en el detalle.
- Export CSV del Timeline incluye columnas específicas para `PieceMoved`
  (`piece`, `kind`, `from_*`, `to_*`, panel origen/destino) además de
  `payload_json`.
- Panel Timeline añade filtro rápido “Solo movimientos” para alternar
  `PieceMoved` ↔ todos los eventos sin abrir el combo de filtros.
- Panel Timeline añade filtro rápido “Solo marcadores” para alternar
  `TimelineMarked` ↔ todos los eventos.
- Filtros de Timeline (evento, algoritmo, periodo) persisten en preferencias
- Modo de reproducción del Timeline (colocaciones / fases) persiste en
  preferencias entre reinicios.
- Velocidad de autoplay del Timeline (lenta / normal / rápida) con selector
  en el dock y persistencia en preferencias.
- Timeline: toggle «Seguir» para auto-scroll a eventos nuevos (desactivable;
  persistido en preferencias).
- Export Timeline recuerda el último formato (JSON/CSV) y lo preselecciona
  en el diálogo de guardar.
- Timeline: atajos de reproducción con la lista enfocada (Espacio play/pausa,
  ←/→ paso, Inicio reset).
- Timeline muestra contador de eventos visibles (y total si hay filtros
  activos).
- Vaciar Timeline pide confirmación (con recuento de eventos) antes de
  borrar el historial.
- Timeline: menú contextual / Ctrl+C copia la línea del evento (o el payload
  JSON) al portapapeles.
- Timeline: botón «Limpiar filtros» restaura evento/algoritmo/periodo de un
  clic (habilitado solo con filtros activos).

### Corregido

- `make run` arranca Studio (`python -m studio.app`); antes lanzaba la CLI
  y salía al instante. CLI corta: `make run-cli` / `make demo`.
- Toggle cuadrícula (Ctrl+G): tip dinámico Mostrar/Ocultar según estado +
  status «Cuadrícula visible/oculta» al cambiar.
- «Ajustar al tablero» muestra status honesto si no hay tableros (paridad con
  «Ajustar a la selección»; antes no-op silencioso si se invocaba).
- «Pantalla de inicio» deshabilitada si ya estás en Welcome; tip
  `already_on_welcome` (evita no-op de Ctrl+Shift+H).
- «Nuevo desde plantilla» (menú + Welcome) deshabilitado sin plantillas
  guardadas; tip `template_empty` en vez de atajo genérico + diálogo vacío.
- Zoom +/- deshabilitado al llegar al máximo/mínimo de cámara; tip honesto
  (antes el atajo seguía activo sin efecto visible).
- Seleccionar todas / Invertir deshabilitados sin piezas en canvas; Deseleccionar
  deshabilitado sin selección; tips honestos (antes Escape podía ser no-op
  silencioso).
- Acciones Edit (Eliminar / Duplicar / Editar / Renombrar / Copiar ID)
  deshabilitadas sin pieza, tablero o proyecto seleccionable; tips honestos
  en vez de atajo genérico con no-op vía menú.
- «Rotar» (R) deshabilitado sin pieza seleccionada (con placement); tip pide
  seleccionar pieza en vez de no-op silencioso.
- «Calcular layout» deshabilitado sin proyecto; tip honesto (antes mostraba
  atajo genérico sin contexto).
- «Ajustar al tablero» deshabilitado sin tableros/proyecto; tip honesto en vez
  de atajo genérico.
- «Ajustar a la selección» deshabilitado sin selección/foco de tablero; se
  activa al seleccionar pieza o enfocar tablero.
- Re/Av Pág sin soluciones: tip vuelve a «calcula layout» (antes decía «1
  candidata visible» incluso con 0).
- Export Timeline ahora respeta filtros activos para enablement (si filtro
  deja 0 eventos, menú/botón quedan deshabilitados).
- Welcome: botón «Vaciar lista» ahora muestra tip/shortcut cuando hay
  recientes y mensaje honesto cuando está deshabilitado.
- Atajo/acción «Vaciar recientes» también queda deshabilitado sin recientes y
  muestra estado honesto (evita no-op silencioso).
- Timeline filtrado a 0 eventos: Exportar se deshabilita, pero «Vaciar» sigue
  activo si existe historial global.
- Menú/atajo `Exportar Timeline` ahora se resincroniza al cambiar filtros del
  panel Timeline (antes podía quedar stale hasta nuevo evento).
- Undo / Redo: con historial vacío quedan deshabilitados y su tip explica
  «no hay acciones para deshacer/rehacer» (antes mantenían tip genérico).
- «Abrir carpeta del proyecto» tip pide guardar cuando aún no hay `.bcproj`
  en disco (antes repetía el tip de abrir carpeta estando deshabilitado).
- Guardar / Guardar como / Guardar plantilla / Renombrar proyecto
  deshabilitados sin proyecto abierto; tips honestos.
- Timeline: «Vaciar» deshabilitado sin eventos; tip explica el vacío (mismo
  patrón que Exportar).
- Comparador: ordenar y «solo completas» deshabilitados sin candidatas; tip
  pide Ctrl+Return. Tip del pin distingue 0 / 1 / ≥2 soluciones.
- Export Timeline deshabilitado sin eventos (menú + botón del dock); tip
  explica el vacío. Arranque: `bootstrap_ui_font` evita warning `Sans Serif`
  antes de construir widgets.
- Tema «Sistema»: ya no fuerza la familia ficticia `Sans Serif` (warning
  Qt/`qt.qpa.fonts` en macOS y CI offscreen); usa Source Sans 3 bundled.
- Comparador: «Fijar como referencia» solo con >=2 candidatas; tips de
  Aplicar/Exportar/Re-Av Pág explican por qué están deshabilitados.
- Acciones sin candidata útil quedan deshabilitadas: `Aplicar layout` y
  `Exportar` solo con >=1 solución; `Re/Av Pág` solo con >=2.
- Exportar historial del **Timeline**: tras guardar, mismo diálogo
  «Abrir archivo» / «Mostrar en carpeta» que al exportar una solución.
- Tips del Comparador con ≥2 candidatas: post-solve menciona Re/Av Pág y
  «Fijar referencia»; con 1 sola, apunta al demo; tooltip del botón pin;
  `diff.need_two` indica Ctrl+Shift+D.
- Tras Calcular layout, el **Comparador** sale al frente (Ctrl+4) y el tip
  menciona **Exportar Ctrl+Shift+E**; sin layout, el tip de export/aplicar
  indica el camino Ctrl+Return → Exportar/Aplicar.
- **Re Pág / Av Pág** con una sola candidata visible: tip claro («solo hay 1…
  no tienen otra») en vez de «No hay soluciones calculadas»; si el filtro del
  Comparador deja la lista vacía, lo dice.
- Tras Calcular layout con **1 sola** candidata aceptada, el status lo dice
  claro («única candidata… no hay más distintas») con generadas/únicas —
  no se confunde con el límite de Preferencias.
- Proyecto demo (**Ctrl+Shift+D**): si `Máx. soluciones` era 1, se restaura
  al default (20) para que Calcular layout muestre el Comparador / PgUp.
- Crash macOS (SIGSEGV en `QDockWidget::raise`): Timeline/Comparador se
  tabifican **después** de `addDockWidget`; `raise_()` va diferido y no
  toca docks ocultos/destruidos.
- Cuando hay más candidatas aceptadas que visibles por `Máx. soluciones`,
  Studio avisa en status (`mostrando n/m`) para evitar confusión en UAT.
- Piezas sin colocar (p. ej. T* omitidas del layout) se pueden pegar/colocar
  en el tablero enfocado del Explorador (menú contextual o doble clic);
  valida material/espesor y muestra el motivo si no caben.
- Colocar en tablero: el destino sobrevive al seleccionar la pieza (antes el
  clic en T* borraba el foco del tablero y deshabilitaba la acción).
- Drag entre paneles: exige mismo espesor y material (antes solo geometría;
  se podía soltar 18 mm en Tablex 5 mm).
- Explorador: vista previa de solución (doble clic / Enter) — ya no se
  reconstruye el árbol al seleccionar (borraba el ítem y mataba el segundo
  clic del doble clic).
- **R** rota la pieza seleccionada en el Workspace (el atajo QAction no
  llegaba con foco en el canvas); `rotated`/`rotation` quedan sincronizados.
- Atajos en macOS: tips y Ayuda → Atajos muestran ⌘ (Command) en vez de
  texto `Ctrl+…` (Qt ya mapeaba `Ctrl`→⌘; la UI inducía a pulsar Control ⌃).
  Acordes `Ctrl+…` usan `ApplicationShortcut`; teclas sueltas (R, F2…) no.

### Añadido

- Exportación: recuerda la última carpeta de destino (`last_export_directory`
  en `preferences.json`); el diálogo de guardar (solución y Timeline) reabre
  ahí si la carpeta sigue existiendo.
- Plantillas de proyecto: renombrar desde el diálogo **Nuevo desde plantilla**
  (SCR-005).
- Plantillas de proyecto: restaurar colocaciones al crear desde plantilla
  (si las hay) y eliminar plantilla desde el diálogo de elección (SCR-005).
- Preferencias: i18n completo del diálogo (pesos, export, temas, estrategias;
  SCR-006).
- Comparador: highlights «mejor en» incluyen tablero libre, largo y ancho
  (además de piezas / huecos / score).
- Comparador: **Re Pág / Av Pág** siguen el orden y filtro visibles de la
  tabla (no solo el ranking del solver).
- Comparador: la referencia fijada se marca en la tabla y miniaturas
  (`Ref n` / fondo; SCR-003).
- Anillo de revisiones locales al guardar `.bcproj` (carpeta
  `.<nombre>.bcproj.revs/`, máx. 5); el diálogo de diff ofrece la última
  revisión vs el proyecto abierto.
- Studio: **Proyecto → Comparar revisiones .bcproj…** (`Ctrl+Shift+Y`) —
  UI sobre `diff_bcproj` (proyecto abierto vs archivo, o dos archivos).
- Contenedor HTTP de referencia (EP-003 / SPR-003): `Dockerfile`,
  `docker-compose.yml`, `scripts/serve_docker.sh`; amenazas en DOC-010.
- Diff estructural `.bcproj` (FLW-006): `boardcomposer-diff` / `diff_bcproj` — meta, tableros, piezas, placements.
- Adaptador HTTP opcional `boardcomposer-serve` (EP-003 / SPR-001):
  Flask sobre `api.v1` — `/health`, `/v1/run`, `/v1/openapi.json`;
  auth por `BOARDCOMPOSER_API_KEY`.
- Batch `--list` / `--dry-run` (EP-002 / SPR-003): lista explícita de
  paths + manifiesto sin solver; sample `data/samples/batch_jobs.list`.
- Batch headless `boardcomposer-batch` (EP-002 / SPR-001): carpeta CSV /
  `.bcproj` → exports + `manifest.json`, perfil JSON, exit 0/1/2;
  `scripts/batch_samples.sh` y `data/samples/batch_inbox/`.
- API `v1.1.0` (EP-001 / SPR-003): `load_project` / `run` aceptan `.bcproj`
  (stock + piezas); migraciones ADR-015 en Core (`boardcomposer.io.bcproj`),
  compartidas con Studio; sample `data/samples/multipanel_demo.bcproj`.
- DOC-009 — formatos de intercambio API `v1` (EP-001 / SPR-002): CSV de
  piezas, JSON/CSV/SVG de solución alineados a Core.
- API Python pública `boardcomposer.api.v1` (EP-001 / SPR-001):
  `load_project` → `solve` → `export_json|svg|csv`, `run`;
  tests de contrato y `examples/api_v1_minimal.py` (sin Studio/Qt).
- `AddBoardCommand` / `AddPieceCommand`: añadir tablero o pieza(s) es
  deshacible (Ctrl+Z), cerrando la deuda de FLW-006 / ADR-008.
- `StockPanel.quantity` como inventario de unidades físicas.
- `PanelReference` para asignar colocaciones a tipo e instancia de panel.
- Packing MaxRects sobre múltiples paneles y tipos de espesor compatible.
- Validación de referencia, límites, espesor y solapes por panel físico.
- Estado completo/parcial en `ValidationResult`.
- Métricas de área usada y desperdicio por panel consumido.
- Persistencia Studio versión 2 compatible con proyectos versión 1.
- Cantidad y espesor editables en tableros y piezas de Studio.
- Disposición visual y exportación SVG de paneles lado a lado.
- ADR-014 con el contrato multipanel.
- Compatibilidad de **material** (además de espesor) entre pieza y panel,
  validada en el solver y enrutada por `multi_panel_maxrects`.
- Búsqueda de órdenes de panel (`panel_ordering.py`) como eje adicional del
  generador MaxRects, junto a heurísticas y órdenes de pieza.
- **Retales aprovechables** (`Offcut`) reportados de forma informativa por
  panel consumido, en Inspector, SVG y presentadores JSON/texto (ADR-016).
- Soluciones **parciales**: piezas que no caben se reportan como
  `omitted_piece_ids` en vez de descartar toda la solución.
- Migraciones explícitas y versionadas de `.bcproj`, con
  `UnsupportedProjectVersionError` para ficheros de una versión futura
  desconocida (ADR-015).
- Importación de inventario de tableros desde CSV
  (`Proyecto → Importar inventario de tableros (CSV)…`), con vista previa,
  validación por fila y detección de duplicados.
- Campo de cantidad al crear una pieza nueva, generando varios ids
  correlativos de una sola vez.
- Movimiento y reasignación interactiva de piezas entre paneles físicos
  distintos desde el Workspace, arrastrando la pieza sobre el panel destino.
- Identificador e instancia de panel físico visibles en el Inspector de
  pieza.
- Resaltado de "puntos clave" (mejor solución por métrica) en el comparador
  de soluciones de Studio (SCR-003).
- Diagnóstico con estadísticas del solver cuando no se encuentra ninguna
  solución.
- Suite de pruebas de interacción Qt para el Workspace (arrastre,
  reasignación de panel, selección, reversión de movimientos inválidos).
- Script de benchmarks reproducibles para `multi_panel_maxrects`
  (`scripts/benchmark_multipanel_maxrects.py`).
- Generador exacto CP-SAT de un solo panel (opcional,
  `pip install 'boardcomposer[cp_sat]'`, estrategia `exact`, ADR-017).
- Comparador: ordenar por métrica y filtrar «solo completas» (SCR-003).
- Exportación DXF y PDF de la solución seleccionada (además de SVG).
- Importación de piezas desde CSV (`Proyecto → Importar piezas (CSV)…`).
- Revisión UI `docs/masterplan/ui/REVIEW-2026-07-17.md`.
- Preferencias de Studio (SCR-006): estrategia y pesos de scoring en
  `~/.boardcomposer/preferences.json` (`Editar → Preferencias…`).
- Miniaturas SVG sincronizadas en el comparador de soluciones (misma escala).
- Importación CSV/Excel (`.xlsx`) de tableros y piezas (FLW-002), sin
  dependencias extra (lector OOXML mínimo).
- Panel de diferencias del comparador (SCR-003): métricas y colocaciones
  respecto a una solución de referencia fijable.
- Exportación JSON y CSV de la solución seleccionada (SCR-007).
- Preferencias ampliadas SCR-006: tema (sistema/claro/oscuro), mostrar
  cuadrícula y tamaño de grid persistidos en `preferences.json`.
- Pantalla de inicio SCR-001 con acciones principales, recientes
  persistidos y acceso a preferencias/ejemplo.
- Diálogo de exportación SCR-007 con formato, opciones (métricas,
  explicación, retales), vista previa y recuerdo de la última elección.
- Preferencias SCR-006: idioma (es/en), unidades (mm/cm/in) aplicadas a
  inspector, explorador y formularios; defaults de exportación editables.
- Miniaturas reales de proyectos recientes en la pantalla de inicio
  (SCR-001): SVG del layout del `.bcproj` más fecha de modificación.
- Vista previa gráfica SVG embebida en el diálogo de exportación
  (SCR-007), actualizada al cambiar formato u opciones.
- Idioma es/en aplicado a menús, docks, Inspector y comparador (SCR-006).
- Plantillas de exportación nombradas en el diálogo SCR-007
  (`~/.boardcomposer/export_templates.json`).
- i18n es/en de diálogos (export/import) y mensajes de la barra de estado.
- i18n es/en de formularios Nuevo/Editar tablero y pieza.
- i18n es/en del panel de diferencias del comparador (SCR-003).
- Perfiles de exportación por cliente (plantillas SCR-007 con campo
  `client` y filtro en el diálogo).
- Tema visual «Industrial madera»: tokens + QSS (claro/oscuro), fuentes
  Archivo / Source Sans 3, y pantalla de inicio brand-first (`docs/DESIGN.md`).
- Colores del canvas/workspace alineados al tema (tablero, pieza, selección,
  validación y grid).
- Paleta SVG Industrial madera en exportación y miniaturas (inicio,
  comparador, vista previa de export).
- Compartir plantillas de exportación entre equipos (pack JSON).
- Plantillas de proyecto (guardar / nuevo desde plantilla).
- Accesos a documentación y novedades (menú Ayuda + pantalla de inicio).
- Preferencias avanzadas: tope de soluciones y progreso al calcular layout
  (FLW-003 / SCR-006).
- Cancelación cooperativa del solver (`CancellationToken`) con botón
  Cancelar en el diálogo de progreso de layout (FLW-003).
- Timeline MVP (ADR-005): dock alimentado por el Event Bus (ADR-003) con
  filtro por tipo de evento y vaciado; publicación de hechos clave
  (proyecto, CSV, cálculo, selección, export, workspace).
- Reproducción paso a paso de colocaciones de la solución seleccionada
  en el Timeline (Inicio / ◀ / ▶ / Play), sin mutar el proyecto.
- Detección de soluciones desactualizadas al editar el proyecto (FLW-006):
  banner en el Comparador, aviso al aplicar y eventos `ProjectModified` /
  `SolutionsMarkedOutdated`.
- Comparador sincronizado con la reproducción del Timeline: el panel de
  diferencias muestra el divergencia paso a paso vs la referencia (SCR-003).
- Trazas de algoritmo del solver (`SolveTrace`): el Timeline registra
  `AlgorithmStarted` / `AlgorithmFinished` / `EvaluationFinished`, y el
  replay etiqueta el generador y la pieza actual (ADR-005).
- Exportación del historial del Timeline a JSON/CSV (menú Exportar y botón
  en el dock) respetando el filtro activo.
- Instrumentación de fallos de colocación MaxRects (`incompatible` / `no_fit`)
  en la traza del solver y el Timeline (`PlacementFailed` + resumen).
- Filtro del Timeline por algoritmo y métricas temporales (`duration_ms`) en
  `AlgorithmFinished` / `EvaluationFinished` (ADR-005).
- Marcadores/anotaciones de usuario en el Timeline (`TimelineMarked`) con
  nota libre y contexto opcional del replay (algoritmo, pieza, paso).
- Filtro del Timeline por intervalo temporal (presets 1/5/15 min y 1 h),
  respetado también al exportar (`since` / `period_seconds`).
- Instrumentación de fallos de colocación Skyline (`no_fit`) en la traza
  y el Timeline; captura activa para todos los generadores instrumentados.
- Reproducción de fases del solver en el Timeline (modo Colocaciones /
  Fases): recorre `SolveTrace` y sincroniza solución/pieza cuando aplica.
- Clic en un hecho del Timeline para buscar contexto (algoritmo → solución,
  pieza fallida, índice de solución, nota de marcador).
- Asistente de mapeo de columnas al importar CSV/Excel cuando no se
  reconocen cabeceras obligatorias (FLW-002).
- Selector de hoja al importar libros Excel con varias hojas; el preview
  muestra el id aunque la fila sea inválida.
- Importación CSV/Excel de tableros y piezas deshacible (Ctrl+Z) con
  `ImportBoardsCommand` / `ImportPiecesCommand`.
- Plantillas de mapeo de columnas al importar CSV/Excel: se guardan y
  reaplican automáticamente cuando el archivo trae las mismas cabeceras.
- Tras exportar una solución, diálogo para abrir el archivo o mostrar su
  carpeta; eventos `ExportStarted` / `ExportFailed` en el Timeline (FLW-005).
- Eliminar plantillas de mapeo de columnas desde el asistente de
  importación CSV/Excel.
- Duplicar la pieza seleccionada (`Editar → Duplicar pieza`, Ctrl+D) con
  undo/redo.
- Diálogo de cambios sin guardar con nombre del proyecto, ruta o aviso de
  «aún no guardado», botones traducidos y error explícito si falla el
  guardado.
- Diálogo «Nuevo proyecto» con nombre y unidades; `project_id` único y
  evento `WorkspaceOpened` al abrir el Workspace (FLW-001).
- Editar pieza o tablero con undo/redo (`EditPieceCommand` /
  `EditBoardCommand`), actualizando ids en colocaciones.
- Menú contextual en el Explorador: editar/duplicar/eliminar pieza,
  editar tablero, añadir en categorías y vista previa de solución.
- Eliminar tablero desde el Explorador con undo (`DeleteBoardCommand`);
  se quitan colocaciones del tablero y se conservan las piezas.
- Renombrar proyecto (`Proyecto → Renombrar…` o clic derecho en la raíz
  del Explorador) con undo, sin marcar soluciones como desactualizadas.
- Diálogo **Ayuda → Atajos de teclado…** con catálogo compartido
  (`studio/keyboard_shortcuts.py`); incluye atajos de archivo (Ctrl+N/O/S)
  y preferencias además de undo/redo/rotar/duplicar/eliminar.
- Menú **Ver**: Ajustar al tablero (Ctrl+0) y Mostrar cuadrícula (Ctrl+G),
  persistiendo `show_grid` sin resetear el zoom.
- Vaciar lista de proyectos recientes desde **Archivo → Abrir recientes**
  o la pantalla de bienvenida (confirma; no borra ficheros).
- Menús **Generar** y **Comparar** poblados (Calcular layout; navegar/aplicar
  solución); se elimina el menú Herramientas vacío.
- Menú **Ver**: Acercar / Alejar (Ctrl+= / Ctrl+-), además de ajustar y
  cuadrícula.
- Higiene de proyectos recientes: se podan rutas inexistentes al refrescar
  el menú/bienvenida, y se quita la entrada si falla al abrir.
- Tips en la barra de estado al pasar el ratón sobre las acciones de menú
  (`setStatusTip`, i18n es/en).
- Ruta del proyecto en la barra de estado (permanente) y
  **Proyecto → Abrir carpeta del proyecto** (también en el Explorador).
- **Editar → Seleccionar todas las piezas** (Ctrl+A) en el Workspace.
- **Editar → Deseleccionar piezas** (Escape) para limpiar la selección del
  canvas.
- **Editar → Invertir selección** (Ctrl+Shift+I) en el Workspace.
- CTA de primeros pasos en el Workspace cuando el proyecto no tiene
  tableros ni piezas (añadir/importar).
- Barra de herramientas principal (archivo, undo, zoom, generar, comparar,
  exportar) con toggle en **Ver**.
- Persistencia de geometría de ventana y disposición de docks/toolbar en
  preferencias (se restaura al reabrir Studio).
- Clic izquierdo en el canvas vacío (o fuera de una pieza) deselecciona.
- Duplicar tablero desde el menú contextual del Explorador (con undo).
- Contadores en cabeceras del Explorador: Tableros/Piezas/Soluciones `(n)`.
- Selección de pieza en el Workspace se refleja en el Explorador (y se limpia
  al deseleccionar).
- Selección desde el Explorador: Inspector de pieza completo (posición/panel) y
  al elegir un tablero se limpia la selección del canvas.
- Confirmación al eliminar una pieza (menú, Backspace o Explorador), alineada
  con la de tableros.
- Seleccionar un tablero en el Explorador lo resalta y centra en el Workspace.
- Clic en un tablero del canvas lo enfoca y sincroniza Explorador e Inspector.
- Menú Ver: mostrar/ocultar Explorador, Inspector, Timeline y Comparador.
- Nivel de zoom del Workspace como porcentaje en la barra de estado.
- Desplazar el Workspace con el botón medio del ratón (también sobre piezas).
- Doble clic en una solución del Explorador para verla en vista previa.
- Tecla Delete como atajo alternativo a Backspace para eliminar pieza;
  Ayuda → Atajos muestra también las secuencias alternativas.
- Menú Ver → Restablecer disposición de ventana (docks, toolbar y tamaño).
- Copiar ID de pieza/tablero desde el menú contextual del Explorador.
- Renombrar pieza/tablero desde el menú contextual del Explorador (con undo).
- Desplazar el Workspace con Espacio + arrastre (además de botón medio/derecho).
- Centrar la cámara al seleccionar una pieza en el Explorador.
- Renombrar con F2 la pieza, tablero o proyecto seleccionado.
- Doble clic en pieza/tablero del canvas para editar (vacío ajusta la vista).
- Mover la pieza seleccionada con las flechas (Shift = 10 mm).
- Editar pieza/tablero seleccionado con Enter (Editar…).
- Icono propio de BoardComposer Studio (ventana / Acerca de).
- Ver → Ajustar a la selección (Ctrl+Shift+0).
- Copiar ID de la pieza/tablero seleccionado (Ctrl+Shift+C).
- Shift+flechas mueven la pieza según el tamaño de cuadrícula.
- Ctrl+D duplica la pieza o el tablero seleccionado/enfocado.
- Delete/Backspace elimina la pieza o el tablero seleccionado/enfocado.
- Re Pág / Av Pág navegan entre soluciones candidatas (Comparar).
- Ctrl+Shift+Return aplica la solución candidata al proyecto.
- Ctrl+Shift+E exporta la solución seleccionada.
- Ctrl+Shift+P abre el diálogo para añadir una pieza.
- Ctrl+Shift+B abre el diálogo para añadir un tablero.
- Ctrl+Shift+O importa piezas desde CSV o Excel.
- Ctrl+Shift+T importa inventario de tableros desde CSV o Excel.
- Ctrl+Shift+L exporta el historial del Timeline.
- Ctrl+Shift+H vuelve a la pantalla de inicio.
- Ctrl+Shift+R abre la carpeta del archivo `.bcproj`.
- F1 abre el catálogo de atajos de teclado.
- Ctrl+Shift+W restablece la disposición de docks, toolbar y ventana.
- Ctrl+Shift+N crea un proyecto desde una plantilla.
- Ctrl+Shift+M guarda el proyecto actual como plantilla.
- Ctrl+Shift+U abre las novedades del CHANGELOG.
- Ctrl+Shift+D abre el proyecto de ejemplo.
- Shift+F1 abre la documentación local.
- Ctrl+Shift+A abre Acerca de BoardComposer.
- Ctrl+Shift+F2 renombra el proyecto actual.
- Ctrl+Q cierra BoardComposer Studio.
- Ctrl+Shift+X vacía la lista de proyectos recientes.
- Ctrl+Shift+K muestra u oculta la barra de herramientas.
- Ctrl+1 muestra u oculta el Explorador.
- Ctrl+2 muestra u oculta el Inspector.
- Ctrl+3 muestra u oculta el Timeline.
- Ctrl+4 muestra u oculta el Comparador de soluciones.
- Tip de estado de Calcular layout incluye Ctrl+Return.
- Tip de estado de Guardar incluye Ctrl+S.
- Tip de estado de Mostrar cuadrícula incluye Ctrl+G.
- Tip de estado de Deshacer incluye Ctrl+Z.
- Tip de estado de Rehacer incluye Ctrl+Shift+Z.
- Tip de estado de Rotar pieza incluye R.
- Importación CSV de piezas ya no apila todas en la misma esquina.
- Tip de estado de Abrir incluye Ctrl+O.
- Cierre de Studio tolera Ctrl+C / SIGINT sin traceback en closeEvent.
- Tip de estado de Nuevo proyecto incluye Ctrl+N.
- Tip de estado de Guardar como incluye Ctrl+Shift+S.
- Tip de estado de Preferencias incluye Ctrl+,.
- Tip de estado de Ajustar al tablero incluye Ctrl+0.
- Tip de estado de Ajustar a la selección incluye Ctrl+Shift+0.
- Tip de estado de Acercar incluye Ctrl+=.
- Tip de estado de Alejar incluye Ctrl+-.
- Tip de estado de Seleccionar todas las piezas incluye Ctrl+A.
- Tip de estado de Deseleccionar piezas incluye Escape.
- Tip de estado de Invertir selección incluye Ctrl+Shift+I.
- Tip de estado de Duplicar incluye Ctrl+D.
- Tip de estado de Editar selección incluye Return.
- Tip de estado de Renombrar selección incluye F2.
- Tip de estado de Copiar ID de selección incluye Ctrl+Shift+C.
- Tip de estado de Eliminar incluye Backspace o Delete.
- Tip de estado de Solución anterior incluye Re Pág / Page Up.
- Tip de estado de Solución siguiente incluye Av Pág / Page Down.
- Tip de estado de Aplicar layout incluye Ctrl+Shift+Return.
- Tip de estado de Exportar solución incluye Ctrl+Shift+E.
- Tip de estado de Exportar Timeline incluye Ctrl+Shift+L.
- Tip de estado de Salir incluye Ctrl+Q.
- Tip de estado de Restablecer disposición de ventana incluye Ctrl+Shift+W.
- Tip de estado de Atajos de teclado incluye F1.
- Tip de estado de Novedades incluye Ctrl+Shift+U.
- Tip de estado de Documentación incluye Shift+F1.
- Tip de estado de Acerca de incluye Ctrl+Shift+A.
- Tip de estado de Vaciar lista de recientes incluye Ctrl+Shift+X.
- Tip de estado de Barra de herramientas incluye Ctrl+Shift+K.
- Tip de estado de Explorador incluye Ctrl+1.
- Tip de estado de Inspector incluye Ctrl+2.
- Tip de estado de Timeline incluye Ctrl+3.
- Tip de estado de Comparador de soluciones incluye Ctrl+4.
- Tip de estado de Nuevo proyecto demo incluye Ctrl+Shift+D.
- Tip de estado de Pantalla de inicio incluye Ctrl+Shift+H.
- Tip de estado de Nuevo desde plantilla incluye Ctrl+Shift+N.
- Tip de estado de Guardar como plantilla incluye Ctrl+Shift+M.
- Tip de estado de Renombrar proyecto incluye Ctrl+Shift+F2.
- Tip de estado de Abrir carpeta del proyecto incluye Ctrl+Shift+R.
- Tip de estado de Añadir tablero incluye Ctrl+Shift+B.
- Tip de estado de Añadir pieza incluye Ctrl+Shift+P.
- Tip de estado de Importar inventario de tableros incluye Ctrl+Shift+T.
- Tip de estado de Importar piezas incluye Ctrl+Shift+O.
- CI y deps de desarrollo fijan `ruff==0.15.22` para evitar roturas con 0.16.

### Cambiado

- Fase 3 descompuesta en EP-001…003 (API, batch, integraciones);
  DOC-003/004, INDEX y ROADMAP enlazados; IDE-0006 → 🔵 P1.
- Preview import CSV: filas con error usan `invalid_fill` del tema canvas
  (Industrial madera light/dark) en vez de un rosa fijo.
- `polish_dialog_button_box` también en import/preview, mapeo, plantillas y
  ayuda (What's New / About / Atajos).
- Inspector + diálogos: `#inspectorPanel`, OK primario en formularios,
  checkbox/button-box tokenizados; preview export sin QSS inline.
- FLW-006 / DOC-003: añadir tablero/pieza pasa por Command (undo dedicado).
- Workspace empty overlay + chrome docks/toolbar alineados a Industrial
  madera (targets CTA, títulos de dock, splitter).
- Tema Industrial madera: CTA light con tinta sobre ámbar (WCAG AA), focus
  visible en botones/listas, targets Welcome y banner outdated con mejor
  contraste en dark.
- DOC-003 Roadmap v1.2 alineado con Studio (Fase 2 núcleo operativo; Fase 3
  como siguiente bloque; prioridades P0/P1 actualizadas).
- ROADMAP Fase 2, checklist UAT Studio y DOC-004 (IDE-0002/0005) alineados
  con el Studio tras el sync SCR/FLW.
- FLW-001 Crear proyecto alineado con el Studio real (Ctrl+N, diálogo
  nombre/unidades, demo/plantilla y `ProjectCreated`).
- FLW-002 Importar CSV/Excel alineado con el Studio real (Ctrl+Shift+T/O,
  mapeo/plantillas, preview, undo y `CsvImported`).
- FLW-005 Exportar alineado con el Studio real (Ctrl+Shift+E, diálogo
  SCR-007, Timeline Ctrl+Shift+L y post-export abrir/revelar).
- FLW-004 Comparar alineado con el Studio real (navegación de candidatas,
  diffs ≥2, referencia, apply/export y banner outdated).
- FLW-003 Generar soluciones alineado con el Studio real (progreso
  cancelable, ranking/`max_solutions`, 0/1/N candidatas y eventos Timeline).
- SCR-007 Exportación alineada con el Studio real (diálogo de solución,
  formatos SVG/DXF/PDF/JSON/CSV, plantillas, Timeline aparte).
- SCR-006 Preferencias alineada con el Studio real (grupos, campos,
  `preferences.json`, apply al OK y límites).
- SCR-001 Pantalla de inicio alineada con el Studio real (hero brand-first,
  CTAs, recientes con miniatura y vuelta con Ctrl+Shift+H).
- SCR-004 Inspector alineado con el Studio real (texto contextual RO,
  pieza/tablero/solución, retales, diagnóstico y sync).
- SCR-005 Proyecto alineado con el Studio real (ciclo `.bcproj`, plantillas,
  import CSV/Excel, Explorador y atajos).
- SCR-003 Comparador alineado con el Studio real (tabla, miniaturas, sort,
  filtro, highlights, diff vs referencia y límites con 0/1 candidata).
- MASTERPLAN y SCR-002 alineados con el Workspace real (arrastre entre
  paneles, material/espesor, límites de candidatas).
- El pipeline utiliza MaxRects cuando el proyecto declara inventario físico.
- El scoring de aprovechamiento usa el área de panel consumida.
- La deduplicación incluye la asignación física de panel.
- README, contexto de IA, roadmap, backlog y documentación técnica alineados.
- Versión de paquete actualizada a `0.4.0.dev0`.

### Compatibilidad

- Los proyectos sin `StockPanel` conservan restricciones y coordenadas legacy.
- Los ficheros Studio versión 1 cargan espesor 19 mm, cantidad 1 y panel sin
  asignar como valores por defecto (ahora vía migración explícita v1→v2).

### Documentación y limpieza

- README, ROADMAP, TODO, AI_CONTEXT, DECISIONS y masterplan (INDEX,
  DOC-003/004/005/006) alineados con el estado post-PR #21.
- Checklist UAT multipanel en `uat/multipanel/CHECKLIST.md`.
- Eliminados prototipos obsoletos (`workbench/`, `tools/visualize_demo.py`,
  `out/demo.html`) y directorios vacíos.

## 0.3.0-stable — 2026-07-11

### Añadido-1

- Edición de proyectos, tableros y piezas en Studio.
- Generación, selección y aplicación de varias soluciones.
- Exportación SVG y persistencia de proyectos.
- Validación, evaluación y deduplicación centralizadas.

## 0.1-prototype — 2026-06-27

### Añadido-2

- Primer motor funcional con layouts básicos y free-space.
- CLI, CSV, presentadores y pruebas iniciales.

## 0.0.1 — 2026-06-26

### Añadido-3

- Documentación fundacional.
- Estructura base del proyecto.
- Backlog y decisiones iniciales.
