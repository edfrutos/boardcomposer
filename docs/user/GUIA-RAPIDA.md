# Guía rápida — BoardComposer Studio

Para carpinteros y talladores que usan la app día a día.
Detalle de producto y arquitectura: [`../masterplan/INDEX.md`](../masterplan/INDEX.md).

> **Atajos en macOS:** **Cmd** = **⌘** (Command), **Alt** = **⌥** (Option), **Shift** = **⇧** (en Windows/Linux, **Cmd** equivale a **Ctrl**).

## Arranque

```bash
make run
# o
.venv/bin/python -m studio.app
```

## Pantalla de inicio

Welcome (**Cmd+Shift+H** para volver). CTAs: nuevo, abrir, importar piezas,
demo (**Cmd+Shift+D**), desde plantilla, docs, novedades (**Cmd+Shift+U**),
preferencias, atajos (**F1**), acerca de (**Cmd+Shift+A**).

- **Recientes:** clic o Enter abre; menú: anclar / carpeta / quitar.
  **Delete** / **Backspace** quita de la lista; **Vaciar lista**
  (**Cmd+Shift+X**) limpia todo.
- Sin recientes: mensaje vacío. Plantilla deshabilitada si no hay catálogo.

## Flujo típico

1. **Nuevo proyecto** (**Cmd+N**) — nombre y unidades (mm / pulgadas).
   Opcional: cliente / referencia / notas (**Cmd+Alt+M**).
2. **Añadir tableros** (**Cmd+Shift+B**) y **piezas** (**Cmd+Shift+P**), o
   importar CSV/Excel (**Cmd+Shift+T** / **Cmd+Shift+O**). El material es
   un combo del **catálogo** (**Cmd+Alt+T**; archivo de usuario, no va en
   el `.bcproj`; precio opcional €/m²; medidas L×A típicas de tablero;
   **Exportar/Importar** JSON para otro PC, sin nube). Tableros y piezas
   **nuevos** arrancan con el material por defecto de Preferencias
   (semilla «Melamina blanca»); el CSV no lo usa.
   En cada pieza,
   «Permitir rotación» desmarcado fija la
   **veta** (el cálculo y **R** no giran esa pieza). Espesor de sierra del
   proyecto: **Cmd+Alt+K**.
3. **Calcular layout** (**Cmd+Return**) — hace falta ≥1 tablero y ≥1 pieza;
   genera soluciones candidatas (con varios tableros compara MaxRects y
   Skyline). El **Workspace** muestra preview de la mejor candidata
   sin aplicar; **Cmd+Shift+Return** la conserva.
4. Revisar en **Workspace** (paneles, piezas, cámara).
5. Comparar en **Comparador** (**Cmd+4**): **Re Pág** / **Av Pág** entre
   candidatas; **Cmd+Shift+Return** aplica la elegida. Si editas el
   inventario después de calcular, el banner avisa y ofrece **Calcular
   layout**; al aplicar o exportar con soluciones viejas, el diálogo prioriza
   **Calcular layout** frente a continuar de todos modos.
6. **Exportar** la solución (**Cmd+Shift+E**): SVG / PNG / JPEG / PDF / DXF /
   JSON / CSV. **Lista de corte** de taller (**Cmd+Alt+C**): CSV o PDF.
7. **Guardar** (**Cmd+S**) el proyecto `.bcproj`.

## Revisiones locales del `.bcproj`

Al **Guardar** sobre un archivo ya existente, Studio copia la versión anterior
en una carpeta oculta junto al proyecto (`.<nombre>.bcproj.revs/`, máx. 10).

| Acción | Cómo |
|---|---|
| Comparar | **Proyecto → Comparar revisiones .bcproj…** (**Cmd+Shift+Y**) |
| Restaurar la última | **Proyecto → Restaurar última revisión local…** (**Cmd+Alt+Y**) |
| Restaurar una concreta | En el diálogo de comparar, elige revisión → **Restaurar esta revisión…** |
| Backup (anillo + archivo) | **Proyecto → Exportar backup de revisiones…** (**Cmd+Alt+B**; luego Abrir carpeta) o CLI `boardcomposer-backup` |

La restauración carga el snapshot **en memoria** (misma ruta del archivo).
Queda pendiente de **Guardar** para escribirlo en disco. La pila Deshacer se
vacía al restaurar o al abrir otro proyecto.

Tras **Calcular layout**, **Ayuda → Explicar candidata…** (**Cmd+Alt+E**)
muestra fortalezas / debilidades / notas de la solución seleccionada (sin IA
en red; puedes **Copiar**).

## Atajos útiles

