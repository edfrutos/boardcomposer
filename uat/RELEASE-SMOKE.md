# Release / demo smoke — BoardComposer

**Versión:** `0.4.2`  
**Fecha:** 2026-08-02  
**Base:** `main` @ release `0.4.2`

Checklist corta para validar «listo para demo / uso diario» sin sustituir UAT
completo (`uat/studio/`, `uat/plataforma/`).

---

## 1. Automatizado

- [ ] `make check` (project check + ruff + pytest) → OK
- [ ] `make demo` → sale con layout / JSON sin crash
- [ ] Cubierto por `make check` (`test_batch` + `test_http_api`)

## 2. Studio (manual ligero, 5–10 min)

- [ ] `make run` → Welcome / About muestran `0.4.2`
- [ ] Nuevo demo → calcular layout → Comparador → Ayuda → Explicar candidata → Copiar
- [ ] Proyecto guardado → Exportar backup de revisiones… (o CLI `boardcomposer-backup`)
- [ ] Restore: guardar 2× → Ctrl+Alt+Y → confirm → dirty

## 3. Docs / deuda

- [x] `ROADMAP.md` / CHANGELOG 0.4.2
- [x] DOC-006: DT-0006 en piloto D; IDE-0007 MVP local
- [x] UAT plataforma marcado OK (`uat/plataforma/CHECKLIST.md`)

## Resultado (rellenar al ejecutar)

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 1 Automatizado |  |  |
| 2 Studio |  |  |
| 3 Docs / deuda | OK | Corte 0.4.2 |

**Veredicto:** [ ] OK demo · [ ] Con reservas · [ ] Bloqueante
