# Plan y seguimiento — Empaquetado macOS y Mac App Store (MAS)

**Estado:** 🟢 Fases 1, 2, 3 y 4 completadas (`dist/BoardComposer-0.4.4.pkg` construido y firmado) · 🔵 Fase 5 lista para subida a App Store Connect  
**Versión base:** `0.4.4` (ciclo `0.4.5.dev0`)  
**Plataforma destino:** macOS (`arm64` Apple Silicon, `LSMinimumSystemVersion = 14.0`)  
**Canal principal:** Mac App Store (`dist/BoardComposer-0.4.4.pkg` firmado con App Sandbox)

---

## 1. Fidelidad con Apple HIG y App Store Review Guidelines (macOS)

| Criterio de Apple (HIG / Review Guideline) | Implementación en BoardComposer | Estado |
|---|---|---|
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
|---|---|---|
| **Apple Developer Team** | `Eugenio de Frutos Sanchez` (`V29BTBRY6G`) | 🟢 Activo |
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

### Fase 5 — Validación y subida a App Store Connect (🔵 Lista para subir)

- [ ] Subir `dist/BoardComposer-0.4.4.pkg` con **Transporter.app** (arrastrar `/Volumes/BACKUPS_PROYECTOS/__01.-Github_Repositories/boardcomposer/dist/BoardComposer-0.4.4.pkg` a Transporter y pulsar **Entregar** / **Deliver**), o por CLI:
  ```bash
  xcrun altool --validate-app -f dist/BoardComposer-0.4.4.pkg \
    -t macos -u "<apple-id>" -p "<app-specific-password>"
  xcrun altool --upload-app -f dist/BoardComposer-0.4.4.pkg \
    -t macos -u "<apple-id>" -p "<app-specific-password>"
  ```
- [ ] Probar compilación desde **TestFlight para macOS** (verifica contenedor Sandbox, apertura/guardado `.bcproj` y exportación PDF/SVG/DXF/CSV).
- [ ] Completar metadatos de App Store Connect usando la sección 5 de este documento.
- [ ] Enviar a revisión de Apple (**Submit for Review**).

---

## 5. Formulario completo para App Store Connect (Copiar y pegar)

### 5.1 Alta inicial («Nueva App» / New App)

| Campo en App Store Connect | Valor a rellenar |
|---|---|
| **Plataformas (Platforms)** | `macOS` |
| **Nombre (Name)** | `BoardComposer` *(máx. 30 caracteres)* |
| **Idioma principal (Primary Language)** | `Español (España)` *(Spanish - Spain)* |
| **ID del paquete (Bundle ID)** | `BoardComposer - com.edefrutos.boardcomposer` |
| **SKU** | `BC-MACOS-001` |
| **Acceso de usuarios (User Access)** | `Acceso completo (Full Access)` |

---

### 5.2 Información de la App (App Information)

| Campo | Español (ES) | English (EN-US) |
|---|---|---|
| **Nombre (30 máx.)** | `BoardComposer` | `BoardComposer` |
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

**5 capturas recomendadas:**
1. **Workspace + Proyecto demo:** Vista principal con los tableros físicos, piezas acotadas, retales y el Inspector a la derecha.
2. **Comparador de soluciones (`Cmd+4`):** Tabla inferior comparando candidatas y miniaturas junto al diálogo de **Explicar candidata** (`Cmd+Alt+E`).
3. **Diálogo de Exportación (`Cmd+Shift+E`):** Vista previa del plano con cotas, secuencia de corte y selección de formato (SVG/PDF/DXF/PNG).
4. **Catálogo de materiales (`Cmd+Alt+T`):** Tabla de materiales con espesores, precios €/m² y medidas estándar.
5. **Pantalla de Inicio (Welcome):** Con acceso rápido a proyectos recientes, plantillas y proyecto demo.

---

## 4. Registro de progreso

| Fecha | Fase | Hito / Resultado | Estado |
|---|---|---|---|
| 2026-11-12 | Prep | Cierre de `v0.4.4`, UAT smoke en macOS `OK` y creación del plan de seguimiento | 🟢 Hecho |
| 2026-11-13 | Fase 1 | Generación de `studio/assets/AppIcon.icns`, soporte en `branding.py` y `packaging/macos/Info.plist` (`com.edefrutos.boardcomposer`) | 🟢 Hecho |
| 2026-11-13 | Fase 2 | `QAction.MenuRole` macOS, soporte `sys._MEIPASS`, fallback `.revs/` en App Sandbox y entitlements MAS | 🟢 Hecho |
| 2026-11-13 | Fase 3 | `packaging/macos/BoardComposer.spec`, `packaging/macos/build_mas.sh` y build `dist/BoardComposer.app` (104 MB `arm64`) | 🟢 Hecho |
| 2026-11-13 | Fase 4 | Incrustación de `BoardComposer.provisionprofile`, firma profunda MAS y generación de `dist/BoardComposer-0.4.4.pkg` (43 MB) | 🟢 Hecho |
| — | Fase 5 | Subida con Transporter, TestFlight macOS y envío a revisión | 🔵 Pendiente |
