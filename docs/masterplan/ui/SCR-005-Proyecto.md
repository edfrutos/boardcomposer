# SCR-005 — Gestión del Proyecto

**Módulo:** BoardComposer Studio

**Código:** SCR-005  
**Versión:** 1.3.0  
**Estado:** Alineado con Studio  
**Última revisión:** 16/09/2026

---

## Objetivo

La gestión del proyecto cubre el ciclo de vida del `.bcproj`: crear, abrir,
guardar, renombrar, plantillas, inventario de tableros/piezas (manual o
CSV/Excel) y el Explorador como árbol del trabajo en curso. No es una pantalla
única: se reparte entre menús **Archivo** / **Proyecto**, la pantalla de inicio
(SCR-001) y el dock Explorador.

---

## Filosofía

Un proyecto es una unidad reproducible en disco (`.bcproj` v6, con
migraciones ADR-015). El usuario debe poder retomarlo meses después con el
mismo inventario, colocaciones y contexto. La configuración de solver/tema
y el catálogo de materiales viven fuera del `.bcproj` (SCR-006 /
`material_catalog.json`).

---

## Dónde vive en Studio

```text
Archivo          Proyecto              Explorador (Ctrl+1)
────────         ────────              ────────────────────
Nuevo            Renombrar…            Raíz: nombre proyecto
Desde plantilla  Abrir carpeta         ├ Tableros (n)
Demo             Comparar revisiones…  ├ Piezas (n)
Inicio           Restaurar revisión…   └ Soluciones (n)
Abrir / Recientes Añadir tablero…
Guardar / Como   Añadir pieza…
Plantilla…       Importar tableros…
Salir            Importar piezas…
                 Catálogo materiales…
```

