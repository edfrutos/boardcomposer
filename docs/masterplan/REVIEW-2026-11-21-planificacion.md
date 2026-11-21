# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#921` (IDE-0234) cierra ola 52; cola vacía +
Issues = 0 → **abre quincuagésima tercera ola IDE-0235…0237** (show/copy/clic
de la mediana de relaciones `mrel.`/`mdas`, simetría de `mdnr.` sobre forma;
distinta de `reln.` = forma del retal de área mediana). Esta entrega
(IDE-0235) abre el show. Tip `main` post-`#921` = `cafb906c`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `REVIEW-2026-11-20-planificacion.md`, PRs
`#915`…`#921`.
**Issues GitHub:** vacío.
**Planning previo:** `#914` / `REVIEW-2026-11-20` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0234 (status QoL, retales, relaciones de forma…) | 🟢 en `main` |
| IDE-0229…0232 ola 51 amplitud / media de relaciones | 🟢 (#915…#919) |
| IDE-0233…0234 ola 52 copy/clic `relp.`/`asav` | 🟢 (#920…#921) |
| IDE-0235 mediana de relaciones de forma de retales | 🟢 (esta entrega) |
| IDE-0236 / IDE-0237 copy/clic `mrel.`/`mdas` | 🔵 |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 51–52 **cerradas**. Ola 53 **abierta** (0235…0237).
Criterio del cron (*proponer si cola vacía y bugs cerrados*) → **sí**:
mediana de relaciones (cierra trío estadístico span / media / mediana
sobre aspectos).

---

## 3. Siguientes pasos

1. **Cola `0.4.5` ola 53** — IDE-0236 (copiar; Ctrl+Alt+Shift+{); luego
   IDE-0237 (clic → `solution:{index}`).
2. Piloto DT-0006 D; gate release; ops MAS paralelo.
3. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0235 | Barra: mediana de relaciones de forma de retales | `mrel.`/`mdas` = mediana de aspectos; simetría de `mdnr.` |
| IDE-0236 | Copiar la mediana de relaciones de forma de retales | Valor sin `mrel.`; Ctrl+Alt+Shift+{ |
| IDE-0237 | Clic en la mediana de relaciones de forma selecciona su solución | Click → `solution:{index}`; arrastre no; cierra trío |

Prioridad: **IDE-0235** → 0236 → 0237.

| ID | Título | Estado |
|----|--------|--------|
| IDE-0235 | Barra: mediana de relaciones de forma de retales | 🟢 (esta entrega) |
| IDE-0236 | Copiar la mediana de relaciones de forma de retales | 🔵 |
| IDE-0237 | Clic en la mediana de relaciones de forma selecciona su solución | 🔵 |

Contrato (0235):

- `mrel. {value}` / `mdas {value}` = mediana de max(L,A)/min(L,A)
  de todos los retales; n par → inferior de los dos centrales.
- Distinta de `reln.`/`aspm` (forma del retal de área mediana) y de
  `relp.`/`asav` (media aritmética de aspectos).
- Oculta si no hay retales; `1.00` si todos cuadrados.
- Sin unidades. Cursor flecha. Sin clic en el show.
