# BoardComposer

## Documento 6 — Gestión de la Deuda Técnica

**Código:** DOC-006
**Versión:** 1.2.42
**Estado:** Actualizado
**Fecha de creación:** 01/07/2026
**Última revisión:** 25/09/2026

---

## Objetivo

Registrar, clasificar y gestionar toda la deuda técnica del proyecto BoardComposer para asegurar que el crecimiento del producto no comprometa su calidad, mantenibilidad ni capacidad de evolución.

La deuda técnica es un elemento normal del desarrollo. El objetivo no es eliminarla por completo, sino hacerla visible, controlarla y decidir conscientemente cuándo asumirla o resolverla.

---

## Principios

- Toda deuda técnica conocida debe registrarse.
- La deuda nunca debe depender de la memoria del equipo.
- Cada elemento tendrá una prioridad y un impacto estimado.
- La deuda técnica forma parte de la planificación del producto.
- Ninguna deuda crítica podrá permanecer indefinidamente sin revisión.

---

## Clasificación

### DT-A — Arquitectura

Problemas de diseño estructural.

### DT-C — Código

Duplicación, complejidad o refactorizaciones pendientes.

### DT-T — Tests

Cobertura insuficiente o pruebas mejorables.

### DT-D — Documentación

Documentación incompleta o desactualizada.

### DT-P — Rendimiento

Aspectos relacionados con optimización y escalabilidad.

### DT-UX — Experiencia de usuario

Limitaciones conocidas en la interfaz o flujo de trabajo.

---

## Formato de un registro

```text
DT-0001

Título

Categoría

Prioridad

Descripción

Impacto

Riesgo

Propuesta de resolución

Documentos relacionados

Estado
```

---

## Registro inicial

| ID | Categoría | Descripción | Estado |
|----|-----------|-------------|--------|
| DT-0001 | DT-D | Contrastar flujos y pantallas documentados con el Studio real. | 🟢 Controlado (UAT visual 2026-07-28) |
| DT-0002 | DT-A | Documentar arquitectura interna y contrato multipanel del Solver. | 🟢 Controlado |
| DT-0003 | DT-T | Mantener la cobertura de pruebas por encima del objetivo definido. | 🟢 Controlado |
| DT-0004 | DT-T | Añadir cobertura automatizada de interacción Qt y Workspace. | 🟢 Resuelto (`tests/conftest.py`, `tests/test_workspace_qt_interaction.py`) |
| DT-0005 | DT-UX | Habilitar movimiento y reasignación interactiva entre paneles. | 🟢 Resuelto (arrastre entre paneles físicos en el Workspace) |
| DT-0006 | DT-A | Historial cloud/multi-usuario de revisiones `.bcproj` (el anillo local ya está entregado). Spike: `spikes/SPIKE-DT-0006-historial-cloud.md`. Piloto opción D: `docs/ops/PILOT-DT-0006-backup.md` + `boardcomposer-backup`. | 🟡 En piloto (D) |

---

## Métricas mínimas por release

Revisar este documento en cada corte de release (`0.x.y` o RC). Anotar fecha y
conteo en «Estado» o en las notas de release.

| Métrica | Cómo contar | Umbral |
|---------|-------------|--------|
| Abiertas ⚪/🔵 | Filas del registro con estado no resuelto/controlado | Advertencia si **> 5**; bloquear release mayor si **> 0 críticas sin plan** |
| Antigüedad máxima | Días desde última revisión del ítem abierto más viejo | Advertencia si **> 90 días** sin actualización de estado |
| Por categoría | Conteo DT-A / C / T / D / P / UX abiertas | Flag si DT-A o DT-T abiertas crecen respecto al release anterior |
| Resueltas en el ciclo | Ítems que pasaron a 🟢 Resuelto/Controlado desde el release previo | Informativo (tendencia) |

**Severidad:**

- **Bloqueante (release mayor):** deuda DT-A o seguridad sin mitigación documentada
  y sin decisión en DOC-005.
- **Advertencia:** umbrales de la tabla; no bloquea patch/`dev0` si hay plan
  explícito en «Próximo foco».

