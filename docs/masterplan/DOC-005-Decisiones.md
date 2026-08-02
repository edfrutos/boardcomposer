# BoardComposer

## Documento 5 — Registro de Decisiones

**Código:** DOC-005
**Versión:** 1.1.0
**Estado:** En revisión — actualizado
**Fecha de creación:** 01/07/2026
**Última revisión:** 16/07/2026

---

## Objetivo

Registrar de forma permanente todas las decisiones estratégicas, funcionales y arquitectónicas que afecten al desarrollo de BoardComposer.

Este documento actúa como índice del conocimiento acumulado del proyecto y evita que decisiones importantes dependan de la memoria de sus desarrolladores.

---

## Principios

- Toda decisión relevante debe quedar documentada.
- Las decisiones nunca se eliminan; pueden quedar sustituidas o marcadas como obsoletas.
- Cada decisión debe poder justificarse en su contexto.
- Las decisiones importantes podrán ampliarse mediante un ADR (Architecture Decision Record).

---

## Formato de una decisión

```text
DEC-XXXX

Título

Fecha

Estado

Contexto

Alternativas consideradas

Decisión adoptada

Justificación

Consecuencias

Documentos relacionados
```

---

## Registro inicial

| ID | Título | Estado |
|----|--------|--------|
| DEC-0001 | El Core será independiente de cualquier interfaz | ✅ Vigente |
| DEC-0002 | BoardComposer será una plataforma multiplataforma | ✅ Vigente |
| DEC-0003 | El usuario explorará soluciones en lugar de ejecutar un único «Resolver» | ✅ Vigente |
| DEC-0004 | Toda funcionalidad comenzará en el Core antes de llegar a cualquier interfaz | ✅ Vigente |
| DEC-0005 | El proyecto utilizará un Master Plan versionado como referencia oficial | ✅ Vigente |
| DEC-0006 | Las colocaciones multipanel usan referencias físicas y coordenadas locales | ✅ Vigente |
| DEC-0007 | Las migraciones de `.bcproj` son explícitas y versionadas (ADR-015) | ✅ Vigente |
| DEC-0008 | Los retales se reportan como información, no como inventario (ADR-016) | ✅ Vigente |
| DEC-0009 | Una solución parcial (piezas omitidas) es válida; solo fallan motivos duros | ✅ Vigente |
| DEC-0010 | Piloto DT-0006: backup de revisiones (opción D), sin cloud multi-usuario | ✅ Vigente |
| DEC-0011 | IDE-0007 arranca con explicación determinista; LLM solo opt-in | ✅ Vigente |

---

## Relación con ADR

Las decisiones que requieran un análisis técnico más profundo se desarrollarán en documentos independientes dentro de `docs/masterplan/adr/`.

Este documento actúa como índice de dichas decisiones y como referencia histórica del proyecto.

---

## Normas de mantenimiento

- Toda decisión aprobada recibirá un identificador permanente.
- Las modificaciones deberán crear una nueva versión de la decisión o un ADR relacionado, nunca sobrescribir el contexto original.
- Ninguna decisión histórica será eliminada.

---

## Estado

**Estado actual:** 🟡 En revisión — ADR-001 a ADR-014 registrados

Pendiente de:

- enlazar decisiones con los documentos DOC-000 a DOC-004;
- incorporar referencias cruzadas con futuras Épicas y Sprints.
