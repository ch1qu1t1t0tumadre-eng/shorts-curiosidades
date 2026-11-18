#!/usr/bin/env python3
"""Motor de la sitcom animada de AnimalCity TV (vectorial, cairo).

Reutiliza las primitivas de ../../pipeline/anim.py y añade:
  - los 4 personajes (teddy, moe, nana, mia) con estados de ánimo y boca sincronizada con el audio
  - decorados (salon, puerta, cocina, rafaga) con variantes para no repetir planos
  - rótulos de diálogo del color de cada personaje y textos de impacto
  - render: escenas.py + timeline.json (de dialogo.py) -> short.mp4

Cada episodio tiene work/epNN/escenas.py:
    from sitcom import *
    def e1(ctx, lt, dur, T, L): ...      # L = ayudante del diálogo (L.talk("nana", T) -> 0..1)
    ESCENAS = [(0.0, e1), (2.4, e2), ...]
    SFX = [(4.1, "doorbell"), ...]        # opcional
Uso:
    python3 sitcom.py work/epNN               -> short.mp4 (1440x2560, 60 fps)
    python3 sitcom.py work/epNN preview 0.5 3 7.2   -> prev_T.png para revisar
"""
import importlib.util, json, math, os, re, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
from anim import *  # noqa: F401,F403  (W, H, FPS, OUT_W, OUT_H, SCALE, primitivas, cairo...)
import anim as _anim
import cairocffi as cairo
sys.path.insert(0, HERE)
from efectos import *  # noqa: F401,F403  (movimiento cartoon, partículas, ambientes)
from escenarios import *  # noqa: F401,F403  (decorados con ambiente)

FONT_IMPACT = "Anton"
INK = (0.08, 0.07, 0.12)

# ---------------------------------------------------------------- paleta de personajes
PJ = {
    "teddy": {"nombre": "TEDDY", "color": hexc("#F08A3C"), "oscuro": hexc("#B9561A")},
    "moe":   {"nombre": "MOE",   "color": hexc("#5B8FE0"), "oscuro": hexc("#2A4C8F")},
    "nana":  {"nombre": "NANA",  "color": hexc("#B07CE8"), "oscuro": hexc("#6A3590")},
    "mia":   {"nombre": "MIA",   "color": hexc("#6CC26A"), "oscuro": hexc("#3A6E37")},
}


def _register_fonts():
    try:
        fp = os.path.join(HERE, "..", "..", "pipeline", "assets", "Anton.ttf")
        if os.path.exists(fp):
            subprocess.run(["fc-cache", "-f"], capture_output=True)
    except Exception:
        pass


# ---------------------------------------------------------------- piezas comunes de cara
def _eyes(ctx, ex, ey, r, mood, T, look=(0, 0), lid_rgb=(0.2, 0.2, 0.2), seed=0):
    """Dos ojos centrados en (±ex, ey). mood cambia párpados y pupilas."""
    ph = (T + seed * 0.37) % 3.9
    blink = 0.0 if ph < 0.1 else 1.0
    if mood == "dormido":
        blink = 0.0
    big = {"sorpresa": 1.25, "panico": 1.3}.get(mood, 1.0)
    pup = {"panico": 0.45, "sorpresa": 0.8}.get(mood, 1.0)
    for sx in (-1, 1):
        x = sx * ex
        if blink == 0.0:
            ctx.move_to(x - r, ey)
            ctx.curve_to(x - r * 0.4, ey + r * 0.5, x + r * 0.4, ey + r * 0.5, x + r, ey)
            stroke(ctx, INK, r * 0.28)
            continue
        ellipse(ctx, x, ey, r * big, r * 1.12 * big)
        fill_keep(ctx, WHITE)
        stroke(ctx, INK, 5)
        px, py = x + look[0] * r * 0.35, ey + look[1] * r * 0.35
        circle(ctx, px, py, r * 0.52 * pup)
        fill(ctx, INK)
        circle(ctx, px + r * 0.18, py - r * 0.2, r * 0.16)
        fill(ctx, WHITE)
        # párpado
        lid = {"sospecha": 0.5, "smug": 0.45, "cansado": 0.55, "enfado": 0.35}.get(mood, 0.0)
        if lid:
            ctx.save()
            ellipse(ctx, x, ey, r * big + 2, r * 1.12 * big + 2)
            ctx.clip()
            ctx.rectangle(x - r * 2, ey - r * 2.2, r * 4, r * 2.2 * lid * 1.9)
            fill(ctx, lid_rgb)
            ctx.restore()
        # ceja
        by = ey - r * 1.45
        tilt = {"enfado": 0.35 * sx, "sospecha": -0.15 * sx, "panico": -0.3 * sx, "triste": -0.3 * sx}.get(mood, 0.0)
        if mood in ("sorpresa", "panico"):
            by -= r * 0.35
        ctx.save()
        ctx.translate(x, by)
        ctx.rotate(tilt)
        rrect(ctx, -r * 0.8, -r * 0.14, r * 1.6, r * 0.28, r * 0.14)
        fill(ctx, INK)
        ctx.restore()


def _mouth(ctx, mx, my, w, talk, mood):
    """Boca: talk 0..1 abre la boca (sincronía con la voz)."""
    o = clamp(talk)
    if mood in ("sorpresa", "panico") and o < 0.3:
        o = 0.55
    if o > 0.08:
        h = w * (0.15 + 0.7 * o)
        ctx.move_to(mx - w / 2, my)
        ctx.curve_to(mx - w / 2, my + h * 1.3, mx + w / 2, my + h * 1.3, mx + w / 2, my)
        ctx.curve_to(mx + w / 4, my - h * 0.15, mx - w / 4, my - h * 0.15, mx - w / 2, my)
        fill_keep(ctx, (0.35, 0.08, 0.12))
        stroke(ctx, INK, 5)
        ellipse(ctx, mx, my + h * 0.85, w * 0.22, h * 0.28)
        fill(ctx, (0.95, 0.45, 0.5))
        return
    if mood in ("feliz", "smug"):
        ctx.move_to(mx - w / 2, my - (6 if mood == "smug" else 0))
        ctx.curve_to(mx - w / 4, my + w * 0.35, mx + w / 4, my + w * 0.35, mx + w / 2, my - (14 if mood == "smug" else 0))
    elif mood in ("enfado", "triste", "cansado"):
        ctx.move_to(mx - w / 2, my + w * 0.12)
        ctx.curve_to(mx - w / 4, my - w * 0.12, mx + w / 4, my - w * 0.12, mx + w / 2, my + w * 0.12)
    elif mood == "sospecha":
        ctx.move_to(mx - w / 2, my + 4)
        ctx.line_to(mx + w / 2, my - 4)
    else:
        ctx.move_to(mx - w / 2, my)
        ctx.curve_to(mx - w / 4, my + w * 0.15, mx + w / 4, my + w * 0.15, mx + w / 2, my)
    stroke(ctx, INK, 8)


def _sweat(ctx, x, y, T):
    k = (T * 1.5) % 1.0
    ctx.save()
    ctx.translate(x, y + k * 40)
    ctx.move_to(0, -26)
    ctx.curve_to(18, 0, 14, 18, 0, 18)
    ctx.curve_to(-14, 18, -18, 0, 0, -26)
    fill_keep(ctx, (0.6, 0.85, 1.0), 1 - k)
    stroke(ctx, INK, 3, 1 - k)
    ctx.restore()


def _arm(ctx, x0, y0, ang, length, rgb, hand_rgb, w=34):
    ctx.save()
    ctx.translate(x0, y0)
    ctx.rotate(ang)
    rrect(ctx, -w / 2, 0, w, length, w / 2)
    fill_keep(ctx, rgb)
    stroke(ctx, INK, 5)
    circle(ctx, 0, length, w * 0.72)
    fill_keep(ctx, hand_rgb)
    stroke(ctx, INK, 5)
    ctx.restore()


def phone(ctx, x, y, s=1.0, rot=0.0, glow=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -38, -70, 76, 140, 14)
    fill_keep(ctx, (0.12, 0.12, 0.16))
    stroke(ctx, INK, 5)
    rrect(ctx, -30, -60, 60, 118, 8)
    fill(ctx, (0.55 + 0.4 * glow, 0.8, 1.0))
    ctx.restore()


def tablet(ctx, x, y, s=1.0, rot=0.0, screen_text=None):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -110, -80, 220, 160, 18)
    fill_keep(ctx, (0.15, 0.14, 0.2))
    stroke(ctx, INK, 6)
    rrect(ctx, -96, -66, 192, 132, 10)
    fill(ctx, (0.62, 0.86, 1.0))
    if screen_text:
        sz = 30
        while sz > 12 and text_width(ctx, screen_text, sz) > 176:
            sz -= 1
        text(ctx, screen_text, 0, 0, sz, INK, shadow=False)
    ctx.restore()


# ---------------------------------------------------------------- personajes (muñecos articulados)
# Los personajes son los DIBUJOS OFICIALES del reparto (variante 2, referencias/reparto_v2.png), recortados en
# assets/personajes/*.png. No se redibujan: pipeline/rig.py los separa en piezas con esqueleto (hombros, codos,
# muñecas, caderas, rodillas, cuello, mandíbula, cola, orejas, coleta) y aquí se animan con movimiento natural:
# respiración, balanceo del peso, la cabeza sigue al cuerpo con un poco de retraso, la cola y las orejas tienen
# inercia, los brazos gesticulan al ritmo de la voz y la boca cambia de forma según la vocal.
import rig as _rig
import skia as _skia

_PUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "personajes")
_PUP_WORLD = 0.29  # unidades del lienzo (1080x1920) por píxel del recorte (x4)
PUP = {
    "teddy": {"eyes": [(836, 340, 78), (1012, 300, 78)], "mouth": None, "hand": ("mano_d", (1704, 900)),
              "head": (930, 330), "cheeks": [(790, 470), (1100, 430)]},
    "moe": {"eyes": [(496, 476, 60), (708, 476, 60)], "mouth": (612, 632, 250), "hand": ("brazos", (612, 900)),
            "head": (600, 470), "cheeks": [(450, 590), (760, 590)]},
    "nana": {"eyes": [(228, 508, 46), (484, 516, 46)], "mouth": (412, 676, 120), "hand": ("antebrazo_i", (130, 990)),
             "screen": (128, 990, -0.38), "head": (360, 520), "cheeks": [(250, 610), (500, 620)]},
    "mia": {"eyes": [(192, 708, 52), (440, 716, 52)], "mouth": (380, 824, 190), "hand": ("brazos", (560, 1380)),
            "head": (330, 700), "cheeks": [(200, 810), (470, 820)]},
}
_pup_cache = {}
_skimg = {}


def _pup(name):
    if name not in _pup_cache:
        surf = cairo.ImageSurface.create_from_png(os.path.join(_PUP_DIR, f"{name}.png"))
        w, h = surf.get_width(), surf.get_height()
        data = np.frombuffer(surf.get_data(), np.uint8).reshape(h, surf.get_stride() // 4, 4)[:, :w]
        alpha = data[..., 3]
        rows = np.where(alpha.max(1) > 200)[0]
        bottom, top = rows[-1], rows[0]
        cols = np.where(alpha[max(0, bottom - 120):bottom + 1].max(0) > 200)[0]
        foot_x = (cols[0] + cols[-1]) / 2
        tcols = np.where(alpha[top:top + 60].max(0) > 200)[0]
        meta = dict(PUP[name])
        meta["top"] = ((tcols[0] + tcols[-1]) / 2, top)

        def sample(px, py):
            b, g, r, a = data[int(py), int(px)]
            return (r / 255, g / 255, b / 255)
        ex, ey, er = meta["eyes"][0]
        meta["lid"] = sample(ex, ey - er * 1.35)
        if meta["mouth"]:
            mx, my, mw = meta["mouth"]
            meta["skin"] = sample(mx - mw * 0.75, my - mw * 0.05)
        _pup_cache[name] = (surf, None, w, h, foot_x, bottom, meta)
    return _pup_cache[name]


def _img_pieza(p):
    k = id(p["bgra"])
    if k not in _skimg:
        _skimg[k] = _skia.Image.fromarray(p["bgra"], colorType=_skia.kBGRA_8888_ColorType,
                                          alphaType=_skia.kPremul_AlphaType).withDefaultMipmaps()
    return _skimg[k]


def _ruido(T, f, seed):
    """Movimiento suave y orgánico (suma de senos de frecuencias que no se repiten)."""
    return (math.sin(T * f + seed) * 0.6 + math.sin(T * f * 1.71 + seed * 2.3) * 0.3
            + math.sin(T * f * 2.93 + seed * 0.7) * 0.1)


# Gestos: cada uno devuelve ángulos (radianes) por hueso. Convención: "sube" el brazo izquierdo de la imagen con
# ángulo positivo y el derecho con negativo; las piernas igual.
FRENTE = {"teddy": 1, "mia": 1, "moe": 1, "nana": -1}  # hacia dónde mira el dibujo original (+1 derecha)


def _pose(name, T, mood, abre, ancho, ene, gesto, lean, nod, head_dy, paso=None, correr=False, escucha=0.0, mira=0):
    """Ángulos de cada hueso. Brazos en unidades de "subida" (0 = colgando, ~2 = por encima de la cabeza)."""
    sd = len(name) * 1.37
    fr = FRENTE[name]
    P = {}
    resp = math.sin(T * 2.4 + sd)
    raiz = lean + 0.016 * _ruido(T, 0.9, sd)
    pecho_a = -0.4 * lean + 0.012 * _ruido(T, 1.1, sd + 1)
    pecho_y = -3.0 * resp
    # cabeza: sigue al cuerpo con retraso, asiente al hablar, escucha y mira al otro
    cab = 0.03 * _ruido(T - 0.15, 0.9, sd) + nod + ene * 0.06 * math.sin(T * 7.3 + sd) + abre * 0.03
    cab += escucha * (0.045 * math.sin(T * 4.3 + sd) + 0.05 * mira * fr)
    cab_y = head_dy - 7 * ene * abs(math.sin(T * 6.1 + sd)) - 6 * escucha
    # brazos: subida izquierda/derecha y codo
    rL = 0.06 * _ruido(T, 1.3, sd + 2) + ene * (0.3 + 0.35 * (0.5 + 0.5 * math.sin(T * 4.7 + sd)))
    rR = 0.06 * _ruido(T, 1.2, sd + 3) + ene * (0.25 + 0.4 * (0.5 + 0.5 * math.sin(T * 5.3 + sd + 1.5)))
    fL = 0.15 + 0.08 * _ruido(T - 0.08, 1.6, sd + 4) + ene * (0.45 + 0.35 * math.sin(T * 6.2 + sd))
    fR = 0.15 + 0.08 * _ruido(T - 0.08, 1.5, sd + 5) + ene * (0.45 + 0.35 * math.sin(T * 5.8 + sd + 2))
    piernas = {}
    dy_cuerpo = 0.0
    cola_a, cola_f = 0.18, 3.0
    g = gesto
    if g is None:
        g = {"panico": "agitar", "sorpresa": "arriba", "feliz": "celebrar", "triste": "caido", "cansado": "caido",
             "enfado": "punos", "smug": "tranquilo"}.get(mood)
    if g == "agitar":
        rL += 1.0 + 0.6 * math.sin(T * 13 + sd)
        rR += 1.0 + 0.6 * math.sin(T * 13 + sd + 2.2)
        fL += 0.5 * math.sin(T * 15 + sd + 1)
        fR += 0.5 * math.sin(T * 15 + sd + 3)
        cab += 0.06 * math.sin(T * 11)
        cola_a, cola_f = 0.35, 12
    elif g == "arriba":
        rL += 2.0
        rR += 2.0
        fL += 0.4
        fR += 0.4
    elif g == "celebrar":
        k = 0.5 + 0.5 * math.sin(T * 8)
        rL += 1.8 + 0.4 * k
        rR += 1.8 + 0.4 * k
        fL += 0.4 * k
        fR += 0.4 * k
        cola_a, cola_f = 0.4, 11
    elif g == "caido":
        rL = 0.02 * _ruido(T, 0.7, 3)
        rR = 0.02 * _ruido(T, 0.7, 4)
        fL, fR = 0.05, 0.05
        cab += 0.12
        cab_y += 30
        cola_a, cola_f = 0.05, 1.2
    elif g == "punos":
        rL += 0.5 + 0.15 * math.sin(T * 22)
        rR += 0.5 + 0.15 * math.sin(T * 22 + 1)
        fL += 1.3
        fR += 1.3
    elif g == "tranquilo":
        cab -= 0.05
    elif g == "saludo":
        rR += 2.1
        fR += 0.3 + 0.5 * math.sin(T * 10)
    elif g == "senalar":
        rR += 1.3
        fR = 0.1
    elif g == "suplicar":
        rL += 0.9 + 0.08 * math.sin(T * 9)
        rR += 0.9 + 0.08 * math.sin(T * 9 + 0.4)
        fL += 1.1
        fR += 1.1
        cab += 0.08
    elif g == "encoger":
        rL += 0.45
        rR += 0.45
        fL += 0.9
        fR += 0.9
        cab_y += 18
    elif g == "manos_cadera":
        rL, rR, fL, fR = 0.6, 0.6, 1.4, 1.4
    # ---- andar / correr: la fase sale de la distancia recorrida (los pies no resbalan)
    if paso is not None:
        ph = 2 * math.pi * paso
        A, K, B = (0.75, 1.15, 26) if correr else (0.45, 0.6, 12)
        piernas["i"] = (-fr * A * math.sin(ph), K * max(0.0, math.sin(ph + 0.9)), 0.35 * math.sin(ph + 0.4))
        piernas["d"] = (fr * A * math.sin(ph), K * max(0.0, math.sin(ph + math.pi + 0.9)), -0.35 * math.sin(ph + 0.4))
        dy_cuerpo = -B * abs(math.cos(ph))
        raiz += fr * (0.1 if correr else 0.04)
        swing = (0.9 if correr else 0.45)
        if g not in ("agitar", "arriba", "celebrar", "saludo", "suplicar"):
            rL += 0.4 if correr else 0.1
            rR += 0.4 if correr else 0.1
            fL += 1.0 if correr else 0.25
            fR += 1.0 if correr else 0.25
            P["_swing"] = swing * math.sin(ph)
        else:
            P["_swing"] = 0.0
        cab += 0.03 * math.sin(2 * ph)
        cola_a, cola_f = (0.3, 9) if correr else (0.22, 5)
    else:
        P["_swing"] = 0.0
    P["_dy"] = dy_cuerpo
    P["raiz"] = raiz
    P["pecho"] = (pecho_a, 0.0, pecho_y)
    P["cabeza"] = (cab, 0.0, cab_y)
    sw = P.pop("_swing")
    # ---- a cada esqueleto
    if name == "teddy":
        # 0 = brazos colgando junto al cuerpo (el dibujo original los tiene abiertos: subida ~0,75)
        P["brazo_i"] = -0.75 + rL + fr * sw
        P["antebrazo_i"] = -0.3 + fL
        P["mano_i"] = 0.25 * fL
        P["brazo_d"] = 0.7 - rR - fr * sw
        P["antebrazo_d"] = 0.55 - fR
        P["mano_d"] = -0.25 * fR
        P["mandibula"] = -0.05 + abre * (0.34 + 0.12 * (1 - ancho))
        li = piernas.get("i", (0.04 * _ruido(T, 0.8, 6), 0.0, 0.0))
        ld = piernas.get("d", (-0.04 * _ruido(T, 0.8, 6), 0.0, 0.0))
        P["muslo_i"], P["pierna_i"], P["pie_i"] = li
        P["muslo_d"], P["pierna_d"], P["pie_d"] = ld
        P["cola"] = cola_a * math.sin(T * cola_f)
        P["cola2"] = cola_a * 1.3 * math.sin(T * cola_f - 0.9)
        dcab = cab - (0.03 * _ruido(T - 0.27, 0.9, sd))
        P["oreja_i"] = -dcab * 4 + 0.05 * math.sin(T * 3.1) + 0.1 * escucha
        P["oreja_d"] = dcab * 5 + 0.08 * math.sin(T * 2.7 + 1) + abre * 0.06 - 0.12 * escucha
    elif name == "moe":
        sip = 1.0 if g == "sorber" else 0.0
        P["brazos"] = (0.03 * _ruido(T, 1.2, 2), 0.0, -6 * resp - 30 * ene - 120 * sip + 20 * (g == "caido") - 25 * (g in ("arriba", "celebrar", "agitar")))
        if paso is not None:
            ph = 2 * math.pi * paso
            P["pie_i"] = 0.45 * math.sin(ph)
            P["pie_d"] = 0.45 * math.sin(ph + math.pi)
            P["raiz"] = P["raiz"] + 0.07 * math.sin(ph)
        else:
            P["pie_i"] = 0.05 * _ruido(T, 1.3, 1) + (0.25 * math.sin(T * 12) if g == "agitar" else 0)
            P["pie_d"] = 0.05 * _ruido(T, 1.1, 2) - (0.25 * math.sin(T * 12) if g == "agitar" else 0)
        P["cabeza"] = (cab * 0.5, 0.0, cab_y * 0.5)
    elif name == "nana":
        tec = 1.0 if g == "teclear" else 0.0
        P["brazo_i"] = 0.35 * (rL - 0.3) + 0.02 * tec * math.sin(T * 31)
        P["antebrazo_i"] = 0.25 * (fL - 0.15) + 0.03 * tec * math.sin(T * 27 + 1)
        P["brazo_d"] = (-0.25 * (rR - 0.2) + 0.04 * tec * math.sin(T * 23), 0.0, 0.0)
        P["mano_d"] = -0.3 * (fR - 0.15) + 0.12 * tec * abs(math.sin(T * 17)) - 0.15 * ene * math.sin(T * 5)
        if paso is not None:
            ph = 2 * math.pi * paso
            P["pie_i"] = 0.3 * math.sin(ph)
            P["pie_d"] = 0.3 * math.sin(ph + math.pi)
            P["raiz"] = P["raiz"] + 0.06 * math.sin(ph)
        else:
            P["pie_i"] = 0.03 * _ruido(T, 0.8, 6)
            P["pie_d"] = -0.03 * _ruido(T, 0.8, 6)
    elif name == "mia":
        P["brazos"] = (0.02 * _ruido(T, 1.0, 3) + 0.03 * ene * math.sin(T * 5), 0.0,
                       -5 * resp - 22 * ene - 35 * (g in ("celebrar", "arriba", "encoger")))
        li = piernas.get("i", (0.03 * _ruido(T, 0.8, 6), 0.0, 0.0))
        ld = piernas.get("d", (-0.03 * _ruido(T, 0.8, 6), 0.0, 0.0))
        P["muslo_i"], P["pierna_i"] = li[0], li[1]
        P["muslo_d"], P["pierna_d"] = ld[0], ld[1]
        P["cola"] = -cola_a * 0.8 * (0.4 + math.sin(T * cola_f * 0.6))
        P["cola2"] = -cola_a * 1.1 * math.sin(T * cola_f * 0.6 - 1.0)
        dcab = cab - (0.03 * _ruido(T - 0.27, 0.9, sd))
        P["coleta"] = -dcab * 4 + 0.07 * math.sin(T * 2.3) - 0.12 * abs(math.sin(T * 6)) * (g == "celebrar" or paso is not None)
        P["oreja_i"] = 0.04 * math.sin(T * 1.9) + dcab * 2
        P["oreja_d"] = -0.05 * math.sin(T * 2.2 + 1) - dcab * 2
    return P


def recorrido(lt, puntos, zancada=330.0):
    """Desplazamiento por la escena. puntos = [(t, x), ...] (t en segundos de la escena).
    Devuelve (x, paso, mirando_derecha, en_marcha): paso = distancia/zancada (para el ciclo de andar)."""
    pts = sorted(puntos)
    if lt <= pts[0][0]:
        return pts[0][1], 0.0, pts[1][1] >= pts[0][1] if len(pts) > 1 else True, False
    dist = 0.0
    for (t0, x0), (t1, x1) in zip(pts, pts[1:]):
        if lt < t1:
            p = (lt - t0) / max(1e-6, t1 - t0)
            e = p * p * (3 - 2 * p)
            x = x0 + (x1 - x0) * e
            dist += abs(x - x0)
            return x, dist / zancada, x1 >= x0, abs(x1 - x0) > 1
        dist += abs(x1 - x0)
    return pts[-1][1], dist / zancada, pts[-1][1] >= pts[-2][1] if len(pts) > 1 else True, False


def _mat(M):
    return cairo.Matrix(M[0, 0], M[1, 0], M[0, 1], M[1, 1], M[0, 2], M[1, 2])


def _dibuja_malla(ctx, name, pose, alpha=1.0, tint=None, smear=0.0, k=1.0, sgn=1):
    """Deforma las piezas del personaje y las pinta con skia en coordenadas de pantalla."""
    piezas, M = _rig.deformar(name, pose)
    m = ctx.get_matrix()
    xx, yx, xy, yy, x0, y0 = m.xx, m.yx, m.xy, m.yy, m.x0, m.y0
    devs = []
    for p, P in piezas:
        dxs = xx * P[:, 0] + xy * P[:, 1] + x0
        dys = yx * P[:, 0] + yy * P[:, 1] + y0
        devs.append((p, dxs, dys))
    allx = np.concatenate([d[1] for d in devs])
    ally = np.concatenate([d[2] for d in devs])
    ctx.save()
    ctx.identity_matrix()
    cx0, cy0, cx1, cy1 = ctx.clip_extents()
    ctx.restore()
    bx0, by0 = max(cx0, math.floor(allx.min()) - 2), max(cy0, math.floor(ally.min()) - 2)
    bx1, by1 = min(cx1, math.ceil(allx.max()) + 2), min(cy1, math.ceil(ally.max()) + 2)
    if bx1 - bx0 < 2 or by1 - by0 < 2:
        return M
    bw, bh = int(bx1 - bx0), int(by1 - by0)
    sk = _skia.Surface(bw, bh)
    cv = sk.getCanvas()
    cv.clear(_skia.ColorTRANSPARENT)
    samp = _skia.SamplingOptions(_skia.FilterMode.kLinear, _skia.MipmapMode.kLinear)
    for p, dxs, dys in devs:
        pts = [_skia.Point(float(a - bx0), float(b - by0)) for a, b in zip(dxs, dys)]
        uv = [_skia.Point(float(a), float(b)) for a, b in p["V"]]
        v = _skia.Vertices(_skia.Vertices.kTriangles_VertexMode, pts, uv, None, p["T"].ravel().tolist())
        paint = _skia.Paint(Shader=_img_pieza(p).makeShader(_skia.TileMode.kDecal, _skia.TileMode.kDecal, samp),
                            AntiAlias=True)
        cv.drawVertices(v, paint)
    arr = np.ascontiguousarray(sk.toarray())
    cs = cairo.ImageSurface.create_for_data(memoryview(arr.reshape(-1)), cairo.FORMAT_ARGB32, bw, bh, bw * 4)
    ctx.save()
    ctx.identity_matrix()
    if abs(smear) > 1:  # estela
        for i in range(1, 5):
            off = -smear * i * 0.55 * (math.hypot(xx, yx) / max(1e-6, abs(k))) * k
            ctx.set_source_surface(cs, bx0 + off, by0)
            ctx.paint_with_alpha(alpha * 0.22 * (1 - i / 5))
    ctx.set_source_surface(cs, bx0, by0)
    ctx.paint_with_alpha(alpha) if alpha < 0.999 else ctx.paint()
    if tint:
        ctx.set_source_rgba(*tint)
        ctx.mask_surface(cs, bx0, by0)
    ctx.restore()
    cs.finish()
    return M


def puppet(ctx, name, x, y, s=1.0, T=0.0, mood="normal", talk=0.0, look=(0, 0), flip=False, bounce=0.0, phone_prop=False,
           screen_text=None, rot=0.0, sq=1.0, lean=0.0, dx=0.0, dy=0.0, head_dy=0.0, nod=0.0, smear=0.0, tint=None,
           blush=0.0, alpha=1.0, spin=0.0, shadow=True, sway=1.0, lid=None, gesto=None, pose=None, ene=None,
           paso=None, correr=False, escucha=0.0, mira=0):
    """Dibuja a un personaje oficial (muñeco articulado) con los pies en (x, y).

    talk: apertura de boca 0..1, o (apertura, forma) de L.boca(...) · gesto: agitar, arriba, celebrar, caido, punos,
    tranquilo, saludo, senalar, suplicar, encoger, manos_cadera, sorber (Moe), teclear (Nana) · paso: fase del ciclo de
    andar (sale de recorrido(); correr=True para correr) · escucha 0..1: reacciona a quien habla (asiente) y mira=±1 le
    gira la cabeza hacia ese lado · pose: ángulos por hueso que
    se suman · ene: energía de la voz 0..1 (gesticula más) · s escala · sq estirar/aplastar · lean doblarse ·
    dx, dy desplazar · head_dy, nod cabeza · smear estela · blush colorete · tint (r,g,b,a) · lid párpados.
    Devuelve {"head", "top", "feet"} en coordenadas del mundo.
    """
    surf, _h, w, h, fx, fb, meta = _pup(name)
    k = _PUP_WORLD * s
    if isinstance(talk, (tuple, list)):
        abre, ancho = float(talk[0]), float(talk[1])
    else:
        abre, ancho = clamp(float(talk)), 0.5
    if ene is None:
        ene = clamp(abre * 1.3)
    hop = -abs(math.sin(T * 7)) * 18 * s * bounce
    jx = 0.0
    sq_t = sq
    if mood == "panico":
        jx = 4 * s * math.sin(T * 47)
    elif mood == "sorpresa":
        hop -= 14 * s * abs(math.sin(T * 10))
        sq_t *= 1.04
    elif mood == "enfado":
        jx = 5 * s * math.sin(T * 61)
    elif mood == "feliz":
        hop -= abs(math.sin(T * 6)) * 12 * s
    P = _pose(name, T, mood, abre, ancho, ene, gesto, lean, nod, head_dy, paso, correr, escucha, mira)
    hop += P.pop("_dy") * s
    for b, v in (pose or {}).items():
        base = P.get(b, 0.0)
        if isinstance(base, tuple) or isinstance(v, tuple):
            bb = base if isinstance(base, tuple) else (base, 0.0, 0.0)
            vv = v if isinstance(v, tuple) else (v, 0.0, 0.0)
            P[b] = (bb[0] + vv[0], bb[1] + vv[1], bb[2] + vv[2])
        else:
            P[b] = base + v
    ctx.save()
    ctx.translate(x + dx, y)
    if shadow:
        lift = clamp(-(dy + hop) / 300)
        soft_shadow(ctx, 0, 0, w * k * 0.38 * (1 - 0.4 * lift), 22 * s * (1 - 0.4 * lift), 0.28 * (1 - 0.5 * lift) * alpha)
    ctx.translate(jx, dy + hop)
    ctx.rotate(rot + spin)
    sgn = -1 if flip else 1
    ctx.scale(k * sgn / (sq_t ** 0.6), k * sq_t)
    ctx.translate(-fx, -fb)
    M = _dibuja_malla(ctx, name, P, alpha, tint, smear, k, sgn)
    Mh = M["cabeza"]
    # --- colorete, párpados y boca (pegados a la cabeza)
    ctx.save()
    ctx.transform(_mat(Mh))
    if blush > 0.01:
        for cx, cy in meta["cheeks"]:
            g = cairo.RadialGradient(cx, cy, 0, cx, cy, 70)
            g.add_color_stop_rgba(0, 1, 0.35, 0.5, 0.75 * blush)
            g.add_color_stop_rgba(1, 1, 0.35, 0.5, 0)
            ctx.set_source(g)
            ellipse(ctx, cx, cy, 80, 50)
            ctx.fill()
    ph = (T + len(name) * 0.71) % 3.8
    lv = 1.0 if ph < 0.11 else 0.0
    if mood in ("sospecha", "cansado") and name in ("teddy", "moe"):
        lv = max(lv, 0.5)
    if mood == "dormido":
        lv = 1.0
    if lid is not None:
        lv = max(lv, lid)
    if lv > 0:
        for ex, ey, er in meta["eyes"]:
            ctx.save()
            ellipse(ctx, ex, ey, er * 1.12, er * 1.12)
            ctx.clip()
            ctx.rectangle(ex - er * 1.3, ey - er * 1.25, er * 2.6, er * 2.5 * lv)
            ctx.set_source_rgb(*meta["lid"])
            ctx.fill()
            ctx.move_to(ex - er * 1.05, ey - er * 1.2 + er * 2.4 * lv)
            ctx.line_to(ex + er * 1.05, ey - er * 1.2 + er * 2.4 * lv)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(er * 0.16)
            ctx.stroke()
            ctx.restore()
    if meta["mouth"] and abre > 0.05:  # boca con forma de vocal: "oo" redonda, "ee" ancha
        mx, my, mw = meta["mouth"]
        ellipse(ctx, mx, my, mw * 0.74, mw * 0.3)
        ctx.set_source_rgb(*meta["skin"])
        ctx.fill()
        wid = mw * (0.75 + 0.6 * ancho)
        hgt = mw * (0.14 + 0.66 * abre) * (1.25 - 0.4 * ancho)
        ctx.move_to(mx - wid / 2, my)
        ctx.curve_to(mx - wid / 2, my + hgt * 1.3, mx + wid / 2, my + hgt * 1.3, mx + wid / 2, my)
        ctx.curve_to(mx + wid / 4, my - hgt * 0.25, mx - wid / 4, my - hgt * 0.25, mx - wid / 2, my)
        ctx.close_path()
        ctx.set_source_rgb(0.3, 0.06, 0.11)
        ctx.fill_preserve()
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(mw * 0.06)
        ctx.stroke()
        if abre > 0.35:  # dientes de arriba
            ctx.save()
            ctx.move_to(mx - wid / 2, my)
            ctx.curve_to(mx - wid / 2, my + hgt * 1.3, mx + wid / 2, my + hgt * 1.3, mx + wid / 2, my)
            ctx.close_path()
            ctx.clip()
            ctx.rectangle(mx - wid / 2, my - 2, wid, hgt * 0.28)
            ctx.set_source_rgb(0.97, 0.96, 0.92)
            ctx.fill()
            ctx.restore()
        ellipse(ctx, mx, my + hgt * 0.92, wid * 0.22, hgt * 0.3)
        ctx.set_source_rgb(0.93, 0.45, 0.52)
        ctx.fill()
    ctx.restore()
    # --- móvil en la mano (Teddy / Mia) y texto en la pantalla del móvil de Nana
    hb, (hx_, hy_) = meta["hand"]
    if phone_prop and name != "nana":
        ctx.save()
        ctx.transform(_mat(M[hb]))
        phone(ctx, hx_, hy_ - (0 if name == "mia" else 70), 3.2, 0.12, glow=0.5 + 0.5 * math.sin(T * 5))
        ctx.restore()
    if screen_text and "screen" in meta:
        sx, sy, sr = meta["screen"]
        ctx.save()
        ctx.transform(_mat(M[hb]))
        ctx.translate(sx, sy)
        ctx.rotate(sr)
        sz = 60
        while sz > 18 and text_width(ctx, screen_text, sz) > 150:
            sz -= 2
        text(ctx, screen_text, 0, 0, sz, INK, shadow=False)
        ctx.restore()
    pts = {}
    for key, (px, py), bone in (("head", meta["head"], "cabeza"), ("top", meta["top"], "cabeza"), ("feet", (fx, fb), "raiz")):
        Mb = M[bone]
        qx = Mb[0, 0] * px + Mb[0, 1] * py + Mb[0, 2]
        qy = Mb[1, 0] * px + Mb[1, 1] * py + Mb[1, 2]
        pts[key] = ctx.user_to_device(qx, qy)
    ctx.restore()
    out = {kk: ctx.device_to_user(*v) for kk, v in pts.items()}
    hx, hy = out["head"]
    tx, ty = out["top"]
    if mood == "panico":
        gotas_sudor(ctx, hx, hy - 40 * s, T, s)
    if mood == "enfado":
        _anger(ctx, hx + 140 * s * sgn, ty + 30 * s, 44 * s, T)
        vapor(ctx, hx, ty + 20 * s, T, s * 0.9)
    if mood == "sorpresa":
        _shock_lines(ctx, tx, ty + 40 * s, 170 * s, T)
    return out


def cabeza(name, x, y, s=1.0, flip=False):
    """Dónde queda la cabeza (mundo) de un personaje con los pies en (x, y): útil para apuntar la cámara."""
    surf, half, w, h, fx, fb, meta = _pup(name)
    k = _PUP_WORLD * s
    hx, hy = meta["head"]
    return x + (hx - fx) * k * (-1 if flip else 1), y + (hy - fb) * k


def _anger(ctx, x, y, r, T):
    k = 1 + 0.12 * math.sin(T * 12)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    for a in range(4):
        ctx.save()
        ctx.rotate(a * math.pi / 2)
        ctx.move_to(r * 0.25, r * 0.25)
        ctx.curve_to(r * 0.3, r * 0.9, r * 0.9, r * 0.3, r * 0.25, r * 0.25)
        ctx.restore()
    stroke(ctx, hexc("#FF3B3B"), r * 0.22)
    ctx.restore()


def _shock_lines(ctx, x, y, r, T):
    a = 0.6 + 0.4 * math.sin(T * 20)
    for k in (-2, -1, 0, 1, 2):
        ang = -math.pi / 2 + k * 0.32
        ctx.move_to(x + math.cos(ang) * r, y + math.sin(ang) * r)
        ctx.line_to(x + math.cos(ang) * r * 1.35, y + math.sin(ang) * r * 1.35)
    stroke(ctx, INK, 9, a)


# Envoltorios con la misma firma que usan los escenas.py (los argumentos extra pasan a puppet: sq, lean, dx, dy...)
def teddy(ctx, x, y, s=1.0, T=0.0, mood="normal", talk=0.0, look=(0, 0), arms="abajo", prop=None, bounce=True, flip=False,
          **kw):
    return puppet(ctx, "teddy", x, y, s, T, mood, talk, look, flip, 1.0 if bounce else 0.0, phone_prop=(arms == "movil"),
                  rot=kw.pop("rot", -0.06 if arms == "arriba" else 0.0), **kw)


def moe(ctx, x, y, s=1.0, T=0.0, mood="normal", talk=0.0, look=(0, 0), arms="taza", prop=None, bounce=False, flip=False,
        **kw):
    return puppet(ctx, "moe", x, y, s, T, mood, talk, look, flip, 0.4 if bounce else 0.0, **kw)


def nana(ctx, x, y, s=1.0, T=0.0, mood="smug", talk=0.0, look=(0, 0), gafas=None, prop="movil", screen_text=None, typing=False,
         flip=False, **kw):
    if typing:
        kw.setdefault("gesto", "teclear")
    return puppet(ctx, "nana", x, y, s, T, mood, talk, look, flip, 0.0, screen_text=screen_text,
                  rot=kw.pop("rot", 0.0), **kw)


def mia(ctx, x, y, s=1.0, T=0.0, mood="smug", talk=0.0, look=(0, 0), arms="cruzados", prop=None, bounce=False, flip=False,
        **kw):
    return puppet(ctx, "mia", x, y, s, T, mood, talk, look, flip, 0.3 if bounce else 0.0, phone_prop=(arms == "movil"), **kw)


PERSONAJES = {"teddy": teddy, "moe": moe, "nana": nana, "mia": mia}


# ---------------------------------------------------------------- decorados
# Cada decorado acepta `var` (0..n) para cambiar colores/objetos y no repetir planos.
WALLS = [hexc("#3B3366"), hexc("#2E4A5C"), hexc("#5A3B4F"), hexc("#3A4F3A"), hexc("#4B3F2E")]
FLOORS = [hexc("#6B4E3D"), hexc("#4F5966"), hexc("#7A5A44"), hexc("#5D4A5E")]


def city_window(ctx, x, y, w, h, T, noche=True, var=0):
    rrect(ctx, x - 14, y - 14, w + 28, h + 28, 10)
    fill_keep(ctx, hexc("#EDE6D6"))
    stroke(ctx, INK, 6)
    sky = [(0, hexc("#1B1F4A")), (1, hexc("#4B3A7A"))] if noche else [(0, hexc("#7CC7FF")), (1, hexc("#CFEFFF"))]
    ctx.rectangle(x, y, w, h)
    ctx.set_source(vgrad(ctx, 0, y, 0, y + h, sky))
    ctx.fill()
    rng = np.random.default_rng(10 + var)
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    bx = x - 10
    while bx < x + w:
        bw, bh = rng.uniform(50, 110), rng.uniform(h * 0.3, h * 0.85)
        ctx.rectangle(bx, y + h - bh, bw, bh)
        fill(ctx, hexc("#2A2552") if noche else hexc("#8FA3C7"))
        for wx in np.arange(bx + 10, bx + bw - 14, 22):
            for wy in np.arange(y + h - bh + 12, y + h - 10, 26):
                if rng.random() < (0.45 if noche else 0.2):
                    ctx.rectangle(wx, wy, 10, 14)
                    fill(ctx, hexc("#FFD46B") if noche else WHITE, 0.9)
        bx += bw + rng.uniform(2, 12)
    if noche:  # cartel de la ciudad
        rrect(ctx, x + w * 0.55, y + h * 0.18, 150, 44, 8)
        fill(ctx, hexc("#FF5FA2"), 0.85 + 0.15 * math.sin(T * 6))
        text(ctx, "ANIMAL CITY", x + w * 0.55 + 75, y + h * 0.18 + 22, 22, WHITE, shadow=False)
    ctx.restore()
    ctx.move_to(x + w / 2, y)
    ctx.line_to(x + w / 2, y + h)
    ctx.move_to(x, y + h / 2)
    ctx.line_to(x + w, y + h / 2)
    stroke(ctx, hexc("#EDE6D6"), 10)


def salon(ctx, T, var=0, noche=True, sofa=True, sillon=True):
    """Salón del piso compartido: pared, ventana con la ciudad, sofá azul, sillón de Nana."""
    wall = WALLS[var % len(WALLS)]
    ctx.rectangle(-3000, -3000, W + 6000, 3000 + 1380)
    ctx.set_source(vgrad(ctx, 0, 0, 0, 1380, [(0, wall), (1, tuple(c * 0.8 for c in wall))]))
    ctx.fill()
    for k in range(-30, 40):  # papel pintado de rayas suaves
        ctx.rectangle(k * 90, -3000, 30, 3000 + 1380)
        fill(ctx, WHITE, 0.035)
    city_window(ctx, 360, 360, 360, 420, T, noche, var)
    # cuadro
    rrect(ctx, 840, 470, 170, 210, 8)
    fill_keep(ctx, hexc("#F4D35E") if var % 2 else hexc("#7FD1B9"))
    stroke(ctx, INK, 6)
    circle(ctx, 925, 560, 45)
    fill(ctx, hexc("#E04A3A"), 0.8)
    # suelo
    floor = FLOORS[var % len(FLOORS)]
    ctx.rectangle(-3000, 1380, W + 6000, 3000)
    fill(ctx, floor)
    for k in range(-30, 40):
        ctx.move_to(k * 140, 1380)
        ctx.line_to(k * 140 - 200, 3000)
    stroke(ctx, INK, 3, 0.25)
    ellipse(ctx, 540, 1560, 560, 110)  # alfombra
    fill(ctx, hexc("#E8C07D") if var % 2 == 0 else hexc("#9FD4E8"), 0.55)
    # lámpara
    ctx.move_to(130, 1380)
    ctx.line_to(130, 860)
    stroke(ctx, INK, 10)
    ctx.move_to(60, 860)
    ctx.line_to(200, 860)
    ctx.line_to(170, 760)
    ctx.line_to(90, 760)
    ctx.close_path()
    fill_keep(ctx, hexc("#FFE08A"))
    stroke(ctx, INK, 6)
    if noche:
        g = cairo.RadialGradient(130, 860, 10, 130, 860, 420)
        g.add_color_stop_rgba(0, 1, 0.9, 0.55, 0.28)
        g.add_color_stop_rgba(1, 1, 0.9, 0.55, 0)
        ctx.set_source(g)
        circle(ctx, 130, 860, 420)
        ctx.fill()
    if sofa:
        rrect(ctx, 220, 1100, 640, 300, 60)
        fill_keep(ctx, hexc("#3E7CC4"))
        stroke(ctx, INK, 7)
        rrect(ctx, 260, 1200, 560, 120, 30)
        fill_keep(ctx, hexc("#5B97DB"))
        stroke(ctx, INK, 5)
    if sillon:
        rrect(ctx, 760, 1120, 300, 300, 70)
        fill_keep(ctx, hexc("#B5524E"))
        stroke(ctx, INK, 7)


def puerta(ctx, T, var=0, abierta=1.0):
    """Recibidor con la puerta de entrada (abierta 0..1) y el pasillo del edificio detrás."""
    wall = WALLS[(var + 2) % len(WALLS)]
    ctx.rectangle(-3000, -3000, W + 6000, 6000)
    fill(ctx, wall)
    ctx.rectangle(-3000, 1440, W + 6000, 3000)
    fill(ctx, FLOORS[(var + 1) % len(FLOORS)])
    # hueco
    rrect(ctx, 250, 420, 580, 1030, 12)
    fill_keep(ctx, hexc("#F2E3C6"))
    stroke(ctx, INK, 8)
    ctx.rectangle(280, 450, 520, 1000)
    ctx.set_source(vgrad(ctx, 0, 450, 0, 1450, [(0, hexc("#E9D9B8")), (1, hexc("#C9B48C"))]))
    ctx.fill()
    ctx.rectangle(280, 1300, 520, 150)
    fill(ctx, hexc("#A47A55"))
    # hoja de la puerta
    k = clamp(abierta)
    pw = 520 * (1 - 0.82 * k)
    ctx.rectangle(280, 450, pw, 1000)
    fill_keep(ctx, hexc("#8C3B2E"))
    stroke(ctx, INK, 7)
    circle(ctx, 280 + pw - 40, 960, 16)
    fill(ctx, hexc("#F4D35E"))
    # felpudo
    rrect(ctx, 340, 1470, 400, 70, 14)
    fill(ctx, hexc("#C98C4A"))
    text(ctx, "HI", 540, 1505, 38, hexc("#6B4423"), shadow=False)


def cocina(ctx, T, var=0):
    wall = WALLS[(var + 1) % len(WALLS)]
    ctx.rectangle(-3000, -3000, W + 6000, 6000)
    fill(ctx, wall)
    for gx in range(-20, 30):  # azulejos
        for gy in range(5, 13):
            ctx.rectangle(gx * 80 + 2, gy * 80 + 2, 76, 76)
            fill(ctx, WHITE, 0.06)
    rrect(ctx, 760, 520, 260, 900, 20)  # nevera
    fill_keep(ctx, hexc("#DDE7F0"))
    stroke(ctx, INK, 7)
    ctx.move_to(760, 860)
    ctx.line_to(1020, 860)
    stroke(ctx, INK, 6)
    ctx.rectangle(-3000, 1180, 3760, 260)  # encimera
    fill_keep(ctx, hexc("#C98C4A"))
    stroke(ctx, INK, 7)
    ctx.rectangle(-3000, 1440, W + 6000, 3000)
    fill(ctx, FLOORS[(var + 2) % len(FLOORS)])


def rafaga(ctx, T, rgb=None, var=0):
    """Fondo de impacto para primeros planos de reacción: color plano con rayos."""
    pal = [hexc("#FFD23F"), hexc("#FF5FA2"), hexc("#5EB8F2"), hexc("#7CE38B"), hexc("#B07CE8")]
    base = rgb or pal[var % len(pal)]
    ctx.rectangle(-3000, -3000, W + 6000, H + 6000)
    fill(ctx, base)
    ctx.save()
    ctx.translate(W / 2, H * 0.45)
    ctx.rotate(T * 0.25)
    for k in range(18):
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 2600, k * math.pi / 9, k * math.pi / 9 + math.pi / 18)
        ctx.close_path()
        fill(ctx, WHITE, 0.18)
    ctx.restore()


