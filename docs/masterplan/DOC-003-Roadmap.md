# BoardComposer

## Documento 3 — Roadmap del Producto

**Código:** DOC-003  
**Versión:** 1.2.0  
**Estado:** En revisión — actualizado  
**Fecha de creación:** 01/07/2026  
**Última revisión:** 25/07/2026

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

- `AddBoard` / `AddPiece` aún sin Command dedicado (undo vía otros caminos).
- Sin control de versiones / diffs de revisiones del `.bcproj`.
- Pulido UAT humano continuo sobre la checklist.

---

# Fase 3 — Plataforma

**Estado:** ⚪ Planificada — **siguiente bloque de producto**

Incluye:

- API pública y contratos versionados.
- Automatización e integraciones.
- Exportadores / servicios remotos avanzados.

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

- Fase 3: API pública y automatización (alcance a descomponer en EP).
- Cierre de deuda menor Fase 2 (p. ej. Add*Command).

### Prioridad P2

- IA (Fase 4).
- Plugins / ecosistema (Fase 5).
- Cloud.

---

## Criterios para modificar el Roadmap

Toda modificación deberá:

- aportar valor al usuario;
- mantener la coherencia con el Manifiesto;
- respetar la arquitectura definida;
- quedar registrada en el historial de decisiones.

---

## Estado

**Estado actual:** 🟡 Fase 2 con núcleo operativo entregado; documento
alineado con `ROADMAP.md` y DOC-004 (IDE-0001…0018).

Pendiente de:

- descomponer Fase 3 en épicas (EP);
- vincular sprints;
- incorporar estimaciones y dependencias;
- aprobar como hoja de ruta oficial del proyecto.
