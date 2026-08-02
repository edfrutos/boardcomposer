# Piloto DT-0006 — Backup de revisiones (opción D)

**Piloto:** mono-equipo / backup operativo (sin multi-usuario cloud).  
**Decisión:** DEC-0010 · Spike: `SPIKE-DT-0006-historial-cloud.md`  
**Fecha:** 2026-08-02

---

## Qué cubre

Copiar el `.bcproj` actual y el anillo local `.<nombre>.bcproj.revs/` a una
carpeta de destino (disco montado, NAS, sync folder). No hay servidor propio.

## CLI

```bash
boardcomposer-backup ruta/al/proyecto.bcproj --dest /mnt/backup/boardcomposer
```

Crea `/mnt/backup/boardcomposer/<stem>-<UTC>/` con el archivo y, si existe, el
sidecar de revisiones.

## Studio

**Proyecto → Exportar backup de revisiones…** — elige carpeta destino (mismo
comportamiento que el CLI).

## Cron / ops (ejemplo)

```bash
# Diario 02:15 — ajustar rutas
15 2 * * * /path/to/.venv/bin/boardcomposer-backup \
  /data/jobs/actual.bcproj --dest /mnt/backup/bcproj >>/var/log/bc-backup.log 2>&1
```

## Fuera de alcance de este piloto

- Merge multi-escritor, ACL, OAuth, API de revisiones (opción C).
- Sustituir el anillo local (sigue siendo la fuente de verdad offline).

## Siguiente escalón

Si el piloto exige colaboración concurrente → reabrir spike y evaluar **C**
con identidad + DOC-010 actualizado. No inventar “falso cloud” vía sync del
anillo (opción B descartada).
