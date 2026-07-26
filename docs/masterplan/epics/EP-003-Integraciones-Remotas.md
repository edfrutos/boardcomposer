# EP-003 — Integraciones y servicios remotos

**Épica:** EP-003  
**Fase:** 3 — Plataforma  
**Estado:** 🔵 Planificada  
**Prioridad:** P2  
**Ideas:** IDE-0006 (extensión), exportadores avanzados  
**Docs:** DOC-008, EP-001, EP-002  

**Creada:** 26/07/2026  

---

## Objetivo

Adaptar los contratos `v1` a **canales de integración** (HTTP u otros) y
a consumidores externos (ERP, pipelines, almacenamiento), sin acoplar el
Core a un vendor concreto.

---

## Fuera de alcance

- Marketplace / plugins de terceros (Fase 5).
- IA (Fase 4).
- Multi-tenant SaaS completo.

---

## Entregables

1. **Adaptador HTTP opcional** (si hay demanda piloto)  
   Thin layer sobre EP-001: health, solve, export; OpenAPI publicado.
2. **Hooks de integración**  
   Webhooks o escritura a rutas/credenciales configurables tras un job
   (local o remoto).
3. **Auth mínima**  
   Token/API key o mTLS documentado; sin SSO complejo en el primer corte.
4. **Límites y observabilidad**  
   Timeouts, tamaño de payload, logs correlacionables (ADR-003 eventos).
5. **Doc de despliegue**  
   Contenedor o servicio de referencia (opcional) + amenazas/mitigaciones.

---

## Dependencias

- EP-001 obligatorio.
- EP-002 recomendable (mismos jobs detrás del adaptador).

---

## Criterios de aceptación

- Un cliente HTTP (o integración acordada) completa solve+export vía
  contrato versionado.
- Credenciales no viven en el repo; se cargan por entorno/config.
- Fallos del adaptador no corrompen el Core ni proyectos locales.

---

## Notas de diseño

Si no hay piloto externo concreto, esta épica permanece 🔵 hasta que
EP-001/002 estén estables. No inventar cloud por inercia.
