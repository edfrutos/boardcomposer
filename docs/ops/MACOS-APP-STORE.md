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
- [ ] Completar metadatos de App Store Connect:
  - Capturas de pantalla macOS (`1280x800`, `1440x900`, `2560x1600` o `2880x1800` — relación 16:10 obligatoria en Mac App Store).
  - Descripción (ES / EN), palabras clave, URL de soporte y Política de Privacidad (indicar que no recolecta datos ni usa telemetría/nube).
  - Notas para el revisor de Apple (explicar botón **Proyecto demo** en la pantalla de inicio para probar la app en 1 clic sin necesitar archivos externos).
- [ ] Enviar a revisión de Apple (**Submit for Review**).

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
