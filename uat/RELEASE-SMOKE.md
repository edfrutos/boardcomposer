# Release / demo smoke — BoardComposer

**Versión:** `0.4.4`  
**Fecha:** 2026-11-11  
**Base:** `main` @ release `0.4.4`

Checklist corta para validar «listo para demo / uso diario» sin sustituir UAT
completo (`uat/studio/`, `uat/plataforma/`).

> **Atajos en macOS:** **Cmd** = **⌘** (Command), **Alt** = **⌥** (Option), **Shift** = **⇧** (en Windows/Linux, **Cmd** equivale a **Ctrl**).

---

## 1. Automatizado

- [x] `make check` (project check + ruff + pytest) → OK
- [x] `make demo` → sale con layout / JSON sin crash
- [x] Cubierto por `make check` (`test_batch` + `test_http_api`)

## 2. Studio (manual ligero, 5–10 min)

- [x] `make run` → Welcome / About muestran `0.4.4`
- [x] Nuevo demo → calcular layout → Comparador → **Cmd+Alt+E** Explicar candidata → Copiar
  (eval 5 candidatas: [`studio/CHECKLIST-EXPLAIN-EVAL.md`](studio/CHECKLIST-EXPLAIN-EVAL.md))
- [x] **Cmd+Alt+M** metadatos; **Cmd+Alt+K** kerf; pieza con veta fija no rota (**R**)
- [x] Dos piezas colocadas → **Cmd+Alt+X** intercambia; **Cmd+Alt+C** lista de corte CSV/PDF
- [x] Editar pieza tras calcular → banner desactualizadas + CTA **Calcular layout**;
  Aplicar/Exportar muestran diálogo recalcular / continuar / cancelar
- [x] Proyecto guardado → **Cmd+Alt+B** Exportar backup → Abrir carpeta (o CLI `boardcomposer-backup`)
- [x] Restore: guardar 2× → Cmd+Alt+Y → confirm → dirty

## 3. Docs / deuda

- [x] `ROADMAP.md` / CHANGELOG 0.4.4
- [x] DOC-006: DT-0006 en piloto D; cola 0025…0228 cerrada
- [x] UAT plataforma marcado OK (`uat/plataforma/CHECKLIST.md`)

## Resultado (rellenar al ejecutar)

| Bloque | ¿OK? | Notas |
| -------- | ------ | ------- |
| 1 Automatizado | OK | Suite verde; demo layout `free_space` |
| 2 Studio | OK | Verificación humana OK en macOS (`make run`) |
| 3 Docs / deuda | OK | Corte 0.4.4 |

**Veredicto:** [x] OK demo · [ ] Con reservas · [ ] Bloqueante
