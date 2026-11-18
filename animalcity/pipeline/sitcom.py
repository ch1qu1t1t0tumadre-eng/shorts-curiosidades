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
import importlib.util, json, math, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
from anim import *  # noqa: F401,F403  (W, H, FPS, OUT_W, OUT_H, SCALE, primitivas, cairo...)
import anim as _anim
import cairocffi as cairo

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
# No se redibujan: se animan encima (respiración, rebote, temblor, parpadeo, boca con la voz, gestos).
_PUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "personajes")
_PUP_WORLD = 0.29  # unidades del lienzo (1080x1920) por píxel del recorte (x4)
# Puntos de la cara en píxeles del recorte: ojos (x, y, radio), boca (x, y, ancho), mano para el móvil, pantalla.
PUP = {
    "teddy": {"eyes": [(836, 340, 78), (1012, 300, 78)], "mouth": (976, 520, 150), "cover": False,
              "hand": (1704, 948), "head": (930, 330)},
    "moe": {"eyes": [(496, 476, 60), (708, 476, 60)], "mouth": (612, 632, 250), "cover": True,
            "hand": (612, 900), "head": (600, 470)},
    "nana": {"eyes": [(228, 508, 46), (484, 516, 46)], "mouth": (412, 676, 120), "cover": True,
             "hand": (130, 990), "screen": (128, 990, -0.38), "head": (360, 520)},
    "mia": {"eyes": [(192, 708, 52), (440, 716, 52)], "mouth": (380, 824, 190), "cover": True,
            "hand": (560, 1440), "head": (330, 700)},
}
_pup_cache = {}


