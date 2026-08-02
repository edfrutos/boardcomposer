# SPIKE — IDE-0007 Asistente IA (bajo demanda)

**Código:** SPIKE-IDE-0007  
**Idea:** [IDE-0007](../DOC-004-Backlog.md)  
**Fecha:** 2026-08-02  
**Estado:** Spike + MVP local (sin LLM cloud)

---

## Pregunta

¿Qué primer caso de IA aporta valor sin filtrar proyectos a un proveedor?

---

## Decisión de arranque (DEC-0011)

1. **MVP ahora:** explicación **determinista** de la candidata seleccionada
   (`SolutionExplanation` del Core + diálogo Studio). Sin red, sin API key.
2. **LLM opcional (fase siguiente):** solo con opt-in explícito; payload mínimo
   (métricas / texto de explicación), **nunca** `.bcproj` completo por defecto.
3. Core permanece libre de Qt y de SDKs de proveedores.

---

## Criterios de aceptación MVP

- [x] Formateo de fortalezas / debilidades / notas reutilizable.
- [x] Ayuda → **Explicar candidata…** (enablement si hay solución seleccionada;
  atajo **Ctrl+Alt+E**).
- [x] Botón **Copiar** + confirmación en status bar; tip en el botón.
- [ ] Eval humana: 5 candidatas demo → explicación útil vs ruido
  ([checklist UAT](../../../uat/studio/CHECKLIST-EXPLAIN-EVAL.md)).
- [ ] LLM: ADR + política datos + prompt/eval plan antes de cablear proveedor.

---

## Fuera de alcance MVP

- Chat libre, generación de layout por prompt, plugins de modelo.
- Envío automático de inventario/cliente a cloud.

---

## Relacionados

- `domain/explanation.py`, `domain/explain_text.py`
- `solver/evaluation.py` (fortalezas/debilidades)
- DEC-0011 en DOC-005
