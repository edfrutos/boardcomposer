#!/usr/bin/env bash
# captura-boardcomposer.sh — Captura la ventana de BoardComposer Studio a
# 2880×1800 px o 1440×900 px (16:10) para la ficha de la Mac App Store.
#
# Redimensiona la ventana a 1440×900 puntos y captura ese rectángulo. En una
# pantalla Retina salen 2880×1800 px; en una no Retina, 1440×900 px (ambos
# tamaños oficiales aceptados por App Store Connect).
#
# USO:
#   scripts/captura-boardcomposer.sh <nombre>   # → ~/Desktop/appstore-<nombre>.png
#   scripts/captura-boardcomposer.sh --sin-redimensionar <nombre>
#
# Con --sin-redimensionar no mueve ni redimensiona nada: pone la app en primer
# plano, busca la ventana de la app que ya mide 1440×900 y captura su
# rectángulo con todo lo que haya encima (diálogos modales como Explicar
# candidata, Exportar, Catálogo de materiales o el panel de Guardar).
# Haz antes una captura normal para dejar la ventana principal en 1440×900 y
# después abre el diálogo/panel.
#
# Requisitos:
#   - La app abierta (`open dist/BoardComposer.app` o `make run`).
#   - Permiso de Accesibilidad para Terminal/iTerm (Ajustes del Sistema →
#     Privacidad y seguridad → Accesibilidad), para mover/redimensionar.
#   - Permiso de Grabación de pantalla para Terminal/iTerm, para capturar.
#   - Una pantalla de al menos 1440×900 puntos libres bajo la barra de menús.
set -euo pipefail

RESIZE=1
if [[ "${1:-}" == "--sin-redimensionar" ]]; then
	RESIZE=0
	shift
fi
NAME="${1:?Uso: $0 [--sin-redimensionar] <nombre>   (p. ej. 1-workspace)}"
WIDTH=1440
HEIGHT=900
OUT="${HOME}/Desktop/appstore-${NAME}.png"

# Autodetecta el nombre del proceso en System Events si no se definió PROCESS.
if [[ -z "${PROCESS:-}" ]]; then
	PROCESS="$(osascript <<'OSA'
tell application "System Events"
	repeat with candidate in {"BoardComposer", "BoardComposer Studio", "Python", "python3.13"}
		if exists (process (contents of candidate)) then
			return contents of candidate
		end if
	end repeat
	return ""
end tell
OSA
	)"
	if [[ -z "${PROCESS}" ]]; then
		echo "Error: no se encontró ningún proceso abierto de BoardComposer." >&2
		echo "Abre primero la app con: open dist/BoardComposer.app (o make run)" >&2
		exit 1
	fi
fi

if ((RESIZE)); then
	geometry="$(osascript <<OSA
tell application "System Events" to tell process "${PROCESS}"
	set frontmost to true
	delay 0.3
	set position of front window to {20, 40}
	set size of front window to {${WIDTH}, ${HEIGHT}}
	delay 0.5
	set {x, y} to position of front window
	set {w, h} to size of front window
	return (x as text) & "," & (y as text) & "," & (w as text) & "," & (h as text)
end tell
OSA
	)"
else
	geometry="$(osascript <<OSA
tell application "System Events" to tell process "${PROCESS}"
	set frontmost to true
	delay 0.3
	repeat with win in windows
		set {w, h} to size of win
		if w is ${WIDTH} and h is ${HEIGHT} then
			set {x, y} to position of win
			return (x as text) & "," & (y as text) & "," & (w as text) & "," & (h as text)
		end if
	end repeat
	return ""
end tell
OSA
	)"
	if [[ -z "${geometry}" ]]; then
		echo "Error: ninguna ventana de «${PROCESS}» mide ${WIDTH}×${HEIGHT} puntos." >&2
		echo "Cierra el diálogo/panel, haz una captura normal para dejar la ventana" >&2
		echo "principal a esa medida y vuelve a abrir el diálogo." >&2
		exit 1
	fi
fi
IFS=, read -r x y w h <<<"${geometry}"

if ((w != WIDTH || h != HEIGHT)); then
	echo "Error: la ventana ha quedado en ${w}×${h} puntos, no ${WIDTH}×${HEIGHT}." >&2
	echo "La pantalla es demasiado pequeña: elige «Más espacio» en Ajustes del" >&2
	echo "Sistema → Pantallas, o usa un monitor externo." >&2
	exit 1
fi

# Deja que la app termine de redibujar tras el cambio de tamaño / foco.
sleep 0.8
screencapture -x -R"${x},${y},${w},${h}" "${OUT}"

px_w="$(sips -g pixelWidth "${OUT}" | awk '/pixelWidth/ {print $2}')"
px_h="$(sips -g pixelHeight "${OUT}" | awk '/pixelHeight/ {print $2}')"

# Si la pantalla tiene un factor de escala intermedio, normaliza a tamaño MAS.
case "${px_w}x${px_h}" in
2880x1800 | 2560x1600 | 1440x900 | 1280x800) ;;
*)
	echo "Normalizando resolución de ${px_w}×${px_h} a 2880×1800 px para Mac App Store..."
	sips -z 1800 2880 "${OUT}" >/dev/null
	px_w=2880
	px_h=1800
	;;
esac

echo "Captura lista (${PROCESS}): ${OUT} (${px_w}×${px_h} px)"
