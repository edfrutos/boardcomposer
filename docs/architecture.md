# Arquitectura actual

Última revisión: 2026-07-16.

## Regla principal

`src/boardcomposer` es el Core y no depende de Studio ni de una tecnología de
presentación. CLI, Studio y futuras API consumen sus interfaces públicas.

## Capas

```text
CLI                 Studio                 futura API
 │                    │                        │
 └────────────────────┴────────────────────────┘
                      ▼
              BoardComposer Core
     ┌──────────┬──────────┬───────────┬───────────┐
     │ Domain   │ Geometry │ Solver    │ I/O       │
     │          │ Layout   │ Pipeline  │ Exporters │
     └──────────┴──────────┴───────────┴───────────┘
```

## Core

- `domain`: entidades inmutables y contratos de proyecto/solución.
- `geometry` y `layout`: rectángulos, colisiones, límites y espacios libres.
- `solver`: generadores, búsqueda, validación, evaluación, ranking y métricas.
- `io`: adaptadores de entrada como CSV.
- `presenters` y `export`: salida texto, JSON y SVG.

El punto de entrada principal es `GeometrySolver`, que delega en
`CandidatePipeline`.

## Pipeline

1. Selecciona generadores según estrategia y capacidades del proyecto.
2. Genera candidatas.
3. Deduplica geometría y asignación física.
4. Valida integridad, límites, solapes e inventario.
5. Evalúa y puntúa.
6. Ordena soluciones y publica estadísticas.

Con una única instancia física, el pipeline conserva las familias de la
estrategia y asigna la referencia de panel a sus resultados. Con más de una
instancia física, MaxRects es el generador habilitado hasta que otros algoritmos
implementen el contrato multipanel.

## Studio

Studio usa servicios compartidos para proyectos, comandos, selección, eventos y
layout. `LayoutService` es el adaptador entre modelos de Studio y Core.

El Workspace separa cámara, selección, drag, validación, factories y disposición
de paneles. Los paneles físicos se muestran en coordenadas de escena, mientras
las colocaciones persistidas mantienen coordenadas locales al panel.

## Decisiones relacionadas

- ADR-001: Core como fuente de verdad.
- ADR-008: Command Pattern.
- ADR-010: PlacementValidator.
- ADR-011: Blueprint del Workspace.
- ADR-013: Geometry Engine.
- ADR-014: packing multipanel.
