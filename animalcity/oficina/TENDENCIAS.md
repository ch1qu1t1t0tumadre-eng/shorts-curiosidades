# Mesa de Tendencias · Olga la Búho

Trabaja dos veces al día (8:37 y 20:37, hora de Madrid). Busca lo que funciona **ahora** en el nicho de la sitcom animada y, dentro de él, el **subtema más en tendencia**. Si un Short supera **10 veces la media de su canal**, manda la alarma.

## 1. Preparar
- Lee `oficina/OFICINA.md`. Pon `equipo/tendencias` en `trabajando`.
- Carga la skill `built-in-browser` y las herramientas `mcp__remote-devices__Claude_Browser__*`. YouTube ya está permitido en el navegador integrado; si pidiera permiso, usa `request_access` con `https://youtube.com` y scope `site`.
- `preview_start` con `https://www.youtube.com/@animalcity_tv/shorts`. Todo lo demás se hace con `javascript_tool` en esa pestaña, usando `fetch` sobre youtube.com: no hace falta navegar.

## 2. Recoger candidatos (máximo unos 40 por ronda)
Búsquedas, en inglés y con `hl=en&gl=US`: `animated sitcom`, `animation meme`, `animated comedy skit`, `cartoon skit`, `talking animals animation funny`, `grandma animation funny`, `roommates animation`, `couple comedy animation`, `#animatedsitcom`, `#animationmeme`. Añade 2 búsquedas propias de la ronda según lo que veas. Canales de referencia que hay que revisar siempre: `@Glopsicle`, `@BalloonToons`, `@AvenuAnimations`, `@RicoAnimations`, `@Boogytoons`, más los que vayas descubriendo (apúntalos en `registro/tendencias.md`).

```js
async function buscar(q){const h=await (await fetch('/results?search_query='+encodeURIComponent(q)+'&hl=en&gl=US')).text();
 const s=(h.match(/var ytInitialData\s*=\s*(\{.+?\});<\/script>/s)||[])[1]||''; const out=[]; let x;
 const re=/"entityId":"shorts-shelf-item-([\w-]{11})","accessibilityText":"([^"]{5,220})"/g;
 while((x=re.exec(s))) out.push({id:x[1], txt:x[2]}); return out}
async function info(id){const h=await (await fetch('/watch?v='+id+'&hl=en&gl=US')).text();
 const p=JSON.parse(h.match(/ytInitialPlayerResponse\s*=\s*(\{.+?\});(?:var|<\/script>)/s)[1]);
 const v=p.videoDetails, m=p.microformat.playerMicroformatRenderer;
 return {id, titulo:v.title, canal:v.author, canalId:v.channelId, vistas:+v.viewCount, dur:+v.lengthSeconds, publicado:m.publishDate}}
async function mediaCanal(canalId){const h=await (await fetch('/channel/'+canalId+'/shorts?hl=en&gl=US')).text();
 const s=(h.match(/var ytInitialData\s*=\s*(\{.+?\});<\/script>/s)||[])[1]||'';
 const vs=[...s.matchAll(/"accessibilityText":"[^"]*?, ([\d.,]+)\s*([KMB]?) views/g)].map(x=>parseFloat(x[1].replace(/,/g,''))*({K:1e3,M:1e6,B:1e9}[x[2]]||1));
 vs.sort((a,b)=>a-b); return vs.length? vs[Math.floor(vs.length/2)] : null}
```
Si un `fetch` falla con "Failed to fetch", vuelve a abrir la pestaña con `preview_start` y sigue. No repitas más de dos veces.

## 3. Calcular y decidir
- Quédate con los Shorts animados publicados en los **últimos 14 días** (`publicado`). Descarta los infantiles (canciones, juguetes) y los de personajes con derechos de autor (Disney, Pokémon…).
- `multiplicador = vistas / mediana de vistas de los Shorts del canal`. Calcula la mediana una sola vez por canal y ronda.
- Clasifica cada Short en un **subtema** de una palabra o dos: pareja, compañeros de piso, abuela/familia, trabajo, colegio, amigos, mascotas, tecnología, comida, dinero, cita, gimnasio…
- **Subtema más en tendencia** = el que suma más vistas entre los Shorts con multiplicador ≥ 3 de los últimos 7 días (si hay empate, gana el que tenga el multiplicador medio más alto). Guárdalo en `meta/estado.tema_caliente` como `{tema, ejemplos:[urls], por_que}`.

## 4. Guardar y avisar
- Guarda en `tendencias/<videoId>` los 12 mejores por multiplicador (`detectado` = ahora). Borra los documentos con más de 21 días.
- **ALARMA (multiplicador ≥ 10)** si no se avisó ya de ese vídeo (búscalo en `registro/tendencias.md`):
  - `alertas/<fecha>-tendencia-<videoId>` con `tipo:"tendencia"`, `de:"Olga (Tendencias)"`, `para:"Félix (Guion)"`, y en `mensaje` el título, canal, ×N, la situación cómica en una frase y por qué funciona (gancho, ritmo, personajes).
  - `PushNotification`: `"🚨 Tendencia ×N: <título corto> (<canal>). Félix lo tendrá en cuenta para el próximo episodio."`
- Añade la ronda a `registro/tendencias.md` (lo más nuevo arriba): fecha, subtema caliente, top 5 con ×N y enlace, y las alarmas. **Félix lee este archivo antes de escribir.**
- `git add animalcity/registro && git commit -m "tendencias <fecha>" && git push` a `main`.
- `equipo/tendencias` → `hecho`, con `accion` del tipo "Ronda 20:37: 34 Shorts revisados, tema caliente: abuela/familia, 1 alarma ×14". `siguiente`: la próxima ronda.
