# Rutina diaria: 2 Shorts de curiosidades

Canal: curiosidades de todo tipo. **TODO EN INGLÉS AMERICANO** (guion, voz, textos en pantalla, subtítulos, título, descripción y hashtags), pensado para público de EE. UU. Categorías (ir rotando, que no se repita la misma dos días seguidos): animales, historia, cuerpo humano, ingeniería, **aviación**, **astronomía y espacio**, ciencia, geografía, tecnología, comida, océanos, mente y psicología…
Cada día se crean **2 Shorts** y se suben a YouTube Studio en **privado y programados** a las **17:00 y 20:00 (Europe/Madrid)**. El dueño los revisa antes y borra o edita los que no le gusten.
(La voz es propia del canal y se genera aquí mismo con `pipeline/narrador.py`: sin ElevenLabs, sin créditos y sin límite. Siempre 2 vídeos al día.)

## 0. Preparar
1. `add_repo` ch1qu1t1t0tumadre-eng/shorts-curiosidades con access "push", clonarlo en /home/claude/shorts-curiosidades.
2. `bash pipeline/setup.sh`
3. Leer `temas_usados.md` (no repetir ningún tema).

## 1. Elegir el tema y escribir los 2 guiones (rol: el creador de Shorts más influyente de nuestra época)
Actúa como un creador de vídeos cortos de primer nivel, experto en todos los temas del canal, en psicología del consumidor y en técnicas de atención y retención.

**Nicho:** "Hidden reasons behind everyday things" — curiosidades con un "por qué" oculto detrás de cosas que todo el mundo ve o vive (aviones, cuerpo, animales, espacio, ingeniería, historia…) y que cambian cómo miras el mundo. No datos sueltos: cada vídeo revela algo que "nadie te explicó" y deja una idea práctica.
**Audiencia:** EE. UU., 18–34 años, móvil, scroll rápido; curiosos que ven Shorts en ratos muertos (cola, transporte, antes de dormir); les gusta sentirse "más listos que los demás" y compartir el dato con amigos. Atención de 1–2 s para decidir si se quedan.

**Elegir tema:** 2 temas sin repetir (`temas_usados.md`), categorías distintas y rotando. Prioriza temas con: (a) algo que el espectador ha visto o vivido, (b) una creencia común falsa o un "nadie te lo dice", (c) un consejo práctico al final. Verifica cada dato con WebSearch (fuentes fiables). Si algo no se confirma, fuera.

**Estructura del guion (35–45 s, 600–750 caracteres, ~110–125 palabras):**
1. **HOOK (0–3 s):** una frase imposible de ignorar: afirmación fuerte, contraintuitiva o "polémica" (pero 100 % verdadera), que cree tensión. + **hook visual** para la escena 1 (algo que se mueve/cambia en el primer segundo: zoom brusco, objeto que aparece, cifra gigante).
2. **LOOP DE CURIOSIDAD (3–6 s):** abre una pregunta que solo se resuelve al final ("Stay till the end, because…").
3. **CUERPO:** el **problema** (creencia común / error / lo que nadie explica) → la **explicación real** en golpes cortos → **consejo accionable concreto** (no genérico). Cambio de ritmo cada 3–5 s (nueva escena, zoom, cifra, giro "But here's the crazy part…"). Disparadores emocionales: sorpresa, "esto te afecta a ti", sensación de saber un secreto.
4. **RESOLUCIÓN DEL LOOP + CTA (últimos 5 s):** resuelve la pregunta del inicio y termina con un CTA natural ligado al tema: una pregunta para comentar + "follow for…" con promesa concreta. Si se puede, que la última frase enlace con la primera (replay).
- Frases de ≤ 10 palabras, tono conversacional y con energía, inglés americano natural. Nada de consejos genéricos ni relleno.
- "Polémico" = encuadre contraintuitivo, nunca exagerar ni inventar. Nada de alarmismo médico, política o tragedias recientes.

