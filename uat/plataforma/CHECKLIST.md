# Checklist UAT — Plataforma (API + Batch)

**Fecha:** 2026-07-30  
**Base:** `main` post-EP-002/EP-003  
**Versión:** `0.4.0.dev0`

Objetivo: validar uso operativo **sin UI Studio** (CLI batch + HTTP API).

---

## 0. Entorno

- [ ] `python --version` y `.venv` activos.
- [ ] Dependencias instaladas (`make test` debe arrancar sin errores de import).
- [ ] Fixtures disponibles: `data/samples/batch_inbox`, `data/samples/batch_jobs.list`.

---

## 1. Batch CLI (EP-002)

- [ ] `python -m boardcomposer.batch_cli --help` devuelve `0`.
- [ ] Ejecución básica:
  - `python -m boardcomposer.batch_cli -i data/samples/batch_inbox/basic_boards.csv -o /tmp/bc-batch --formats json --no-hooks`
  - Se genera `/tmp/bc-batch/basic_boards/solution.json`.
- [ ] Dry-run con lista:
  - `python -m boardcomposer.batch_cli -L data/samples/batch_jobs.list -o /tmp/bc-batch-dry --dry-run --no-hooks`
  - Se genera `manifest.json` con jobs `planned` y sin exports.
- [ ] Error parcial no tumba lote:
  - Entrada mixta (un archivo válido + uno inválido) produce `ok>=1`, `error>=1`.
  - Se genera `ERROR.txt` para fallos y `manifest.json` final.

---

## 2. HTTP API (EP-003)

- [ ] Health:
  - `GET /health` responde `200` y payload con `status: ok`.
- [ ] OpenAPI:
  - `GET /v1/openapi.json` responde `200` y expone `/v1/run`.
- [ ] Run multipart:
  - `POST /v1/run` con `basic_boards.csv` y `format=json` responde `200`.
  - Respuesta incluye `placements`.
- [ ] Auth opcional:
  - Con `BOARDCOMPOSER_API_KEY` configurada, `POST /v1/run` sin key -> `401`.
  - Con header `X-API-Key` correcto -> `200`.

---

## 3. Regresión automatizada mínima

- [ ] `./.venv/bin/pytest tests/test_batch.py tests/test_http_api.py -q`
- [ ] Resultado esperado: tests verdes sin depender de Qt/UI.

---

## Resultado

| Bloque | ¿OK? | Notas |
| --- | --- | --- |
| 0 Entorno |  |  |
| 1 Batch CLI |  |  |
| 2 HTTP API |  |  |
| 3 Regresión |  |  |

**Veredicto:** [ ] OK operativo · [ ] Con reservas · [ ] Bloqueante