**Corte 2026-09-14 (`0.4.3`):** abiertas = **1** (DT-0006 en piloto D;
opción C diferida); sin críticas sin plan. Cola producto 0019…0024 cerrada.

**Revisión 2026-09-15 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. Cola implementable 0019…0024 vacía → IDE-0025…0030.

**Revisión 2026-09-16 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. Ola 1 (0025…0030) cerrada (`#638`); segunda ola
IDE-0031…0036.

**Revisión 2026-09-17 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. Segunda ola 0031…0036 en `main`; IDE-0037 cotas
de tablero; IDE-0038 raster; cola 0039…0040; Issues = 0.

**Revisión 2026-09-18 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. Cola implementable vacía en `main` → tercera ola
IDE-0037…0042 (PR `#648`); `#647` 🟡 al corte.

**Revisión 2026-09-19 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. `#647`/`#649` mergeados; IDE-0039 trazabilidad
de plano; cola 0040…0042; Issues = 0.

**Revisión 2026-09-20 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. `#651` (IDE-0039) mergeado; residual 0040…0042;
Issues = 0.

**Revisión 2026-09-21 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. `#653`/`#654` mergeados; cola 0042…0046; Issues = 0.

**Revisión 2026-09-22 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. `#655`/`#657`/`#658`/`#659` (0042…0045) en `main`;
0048 `#663` / 0049 `#664` / 0050 `#665` / 0051 `#666` / 0052
entregadas; sexta ola 0053…0054; Issues = 0.

**Revisión 2026-09-23 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. `#661`…`#667` (0046…0052) en `main`; IDE-0053
entregada; residual 0054; Issues = 0.

**Revisión 2026-09-24 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. `#671` (IDE-0053) en `main`; residual 0054; Issues = 0.

**Revisión 2026-09-25 (`0.4.4.dev0`):** abiertas = **1** (DT-0006 en piloto D);
sin críticas sin plan. `#672` (IDE-0054) en `main`; sexta ola cerrada;
séptima ola 0055…0058 (`#673` 🟡); Issues = 0.

---

## Política de gestión

- La deuda técnica deberá revisarse al cierre de cada Sprint **y** en el
  checklist de release (`uat/RELEASE-SMOKE.md`).
- Ninguna versión mayor del producto se publicará sin revisar este documento.
- Las deudas resueltas permanecerán registradas como histórico.
- La prioridad podrá modificarse, pero nunca desaparecerá el registro.
- Vincular cambios de estado a una línea en CHANGELOG / notas de release.

---

## Relación con otros documentos

- DOC-002 — Arquitectura.
- DOC-003 — Roadmap.
- DOC-004 — Backlog.
- DOC-005 — Registro de Decisiones.
- ADR relacionados.

---

## Estado

**Estado actual:** 🟢 Actualizado — revisado para ciclo `0.4.4.dev0`; snapshot
2026-09-25 en `REVIEW-2026-09-25-planificacion.md` (abiertas = 1, DT-0006).
Históricos: `REVIEW-2026-09-11`…`09-24` (abiertas = 1, DT-0006).

Próximo foco:

- Spike DT-0006 documentado (`spikes/SPIKE-DT-0006-historial-cloud.md`):
  piloto **opción D** activo (`docs/ops/PILOT-DT-0006-backup.md`); **C** solo
  con multi-usuario real.
- IDE-0007: MVP explicación local + eval humana cerrada 2026-09-12
  (`spikes/SPIKE-IDE-0007-asistente-ia.md`); LLM diferido (DEC-0011).
<<<<<<< HEAD
- Cola producto ciclo `0.4.4` séptima ola: `#673` (IDE-0055) → 0056…0058
=======
- Cola producto ciclo `0.4.4` séptima ola IDE-0056 (0055 entregada)
>>>>>>> origin/main
- Aplicar métricas de la sección «Métricas mínimas por release» en cada corte.
- Vincular revisión DOC-006 al cierre de sprint y a `uat/RELEASE-SMOKE.md`.
