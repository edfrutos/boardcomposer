# Revisión de planificación — 2026-09-26

**Origen:** cron diario; cola implementable residual tras `#676`
(IDE-0057). Confirmar siguiente foco sin abrir IDE nuevas antes de 0058.
**Fuentes:** `ROADMAP.md`, `MASTERPLAN.md`, `DOC-003`, `DOC-004`, `DOC-006`,
spikes IDE-0007 / DT-0006, `CHANGELOG` Unreleased, UAT release smoke,
revisión `REVIEW-2026-09-25-planificacion.md`, merge de `#676`.
**Issues GitHub:** `gh issue list --state open` → **vacío**.
**PRs de producto al corte:** `#673` **mergeado** (IDE-0055); `#675`
**mergeado** (IDE-0056); `#676` **mergeado** (IDE-0057 copiar Inspector).
**Planning previo:** `#674` (2026-09-25) — histórico en `main`.

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
| IDE-0057 copiar texto del Inspector | 🟢 (`#676`) |
| IDE-0058 marca sin guardar en la barra de ruta | 🟢 |
| IDE-0059 Inspector área de una hoja de tablero | 🟢 |
| IDE-0060 barra de estado piezas colocadas / total | 🟢 |
| IDE-0061 copiar ruta del .bcproj | 🟢 |
| IDE-0062 clic en el zoom vuelve al 100% | 🟢 |
| IDE-0063 barra de estado piezas seleccionadas | 🟢 |
| IDE-0064 copiar medidas de la pieza seleccionada | 🟢 |
| IDE-0065 barra de estado kerf del proyecto | 🟢 |
| IDE-0066 clic en la selección ajusta el encuadre | 🟢 |
| IDE-0067 clic en el kerf abre el espesor de sierra | 🟢 |
| IDE-0068 copiar medidas L×A del tablero | 🟢 |
| IDE-0069 barra de estado tableros físicos | 🟢 |
| IDE-0070 clic en colocadas/total encuadra las colocadas | 🟢 |
| IDE-0071 clic en tableros físicos encuadra todos | 🟢 |
| IDE-0072 copiar el kerf del proyecto | 🟢 |
| IDE-0073 barra de estado: espesor del tablero enfocado | 🟢 |
| IDE-0074 clic en el espesor abre la edición | 🟢 |
| IDE-0075 copiar espesor del tablero de la barra | 🟢 |
| IDE-0076 barra de estado: material del tablero | 🟢 |
| IDE-0077 copiar material del tablero | 🟢 |
| IDE-0078 clic en el material abre la edición | 🟢 |
| IDE-0079 barra de estado: piezas omitidas | 🟢 |
| IDE-0080 clic en omitidas selecciona y encuadra | 🟢 |
| IDE-0081 barra de estado: aprovechamiento del tablero | 🟢 |
| IDE-0082 clic en el aprovechamiento selecciona el tablero | 🟢 |
| IDE-0083 copiar el aprovechamiento del tablero | 🟢 |
| IDE-0084 barra de estado: material libre del tablero | 🟢 |
| IDE-0085 copiar el material libre del tablero | 🟢 |
| IDE-0086 clic en el material libre selecciona el tablero | 🟢 |
| IDE-0087 copiar piezas colocadas/total | 🟢 |
| IDE-0088 copiar las piezas omitidas | 🟢 |
| IDE-0089 copiar los tableros físicos | 🟢 |
| IDE-0090 copiar la selección de la barra | 🟢 |
| IDE-0091 copiar el zoom de la barra | 🟢 |
| IDE-0092 barra: retales de la solución seleccionada | 🟢 |
| IDE-0093 copiar los retales de la barra | 🟢 |
| IDE-0094 clic en retales selecciona su tablero | 🟢 |
| IDE-0095 barra: índice de la solución seleccionada | 🟢 |
| IDE-0096 copiar el índice de la solución | 🟢 |
| IDE-0097 clic en el índice pasa a la siguiente | 🟢 |
| IDE-0098 barra: huecos internos de la solución | 🟢 |
| IDE-0099 copiar los huecos internos de la barra | 🟢 |
| IDE-0100 clic en huecos selecciona su solución | 🟢 |
| IDE-0101 barra: coste de la solución seleccionada | ⚪ diferido |
| IDE-0102 copiar el coste de la solución | ⚪ diferido |
| IDE-0103 barra: estrategia de la solución seleccionada | 🟢 |
| IDE-0104 copiar la estrategia | 🟢 |
| IDE-0105 clic en la estrategia selecciona su solución | 🟢 |
| IDE-0106 barra: piezas de la solución seleccionada | 🟢 |
| IDE-0107 copiar las piezas de la solución | 🟢 |
| IDE-0108 clic en las piezas selecciona su solución | 🟢 |
| IDE-0109 barra: omitidas de la solución seleccionada | 🟢 |
| IDE-0110 copiar las omitidas de la solución | 🟢 |
| IDE-0111 clic en las omitidas selecciona su solución | 🟢 |
| IDE-0112 barra: tableros de la solución seleccionada | 🟢 |
| IDE-0113 copiar los tableros de la solución | 🟢 |
| IDE-0114 clic en los tableros selecciona su solución | 🟢 |
| IDE-0115 barra: puntuación de la solución seleccionada | 🟢 |
| IDE-0116 copiar la puntuación de la solución | 🟢 |
| IDE-0117 clic en la puntuación selecciona su solución | 🟢 |
| IDE-0118 barra: tablero libre de la solución seleccionada | 🟢 |
| IDE-0119 copiar el tablero libre de la solución | 🟢 |
| IDE-0120 clic en el tablero libre selecciona su solución | 🟢 |
| IDE-0121 barra: largo total de la solución seleccionada | 🟢 |
| IDE-0122 copiar el largo total de la solución | 🟢 |
| IDE-0123 clic en el largo total selecciona su solución | 🟢 |
| IDE-0124 barra: ancho total de la solución seleccionada | 🟢 |
| IDE-0125 copiar el ancho total de la solución | 🟢 |
| IDE-0126 clic en el ancho total selecciona su solución | 🟢 |
| IDE-0127 barra: área usada de la solución seleccionada | 🟢 |
| IDE-0128 copiar el área usada de la solución | 🟢 |
| IDE-0129 clic en el área usada selecciona su solución | 🟢 |
| IDE-0130 barra: área de retales de la solución seleccionada | 🟢 |
| IDE-0131 copiar el área de retales de la solución | 🟢 |
| IDE-0132 clic en el área de retales selecciona su solución | 🟢 |
| IDE-0133 barra: área envolvente de la solución seleccionada | 🟢 |
| IDE-0134 copiar el área envolvente de la solución | 🟢 |
| IDE-0135 clic en el área envolvente selecciona su solución | 🟢 |
| IDE-0136 barra: área de huecos internos de la solución seleccionada | 🟢 |
| IDE-0137 copiar el área de huecos internos de la solución | 🟡 |
| IDE-0138 clic en el área de huecos internos selecciona su solución | 🟡 |
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
IDE-0037…0057 **entregadas** (`#647`…`#667`, `#671`…`#673`, `#675`, `#676`);
séptima ola 0055…0058 cerrada.

