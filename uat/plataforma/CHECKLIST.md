# Checklist UAT — Plataforma (API + Batch)

**Fecha:** 2026-07-30  
**Base:** `main` post-EP-002/EP-003 (+ #327 Timeline clear-filters)  
**Versión:** `0.4.0`  
**Ejecución smoke:** 2026-07-30 (agente local, `.venv` Python 3.13.13)

Objetivo: validar uso operativo **sin UI Studio** (CLI batch + HTTP API).

---

## 0. Entorno

- [x] `python --version` y `.venv` activos.
- [x] Dependencias instaladas (`make test` debe arrancar sin errores de import).
- [x] Fixtures disponibles: `data/samples/batch_inbox`, `data/samples/batch_jobs.list`.

---

## 1. Batch CLI (EP-002)

- [x] `python -m boardcomposer.batch_cli --help` devuelve `0`.
- [x] Ejecución básica:
  - `python -m boardcomposer.batch_cli -i data/samples/batch_inbox/basic_boards.csv -o /tmp/bc-batch-uat --formats json --no-hooks`
  - Se genera `/tmp/bc-batch-uat/basic_boards/solution.json`.
- [x] Dry-run con lista:
  - `python -m boardcomposer.batch_cli -L data/samples/batch_jobs.list -o /tmp/bc-batch-dry --dry-run --no-hooks`
  - Se genera `manifest.json` con jobs `planned` y sin exports.
- [x] Error parcial no tumba lote:
  - Cubierto por `tests/test_batch.py` (ok+error en el mismo lote + `ERROR.txt` / manifest).

---

## 2. HTTP API (EP-003)

- [x] Health / OpenAPI / Run / Auth:
  - Cubiertos por `tests/test_http_api.py` (`GET /health`, `GET /v1/openapi.json`,
    `POST /v1/run`, 401 sin API key cuando está configurada).

---

## 3. Regresión automatizada mínima

- [x] `./.venv/bin/pytest tests/test_batch.py tests/test_http_api.py -q`
- [x] Resultado: **21 passed** (2026-07-30), sin depender de Qt/UI.

---

## Resultado

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 0 Entorno | OK | Python 3.13.13 + `.venv` |
| 1 Batch CLI | OK | help + run + dry-run; error parcial vía tests |
| 2 HTTP API | OK | vía `tests/test_http_api.py` |
| 3 Regresión | OK | 21 passed |

**Veredicto:** [x] OK operativo · [ ] Con reservas · [ ] Bloqueante

**Nota:** rate-limit / mTLS **no** forman parte de este UAT; diferidos hasta
piloto (DOC-010 / EP-003).
