# Biblia del show · AnimalCity TV (@animalcity_tv)

Sitcom animada en YouTube Shorts. Animales que viven en un piso compartido de **Animal City**. Todo lo que sale en los vídeos (diálogo, subtítulos, textos en pantalla, título, descripción y hashtags) va en **inglés americano**. Es un **dibujo animado para todos los públicos, pensado también para niños**: lo ven familias de EE. UU. en el móvil y lo comparten con hermanos, padres y abuelos.

**Estilo:** dibujos animados de tele clásicos. Mucho movimiento, rebotes, estirones, entradas y salidas disparadas, efectos de cartoon (humo, estrellas, nubes de lluvia, rayas de velocidad) y un ambiente distinto en cada escena. Subtítulos grandes palabra a palabra en todas las frases.

## Fórmula del episodio (15–32 s)
Situación que todo el mundo reconoce → conflicto en el **primer segundo** → escalada en 3 pasos → silencio o pausa justo antes del golpe → giro (casi siempre Nana) → último plano que enlaza con el primero para que el vídeo se repita.
- Una sola situación por episodio. Nada de explicaciones ni de narrador.
- Frases de ≤ 8 palabras, con palabras sencillas que entienda un niño de 6–10 años (nada de "literally", "incorrect", ironías de adultos ni dobles sentidos). Entre 8 y 14 líneas.
- El chiste tiene que entenderse sin sonido: los rótulos y las caras cuentan la historia.
- Comedia blanca de situación para niños: nada de citas ni romances, política, sustos, violencia, insultos, marcas ni famosos. Los golpes son de cartoon (aplastones, humo, estrellitas) y nadie se hace daño. Tampoco se parodian personajes de otras series.
- Mia es la **nueva amiga** de Teddy (no su cita ni su novia).

## Reparto (personajes originales del canal · diseño oficial "variante 2")
Los personajes son **los dibujos oficiales** creados en el flujo "Personajes" de ElevenLabs (variante 2 del reparto, `referencias/reparto_v2.png`). No se redibujan: `pipeline/recortar_reparto.py` los recorta en `pipeline/assets/personajes/*.png` y `sitcom.py` los anima como marionetas (respiran, rebotan, parpadean y mueven la boca con la voz).

| Personaje | Animal y aspecto | Personalidad | Cómo actúa | Frases o tics | Voz ElevenLabs (eleven_v4) |
| --- | --- | --- | --- | --- | --- |
| **Teddy** (24) | Golden retriever larguirucho, sudadera naranja con capucha, lengua fuera | Entusiasta, dice que sí a todo, no se entera de nada. Casi siempre es el que provoca el lío | Energía alta, salta, grita, cara de pánico cuando sale mal | "Okay okay okay…", "Nana…" | Jake · `WAYsiv3Yudejrr5Di4lf` |
| **Moe** (25) | Erizo azul marino con gafas redondas, rebeca azul y taza | Ansioso, lo piensa todo demasiado. Reacciona en vez de actuar | Tiembla, suda, escupe la bebida, susurra "Oh no." | Mira a cámara | Timmy (Anxious Nerd) · `mrQhZWGbb2k9qWJb5qeA` |
| **Nana June** (84) | Tortuga, gorro morado de lana, chal morado, pelo blanco rizado, gafas de cerca colgadas de una cadena, móvil en la mano | Abuela de Teddy. Más conectada que nadie, tranquila y letal. **Siempre gana.** No levanta la vista del móvil | Lenta, cara de póquer, mirada de reojo | "I changed it." | Grandma Muffins · `vFLqXa8bgbofGarf6fZh` |
| **Mia** (23) | Zorra con coleta pelirroja, bomber verde, brazos cruzados | La nueva amiga de Teddy. Lista y con chispa. Siempre se pone de parte de Nana | Sonrisa de lado, ceja levantada | — | Melody · `Lb0YjiVdotJrGAKbDrUs` |

Colores fijos (rótulo y miniatura): Teddy naranja `#F08A3C` · Moe azul `#5B8FE0` · Nana morado `#B07CE8` · Mia verde `#6CC26A`.
Para poses nuevas (p. ej. Mia con el puño en alto, Teddy sentado) hay que generar la pose en el mismo flujo "Personajes" partiendo del dibujo oficial y recortarla igual; nunca se sustituyen por dibujos hechos a mano.
Se pueden añadir personajes secundarios (casero, vecino, jefe…), siempre animales originales y con su función en `sitcom.py`.

## Lugares
Rincón de Nana con chimenea, salón (sofá azul, ventana con la ciudad y el cartel ANIMAL CITY), cocina de noche, pasillo, la puerta de casa abierta a la calle de noche, el edificio visto desde fuera y el escenario con foco para los momentos dramáticos. Hay que ir añadiendo decorados nuevos en `pipeline/sitcom.py`: ascensor, calle, supermercado, gimnasio, coche, oficina de Teddy…

## Series dentro del canal
- **"Nana always wins"**: Nana gana en todos los episodios.
- **"Moe's inner monologue"**: Moe narra lo que de verdad piensa.
- **"Teddy vs. technology"**: Teddy contra los aparatos de casa.

## Reglas de autenticidad (monetización)
Personajes, guiones, decorados y voces son propios del canal. Cada episodio cuenta una historia nueva y tiene planos nuevos. Nunca se copian el guion ni la animación de otro canal: de las tendencias solo se toma la **situación** y se cuenta a nuestra manera.
