
# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.2.0  
**Estado:** En revisión — actualizado  
**Fecha de creación:** 01/07/2026  
**Última revisión:** 26/07/2026

---

## Objetivo

Mantener un registro único, priorizado y trazable de todas las funcionalidades, mejoras, ideas e iniciativas previstas para BoardComposer.

El Backlog constituye la fuente oficial de trabajo del proyecto y evoluciona de forma continua.

---

## Principios

- Ninguna idea se pierde.
- Ninguna funcionalidad se implementa sin pasar previamente por el Backlog.
- Toda entrada debe tener un identificador único.
- La prioridad puede cambiar; la trazabilidad nunca.

---

## Estados

- ⚪ Idea
- 🔵 Planificada
- 🟡 En desarrollo
- 🟢 Completada
- 🔴 Bloqueada
- ⚫ Descartada

---

## Prioridades

- **P0** — Crítica
- **P1** — Alta
- **P2** — Media
- **P3** — Baja

---

## Formato de una entrada

```text
ID: IDE-0001
Título:
Estado:
Prioridad:
Impacto:
Esfuerzo:
Dependencias:
Documentos relacionados:
Descripción:
Criterios de aceptación:
Observaciones:
```

---

## Backlog inicial

| ID | Título | Estado | Prioridad |
|----|--------|--------|-----------|
| IDE-0001 | Workspace interactivo | 🟢 | P0 |
| IDE-0002 | Comparador de algoritmos | 🟢 | P0 |
| IDE-0003 | Inspector de piezas | 🟢 | P0 |
| IDE-0004 | Gestión de proyectos | 🟢 | P1 |
| IDE-0005 | Exportación PDF/SVG | 🟢 | P1 |
| IDE-0006 | API pública | 🟢 | P1 |
| IDE-0007 | Asistente IA | ⚪ | P2 |
| IDE-0008 | Sistema de plugins | ⚪ | P3 |
| IDE-0009 | Packing multipanel MaxRects | 🟢 | P0 |
| IDE-0010 | Tests de interacción Qt | 🟢 | P1 |
| IDE-0011 | Movimiento de piezas entre paneles | 🟢 | P0 |
| IDE-0012 | Importación de inventario multipanel | 🟢 | P1 |
| IDE-0013 | Migraciones explícitas `.bcproj` | 🟢 | P1 |
| IDE-0014 | Retales informativos por panel | 🟢 | P1 |
| IDE-0015 | Compatibilidad material pieza/panel | 🟢 | P0 |
| IDE-0016 | Generador CP-SAT (un panel) | 🟢 | P1 |
| IDE-0017 | Importación de piezas desde CSV/Excel | 🟢 | P1 |
| IDE-0018 | Icono/logo propio de BoardComposer Studio | 🟢 | P1 |

---

## Épicas (Fase 3)

| ID | Título | Estado | Prioridad | Ideas |
|----|--------|--------|-----------|-------|
| EP-001 | API pública y contratos | 🟢 | P1 | IDE-0006 |
| EP-002 | Automatización y batch | 🟢 | P1 | IDE-0006 |
| EP-003 | Integraciones remotas | 🔵 | P2 | IDE-0006 |

Detalle: `docs/masterplan/epics/`.

---

## Reglas de mantenimiento

- Cada nueva idea comienza como **IDE**.
- Cuando una idea se aprueba para desarrollo, se vincula a una Épica (EP) y
  posteriormente a uno o varios Sprints (SPR).
- Las funcionalidades completadas permanecerán en este documento como histórico.
- Ninguna entrada se elimina; únicamente cambia de estado.

---

## Estado

**Estado actual:** 🟡 En revisión — IDE-0001…0018 en Studio/Core; primeras
EP (001…003) creadas para Fase 3; IDE-0006 → 🔵 P1.

Pendiente de:

- Diff `.bcproj` Core/CLI 🟢 (`boardcomposer-diff`); UI revisiones aún no;
- Fase 3 EP-001…003 🟢; siguiente: UAT humano / Fase 4 IA bajo demanda;
- completar el flujo Idea → Épica → Sprint → Implementación → Liberación;
- estimar esfuerzo por épica.
