# BoardComposer Studio

## SCR-001 — Pantalla de Inicio

**Código:** SCR-001  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 02/08/2026

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
│                                            │  (clic / Enter → abrir)         │
│ CTAs:                                      │                                 │
│   Nuevo proyecto                           │                                 │
│   Abrir proyecto…                          │                                 │
│   Importar piezas (CSV/Excel)…             │                                 │
│   Proyecto de ejemplo                      │                                 │
│   Desde plantilla…                         │                                 │
│   Documentación…                           │                                 │
│   Novedades…                               │                                 │
│   Preferencias…                            │                                 │
│   Atajos… / Acerca de…                     │                                 │
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
| Atajos… | Diálogo atajos (**F1**; misma entrada que Ayuda) |
| Acerca de… | Diálogo About (**Ctrl+Shift+A**) |

Fila help (tercera): Atajos / Acerca de, sin abarrotar la fila secundaria.

### Proyectos recientes

- Persistencia: `~/.boardcomposer/recent_files.json` (máx. 10).
- Por entrada: miniatura SVG del layout guardado, nombre, fecha
  `YYYY-MM-DD HH:MM`, ruta completa.
- Abrir: **clic** o **Enter**.
- Anclar / desanclar: menú contextual (★ arriba; persiste en
  `recent_files.json`).
- Quitar uno: **Delete** / **Backspace** o menú contextual «Quitar de
  recientes» (sin confirmación; el archivo en disco no se borra).
- Vaciar lista: botón en cabecera + confirmación (también
  **Ctrl+Shift+X** / menú Archivo).
- Fantasmas: se podan al refrescar o al fallar la apertura.

---

## Flujo principal

1. Abrir Studio → welcome.
2. Elegir reciente, nuevo, demo, plantilla o importar piezas.
3. Pasar al Workspace (SCR-002) con el proyecto activo.

---

## Criterios de aceptación

- Arranque muestra welcome sin wizard extra.
- Brand legible como señal principal del primer viewport.
- Recientes con miniatura y fecha; abrir en un gesto (clic / Enter);
  anclar / quitar uno con menú contextual (Delete quita).
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

- Sin cloud / búsqueda global en welcome.

---

## Evolución prevista

- (ninguna abierta para Welcome; metadatos / cloud fuera de SCR-001).
