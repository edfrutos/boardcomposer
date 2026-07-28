# Checklist visual — BoardComposer Studio

**Fecha:** _______________  
**Base / commit:** _______________  
**Versión:** `0.4.0.dev0`  
**Cómo arrancar:** `make run` o `.venv/bin/python -m studio.app`  
**Guía:** [`../../docs/user/GUIA-RAPIDA.md`](../../docs/user/GUIA-RAPIDA.md)

Marca cada ítem al **verlo** en pantalla. Objetivo: confirmar que la UI se
comporta y se ve bien de punta a punta. No es caza de bugs de borde.

Referencia funcional histórica: [`CHECKLIST-FUNCIONAL.md`](CHECKLIST-FUNCIONAL.md).

---

## 0. Arranque y chrome

- [ ] App abre con icono propio (no genérico Python).
- [ ] Pantalla de inicio: hero, CTAs, recientes, plantilla, docs, novedades.
- [ ] Tema Industrial madera coherente (claro).
- [ ] Tema oscuro vía Preferencias se ve coherente.
- [ ] Idioma es ↔ en cambia menús y textos visibles.
- [ ] Barra de estado muestra feedback al hacer acciones clave.
- [ ] Tips de estado / tooltips honestos (acciones deshabilitadas explican por qué).

---

## 1. Proyecto

- [ ] Nuevo proyecto (Ctrl+N): diálogo nombre/unidades → workspace vacío con CTAs.
- [ ] Añadir tablero (Ctrl+Shift+B): aparece en Explorador y canvas.
- [ ] Añadir pieza (Ctrl+Shift+P): aparece en Explorador.
- [ ] Guardar / Guardar como / Abrir `.bcproj`; ruta en barra de estado.
- [ ] Abrir carpeta del proyecto (Ctrl+Shift+R) si hay ruta.
- [ ] Recientes en inicio y menú; quitar / vaciar lista si aplica.
- [ ] Guardar como plantilla y crear desde plantilla (si hay plantillas).
- [ ] Renombrar proyecto (F2 / menú / clic derecho raíz).
- [ ] Cerrar o Salir con cambios sin guardar → diálogo claro (nombre, ruta, botones).

---

## 2. Explorador e Inspector

- [ ] Contadores Tableros / Piezas / Soluciones actualizan.
- [ ] Clic pieza → Inspector completo + selección en canvas.
- [ ] Clic tablero → centra cámara / resalta en Workspace.
- [ ] Menú contextual pieza: editar, duplicar, eliminar, copiar ID, renombrar.
- [ ] Menú contextual tablero: editar, duplicar, eliminar, copiar ID, renombrar.
- [ ] Clic / Enter en solución del Explorador → vista previa + tip de estado.

---

## 3. Workspace (canvas)

- [ ] Paneles físicos visibles lado a lado si cantidad > 1.
- [ ] Zoom +/- respeta límites (acciones deshabilitadas en tope).
- [ ] Pan / scroll de cámara fluido.
- [ ] Ajustar al tablero / a la selección funcionan o muestran status honesto.
- [ ] Cuadrícula Ctrl+G: visible/oculta + tip Mostrar/Ocultar.
- [ ] Selección pieza: borde/resaltado claro.
- [ ] Seleccionar todas / Invertir / Deseleccionar (Escape) según estado.
- [ ] Rotar (R) con pieza seleccionada; deshabilitado sin selección.
- [ ] Mover pieza entre paneles físicos (drag o flujo previsto) se refleja.
- [ ] Identificador / instancia de panel visible en Inspector de pieza.

---

## 4. Solver y soluciones

- [ ] Calcular layout con proyecto válido produce ≥1 solución (o mensaje claro).
- [ ] Demo (Ctrl+Shift+D) deja proyecto usable con soluciones.
- [ ] Comparador: ≥2 candidatas si el caso las genera; miniaturas legibles.
- [ ] Navegar candidatas (Re Pág / Av Pág o UI) cambia vista.
- [ ] Pin / diff de diferencias visible y comprensible.
- [ ] Explorador lista soluciones; seleccionar cambia preview.
- [ ] Piezas omitidas / solución parcial se comunican sin “falso vacío”.

---

## 5. Importación CSV

- [ ] Importar inventario de tableros desde CSV de muestra.
- [ ] Vista previa por fila (válida / error) antes de incorporar.
- [ ] Tras aceptar, tableros aparecen en Explorador con material/espesor.

---

## 6. Exportación

- [ ] Exportar solución (menú/flujo) completa sin error visible.
- [ ] Opción abrir después (si existe) abre el artefacto.
- [ ] Export con open-after no deja la UI colgada.

---

## 7. Docks, barra y navegación UI

- [ ] Toggle docks Ctrl+1…4: tip Mostrar/Ocultar + status.
- [ ] Toggle barra Ctrl+Shift+K: tip Mostrar/Ocultar + status.
- [ ] Pantalla de inicio Ctrl+Shift+H: tip si ya estás en Welcome.
- [ ] Preferencias (Ctrl+,): unidades, idioma, tema aplican al cerrar.

---

## 8. Ayuda

- [ ] Ayuda → Documentación abre la guía rápida (`docs/user/GUIA-RAPIDA.md`).
- [ ] Ayuda → Novedades muestra bullets de CHANGELOG Unreleased.
- [ ] Ayuda → Atajos lista atajos legibles.
- [ ] Acerca de muestra nombre/versión coherente.

---

## 9. Multipanel (visual)

- [ ] Tablero con varios paneles físicos: layout multipanel legible.
- [ ] Material/espesor incompatibles: mensaje o rechazo claro al resolver/colocar.
- [ ] Retales informativos visibles; no se comportan como stock editable.
- [ ] Benchmark / caso muestra no rompe la UI (opcional).

---

## 10. Cierre de pasada

- [ ] Sin pantallas en blanco persistentes tras flujos anteriores.
- [ ] Sin diálogos de error crudos no recuperables en el camino feliz.
- [ ] Notas libres (bugs visuales / copy):

```
(anotar aquí)
```

**Resultado:** [ ] OK para uso diario  ·  [ ] Con reservas  ·  [ ] Bloqueante

**Revisor:** _______________
