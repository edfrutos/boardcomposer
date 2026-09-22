
# BoardComposer

## Documento 4 — Backlog del Producto

**Código:** DOC-004
**Versión:** 1.3.46
**Estado:** En revisión — actualizado
**Fecha de creación:** 01/07/2026
**Última revisión:** 22/09/2026

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
| IDE-0007 | Asistente IA | 🟢 MVP + eval | P2 |
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
| IDE-0019 | Intercambiar dos piezas seleccionadas | 🟢 | P2 |
| IDE-0020 | Kerf / espesor de sierra en packing | 🟢 | P2 |
| IDE-0021 | Restricción de veta / orientación de fibra | 🟢 | P2 |
| IDE-0022 | Packing multipanel Skyline | 🟢 | P2 |
| IDE-0023 | Lista de corte / informe de taller | 🟢 | P2 |
| IDE-0024 | Metadatos de proyecto (cliente, ref., notas) | 🟢 | P2 |
| IDE-0025 | Retales como inventario reutilizable | 🟢 | P2 |
| IDE-0026 | Etiquetas de piezas en plano (SVG/PDF) | 🟢 | P2 |
| IDE-0027 | Secuencia de corte por panel | 🟢 | P2 |
| IDE-0028 | Catálogo de materiales / espesores | 🟢 | P2 |
| IDE-0029 | Coste estimado de material | 🟢 | P3 |
| IDE-0030 | Congelar colocaciones / re-pack omitidas | 🟢 | P2 |
| IDE-0031 | Medidas típicas de tablero en catálogo | 🟢 | P2 |
| IDE-0032 | Informe de presupuesto PDF | 🟢 | P2 |
| IDE-0033 | Etiquetas de retales en plano | 🟢 | P2 |
| IDE-0034 | Papel / márgenes / escala en PDF | 🟢 | P2 |
| IDE-0035 | Exportar soluciones en lote | 🟢 | P2 |
| IDE-0036 | Colocación manual asistida (sugerir hueco) | 🟢 | P3 |
| IDE-0037 | Cotas L×A del tablero en plano | 🟢 | P2 |
| IDE-0038 | Calidad raster PNG/JPEG (DPI) | 🟢 | P3 |
| IDE-0039 | Trazabilidad en plano (versión, algoritmo, fecha) | 🟢 | P3 |
| IDE-0040 | Unidades en Inspector (mm/cm/in) | 🟢 | P3 |
| IDE-0041 | Capas DXF por rol (marco/pieza/retal/cota) | 🟢 | P3 |
| IDE-0042 | Exportar/importar catálogo de materiales | 🟢 | P3 |
| IDE-0043 | Trazabilidad en lista de corte / presupuesto | 🟢 | P3 |
| IDE-0044 | Unidades prefs en plano y etiquetas de export | 🟢 | P3 |
| IDE-0045 | Mano de obra en presupuesto | 🟢 | P3 |
| IDE-0046 | Inspector: espesor / rotación / veta de pieza | ⚪ | P3 |

### Estimaciones de esfuerzo (ideas abiertas)

Escala: **S** ≤ 1 semana · **M** 2–4 semanas · **L** 1–2 meses · **XL** > 2 meses
(equipo pequeño / 1–2 personas). Son órdenes de magnitud, no compromisos.

