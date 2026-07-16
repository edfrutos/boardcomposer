
# DECISIONS - BoardComposer

## 2026-06-26 - Ensamblaje 2D

Se decide comenzar con ensamblaje plano 2D de tablas rectangulares.

Motivo: reduce la complejidad y permite validar el motor antes de añadir interfaz gráfica o algoritmos avanzados.

## 2026-06-26 - Núcleo independiente

El núcleo no dependerá de PySide6, ficherosos ni IA.

Motivo: debe poder probarse desde consola y con tests unitarios.

## 2026-06-26 - Soluciones explicables

Cada solución deberá incluir puntuación y explicación.

Motivo: el usuario debe entender por qué una composición es mejor que otra.

## 2026-07-16 - Packing multipanel con coordenadas locales

Cada colocación puede referenciar una instancia física de `StockPanel`. Las
coordenadas son locales a ese panel y `quantity` representa unidades físicas
disponibles.

Motivo: evita trasladar artificialmente los paneles a un plano global y permite
validar límites, espesor, solapes y desperdicio por cada tablero consumido.

Documento: `docs/masterplan/adr/ADR-014-Multi-Panel-Packing.md`.
