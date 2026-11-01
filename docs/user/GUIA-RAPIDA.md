# Guía rápida — BoardComposer Studio

Para carpinteros y talladores que usan la app día a día.
Detalle de producto y arquitectura: [`../masterplan/INDEX.md`](../masterplan/INDEX.md).

## Arranque

```bash
make run
# o
.venv/bin/python -m studio.app
```

## Pantalla de inicio

Welcome (**Ctrl+Shift+H** para volver). CTAs: nuevo, abrir, importar piezas,
demo (**Ctrl+Shift+D**), desde plantilla, docs, novedades (**Ctrl+Shift+U**),
preferencias, atajos (**F1**), acerca de (**Ctrl+Shift+A**).

- **Recientes:** clic o Enter abre; menú: anclar / carpeta / quitar.
  **Delete** / **Backspace** quita de la lista; **Vaciar lista**
  (**Ctrl+Shift+X**) limpia todo.
- Sin recientes: mensaje vacío. Plantilla deshabilitada si no hay catálogo.

## Flujo típico

1. **Nuevo proyecto** (**Ctrl+N**) — nombre y unidades (mm / pulgadas).
   Opcional: cliente / referencia / notas (**Ctrl+Alt+M**).
2. **Añadir tableros** (**Ctrl+Shift+B**) y **piezas** (**Ctrl+Shift+P**), o
   importar CSV/Excel (**Ctrl+Shift+T** / **Ctrl+Shift+O**). El material es
   un combo del **catálogo** (**Ctrl+Alt+T**; archivo de usuario, no va en
   el `.bcproj`; precio opcional €/m²; medidas L×A típicas de tablero;
   **Exportar/Importar** JSON para otro PC, sin nube). Tableros y piezas
   **nuevos** arrancan con el material por defecto de Preferencias
   (semilla «Melamina blanca»); el CSV no lo usa.
   En cada pieza,
   «Permitir rotación» desmarcado fija la
   **veta** (el cálculo y **R** no giran esa pieza). Espesor de sierra del
   proyecto: **Ctrl+Alt+K**.
3. **Calcular layout** (**Ctrl+Return**) — hace falta ≥1 tablero y ≥1 pieza;
   genera soluciones candidatas (con varios tableros compara MaxRects y
   Skyline). El **Workspace** muestra preview de la mejor candidata
   sin aplicar; **Ctrl+Shift+Return** la conserva.
4. Revisar en **Workspace** (paneles, piezas, cámara).
5. Comparar en **Comparador** (**Ctrl+4**): **Re Pág** / **Av Pág** entre
   candidatas; **Ctrl+Shift+Return** aplica la elegida. Si editas el
   inventario después de calcular, el banner avisa y ofrece **Calcular
   layout**; al aplicar o exportar con soluciones viejas, el diálogo prioriza
   **Calcular layout** frente a continuar de todos modos.
6. **Exportar** la solución (**Ctrl+Shift+E**): SVG / PNG / JPEG / PDF / DXF /
   JSON / CSV. **Lista de corte** de taller (**Ctrl+Alt+C**): CSV o PDF.
7. **Guardar** (**Ctrl+S**) el proyecto `.bcproj`.

## Revisiones locales del `.bcproj`

Al **Guardar** sobre un archivo ya existente, Studio copia la versión anterior
en una carpeta oculta junto al proyecto (`.<nombre>.bcproj.revs/`, máx. 10).

| Acción | Cómo |
|---|---|
| Comparar | **Proyecto → Comparar revisiones .bcproj…** (**Ctrl+Shift+Y**) |
| Restaurar la última | **Proyecto → Restaurar última revisión local…** (**Ctrl+Alt+Y**) |
| Restaurar una concreta | En el diálogo de comparar, elige revisión → **Restaurar esta revisión…** |
| Backup (anillo + archivo) | **Proyecto → Exportar backup de revisiones…** (**Ctrl+Alt+B**; luego Abrir carpeta) o CLI `boardcomposer-backup` |

La restauración carga el snapshot **en memoria** (misma ruta del archivo).
Queda pendiente de **Guardar** para escribirlo en disco. La pila Deshacer se
vacía al restaurar o al abrir otro proyecto.

