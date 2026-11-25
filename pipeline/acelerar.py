#!/usr/bin/env python3
"""Lleva la voz al ritmo de los Shorts virales de curiosidades: SIN PAUSAS y a ~195 palabras/min.

1. Detecta los silencios (> 0,12 s) entre frases y los deja en 0,08 s (la voz "no para nunca").
2. Si aún va lenta, acelera con atempo (máx. x1.20) hasta ~195 palabras/min.
3. Recorta el silencio del principio y del final (el vídeo empieza y acaba hablando: bucle).
4. Reescala words.json para que subtítulos y escenas sigan sincronizados.

Uso: python3 pipeline/acelerar.py work/vNN            -> automático
     python3 pipeline/acelerar.py work/vNN 1.08       -> factor de atempo fijo (tras quitar pausas)
Guarda el original como voz_original.mp3 / words_original.json (si ya existen, parte de ellos).
"""
import json, os, re, shutil, subprocess, sys

PAUSA_MIN, PAUSA_QUEDA, PPM_OBJ = 0.12, 0.08, 215  # formato v3 (25/11/2026): ~215 ppm

d = sys.argv[1]
vo, wo = os.path.join(d, "voz_original.mp3"), os.path.join(d, "words_original.json")
if not os.path.exists(vo):
    shutil.copy(os.path.join(d, "voz.mp3"), vo)
    shutil.copy(os.path.join(d, "words.json"), wo)
data = json.load(open(wo))
ws = [w for w in data["words"] if w.get("type") == "word" and not w["text"].startswith("[")]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vo]))

# --- tramos de audio que se conservan ---
log = subprocess.run(["ffmpeg", "-i", vo, "-af", f"silencedetect=noise=-38dB:d={PAUSA_MIN}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
ini = max(ws[0]["start"] - 0.03, 0)
fin = min(ws[-1]["end"] + 0.06, dur)
keep, cur = [], ini
for s, e in zip(st, en):
    if e <= ini or s >= fin:
        continue
    s, e = max(s, ini), min(e, fin)
    corte_a, corte_b = s + PAUSA_QUEDA / 2, e - PAUSA_QUEDA / 2
    if corte_b > corte_a:
        keep.append((cur, corte_a))
        cur = corte_b
keep.append((cur, fin))


def mapa(t):
    """tiempo original -> tiempo tras quitar pausas"""
    acc = 0.0
    for a, b in keep:
        if t <= a:
            return acc
        if t <= b:
            return acc + t - a
        acc += b - a
    return acc


habla = sum(b - a for a, b in keep)
ppm = len(ws) / habla * 60
f = float(sys.argv[2]) if len(sys.argv) > 2 else min(max(PPM_OBJ / ppm, 1.0), 1.25)
sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vo, "-af",
                f"aselect='{sel}',asetpts=N/SR/TB,atempo={f:.4f}", "-c:a", "libmp3lame", "-q:a", "2",
                os.path.join(d, "voz.mp3")], check=True)
for w in data["words"]:
    for k in ("start", "end"):
        if k in w:
            w[k] = round(mapa(w[k]) / f, 3)
json.dump(data, open(os.path.join(d, "words.json"), "w"))
print(f"{len(ws)} palabras · original {dur:.1f} s · sin pausas {habla:.1f} s ({ppm:.0f} ppm) · "
      f"x{f:.3f} -> {habla / f:.1f} s ({ppm * f:.0f} ppm)")
