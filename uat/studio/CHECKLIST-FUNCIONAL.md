# Checklist humana — funcionalidad Studio (post polish bt)

**Fecha:** 2026-07-20  
**Base:** `main` tras PR #121 (`Ctrl+Shift+E` exportar)  
**Versión:** `0.4.0.dev0` (Unreleased)  
**Cómo arrancar:** `make run` o `.venv/bin/python -m studio.app`

Marca cada ítem al comprobarlo. Objetivo: ver **qué hay implementado y usable**, no buscar bugs de borde.

---

## 0. Arranque y entorno

- [ ] La app abre con icono propio (no el genérico de Python).
- [ ] Pantalla de inicio (SCR-001): hero, CTAs, recientes, plantilla, docs/novedades; volver con **Ctrl+Shift+H**.
- [ ] Tema «Industrial madera» se ve coherente (claro/oscuro vía Preferencias).
- [ ] Idioma es/en cambia menús y tip de estado (`Editar → Preferencias…`).

---

## 1. Proyecto (SCR-005 / FLW-001)

- [ ] **Nuevo proyecto** pide nombre y unidades; aparece workspace vacío con CTAs.
- [ ] **Añadir tablero** (**Ctrl+Shift+B**) y **añadir pieza** (**Ctrl+Shift+P**) (menú / Explorador / CTA vacío).
- [ ] **Guardar** / **Abrir** `.bcproj`; ruta visible en la barra de estado; **Ctrl+Shift+R** abre la carpeta.
- [ ] **Recientes** en inicio y menú; quitar fantasma / vaciar lista si aplica.
- [ ] **Plantilla de proyecto**: guardar y crear desde plantilla (**Ctrl+Shift+N**).
- [ ] Cerrar con cambios sin guardar → diálogo claro (nombre/ruta/botones).
- [ ] **Renombrar proyecto** (menú o clic derecho en raíz del Explorador / F2).

---

## 2. Explorador e Inspector

- [ ] Contadores `Tableros (n)`, `Piezas (n)`, `Soluciones (n)`.
- [ ] Clic en **pieza** → Inspector completo + selección en canvas.
- [ ] Clic en **tablero** → centra cámara y resalta en Workspace.
- [ ] Menú contextual pieza: editar / duplicar / eliminar / copiar ID / renombrar.
- [ ] Menú contextual tablero: editar / duplicar / eliminar / copiar ID / renombrar.
- [ ] Doble clic en **solución** del Explorador → vista previa.

---

## 3. Workspace (SCR-002)

- [ ] Paneles físicos lado a lado (cantidad > 1 en un tablero).
- [ ] Arrastrar pieza dentro del panel; soltar en **otro panel** reasigna instancia.
- [ ] Solape inválido revierte el movimiento.
- [ ] Zoom: rueda / **Ctrl+=** / **Ctrl+-**; % en barra de estado.
- [ ] **Ctrl+0** ajusta a todos los tableros; **Ctrl+Shift+0** a la selección.
- [ ] Pan: botón medio, botón derecho, **Espacio + arrastre**.
- [ ] Clic en vacío deselecciona; **Ctrl+A** / **Esc** / **Ctrl+Shift+I**.
- [ ] **Flechas** mueven 1 mm; **Shift+flechas** = tamaño de cuadrícula (prefs).
- [ ] **R** rota si cabe; si no, se rechaza.
- [ ] Doble clic pieza/tablero → editar; vacío → ajustar vista.
- [ ] **Enter** edita selección; **F2** renombra; **Ctrl+Shift+C** copia ID.
- [ ] **Ctrl+D** duplica pieza o tablero enfocado.
- [ ] **Delete/Backspace** elimina pieza o tablero enfocado (con confirmación).
- [ ] **Ctrl+G** muestra/oculta cuadrícula.
- [ ] Docks: Ver → Explorador / Inspector / Timeline / Comparador; restablecer disposición (**Ctrl+Shift+W**).

---

## 4. Layout / Comparar / Exportar (flujo estrella)

- [ ] **Ctrl+Return** calcula layout (progreso + Cancelar funcionan).
- [ ] Aparecen soluciones en Comparador + Explorador.
- [ ] **Re Pág / Av Pág** recorren candidatas (preview en canvas + status).
- [ ] **Ctrl+Shift+Return** aplica la solución al proyecto.
- [ ] Editar pieza tras aplicar → aviso de soluciones **desactualizadas**.
- [ ] Comparador: ordenar, filtrar «solo completas», miniaturas, fijar referencia + diff.
- [ ] **Ctrl+Shift+E** abre exportar solución (SVG/PDF/DXF/JSON/CSV + preview).
- [ ] Tras exportar, opción de abrir archivo/carpeta.

---

## 5. Importación (FLW-002)

- [ ] Importar **tableros** CSV/Excel (**Ctrl+Shift+T**) con vista previa.
- [ ] Importar **piezas** CSV/Excel (**Ctrl+Shift+O**; cantidad expandida si aplica).
- [ ] Excel multi-hoja: selector de hoja.
- [ ] Si fallan columnas: asistente de mapeo + guardar/reaplicar/eliminar plantilla.
- [ ] Importación **deshacible** (Ctrl+Z).

---

## 6. Timeline (ADR-005)

- [ ] Eventos del cálculo aparecen en el dock.
- [ ] Replay colocaciones / fases (no muta el proyecto).
- [ ] Filtros por algoritmo / periodo; marcador de usuario.
- [ ] Clic en hecho → busca contexto.
- [ ] Exportar historial Timeline JSON/CSV (**Ctrl+Shift+L**).

---

## 7. Preferencias y ayuda (SCR-006)

- [ ] Tema, idioma, unidades, grid, estrategia/pesos, máx. soluciones, defaults export.
- [ ] Geometría de ventana/docks se recuerda al reiniciar.
- [ ] **Ayuda → Atajos de teclado…** (**F1**) lista el catálogo (incl. PgUp/PgDown, Ctrl+Shift+Return/E).
- [ ] Ayuda → Novedades / Documentación / Acerca de (icono correcto).

---

## 8. Multipanel / Core (smoke)

- [ ] Proyecto con 2+ tipos o cantidades: solver usa paneles físicos.
- [ ] Material/espesor incompatible → pieza omitida o fallo visible (parcial).
- [ ] Inspector muestra panel + instancia; retales informativos si hay.
- [ ] Guardar/reabrir `.bcproj` conserva colocaciones e inventario.

---

## Resultado

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 0 Arranque | | |
| 1 Proyecto | | |
| 2 Explorador/Inspector | | |
| 3 Workspace | | |
| 4 Layout→Export | | |
| 5 Importación | | |
| 6 Timeline | | |
| 7 Preferencias/Ayuda | | |
| 8 Multipanel | | |

**Veredicto:** □ Listo para uso diario de estudio  □ Faltan huecos (anotar arriba)  □ Solo regresión automatizada

**Regresión auto (opcional):** `make test` → 562+ passed.
