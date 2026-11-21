# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#924` (IDE-0236); esta entrega (IDE-0237)
**cierra ola 53** (0235…0237). Cola vacía → siguiente Merge OK abre
ola 54. Tip `main` post-`#924` = `47f9ef59`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#924`.
**Issues GitHub:** vacío.
**Planning previo:** `#914` / `REVIEW-2026-11-20` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0237 (status QoL, retales, relaciones de forma…) | 🟢 en `main` (0237 esta entrega) |
| IDE-0235…0237 ola 53 mediana de relaciones `mrel.`/`mdas` | 🟢 (#922…#924 + esta) |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review 4.3/4.2.6 respondida 16 nov; esperando Apple |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 53 **cerrada**. Cola producto **vacía**.
Ops paralelo: App Review — **no reenviar**; esperar Apple.

---

## 3. Siguientes pasos

1. **Cola `0.4.5` vacía** — tras merge de 0237, proponer ola 54
   (otra métrica de forma o coste cuando haya datos).
2. **Ops MAS** — monitorizar Resolution Center; build 46 en TestFlight.
3. Piloto DT-0006 D; gate release.
4. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Estado |
|----|--------|--------|
| IDE-0235 | Barra: mediana de relaciones de forma de retales | 🟢 |
| IDE-0236 | Copiar la mediana de relaciones de forma de retales | 🟢 |
| IDE-0237 | Clic en la mediana de relaciones de forma selecciona su solución | 🟢 (esta entrega) |

Contrato (0237): clic → `solution:{index}`; arrastre no; cursor mano;
no avanza ni aplica el layout.
