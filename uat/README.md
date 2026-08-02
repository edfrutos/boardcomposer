# UAT — BoardComposer

Pruebas humanas (y enlace a regresión automatizada).

| Checklist | Estado típico | Uso |
| --- | --- | --- |
| [`studio/CHECKLIST-VISUAL.md`](studio/CHECKLIST-VISUAL.md) | Cerrada 2026-07-28 | Pasada visual completa (+ huecos residuales cubiertos por test) |
| [`studio/CHECKLIST-FUNCIONAL.md`](studio/CHECKLIST-FUNCIONAL.md) | Marcada (histórico) | Funcionalidad Studio ya verificada |
| [`studio/CHECKLIST-EXPLAIN-EVAL.md`](studio/CHECKLIST-EXPLAIN-EVAL.md) | Pendiente humana | IDE-0007: 5 candidatas demo → útil vs ruido |
| [`multipanel/CHECKLIST.md`](multipanel/CHECKLIST.md) | Cerrada | Multipanel absorbido por Studio |
| [`plataforma/CHECKLIST.md`](plataforma/CHECKLIST.md) | OK operativo 2026-07-30 | Smoke batch+HTTP (+ 21 tests) |
| [`RELEASE-SMOKE.md`](RELEASE-SMOKE.md) | Activa | Gate corto demo / release `0.4.2` |

Arranque: `make run` o `.venv/bin/python -m studio.app`.

Regresión multi-candidata automatizada:
`tests/test_uat_multi_candidate_flow.py` (`make test`).

Docs usuario: [`../docs/user/GUIA-RAPIDA.md`](../docs/user/GUIA-RAPIDA.md).
