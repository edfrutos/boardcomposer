# Release / demo smoke — BoardComposer

**Versión:** `0.4.3`  
**Fecha:** 2026-09-14  
**Base:** `main` @ release `0.4.3`

Checklist corta para validar «listo para demo / uso diario» sin sustituir UAT
completo (`uat/studio/`, `uat/plataforma/`).

---

## 1. Automatizado

- [x] `make check` (project check + ruff + pytest) → OK
- [x] `make demo` → sale con layout / JSON sin crash
- [x] Cubierto por `make check` (`test_batch` + `test_http_api`)

## 2. Studio (manual ligero, 5–10 min)

- [ ] `make run` → Welcome / About muestran `0.4.3`
- [ ] Nuevo demo → calcular layout → Comparador → **Ctrl+Alt+E** Explicar candidata → Copiar
  (eval 5 candidatas: [`studio/CHECKLIST-EXPLAIN-EVAL.md`](studio/CHECKLIST-EXPLAIN-EVAL.md))
- [ ] **Ctrl+Alt+M** metadatos; **Ctrl+Alt+K** kerf; pieza con veta fija no rota (**R**)
- [ ] Dos piezas colocadas → **Ctrl+Alt+X** intercambia; **Ctrl+Alt+C** lista de corte CSV/PDF
- [ ] Editar pieza tras calcular → banner desactualizadas + CTA **Calcular layout**;
  Aplicar/Exportar muestran diálogo recalcular / continuar / cancelar
- [ ] Proyecto guardado → **Ctrl+Alt+B** Exportar backup → Abrir carpeta (o CLI `boardcomposer-backup`)
- [ ] Restore: guardar 2× → Ctrl+Alt+Y → confirm → dirty

## 3. Docs / deuda

- [x] `ROADMAP.md` / CHANGELOG 0.4.3
- [x] DOC-006: DT-0006 en piloto D; cola 0019…0024 cerrada
- [x] UAT plataforma marcado OK (`uat/plataforma/CHECKLIST.md`)

## Resultado (rellenar al ejecutar)

| Bloque | ¿OK? | Notas |
|--------|------|-------|
| 1 Automatizado | OK | 1182 passed; demo layout `free_space` |
| 2 Studio |  | Pendiente `make run` humano |
| 3 Docs / deuda | OK | Corte 0.4.3 |

**Veredicto:** [ ] OK demo · [ ] Con reservas · [ ] Bloqueante
