# Algoritmos y pipeline

Última revisión: 2026-07-16.

## Familias disponibles

- Horizontal y vertical: composiciones deterministas y permutaciones simples.
- Free-space: colocación sobre regiones libres.
- Skyline: perfil de alturas, rotación y múltiples ordenaciones.
- MaxRects: rectángulos libres, varias heurísticas y ordenaciones.
- Beam Search MaxRects: exploración limitada de estados prometedores.
- MaxRects adaptativo: selección de heurística según el estado.

## Pipeline común

Los generadores no deciden por sí solos qué solución es definitiva. Entregan
candidatas a `CandidatePipeline`, que deduplica, valida, evalúa y ordena.

Una sola instancia de stock mantiene las familias de la estrategia y recibe una
asignación de panel compatible. Con varias instancias, el pipeline usa MaxRects,
primer generador que implementa el contrato multipanel completo.

Las estadísticas registran candidatas generadas, únicas, aceptadas, rechazadas
y motivos estructurados de rechazo.

## MaxRects multipanel

Para cada combinación de heurística y orden de piezas:

1. Expande `StockPanel.quantity` en paneles físicos.
2. Recorre los paneles en el orden declarado por el proyecto.
3. Intenta colocar las piezas de espesor compatible.
4. Conserva las que no caben para el siguiente panel.
5. Asigna `PanelReference` a cada colocación.
6. Prefiere más piezas, menos paneles, menos desperdicio y menos rotaciones.

Una candidata puede ser parcial cuando el inventario es insuficiente; el
pipeline solo acepta soluciones completas y válidas como resultado final.

## Evolución prevista

- Comparar órdenes de panel y políticas best-fit entre tipos.
- Benchmarks multipanel reproducibles.
- Incorporar material y retales al inventario.
- Añadir CP-SAT cuando el contrato de dominio esté estabilizado.
