# Mesa de Miniaturas · Cami la Camaleón

Crea **10 versiones**, las puntúa y se queda con la que más clics promete. En Shorts, la miniatura cuenta sobre todo en la búsqueda, en la página del canal y en las sugerencias. En el feed manda el primer fotograma, que es cosa del guion y la animación.

## 1. Crear las 10
`work/epNN/miniaturas.json` con 10 variantes (A–J). Cada una cambia **al menos dos** de estas cosas: fotograma (`t`), texto, color del texto, posición, zoom o encuadre, marco (`borde`) y pegatina (emoji de OpenMoji). Hay que cubrir al menos:
- 3 con la cara más exagerada del episodio en primer plano.
- 2 con el giro (sin destriparlo del todo: que provoque la pregunta).
- 2 con Nana, que es la marca del canal.
- 1 con el texto del gancho literal.
- 1 "rara" que pruebe algo nuevo (otro color o composición).
- 1 con lo que mejor funcionó según `registro/aprendizajes_miniaturas.md`.
Texto: **2–4 palabras**, en mayúsculas, que no repita el título y abra una pregunta. Formato vertical 1080x1920.
`python3 pipeline/miniaturas.py work/epNN` → `thumbs/A..J.png`, `thumbs/hoja.png` y versiones pequeñas (`*_small.png`, 180 px de ancho, como se ven en el móvil).

## 2. Puntuar (mira `thumbs/hoja.png` con Read)
Del 1 al 5 en cada criterio:
1. Se lee a 180 px de ancho.
2. Emoción clara en una cara.
3. Contraste con el fondo y con el feed oscuro de YouTube.
4. Curiosidad: ¿abre una pregunta?
5. Se reconoce el canal (personaje y colores).
6. Limpieza: un solo foco, sin ruido.
Total sobre 30. Ganadora = la puntuación más alta. Si hay empate, la que tenga más emoción. Guarda la tabla en `work/epNN/miniaturas_puntos.md`.
`python3 pipeline/miniaturas.py work/epNN elegir <letra>` → `thumb_final.jpg`. Copia también las 3 mejores a `work/epNN/top3/`.

## 3. Subir (lo hace Bruno en el paso de Studio)
- Si Studio deja subir una miniatura propia ("Subir archivo"), se sube `thumb_final.jpg`.
- Si además aparece **"Experimentos A/B"** (Test & Compare), se suben las 3 mejores. YouTube elige la ganadora por tiempo de visualización.
- Si Studio pide verificar el canal por teléfono, NO se hace nada (es cosa del dueño): se usa "Seleccionar desde el vídeo" con el fotograma más parecido a la ganadora, y se crea o actualiza la alerta `aviso` para el dueño.

## 4. Aprender
Cada lunes, mira en Studio el CTR (porcentaje de clics por impresiones) y los resultados A/B de la semana. Apunta en `registro/aprendizajes_miniaturas.md` qué estilo ganó (colores, texto, personaje, encuadre) y úsalo en la variante "la que mejor funcionó". Panel: `equipo/miniaturas` → `hecho` con la letra ganadora y su puntuación.
