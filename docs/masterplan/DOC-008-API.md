
# BoardComposer

## Documento 8 — API y Extensibilidad

**Código:** DOC-008
**Versión:** 1.0.0
**Estado:** En revisión
**Fecha de creación:** 01/07/2026
**Última revisión:** 26/07/2026 (SPR-001 Python `v1`)

---

## Objetivo

Definir la arquitectura de integración de BoardComposer mediante una API pública, estable y desacoplada del Core, permitiendo que aplicaciones, automatizaciones y servicios externos puedan utilizar el motor de optimización sin depender de una interfaz concreta.

---

## Principios

- El Core será la única fuente de lógica de negocio.
- La API expondrá capacidades, nunca implementaciones internas.
- La compatibilidad hacia atrás será un objetivo prioritario.
- Toda operación deberá ser reproducible y trazable.
- La API deberá ser válida para aplicaciones de escritorio, web, móviles y servicios.

---

## Objetivos funcionales

La API deberá permitir:

- crear y gestionar proyectos;
- importar piezas y tableros;
- ejecutar algoritmos de optimización;
- comparar soluciones;
- consultar métricas y explicaciones;
- exportar resultados;
- administrar configuraciones y perfiles.

---

## Arquitectura

```text
Cliente
    │
    ▼
BoardComposer API
    │
    ▼
BoardComposer Core
    │
    ├── Domain
    ├── Solver
    ├── Evaluation
    └── Exporters
```

La API actuará como una capa de adaptación entre los clientes y el Core, evitando que estos dependan de detalles internos.

---

## Versionado

Se adoptará versionado semántico para la API.

Ejemplos:

- Paquete Python: `boardcomposer.api.v1` (`API_VERSION`, p. ej. `1.0.0`)
- HTTP futuro: `/api/v1/`, `/api/v2/` (EP-003)

Los cambios incompatibles requerirán una nueva versión mayor
(`boardcomposer.api.v2` / `/api/v2/`), no mutar `v1` in-place.

### Primer corte Python (SPR-001 / EP-001)

Superficie estable sin Qt ni `studio.*`:

| Función | Rol |
|---------|-----|
| `load_project(path)` | CSV de piezas → `Project` |
| `solve(project, strategy=…, top=…)` | candidatas rankeadas |
| `export_json` / `export_svg` / `export_csv` | artefactos de solución |
| `run(path, …)` | load + solve |
| `API_VERSION` | semver del contrato |

Ejemplo: `examples/api_v1_minimal.py`. Tests de contrato:
`tests/test_api_v1_contract.py`.

Formatos de intercambio (CSV entrada, JSON/CSV/SVG solución):
[DOC-009](DOC-009-API-v1-Formatos.md) (SPR-002).

---

## Extensibilidad

La arquitectura deberá facilitar:

- nuevos algoritmos;
- nuevos importadores y exportadores;
- proveedores de autenticación;
- asistentes basados en IA;
- plugins desarrollados por terceros.

---

## Seguridad

La especificación definitiva contemplará:

- autenticación;
- autorización;
- validación de entradas;
- limitación de uso cuando proceda;
- trazabilidad de operaciones.

---

## Relación con otros documentos

- DOC-001 — Producto.
- DOC-002 — Arquitectura.
- DOC-005 — Registro de Decisiones.
- ADR relacionados.

---

## Estado

**Estado actual:** 🟡 En revisión — SPR-001/002 entregados (`v1` + DOC-009)

Pendiente de (ejecución vía [EP-001](epics/EP-001-API-Publica-Contratos.md)):

- ampliar carga de proyecto (`.bcproj` / multipanel) vía API (SPR-003);
- especificar recursos HTTP si un piloto lo exige (EP-003);
- elaborar una guía para desarrolladores e integradores.
