# SCR-006 — Preferencias

**Módulo:** BoardComposer Studio

**Código:** SCR-006  
**Versión:** 1.9.0  
**Estado:** Alineado con Studio  
**Última revisión:** 22/09/2026

---

## Objetivo

Preferencias del **usuario** (entorno habitual), independientes del `.bcproj`.
No sustituyen la configuración de inventario ni colocaciones del proyecto.

---

## Filosofía

Las preferencias pertenecen al usuario.  
Los proyectos pertenecen al trabajo.

Así un `.bcproj` se puede compartir sin arrastrar tema, idioma o pesos de
scoring personales.

---

## Acceso

- **Editar → Preferencias…**
- Botón en pantalla de inicio (SCR-001)
- Atajo **Ctrl+,**

Persistencia: `~/.boardcomposer/preferences.json` y
`~/.boardcomposer/material_catalog.json` (fuera del proyecto).
Export/import del catálogo recuerda `last_material_catalog_directory`.

---

## Distribución actual

Diálogo modal **sin pestañas**: cinco grupos apilados + OK / Cancelar /
Restaurar valores por defecto.

```text
┌────────────────────────────────────────────────────────────┐
│ Preferencias                                               │
├────────────────────────────────────────────────────────────┤
│ General        idioma · tema · unidades                    │
│ Workspace      cuadrícula on/off · tamaño (mm)             │
│ Algoritmos     estrategia · pesos custom (4)               │
│ Exportación    formato default · métricas/explicación/     │
│                retales · etiquetas piezas/retales · cotas  │
│                · trazabilidad · DPI/calidad JPEG           │
│                · mano de obra EUR/h y min/pieza            │
│ Avanzado       máx. soluciones · kerf default · catálogo   │
│                · abrir ~/.boardcomposer/                   │
├────────────────────────────────────────────────────────────┤
│              [Restaurar]  [Cancelar]  [OK]                 │
└────────────────────────────────────────────────────────────┘
```

---

## Campos implementados

### General

| Campo | Valores |
| --- | --- |
| Idioma | `es` / `en` |
| Tema | sistema / claro / oscuro |
| Unidades | `mm` / `cm` / `in` (interno siempre mm; Inspector y plano TEXT) |

### Workspace

| Campo | Notas |
| --- | --- |
| Mostrar cuadrícula | Toggle en vista (**Ctrl+G**); persiste al instante |
| Tamaño de cuadrícula | 10–500 mm (paso 10) |

### Algoritmos

| Campo | Notas |
| --- | --- |
| Estrategia | `balanced` / `material` / `compact` / `exact` |
| Pesos custom | Spins 0–100: material, placed, compactness, rotation_penalty |
| Sin custom | Spins deshabilitados; usan preset de la estrategia |

### Exportación (defaults SCR-007)

| Campo | Notas |
| --- | --- |
| Formato | `svg` / `dxf` / `pdf` / `json` / `csv` |
| Incluir métricas / explicación / retales | Checkboxes |
| Etiquetas de piezas / retales | Checkboxes; planos SVG/PDF/DXF |
| Cotas L×A del tablero | Checkbox; planos SVG/PDF/DXF; default sí |
| Trazabilidad (versión, algoritmo, fecha) | Checkbox; planos SVG/PDF/DXF y PDF de lista de corte / presupuesto; default sí |
| Papel / orientación / escala / márgenes PDF | Solo plano PDF; default ajustar al dibujo |
| Resolución PNG/JPEG | DPI 36–300; default 96 |
| Calidad JPEG | 1–100; default 90; solo JPEG |
| Lote de candidatas | Checkbox; default no; requiere ≥2 soluciones |
| Mano de obra EUR/h | 0–999; default 0 = omitir en presupuesto PDF |
| Minutos por pieza | 0–180; default 0; piezas colocadas × min × tarifa |

### Avanzado

| Campo | Notas |
| --- | --- |
| Máx. soluciones | 1–100 (default 20); trunca ranking tras calcular |
| Catálogo de materiales | Editor (**Ctrl+Alt+T**); nombres, espesores, L×A y €/m² (0 = sin coste); export/import JSON (IDE-0042) |
| Exportar / importar preferencias | JSON de taller (IDE-0049); fusionar o reemplazar; sin rutas locales ni ventana; OK guarda |
| Abrir carpeta de datos | Revela `~/.boardcomposer/` |

No implementados (visión antigua): zoom inicial, guías/reglas/cotas, beam
width, caché, hilos, logs de depuración, búsqueda de preferencias.

---

## Comportamiento al aplicar

- **OK:** escribe `preferences.json` y aplica tema, i18n de UI, recarga
  workspace/explorador/soluciones afectadas.
- **Cancelar:** descarta cambios del diálogo.
- **Restaurar valores por defecto:** solo reinicia widgets; hace falta OK para
  persistir.
- **Importar preferencias:** aplica al diálogo; OK persiste. Carpetas
  locales y geometría de ventana no viajan en el JSON.
- Cambio de idioma **dentro** del diálogo: retraduce el propio diálogo; el
  resto de la app al confirmar OK.

---

## Flujo principal

1. Abrir Preferencias (**Ctrl+,**).
2. Ajustar grupos necesarios.
3. OK → persistir y refrescar UI afectada.
4. Calcular / exportar usando estrategia, `max_solutions` y defaults de export.

---

## Criterios de aceptación

- Preferencias no se mezclan con el `.bcproj`.
- Tema e idioma se reflejan tras OK sin reiniciar Studio.
- Unidades afectan Inspector / Explorador / formularios de tablero y pieza.
- `max_solutions` limita candidatas conservadas tras el ranking.
- Defaults de exportación alimentan SCR-007.

---

## Relación con otras pantallas

- SCR-001 — Inicio (acceso al diálogo).
- SCR-002 — Workspace (cuadrícula / unidades).
- SCR-003 — Comparador (`max_solutions`, scoring).
- SCR-005 — Proyecto (inventario ajeno a prefs).
- SCR-007 — Exportación (formato y flags por defecto).
- FLW-003 — Generar (progreso + cancelación; estrategia desde prefs).

---

## Límites conocidos (Studio actual)

- Sin pestañas ni búsqueda de preferencias.
- Export/import JSON de taller (IDE-0049); sin perfiles nombrados ni
  sync en la nube.
- Tema **sistema**: el diálogo Preferencias sigue el chrome de la plataforma
  (sin root LIGHT scoped; Industrial completo solo en claro/oscuro). Ver
  `docs/DESIGN.md`.

---

## Evolución prevista

- Perfiles nombrados de preferencias (export/import JSON entregado).
- Controles de rendimiento / depuración si hacen falta operativamente.