La barra de estado muestra el basename del `.bcproj` cuando el proyecto está
guardado; el tooltip lleva la ruta completa. Clic (o **Ctrl+Shift+R**) abre la
carpeta. Sin archivo en disco: «aún no guardado» + tip **Ctrl+S**.
**Ctrl+Alt+Shift+C** copia la ruta del archivo (deshabilitado si no hay
archivo en disco). A la derecha, piezas colocadas / total del inventario
(IDE-0060; una colocación de un id que no está en el inventario no
cuenta; clic encuadra las colocadas, IDE-0070; **Ctrl+Alt+Shift+P** lo copia, IDE-0087), las piezas omitidas (`2 om.`, IDE-0079; inventario sin colocación; oculta si es 0; clic las selecciona y encuadra, IDE-0080; **Ctrl+Alt+Shift+O** copia el número, IDE-0088), los tableros físicos (`n tab.`, IDE-0069; suma de
cantidades; oculto si no hay; clic encuadra todos, IDE-0071; **Ctrl+Alt+Shift+N** copia el número, IDE-0089), el espesor del tablero (`esp. 19 mm`, IDE-0073; el enfocado, o el único tipo; oculto si hay varios sin foco; clic lo edita, IDE-0074; **Ctrl+Alt+Shift+T** lo copia, IDE-0075), el material del tablero (`mat. Demo`, IDE-0076; el mismo tablero; oculto si el material está vacío; clic lo edita, IDE-0078; **Ctrl+Alt+Shift+M** lo copia, IDE-0077), el aprovechamiento del tablero enfocado (`uso 24.0%`, IDE-0081; la misma fórmula que el Inspector; oculto sin foco o sin uso; clic lo selecciona, IDE-0082; **Ctrl+Alt+Shift+U** lo copia, IDE-0083), el material libre del tablero enfocado (`libre 76.0%`, IDE-0084; complemento del aprovechamiento; la misma visibilidad; clic lo selecciona, IDE-0086; **Ctrl+Alt+Shift+F** lo copia, IDE-0085), las piezas seleccionadas en el Workspace (`n sel.`, IDE-0063;
oculta si no hay selección; clic ajusta el encuadre, IDE-0066;
**Ctrl+Alt+Shift+S** copia el número, IDE-0090), el kerf
del proyecto (`kerf 3.2 mm`,
IDE-0065; unidades de Preferencias; oculto si no hay proyecto; clic abre
el espesor de sierra, IDE-0067; **Ctrl+Alt+Shift+K** lo copia, IDE-0072) y el zoom
del Workspace (clic vuelve al 100%, IDE-0062; **Ctrl+Alt+Shift+Z** lo copia, IDE-0091), los retales de la solución seleccionada (`n ret.`, IDE-0092; ocultos si no hay solución o si es 0; clic selecciona su tablero, IDE-0094; **Ctrl+Alt+Shift+R** copia el número, IDE-0093), el índice de la solución seleccionada (`1/2 sol.`, IDE-0095; oculto si no hay solución o si el índice no mapea; clic pasa a la siguiente, IDE-0097; no aplica el layout; **Ctrl+Alt+Shift+L** copia `1/2`, sin `sol.`, IDE-0096), los huecos internos de esa solución (`hueco 0.0%` / `gap 33.3%`, IDE-0098; la misma visibilidad; `0.0%` se muestra; clic selecciona esa solución en el explorador, IDE-0100; no avanza; **Ctrl+Alt+Shift+G** copia el porcentaje, sin `hueco`, IDE-0099), la estrategia de esa solución (`est. material` / `str. material`, IDE-0103; la misma visibilidad que el índice; sin nombre se muestra `est. desconocida`; clic selecciona esa solución en el explorador, IDE-0105; no avanza; **Ctrl+Alt+Shift+Y** copia el nombre, sin `est.`, IDE-0104), las piezas de esa solución (`n pza` / `n pcs`, IDE-0106; la misma visibilidad que el índice; `0` se muestra; clic selecciona esa solución en el explorador, IDE-0108; no avanza; **Ctrl+Alt+Shift+J** copia el número, sin `pza`, IDE-0107), las omitidas de esa solución (`fuera 0` / `out 2`, IDE-0109; la misma visibilidad que el índice; `0` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0111; no avanza; arrastre no; distinto de `n om.`; **Ctrl+Alt+Shift+Q** copia el número, sin `fuera`, IDE-0110), los tableros de esa solución (`pan. 0` / `pnl 2`, IDE-0112; la misma visibilidad que el índice; `0` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0114; no avanza; arrastre no; distinto de `n tab.`; **Ctrl+Alt+Shift+W** copia el número, sin `pan.`, IDE-0113), la puntuación de esa solución (`pts. 0.00` / `pts 0.75`, IDE-0115; la misma visibilidad que el índice; `0.00` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0117; no avanza; arrastre no; **Ctrl+Alt+Shift+V** copia el valor, sin `pts.`, IDE-0116) el tablero libre de esa solución (`sbr. 0.0%` / `rem. 76.0%`, IDE-0118; la misma visibilidad que el índice; `0.0%` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0120; no avanza; arrastre no; distinto de `libre`; **Ctrl+Alt+Shift+E** copia el porcentaje, sin `sbr.`, IDE-0119) el largo total de esa solución (`lrg. 0 mm` / `len. 400 mm`, IDE-0121; la misma visibilidad que el índice; `0 mm` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0123; no avanza; arrastre no; **Ctrl+Alt+Shift+H** copia el largo con unidad, sin `lrg.`, IDE-0122) el ancho total de esa solución (`anc. 0 mm` / `wid. 300 mm`, IDE-0124; la misma visibilidad que el índice; `0 mm` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0126; no avanza; arrastre no; **Ctrl+Alt+Shift+X** copia el ancho con unidad, sin `anc.`, IDE-0125) el área usada de esa solución (`ár. 0 mm²` / `area 20000 mm²`, IDE-0127; la misma visibilidad que el índice; `0 mm²` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0129; no avanza; arrastre no; **Ctrl+Alt+Shift+A** copia el área con unidad, sin `ár.`, IDE-0128) el área de retales de esa solución (`retár. 0 mm²` / `offar. 20000 mm²`, IDE-0130; la misma visibilidad que el índice; `0 mm²` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0132; no avanza; arrastre no; distinto de `n ret.`; **Ctrl+Alt+Shift+I** copia el área con unidad, sin `retár.`, IDE-0131) el área envolvente de esa solución (`env. 0 mm²` / `bnd. 60000 mm²`, IDE-0133; la misma visibilidad que el índice; `0 mm²` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0135; no avanza; arrastre no; **Ctrl+Alt+Shift+1** copia el área con unidad, sin `env.`, IDE-0134) el área de huecos internos de esa solución (`hueár. 0 mm²` / `gapar. 30000 mm²`, IDE-0136; la misma visibilidad que el índice; `0 mm²` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0138; no avanza; arrastre no; distinto de `hueco n%`; **Ctrl+Alt+Shift+2** copia el área con unidad, sin `hueár.`, IDE-0137) el área de tablero libre de esa solución (`sbrár. 0 mm²` / `remar. 380000 mm²`, IDE-0139; la misma visibilidad que el índice; `0 mm²` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0141; no avanza; arrastre no; distinto de `sbr. n%`; **Ctrl+Alt+Shift+3** copia el área con unidad, sin `sbrár.`, IDE-0140) el área de tableros consumidos de esa solución (`panár. 0 mm²` / `pnlar. 500000 mm²`, IDE-0142; la misma visibilidad que el índice; `0 mm²` se muestra; sigue las unidades de Preferencias; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0144; no avanza; arrastre no; distinto de `pan. {n}`; **Ctrl+Alt+Shift+4** copia el área con unidad, sin `panár.`, IDE-0143) el aprovechamiento de tableros de esa solución (`aprv. 0.0%` / `util. 24.0%`, IDE-0145; la misma visibilidad que el índice; `0.0%` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0147; no avanza; arrastre no; distinto de `uso`; **Ctrl+Alt+Shift+5** copia el porcentaje, sin `aprv.`, IDE-0146) las piezas rotadas de esa solución (`rot. 0` / `rot 2`, IDE-0148; la misma visibilidad que el índice; `0` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0150; no avanza; arrastre no; distinto de `n pza`; **Ctrl+Alt+Shift+6** copia el número, sin `rot.`, IDE-0149) las piezas sin rotar de esa solución (`nrot. 0` / `unrot 2`, IDE-0151; la misma visibilidad que el índice; `0` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0153; no avanza; arrastre no; distinto de `rot. {n}`; **Ctrl+Alt+Shift+7** copia el número, sin `nrot.`, IDE-0152) el porcentaje de piezas rotadas de esa solución (`rot% 0.0%` / `rot% 50.0%`, IDE-0154; la misma visibilidad que el índice; `0.0%` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0156; no avanza; arrastre no; distinto de `rot. {n}`; **Ctrl+Alt+Shift+8** copia el porcentaje, sin `rot%`, IDE-0155) el porcentaje de piezas sin rotar de esa solución (`nrot% 0.0%` / `unrot% 75.0%`, IDE-0157; la misma visibilidad que el índice; `0.0%` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0159; no avanza; arrastre no; distinto de `nrot. {n}`; **Ctrl+Alt+Shift+9** copia el porcentaje, sin `nrot%`, IDE-0158) el aprovechamiento envolvente de esa solución (`env% 0.0%` / `bnd% 50.0%`, IDE-0160; la misma visibilidad que el índice; `0.0%` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0162; no avanza; arrastre no; distinto de `aprv.` y `uso`; **Ctrl+Alt+Shift+0** copia el porcentaje, sin `env%`, IDE-0161) el porcentaje de retales de esa solución (`ret% 0.0%` / `off% 4.0%`, IDE-0163; la misma visibilidad que el índice; `0.0%` se muestra; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0165; no avanza; arrastre no; distinto de `n ret.` y `retár.`; **Ctrl+Alt+Shift+F1** copia el porcentaje, sin `ret%`, IDE-0164) y la puntuación de desperdicio de esa solución (`ptsh. 0.00` / `ptsw 0.50`, IDE-0166; la misma visibilidad que el índice; `0.00` se muestra; clic selecciona esa solución en el explorador, IDE-0168; no avanza; arrastre no; distinto de `pts.`; **Ctrl+Alt+Shift+F2** copia el valor, sin `ptsh.`, IDE-0167) y la puntuación de uso de material de esa solución (`ptsu. 0.00` / `ptsu 0.25`, IDE-0169; la misma visibilidad que el índice; `0.00` se muestra; clic selecciona esa solución en el explorador, IDE-0171; no avanza; arrastre no; distinto de `pts.` y `ptsh.`; **Ctrl+Alt+Shift+F3** copia el valor, sin `ptsu.`, IDE-0170) y la puntuación de cortes de esa solución (`ptsc. 0.00` / `ptsc 0.75`, IDE-0172; la misma visibilidad que el índice; `0.00` se muestra; clic selecciona esa solución en el explorador, IDE-0174; no avanza; arrastre no; distinto de `pts.`, `ptsh.` y `ptsu.`; **Ctrl+Alt+Shift+F4** copia el valor, sin `ptsc.`, IDE-0173) y la puntuación de regularidad de esa solución (`ptsr. 0.00` / `ptsr 0.40`, IDE-0175; la misma visibilidad que el índice; `0.00` se muestra; clic selecciona esa solución en el explorador, IDE-0177; no avanza; arrastre no; distinto de `pts.`, `ptsh.`, `ptsu.` y `ptsc.`; **Ctrl+Alt+Shift+F5** copia el valor, sin `ptsr.`, IDE-0176) y la puntuación de veta de esa solución (`ptsv. 0.00` / `ptsg 0.40`, IDE-0178; la misma visibilidad que el índice; `0.00` se muestra; clic selecciona esa solución en el explorador, IDE-0180; no avanza; arrastre no; distinto de `pts.`, `ptsh.`, `ptsu.`, `ptsc.` y `ptsr.`; **Ctrl+Alt+Shift+F6** copia el valor, sin `ptsv.`, IDE-0179) y la completitud de esa solución (`comp. sí` / `full yes`, IDE-0181; `comp. no` / `full no` si hay omitidas; la misma visibilidad que el índice; distinto de `fuera`; clic selecciona esa solución en el explorador, IDE-0183; no avanza; arrastre no; **Ctrl+Alt+Shift+F7** copia el valor, sin `comp.`, IDE-0182) y el área del mayor retal (`maxr. {area}` / `maxo {area}`, IDE-0184; oculta si no hay retales; distinta de `n ret.`, `retár.` y `ret%`; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0186; no avanza; arrastre no; **Ctrl+Alt+Shift+F8** copia el área con unidad, sin `maxr.`, IDE-0185) y el área del menor retal (`minr. {area}` / `mino {area}`, IDE-0187; oculta si no hay retales; distinta de `maxr.`, `n ret.`, `retár.` y `ret%`; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0189; no avanza; arrastre no; **Ctrl+Alt+Shift+F9** copia el área con unidad, sin `minr.`, IDE-0188) y las dimensiones del mayor retal (`maxd. {size}` / `maxd {size}`, IDE-0190; oculta si no hay retales; distinta de `maxr.`, `minr.`, `retár.` y `ret%`; cursor mano si está visible; clic selecciona esa solución en el explorador, IDE-0192; no avanza; arrastre no; **Ctrl+Alt+Shift+F10** copia el L×A con unidad, sin `maxd.`, IDE-0191).

