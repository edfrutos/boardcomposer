# Plan y seguimiento — Empaquetado macOS y Mac App Store (MAS)

**Estado:** 🟡 En preparación (documentación de seguimiento lista)  
**Versión base:** `0.4.4` (ciclo `0.4.5.dev0`)  
**Plataforma destino:** macOS (`arm64` Apple Silicon / Universal2)  
**Canal principal:** Mac App Store (`.pkg` firmado con App Sandbox) + distribución directa opcional (`.dmg` Developer ID + Notarization)

---

## 1. Arquitectura actual y consideraciones técnicas

BoardComposer Studio es una aplicación Python 3.13 + PySide6 (`Qt6`):

- **Entry point GUI:** `studio/app.py` (`main()`).
- **Organización declarada:** `EDF Developer` · **Nombre:** `BoardComposer Studio`.
- **Icono actual:** `studio/assets/app_icon.jpg` (requiere conversión a `.icns` con `iconutil` en tamaños `16x16` a `1024x1024`).
- **Rutas de configuración local actuales:** `~/.boardcomposer/` (`preferences.json`, `recent_projects.json`, `material_catalog.json`, `project_templates/`, `export_templates/`, `import_templates/`).
  - ⚠️ **Impacto App Sandbox (MAS):** En Mac App Store es obligatorio `com.apple.security.app-sandbox = true`. Dentro del sandbox, `Path.home()` redirige automáticamente al contenedor `~/Library/Containers/<bundle-id>/Data/`, por lo que `~/.boardcomposer/` funcionará dentro del contenedor sin romper el código actual.
  - ⚠️ **Archivos del usuario (`.bcproj`, CSV, PDF, SVG, DXF) y anillo `.revs/`:**
    - Para abrir/guardar `.bcproj` o exportar mediante `QFileDialog`, se requiere el entitlement `com.apple.security.files.user-selected.read-write`.
    - **Punto crítico (anillo `.revs/` y backups DT-0006):** Bajo App Sandbox, la app solo tiene permiso sobre el archivo exacto elegido en `QFileDialog` (`NSOpenPanel`/`NSSavePanel`), **no** para crear automáticamente carpetas hermanas ocultas (`.<nombre>.bcproj.revs/`) en el mismo directorio salvo que el usuario conceda acceso a la carpeta o se guarden las revisiones dentro del contenedor de la app (`~/Library/Containers/<bundle-id>/Data/.boardcomposer/revs/`).

---

## 2. Identificadores y certificados requeridos (Apple Developer)

| Elemento | Valor previsto / Requisito | Estado |
|---|---|---|
| **Apple Developer Program** | Cuenta activa (Team ID `XXXXXXXXXX`) | [ ] Pendiente |
| **Bundle ID** | `com.edfdeveloper.boardcomposer` | [ ] Pendiente registrar en Apple Developer Portal |
| **Categoría App Store** | `public.app-category.productivity` (o `graphics-design` / `business`) | [ ] Pendiente |
| **Certificado 1 (MAS App)** | `3rd Party Mac Developer Application: <Nombre> (<TeamID>)` | [ ] Pendiente en Llavero |
| **Certificado 2 (MAS Installer)** | `3rd Party Mac Developer Installer: <Nombre> (<TeamID>)` | [ ] Pendiente en Llavero |
| **Provisioning Profile** | Perfil `Mac App Store` vinculado a `com.edfdeveloper.boardcomposer` | [ ] Pendiente (`embedded.provisionprofile`) |
| **Certificado opcional (DMG directo)** | `Developer ID Application` + `xcrun notarytool` | [ ] Opcional |

---

## 3. Fases de ejecución y checklist de seguimiento

### Fase 1 — Activos e `Info.plist` / `.icns`

- [ ] Generar `studio/assets/AppIcon.iconset` (`16`, `32`, `128`, `256`, `512`, `1024` px `@1x`/`@2x`) a partir de `studio/assets/app_icon.jpg`.
- [ ] Compilar `studio/assets/AppIcon.icns` con `iconutil -c icns studio/assets/AppIcon.iconset`.
- [ ] Definir `Info.plist`:
  - `CFBundleName`: `BoardComposer`
  - `CFBundleDisplayName`: `BoardComposer Studio`
  - `CFBundleIdentifier`: `com.edfdeveloper.boardcomposer`
  - `CFBundleShortVersionString`: `0.4.4`
  - `CFBundleVersion`: `44` (entero incremental por subida a TestFlight / App Store Connect)
  - `LSMinimumSystemVersion`: `14.0` (macOS Sonoma o superior)
  - `LSApplicationCategoryType`: `public.app-category.productivity`
  - `NSHighResolutionCapable`: `true`
  - `CFBundleDocumentTypes`: asociación de extensión `.bcproj` (`UTExportedTypeDeclarations` para `com.edfdeveloper.boardcomposer.project`).

### Fase 2 — Adaptación a App Sandbox (Mac App Store)

- [ ] Verificar/adaptar ruta del anillo de revisiones `.revs/` cuando corre en App Sandbox:
  - Si `os.environ.get("APP_SANDBOX_CONTAINER_ID")` está presente (o falla `mkdir` junto al `.bcproj` por `PermissionError`), almacenar el anillo `.revs/` en `~/.boardcomposer/revs/<hash-ruta>/` dentro del contenedor.
- [ ] Verificar que `studio/whats_new.py` y `studio/version.py` resuelven `CHANGELOG.md`, `pyproject.toml` y `docs/user/GUIA-RAPIDA.md` desde `sys._MEIPASS` / `Contents/Resources/` cuando la app está empaquetada (`getattr(sys, "frozen", False)`).
- [ ]Crear archivo `packaging/macos/entitlements.mas.plist`:
  - `com.apple.security.app-sandbox`: `true`
  - `com.apple.security.files.user-selected.read-write`: `true`
  - `com.apple.security.print`: `true` (si aplica impresión PDF)
