"""Voz del narrador del canal de curiosidades ("Wait, What."), propia y sin ElevenLabs.

Motor: Kokoro-82M (Apache 2.0, uso comercial permitido) en ONNX, que corre aquí mismo: sin créditos, sin
conexión y sin límite de vídeos. La voz del canal está GUARDADA en NARRADOR (mezcla fija de voces base): es la
misma en todos los vídeos. Genera lo mismo que antes daba ElevenLabs:

    python3 pipeline/narrador.py work/vNN              # lee work/vNN/texto_voz.txt -> voz.mp3 + words.json
    python3 pipeline/narrador.py work/vNN "texto..."   # o el texto directamente
    python3 pipeline/narrador.py muestra salida.mp3 [voz]   # muestra de la voz (o de una candidata)

words.json tiene el mismo formato que la transcripción de ElevenLabs ({"words": [{text, start, end, type}]}),
así que anim.py (subtítulos e inicio de escenas) funciona igual.
Etiquetas opcionales en el texto: [excited] (un poco más rápido y vivo) y [curious] (más pausado). "..." hace
una pausa más larga antes del dato clave.
"""
import json, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "modelos")
SR = 24000

# La voz del canal (18/11/2026: sustituye a Dean de ElevenLabs; mismo tono grave y cálido). No cambiarla: los espectadores la reconocen.
NARRADOR = {"mezcla": [("am_michael", 0.6), ("am_liam", 0.4)], "velocidad": 1.17}  # la más parecida a la de antes

CANDIDATAS = {
    "A": {"mezcla": [("am_michael", 0.5), ("am_fenrir", 0.3), ("am_puck", 0.2)], "velocidad": 1.1},
    "B": {"mezcla": [("am_michael", 0.6), ("am_liam", 0.4)], "velocidad": 1.1},
    "C": {"mezcla": [("am_fenrir", 0.6), ("am_puck", 0.4)], "velocidad": 1.1},
}
EMO = {"excited": 1.07, "curious": 0.95}

_K = None


def _kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(os.path.join(MOD, "kokoro-v1.0.onnx"), os.path.join(MOD, "voices-v1.0.bin"))
    return _K


def _estilo(voz):
    k = _kokoro()
    st = None
    for nombre, peso in voz["mezcla"]:
        v = k.get_voice_style(nombre) * peso
        st = v if st is None else st + v
    return st


def _frases(texto):
    """Divide en frases conservando la etiqueta activa y la pausa que va detrás."""
    texto = re.sub(r"\s+", " ", texto.strip())
    partes = re.split(r"(\[[a-z ]+\])", texto)
    out, emo = [], None
    for p in partes:
        if not p.strip():
            continue
        m = re.fullmatch(r"\[([a-z ]+)\]", p.strip())
        if m:
            emo = m.group(1)
            continue
        for fr in re.findall(r"[^.!?…]+(?:\.\.\.|…|[.!?]+)?", p):
            fr = fr.strip()
            if fr:
                pausa = 0.5 if fr.endswith(("...", "…")) else (0.28 if fr[-1] in ".!?" else 0.15)
                out.append((emo, fr, pausa))
        emo = None if p.strip()[-1:] in ".!?" else emo
    return out


def _dur_palabra(k, estilo, w, vel):
    w2 = re.sub(r"[^\w'%$-]", "", w)
    if not w2:
        return 0.05
    y, _ = k.create(w2, voice=estilo, speed=vel, lang="en-us", trim=True)
    return max(0.08, len(y) / SR)


def narrar(texto, voz=None):
    """-> (audio float32 24 kHz, lista de palabras con start/end en segundos)."""
    voz = voz or NARRADOR
    k = _kokoro()
    estilo = _estilo(voz)
    audio, palabras, t = [], [], 0.0
    lead = np.zeros(int(SR * 0.15), np.float32)
    audio.append(lead)
    t += len(lead) / SR
    for emo, fr, pausa in _frases(texto):
        vel = voz["velocidad"] * EMO.get(emo, 1.0)
        decir = fr.replace("…", "...")
        y, _ = k.create(decir, voice=estilo, speed=vel, lang="en-us", trim=True)
        y = np.asarray(y, np.float32)
        # palabras repartidas por los tramos con voz, en proporción a lo que dura cada palabra dicha sola
        ws = fr.split()
        pesos = np.array([_dur_palabra(k, estilo, w, vel) for w in ws])
        hop = int(SR * 0.01)
        n = max(1, len(y) // hop)
        rms = np.array([np.sqrt(np.mean(y[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
        voiced = (rms > rms.max() * 0.06).astype(float)
        voiced = np.convolve(voiced, np.ones(5) / 5, mode="same") > 0.2
        cum = np.cumsum(voiced)
        total = max(1, cum[-1])
        lim = np.concatenate([[0], np.cumsum(pesos) / pesos.sum() * total])
        for i, w in enumerate(ws):
            f0 = int(np.searchsorted(cum, lim[i] + 0.5))
            f1 = int(np.searchsorted(cum, lim[i + 1]))
            palabras.append({"text": w, "start": round(t + f0 * 0.01, 3), "end": round(t + max(f1, f0 + 3) * 0.01, 3),
                             "type": "word"})
        audio.append(y)
        t += len(y) / SR
        sil = np.zeros(int(SR * pausa), np.float32)
        audio.append(sil)
        t += len(sil) / SR
    y = np.concatenate(audio)
    pk = np.abs(y).max() + 1e-9
    if pk > 0.95:
        y = y / pk * 0.95
    return y, palabras


def guardar(y, palabras, carpeta):
    import soundfile as sf
    wav = os.path.join(carpeta, "voz.wav")
    sf.write(wav, y, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k",
                    os.path.join(carpeta, "voz.mp3")], check=True)
    os.remove(wav)
    words = []
    for i, w in enumerate(palabras):
        words.append(w)
        if i + 1 < len(palabras):
            words.append({"text": " ", "start": w["end"], "end": palabras[i + 1]["start"], "type": "spacing"})
    json.dump({"text": " ".join(w["text"] for w in palabras), "words": words}, open(os.path.join(carpeta, "words.json"), "w"),
              indent=1, ensure_ascii=False)


if __name__ == "__main__":
    if sys.argv[1] == "muestra":
        destino = sys.argv[2]
        voz = CANDIDATAS.get(sys.argv[3]) if len(sys.argv) > 3 else None
        txt = ("Airline food isn't that bad. At thirty-five thousand feet, you taste like you have a cold. "
               "[curious] But here's the crazy part... the engine noise. It mutes sweetness even more. "
               "Follow for more hidden reasons behind everyday things.")
        y, _ = narrar(txt, voz)
        import soundfile as sf
        sf.write("/tmp/_m.wav", y, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/_m.wav", "-c:a", "libmp3lame", "-b:a", "192k", destino],
                       check=True)
        print("ok", destino, f"{len(y) / SR:.1f}s")
    else:
        carpeta = sys.argv[1]
        texto = sys.argv[2] if len(sys.argv) > 2 else open(os.path.join(carpeta, "texto_voz.txt")).read()
        y, pal = narrar(texto)
        guardar(y, pal, carpeta)
        print(f"ok voz.mp3 {len(y) / SR:.1f}s · {len(pal)} palabras · words.json")
