# Revisión de planificación — 2026-11-13

**Origen:** cron diario; corte tras `#897` (UAT smoke `0.4.4` OK) en `main`.
PRs de producto abiertos hacia `main`: **0** (solo docs ops `#898`
macOS App Store — fuera de cola IDE). Issues abiertos: **0**.
Planning `#892` / `REVIEW-2026-11-12-planificacion.md` **mergeado**
(histórico; entonces ola 50 0227…0228 🔵 tip `#891` fuera de `main`;
ahora ola 50 🟢 vía `#893` + corte `0.4.4` + ciclo `0.4.5.dev0` `#894`).
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-11-12-planificacion.md`, PRs `#892`…`#898`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#893` (IDE-0227/0228 + corte `0.4.4`),
`#894` (`0.4.5.dev0`), `#895` (fix Studio path/macOS tip), `#896`
(docs Cmd+), `#897` (UAT smoke OK) **mergeados** en `main`. `#898`
abierto (docs ops MAS; no cola IDE). Cola implementable residual en
`main`: **vacía**.
Residual diferido (no cola): IDE-0101/0102 ⚪ (sin costes).
Residual bloqueado: piloto DT-0006 D + IDE-0008 / LLM / DT-0006 C.
**Planning previo:** `#892` / `REVIEW-2026-11-12` queda histórico.

---

## 1. Funcionalidades (qué hay)