# ---------------------------------------------------------------- rótulos y textos
def _wrap(ctx, s, size, maxw, font=FONT):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if text_width(ctx, t, size, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def rotulo(ctx, s, pj, appear=1.0, y=330, size=58, maxw=880):
    """Rótulo de diálogo arriba, con el color del personaje y su nombre."""
    if appear <= 0.01 or not s:
        return
    col = PJ[pj]["color"]
    lines = _wrap(ctx, s, size, maxw)
    if len(lines) > 3:
        size = int(size * 0.8)
        lines = _wrap(ctx, s, size, maxw)
    lh = size * 1.18
    w = max(text_width(ctx, ln, size) for ln in lines) + size * 1.2
    h = lh * len(lines) + size * 0.9
    ctx.save()
    ctx.translate(W / 2, y + h / 2)
    k = 0.85 + 0.15 * appear
    ctx.scale(k, k)
    rrect(ctx, -w / 2 + 8, -h / 2 + 10, w, h, 26)
    fill(ctx, INK, 0.6)
    rrect(ctx, -w / 2, -h / 2, w, h, 26)
    fill_keep(ctx, (0.07, 0.06, 0.11), 0.92)
    stroke(ctx, col, 7)
    # etiqueta con el nombre
    nm = PJ[pj]["nombre"]
    nw = text_width(ctx, nm, 30) + 34
    rrect(ctx, -w / 2 + 26, -h / 2 - 24, nw, 46, 14)
    fill_keep(ctx, col)
    stroke(ctx, INK, 4)
    text(ctx, nm, -w / 2 + 26 + nw / 2, -h / 2 - 1, 30, INK, shadow=False)
    for i, ln in enumerate(lines):
        text(ctx, ln, 0, -h / 2 + size * 0.45 + lh * (i + 0.5), size, WHITE, shadow=False)
    ctx.restore()


_MUTE = {"impacto": False}  # miniaturas.py lo activa para sacar fotogramas limpios (sin textos de impacto ni badges)


def impacto(ctx, s, x=W / 2, y=760, size=170, rgb=WHITE, appear=1.0, T=0.0, shake_amp=6, rot=-0.04):
    """Texto gigante (Anton) para golpes: 'NOW.', 'PLEASE.'..."""
    if appear <= 0.01 or _MUTE["impacto"]:
        return
    dx, dy = shake(T, shake_amp) if shake_amp else (0, 0)
    ctx.save()
    ctx.translate(x + dx, y + dy)
    ctx.rotate(rot)
    k = appear
    ctx.scale(k, k)
    ctx.select_font_face(FONT_IMPACT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    wdt = ctx.text_extents(s)[4]
    ctx.move_to(-wdt / 2, size * 0.36)
    ctx.text_path(s)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*INK, 1)
    ctx.set_line_width(22)
    ctx.stroke_preserve()
    ctx.set_source_rgba(*rgb, 1)
    ctx.fill()
    ctx.restore()


def zoom_cam(ctx, lt, kfs):
    """Cámara con keyframes [(t, (zoom, cx, cy)), ...]."""
    z, cx, cy = keyframes(lt, kfs)
    camera(ctx, z, cx, cy)


def badge(ctx, s, x, y, appear=1.0, size=56, bg=RED, fg=WHITE):
    if _MUTE["impacto"]:
        return
    _anim.badge(ctx, s, x, y, appear, size, bg, fg)


# ---------------------------------------------------------------- diálogo
class Dialogo:
    def __init__(self, timeline):
        self.lines = timeline["lineas"]
        self.fps = timeline.get("env_fps", 60)
        self.trozos = [_trozos(_palabras(ln, self.fps)) for ln in self.lines]

    def line(self, T):
        for ln in self.lines:
            if ln["ini"] <= T < ln["fin"] + 0.25:
                return ln
        return None

    def boca(self, pj, T):
        """(apertura 0..1, forma 0 = "oo" redonda .. 1 = "ee" ancha) de la boca de ese personaje en el instante T."""
        for ln in self.lines:
            if ln["pj"] == pj and ln["ini"] <= T < ln["fin"]:
                i = int((T - ln["ini"]) * self.fps)
                env = ln.get("env") or []
                cen = ln.get("cen") or []
                if 0 <= i < len(env):
                    a = clamp(env[i] * 1.25)
                    if a < 0.1:
                        a = 0.0
                    return (a, cen[i] if i < len(cen) else 0.5)
        return (0.0, 0.5)

    def energia(self, pj, T, ventana=0.35):
        """Energía media de la voz en la última fracción de segundo (para los gestos)."""
        n = 6
        return sum(self.talk(pj, T - ventana * j / n) for j in range(n)) / n

    def speaking(self, pj, T):
        ln = self.line(T)
        return bool(ln and ln["pj"] == pj and T < ln["fin"])

    def talk(self, pj, T):
        """0..1 apertura de boca según el volumen de la voz de ese personaje en el instante T."""
        for ln in self.lines:
            if ln["pj"] == pj and ln["ini"] <= T < ln["fin"]:
                i = int((T - ln["ini"]) * self.fps)
                env = ln.get("env") or []
                if 0 <= i < len(env):
                    return clamp(env[i] * 1.25)
        return 0.0


# ---------------------------------------------------------------- efectos de sonido extra
SR = 44100


def _tone(f, d, a=0.4, decay=4.0):
    t = np.arange(int(SR * d)) / SR
    return a * np.sin(2 * np.pi * f * t) * np.exp(-t * decay)


def sfx_doorbell():
    return np.concatenate([_tone(988, 0.45, 0.45, 3), _tone(784, 0.8, 0.45, 2.5)])


def sfx_error():
    t = np.arange(int(SR * 0.35)) / SR
    return 0.25 * np.sign(np.sin(2 * np.pi * 220 * t)) * np.exp(-t * 3)


def sfx_crickets():
    t = np.arange(int(SR * 1.2)) / SR
    chirp = (np.sin(2 * np.pi * 4300 * t) * (np.sin(2 * np.pi * 9 * t) > 0.6)) * 0.12
    return chirp * np.minimum(1, (1.2 - t) * 3)


def sfx_typing():
    rng = np.random.default_rng(3)
    out = np.zeros(int(SR * 1.0))
    for k in range(14):
        i = int(k * SR * 0.065 + rng.integers(0, 600))
        n = 400
        out[i:i + n] += 0.35 * rng.standard_normal(n) * np.exp(-np.arange(n) / 60)
    return out


def sfx_sting():
    t = np.arange(int(SR * 0.6)) / SR
    return 0.5 * (np.sin(2 * np.pi * 82 * t) + 0.5 * np.sin(2 * np.pi * 164 * t)) * np.exp(-t * 5)


def sfx_spit():
    rng = np.random.default_rng(7)
    n = int(SR * 0.35)
    return 0.5 * rng.standard_normal(n) * np.exp(-np.arange(n) / (SR * 0.06))


def sfx_connect():
    return np.concatenate([_tone(660, 0.12, 0.35, 8), _tone(990, 0.35, 0.35, 5)])


def sfx_boing():
    t = np.arange(int(SR * 0.6)) / SR
    f = 180 + 120 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4)
    return 0.45 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)