Tras **Calcular layout**, **Ayuda → Explicar candidata…** (**Ctrl+Alt+E**)
muestra fortalezas / debilidades / notas de la solución seleccionada (sin IA
en red; puedes **Copiar**).

## Atajos útiles

| Acción | Atajo |
|---|---|
| Nuevo / Abrir / Guardar | Ctrl+N / Ctrl+O / Ctrl+S |
| Guardar como | Ctrl+Shift+S |
| Abrir carpeta del proyecto | Ctrl+Shift+R |
| Copiar ruta del .bcproj | Ctrl+Alt+Shift+C |
| Preferencias | Ctrl+, |
| Añadir tablero / pieza | Ctrl+Shift+B / Ctrl+Shift+P |
| Importar tableros / piezas (CSV/Excel) | Ctrl+Shift+T / Ctrl+Shift+O |
| Calcular layout | Ctrl+Return |
| Re-empaquetar omitidas (congelar OK) | Ctrl+Alt+F |
| Añadir retales al inventario | Ctrl+Alt+R |
| Catálogo de materiales / espesores / L×A | Ctrl+Alt+T |
| Aplicar layout del Comparador | Ctrl+Shift+Return |
| Candidata anterior / siguiente | Re Pág / Av Pág |
| Exportar solución | Ctrl+Shift+E |
| Exportar lista de corte (CSV/PDF) | Ctrl+Alt+C |
| Exportar historial Timeline | Ctrl+Shift+L |
| Replay Timeline (lista enfocada) | Espacio / Inicio / ← / → |
| Comparar revisiones `.bcproj` | Ctrl+Shift+Y |
| Restaurar última revisión local | Ctrl+Alt+Y |
| Exportar backup de revisiones | Ctrl+Alt+B |
| Explicar candidata | Ctrl+Alt+E |
| Deshacer / Rehacer | Ctrl+Z / Ctrl+Shift+Z |
| Rotar pieza | R (no si la veta está fija) |
| Intercambiar dos piezas colocadas | Ctrl+Alt+X |
| Sugerir hueco | Ctrl+Alt+G |
| Metadatos del proyecto | Ctrl+Alt+M |
| Espesor de sierra / kerf | Ctrl+Alt+K |
| Copiar espesor de sierra | Ctrl+Alt+Shift+K |
| Mover pieza seleccionada | Flechas (Shift = tamaño cuadrícula) |
| Seleccionar todas / Deseleccionar / Invertir | Ctrl+A / Escape / Ctrl+Shift+I |
| Editar selección / Copiar ID / Copiar medidas | Return / Ctrl+Shift+C / Ctrl+Alt+Shift+D |
| Copiar medidas del tablero | Ctrl+Alt+Shift+B |
| Copiar espesor del tablero | Ctrl+Alt+Shift+T |
| Copiar material del tablero | Ctrl+Alt+Shift+M |
| Copiar aprovechamiento del tablero | Ctrl+Alt+Shift+U |
| Copiar material libre del tablero | Ctrl+Alt+Shift+F |
| Copiar piezas colocadas | Ctrl+Alt+Shift+P |
| Copiar piezas omitidas | Ctrl+Alt+Shift+O |
| Copiar tableros físicos | Ctrl+Alt+Shift+N |
| Copiar selección de la barra | Ctrl+Alt+Shift+S |
| Renombrar selección | F2 |
| Renombrar proyecto | Ctrl+Shift+F2 |
| Duplicar / Eliminar | Ctrl+D / Backspace o Delete |
| Cuadrícula | Ctrl+G |
| Ajustar al tablero / selección | Ctrl+0 / Ctrl+Shift+0 |
| Zoom al 100% | Ctrl+Alt+0 |
| Copiar zoom | Ctrl+Alt+Shift+Z |
| Copiar retales | Ctrl+Alt+Shift+R |
| Copiar índice de la solución | Ctrl+Alt+Shift+L |
| Copiar huecos internos | Ctrl+Alt+Shift+G |
| Copiar estrategia | Ctrl+Alt+Shift+Y |
| Copiar piezas de la solución | Ctrl+Alt+Shift+J |
| Copiar omitidas de la solución | Ctrl+Alt+Shift+Q |
| Copiar tableros de la solución | Ctrl+Alt+Shift+W |
| Copiar puntuación de la solución | Ctrl+Alt+Shift+V |
| Zoom + / − (también rueda) | Ctrl+= / Ctrl+- |
| Desplazar cámara (pan) | Botón medio / derecho / Espacio+arrastre |
| Nuevo desde plantilla | Ctrl+Shift+N |
| Guardar como plantilla | Ctrl+Shift+M |
| Pantalla de inicio | Ctrl+Shift+H |
| Demo | Ctrl+Shift+D |
| Mostrar/ocultar docks | Ctrl+1…4 |
| Mostrar/ocultar barra | Ctrl+Shift+K |
| Restablecer disposición | Ctrl+Shift+W |
| Documentación | Shift+F1 (o Ayuda → Documentación) |
| Atajos / Novedades | F1 / Ctrl+Shift+U |
| Acerca de | Ctrl+Shift+A |
| Salir | Ctrl+Q |

