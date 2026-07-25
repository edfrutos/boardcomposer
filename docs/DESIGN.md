# BoardComposer Studio — DESIGN

**Registro:** product (herramienta de taller)  
**Dirección:** Industrial madera  
**Alcance actual:** chrome QSS + pantalla de inicio + canvas/workspace

## Escena

Carpintero/tallador frente al monitor en un taller con luz diurna. La UI
sirve al oficio: clara, cálida, sin look SaaS ni CAD genérico azul.

## Color (restrained)

Neutros cálidos tintados + acento ámbar herramienta ≤10% del chrome.

| Token | Light | Dark |
|---|---|---|
| window | `#f3ebe1` | `#1f1b17` |
| base | `#faf6f0` | `#2a241f` |
| panel | `#e8ddd0` | `#342c25` |
| text | `#2c241c` | `#ebe1d4` |
| muted | `#6b5c4d` | `#a89480` |
| border | `#c9b8a4` | `#4a3f34` |
| accent | `#c47a1a` | `#d4922a` |
| accent_text | `#1a1410` | `#1a1410` |

CTA primario: tinta oscura sobre ámbar (WCAG AA ≥4.5:1). Evitar crema
sobre ámbar en light (quedaba ~3.2:1).

Fuente de verdad: `studio/theme_tokens.py`. Aplicación: `studio/theme.py`
(`QPalette` + QSS). Preferencia `system` limpia el stylesheet (Welcome pierde
tipografía de marca hasta elegir light/dark).

## Accesibilidad (chrome)

- Focus visible en `QPushButton` / toolbar / listas (`border` acento).
- CTAs Welcome primarios ≥44px; secundarios ≥36px; vaciar recientes ≥32px.
- Banner outdated usa fondo `window` para contraste del danger en dark.

## Canvas / workspace

Colores de tablero, pieza, selección, válido/inválido y grid viven en
`CanvasColors` (`LIGHT_CANVAS` / `DARK_CANVAS`) y se activan con el tema vía
`studio.workspace.canvas_style`. `system` usa el canvas claro (taller diurno).

| Rol | Light | Dark |
|---|---|---|
| background | `#e8ddd0` | `#1f1b17` |
| board_fill | `#faf6f0` | `#342c25` |
| piece_fill | `#edd5a8` | `#4a3828` |
| piece_stroke | `#a86512` | `#d4922a` |
| selected_stroke | `#b42318` | `#f04438` |
| grid | `#d4c4b0` | `#4a3f34` |

## Tipografía

| Rol | Familia | Notas |
|---|---|---|
| Marca | Archivo (bundled) | Hero `QLabel#welcomeBrand` |
| UI | Source Sans 3 (bundled) | Cuerpo y controles |
| Énfasis | Source Sans 3 SemiBold | Headers, primario |

Fuentes OFL en `studio/assets/fonts/`.

## Componentes clave

- `QPushButton#primaryButton` — CTA principal (ámbar + `accent_text` tinta).
- Welcome: marca hero + tagline + CTAs; recientes en columna secundaria;
  `welcomeClearRecent` con hover/focus propios.
- Workspace: tableros/piezas/grid/selección con tokens Industrial madera
  (sin azul Tailwind legacy).
- SVG de exportación y miniaturas (inicio, comparador, preview) usan
  `DEFAULT_SVG_PALETTE` alineada a `LIGHT_CANVAS`.
