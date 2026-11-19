# Por qué retienen los Shorts de curiosidades virales (análisis 18/11/2026)

Referencia principal: "¿Qué hay en el cerebro de Albert Einstein?" — @Vidacuriosa24 — youtube.com/shorts/Rs0WLQvh1A4
**9,98 M de visualizaciones, 570 K likes (5,7 % de likes), 37,5 s.** Comparado con 3 Shorts en inglés del mismo tipo (Cleopatra 21,7 M; "Historical facts that distort time" 9,3 M; "History facts school didn't teach you" 8,2 M).

## Lo que encontramos (medido, no a ojo)

| Qué | Dato medido | Por qué retiene |
|---|---|---|
| **Final en bucle** | Acaba "...las habilidades de Einstein, pero no su causa" y corta en seco, sin despedida ni "sígueme". 3 de los 4 vídeos analizados lo hacen. El de Cleopatra (21,7 M) termina "...so here are some" y arranca "facts about Egypt's last pharaoh". | El espectador no detecta el final y lo ve una segunda vez → % visto > 100 %. Es la señal que más empuja YouTube. |
| **Hook = nombre famoso + lo prohibido** | 0–2 s: "¿Qué pasó con el cerebro de Albert Einstein después de su muerte?". Sin intro, sin "¿sabías que…?". | Reconoces al protagonista en 1 s y la pregunta es morbosa: no puedes no saber la respuesta. |
| **Ritmo de voz** | 133 palabras en 37,5 s = **~213 palabras/min**, sin una sola pausa (el volumen nunca baja a silencio en todo el vídeo). Nuestro formato iba a ~165. | No hay hueco para deslizar. |
| **"Es decir…"** | En el s 11: "extrajo el cerebro sin el consentimiento de su familia. **Es decir, robó el cerebro de Einstein**." | Segundo gancho: reformula un dato neutro en lenguaje brutal. Pico de energía de la voz. |
| **Repetición de la palabra clave** | "Einstein" ×7, "cerebro" ×6 en 37 s. | Ancla; quien entra a mitad entiende de qué va. |
| **Cambio de plano** | Imagen nueva cada ~2,5–3 s, siempre con zoom lento. En el audio se ven picos de "whoosh" cada ~3 s (0,1 · 2 · 5,7 · 8,7 · 10,5 · 12,6 · 16 · 21,5 · 25,4 · 31,4 · 34,5 s). | Interrupción de patrón constante. |
| **Subtítulo gigante** | UNA palabra en el centro, amarilla, fuente de cómic (tipo Bangers), borde negro y sombra roja. Además subtítulos pequeños automáticos arriba. | Se lee aunque estés sin sonido; el ojo va al centro, donde está la acción. |
| **Datos concretos encadenados** | 1955 · Dr. Thomas Harvey · frasco · 240 pedazos · 1.000 diapositivas · científica Diamond · células gliales. | Cada 2–3 s hay "algo nuevo" → recompensa continua. |
| **Entonación** | Narrador uniforme y con energía constante; el énfasis cae en números y nombres al final de frase; nada de susurros ni dramatismo excesivo. | Sensación de "te estoy contando un secreto rápido". |

## Lo que cambiamos en nuestro canal

1. Guion en **formato bucle** (ver INSTRUCCIONES.md paso 1): sin "Stay till the end", sin CTA, la última frase se corta y empalma con la primera.
2. Voz acelerada a **~195 palabras/min** con `pipeline/acelerar.py` (Dean no tiene control de velocidad en el conector; se acelera con `atempo` y se reescalan los tiempos).
3. **Plano nuevo cada 2–3 s** (13–18 escenas), la última escena repite la imagen de la primera.
4. **Subtítulo gigante de una palabra** en el centro (`draw_caption_big` en pipeline/anim.py, fuente Bangers en pipeline/fonts).
5. Título con el nombre del protagonista en forma de pregunta o afirmación imposible.
6. Temas: protagonista conocido + giro morboso/prohibido/absurdo, siempre verificado.
