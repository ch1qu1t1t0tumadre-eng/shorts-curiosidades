# Mesa de Animación · Otto el Pulpo

Estilo: **dibujos animados de tele clásicos**. Todo se mueve, rebota y se exagera, con efectos de cartoon y un ambiente distinto en cada escena. Los personajes son los **dibujos oficiales** (`pipeline/assets/personajes/`, ver BIBLIA): nunca se redibujan, se animan.

Motor: `pipeline/sitcom.py`, más `pipeline/efectos.py` (movimiento, partículas, luces) y `pipeline/escenarios.py` (decorados). Ejemplo completo: `episodios/ep01/escenas.py`.

## Qué hay en la caja de herramientas
**Personajes: muñecos articulados.** `pipeline/rig.py` separa cada dibujo oficial en piezas con esqueleto: hombros, codos, muñecas, caderas, rodillas, cuello, mandíbula (Teddy), cola (Teddy, Mia), orejas y coleta. Debajo de las piezas que tapan el cuerpo se rellena solo, y las costuras no se abren. No hay que tocar nada para usarlo.
- Movimiento natural automático: respiran, cambian el peso, la cabeza sigue al cuerpo con retraso y asiente al hablar, la cola y las orejas tienen inercia, y los brazos gesticulan con la energía de la voz.
- **Boca:** pasa `talk=L.boca("pj", T)` (no `L.talk`). En silencio se ve la boca del dibujo; al hablar se oculta y se dibuja una boca abierta sobre la cara limpia, con la forma de cada vocal (dientes y lengua). Teddy tiene la boca cerrada (solo la línea del labio) y la abre al hablar. Para que gesticule más, pasa `ene=L.energia("pj", T)`.
- `gesto=`:
  - Generales: `agitar` (pánico), `arriba`, `celebrar`, `caido`, `punos`, `tranquilo`, `saludo`, `suplicar`, `correr`, `andar`, `encoger`.
  - Propios: `sorber` (Moe sube la taza), `teclear` (Nana; sale solo con `typing=True`).
  - Sin `gesto`, sale del ánimo: panico→agitar, sorpresa→arriba, feliz→celebrar, triste→caido, enfado→punos, smug→tranquilo.
- **Andar y correr:** `x, paso, derecha, en_marcha = recorrido(lt, [(t0, x0), (t1, x1), ...], zancada)` mueve al personaje por la escena. Pásale `paso=paso if en_marcha else None` (y `correr=True` para correr). El ciclo de piernas va con la distancia recorrida, así que los pies no resbalan.
  - Movimiento: cadera, rodilla y pie; brazos al contrario de las piernas; rebote y cuerpo inclinado hacia delante.
  - Estilo por personaje: Teddy y Mia andan; Nana y Moe andan como un pato, balanceándose.
  - `flip=True` para que miren a la izquierda: Teddy, Mia y Moe miran a la derecha en su dibujo y Nana a la izquierda.
- **Conversación:** en los planos a dos, cada uno mira al otro (con `flip`).
  - El que escucha lleva `escucha=L.energia("el_otro", T) * 2, mira=1`: asiente, ladea la cabeza y mueve las orejas.
  - `cam_charla(L, T, {"teddy": (x, y), "mia": (x, y)}, zoom, y)` (en `episodios/ep01/escenas.py`) desliza la cámara hacia quien habla.
- Teddy está de pie con las dos piernas en el suelo: su segunda pierna es una copia de la recta del dibujo, un poco más oscura y detrás. Así puede andar.
- `pose={"brazo_i": 0.3, "cabeza": (0.1, 0, -20), ...}` suma ángulos a mano (huesos en `rig.RIGS`). Brazo de la izquierda de la imagen: ángulo + = sube; brazo de la derecha: − = sube.
- Límites de cada dibujo: Mia tiene los brazos cruzados (solo se mueven un poco), Moe sujeta la taza con las dos manos y Nana el móvil.

`teddy / moe / nana / mia(ctx, x, y, s, T, mood, talk, ...)`, con los pies en (x, y). Devuelven `{"head", "top", "feet"}` (mundo) para colgar efectos. Argumentos extra:
- `sq` estira (>1) o aplasta (<1) · `lean` se doblan (+ derecha) · `dx`, `dy` desplazan (dy<0 = arriba) · `head_dy` sube o baja la cabeza · `nod` cabeceo.
- `smear` (velocidad) deja estela · `blush` colorete · `tint=(r,g,b,a)` colorea · `lid` párpados · `flip` mira al otro lado · `spin` gira · `alpha`.
- Ánimo (`mood`): `panico` (tiembla + gotas de sudor que saltan), `enfado` (vibra + vapor + vena), `sorpresa` (salta + líneas), `feliz` (bota), `smug` (se echa atrás), `triste`/`cansado` (se encoge), `sospecha`.
- `cabeza("nana", x, y, s)` da dónde queda la cabeza, para apuntar la cámara.

**Movimientos de cartoon** (devuelven números para pasar al personaje):
- `salto(lt, t0, d, alto)`: anticipación, vuelo estirado y aplastón al caer.
- `toma(lt, t0, fuerza)`: el "take" de sorpresa (se encoge, se estira hacia arriba, rebota).
- `entrada(lt, t0, d, desde)` / `salida(...)`: entra o sale disparado, con rebote y `smear`.
- `carrera(T, ancho, vel)`: corre de lado a lado. `temblor(T, amp)`: para la cámara.

