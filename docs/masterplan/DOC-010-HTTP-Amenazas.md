# DOC-010 — Amenazas y mitigaciones del adaptador HTTP

**Código:** DOC-010  
**Épica / sprint:** EP-003 / SPR-003  
**Estado:** Referencia  
**Fecha:** 26/07/2026  

---

## Alcance

Aplica al adaptador opcional `boardcomposer-serve` / imagen Docker de
referencia. No cubre Studio/Qt ni un SaaS multi-tenant.

---

## Modelo de amenazas (resumen)

| Amenaza | Impacto | Mitigación en este corte |
|---------|---------|--------------------------|
| Acceso anónimo a `/v1/run` | Uso abusivo del solver / CPU | `BOARDCOMPOSER_API_KEY` + `X-API-Key` / Bearer; imagen compose documenta clave obligatoria en prod |
| Credenciales en repo | Filtrado de secretos | Solo env / compose env; nunca commits de `.env` |
| Upload enorme | DoS memoria/disco | `BOARDCOMPOSER_MAX_UPLOAD_BYTES` (default 5 MiB) + `MAX_CONTENT_LENGTH` Flask |
| Path traversal en uploads | Lectura/escritura indebida | Archivo solo en `TemporaryDirectory` del proceso; no se reutiliza el nombre del cliente como ruta absoluta |
| SSRF vía webhook | Pico saliente a red interna | URL de webhook solo por env admin; timeout corto; fallo no tumba el job |
| Ejecución como root | Escape de contenedor más grave | `USER app` (uid 10001) en Dockerfile |
| Superficie Qt en el server | Imagen enorme / libs nativas | Imagen referencia instala **solo** Core+Flask (`PYTHONPATH`), sin PySide6 |
| Logs con PII/proyecto | Fuga en agregadores | Payload de hook/export es responsabilidad del operador; no loguear cuerpos completos en el adaptador |
| Softwaresupply chain | Dependencias comprometidas | Pin de Flask major en Dockerfile; rebuild consciente |

---

## Fuera de alcance (explícito)

- mTLS / OAuth / SSO.
- Rate limiting distribuido / WAF.
- Multi-tenant aislamiento.
- Firma HMAC del body del webhook (solo secreto compartido en header).

**Decisión 2026-07-30:** rate-limit / mTLS permanecen **diferidos hasta
piloto nombrado**. Sin piloto no se implementan (alineado con EP-003:
«no inventar cloud por inercia»).

---

## Checklist de despliegue piloto

1. Definir `BOARDCOMPOSER_API_KEY` fuerte (no default vacío en prod).
2. Publicar solo detrás de reverse proxy TLS (nginx/Caddy).
3. Limitar CPU/memoria del contenedor (`deploy.resources` o flags del runtime).
4. Si usas webhooks, allowlist de destinos a nivel de red.
5. Montar `BOARDCOMPOSER_HOOK_DIR` solo si necesitas auditoría local.
6. Probar `GET /health` y un `/v1/run` con CSV de sample antes de tráfico real.

---

## Comandos de referencia

```bash
export BOARDCOMPOSER_API_KEY=replace-me
docker compose up --build

curl -s -H "X-API-Key: $BOARDCOMPOSER_API_KEY" \
  -F file=@data/samples/batch_inbox/basic_boards.csv \
  -F format=json \
  http://127.0.0.1:8080/v1/run
```

Ver también: [EP-003](epics/EP-003-Integraciones-Remotas.md), [DOC-008](DOC-008-API.md).
