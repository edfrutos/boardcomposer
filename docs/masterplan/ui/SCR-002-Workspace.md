# BoardComposer Studio

## SCR-002 — Workspace

**Código:** SCR-002  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 24/07/2026

---

## Objetivo

El Workspace es el núcleo operativo de BoardComposer Studio. Desde esta pantalla
el usuario visualiza los paneles físicos, genera y aplica soluciones, mueve
piezas (incluido entre paneles) e inspecciona cada colocación sin abandonar el
contexto de trabajo.

---

## Filosofía

El Workspace no es un simple visor de planos. Es un entorno interactivo donde el
usuario explora alternativas, corrige a mano lo que el solver propuso y toma la
decisión final antes de exportar.

---

## Distribución conceptual

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Menú / toolbar: Archivo · Proyecto · Editar · Ver · Generar · Comparar · …  │
├──────────────┬───────────────────────────────────────────────┬───────────────┤
│ Explorador   │                                               │ Inspector     │
│ Tableros     │           Workspace gráfico                   │ Propiedades   │
│ Piezas       │     (paneles físicos lado a lado)             │ Panel/inst.   │
│ Soluciones   │                                               │               │
├──────────────┴───────────────────────────────────────────────┴───────────────┤
│ Timeline                          │ Comparador de soluciones                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Componentes principales

### Workspace gráfico

- Representa **paneles físicos** lado a lado (cada unidad de inventario con
  `quantity > 1` aparece como instancia distinta).
- Piezas colocadas con id, rotación y panel de origen.
- Zoom (rueda, **Ctrl+=** / **Ctrl+-**), ajuste (**Ctrl+0**, **Ctrl+Shift+0**),
  pan (botón medio / derecho / Espacio+arrastre) y cuadrícula (**Ctrl+G**).

### Explorador

Árbol con tableros, piezas y soluciones; selección sincronizada con el canvas.

### Inspector

Contexto del elemento seleccionado: dims, posición, material, espesor,
identificador de panel físico e instancia.

### Timeline / Comparador

Historial de eventos y tabla de candidatas (si hay más de una tras calcular).

---

## Interacción: mover y reasignar piezas

No hay botón «intercambiar piezas». La reasignación es **arrastrar y soltar**:

1. Selecciona una pieza en el canvas (o en el Explorador).
2. Arrástrala dentro de su panel para reposicionarla, **o** suéltala sobre
   **otro panel físico** visible en el Workspace.
3. Si la pieza cabe sin solape y el **material/espesor** son compatibles con el
   panel destino, la colocación se actualiza y se registra en el historial
   (undo/redo con **Ctrl+Z** / **Ctrl+Shift+Z**).
4. Si el destino es inválido (solape, fuera de límites, material/espesor
   incompatible), el movimiento **revierte** a la posición anterior.

Notas:

- Piezas de materiales distintos (p. ej. MDF vs Tablex) no se pueden soltar
  en paneles incompatibles.
- Tras **Aplicar layout**, el canvas refleja la solución aplicada; el arrastre
  edita las colocaciones del proyecto (no inventa una segunda solución del
  solver por sí solo).

---

## Flujo principal

1. Abrir o crear un proyecto.
2. Añadir / importar tableros y piezas.
3. **Calcular layout** (**Ctrl+Return**).
4. Si hay varias candidatas, recorrerlas (**Re Pág** / **Av Pág**) y comparar.
5. **Aplicar** la elegida (**Ctrl+Shift+Return**).
6. Ajustar a mano en el Workspace (arrastre / rotación **R** / flechas).
7. Exportar (**Ctrl+Shift+E**).

Una sola candidata tras calcular es un resultado válido del pipeline
(deduplicación / inventario restringido).

---

## Principios de interacción

- Selección directa sobre el canvas.
- Actualización inmediata del Inspector.
- Feedback inmediato: movimiento inválido no se confirma.
- Atajos de teclado documentados en tip de estado y Ayuda → Atajos (**F1**).

---

## Criterios de aceptación

- El usuario ve todos los paneles físicos usados en la solución.
- Arrastrar una pieza a otro panel compatible reasigna instancia y posición.
- Un drop inválido no deja el proyecto en estado inconsistente.
- Undo restaura panel e instancia previos.
- Zoom, pan y selección no bloquean el flujo de cálculo/exportación.

---

## Relación con otras pantallas

- SCR-001 — Inicio.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- SCR-005 — Proyecto.
- SCR-006 — Preferencias.
- SCR-007 — Exportación.

---

## Evolución prevista

- Animación paso a paso del packing (parcial vía Timeline).
- Edición manual asistida (sugerencias de hueco).
- Vista múltiple / comparación lado a lado de dos soluciones en el canvas.
- Colaboración e integración con asistentes de IA.
