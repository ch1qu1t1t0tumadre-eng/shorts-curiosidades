# Rutina diaria: 2 Shorts de curiosidades

Canal: curiosidades de todo tipo. **TODO EN INGLÉS AMERICANO** (guion, voz, textos en pantalla, subtítulos, título, descripción y hashtags), pensado para público de EE. UU. Categorías (ir rotando, que no se repita la misma dos días seguidos): animales, historia, cuerpo humano, ingeniería, **aviación**, **astronomía y espacio**, ciencia, geografía, tecnología, comida, océanos, mente y psicología…
**Ritmo y horario (orden del dueño, 25/11/2026; horario nuevo desde el 27/11/2026): de lunes a viernes 3 Shorts a las 20:00, 23:00 y 01:00, y sábado y domingo 2 Shorts a las 20:00 y 23:00, hora Europe/Madrid** (= 14:00, 17:00 y 19:00 en Nueva York; el público principal es de EE. UU. y su pico de Shorts es de 18:00 a 23:00, hora local). **El hueco de la 01:00 del día D se programa con la fecha D+1 a la 01:00** (p. ej. el 3.º Short del jueves 27/11 → viernes 28/11 01:00). El domingo no hay hueco de 01:00. El Short con el tema más fuerte del día va al hueco de más audiencia: 01:00 entre semana, 23:00 en fin de semana. Ver «Horario» más abajo. Se suben a YouTube Studio en **privado y programados**. Muchos días ya habrá vídeos preparados por adelantado: mira `agenda.md` y haz solo los huecos libres de HOY. El dueño los revisa antes y borra o edita los que no le gusten.
(Plan ElevenLabs Starter: 30.000 créditos/mes. Modelo `eleven_v4`, la voz buena: ~1 crédito por carácter. Guiones de 600–750 caracteres → ~680 créditos/vídeo. Con 2 vídeos/día el plan Starter NO llega a todo el mes: el freno de créditos para la tarea cuando se acaban.)

## Horario (análisis del 25/11/2026)
- Studio aún no muestra «horas de actividad» del canal (pocos datos). Audiencia: EE. UU. 28 %, Reino Unido 10 %, Filipinas 7 %, India 4 %, España 3,5 %; 99,6 % espectadores nuevos (llegan por el feed).
- Datos propios (13 Shorts): media de vistas por hora de subida (Madrid): 17:00 ≈ 760 · 20:00 ≈ 840 · 23:00 ≈ 1.080.
- Estudios (Buffer, 1,8 M vídeos; SocialPilot, 301 K): los Shorts rinden más de 18:00 a 23:00 hora local; mejor día el viernes (16:00–19:00), luego sábado y jueves; peor lunes/martes; el domingo por la noche baja. Los Shorts siguen recibiendo vistas días después: la constancia importa más que la hora exacta.
- Por eso: L–V 20:00 / 23:00 / 01:00 y S–D 20:00 / 23:00 (Madrid). Cuando Studio muestre las horas reales del canal, revisar este horario.

## 0. Preparar
1. `add_repo` ch1qu1t1t0tumadre-eng/shorts-curiosidades con access "push", clonarlo en /home/claude/shorts-curiosidades.
2. `bash pipeline/setup.sh`
3. Leer `temas_usados.md` (no repetir ningún tema).
4. Leer `agenda.md`: si hoy ya hay una hora ocupada por un vídeo programado antes (p. ej. un vídeo de ejemplo), haz solo los vídeos de las horas libres.

## 1. Elegir el tema y escribir los 2 guiones (rol: el creador de Shorts más influyente de nuestra época)
Actúa como un creador de vídeos cortos de primer nivel, experto en todos los temas del canal, en psicología del consumidor y en técnicas de atención y retención.

**Nicho:** "Hidden reasons behind everyday things" — curiosidades con un "por qué" oculto detrás de cosas que todo el mundo ve o vive (aviones, cuerpo, animales, espacio, ingeniería, historia…) y que cambian cómo miras el mundo. No datos sueltos: cada vídeo revela algo que "nadie te explicó" y deja una idea práctica.
**Audiencia:** EE. UU., 18–34 años, móvil, scroll rápido; curiosos que ven Shorts en ratos muertos (cola, transporte, antes de dormir); les gusta sentirse "más listos que los demás" y compartir el dato con amigos. Atención de 1–2 s para decidir si se quedan.

**Elegir tema:** 2 temas sin repetir (`temas_usados.md`), categorías distintas y rotando. Prioriza temas con: (a) algo que el espectador ha visto o vivido, (b) una creencia común falsa o un "nadie te lo dice", (c) un consejo práctico al final. Verifica cada dato con WebSearch (fuentes fiables). Si algo no se confirma, fuera.

**FORMATO BUCLE (v2, 18/11/2026 — sustituye al formato con CTA).** Sale del análisis de Shorts de curiosidades con 10–22 M de visitas (ver `FORMATO_VIRAL.md`). Lo que les hace retener: no hay ni un segundo "vacío", el final empalma con el principio y el espectador lo ve 2 veces sin darse cuenta.

