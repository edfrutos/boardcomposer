# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#919` (IDE-0232) cierra ola 51; cola vacía +
Issues = 0 → **abre quincuagésima segunda ola IDE-0233…0234** (copy/clic
de `relp.`/`asav`, simetría de ola 50 sobre `rela.`).
Tip `main` post-`#919` = `301c14cb`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `REVIEW-2026-11-20-planificacion.md`, PRs
`#915`…`#919`.
**Issues GitHub:** vacío.
**Planning previo:** `#914` / `REVIEW-2026-11-20` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0232 (status QoL, retales, relaciones de forma…) | 🟢 en `main` |
| IDE-0229…0232 ola 51 amplitud / media de relaciones | 🟢 (#915…#919) |
| IDE-0233 copiar la relación de forma media de retales | 🟢 (esta entrega) |
| IDE-0234 clic en la relación de forma media selecciona su solución | 🔵 |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 51 **cerrada**. Ola 52 **abierta** (0233…0234).
Criterio del cron (*proponer si cola vacía y bugs cerrados*) → **sí**:
copy/clic de `relp.` (previsto en REVIEW-2026-11-20 §6).

---

## 3. Siguientes pasos

1. **Cola `0.4.5` ola 52** — IDE-0233 (copiar; Ctrl+Alt+Shift+?); luego
   IDE-0234 (clic → `solution:{index}`).
2. Piloto DT-0006 D; gate release; ops MAS paralelo.
3. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0233 | Copiar la relación de forma media de retales | Simetría de 0227 sobre `relp.`/`asav` |
| IDE-0234 | Clic en la relación de forma media selecciona su solución | Cierra el trío; simetría de 0228 |

Prioridad: **IDE-0233** → 0234.

| ID | Título | Estado |
|----|--------|--------|
| IDE-0233 | Copiar la relación de forma media de retales | 🟢 |
| IDE-0234 | Clic en la relación de forma media selecciona su solución | 🔵 |

Contrato (0233): Cmd+Alt+Shift+? copia el valor sin `relp.` (EN sin `asav`);
deshabilitado si etiqueta oculta; no avanza.

Contrato (0234): clic → `solution:{index}`; arrastre no; cursor mano.

Si 0233…0234 mergean y cola vacía → proponer ola 53 (otra métrica de forma
o coste cuando haya datos).