def sfx_zip():
    t = np.arange(int(SR * 0.28)) / SR
    f = 400 + 2600 * (t / t[-1]) ** 2
    return 0.25 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, (0.28 - t) * 12)


def sfx_zip_out():
    t = np.arange(int(SR * 0.28)) / SR
    f = 2800 - 2400 * (t / t[-1]) ** 0.5
    return 0.25 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, (0.28 - t) * 12)


def sfx_poof():
    rng = np.random.default_rng(11)
    n = int(SR * 0.5)
    x = rng.standard_normal(n)
    x = np.convolve(x, np.ones(30) / 30, mode="same")
    t = np.arange(n) / SR
    return 1.6 * x * np.exp(-t * 7) * np.minimum(1, t * 80)


def sfx_slide_up():
    t = np.arange(int(SR * 0.55)) / SR
    f = 500 * 2 ** (2.2 * t / t[-1])
    return 0.28 * np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.3 * np.sin(2 * np.pi * 7 * t))


def sfx_slide_down():
    t = np.arange(int(SR * 0.7)) / SR
    f = 1400 * 2 ** (-2.4 * t / t[-1])
    return 0.28 * np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.3 * np.sin(2 * np.pi * 7 * t)) * np.minimum(1, (0.7 - t) * 8)


def sfx_twinkle():
    return np.concatenate([_tone(f, 0.09, 0.22, 10) for f in (1568, 2093, 2637, 3136)] + [_tone(4186, 0.4, 0.18, 6)])