**ANÁLISIS DE CADA VÍDEO (orden del dueño, 27/11/2026: "cada vídeo que subas lo analices, cojas las mejores partes y las peores, las compares y apliques los mejores métodos a los siguientes").** Se hace en CADA ejecución diaria, ANTES de hacer vídeos nuevos:
1. Mira `analisis/pendientes.md`: los Shorts con ≥3 días publicados (antes Studio no enseña la curva).
2. En Studio (navegador integrado), pega `pipeline/studio_curva.js` con javascript_tool y llama `await window.__curvas(['ID1','ID2'])` (si tarda, lánzalo con `.then(r=>window.__R=r)` y lee `window.__R` después): devuelve la curva (41 puntos), "se quedaron viendo" y vistas. Si la curva sale `null`, aún no hay datos: déjalo para mañana.
3. Guarda la curva en `analisis/vNN_curva.json` y ejecuta `python3 pipeline/analizar_retencion.py work/vNN analisis/vNN_curva.json ID stayed vistas`. Escribe `analisis/vNN.md` (los 3 peores segundos y las 3 mejores ventanas de 3 s, con la frase dicha, la escena y el tipo de tramo) y añade la fila a `analisis/registro.md`. Bórralo de pendientes.
4. COMPARA con los anteriores del registro: qué tipo de tramo pierde gente una y otra vez (gancho, planteamiento, burla, rival, escalada, explicación, analogía, in-other-words, cierre) y qué tipo de tramo aguanta; qué tienen en común los vídeos con más "se quedaron" y más vistas (tema, título, primer plano, duración, ritmo de cortes).
5. APLICA: escribe la conclusión con datos en la sección «LECCIONES DE LOS VÍDEOS» de abajo (nueva entrada con fecha, vídeos en los que se basa y la regla concreta: qué hacer más y qué dejar de hacer), y úsala en los vídeos de ese mismo día. Si una lección contradice una regla anterior con más datos, gana la que tenga más vídeos detrás.
6. Cada Short nuevo que subas se añade a `analisis/pendientes.md` con su carpeta, ID y fecha.

**LECCIONES DE LOS VÍDEOS (se añaden aquí, la más reciente arriba):**
- 28/11/2026 — Pisa (01:00) vs aceras (20:00) y cables (23:00), datos de Studio a las 12:20 del 28/11:
  - Aceras: **74,1 % se quedaron, 3,3 K vistas** (récord del canal, aún sumando ~580/h). Cables: 59,7 %, 1,3 K. **Pisa: 35,5 % se quedaron, 299 vistas** (64,5 % deslizó).
  - El fallo de Pisa NO es la hora: con dos de cada tres deslizando, YouTube deja de enseñarlo a cualquier hora (seguía saliendo en el feed: 37 vistas en la última hora). Es el arranque y el tema:
    1. Fotograma 0 = postal de un monumento que todo el mundo ya conoce + ficha informativa abajo → parece un documental; nadie hace nada raro. Las aceras abren con una PERSONA HACIENDO ALGO "MAL" A PROPÓSITO (el chico cortando el cemento) → curiosidad inmediata.
    2. A los 3 s Pisa salta a un calendario "1173" y a "Floor one. Perfect. Floor two…": clase de historia justo en el tramo 3–9 s donde más gente se va. Las aceras a los 3 s ya tienen dos cuadrillas rivales y a los 7 s el jefe dice "Kid, you're ruining it" (conflicto antes del segundo 8).
    3. Tema: los monumentos/personajes históricos del canal se quedan en 35–46 % (Pisa 35, Eiffel 38, Hope 38, Nobel 40, Einstein 46). Los objetos cotidianos con un "¿por qué?" que todo el mundo se ha preguntado están en 59–74 %.
    4. Cables (60 %) vs aceras (74 %): mismo formato, pero en los cables el chico está quieto en el fotograma 0 y el cable flojo casi no se ve. **La acción del protagonista en el fotograma 0 marca la diferencia.**
  - REGLAS desde hoy: (a) nada de monumentos, fechas ni personajes históricos como tema principal; solo objetos cotidianos con un "¿por qué?" que la gente se ha preguntado alguna vez; (b) fotograma 0 = el chico haciendo la cosa rara, grande y en movimiento (rodando, cortando, colgando…), con el objeto ocupando media pantalla; (c) el rival/jefe y el primer conflicto antes del segundo 8; (d) ni un año ni un calendario en los primeros 10 s; (e) la franja de 01:00 se mantiene de lunes a viernes: se volverá a mirar cuando tenga un vídeo del formato historia (Pisa no sirve para medir la hora).
- 27/11/2026 (20 Shorts, sin curvas aún de v26–v31): se mantienen las reglas de RETENCIÓN del 26/11. Primeros datos del formato historia: patatas 62 % / 1,0 K, neumáticos (apertura nueva) 59 % / 1,3 K, ventanillas (apertura nueva) 64 % / 990 en 1 día: el formato historia arranca mejor que los de famosos del 25/11 (46–52 %).

