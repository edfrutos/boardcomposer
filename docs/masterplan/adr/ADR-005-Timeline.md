
# ADR-005 — El Timeline como representación del sistema

| Campo | Valor |
|--------|-------|
| Estado | ✅ Aceptado |
| Fecha | 01/07/2026 |
| Decisor | Equipo de Arquitectura |
| Impacto | Alto |
| Revisión | N/A |

---

## Contexto

BoardComposer no solo debe generar soluciones; también debe permitir comprender cómo se han obtenido. Para ello es necesario disponer de una representación cronológica y reproducible de los acontecimientos relevantes ocurridos durante la vida de un proyecto.

---

## Problema

Los algoritmos de optimización suelen comportarse como una "caja negra": el usuario únicamente ve el resultado final y desconoce el proceso seguido para alcanzarlo.

Alternativas consideradas:

1. Mostrar únicamente el resultado final.
2. Implementar un registro técnico orientado al desarrollador.
3. Construir un Timeline visual basado en los eventos del sistema.

---

## Decisión

Se adopta la tercera alternativa.

BoardComposer dispondrá de un **Timeline** construido a partir de los eventos publicados por el sistema. El Timeline será una representación visual del historial del proyecto y permitirá reproducir, analizar y comprender la evolución de cada operación sin introducir una lógica paralela.

El Timeline consumirá eventos; no generará reglas de negocio.

---

## Consecuencias

### Ventajas

- Explicabilidad de los algoritmos.
- Depuración simplificada.
- Historial cronológico unificado.
- Base para auditorías y formación.
- Reutilización del Event Bus existente.

### Inconvenientes

- Necesidad de mantener un catálogo de eventos estable.
- Posible incremento del volumen de información almacenada.

---

## Principios derivados

- El Timeline refleja hechos ocurridos, nunca estados hipotéticos.
- Toda entrada del Timeline procede de uno o varios eventos registrados.
- El Timeline podrá filtrarse por tipo de evento, algoritmo o intervalo temporal.
- La reproducción nunca modificará el estado del proyecto.

---

## Impacto

Esta decisión afecta a Studio, Event Bus, Inspector, Comparador, sistema de auditoría, IA explicativa y futuras herramientas de análisis.

---

## Relación con otros documentos

- ADR-003 — Arquitectura basada en eventos.
- SCR-002 — Workspace.
- SCR-003 — Comparador.
- SCR-004 — Inspector.
- FLW-003 — Generar Soluciones.

---

## Revisión futura

En versiones posteriores el Timeline permitirá reproducción paso a paso de algoritmos, marcadores, anotaciones del usuario, comparación sincronizada entre soluciones, métricas temporales y exportación del historial para análisis o soporte técnico.

**Estado 2026-07-17:** MVP en Studio — dock Timeline con hechos del Event Bus (filtro, vaciado).

**Estado 2026-07-17 (c):** reproducción paso a paso de colocaciones de la solución seleccionada (Inicio / ◀ / ▶ / Play), sin mutar el proyecto. La reproducción a nivel de algoritmo interno sigue pendiente.

**Estado 2026-07-17 (e):** Comparador sincronizado con el replay de colocaciones (diff parcial por paso vs referencia).
**Estado 2026-07-17 (f):** traza de fases del solver (`SolveTrace`) publicada en el Timeline; el replay muestra algoritmo y pieza. Instrumentación de intentos fallidos internos sigue pendiente.
**Estado 2026-07-17 (g):** exportación del historial del Timeline a JSON/CSV (filtro activo respetado).
**Estado 2026-07-17 (h):** MaxRects registra fallos de colocación (`incompatible` / `no_fit`) en `SolveTrace` y el Timeline (muestra deduplicada + resumen).
**Estado 2026-07-17 (i):** filtro del Timeline por algoritmo (además del tipo de evento) y duración en ms de generadores/evaluación (`duration_ms`).
**Estado 2026-07-17 (j):** marcadores/anotaciones de usuario (`TimelineMarked`) vía Event Bus, con contexto opcional del replay (algoritmo, pieza, paso).
**Estado 2026-07-17 (k):** filtro del Timeline por intervalo temporal (presets: 1/5/15 min, 1 h) además de tipo de evento y algoritmo.
**Estado 2026-07-17 (l):** Skyline registra fallos `no_fit` en `SolveTrace` / Timeline; el pipeline captura fallos de todos los generadores instrumentados.
