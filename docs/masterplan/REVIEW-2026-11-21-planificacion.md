# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#925` (IDE-0237) cierra ola 53; cola vacía +
Issues = 0 → **abre quincuagésima cuarta ola IDE-0238…0240** (show/copy/clic
de la desviación típica de relaciones `drel.`/`sdas`; cierra el bloque
estadístico span / media / mediana / stddev sobre aspectos). Esta entrega
(IDE-0238) abre el show. Tip `main` post-`#925` = `8b6191aa`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#925`.
**Issues GitHub:** vacío.
**Planning previo:** `#914` / `REVIEW-2026-11-20` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0237 (status QoL, retales, relaciones de forma…) | 🟢 en `main` |
| IDE-0235…0237 ola 53 mediana de relaciones | 🟢 (#922…#925) |
| IDE-0238 desviación típica de relaciones de forma | 🟢 (esta entrega) |
| IDE-0239 / IDE-0240 copy/clic `drel.`/`sdas` | 🔵 |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review respondida 16 nov; esperando Apple |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 53 **cerrada**. Ola 54 **abierta** (0238…0240).
Ops paralelo: App Review — **no reenviar**; esperar Apple.

---

## 3. Siguientes pasos

1. **Cola `0.4.5` ola 54** — IDE-0239 (copiar; Ctrl+Alt+Shift+}); luego
   IDE-0240 (clic → `solution:{index}`).
2. **Ops MAS** — Resolution Center; build 46 TestFlight.
3. Piloto DT-0006 D; gate release.
4. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0238 | Barra: desviación típica de relaciones de forma | `drel.`/`sdas` = pstdev; cierra trío+stddev |
| IDE-0239 | Copiar la desviación típica de relaciones de forma | Valor sin `drel.`; Ctrl+Alt+Shift+} |
| IDE-0240 | Clic en la desviación típica selecciona su solución | Click → `solution:{index}`; cierra trío |

| ID | Título | Estado |
|----|--------|--------|
| IDE-0238 | Barra: desviación típica de relaciones de forma de retales | 🟢 (esta entrega) |
| IDE-0239 | Copiar la desviación típica de relaciones de forma de retales | 🔵 |
| IDE-0240 | Clic en la desviación típica de relaciones de forma selecciona su solución | 🔵 |

Contrato (0238):

- `drel. {value}` / `sdas {value}` = desviación típica poblacional
  (`statistics.pstdev`) de max(L,A)/min(L,A) de todos los retales.
- Distinta de `arel.`/`spna`, `relp.`/`asav` y `mrel.`/`mdas`.
- Oculta si no hay retales; con un retal muestra `0.00`.
- Sin unidades. Cursor flecha. Sin clic en el show.
