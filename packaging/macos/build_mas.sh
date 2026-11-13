#!/usr/bin/env bash
# Build, sign, and package BoardComposer.app / BoardComposer.pkg for Mac App Store.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

PYTHON="${PYTHON:-.venv/bin/python}"
SPEC="packaging/macos/BoardComposer.spec"
APP_BUNDLE="dist/BoardComposer.app"
ENTITLEMENTS_MAS="packaging/macos/entitlements.mas.plist"
ENTITLEMENTS_INHERIT="packaging/macos/entitlements.inherit.plist"

echo "==> 1. Limpiando artefactos previos..."
rm -rf build/BoardComposer dist/BoardComposer dist/BoardComposer.app

echo "==> 2. Construyendo BoardComposer.app con PyInstaller..."
"$PYTHON" -m PyInstaller "$SPEC" --noconfirm --clean

echo "==> 3. Limpiando atributos extendidos de Finder y archivos residuales..."
find "$APP_BUNDLE" -name "Icon"$'\r' -delete || true
find "$APP_BUNDLE" -name ".DS_Store" -delete || true
xattr -cr "$APP_BUNDLE"

if [[ -n "${PROVISION_PROFILE:-}" && -f "${PROVISION_PROFILE}" ]]; then
  echo "==> 4. Incrustando perfil de aprovisionamiento..."
  cp "$PROVISION_PROFILE" "$APP_BUNDLE/Contents/embedded.provisionprofile"
fi

if [[ -n "${MAS_APP_IDENTITY:-}" ]]; then
  echo "==> 5. Firmando binarios internos con entitlements heredados..."
  while IFS= read -r -d '' bin; do
    codesign --force --verify --verbose --timestamp \
      --options runtime \
      --entitlements "$ENTITLEMENTS_INHERIT" \
      --sign "$MAS_APP_IDENTITY" \
      "$bin"
  done < <(find "$APP_BUNDLE/Contents/Frameworks" "$APP_BUNDLE/Contents/Resources" \
    \( -name "*.dylib" -o -name "*.so" -o -path "*.framework/Versions/A/*" \) \
    -type f -print0 2>/dev/null || true)

  echo "==> 6. Firmando bundle principal $APP_BUNDLE..."
  codesign --force --verify --verbose --timestamp \
    --options runtime \
    --entitlements "$ENTITLEMENTS_MAS" \
    --sign "$MAS_APP_IDENTITY" \
    "$APP_BUNDLE"

  echo "==> 7. Verificando firma..."
  codesign --verify --deep --strict --verbose=2 "$APP_BUNDLE"
else
  echo "==> (Omitiendo firma MAS: define MAS_APP_IDENTITY para firmar para App Store)"
fi

if [[ -n "${MAS_INSTALLER_IDENTITY:-}" ]]; then
  VERSION="$("$PYTHON" -c 'import studio.version as v; print(v.STUDIO_VERSION)')"
  PKG_PATH="dist/BoardComposer-${VERSION}.pkg"
  echo "==> 8. Generando paquete instalador $PKG_PATH..."
  productbuild \
    --component "$APP_BUNDLE" /Applications \
    --sign "$MAS_INSTALLER_IDENTITY" \
    "$PKG_PATH"
  echo "==> Paquete listo para Transporter: $PKG_PATH"
fi

echo "==> Build finalizado: $APP_BUNDLE"
