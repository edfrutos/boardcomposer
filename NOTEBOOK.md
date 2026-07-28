# NOTEBOOK - BoardComposer

> **Archivo histórico.** Decisiones vivas → `docs/masterplan/DOC-005-Decisiones.md`
> y ADR. Mapa docs → `docs/README.md`.

Cuaderno de ingeniería del proyecto.

## 2026-06-26 - Sesión inicial de arquitectura

BoardComposer no será un optimizador de corte tradicional. Será un motor para generar composiciones 2D a partir de tablas disponibles, puntuarlas y explicar sus ventajas e inconvenientes.

### Alcance inicial

- Composición plana 2D.

- Tablas rectangulares.

- Medidas internas en milímetros.

- Motor independiente de la interfaz.

- Salida inicial por consola.

### Queda fuera por ahora

- Modelado 3D.

- Muebles completos.

- Interfaz gráfica.

- IA integrada.

- Uniones complejas de carpintería.

## 2026-07-16 - Vertical multipanel

Se completa la primera vertical multipanel sobre MaxRects:

- inventario mediante `StockPanel.quantity`;
- referencia estable a tipo e instancia física;
- validación y desperdicio por panel;
- compatibilidad de espesor;
- persistencia Studio versión 2 compatible con proyectos versión 1;
- representación de paneles lado a lado en Workspace y SVG.

La siguiente validación debe ser un UAT visual completo en Studio, incluyendo
proyectos con varios tipos, cantidades y espesores.

## 2026-07-16 - UAT multipanel y cierre del backlog inmediato

Tras el UAT visual se cerraron los puntos abiertos del backlog inmediato y
de datos/flujo de trabajo:

- material como segundo criterio de compatibilidad pieza/panel, además de
  espesor;
- movimiento y reasignación interactiva de piezas entre paneles físicos
  desde el Workspace (arrastre + snapping al panel bajo el cursor);
- identificador e instancia de panel en el Inspector de pieza;
- cantidad al crear una pieza nueva (genera varios ids correlativos);
- importación de inventario de tableros desde CSV, con vista previa y
  detección de duplicados;
- migraciones explícitas y versionadas de `.bcproj` (ADR-015);
- retales informativos por panel consumido (ADR-016), en vez de solo
  "desperdicio" agregado;
- soluciones parciales (piezas omitidas) en vez de "sin solución" cuando no
  todo cabe;
- comparador de soluciones con resaltado de mejor métrica por solución;
- pruebas de interacción Qt para el Workspace, corriendo en modo offscreen;
- benchmarks reproducibles del generador multipanel.

### Incidente: pérdida de trabajo y reconstrucción

Durante la exploración de CP-SAT como generador exacto de un solo panel se
detectó que buena parte de este trabajo —ya dado por completado en una
sesión anterior— no estaba presente en disco (código, tests y ADRs
correspondientes). Se reconstruyó íntegramente a partir del resumen de la
conversación y del transcript completo, verificando cada pieza contra el
estado real del repositorio antes de darla por buena. Lección: no asumir que
un resumen de conversación refleja el estado del disco sin verificarlo
primero contra el código y `git status`/`git log`.

### Próximo paso

Con el contrato multipanel estabilizado (material, retales, soluciones
parciales, migraciones), retomar la exploración de CP-SAT como generador
exacto de un solo panel, ya iniciada en `cp_sat_runner.py`.

## 2026-07-16 - Cierre de sesión (docs + limpieza)

- Documentación alineada con el código fusionado en `main` (PR #21):
  README, ROADMAP, TODO, AI_CONTEXT, DECISIONS, INDEX, DOC-003/004/005/006,
  `data_model.md`, `algorithms.md`, `project_structure.md`.
- Checklist UAT multipanel en `uat/multipanel/CHECKLIST.md`.
- Eliminados prototipos obsoletos (`workbench/`, `tools/visualize_demo.py`,
  `out/demo.html`) y directorios vacíos (`prompts/`, `research/`,
  `assets/icons/`, `assets/images/`). `out/` queda en `.gitignore`.