| Acción | Atajo |
|---|---|
| Nuevo / Abrir / Guardar | Cmd+N / Cmd+O / Cmd+S |
| Guardar como | Cmd+Shift+S |
| Abrir carpeta del proyecto | Cmd+Shift+R |
| Copiar ruta del .bcproj | Cmd+Alt+Shift+C |
| Preferencias | Cmd+, |
| Añadir tablero / pieza | Cmd+Shift+B / Cmd+Shift+P |
| Importar tableros / piezas (CSV/Excel) | Cmd+Shift+T / Cmd+Shift+O |
| Calcular layout | Cmd+Return |
| Re-empaquetar omitidas (congelar OK) | Cmd+Alt+F |
| Añadir retales al inventario | Cmd+Alt+R |
| Catálogo de materiales / espesores / L×A | Cmd+Alt+T |
| Aplicar layout del Comparador | Cmd+Shift+Return |
| Candidata anterior / siguiente | Re Pág / Av Pág |
| Exportar solución | Cmd+Shift+E |
| Exportar lista de corte (CSV/PDF) | Cmd+Alt+C |
| Exportar historial Timeline | Cmd+Shift+L |
| Replay Timeline (lista enfocada) | Espacio / Inicio / ← / → |
| Comparar revisiones `.bcproj` | Cmd+Shift+Y |
| Restaurar última revisión local | Cmd+Alt+Y |
| Exportar backup de revisiones | Cmd+Alt+B |
| Explicar candidata | Cmd+Alt+E |
| Deshacer / Rehacer | Cmd+Z / Cmd+Shift+Z |
| Rotar pieza | R (no si la veta está fija) |
| Intercambiar dos piezas colocadas | Cmd+Alt+X |
| Sugerir hueco | Cmd+Alt+G |
| Metadatos del proyecto | Cmd+Alt+M |
| Espesor de sierra / kerf | Cmd+Alt+K |
| Copiar espesor de sierra | Cmd+Alt+Shift+K |
| Mover pieza seleccionada | Flechas (Shift = tamaño cuadrícula) |
| Seleccionar todas / Deseleccionar / Invertir | Cmd+A / Escape / Cmd+Shift+I |
| Editar selección / Copiar ID / Copiar medidas | Return / Cmd+Shift+C / Cmd+Alt+Shift+D |
| Copiar medidas del tablero | Cmd+Alt+Shift+B |
| Copiar espesor del tablero | Cmd+Alt+Shift+T |
| Copiar material del tablero | Cmd+Alt+Shift+M |
| Copiar aprovechamiento del tablero | Cmd+Alt+Shift+U |
| Copiar material libre del tablero | Cmd+Alt+Shift+F |
| Copiar piezas colocadas | Cmd+Alt+Shift+P |
| Copiar piezas omitidas | Cmd+Alt+Shift+O |
| Copiar tableros físicos | Cmd+Alt+Shift+N |
| Copiar selección de la barra | Cmd+Alt+Shift+S |
| Renombrar selección | F2 |
| Renombrar proyecto | Cmd+Shift+F2 |
| Duplicar / Eliminar | Cmd+D / Backspace o Delete |
| Cuadrícula | Cmd+G |
| Ajustar al tablero / selección | Cmd+0 / Cmd+Shift+0 |
| Zoom al 100% | Cmd+Alt+0 |
| Copiar zoom | Cmd+Alt+Shift+Z |
| Copiar retales | Cmd+Alt+Shift+R |
| Copiar índice de la solución | Cmd+Alt+Shift+L |
| Copiar huecos internos | Cmd+Alt+Shift+G |
| Copiar estrategia | Cmd+Alt+Shift+Y |
| Copiar piezas de la solución | Cmd+Alt+Shift+J |
| Copiar omitidas de la solución | Cmd+Alt+Shift+Q |
| Copiar tableros de la solución | Cmd+Alt+Shift+W |
| Copiar puntuación de la solución | Cmd+Alt+Shift+V |
| Zoom + / − (también rueda) | Cmd+= / Cmd+- |
| Desplazar cámara (pan) | Botón medio / derecho / Espacio+arrastre |
| Nuevo desde plantilla | Cmd+Shift+N |
| Guardar como plantilla | Cmd+Shift+M |
| Pantalla de inicio | Cmd+Shift+H |
| Demo | Cmd+Shift+D |
| Mostrar/ocultar docks | Cmd+1…4 |
| Mostrar/ocultar barra | Cmd+Shift+K |
| Restablecer disposición | Cmd+Shift+W |
| Documentación | Shift+F1 (o Ayuda → Documentación) |
| Atajos / Novedades | F1 / Cmd+Shift+U |
| Acerca de | Cmd+Shift+A |
| Salir | Cmd+Q |

Lista completa: **Ayuda → Atajos de teclado** (**F1**).

## Importar CSV/Excel

- **Tableros:** **Cmd+Shift+T** — id, largo, ancho, espesor, cantidad, material.
  Ejemplo: `data/samples/studio_boards_inventory.csv`.
- **Piezas:** **Cmd+Shift+O** — mismos campos habituales; la cantidad puede
  expandirse a varios IDs.
- Formatos: `.csv` y `.xlsx`. Tras elegir archivo, Studio muestra vista previa
  fila a fila (OK / error) antes de incorporar.

## Workspace

Canvas central del layout.

- Sin tableros ni piezas: overlay con CTAs (añadir / importar).
- **Pan:** botón medio, botón derecho o **Espacio + arrastre**.
- **Zoom:** rueda, **Cmd+=** / **Cmd+-**, ajustar todo (**Cmd+0**),
  zoom al 100% (**Cmd+Alt+0**) o
  selección (**Cmd+Shift+0**). Cuadrícula: **Cmd+G**.
