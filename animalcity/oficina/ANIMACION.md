# Mesa de Animación · Otto el Pulpo

Motor: `pipeline/sitcom.py` (personajes `teddy`, `moe`, `nana`, `mia`; decorados `salon`, `puerta`, `cocina`, `rafaga`; `rotulo`, `impacto`, `badge`, `zoom_cam`, `phone`, `tablet`; efectos `SFX`). Ejemplo completo: `episodios/ep01/escenas.py`.

## Regla de oro: no repetir ningún plano
`registro/planos_usados.md` guarda cada plano ya emitido como `decorado:variante · encuadre · personajes · elemento distintivo`. En cada episodio:
- **Ninguna fila puede repetirse.** Cambia la variante de color del decorado (`var`), el encuadre (zoom y punto de la cámara), la hora (`noche=False`), los objetos o el personaje en primer plano.
- **Cada episodio estrena al menos una cosa:** un decorado nuevo, un objeto nuevo, una pose o expresión nueva, o un movimiento de cámara nuevo. Si hace falta, añade la función a `sitcom.py`: decorados como `ascensor`, `calle`, `super`, `gimnasio`, `coche`, `oficina`; props; poses. Pruébalo con una vista previa antes de usarlo y haz commit de `sitcom.py`.
- Al terminar, añade a `planos_usados.md` todas las filas del episodio.

## Pasos
1. Escribe `work/epNN/escenas.py` (`from sitcom import *`):
   - Un plano por línea de diálogo aproximadamente, con cortes cada 1–2,5 s. Los cambios de plano coinciden con el `ini` de cada línea en `timeline.json`.
   - Cada escena es `def eN(ctx, lt, dur, T, L):`. Siempre lleva `zoom_cam(...)` con keyframes para que la cámara se mueva, un decorado y los personajes con `talk=L.talk("<pj>", T)` para que las bocas sigan la voz.
   - Ánimo de cada personaje según la frase (`normal`, `feliz`, `sorpresa`, `panico`, `enfado`, `sospecha`, `smug`, `cansado`, `triste`). Nana: `gafas="puestas"|"bajadas"|"frente"`.
   - Gancho: el plano 1 es un primer plano con emoción extrema desde el fotograma 0, y lleva un `impacto(...)` en el segundo 1–2.
   - Los gritos van como `impacto` (y `rotulo:false` en `lineas.json`). Los rótulos de diálogo salen solos.
   - Zona segura: lo importante entre x 80–1000 e y 250–1550. Abajo va la interfaz de YouTube.
   - `ESCENAS = [(t, eN), ...]`, `SFX = [(t, "doorbell"|"error"|"crickets"|"typing"|"sting"|"spit"|"connect"|"pop"|"ding"|"whoosh"), ...]` (máximo 12) y `COLA = 0.15`.
2. Revisa: `python3 pipeline/sitcom.py work/epNN preview <un instante de cada plano>` y junta las imágenes en una hoja (como se hizo con el ep01). Mírala con Read. Corrige solapes, personajes cortados, rótulos que tapan caras y texto fuera de la zona segura. Repite hasta que esté bien.
3. Render: `python3 pipeline/sitcom.py work/epNN` → `short.mp4` (1440x2560, 60 fps, unos 3 min). Comprueba con ffprobe la duración y que haya audio.
4. Panel: `episodios/epNN.fase = "animacion"`, `duracion`. `equipo/animacion` → `hecho`, con lo que se estrenó en este episodio.
