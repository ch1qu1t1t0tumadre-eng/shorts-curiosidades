"""Voces propias de AnimalCity TV (sin ElevenLabs, sin créditos, sin conexión).

Motor: Kokoro-82M (Apache 2.0, uso comercial permitido) en ONNX, que corre aquí mismo, más un procesado WORLD
(pyworld) que da a cada personaje su voz fija: tono, formantes (tamaño de la "cabeza"), entonación, temblor...
La voz de cada personaje está GUARDADA en VOCES (mezcla de voces base + ajustes) y es la misma en todos los vídeos.

    python3 voces.py work/epNN            # genera audio/NN.wav de cada línea de lineas.json y monta el diálogo
    python3 voces.py work/epNN 6 11 13    # sólo esas líneas
    python3 voces.py casting salida.wav   # muestra de las 4 voces

Emociones con etiquetas en el texto, como antes: [panicked] [shouting] [whispers] [mumbles] [flatly] [smug]
[reading slowly] [delighted] [excited] [sad] [nervous]. Un texto en MAYÚSCULAS se grita. Varias etiquetas en una
línea = varios trozos con su emoción. Si el texto escrito no se lee bien en voz alta (una contraseña pegada), pon
"voz": "texto para decir" en la línea. Las palabras PegadasAsí se separan solas al hablar.
"""
import json, math, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "modelos")
SR = 24000

# ---------------------------------------------------------------- las voces del reparto (no cambiar: son "su" voz)
VOCES = {
    "teddy": {"mezcla": [("am_puck", 0.65), ("am_liam", 0.35)], "velocidad": 1.08, "semitonos": 8.0, "formante": 1.12,
              "expresion": 1.35, "temblor": 0.0},
    "moe": {"mezcla": [("am_echo", 0.55), ("am_michael", 0.45)], "velocidad": 1.02, "semitonos": 5.5, "formante": 1.12,
            "expresion": 1.1, "temblor": 0.012},
    "nana": {"mezcla": [("af_sarah", 0.6), ("bf_emma", 0.4)], "velocidad": 0.9, "semitonos": -5.0, "formante": 0.95,
             "expresion": 0.85, "temblor": 0.025},
    "mia": {"mezcla": [("af_heart", 0.6), ("af_bella", 0.4)], "velocidad": 1.05, "semitonos": 3.5, "formante": 1.05,
            "expresion": 1.2, "temblor": 0.0},
}

EMOCIONES = {
    "panicked": {"velocidad": 1.14, "semitonos": 1.5, "expresion": 1.35, "gan": 2},
    "nervous": {"velocidad": 1.08, "semitonos": 1.0, "expresion": 1.2, "temblor": 0.02},
    "shouting": {"velocidad": 1.06, "semitonos": 3.0, "expresion": 1.45, "gan": 5, "grito": True},
    "whispers": {"velocidad": 1.0, "susurro": True, "gan": -9},
    "mumbles": {"velocidad": 1.25, "susurro": True, "gan": -11, "apagada": True},
    "flatly": {"velocidad": 0.94, "expresion": 0.45, "semitonos": -0.5},
    "smug": {"velocidad": 0.9, "expresion": 0.8},
    "reading slowly": {"velocidad": 0.78, "expresion": 0.9},
    "delighted": {"velocidad": 1.04, "semitonos": 1.5, "expresion": 1.45, "gan": 1},
    "excited": {"velocidad": 1.1, "semitonos": 2.0, "expresion": 1.5, "gan": 2},
    "sad": {"velocidad": 0.86, "semitonos": -1.0, "expresion": 0.7, "gan": -2},
}

_K = None


def _kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(os.path.join(MOD, "kokoro-v1.0.onnx"), os.path.join(MOD, "voices-v1.0.bin"))
    return _K


def _estilo(pj):
    k = _kokoro()
    st = None
    for nombre, peso in VOCES[pj]["mezcla"]:
        v = k.get_voice_style(nombre) * peso
        st = v if st is None else st + v
    return st


def _para_decir(t):
    t = re.sub(r"\*[^*]*\*", "", t)
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)  # PegadasAsí -> Pegadas Así
    t = t.replace("Wi-Fi", "Wi-Fi")
    return re.sub(r"\s+", " ", t).strip()


def _trozos(texto):
    """'[a] uno [b] dos' -> [('a', 'uno'), ('b', 'dos')]"""
    partes = re.split(r"\[([^\]]+)\]", texto)
    out = []
    emo = None
    if partes[0].strip():
        out.append((None, partes[0].strip()))
    for i in range(1, len(partes), 2):
        emo = partes[i].strip().lower()
        txt = partes[i + 1].strip() if i + 1 < len(partes) else ""
        if txt:
            out.append((emo, txt))
    return out


