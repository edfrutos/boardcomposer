# Plan y seguimiento — Empaquetado macOS y Mac App Store (MAS)

**Estado:** 🟢 Fases 1–5 completadas · App **`BoardComposer` (`0.4.4`, Apple ID `6834470521`, SKU `BC-MACOS-001`)** en estado **Lista para revisión (*Ready for Review*)** en App Store Connect  
**Versión base:** `0.4.4` (build `46` · ciclo `0.4.5.dev0`)  
**Plataforma destino:** macOS (`arm64` Apple Silicon, `LSMinimumSystemVersion = 14.0`)  
**Canal principal:** Mac App Store (`dist/BoardComposer-0.4.4.pkg` firmado con App Sandbox)

---

## 1. Fidelidad con Apple HIG y App Store Review Guidelines (macOS)

| Criterio de Apple (HIG / Review Guideline) | Implementación en BoardComposer | Estado |
| --- | --- | --- |
| **HIG — App Icons (macOS)** | `studio/assets/AppIcon.icns` generado con `iconutil` (`16` a `1024` px `@1x`/`@2x`), sin pre-máscara para que macOS aplique la máscara squircle y efectos dinámicos. | 🟢 Listo |
| **HIG — The Menu Bar (macOS App Menu)** | `QAction.MenuRole`: `AboutRole` (`about`), `PreferencesRole` (`preferences` con `⌘,`) y `QuitRole` (`exit` con `⌘Q`) ubicados automáticamente en el menú **BoardComposer** de macOS. | 🟢 Listo |
| **Guideline 2.4.5(i) — App Sandbox** | `packaging/macos/entitlements.mas.plist` (`com.apple.application-identifier = V29BTBRY6G.com.edefrutos.boardcomposer`, `com.apple.developer.team-identifier = V29BTBRY6G`, `com.apple.security.app-sandbox = true`, `com.apple.security.files.user-selected.read-write = true`, `com.apple.security.print = true`) y `entitlements.inherit.plist` para binarios internos. | 🟢 Listo |
| **Guideline 2.4.5(i) — Rutas dentro del contenedor Sandbox** | En App Sandbox, `~/.boardcomposer/` se resuelve dentro del contenedor (`~/Library/Containers/com.edefrutos.boardcomposer/Data/.boardcomposer/`). Además, `bcproj_revisions.py` hace fallback automático a `~/.boardcomposer/revs/` cuando el sandbox impide crear carpetas ocultas `.revs/` junto al archivo elegido por el usuario. | 🟢 Listo |
| **Guideline 2.5.1 — Sin APIs privadas** | `packaging/macos/BoardComposer.spec` excluye explícitamente `PySide6.QtWebEngine*`, `QtQml*`, `QtQuick*`, `Qt3D*` y módulos de test/desarrollo. | 🟢 Listo |
| **Export Compliance (`ITSAppUsesNonExemptEncryption`)** | Declarado `<false/>` en `packaging/macos/Info.plist` para evitar bloqueos de cuestionario de cifrado en App Store Connect / TestFlight. | 🟢 Listo |
| **Document Types & UTType (`.bcproj`)** | Declarados `CFBundleDocumentTypes` y `UTExportedTypeDeclarations` (`com.edefrutos.boardcomposer.project`) en `packaging/macos/Info.plist`. | 🟢 Listo |

---

## 2. Identificadores y certificados registrados (Apple Developer)

| Elemento | Valor registrado | Estado |
| --- | --- | --- |
| **Apple Developer Team** | `Eugenio de Frutos Sanchez` (`V29BTBRY6G`) | 🟢 Activo |
| **Apple ID de la App** | `6834470521` | 🟢 Asignado en App Store Connect |
| **SKU** | `BC-MACOS-001` | 🟢 Registrado |
| **Bundle ID** | `com.edefrutos.boardcomposer` (`V29BTBRY6G.com.edefrutos.boardcomposer`) | 🟢 Registrado |
| **Categoría App Store** | `public.app-category.productivity` | 🟢 Definido en `Info.plist` |
| **Certificado App (MAS)** | `Apple Distribution: Eugenio de Frutos Sanchez (V29BTBRY6G)` (`C4F503FE87828623C3664F818F9C9E350FCCEB5A`) | 🟢 Instalado y verificado |
| **Certificado Installer (MAS)** | `3rd Party Mac Developer Installer: Eugenio de Frutos Sanchez (V29BTBRY6G)` (`60E5E198326F445869749D36C5A7659DE83D94E6`) | 🟢 Instalado y verificado |
| **Provisioning Profile** | `BoardComposer.provisionprofile` (UUID `f04a5255-d9fb-4c7e-a593-90a24caf1e04`, tipo `STORE`, expira `2027-09-12`) | 🟢 Incrustado (`embedded.provisionprofile`) |