def sfx_scratch():
    rng = np.random.default_rng(5)
    n = int(SR * 0.45)
    t = np.arange(n) / SR
    f = 300 + 900 * np.abs(np.sin(2 * np.pi * 3 * t))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    return 0.35 * (0.6 * tone + 0.4 * rng.standard_normal(n)) * np.exp(-t * 3)


def sfx_wind():
    rng = np.random.default_rng(8)
    n = int(SR * 2.0)
    x = np.convolve(rng.standard_normal(n), np.ones(80) / 80, mode="same")
    t = np.arange(n) / SR
    return 2.2 * x * np.sin(np.pi * t / 2.0) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.8 * t))


def sfx_bonk():
    t = np.arange(int(SR * 0.3)) / SR
    return 0.5 * np.sin(2 * np.pi * (220 * np.exp(-t * 6)) * t * 3) * np.exp(-t * 14)


def sfx_thunder():
    rng = np.random.default_rng(2)
    n = int(SR * 1.4)
    x = np.convolve(rng.standard_normal(n), np.ones(200) / 200, mode="same")
    t = np.arange(n) / SR
    return 4.0 * x * np.exp(-t * 2.5) * np.minimum(1, t * 30)


def sfx_gasp():
    rng = np.random.default_rng(4)
    n = int(SR * 0.5)
    x = np.convolve(rng.standard_normal(n), np.ones(12) / 12, mode="same")
    t = np.arange(n) / SR
    return 0.9 * x * np.sin(np.pi * t / 0.5) ** 2