**RETENCIÓN — análisis del 26/11/2026 (orden del dueño: "mira qué falla y corrígelo"). Datos de Studio de los 20 Shorts publicados:**
- Lo que decide las vistas es **"Se quedaron viendo"** (vs. "Saltaron el contenido"): con ≥58 % → 1.200–1.400 vistas (Luna 64 %, Galileo 62 %, Newton 61 %, Edison 61 %, Napoleón 59 %); con ≤46 % → 180–450 (Torre Eiffel 38 %, Hope 38 %, Nobel 40 %, Einstein 46 %). Objetivo: **≥60 %**. El primer formato historia (patatas, v28) sacó **64 % y 595 vistas en 2 h**, el mejor arranque del canal.
- **Todas las curvas pierden 30–45 puntos entre el 10 % y el 20 % del vídeo (segundos 4–9)**, justo después del gancho, cuando el guion mete relleno ("And it's real.", año y lugar, "the airline will buy whichever…"). Reglas: **nada de frases de confirmación ni de contexto** entre el gancho y el primer giro; el planteamiento es UNA frase corta (≤ 8 palabras: "See, two companies are building jets."); en el segundo 4 ya pasa algo nuevo (burla del jefe, primer paso de la escalada, primer dato chocante). Si una voz ya generada trae relleno, se quita sin gastar créditos con `python3 pipeline/recortar.py work/vNN T0 T1` + `CORTES = [(T0, T1)]` en escenas.py (anim.py traduce el tiempo solo).
- **Primeros 3 segundos:** los peores tenían 2,5 s del mismo plano quieto de algo normal (una torre, un cuaderno, un periódico). Los mejores enseñan la cosa rara desde el fotograma 0 (el dedo en el huevo de cristal, Napoleón junto a la regla, el sello "LIE"). Reglas: fotograma 0 = **primer plano del objeto raro con la cámara ya moviéndose** (zoom de 1,35 a 1,15); **texto de gancho fijo arriba de 0 a ~3 s** con `gancho(ctx, ["WHY DO TIRES", ("HAVE GROOVES?", WHITE)], T)` (estilo_v3); **primer corte seco a ~1,5–2 s** a un ✓/✗ o a una pista del giro; el último plano del vídeo = el fotograma 0 (mismo encuadre y zoom) para el bucle.
- **Gancho y título como pregunta o contradicción**, nunca contando el dato entero: "Why…?", "What happened to…?", "…is a lie", "…was NOT…" funcionan; "Marie Curie's notebooks are still radioactive" o "Nobel read his own obituary" ya lo cuentan todo y la gente desliza.
- No publicar 3 Shorts en 3 horas (el 25/11 a las 19:30/21:30/22:30 se quitaron vistas entre ellos: 281–936). Mantener el horario 20:00/23:00/01:00.

**FORMATO «HISTORIA» (26/11/2026 — orden del dueño, es el formato POR DEFECTO desde hoy; sustituye a v3 en lo que choque).** Inspirado en «Why He Built His Bridge Six Inches Too Short» (You Change History, 3,2 M de vistas en 1 día). Ejemplos aprobados y publicados: v28 patatas/nitrógeno, v29 neumáticos/surcos, v30 ventanillas redondas (`ejemplos/escenas_v28/29/30_historia_en.py` + `ejemplos/guion_v28/29/30_historia.md`).
- **Historia INVENTADA con física/ciencia REAL.** La descripción del vídeo SIEMPRE dice: "The story is made up, but the physics/science is real: …" y explica el dato verificado. Nunca atribuir la historia a una persona o empresa real.
- **Guion (150–165 palabras, ~45 s a 215 ppm), plantilla:** "[intrigued] This guy did X on purpose." → "See, two companies/teams/crews are … and only one gets …" → "His boss sees … Kid, …" (burla) → el protagonista sigue / "And he's right…" → "The other company does it perfectly. … Everybody loves it." → escalada en el tiempo ("Then … Flight one, nothing. Flight one thousand, …") → el rival fracasa y el chico gana → "You see, …" + la física en 1–2 frases + **una analogía cotidiana** ("Like the drains in a street.") → "[dramatic] In other words, … didn't X. They Y." → "That's why the X on your Y has Z." → "Because, just like" (bucle: empalma con "This guy…").
- **Temas:** objetos cotidianos con un "por qué" de diseño oculto que se pueda dibujar (bolsas de patatas, surcos de neumáticos, ventanillas redondas, juntas de las aceras…).
- **Imagen:** `from kit import *` + `from estilo_v3 import *` (piezas comunes: `worker` para el chico/jefe/rival, `bubble` para "Kid, …", `label`, `check`, `cal`, `rain`, `zig/partial/crack_path`, `blur_layer`, arco de luz con `set_azul(t_you_see, t_fin_in_other_words)`). Chico en azul (KID), rival en rojo (RIV), jefe marrón con corbata. Escena final = escena 1 (bucle). Todo lo demás de v3 se mantiene (cámara, sonido, contornos, microanimación).
- **SUBTÍTULOS ABAJO (orden del dueño, 26/11/2026: "son más cómodos para el espectador"):** `Y_SUBTITULO = 1430`, `TAM_SUBTITULO = 135`. Lo esencial va entre y 250 y 1300; las etiquetas de arriba en y 260–330; nada importante en la franja y 1340–1520. El lienzo lógico es 1080×1920 (no pongas nada en x > 1040).