---

## 3. Fases de ejecución y checklist de seguimiento

### Fase 1 — Activos e `Info.plist` / `.icns` (🟢 Completada)

- [x] Generar `studio/assets/AppIcon.icns` (`16`, `32`, `128`, `256`, `512`, `1024` px `@1x`/`@2x`) con `sips` + `iconutil`.
- [x] Priorizar `AppIcon.icns` en `studio/branding.py` (`app_icon()`).
- [x] Crear `packaging/macos/Info.plist` con `CFBundleIdentifier = com.edefrutos.boardcomposer`, `ITSAppUsesNonExemptEncryption = false` y UTType `com.edefrutos.boardcomposer.project` para `.bcproj`.

### Fase 2 — Adaptación a App Sandbox y Apple HIG (🟢 Completada)

- [x] Configurar `QAction.MenuRole` (`AboutRole`, `PreferencesRole`, `QuitRole`) en `studio/main_window.py` para integración nativa con la barra de menús de macOS.
- [x] Adaptar `src/boardcomposer/io/bcproj_revisions.py` para hacer fallback a `~/.boardcomposer/revs/<nombre>-<hash>.revs` cuando `APP_SANDBOX_CONTAINER_ID` está activo o `mkdir` junto al `.bcproj` lanza `PermissionError`.
- [x] Adaptar `studio/whats_new.py` y `studio/version.py` para resolver recursos (`CHANGELOG.md`, `pyproject.toml`, `docs/user/GUIA-RAPIDA.md`) desde `sys._MEIPASS` cuando la app corre empaquetada.
- [x] Crear `packaging/macos/entitlements.mas.plist` y `packaging/macos/entitlements.inherit.plist`.

### Fase 3 — Construcción del bundle `.app` con PyInstaller (🟢 Completada)

- [x] Añadir grupo opcional `packaging = ["pyinstaller>=6.0"]` en `pyproject.toml`.
- [x] Crear `packaging/macos/BoardComposer.spec` y script `packaging/macos/build_mas.sh` (+ target `make build-macos-app`).
- [x] Ejecutar build local del bundle `.app` (`dist/BoardComposer.app`, 104 MB, `arm64`, 0 restos de `QtWebEngine`, `Info.plist` OK).
- [x] Verificar arranque de `dist/BoardComposer.app` (`RUNNING OK`).

### Fase 4 — Firma profunda (`codesign`) y empaquetado `.pkg` (🟢 Completada)

Comando reproducible ejecutado:

```bash
PROVISION_PROFILE="packaging/macos/BoardComposer.provisionprofile" \
MAS_APP_IDENTITY="C4F503FE87828623C3664F818F9C9E350FCCEB5A" \
MAS_INSTALLER_IDENTITY="60E5E198326F445869749D36C5A7659DE83D94E6" \
make build-macos-app
```

- [x] Limpieza automática de atributos extendidos (`xattr -cr`) e `Icon\r`.
- [x] Copia de `BoardComposer.provisionprofile` a `dist/BoardComposer.app/Contents/embedded.provisionprofile`.
- [x] Firma de todos los binarios Mach-O (`.so`, `.dylib`) y `.framework` internos con `entitlements.inherit.plist`, y del bundle principal `dist/BoardComposer.app` con `entitlements.mas.plist` (`Apple Distribution: Eugenio de Frutos Sanchez (V29BTBRY6G)`).
- [x] Verificación `codesign --verify --deep --strict --verbose=2 dist/BoardComposer.app` → `valid on disk` / `satisfies its Designated Requirement`.
- [x] Generación y verificación de `dist/BoardComposer-0.4.4.pkg` (43 MB) con `productbuild` + `pkgutil --check-signature` (`3rd Party Mac Developer Installer: Eugenio de Frutos Sanchez (V29BTBRY6G)`).

