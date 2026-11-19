# Rutina diaria: 2 Shorts de curiosidades

Canal: curiosidades de todo tipo. **TODO EN INGLÉS AMERICANO** (guion, voz, textos en pantalla, subtítulos, título, descripción y hashtags), pensado para público de EE. UU. Categorías (ir rotando, que no se repita la misma dos días seguidos): animales, historia, cuerpo humano, ingeniería, **aviación**, **astronomía y espacio**, ciencia, geografía, tecnología, comida, océanos, mente y psicología…
Cada día se publican **3 Shorts** (desde el 19/11/2026), subidos a YouTube Studio en **privado y programados** a las **17:00, 20:00 y 23:00 (Europe/Madrid)** (= 11:00, 14:00 y 17:00 en Nueva York). Muchos días ya habrá vídeos preparados por adelantado: mira `agenda.md` y haz solo los huecos libres de HOY. El dueño los revisa antes y borra o edita los que no le gusten.
(Plan ElevenLabs Starter: 30.000 créditos/mes. Modelo `eleven_v4`, la voz buena: ~1 crédito por carácter. Guiones de 600–750 caracteres → ~680 créditos/vídeo. Con 2 vídeos/día el plan Starter NO llega a todo el mes: el freno de créditos para la tarea cuando se acaban.)

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

**Elegir el ángulo:** dentro del nicho, prioriza temas con **un protagonista conocido** (persona, lugar u objeto famoso que el espectador ya reconoce) + **un giro inquietante, prohibido o absurdo** ("lo robaron", "sigue ahí", "nadie lo sabe", "lo hicieron a escondidas"). Morbo y sorpresa, siempre 100 % verdadero y verificado.

**Estructura del guion (38–45 s, 125–140 palabras, 680–780 caracteres):**
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
- Antes de nada, mira `agenda.md`: los huecos de hoy (17:00, 20:00, 23:00) que ya tengan vídeo programado NO se hacen. Si los 3 están ocupados, no generes nada: solo comprueba en Studio que siguen programados y avisa al dueño.
- Luego `account_get_usage`: `quedan = character_limit - character_count`. Haz un vídeo por cada hueco libre mientras queden **≥ 750 créditos** antes de generar cada voz (prioridad de huecos: 20:00, 23:00, 17:00). Si `quedan < 750`, no generes nada y avisa al dueño (en español) de que faltan créditos hasta la renovación (o de que puede subir al plan Creator).
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
   - **Cambio de plano cada 2–3 s** (13–18 escenas por vídeo, como los Shorts de referencia; nunca más de 3,5 s con el mismo plano). El inicio de cada escena = segundo en que empieza esa palabra en `words.json`. Dentro de cada escena la cámara SIEMPRE se mueve (zoom lento hacia dentro o paneo): nada estático.
   - **Escena 1 = el protagonista en primer plano desde el fotograma 0** (sin fundidos ni títulos) y la **última escena = la misma imagen que la escena 1**, para que el salto del bucle no se note.
   - Cada escena es `def eN(ctx, lt, dur, T):` y SIEMPRE: fija la cámara con `camera(ctx, zoom, cx, cy)` usando `keyframes(...)` para que se mueva (acercar, alejar, desplazar), dibuja un fondo (`bg_night`, `bg_sky`, `bg_dark`, `bg_blueprint`, `ground`, `sun`…) y el protagonista del tema.
   - Dibuja el objeto del tema con primitivas de cairo (como la función `tower` del ejemplo): un avión, un planeta, un corazón, un puente… Formas planas con degradados suaves, paleta azul marino/morado de fondo y colores vivos para lo importante. Los emojis de OpenMoji (`icon`) solo como objetos secundarios.
   - El personaje del canal (`character`) aparece en al menos 2 escenas, con la expresión que pida la frase (`duda`, `sorpresa`, `feliz`, `dormido`; `helmet=True`, `wave=1.0`…). NO pongas "FOLLOW" ni despedida al final (rompe el bucle). Todas las etiquetas y textos en pantalla, en inglés americano (MPH, MILES, POUNDS, °F…).
   - **Personajes famosos (18/11/2026):** cada vez que la voz nombre a alguien conocido, en ese plano aparece su **ficha** para que el espectador lo ubique al instante: `ficha(ctx, "THOMAS EDISON", "INVENTOR · 1847–1931", x, y, pop(lt, t), "💡", YELLOW)` (nombre gigante + a qué se dedica/años + su objeto icónico en el círculo). Si el famoso es el protagonista, su ficha va también en el plano del gancho (y por tanto en el último, por el bucle). **No se usan fotos de personas reales** (ni descargadas ni copiadas): solo la ficha, su objeto icónico y siluetas genéricas (`gent` en ejemplos/escenas_edison_bucle_en.py).
   - Datos en pantalla con `pill` (etiqueta con borde), `badge` (etiqueta roja), `digital_clock`, `counter`, `line_chart`, `arrow`. Que aparezcan con `pop(lt, segundo)` justo cuando la voz dice el dato.
   - Todo lo importante dentro de la zona segura: x 80–1000, y 250–1550 (abajo van los subtítulos y la interfaz de YouTube).
   - `ESCENAS = [(0.0, e1), (t2, e2), ...]`. Subtítulos: por defecto el estilo nuevo (`ESTILO_SUBTITULO = "grande"`): **una palabra gigante** amarilla con borde negro en el centro de la pantalla (y≈1060), como los Shorts virales. No pongas `PALABRAS_POR_SUBTITULO` (por defecto 1). Deja la zona y 900–1200 libre de objetos importantes (o mueve el texto con `Y_SUBTITULO`).
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
Para cada vídeo, en el hueco que le toque según `agenda.md` (17:00, 20:00 o 23:00):
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
- Enviar al dueño (SendUserMessage + notificación): título, hora y enlace de cada vídeo, créditos de ElevenLabs que quedan, y recordarle que los revise antes de las 17:00. Indicar cualquier problema.

## Coste aproximado
Voz con eleven_v4: ~680 créditos por vídeo (35–45 s) → 2/día ≈ 41.000/mes. Plan Starter: 30.000 → da para ~44 vídeos/mes. Plan Creator (121.000) daría de sobra.
