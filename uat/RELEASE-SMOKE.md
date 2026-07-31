# Release / demo smoke — BoardComposer

**Versión:** `0.4.0.dev0`  
**Fecha:** 2026-07-31  
**Base:** `main` (post #328 + este corte de pulido)

Checklist corta para validar «listo para demo / uso diario» sin sustituir UAT
completo (`uat/studio/`, `uat/plataforma/`).

---

## 1. Automatizado

- [x] `make check` (project check + ruff + pytest) → OK (875 passed, 2026-07-31)
- [x] `make demo` → OK (`free_space`, 1 solución, sin crash)
- [x] Cubierto por `make check` (`test_batch` + `test_http_api`)

## 2. Studio (manual ligero, 5–10 min)

- [ ] `make run` → Welcome con tips en CTAs
- [ ] Nuevo demo → calcular layout → Comparador con ≥1 candidata
- [ ] Timeline visible (Ctrl+3); filtros / Seguir / Limpiar filtros
- [ ] Guardar `.bcproj` → status menciona revisión local si aplica

## 3. Docs / deuda

- [x] `ROADMAP.md` alineado con DOC-003 (Fase 3 entregada)
- [x] DOC-006: métricas release revisadas (abiertas = 1 DT-0006 ≤ umbral)
- [x] UAT plataforma marcado OK (`uat/plataforma/CHECKLIST.md`)

## Resultado (rellenar al ejecutar)

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 1 Automatizado | OK | `make check` + `make demo` 2026-07-31 |
| 2 Studio | Pendiente | Checklist visual 5–10 min en máquina operador |
| 3 Docs / deuda | OK | DOC-004 estimaciones; DOC-006 métricas |

**Veredicto:** [x] OK demo (automatizado + docs) · [ ] Con reservas · [ ] Bloqueante

Reserva: paso 2 Studio manual aún sin tick en esta máquina CI-local.
