# Rutina diaria: 2 Shorts de curiosidades

Canal: curiosidades de todo tipo (animales, historia, cuerpo humano, ingeniería, espacio, ciencia, geografía, tecnología, comida…), en **español de España**.
Cada día se crean **2 Shorts** y se suben a YouTube Studio en **privado y programados** a las **17:00 y 20:00 (Europe/Madrid)**. El dueño los revisa antes y borra o edita los que no le gusten.
(Plan ElevenLabs Starter: 30.000 créditos/mes. Modelo `eleven_flash_v2_5`, ~270 créditos/vídeo → ~16.000/mes; el resto es margen para repetir voces.)

## 0. Preparar
1. `add_repo` ch1qu1t1t0tumadre-eng/shorts-curiosidades con access "push", clonarlo en /home/claude/shorts-curiosidades.
2. `bash pipeline/setup.sh`
3. Leer `temas_usados.md` (no repetir ningún tema).

## 1. Elegir y escribir los 2 guiones
- 2 temas de categorías distintas, nada repetido de `temas_usados.md`; alterna las categorías respecto a los últimos días.
- Verifica cada dato con WebSearch (fuentes fiables). Si un dato no se confirma, cámbialo.
- Guion: 80–95 palabras (30–40 s). Empieza con un gancho tipo "¿Sabías que…?" con el dato más sorprendente en la primera frase. Frases cortas. Números escritos con letras para la voz ("cuatrocientos kilos"). Termina siempre con "Síguenos para más curiosidades."
- Nada de temas delicados (tragedias recientes, política, medicina con consejos de dosis).

## 2. Voz (ElevenLabs, conector MCP)
- Antes, `account_get_usage`: si quedan menos de 700 créditos, NO generes; avisa al dueño y termina.
- `creative_generate_speech` con model_id `eleven_flash_v2_5`, voice_id `1lUeAlGYnkWZz31Wixae` (Leo, español peninsular), generations_count **1**. No reintentar llamadas: cada una cobra.
- Esperar (sleep) y `creative_get_flow_run_status` hasta completed; descargar el mp3 con curl (`elevenlabsusercontent.com` está permitido) a `work/vNN/voz.mp3`.
- `creative_transcribe_audio` con `eleven_scribe_v1`, el mismo flow_id y connect_from = node_id del audio (es gratis). Descargar `words_download_url` a `work/vNN/words.json`.

## 3. Montaje
- Escribir `work/vNN/spec.json` como `pipeline/ejemplo_spec.json`: 6–9 beats, cada beat con `t` = segundo en que se dice la palabra clave (sacado de words.json), un emoji (OpenMoji), `big` (2–3 palabras en mayúsculas, el dato) y `small` (contexto corto). `categoria` en mayúsculas. `palette` = 3 colores (fondo oscuro, medio, acento) distinta por categoría. Título ≤ 90 caracteres terminado en emoji + " #shorts". Descripción de 2 frases + hashtags.
- `python3 pipeline/render.py work/vNN` → `short.mp4` y `thumb.jpg`.
- Revisar 3 fotogramas (ffmpeg -ss) mirándolos con Read: texto que no se salga, emoji correcto.

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
const [t,d]=all(document,'#textbox'); setBox(t,'TITULO'); await new Promise(r=>setTimeout(r,300)); setBox(d,'DESCRIPCION');
all(document,'tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]')[0].click();
all(document,'#textbox').map(e=>e.innerText)
```
5. Pulsar `#next-button` 3 veces (esperar ~1,2 s entre clics) hasta el paso Visibilidad.
6. Programar: expandir la sección "Programar" (`#second-container-expand-button`), poner la fecha de hoy y la hora que le toca (17:00 o 20:00). Usar `read_page`/`find` para localizar los campos de fecha y hora; comprobar con captura que se ven bien antes de pulsar el botón final (`#done-button`, dice "Programar").
7. Comprobar en `…/videos/short` que el vídeo aparece como "Programado" con la hora correcta y que no hay duplicados. Guardar el enlace `youtube.com/shorts/ID`.

Si el ordenador no responde (navegador integrado offline): guardar igualmente los vídeos en la rama `media`, y avisar al dueño con los enlaces raw para que los suba él.

## 6. Cerrar
- Añadir los 2 temas a `temas_usados.md`, commit y push a `main`.
- Enviar al dueño (SendUserMessage + notificación): título, hora y enlace de cada vídeo, créditos de ElevenLabs que quedan, y recordarle que los revise antes de las 17:00. Indicar cualquier problema.

## Coste aproximado
Voz con eleven_flash_v2_5: ~270 créditos por vídeo de 35 s → 2/día ≈ 16.000/mes (plan Starter: 30.000).
