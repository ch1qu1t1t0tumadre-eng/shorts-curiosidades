# Mesa de Voz y audio · Polly la Lora

1. Comprueba los créditos con la regla de `oficina/OFICINA.md`. Si no llegan, para la producción de hoy y avisa.
2. `creative_create_flow` (nombre `AnimalCity epNN`). Por cada línea de `work/epNN/lineas.json`, llama a `creative_generate_speech` con ese `flow_id`, `model_id: eleven_v4`, `generations_count: 1` y la voz del personaje según `BIBLIA.md`:
   Teddy `WAYsiv3Yudejrr5Di4lf` · Moe `mrQhZWGbb2k9qWJb5qeA` · Nana `vFLqXa8bgbofGarf6fZh` · Mia `Lb0YjiVdotJrGAKbDrUs`.
   Puedes lanzar todas las líneas en paralelo. **Nunca repitas una llamada para "reintentar"**: cada llamada cobra.
3. Espera unos 20 s y llama a `creative_get_flow_run_status` con todos los `session_ids` hasta que `all_completed` sea true. Descarga cada `content_url` con curl a `work/epNN/audio/NN.mp3` (`elevenlabsusercontent.com` está permitido), en el orden de `lineas.json`.
4. `python3 pipeline/dialogo.py work/epNN` → `dialogo.wav` + `timeline.json`. Comprueba la lista de tiempos que imprime: total entre 15 y 32 s, sin huecos de más de 1,2 s salvo los que pida el guion.
5. Control de calidad de cada línea (gratis): `creative_transcribe_audio` con `eleven_scribe_v1`, el mismo `flow_id` y `connect_from` = node_id de la línea, solo en las líneas con etiquetas o palabras raras. Si una etiqueta se lee en voz alta o falta una palabra, regenera **solo esa línea, una vez**, y vuelve a montar.
6. Panel: `episodios/epNN.fase = "voz"` y `creditos` (suma de los `credit_costs`). `equipo/voz` → `hecho` con la duración y los créditos.
