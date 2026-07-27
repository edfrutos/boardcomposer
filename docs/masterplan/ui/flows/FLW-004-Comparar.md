# FLW-004 — Comparar Soluciones

**Módulo:** BoardComposer Studio

**Código:** FLW-004  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 25/07/2026

---

## Objetivo

Describir cómo el usuario explora las candidatas del último cálculo, compara
métricas/diferencias y elige una para aplicar o exportar.

Detalle de UI: SCR-003. Generación previa: FLW-003.

---

## Actor principal

- Usuario.

---

## Precondiciones

- Se ha ejecutado **Calcular layout** (FLW-003), con 0…N candidatas.
- Para el panel de diferencias y highlights «mejor en…» hacen falta **≥ 2**
  candidatas. Con 0 o 1 el Comparador sigue siendo usable (tabla/preview),
  pero no hay diffs.

---

## Trigger / acceso

| Control | Atajo |
|---------|--------|
| Ver → Comparador de soluciones | **Ctrl+4** |
| Selección tras calcular | dock inferior (tabificado con Timeline) |
| Solución anterior / siguiente | **Re Pág** / **Av Pág** |
| Aplicar layout calculado | **Ctrl+Shift+Return** |
| Exportar solución seleccionada | **Ctrl+Shift+E** (FLW-005) |

---

## Flujo principal (≥ 2 candidatas)

1. Tras FLW-003, el Comparador lista candidatas (miniaturas + tabla).
2. El usuario abre el dock si hace falta (**Ctrl+4**).
3. Opcional: ordenar (ranking / piezas / huecos / tablero libre / score) y
   filtrar «solo completas».
4. Opcional: **Fijar como referencia** la candidata actual (base del panel de
   diferencias; se reinicia al volver a calcular).
5. Clic en fila/miniatura (o **Re Pág** / **Av Pág**) → preview en Workspace +
   Inspector; evento `SolutionSelected`.
6. Revisar highlights («mejor en» piezas / huecos / score / tablero libre /
   largo / ancho) y el texto de
   diferencias vs referencia.
7. Elegir destino:
   - **Aplicar** → placements al proyecto (`WorkspaceUpdated`,
     `reason=apply_layout`); confirma si hay banner outdated.
   - **Exportar** → FLW-005 / SCR-007.
   - Seguir editando el proyecto → puede marcar soluciones desactualizadas
     (volver a FLW-003).

---

## Flujo alternativo A — 0 candidatas

1. Tabla y thumbs vacíos.
2. Panel de diferencias: mensaje de que hacen falta al menos dos soluciones.
3. Inspector (si aplica) muestra diagnóstico del solver (FLW-003).
4. El usuario ajusta inventario y regenera.

---

## Flujo alternativo B — 1 candidata

1. Una fila / una miniatura; sin highlights ni diffs útiles.
2. El usuario puede aplicar o exportar esa única solución.
3. No es un error: el pipeline puede deduplicar a una sola.

---

## Flujo alternativo C — Soluciones desactualizadas

1. El usuario edita el proyecto con impacto en layout.
2. Aparece el banner en el Comparador.
3. Aplicar pide confirmación; lo recomendable es recalcular (FLW-003).

---

## Flujo alternativo D — Replay Timeline

1. Con referencia fijada (o default), el usuario reproduce pasos en el Timeline.
2. El panel de diferencias se actualiza paso a paso frente a la referencia
   (SCR-003 / ADR-005).

---

## Información comparada (Studio actual)

Tabla / Inspector:

- Piezas (y omitidas si parcial)
- Huecos (`waste_ratio`)
- Tablero libre
- Largo / ancho totales
- Score
- Estrategia (en resumen de layout)
- Highlights best-of (piezas ↑, waste ↓, score ↑) si ≥ 2

Panel de diferencias: deltas de métricas + cambios de colocación
(solo-ref / solo-cand / movidas).

No hay columnas de «número de cortes», «tiempo de mecanizado» ni selección
multi-solución lado a lado en pestañas.

---

## Eventos relevantes

- `SolutionSelected` al cambiar candidata
- Traza / replay Timeline (fases y colocaciones)
- `SolutionsMarkedOutdated` al editar con impacto
- `WorkspaceUpdated` al **aplicar** (no al solo previsualizar)

---

## Resultado esperado

El usuario entiende ventajas/inconvenientes relativos (cuando hay ≥ 2
candidatas) y aplica o exporta la elegida de forma consciente.

---

## Criterios de aceptación

- Abrir Comparador y navegar candidatas sin recalcular.
- Preview Workspace/Inspector al seleccionar.
- Diffs y highlights solo cuando ≥ 2; mensaje claro con 0/1.
- Fijar referencia sin regenerar.
- Aplicar / exportar usan la candidata seleccionada.
- Banner outdated visible y apply confirmado si aplica.

---

## Pantallas implicadas

- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- SCR-007 — Exportación.
- FLW-003 — Generar.
- FLW-005 — Exportar.
- ADR-005 — Timeline.

---

## Límites conocidos

- Referencia fijada marcada en tabla/miniaturas (`Ref n` / fondo).
- Diff inútil con menos de dos candidatas.
