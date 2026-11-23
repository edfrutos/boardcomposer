# Revisión de planificación — 2026-11-23

**Origen:** cron diario; corte tras `#929` (IDE-0241) en `main`.
Tip `main` = `e5587768`. PR de producto abierto hacia `main`: **`#930`**
(IDE-0242; **no mergeado** → 🟡). Issues abiertos: **0**.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
`CHANGELOG` Unreleased, `docs/ops/MACOS-APP-STORE.md`, PRs `#915`…`#930`,
revisión `REVIEW-2026-11-21-planificacion.md`.
**Issues GitHub:** `is:issue is:open` → **vacío**.
**PRs al corte:** `#929` mergeado (0241 🟢); `#930` abierto (0242 🟡).
Cola implementable residual: **IDE-0242** (en vuelo) + **IDE-0243**
(planificada). Residual diferido: IDE-0101/0102 ⚪ (sin costes).
Residual bloqueado: piloto DT-0006 D + IDE-0008 / LLM / DT-0006 C.
**Planning previo:** `REVIEW-2026-11-21` queda histórico (abrió ola 55 /
0241).

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| Core 2D + multipanel MaxRects/Skyline + CP-SAT un panel | 🟢 |
| Studio núcleo (Workspace, Inspector, Comparador, Timeline, prefs) | 🟢 usable |
| IDE-0019…0241 (QoL barra estado / retales / relaciones de forma…) | 🟢 en `main` |
| IDE-0238…0240 ola 54 desviación típica `drel.`/`sdas` | 🟢 (#926…#928) |
| IDE-0241 barra: media geométrica `grel.`/`gmas` | 🟢 (#929) |
| IDE-0242 copiar media geométrica (Cmd+Alt+Shift+\|) | 🟡 (#930 abierto) |
| IDE-0243 clic en media geométrica selecciona solución | 🔵 residual ola 55 |
| IDE-0101 / IDE-0102 coste por solución | ⚪ Diferido (sin costes) |
| Fase 3 EP-001…003 | 🟢 |
| IDE-0007 MVP+eval | 🟢; LLM diferido |
| IDE-0008 plugins | ⚪ bloqueado |
| DT-0006 historial cloud | 🟡 Piloto D; C diferida |
| MAS `0.4.4` / TestFlight build 46 | 🟡 Review respondida 16 nov; esperando Apple |

Detalle: `DOC-004-Backlog.md`.

---

## 2. Planificación de construcción

| Fase | Estado | Notas |
|------|--------|-------|
| 0 Fundamentos | 🟢 | Repo, CI, ADR |
| 1 Core 2D | 🟢 Base | Extensiones controladas |
| 2 Studio | 🟡 En curso | Núcleo usable; ola 55 abierta |
| 3 Plataforma | 🟢 | EP-001…003 |
| 4 Inteligencia | ⚪ | IDE-0007 MVP+eval; LLM bajo política |
| 5 Ecosistema | ⚪ | Plugins / marketplace |

Versión: desarrollo `0.4.5.dev0` · estable `0.4.4` (`v0.4.4` publicada
2026-11-12).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel. No es
greenfield: plataforma entregada; olas `0.4.4` hasta 0228 cerradas;
ciclo `0.4.5.dev0` abierto; olas 51–54 cerradas; **ola 55 abierta**
(0241 🟢 en `main`; 0242 🟡 en `#930`; 0243 🔵).

Criterio del cron (*proponer solo si cola vacía y bugs cerrados*) →
**no se proponen IDE nuevas**: residual implementable =
IDE-0242 + IDE-0243.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Bugs
GitHub abiertos: **0**.

---

## 4. Siguientes pasos (orden)

1. **Ola 55** — merge `#930` (IDE-0242 copy); luego IDE-0243 (clic →
   `solution:{index}`; arrastre no; no avanza).
2. **Piloto DT-0006 D** — runbook `docs/ops/PILOT-DT-0006-backup.md`.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **Ops MAS** — Resolution Center / App Store Connect; **no reenviar**;
   esperar Apple (fuera de cola IDE).
5. **No priorizar** IDE-0008 / LLM / DT-0006 C / IDE-0101–0102.

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Cola implementable: **no vacía** → **sin IDE
nuevas**. Se reafirma ola 55 existente (no renumerar).

| ID | Título | Estado |
|----|--------|--------|
| IDE-0241 | Barra: media geométrica de relaciones de forma de retales | 🟢 (#929) |
| IDE-0242 | Copiar la media geométrica de relaciones de forma de retales | 🟡 (#930) |
| IDE-0243 | Clic en la media geométrica de relaciones de forma selecciona su solución | 🔵 |

Contrato: `grel.`/`gmas` = `geometric_mean` de aspectos; distinta de
`arel.`, `relp.`, `mrel.`, `drel.`; oculta sin retales; copy
Ctrl+Alt+Shift+\| (valor sin prefijo); clic selecciona sin avanzar.

Prioridad de ataque: **IDE-0242** → **IDE-0243**.

---

## 6. Ops paralelo (no cola IDE)

- TestFlight `0.4.4` build **46**.
- App Review Guidelines 4.3 / 4.2.6 respondida 2026-11-16; esperando Apple.
- Docs: `docs/ops/MACOS-APP-STORE.md`.
