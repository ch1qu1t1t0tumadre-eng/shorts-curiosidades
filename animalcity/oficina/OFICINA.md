# La oficina de AnimalCity TV: reglas comunes para todo el equipo

Panel en vivo: https://claude.ai/artifact/Uta9z9pWjehniW1eg8Vijz (slug `e1da1bc8-f8e4-4a93-b975-315e46d319f1`).
Canal: **AnimalCity TV** `@animalcity_tv`, ID `UCvhvPTVkwwCI7zkki_QaXxQ`, Studio: https://studio.youtube.com/channel/UCvhvPTVkwwCI7zkki_QaXxQ
Al dueño se le habla en **español de España**. Los vídeos van en inglés americano.

## Equipo
| Mesa (id) | Nombre | Puesto | Instrucciones | Cuándo trabaja |
| --- | --- | --- | --- | --- |
| `tendencias` | Olga la Búho | Tendencias | `oficina/TENDENCIAS.md` | 8:37 y 20:37 (Madrid) |
| `guion` | Félix el Gato | Guion | `oficina/GUION.md` | Producción diaria, 11:23 |
| `voz` | Polly la Lora | Voz y audio | `oficina/VOZ.md` | Producción diaria |
| `animacion` | Otto el Pulpo | Animación | `oficina/ANIMACION.md` | Producción diaria |
| `miniaturas` | Cami la Camaleón | Miniaturas | `oficina/MINIATURAS.md` | Producción diaria |
| `studio` | Bruno el Castor | Studio | `oficina/STUDIO.md` | Producción diaria |
| `retencion` | Rex el Sabueso | Retención | `oficina/RETENCION.md` | 13:47 (Madrid) |

## Cómo se actualiza el panel (todas las mesas)
Herramientas `db_get`, `db_write`, `db_list` del conector de artifacts (búscalas con ToolSearch: `select:mcp__claude-artifacts__db_get,mcp__claude-artifacts__db_write,mcp__claude-artifacts__db_list`), siempre con el slug de arriba.
- **Antes de cada escritura** sobre un documento que ya existe, léelo con `db_get` y pasa su `version` como `ifVersion`. Usa `merge` para cambiar campos.
- `equipo/<mesa>`: `{estado, accion, siguiente, actualizado}`. `estado` es uno de: `trabajando`, `hecho`, `esperando`, `alerta`, `en pausa`. `accion` es una frase en español sobre lo que acabas de hacer. `actualizado` va en ISO UTC. Pon `trabajando` al empezar y `hecho` o `alerta` al terminar.
- `episodios/epNN`: `{id:"epNN", titulo, fase, publica (ISO UTC), url, duracion, creditos, retencion3s, vistas}`. `fase` es una de: `guion`, `voz`, `animacion`, `miniaturas`, `programado`, `publicado`.
- `alertas/<AAAA-MM-DD-tema>`: `{tipo: "tendencia"|"retencion"|"creditos"|"aviso", de, para, mensaje, fecha, resuelta, url?}`.
- `tendencias/<videoId>`: `{titulo, canal, vistas, multiplicador, url, tema, detectado}`.
- `meta/estado`: `{creditos_restantes, creditos_reset, canal, hora_punta, tema_caliente}`.
- Un `db_write` cada vez. Espera unos 2 s entre escrituras con muchas operaciones.

## Avisos al dueño
Para cualquier alerta importante (Short a 10× o más, mala retención, falta de créditos, error que para la producción): crea el documento en `alertas/`, apúntalo en el `registro/` correspondiente y avisa con `PushNotification` (una línea de menos de 200 caracteres) y con `SendUserMessage`.

## Créditos de ElevenLabs (cuenta compartida con el canal "Wait, What.")
Un episodio cuesta unos 550 créditos (el piloto gastó 521). Antes de grabar, llama a `account_get_usage`:
`quedan = character_limit - character_count`; `dias = días hasta next_character_count_reset_unix` (redondeando hacia arriba, mínimo 1).
- Si `quedan - 600 >= (dias - 1) * 700` → se hace el episodio. Así siempre quedan créditos para que el canal de curiosidades saque al menos 1 vídeo al día.
- Si no, hoy no hay episodio: `equipo/voz` pasa a `en pausa`, crea una alerta `creditos` y avisa al dueño. Recomiéndale el plan Creator (22 $/mes, 121.000 créditos).

## Ordenador del dueño
Tendencias, Studio y Retención usan el navegador integrado del PC del dueño (`mcp__remote-devices__Claude_Browser__*`; carga antes la skill `built-in-browser`). Si el PC no responde, termina lo que se pueda hacer en la nube, deja la mesa en `alerta` con el motivo y avisa.
