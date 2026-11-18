# Mesa de Voz y audio · Polly la Lora

Las voces son **propias del canal** y se generan aquí, sin ElevenLabs, sin conexión y sin créditos: `pipeline/voces.py`.
- Motor: Kokoro-82M (Apache 2.0, uso comercial permitido) más un procesado de tono y formantes (WORLD).
- La voz de cada personaje está guardada en `VOCES` (mezcla de voces base + tono, formantes, entonación y temblor). **Es la misma en todos los vídeos: no la cambies.**

| Personaje | Voz guardada |
| --- | --- |
| Teddy | joven, aguda y con energía (am_puck + am_liam, +8 semitonos, rápida, muy expresiva) |
| Moe | nerviosa y temblorosa (am_echo + am_michael, +5,5 semitonos, temblor ligero) |
| Nana | de abuela, lenta y socarrona (af_sarah + bf_emma, −5 semitonos, formantes de mayor, temblor de voz) |
| Mia | joven y con chispa (af_heart + af_bella, +3,5 semitonos, expresiva) |

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