Desde la revisión 2026-09-25, en `main` entraron `#673` (IDE-0055), `#675`
(IDE-0056) y `#676` (IDE-0057). Planning `#674` queda histórico.

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
- Inspector: unidades prefs mm/cm/in (IDE-0040 `#653`); disco sigue mm.
  Pieza muestra espesor, rotación 0°/90° (— si no colocada), veta
  (IDE-0046 `#661`) y área L×A (IDE-0055 `#673`). Comparador Largo/Ancho
  y diffs (IDE-0047 `#662`). Lista de corte / presupuesto PDF TEXT siguen
  `prefs.units` (IDE-0048); CSV/JSON y área m² siguen mm.
  Prefs: export/import JSON de taller (IDE-0049 `#664`); perfiles
  nombrados locales (IDE-0054 `#672`); sin rutas locales ni ventana.
  Inspector de raíz/categoría: conteos, materiales y área (IDE-0050
  `#665`). Tablero: aprovechamiento (IDE-0051 `#666`). Material por
  defecto de taller (IDE-0053 `#671`); no va en el `.bcproj`. Copiar
  texto del Inspector: entregado (`#676`, IDE-0057; Ctrl+Alt+I).

Deuda abierta explícita: **1** ítem (`DT-0006` en piloto D). Sin críticas sin
plan (`DOC-006`). Bugs GitHub abiertos: **0** (consulta `gh`).