def sfx_tada():
    return np.concatenate([_tone(784, 0.12, 0.3, 6), _tone(1047, 0.5, 0.35, 3)]) + 0


def _sfx_table():
    import sonido
    t = dict(sonido.SFX)
    t.update({"doorbell": sfx_doorbell, "error": sfx_error, "crickets": sfx_crickets, "typing": sfx_typing,
              "sting": sfx_sting, "spit": sfx_spit, "connect": sfx_connect, "boing": sfx_boing, "zip": sfx_zip,
              "zip_out": sfx_zip_out, "poof": sfx_poof, "slide_up": sfx_slide_up, "slide_down": sfx_slide_down,
              "twinkle": sfx_twinkle, "scratch": sfx_scratch, "wind": sfx_wind, "bonk": sfx_bonk,
              "thunder": sfx_thunder, "gasp": sfx_gasp, "tada": sfx_tada})
    return t


def mezcla_sfx(dur, eventos, path, extra=None):
    tab = _sfx_table()
    n = int(SR * dur)
    out = np.zeros(n)
    if extra is not None:
        out[:min(n, len(extra))] += extra[:n]
    for k, (t, name) in enumerate(eventos):
        if name not in tab:
            continue
        s = tab[name]() if name != "whoosh" else 0.5 * tab[name](seed=k)
        i = int(t * SR)
        if i >= n:
            continue
        m = min(len(s), n - i)
        out[i:i + m] += s[:m]
    out = np.clip(0.55 * out, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- subtítulos karaoke
FONT_SUB = "Lilita One"
SUB = {"y": 1330, "size": 92, "maxw": 860, "nombre": True}


def _silabas(wd):
    w = re.sub(r"[^a-z]", "", wd.lower())
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n) + (0.6 if re.search(r"[.!?,…]$", wd) else 0)


