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

Para cada combinación de heurística, orden de piezas **y orden de panel**
(`panel_ordering.py`: orden original, mayor área primero, menor área
primero):

1. Expande `StockPanel.quantity` en paneles físicos.
2. Recorre los paneles en el orden de la combinación actual.
3. Intenta colocar las piezas de espesor **y material** compatibles con el
   panel (`material_key` normalizado en ambos lados).
4. Conserva las que no caben para el siguiente panel.
5. Asigna `PanelReference` a cada colocación.
6. Registra los rectángulos libres restantes de cada panel consumido como
   `Offcut`, descartando los menores al umbral mínimo (`_MIN_OFFCUT_SIDE_MM`,
   ver ADR-016).
7. Prefiere más piezas, menos paneles, menos desperdicio y menos rotaciones.

Una candidata puede ser parcial cuando el inventario es insuficiente o hay
incompatibilidad de material/espesor: el pipeline acepta soluciones
parciales como resultado final (piezas no colocadas se listan en
`omitted_piece_ids`), reservando el rechazo total para motivos "duros"
(solapes, límites excedidos).

## Evolución prevista

- Extender el comparador de Studio (SCR-003) con ordenación/filtrado por
  métrica, además del resaltado ya disponible.
- Evaluar si los retales informativos (ADR-016) deben pasar a ser inventario
  reutilizable entre proyectos.
- Valorar CP-SAT multipanel si aparece un caso de uso real (hoy solo un
  panel, ADR-017).

## CP-SAT (un panel)

Generador exacto opcional (`pip install 'boardcomposer[cp_sat]'`), registrado
como `"cp_sat"` y activado con la estrategia `exact` (`maxrects` + `cp_sat`).
Sin `ortools` el generador no aporta candidatas y el pipeline sigue con las
heurísticas. Ver ADR-017.
