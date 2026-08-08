# Guía rápida — BoardComposer Studio

Para carpinteros y talladores que usan la app día a día.
Detalle de producto y arquitectura: [`../masterplan/INDEX.md`](../masterplan/INDEX.md).

## Arranque

```bash
make run
# o
.venv/bin/python -m studio.app
```

Pantalla de inicio: nuevo proyecto, abrir, recientes (clic o Enter; menú: anclar / carpeta / Delete quita), demo, plantilla, docs, novedades, atajos y acerca de.

## Flujo típico

1. **Nuevo proyecto** (**Ctrl+N**) — nombre y unidades (mm / pulgadas).
2. **Añadir tableros** (**Ctrl+Shift+B**) y **piezas** (**Ctrl+Shift+P**), o
   importar CSV/Excel (**Ctrl+Shift+T** / **Ctrl+Shift+O**).
3. **Calcular layout** (**Ctrl+Return**) — hace falta ≥1 tablero y ≥1 pieza;
   genera soluciones candidatas.
4. Revisar en **Workspace** (paneles, piezas, cámara).
5. Comparar en **Comparador** (**Ctrl+4**): **Re Pág** / **Av Pág** entre
   candidatas; **Ctrl+Shift+Return** aplica la elegida. Si editas el
   inventario después de calcular, el banner avisa y ofrece **Calcular
   layout**; al aplicar o exportar con soluciones viejas, el diálogo prioriza
   **Calcular layout** frente a continuar de todos modos.
6. **Exportar** (**Ctrl+Shift+E**): SVG / PNG / JPEG / PDF / DXF / JSON / CSV.
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
en red; podés **Copiar**).

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
| Aplicar layout del Comparador | Ctrl+Shift+Return |
| Candidata anterior / siguiente | Re Pág / Av Pág |
| Exportar solución | Ctrl+Shift+E |
| Exportar historial Timeline | Ctrl+Shift+L |
| Replay Timeline (lista enfocada) | Espacio / Inicio / ← / → |
| Comparar revisiones `.bcproj` | Ctrl+Shift+Y |
| Restaurar última revisión local | Ctrl+Alt+Y |
| Exportar backup de revisiones | Ctrl+Alt+B |
| Explicar candidata | Ctrl+Alt+E |
| Deshacer / Rehacer | Ctrl+Z / Ctrl+Shift+Z |
| Rotar pieza | R |
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
  tamaño de cuadrícula (Preferencias); **R** rota 90°.
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

- Sin selección: mensaje vacío. Con **tablero** o **pieza**: dimensiones,
  espesor, cantidad, material; en piezas, posición o «sin colocar» (con
  consejo de colocar vía Explorador).
- Tras **Calcular layout**: métricas de la candidata (piezas, huecos,
  material libre, omitidas, puntos clave).
- **Retales** son **informativos** — no inventario reutilizable automático.
- Si el inventario cambió tras calcular, el Inspector también avisa de
  soluciones desactualizadas.

## Comparador

Dock **Ctrl+4**. Candidatas tras **Calcular layout**.

- **Ordenar por:** ranking del solver, piezas, huecos, tablero libre, etc.
- **Solo soluciones completas:** oculta candidatas parciales.
- **Fijar como referencia** (≥2 soluciones): marca la candidata y muestra
  el diff frente a ella.
- Navegar: **Re Pág** / **Av Pág**; **Ctrl+Shift+Return** aplica la elegida
  al proyecto.
- Si editas inventario después de calcular, el banner avisa y el CTA
  **Calcular layout** recalcula; tips de aplicar / navegar / explicar
  también lo advierten.
- **Ayuda → Explicar candidata…** (**Ctrl+Alt+E**): fortalezas / debilidades
  / notas (sin IA en red; podés **Copiar**).

## Timeline

Dock **Ctrl+3**. Historial de eventos del proyecto (cálculos, movimientos,
marcadores…).

- **Seguir:** mantiene la vista en el último evento.
- **Filtros:** combos de evento / algoritmo / periodo; botones **Solo
  movimientos** y **Solo marcadores**; **Limpiar filtros** si hay alguno
  activo.
- **Replay:** tras **Calcular layout**, modo colocaciones o fases del solver +
  velocidad. Con la lista enfocada: **Espacio** play/pausa, **Inicio**
  reinicia, **←** / **→** paso a paso.
- **Exportar…** (**Ctrl+Shift+L**) respeta los filtros visibles; **Vaciar**
  pide confirmación. **Ctrl+C** (lista enfocada) copia la **línea** del
  evento; el menú contextual ofrece también el **payload JSON**.

## Exportar

**Archivo → Exportar…** (**Ctrl+Shift+E**) exporta la **solución seleccionada**.

- Formatos: SVG / PNG / JPEG / PDF / DXF / JSON / CSV. Vista previa según
  opciones (métricas, explicación, retales en JSON).
- **Cliente** y **plantilla** reutilizan un perfil; **Guardar…** / **Eliminar**
  gestionan el catálogo; **Exportar/Importar pack…** comparte plantillas
  (recuerda la última carpeta).
- Al terminar: diálogo con **Abrir archivo** / **Abrir carpeta**.
- Si las soluciones están desactualizadas, el diálogo prioriza **Calcular
  layout** antes de continuar.

## Preferencias

**Editar → Preferencias** (**Ctrl+,**). Globales: **no** van en el `.bcproj`.

- **General:** idioma, tema (sistema / claro / oscuro), unidades.
- **Workspace:** mostrar cuadrícula y tamaño (afecta **Shift+flechas**).
- **Algoritmos:** estrategia y pesos opcionales.
- **Exportación:** formato por defecto y opciones JSON (métricas /
  explicación / retales).
- **Avanzado:** máx. soluciones a conservar; **Abrir carpeta de
  configuración…** (`preferences.json`); **Restaurar valores**.

## Consejos

- **Barra de estado:** con proyecto guardado muestra el nombre del `.bcproj`
  (tooltip = ruta completa); **clic** abre la carpeta (igual que
  **Ctrl+Shift+R**). Sin guardar: «Proyecto aún no guardado» — tip pide
  **Ctrl+S** antes de poder abrir carpeta. El **%** es el zoom del Workspace
  (rueda, **Ctrl+=** / **Ctrl+-**, **Ctrl+0**).
- Material y espesor deben ser compatibles entre pieza y tablero.
- Varias soluciones = alternativas puntuadas; tú eliges.
- Retales en Inspector son **informativos**, no inventario reutilizable automático.
- Si te arrepientes tras varios Guardar: **Ctrl+Alt+Y** restaura la última
  copia del anillo local (luego Guardar otra vez).
- En macOS, **Ctrl** de los atajos es la tecla **⌘** (Command).

## Comprobar que todo se ve bien

Pasada visual humana: [`../../uat/studio/CHECKLIST-VISUAL.md`](../../uat/studio/CHECKLIST-VISUAL.md).
