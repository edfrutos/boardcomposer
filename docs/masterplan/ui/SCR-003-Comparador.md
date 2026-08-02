# SCR-003 — Comparador de Soluciones

**Módulo:** BoardComposer Studio

**Código:** SCR-003  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 24/07/2026

---

## Objetivo

El Comparador muestra las candidatas del último cálculo de layout, permite
ordenarlas/filtrarlas, resaltar las mejores por métrica y revisar diferencias
frente a una solución de referencia antes de aplicar o exportar.

---

## Filosofía

BoardComposer no ofrece una única respuesta «correcta». El Comparador ayuda a
elegir entre alternativas cuando el solver produce más de una candidata. Con
cero o una sola solución, la comparación de diferencias no aplica (es un
resultado válido del pipeline).

---

## Distribución en Studio

Dock inferior (`Comparador de soluciones`), tabificado junto al Timeline.
Visible/ocultable con **Ver → Comparador de soluciones** (**Ctrl+4**).

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ [banner soluciones desactualizadas, si el proyecto cambió tras calcular]     │
├──────────────────────────────────────────────────────────────────────────────┤
│ Ordenar por…  ☐ Solo completas  [Fijar como referencia]                      │
├──────────────────────────────────────────────────────────────────────────────┤
│ Miniaturas SVG (misma escala)  #1  #2  …                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│ Tabla: # │ Piezas │ Huecos │ Tablero libre │ Largo │ Ancho │ Score           │
├──────────────────────────────────────────────────────────────────────────────┤
│ Diferencias vs referencia (texto; métricas + cambios de colocación)          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Componentes

### Controles

- **Ordenar por:** ranking del pipeline, piezas, huecos, tablero libre o score.
- **Solo completas:** oculta soluciones parciales (con piezas omitidas).
- **Fijar como referencia:** usa la candidata seleccionada como base del panel
  de diferencias (se reinicia tras un nuevo cálculo).

### Miniaturas

SVG de cada candidata a la misma escala. Clic selecciona; tooltip si es
«mejor en…» alguna métrica.

### Tabla

Columnas: `#`, Piezas (con sufijo de omitidas si incompleta), Huecos
(`waste_ratio`), Tablero libre, Largo, Ancho, Score.

### Resaltado «mejor en métrica»

Solo con **≥ 2** soluciones. Criterios: más piezas, menos huecos internos,
mayor score, menos tablero libre, menor largo y menor ancho. La fila/thumb
va en negrita y el tooltip lista las métricas.

### Panel de diferencias

Texto de solo lectura. Requiere **≥ 2** soluciones; si no, muestra que se
necesitan al menos dos. Compara la candidata seleccionada con la referencia
(métricas y placements: solo-ref / solo-cand / movidas). También se actualiza
en sync con el replay del Timeline (diff parcial por paso).

---

## Interacciones

| Acción | Atajo / control | Efecto |
|--------|-----------------|--------|
| Seleccionar candidata | clic fila o miniatura | Preview en Workspace + Inspector |
| Solución anterior / siguiente | **Re Pág** / **Av Pág** | Sigue orden/filtro visibles del Comparador |
| Aplicar al proyecto | **Ctrl+Shift+Return** | Confirma si las soluciones están desactualizadas |
| Exportar seleccionada | **Ctrl+Shift+E** | Diálogo SCR-007 |
| Explicar candidata | **Ctrl+Alt+E** | Ayuda → diálogo determinista + Copiar |
| Mostrar/ocultar dock | **Ctrl+4** | Toggle Comparador |

---

## Flujo principal

1. **Calcular layout** (**Ctrl+Return**).
2. Abrir el Comparador (**Ctrl+4**) si no está visible.
3. Ordenar / filtrar; fijar referencia si conviene.
4. Revisar miniaturas, métricas y panel de diferencias.
5. **Aplicar** o **exportar** la elegida.

---

## Criterios de aceptación

- Con 0 o 1 solución, la UI no engaña: no hay diffs ni highlights.
- Con ≥ 2, el usuario identifica mejores por métrica y ve deltas vs referencia.
- Cambiar de candidata no regenera el solver.
- Exportar y aplicar usan la solución seleccionada.
- Miniaturas comparten escala para comparación visual justa.

---

## Relación con otras pantallas

- SCR-002 — Workspace (preview al seleccionar).
- SCR-004 — Inspector (métricas / highlights de la candidata).
- SCR-006 — Preferencias (`max_solutions` y pesos de scoring).
- SCR-007 — Exportación.
- Timeline — replay sincronizado con el panel de diferencias.

---

## Límites conocidos (Studio actual)

_(Ninguno prioritario en highlights / navegación del Comparador.)_

---

## Evolución prevista

- Gráficos históricos y recomendaciones asistidas.