---

## Flujos implementados

### Ciclo de archivo

| Acción | Atajo | Notas |
| -------- | ------- | -------- |
| Nuevo | **Ctrl+N** | Diálogo nombre + unidades; untitled |
| Abrir | **Ctrl+O** | `.bcproj`; migra v1→v2; rechaza versión futura; recuerda carpeta |
| Guardar | **Ctrl+S** | Si no hay ruta → Guardar como |
| Guardar como | **Ctrl+Shift+S** | Filtro `.bcproj`; recuerda carpeta (`last_project_directory`) |
| Salir | **Ctrl+Q** | Diálogo si hay cambios sin guardar |
| Recientes | menú / inicio | Máx. 10; poda fantasmas; label = basename (★ pin); submenú Abrir/anclar/carpeta/quitar; tip padre e hijos = ruta |
| Vaciar recientes | **Ctrl+Shift+X** | Confirmación |

### Identidad y ubicación

| Acción | Atajo | Notas |
| -------- | ------- | -------- |
| Renombrar proyecto | **Ctrl+Shift+F2** (también **F2** en raíz) | Undoable; menú y ctx Explorador |
| Metadatos (cliente, ref., notas) | **Ctrl+Alt+M** (también **Return** / Editar en raíz) | Undoable; `.bcproj` v3; Inspector |
| Espesor de sierra / kerf | **Ctrl+Alt+K** | Undoable; `.bcproj` v4; hueco al calcular/mover |
| Catálogo de materiales | **Ctrl+Alt+T** | Usuario; `material_catalog.json`; export/import JSON; no va en el `.bcproj` |
| Abrir carpeta | **Ctrl+Shift+R** | Solo si hay archivo en disco |
| Copiar ruta | **Ctrl+Alt+Shift+C** | Ruta del `.bcproj`; sin nube |
| Comparar revisiones | **Ctrl+Shift+Y** | Diff vs anillo local / archivos; recuerda carpeta (`last_diff_directory`) |
| Restaurar última revisión | **Ctrl+Alt+Y** | Snapshot más reciente del anillo; dirty hasta Guardar; vacía undo |
| Exportar backup de revisiones | **Ctrl+Alt+B** | Copia `.bcproj` + anillo a carpeta; diálogo Abrir carpeta; recuerda destino |

