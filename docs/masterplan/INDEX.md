# Índice documental de BoardComposer

Última revisión: 2026-08-09.

## Precedencia

Cuando dos documentos discrepen, usar este orden:

1. Código y tests vigentes.
2. ADR aceptados.
3. `MASTERPLAN.md`.
4. Documentos DOC aprobados o en revisión.
5. Resúmenes operativos de la raíz.

Las discrepancias deben corregirse, no mantenerse como conocimiento implícito.

## Mapa docs (proyecto vs usuario)

Índice legible: [`../README.md`](../README.md).

- **Usuario final:** [`../user/GUIA-RAPIDA.md`](../user/GUIA-RAPIDA.md)
- **UAT visual:** [`../../uat/studio/CHECKLIST-VISUAL.md`](../../uat/studio/CHECKLIST-VISUAL.md)
- **Release/demo smoke:** [`../../uat/RELEASE-SMOKE.md`](../../uat/RELEASE-SMOKE.md)

## Dirección del proyecto

| Documento | Contenido | Estado |
|---|---|---|
| `DOC-000-Manifiesto.md` | Principios fundacionales | Aprobado |
| `DOC-001-Producto.md` | Problema, propuesta y usuarios | En revisión |
| `DOC-002-Arquitectura.md` | Arquitectura objetivo | En revisión |
| `DOC-003-Roadmap.md` | Fases del producto | Actualizado |
| `DOC-004-Backlog.md` | Iniciativas priorizadas | Actualizado |
| `REVIEW-2026-08-09-planificacion.md` | Snapshot estado / siguientes pasos | Actualizado |
| `REVIEW-2026-08-08-planificacion.md` | Snapshot previo (histórico) | Histórico |
| `REVIEW-2026-08-07-planificacion.md` | Snapshot previo (histórico) | Histórico |
| `REVIEW-2026-08-06-planificacion.md` | Snapshot previo (histórico) | Histórico |
| `REVIEW-2026-08-05-planificacion.md` | Snapshot previo (histórico) | Histórico |
| `epics/` | Épicas Fase 3 (EP-001…003) | Entregadas |
| `DOC-005-Decisiones.md` | Índice de decisiones | En revisión |
| `DOC-006-DeudaTecnica.md` | Registro de deuda | Actualizado |
| `DOC-007-UX-Studio.md` | Principios UX | En revisión |
| `DOC-008-API.md` | API y extensibilidad futura | En revisión |
| `DOC-009-API-v1-Formatos.md` | Formatos intercambio API `v1` | En revisión |
| `DOC-010-HTTP-Amenazas.md` | Amenazas/mitigaciones HTTP + Docker | Referencia |

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
`ui/REVIEW-2026-07-17.md`. Pasada visual fresca: `uat/studio/CHECKLIST-VISUAL.md`.

## Documentación técnica viva

- `../README.md` — mapa docs (usuario vs proyecto)
- `../user/GUIA-RAPIDA.md` — guía usuario Studio
- `spikes/` — spikes de deuda / alcance (DT-0006, IDE-0007)
- `../ops/PILOT-DT-0006-backup.md` — piloto backup revisiones (opción D)
- `../architecture.md`
- `../data_model.md`
- `../algorithms.md`
- `../scoring.md`
- `../../README.md`
- `../../CHANGELOG.md`
- `../../ROADMAP.md` — resumen operativo (alineado con DOC-003)
- `../../uat/README.md` — índice UAT
