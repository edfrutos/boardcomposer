# Release / demo smoke — BoardComposer

**Versión:** `0.4.1`  
**Fecha:** 2026-08-01  
**Base:** `main` @ release `0.4.1`

Checklist corta para validar «listo para demo / uso diario» sin sustituir UAT
completo (`uat/studio/`, `uat/plataforma/`).

---

## 1. Automatizado

- [ ] `make check` (project check + ruff + pytest) → OK
- [ ] `make demo` → sale con layout / JSON sin crash
- [ ] Cubierto por `make check` (`test_batch` + `test_http_api`)

## 2. Studio (manual ligero, 5–10 min)

- [ ] `make run` → Welcome / About muestran `0.4.1`
- [ ] Nuevo demo → calcular layout → Comparador con ≥1 candidata
- [ ] Restore: guardar 2× → Ctrl+Alt+Y → confirm → dirty
- [ ] Calcular layout deshabilitado en proyecto vacío (sin tablero/pieza)

## 3. Docs / deuda

- [x] `ROADMAP.md` / CHANGELOG 0.4.1
- [x] DOC-006: deuda abierta = DT-0006 (≤ umbral)
- [x] UAT plataforma marcado OK (`uat/plataforma/CHECKLIST.md`)

## Resultado (rellenar al ejecutar)

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 1 Automatizado |  |  |
| 2 Studio |  |  |
| 3 Docs / deuda | OK | Corte 0.4.1 |

**Veredicto:** [ ] OK demo · [ ] Con reservas · [ ] Bloqueante
