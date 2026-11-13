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
PROVISION_PROFILE="${PROVISION_PROFILE:-}"

if [[ -z "$PROVISION_PROFILE" ]]; then
  if [[ -f "packaging/macos/BoardComposer.provisionprofile" ]]; then
    PROVISION_PROFILE="packaging/macos/BoardComposer.provisionprofile"
  elif [[ -f "$HOME/Downloads/BoardComposer.provisionprofile" ]]; then
    PROVISION_PROFILE="$HOME/Downloads/BoardComposer.provisionprofile"
  fi
fi

echo "==> 1. Limpiando artefactos previos..."
rm -rf build/BoardComposer dist/BoardComposer dist/BoardComposer.app

echo "==> 2. Construyendo BoardComposer.app con PyInstaller..."
"$PYTHON" -m PyInstaller "$SPEC" --noconfirm --clean

echo "==> 3. Incrustando perfil de aprovisionamiento y limpiando atributos extendidos..."
if [[ -n "$PROVISION_PROFILE" && -f "$PROVISION_PROFILE" ]]; then
  echo "    Perfil: $PROVISION_PROFILE"
  xattr -c "$PROVISION_PROFILE" 2>/dev/null || true
  cp "$PROVISION_PROFILE" "$APP_BUNDLE/Contents/embedded.provisionprofile"
fi

find "$APP_BUNDLE" -name "Icon"$'\r' -delete || true
find "$APP_BUNDLE" -name ".DS_Store" -delete || true
xattr -cr "$APP_BUNDLE"

if xattr -lr "$APP_BUNDLE" | grep -q "com.apple.quarantine"; then
  echo "Error: aún quedan atributos com.apple.quarantine en $APP_BUNDLE" >&2
  exit 1
fi

if [[ -n "${MAS_APP_IDENTITY:-}" ]]; then
  echo "==> 5. Firmando binarios Mach-O internos (.so / .dylib) con entitlements heredados..."
  while IFS= read -r -d '' bin; do
    if file "$bin" | grep -q "Mach-O"; then
      codesign --force --verify --timestamp \
        --options runtime \
        --entitlements "$ENTITLEMENTS_INHERIT" \
        --sign "$MAS_APP_IDENTITY" \
        "$bin"
    fi
  done < <(find "$APP_BUNDLE/Contents/Frameworks" "$APP_BUNDLE/Contents/Resources" \
    \( -name "*.dylib" -o -name "*.so" \) -type f -print0 2>/dev/null || true)

  echo "==> 6. Firmando frameworks internos (.framework)..."
  while IFS= read -r -d '' fw; do
    codesign --force --verify --timestamp \
      --options runtime \
      --entitlements "$ENTITLEMENTS_INHERIT" \
      --sign "$MAS_APP_IDENTITY" \
      "$fw"
  done < <(find "$APP_BUNDLE/Contents/Frameworks" -name "*.framework" -type d -print0 2>/dev/null || true)

  echo "==> 7. Firmando bundle principal $APP_BUNDLE..."
  codesign --force --verify --verbose --timestamp \
    --options runtime \
    --entitlements "$ENTITLEMENTS_MAS" \
    --sign "$MAS_APP_IDENTITY" \
    "$APP_BUNDLE"

  echo "==> 8. Verificando firma profunda..."
  codesign --verify --deep --strict --verbose=2 "$APP_BUNDLE"
else
  echo "==> (Omitiendo firma MAS: define MAS_APP_IDENTITY para firmar para App Store)"
fi

if [[ -n "${MAS_INSTALLER_IDENTITY:-}" ]]; then
  VERSION="$(plutil -extract CFBundleShortVersionString raw -o - "$APP_BUNDLE/Contents/Info.plist")"
  PKG_PATH="dist/BoardComposer-${VERSION}.pkg"
  echo "==> 9. Generando paquete instalador $PKG_PATH..."
  productbuild \
    --component "$APP_BUNDLE" /Applications \
    --sign "$MAS_INSTALLER_IDENTITY" \
    "$PKG_PATH"
  pkgutil --check-signature "$PKG_PATH"
  echo "==> Paquete listo para Transporter / App Store Connect: $PKG_PATH"
fi

echo "==> Build finalizado: $APP_BUNDLE"
