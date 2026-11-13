# Plan y seguimiento — Empaquetado macOS y Mac App Store (MAS)

**Estado:** 🟢 Fases 1, 2 y 3 implementadas en código y `packaging/macos/` · 🔵 Fases 4 y 5 pendientes de certificados de Apple Developer  
**Versión base:** `0.4.4` (ciclo `0.4.5.dev0`)  
**Plataforma destino:** macOS (`arm64` Apple Silicon / Universal2, `LSMinimumSystemVersion = 14.0`)  
**Canal principal:** Mac App Store (`.pkg` firmado con App Sandbox) + distribución directa opcional (`.dmg` Developer ID + Notarization)

---

## 1. Fidelidad con Apple HIG y App Store Review Guidelines (macOS)

| Criterio de Apple (HIG / Review Guideline) | Implementación en BoardComposer | Estado |
|---|---|---|
| **HIG — App Icons (macOS)** | `studio/assets/AppIcon.icns` generado con `iconutil` (`16` a `1024` px `@1x`/`@2x`), sin pre-máscara para que macOS aplique la máscara squircle y efectos dinámicos. | 🟢 Listo |
| **HIG — The Menu Bar (macOS App Menu)** | `QAction.MenuRole`: `AboutRole` (`about`), `PreferencesRole` (`preferences` con `⌘,`) y `QuitRole` (`exit` con `⌘Q`) ubicados automáticamente en el menú **BoardComposer** de macOS. | 🟢 Listo |
| **Guideline 2.4.5(i) — App Sandbox** | `packaging/macos/entitlements.mas.plist` (`com.apple.security.app-sandbox = true`, `com.apple.security.files.user-selected.read-write = true`, `com.apple.security.print = true`) y `entitlements.inherit.plist` para binarios internos. | 🟢 Listo |
| **Guideline 2.4.5(i) — Rutas dentro del contenedor Sandbox** | En App Sandbox, `~/.boardcomposer/` se resuelve dentro del contenedor (`~/Library/Containers/com.edfdeveloper.boardcomposer/Data/.boardcomposer/`). Además, `bcproj_revisions.py` hace fallback automático a `~/.boardcomposer/revs/` cuando el sandbox impide crear carpetas ocultas `.revs/` junto al archivo elegido por el usuario. | 🟢 Listo |
| **Guideline 2.5.1 — Sin APIs privadas** | `packaging/macos/BoardComposer.spec` excluye explícitamente `PySide6.QtWebEngine*`, `QtQml*`, `QtQuick*`, `Qt3D*` y módulos de test/desarrollo. | 🟢 Listo |
| **Export Compliance (`ITSAppUsesNonExemptEncryption`)** | Declarado `<false/>` en `packaging/macos/Info.plist` para evitar bloqueos de cuestionario de cifrado en App Store Connect / TestFlight. | 🟢 Listo |
| **Document Types & UTType (`.bcproj`)** | Declarados `CFBundleDocumentTypes` y `UTExportedTypeDeclarations` (`com.edfdeveloper.boardcomposer.project`) en `packaging/macos/Info.plist`. | 🟢 Listo |

---

## 2. Identificadores y certificados requeridos (Apple Developer)

| Elemento | Valor previsto / Requisito | Estado |
|---|---|---|
| **Apple Developer Program** | Cuenta activa (Team ID `XXXXXXXXXX`) | [ ] Pendiente |
| **Bundle ID** | `com.edfdeveloper.boardcomposer` | [ ] Pendiente registrar en Apple Developer Portal |
| **Categoría App Store** | `public.app-category.productivity` | [x] Definido en `Info.plist` |
| **Certificado 1 (MAS App)** | `3rd Party Mac Developer Application: <Nombre> (<TeamID>)` | [ ] Pendiente en Llavero |
| **Certificado 2 (MAS Installer)** | `3rd Party Mac Developer Installer: <Nombre> (<TeamID>)` | [ ] Pendiente en Llavero |
| **Provisioning Profile** | Perfil `Mac App Store` vinculado a `com.edfdeveloper.boardcomposer` | [ ] Pendiente (`embedded.provisionprofile`) |
| **Certificado opcional (DMG directo)** | `Developer ID Application` + `xcrun notarytool` | [ ] Opcional |

---

## 3. Fases de ejecución y checklist de seguimiento

### Fase 1 — Activos e `Info.plist` / `.icns` (🟢 Completada)

