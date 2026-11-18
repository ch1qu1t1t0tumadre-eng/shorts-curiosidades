# Producción diaria de AnimalCity TV (1 episodio al día)

Turno de las 11:23 (Madrid). Pasan por él, en orden, Guion → Voz → Animación → Miniaturas → Studio. Antes de que cada mesa empiece, su `equipo/<mesa>` pasa a `trabajando`, y al terminar a `hecho` (o `alerta` con el motivo).

## 0. Preparar
1. `add_repo` ch1qu1t1t0tumadre-eng/shorts-curiosidades con access `push`. Clónalo en `/home/claude/shorts-curiosidades` (el resultado de add_repo te da el comando exacto).
2. `bash animalcity/pipeline/setup.sh`
3. Lee `animalcity/BIBLIA.md`, `animalcity/oficina/OFICINA.md` y los archivos de `animalcity/registro/`.
4. Carga las herramientas del panel (`db_get`, `db_write`) y comprueba los créditos (regla en OFICINA.md). Si no llegan, para la producción, avisa y termina.
5. Todos los comandos de las mesas se ejecutan desde `/home/claude/shorts-curiosidades/animalcity`.

## 1–5. Las mesas
1. **Guion**: `oficina/GUION.md`
2. **Voz y audio**: `oficina/VOZ.md`
3. **Animación**: `oficina/ANIMACION.md`
4. **Miniaturas**: `oficina/MINIATURAS.md`
5. **Studio**: `oficina/STUDIO.md` (navegador integrado del PC del dueño)

## 6. Cerrar
- Copia a `episodios/epNN/` los archivos del episodio: `guion.md`, `lineas.json`, `escenas.py`, `miniaturas.json`, `miniaturas_puntos.md`, `meta.json`. No copies audio, vídeo ni PNG.
- Actualiza `registro/episodios.md` (nueva fila: nº, fecha, título, situación, de dónde salió la idea, enlace, hora de salida, comentario fijado pendiente) y `registro/planos_usados.md`. Tacha la idea usada en `registro/ideas.md` y marca como `APLICADO` los avisos de `avisos_guion.md` que se hayan aplicado.
- `git add animalcity && git commit -m "AnimalCity epNN: <título>" && git push` a `main` (si el push falla porque hay cambios nuevos, `git pull --rebase` y repite).
- Panel: `meta/estado.creditos_restantes`.
- **SendUserMessage al dueño, en español**: título, cuándo sale y enlace del Short, idea de la que salió (tendencia, aviso de retención o lista de ideas), miniatura ganadora, créditos que quedan y cualquier problema. Recuérdale que puede revisarlo o borrarlo en Studio antes de que salga y que el panel está en https://claude.ai/artifact/Uta9z9pWjehniW1eg8Vijz
