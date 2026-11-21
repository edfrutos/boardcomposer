# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#922` (IDE-0235) abre show de ola 53; esta
entrega (IDE-0236) añade copy de `mrel.`/`mdas`. Residual IDE-0237
(clic). Tip `main` post-`#922` = `1d0fd841`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#922`.
**Issues GitHub:** vacío.
**Planning previo:** `#914` / `REVIEW-2026-11-20` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0235 (status QoL, retales, relaciones de forma…) | 🟢 en `main` |
| IDE-0235…0237 ola 53 mediana de relaciones `mrel.`/`mdas` | 0235–0236 🟢; 0237 🔵 |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review 4.3/4.2.6 respondida 16 nov; esperando Apple |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 53 **abierta** (0235…0237). Ops paralelo (no
cola IDE): App Store Connect — respuesta Guidelines 4.3 / 4.2.6 enviada
2026-11-16 (Submission `878b3b3b-…`); **no reenviar** app; esperar
Apple. Texto canónico en `docs/ops/MACOS-APP-STORE.md` §6.

---

## 3. Siguientes pasos

1. **Cola `0.4.5` ola 53** — IDE-0237 (clic → `solution:{index}`).
2. **Ops MAS** — monitorizar Resolution Center; si Apple pide más, no
   resubmit sin instrucción nueva; build 46 sigue en TestFlight.
3. Piloto DT-0006 D; gate release.
4. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Estado |
|----|--------|--------|
| IDE-0235 | Barra: mediana de relaciones de forma de retales | 🟢 |
| IDE-0236 | Copiar la mediana de relaciones de forma de retales | 🟢 (esta entrega) |
| IDE-0237 | Clic en la mediana de relaciones de forma selecciona su solución | 🔵 |

Contrato (0236): Cmd+Alt+Shift+{ copia el valor sin `mrel.` (EN sin
`mdas`); deshabilitado si etiqueta oculta; no avanza.

Contrato (0237): clic → `solution:{index}`; arrastre no; cursor mano.
