# Revisión de planificación — 2026-11-23

**Origen:** Merge OK de `#930` (IDE-0242); esta entrega (IDE-0243)
**cierra ola 55** (0241…0243). Tip `main` post-`#930` / `#931` =
`9c62c2c5`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#930`.
**Issues GitHub:** vacío.
**Planning previo:** cron `REVIEW-2026-11-23` (0242 abierto) queda
superseded por este cierre de ola.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0243 (status QoL, retales, relaciones de forma…) | 🟢 en `main` (+0243 esta) |
| IDE-0238…0240 ola 54 desviación típica `drel.`/`sdas` | 🟢 |
| IDE-0241…0243 ola 55 media geométrica `grel.`/`gmas` | 🟢 (#929…#930 + esta) |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review respondida 16 nov; esperando Apple |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 55 **cerrada**. Cola producto **vacía**.
Ops paralelo: App Review — **no reenviar**; esperar Apple (respuesta
Guidelines 4.3 / 4.2.6 enviada 2026-11-16; Submission ID
`878b3b3b-9b09-46e8-843f-1c60268f74a1`). Estado vivo solo en App Store
Connect (Resolution Center); sin API/sesión agent → verificar manual.

---

## 3. Siguientes pasos

1. **Cola `0.4.5` vacía** — tras merge de 0243, proponer ola 56
   (otra métrica de forma o coste cuando haya datos).
2. **Ops MAS** — Resolution Center; build 46 TestFlight; **no reenviar**.
3. Piloto DT-0006 D; gate release.
4. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Estado |
|----|--------|--------|
| IDE-0241 | Barra: media geométrica de relaciones de forma de retales | 🟢 |
| IDE-0242 | Copiar la media geométrica de relaciones de forma de retales | 🟢 |
| IDE-0243 | Clic en la media geométrica de relaciones de forma selecciona su solución | 🟢 (esta entrega) |

Contrato (0243): clic → `solution:{index}`; arrastre no; cursor mano;
no avanza ni aplica el layout.
