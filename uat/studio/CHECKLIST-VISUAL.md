# Checklist visual — BoardComposer Studio

**Fecha:** 2026-07-28 (taller 0019–0024: 2026-09-14)  
**Base / commit:** `main` post-IDE-0019…0024  
**Versión:** `0.4.3`  
**Cómo arrancar:** `make run` o `.venv/bin/python -m studio.app`  
**Guía:** [`../../docs/user/GUIA-RAPIDA.md`](../../docs/user/GUIA-RAPIDA.md)

Marca cada ítem al **verlo** en pantalla. Objetivo: confirmar que la UI se
comporta y se ve bien de punta a punta. No es caza de bugs de borde.

Referencia funcional histórica: [`CHECKLIST-FUNCIONAL.md`](CHECKLIST-FUNCIONAL.md).

---

## 0. Arranque y chrome

- [x] App abre con icono propio (no genérico Python).
- [x] Pantalla de inicio: hero, CTAs, recientes, plantilla, docs, novedades, atajos, acerca.
- [x] Tema Industrial madera coherente (claro).
- [x] Tema oscuro vía Preferencias se ve coherente.
- [x] Tema **sistema**: Preferencias usan chrome OS (no parchment Welcome/help).
- [x] Idioma es ↔ en cambia menús y textos visibles.
- [x] Barra de estado muestra feedback al hacer acciones clave.
- [x] Tips de estado / tooltips honestos (acciones deshabilitadas explican por qué).

---

## 1. Proyecto

- [x] Nuevo proyecto (Ctrl+N): diálogo nombre/unidades → workspace vacío con CTAs.
- [x] Añadir tablero (Ctrl+Shift+B): aparece en Explorador y canvas.
- [x] Añadir pieza (Ctrl+Shift+P): aparece en Explorador.
- [x] Guardar / Guardar como / Abrir `.bcproj`; basename en barra de estado (tooltip = ruta; clic abre carpeta).
- [x] Abrir carpeta del proyecto (Ctrl+Shift+R) si hay ruta.
- [x] Comparar revisiones `.bcproj` (Ctrl+Shift+Y): diálogo abre con proyecto actual y muestra diff textual comprensible.
- [x] Restaurar última revisión (Ctrl+Alt+Y / menú Proyecto): confirmación clara; status y dirty tras restaurar.
- [x] Exportar backup de revisiones (Ctrl+Alt+B): diálogo carpeta → «Carpeta creada» / Abrir carpeta.
- [x] Recientes en inicio y menú; quitar / vaciar lista si aplica.
- [x] Guardar como plantilla y crear desde plantilla (si hay plantillas).
- [x] Renombrar proyecto (F2 / menú / clic derecho raíz).
- [x] Metadatos del proyecto (**Ctrl+Alt+M**): cliente / referencia / notas.
- [x] Espesor de sierra (**Ctrl+Alt+K**): diálogo mm; Inspector en raíz.
- [ ] Catálogo (**Ctrl+Alt+T**): botones Exportar/Importar JSON visibles.
- [x] Cerrar o Salir con cambios sin guardar → diálogo claro (nombre, ruta, botones).

---

## 2. Explorador e Inspector

- [x] Contadores Tableros / Piezas / Soluciones actualizan.
- [x] Clic pieza → Inspector completo + selección en canvas.
- [ ] Preferencias cm/in: Inspector muestra esas unidades en dims, kerf,
  posición y métricas de layout (no mm hardcodeados).
- [x] Clic tablero → centra cámara / resalta en Workspace.
- [x] Menú contextual pieza: editar, duplicar, eliminar, copiar ID, renombrar.
- [x] Menú contextual tablero: editar, duplicar, eliminar, copiar ID, renombrar.
- [x] Clic / Enter en solución del Explorador → vista previa + tip de estado.

---

## 3. Workspace (canvas)

- [x] Paneles físicos visibles lado a lado si cantidad > 1.
- [x] Zoom +/- respeta límites (acciones deshabilitadas en tope).
- [x] Pan / scroll de cámara fluido.
- [x] Ajustar al tablero / a la selección funcionan o muestran status honesto.
- [x] Cuadrícula Ctrl+G: visible/oculta + tip Mostrar/Ocultar.
- [x] Selección pieza: borde/resaltado claro.
- [x] Seleccionar todas / Invertir / Deseleccionar (Escape) según estado.
- [x] Rotar (R) con pieza seleccionada; deshabilitado sin selección o con
  veta fija (status lo dice).
- [x] Intercambiar dos piezas colocadas (**Ctrl+Alt+X**); no-op visible si
  no caben.