Lista completa: **Ayuda → Atajos de teclado** (**F1**).

## Importar CSV/Excel

- **Tableros:** **Ctrl+Shift+T** — id, largo, ancho, espesor, cantidad, material.
  Ejemplo: `data/samples/studio_boards_inventory.csv`.
- **Piezas:** **Ctrl+Shift+O** — mismos campos habituales; la cantidad puede
  expandirse a varios IDs.
- Formatos: `.csv` y `.xlsx`. Tras elegir archivo, Studio muestra vista previa
  fila a fila (OK / error) antes de incorporar.

## Workspace

Canvas central del layout.

- Sin tableros ni piezas: overlay con CTAs (añadir / importar).
- **Pan:** botón medio, botón derecho o **Espacio + arrastre**.
- **Zoom:** rueda, **Ctrl+=** / **Ctrl+-**, ajustar todo (**Ctrl+0**),
  zoom al 100% (**Ctrl+Alt+0**) o
  selección (**Ctrl+Shift+0**). Cuadrícula: **Ctrl+G**.
- **Pieza colocada:** **flechas** mueven 1 mm; **Shift+flechas** usan el
  tamaño de cuadrícula (Preferencias); **R** rota 90° (deshabilitado si la
  veta está fija). Con **exactamente dos** piezas colocadas
  seleccionadas, **Ctrl+Alt+X** intercambia posiciones (si no caben o el
  material no coincide, no cambia nada; se puede deshacer).
  **Ctrl+Alt+G** coloca la pieza seleccionada en un hueco libre (mismo
  panel si ya está colocada; tablero enfocado si no). Un drop que solapa
  ajusta al hueco más cercano; incompatibilidad de material/espesor sigue
  revirtiendo.
- **Selección:** **Ctrl+A** / **Escape** / **Ctrl+Shift+I**; **Return**
  edita; **Ctrl+Shift+C** copia el ID; **Ctrl+Alt+Shift+D** copia L×A
  de una sola pieza; **Ctrl+Alt+Shift+B** copia L×A de una hoja de tablero
  (la cantidad no multiplica).

## Explorador

Dock **Ctrl+1**. Árbol del proyecto: **Tableros**, **Piezas** y **Soluciones**.

- **Doble clic / Return:** edita tablero o pieza; si la pieza está sin
  colocar y hay tablero enfocado en el Workspace, la **coloca** ahí.
  En una solución: vista previa en el Workspace (sin aplicar).
- **Menú contextual:** editar / renombrar (**F2**) / duplicar (**Ctrl+D**) /
  copiar ID (**Ctrl+Shift+C**) / copiar medidas (**Ctrl+Alt+Shift+D**,
  solo piezas; en tableros **Ctrl+Alt+Shift+B**) / eliminar; en piezas también
  **Colocar en tablero enfocado**; en categorías, añadir tablero/pieza;
  en el proyecto, renombrar, **Abrir carpeta…** o **Copiar ruta**.
- Piezas sin colocar llevan marca **sin colocar**.

## Inspector

Dock **Ctrl+2**. Detalle de la selección y del layout.

