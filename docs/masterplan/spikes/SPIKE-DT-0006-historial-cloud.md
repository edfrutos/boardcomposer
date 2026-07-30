# SPIKE — DT-0006 Historial cloud / multi-usuario `.bcproj`

**Código:** SPIKE-DT-0006  
**Deuda:** [DT-0006](../DOC-006-DeudaTecnica.md)  
**Fecha:** 2026-07-30  
**Estado:** Spike documentado (sin implementación)

---

## Contexto

Studio ya persiste un **anillo local** de revisiones al guardar:

- Módulo: `boardcomposer.io.bcproj_revisions`
- Sidecar: `.<nombre>.bcproj.revs/` junto al `.bcproj`
- Capacidad: `MAX_REVISIONS = 5`
- UI: comparar revisiones / diff local (FLW-006)

**DT-0006** pide historial **cloud / multi-usuario**. El anillo local cubre
mono-usuario offline; no cubre colaboración ni auditoría remota.

---

## Pregunta del spike

¿Qué alcance mínimo de “historial cloud” aporta valor sin inventar SaaS?

---

## Opciones (comparación)

| Opción | Idea | Pros | Contras | Esfuerzo |
|--------|------|------|---------|----------|
| **A. Git remoto** | Usuario versiona `.bcproj` (+ opcional `.revs/`) en Git | Cero backend propio; familiar | Diff binario/JSON ruidoso; no UX Studio; requiere disciplina | Bajo |
| **B. Sync de anillo** | Subir/bajar snapshots del sidecar a object storage (S3/GCS) con API key | Reutiliza modelo local; backup | Conflictos multi-escritor; auth; no “merge” semántico | Medio |
| **C. Servidor de revisiones** | API `POST/GET /v1/projects/{id}/revisions` sobre EP-003 | Auditoría, multi-usuario real | SaaS: identidad, ACL, cuota, retención | Alto |
| **D. Solo export periódico** | Hook batch/HTTP guarda copia en carpeta remota montada | Simple ops | Sin timeline UI; sin concurrencia | Bajo |

---

## Recomendación

**Corto plazo (ahora):** **no implementar cloud**. Mantener DT-0006 ⚪ Planificada.

**Si hay piloto mono-equipo con backup:** empezar por **D** o **A** (ops, no código Core).

**Si hay piloto multi-usuario real:** abrir épica dedicada con **C** (identidad + ACL), no extender el anillo local a “falso cloud”.

**Evitar B** salvo backup personal: mezcla peor de A y C (conflictos sin UX).

---

## Criterios para salir de “Planificada”

1. Piloto nombrado (quién escribe concurrente, cuántos puestos).
2. Decisión A/C/D registrada en DOC-005.
3. Amenazas HTTP/ACL actualizadas en DOC-010 si se elige C.
4. Spike cerrado → IDE + EP o se descarta explícitamente.

---

## Fuera de alcance de este spike

- Implementación de sync, OAuth, CRDT o merge de layouts.
- Cambiar `MAX_REVISIONS` del anillo local (ajuste aparte si hace falta).

---

## Relacionados

- `DOC-006` DT-0006  
- `DOC-003` / `DOC-004` próximo foco  
- `FLW-006` editar proyecto / revisiones locales  
- `EP-003` (HTTP) — no implica historial de proyecto por sí solo  