def _palabras(ln, fps):
    """Reparte las palabras del subtítulo sobre los fotogramas con voz de la línea (sílabas como peso)."""
    txt = ln.get("sub") or ln.get("texto") or ""
    words = txt.split()
    if not words:
        return []
    env = np.array(ln.get("env") or [0.5], dtype=float)
    voiced = (env > 0.12).astype(float)
    if voiced.sum() < 3:
        voiced[:] = 1
    cum = np.cumsum(voiced)
    total = cum[-1]
    pesos = np.array([_silabas(wd) for wd in words], dtype=float)
    lim = np.concatenate([[0], np.cumsum(pesos) / pesos.sum() * total])
    out = []
    for i, wd in enumerate(words):
        f0 = int(np.searchsorted(cum, lim[i] + 0.5))
        f1 = int(np.searchsorted(cum, lim[i + 1]))
        out.append({"w": wd, "t0": ln["ini"] + f0 / fps, "t1": ln["ini"] + max(f1, f0 + 1) / fps})
    return out


def _trozos(words, maxw_chars=16, maxn=3):
    """Agrupa palabras en trozos cortos (para niños): corta en puntuación o cada 3 palabras."""
    trozos, cur = [], []
    for wd in words:
        cur.append(wd)
        largo = sum(len(x["w"]) for x in cur) + len(cur) - 1
        if re.search(r"[.!?…]$", wd["w"]) or len(cur) >= maxn or largo >= maxw_chars:
            trozos.append(cur)
            cur = []
    if cur:
        trozos.append(cur)
    return trozos