- [ ] Crear archivo `packaging/macos/entitlements.inherit.plist` (para binarios internos / helpers de Python y Qt):
  - `com.apple.security.app-sandbox`: `true`
  - `com.apple.security.inherit`: `true`

### Fase 3 — Construcción del bundle `.app` (PyInstaller)

- [ ] Añadir `pyinstaller` a dependencias de empaquetado (`pyproject.toml` grupo `packaging`).
- [ ] Crear especificación `packaging/macos/BoardComposer.spec`:
  - Entry point: `studio/app.py` (`windowed=True`, `console=False`, `argv_emulation=False`).
  - Datos incluidos (`datas`): `CHANGELOG.md`, `pyproject.toml`, `docs/user/GUIA-RAPIDA.md`, `docs/DESIGN.md`, `studio/assets/`, `studio/fonts/` (si existen), `data/samples/`.
  - Exclusiones (`excludes`): `tkinter`, `matplotlib`, `scipy`, `pytest`, `ruff`, `mypy`, `pylint`, `flake8`, `flask` (salvo que se requiera en Studio), `QtWebEngine*` / `Qt3D*` / `QtQuick*` / `QtQml*` (obligatorio excluir `QtWebEngine` si no se usa, ya que usa APIs privadas que Apple rechaza en MAS).
- [ ] Ejecutar build limpio:
  ```bash
  .venv/bin/pyinstaller packaging/macos/BoardComposer.spec --noconfirm --clean
  ```
- [ ] Verificar arranque de `dist/BoardComposer.app/Contents/MacOS/BoardComposer` en local.

### Fase 4 — Firma profunda (`codesign`) y empaquetado `.pkg`

- [ ] Limpiar atributos extendidos de Finder (`xattr -cr dist/BoardComposer.app`) e `Icon\r`.
- [ ] Copiar `embedded.provisionprofile` a `dist/BoardComposer.app/Contents/embedded.provisionprofile`.
- [ ] Firmar de dentro hacia afuera (todos los `.dylib`, `.so`, frameworks de `PySide6/Qt/lib/*.framework` y `Python`) con `entitlements.inherit.plist`:
  ```bash
  codesign --force --verify --verbose --timestamp \
    --options runtime \
    --entitlements packaging/macos/entitlements.inherit.plist \
    --sign "3rd Party Mac Developer Application: <Nombre> (<TeamID>)" \
    <cada-binario-interno>
  ```
- [ ] Firmar el bundle principal `dist/BoardComposer.app` con `entitlements.mas.plist`:
  ```bash
  codesign --force --verify --verbose --timestamp \
    --options runtime \
    --entitlements packaging/macos/entitlements.mas.plist \
    --sign "3rd Party Mac Developer Application: <Nombre> (<TeamID>)" \
    dist/BoardComposer.app
  ```
- [ ] Verificar firma:
  ```bash
  codesign --verify --deep --strict --verbose=2 dist/BoardComposer.app
  ```
- [ ] Generar instalador `.pkg` para App Store Connect:
  ```bash
  productbuild \
    --component dist/BoardComposer.app /Applications \
    --sign "3rd Party Mac Developer Installer: <Nombre> (<TeamID>)" \
    dist/BoardComposer-0.4.4.pkg
  ```

### Fase 5 — Validación y subida a App Store Connect

- [ ] Crear la ficha de la app en **App Store Connect** (macOS, Bundle ID `com.edfdeveloper.boardcomposer`).
- [ ] Validar el `.pkg` con Xcode / `altool` / **Transporter**:
  ```bash
  xcrun altool --validate-app -f dist/BoardComposer-0.4.4.pkg \
    -t macos -u "<apple-id>" -p "<app-specific-password>"
  ```
- [ ] Subir el `.pkg` vía **Transporter.app** o `xcrun altool --upload-app`.
- [ ] Probar compilación desde **TestFlight para macOS** (verifica que el contenedor Sandbox y la apertura/guardado de `.bcproj` y exportación PDF/SVG/DXF/CSV funcionan sin errores de permisos).
- [ ] Completar metadatos de App Store Connect:
  - Capturas de pantalla macOS (`1280x800`, `1440x900`, `2560x1600` o `2880x1800` — relación 16:10 obligatoria en Mac App Store).
  - Descripción (ES / EN), palabras clave, URL de soporte y Política de Privacidad (indicar que no recolecta datos ni usa telemetría/nube).
  - Notas para el revisor de Apple (explicar botón **Proyecto demo** en la pantalla de inicio para probar la app en 1 clic sin necesitar archivos externos).
- [ ] Enviar a revisión de Apple (**Submit for Review**).

---

## 4. Registro de progreso

| Fecha | Fase | Hito / Resultado | Estado |
|---|---|---|---|
| 2026-11-12 | Prep | Cierre de `v0.4.4`, UAT smoke en macOS `OK` y creación de este plan de seguimiento | 🟢 Hecho |
| — | Fase 1 | Conversión de icono a `.icns` e `Info.plist` | 🔵 Pendiente |
| — | Fase 2 | Soporte `sys.frozen` en recursos + fallback de `.revs/` en App Sandbox | 🔵 Pendiente |
| — | Fase 3 | Spec PyInstaller (`packaging/macos/BoardComposer.spec`) + script de build `.app` | 🔵 Pendiente |
| — | Fase 4 | Firma con certificados MAS + generación de `.pkg` | 🔵 Pendiente |
| — | Fase 5 | Subida con Transporter, TestFlight macOS y envío a revisión | 🔵 Pendiente |
