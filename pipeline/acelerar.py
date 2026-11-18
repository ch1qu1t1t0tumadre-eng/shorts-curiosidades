#!/usr/bin/env python3
"""Acelera la voz al ritmo de los Shorts virales de curiosidades (~190-200 palabras/min)
y reescala los tiempos de words.json para que subtítulos y escenas sigan sincronizados.

Uso: python3 pipeline/acelerar.py work/vNN            -> calcula el factor solo (objetivo 195 ppm, máx. 1.20)
     python3 pipeline/acelerar.py work/vNN 1.12       -> factor fijo
Guarda el original como voz_original.mp3 / words_original.json (si ya existen, parte de ellos).
"""
import json, os, shutil, subprocess, sys

d = sys.argv[1]
vo, wo = os.path.join(d, "voz_original.mp3"), os.path.join(d, "words_original.json")
if not os.path.exists(vo):
    shutil.copy(os.path.join(d, "voz.mp3"), vo)
    shutil.copy(os.path.join(d, "words.json"), wo)
data = json.load(open(wo))
ws = [w for w in data["words"] if w.get("type") == "word" and not w["text"].startswith("[")]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vo]))
habla = ws[-1]["end"] - ws[0]["start"]
ppm = len(ws) / habla * 60
if len(sys.argv) > 2:
    f = float(sys.argv[2])
else:
    f = min(max(195 / ppm, 1.0), 1.20)
# recorta el silencio inicial y final (el vídeo debe empezar y acabar hablando, para el bucle)
ini = max(ws[0]["start"] - 0.05, 0)
fin = ws[-1]["end"] + 0.05
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vo, "-af",
                f"atrim={ini:.3f}:{fin:.3f},asetpts=PTS-STARTPTS,atempo={f:.4f}", "-c:a", "libmp3lame", "-q:a", "2",
                os.path.join(d, "voz.mp3")], check=True)
for w in data["words"]:
    for k in ("start", "end"):
        if k in w:
            w[k] = round(max(w[k] - ini, 0) / f, 3)
json.dump(data, open(os.path.join(d, "words.json"), "w"))
print(f"{len(ws)} palabras · {ppm:.0f} ppm -> {ppm * f:.0f} ppm (x{f:.3f}) · {(fin - ini) / f:.1f} s")
