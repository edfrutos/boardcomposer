# Revisión de planificación — 2026-11-23

**Origen:** Merge OK de `#934` (IDE-0245); esta entrega (IDE-0246,
2026-11-24) **cierra ola 56** (0244…0246). Tip `main` post-`#934` =
`b762e4e4`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#934`.
**Issues GitHub:** vacío.
**Planning previo:** cierre de ola 55 (0243) queda histórico en el mismo
fichero (actualizado).

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0243 (status QoL, retales, relaciones de forma…) | 🟢 en `main` |
| IDE-0238…0240 ola 54 desviación típica `drel.`/`sdas` | 🟢 |
| IDE-0241…0243 ola 55 media geométrica `grel.`/`gmas` | 🟢 (#929, #930, #932) |
| IDE-0244…0246 ola 56 relación de forma máxima `xrel.`/`mxas` | 🟢 (#933, #934 + esta) |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review respondida 16 nov; esperando Apple |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 56 **cerrada**. Cola producto **vacía**.
Ops paralelo: App Review — **no reenviar**; esperar Apple (respuesta
Guidelines 4.3 / 4.2.6 enviada 2026-11-16; Submission ID
`878b3b3b-9b09-46e8-843f-1c60268f74a1`). Estado vivo solo en App Store
Connect (Resolution Center); sin API/sesión agent → verificar manual.

---

## 3. Siguientes pasos

1. **Cola `0.4.5` vacía** — decidir panel que agrupe métricas antes de
   abrir ola 57; no añadir otra métrica a la barra.
2. **Ops MAS** — Resolution Center; build 46 TestFlight; **no reenviar**.
3. Piloto DT-0006 D; gate release.
4. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Estado |
|----|--------|--------|
| IDE-0244 | Barra: relación de forma máxima de retales | 🟢 |
| IDE-0245 | Copiar la relación de forma máxima de retales | 🟢 |
| IDE-0246 | Clic en la relación de forma máxima selecciona su solución | 🟢 (esta entrega) |

Contrato (0244): `xrel.`/`mxas` = máximo de aspectos; distinta de
`relr.` (retal de mayor área) y `arel.` (amplitud); oculta sin retales.

Contrato (0245): copia el valor sin `xrel.`; deshabilitado si la etiqueta
está oculta; no avanza.

Contrato (0246): clic → `solution:{index}`; arrastre no; cursor mano;
no avanza ni aplica el layout.

Decisión (0245, 2026-11-24): acción solo en el menú, sin atajo;
**Cmd+Alt+Shift+** agotado en letras, dígitos y F1–F12.