### Plantillas y demo

| Acción | Atajo | Notas |
| -------- | ------- | -------- |
| Guardar como plantilla | **Ctrl+Shift+M** | `~/.boardcomposer/project_templates/`; opcional incluir placements |
| Nuevo desde plantilla | **Ctrl+Shift+N** | Instancia **sin** placements |
| Proyecto demo | **Ctrl+Shift+D** | Inventario de ejemplo; untitled modificado |
| Pantalla de inicio | **Ctrl+Shift+H** | SCR-001 |

### Inventario

| Acción | Atajo | Notas |
| -------- | ------- | -------- |
| Añadir tablero | **Ctrl+Shift+B** | Diálogo combo catálogo; `AddBoardCommand` (undo) |
| Añadir pieza | **Ctrl+Shift+P** | Qty → varios IDs; combo catálogo; `AddPieceCommand` |
| Importar tableros CSV/Excel | **Ctrl+Shift+T** | Preview + mapeo; con undo |
| Importar piezas CSV/Excel | **Ctrl+Shift+O** | Preview; qty expandida; con undo |

Entradas alternativas: menú contextual del Explorador, CTAs del canvas vacío,
botones de la pantalla de inicio (piezas / plantilla / demo).

---

## Explorador

- Árbol: proyecto → Tableros / Piezas / Soluciones (conteos).
- Clic pieza → Inspector + selección en Workspace.
- Clic tablero → centra/resalta paneles.
- Doble clic / ctx solución → preview de candidata.
- Ctx pieza: editar, renombrar, duplicar, copiar ID, copiar medidas, eliminar.
- Ctx tablero: editar, renombrar, duplicar, copiar ID, copiar medidas, eliminar.

