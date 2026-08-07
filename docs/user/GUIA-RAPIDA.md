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

## Consejos

- **Barra de estado:** con proyecto guardado muestra el nombre del `.bcproj`
  (tooltip = ruta completa); **clic** abre la carpeta (igual que
  **Ctrl+Shift+R**). Sin guardar: «Proyecto aún no guardado» — tip pide
  **Ctrl+S** antes de poder abrir carpeta. El **%** es el zoom del Workspace
  (rueda, **Ctrl+=** / **Ctrl+-**, **Ctrl+0**).
- **Workspace — pan:** desplaza la cámara con botón medio, botón derecho o
  **Espacio + arrastre** (la rueda sigue siendo zoom).
- **Workspace — mover pieza:** con una pieza colocada seleccionada, **flechas**
  mueven 1 mm; **Shift+flechas** usan el tamaño de cuadrícula (Preferencias).
- **Selección:** **Ctrl+A** / **Escape** / **Ctrl+Shift+I** en el canvas;
  **Return** edita; **Ctrl+Shift+C** copia el ID (Explorador también).
- Material y espesor deben ser compatibles entre pieza y tablero.
- Varias soluciones = alternativas puntuadas; tú eliges.
- Retales en Inspector son **informativos**, no inventario reutilizable automático.
- Tema **sistema**/claro/oscuro e idioma: **Editar → Preferencias**.
- Si te arrepientes tras varios Guardar: **Ctrl+Alt+Y** restaura la última
  copia del anillo local (luego Guardar otra vez).
- En macOS, **Ctrl** de los atajos es la tecla **⌘** (Command).

## Comprobar que todo se ve bien

Pasada visual humana: [`../../uat/studio/CHECKLIST-VISUAL.md`](../../uat/studio/CHECKLIST-VISUAL.md).
