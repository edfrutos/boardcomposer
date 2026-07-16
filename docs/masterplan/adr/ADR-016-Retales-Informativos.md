# ADR-016 — Retales como información, no como inventario

## Estado

Aceptada.

## Contexto

`multi_panel_maxrects` genera, para cada panel físico consumido, una lista de
`FreeRectangle` que quedan sin ocupar tras colocar todas las piezas que
pudieron encajar en él. El punto abierto del TODO ("Evaluar reutilización de
retales como inventario futuro") planteaba dos caminos:

1. **Inventario reutilizable**: persistir los retales como `StockPanel`
   nuevos, disponibles para futuros proyectos (o incluso para el propio
   proyecto, en una segunda pasada del solver).
2. **Informativo únicamente**: reportar los retales aprovechables de la
   solución actual, sin intentar reutilizarlos como inventario todavía.

La opción 1 implica decisiones adicionales no triviales: ¿cómo se identifica
un retal ya usado parcialmente en otro proyecto?, ¿qué pasa si dos proyectos
compiten por el mismo retal?, ¿cómo se persiste su ciclo de vida (creado,
reservado, consumido, descartado) fuera del propio `.bcproj`? Ninguna de
estas preguntas tenía aún un caso de uso validado por UAT.

## Decisión

Se adopta la opción informativa. `AssemblySolution` expone:

- `offcuts: tuple[Offcut, ...]`: la lista de rectángulos aprovechables por
  panel físico consumido, con posición y dimensiones locales a ese panel
  (mismo sistema de referencia que `PanelReference`, ADR-014).
- `total_offcut_area_mm2`: suma de área de todos los retales, para comparar
  soluciones de un vistazo.

`multi_panel_maxrects` filtra los rectángulos libres finales de cada panel
consumido con un umbral mínimo (`_MIN_OFFCUT_SIDE_MM = 50` mm de lado): por
debajo de ese tamaño un recorte no es realista como material reutilizable y
se descarta para no inflar el listado con ruido. Solo se reportan retales de
paneles que la solución consumió (con al menos una pieza colocada); un panel
de inventario sin usar no genera retales.

Los retales se muestran en:

- el Inspector de Studio (recuento y área total de la solución seleccionada);
- el exportador SVG (rectángulos punteados en verde, con su área);
- los presenters de texto y JSON (detalle por panel).

## Fuera de alcance (por ahora)

No se persisten los retales como `StockPanel` ni se ofrecen para su reserva
o consumo por otros proyectos. Si en el futuro se valida una necesidad real
de inventario de recortes, esta ADR debería revisarse o sustituirse por una
que defina el ciclo de vida completo (persistencia, concurrencia entre
proyectos, expiración).

## Consecuencias

- La funcionalidad es aditiva: no cambia cómo se calculan ni se puntúan las
  soluciones, solo qué información adicional exponen.
- Es reversible: si se decide construir inventario reutilizable más
  adelante, `Offcut` ya captura la geometría necesaria como punto de partida.
- El umbral mínimo de 50 mm es una heurística inicial; puede convertirse en
  preferencia de usuario si el UAT lo demanda.