### Fase 5 — Validación y subida a App Store Connect (🟢 Lista para revisión)

- [x] Subir `dist/BoardComposer-0.4.4.pkg` con **Transporter.app** (builds `44`–`46` procesadas en TestFlight sin errores).
- [x] Probar compilación desde **TestFlight para macOS** (verificado contenedor Sandbox, versión `0.4.4` desde `Info.plist`, botones y redimensionado `1440×900`).
- [x] Completar metadatos, política de privacidad y capturas 16:10 de App Store Connect usando la sección 5 de este documento.
- [x] Seleccionar compilación de `0.4.4` y dejar la app en estado **Lista para revisión (*Ready for Review*)** (Apple ID `6834470521`).

---

## 5. Formulario completo para App Store Connect (Copiar y pegar)

### 5.1 Alta inicial («Nueva App» / New App)

| Campo en App Store Connect | Valor a rellenar |
| --- | --- |
| **Plataformas (Platforms)** | `macOS` |
| **Nombre (Name)** | `BoardComposer` *(máx. 30 caracteres)* |
| **Idioma principal (Primary Language)** | `Español (España)` *(Spanish - Spain)* |
| **ID del paquete (Bundle ID)** | `BoardComposer - com.edefrutos.boardcomposer` |
| **SKU** | `BC-MACOS-001` |
| **ID de Apple (Apple ID)** | `6834470521` |
| **Acceso de usuarios (User Access)** | `Acceso completo (Full Access)` |

---

### 5.2 Información de la App (App Information)

| Campo | Español (ES) | English (EN-US) |
| --- | --- | --- |
| **Nombre (30 máx.)** | `BoardComposer` | `BoardComposer Cut Studio` |
| **Subtítulo (30 máx.)** | `Optimizador de corte 2D` | `2D Panel Cut Optimizer` |
| **Categoría principal** | `Productividad` (*Productivity*) | `Productivity` |
| **Categoría secundaria** | `Diseño gráfico` (*Graphics & Design*) | `Graphics & Design` |
| **Derechos de contenido** | **No** *(No contiene, muestra ni accede a contenido de terceros)* | **No** |

---

### 5.3 Clasificación por edades (Age Rating) y Regulaciones

- **Cuestionario de clasificación por edades (todas las casillas):**
  - Violencia, contenido sexual, lenguaje soez, drogas/alcohol/tabaco, apuestas, terror, información médica, acceso web sin restricciones: **Ninguno / No (None)** en todas.
  - **Resultado automático:** `4+`.
- **Ley de Servicios Digitales de la UE (DSA — Comerciante / Trader):**
  - Seleccionar según corresponda a tu estado fiscal en App Store Connect.
- **Cifrado y cumplimiento de exportación (Export Compliance):**
  - *¿Tu app utiliza cifrado?* → **No** (ya está preconfigurado en `Info.plist` con `ITSAppUsesNonExemptEncryption = false`).

---

### 5.4 Privacidad de la App (App Privacy — «Nutrition Labels»)

- **URL de la política de privacidad (Privacy Policy URL):**
  `https://github.com/edfrutos/boardcomposer/blob/main/docs/PRIVACY.md`
- **Cuestionario de recopilación de datos (*Data Collection*):**
  - *¿Tú o tus socios terceros recopiláis datos de esta app?* → **No, no recopilamos datos de esta app** (*No, we do not collect data from this app*).

---

### 5.5 Textos de la versión `0.4.4` — Español (España)

**Texto promocional (Promotional Text — máx. 170 caracteres; 159 car.):**

```text
Optimiza el despiece de tableros en tu taller: compara soluciones de corte 2D, controla veta y espesor de sierra (kerf) y exporta planos CAD/PDF y presupuestos.
```

**Descripción (Description — máx. 4000 caracteres):**

