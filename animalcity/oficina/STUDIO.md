# Mesa de Studio · Bruno el Castor

Sube el episodio en **privado y programado** a la hora punta de la audiencia. El dueño lo puede revisar antes de que salga. **Nunca se publica como público al momento.**

## 1. Hora de publicación
- `meta/estado.hora_punta` (hora de Madrid). Si no existe, usa **00:30** (18:30 en Nueva York).
- Una vez a la semana (lunes), o si el canal ya tiene más de 1.000 visualizaciones y no hay `hora_punta`: en Studio, Estadísticas → Audiencia → "Cuándo están conectados tus espectadores". Elige la franja con más audiencia, prográmalo 1 h antes de ese pico y guárdala en `meta/estado.hora_punta`.
- La fecha es la próxima vez que llegue esa hora y que quede al menos 2 h en el futuro.

## 2. Subir el vídeo a GitHub (rama `media-animalcity`, se sobrescribe cada vez)
```
rm -rf /tmp/mediaac && mkdir -p /tmp/mediaac/media && cd /tmp/mediaac && git init -q
cp /home/claude/shorts-curiosidades/animalcity/work/epNN/short.mp4 media/epNN.mp4
cp /home/claude/shorts-curiosidades/animalcity/work/epNN/thumb_final.jpg media/epNN_thumb.jpg
cp /home/claude/shorts-curiosidades/animalcity/work/epNN/top3/* media/ 2>/dev/null
git add media && git -c user.email=noreply@anthropic.com -c user.name=Claude commit -qm "media epNN"
git push -qf https://github.com/ch1qu1t1t0tumadre-eng/shorts-curiosidades HEAD:media-animalcity
git rev-parse HEAD   → SHA
```
(No uses la rama `media`: es del canal de curiosidades. No hagas `git checkout --orphan` en la carpeta del repositorio.)
URL: `https://raw.githubusercontent.com/ch1qu1t1t0tumadre-eng/shorts-curiosidades/SHA/media/epNN.mp4`

## 3. Subir a YouTube Studio (navegador integrado; probado el 18/11/2026)
1. `preview_start` (o `navigate`) a `https://studio.youtube.com/channel/UCvhvPTVkwwCI7zkki_QaXxQ/videos/upload?d=ud`. Abre directamente el canal AnimalCity TV. Comprueba con JS que `document.querySelector('#entity-name').innerText` es "AnimalCity TV". Si no lo es, PARA: no subas nada a otro canal.
2. Inyecta el vídeo (intercepta el selector de archivos):
```js
const r = await fetch('URL_RAW_MP4');
window.__v = new File([await r.blob()], 'animalcity_epNN.mp4', {type:'video/mp4'});
if(!window.__origClick) window.__origClick = HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click = function(){ if(this.type==='file' && window.__v){ const dt=new DataTransfer(); dt.items.add(window.__v); this.files=dt.files; window.__v=null; setTimeout(()=>{this.dispatchEvent(new Event('input',{bubbles:true}));this.dispatchEvent(new Event('change',{bubbles:true}))},50); return;} return window.__origClick.call(this); };
'ok '+r.status
```
3. `find` "Seleccionar archivos" → clic en el botón. Espera unos 6 s: se abre "Detalles".
4. Título y descripción con JS (no teclees: el autocompletado de hashtags estropea el texto), y "No es contenido para niños":
```js
function all(root,sel,out=[]){root.querySelectorAll(sel).forEach(x=>out.push(x));root.querySelectorAll('*').forEach(x=>{if(x.shadowRoot)all(x.shadowRoot,sel,out)});return out}
function setBox(el,text){el.focus();document.execCommand('selectAll',false,null);document.execCommand('insertText',false,text);el.dispatchEvent(new Event('input',{bubbles:true}));el.blur();}
const [t,d]=all(document,'#textbox'); setBox(t,'TITULO'); await new Promise(r=>setTimeout(r,400)); setBox(d,'DESCRIPCION');
all(document,'tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]')[0].click();
all(document,'#textbox').map(e=>e.innerText)
```
   Si queda abierta una lista de sugerencias de hashtags, pulsa `Escape` (sin elegir nada).
5. Miniatura (ver `oficina/MINIATURAS.md`): pon `window.__v` = File de `thumb_final.jpg` (mismo código del paso 2, con `type:'image/jpeg'`) y haz clic en el botón "Subir archivo" (`find` "Subir archivo"). **Si aparece "debes verificar tu número de teléfono", pulsa Cancelar**, pon `window.__v=null` y sigue sin miniatura propia (la alerta para el dueño ya existe). Si el canal está verificado y aparece "Experimentos A/B", sube las 3 de `top3/`.
6. Pulsa `#next-button` 3 veces (esperando unos 1,3 s entre clics) hasta Visibilidad.
7. Programar: con JS haz clic en `#second-container-expand-button`. Después, con `find` "textbox", localiza el campo de fecha (p. ej. "19 nov 2026") y el de hora ("0:00"):
   - Fecha: `triple_click` en el campo de fecha (por ref), `type` "D mmm AAAA" (p. ej. `20 nov 2026`) y `key` Return.
   - Hora: clic en el campo de hora (por ref), después `find` con la hora exacta (p. ej. "0:30") y clic en la `option` que coincida exactamente (no en "10:30" ni en "20:30").
   - Comprueba con JS que `#datepicker-trigger` muestra la fecha correcta, que el input de hora muestra la hora correcta y que NO aparece "Selecciona una fecha y una hora en el futuro". La zona horaria es la de Madrid.
8. Con JS, clic en `#done-button` ("Programar"). Espera 5 s y lee en `document.body.innerText` "pasará a ser público el … a las …" y el enlace `youtube.com/shorts/ID`. Cierra con `#close-button`.
9. Comprueba en `https://studio.youtube.com/channel/UCvhvPTVkwwCI7zkki_QaXxQ/videos/short` que aparece una sola vez como "Programado".
10. Comentario fijado: después de que se publique no se puede programar, así que guárdalo en `registro/episodios.md`. Rex lo publicará y lo fijará en su primera revisión.

Si el PC no responde: deja el vídeo en la rama `media-animalcity` y manda al dueño el enlace raw para que lo suba él.

## 4. Cerrar
Panel: `episodios/epNN` con `fase:"programado"`, `publica` (ISO UTC) y `url`. `equipo/studio` → `hecho` ("Sale el <fecha> a las <hora>").
