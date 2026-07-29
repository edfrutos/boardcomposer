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

1. **Nuevo proyecto** (Ctrl+N) — nombre y unidades (mm / pulgadas).
2. **Añadir tableros** (Ctrl+Shift+B) y **piezas** (Ctrl+Shift+P), o importar CSV.
3. **Calcular layout** — genera soluciones candidatas.
4. Revisar en **Workspace** (paneles, piezas, cámara).
5. Comparar en **Comparador** / **Explorador de soluciones**.
6. **Exportar** la solución elegida (imagen / datos según menú).
7. **Guardar** (Ctrl+S) el proyecto `.bcproj`.

## Atajos útiles

| Acción | Atajo |
|---|---|
| Nuevo / Abrir / Guardar | Ctrl+N / Ctrl+O / Ctrl+S |
| Guardar como | Ctrl+Shift+S |
| Preferencias | Ctrl+, |
| Añadir tablero / pieza | Ctrl+Shift+B / Ctrl+Shift+P |
| Calcular layout | (menú Solucionar / barra) |
| Rotar pieza | R |
| Cuadrícula | Ctrl+G |
| Ajustar al tablero / selección | menú Vista |
| Pantalla de inicio | Ctrl+Shift+H |
| Demo | Ctrl+Shift+D |
| Mostrar/ocultar docks | Ctrl+1…4 |
| Mostrar/ocultar barra | Ctrl+Shift+K |
| Documentación | Ayuda → Documentación |
| Novedades | Ayuda → Novedades |
| Atajos | Ayuda → Atajos de teclado |

Lista completa: **Ayuda → Atajos de teclado**.

## Importar CSV de tableros

Formato típico: id, largo, ancho, espesor, cantidad, material.
Ejemplo: `data/samples/studio_boards_inventory.csv`.
Tras importar, Studio muestra vista previa fila a fila antes de incorporar.

## Consejos

- Material y espesor deben ser compatibles entre pieza y tablero.
- Varias soluciones = alternativas puntuadas; tú eliges.
- Retales en Inspector son **informativos**, no inventario reutilizable automático.
- Tema claro/oscuro e idioma: **Editar → Preferencias**.

## Comprobar que todo se ve bien

Pasada visual humana: [`../../uat/studio/CHECKLIST-VISUAL.md`](../../uat/studio/CHECKLIST-VISUAL.md).
