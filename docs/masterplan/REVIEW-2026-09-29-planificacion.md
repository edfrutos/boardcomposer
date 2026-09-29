# Revisión de planificación — 2026-09-29

**Origen:** cron diario; corte tras `#692` (IDE-0069) en `main`.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-09-28-planificacion.md`, PRs `#687`…`#693`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#687`…`#692` **mergeados** (IDE-0064…0069).
Abierto: `#693` (IDE-0070, CI verde). Residual: décima ola IDE-0070.
**Planning previo:** `#685` (2026-09-28) — histórico en `main`.

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
| IDE-0024 metadatos proyecto (cliente / ref. / notas; Ctrl+Alt+M; v3) | 🟢 (#617) |
| IDE-0019 intercambiar dos piezas colocadas (Ctrl+Alt+X) | 🟢 (#618) |
| IDE-0020 kerf / espesor de sierra (Ctrl+Alt+K; `.bcproj` v4) | 🟢 (#619) |
| IDE-0023 lista de corte / informe taller (Ctrl+Alt+C; CSV/PDF) | 🟢 (#621) |
| IDE-0021 veta / orientación de fibra (`.bcproj` v5; no rotar si fija) | 🟢 (#622) |
| IDE-0022 packing multipanel Skyline | 🟢 (#623) |
| IDE-0025 retales a inventario remnant (Ctrl+Alt+R; `.bcproj` v6) | 🟢 (#636) |
| IDE-0026 etiquetas de piezas en plano (SVG/PDF/DXF) | 🟢 (#631) |
| IDE-0027 secuencia de corte por panel | 🟢 (#632) |
| IDE-0030 congelar colocaciones / re-pack omitidas (Ctrl+Alt+F) | 🟢 (#634) |
| IDE-0028 catálogo materiales / espesores (Ctrl+Alt+T) | 🟢 (#637) |
| IDE-0029 coste estimado de material (€/m² catálogo) | 🟢 (#638) |
| IDE-0031 medidas típicas de tablero en catálogo (L×A) | 🟢 (#640) |
| IDE-0032 presupuesto de material PDF (Ctrl+Alt+Q) | 🟢 (#642) |
| IDE-0033 etiquetas de retales en plano (LxW SVG/PDF/DXF) | 🟢 (#641) |
| IDE-0034 papel / márgenes / escala en PDF de plano | 🟢 (#643) |
| IDE-0035 exportar soluciones en lote | 🟢 (#644) |
| IDE-0036 colocación manual asistida (sugerir hueco) | 🟢 (#645) |
| IDE-0037 cotas L×A del tablero en plano | 🟢 (#647) |
| IDE-0038 calidad raster PNG/JPEG (DPI) | 🟢 (#649) |
| IDE-0039 trazabilidad en plano (versión, algoritmo, fecha) | 🟢 (#651) |
| IDE-0040 unidades Inspector (mm/cm/in) | 🟢 (#653) |
| IDE-0041 capas DXF por rol (marco/pieza/retal/cota) | 🟢 (#654) |
| IDE-0042 exportar/importar catálogo de materiales | 🟢 (#655) |
| IDE-0043 trazabilidad lista de corte / presupuesto PDF | 🟢 (#657) |
| IDE-0044 unidades prefs en plano / etiquetas export | 🟢 (#658) |
| IDE-0045 mano de obra en presupuesto | 🟢 (#659) |
| IDE-0046 Inspector espesor / rotación / veta de pieza | 🟢 (#661) |
| IDE-0047 unidades prefs en Comparador | 🟢 (#662) |
| IDE-0048 unidades prefs en lista de corte / presupuesto | 🟢 (#663) |
| IDE-0049 exportar/importar preferencias JSON | 🟢 (#664) |
| IDE-0050 Inspector resumen rico proyecto/categoría | 🟢 (#665) |
| IDE-0051 Inspector aprovechamiento de tablero | 🟢 (#666) |
| IDE-0052 preview canvas al terminar el solve | 🟢 (#667) |
| IDE-0053 material por defecto de taller | 🟢 (#671) |
| IDE-0054 perfiles nombrados de preferencias | 🟢 (#672) |
| IDE-0055 Inspector área de la pieza | 🟢 (#673) |
| IDE-0056 zoom del Workspace al 100% | 🟢 (#675) |
| IDE-0057 copiar texto del Inspector | 🟢 (#676) |
| IDE-0058 marca sin guardar en la barra de ruta | 🟢 (#678) |
| IDE-0059 Inspector área de una hoja de tablero | 🟢 (#680) |
| IDE-0060 barra de estado piezas colocadas / total | 🟢 (#682) |
| IDE-0061 copiar ruta del `.bcproj` | 🟢 (#683) |
| IDE-0062 clic en el zoom vuelve al 100% | 🟢 (#684) |
| IDE-0063 barra de estado piezas seleccionadas | 🟢 (#686) |
| IDE-0064 copiar medidas de la pieza seleccionada | 🟢 (#687) |
| IDE-0065 barra de estado kerf del proyecto | 🟢 (#688) |
| IDE-0066 clic en la selección ajusta el encuadre | 🟢 (#689) |
| IDE-0067 clic en el kerf abre el espesor de sierra | 🟢 (#690) |
| IDE-0068 copiar medidas L×A del tablero | 🟢 (#691) |
| IDE-0069 barra de estado tableros físicos | 🟢 (#692) |
| IDE-0070 clic en colocadas/total encuadra las colocadas | 🟡 (#693) |
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

Versión: desarrollo `0.4.4.dev0` · estable `0.4.3` (2026-09-14;
etiqueta `v0.4.3` **publicada** 2026-09-16 — latest GitHub Releases).

---

## 3. Situación de creación

Producto **operativo** para flujo diario de corte 2D multipanel en Studio, con
CLI, batch e HTTP de referencia. No es greenfield: plataforma entregada; cola
producto IDE-0019…0024 **cerrada** en `0.4.3`; primera ola `0.4.4.dev0`
(0025…0030) **cerrada**; segunda ola 0031…0036 **cerrada** (`#640`…`#645`);
IDE-0037…0069 **entregadas** (`#647`…`#667`, `#671`…`#673`, `#675`, `#676`,
`#678`, `#680`, `#682`…`#692`); octava ola 0059…0062 cerrada; novena ola
0063…0066 cerrada; décima ola 0067…0070 abierta (queda IDE-0070 🟡 `#693`).

Desde la revisión 2026-09-28, planning `#685` entra en `main` como histórico.
Producto `#687`…`#692` (IDE-0064…0069) en `main`. PR de producto abierto:
`#693` (IDE-0070).

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
  minutos/pieza en Preferencias. Sigue sin herrajes.
- Export PDF: papel/márgenes/escala en plano (IDE-0034); lote de
  candidatas Studio (IDE-0035). Raster PNG/JPEG: DPI y calidad JPEG
  (IDE-0038). Capas DXF por rol (IDE-0041 `#654`). Sin nube.
- Workspace: sugerir hueco para colocación manual (IDE-0036; SCR-002).
  Preview canvas al terminar Calcular layout, sin aplicar placements
  (IDE-0052 `#667`). Zoom al 100% (**Ctrl+Alt+0**, IDE-0056 `#675`).
  Clic en la etiqueta de zoom → 100%: entregado (`#684`, IDE-0062).
  Barra de estado, piezas seleccionadas: entregado (`#686`, IDE-0063).
  Copiar medidas L×A de una pieza: entregado (`#687`, IDE-0064;
  Ctrl+Alt+Shift+D).
  Copiar medidas L×A de un tablero: entregado (`#691`, IDE-0068;
  Ctrl+Alt+Shift+B).
  Barra de estado, tableros físicos: entregado (`#692`, IDE-0069;
  suma de cantidades; sin clic).
  Barra de estado, kerf del proyecto: entregado (`#688`, IDE-0065).
  Clic en `n sel.` ajusta el encuadre: entregado (`#689`, IDE-0066).
  Novena ola cerrada.
  Clic en el kerf abre el espesor de sierra: entregado (`#690`, IDE-0067).
  Clic en colocadas/total encuadra colocadas: en desarrollo (`#693`,
  IDE-0070).
- Inspector: unidades prefs mm/cm/in (IDE-0040 `#653`); disco sigue mm.
  Pieza muestra espesor, rotación 0°/90° (— si no colocada), veta
  (IDE-0046 `#661`) y área L×A (IDE-0055 `#673`). Comparador Largo/Ancho
  y diffs (IDE-0047 `#662`). Lista de corte / presupuesto PDF TEXT siguen
  `prefs.units` (IDE-0048); CSV/JSON y área m² siguen mm.
  Prefs: export/import JSON de taller (IDE-0049 `#664`); perfiles
  nombrados locales (IDE-0054 `#672`); sin rutas locales ni ventana.
  Inspector de raíz/categoría: conteos, materiales y área (IDE-0050
  `#665`). Tablero: aprovechamiento (IDE-0051 `#666`) y área de una hoja
  (IDE-0059 `#680`). Material por defecto de taller (IDE-0053 `#671`);
  no va en el `.bcproj`. Copiar texto del Inspector: entregado (`#676`,
  IDE-0057; Ctrl+Alt+I). Marca sin guardar en barra de ruta: entregado
  (`#678`, IDE-0058). Barra de estado: piezas colocadas / total
  (`#682`, IDE-0060). Copiar ruta del `.bcproj`: entregado (`#683`,
  IDE-0061; Ctrl+Alt+Shift+C).

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4` décima ola** — IDE-0070 🟡 `#693` (0069 entregada
   `#692`; queda 0070).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0064…0069: **cerrada** en `main` (`#687`…`#692`). Residual abierto:
IDE-0070 🟡 `#693`. Residual bloqueado: piloto DT-0006 D (operativo) +
IDE-0008 / LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → décima ola residual IDE-0070
abierta; **no se añaden IDE nuevas** hasta cerrarla.

Octava…décima ola ya registradas (no renumerar):

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0059 | Inspector: área de una hoja de tablero | Entregado (`#680`) |
| IDE-0060 | Barra de estado: piezas colocadas / total | Entregado (`#682`) |
| IDE-0061 | Copiar ruta del `.bcproj` | Entregado (`#683`) |
| IDE-0062 | Clic en el zoom vuelve al 100% | Entregado (`#684`) |
| IDE-0063 | Barra de estado: piezas seleccionadas | Entregado (`#686`) |
| IDE-0064 | Copiar medidas de la pieza seleccionada | Entregado (`#687`) |
| IDE-0065 | Barra de estado: kerf del proyecto | Entregado (`#688`) |
| IDE-0066 | Clic en la selección ajusta el encuadre | Entregado (`#689`) |
| IDE-0067 | Clic en el kerf abre el espesor de sierra | Entregado (`#690`) |
| IDE-0068 | Copiar medidas L×A del tablero | Entregado (`#691`) |
| IDE-0069 | Barra de estado: tableros físicos | Entregado (`#692`) |
| IDE-0070 | Clic en colocadas/total encuadra las piezas colocadas | En desarrollo (`#693`) |

Prioridad de ataque: **IDE-0070** (clic en colocadas/total → encuadrar
colocadas; CI verde en `#693`).

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0069.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; registrar IDE-0069 🟢 (`#692`) e IDE-0070 🟡
  (`#693`, no 🟢). `#685` / `REVIEW-2026-09-28` queda histórico.
  Residual: IDE-0070.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
  Si IDE-0070 mergea y la cola queda vacía → proponer nueva ola IDE.
