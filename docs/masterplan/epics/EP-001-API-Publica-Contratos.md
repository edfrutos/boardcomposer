# EP-001 — API pública y contratos versionados

**Épica:** EP-001  
**Fase:** 3 — Plataforma  
**Estado:** 🔵 Planificada  
**Prioridad:** P1  
**Ideas:** IDE-0006  
**Docs:** DOC-008, DOC-002, ADR-001, ADR-003  

**Creada:** 26/07/2026  

---

## Objetivo

Exponer capacidades del Core (proyecto, solve, métricas, export) como
**contratos públicos versionados**, consumibles sin depender de Studio ni
de detalles internos del solver.

---

## Fuera de alcance

- UI Studio nueva.
- Autenticación multi-tenant / nube (EP-003 / evolución).
- Plugins de terceros (Fase 5 / IDE-0008).

---

## Entregables

1. **Superficie estable Core→API**  
   Operaciones mínimas: cargar/validar proyecto, ejecutar layout,
   listar/rankear candidatas, exportar (SVG/JSON/CSV al menos).
2. **Contrato versionado**  
   Semver + ruta/paquete `v1` (p. ej. módulo Python público y/o esquema
   OpenAPI si hay HTTP). Cambios breaking → `v2`.
3. **Formatos de intercambio**  
   Documentar payload de proyecto (alineado a `.bcproj` / Core) y de
   solución (métricas, placements, offcuts informativos).
4. **Guía de integrador**  
   Ejemplo mínimo (script o notebook) que resuelve un proyecto sin Qt.
5. **Tests de contrato**  
   Suite que falle si se rompe la API pública sin bump de versión.

---

## Dependencias

- Core inmutable (ADR-001) y CLI/exportadores existentes.
- DOC-008 como visión; esta épica concreta el primer corte `v1`.

---

## Criterios de aceptación

- Un cliente externo puede resolver y exportar sin importar `studio.*`.
- Versión de API visible y documentada.
- Breaking change exige versión mayor o deprecación explícita.
- Cobertura de tests sobre los endpoints/funciones públicas `v1`.

---

## Notas de diseño

Preferir primero **API Python empaquetada** (reutiliza Core/CLI) y dejar
HTTP como adaptador opcional en EP-003, salvo que un piloto concreto
exija REST desde el día uno.
