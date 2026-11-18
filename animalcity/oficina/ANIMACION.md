# Mesa de Animación · Otto el Pulpo

Estilo: **dibujos animados de tele clásicos**. Todo se mueve, rebota y se exagera, con efectos de cartoon y un ambiente distinto en cada escena. Los personajes son los **dibujos oficiales** (`pipeline/assets/personajes/`, ver BIBLIA): nunca se redibujan, se animan.

Motor: `pipeline/sitcom.py`, más `pipeline/efectos.py` (movimiento, partículas, luces) y `pipeline/escenarios.py` (decorados). Ejemplo completo: `episodios/ep01/escenas.py`.

## Qué hay en la caja de herramientas
**Personajes** `teddy / moe / nana / mia(ctx, x, y, s, T, mood, talk, ...)`, con los pies en (x, y). Devuelven `{"head", "top", "feet"}` (mundo) para colgar efectos. Argumentos extra:
- `sq` estira (>1) o aplasta (<1) · `lean` se doblan (+ derecha) · `dx`, `dy` desplazan (dy<0 = arriba) · `head_dy` sube o baja la cabeza · `nod` cabeceo.
- `smear` (velocidad) deja estela · `blush` colorete · `tint=(r,g,b,a)` colorea · `lid` párpados · `flip` mira al otro lado · `spin` gira · `alpha`.
- Solos ya respiran, se balancean, parpadean, cabecean y abren la boca con la voz (`talk=L.talk("pj", T)`).
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
   - Un plano por línea más o menos, con un corte o una transición cada 1–2,5 s. Cada escena es `def eN(ctx, lt, dur, T, L):`, con `zoom_cam(...)` en movimiento, un decorado, los personajes con `talk=L.talk(...)` y al menos **un movimiento de cartoon o un efecto** (nada de personajes quietos).
   - Gancho: en el fotograma 0 ya pasa algo (alguien entra disparado, un "take", un grito con `lineas_foco`).
   - Cada frase importante lleva un gesto: anticipación antes de un salto, aplastón al caer, estela al correr, "take" en las sorpresas.
   - Zona segura: lo importante entre x 80–1000 e y 250–1550. Los subtítulos van en y≈1330 (cámbialo con `SUB_Y` si tapan algo).
2. Revisa: `python3 pipeline/sitcom.py work/epNN hoja /tmp/hoja.png <30–40 instantes>` y mírala con Read. Corrige solapes, caras tapadas, textos montados y personajes cortados. Repite hasta que esté bien.
3. Render: `python3 pipeline/sitcom.py work/epNN` → `short.mp4` (1440x2560, 60 fps, unos 8–10 min; lánzalo en segundo plano y espera). Comprueba la duración y el audio con ffprobe y mira 4–6 fotogramas del vídeo.
4. Panel: `episodios/epNN.fase = "animacion"`, `duracion`. `equipo/animacion` → `hecho`, con lo que se estrenó en este episodio.
