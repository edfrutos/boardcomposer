# SCR-004 — Inspector Contextual

**Módulo:** BoardComposer Studio

**Código:** SCR-004  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 24/07/2026

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

Solo la etiqueta del ítem del árbol (nombre de proyecto, «Tableros…»,
«Piezas…», «Soluciones…»). Sin resumen enriquecido.

### Tablero (stock)

- Id
- Dimensiones L×A (unidades de preferencias)
- Espesor (prefs)
- Cantidad
- Material

Sin métricas de aprovechamiento del panel en este contexto.

### Pieza

- Id, L×A (prefs), material
- Si no hay placement: indicación de no colocada
- Si colocada: posición x,y (prefs) y **panel físico / instancia**
  (`board · instancia i/n` cuando `quantity > 1`)

No muestra en el Inspector: espesor de pieza, rotación ni canto (sí en el
diálogo Editar…).

### Solución / layout calculado

Al seleccionar una candidata (Comparador, Explorador o tras calcular):

- Índice y estrategia
- Piezas colocadas / omitidas (si parcial)
- Largo y ancho totales (texto en mm en i18n actual)
- Huecos internos % y material libre %
- Aviso si las soluciones están desactualizadas respecto al proyecto
- Highlights del Comparador («mejor en…») si hay ≥ 2 candidatas
- Fortalezas / debilidades cuando existen
- Retales aprovechables: conteo + área total (mm²) si `offcuts` no vacío
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
- Pieza colocada identifica panel e instancia.
- Solución parcial y retales informativos visibles cuando existen.
- Diagnóstico útil cuando el solver no devuelve candidatas.
- Toggle **Ctrl+2** no pierde el último contexto al volver a mostrar.

---

## Relación con otras pantallas

- SCR-002 — Workspace (selección).
- SCR-003 — Comparador (candidata + highlights).
- SCR-005 — Proyecto / Explorador.
- SCR-006 — Preferencias (unidades de display en pieza/tablero).
- ADR-016 — Retales informativos.

---

## Límites conocidos (Studio actual)

- Solo lectura: no edita propiedades inline.
- Contexto de proyecto/categoría muy pobre (solo etiqueta).
- Unidades de prefs en pieza/tablero; métricas de layout y retales aún en mm
  hardcodeados en strings i18n.
- Sin contexto «algoritmo» dedicado (parámetros viven en Preferencias).

---

## Evolución prevista

- Resumen rico de proyecto/categoría.
- Edición inline de campos seguros.
- Unidades coherentes en todas las métricas.
- Gráficos / historial del elemento seleccionado.