```text
BoardComposer Studio es una herramienta de escritorio para carpinteros, ebanistas, fabricantes de mobiliario y talleres de corte que necesitan optimizar el despiece de tableros 2D sobre uno o varios paneles físicos.

A diferencia de las calculadoras rígidas que imponen un único resultado, BoardComposer genera, valida, puntúa y explica múltiples alternativas de corte para que tú conserves siempre la decisión final.

CARACTERÍSTICAS PRINCIPALES

• Optimización multipanel real (MaxRects y Skyline):
  Empaqueta piezas sobre múltiples tableros físicos respetando compatibilidad de material, espesor, cantidades en stock y dirección de la veta.

• Ajustes reales de taller:
  Configura el espesor de sierra (kerf), bloquea la rotación en piezas con veta fija, intercambia piezas colocadas, sugiere huecos libres y congela colocaciones para re-empaquetar solo las piezas omitidas.

• Comparador visual y explicación local:
  Compara soluciones candidatas por aprovechamiento, área envolvente, número de cortes, regularidad y respeto de veta. Incluye explicación detallada en lenguaje natural 100 % local (sin enviar datos a la nube).

• Gestión de retales y catálogo de materiales:
  Identifica automáticamente los retales aprovechables de cada tablero y promuévelos al inventario del proyecto con un clic. Mantén tu propio catálogo local de materiales, espesores y precios por m².

• Exportación lista para taller y cliente:
  - Planos de corte en PDF, SVG, DXF (con capas por rol: PANELS, PIECES, OFFCUTS, DIMS, SEQ, META) y PNG/JPEG.
  - Lista de corte de taller ordenada por secuencia de sierra (CSV y PDF).
  - Presupuesto de material y mano de obra opcional en PDF listo para entregar al cliente.

• Importación rápida:
  Importa listados de piezas e inventario de tableros desde archivos CSV o Excel (.xlsx) con vista previa y mapeo de columnas.

• 100 % local, privado y sin suscripciones:
  Funciona completamente offline en tu Mac. No requiere cuenta, no usa telemetría y guarda un historial local de revisiones de tus proyectos (.bcproj).
```

**Palabras clave (Keywords — máx. 100 caracteres, separadas por comas sin espacios; 96 car.):**

```text
carpinteria,despiece,tableros,corte,madera,optimizador,nesting,plano,dxf,presupuesto,taller,cad
```

