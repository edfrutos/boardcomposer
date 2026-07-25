# FLW-003 — Generar Soluciones

**Módulo:** BoardComposer Studio

**Código:** FLW-003  
**Versión:** 1.2.0  
**Estado:** Alineado con Studio  
**Última revisión:** 25/07/2026

---

## Objetivo

Describir cómo Studio calcula candidatas de layout a partir del proyecto
actual, con progreso cancelable, ranking truncado y actualización del
Comparador / Inspector.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Hay un proyecto cargado (nuevo, abierto o demo).
- Idealmente hay tableros y piezas; el flujo no bloquea con un wizard de
  validación previa — un inventario vacío o incompatible acaba en 0
  candidatas + diagnóstico.

---

## Trigger

| Control | Atajo |
|---------|--------|
| Generar → Calcular layout | **Ctrl+Return** |
| Botón toolbar «Calcular layout» | igual |

Preferencias que afectan el cálculo (SCR-006):

- estrategia (`balanced` / `material` / `compact` / `exact`)
- pesos custom (opcional)
- `max_solutions` (1–100; trunca el ranking final)

---

## Flujo principal

1. El usuario dispara **Calcular layout**.
2. Studio abre un diálogo modal de progreso (indeterminado) con **Cancelar**.
3. Un worker en hilo secundario convierte el proyecto Studio → Core y ejecuta
   el pipeline (`GeometrySolver` / MaxRects multipanel según inventario).
4. Generación → deduplicación → evaluación → ranking.
5. Se conservan como máximo `max_solutions` candidatas; la seleccionada pasa
   a ser la de índice 0 (mejor score).
6. Se limpia el flag «soluciones desactualizadas».
7. Studio actualiza Comparador (tabla + miniaturas) e Inspector (métricas /
   diagnóstico). El preview en Workspace ocurre al seleccionar candidata
   (clic / **Re Pág** / **Av Pág**), no automáticamente al terminar el
   cálculo.
8. El usuario explora (FLW-004), aplica (**Ctrl+Shift+Return**) o exporta
   (FLW-005).

Una sola candidata tras el ranking es un resultado **válido** (dedupe /
inventario restringido).

---

## Flujo alternativo A — Sin candidatas

1. El pipeline termina con lista vacía (incompatible, no cabe, etc.).
2. Comparador vacío; Inspector muestra diagnóstico
   (`stats_summary_lines`: generadas / únicas / aceptadas / rechazadas +
   motivos).
3. Status: no se pudo calcular layout.
4. El usuario ajusta inventario/material/espesor y vuelve a calcular.

---

## Flujo alternativo B — Cancelación

1. El usuario pulsa **Cancelar** en el progreso.
2. Se marca el token de cancelación cooperativa; el pipeline corta entre
   generadores/candidatas.
3. **No** se conservan resultados parciales: la lista de soluciones queda
   vacía.
4. Inspector / status informan del cálculo cancelado.

---

## Flujo alternativo C — Error

1. Excepción en el worker.
2. Evento `SolutionGenerated` con `status=error`.
3. Status muestra el mensaje; no se aplica layout.

---

## Soluciones desactualizadas

- Editar el proyecto con impacto en layout marca `solutions_outdated`.
- Banner en el Comparador: el proyecto cambió; conviene volver a generar.
- **Aplicar** con outdated pide confirmación.
- Un cálculo nuevo limpia el flag.

---

## Eventos relevantes (Timeline)

Emitidos en la práctica:

- `SolutionGenerationStarted` (strategy)
- Traza de algoritmos: `AlgorithmStarted` / `AlgorithmFinished`,
  `EvaluationFinished`, `PlacementFailed` / resumen
- `SolutionGenerated` (`ok` | `partial` | `none` | `cancelled` | `error`,
  + `count` cuando aplica)
- `SolutionsMarkedOutdated` al editar con impacto

`WorkspaceUpdated` aparece al **aplicar** layout, no al terminar el cálculo.

---

## Resultado esperado

El usuario dispone de 0…N candidatas rankeadas (tope `max_solutions`), con
métricas/explicación cuando existen, listas para comparar, aplicar o
exportar. El Timeline registra inicio/fin y fases del solver.

---

## Criterios de aceptación

- Progreso modal con Cancelar cooperativo.
- Cancelar no deja candidatas a medias.
- 0 candidatas → diagnóstico usable en Inspector.
- ≥1 candidata → Comparador e Inspector actualizados.
- `max_solutions` y estrategia salen de Preferencias.
- Timeline refleja el cálculo y permite replay de fases/colocaciones.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- SCR-006 — Preferencias.
- FLW-004 — Comparar.
- FLW-005 — Exportar.
- ADR-005 — Timeline.

---

## Límites conocidos

- Sin validación previa amigable «faltan tableros/piezas» antes de lanzar.
- Preview del canvas no se fuerza al acabar el solve (hay que seleccionar).
- Solo MaxRects cubre el contrato multipanel completo (`exact` = un panel).