def _world(y, cfg):
    import pyworld as pw
    x = y.astype(np.float64)
    f0, sp, ap = pw.wav2world(x, SR, frame_period=5.0)
    v = f0 > 0
    if v.any():
        lf = np.log(f0[v])
        m = lf.mean()
        lf = m + (lf - m) * cfg["expresion"] + cfg["semitonos"] * math.log(2) / 12
        f0[v] = np.exp(lf)
        if cfg.get("temblor"):
            t = np.arange(len(f0)) * 0.005
            f0[v] *= 1 + cfg["temblor"] * np.sin(2 * np.pi * 5.6 * t[v])
    a = cfg["formante"]
    if abs(a - 1) > 1e-3:  # formantes: >1 voz de "cabeza pequeña", <1 más grande/mayor
        n = sp.shape[1]
        src = np.clip(np.arange(n) / a, 0, n - 1)
        lo = np.floor(src).astype(int)
        hi = np.minimum(lo + 1, n - 1)
        fr = src - lo
        sp = sp[:, lo] * (1 - fr) + sp[:, hi] * fr
    if cfg.get("susurro"):
        ap = np.ones_like(ap) * 0.98
    out = pw.synthesize(np.ascontiguousarray(f0), np.ascontiguousarray(sp), np.ascontiguousarray(ap), SR, frame_period=5.0)
    return out.astype(np.float32)


def _filtro(y, cfg):
    if cfg.get("apagada"):  # como dicho entre dientes
        k = np.ones(9) / 9
        y = np.convolve(y, k, mode="same")
    if cfg.get("grito"):
        y = np.tanh(y * 2.2) / np.tanh(2.2)
    y = y * (10 ** (cfg.get("gan", 0) / 20))
    return y


def decir(pj, texto):
    """Audio (float32, 24 kHz) de una línea con la voz guardada del personaje."""
    k = _kokoro()
    estilo = _estilo(pj)
    trozos = _trozos(texto) or [(None, texto)]
    piezas = []
    for emo, txt in trozos:
        cfg = dict(VOCES[pj])
        e = dict(EMOCIONES.get(emo, {})) if emo else {}
        decir_txt = _para_decir(txt)
        if decir_txt.isupper() and len(re.sub(r"[^A-Z]", "", decir_txt)) > 2 and not e.get("grito"):
            e = dict(EMOCIONES["shouting"])
        if decir_txt.isupper():
            decir_txt = decir_txt.lower().capitalize()  # el motor lee mejor en minúsculas; la emoción lo grita
        cfg["velocidad"] *= e.pop("velocidad", 1.0)
        for kk in ("semitonos",):
            cfg[kk] += e.pop(kk, 0.0)
        for kk in ("expresion",):
            cfg[kk] *= e.pop(kk, 1.0)
        if "temblor" in e:
            cfg["temblor"] = cfg.get("temblor", 0) + e.pop("temblor")
        cfg.update(e)
        y, sr = k.create(decir_txt, voice=estilo, speed=cfg["velocidad"], lang="en-us")
        y = _world(np.asarray(y, np.float32), cfg)
        y = _filtro(y, cfg)
        piezas.append(y)
        piezas.append(np.zeros(int(SR * 0.12), np.float32))
    y = np.concatenate(piezas[:-1]) if piezas else np.zeros(1, np.float32)
    pk = np.abs(y).max() + 1e-9
    return (y / pk * 0.89).astype(np.float32) if pk > 0.89 else y


def guardar(y, path):
    import soundfile as sf
    sf.write(path, y, SR, subtype="PCM_16")


def episodio(workdir, solo=None):
    p = os.path.join(workdir, "lineas.json")
    L = json.load(open(p))
    os.makedirs(os.path.join(workdir, "audio"), exist_ok=True)
    for i, ln in enumerate(L, 1):
        if solo and i not in solo:
            continue
        rel = f"audio/{i:02d}.wav"
        y = decir(ln["pj"], ln.get("voz") or ln["texto"])
        guardar(y, os.path.join(workdir, rel))
        ln["audio"] = rel
        print(f"{i:02d} {ln['pj']:6s} {len(y) / SR:4.1f}s  {ln.get('voz') or ln['texto']}")
    json.dump(L, open(p, "w"), indent=1, ensure_ascii=False)
    subprocess.run([sys.executable, os.path.join(HERE, "dialogo.py"), workdir], check=True)


def casting(path):
    frases = {"teddy": "[excited] Nana! I need the Wi-Fi password, right now!",
              "moe": "[nervous] Oh no. Oh no, no, no. This is bad.",
              "nana": "[smug] Say please, sweetie.",
              "mia": "Hey! What's your Wi-Fi? [delighted] It works!"}
    ys = []
    for pj, f in frases.items():
        ys += [decir(pj, f), np.zeros(int(SR * 0.6), np.float32)]
    guardar(np.concatenate(ys), path)
    print("ok", path)


if __name__ == "__main__":
    if sys.argv[1] == "casting":
        casting(sys.argv[2])
    else:
        episodio(sys.argv[1], [int(x) for x in sys.argv[2:]] or None)