| Área | Estado |
|------|--------|
| Core 2D (modelos, geometría, pipeline, Skyline/MaxRects, Beam Search) | 🟢 Base Fase 1 |
| Multipanel MaxRects **y** Skyline (material + espesor, retales, parciales) | 🟢 (#623) |
| CP-SAT un panel (opcional) | 🟢 Explorado |
| Studio: Workspace, Inspector, comandos, persistencia `.bcproj` | 🟢 Núcleo usable |
| Comparador SCR-003, Timeline, Preferencias, Welcome | 🟢 |
| QoL tips honesty / Welcome / barra estado / Timeline (ciclo `0.4.3`) | 🟢 |
| IDE-0019…0228 (swap, kerf, grain, cut list, catalog, quote, status QoL…) | 🟢 en `main` |
| IDE-0223…0225 trío relación de forma retal área mediana (`reln.`/`aspm`) | 🟢 |
| IDE-0226…0228 trío relación de forma retal área media (`rela.`/`aspa`) | 🟢 (#890/#893) |
| IDE-0229 barra: amplitud de relaciones de forma de retales | 🔵 (nueva) |
| IDE-0230 copiar la amplitud de relaciones de forma de retales | 🔵 (nueva) |
| IDE-0231 clic en la amplitud de relaciones de forma selecciona su solución | 🔵 (nueva) |
| IDE-0232 barra: relación de forma media de retales | 🔵 (nueva) |
| IDE-0101 barra: coste de la solución seleccionada | ⚪ Diferido (sin costes) |
| IDE-0102 copiar el coste de la solución | ⚪ Diferido (sin costes) |
| Import CSV/Excel; export SVG/DXF/PDF/JSON/CSV + plantillas | 🟢 |
| Fase 3: EP-001 API `v1`, EP-002 batch, EP-003 HTTP/Docker | 🟢 Entregada |
| IDE-0007 explicación local (sin LLM) | 🟢 MVP + eval humana (2026-09-12) |
| IDE-0008 plugins | ⚪ Visión Fase 5 |
| DT-0006 historial cloud | 🟡 Piloto D (backup); C diferida |

Detalle de ideas: `DOC-004-Backlog.md`.

---

## 2. Planificación de construcción

| Fase | Estado | Notas |
|------|--------|-------|
| 0 Fundamentos | 🟢 | Repo, CI, ADR |
| 1 Core 2D | 🟢 Base | Extensiones controladas (kerf, grain, Skyline MP, freeze) |
| 2 Studio | 🟡 En curso | Núcleo usable; pulido continuo |
| 3 Plataforma | 🟢 | EP-001…003 cerradas (corte 2026-07) |
| 4 Inteligencia | ⚪ | IDE-0007 MVP+eval; LLM bajo política |
| 5 Ecosistema | ⚪ | Plugins / marketplace |

Versión: desarrollo `0.4.5.dev0` · estable `0.4.4` (2026-11-12;
etiqueta `v0.4.4` **publicada**). Smoke UAT humano `0.4.4` OK (`#897`).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; cola
producto IDE-0019…0024 **cerrada** en `0.4.3`; olas `0.4.4` 0025…0228
**cerradas** en `main` (`#631`…`#893`; IDE-0101/0102 diferidas ⚪).
Quincuagésima ola 0227…0228 **cerrada** (`#893`) con corte `0.4.4`.
Ciclo `0.4.5.dev0` **abierto** (`#894`). Quincuagésima primera ola
0229…0232 **abierta por planning** (🔵).

Desde la revisión 2026-11-12 (PR `#892`, mergeado): mergeados `#893`/
`#894`/`#895`/`#896`/`#897`. Issues = 0. PRs producto a `main` = 0.
Criterio del cron **cumplido** → **sí se proponen IDE-0229…0232**
(primera ola del ciclo `0.4.5.dev0`; simetría post-aspectos → amplitud
de relaciones + media de relaciones).

Límites conocidos (no son bugs; son alcance):

- Retales se reportan (ADR-016) y se pueden promover a inventario del
  mismo `.bcproj` (IDE-0025); no hay librería de retales entre proyectos.
- CP-SAT exacto sigue siendo un solo panel (opcional).
- DT-0006 C (API revisiones + ACL) bloqueada hasta demanda multi-usuario.
- Catálogo de usuario (IDE-0028/0031) guarda nombre / espesor / €/m² /
  L×A; export/import JSON (IDE-0042 `#655`). Sin nube.
- Etiquetas de plano cubren piezas (IDE-0026), retales LxW (IDE-0033) y
  cotas L×A del tablero (IDE-0037) y pie de trazabilidad (IDE-0039);
  lista de corte / presupuesto PDF (IDE-0043). Etiquetas de plano siguen
  `prefs.units` (IDE-0044); geometría / JSON / `$INSUNITS` en mm.
- Coste (IDE-0029) y presupuesto PDF (IDE-0032) cubren material de
  tableros físicos; mano de obra opcional (IDE-0045 `#659`) vía EUR/h y
  minutos/pieza en Preferencias. Sigue sin herrajes. Coste *por
  solución* en barra (IDE-0101/0102) diferido.
- Export PDF: papel/márgenes/escala en plano (IDE-0034); lote de
  candidatas Studio (IDE-0035). Raster PNG/JPEG: DPI y calidad JPEG
  (IDE-0038). Capas DXF por rol (IDE-0041 `#654`). Sin nube.
- Workspace: sugerir hueco (IDE-0036); preview al terminar solve
  (IDE-0052); zoom 100% / clic zoom (IDE-0056/0062); copiar zoom
  (IDE-0091).
- Barra de estado (SCR-005): colocadas/total, omitidas, selección, kerf,
  tableros físicos, espesor/material/aprovechamiento/libre del tablero
  enfocado, zoom, retales (`n ret.`, IDE-0092…0094), índice de solución
  (`1/2 sol.`, IDE-0095…0097), huecos internos (`hueco n%`, IDE-0098…
  0100), estrategia (`est. …`, IDE-0103…0105), piezas (`n pza`,
  IDE-0106…0108), omitidas de solución (`fuera n`, IDE-0109…0111),
  tableros de solución (`pan. n`, IDE-0112…0114), puntuación
  (`pts. …`, IDE-0115…0117), tablero libre (`sbr. …`, IDE-0118…0120),
  largo total (`lrg. …`, IDE-0121…0123), ancho total (`anc. …`,
  IDE-0124…0126), área usada (`ár. …`, IDE-0127…0129), área de retales
  (`retár. …`, IDE-0130…0132), área envolvente (`env. …`, IDE-0133…
  0135), área de huecos internos (`hueár. …`, IDE-0136…0138), área de
  tablero libre (`sbrár. …`, IDE-0139…0141), área de tableros consumidos
  (`panár. …`, IDE-0142…0144), aprovechamiento (`aprv. …`,
  IDE-0145…0147), piezas rotadas (`rot. …`, IDE-0148…0150), piezas sin
  rotar (`nrot. …`, IDE-0151…0153), porcentaje rotadas (`rot% …`,
  IDE-0154…0156), porcentaje sin rotar (`nrot% …`, IDE-0157…0159),
  aprovechamiento envolvente (`env% …`, IDE-0160…0162), porcentaje de
  retales (`ret% …`, IDE-0163…0165), puntuación de desperdicio
  (`ptsh. …`, IDE-0166…0168), puntuación de uso de material
  (`ptsu. …`, IDE-0169…0171), puntuación de cortes (`ptsc. …`,
  IDE-0172…0174), puntuación de regularidad (`ptsr. …`,
  IDE-0175…0177), puntuación de veta (`ptsv. …`, IDE-0178…0180),
  completitud (`comp. sí`/`comp. no`, IDE-0181…0183), área del mayor
  retal (`maxr.`/`maxo`, IDE-0184…0186 🟢), área del menor retal
  (`minr.`/`mino`, IDE-0187…0189 🟢), dimensiones del mayor retal
  (`maxd.`/`maxd`, IDE-0190…0192 🟢), dimensiones del menor retal
  (`mind.`/`mind`, IDE-0193…0195 🟢), área media (`medr.`/`avgo`,
  IDE-0196…0198 🟢), área mediana (`mdnr.`/`medo`, IDE-0199…0201 🟢),
  dimensiones del retal de área mediana (`mdnd.`/`medd`,
  IDE-0202…0204 🟢), dimensiones del retal de área media
  (`mdds.`/`avgd`, IDE-0205…0207 🟢), amplitud de áreas
  (`ampr.`/`spno`, IDE-0208…0210 🟢), cuota mayor/menor
  (`cmay.`/`cmen.`, IDE-0211…0216 🟢), relaciones de forma mayor /
  menor / mediana / media (`relr.`/`relm.`/`reln.`/`rela.`,
  IDE-0217…0228 🟢). Siguiente familia: amplitud de relaciones
  (`arel.`/`spna`) y media de relaciones (`relp.`/`asav`).
- Inspector: unidades prefs mm/cm/in; disco sigue mm. Prefs:
  export/import JSON; perfiles nombrados locales; sin nube.

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.5` quincuagésima primera ola** — implementar IDE-0229
   (barra: amplitud de relaciones de forma `arel.` / `spna`); luego
   IDE-0230 (copiar; Ctrl+Alt+Shift+/); IDE-0231 (clic →
   `solution:{index}`); IDE-0232 (barra: relación de forma media
   `relp.` / `asav`).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **Ops paralelo (no cola IDE)** — `#898` docs empaquetado macOS / MAS
   (seguimiento; no bloquea ola 51).
5. **No priorizar** IDE-0008 / LLM / DT-0006 C / IDE-0101–0102 sin ADR
   o decisión vigente (eval IDE-0007 ya cerrada; LLM sigue diferido
   DEC-0011; coste por solución diferido).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0227…0228: **cerrada** en `main` (`#893`; corte `0.4.4`). Ciclo
`0.4.5.dev0` abierto (`#894`). En cola (nueva): IDE-0229…0232 🔵
(quincuagésima primera ola). Diferidas (fuera de cola): IDE-0101/0102
⚪. Residual bloqueado: piloto DT-0006 D (operativo) + IDE-0008 / LLM /
DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → cola vacía + Issues = 0 →
**sí se proponen IDE-0229…0232**. Tras cerrar simetría 100% de
relaciones de forma por retal representante (mayor / menor / mediana /
media), la familia natural siguiente —paralela a `ampr.` tras áreas—
es la **amplitud** de relaciones y la **media** de relaciones (distinta
de `rela.`/`aspa` = forma del retal de área media).

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0229 | Barra: amplitud de relaciones de forma de retales | `arel.`/`spna` = max(aspect)−min(aspect); simetría de `ampr.` sobre forma |
| IDE-0230 | Copiar la amplitud de relaciones de forma de retales | Valor sin `arel.`; Ctrl+Alt+Shift+/ |
| IDE-0231 | Clic en la amplitud de relaciones de forma selecciona su solución | Click → `solution:{index}`; arrastre no; cierra trío |
| IDE-0232 | Barra: relación de forma media de retales | `relp.`/`asav` = media de aspectos; distinta de `rela.`/`aspa` |

Prioridad de ataque: **IDE-0229** → 0230 → 0231 → 0232.

Quincuagésima primera ola (no renumerar; **nueva / abierta**):

| ID | Título | Estado |
|----|--------|--------|
| IDE-0229 | Barra: amplitud de relaciones de forma de retales | 🔵 |
| IDE-0230 | Copiar la amplitud de relaciones de forma de retales | 🔵 |
| IDE-0231 | Clic en la amplitud de relaciones de forma selecciona su solución | 🔵 |
| IDE-0232 | Barra: relación de forma media de retales | 🔵 |

Contrato mínimo (0229):

- `arel. {value}` / `spna {value}` = maxᵢ(max(L,A)/min(L,A)) −
  minᵢ(max(L,A)/min(L,A)) sobre retales de la solución seleccionada.
- Oculta si no hay retales; con un retal muestra `0.00`.
- Distinta de `ampr.`, `relr.`, `relm.`, `reln.` y `rela.`.
- Sin unidades de Preferencias. Cursor flecha. Sin clic en el show.

Contrato mínimo (0232):

- `relp. {value}` / `asav {value}` = media aritmética de
  max(L,A)/min(L,A) de todos los retales.
- Distinta de `rela.`/`aspa` (forma del retal cuya área ≈ media).
- Oculta si no hay retales; `1.00` si todos cuadrados.

Olas ya cerradas en este ciclo (no renumerar):

| Ola | IDs | Estado |
|-----|-----|--------|
| Decimoctava…Quincuagésima | 0099…0228 (+ 0101/0102 diferidas) | 🟢 / ⚪ |
| Cuadragésima novena | 0223…0226 | 🟢 |
| Quincuagésima | 0227…0228 (+ corte `0.4.4`) | 🟢 |

Cerradas en ciclo `0.4.4` (en `main`): IDE-0025…0100, IDE-0103…0228.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).
Planificadas (ola 51 / `0.4.5.dev0`): IDE-0229…0232.

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; confirmar IDE-0227…0228 🟢 (`#893`) + corte
  `0.4.4` / `0.4.5.dev0`, y abrir IDE-0229…0232 🔵.
  `#892` / `REVIEW-2026-11-12` queda histórico.
- **Con IDE nuevas del cron:** cola vacía + Issues = 0; primera ola
  post-`0.4.4` anclada a simetría amplitud/media de relaciones.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0229…0232 mergean y la cola queda vacía → proponer
  continuación (copy/clic de `relp.` u otra métrica de forma).