**Guarda `work/vNN/guion.md`** con: nicho/ángulo, el texto exacto para la voz y una tabla por bloque: tiempo · voz · escena/plano de cámara (zoom, paneo, primer plano…) · elementos visuales (equivalente a b-roll en animación) · texto en pantalla (≤ 4 palabras) · caption. Ese guion manda en el diseño de las escenas (paso 3).

## 2. Voz (propia del canal, sin ElevenLabs)
- La voz del narrador está guardada en `pipeline/narrador.py` (`NARRADOR`). Es siempre la misma: no la cambies. No se usa ElevenLabs para nada.
- Guarda el texto exacto de la voz en `work/vNN/texto_voz.txt`. Puedes usar 1–2 etiquetas `[excited]` (más vivo) o `[curious]` (más pausado) donde aporten, y "..." para la pausa antes del dato clave. Escribe los números en palabras cuando haya duda de cómo se leen ("thirty-five thousand feet").
- `python3 pipeline/narrador.py work/vNN` → `voz.mp3` + `words.json` (mismo formato que antes, con el segundo de cada palabra). Tarda unos segundos.
- **La voz es prioritaria.** Escribe el guion para ser escuchado: frases cortas, ritmo y una pausa ("...") antes del dato clave.
- Comprueba la duración que imprime: entre 35 y 45 s. Si se pasa, recorta el guion (no aceleres la voz); si se queda corta, añade una frase.

## 3. Montaje (estilo ANIMADO 2D — es el estilo fijo del canal)
El vídeo es una animación vectorial tipo "explainer": escenas dibujadas, el personaje propio del canal, movimientos de cámara y etiquetas de datos. Motor: `pipeline/anim.py`. Ejemplo completo a imitar: `ejemplos/escenas_torre_eiffel.py`.

1. Escribe `work/vNN/escenas.py` (empieza con `from anim import *`):
   - Una escena por frase del guion (5–8 escenas). El inicio de cada escena = segundo en que empieza esa frase en `words.json`.
   - Cada escena es `def eN(ctx, lt, dur, T):` y SIEMPRE: fija la cámara con `camera(ctx, zoom, cx, cy)` usando `keyframes(...)` para que se mueva (acercar, alejar, desplazar), dibuja un fondo (`bg_night`, `bg_sky`, `bg_dark`, `bg_blueprint`, `ground`, `sun`…) y el protagonista del tema.
   - Dibuja el objeto del tema con primitivas de cairo (como la función `tower` del ejemplo): un avión, un planeta, un corazón, un puente… Formas planas con degradados suaves, paleta azul marino/morado de fondo y colores vivos para lo importante. Los emojis de OpenMoji (`icon`) solo como objetos secundarios.
   - El personaje del canal (`character`) aparece en al menos 2 escenas, con la expresión que pida la frase (`duda`, `sorpresa`, `feliz`, `dormido`; `helmet=True`, `wave=1.0`…). Siempre en la escena final saludando junto a la etiqueta "FOLLOW". Todas las etiquetas y textos en pantalla, en inglés americano (MPH, MILES, POUNDS, °F…).
   - Datos en pantalla con `pill` (etiqueta con borde), `badge` (etiqueta roja), `digital_clock`, `counter`, `line_chart`, `arrow`. Que aparezcan con `pop(lt, segundo)` justo cuando la voz dice el dato.
   - Todo lo importante dentro de la zona segura: x 80–1000, y 250–1550 (abajo van los subtítulos y la interfaz de YouTube).
   - `ESCENAS = [(0.0, e1), (t2, e2), ...]` y `PALABRAS_POR_SUBTITULO = 2`.
   - Sonido: el ambiente debe ser de FONDO, solo para que el espectador esté a gusto. La música ambiental suave y los "whoosh" discretos de cambio de escena se ponen solos (pipeline/sonido.py) y la voz se trata sola. Opcional y con moderación: `SFX = [(t, "pop"), (t, "ding")]` (máximo 4–5 por vídeo, solo en los datos clave).