def subtitulos(ctx, L, T, y=None):
    """Subtítulos grandes abajo; la palabra que suena salta y se pinta del color del personaje."""
    if _MUTE["impacto"]:
        return
    for li, ln in enumerate(L.lines):
        if ln.get("sub") == "-":
            continue
        nxt = L.lines[li + 1]["ini"] if li + 1 < len(L.lines) else 1e9
        if not (ln["ini"] - 0.1 <= T < min(ln["fin"] + 0.35, nxt)):
            continue
        trozos = L.trozos[li]
        if not trozos:
            return
        k = 0
        for j, tz in enumerate(trozos):
            if T >= tz[0]["t0"] - 0.06:
                k = j
        tz = trozos[k]
        col = PJ[ln["pj"]]["color"]
        grito = (ln.get("sub") or ln.get("texto") or "").isupper()
        size = SUB["size"] * (1.22 if grito else 1.0)
        ctx.save()
        ctx.select_font_face(FONT_SUB, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        txts = [wd["w"] for wd in tz]
        sp = size * 0.55
        while True:
            ctx.set_font_size(size)
            ws = [ctx.text_extents(t)[4] for t in txts]
            tot = sum(ws) + sp * (len(ws) - 1)
            if tot <= SUB["maxw"] or size < 40:
                break
            size *= 0.92
            sp = size * 0.55
        yy = SUB["y"] if y is None else y
        if grito:
            dx, dy = shake(T, 6)
        else:
            dx, dy = 0, 0
        appear = max(0.02, e_back(clamp((T - tz[0]["t0"] + 0.06) / 0.18)))
        x = W / 2 - tot / 2
        # etiqueta con el nombre de quien habla
        if SUB["nombre"]:
            nm = PJ[ln["pj"]]["nombre"]
            ctx.set_font_size(34)
            nw = ctx.text_extents(nm)[4] + 30
            ctx.save()
            ctx.translate(W / 2 - tot / 2 + nw / 2 - 6, yy - size * 0.95 + dy)
            ctx.rotate(-0.05)
            ctx.scale(appear, appear)
            rrect(ctx, -nw / 2, -26, nw, 50, 16)
            fill_keep(ctx, col)
            stroke(ctx, INK, 5)
            ctx.move_to(-nw / 2 + 15, 12)
            ctx.text_path(nm)
            ctx.set_source_rgb(*INK)
            ctx.fill()
            ctx.restore()
            ctx.set_font_size(size)
        for wd, wdt in zip(tz, ws):
            activa = wd["t0"] - 0.03 <= T < max(wd["t1"], wd["t0"] + 0.12)
            dicha = T >= wd["t0"] - 0.03
            p = clamp((T - wd["t0"] + 0.03) / 0.16)
            bump = (1 + 0.1 * math.sin(math.pi * p)) if activa else 1.0
            ctx.save()
            ctx.translate(x + wdt / 2 + dx, yy + dy)
            ctx.rotate(0.03 * math.sin(T * 5 + x * 0.01) if activa else 0)
            ctx.scale(appear * bump, appear * bump)
            ctx.move_to(-wdt / 2, size * 0.34)
            ctx.text_path(wd["w"])
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgba(*INK, 1)
            ctx.set_line_width(size * 0.24)
            ctx.stroke_preserve()
            ctx.set_source_rgba(*(col if activa else WHITE), 1 if dicha else 0.92)
            ctx.fill()
            ctx.restore()
            x += wdt + sp
        ctx.restore()
        return


# ---------------------------------------------------------------- transiciones entre escenas
# En escenas.py: TRANS = {indice_escena_que_entra: ("whip" | "estrella" | "iris" | "poof" | "flash" | "zoom", duracion)}
def _forma(ctx, tipo, p, cx, cy):
    R = 1500 * e_in(p) if tipo == "iris_out" else 1500 * e_out(p)
    if tipo == "estrella":
        estrella_path(ctx, cx, cy, R * 1.25, 5, -math.pi / 2 + p * 1.2)
    else:
        ctx.arc(cx, cy, max(1, R), 0, 2 * math.pi)


def _escena(ctx, escenas, k, T, L):
    t0, fn = escenas[k][0], escenas[k][1]
    t1 = escenas[k + 1][0] if k + 1 < len(escenas) else 1e9
    ctx.save()
    fn(ctx, T - t0, t1 - t0, T, L)
    ctx.restore()


def _transicion(ctx, escenas, k, T, L, tipo, d):
    t0 = escenas[k][0]
    p = clamp((T - t0) / d)
    if tipo == "whip":
        e = e_in(min(1, p * 2)) if p < 0.5 else 1
        if p < 0.5:
            ctx.save()
            ctx.translate(-W * 0.9 * e_in(p * 2), 0)
            _escena(ctx, escenas, k - 1, T, L)
            ctx.restore()
        else:
            ctx.save()
            ctx.translate(W * 0.9 * (1 - e_out((p - 0.5) * 2)), 0)
            _escena(ctx, escenas, k, T, L)
            ctx.restore()
        a = math.sin(math.pi * p)
        ctx.save()
        ctx.set_source_rgba(1, 1, 1, 0.25 * a)
        ctx.paint()
        lineas_velocidad(ctx, -200, -100, W + 400, H + 200, -1, T, 30, WHITE, 0.9 * a, 17)
        ctx.restore()
        return
    if tipo in ("estrella", "iris"):
        _escena(ctx, escenas, k - 1, T, L)
        ctx.push_group()
        _escena(ctx, escenas, k, T, L)
        pat = ctx.pop_group()
        cx, cy = escenas[k][2].get("centro", (W / 2, H * 0.45)) if len(escenas[k]) > 2 else (W / 2, H * 0.45)
        ctx.save()
        _forma(ctx, tipo, p, cx, cy)
        ctx.clip_preserve()
        ctx.set_source(pat)
        ctx.paint()
        ctx.restore()
        ctx.save()
        _forma(ctx, tipo, p, cx, cy)
        stroke(ctx, INK, 26 * (1 - p) + 4)
        ctx.restore()
        return
    if tipo == "poof":
        _escena(ctx, escenas, k - 1 if p < 0.45 else k, T, L)
        nube_poof(ctx, W / 2, H * 0.45, 900, 0.15 + p * 0.8, seed=21)
        return
    if tipo == "zoom":
        ctx.save()
        z = 1 + 2.5 * e_in(p) if p < 0.5 else 1
        if p < 0.5:
            camera(ctx, z, W / 2, H * 0.45)
            _escena(ctx, escenas, k - 1, T, L)
        else:
            _escena(ctx, escenas, k, T, L)
        ctx.restore()
        flash(ctx, 0.9 * math.sin(math.pi * p))
        return
    # flash por defecto
    _escena(ctx, escenas, k, T, L)
    flash(ctx, 1 - p)


def iris_final(ctx, T, dur, cx, cy, d=0.6):
    """Cierre en círculo negro (estilo cartoon) sobre (cx, cy) en coordenadas de pantalla."""
    p = clamp((T - (dur - d)) / d)
    if p <= 0:
        return
    r = max(0.0, 1500 * (1 - e_in(p)))
    ctx.save()
    ctx.rectangle(-10, -10, W + 20, H + 20)
    ctx.arc_negative(cx, cy, r, 2 * math.pi, 0)
    fill(ctx, INK)
    ctx.restore()


# ---------------------------------------------------------------- música de fondo (sintetizada, propia)
def musica(dur, tramos, lineas, bpm=118):
    """Cancioncilla alegre de pizzicato + bajo + platillo suave. tramos = [(t0, t1, "alegre"|"tension"|"triste")].
    Baja 9 dB mientras alguien habla."""
    n = int(SR * dur)
    out = np.zeros(n)
    beat = 60 / bpm
    prog = {"alegre": [(60, 64, 67), (57, 60, 64), (65, 69, 72), (67, 71, 74)],
            "tension": [(57, 60, 64), (56, 60, 63), (57, 60, 64), (59, 62, 65)],
            "triste": [(57, 60, 64), (53, 57, 60), (55, 59, 62), (52, 55, 59)]}

    def nota(midi, d, a, dec):
        f = 440 * 2 ** ((midi - 69) / 12)
        t = np.arange(int(SR * d)) / SR
        return a * (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t)) * np.exp(-t * dec)

    for (a0, a1, tipo) in tramos:
        ch = prog.get(tipo, prog["alegre"])
        t = a0
        i = 0
        while t < min(a1, dur):
            acorde = ch[(i // 8) % len(ch)]
            m = acorde[[0, 1, 2, 1][i % 4]] + (12 if i % 8 >= 4 else 0)
            s = nota(m, beat * 0.9, 0.09 if tipo != "triste" else 0.07, 9 if tipo != "triste" else 4)
            if i % 4 == 0:
                s = s + nota(acorde[0] - 24, beat * 1.8, 0.16, 3)[:len(s)] if len(s) else s
            j = int(t * SR)
            m_ = min(len(s), n - j, int((a1 - t) * SR))
            if m_ > 0:
                out[j:j + m_] += s[:m_]
            t += beat / 2
            i += 1
    # duck bajo la voz
    g = np.ones(n)
    for ln in lineas:
        j0, j1 = int((ln["ini"] - 0.05) * SR), int((ln["fin"] + 0.1) * SR)
        g[max(0, j0):max(0, min(n, j1))] = 0.35
    g = np.convolve(g, np.ones(2205) / 2205, mode="same")
    return out * g


# ---------------------------------------------------------------- render
def _t(spec, tl):
    """Tiempo absoluto: número, o "L6" / "L6-0.3" / "L6+0.2" (inicio de la línea 6 del diálogo, contando desde 1),
    o "F6" (final de la línea 6)."""
    if isinstance(spec, (int, float)):
        return float(spec)
    m = re.match(r"([LF])(\d+)\s*([+-]\s*[\d.]+)?$", spec.strip())
    if not m:
        raise ValueError(f"tiempo no válido: {spec}")
    ln = tl["lineas"][int(m.group(2)) - 1]
    base = ln["ini"] if m.group(1) == "L" else ln["fin"]
    return base + (float(m.group(3).replace(" ", "")) if m.group(3) else 0.0)


def _load(workdir):
    spec = importlib.util.spec_from_file_location("escenas", os.path.join(workdir, "escenas.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sitcom"] = sys.modules[__name__]
    spec.loader.exec_module(mod)
    tl = json.load(open(os.path.join(workdir, "timeline.json")))
    escenas = []
    for e in mod.ESCENAS:
        escenas.append((_t(e[0], tl), e[1]) + tuple(e[2:]))
    escenas.sort(key=lambda e: e[0])
    mod._ESC = escenas
    mod._SFX = [(_t(t, tl), nm) for t, nm in getattr(mod, "SFX", [])]
    mod._MUSICA = [(_t(a, tl), _t(b, tl), tipo) for a, b, tipo in getattr(mod, "MUSICA", [])]
    return mod, tl


def _frame(ctx, mod, escenas, L, T, dur):
    k = max([j for j, e in enumerate(escenas) if e[0] <= T] or [0])
    tr = getattr(mod, "TRANS", {}).get(k)
    if tr and k > 0 and T - escenas[k][0] < tr[1]:
        _transicion(ctx, escenas, k, T, L, tr[0], tr[1])
    else:
        _escena(ctx, escenas, k, T, L)
    if getattr(mod, "SUBTITULOS", True):
        subtitulos(ctx, L, T, getattr(mod, "SUB_Y", None))
    elif getattr(mod, "ROTULOS", True):
        ln = L.line(T)
        if ln and ln.get("rotulo", True) and ln.get("texto"):
            rotulo(ctx, ln.get("rotulo_texto") or ln["texto"], ln["pj"], pop(T - ln["ini"], 0, 0.2))
    fin = getattr(mod, "FINAL", None)
    if fin:
        iris_final(ctx, T, dur, fin[0], fin[1], fin[2] if len(fin) > 2 else 0.6)


def render(workdir):
    mod, tl = _load(workdir)
    L = Dialogo(tl)
    dur = tl["dur"] + float(getattr(mod, "COLA", 0.4))
    nframes = int(dur * FPS)
    escenas = mod._ESC
    fx = os.path.join(workdir, "fx.wav")
    mus = musica(dur, mod._MUSICA, tl["lineas"]) if mod._MUSICA else None
    mezcla_sfx(dur, mod._SFX, fx, mus)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, OUT_W, OUT_H)
    out = os.path.join(workdir, "short.tmp.mp4")
    voz = os.path.join(workdir, "dialogo.wav")
    filt = ("[1:a]highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
            "loudnorm=I=-14:TP=-1.5:LRA=9,apad[v];[2:a]aformat=sample_rates=44100:channel_layouts=mono[f];"
            "[v][f]amix=inputs=2:duration=first:normalize=0[a]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{OUT_W}x{OUT_H}",
           "-r", str(FPS), "-i", "-", "-i", voz, "-i", fx, "-filter_complex", filt, "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", "16", "-profile:v", "high",
           "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{nframes / FPS:.3f}", "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(nframes):
        T = i / FPS
        ctx = cairo.Context(surf)
        ctx.set_antialias(cairo.ANTIALIAS_GOOD)
        ctx.scale(SCALE, SCALE)
        _frame(ctx, mod, escenas, L, T, dur)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit("ffmpeg falló")
    os.replace(out, os.path.join(workdir, "short.mp4"))
    print("ok", workdir, f"{dur:.1f}s")


def frame_png(workdir, T, path, w=W, h=H):
    mod, tl = _load(workdir)
    L = Dialogo(tl)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    ctx.scale(w / W, h / H)
    _frame(ctx, mod, mod._ESC, L, T, tl["dur"] + float(getattr(mod, "COLA", 0.4)))
    surf.write_to_png(path)
    return path


def hoja(workdir, times, path, cols=8, tw=270):
    """Hoja de contactos: varios instantes en una sola imagen para revisar."""
    from PIL import Image
    mod, tl = _load(workdir)
    L = Dialogo(tl)
    th = int(tw * H / W)
    rows = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (0, 0, 0))
    for i, T in enumerate(times):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, tw * 2, th * 2)
        ctx = cairo.Context(surf)
        ctx.scale(tw * 2 / W, th * 2 / H)
        _frame(ctx, mod, mod._ESC, L, T, tl["dur"] + float(getattr(mod, "COLA", 0.4)))
        im = Image.frombuffer("RGBA", (tw * 2, th * 2), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB")
        sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(path)
    return path


def preview(workdir, times):
    return [frame_png(workdir, T, os.path.join(workdir, f"prev_{T:.1f}.png")) for T in times]


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        print(preview(sys.argv[1], [float(x) for x in sys.argv[3:]]))
    elif len(sys.argv) > 3 and sys.argv[2] == "hoja":
        print(hoja(sys.argv[1], [float(x) for x in sys.argv[4:]], sys.argv[3]))
    else:
        render(sys.argv[1])
