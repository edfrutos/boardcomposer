# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#927` (IDE-0239); esta entrega (IDE-0240)
**cierra ola 54** (0238…0240). Cola vacía → siguiente Merge OK abre
ola 55. Tip `main` post-`#927` = `33e5b3e8`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#927`.
**Issues GitHub:** vacío.
**Planning previo:** `#914` / `REVIEW-2026-11-20` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0240 (status QoL, retales, relaciones de forma…) | 🟢 en `main` (0240 esta entrega) |
| IDE-0238…0240 ola 54 desviación típica `drel.`/`sdas` | 🟢 (#926…#927 + esta) |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review respondida 16 nov; esperando Apple |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 54 **cerrada**. Cola producto **vacía**.
Ops paralelo: App Review — **no reenviar**; esperar Apple.

---

## 3. Siguientes pasos

1. **Cola `0.4.5` vacía** — tras merge de 0240, proponer ola 55
   (otra métrica de forma o coste cuando haya datos).
2. **Ops MAS** — Resolution Center; build 46 TestFlight.
3. Piloto DT-0006 D; gate release.
4. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Estado |
|----|--------|--------|
| IDE-0238 | Barra: desviación típica de relaciones de forma de retales | 🟢 |
| IDE-0239 | Copiar la desviación típica de relaciones de forma de retales | 🟢 |
| IDE-0240 | Clic en la desviación típica de relaciones de forma selecciona su solución | 🟢 (esta entrega) |

Contrato (0240): clic → `solution:{index}`; arrastre no; cursor mano;
no avanza ni aplica el layout.