- Sin selección: mensaje vacío. Con la **raíz del proyecto** en el
  Explorador: cliente, referencia, notas (**Ctrl+Alt+M**), espesor de
  sierra (**Ctrl+Alt+K**), conteos (tableros/piezas/soluciones),
  materiales y área de stock. Con las **categorías** del árbol: tipos
  y físicos, retales, colocadas/sin colocar o candidatas. Con
  **tablero** o **pieza**: dimensiones, área (pieza, o una hoja de
  tablero sin multiplicar la cantidad),
  espesor, cantidad, material. **Ctrl+Alt+I** copia el texto del dock. En tablero, aprovechamiento (instancias,
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

Dock **Ctrl+4**. Candidatas tras **Calcular layout**.

- **Ordenar por:** ranking del solver, piezas, huecos, tablero libre,
  coste material, puntuación.
- **Solo soluciones completas:** oculta candidatas parciales.
- **Fijar como referencia** (≥2 soluciones): marca la candidata y muestra
  el diff frente a ella. Largo, ancho y coords del diff usan las
  **unidades** de Preferencias (mm / cm / in).
- Navegar: **Re Pág** / **Av Pág**; **Ctrl+Shift+Return** aplica la elegida
  al proyecto.
- **Generar → Re-empaquetar omitidas** (**Ctrl+Alt+F**): congela las piezas
  ya colocadas de la candidata parcial y solo intenta colocar las omitidas
  en retales y tableros libres. No sustituye a Calcular layout.
- **Generar → Añadir retales al inventario** (**Ctrl+Alt+R**): crea tableros
  remnant con las medidas de los retales ≥ 50 mm. No baja solo la cantidad
  de tableros ya cortados; hazlo antes del próximo cálculo. Se puede
  deshacer.
- Si editas inventario después de calcular, el banner avisa y el CTA
  **Calcular layout** recalcula; tips de aplicar / navegar / explicar
  también lo advierten.
- **Ayuda → Explicar candidata…** (**Ctrl+Alt+E**): fortalezas / debilidades
  / notas (sin IA en red; puedes **Copiar**).

## Timeline

Dock **Ctrl+3**. Historial de eventos del proyecto (cálculos, movimientos,
marcadores…).

- **Seguir:** mantiene la vista en el último evento.
- **Filtros:** combos de evento / algoritmo / periodo; botones **Solo
  movimientos** y **Solo marcadores**; **Limpiar filtros** si hay alguno
  activo.
- **Marcador…:** pide una nota; si hay replay activo, guarda paso/algoritmo.
- **Replay:** tras **Calcular layout**, modo colocaciones o fases del solver +
  velocidad. Con la lista enfocada: **Espacio** play/pausa, **Inicio**
  reinicia, **←** / **→** paso a paso.
- **Exportar…** (**Ctrl+Shift+L**) respeta los filtros visibles; **Vaciar**
  pide confirmación. **Ctrl+C** (lista enfocada) copia la **línea** del
  evento; el menú contextual ofrece también el **payload JSON**.

## Exportar

**Archivo → Exportar…** (**Ctrl+Shift+E**) exporta la **solución seleccionada**.

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
- **Archivo → Exportar lista de corte…** (**Ctrl+Alt+C**) es otro flujo:
  CSV o PDF de taller (piezas, tableros y **secuencia de sierra** por
  panel). El **PDF** usa las unidades de Preferencias (mm/cm/in) y el pie
  de trazabilidad (versión, algoritmo, fecha); el CSV sigue en mm y no
  lleva pie. Recuerda carpeta y formato. El plano SVG/PDF/DXF
  numera cada pieza con ese orden. No sustituye el CSV de colocaciones
  del diálogo de solución.
- **Archivo → Exportar presupuesto…** (**Ctrl+Alt+Q**) PDF de coste de
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

**Editar → Preferencias** (**Ctrl+,**). Globales: **no** van en el `.bcproj`.

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

- **Guardar como plantilla…** (**Ctrl+Shift+M**): pide nombre; opcional
  incluir colocaciones actuales. Requiere proyecto abierto.
- **Nuevo desde plantilla…** (**Ctrl+Shift+N** o Welcome): elige plantilla;
  opcional restaurar colocaciones; renombrar / eliminar desde el diálogo.
- Sin catálogo, el atajo/botón queda deshabilitado (tip honesto).

## Disposición

Chrome de Studio (se recuerda entre sesiones).

- **Docks:** Explorador (**Ctrl+1**), Inspector (**Ctrl+2**), Timeline
  (**Ctrl+3**), Comparador (**Ctrl+4**).
- **Barra de herramientas:** mostrar/ocultar (**Ctrl+Shift+K**).
- **Restablecer disposición** (**Ctrl+Shift+W**): docks, toolbar y tamaño
  de ventana a valores iniciales (status: «Disposición de ventana
  restablecida»).

## Consejos

- **Barra de estado:** con proyecto guardado muestra el nombre del `.bcproj`
  (tooltip = ruta completa); **clic** abre la carpeta (igual que
  **Ctrl+Shift+R**). Sin guardar: «Proyecto aún no guardado» — tip pide
  **Ctrl+S** antes de poder abrir carpeta. Entre el nombre y el **%** va
  piezas colocadas / total (`1/2`; tooltip «Piezas colocadas: 1 de 2»).
  **Clic** encuadra esas colocadas (no el tablero ni la selección).
  **Ctrl+Alt+Shift+P** copia `1/2`, como el rótulo.
  Las omitidas van como `2 om.` (inventario sin colocación; oculto si
  es 0). **Clic** las selecciona y encuadra si están en el Workspace.
  **Ctrl+Alt+Shift+O** copia el número, sin `om.`.
  Los tableros físicos van como `3 tab.` (suma de cantidades; oculto si
  no hay). **Clic** encuadra todos los tableros (**Ctrl+0**).
  **Ctrl+Alt+Shift+N** copia el número, sin `tab.`. El espesor
  del tablero va como `esp. 19 mm` (el enfocado, o el único tipo; oculto
  si hay varios y ninguno enfocado). **Clic** abre la edición de ese
  tablero. El material va como `mat. Demo` (el mismo tablero; oculto
  si el material está vacío). **Clic** abre la edición de ese tablero.
  **Ctrl+Alt+Shift+M** copia ese material. El aprovechamiento del
  tablero enfocado va como `uso 24.0%` (la misma fórmula que el
  Inspector; oculto sin foco o sin uso). **Clic** selecciona ese tablero.
  **Ctrl+Alt+Shift+U** copia el porcentaje (`24.0%`), sin el prefijo.
  El material libre va como `libre 76.0%` (complemento del
  aprovechamiento; la misma visibilidad). **Clic** selecciona ese tablero.
  **Ctrl+Alt+Shift+F** copia el porcentaje (`76.0%`), sin el prefijo.
  Si hay piezas seleccionadas en el Workspace, aparece `1 sel.` / `2 sel.`
  (oculta si no hay selección). **Clic** en `n sel.` ajusta el encuadre
  (**Ctrl+Shift+0**). **Ctrl+Alt+Shift+S** copia el número, sin `sel.`.
  El kerf del proyecto va como `kerf 3.2 mm`
  (unidades de Preferencias; oculto si no hay proyecto). **Clic** lo
  edita (**Ctrl+Alt+K**). **Ctrl+Alt+Shift+K** copia ese espesor
  (unidades de Preferencias; kerf 0 también). El
  **%** es el zoom del Workspace
  (rueda, **Ctrl+=** / **Ctrl+-**, **Ctrl+0**). **Clic** en el **%**
  vuelve al 100% (**Ctrl+Alt+0**); si ya está, el cursor no es mano.
  **Ctrl+Alt+Shift+Z** copia ese porcentaje, sin volver al 100%.
  Los retales de la solución seleccionada van como `2 ret.` (oculto si
  no hay solución o si es 0). **Clic** selecciona su tablero. No encuadra
  ni promociona. **Ctrl+Alt+Shift+R** copia el
  número, sin `ret.`.
  La solución seleccionada va como `1/2 sol.` (oculto si no hay
  solución o si el índice no mapea). **Clic** pasa a la siguiente.
  No aplica el layout ni cambia el zoom. Arrastre no.
  **Ctrl+Alt+Shift+L** copia `1/2`, sin `sol.`. No avanza.
  Los huecos internos van como `hueco 0.0%` (en inglés `gap 0.0%`).
  La misma visibilidad que el índice. `0.0%` se muestra.
  **Clic** selecciona esa solución en el explorador. No avanza ni
  aplica el layout. Arrastre no.
  **Ctrl+Alt+Shift+G** copia el porcentaje, sin `hueco`. No avanza.
  La estrategia va como `est. material` (en inglés `str. material`).
  La misma visibilidad que el índice. Sin nombre: `est. desconocida`.
  Cursor mano si está visible. **Clic** selecciona esa solución en
  el explorador. No avanza ni aplica el layout. Arrastre no.
  **Ctrl+Alt+Shift+Y** copia el nombre (`material`, `desconocida`),
  sin `est.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las piezas de esa solución van como `0 pza` (en inglés `0 pcs`).
  La misma visibilidad que el índice. `0` se muestra. Distinto de
  colocadas/total. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout.
  Arrastre no.
  **Ctrl+Alt+Shift+J** copia el número (`0`, `2`), sin `pza`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  Las omitidas de esa solución van como `fuera 0` (en inglés `out 2`).
  La misma visibilidad que el índice. `0` se muestra. Distinto de
  `n om.`. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout.
  Arrastre no.
  **Ctrl+Alt+Shift+Q** copia el número (`0`, `2`), sin `fuera`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  Los tableros usados por esa solución van como `pan. 0` (en inglés
  `pnl 2`). La misma visibilidad que el índice. `0` se muestra.
  Distinto de `n tab.`. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout.
  Arrastre no.
  **Ctrl+Alt+Shift+W** copia el número (`0`, `2`), sin `pan.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de esa solución va como `pts. 0.00` (en inglés
  `pts 0.75`). La misma visibilidad que el índice. `0.00` se muestra.
  Cursor mano si está visible. **Clic** selecciona esa solución en el
  explorador. No avanza ni aplica el layout. Arrastre no.
  **Ctrl+Alt+Shift+V** copia el valor (`0.00`, `0.75`), sin `pts.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  El tablero libre de esa solución va como `sbr. 0.0%` (en inglés
  `rem. 76.0%`). La misma visibilidad que el índice. `0.0%` se muestra.
  Distinto de `libre`. Cursor mano si está visible. **Clic** selecciona
  esa solución en el explorador. No avanza ni aplica el layout. Arrastre no.
  **Ctrl+Alt+Shift+E** copia el porcentaje (`0.0%`, `76.0%`), sin `sbr.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  El largo total de esa solución va como `lrg. 0 mm` (en inglés
  `len. 400 mm`). La misma visibilidad que el índice. `0 mm` se muestra.
  Sigue las unidades de Preferencias. Cursor mano si está visible.
  **Clic** selecciona esa solución en el explorador. No avanza ni
  aplica el layout. Arrastre no.
  **Ctrl+Alt+Shift+H** copia el largo con unidad (`0 mm`, `400 mm`,
  `40 cm`), sin `lrg.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El ancho total de esa solución va como `anc. 0 mm` (en inglés
  `wid. 300 mm`). La misma visibilidad que el índice. `0 mm` se muestra.
  Sigue las unidades de Preferencias. Cursor mano si está visible.
  **Clic** selecciona esa solución en el explorador. No avanza ni
  aplica el layout. Arrastre no.
  **Ctrl+Alt+Shift+X** copia el ancho con unidad (`0 mm`, `300 mm`,
  `30 cm`), sin `anc.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área usada de esa solución va como `ár. 0 mm²` (en inglés
  `area 20000 mm²`). La misma visibilidad que el índice. `0 mm²` se
  muestra. Sigue las unidades de Preferencias. Cursor mano si está
  visible. **Clic** selecciona esa solución en el explorador. No avanza
  ni aplica el layout. Arrastre no.
  **Ctrl+Alt+Shift+A** copia el área con unidad (`0 mm²`, `20000 mm²`,
  `200 cm²`), sin `ár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de retales de esa solución va como `retár. 0 mm²` (en inglés
  `offar. 20000 mm²`). La misma visibilidad que el índice (distinto de
  `n ret.`). `0 mm²` se muestra. Sigue las unidades de Preferencias.
  Cursor mano si está visible. Clic selecciona esa solución en el
  explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+I** copia el área con unidad (`0 mm²`, `20000 mm²`,
  `200 cm²`), sin `retár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área envolvente de esa solución va como `env. 0 mm²` (en inglés
  `bnd. 60000 mm²`). La misma visibilidad que el índice. `0 mm²` se
  muestra. Sigue las unidades de Preferencias. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Ctrl+Alt+Shift+1** copia el área con unidad (`0 mm²`, `60000 mm²`,
  `600 cm²`), sin `env.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de huecos internos de esa solución va como `hueár. 0 mm²` (en
  inglés `gapar. 30000 mm²`). La misma visibilidad que el índice
  (distinto de `hueco n%`). `0 mm²` se muestra. Sigue las unidades de
  Preferencias. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+2** copia el área con unidad (`0 mm²`, `30000 mm²`,
  `300 cm²`), sin `hueár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de tablero libre de esa solución va como `sbrár. 0 mm²` (en
  inglés `remar. 380000 mm²`). La misma visibilidad que el índice
  (distinto de `sbr. n%`). `0 mm²` se muestra. Sigue las unidades de
  Preferencias. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+3** copia el área con unidad (`0 mm²`, `380000 mm²`,
  `3800 cm²`), sin `sbrár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El área de tableros consumidos de esa solución va como `panár. 0 mm²`
  (en inglés `pnlar. 500000 mm²`). La misma visibilidad que el índice
  (distinto de `pan. {n}`). `0 mm²` se muestra. Sigue las unidades de
  Preferencias. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+4** copia el área con unidad (`0 mm²`, `500000 mm²`,
  `5000 cm²`), sin `panár.`. Deshabilitado si la etiqueta está oculta.
  No avanza.
  El aprovechamiento de tableros de esa solución va como `aprv. 0.0%`
  (en inglés `util. 24.0%`). La misma visibilidad que el índice
  (distinto de `uso`). `0.0%` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+5** copia el porcentaje (`0.0%`, `24.0%`), sin
  `aprv.`. Deshabilitado si la etiqueta está oculta. No avanza.
  Las piezas rotadas de esa solución van como `rot. 0` (en inglés
  `rot 2`). La misma visibilidad que el índice (distinto de `n pza`).
  `0` se muestra. Cursor mano si está visible. Clic selecciona esa
  solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+6** copia el número (`0`, `2`), sin `rot.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  Las piezas sin rotar de esa solución van como `nrot. 0` (en inglés
  `unrot 2`). La misma visibilidad que el índice (distinto de
  `rot. {n}`). `0` se muestra. Cursor mano si está visible. Clic
  selecciona esa solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+7** copia el número (`0`, `2`), sin `nrot.`.
  Deshabilitado si la etiqueta está oculta. No avanza.
  El porcentaje de piezas rotadas de esa solución va como `rot% 0.0%`
  (en inglés `rot% 50.0%`). La misma visibilidad que el índice
  (distinto de `rot. {n}`). `0.0%` se muestra. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Ctrl+Alt+Shift+8** copia el porcentaje (`0.0%`, `50.0%`), sin
  `rot%`. Deshabilitado si la etiqueta está oculta. No avanza.
  El porcentaje de piezas sin rotar de esa solución va como
  `nrot% 0.0%` (en inglés `unrot% 75.0%`). La misma visibilidad que el
  índice (distinto de `nrot. {n}`). `0.0%` se muestra. Cursor mano si
  está visible. Clic selecciona esa solución en el explorador; no
  avanza; arrastre no.
  **Ctrl+Alt+Shift+9** copia el porcentaje (`0.0%`, `75.0%`), sin
  `nrot%`. Deshabilitado si la etiqueta está oculta. No avanza.
  El aprovechamiento envolvente de esa solución va como `env% 0.0%`
  (en inglés `bnd% 50.0%`). La misma visibilidad que el índice
  (distinto de `aprv.` y `uso`). `0.0%` se muestra. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Ctrl+Alt+Shift+0** copia el porcentaje (`0.0%`, `50.0%`), sin
  `env%`. Deshabilitado si la etiqueta está oculta. No avanza.
  El porcentaje de retales de esa solución va como `ret% 0.0%` (en
  inglés `off% 4.0%`). La misma visibilidad que el índice (distinto de
  `n ret.` y `retár.`). `0.0%` se muestra. Cursor mano si está
  visible. Clic selecciona esa solución en el explorador; no avanza;
  arrastre no.
  **Ctrl+Alt+Shift+F1** copia el porcentaje (`0.0%`, `4.0%`), sin
  `ret%`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de desperdicio de esa solución va como `ptsh. 0.00`
  (en inglés `ptsw 0.50`). La misma visibilidad que el índice (distinto
  de `pts.`). `0.00` se muestra. Cursor mano si está visible. Clic
  selecciona esa solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+F2** copia el valor (`0.00`, `0.50`), sin
  `ptsh.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de uso de material de esa solución va como `ptsu. 0.00`
  (en inglés `ptsu 0.25`). La misma visibilidad que el índice (distinto
  de `pts.` y `ptsh.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+F3** copia el valor (`0.00`, `0.25`), sin
  `ptsu.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de cortes de esa solución va como `ptsc. 0.00`
  (en inglés `ptsc 0.75`). La misma visibilidad que el índice (distinto
  de `pts.`, `ptsh.` y `ptsu.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+F4** copia el valor (`0.00`, `0.75`), sin
  `ptsc.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de regularidad de esa solución va como `ptsr. 0.00`
  (en inglés `ptsr 0.40`). La misma visibilidad que el índice (distinto
  de `pts.`, `ptsh.`, `ptsu.` y `ptsc.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+F5** copia el valor (`0.00`, `0.40`), sin
  `ptsr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La puntuación de veta de esa solución va como `ptsv. 0.00`
  (en inglés `ptsg 0.40`). La misma visibilidad que el índice (distinto
  de `pts.`, `ptsh.`, `ptsu.`, `ptsc.` y `ptsr.`). `0.00` se muestra. Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza; arrastre no.
  **Ctrl+Alt+Shift+F6** copia el valor (`0.00`, `0.40`), sin
  `ptsv.`. Deshabilitado si la etiqueta está oculta. No avanza.
  La completitud de esa solución va como `comp. sí` (en inglés
  `full yes`; `comp. no` / `full no` si hay piezas omitidas).
  La misma visibilidad que el índice (distinto de `fuera`). Cursor
  mano si está visible. Clic selecciona esa solución en el explorador;
  no avanza; arrastre no.
  **Ctrl+Alt+Shift+F7** copia el valor (`sí`, `no`), sin
  `comp.`. Deshabilitado si la etiqueta está oculta. No avanza.
  El área del mayor retal va como `maxr. 20000 mm²` (en inglés
  `maxo 20000 mm²`). Oculta si no hay retales (como `n ret.`;
  distinta de `retár.` y `ret%`). Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza;
  arrastre no. Sigue las unidades de Preferencias.
  **Ctrl+Alt+Shift+F8** copia el área con unidad, sin
  `maxr.`. Deshabilitado si la etiqueta está oculta. No avanza.
  El área del menor retal va como `minr. 2500 mm²` (en inglés
  `mino 2500 mm²`). Oculta si no hay retales (como `n ret.` y
  `maxr.`; distinta de `maxr.`, `retár.` y `ret%`). Cursor mano si está visible.
  Clic selecciona esa solución en el explorador; no avanza;
  arrastre no. Sigue las unidades de Preferencias.
  **Ctrl+Alt+Shift+F9** copia el área con unidad, sin
  `minr.`. Deshabilitado si la etiqueta está oculta. No avanza.
- Material y espesor deben ser compatibles entre pieza y tablero.
- El **kerf** (**Ctrl+Alt+K**) deja hueco de sierra entre piezas al calcular
  y al mover; 0 mm = sin hueco. Piezas con **veta fija** no rotan.
- Varias soluciones = alternativas puntuadas; tú eliges. Con más de un
  tablero físico el cálculo compara MaxRects y Skyline.
- Retales en Inspector son **informativos**, no inventario reutilizable automático.
- Si te arrepientes tras varios Guardar: **Ctrl+Alt+Y** restaura la última
  copia del anillo local (luego Guardar otra vez).
- En macOS, **Ctrl** de los atajos es la tecla **⌘** (Command).

## Comprobar que todo se ve bien

Pasada visual humana: [`../../uat/studio/CHECKLIST-VISUAL.md`](../../uat/studio/CHECKLIST-VISUAL.md).
