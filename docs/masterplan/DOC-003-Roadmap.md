# BoardComposer

## Documento 3 — Roadmap del Producto

**Código:** DOC-003
**Versión:** 1.1.0
**Estado:** En revisión — actualizado
**Fecha de creación:** 01/07/2026
**Última revisión:** 16/07/2026

---

## Objetivo

Definir la evolución prevista de BoardComposer mediante fases, hitos y prioridades, proporcionando una visión clara del desarrollo del producto a corto, medio y largo plazo.

---

## Principios

El Roadmap representa la dirección del proyecto, no una planificación cerrada. Podrá evolucionar conforme aparezcan nuevas necesidades, siempre respetando el Manifiesto y la Arquitectura.

---

# Fase 1 — Core (Completada)

**Estado:** 🟢

Objetivos alcanzados:

- Motor de optimización desacoplado.
- Algoritmos Skyline y MaxRects.
- Beam Search.
- Sistema de evaluación.
- Exportadores básicos.
- Cobertura amplia mediante pruebas automatizadas.
- Pipeline común de validación, evaluación, ranking y diagnósticos.
- Primera vertical de packing multipanel con MaxRects.

La base del Core está completada, pero continúa recibiendo extensiones
controladas que preservan sus contratos públicos.

---

# Fase 2 — BoardComposer Studio (En curso)

**Estado:** 🟡

Objetivo:

Construir la aplicación visual profesional para explorar, comparar y comprender soluciones de corte.

Entregables principales:

- Workspace y cámara: funcionales.
- Selección, inspector y comandos undo/redo: funcionales.
- Gestión y persistencia de proyectos: funcionales.
- Exploración de varias soluciones y diagnósticos: funcionales.
- Exportación SVG: funcional, incluido multipanel.
- Representación básica de varios paneles: funcional.
- Comparador visual avanzado: en desarrollo.
- UAT visual multipanel: siguiente bloque.

---

# Fase 3 — Plataforma

**Estado:** ⚪ Planificada

Incluye:

- API pública.
- Automatización.
- Integraciones.
- Servicios remotos.

---

# Fase 4 — Inteligencia

**Estado:** ⚪ Idea consolidada

Objetivos:

- Asistencia mediante IA.
- Explicaciones inteligentes.
- Recomendación automática de estrategias.
- Análisis avanzado de soluciones.

---

# Fase 5 — Ecosistema

**Estado:** ⚪ Visión futura

Objetivos:

- Plugins.
- Marketplace.
- Biblioteca de materiales.
- Comunidad.

---

## Prioridades actuales

### Prioridad P0

- UAT visual multipanel.
- Flujo completo de trabajo en Studio.
- Movimiento y reasignación interactiva entre paneles.

### Prioridad P1

- Comparador visual avanzado.
- Importación de inventario multipanel.
- Exportadores avanzados.
- Cobertura automatizada de interacción Qt.

### Prioridad P2

- IA.
- Plugins.
- Cloud.

---

## Criterios para modificar el Roadmap

Toda modificación deberá:

- aportar valor al usuario;
- mantener la coherencia con el Manifiesto;
- respetar la arquitectura definida;
- quedar registrada en el historial de decisiones.

---

## Estado

**Estado actual:** 🟡 Fase 2 en curso; documento actualizado

Pendiente de:

- descomponer las fases en épicas (EP);
- vincular los futuros sprints;
- incorporar estimaciones y dependencias;
- aprobar como hoja de ruta oficial del proyecto.