- **Pieza colocada:** **flechas** mueven 1 mm; **Shift+flechas** usan el
  tamaño de cuadrícula (Preferencias); **R** rota 90° (deshabilitado si la
  veta está fija). Con **exactamente dos** piezas colocadas
  seleccionadas, **Cmd+Alt+X** intercambia posiciones (si no caben o el
  material no coincide, no cambia nada; se puede deshacer).
  **Cmd+Alt+G** coloca la pieza seleccionada en un hueco libre (mismo
  panel si ya está colocada; tablero enfocado si no). Un drop que solapa
  ajusta al hueco más cercano; incompatibilidad de material/espesor sigue
  revirtiendo.
- **Selección:** **Cmd+A** / **Escape** / **Cmd+Shift+I**; **Return**
  edita; **Cmd+Shift+C** copia el ID; **Cmd+Alt+Shift+D** copia L×A
  de una sola pieza; **Cmd+Alt+Shift+B** copia L×A de una hoja de tablero
  (la cantidad no multiplica).

## Explorador

Dock **Cmd+1**. Árbol del proyecto: **Tableros**, **Piezas** y **Soluciones**.

- **Doble clic / Return:** edita tablero o pieza; si la pieza está sin
  colocar y hay tablero enfocado en el Workspace, la **coloca** ahí.
  En una solución: vista previa en el Workspace (sin aplicar).
- **Menú contextual:** editar / renombrar (**F2**) / duplicar (**Cmd+D**) /
  copiar ID (**Cmd+Shift+C**) / copiar medidas (**Cmd+Alt+Shift+D**,
  solo piezas; en tableros **Cmd+Alt+Shift+B**) / eliminar; en piezas también
  **Colocar en tablero enfocado**; en categorías, añadir tablero/pieza;
  en el proyecto, renombrar, **Abrir carpeta…** o **Copiar ruta**.
- Piezas sin colocar llevan marca **sin colocar**.

## Inspector

Dock **Cmd+2**. Detalle de la selección y del layout.

- Sin selección: mensaje vacío. Con la **raíz del proyecto** en el
  Explorador: cliente, referencia, notas (**Cmd+Alt+M**), espesor de
  sierra (**Cmd+Alt+K**), conteos (tableros/piezas/soluciones),
  materiales y área de stock. Con las **categorías** del árbol: tipos
  y físicos, retales, colocadas/sin colocar o candidatas. Con
  **tablero** o **pieza**: dimensiones, área (pieza, o una hoja de
  tablero sin multiplicar la cantidad),
  espesor, cantidad, material. **Cmd+Alt+I** copia el texto del dock. En tablero, aprovechamiento (instancias,
  % uso, retales) si hay layout; en piezas, veta (libre o fija) y posición
  o «sin colocar» (con consejo de colocar vía Explorador). Rotación
  `0°`/`90°` si está colocada; `—` si no.
- Tras **Calcular layout**: métricas de la candidata (piezas, huecos,
  material libre, coste de tableros si el catálogo tiene €/m², omitidas,
  puntos clave). Largos, anchos y área de retales usan las **unidades**
  de Preferencias (mm / cm / in). El proyecto sigue guardando mm.
- **Retales** son **informativos** — no inventario reutilizable automático.
- Si el inventario cambió tras calcular, el Inspector también avisa de
  soluciones desactualizadas.

## Comparador

Dock **Cmd+4**. Candidatas tras **Calcular layout**.

- **Ordenar por:** ranking del solver, piezas, huecos, tablero libre,
  coste material, puntuación.
- **Solo soluciones completas:** oculta candidatas parciales.
- **Fijar como referencia** (≥2 soluciones): marca la candidata y muestra
  el diff frente a ella. Largo, ancho y coords del diff usan las
  **unidades** de Preferencias (mm / cm / in).
- Navegar: **Re Pág** / **Av Pág**; **Cmd+Shift+Return** aplica la elegida
  al proyecto.
- **Generar → Re-empaquetar omitidas** (**Cmd+Alt+F**): congela las piezas
  ya colocadas de la candidata parcial y solo intenta colocar las omitidas
  en retales y tableros libres. No sustituye a Calcular layout.
- **Generar → Añadir retales al inventario** (**Cmd+Alt+R**): crea tableros
  remnant con las medidas de los retales ≥ 50 mm. No baja solo la cantidad
  de tableros ya cortados; hazlo antes del próximo cálculo. Se puede
  deshacer.
- Si editas inventario después de calcular, el banner avisa y el CTA
  **Calcular layout** recalcula; tips de aplicar / navegar / explicar
  también lo advierten.
- **Ayuda → Explicar candidata…** (**Cmd+Alt+E**): fortalezas / debilidades
  / notas (sin IA en red; puedes **Copiar**).

## Timeline

Dock **Cmd+3**. Historial de eventos del proyecto (cálculos, movimientos,
marcadores…).

- **Seguir:** mantiene la vista en el último evento.
- **Filtros:** combos de evento / algoritmo / periodo; botones **Solo
  movimientos** y **Solo marcadores**; **Limpiar filtros** si hay alguno
  activo.
- **Marcador…:** pide una nota; si hay replay activo, guarda paso/algoritmo.
- **Replay:** tras **Calcular layout**, modo colocaciones o fases del solver +
  velocidad. Con la lista enfocada: **Espacio** play/pausa, **Inicio**
  reinicia, **←** / **→** paso a paso.
- **Exportar…** (**Cmd+Shift+L**) respeta los filtros visibles; **Vaciar**
  pide confirmación. **Cmd+C** (lista enfocada) copia la **línea** del
  evento; el menú contextual ofrece también el **payload JSON**.

