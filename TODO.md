# TODO — BoardComposer

Backlog operativo de corto plazo. El registro de producto se mantiene en
`docs/masterplan/DOC-004-Backlog.md`.

## Inmediato

- [x] Ejecutar UAT visual con varios tipos, cantidades y espesores.
- [x] Permitir mover una pieza entre paneles físicos desde el Workspace.
- [x] Mostrar identificador e instancia de panel en el Inspector de pieza.
- [x] Añadir pruebas automatizadas de interacción Qt para el Workspace.

## Datos y flujo de trabajo

- [x] Importar inventario de tableros y cantidades desde CSV.
- [x] Incorporar material al modelo Core y validar compatibilidad material/espesor.
- [x] Definir migraciones explícitas para futuras versiones de `.bcproj`.

## Solver

- [x] Comparar órdenes de panel además de órdenes de piezas.
- [x] Evaluar reutilización de retales como inventario futuro (decisión: informativo por ahora, ADR-016).
- [x] Añadir benchmarks multipanel reproducibles.
- [ ] Explorar CP-SAT tras estabilizar el contrato multipanel.

## Studio

- [ ] Completar el comparador visual definido en SCR-003 (resaltado por métrica añadido; queda ordenar/filtrar por criterio).
- [ ] Exportación PDF/DXF.
- [ ] Preferencias de estrategia y pesos de scoring.
- [ ] Importación de piezas (no solo tableros) desde CSV; soporte Excel (.xlsx).

## Documentación

- [x] Registrar resultados del UAT multipanel.
- [ ] Revisar flujos y pantallas de `docs/masterplan/ui/` contra Studio real.
- [x] Mantener CHANGELOG, MASTERPLAN y deuda técnica al cerrar cada bloque.
