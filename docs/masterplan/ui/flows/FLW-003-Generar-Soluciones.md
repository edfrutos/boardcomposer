# FLW-003 — Generar Soluciones

**Módulo:** BoardComposer Studio

**Código:** FLW-003
**Versión:** 1.1.0
**Estado:** En revisión
**Última revisión:** 17/07/2026

---

## Objetivo

Describir el flujo mediante el cual BoardComposer genera una o varias soluciones de optimización a partir de un proyecto, permitiendo al usuario explorar alternativas en lugar de recibir un único resultado.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Existe un proyecto válido.
- Hay al menos un tablero y una pieza.
- Las restricciones han sido validadas.

---

## Flujo principal

1. El usuario pulsa **Generar soluciones**.
2. Studio recopila la configuración activa del proyecto.
3. El Core valida los datos de entrada.
4. Se muestra un diálogo de progreso modal; el cálculo corre en segundo plano.
5. Se ejecutan los algoritmos seleccionados (con cancelación cooperativa entre generadores y candidatas).
6. Cada solución es evaluada y puntuada.
7. Las soluciones se ordenan según el perfil de evaluación activo.
8. Studio actualiza el Workspace y el Comparador.
9. El usuario comienza la exploración de resultados.

---

## Flujo alternativo A — Configuración incompleta

1. Se detecta una restricción o dato obligatorio ausente.
2. Studio muestra el problema y ofrece acceder directamente a la pantalla correspondiente.
3. La generación no comienza hasta resolver la incidencia.

---

## Flujo alternativo B — Sin solución válida

1. Ningún algoritmo encuentra una solución aceptable.
2. Studio informa del motivo.
3. Se sugieren posibles acciones (permitir rotación, cambiar tableros, revisar restricciones, etc.).

---

## Flujo alternativo C — Cancelación del cálculo

1. El usuario pulsa **Cancelar** en el diálogo de progreso.
2. Studio marca el token de cancelación cooperativa.
3. El pipeline interrumpe entre generadores o candidatas y no aplica resultados parciales.
4. El Workspace/Comparador se limpian de soluciones previas del cálculo y se informa del cancelado.

---

## Eventos generados

- SolutionGenerationStarted
- AlgorithmStarted
- SolutionGenerated
- SolutionEvaluated
- SolutionRankingUpdated
- WorkspaceUpdated

---

## Resultado esperado

El usuario dispone de una colección de soluciones clasificadas, explicadas y listas para inspección, comparación o exportación.

---

## Criterios de aceptación

- La generación muestra progreso cuando el cálculo supera un tiempo apreciable.
- El usuario puede cancelar el cálculo en curso; el solver responde de forma cooperativa.
- El usuario puede identificar qué algoritmos han participado.
- Cada solución conserva su explicación y métricas.
- El proceso queda registrado en el historial del proyecto.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.

---

## Observaciones

En versiones futuras este flujo incorporará ejecución en paralelo y
generación incremental de soluciones. El Timeline (ADR-005) ya registra el
inicio/fin del cálculo y permite reproducir las colocaciones de la solución
seleccionada; el Timeline registra las fases de cada algoritmo (`AlgorithmStarted`/`Finished` con duración), permite filtrar por algoritmo y muestra los fallos de colocación MaxRects (`PlacementFailed` / resumen).