| ID | Esfuerzo | Dependencias | Notas |
|----|----------|--------------|-------|
| IDE-0007 | L–XL | Caso de uso claro; política de datos | Fase 4; MVP+eval 2026-09-12; LLM diferido |
| IDE-0008 | XL | ADR-004; contratos de extensión | Fase 5; marketplace fuera del MVP plugin |
| DT-0006 | M (opción D/A) · L–XL (opción C) | Piloto nombrado; DOC-005 | Spike: `spikes/SPIKE-DT-0006-historial-cloud.md` |
| IDE-0019 | S–M | SelectionController; Command Pattern | Entregado; Ctrl+Alt+X; no-op si no cabe |
| IDE-0020 | M | PlacementValidator (ADR-010); migraciones | Entregado; v4 `kerf_mm`; default prefs |
| IDE-0021 | M | Modelo de pieza; solvers | Entregado; v5 `grain`; no rotar |
| IDE-0022 | M–L | ADR-014 contrato multipanel | Entregado; Skyline + MaxRects (#623) |
| IDE-0023 | M | Export PDF/CSV; SCR-007 | Entregado; Ctrl+Alt+C; CSV/PDF |
| IDE-0024 | S | SCR-005 evolución; persistencia v3 | Entregado; kerf/vetas en 0020/0021 |
| IDE-0025 | M–L | ADR-016; migraciones `.bcproj`; StockPanel | Entregado; Ctrl+Alt+R; v6 remnant |
| IDE-0026 | S–M | SCR-007 export; Workspace labels | Entregado; id + LxW mm; casilla export |
| IDE-0027 | M | IDE-0023; métricas por panel | Entregado; CSV/PDF + números plano |
| IDE-0028 | M | SCR-005; prefs / archivo usuario | Entregado; Ctrl+Alt+T; JSON usuario |
| IDE-0029 | S–M | IDE-0028 útil; scoring / export | Entregado; €/m² catálogo; tablero físico |
| IDE-0030 | M | Pipeline parciales; Command Pattern | Entregado; Ctrl+Alt+F; freeze OK |
| IDE-0031 | S | IDE-0028; NewBoardDialog | Entregado; L×A en catálogo; combo tablero |
| IDE-0032 | S–M | IDE-0029; IDE-0023; SCR-007 | PDF presupuesto; no cambia solver |
| IDE-0033 | S–M | IDE-0026; ADR-016 | Medidas de retal en plano |
| IDE-0034 | M | SCR-007; export PDF | Entregado; papel/márgenes/escala plano |
| IDE-0035 | M | SCR-007; ExportDialog | Entregado; lote candidatas Studio |
| IDE-0036 | M–L | Workspace; PlacementValidator | Entregado; Ctrl+Alt+G; snap drop |
| IDE-0037 | S–M | SCR-007; export SVG/PDF/DXF | Entregado; cotas L×A; casilla export |
| IDE-0038 | S | SCR-007; raster PNG/JPEG | Entregado; DPI 36–300; JPEG 1–100 |
| IDE-0039 | S–M | SCR-007; export plan | Entregado; pie versión/algoritmo/fecha |
| IDE-0040 | S–M | Inspector; prefs.units | Entregado (#653); display prefs; mm en disco |
| IDE-0041 | S–M | SCR-007; DXF exporter | Entregado (#654); tabla LAYER por rol |
| IDE-0042 | S | IDE-0028; catálogo JSON | Entregado (#655); export/import JSON; sin nube |
| IDE-0043 | S | IDE-0039; cut list / quote PDF | Entregado; pie en PDF; CSV no |
| IDE-0044 | S–M | IDE-0040; SCR-007 etiquetas | Entregado; prefs.units en plano TEXT; mm en disco |
| IDE-0045 | S–M | IDE-0032; catálogo / prefs | Entregado; EUR/h + min/pieza; 0 omite |
| IDE-0046 | S | SCR-004 Inspector | Espesor, rotación y veta de pieza |

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

**Estado actual:** 🟢 Actualizado — IDE-0001…0045 Studio/Core
completadas (ciclo `0.4.4` ola 1 + 0031…0045; `#647`/`#649`/`#651`/
`#653`/`#654`/`#655`/`#657`/`#658`/`#659`). IDE-0007 🟢 MVP+eval
(2026-09-12; LLM diferido). EP (001…003) Fase 3 entregadas. Snapshot:
`REVIEW-2026-09-22-planificacion.md`.

Próximo foco:

1. Cola producto `0.4.4` cuarta ola: IDE-0046 (0042…0045 en `main`).
2. Mantener piloto DT-0006 D; no abrir C sin demanda multi-usuario.
3. Ciclo `0.4.4.dev0` abierto; `v0.4.3` publicado.
4. Plugins (IDE-0008) — XL; no priorizar sin ADR-004 operativo.
5. LLM opt-in — solo tras DEC-0011 / política de datos (eval ya cerrada).