**FORMATO v3 «EXPLICACIÓN» (25/11/2026 — orden del dueño, sustituye en lo que choque a v2).** Sale del análisis del vídeo de Mr omi (canal de Shorts animados con 200 M de vistas; doc «Análisis: Shorts animados virales (Mr omi) vs Wait, What.») y de la prueba v26 (Torre de Pisa, `ejemplos/escenas_v26_prueba_en.py` + `ejemplos/guion_v26_prueba.md`), que el dueño aprobó. Se mantiene todo lo de v2 (gancho con nombre famoso + giro, "In other words", bucle sin CTA, datos verificados) y se añade:
- **Guion de 150–165 palabras (≈ 830–900 caracteres, 42–46 s a ~215 ppm).** Estructura: gancho-paradoja → "And it's real." → escenario (año, lugar) → **escalada en 3–4 pasos, cada uno un poco mayor** ("Floor one. Perfect. Floor two. Still perfect. By floor three…") → **"You see, …"** + la causa real explicada con **una analogía cotidiana** (una esponja, un columpio, una pajita…) → "In other words, …" (reformulación brutal) → **un golpe de humor seco basado en un dato real** (estilo "Luckily for X, … Unluckily for Y, …") → giro final → frase cortada que empalma con la primera.
- Elige temas con **causa → efecto que se pueda ver** (algo que se cae, se hunde, explota, se congela…) y que se expliquen con una analogía.
- **Voz a ~215 ppm**: `acelerar.py` ya apunta a 215 por defecto; si suena atropellada, baja a `… work/vNN 1.10`.
- **Imagen**: arco de luz (cálido al presentar → azul noche desde "You see" hasta el final de la explicación → cálido al final, igual que el principio), **sin negros puros** (lo más oscuro, azul/violeta), **contorno de tinta** (~4,5 px, color casi negro violáceo) en todo lo dibujado, **fondo desenfocado** (`blur_layer`) en primeros planos, **microanimación** en todo (parpadeo, balanceo, respiración).
- **Cámara**: 10–14 escenas («decorados»); dentro de cada una la cámara viaja (zoom/paneo con `keyframes`) y aparece algo nuevo cada 2–3 s. Cortes secos solo en saltos grandes (cambio de lugar o de época). `FLASH = False`, `WHOOSH = False` (el whoosh va a mano en `SFX` solo en esos saltos).
- **Sonido**: `MUSICA_GAIN = 0.42`, `FX_GAIN = 0.30` y **un efecto por cada acción visible** (`SFX` admite: whoosh, pop, ding, tick, rise, thud, crack, bell, squish, drum).
- **Subtítulos ABAJO** desde el 26/11/2026 (`Y_SUBTITULO = 1430`, `TAM_SUBTITULO = 135`), nunca tapando lo esencial (ver 3b).
- Funciones reutilizables de la prueba: `luz/pal` (arco de luz), `ink/fill_ink` (contorno), `blur_layer` (desenfoque), `builder` (personaje plano con parpadeo), `check` (✓/✗), `cal` (calendario). Cópialas de `ejemplos/escenas_v26_prueba_en.py` y adapta los decorados al tema.

**Elegir el ángulo:** dentro del nicho, prioriza temas con **un protagonista conocido** (persona, lugar u objeto famoso que el espectador ya reconoce) + **un giro inquietante, prohibido o absurdo** ("lo robaron", "sigue ahí", "nadie lo sabe", "lo hicieron a escondidas"). Morbo y sorpresa, siempre 100 % verdadero y verificado.

**Estructura del guion v2 (base; con v3 el guion es de 150–165 palabras y añade escalada, "You see" + analogía y humor seco):**
1. **HOOK = primera frase (0–2 s):** empieza directamente por el **nombre del protagonista + lo increíble**, sin presentación ni "did you know", ni "stay till the end". Ej.: "Thomas Edison's last breath is sealed inside a glass tube in Michigan." Que la frase 1 pueda leerse también como **continuación** de la última frase del vídeo (bucle).
2. **Confirmación seca (2–4 s):** 2–4 palabras que suben la apuesta: "And it's real." / "Nobody asked his family."
3. **Historia en cadena (4–30 s):** hechos concretos en orden (año, lugar, cifra, nombre), una idea por frase, sin relleno. Cada 2–3 s aparece un dato nuevo (número, objeto, nombre). **Repite el nombre del protagonista 5–7 veces** (ancla la atención y da palabra clave a los subtítulos gigantes).
4. **"In other words" (≈ 10–15 s):** cuenta un hecho de forma neutra y justo después lo **reformula en lenguaje brutal** y corto: "...without his family's consent. In other words, he stole it." Es el segundo gancho: el pico de energía de la voz.
5. **Giro final (30–40 s):** el dato más raro o actual ("Today it's still sealed, on display at…").
6. **CIERRE EN BUCLE (sin CTA):** NO hay "follow", ni pregunta, ni despedida (señalan "se acabó" → el espectador desliza). La última frase **se corta a media idea** y enlaza gramaticalmente con la primera: "...Henry Ford actually did. He saved" → (vuelve al inicio) "Thomas Edison's last breath is sealed…". El vídeo termina en la última palabra, sin silencio.
- Frases de 5–12 palabras, tono de narrador contando un secreto, inglés americano natural. Nada de "..." para pausas: la voz no para nunca.
- "Polémico" = encuadre contraintuitivo o morboso, nunca exagerar ni inventar. Lo que sea leyenda, dilo como leyenda ("Legend says…"). Nada de alarmismo médico, política o tragedias recientes.
- Ejemplo completo: `ejemplos/guion_bucle_edison.md`.

**Guarda `work/vNN/guion.md`** con: nicho/ángulo, el texto exacto para la voz y una tabla por bloque: tiempo · voz · escena/plano de cámara (zoom, paneo, primer plano…) · elementos visuales (equivalente a b-roll en animación) · texto en pantalla (≤ 4 palabras) · caption. Ese guion manda en el diseño de las escenas (paso 3). En la tabla, una fila cada 2–3 s (13–18 filas), no por bloques.