---

## Flujo principal recomendado

1. Nuevo, demo, plantilla o abrir reciente.
2. Añadir o importar tableros y piezas.
3. Guardar `.bcproj`.
4. Calcular layout (flujo Generar / SCR-002 / SCR-003).
5. Aplicar, ajustar en Workspace, exportar (SCR-007).

---

## Criterios de aceptación

- Crear / abrir / guardar / guardar como un `.bcproj` sin perder inventario.
- Renombrar y revelar carpeta cuando el archivo existe en disco.
- Importar CSV/Excel de tableros y piezas con vista previa.
- El Explorador refleja conteos y permite editar elementos.
- Cambios sin guardar bloquean el cierre con diálogo claro.

---

## Relación con otras pantallas

- SCR-001 — Inicio (CTAs y recientes).
- SCR-002 — Workspace.
- SCR-003 — Comparador (nodo Soluciones).
- SCR-004 — Inspector.
- SCR-006 — Preferencias (estrategia, idioma, tema; no sustituye al `.bcproj`).
- SCR-007 — Exportación.
- FLW-002 — Importar CSV/Excel.

---

## Límites conocidos (Studio actual)

- Metadatos de proyecto (cliente, referencia, notas) entregados (IDE-0024).
  Kerf / espesor de sierra entregado (IDE-0020; `.bcproj` v4; **Ctrl+Alt+K**).
  Veta / orientación de fibra entregada (IDE-0021; `.bcproj` v5; por pieza).
  Packing Skyline multipanel entregado (IDE-0022).
  Catálogo de materiales / espesores / €/m² / L×A entregado
  (IDE-0028/0029/0031; archivo usuario; coste y medidas típicas, no en
  `.bcproj`).

---

## Evolución prevista

- Kerf entregado (IDE-0020). Veta por pieza entregada (IDE-0021; no
  mezclar con metadatos de proyecto).
- Historial cloud / multi-usuario (DT-0006; piloto D activo).
