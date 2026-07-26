# EP-002 — Automatización y batch

**Épica:** EP-002  
**Fase:** 3 — Plataforma  
**Estado:** 🟢 Completada (SPR-001…003)  
**Prioridad:** P1  
**Ideas:** IDE-0006 (soporte), CLI existente  
**Docs:** DOC-003, DOC-008, DOC-009, EP-001  

**Creada:** 26/07/2026  
**Última actualización:** 26/07/2026  

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

## Sprints

| ID | Título | Estado | Notas |
|----|--------|--------|-------|
| SPR-001 | CLI `boardcomposer-batch` + perfil JSON | 🟢 | `batch.py` / `batch_cli.py`; formats json/csv/svg; `manifest.json`; exit 0/1/2; `scripts/batch_samples.sh` |
| SPR-002 | Perfiles nombrados / plantillas export Studio | 🟢 | `--template` / `--client` + Core `io.export_templates`; sample `data/samples/export_templates.json` |
| SPR-003 | Lista explícita de paths + dry-run | 🟢 | `--list` / `-L` + `--dry-run`; sample `data/samples/batch_jobs.list` |

---

## Dependencias

- EP-001 (`boardcomposer.api.v1`) — load CSV/`.bcproj`, solve, export.
- Import CSV/Excel y exporters ya en Core.

---

## Criterios de aceptación

- Un directorio con N proyectos genera N carpetas de salida o un manifiesto.
- Estrategia y flags de export configurables sin editar código.
- Ejecutable en CI con `QT_QPA_PLATFORM` innecesario (sin Studio).

---

## Uso (SPR-001)

```bash
boardcomposer-batch \
  --input data/samples/batch_inbox \
  --output out/batch \
  --profile data/samples/batch_profile.json

# o
python -m boardcomposer.batch_cli -i data/samples/batch_inbox -o out/batch \
  --strategy balanced --formats json,csv,svg
```

Salida por proyecto: `out/batch/<stem>/solution.json` (+ csv/svg).  
Resumen: `out/batch/manifest.json`.  
Exit: `0` todo ok, `1` mixto, `2` ningún ok (o perfil inválido).

### Lista explícita + dry-run (SPR-003)

```bash
# Inventario sin solver
boardcomposer-batch -L data/samples/batch_jobs.list -o out/batch --dry-run

# Ejecutar solo los paths del listado
boardcomposer-batch -L data/samples/batch_jobs.list -o out/batch \
  -p data/samples/batch_profile.json

# Combinar carpeta + lista (unión, sin duplicados)
boardcomposer-batch -i data/samples/batch_inbox -L data/samples/batch_jobs.list \
  -o out/batch --dry-run
```

El listado admite rutas relativas (respecto al `.list`), absolutas, líneas
en blanco y comentarios `#…`. En dry-run el manifiesto marca jobs
`planned` y no escribe exports.

---

### Plantillas nombradas (SPR-002)

Lee el catálogo Studio (`~/.boardcomposer/export_templates.json`) o un pack /
sample sin Qt:

```bash
boardcomposer-batch -i data/samples/batch_inbox -o out/batch \
  --template "SVG sin retales" --client Demo \
  --templates-file data/samples/export_templates.json
```

También en perfil JSON: `"template"`, `"client"`, `"templates_file"`.
Formato de la plantilla + flags `include_*`; `--formats` puede sobrescribir
el formato. Batch acepta `json,csv,svg,dxf,pdf`.

## Notas de diseño

Maximizar reuso de `boardcomposer.api.v1`. Studio sigue siendo la UI; el
batch no duplica el solver.
