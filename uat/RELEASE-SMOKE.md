# Release / demo smoke — BoardComposer

**Versión:** `0.4.3.dev0`  
**Fecha:** 2026-08-02  
**Base:** `main` @ ciclo `0.4.3.dev0` (última estable: `0.4.2`)

Checklist corta para validar «listo para demo / uso diario» sin sustituir UAT
completo (`uat/studio/`, `uat/plataforma/`).

---

## 1. Automatizado

- [ ] `make check` (project check + ruff + pytest) → OK
- [ ] `make demo` → sale con layout / JSON sin crash
- [ ] Cubierto por `make check` (`test_batch` + `test_http_api`)

## 2. Studio (manual ligero, 5–10 min)

- [ ] `make run` → Welcome / About muestran `0.4.3.dev0`
- [ ] Nuevo demo → calcular layout → Comparador → **Ctrl+Alt+E** Explicar candidata → Copiar
  (eval 5 candidatas: [`studio/CHECKLIST-EXPLAIN-EVAL.md`](studio/CHECKLIST-EXPLAIN-EVAL.md))
- [ ] Editar pieza tras calcular → banner desactualizadas + CTA **Calcular layout**
- [ ] Proyecto guardado → **Ctrl+Alt+B** Exportar backup → Abrir carpeta (o CLI `boardcomposer-backup`)
- [ ] Restore: guardar 2× → Ctrl+Alt+Y → confirm → dirty

## 3. Docs / deuda

- [x] `ROADMAP.md` / CHANGELOG ciclo `0.4.3.dev0`
- [x] DOC-006: DT-0006 en piloto D; IDE-0007 MVP local (+ checklist eval)
- [x] UAT plataforma marcado OK (`uat/plataforma/CHECKLIST.md`)

## Resultado (rellenar al ejecutar)

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 1 Automatizado |  |  |
| 2 Studio |  |  |
| 3 Docs / deuda |  | Ciclo 0.4.3.dev0 |

**Veredicto:** [ ] OK demo · [ ] Con reservas · [ ] Bloqueante
