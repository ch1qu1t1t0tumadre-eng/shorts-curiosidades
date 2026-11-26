"""Quita un trozo de la voz ya acelerada (sin gastar créditos) y desplaza words.json.

Uso:  python3 pipeline/recortar.py work/vNN T0 T1
  - T0, T1 en el tiempo ACTUAL de voz.mp3/words.json (segundos). Se borra [T0, T1).
  - Guarda copia de seguridad la primera vez (voz_precorte.mp3, words_precorte.json).
  - Después añade en escenas.py  CORTES = [(T0, T1)]  (en el tiempo ORIGINAL de las escenas):
    anim.py traduce el tiempo y no hace falta reescribir las escenas ni los SFX.
Úsalo para quitar relleno entre el gancho y el primer giro (segundos 3-9, donde más gente se va).
"""
import json
import os
import shutil
import subprocess
import sys

d, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
voz, wj = os.path.join(d, "voz.mp3"), os.path.join(d, "words.json")
if not os.path.exists(os.path.join(d, "voz_precorte.mp3")):
    shutil.copy(voz, os.path.join(d, "voz_precorte.mp3"))
    shutil.copy(wj, os.path.join(d, "words_precorte.json"))
tmp = os.path.join(d, "voz_tmp.mp3")
f = 0.012  # micro-fundido para que no haga clic
subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", voz, "-filter_complex",
                       f"[0:a]atrim=0:{t0},asetpts=N/SR/TB,afade=t=out:st={max(t0 - f, 0)}:d={f}[a];"
                       f"[0:a]atrim=start={t1},asetpts=N/SR/TB,afade=t=in:st=0:d={f}[b];[a][b]concat=n=2:v=0:a=1[o]",
                       "-map", "[o]", "-c:a", "libmp3lame", "-q:a", "2", tmp])
os.replace(tmp, voz)
data = json.load(open(wj))
L = t1 - t0
out = []
for w in data["words"]:
    if w["start"] >= t1:
        w = dict(w, start=round(w["start"] - L, 3), end=round(w["end"] - L, 3))
    elif w["end"] > t0:
        continue
    out.append(w)
data["words"] = out
json.dump(data, open(wj, "w"), ensure_ascii=False)
print(f"recortado {L:.2f}s de {d}; añade en escenas.py: CORTES = [({t0}, {t1})] (si no había cortes antes)")
