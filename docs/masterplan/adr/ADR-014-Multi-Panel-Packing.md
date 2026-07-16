# ADR-014 — Contrato de packing multipanel

## Estado

Aceptada.

## Contexto

El modelo `StockPanel` permite describir material disponible, pero una solución
solo contiene coordenadas sobre un único plano. Para utilizar varias unidades
de uno o más tableros es necesario identificar el panel físico al que pertenece
cada colocación y definir cómo se validan y puntúan esas soluciones.

## Decisión

Cada `BoardPlacement` puede incluir una `PanelReference` formada por:

- `stock_panel_index`: posición del tipo de tablero en `Project.stock_panels`;
- `instance_index`: unidad física dentro de `StockPanel.quantity`.

Las coordenadas de una colocación son locales al panel físico referenciado.
Dos piezas con las mismas coordenadas no colisionan si pertenecen a paneles
físicos distintos.

## Inventario

`StockPanel.quantity` se expande en instancias físicas numeradas desde cero.
Una referencia es válida únicamente si ambos índices existen en el proyecto.
Los identificadores de usuario de `StockPanel` siguen siendo opcionales y no se
utilizan como clave interna, evitando ambigüedades por identificadores repetidos
o ausentes.

## Compatibilidad de material

Una pieza solo puede colocarse en un panel con el mismo espesor. El material se
considerará en una evolución posterior cuando el Core disponga de ese atributo.

## Validación

En proyectos con inventario de paneles:

- toda colocación debe tener una referencia válida;
- cada pieza debe quedar dentro de las dimensiones de su panel;
- el espesor de pieza y panel debe coincidir;
- los solapes se comprueban de forma independiente por panel físico;
- los límites globales de `ProjectConstraints` dejan de definir el área física;
- una solución parcial se distingue de una completa mediante el resultado de
  validación, aunque ambas puedan conservarse como candidatas internas.

En proyectos sin inventario se mantiene el comportamiento histórico basado en
`ProjectConstraints` y colocaciones sin referencia de panel.

## Desperdicio

El desperdicio multipanel se calcula sobre los paneles físicos utilizados. Un
panel de inventario sin colocaciones no se considera consumido ni desperdiciado.
La solución expone área usada y desperdicio tanto por panel como de forma total.

## Algoritmo inicial

MaxRects será el primer generador compatible. Evaluará los tipos e instancias
en el orden declarado por el proyecto y conservará las piezas que no quepan para
el siguiente panel compatible. Las estrategias históricas siguen disponibles
para proyectos sin inventario.

## Studio y persistencia

Studio conservará espesor y cantidad de cada tablero, y cada colocación podrá
guardar el identificador de tablero y su instancia. El puente Studio → Core
mantendrá el orden de tableros para resolver `PanelReference` de forma estable.
Los proyectos versión 1 se seguirán cargando con valores por defecto.

## Consecuencias

- Las soluciones antiguas siguen siendo válidas sin `StockPanel`.
- El packing multipanel puede crecer sin trasladar tableros a un plano global.
- Exportadores y vistas que representen varios paneles deberán resolver las
  referencias contra el proyecto.