def _pup(name):
    if name not in _pup_cache:
        surf = cairo.ImageSurface.create_from_png(os.path.join(_PUP_DIR, f"{name}.png"))
        w, h = surf.get_width(), surf.get_height()
        data = np.frombuffer(surf.get_data(), np.uint8).reshape(h, surf.get_stride() // 4, 4)[:, :w]
        alpha = data[..., 3]
        rows = np.where(alpha.max(1) > 200)[0]
        bottom = rows[-1]
        cols = np.where(alpha[max(0, bottom - 120):bottom + 1].max(0) > 200)[0]
        foot_x = (cols[0] + cols[-1]) / 2
        meta = dict(PUP[name])
        # colores de piel/pelo para párpados y para tapar la boca (muestreados del propio dibujo)
        def sample(px, py):
            px, py = int(px), int(py)
            b, g, r, a = data[py, px]
            return (r / 255, g / 255, b / 255)
        ex, ey, er = meta["eyes"][0]
        meta["lid"] = sample(ex, ey - er * 1.35)
        mx, my, mw = meta["mouth"]
        meta["skin"] = sample(mx - mw * 0.75, my - mw * 0.05)
        _pup_cache[name] = (surf, w, h, foot_x, bottom, meta)
    return _pup_cache[name]


def puppet(ctx, name, x, y, s=1.0, T=0.0, mood="normal", talk=0.0, look=(0, 0), flip=False, bounce=0.0, phone_prop=False,
           screen_text=None, rot=0.0):
    """Dibuja a un personaje oficial con los pies en (x, y). s = escala (1 = tamaño estándar)."""
    surf, w, h, fx, fb, meta = _pup(name)
    k = _PUP_WORLD * s
    ctx.save()
    ctx.translate(x, y)
    soft_shadow(ctx, 0, 0, w * k * 0.38, 22 * s, 0.28)
    # movimiento de cuerpo: respiración, rebote, temblor, salto de sorpresa, inclinación al hablar
    breath = 1 + 0.012 * math.sin(T * 2.6 + len(name))
    hop = -abs(math.sin(T * 7)) * 18 * s * bounce
    if mood == "sorpresa":
        hop -= 14 * s * abs(math.sin(T * 10))
    jit = (3 * s * math.sin(T * 45), 0) if mood in ("panico",) else (0, 0)
    tl = clamp(talk)
    ctx.translate(jit[0], hop)
    ctx.rotate(rot + 0.025 * math.sin(T * 1.9 + len(name)) + 0.03 * tl * math.sin(T * 13))
    ctx.scale(k * (-1 if flip else 1) * (1 - 0.01 * tl), k * breath * (1 + 0.02 * tl))
    ctx.translate(-fx, -fb)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint()
    # --- párpados (parpadeo; medio cerrados con sospecha / cansado)
    ph = (T + len(name) * 0.71) % 3.8
    lid = 1.0 if ph < 0.11 else 0.0
    if mood in ("sospecha", "cansado") and name in ("teddy", "moe"):
        lid = max(lid, 0.5)
    if mood == "dormido":
        lid = 1.0
    if lid > 0:
        for ex, ey, er in meta["eyes"]:
            ctx.save()
            ellipse(ctx, ex, ey, er * 1.12, er * 1.12)
            ctx.clip()
            ctx.rectangle(ex - er * 1.3, ey - er * 1.25, er * 2.6, er * 2.5 * lid)
            ctx.set_source_rgb(*meta["lid"])
            ctx.fill()
            ctx.move_to(ex - er * 1.05, ey - er * 1.2 + er * 2.4 * lid)
            ctx.line_to(ex + er * 1.05, ey - er * 1.2 + er * 2.4 * lid)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(er * 0.16)
            ctx.stroke()
            ctx.restore()
    # --- boca que habla
    mx, my, mw = meta["mouth"]
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
        phone(ctx, hx, hy - (0 if name == "mia" else 120), 3.2, 0.12, glow=0.5 + 0.5 * math.sin(T * 5))
    if screen_text and "screen" in meta:
        sx, sy, sr = meta["screen"]
        ctx.save()
        ctx.translate(sx, sy)
        ctx.rotate(sr)
        sz = 60
        while sz > 18 and text_width(ctx, screen_text, sz) > 150:
            sz -= 2
        text(ctx, screen_text, 0, 0, sz, INK, shadow=False)
        ctx.restore()
    hx, hy = meta["head"]
    ctx.restore()
    # --- gestos encima (en coordenadas del mundo, junto a la cabeza)
    sgn = -1 if flip else 1
    head_x = x + (hx - fx) * k * sgn
    head_y = y + hop + (hy - fb) * k
    if mood == "panico":
        _sweat(ctx, head_x + 120 * s * sgn, head_y - 60 * s, T)
    if mood == "enfado":
        _anger(ctx, head_x + 120 * s * sgn, head_y - 110 * s, 40 * s, T)
    if mood == "sorpresa":
        _shock_lines(ctx, head_x, head_y - 30 * s, 190 * s, T)


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


# Envoltorios con la misma firma que usan los escenas.py
def teddy(ctx, x, y, s=1.0, T=0.0, mood="normal", talk=0.0, look=(0, 0), arms="abajo", prop=None, bounce=True, flip=False):
    puppet(ctx, "teddy", x, y, s, T, mood, talk, look, flip, 1.0 if bounce else 0.0, phone_prop=(arms == "movil"),
           rot=(-0.06 if arms == "arriba" else 0.0))


def moe(ctx, x, y, s=1.0, T=0.0, mood="normal", talk=0.0, look=(0, 0), arms="taza", prop=None, bounce=False, flip=False):
    puppet(ctx, "moe", x, y, s, T, mood, talk, look, flip, 0.4 if bounce else 0.0)


def nana(ctx, x, y, s=1.0, T=0.0, mood="smug", talk=0.0, look=(0, 0), gafas=None, prop="movil", screen_text=None, typing=False,
         flip=False):
    puppet(ctx, "nana", x, y, s, T, mood, talk, look, flip, 0.0, screen_text=screen_text,
           rot=(0.012 * math.sin(T * 30) if typing else 0.0))


def mia(ctx, x, y, s=1.0, T=0.0, mood="smug", talk=0.0, look=(0, 0), arms="cruzados", prop=None, bounce=False, flip=False):
    puppet(ctx, "mia", x, y, s, T, mood, talk, look, flip, 0.3 if bounce else 0.0, phone_prop=(arms == "movil"))


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


def _sfx_table():
    import sonido
    t = dict(sonido.SFX)
    t.update({"doorbell": sfx_doorbell, "error": sfx_error, "crickets": sfx_crickets, "typing": sfx_typing,
              "sting": sfx_sting, "spit": sfx_spit, "connect": sfx_connect})
    return t


def mezcla_sfx(dur, eventos, path):
    tab = _sfx_table()
    n = int(SR * dur)
    out = np.zeros(n)
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


# ---------------------------------------------------------------- render
def _load(workdir):
    spec = importlib.util.spec_from_file_location("escenas", os.path.join(workdir, "escenas.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sitcom"] = sys.modules[__name__]
    spec.loader.exec_module(mod)
    tl = json.load(open(os.path.join(workdir, "timeline.json")))
    return mod, tl


def _frame(ctx, mod, escenas, L, T, dur):
    k = max([j for j, e in enumerate(escenas) if e[0] <= T] or [0])
    t0, fn = escenas[k][0], escenas[k][1]
    t1 = escenas[k + 1][0] if k + 1 < len(escenas) else dur
    ctx.save()
    fn(ctx, T - t0, t1 - t0, T, L)
    ctx.restore()
    if getattr(mod, "ROTULOS", True):
        ln = L.line(T)
        if ln and ln.get("rotulo", True) and ln.get("texto"):
            rotulo(ctx, ln.get("rotulo_texto") or ln["texto"], ln["pj"], pop(T - ln["ini"], 0, 0.2))


def render(workdir):
    mod, tl = _load(workdir)
    L = Dialogo(tl)
    dur = tl["dur"] + float(getattr(mod, "COLA", 0.4))
    nframes = int(dur * FPS)
    escenas = sorted(mod.ESCENAS, key=lambda e: e[0])
    fx = os.path.join(workdir, "fx.wav")
    mezcla_sfx(dur, list(getattr(mod, "SFX", [])), fx)
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
    escenas = sorted(mod.ESCENAS, key=lambda e: e[0])
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    ctx.scale(w / W, h / H)
    _frame(ctx, mod, escenas, L, T, tl["dur"] + 0.4)
    surf.write_to_png(path)
    return path


def preview(workdir, times):
    return [frame_png(workdir, T, os.path.join(workdir, f"prev_{T:.1f}.png")) for T in times]


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        print(preview(sys.argv[1], [float(x) for x in sys.argv[3:]]))
    else:
        render(sys.argv[1])
