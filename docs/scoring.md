# Scoring y ranking

Última revisión: 2026-07-16.

## Objetivos

El score combina pesos configurables para:

- aprovechamiento de material;
- proporción de piezas colocadas;
- compacidad;
- penalización de rotaciones.

Las estrategias `balanced`, `material` y `compact` seleccionan pesos y familias
de generadores. El score no sustituye la validación: una candidata inválida se
rechaza antes de puntuarla.

## Aprovechamiento

- Plano legacy: área de piezas / bounding area.
- Multipanel: área de piezas / área total de paneles físicos consumidos.

Los paneles de inventario no utilizados no cuentan como consumo ni desperdicio.

## Ranking estable

Las soluciones priorizan, en este orden general:

1. mayor número de piezas colocadas;
2. mayor score ponderado;
3. menor desperdicio interno;
4. menor bounding area;
5. menos rotaciones;
6. mayor compacidad.

Durante la generación multipanel, MaxRects añade preferencia por menos paneles
consumidos y menor desperdicio total de esos paneles.
