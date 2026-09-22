# SCR-004 — Inspector Contextual

**Módulo:** BoardComposer Studio

**Código:** SCR-004  
**Versión:** 1.4.0  
**Estado:** Alineado con Studio  
**Última revisión:** 22/09/2026

---

## Objetivo

El Inspector es el dock contextual de solo lectura que responde a una pregunta:

> **¿Qué necesito saber ahora sobre lo seleccionado?**

Muestra texto plano según el contexto (pieza, tablero, solución, vacío o
diagnóstico). La edición de datos se hace en diálogos / comandos, no en este
panel.

---

## Dónde vive en Studio

- Dock derecho `Inspector`.
- Mostrar/ocultar: **Ver → Inspector** (**Ctrl+2**).
- Se actualiza al cambiar la selección del Explorador o del Workspace.

---

## Distribución actual

```text
┌───────────────────────────────┐
│ Inspector (QTextEdit RO)      │
├───────────────────────────────┤
│ Título del contexto           │
│ Propiedades / métricas        │
│ (retales, highlights, diag…)  │
└───────────────────────────────┘
```

No hay botones de acción ni campos editables en el dock.

---

## Contextos implementados

### Sin selección

Mensaje «Sin selección». Casos: canvas vacío, limpieza de selección,
multiselección de piezas, pieza huérfana.

### Raíz / categorías del Explorador

**Raíz del proyecto:** nombre, cliente, referencia, notas, kerf
(prefs.units) más conteos (tableros tipos/físicos, piezas
colocadas/sin colocar, soluciones), materiales distintos y área de
stock (prefs.units²). Aviso si las soluciones están desactualizadas.

**Tableros:** tipos, físicos (suma de cantidades), retales de
inventario, materiales y área de stock.

**Piezas:** total, colocadas, sin colocar, materiales y área de piezas
(prefs.units²).

**Soluciones:** candidatas, seleccionada `i / n` si hay layout; aviso
si desactualizadas; «sin candidatas» si el cache está vacío.

Solo lectura. Sin edición inline.

### Tablero (stock)

- Id
- Dimensiones L×A (unidades de preferencias)
- Espesor (prefs)
- Cantidad
- Material
- Aprovechamiento (IDE-0051): instancias usadas, piezas, % uso y
  material libre sobre instancias consumidas; retales del panel si la
  solución los reporta. Sin layout: mensaje vacío. Sin piezas en el
  tablero: 0 instancias. Preview de la candidata gana sobre placements
  aplicados.

### Pieza

- Id, L×A (prefs), espesor (prefs), material
- Rotación: `0°` / `90°` si colocada; `—` si no hay placement
- Veta: libre (puede rotar) o fija (no rotar)
- Si no hay placement: indicación de no colocada
- Si colocada: posición x,y (prefs) y **panel físico / instancia**
  (`board · instancia i/n` cuando `quantity > 1`)

No muestra en el Inspector: canto (sí en el diálogo Editar…).

### Solución / layout calculado

Al seleccionar una candidata (Comparador, Explorador o tras calcular):

- Índice y estrategia
- Piezas colocadas / omitidas (si parcial)
- Largo y ancho totales (unidades de preferencias; persistencia mm)
- Huecos internos % y material libre %
- Coste estimado de material (€; tableros físicos × €/m² del catálogo;
  «—» si el material no tiene precio; `*` si el coste es parcial)
- Aviso si las soluciones están desactualizadas respecto al proyecto
- Highlights del Comparador («mejor en…») si hay ≥ 2 candidatas
- Fortalezas / debilidades cuando existen
- Retales aprovechables: conteo + área total (prefs.units²) si `offcuts`
  no vacío. JSON / Core siguen en mm².
- Bloque de diagnóstico del solver al final cuando aplica

### Sin solución

Tras un cálculo sin candidatas: título «Sin solución» + estadísticas del
pipeline (generadas / únicas / aceptadas / rechazadas y motivos). Si el
usuario canceló: mensaje de cancelación sin diagnóstico.

---

## Sincronización

| Origen | Efecto en Inspector |
|--------|---------------------|
| Clic pieza en Workspace | Detalle de pieza + sync Explorador |
| Clic tablero en canvas | Detalle de tablero + sync Explorador |
| Clic vacío | «Sin selección» |
| Selección en Explorador | Contexto según tipo de ítem |
| Cambio de candidata (Comparador / Re-Av Pág) | Resumen de layout |

---

## Criterios de aceptación

- Cambio de contexto inmediato y sin formularios en el dock.
- Raíz y categorías del Explorador muestran conteos, materiales y área
  (no solo la etiqueta).
- Pieza colocada identifica panel e instancia.
- Solución parcial y retales informativos visibles cuando existen.
- Diagnóstico útil cuando el solver no devuelve candidatas.
- Toggle **Ctrl+2** no pierde el último contexto al volver a mostrar.

---

## Relación con otras pantallas

- SCR-002 — Workspace (selección).
- SCR-003 — Comparador (candidata + highlights).
- SCR-005 — Proyecto / Explorador.
- SCR-006 — Preferencias (unidades de display en pieza/tablero/layout).
- ADR-016 — Retales informativos.

---

## Límites conocidos (Studio actual)

- Solo lectura: no edita propiedades inline.
- Contexto de proyecto/categoría: conteos, materiales y área (IDE-0050).
  Sin edición inline.
- Unidades de prefs en pieza, tablero, kerf, posición y métricas de layout
  (IDE-0040). Disco / `.bcproj` / JSON siguen en mm.
- Pieza: espesor, rotación 0°/90° y veta (IDE-0046). Canto sigue en
  Editar…, no en el dock.
- Tablero: aprovechamiento de panel (IDE-0051). Sin edición inline.
- Sin contexto «algoritmo» dedicado (parámetros viven en Preferencias).

---

## Evolución prevista

- Resumen rico de proyecto/categoría entregado (IDE-0050).
- Aprovechamiento de tablero entregado (IDE-0051).
- Edición inline de campos seguros.
- Unidades en Comparador entregadas (IDE-0047).
- Gráficos / historial del elemento seleccionado.
