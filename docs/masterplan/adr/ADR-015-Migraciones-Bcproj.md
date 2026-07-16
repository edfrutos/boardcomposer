# ADR-015 — Migraciones explícitas de `.bcproj`

## Estado

Aceptada.

## Contexto

`project_serializer.py` guarda un campo `version` en cada archivo `.bcproj`
desde que el formato incorporó material, espesor, cantidad y asignación de
panel físico por colocación (ADR-014). Hasta ahora, la compatibilidad con
archivos antiguos se resolvía de forma implícita: cada lectura de campo usaba
`dict.get(clave, valor_por_defecto)`, sin ningún punto único que documentase
qué cambió entre versiones ni qué ocurre si un archivo declara una versión
más reciente que la que la aplicación instalada entiende.

Esto funciona mientras solo exista una versión "antigua" y una "actual", pero
no escala: cada nuevo cambio de esquema añadiría más `.get()` dispersos, sin
rastro de qué migración corresponde a qué versión, y sin ningún error claro
para el caso de un archivo "del futuro" abierto con una build anterior.

## Decisión

Se define una cadena explícita de migraciones en `project_serializer.py`:

- `CURRENT_VERSION` es la versión de esquema que esta build escribe y sabe
  leer sin necesidad de migrar.
- `_MIGRATIONS` es un diccionario `{version_origen: función_migración}`. Cada
  función recibe el `dict` crudo en `version_origen` y devuelve el `dict`
  equivalente en `version_origen + 1`.
- `_migrate_to_current_version` lee `data.get("version", 1)` (los archivos
  sin campo `version` se tratan como versión 1, el formato previo a
  ADR-014), aplica las migraciones necesarias en cadena hasta
  `CURRENT_VERSION`, y lanza `UnsupportedProjectVersionError` si el archivo
  declara una versión **mayor** que `CURRENT_VERSION`.
- `project_from_dict` siempre migra antes de construir el modelo en memoria,
  de forma que el resto del código nunca necesita conocer versiones antiguas
  del esquema.

## Migración v1 → v2

Introducida junto con ADR-014: añade valores por defecto explícitos para
`material`, `thickness_mm` y `quantity` en tableros; `material` y
`thickness_mm` en piezas; y `rotated`, `rotation`, `board_id`,
`board_instance`, `stock_panel_index` en colocaciones. Los valores por
defecto son los mismos que ya usaba el código implícito, pero ahora viven en
una única función documentada (`_migrate_v1_to_v2`) en vez de repartidos por
`project_from_dict`.

## Versiones futuras

Al introducir un cambio de esquema que requiera una migración:

1. Incrementar `CURRENT_VERSION`.
2. Añadir `_migrate_vN_to_vN+1` con la transformación necesaria.
3. Registrarla en `_MIGRATIONS[N] = _migrate_vN_to_vN+1`.
4. Añadir un test que cargue un `dict` en la versión `N` y compruebe el
   resultado migrado.

## Compatibilidad hacia adelante

Un archivo con `version > CURRENT_VERSION` no se adivina ni se trunca: se
rechaza con `UnsupportedProjectVersionError`, cuyo mensaje indica la versión
del archivo y la máxima soportada. Studio captura esta excepción en
`_open_project` y `_open_recent_project` y muestra un aviso explicando que
hay que actualizar la aplicación, en vez de fallar con una traza genérica o
cargar un proyecto parcialmente interpretado.

## Consecuencias

- Cada paso de migración es una función pura, testeable de forma aislada.
- El histórico de cambios de esquema queda documentado en el propio código.
- Abrir un archivo más nuevo que la build instalada falla de forma clara en
  vez de silenciosa.
- Añadir una nueva versión de esquema no requiere tocar `project_from_dict`
  más allá de los `.get()` con los valores ya vigentes en `CURRENT_VERSION`.