- [x] Sugerir hueco (**Ctrl+Alt+G**); drop que solapa ajusta al hueco
  cercano.
- [x] Mover pieza entre paneles físicos (drag o flujo previsto) se refleja.
- [x] Identificador / instancia de panel visible en Inspector de pieza.

---

## 4. Solver y soluciones

- [x] Calcular layout con proyecto válido produce ≥1 solución (o mensaje claro).
- [x] Demo (Ctrl+Shift+D) deja proyecto usable con soluciones.
- [x] Comparador: ≥2 candidatas si el caso las genera; miniaturas legibles.
- [x] Navegar candidatas (Re Pág / Av Pág o UI) cambia vista.
- [x] Pin / diff de diferencias visible y comprensible.
- [x] Tras editar inventario con soluciones: banner desactualizadas + CTA
  **Calcular layout**.
- [x] Explorador lista soluciones; seleccionar cambia preview.
- [x] Piezas omitidas / solución parcial se comunican sin “falso vacío”.

---

## 5. Importación CSV

- [x] Importar inventario de tableros desde CSV de muestra.
- [x] Vista previa por fila (válida / error) antes de incorporar.
- [x] Tras aceptar, tableros aparecen en Explorador con material/espesor.

---

## 6. Exportación

- [x] Exportar solución (menú/flujo) completa sin error visible.
- [ ] Exportar plano: cotas L×A del tablero visibles; desmarcar la casilla
  las quita sin cambiar piezas ni retales.
- [ ] Exportar plano: pie de trazabilidad (versión, algoritmo, fecha)
  visible; desmarcar la casilla lo quita. JSON/CSV deshabilitan la
  casilla.
- [ ] Exportar DXF: capas por rol visibles en el CAD; cotas en DIMS,
  pie en META.
- [ ] Exportar PNG/JPEG: subir DPI agranda el archivo; bajar calidad JPEG
  lo aligera.
- [x] Lista de corte (**Ctrl+Alt+C**): elige CSV o PDF; no es el CSV del
  diálogo de solución.
- [x] Opción abrir después (si existe) abre el artefacto.
- [x] Export con open-after no deja la UI colgada.

---

## 7. Docks, barra y navegación UI

- [x] Toggle docks Ctrl+1…4: tip Mostrar/Ocultar + status.
- [x] Toggle barra Ctrl+Shift+K: tip Mostrar/Ocultar + status.
- [x] Pantalla de inicio Ctrl+Shift+H: tip si ya estás en Welcome.
- [x] Preferencias (Ctrl+,): unidades, idioma, tema aplican al cerrar.

---

## 8. Ayuda

- [x] Ayuda → Documentación abre la guía rápida (`docs/user/GUIA-RAPIDA.md`).
- [x] Ayuda → Novedades muestra bullets de CHANGELOG Unreleased.
- [x] Ayuda → Atajos lista atajos legibles (incl. Ctrl+Alt+B / E / M / K / X / C).
- [x] Ayuda → Explicar candidata (Ctrl+Alt+E): texto + Copiar tras Calcular layout.
- [x] Acerca de muestra nombre/versión coherente.

---

## 9. Multipanel (visual)

- [x] Tablero con varios paneles físicos: layout multipanel legible.
- [x] Material/espesor incompatibles: mensaje o rechazo claro al resolver/colocar.
- [x] Retales informativos visibles; no se comportan como stock editable.
- [x] Benchmark / caso muestra no rompe la UI (opcional).

---

## 10. Cierre de pasada

- [x] Sin pantallas en blanco persistentes tras flujos anteriores.
- [x] Sin diálogos de error crudos no recuperables en el camino feliz.
- [x] Notas libres (bugs visuales / copy):

```text
Cobertura visual completada; regresión auto añadida para preview por fila.
```

**Resultado:** [x] OK para uso diario  ·  [ ] Con reservas  ·  [ ] Bloqueante

**Revisor:** edefrutos

---

## Resultado

- 0 Arranque: OK (tema/idioma/tips)
- 1 Proyecto: OK (save/reveal/template)
- 2 Explorador/Inspector: OK (contextuales)
- 3 Workspace: OK (selección/rotar verificado)
- 4 Solver/soluciones: OK (comparador multi-candidata)
- 5 Importación: OK (preview fila válida/error verificado)
- 6 Exportación: OK (open-after)
- 7 Docks/barra: OK (tips Mostrar/Ocultar)
- 8 Ayuda: OK (guía rápida)
- 9 Multipanel: OK (material/retales)
- 10 Cierre: OK (uso diario)

**Veredicto:** Listo para uso diario de Studio.
