
# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.3.15  
**Estado:** En revisión — actualizado  
**Fecha de creación:** 01/07/2026  
**Última revisión:** 25/08/2026

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
| IDE-0007 | Asistente IA | 🟡 MVP local | P2 |
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
| IDE-0019 | Intercambiar dos piezas seleccionadas | ⚪ | P2 |
| IDE-0020 | Kerf / espesor de sierra en packing | ⚪ | P2 |
| IDE-0021 | Restricción de veta / orientación de fibra | ⚪ | P2 |
| IDE-0022 | Packing multipanel Skyline | ⚪ | P2 |
| IDE-0023 | Lista de corte / informe de taller | ⚪ | P2 |
| IDE-0024 | Metadatos de proyecto (cliente, ref., notas) | ⚪ | P2 |

### Estimaciones de esfuerzo (ideas abiertas)

Escala: **S** ≤ 1 semana · **M** 2–4 semanas · **L** 1–2 meses · **XL** > 2 meses
(equipo pequeño / 1–2 personas). Son órdenes de magnitud, no compromisos.

| ID | Esfuerzo | Dependencias | Notas |
|----|----------|--------------|-------|
| IDE-0007 | L–XL | Caso de uso claro; política de datos | Fase 4; MVP local hecho; eval humana + LLM diferido |
| IDE-0008 | XL | ADR-004; contratos de extensión | Fase 5; marketplace fuera del MVP plugin |
| DT-0006 | M (opción D/A) · L–XL (opción C) | Piloto nombrado; DOC-005 | Spike: `spikes/SPIKE-DT-0006-historial-cloud.md` |
| IDE-0019 | S–M | SelectionController; Command Pattern | Límite MASTERPLAN / SCR-002 |
| IDE-0020 | M | PlacementValidator (ADR-010); migraciones | Preferencias + `.bcproj` |
| IDE-0021 | M | Modelo de pieza; solvers | Afecta rotación automática |
| IDE-0022 | M–L | ADR-014 contrato multipanel | Hoy solo MaxRects multipanel |
| IDE-0023 | M | Export PDF/CSV; SCR-007 | Lista piezas/paneles para taller |
| IDE-0024 | S | SCR-005 evolución; persistencia v2+ | Sin kerf/vetas aún (van en 0020/0021) |

---

## Épicas (Fase 3)

| ID | Título | Estado | Prioridad | Ideas |
|----|--------|--------|-----------|-------|
| EP-001 | API pública y contratos | 🟢 | P1 | IDE-0006 |
| EP-002 | Automatización y batch | 🟢 | P1 | IDE-0006 |
| EP-003 | Integraciones remotas | 🟢 | P2 | IDE-0006 |

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

**Estado actual:** 🟢 Actualizado — IDE-0001…0018 Studio/Core completadas
(salvo IDE-0007 🟡 MVP local + eval abierta); EP (001…003) Fase 3 entregadas;
IDE-0019…0024 siguen como ideas abiertas (revisión 2026-08-25: sin IDE
nuevas; cola no vacía; Issues GitHub abiertos = 0). Ver
`REVIEW-2026-08-25-planificacion.md`.

Próximo foco:

1. Cerrar eval humana IDE-0007 (`uat/studio/CHECKLIST-EXPLAIN-EVAL.md`).
2. Mantener piloto DT-0006 D; no abrir C sin demanda multi-usuario.
3. Ciclo `0.4.3`: QoL / candidatos IDE-0019…0024 bajo demanda
   (orden sugerido en la revisión).
4. Plugins (IDE-0008) — XL; no priorizar sin ADR-004 operativo.
5. LLM opt-in — solo tras eval + DEC-0011 / política de datos.
