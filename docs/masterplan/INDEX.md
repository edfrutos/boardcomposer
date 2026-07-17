# Índice documental de BoardComposer

Última revisión: 2026-07-16.

## Precedencia

Cuando dos documentos discrepen, usar este orden:

1. Código y tests vigentes.
2. ADR aceptados.
3. `MASTERPLAN.md`.
4. Documentos DOC aprobados o en revisión.
5. Resúmenes operativos de la raíz.

Las discrepancias deben corregirse, no mantenerse como conocimiento implícito.

## Dirección del proyecto

| Documento | Contenido | Estado |
|---|---|---|
| `DOC-000-Manifiesto.md` | Principios fundacionales | Aprobado |
| `DOC-001-Producto.md` | Problema, propuesta y usuarios | En revisión |
| `DOC-002-Arquitectura.md` | Arquitectura objetivo | En revisión |
| `DOC-003-Roadmap.md` | Fases del producto | Actualizado |
| `DOC-004-Backlog.md` | Iniciativas priorizadas | Actualizado |
| `DOC-005-Decisiones.md` | Índice de decisiones | En revisión |
| `DOC-006-DeudaTecnica.md` | Registro de deuda | Actualizado |
| `DOC-007-UX-Studio.md` | Principios UX | En revisión |
| `DOC-008-API.md` | API y extensibilidad futura | En revisión |

`DOC-001-Manifiesto.md` se conserva como documento histórico duplicado; la
referencia oficial del manifiesto es `DOC-000-Manifiesto.md`.

## ADR

- ADR-001 — Core como fuente de verdad.
- ADR-002 — Soluciones inmutables.
- ADR-003 — Event Bus.
- ADR-004 — Plugins.
- ADR-005 — Timeline.
- ADR-006 — Identidad permanente.
- ADR-007 — UI contextual.
- ADR-008 — Command Pattern.
- ADR-009 — Estabilidad visual.
- ADR-010 — PlacementValidator.
- ADR-011 — Blueprint del Workspace.
- ADR-012 — SelectionController.
- ADR-013 — Geometry Engine.
- ADR-014 — Packing multipanel.
- ADR-015 — Migraciones explícitas de `.bcproj`.
- ADR-016 — Retales informativos (no inventario).
- ADR-017 — CP-SAT como generador exacto de un solo panel.

## UX

`ui/flows/` contiene los flujos FLW-001 a FLW-006. `ui/SCR-*.md` contiene las
especificaciones de Inicio, Workspace, Comparador, Inspector, Proyecto,
Preferencias y Exportación. El UAT multipanel del 2026-07-16 contrastó el
Workspace real; la revisión del 2026-07-17 está en
`ui/REVIEW-2026-07-17.md`.

## Documentación técnica viva

- `../architecture.md`
- `../data_model.md`
- `../algorithms.md`
- `../scoring.md`
- `../../README.md`
- `../../CHANGELOG.md`
