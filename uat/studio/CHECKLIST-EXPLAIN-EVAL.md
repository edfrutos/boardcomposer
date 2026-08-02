# UAT — Eval humana Explicar candidata (IDE-0007 MVP)

**Spike:** [`SPIKE-IDE-0007`](../../docs/masterplan/spikes/SPIKE-IDE-0007-asistente-ia.md)  
**Objetivo:** 5 candidatas del demo → ¿explicación útil o ruido?  
**Atajo:** **Ctrl+Alt+E** (o Ayuda → Explicar candidata…)

## Preparación

1. `make run` → Welcome → **Proyecto demo**.
2. **Calcular layout** hasta ≥2 candidatas en el Comparador.
3. Si solo hay 1: Preferencias → subir máx. soluciones y recalcular
   (el demo suele pedir ≥2).

## Rúbrica (por candidata)

| Nota | Criterio |
| --- | --- |
| **Útil** | Fortalezas/debilidades/notas ayudan a decidir o descartar. |
| **Ruido** | Genérico, vacío, contradictorio o irrelevante para elegir. |
| **Mixto** | Algo útil + algo sobrante (anotar qué). |

Marca también si **Copiar** deja texto coherente en el portapapeles.

## Tabla de evaluación

| # | Candidata (índice / tip status) | Útil | Mixto | Ruido | Copiar OK | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | □ | □ | □ | □ | |
| 2 | | □ | □ | □ | □ | |
| 3 | | □ | □ | □ | □ | |
| 4 | | □ | □ | □ | □ | |
| 5 | | □ | □ | □ | □ | |

Navega con **Re Pág** / **Av Pág** o miniaturas del Comparador; abre Explicar
en cada una.

## Veredicto

- [ ] ≥4/5 **Útil** o **Mixto** → MVP explicación aceptable para estudio.
- [ ] ≥2/5 **Ruido** → anotar fallos; no cablear LLM hasta revisar texto Core.
- Fecha / evaluador: _______________

**Fuera de alcance:** calidad de un LLM futuro (solo texto determinista actual).