## Exportar

**Archivo → Exportar…** (**Cmd+Shift+E**) exporta la **solución seleccionada**.

- Formatos: SVG / PNG / JPEG / PDF / DXF / JSON / CSV. Vista previa según
  opciones (métricas y explicación solo JSON; retales; **etiquetas** de
  pieza con id y LxW y de retal con LxW según las **unidades** de
  Preferencias; **cotas L×A** del tablero y **trazabilidad** (versión,
  algoritmo, fecha) en el plano SVG/PDF/DXF/raster).
  El JSON de Studio incluye coste estimado si el catálogo tiene precio €/m².
  En **PDF** de plano: papel (ajustar al dibujo, A4, A3, Letter),
  orientación, escala (ajustar o 1:n) y márgenes mm. Lista de corte y
  presupuesto PDF siguen en A4.
  En **PNG/JPEG**: resolución DPI (36–300, default 96) y, en JPEG,
  calidad 1–100 (default 90).
  En **DXF**: capas `PANELS` / `PIECES` / `OFFCUTS` / `DIMS` / `SEQ` /
  `META` (el CAD puede ocultar cotas o el pie).
  **Lote:** marca «Exportar las N candidatas del ranking» y elige carpeta;
  un archivo numerado por candidata (`boardcomposer-solution-01…`). El CLI
  `boardcomposer-batch` sigue siendo para carpetas de proyectos, no para
  el Comparador.
- **Archivo → Exportar lista de corte…** (**Cmd+Alt+C**) es otro flujo:
  CSV o PDF de taller (piezas, tableros y **secuencia de sierra** por
  panel). El **PDF** usa las unidades de Preferencias (mm/cm/in) y el pie
  de trazabilidad (versión, algoritmo, fecha); el CSV sigue en mm y no
  lleva pie. Recuerda carpeta y formato. El plano SVG/PDF/DXF
  numera cada pieza con ese orden. No sustituye el CSV de colocaciones
  del diálogo de solución.
- **Archivo → Exportar presupuesto…** (**Cmd+Alt+Q**) PDF de coste de
  material: tableros físicos consumidos × €/m² del catálogo, más mano
  de obra si Preferencias tiene EUR/h y minutos/pieza (0 = omitir),
  con el mismo pie de trazabilidad. LxW y espesor del PDF siguen las
  unidades de Preferencias; el área sigue en m². No incluye herrajes.
  Recuerda la carpeta. No sustituye el JSON de métricas.
- **Cliente** y **plantilla** reutilizan un perfil; **Guardar…** / **Eliminar**
  gestionan el catálogo; **Exportar/Importar pack…** comparte plantillas
  (recuerda la última carpeta).
- Al terminar: diálogo con **Abrir archivo** / **Abrir carpeta**.
- Si las soluciones están desactualizadas, el diálogo prioriza **Calcular
  layout** antes de continuar.

## Preferencias

**Editar → Preferencias** (**Cmd+,**). Globales: **no** van en el `.bcproj`.

- **General:** idioma, tema (sistema / claro / oscuro), unidades
  (Inspector, Workspace y etiquetas de plano; disco sigue mm).
- **Workspace:** mostrar cuadrícula y tamaño (afecta **Shift+flechas**).
- **Algoritmos:** estrategia y pesos opcionales.
- **Exportación:** formato por defecto y opciones (métricas / explicación
  JSON, retales, etiquetas de piezas y de retales, cotas de tablero,
  trazabilidad, DPI y calidad JPEG, mano de obra EUR/h y min/pieza).
- **Avanzado:** máx. soluciones a conservar; **material por defecto**
  de tableros y piezas nuevos (combo del catálogo; no va en el
  `.bcproj`); **Catálogo de materiales** (nombres, espesores, medidas
  L×A, precio €/m²); **Exportar / importar preferencias** (JSON de
  taller: fusionar o reemplazar; no incluye carpetas locales ni
  ventana; OK guarda); **perfiles de taller** (guardar / aplicar /
  eliminar; locales, no van en el pack); **Abrir carpeta de
  configuración…**
  (`preferences.json`); **Restaurar valores**.

## Plantillas de proyecto

Inventario reutilizable (tableros / piezas), distinto de las **plantillas de
exportación**.

- **Guardar como plantilla…** (**Cmd+Shift+M**): pide nombre; opcional
  incluir colocaciones actuales. Requiere proyecto abierto.
- **Nuevo desde plantilla…** (**Cmd+Shift+N** o Welcome): elige plantilla;
  opcional restaurar colocaciones; renombrar / eliminar desde el diálogo.
- Sin catálogo, el atajo/botón queda deshabilitado (tip honesto).

## Disposición

Chrome de Studio (se recuerda entre sesiones).

- **Docks:** Explorador (**Cmd+1**), Inspector (**Cmd+2**), Timeline
  (**Cmd+3**), Comparador (**Cmd+4**).
- **Barra de herramientas:** mostrar/ocultar (**Cmd+Shift+K**).
- **Restablecer disposición** (**Cmd+Shift+W**): docks, toolbar y tamaño
  de ventana a valores iniciales (status: «Disposición de ventana
  restablecida»).

## Consejos

