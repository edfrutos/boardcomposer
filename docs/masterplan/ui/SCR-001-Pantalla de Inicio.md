# BoardComposer Studio

## SCR-001 — Pantalla de Inicio

**Código:** SCR-001  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 01/08/2026

---

## Objetivo

Punto de entrada a BoardComposer Studio: comenzar en segundos, recuperar
recientes y alcanzar las acciones principales sin pasar por el Workspace.

---

## Principios de diseño

- Brand-first: el nombre del producto domina el primer viewport.
- Una composición clara (hero + columna de recientes), no un dashboard.
- Acciones principales visibles sin scroll en desktop típico.
- Tema visual «Industrial madera» (tokens + QSS; tipografías Archivo / Source
  Sans 3).

---

## Distribución actual

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ welcomeRoot                                                                  │
├────────────────────────────────────────────┬─────────────────────────────────┤
│ Hero (brand-first)                         │ Proyectos recientes             │
│   BoardComposer                            │  [Vaciar lista]                 │
│   Studio {pyproject version}              │  · miniatura · nombre · fecha   │
│   tagline i18n                             │  · ruta completa                │
│                                            │  (doble clic / Enter → abrir)   │
│ CTAs:                                      │                                 │
│   Nuevo proyecto                           │                                 │
│   Abrir proyecto…                          │                                 │
│   Importar piezas (CSV/Excel)…             │                                 │
│   Proyecto de ejemplo                      │                                 │
│   Desde plantilla…                         │                                 │
│   Documentación…                           │                                 │
│   Novedades…                               │                                 │
│   Preferencias…                            │                                 │
└────────────────────────────────────────────┴─────────────────────────────────┘
```

Al arrancar, el stack central muestra el welcome delante del Workspace.
Volver: **Archivo → Pantalla de inicio** (**Ctrl+Shift+H**).

---

## Componentes

### Hero

- Marca `BoardComposer` (señal dominante).
- Subtítulo con versión de desarrollo.
- Tagline localizada (es/en).

### Acciones principales (CTAs)

| Botón | Efecto |
|-------|--------|
| Nuevo proyecto | Diálogo nuevo (SCR-005) |
| Abrir proyecto… | Diálogo `.bcproj` |
| Importar piezas (CSV/Excel)… | Flujo FLW-002 (piezas) |
| Proyecto de ejemplo | Demo (**Ctrl+Shift+D**) |
| Desde plantilla… | Picker de plantillas; info si el catálogo está vacío |
| Documentación… | Abre guía rápida usuario (`docs/user/GUIA-RAPIDA.md`) |
| Novedades… | Diálogo CHANGELOG (Unreleased) |
| Preferencias… | SCR-006 |

No hay CTA «Ayuda / Atajos / Acerca de» en el welcome (sí en menú Ayuda:
**F1**, **Shift+F1**, **Ctrl+Shift+A**).

### Proyectos recientes

- Persistencia: `~/.boardcomposer/recent_files.json` (máx. 10).
- Por entrada: miniatura SVG del layout guardado, nombre, fecha
  `YYYY-MM-DD HH:MM`, ruta completa.
- Abrir: **doble clic** o **Enter** (no clic simple).
- Vaciar lista: botón en cabecera + confirmación (también
  **Ctrl+Shift+X** / menú Archivo).
- Fantasmas: se podan al refrescar o al fallar la apertura; no hay botón
  «quitar» por fila.

---

## Flujo principal

1. Abrir Studio → welcome.
2. Elegir reciente, nuevo, demo, plantilla o importar piezas.
3. Pasar al Workspace (SCR-002) con el proyecto activo.

---

## Criterios de aceptación

- Arranque muestra welcome sin wizard extra.
- Brand legible como señal principal del primer viewport.
- Recientes con miniatura y fecha; abrir en un gesto (doble clic / Enter).
- Volver al welcome desde el Workspace con **Ctrl+Shift+H**.
- Tema claro/oscuro/sistema se aplica vía Preferencias (no selector en welcome).

---

## Relación con otras pantallas

- SCR-002 — Workspace.
- SCR-005 — Proyecto (nuevo/abrir/plantillas/import).
- SCR-006 — Preferencias.
- SCR-007 — Exportación (no desde welcome).
- Ayuda — Documentación / Novedades / Atajos / Acerca de.

---

## Límites conocidos (Studio actual)

- Abrir reciente exige doble clic o Enter (no clic único).
- Sin quitar individual de la lista de recientes en UI.
- Sin anclaje / cloud / búsqueda global en welcome.

---

## Evolución prevista

- Clic único o botón Abrir por fila.
- Quitar / anclar recientes.
- Acceso directo a Atajos / Acerca de desde welcome.
