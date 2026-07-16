# BoardComposer

Plataforma para generar, comparar y explicar soluciones de corte 2D sobre uno
o varios tableros disponibles. Los algoritmos proponen alternativas; el usuario
conserva la decisión final.

## Estado actual

- Versión de desarrollo: `0.4.0.dev0`.
- Python 3.13.
- Core independiente de la interfaz.
- CLI con entrada CSV y salida texto/JSON.
- Studio en PySide6 con workspace, proyectos, inspector y soluciones.
- Generadores horizontal, vertical, free-space, Skyline y MaxRects.
- Beam Search, estrategias adaptativas, validación, scoring y diagnósticos.
- Packing MaxRects multipanel con cantidad, espesor y desperdicio por panel.
- Exportación SVG de soluciones de uno o varios paneles.
- Suite automatizada y CI con Ruff y Pytest.

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
make test       # suite completa
make check      # validación de proyecto, Ruff y Pytest
make demo       # ejemplo CLI
make json       # ejemplo CLI en JSON
python -m studio.app
```

## CSV de entrada

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

## Documentación

- [`docs/masterplan/INDEX.md`](docs/masterplan/INDEX.md): índice y precedencia.
- [`docs/masterplan/DOC-000-Manifiesto.md`](docs/masterplan/DOC-000-Manifiesto.md): propósito.
- [`docs/masterplan/DOC-003-Roadmap.md`](docs/masterplan/DOC-003-Roadmap.md): fases.
- [`docs/data_model.md`](docs/data_model.md): entidades y contrato multipanel.
- [`docs/algorithms.md`](docs/algorithms.md): pipeline y algoritmos.
