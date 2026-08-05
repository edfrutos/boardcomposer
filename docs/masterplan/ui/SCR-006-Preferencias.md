# SCR-006 — Preferencias

**Módulo:** BoardComposer Studio

**Código:** SCR-006  
**Versión:** 1.1.0  
**Estado:** Alineado con Studio  
**Última revisión:** 24/07/2026

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

Persistencia: `~/.boardcomposer/preferences.json` (fuera del proyecto).

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
│                retales                                     │
│ Avanzado       máx. soluciones · abrir ~/.boardcomposer/   │
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
| Unidades | `mm` / `cm` / `in` (interno siempre mm) |

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

### Avanzado

| Campo | Notas |
| --- | --- |
| Máx. soluciones | 1–100 (default 20); trunca ranking tras calcular |
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
- Sin perfiles / sync en la nube / import-export del JSON de prefs.
- Tema **sistema**: el diálogo Preferencias sigue el chrome de la plataforma
  (sin root LIGHT scoped; Industrial completo solo en claro/oscuro). Ver
  `docs/DESIGN.md`.

---

## Evolución prevista

- Perfiles de preferencias e import/export.
- Controles de rendimiento / depuración si hacen falta operativamente.