**Novedades de esta versión (What's New in This Version):**

```text
Versión inicial en Mac App Store (0.4.4):
• Motor de optimización 2D multipanel con algoritmos MaxRects y Skyline.
• Control de espesor de sierra (kerf), dirección de veta y promoción de retales a inventario.
• Comparador de soluciones con métricas detalladas en barra de estado e Inspector.
• Exportación de planos (PDF, SVG, DXF por capas, PNG/JPEG), lista de corte y presupuesto PDF con mano de obra.
```

**URL de soporte (Support URL):**

```text
https://github.com/edfrutos/boardcomposer/issues
```

**URL de marketing (Marketing URL — opcional):**

```text
https://github.com/edfrutos/boardcomposer
```

**Derechos de autor (Copyright):**

```text
© 2026 Eugenio de Frutos Sánchez
```

---

### 5.6 Textos de la versión `0.4.4` — English (U.S. / U.K.)

**Name (30 chars max):**

```text
BoardComposer Cut Studio
```

**Subtitle (30 chars max):**

```text
2D Panel Cut Optimizer
```

**Promotional Text (170 chars max; 156 chars):**

```text
Optimize 2D sheet goods cutting in your workshop: compare multi-panel layouts, lock wood grain, set saw kerf, and export CAD/PDF cut lists and quotes.
```

**Description:**

```text
BoardComposer Studio is a desktop tool for woodworkers, cabinetmakers, furniture makers, and cutting workshops that need to optimize 2D sheet goods cutting across one or multiple stock panels.

Unlike rigid calculators that force a single output, BoardComposer generates, validates, scores, and explains multiple layout candidates so you always keep the final decision.

KEY FEATURES

• True Multi-Panel Optimization (MaxRects & Skyline):
  Pack pieces across multiple physical boards while enforcing material compatibility, thickness, stock quantities, and grain direction.

• Real Workshop Controls:
  Configure saw blade kerf, lock rotation on grain-sensitive pieces, swap placed pieces, suggest free gaps, and freeze approved placements to re-pack omitted pieces.

• Visual Comparator & Local Explanation:
  Compare candidate solutions by board utilization, bounding area, cut score, regularity, and grain alignment. Includes a built-in natural-language explanation engine running 100% locally on your Mac.

• Offcut Tracking & Material Catalog:
  Automatically report usable offcuts per panel and promote them to project stock in one click. Maintain your own local catalog of materials, thicknesses, and prices per m².

• Workshop & Client-Ready Exports:
  - Cutting plans in PDF, SVG, layered DXF (PANELS, PIECES, OFFCUTS, DIMS, SEQ, META), and PNG/JPEG.
  - Saw-ordered workshop cut lists in CSV and PDF.
  - Client-ready PDF material and optional labor quotes.

• Fast Tabular Import:
  Import piece lists and board inventories from CSV or Excel (.xlsx) files with row validation preview and column mapping templates.

• 100% Local, Private & Offline:
  Runs entirely offline on your Mac with no accounts, no cloud dependencies, and no telemetry.
```

**Keywords (100 chars max; 94 chars):**

```text
woodworking,cutlist,optimizer,nesting,sheetgoods,plywood,cabinet,carpentry,panel,saw,dxf,quote
```

**What's New in This Version:**

```text
Initial Mac App Store release (0.4.4):
• Multi-panel 2D cutting optimization with MaxRects and Skyline solvers.
• Saw kerf, wood grain lock, and offcut promotion to stock inventory.
• Solution comparator with full status-bar and Inspector metrics.
• PDF/SVG/layered-DXF plan exports, saw-ordered cut lists, and PDF quotes.
```

---

### 5.7 Información para Revisión de la App (App Review Information)

- **Inicio de sesión requerido (Sign-in required):** **Desmarcar (No)** — la app no tiene login.
- **Notas para el revisor (Notes for Review):**

```text
Thank you for reviewing BoardComposer Studio!

No account, login, or external hardware is required to test the application.

Quick 1-minute walkthrough to test all core features:
1. On the Welcome screen, click "Proyecto demo" (Demo project) — or press Cmd+Shift+D. This loads a ready-to-use multi-panel project with sample boards, pieces, and calculated solutions.
2. Press Cmd+Return ("Calcular layout" / Calculate layout) to run the 2D multi-panel solver.
3. Switch between candidate solutions in the bottom Comparator table or Explorer tree, and press Cmd+Alt+E to open the local candidate explanation dialog.
4. Press Cmd+Alt+C to export a workshop Cut List (CSV or PDF), Cmd+Alt+Q to export a PDF Quote, or Cmd+Shift+E to export the cutting plan (SVG, PDF, DXF, PNG, JPEG) using the standard macOS Save panel.
```

---

### 5.8 Capturas de pantalla para Mac App Store (Requisitos)

Apple exige entre **1 y 10 capturas de pantalla** de macOS en relación de aspecto **16:10** en cualquiera de estas resoluciones exactas:

- `1280 × 800` px
- `1440 × 900` px
- `2560 × 1600` px
- `2880 × 1800` px

**5 capturas recomendadas (con `scripts/captura-boardcomposer.sh`):**

```bash
# 1. Abre la aplicación empaquetada
open dist/BoardComposer.app

# 2. Captura 1 — Pantalla de Inicio (Welcome)
scripts/captura-boardcomposer.sh 1-welcome

# 3. Pulsa Cmd+Shift+D (Proyecto demo) y Cmd+Return (Calcular layout)
#    Captura 2 — Workspace multipanel + Inspector
scripts/captura-boardcomposer.sh 2-workspace

# 4. Abre Explicar candidata (Cmd+Alt+E) encima de la ventana de 1440×900
#    Captura 3 — Comparador + Explicación local
scripts/captura-boardcomposer.sh --sin-redimensionar 3-comparador-explicar

# 5. Abre Exportar solución (Cmd+Shift+E)
#    Captura 4 — Diálogo de Exportación con vista previa
scripts/captura-boardcomposer.sh --sin-redimensionar 4-exportar

# 6. Abre Catálogo de materiales (Cmd+Alt+T)
#    Captura 5 — Catálogo de materiales y precios
scripts/captura-boardcomposer.sh --sin-redimensionar 5-catalogo
```

Las 5 capturas quedan en `~/Desktop/appstore-*.png` a `2880 × 1800` px (o `1440 × 900` px) listas para arrastrar a App Store Connect.

---

## 4. Registro de progreso

| Fecha | Fase | Hito / Resultado | Estado |
| --- | --- | --- | --- |
| 2026-11-12 | Prep | Cierre de `v0.4.4`, UAT smoke en macOS `OK` y creación del plan de seguimiento | 🟢 Hecho |
| 2026-11-13 | Fase 1 | Generación de `studio/assets/AppIcon.icns`, soporte en `branding.py` y `packaging/macos/Info.plist` (`com.edefrutos.boardcomposer`) | 🟢 Hecho |
| 2026-11-13 | Fase 2 | `QAction.MenuRole` macOS, soporte `sys._MEIPASS`, fallback `.revs/` en App Sandbox y entitlements MAS | 🟢 Hecho |
| 2026-11-13 | Fase 3 | `packaging/macos/BoardComposer.spec`, `packaging/macos/build_mas.sh` y build `dist/BoardComposer.app` (104 MB `arm64`) | 🟢 Hecho |
| 2026-11-13 | Fase 4 | Incrustación de `BoardComposer.provisionprofile`, firma profunda MAS y generación de `dist/BoardComposer-0.4.4.pkg` (43 MB) | 🟢 Hecho |
| 2026-11-13 | Fase 5 | Subida con Transporter y procesamiento de la compilación `0.4.4` (`44`–`46`) en TestFlight OK | 🟢 Hecho |
| 2026-11-13 | Fase 5 | Ficha completada, capturas 16:10 subidas y estado cambiado a **Lista para revisión** (Apple ID `6834470521`, SKU `BC-MACOS-001`) | 🟢 Hecho |
| 2026-11-16 | Fase 5 | Respuesta a cuestionario estándar de App Review (Guidelines 4.3 / 4.2.6, Submission ID `878b3b3b-9b09-46e8-843f-1c60268f74a1`) lista para enviar sin reenviar binario | 🟡 En curso |

---

## 6. Respuesta oficial a App Review (Guidelines 4.3 & 4.2.6)

> **Importante (instrucción expresa de Apple):** *"If you believe the app already meets the requirements of guidelines 4.3(a), 4.3(b) and 4.2.6, **do not resubmit the app**. Instead, reply to this message and answer all of the following questions in full."*  
> Responde directamente en el hilo de **App Store Connect → App Review (Resolution Center)** copiando y pegando el siguiente texto en inglés:

```text
Hello App Review Team,

Thank you for your review of BoardComposer (Apple ID: 6834470521, Version 0.4.4, Submission ID: 878b3b3b-9b09-46e8-843f-1c60268f74a1).

BoardComposer is a 100% original, custom-engineered 2D sheet-goods cutting optimization ("2D bin packing / nesting") CAD/CAM desktop application written from scratch by me (Eugenio de Frutos Sanchez). It is not built from any template or app generation service, nor does it duplicate any other app on my account or on the App Store.

Below are the full, detailed answers to all nine questions:

1. Describe in detail what this app does and the primary problem it solves for users. Do not use the App Store marketing description as your response.

BoardComposer solves the two-dimensional rectangular cutting stock and guillotine/non-guillotine bin-packing problem (NP-hard 2D nesting) for physical sheet materials (wood panels, MDF, melamine, plywood, acrylic, and sheet metal).
In a physical workshop, when a carpenter or fabricator needs to cut dozens of rectangular parts of varying dimensions out of standard stock sheets (e.g., 2440×1220 mm or 2800×2070 mm), doing the layout manually wastes 15–30% of raw material and leads to errors with saw blade thickness (kerf) and wood grain orientation.
Technically, BoardComposer implements a custom computational geometry engine from scratch (`src/boardcomposer/`) featuring:
- Multi-panel MaxRects (Maximal Rectangles) and Skyline heuristic solvers, plus Beam Search and an exact single-panel constraint solver, evaluating multiple board/panel orderings and placement heuristics.
- Physical workshop constraints: saw kerf spacing (`kerf_mm`) between every cut, per-piece grain direction locking (`grain: locked` preventing 90° rotation when wood fiber direction matters), material-type and thickness matching across heterogeneous stock inventories, and partial-solution diagnostics when inventory is insufficient.
- Interactive 2D CAD canvas (`BoardWorkspace`): users can manually drag and reassign pieces across physical panel instances, swap placed pieces (`Cmd+Alt+X`), auto-suggest valid free gaps (`Cmd+Alt+G`), freeze approved placements (`Cmd+Alt+F`) to re-pack only omitted pieces, and promote usable rectangular offcuts (`Offcut`) back into the project's remnant stock inventory (`Cmd+Alt+R`).
- Multi-candidate visual comparator and deterministic explanation engine: instead of outputting a single black-box layout, the solver ranks distinct candidate solutions across weighted criteria (material utilization, bounding box, cut regularity, waste, and grain score) and explains in plain language why one candidate outperforms another.
- Native vector and tabular manufacturing outputs generated directly by our own exporters (no external CAD dependencies): multi-layer DXF files (`PANELS`, `PIECES`, `OFFCUTS`, `DIMS`, `SEQ`, `META`) for CNC/CAD software, scaled vector SVG/PDF cutting plans with saw-cut sequence numbering, saw-ordered workshop cut lists (CSV/PDF), and itemized material + labor cost quotes (PDF).

2. Who is the intended user of this app? Provide a detailed description of the specific target audience.

The target audience consists of:
- Professional cabinetmakers, carpenters, furniture designers, and woodworking shops who cut sheet goods (melamine, plywood, MDF, particleboard) on panel saws, table saws, or CNC routers.
- Glaziers, acrylic/plastics fabricators, and light sheet-metal workshops that cut rectangular flat stock.
- Advanced DIY woodworkers and luthiers/makers running macOS who need an offline desktop tool to calculate how many stock boards to buy, generate a numbered saw-cutting sequence for the workshop floor, and produce a formal PDF material/labor estimate for their clients.

3. What need or gap in the market does this app address that existing apps do not currently address, or address less effectively? Provide a detailed, substantive explanation.

Existing cut-list calculators on macOS or the web suffer from three major limitations that BoardComposer specifically addresses:
- Black-box single output vs. human-in-the-loop comparison: Traditional calculators output a single rigid layout. If a workshop operator dislikes a specific cut on panel #2, they cannot easily compare alternative heuristics or manually drag/swap pieces between panels with real-time collision and kerf validation. BoardComposer generates multiple ranked candidate solutions, shows side-by-side visual diffs, explains the trade-offs locally, and allows interactive post-solve manual editing on the canvas with full Undo/Redo and an Action Timeline replay.
- End-to-end offcut lifecycle (Remnant reuse): Most tools treat leftover areas as dead waste. BoardComposer computes usable rectangular offcuts (`Offcut`), reports their exact dimensions, areas, shares, and aspect ratios, and lets the user promote those offcuts into reusable `remnant` stock boards within the `.bcproj` project file.
- Native offline macOS engineering workflow with layered DXF & local revision ring: Many competing tools are cloud-only web wrappers requiring paid monthly subscriptions and internet access on the workshop floor. BoardComposer runs 100% offline in the macOS App Sandbox, exports industry-standard R12 ASCII DXF with semantic CAD layers (`PANELS`, `PIECES`, `OFFCUTS`, `DIMS`, `SEQ`, `META`), and maintains an automatic local revision history ring (`.revs/`) with a built-in project diff viewer (`BcprojDiffDialog`).

4. What beta testing did you conduct before submitting the app for review? Provide examples of user feedback provided in beta that was applied to the production build.

Before submitting for App Review, we conducted structured User Acceptance Testing (UAT) across 50 iterative development waves (tracked in our repository under `uat/studio/CHECKLIST-FUNCIONAL.md`, `uat/studio/CHECKLIST-VISUAL.md`, and `uat/RELEASE-SMOKE.md`) as well as macOS TestFlight testing (builds 44, 45, and 46).
Concrete examples of feedback found during beta testing and applied directly to the production build (build 46):
- Example 1 (Window width overflow on 1440×900 MacBook screens): During TestFlight testing of build 45, calculating a multi-panel layout activated ~40 permanent metric indicators in the bottom `QStatusBar`, which caused Qt's layout engine to force the minimum window width to 2699 px—wider than standard MacBook screens. Based on this beta finding, we updated `QStatusBar` and the central stack size policies (`QSizePolicy.Policy.Ignored`) in build 46 so the window resizes smoothly down to 937×475 pt and fits 1440×900 displays properly.
- Example 2 (macOS keyboard shortcut conventions & native App Menu): Beta testing on macOS highlighted that documentation and status tips needed native macOS modifier conventions (`⌘`, `⌥`, `⇧`) and standard macOS Application Menu placement (`About BoardComposer`, `Settings…` with `⌘,`, and `Quit` with `⌘Q` via `QAction.MenuRole`).
- Example 3 (System theme button padding & frozen bundle version resolution): In TestFlight build 44, testing revealed that under the macOS `system` theme the `OK` button in the About dialog had tight horizontal padding, and the version label read the development cycle string instead of `CFBundleShortVersionString` (`0.4.4`). Both were fixed and verified in builds 45 and 46.
- Example 4 (Workshop workflow feedback from early UAT): Testers requested the ability to lock piece rotation for wood grain (`IDE-0021`), account for saw kerf thickness (`IDE-0020`), freeze already-cut panels while re-packing omitted pieces (`IDE-0030`), and include optional hourly labor cost in client PDF quotes (`IDE-0045`). All of these were implemented and verified prior to submission.

5. Is this app intended to function as a standalone product, or is it part of a suite of related apps published under your developer account? If part of a suite, provide a detailed description of how this app's scope and functionality differ from each other app in the suite.

BoardComposer is a completely standalone product. Its domain (industrial 2D cutting stock optimization, woodworking layout, CAD DXF/SVG/PDF plan generation, and carpentry workshop quoting) is entirely unrelated to any other app under my developer account (such as text/URL utilities or task management tools).

6. Could the functionality of this app be fully delivered as an in-app purchase, feature expansion, or content addition within any other app on your developer account? If so, provide a detailed explanation of why this functionality was not consolidated into that existing app.

No. BoardComposer is a specialized CAD/CAM and combinatorial optimization application for woodworking and sheet-goods manufacturing, with its own `.bcproj` document format (versioned schema v1–v6), 2D geometric packing solvers, interactive canvas, and DXF/SVG/PDF CAD exporters. It shares no domain, user workflow, or purpose with any other app on my developer account, so consolidating it into another app would make no sense for users.

7. Does this app's binary share any significant code, frameworks, or assets with any other app on your developer account, beyond standard third-party frameworks? If so, identify each shared component and describe its role in detail.

No. BoardComposer does not share any application code, domain logic, UI components, or graphical assets with any other app on my developer account. The entire codebase (~12,000+ lines of domain/solver/export/studio code and 1,670+ automated unit and integration tests) was written specifically for BoardComposer. Beyond the standard Python 3.13 runtime and PySide6 (Qt6) UI framework, all solvers, DXF/PDF/SVG exporters, and studio widgets are 100% bespoke to BoardComposer.

8. Does this app share any codebase, SDK, or content library with any third-party app, beyond standard third-party frameworks? If so, identify the shared component and provide a detailed explanation of the original functionality this app adds beyond it.

No. BoardComposer does not share any codebase, template, SDK, or content library with any third-party app. It uses only standard open-source runtime libraries (Python standard library and PySide6/Qt6 for the desktop GUI, plus open-source OFL fonts Archivo and Source Sans 3). All 2D packing algorithms (`MaxRects`, `Skyline`, `Beam Search`), the `.bcproj` serializer, the layered DXF writer, the PDF/SVG plan and quote renderers, and the Studio interface are original code written for this project.

9. Was this app created for a client, partner, or other third party who provided the app's content, concept, or branding? If so, identify who provided the content and provide a detailed explanation of why the app is submitted under your developer account rather than theirs.

No. BoardComposer was conceived, designed, developed, and branded entirely by me (Eugenio de Frutos Sanchez) as my own original product. No client, partner, template service, or third party provided the concept, code, content, or branding.

Please let me know if you need any additional technical details or a video walkthrough of the solver and CAD export workflows.

Best regards,
Eugenio de Frutos Sanchez
```