- [x] Generar `studio/assets/AppIcon.icns` (`16`, `32`, `128`, `256`, `512`, `1024` px `@1x`/`@2x`) con `sips` + `iconutil`.
- [x] Priorizar `AppIcon.icns` en `studio/branding.py` (`app_icon()`).
- [x] Crear `packaging/macos/Info.plist` con metadatos MAS, `ITSAppUsesNonExemptEncryption = false` y UTType `com.edfdeveloper.boardcomposer.project` para `.bcproj`.

### Fase 2 — Adaptación a App Sandbox y Apple HIG (🟢 Completada)

- [x] Configurar `QAction.MenuRole` (`AboutRole`, `PreferencesRole`, `QuitRole`) en `studio/main_window.py` para integración nativa con la barra de menús de macOS.
- [x] Adaptar `src/boardcomposer/io/bcproj_revisions.py` para hacer fallback a `~/.boardcomposer/revs/<nombre>-<hash>.revs` cuando `APP_SANDBOX_CONTAINER_ID` está activo o `mkdir` junto al `.bcproj` lanza `PermissionError`.
- [x] Adaptar `studio/whats_new.py` y `studio/version.py` para resolver recursos (`CHANGELOG.md`, `pyproject.toml`, `docs/user/GUIA-RAPIDA.md`) desde `sys._MEIPASS` cuando la app corre empaquetada.
- [x] Crear `packaging/macos/entitlements.mas.plist` y `packaging/macos/entitlements.inherit.plist`.

### Fase 3 — Construcción del bundle `.app` con PyInstaller (🟢 Completada)

- [x] Añadir grupo opcional `packaging = ["pyinstaller>=6.0"]` en `pyproject.toml`.
- [x] Crear `packaging/macos/BoardComposer.spec` y script `packaging/macos/build_mas.sh` (+ target `make build-macos-app`).
- [x] Ejecutar build local del bundle `.app` (`dist/BoardComposer.app`, 104 MB, `arm64`, 0 restos de `QtWebEngine`, `Info.plist` y `codesign --verify --deep --strict` OK):
  ```bash
  .venv/bin/pip install -e ".[packaging]"
  make build-macos-app
  ```
- [x] Verificar arranque de `dist/BoardComposer.app` (`RUNNING OK`, cierre limpio con `SIGINT`).

### Fase 4 — Firma profunda (`codesign`) y empaquetado `.pkg` (🔵 Pendiente de certificados)

Con los certificados instalados en el Llavero y el perfil descargado:

```bash
PROVISION_PROFILE="packaging/macos/embedded.provisionprofile" \
MAS_APP_IDENTITY="3rd Party Mac Developer Application: Tu Nombre (TEAMID)" \
MAS_INSTALLER_IDENTITY="3rd Party Mac Developer Installer: Tu Nombre (TEAMID)" \
make build-macos-app
```

- [ ] Limpieza automática de atributos extendidos (`xattr -cr`) e `Icon\r`.
- [ ] Copia de `embedded.provisionprofile` a `Contents/embedded.provisionprofile`.
- [ ] Firma de binarios internos con `entitlements.inherit.plist` y del `.app` con `entitlements.mas.plist`.
- [ ] Verificación `codesign --verify --deep --strict --verbose=2 dist/BoardComposer.app`.
- [ ] Generación de `dist/BoardComposer-0.4.4.pkg` con `productbuild`.

### Fase 5 — Validación y subida a App Store Connect (🔵 Pendiente)

- [ ] Crear la ficha de la app en **App Store Connect** (macOS, Bundle ID `com.edfdeveloper.boardcomposer`).
- [ ] Validar el `.pkg` con Xcode / `altool` / **Transporter**:
  ```bash
  xcrun altool --validate-app -f dist/BoardComposer-0.4.4.pkg \
    -t macos -u "<apple-id>" -p "<app-specific-password>"
  ```
- [ ] Subir el `.pkg` vía **Transporter.app** o `xcrun altool --upload-app`.
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
| 2026-11-13 | Fase 1 | Generación de `studio/assets/AppIcon.icns`, soporte en `branding.py` y `packaging/macos/Info.plist` | 🟢 Hecho |
| 2026-11-13 | Fase 2 | `QAction.MenuRole` macOS, soporte `sys._MEIPASS`, fallback `.revs/` en App Sandbox y entitlements MAS | 🟢 Hecho |
| 2026-11-13 | Fase 3 | `packaging/macos/BoardComposer.spec`, `packaging/macos/build_mas.sh`, build `dist/BoardComposer.app` (104 MB `arm64`) y verificación de arranque OK | 🟢 Hecho |
| — | Fase 4 | Firma con certificados MAS + generación de `.pkg` | 🔵 Pendiente |
| — | Fase 5 | Subida con Transporter, TestFlight macOS y envío a revisión | 🔵 Pendiente |
