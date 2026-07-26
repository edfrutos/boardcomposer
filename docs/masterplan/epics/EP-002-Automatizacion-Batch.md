# EP-002 — Automatización y batch

**Épica:** EP-002  
**Fase:** 3 — Plataforma  
**Estado:** 🔵 Planificada  
**Prioridad:** P1  
**Ideas:** IDE-0006 (soporte), CLI existente  
**Docs:** DOC-003, DOC-008, EP-001  

**Creada:** 26/07/2026  

---

## Objetivo

Permitir **jobs reproducibles sin UI**: lotes de proyectos, perfiles de
estrategia/export y salidas en carpetas, aptos para CI o scripts de taller.

---

## Fuera de alcance

- Orquestación cloud / colas remotas (EP-003).
- Scheduler GUI en Studio.

---

## Entregables

1. **CLI batch**  
   Entrada: carpeta o lista de `.bcproj` / CSV; salida: soluciones +
   exports en árbol de directorios.
2. **Perfiles**  
   Reutilizar preferencias/export templates (o equivalente headless) por
   nombre de perfil.
3. **Códigos de salida y logs**  
   Fallo por proyecto no tumba el lote entero; resumen final
   (ok / error / omitidos).
4. **Receta documentada**  
   Ejemplo `make` o script en `scripts/` + nota en README/docs.
5. **Tests**  
   Lote pequeño en CI (sin Qt) sobre fixtures existentes.

---

## Dependencias

- EP-001 (contratos `v1`) idealmente primero; puede arrancar sobre CLI
  actual si el contrato se congela en paralelo.
- Import CSV/Excel y exporters ya en Core/Studio.

---

## Criterios de aceptación

- Un directorio con N proyectos genera N carpetas de salida o un manifiesto.
- Estrategia y flags de export configurables sin editar código.
- Ejecutable en CI con `QT_QPA_PLATFORM` innecesario (sin Studio).

---

## Notas de diseño

Maximizar reuso del CLI y de `boardcomposer` como librería. Studio sigue
siendo la UI; el batch no duplica el solver.
