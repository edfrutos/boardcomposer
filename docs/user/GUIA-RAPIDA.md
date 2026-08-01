# Guía rápida — BoardComposer Studio

Para carpinteros y talladores que usan la app día a día.
Detalle de producto y arquitectura: [`../masterplan/INDEX.md`](../masterplan/INDEX.md).

## Arranque

```bash
make run
# o
.venv/bin/python -m studio.app
```

Pantalla de inicio: nuevo proyecto, abrir, recientes, demo, plantilla, docs y novedades.

## Flujo típico

1. **Nuevo proyecto** (**Ctrl+N**) — nombre y unidades (mm / pulgadas).
2. **Añadir tableros** (**Ctrl+Shift+B**) y **piezas** (**Ctrl+Shift+P**), o
   importar CSV/Excel (**Ctrl+Shift+T** / **Ctrl+Shift+O**).
3. **Calcular layout** (**Ctrl+Return**) — hace falta ≥1 tablero y ≥1 pieza;
   genera soluciones candidatas.
4. Revisar en **Workspace** (paneles, piezas, cámara).
5. Comparar en **Comparador** (**Ctrl+4**): **Re Pág** / **Av Pág** entre
   candidatas; **Ctrl+Shift+Return** aplica la elegida.
6. **Exportar** (**Ctrl+Shift+E**): SVG / PNG / JPEG / PDF / DXF / JSON / CSV.
7. **Guardar** (**Ctrl+S**) el proyecto `.bcproj`.

## Revisiones locales del `.bcproj`

Al **Guardar** sobre un archivo ya existente, Studio copia la versión anterior
en una carpeta oculta junto al proyecto (`.<nombre>.bcproj.revs/`, máx. 5).

| Acción | Cómo |
|---|---|
| Comparar | **Proyecto → Comparar revisiones .bcproj…** (**Ctrl+Shift+Y**) |
| Restaurar la última | **Proyecto → Restaurar última revisión local…** (**Ctrl+Alt+Y**) |
| Restaurar una concreta | En el diálogo de comparar, elige revisión → **Restaurar esta revisión…** |

La restauración carga el snapshot **en memoria** (misma ruta del archivo).
Queda pendiente de **Guardar** para escribirlo en disco. La pila Deshacer se
vacía al restaurar o al abrir otro proyecto.

## Atajos útiles

| Acción | Atajo |
|---|---|
| Nuevo / Abrir / Guardar | Ctrl+N / Ctrl+O / Ctrl+S |
| Guardar como | Ctrl+Shift+S |
| Preferencias | Ctrl+, |
| Añadir tablero / pieza | Ctrl+Shift+B / Ctrl+Shift+P |
| Importar tableros / piezas (CSV/Excel) | Ctrl+Shift+T / Ctrl+Shift+O |
| Calcular layout | Ctrl+Return |
| Aplicar layout del Comparador | Ctrl+Shift+Return |
| Candidata anterior / siguiente | Re Pág / Av Pág |
| Exportar solución | Ctrl+Shift+E |
| Comparar revisiones `.bcproj` | Ctrl+Shift+Y |
| Restaurar última revisión local | Ctrl+Alt+Y |
| Deshacer / Rehacer | Ctrl+Z / Ctrl+Shift+Z |
| Rotar pieza | R |
| Renombrar selección | F2 |
| Duplicar / Eliminar | Ctrl+D / Backspace |
| Cuadrícula | Ctrl+G |
| Ajustar al tablero / selección | Ctrl+0 / Ctrl+Shift+0 |
| Zoom + / − | Ctrl+= / Ctrl+- |
| Pantalla de inicio | Ctrl+Shift+H |
| Demo | Ctrl+Shift+D |
| Mostrar/ocultar docks | Ctrl+1…4 |
| Mostrar/ocultar barra | Ctrl+Shift+K |
| Documentación | Shift+F1 (o Ayuda → Documentación) |
| Atajos / Novedades | F1 / Ctrl+Shift+U |

Lista completa: **Ayuda → Atajos de teclado** (**F1**).

## Importar CSV/Excel

- **Tableros:** **Ctrl+Shift+T** — id, largo, ancho, espesor, cantidad, material.
  Ejemplo: `data/samples/studio_boards_inventory.csv`.
- **Piezas:** **Ctrl+Shift+O** — mismos campos habituales; la cantidad puede
  expandirse a varios IDs.
- Formatos: `.csv` y `.xlsx`. Tras elegir archivo, Studio muestra vista previa
  fila a fila (OK / error) antes de incorporar.

## Consejos

- Material y espesor deben ser compatibles entre pieza y tablero.
- Varias soluciones = alternativas puntuadas; tú eliges.
- Retales en Inspector son **informativos**, no inventario reutilizable automático.
- Tema claro/oscuro e idioma: **Editar → Preferencias**.
- Si te arrepientes tras varios Guardar: **Ctrl+Alt+Y** restaura la última
  copia del anillo local (luego Guardar otra vez).
- En macOS, **Ctrl** de los atajos es la tecla **⌘** (Command).

## Comprobar que todo se ve bien

Pasada visual humana: [`../../uat/studio/CHECKLIST-VISUAL.md`](../../uat/studio/CHECKLIST-VISUAL.md).