## 2. Voz (ElevenLabs, conector MCP)
- Antes de nada, mira `agenda.md`: los huecos de hoy (L–V: 20:00, 23:00 y 01:00 de la madrugada siguiente · S–D: 20:00, 23:00) que ya tengan vídeo programado NO se hacen. Si todos están ocupados, no generes nada: solo comprueba en Studio que siguen programados y avisa al dueño.
- Luego `account_get_usage`: `quedan = character_limit - character_count`. Aplica la regla de créditos de abajo ("Créditos y ritmo"): hasta 3 vídeos al día de lunes a viernes y 2 el fin de semana. Prioridad de huecos: 01:00, 23:00, 20:00 (fin de semana: 23:00, 20:00). Si no cabe ninguno, no generes nada y avisa al dueño (en español) de cuándo se renuevan los créditos.
- Cada vídeo que hagas, apúntalo en `agenda.md` (fecha, hora, título, enlace) y haz commit + push.
  - Indica en el resumen final cuántos vídeos se hicieron y por qué.
- Etiquetas de eleven_v4: como mucho 1–2, en inglés, para el pico (`[intrigued]` al inicio, `[shocked]` o `[dramatic]` justo antes del "In other words"). Si alguna se lee en voz alta, quítala.
- `creative_generate_speech` con model_id `eleven_v4`, voice_id `hqsADTrqjrr0sI9LFcYV` (Dean, inglés americano, cálido y claro), generations_count **1**. No reintentar llamadas: cada una cobra.
- Esperar (sleep) y `creative_get_flow_run_status` hasta completed; descargar el mp3 con curl (`elevenlabsusercontent.com` está permitido) a `work/vNN/voz.mp3`.
- **La voz es prioritaria.** Escribe el guion para ser escuchado: frases cortas, sin pausas ("..."), con los números y nombres al final de la frase, donde la voz carga el énfasis. Termina el texto SIN punto final en la frase cortada (p. ej. `He saved`) para que la entonación quede en el aire.
- `creative_transcribe_audio` con `eleven_scribe_v1`, el mismo flow_id y connect_from = node_id del audio (es gratis). Descargar `words_download_url` a `work/vNN/words.json`.
- **Acelerar al ritmo viral:** `python3 pipeline/acelerar.py work/vNN` (recorta silencios del principio y del final y lleva la voz a ~195 palabras/min, como los Shorts de 10 M; reescala `words.json`). Los Shorts analizados van a 190–215 ppm; Dean suelto va a ~165. Escucha el resultado: si suena atropellado, usa un factor menor (`… work/vNN 1.08`).
- Control de calidad de la voz: compara la transcripción con el guion. Si falta o cambia alguna palabra, si se lee en voz alta una etiqueta o si la duración (ya acelerada) queda fuera de 36–46 s, regenera esa voz una vez (cuesta créditos: solo si hace falta).

## 3. Montaje (estilo ANIMADO 2D — es el estilo fijo del canal)
El vídeo es una animación vectorial tipo "explainer": escenas dibujadas, el personaje propio del canal, movimientos de cámara y etiquetas de datos. Motor: `pipeline/anim.py`. Ejemplo completo a imitar: `ejemplos/escenas_torre_eiffel.py`.

1. Escribe `work/vNN/escenas.py` (empieza con `from anim import *`):
   - **Algo nuevo cada 2–3 s** (formato v3: 10–14 escenas en las que la cámara viaja; cortes secos solo en saltos grandes; nunca más de 3,5 s sin un cambio visible). El inicio de cada escena = segundo en que empieza esa palabra en `words.json`. Dentro de cada escena la cámara SIEMPRE se mueve (zoom lento hacia dentro o paneo): nada estático.
   - **Escena 1 = el protagonista en primer plano desde el fotograma 0** (sin fundidos ni títulos) y la **última escena = la misma imagen que la escena 1**, para que el salto del bucle no se note.
   - Cada escena es `def eN(ctx, lt, dur, T):` y SIEMPRE: fija la cámara con `camera(ctx, zoom, cx, cy)` usando `keyframes(...)` para que se mueva (acercar, alejar, desplazar), dibuja un fondo (`bg_night`, `bg_sky`, `bg_dark`, `bg_blueprint`, `ground`, `sun`…) y el protagonista del tema.
   - Dibuja el objeto del tema con primitivas de cairo (como la función `tower` del ejemplo): un avión, un planeta, un corazón, un puente… Formas planas con degradados suaves, paleta azul marino/morado de fondo y colores vivos para lo importante. Los emojis de OpenMoji (`icon`) solo como objetos secundarios.
   - El personaje del canal (`character`) aparece en al menos 2 escenas, con la expresión que pida la frase (`duda`, `sorpresa`, `feliz`, `dormido`; `helmet=True`, `wave=1.0`…). NO pongas "FOLLOW" ni despedida al final (rompe el bucle). Todas las etiquetas y textos en pantalla, en inglés americano (MPH, MILES, POUNDS, °F…).
   - **Personajes famosos (18/11/2026):** cada vez que la voz nombre a alguien conocido, en ese plano aparece su **ficha** para que el espectador lo ubique al instante: `ficha(ctx, "THOMAS EDISON", "INVENTOR · 1847–1931", x, y, pop(lt, t), "💡", YELLOW)` (nombre gigante + a qué se dedica/años + su objeto icónico en el círculo). Si el famoso es el protagonista, su ficha va también en el plano del gancho (y por tanto en el último, por el bucle). **No se usan fotos de personas reales** (ni descargadas ni copiadas): solo la ficha, su objeto icónico y siluetas genéricas (`gent` en ejemplos/escenas_edison_bucle_en.py).
   - Datos en pantalla con `pill` (etiqueta con borde), `badge` (etiqueta roja), `digital_clock`, `counter`, `line_chart`, `arrow`. Que aparezcan con `pop(lt, segundo)` justo cuando la voz dice el dato.
   - Todo lo importante dentro de la zona segura: x 80–1000, y 250–1550 (abajo van los subtítulos y la interfaz de YouTube).
   - `ESCENAS = [(0.0, e1), (t2, e2), ...]`. Subtítulos: por defecto el estilo nuevo (`ESTILO_SUBTITULO = "grande"`): **una palabra gigante** amarilla con borde negro, como los Shorts virales. No pongas `PALABRAS_POR_SUBTITULO` (por defecto 1). **Desde el 26/11/2026 va ABAJO (`Y_SUBTITULO = 1430`, `TAM_SUBTITULO = 135`) y nunca puede tapar lo esencial**; por escena se cambia con `eN.cap_y` (ver 3b). Ejemplo: `ejemplos/escenas_v28_historia_en.py`.
   - `COLA = 0.08` (por defecto): el vídeo acaba justo en la última palabra.
   - Sonido: el ambiente debe ser de FONDO, solo para que el espectador esté a gusto. La música ambiental suave y los "whoosh" discretos de cambio de escena se ponen solos (pipeline/sonido.py) y la voz se trata sola. Opcional y con moderación: `SFX = [(t, "pop"), (t, "ding")]` (máximo 4–5 por vídeo, solo en los datos clave).
