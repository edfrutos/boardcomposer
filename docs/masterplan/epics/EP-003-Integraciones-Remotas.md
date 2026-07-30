# EP-003 — Integraciones y servicios remotos

**Épica:** EP-003  
**Fase:** 3 — Plataforma  
**Estado:** 🟢 Completada (SPR-001…003)
**Prioridad:** P2  
**Ideas:** IDE-0006 (extensión), exportadores avanzados  
**Docs:** DOC-008, EP-001, EP-002  

**Creada:** 26/07/2026  
**Última actualización:** 26/07/2026  

---

## Objetivo

Adaptar los contratos `v1` a **canales de integración** (HTTP u otros) y
a consumidores externos (ERP, pipelines, almacenamiento), sin acoplar el
Core a un vendor concreto.

---

## Fuera de alcance

- Marketplace / plugins de terceros (Fase 5).
- IA (Fase 4).
- Multi-tenant SaaS completo.

---

## Entregables

1. **Adaptador HTTP opcional** (si hay demanda piloto)  
   Thin layer sobre EP-001: health, solve, export; OpenAPI publicado.
2. **Hooks de integración**  
   Webhooks o escritura a rutas/credenciales configurables tras un job
   (local o remoto).
3. **Auth mínima**  
   Token/API key o mTLS documentado; sin SSO complejo en el primer corte.
4. **Límites y observabilidad**  
   Timeouts, tamaño de payload, logs correlacionables (ADR-003 eventos).
5. **Doc de despliegue**  
   Contenedor o servicio de referencia (opcional) + amenazas/mitigaciones.

---

## Sprints

| ID | Título | Estado | Notas |
|----|--------|--------|-------|
| SPR-001 | Adaptador HTTP Flask + OpenAPI + API key | 🟢 | `boardcomposer.api.http` / `boardcomposer-serve`; `GET /health`, `POST /v1/run`, `GET /v1/openapi.json`; env `BOARDCOMPOSER_API_KEY` |
| SPR-002 | Hooks post-job (webhook / carpeta) | 🟢 | `boardcomposer.integration.hooks`; env `BOARDCOMPOSER_HOOK_DIR` / `WEBHOOK_URL` / `SECRET`; batch `--hook-dir` |
| SPR-003 | Contenedor de referencia + amenazas | 🟢 | `Dockerfile` / `docker-compose.yml`; [DOC-010](../DOC-010-HTTP-Amenazas.md); `scripts/serve_docker.sh` |

---

## Dependencias

- EP-001 obligatorio.
- EP-002 recomendable (mismos jobs detrás del adaptador).

---

## Criterios de aceptación

- Un cliente HTTP (o integración acordada) completa solve+export vía
  contrato versionado.
- Credenciales no viven en el repo; se cargan por entorno/config.
- Fallos del adaptador no corrompen el Core ni proyectos locales.

---

## Uso (SPR-001)

```bash
export BOARDCOMPOSER_API_KEY=dev-secret   # opcional pero recomendado
boardcomposer-serve --host 127.0.0.1 --port 8080

curl -s http://127.0.0.1:8080/health
curl -s -H "X-API-Key: $BOARDCOMPOSER_API_KEY" \
  -F file=@data/samples/batch_inbox/basic_boards.csv \
  -F strategy=balanced -F format=json \
  http://127.0.0.1:8080/v1/run
```

OpenAPI: `GET /v1/openapi.json`.  
Límite upload: `BOARDCOMPOSER_MAX_UPLOAD_BYTES` (default 5 MiB).

---

### Hooks post-job (SPR-002)

Tras cada job ok/error (batch o HTTP):

- Carpeta: `BOARDCOMPOSER_HOOK_DIR` → `job.json` + copia de exports.
- Webhook: `BOARDCOMPOSER_WEBHOOK_URL` POST JSON; opcional
  `BOARDCOMPOSER_WEBHOOK_SECRET` → header `X-BoardComposer-Secret`.
- Timeout: `BOARDCOMPOSER_WEBHOOK_TIMEOUT` (default 5s).
- Fallo del hook **no** tumba el job.

```bash
boardcomposer-batch -i data/samples/batch_inbox -o out/batch \
  --hook-dir out/hooks --no-hooks   # --no-hooks desactiva
```

### Contenedor (SPR-003)

```bash
export BOARDCOMPOSER_API_KEY=dev-secret
docker compose up --build
# o: scripts/serve_docker.sh
```

Imagen: Core + Flask (sin PySide6). Amenazas: [DOC-010](../DOC-010-HTTP-Amenazas.md).

## Notas de diseño

Capa fina sobre `boardcomposer.api.v1` — sin lógica de packing en Flask.
EP-003 cerrada en el corte de referencia; ampliar rate-limit/mTLS solo con piloto
(**diferido 2026-07-30** hasta piloto nombrado; ver DOC-010).
No inventar cloud por inercia.
