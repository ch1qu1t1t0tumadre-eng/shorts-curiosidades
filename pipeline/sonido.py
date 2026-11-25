#!/usr/bin/env python3
"""Efectos de sonido y música de fondo generados por síntesis (sin derechos de autor de terceros).

- whoosh: barrido de ruido filtrado (cambios de escena)
- pop:    "plop" corto (aparece una etiqueta o un objeto)
- ding:   campanita (dato importante)
- tick:   clic de contador
- rise:   subida tensa (antes del dato sorprendente)
- musica: base ambiental suave con pulso ligero, en bucle, tonalidad aleatoria por vídeo
"""
import numpy as np
import wave

SR = 44100


def _env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


def whoosh(d=0.45, seed=0):
    n = int(SR * d)
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    # filtro pasa-banda que barre de grave a agudo (aprox. con media móvil de ancho variable)
    out = np.zeros(n)
    cs = np.cumsum(np.insert(x, 0, 0))
    for i in range(n):
        w = int(40 - 34 * (i / n))
        j0 = max(0, i - w)
        out[i] = (cs[i + 1] - cs[j0]) / (i + 1 - j0)
    t = np.linspace(0, 1, n)
    env = np.sin(np.pi * t) ** 1.5
    out = out * env
    return 0.9 * out / (np.abs(out).max() + 1e-9)


def pop(f0=420):
    n = int(SR * 0.12)
    t = np.arange(n) / SR
    f = f0 * (1 + 1.6 * np.exp(-t * 60))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return 0.5 * np.sin(ph) * _env(n, 0.004, 0.03)


def ding(f0=1320):
    n = int(SR * 0.9)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 2.01 * t) + 0.25 * np.sin(2 * np.pi * f0 * 3.02 * t)
    return 0.45 * s * _env(n, 0.002, 0.25)


def tick():
    n = int(SR * 0.03)
    rng = np.random.default_rng(1)
    return 0.5 * rng.standard_normal(n) * _env(n, 0.0005, 0.006)


def rise(d=1.0):
    n = int(SR * d)
    t = np.arange(n) / SR
    f = 180 * (2 ** (2.0 * t / d))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.3 + np.sin(ph * 2) * 0.3
    return 0.35 * s * (t / d) ** 2


def thud(f0=70):
    """Golpe grave (algo pesado cae o se hunde)."""
    n = int(SR * 0.5)
    t = np.arange(n) / SR
    f = f0 * (1 + 1.5 * np.exp(-t * 25))
    ph = 2 * np.pi * np.cumsum(f) / SR
    rng = np.random.default_rng(3)
    return 0.8 * np.sin(ph) * _env(n, 0.002, 0.12) + 0.15 * rng.standard_normal(n) * _env(n, 0.001, 0.02)


def crack():
    """Crujido (piedra o madera que cede)."""
    n = int(SR * 0.35)
    rng = np.random.default_rng(5)
    x = rng.standard_normal(n)
    clicks = (rng.random(n) < 0.004) * rng.standard_normal(n) * 6
    return 0.35 * (x * _env(n, 0.001, 0.05) + np.convolve(clicks, np.ones(20) / 20, mode="same"))


def bell(f0=440):
    """Campana de torre (grave, larga)."""
    n = int(SR * 1.6)
    t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f0 * m * t) for a, m in ((1, 1), (0.6, 2.0), (0.4, 2.4), (0.25, 3.0), (0.15, 4.2)))
    return 0.35 * s * _env(n, 0.003, 0.6)


def squish():
    """Esponja que se aprieta (agua)."""
    n = int(SR * 0.45)
    rng = np.random.default_rng(9)
    x = np.convolve(rng.standard_normal(n), np.ones(30) / 30, mode="same")
    t = np.linspace(0, 1, n)
    return 2.2 * x * np.sin(np.pi * t) ** 2


def drum():
    """Tambor de guerra."""
    n = int(SR * 0.4)
    t = np.arange(n) / SR
    rng = np.random.default_rng(2)
    return 0.7 * np.sin(2 * np.pi * 95 * t) * _env(n, 0.002, 0.09) + 0.25 * rng.standard_normal(n) * _env(n, 0.001, 0.03)


SFX = {"whoosh": whoosh, "pop": pop, "ding": ding, "tick": tick, "rise": rise,
       "thud": thud, "crack": crack, "bell": bell, "squish": squish, "drum": drum}


def musica(d, seed=0, bpm=70):
    """Base suave: acordes de pad + bajo + pulso de hi-hat. Tonalidad y progresión según seed."""
    rng = np.random.default_rng(seed)
    n = int(SR * d)
    t = np.arange(n) / SR
    root = 110 * 2 ** (rng.integers(0, 12) / 12)
    progs = [[0, 5, 3, 4], [0, 3, 5, 4], [0, 4, 5, 3], [5, 3, 0, 4]]
    prog = progs[rng.integers(0, len(progs))]
    scale = [0, 2, 4, 5, 7, 9, 11]  # mayor: ambiente agradable y relajado
    beat = 60 / bpm
    bar = beat * 4
    out = np.zeros(n)
    for k in range(int(d / bar) + 1):
        deg = prog[k % 4]
        t0 = k * bar
        i0, i1 = int(t0 * SR), min(n, int((t0 + bar) * SR))
        if i0 >= n:
            break
        tt = t[i0:i1] - t0
        env = np.minimum(1, tt / 1.2) * np.minimum(1, (bar - tt) / 1.2) * 0.85 + 0.15
        for step in (0, 2, 4):
            semi = scale[(deg + step) % 7] + 12 * ((deg + step) // 7)
            f = root * 2 * 2 ** (semi / 12)
            out[i0:i1] += 0.10 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * f * 2 * tt + 0.3))
        fb = root * 2 ** (scale[deg % 7] / 12) / 2
        for b in range(4):
            bi0 = int((t0 + b * beat) * SR)
            bi1 = min(n, bi0 + int(SR * beat * 0.9))
            if bi0 >= n:
                break
            tb = t[bi0:bi1] - (t0 + b * beat)
            out[bi0:bi1] += (0.08 if b == 0 else 0.0) * np.sin(2 * np.pi * fb * tb) * np.exp(-tb * 1.2)
    # suavizado (pasa-bajos sencillo) para que quede cálida y de fondo
    for _ in range(3):
        out = np.convolve(out, np.ones(9) / 9, mode="same")
    out *= np.minimum(1, t / 1.5) * np.minimum(1, (d - t) / 1.5)
    return 0.6 * out / (np.abs(out).max() + 1e-9)


def mezcla(d, eventos, path, seed=0, fx_gain=0.14, mus_gain=0.22):
    """Pista de efectos + música (sin voz). eventos = [(t, nombre), ...]."""
    n = int(SR * d)
    fx = np.zeros(n)
    for k, (t, name) in enumerate(eventos):
        s = SFX[name]() if name != "whoosh" else 0.4 * whoosh(seed=k)
        i = int(t * SR)
        if i >= n:
            continue
        m = min(len(s), n - i)
        fx[i:i + m] += s[:m]
    mus = musica(d, seed)
    out = fx_gain * fx + mus_gain * mus  # por defecto: música de ambiente y efectos discretos
    out = np.clip(out, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
