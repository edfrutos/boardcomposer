# ADR-017 — CP-SAT como generador exacto de un solo panel

## Estado

Aceptada (exploratoria).

## Contexto

Tras estabilizar el contrato multipanel (ADR-014 a ADR-016), el backlog
planteaba "Explorar CP-SAT". Las heurísticas (MaxRects, Skyline, …) son
rápidas y producen buenas soluciones, pero no garantizan optimalidad. OR-Tools
CP-SAT permite modelar el packing 2D como un programa de restricciones y
buscar soluciones exactas (o factibles acotadas por tiempo).

Extenderlo a multipanel (selección de bin + packing) dispara la complejidad
combinatoria y todavía no hay un caso de uso de Studio que lo demande.

## Decisión

1. **Alcance:** un solo panel físico. Las dimensiones salen de
   `ProjectConstraints.max_length_mm` / `max_width_mm` (mismo contrato que
   los generadores clásicos de un panel). En proyectos con inventario
   multipanel (`stock_panel_instances() > 1`) el pipeline sigue forzando
   solo MaxRects; CP-SAT no participa ahí.
2. **Dependencia opcional:** `ortools` se instala con
   `pip install 'boardcomposer[cp_sat]'`. Importar `cp_sat_runner` no falla
   sin él; solo `generate_cp_sat_solution` lanza `CpSatUnavailableError`.
   El generador registrado (`cp_sat`) captura ese error y devuelve `[]`,
   de modo que el pipeline no se rompe si falta el paquete.
3. **Estrategia opt-in:** `exact_strategy()` incluye `("maxrects", "cp_sat")`.
   Las estrategias por defecto de Studio (`material`, `balanced`, `compact`)
   **no** invocan CP-SAT, para no alargar el cálculo ni exigir `ortools`.
4. **Objetivo:** maximizar el número de piezas colocadas, con
   `omitted_piece_ids` para las que no caben (mismo contrato de solución
   parcial que el resto del pipeline). Límite de tiempo por defecto: 5 s.
5. **Coordenadas:** enteras (mm redondeados). Suficiente para el dominio
   actual; se revisará si aparece un caso con fracciones.

## Consecuencias

- Se puede pedir una solución exacta sin tocar Studio: basta
  `GeometrySolver(strategy=exact_strategy())` o
  `strategy_by_name("exact")`.
- Sin `ortools`, la estrategia `exact` degrada a MaxRects (CP-SAT no aporta
  candidatas).
- Multipanel exacto queda explícitamente fuera de esta ADR; si se necesita,
  se abrirá una ADR nueva.

## Alternativas descartadas

- Incluir CP-SAT en `material_first` por defecto: coste de tiempo y
  dependencia no deseados en el flujo diario de Studio.
- Modelar multipanel desde el primer día: demasiado alcance para una
  exploración.