2. Revisa: `python3 pipeline/anim.py work/vNN preview 1 5 9 ...` (un instante de cada escena) y mira las imágenes con Read. Corrige lo que se salga, se solape o se vea vacío. Repite hasta que todas las escenas se vean bien.
3. Render: `python3 pipeline/anim.py work/vNN` → `short.mp4` en 1440x2560 (2K) a 60 fps con codificación de alta calidad (tarda ~2 min por vídeo; no bajar la calidad).
4. Escribe también `work/vNN/meta.json` en inglés: `title` (≤ 90 caracteres: pregunta o afirmación con el NOMBRE del protagonista, p. ej. "What Happened To Edison's Last Breath? 🧪 #shorts"), `description` (2 frases + hashtags en inglés: #didyouknow #facts #curiosities #shorts…) y `tags`.
5. Cada vídeo tiene que parecer distinto: cambia fondos, colores de acento, objetos y planos de cámara entre vídeos.
6. **Miniatura (obligatoria, 18/11/2026).** Añade al final de `escenas.py` una función `MINIATURA(ctx)` y genera `python3 pipeline/miniatura.py work/vNN/escenas.py work/vNN/miniatura.jpg` (1080x1920). Reglas:
   - Visual sobre el tema, dibujado con las mismas piezas del vídeo (el protagonista grande, en el centro, con luz/brillo), + `thumb_vignette`.
   - **No desvela nada**: ni la causa, ni el dato final, ni la respuesta. Es parte del gancho: plantea la pregunta o la contradicción y obliga a ver el vídeo.
   - Texto con `thumb_text`: 2 líneas de 2–3 palabras como mucho (amarillo + blanco), arriba (y≈250–300). Fórmulas: pregunta ("WHAT'S INSIDE?"), contradicción ("LIGHTS OFF. ZERO CRASHES."), acusación ("THIS MOON IS A LIE", "IT'S NOT THE CHEF"). Nada falso ni exagerado.
   - Un elemento de "mira aquí": `thumb_circle` rojo alrededor del detalle misterioso y/o `thumb_arrow`, o un objeto tapado con "?".
   - Lo importante entre y 250 y 1700 (los bordes se recortan en algunas vistas). Revisa la imagen con Read antes de subirla.
   - Ejemplos: `ejemplos/escenas_edison_bucle_en.py` (función MINIATURA) y `miniaturas/*.py` (vídeos antiguos).

### 3b. CLARIDAD VISUAL (orden del dueño, 25/11/2026) — el espectador lo entiende todo sin pensar
Regla de oro: **si quitas el sonido, la historia se sigue igual solo con las imágenes.** Cada plano enseña literalmente lo que dice la voz en ese momento.
- **Una idea por plano.** Máximo 3 elementos en pantalla: el protagonista del plano (grande, en el centro), 1 etiqueta y, si hace falta, 1 flecha. Nada decorativo que compita.
- **Mostrar, no decir.** Si la voz dice "cut it into 240 pieces", se ve el objeto partiéndose y el contador llegando a 240. Si dice "moved to Wichita", se ve el coche llegando al cartel. Nada de planos genéricos (estrellas, fondos vacíos) mientras la voz cuenta algo concreto.
- **Toda silueta lleva nombre.** Cada persona que aparece tiene su ficha o una etiqueta corta encima (`pill`): "HARVEY", "COUSIN", "REPORTER". Nunca una silueta sin identificar.
- **Números, fechas y lugares, siempre en pantalla** en el momento exacto en que se dicen: fecha → calendario; lugar → mapa con pin y nombre; cifra → `counter` grande; dinero → billete/etiqueta con $.
- **Comparaciones con cosas conocidas** cuando hay tamaños o cantidades: al lado de una persona, de un móvil, de un autobús…
- **Antes → después** para los giros: dos estados lado a lado o una transformación animada (plata → ✗ → latón), con flecha entre ellos.
- **Texto en pantalla de 1–3 palabras**, en mayúsculas, grande (≥ 50 px) y con contraste fuerte; dentro de la zona segura y sin tapar ni quedar tapado por el subtítulo gigante (ver la regla de subtítulos).
- **"In other words"**: el plano siguiente enseña la frase brutal de forma literal (sello "STOLEN" sobre el objeto, etc.).
- **Colores con significado** y fijos en todo el vídeo: rojo = peligro/prohibido/mentira, verde = verdad/confirmado, amarillo = dato clave.
- **Los subtítulos NUNCA tapan lo esencial (orden del dueño, 25/11/2026).** La palabra gigante ocupa una franja de unos ±90 px alrededor de su altura: en esa franja no puede haber el protagonista, una cara, un dato, una etiqueta ni la acción del plano. Por defecto va **ABAJO (`Y_SUBTITULO = 1430`, `TAM_SUBTITULO = 135`; orden del dueño del 26/11/2026)** y lo esencial se encuadra encima (y 250–1300). Si en un plano el hueco libre está arriba, se cambia solo para esa escena con `eN.cap_y = 300`. Las etiquetas (`pill`, `badge`, calendarios) se colocan fuera de la franja del subtítulo. En la hoja de previews se comprueba plano a plano: si el subtítulo pisa algo importante, se mueve el subtítulo o el objeto antes de renderizar.
- **Revisión obligatoria antes de renderizar ("prueba del mudo")**: mira la hoja de previews en orden y escribe para ti la historia que cuentan las imágenes. Si algún plano no se entiende sin la voz, rehazlo.

## 4. Publicar los vídeos en GitHub (rama `media`)
```
cd /home/claude/shorts-curiosidades
git checkout --orphan media-tmp && git rm -rq --cached . 2>/dev/null; rm -rf media; mkdir media
cp work/vNN/short.mp4 → media/AAAAMMDD_1.mp4 y media/AAAAMMDD_2.mp4
cp work/vNN/miniatura.jpg → media/AAAAMMDD_1.jpg y media/AAAAMMDD_2.jpg
git add media && git commit -m "media AAAAMMDD" && git push -f origin HEAD:media
git rev-parse HEAD   → SHA
git checkout -f main
```
URL de cada vídeo: `https://raw.githubusercontent.com/ch1qu1t1t0tumadre-eng/shorts-curiosidades/SHA/media/AAAAMMDD_N.mp4`
(La rama `media` se sobrescribe cada día; así el repositorio no crece.)

## 5. Subir a YouTube Studio (navegador integrado, `mcp__remote-devices__Claude_Browser__*`)
Canal: https://studio.youtube.com/channel/UC-xRUl9MD0FkZ94w83yAFKQ — la sesión ya está iniciada y los sitios permitidos.
Para cada vídeo, en el hueco que le toque según `agenda.md` (20:00, 23:00 o 01:00 del día siguiente; fin de semana 20:00 o 23:00):
1. `navigate` a `https://studio.youtube.com/channel/UC-xRUl9MD0FkZ94w83yAFKQ/videos/upload?d=ud`
2. `javascript_tool` (inyecta el archivo interceptando el selector de archivos):
```js
const r = await fetch('URL_RAW');
window.__v = new File([await r.blob()], 'NOMBRE.mp4', {type:'video/mp4'});
if(!window.__origClick) window.__origClick = HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click = function(){ if(this.type==='file' && window.__v){ const dt=new DataTransfer(); dt.items.add(window.__v); this.files=dt.files; window.__v=null; setTimeout(()=>{this.dispatchEvent(new Event('input',{bubbles:true}));this.dispatchEvent(new Event('change',{bubbles:true}))},50); return;} return window.__origClick.call(this); };
'ok '+r.status
```
3. `find` "Seleccionar archivos" y hacer clic en el botón (o, si el diálogo ya pasó a Detalles, seguir).
4. Título y descripción con JS (NO teclear: el autocompletado de hashtags estropea el texto):
```js
function all(root,sel,out=[]){root.querySelectorAll(sel).forEach(x=>out.push(x));root.querySelectorAll('*').forEach(x=>{if(x.shadowRoot)all(x.shadowRoot,sel,out)});return out}
function setBox(el,text){el.focus();document.execCommand('selectAll',false,null);document.execCommand('insertText',false,text);el.dispatchEvent(new Event('input',{bubbles:true}));el.blur();}
const [t,d]=all(document,'#textbox'); setBox(t,'TITULO de meta.json'); await new Promise(r=>setTimeout(r,300)); setBox(d,'DESCRIPCION');
all(document,'tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]')[0].click();
all(document,'#textbox').map(e=>e.innerText)
```
4b. **Miniatura** (en la pantalla de Detalles, antes de pasar de paso): copia `miniatura.jpg` a la rama `media` junto al vídeo (`media/AAAAMMDD_N.jpg`) y, con `javascript_tool`, repite la inyección del paso 2 con la URL raw del .jpg (`type:'image/jpeg'`) y pulsa `ytcp-thumbnail-uploader #select-button` (botón "Subir archivo" de la sección Miniatura). Espera ~5 s y comprueba que aparece la imagen en la sección Miniatura. Si el botón no existe o YouTube pide verificar la cuenta, sigue sin miniatura y avísalo en el resumen.
   - Para un vídeo ya subido: `https://studio.youtube.com/video/ID/edit` → misma inyección → "Subir archivo" → esperar 5–7 s → `ytcp-button#save` (a veces hay que pulsarlo 2 veces; está bien cuando queda deshabilitado). Probado el 18/11/2026.
   - Si `setBox` no cambia el texto (pasa cuando el panel del navegador está oculto: `execCommand` devuelve false), escribe con `find` "textbox" → `triple_click` en el título (ref) + `ctrl+a` + `type`, y `left_click` en la descripción + `type`; pulsa `Escape` tras cada uno para cerrar las sugerencias de hashtags (no cierra el diálogo). Comprueba con JS que los dos `#textbox` tienen el texto correcto.
5. Pulsar `#next-button` 3 veces (esperar ~1,2 s entre clics) hasta el paso Visibilidad.
6. Programar (probado el 17/11/2026): `#next-button` 3 veces → en Visibilidad pulsar `#second-container-expand-button` ("Programar").
   - Fecha: `find` "textbox" → hay dos: la hora ("0:00") y, tras abrir el calendario con `#datepicker-trigger` (o clic en la fecha), el campo de fecha. Hacer `triple_click` en el campo de fecha (por ref), escribir p. ej. `17 nov 2026` con `type` y pulsar Return. (Escribir con JS NO funciona.)
   - Hora: abrir la lista de horas con JS (`const inp=all(document,'input').find(i=>i.value==='0:00'); inp.click(); inp.focus();`, esperar 0,8 s; los clics de ratón en el campo a veces no la abren) y, con JS, hacer clic en la opción exacta: `all(document,'tp-yt-paper-item, [role=option]').find(o=>o.innerText.trim()==='17:00').click()`.
   - Comprobar con JS que `#datepicker-trigger` muestra la fecha correcta y el input de hora la hora correcta, y que no aparece "Selecciona una fecha y una hora en el futuro". La zona horaria por defecto es GMT+1 (Madrid).
   - Pulsar `#done-button` (pone "Programar"). El diálogo final confirma "El vídeo pasará a ser público el … a las …" y da el enlace youtube.com/shorts/ID.
7. Comprobar en `…/videos/short` que el vídeo aparece como "Programado" con la hora correcta y que no hay duplicados. Guardar el enlace `youtube.com/shorts/ID`.

Si el ordenador no responde (navegador integrado offline): guardar igualmente los vídeos en la rama `media`, y avisar al dueño con los enlaces raw para que los suba él.

## 6. Cerrar
- Añadir los 2 temas a `temas_usados.md`, commit y push a `main`.
- Enviar al dueño (SendUserMessage + notificación): título, hora y enlace de cada vídeo, créditos de ElevenLabs que quedan, y recordarle que los revise antes de las 20:00. Indicar cualquier problema.

## Coste aproximado
Voz con eleven_v4: ~680 créditos por vídeo (35–45 s) → 2/día ≈ 41.000/mes. Plan Starter: 30.000 → da para ~44 vídeos/mes. Plan Creator (121.000) daría de sobra.

## Vídeos preparados por adelantado
Si `agenda.md` marca un hueco de hoy como **PREPARADO**, el vídeo ya está hecho: descárgalo de la rama `media-lote` (`media/vNN.mp4` + `media/vNN.jpg`), súbelo con el título/descripción de la tabla del lote, ponle la miniatura y prográmalo. No generes voz ni animación para ese hueco. Si un hueco dice "falta PROGRAMAR", el vídeo ya está subido en privado: abre `studio.youtube.com/video/ID/edit` → Visibilidad → Programar a esa hora.
- Si YouTube pide "Verificación única obligatoria" al subir una miniatura, pulsa Cancelar, sigue sin miniatura y avisa al dueño (el límite diario de miniaturas se quita verificando el canal con el teléfono; eso solo lo puede hacer él).
- Si el panel del navegador está oculto (`document.visibilityState === 'hidden'`), la fecha y la hora de programación no se pueden elegir: avisa al dueño para que deje visible la app de Claude.

## Ritmo: 3 al día mientras se pueda, luego bajar (orden del dueño, 19/11)
- Objetivo: L–V 3 vídeos (20:00, 23:00, 01:00 del día siguiente); S–D 2 vídeos (20:00, 23:00).
- Antes de generar voz, mira los créditos de ElevenLabs (`account_get_usage`). Cada vídeo gasta ~800. **Plan Creator (121.125/mes, renovación el día 24) compartido con Behind the HUD**, que hace 2 vídeos al día (decisión del dueño, 25/11/2026: Wait, What. 3/día + Behind the HUD 2/día).
- Cada día haz tantos vídeos como quepan, hasta el máximo del día (3 entre semana, 2 en fin de semana): `min(MAX_DIA, (créditos_libres − 3.000) // 850)`, menos los huecos ya PREPARADOS (los 3.000 de reserva protegen los 2 vídeos diarios de Behind the HUD).
  - Si caben 3 → 3. Si solo caben 2 → 2 (20:00 y 23:00). Si cabe 1 → 1 (20:00). Si no cabe ninguno → no generes; sube solo lo PREPARADO y avisa al dueño de que los créditos se renuevan el día X.
- Los vídeos PREPARADOS de `agenda.md` no gastan créditos: súbelos siempre.
- Cuando bajes el ritmo, apúntalo en `agenda.md` (línea "Ritmo actual: N/día desde FECHA, motivo") para que el dueño lo vea.
