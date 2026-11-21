# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#919` (IDE-0232) cierra ola 51; cola vacía +
Issues = 0 → **abre quincuagésima segunda ola IDE-0233…0234** (copy/clic
de `relp.`/`asav`, simetría de ola 50 sobre `rela.`). Esta entrega
(IDE-0234) **cierra ola 52**. Tip `main` post-`#920` = `49da8625`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `REVIEW-2026-11-20-planificacion.md`, PRs
`#915`…`#920`.
**Issues GitHub:** vacío.
**Planning previo:** `#914` / `REVIEW-2026-11-20` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0234 (status QoL, retales, relaciones de forma…) | 🟢 en `main` (0234 esta entrega) |
| IDE-0229…0232 ola 51 amplitud / media de relaciones | 🟢 (#915…#919) |
| IDE-0233…0234 ola 52 copy/clic `relp.`/`asav` | 🟢 (#920 + esta) |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 51 **cerrada**. Ola 52 **cerrada** (0233…0234).
Cola producto **vacía**. Criterio del cron (*proponer si cola vacía y
bugs cerrados*) → siguiente **Merge OK** abre ola 53.

---

## 3. Siguientes pasos

1. **Cola `0.4.5` vacía** — tras merge de 0234, proponer ola 53
   (otra métrica de forma o coste cuando haya datos).
2. Piloto DT-0006 D; gate release; ops MAS paralelo.
3. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Por qué ahora |
|----|--------|---------------|
| — | Cola vacía | Ola 52 cerrada; siguiente Merge OK abre ola 53 |

| ID | Título | Estado |
|----|--------|--------|
| IDE-0233 | Copiar la relación de forma media de retales | 🟢 |
| IDE-0234 | Clic en la relación de forma media selecciona su solución | 🟢 (esta entrega) |

Contrato (0234): clic → `solution:{index}`; arrastre no; cursor mano;
no avanza ni aplica el layout.