**Efectos:**
- Movimiento: `lineas_velocidad`, `lineas_foco`, `polvo`, `nube_poof`.
- Brillos: `destello`, `destellos`, `estallido` (estrella de cómic).
- Encima de los personajes: `nube_lluvia`, `emote(ctx, "!"/"?", ...)`, `gotas_sudor`, `vapor`, `corazones`, `estrellas_mareo`.
- Ambientales: `rodador` (silencio incómodo), `confeti`, `luciernagas`, `motas`.
- Luz encima de la escena (pantalla): `ambiente(ctx, "calida"|"noche"|"drama"|"gris"|"rosa"|"frio")`. Textos: `badge`, `impacto`.

**Decorados (cada escena con su ambiente):**
- Interiores: `rincon_nana` (chimenea), `cocina_noche`, `pasillo(timbre=)`, `salon`, `cocina`.
- Puertas y exterior: `entrada_noche(abierta=)` (puerta a la calle de noche), `edificio(encendidas=, ondas=)`, `puerta`.
- Fondos de golpe: `escenario_foco`, `rafaga`.
- Cada uno tiene `var` para cambiar colores.

**Transiciones** (`TRANS = {índice_escena: (tipo, duración)}`):
- `whip`: barrido rápido con rayas.
- `zoom`: entra a toda velocidad con un flash.
- `estrella`: cortinilla de estrella.
- `iris`: se abre en círculo.
- `poof`: nube de humo.
- `flash`: destello blanco.

`FINAL = (x, y, d)` cierra en círculo negro al final.

**Subtítulos:** salen solos, abajo y palabra a palabra. La palabra que suena salta y se pinta del color del personaje, con su nombre encima. Usan el campo `sub` de `lineas.json` y en los gritos son más grandes y tiemblan. Ya no hay rótulos arriba ni hace falta `impacto` para las frases.

**Sonido:**
- `SFX`: `zip`, `zip_out`, `whoosh`, `boing`, `poof`, `slide_up`, `slide_down`, `twinkle`, `scratch`, `wind`, `bonk`, `thunder`, `gasp`, `tada`, `doorbell`, `error`, `crickets`, `typing`, `spit`, `connect`, `sting`, `pop`, `ding`.
- `MUSICA = [(desde, hasta, "alegre"|"tension"|"triste")]`: música propia que baja sola cuando alguien habla.
- Un `scratch` (disco rayado) para cortar la música en el momento más incómodo funciona muy bien.

**Tiempos:** en `ESCENAS`, `SFX` y `MUSICA` se puede escribir `"L6"` (empieza la línea 6), `"L6-0.3"`, `"F6"` (termina la línea 6) o `"F6+0.1"`. Si cambia el audio, todo se recoloca solo.

## Regla de oro: no repetir ningún plano
`registro/planos_usados.md` guarda cada plano ya emitido como `decorado:variante · encuadre · personajes · gag o efecto`. En cada episodio:
- **Ninguna fila puede repetirse.** Cambia la variante del decorado, el encuadre, la hora, los objetos, el gag o el personaje en primer plano.
- **Cada escena tiene su ambiente.** Mínimo 4 decorados distintos por episodio. Usa la luz (`ambiente`) para el tono: cálida en casa, noche fuera, rosa en las súplicas, gris en la derrota.
- **Cada episodio estrena al menos una cosa:** un decorado nuevo en `escenarios.py` (ascensor, calle de día, súper, parque, coche, colegio...), un efecto nuevo en `efectos.py` o un gag visual nuevo. Pruébalo con la hoja de contactos antes de usarlo.
- Al terminar, añade a `planos_usados.md` todas las filas del episodio.

## Pasos
1. Escribe `work/epNN/escenas.py` (`from sitcom import *`):
   - **Pocas escenas y largas (3–4 por episodio), sin cortar cada segundo.** Los personajes ENTRAN y SALEN del plano andando o corriendo, la cámara se mueve con `suave(T, [...])` hacia quien habla y los gags (un móvil en burbuja, un "!", luz rosa al suplicar, el temblor de un grito) aparecen encima sin cortar. Solo se corta para un gag que lo pida (el edificio entero oyendo el grito). Ejemplo: `episodios/ep01/escenas.py` (s1, s2, s3). **Que se muevan por las escenas:** que entren andando o corriendo, que crucen el decorado y que se vayan. Las conversaciones van en plano a dos, mirándose. Cada escena es `def eN(ctx, lt, dur, T, L):`, con `zoom_cam(...)` en movimiento, un decorado, los personajes con `talk=L.boca(...)`, un `gesto` que cuente lo que siente y al menos **un movimiento de cartoon o un efecto** (nada de personajes quietos).
   - Gancho: en el fotograma 0 ya pasa algo (alguien entra disparado, un "take", un grito con `lineas_foco`).
   - Cada frase importante lleva un gesto: anticipación antes de un salto, aplastón al caer, estela al correr, "take" en las sorpresas.
   - Zona segura: lo importante entre x 80–1000 e y 250–1550. Los subtítulos van en y≈1330 (cámbialo con `SUB_Y` si tapan algo).
2. Revisa: `python3 pipeline/sitcom.py work/epNN hoja /tmp/hoja.png <30–40 instantes>` y mírala con Read. Corrige solapes, caras tapadas, textos montados y personajes cortados. Repite hasta que esté bien.
3. Render: `python3 pipeline/sitcom.py work/epNN` → `short.mp4` (1440x2560, 60 fps, unos 8–10 min; lánzalo en segundo plano y espera). Comprueba la duración y el audio con ffprobe y mira 4–6 fotogramas del vídeo.
4. Panel: `episodios/epNN.fase = "animacion"`, `duracion`. `equipo/animacion` → `hecho`, con lo que se estrenó en este episodio.
