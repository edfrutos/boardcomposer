# BoardComposer

## Documento 3 — Roadmap del Producto

**Código:** DOC-003  
**Versión:** 1.3.3  
**Estado:** En revisión — actualizado  
**Fecha de creación:** 01/07/2026  
**Última revisión:** 08/08/2026

Resumen operativo paralelo: `ROADMAP.md` en la raíz del repo.

---

## Objetivo

Definir la evolución prevista de BoardComposer mediante fases, hitos y
prioridades, proporcionando una visión clara del desarrollo del producto a
corto, medio y largo plazo.

---

## Principios

El Roadmap representa la dirección del proyecto, no una planificación
cerrada. Podrá evolucionar conforme aparezcan nuevas necesidades, siempre
respetando el Manifiesto y la Arquitectura.

---

# Fase 0 — Fundamentos (Completada)

**Estado:** 🟢

- Repositorio, packaging y CI.
- Documentación fundacional y ADR.
- Estructura modular Core/Studio.

---

# Fase 1 — Core (Base completada)

**Estado:** 🟢

Objetivos alcanzados:

- Motor de optimización desacoplado.
- Algoritmos Skyline y MaxRects (y generadores asociados).
- Beam Search y heurísticas adaptativas.
- Sistema de evaluación, ranking y diagnósticos.
- Exportadores CLI básicos (CSV, texto, JSON, SVG).
- Cobertura amplia mediante pruebas automatizadas.
- Inventario `StockPanel` y packing multipanel MaxRects.
- Compatibilidad material/espesor; retales informativos (ADR-016).
- Generador CP-SAT de un panel explorado.
- Migraciones explícitas `.bcproj` (ADR-015).

La base del Core está completada, pero continúa recibiendo extensiones
controladas que preservan sus contratos públicos.

---

# Fase 2 — BoardComposer Studio (Núcleo operativo)

**Estado:** 🟡 En curso (núcleo usable; evolución continua)

Objetivo:

Construir la aplicación visual profesional para explorar, comparar y
comprender soluciones de corte.

Entregables principales (alcanzados):

- Workspace, cámara, paneles lado a lado y DnD entre paneles físicos.
- Selección, Inspector y comandos undo/redo (ops con Command).
- Gestión y persistencia de proyectos (`.bcproj` v2), recientes, plantillas.
- Pantalla de inicio / bienvenida (SCR-001).
- Comparador visual SCR-003 (resaltado, ordenar/filtrar, miniaturas, diff).
- Cálculo de layout con progreso cancelable (FLW-003) y outdated (FLW-006).
- Importación tableros/piezas CSV y Excel (FLW-002).
- Exportación SVG/DXF/PDF/JSON/CSV con diálogo, preview y plantillas
  (SCR-007 / FLW-005).
- Preferencias: tema, idioma, unidades, grid, estrategia/pesos, export
  (SCR-006).
- Timeline de eventos (ADR-005) + export historial.
- UAT visual multipanel ejecutado; checklist humana en
  `uat/studio/CHECKLIST-FUNCIONAL.md`.
- Docs UI SCR-001…007 y FLW-001…006 alineados
  (`docs/masterplan/ui/REVIEW-2026-07-17.md`).

Deuda / evolución dentro de Fase 2 (no bloquea uso diario):

- Diff `.bcproj` + anillo local de revisiones al guardar: entregado
  (`bcproj_diff` / `bcproj_revisions`); historial cloud / multi-usuario = deuda.
- Pulido UAT humano continuo (`uat/studio/CHECKLIST-VISUAL.md` cerrado
  2026-07-28).

---

# Fase 3 — Plataforma

**Estado:** 🟢 Entregada (EP-001…003)  
**Última descomposición:** 26/07/2026 → `docs/masterplan/epics/`

| Épica | Título | Prioridad | Dependencias |
|-------|--------|-----------|--------------|
| [EP-001](epics/EP-001-API-Publica-Contratos.md) | API pública y contratos `v1` (SPR-001…003 🟢) | P1 | Core / DOC-008 / DOC-009 |
| [EP-002](epics/EP-002-Automatizacion-Batch.md) | Automatización y batch (SPR-001…003 🟢) | P1 | EP-001 |
| [EP-003](epics/EP-003-Integraciones-Remotas.md) | Integraciones / remoto (SPR-001…003 🟢) | P2 | EP-001, EP-002 |

Orden de ataque: EP-001 → EP-002 → EP-003. Índice: [epics/README.md](epics/README.md).

---

# Fase 4 — Inteligencia

**Estado:** ⚪ Idea consolidada

Objetivos:

- Asistencia mediante IA.
- Explicaciones inteligentes.
- Recomendación automática de estrategias.
- Análisis avanzado de soluciones.

---

# Fase 5 — Ecosistema

**Estado:** ⚪ Visión futura

Objetivos:

- Plugins.
- Marketplace.
- Biblioteca de materiales.
- Comunidad.

---

## Prioridades actuales

### Prioridad P0 — Completada

- UAT visual multipanel y flujo Studio núcleo.
- Movimiento / reasignación entre paneles.
- Compatibilidad material + multipanel MaxRects.

### Prioridad P1 — Completada (Studio 2026-07)

- Importación CSV/Excel tableros y piezas.
- Comparador visual completo (SCR-003).
- Preferencias SCR-006.
- Export multi-formato SCR-007.
- Docs UI sync SCR/FLW.
- Cobertura Qt de interacción Workspace.

### Prioridad P1 — Siguiente (producto)

- Eval humana IDE-0007 MVP (`uat/studio/CHECKLIST-EXPLAIN-EVAL.md`).
- Piloto DT-0006 opción D (backup); C diferida.
- Pulido / QoL Fase 2 bajo demanda (ciclo `0.4.3.dev0`).
- Candidatos producto IDE-0019…0024 (ver revisión 2026-08-08) cuando haya
  capacidad tras eval.

### Prioridad P2

- IA LLM opt-in (Fase 4; tras política / eval).
- Plugins / ecosistema (Fase 5).
- Cloud multi-usuario (DT-0006 C).

---

## Criterios para modificar el Roadmap

Toda modificación deberá:

- aportar valor al usuario;
- mantener la coherencia con el Manifiesto;
- respetar la arquitectura definida;
- quedar registrada en el historial de decisiones.

---

## Estado

**Estado actual:** 🟢 Fase 3 (EP-001…003) entregada; Studio núcleo usable;
ciclo `0.4.3.dev0` (QoL Welcome/Recientes/status bar/Timeline + candidatos
IDE-0019…0024). Revisión: `REVIEW-2026-08-08-planificacion.md`.

Pendiente de:

- Eval IDE-0007 + piloto DT-0006 D;
- slices QoL / IDE-0019…0024 bajo demanda;
- aprobar como hoja de ruta oficial del proyecto.
