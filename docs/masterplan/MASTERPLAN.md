# BoardComposer — MASTERPLAN

Última revisión: 2026-07-16.

## Estado actual

- Fase de producto: **Fase 2 — BoardComposer Studio**.
- Versión de desarrollo: `0.4.0.dev0`.
- Core base consolidado y cubierto por tests.
- Studio dispone de flujo funcional de proyecto, edición, cálculo y exportación.
- Primera vertical multipanel implementada sobre MaxRects.

## Último bloque consolidado

### Packing multipanel

- `StockPanel` con cantidad.
- `PanelReference` por tipo e instancia física.
- MaxRects multipanel con compatibilidad de espesor.
- Validación, completitud, deduplicación y scoring por panel.
- Persistencia Studio versión 2 compatible con versión 1.
- Workspace y SVG con paneles dispuestos lado a lado.
- ADR-014 y documentación técnica actualizada.

## Próxima tarea única

Ejecutar y documentar un UAT visual completo de Studio con:

- dos tipos de tablero;
- varias unidades de un tipo;
- piezas de espesores compatibles e incompatibles;
- generación, comparación, aplicación, guardado, reapertura y exportación SVG.

## Criterio de finalización del próximo bloque

- El flujo se completa sin errores ni pérdida de asignación física.
- Inspector y Workspace identifican correctamente panel e instancia.
- Los defectos encontrados tienen test de regresión cuando sea viable.
- Ruff, Mypy y Pytest limpios.
- Resultado del UAT registrado en documentación.

## Límites conocidos

- Solo MaxRects implementa por ahora el contrato multipanel.
- El movimiento interactivo entre paneles todavía no está habilitado.
- La compatibilidad de material no existe en el Core; se valida espesor.
- La cobertura automatizada de interacción Qt sigue siendo reducida.

## Normas de trabajo

1. No añadir funcionalidad sin bloque definido.
2. No introducir dependencias de interfaz en el Core.
3. No duplicar reglas geométricas o de validación.
4. Mantener coordenadas multipanel locales al panel físico.
5. Trabajar desde interfaces públicas con tests de comportamiento.
6. Actualizar ADR, CHANGELOG y MASTERPLAN al cerrar un hito.
7. Ejecutar Ruff, type checking, Pytest y smoke test de Studio antes del commit.
