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
| Mover pieza seleccionada | Flechas (Shift = tamaño cuadrícula) |
| Seleccionar todas / Deseleccionar / Invertir | Ctrl+A / Escape / Ctrl+Shift+I |
| Editar selección / Copiar ID | Return / Ctrl+Shift+C |
| Renombrar selección | F2 |
| Renombrar proyecto | Ctrl+Shift+F2 |
| Duplicar / Eliminar | Ctrl+D / Backspace o Delete |
| Cuadrícula | Ctrl+G |
| Ajustar al tablero / selección | Ctrl+0 / Ctrl+Shift+0 |
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
- **Zoom:** rueda, **Ctrl+=** / **Ctrl+-**, ajustar todo (**Ctrl+0**) o
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
  edita; **Ctrl+Shift+C** copia el ID.

## Explorador

Dock **Ctrl+1**. Árbol del proyecto: **Tableros**, **Piezas** y **Soluciones**.

- **Doble clic / Return:** edita tablero o pieza; si la pieza está sin
  colocar y hay tablero enfocado en el Workspace, la **coloca** ahí.
  En una solución: vista previa en el Workspace (sin aplicar).
- **Menú contextual:** editar / renombrar (**F2**) / duplicar (**Ctrl+D**) /
  copiar ID (**Ctrl+Shift+C**) / eliminar; en piezas también
  **Colocar en tablero enfocado**; en categorías, añadir tablero/pieza;
  en el proyecto, renombrar u **Abrir carpeta…**.
- Piezas sin colocar llevan marca **sin colocar**.

## Inspector

Dock **Ctrl+2**. Detalle de la selección y del layout.

- Sin selección: mensaje vacío. Con la **raíz del proyecto** en el
  Explorador: cliente, referencia, notas (**Ctrl+Alt+M**), espesor de
  sierra (**Ctrl+Alt+K**), conteos (tableros/piezas/soluciones),
  materiales y área de stock. Con las **categorías** del árbol: tipos
  y físicos, retales, colocadas/sin colocar o candidatas. Con
  **tablero** o **pieza**: dimensiones, área de la pieza,
  espesor, cantidad, material; en tablero, aprovechamiento (instancias,
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
  **Ctrl+S** antes de poder abrir carpeta. El **%** es el zoom del Workspace
  (rueda, **Ctrl+=** / **Ctrl+-**, **Ctrl+0**).
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
