# Revisión de planificación — 2026-11-21

**Origen:** Merge OK de `#928` (IDE-0240 cierra ola 54); esta entrega
(IDE-0241) **abre ola 55** (0241…0243). Tip `main` post-`#928` =
`91943c45`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#928`.
**Issues GitHub:** vacío.
**Planning previo:** ola 54 / `REVIEW` de 0240 queda histórico en el mismo
fichero (actualizado).

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| IDE-0019…0240 (status QoL, retales, relaciones de forma…) | 🟢 en `main` |
| IDE-0238…0240 ola 54 desviación típica `drel.`/`sdas` | 🟢 (#926…#928) |
| IDE-0241…0243 ola 55 media geométrica `grel.`/`gmas` | 🟡 (0241 esta) |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| IDE-0008 plugins / LLM | ⚪ Bloqueados |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review respondida 16 nov; esperando Apple |

---

## 2. Situación

Ciclo `0.4.5.dev0`. Ola 54 **cerrada**. Ola 55 **abierta** (0241 show;
0242 copy; 0243 click). Ops paralelo: App Review — **no reenviar**;
esperar Apple.

---

## 3. Siguientes pasos

1. **Ola 55** — residuales copy (IDE-0242; Cmd+Alt+Shift+\|) y click
   (IDE-0243) tras merge de 0241.
2. **Ops MAS** — Resolution Center; build 46 TestFlight.
3. Piloto DT-0006 D; gate release.
4. No priorizar IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 4. Cola candidata

| ID | Título | Estado |
|----|--------|--------|
| IDE-0241 | Barra: media geométrica de relaciones de forma de retales | 🟡 (esta entrega) |
| IDE-0242 | Copiar la media geométrica de relaciones de forma de retales | ⚪ |
| IDE-0243 | Clic en la media geométrica de relaciones de forma selecciona su solución | ⚪ |

Contrato (0241): `grel.`/`gmas` = `geometric_mean` de aspectos; distinta
de `arel.`, `relp.`, `mrel.`, `drel.`; oculta sin retales; cursor flecha;
sin clic.