2. Revisa: `python3 pipeline/anim.py work/vNN preview 1 5 9 ...` (un instante de cada escena) y mira las imágenes con Read. Corrige lo que se salga, se solape o se vea vacío. Repite hasta que todas las escenas se vean bien.
3. Render: `python3 pipeline/anim.py work/vNN` → `short.mp4` en 1440x2560 (2K) a 60 fps con codificación de alta calidad (tarda ~2 min por vídeo; no bajar la calidad).
4. Escribe también `work/vNN/meta.json` en inglés: `title` (≤ 90 caracteres, gancho + emoji + " #shorts"), `description` (2 frases + hashtags en inglés: #didyouknow #facts #curiosities #shorts…) y `tags`.
5. Cada vídeo tiene que parecer distinto: cambia fondos, colores de acento, objetos y planos de cámara entre vídeos.

## 4. Publicar los vídeos en GitHub (rama `media`)
```
cd /home/claude/shorts-curiosidades
git checkout --orphan media-tmp && git rm -rq --cached . 2>/dev/null; rm -rf media; mkdir media
cp work/vNN/short.mp4 → media/AAAAMMDD_1.mp4 y media/AAAAMMDD_2.mp4
git add media && git commit -m "media AAAAMMDD" && git push -f origin HEAD:media
git rev-parse HEAD   → SHA
git checkout -f main
```
URL de cada vídeo: `https://raw.githubusercontent.com/ch1qu1t1t0tumadre-eng/shorts-curiosidades/SHA/media/AAAAMMDD_N.mp4`
(La rama `media` se sobrescribe cada día; así el repositorio no crece.)

## 5. Subir a YouTube Studio (navegador integrado, `mcp__remote-devices__Claude_Browser__*`)
Canal: https://studio.youtube.com/channel/UC-xRUl9MD0FkZ94w83yAFKQ — la sesión ya está iniciada y los sitios permitidos.
Para cada vídeo (el 1 a las 17:00, el 2 a las 20:00):
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
5. Pulsar `#next-button` 3 veces (esperar ~1,2 s entre clics) hasta el paso Visibilidad.
6. Programar (probado el 17/11/2026): `#next-button` 3 veces → en Visibilidad pulsar `#second-container-expand-button` ("Programar").
   - Fecha: `find` "textbox" → hay dos: la hora ("0:00") y, tras abrir el calendario con `#datepicker-trigger` (o clic en la fecha), el campo de fecha. Hacer `triple_click` en el campo de fecha (por ref), escribir p. ej. `17 nov 2026` con `type` y pulsar Return. (Escribir con JS NO funciona.)
   - Hora: abrir la lista de horas haciendo clic en el campo de hora y, con JS, hacer clic en la opción exacta: `all(document,'tp-yt-paper-item, [role=option]').find(o=>o.innerText.trim()==='17:00').click()`.
   - Comprobar con JS que `#datepicker-trigger` muestra la fecha correcta y el input de hora la hora correcta, y que no aparece "Selecciona una fecha y una hora en el futuro". La zona horaria por defecto es GMT+1 (Madrid).
   - Pulsar `#done-button` (pone "Programar"). El diálogo final confirma "El vídeo pasará a ser público el … a las …" y da el enlace youtube.com/shorts/ID.
7. Comprobar en `…/videos/short` que el vídeo aparece como "Programado" con la hora correcta y que no hay duplicados. Guardar el enlace `youtube.com/shorts/ID`.

Si el ordenador no responde (navegador integrado offline): guardar igualmente los vídeos en la rama `media`, y avisar al dueño con los enlaces raw para que los suba él.

## 6. Cerrar
- Añadir los 2 temas a `temas_usados.md`, commit y push a `main`.
- Enviar al dueño (SendUserMessage + notificación): título, hora y enlace de cada vídeo, y recordarle que los revise antes de las 17:00. Indicar cualquier problema.

## Coste aproximado
Voz: propia y local (`pipeline/narrador.py`), sin coste.
