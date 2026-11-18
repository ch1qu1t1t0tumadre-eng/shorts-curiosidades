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


# ---------------------------------------------------------------- personajes (marionetas)
# Los personajes son los DIBUJOS OFICIALES del reparto (variante 2 del lineup "Sitcom – Personajes",
# referencias/reparto_v2.png), recortados por pipeline/recortar_reparto.py en assets/personajes/*.png.
# No se redibujan: se animan encima como en los dibujos animados. El dibujo se trocea en franjas
# horizontales y cada franja se desplaza/estira, así el personaje se dobla, se estira y se aplasta
# (squash & stretch), cabecea al hablar y se balancea, sin perder el trazo original.
_PUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "personajes")
_PUP_WORLD = 0.29  # unidades del lienzo (1080x1920) por píxel del recorte (x4)
# Puntos en píxeles del recorte: ojos (x, y, radio), boca (x, y, ancho), mano, pantalla, cabeza, cuello (y), mejillas.
PUP = {
    "teddy": {"eyes": [(836, 340, 78), (1012, 300, 78)], "mouth": (976, 520, 150), "cover": False,
              "hand": (1704, 948), "head": (930, 330), "neck": 720, "cheeks": [(790, 470), (1100, 430)]},
    "moe": {"eyes": [(496, 476, 60), (708, 476, 60)], "mouth": (612, 632, 250), "cover": True,
            "hand": (612, 900), "head": (600, 470), "neck": 700, "cheeks": [(450, 590), (760, 590)]},
    "nana": {"eyes": [(228, 508, 46), (484, 516, 46)], "mouth": (412, 676, 120), "cover": True,
             "hand": (130, 990), "screen": (128, 990, -0.38), "head": (360, 520), "neck": 840,
             "cheeks": [(250, 610), (500, 620)]},
    "mia": {"eyes": [(192, 708, 52), (440, 716, 52)], "mouth": (380, 824, 190), "cover": True,
            "hand": (560, 1440), "head": (330, 700), "neck": 950, "cheeks": [(200, 810), (470, 820)]},
}
_pup_cache = {}
_STRIPS = 34


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
            px, py = int(px), int(py)
            b, g, r, a = data[py, px]
            return (r / 255, g / 255, b / 255)
        ex, ey, er = meta["eyes"][0]
        meta["lid"] = sample(ex, ey - er * 1.35)
        mx, my, mw = meta["mouth"]
        meta["skin"] = sample(mx - mw * 0.75, my - mw * 0.05)
        # versión a media resolución para planos generales (más rápida y más suave al reducir)
        half = cairo.ImageSurface(cairo.FORMAT_ARGB32, w // 2 + 1, h // 2 + 1)
        c2 = cairo.Context(half)
        c2.scale(0.5, 0.5)
        c2.set_source_surface(surf, 0, 0)
        c2.get_source().set_filter(cairo.FILTER_BEST)
        c2.paint()
        _pup_cache[name] = (surf, half, w, h, foot_x, bottom, meta)
    return _pup_cache[name]


def _sstep(a, b, v):
    p = clamp((v - a) / (b - a))
    return p * p * (3 - 2 * p)


def puppet(ctx, name, x, y, s=1.0, T=0.0, mood="normal", talk=0.0, look=(0, 0), flip=False, bounce=0.0, phone_prop=False,
           screen_text=None, rot=0.0, sq=1.0, lean=0.0, dx=0.0, dy=0.0, head_dy=0.0, nod=0.0, smear=0.0, tint=None,
           blush=0.0, alpha=1.0, spin=0.0, shadow=True, sway=1.0, lid=None):
    """Dibuja a un personaje oficial con los pies en (x, y).

    s escala · sq estirar(>1)/aplastar(<1) · lean doblarse (+ derecha) · dx, dy desplazamiento (dy<0 arriba)
    head_dy subir la cabeza (px del recorte, <0 arriba) · nod cabeceo lateral · smear velocidad horizontal
    (deja estela) · tint (r, g, b, a) colorea el dibujo · blush 0..1 colorete · spin giro · lid 0..1 párpados.
    Devuelve {"head": (x, y), "top": (x, y), "feet": (x, y)} en coordenadas del mundo para colgar efectos.
    """
    surf, half, w, h, fx, fb, meta = _pup(name)
    k = _PUP_WORLD * s
    seed = len(name) * 1.7
    tl = clamp(talk)
    # --- movimiento automático: respiración, balanceo, hablar, ánimo
    sq_t = sq * (1 + 0.014 * math.sin(T * 2.6 + seed))
    lean_t = lean + sway * 0.016 * math.sin(T * 1.7 + seed)
    hd = head_dy - tl * 34 * (0.6 + 0.4 * math.sin(T * 17 + seed))
    nod_t = nod + tl * 0.012 * math.sin(T * 9 + seed)
    jx, jy = 0.0, 0.0
    hop = -abs(math.sin(T * 7)) * 18 * s * bounce
    if mood == "panico":
        jx = 4 * s * math.sin(T * 47)
        lean_t += 0.02 * math.sin(T * 31)
    elif mood == "sorpresa":
        hop -= 14 * s * abs(math.sin(T * 10))
        sq_t *= 1.04
    elif mood == "enfado":
        jx = 5 * s * math.sin(T * 61)
        hd -= 10
    elif mood == "feliz":
        hop -= abs(math.sin(T * 6)) * 12 * s
        lean_t += 0.025 * math.sin(T * 6)
    elif mood == "smug":
        lean_t -= 0.02
        hd -= 8
    elif mood in ("cansado", "triste"):
        sq_t *= 0.95
        lean_t += 0.03
        hd += 30
    hd = max(-90, min(90, hd))
    neck = meta["neck"]

    def headw(v):  # 1 en la cabeza, 0 en el cuerpo
        return 1 - _sstep(neck - 90, neck + 70, v)

    def wdx(v):
        return lean_t * ((1 - v / fb) ** 2) * fb + nod_t * fb * headw(v)

    def wy(v):
        return v + hd * headw(v)

    def wp(px, py):
        return px + wdx(py), wy(py)

    ctx.save()
    ctx.translate(x + dx, y)
    if shadow:
        lift = clamp(-(dy + hop) / 300)
        soft_shadow(ctx, 0, 0, w * k * 0.38 * (1 - 0.4 * lift), 22 * s * (1 - 0.4 * lift), 0.28 * (1 - 0.5 * lift) * alpha)
    ctx.translate(jx, dy + hop + jy)
    ctx.rotate(rot + spin)
    sgn = -1 if flip else 1
    ctx.scale(k * sgn / (sq_t ** 0.6), k * sq_t)
    ctx.translate(-fx, -fb)
    # nivel de detalle según el tamaño en pantalla
    m = ctx.get_matrix()
    dev = math.sqrt(abs(m.xx * m.yy - m.xy * m.yx))
    src, sc = (half, 2.0) if dev < 0.45 else (surf, 1.0)
    # estela (smear) para movimientos rápidos
    if abs(smear) > 1:
        for i in range(1, 5):
            ctx.save()
            ctx.translate(-smear * i * 0.55 / k * sgn, 0)
            ctx.scale(sc, sc)
            ctx.set_source_surface(src, 0, 0)
            ctx.paint_with_alpha(alpha * 0.22 * (1 - i / 5))
            ctx.restore()
    # el dibujo, en franjas deformadas
    n = _STRIPS
    for i in range(n):
        y0, y1 = fb * i / n, fb * (i + 1) / n
        Y0, Y1 = wy(y0), wy(y1)
        d0, d1 = wdx(y0), wdx(y1)
        shear = (d1 - d0) / (y1 - y0)
        syy = (Y1 - Y0) / (y1 - y0)
        ctx.save()
        ctx.transform(cairo.Matrix(1, 0, shear, syy, d0 - shear * y0, Y0 - syy * y0))
        ctx.rectangle(-4, y0 - 0.7, w + 8, (y1 - y0) + 1.4)
        ctx.clip()
        ctx.scale(sc, sc)
        ctx.set_source_surface(src, 0, 0)
        ctx.get_source().set_filter(cairo.FILTER_GOOD)
        if alpha >= 0.999:
            ctx.paint()
        else:
            ctx.paint_with_alpha(alpha)
        if tint:
            ctx.set_source_rgba(*tint)
            ctx.mask_surface(src, 0, 0)
        ctx.restore()
    # --- colorete
    if blush > 0.01:
        for cx, cy in meta["cheeks"]:
            px, py = wp(cx, cy)
            g = cairo.RadialGradient(px, py, 0, px, py, 70)
            g.add_color_stop_rgba(0, 1, 0.35, 0.5, 0.75 * blush)
            g.add_color_stop_rgba(1, 1, 0.35, 0.5, 0)
            ctx.set_source(g)
            ellipse(ctx, px, py, 80, 50)
            ctx.fill()
    # --- párpados (parpadeo; medio cerrados con sospecha / cansado)
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
            ex, ey = wp(ex, ey)
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
    # --- boca que habla
    mx, my, mw = meta["mouth"]
    mx, my = wp(mx, my)
    if tl > 0.06:
        if meta["cover"]:
            ellipse(ctx, mx, my, mw * 0.62, mw * 0.24)
            ctx.set_source_rgb(*meta["skin"])
            ctx.fill()
        hgt = mw * (0.12 + 0.42 * tl)
        ctx.move_to(mx - mw / 2, my)
        ctx.curve_to(mx - mw / 2, my + hgt * 1.35, mx + mw / 2, my + hgt * 1.35, mx + mw / 2, my)
        ctx.curve_to(mx + mw / 4, my - hgt * 0.2, mx - mw / 4, my - hgt * 0.2, mx - mw / 2, my)
        ctx.close_path()
        ctx.set_source_rgb(0.33, 0.07, 0.12)
        ctx.fill_preserve()
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(mw * 0.06)
        ctx.stroke()
        ellipse(ctx, mx, my + hgt * 0.9, mw * 0.2, hgt * 0.3)
        ctx.set_source_rgb(0.93, 0.45, 0.52)
        ctx.fill()
    # --- móvil en la mano (Teddy / Mia) y texto en la pantalla del móvil de Nana
    if phone_prop and name != "nana":
        hx, hy = meta["hand"]
        hx, hy = wp(hx, hy - (0 if name == "mia" else 120))
        phone(ctx, hx, hy, 3.2, 0.12, glow=0.5 + 0.5 * math.sin(T * 5))
    if screen_text and "screen" in meta:
        sx, sy, sr = meta["screen"]
        sx, sy = wp(sx, sy)
        ctx.save()
        ctx.translate(sx, sy)
        ctx.rotate(sr)
        sz = 60
        while sz > 18 and text_width(ctx, screen_text, sz) > 150:
            sz -= 2
        text(ctx, screen_text, 0, 0, sz, INK, shadow=False)
        ctx.restore()
    # posiciones útiles en el mundo
    pts = {}
    for key, (px, py) in (("head", meta["head"]), ("top", meta["top"]), ("feet", (fx, fb))):
        pts[key] = ctx.user_to_device(*wp(px, py))
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
    return puppet(ctx, "nana", x, y, s, T, mood, talk, look, flip, 0.0, screen_text=screen_text,
                  rot=kw.pop("rot", 0.012 * math.sin(T * 30) if typing else 0.0), **kw)


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
        sp = size * 0.34
        while True:
            ctx.set_font_size(size)
            ws = [ctx.text_extents(t)[4] for t in txts]
            tot = sum(ws) + sp * (len(ws) - 1)
            if tot <= SUB["maxw"] or size < 40:
                break
            size *= 0.92
            sp = size * 0.34
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