---

## 4. Siguientes pasos (orden)

1. **Cola `0.4.4`** — IDE-0137 (0136 entregada; IDE-0101 e IDE-0102 diferidas, sin costes).
2. **Piloto DT-0006 D** — seguir runbook `docs/ops/PILOT-DT-0006-backup.md`;
   no abrir C sin multi-usuario real + DOC-010.
3. **Gate release** — `uat/RELEASE-SMOKE.md` en cada corte.
4. **No priorizar** IDE-0008 / LLM / DT-0006 C sin ADR o decisión vigente
   (eval IDE-0007 ya cerrada; LLM sigue diferido DEC-0011).

---

## 5. Cola candidata / criterio de nuevas ideas

Bugs abiertos: **0**. Eval IDE-0007: **cerrada**. Cola implementable
0064…0066 (novena ola; 0063 entregada). Residual bloqueado: piloto DT-0006 D
(operativo) + IDE-0008 /
LLM / DT-0006 C.

Criterio del cron: *solo proponer nuevas funcionalidades si no queda
desarrollo pendiente y bugs cerrados* → novena ola 0063…0066 abierta;
no se añaden más hasta cerrarla.

Séptima ola ya registrada (no renumerar):

| ID | Título | Por qué ahora |
|----|--------|---------------|
| IDE-0055 | Inspector: área de la pieza | Entregado (`#673`) |
| IDE-0056 | Zoom del Workspace al 100% | Entregado (`#675`) |
| IDE-0057 | Copiar texto del Inspector | Entregado (`#676`) |
| IDE-0058 | Marca sin guardar en la barra de ruta | Entregado |
| IDE-0059 | Inspector: área de una hoja de tablero | Entregado |
| IDE-0060 | Barra de estado: piezas colocadas / total | Entregado |
| IDE-0061 | Copiar ruta del .bcproj | Entregado |
| IDE-0062 | Clic en el zoom vuelve al 100% | Entregado |
| IDE-0063 | Barra de estado: piezas seleccionadas | Entregado |
| IDE-0064 | Copiar medidas de la pieza seleccionada | Entregado |
| IDE-0065 | Barra de estado: kerf del proyecto | Entregado |
| IDE-0066 | Clic en la selección ajusta el encuadre | Entregado |
| IDE-0067 | Clic en el kerf abre el espesor de sierra | Entregado |
| IDE-0068 | Copiar medidas L×A del tablero | Entregado |
| IDE-0069 | Barra de estado: tableros físicos | Entregado |
| IDE-0070 | Clic en colocadas/total encuadra las piezas colocadas | Entregado |
| IDE-0071 | Clic en tableros físicos encuadra todos los tableros | Entregado |
| IDE-0072 | Copiar el kerf del proyecto | Entregado |
| IDE-0073 | Barra de estado: espesor del tablero enfocado | Entregado |
| IDE-0074 | Clic en el espesor abre la edición de ese tablero | Entregado |
| IDE-0075 | Copiar espesor del tablero de la barra | Entregado |
| IDE-0076 | Barra de estado: material del tablero | Entregado |
| IDE-0077 | Copiar material del tablero | Entregado |
| IDE-0078 | Clic en el material abre la edición de ese tablero | Entregado |
| IDE-0079 | Barra de estado: piezas omitidas | Entregado |
| IDE-0080 | Clic en omitidas selecciona y encuadra las omitidas | Entregado |
| IDE-0081 | Barra de estado: aprovechamiento del tablero enfocado | Entregado |
| IDE-0082 | Clic en el aprovechamiento selecciona ese tablero | Entregado |
| IDE-0083 | Copiar el aprovechamiento del tablero | Entregado; Ctrl+Alt+Shift+U |
| IDE-0084 | Barra de estado: material libre del tablero enfocado | Entregado |
| IDE-0085 | Copiar el material libre del tablero | Entregado; Ctrl+Alt+Shift+F |
| IDE-0086 | Clic en el material libre selecciona ese tablero | Entregado |
| IDE-0087 | Copiar piezas colocadas/total de la barra | Entregado; Ctrl+Alt+Shift+P |
| IDE-0088 | Copiar las piezas omitidas de la barra | Entregado; Ctrl+Alt+Shift+O |
| IDE-0089 | Copiar los tableros físicos de la barra | Entregado; Ctrl+Alt+Shift+N |
| IDE-0090 | Copiar la selección de la barra | Entregado; Ctrl+Alt+Shift+S |
| IDE-0091 | Copiar el zoom de la barra | Entregado; Ctrl+Alt+Shift+Z |
| IDE-0092 | Barra: retales de la solución seleccionada | Entregado; `n ret.`; oculta si 0; sin clic |
| IDE-0093 | Copiar los retales de la barra | Entregado; Ctrl+Alt+Shift+R |
| IDE-0094 | Clic en retales selecciona su tablero | Entregado; no encuadra; no promociona |
| IDE-0095 | Barra: índice de la solución seleccionada | Entregado; `1/2 sol.` |
| IDE-0096 | Copiar el índice de la solución | Entregado; Ctrl+Alt+Shift+L; `1/2` sin `sol.`; no avanza |
| IDE-0097 | Clic en el índice pasa a la siguiente solución | Entregado; arrastre no; no aplica el layout |
| IDE-0098 | Barra: huecos internos de la solución seleccionada | Entregado; `hueco 0.0%`; sin clic |
| IDE-0099 | Copiar los huecos internos de la barra | Entregado; Ctrl+Alt+Shift+G; sin `hueco`; no avanza |
| IDE-0100 | Clic en huecos selecciona su solución | Entregado; no avanza; no aplica el layout |
| IDE-0101 | Barra: coste de la solución seleccionada | Diferido; sin costes |
| IDE-0102 | Copiar el coste de la solución | Diferido; sin costes |
| IDE-0103 | Barra: estrategia de la solución seleccionada | Entregado; `est. material`; `desconocida` se muestra; sin clic |
| IDE-0104 | Copiar la estrategia | Entregado; Ctrl+Alt+Shift+Y; el nombre, sin `est.`; no avanza |
| IDE-0105 | Clic en la estrategia selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0106 | Barra: piezas de la solución seleccionada | Entregado; `n pza` / `n pcs`; `0` se muestra; sin clic |
| IDE-0107 | Copiar las piezas de la solución | Entregado; Ctrl+Alt+Shift+J; el número, sin `pza`; no avanza |
| IDE-0108 | Clic en las piezas selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0109 | Barra: omitidas de la solución seleccionada | Entregado; `fuera {n}` / `out {n}`; `0` se muestra; sin clic |
| IDE-0110 | Copiar las omitidas de la solución | Entregado; Ctrl+Alt+Shift+Q; el número, sin `fuera`; no avanza |
| IDE-0111 | Clic en las omitidas selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0112 | Barra: tableros de la solución seleccionada | Entregado; `pan. {n}` / `pnl {n}`; `0` se muestra; sin clic; distinto de `n tab.` |
| IDE-0113 | Copiar los tableros de la solución | Entregado; Ctrl+Alt+Shift+W; el número, sin `pan.`; no avanza |
| IDE-0114 | Clic en los tableros selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0115 | Barra: puntuación de la solución seleccionada | Entregado; `pts. {value}` / `pts {value}`; `0.00` se muestra; sin clic |
| IDE-0116 | Copiar la puntuación de la solución | Entregado; Ctrl+Alt+Shift+V; el valor, sin `pts.`; no avanza |
| IDE-0117 | Clic en la puntuación selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0118 | Barra: tablero libre de la solución seleccionada | Entregado; `sbr. {value}` / `rem. {value}`; `0.0%` se muestra; sin clic; distinto de `libre` |
| IDE-0119 | Copiar el tablero libre de la solución | Entregado; Ctrl+Alt+Shift+E; el porcentaje, sin `sbr.`; no avanza |
| IDE-0120 | Clic en el tablero libre selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0121 | Barra: largo total de la solución seleccionada | Entregado; `lrg. {length}` / `len. {length}`; `0 mm` se muestra; sin clic |
| IDE-0122 | Copiar el largo total de la solución | Entregado; Ctrl+Alt+Shift+H; el largo con unidad, sin `lrg.`; no avanza |
| IDE-0123 | Clic en el largo total selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0124 | Barra: ancho total de la solución seleccionada | Entregado; `anc. {length}` / `wid. {length}`; `0 mm` se muestra; sin clic |
| IDE-0125 | Copiar el ancho total de la solución | Entregado; Ctrl+Alt+Shift+X; el ancho con unidad, sin `anc.`; no avanza |
| IDE-0126 | Clic en el ancho total selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0127 | Barra: área usada de la solución seleccionada | Entregado; `ár. {area}` / `area {area}`; `0 mm²` se muestra; sin clic |
| IDE-0128 | Copiar el área usada de la solución | Entregado; Ctrl+Alt+Shift+A; el área con unidad, sin `ár.`; no avanza |
| IDE-0129 | Clic en el área usada selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0130 | Barra: área de retales de la solución seleccionada | Entregado; `retár. {area}` / `offar. {area}`; `0 mm²` se muestra; sin clic |
| IDE-0131 | Copiar el área de retales de la solución | Entregado; Ctrl+Alt+Shift+I; el área con unidad, sin `retár.`; no avanza |
| IDE-0132 | Clic en el área de retales selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0133 | Barra: área envolvente de la solución seleccionada | Entregado; `env. {area}` / `bnd. {area}`; `0 mm²` se muestra; sin clic |
| IDE-0134 | Copiar el área envolvente de la solución | Entregado; Ctrl+Alt+Shift+1; el área con unidad, sin `env.`; no avanza |
| IDE-0135 | Clic en el área envolvente selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0136 | Barra: área de huecos internos de la solución seleccionada | Entregado; `hueár. {area}` / `gapar. {area}`; `0 mm²` se muestra; sin clic |
| IDE-0137 | Copiar el área de huecos internos de la solución | Entregado; Ctrl+Alt+Shift+2; el área con unidad, sin `hueár.`; no avanza |
| IDE-0138 | Clic en el área de huecos internos selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0139 | Barra: área de tablero libre de la solución seleccionada | Entregado; `sbrár. {area}` / `remar. {area}`; `0 mm²` se muestra; sin clic |
| IDE-0140 | Copiar el área de tablero libre de la solución | Entregado; Ctrl+Alt+Shift+3; el área con unidad, sin `sbrár.`; no avanza |
| IDE-0141 | Clic en el área de tablero libre selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0142 | Barra: área de tableros consumidos de la solución seleccionada | Entregado; `panár. {area}` / `pnlar. {area}`; `0 mm²` se muestra; sin clic |
| IDE-0143 | Copiar el área de tableros consumidos de la solución | Entregado; Ctrl+Alt+Shift+4; el área con unidad, sin `panár.`; no avanza |
| IDE-0144 | Clic en el área de tableros consumidos selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0145 | Barra: aprovechamiento de tableros de la solución seleccionada | Entregado; `aprv. {value}` / `util. {value}`; `0.0%` se muestra; sin clic |
| IDE-0146 | Copiar el aprovechamiento de tableros de la solución | Entregado; Ctrl+Alt+Shift+5; el porcentaje, sin `aprv.`; no avanza |
| IDE-0147 | Clic en el aprovechamiento de tableros selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0148 | Barra: piezas rotadas de la solución seleccionada | Entregado; `rot. {n}` / `rot {n}`; `0` se muestra; sin clic |
| IDE-0149 | Copiar las piezas rotadas de la solución | Entregado; Ctrl+Alt+Shift+6; el número, sin `rot.`; no avanza |
| IDE-0150 | Clic en las piezas rotadas selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0151 | Barra: piezas sin rotar de la solución seleccionada | Entregado; `nrot. {n}` / `unrot {n}`; `0` se muestra; sin clic |
| IDE-0152 | Copiar las piezas sin rotar de la solución | Entregado; Ctrl+Alt+Shift+7; el número, sin `nrot.`; no avanza |
| IDE-0153 | Clic en las piezas sin rotar selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0154 | Barra: porcentaje de piezas rotadas de la solución seleccionada | Entregado; `rot% {value}` / `rot% {value}`; `0.0%` se muestra; sin clic |
| IDE-0155 | Copiar el porcentaje de piezas rotadas de la solución | Entregado; Ctrl+Alt+Shift+8; el porcentaje, sin `rot%`; no avanza |
| IDE-0156 | Clic en el porcentaje de piezas rotadas selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0157 | Barra: porcentaje de piezas sin rotar de la solución seleccionada | Entregado; `nrot% {value}` / `unrot% {value}`; `0.0%` se muestra; sin clic |
| IDE-0158 | Copiar el porcentaje de piezas sin rotar de la solución | Entregado; Ctrl+Alt+Shift+9; el porcentaje, sin `nrot%`; no avanza |
| IDE-0159 | Clic en el porcentaje de piezas sin rotar selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |
| IDE-0160 | Barra: aprovechamiento envolvente de la solución seleccionada | Entregado; `env% {value}` / `bnd% {value}`; `0.0%` se muestra; sin clic |
| IDE-0161 | Copiar el aprovechamiento envolvente de la solución | Entregado; Ctrl+Alt+Shift+0; el porcentaje, sin `env%`; no avanza |
| IDE-0162 | Clic en el aprovechamiento envolvente selecciona su solución | Entregado; clic selecciona `solution:{index}`; arrastre no; no avanza |

Prioridad de ataque: trigésima tercera ola cerrada (0162 entregada; IDE-0101 e IDE-0102 diferidas, sin costes). Cola vacía.

Cerradas en este ciclo `0.4.4.dev0` (en `main`): IDE-0025…0057.
Cerradas en `0.4.3`: IDE-0019…0024 (+ eval IDE-0007 2026-09-12).

---

## 6. Criterio de esta revisión

- No se implementa código de producto en este pase: solo alinear docs,
  snapshot y backlog; registrar `#673`/`#675`/`#676` en `main` y dejar
  IDE-0058 como única cola implementable. Fold `#674` /
  `REVIEW-2026-09-25` histórico.
- Bugs: Issues GitHub abiertos = 0 (`gh issue list`).
- Próxima revisión automática: re-leer DOC-003/004/006 + CHANGELOG Unreleased
  y sustituir referencias a esta fecha por `REVIEW-YYYY-MM-DD-…`.
