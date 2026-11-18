# Mesa de Voz y audio · Polly la Lora

Las voces son **propias del canal** y se generan aquí, sin ElevenLabs, sin conexión y sin créditos: `pipeline/voces.py`.
- Motor: Kokoro-82M (Apache 2.0, uso comercial permitido), con las voces tal cual (sin procesar).
- La voz de cada personaje está guardada en `VOCES` (mezcla de voces base + tono, formantes, entonación y temblor). **Es la misma en todos los vídeos: no la cambies.**

| Personaje | Voz guardada (sin retocar el tono: retocada sonaba robótica) |
| --- | --- |
| Teddy | am_puck, ritmo 0,94 |
| Moe | am_liam + am_echo, ritmo 0,9 |
| Nana | bf_emma, ritmo 0,86 (pausada) |
| Mia | af_heart, ritmo 0,93 |

**Que se entienda bien es lo primero, aunque el episodio dure más.** Pausas de 0,4–0,8 s entre frases (1–1,6 s cuando hay un silencio cómico). No aceleres las voces.

## Pasos
1. En `work/epNN/lineas.json`, `texto` admite al principio de cada trozo una emoción entre corchetes:
   - `[panicked]`, `[nervous]`, `[shouting]` (o el texto en MAYÚSCULAS)
   - `[whispers]`, `[mumbles]`, `[flatly]`, `[smug]`
   - `[reading slowly]`, `[delighted]`, `[excited]`, `[sad]`

   Ejemplo con dos emociones: `"[reading slowly] Nana... Is... The... Best. [delighted] It works!"`.
   Si lo que se dice no coincide con lo escrito (una contraseña pegada, un murmullo), pon `"voz": "texto para decir"`.
2. `python3 pipeline/voces.py work/epNN` → `audio/NN.wav` de cada línea, y monta `dialogo.wav` + `timeline.json` (también la forma de la boca). Tarda segundos. Para rehacer solo algunas: `python3 pipeline/voces.py work/epNN 6 11`.
3. Comprueba la lista de tiempos que imprime: total entre 15 y 32 s, sin huecos de más de 1,2 s salvo los que pida el guion. Ajusta `pausa` para el ritmo cómico y vuelve a montar con `python3 pipeline/dialogo.py work/epNN`.
4. Muestra de las cuatro voces: `python3 pipeline/voces.py casting /tmp/casting.wav`.
5. Panel: `episodios/epNN.fase = "voz"`. `equipo/voz` → `hecho` con la duración.
