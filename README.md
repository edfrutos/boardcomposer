# BoardComposer

Plataforma para generar, comparar y explicar soluciones de corte 2D sobre uno
o varios tableros disponibles. Los algoritmos proponen alternativas; el usuario
conserva la decisión final.

## Estado actual

- Versión de desarrollo: `0.4.0.dev0`.
- Python 3.13.
- Core independiente de la interfaz.
- CLI con entrada CSV y salida texto/JSON.
- Batch headless (`boardcomposer-batch`) sobre CSV / `.bcproj` (EP-002).
- Studio en PySide6 con workspace, proyectos, inspector y soluciones.
- Generadores horizontal, vertical, free-space, Skyline y MaxRects.
- Beam Search, estrategias adaptativas, validación, scoring y diagnósticos.
- Packing MaxRects multipanel con cantidad, espesor **y material** por panel.
- Movimiento y reasignación interactiva de piezas entre paneles físicos desde
  el Workspace, con deshacer/rehacer.
- Soluciones parciales (piezas omitidas) en vez de "sin solución" cuando no
  todo cabe, con diagnóstico del solver en el Inspector.
- Retales aprovechables (informativos) reportados por panel consumido.
- Comparador de soluciones con resaltado de mejor solución por métrica.
- Importación de inventario de tableros desde CSV, con vista previa y
  validación por fila.
- Migraciones explícitas y versionadas de proyectos `.bcproj`.
- Exportación SVG de soluciones de uno o varios paneles.
- Suite automatizada (incluye pruebas de interacción Qt del Workspace) y CI
  con Ruff y Pytest.
- Benchmarks reproducibles del generador multipanel
  (`scripts/benchmark_multipanel_maxrects.py`).
- Generador CP-SAT opcional de un solo panel (`boardcomposer[cp_sat]`,
  estrategia `exact`).
- Comparador con ordenación/filtrado por métrica.
- Exportación SVG, DXF y PDF de la solución seleccionada.
- Importación CSV de inventario de tableros y de piezas.

## Arquitectura

```text
CLI · Studio · futuras API
           │
           ▼
BoardComposer Core
  ├── Domain
  ├── Geometry / Layout
  ├── Solver pipeline
  ├── Presenters
  └── Exporters
```

El Core nunca importa componentes de Studio. Consulta
[`docs/architecture.md`](docs/architecture.md) y el
[`MASTERPLAN`](docs/masterplan/MASTERPLAN.md).

## Instalación

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Comandos

```bash
make test                 # suite completa
make check                # validación de proyecto, Ruff y Pytest
make demo                 # ejemplo CLI
make json                 # ejemplo CLI en JSON
make benchmark-multipanel # benchmarks reproducibles del packing multipanel
python -m studio.app

# Batch sin Studio/Qt (EP-002)
boardcomposer-batch -i data/samples/batch_inbox -o out/batch \
  -p data/samples/batch_profile.json
# Lista explícita + dry-run:
boardcomposer-batch -L data/samples/batch_jobs.list -o out/batch --dry-run
# Plantilla export Studio (por nombre / cliente):
boardcomposer-batch -i data/samples/batch_inbox -o out/batch \
  --template "SVG sin retales" --client Demo \
  --templates-file data/samples/export_templates.json
# o: scripts/batch_samples.sh

# Diff dos revisiones .bcproj
# boardcomposer-diff a.bcproj b.bcproj

# HTTP opcional (EP-003; API key recomendada)
# BOARDCOMPOSER_API_KEY=dev-secret boardcomposer-serve --port 8080
# Hooks post-job: BOARDCOMPOSER_HOOK_DIR / BOARDCOMPOSER_WEBHOOK_URL
```

## CSV de entrada (CLI)

Columnas obligatorias:

```text
id,length_mm,width_mm,thickness_mm
```

Ejemplo:

```text
A,2000,300,20
B,1000,300,20
C,800,250,20
```

## Importar inventario de tableros en Studio (CSV)

Desde `Proyecto → Importar inventario de tableros (CSV)…`. Columnas
reconocidas (acepta alias en español e inglés; solo las tres primeras son
obligatorias):

```text
board_id,length_mm,width_mm,thickness_mm,quantity,material
```

Ejemplo (`data/samples/studio_boards_inventory.csv`):

```text
TAB-001,2440,1220,19,3,Melamina blanca
TAB-002,2750,1830,19,2,MDF
```

Studio muestra una vista previa con el resultado por fila (válida o con
error) antes de incorporar los tableros al proyecto. Ver
[`FLW-002-Importar-CSV`](docs/masterplan/ui/flows/FLW-002-Importar-CSV.md).

## Documentación

- [`docs/masterplan/INDEX.md`](docs/masterplan/INDEX.md): índice y precedencia.
- [`docs/masterplan/DOC-000-Manifiesto.md`](docs/masterplan/DOC-000-Manifiesto.md): propósito.
- [`docs/masterplan/DOC-003-Roadmap.md`](docs/masterplan/DOC-003-Roadmap.md): fases.
- [`docs/data_model.md`](docs/data_model.md): entidades y contrato multipanel.
- [`docs/algorithms.md`](docs/algorithms.md): pipeline y algoritmos.
- [`docs/masterplan/adr/ADR-014-Multi-Panel-Packing.md`](docs/masterplan/adr/ADR-014-Multi-Panel-Packing.md): contrato multipanel (referencia de panel, validación, desperdicio).
- [`docs/masterplan/adr/ADR-015-Migraciones-Bcproj.md`](docs/masterplan/adr/ADR-015-Migraciones-Bcproj.md): migraciones explícitas de proyectos `.bcproj`.
- [`docs/masterplan/adr/ADR-016-Retales-Informativos.md`](docs/masterplan/adr/ADR-016-Retales-Informativos.md): retales como información, no como inventario.
- [`TODO.md`](TODO.md) y [`CHANGELOG.md`](CHANGELOG.md): backlog operativo e histórico de versiones.