- **Barra de estado:** con proyecto guardado muestra el nombre del `.bcproj`
  (tooltip = ruta completa); **clic** abre la carpeta (igual que
  **Cmd+Shift+R**). Sin guardar: «Proyecto aún no guardado» — tip pide
  **Cmd+S** antes de poder abrir carpeta. Entre el nombre y el **%** va
  piezas colocadas / total (`1/2`; tooltip «Piezas colocadas: 1 de 2»).
  **Clic** encuadra esas colocadas (no el tablero ni la selección).
  **Cmd+Alt+Shift+P** copia `1/2`, como el rótulo.
  Las omitidas van como `2 om.` (inventario sin colocación; oculto si
  es 0). **Clic** las selecciona y encuadra si están en el Workspace.
  **Cmd+Alt+Shift+O** copia el número, sin `om.`.
  Los tableros físicos van como `3 tab.` (suma de cantidades; oculto si
  no hay). **Clic** encuadra todos los tableros (**Cmd+0**).
  **Cmd+Alt+Shift+N** copia el número, sin `tab.`. El espesor
  del tablero va como `esp. 19 mm` (el enfocado, o el único tipo; oculto
  si hay varios y ninguno enfocado). **Clic** abre la edición de ese
  tablero. El material va como `mat. Demo` (el mismo tablero; oculto
  si el material está vacío). **Clic** abre la edición de ese tablero.
  **Cmd+Alt+Shift+M** copia ese material. El aprovechamiento del
  tablero enfocado va como `uso 24.0%` (la misma fórmula que el
  Inspector; oculto sin foco o sin uso). **Clic** selecciona ese tablero.
  **Cmd+Alt+Shift+U** copia el porcentaje (`24.0%`), sin el prefijo.
  El material libre va como `libre 76.0%` (complemento del
  aprovechamiento; la misma visibilidad). **Clic** selecciona ese tablero.
  **Cmd+Alt+Shift+F** copia el porcentaje (`76.0%`), sin el prefijo.
  Si hay piezas seleccionadas en el Workspace, aparece `1 sel.` / `2 sel.`
  (oculta si no hay selección). **Clic** en `n sel.` ajusta el encuadre
  (**Cmd+Shift+0**). **Cmd+Alt+Shift+S** copia el número, sin `sel.`.
  El kerf del proyecto va como `kerf 3.2 mm`
  (unidades de Preferencias; oculto si no hay proyecto). **Clic** lo
  edita (**Cmd+Alt+K**). **Cmd+Alt+Shift+K** copia ese espesor
  (unidades de Preferencias; kerf 0 también). El
  **%** es el zoom del Workspace
  (rueda, **Cmd+=** / **Cmd+-**, **Cmd+0**). **Clic** en el **%**
  vuelve al 100% (**Cmd+Alt+0**); si ya está, el cursor no es mano.
  **Cmd+Alt+Shift+Z** copia ese porcentaje, sin volver al 100%.
  Los retales de la solución seleccionada van como `2 ret.` (oculto si
  no hay solución o si es 0). **Clic** selecciona su tablero. No encuadra
  ni promociona. **Cmd+Alt+Shift+R** copia el
  número, sin `ret.`.
  La solución seleccionada va como `1/2 sol.` (oculto si no hay
  solución o si el índice no mapea). **Clic** pasa a la siguiente.
  No aplica el layout ni cambia el zoom. Arrastre no.
  **Cmd+Alt+Shift+L** copia `1/2`, sin `sol.`. No avanza.
  Los huecos internos van como `hueco 0.0%` (en inglés `gap 0.0%`).
  La misma visibilidad que el índice. `0.0%` se muestra.
  **Clic** selecciona esa solución en el explorador. No avanza ni
  aplica el layout. Arrastre no.
  **Cmd+Alt+Shift+G** copia el porcentaje, sin `hueco`. No avanza.
  La estrategia va como `est. material` (en inglés `str. material`).
  La misma visibilidad que el índice. Sin nombre: `est. desconocida`.
  Cursor mano si está visible. **Clic** selecciona esa solución en
  el explorador. No avanza ni aplica el layout. Arrastre no.
  **Cmd+Alt+Shift+Y** copia el nombre (`material`, `desconocida`),
  sin `est.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las piezas de esa solución van como `0 pza` (en inglés `0 pcs`).
  La misma visibilidad que el índice. `0` se muestra. Distinto de
  colocadas/total. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout.
  Arrastre no.
  **Cmd+Alt+Shift+J** copia el número (`0`, `2`), sin `pza`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  Las omitidas de esa solución van como `fuera 0` (en inglés `out 2`).
  La misma visibilidad que el índice. `0` se muestra. Distinto de
  `n om.`. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout.
  Arrastre no.
  **Cmd+Alt+Shift+Q** copia el número (`0`, `2`), sin `fuera`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  Los tableros usados por esa solución van como `pan. 0` (en inglés
  `pnl 2`). La misma visibilidad que el índice. `0` se muestra.
  Distinto de `n tab.`. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout.
  Arrastre no.
  **Cmd+Alt+Shift+W** copia el número (`0`, `2`), sin `pan.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de esa solución va como `pts. 0.00` (en inglés
  `pts 0.75`). La misma visibilidad que el índice. `0.00` se muestra.
  Cursor mano si está visible. **Clic** selecciona esa solución en el
  explorador. No avanza ni aplica el layout. Arrastre no.
  **Cmd+Alt+Shift+V** copia el valor (`0.00`, `0.75`), sin `pts.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  El tablero libre de esa solución va como `sbr. 0.0%` (en inglés
  `rem. 76.0%`). La misma visibilidad que el índice. `0.0%` se muestra.
  Distinto de `libre`. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout. Arrastre no.
  **Cmd+Alt+Shift+E** copia el porcentaje (`0.0%`, `76.0%`), sin `sbr.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  El largo total de esa solución va como `lrg. 0 mm` (en inglés
  `len. 400 mm`). La misma visibilidad que el índice. `0 mm` se muestra.
  Sigue las unidades de Preferencias. Cursor mano si está visible.
  **Clic** selecciona esa solución en el explorador. No avanza ni
  aplica el layout. Arrastre no.
  **Cmd+Alt+Shift+H** copia el largo con unidad (`0 mm`, `400 mm`,
  `40 cm`), sin `lrg.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El ancho total de esa solución va como `anc. 0 mm` (en inglés
  `wid. 300 mm`). La misma visibilidad que el índice. `0 mm` se muestra.
  Sigue las unidades de Preferencias. Cursor mano si está visible.
  **Clic** selecciona esa solución en el explorador. No avanza ni
  aplica el layout. Arrastre no.
  **Cmd+Alt+Shift+X** copia el ancho con unidad (`0 mm`, `300 mm`,
  `30 cm`), sin `anc.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área usada de esa solución va como `ár. 0 mm²` (en inglés
  `area 20000 mm²`). La misma visibilidad que el índice. `0 mm²` se
  muestra. Sigue las unidades de Preferencias. Cursor mano si está
  visible. **Clic** selecciona esa solución en el explorador. No avanza
  ni aplica el layout. Arrastre no.
  **Cmd+Alt+Shift+A** copia el área con unidad (`0 mm²`, `20000 mm²`,
  `200 cm²`), sin `ár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de retales de esa solución va como `retár. 0 mm²` (en inglés
  `offar. 20000 mm²`). La misma visibilidad que el índice (distinto de
  `n ret.`). `0 mm²` se muestra. Sigue las unidades de Preferencias.
  Cursor mano si está visible. Clic selecciona esa solución en el
  explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+I** copia el área con unidad (`0 mm²`, `20000 mm²`,
  `200 cm²`), sin `retár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área envolvente de esa solución va como `env. 0 mm²` (en inglés
  `bnd. 60000 mm²`). La misma visibilidad que el índice. `0 mm²` se
  muestra. Sigue las unidades de Preferencias. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Cmd+Alt+Shift+1** copia el área con unidad (`0 mm²`, `60000 mm²`,
  `600 cm²`), sin `env.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de huecos internos de esa solución va como `hueár. 0 mm²` (en
  inglés `gapar. 30000 mm²`). La misma visibilidad que el índice
  (distinto de `hueco n%`). `0 mm²` se muestra. Sigue las unidades de
  Preferencias. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+2** copia el área con unidad (`0 mm²`, `30000 mm²`,
  `300 cm²`), sin `hueár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de tablero libre de esa solución va como `sbrár. 0 mm²` (en
  inglés `remar. 380000 mm²`). La misma visibilidad que el índice
  (distinto de `sbr. n%`). `0 mm²` se muestra. Sigue las unidades de
  Preferencias. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+3** copia el área con unidad (`0 mm²`, `380000 mm²`,
  `3800 cm²`), sin `sbrár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de tableros consumidos de esa solución va como `panár. 0 mm²`
  (en inglés `pnlar. 500000 mm²`). La misma visibilidad que el índice
  (distinto de `pan. {n}`). `0 mm²` se muestra. Sigue las unidades de
  Preferencias. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+4** copia el área con unidad (`0 mm²`, `500000 mm²`,
  `5000 cm²`), sin `panár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El aprovechamiento de tableros de esa solución va como `aprv. 0.0%`
  (en inglés `util. 24.0%`). La misma visibilidad que el índice
  (distinto de `uso`). `0.0%` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+5** copia el porcentaje (`0.0%`, `24.0%`), sin
  `aprv.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las piezas rotadas de esa solución van como `rot. 0` (en inglés
  `rot 2`). La misma visibilidad que el índice (distinto de `n pza`).
  `0` se muestra. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+6** copia el número (`0`, `2`), sin `rot.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  Las piezas sin rotar de esa solución van como `nrot. 0` (en inglés
  `unrot 2`). La misma visibilidad que el índice (distinto de
  `rot. {n}`). `0` se muestra. Cursor mano si está visible. Clic
  selecciona esa solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+7** copia el número (`0`, `2`), sin `nrot.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  El porcentaje de piezas rotadas de esa solución va como `rot% 0.0%`
  (en inglés `rot% 50.0%`). La misma visibilidad que el índice
  (distinto de `rot. {n}`). `0.0%` se muestra. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Cmd+Alt+Shift+8** copia el porcentaje (`0.0%`, `50.0%`), sin
  `rot%`. Deshabilitado si la etiqueta está oculta. No avanza.
  El porcentaje de piezas sin rotar de esa solución va como
  `nrot% 0.0%` (en inglés `unrot% 75.0%`). La misma visibilidad que el
  índice (distinto de `nrot. {n}`). `0.0%` se muestra. Cursor mano si
  está visible. Clic selecciona esa solución en el explorador; no
  avanza; arrastre no.
  **Cmd+Alt+Shift+9** copia el porcentaje (`0.0%`, `75.0%`), sin
  `nrot%`. Deshabilitado si la etiqueta está oculta. No avanza.
  El aprovechamiento envolvente de esa solución va como `env% 0.0%`
  (en inglés `bnd% 50.0%`). La misma visibilidad que el índice
  (distinto de `aprv.` y `uso`). `0.0%` se muestra. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Cmd+Alt+Shift+0** copia el porcentaje (`0.0%`, `50.0%`), sin
  `env%`. Deshabilitado si la etiqueta está oculta. No avanza.
  El porcentaje de retales de esa solución va como `ret% 0.0%` (en
  inglés `off% 4.0%`). La misma visibilidad que el índice (distinto de
  `n ret.` y `retár.`). `0.0%` se muestra. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Cmd+Alt+Shift+F1** copia el porcentaje (`0.0%`, `4.0%`), sin
  `ret%`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de desperdicio de esa solución va como `ptsh. 0.00`
  (en inglés `ptsw 0.50`). La misma visibilidad que el índice (distinto
  de `pts.`). `0.00` se muestra. Cursor mano si está visible. Clic
  selecciona esa solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+F2** copia el valor (`0.00`, `0.50`), sin
  `ptsh.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de uso de material de esa solución va como `ptsu. 0.00`
  (en inglés `ptsu 0.25`). La misma visibilidad que el índice (distinto
  de `pts.` y `ptsh.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+F3** copia el valor (`0.00`, `0.25`), sin
  `ptsu.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de cortes de esa solución va como `ptsc. 0.00`
  (en inglés `ptsc 0.75`). La misma visibilidad que el índice (distinto
  de `pts.`, `ptsh.` y `ptsu.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+F4** copia el valor (`0.00`, `0.75`), sin
  `ptsc.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de regularidad de esa solución va como `ptsr. 0.00`
  (en inglés `ptsr 0.40`). La misma visibilidad que el índice (distinto
  de `pts.`, `ptsh.`, `ptsu.` y `ptsc.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+F5** copia el valor (`0.00`, `0.40`), sin
  `ptsr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de veta de esa solución va como `ptsv. 0.00`
  (en inglés `ptsg 0.40`). La misma visibilidad que el índice (distinto
  de `pts.`, `ptsh.`, `ptsu.`, `ptsc.` y `ptsr.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+F6** copia el valor (`0.00`, `0.40`), sin
  `ptsv.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La completitud de esa solución va como `comp. sí` (en inglés
  `full yes`; `comp. no` / `full no` si hay piezas omitidas).
  La misma visibilidad que el índice (distinto de `fuera`). Cursor
  mano si está visible. Clic selecciona esa solución en el explorador;
  no avanza; arrastre no.
  **Cmd+Alt+Shift+F7** copia el valor (`sí`, `no`), sin
  `comp.`. Deshabilitado si la etiqueta está oculta. No avanza.
  El área del mayor retal va como `maxr. 20000 mm²` (en inglés
  `maxo 20000 mm²`). Oculta si no hay retales (como `n ret.`;
  distinta de `retár.` y `ret%`). Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza;
  arrastre no. Sigue las unidades de Preferencias.
  **Cmd+Alt+Shift+F8** copia el área con unidad, sin
  `maxr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  El área del menor retal va como `minr. 2500 mm²` (en inglés
  `mino 2500 mm²`). Oculta si no hay retales (como `n ret.` y
  `maxr.`; distinta de `maxr.`, `retár.` y `ret%`). Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza;
  arrastre no. Sigue las unidades de Preferencias.
  **Cmd+Alt+Shift+F9** copia el área con unidad, sin
  `minr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las dimensiones del mayor retal van como `maxd. 200 x 100 mm`
  (en inglés `maxd 200 x 100 mm`). Oculta si no hay retales
  (como `n ret.` y `maxr.`; distinta de `maxr.`, `minr.`, `retár.`
  y `ret%`). Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no. Sigue las
  unidades de Preferencias.
  **Cmd+Alt+Shift+F10** copia el L×A con unidad, sin
  `maxd.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las dimensiones del menor retal van como `mind. 50 x 50 mm`
  (en inglés `mind 50 x 50 mm`). Oculta si no hay retales
  (como `n ret.` y `minr.`; distinta de `minr.`, `maxd.`, `retár.`
  y `ret%`). Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no. Sigue las
  unidades de Preferencias.
  **Cmd+Alt+Shift+F11** copia el L×A con unidad, sin
  `mind.`. Deshabilitado si la etiqueta está oculta. No avanza.
  El área media de retales va como `medr. 11250 mm²` (en inglés
  `avgo 11250 mm²`). Oculta si no hay retales (como `n ret.` y
  `minr.`; distinta de `minr.`, `maxr.`, `retár.` y `ret%`).
  Cursor mano si está visible. Clic selecciona esa solución en el
  explorador; no avanza; arrastre no. Sigue las unidades de Preferencias.
  **Cmd+Alt+Shift+F12** copia el área con unidad, sin
  `medr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  El área mediana de retales va como `mdnr. 5000 mm²` (en inglés
  `medo 5000 mm²`). Oculta si no hay retales (como `n ret.` y
  `medr.`; distinta de `medr.`, `minr.`, `maxr.`, `retár.` y
  `ret%`). Cursor mano si está visible. Clic selecciona esa solución en el
  explorador; no avanza; arrastre no. Sigue las unidades de Preferencias.
  **Cmd+Alt+Shift+-** copia el área con unidad, sin
  `mdnr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las dimensiones del retal de área mediana van como
  `mdnd. 100 x 50 mm` (en inglés `medd 100 x 50 mm`). Oculta si
  no hay retales (como `n ret.` y `mdnr.`; distinta de `mdnr.`,
  `maxd.` y `mind.`). Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no. Sigue las
  unidades de Preferencias.
  **Cmd+Alt+Shift+=** copia el L×A con unidad, sin
  `mdnd.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las dimensiones del retal de área media van como
  `mdds. 100 x 50 mm` (en inglés `avgd 100 x 50 mm`). Oculta si
  no hay retales (como `n ret.` y `medr.`; distinta de `medr.`,
  `mdnd.`, `maxd.` y `mind.`). Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no. Sigue las
  unidades de Preferencias.
  **Cmd+Alt+Shift+[** copia el L×A con unidad, sin
  `mdds.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La amplitud de áreas de retales va como `ampr. 17500 mm²`
  (en inglés `spno 17500 mm²`): mayor área menos menor. Oculta si
  no hay retales (distinta de `maxr.`, `minr.` y `retár.`). Con un
  solo retal se muestra `0`. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no. Sigue las
  unidades de Preferencias.
  **Cmd+Alt+Shift+]** copia el área con unidad, sin
  `ampr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La cuota del mayor retal va como `cmay. 72.7%`
  (en inglés `lsh 72.7%`): mayor área partida por la suma de
  retales. Oculta si no hay retales (distinta de `maxr.`, `retár.`,
  `ret%` y `ampr.`). Con un solo retal se muestra `100.0%`.
  No sigue las unidades. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+\\** copia el porcentaje, sin
  `cmay.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La cuota del menor retal va como `cmen. 9.1%`
  (en inglés `ssh 11.1%`): menor área partida por la suma de
  retales. Oculta si no hay retales (distinta de `cmay.`, `minr.`
  y `retár.`). Con un solo retal se muestra `100.0%`.
  No sigue las unidades. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+;** copia el porcentaje, sin
  `cmen.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La relación de forma del mayor retal va como `relr. 2.00`
  (en inglés `aspr 2.00`): lado largo partido por lado corto.
  Empate por largo y ancho, como `maxd.`. Oculta si no hay
  retales. Un cuadrado muestra `1.00`. No sigue las unidades.
  Distinta de `maxd.`. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+'** copia el valor, sin
  `relr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La relación de forma del menor retal va como `relm. 1.00`
  (en inglés `asps 1.00`): lado largo partido por lado corto.
  Empate por largo y ancho, como `mind.`. Oculta si no hay
  retales. Un cuadrado muestra `1.00`. No sigue las unidades.
  Distinta de `mind.` y de `relr.`. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+\`** copia el valor, sin
  `relm.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La relación de forma del retal de área mediana va como `reln. 2.50`
  (en inglés `aspm 2.50`): lado largo partido por lado corto del mismo
  retal que `mdnd.`. N impar, el del medio. N par, el inferior de los
  dos centrales. Oculta si no hay retales. Un cuadrado muestra `1.00`.
  No sigue las unidades. Distinta de `mdnd.`, `relr.` y `relm.`.
  Cursor mano si está visible. Clic selecciona esa solución en el
  explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+,** copia el valor, sin
  `reln.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La relación de forma del retal de área media va como `rela. 2.50`
  (en inglés `aspa 2.50`): lado largo partido por lado corto del mismo
  retal que `mdds.` (área más próxima a la media; empate por menor
  largo y ancho). Oculta si no hay retales. Un cuadrado muestra `1.00`.
  No sigue las unidades. Distinta de `mdds.`, `reln.`, `relr.` y `relm.`.
  Cursor mano si está visible. Clic selecciona esa solución en el
  explorador; no avanza; arrastre no.
  **Cmd+Alt+Shift+.** copia el valor, sin
  `rela.`. Deshabilitado si la etiqueta está oculta. No avanza.
- Material y espesor deben ser compatibles entre pieza y tablero.
- El **kerf** (**Cmd+Alt+K**) deja hueco de sierra entre piezas al calcular
  y al mover; 0 mm = sin hueco. Piezas con **veta fija** no rotan.
- Varias soluciones = alternativas puntuadas; tú eliges. Con más de un
  tablero físico el cálculo compara MaxRects y Skyline.
- Retales en Inspector son **informativos**, no inventario reutilizable automático.
- Si te arrepientes tras varios Guardar: **Cmd+Alt+Y** restaura la última
  copia del anillo local (luego Guardar otra vez).
- En macOS, **Cmd** es **⌘** (Command), **Alt** es **⌥** (Option) y **Shift** es **⇧** (en Windows/Linux, **Cmd** corresponde a **Ctrl**).

## Comprobar que todo se ve bien

Pasada visual humana: [`../../uat/studio/CHECKLIST-VISUAL.md`](../../uat/studio/CHECKLIST-VISUAL.md).
