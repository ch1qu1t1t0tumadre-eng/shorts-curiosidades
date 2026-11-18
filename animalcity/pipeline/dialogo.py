#!/usr/bin/env python3
"""Monta la pista de diálogo de un episodio.

Entrada: work/epNN/lineas.json
  [{"pj": "teddy", "texto": "Nana. Wi-Fi password. Now.", "audio": "audio/01.mp3",
    "pausa": 0.15,            # silencio ANTES de la línea (s). Negativo = se pisa con la anterior
    "rotulo": true,           # opcional: mostrar rótulo (false para gritos que ya van como texto de impacto)
    "rotulo_texto": "..."}]   # opcional: texto del rótulo si debe ser distinto del audio (sin etiquetas [..])
Salida: work/epNN/dialogo.wav y work/epNN/timeline.json
  {"dur": s, "env_fps": 60, "lineas": [{"pj","texto","ini","fin","env":[0..1 por fotograma]}, ...]}
Uso: python3 dialogo.py work/epNN
"""
import json, os, re, subprocess, sys, wave
import numpy as np

SR = 44100
FPS = 60


def decode(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768


def trim(x, thr=0.02, pad=0.03):
    idx = np.where(np.abs(x) > thr)[0]
    if not len(idx):
        return x
    a = max(0, idx[0] - int(pad * SR))
    b = min(len(x), idx[-1] + int(pad * SR))
    return x[a:b]


def envelope(x):
    hop = SR // FPS
    n = max(1, len(x) // hop)
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    if rms.max() > 0:
        rms = rms / np.percentile(rms, 95)
    rms = np.clip(rms, 0, 1)
    # suaviza un poco y quita el "temblor": la boca se abre en sílabas, no en cada muestra
    rms = np.convolve(rms, np.ones(3) / 3, mode="same")
    return [round(float(v), 3) for v in rms]


def main(workdir):
    lineas = json.load(open(os.path.join(workdir, "lineas.json")))
    pista = np.zeros(int(SR * 0.25), dtype=np.float32)  # 0,25 s de aire al principio, no más
    t = len(pista) / SR
    out = []
    for k, ln in enumerate(lineas):
        x = trim(decode(os.path.join(workdir, ln["audio"])))
        pausa = float(ln.get("pausa", 0.12 if k else 0.0))
        ini = max(0.0, t + pausa)
        i0 = int(ini * SR)
        need = i0 + len(x)
        if need > len(pista):
            pista = np.concatenate([pista, np.zeros(need - len(pista), dtype=np.float32)])
        pista[i0:i0 + len(x)] += x
        fin = ini + len(x) / SR
        item = {"pj": ln["pj"], "texto": re.sub(r"\[[^\]]*\]\s*", "", ln.get("rotulo_texto") or ln["texto"]).strip(),
                "ini": round(ini, 3), "fin": round(fin, 3), "env": envelope(x)}
        if ln.get("rotulo") is False:
            item["rotulo"] = False
        out.append(item)
        t = fin
    pista = np.clip(pista, -1, 1)
    with wave.open(os.path.join(workdir, "dialogo.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pista * 32767).astype(np.int16).tobytes())
    tl = {"dur": round(len(pista) / SR, 3), "env_fps": FPS, "lineas": out}
    json.dump(tl, open(os.path.join(workdir, "timeline.json"), "w"))
    for ln in out:
        print(f'{ln["ini"]:6.2f}-{ln["fin"]:6.2f}  {ln["pj"]:6s} {ln["texto"]}')
    print(f"duración total: {tl['dur']:.1f} s")


if __name__ == "__main__":
    main(sys.argv[1])
