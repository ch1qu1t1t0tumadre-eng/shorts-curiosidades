#!/usr/bin/env python3
"""Motor de animación 2D estilo "explainer" (vectorial, con cairo).

Cada vídeo tiene un archivo work/vNN/escenas.py que define:
    ESCENAS = [ (t_inicio, funcion_dibujo), ... ]
donde funcion_dibujo(ctx, lt, dur, T) dibuja la escena en el lienzo 1080x1920
(lt = segundos desde el inicio de la escena, dur = duración de la escena, T = tiempo global).
Las funciones de este módulo son las piezas: fondos, personaje, etiquetas, relojes,
gráficas, iconos (OpenMoji), flechas, cámara...

Uso: python3 anim.py work/vNN      -> short.mp4 + thumb.jpg
"""
import importlib.util, json, math, os, subprocess, sys
from functools import lru_cache
import cairocffi as cairo
import cairosvg
import numpy as np

W, H, FPS = 1080, 1920, 60
# Salida en 1440x2560 (2K): YouTube da más calidad (VP9) a los vídeos de más de 1080p.
# Se dibuja con coordenadas de 1080x1920 y se escala (es vectorial, no pierde nitidez).
OUT_W, OUT_H = 1440, 2560
SCALE = OUT_W / W
HERE = os.path.dirname(os.path.abspath(__file__))
EMOJI_DIR = os.path.join(HERE, "assets/package/color/svg")
FONT = "Inter"            # instalada en el sistema
FONT_TITLE = "Anton"      # se registra desde assets si existe
FONT_CAPTION = "Bangers"  # subtítulo gigante estilo "curiosidades virales" (pipeline/fonts, licencia OFL)


def _registrar_fuentes():
    """Copia las fuentes de pipeline/fonts al directorio de fuentes del usuario para que cairo las vea."""
    src = os.path.join(HERE, "fonts")
    dst = os.path.expanduser("~/.local/share/fonts")
    if not os.path.isdir(src):
        return
    os.makedirs(dst, exist_ok=True)
    nuevas = False
    for f in os.listdir(src):
        if not os.path.exists(os.path.join(dst, f)):
            import shutil
            shutil.copy(os.path.join(src, f), dst)
            nuevas = True
    if nuevas:
        subprocess.run(["fc-cache", "-f", dst], check=False)


_registrar_fuentes()

# ---------- paleta ----------
NAVY = (0.07, 0.09, 0.20)
NAVY2 = (0.11, 0.14, 0.29)
NAVY3 = (0.17, 0.21, 0.40)
PURPLE = (0.30, 0.25, 0.45)
YELLOW = (1.0, 0.80, 0.18)
RED = (0.95, 0.22, 0.20)
WHITE = (1, 1, 1)
SKIN = (0.96, 0.78, 0.63)
SKIN_D = (0.88, 0.64, 0.50)
HAIR = (0.33, 0.22, 0.14)
BLUE = (0.36, 0.43, 0.84)
GREEN = (0.30, 0.85, 0.55)


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ---------- easing / tiempo ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):  # ease in-out cubic
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def pop(lt, start=0.0, d=0.35):
    """0..1 con rebote, para que algo aparezca."""
    return ease_back((lt - start) / d)


def lerp(a, b, x):
    return a + (b - a) * x


def keyframes(lt, kfs):
    """kfs = [(t, valor), ...]; interpola con ease. valor puede ser número o tupla."""
    if lt <= kfs[0][0]:
        return kfs[0][1]
    for (t0, v0), (t1, v1) in zip(kfs, kfs[1:]):
        if lt <= t1:
            x = ease((lt - t0) / max(t1 - t0, 1e-6))
            if isinstance(v0, tuple):
                return tuple(lerp(a, b, x) for a, b in zip(v0, v1))
            return lerp(v0, v1, x)
    return kfs[-1][1]


# ---------- cámara ----------
def camera(ctx, zoom=1.0, cx=W / 2, cy=H / 2, rot=0.0):
    """Coloca la cámara: el punto (cx, cy) del mundo queda en el centro de la pantalla."""
    ctx.translate(W / 2, H / 2)
    if rot:
        ctx.rotate(rot)
    ctx.scale(zoom, zoom)
    ctx.translate(-cx, -cy)


def shake(T, amp=6):
    return amp * math.sin(T * 47), amp * math.cos(T * 39)


# ---------- primitivas ----------
def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def fill(ctx, rgb, a=1.0):
    ctx.set_source_rgba(*rgb, a)
    ctx.fill()


def fill_keep(ctx, rgb, a=1.0):
    ctx.set_source_rgba(*rgb, a)
    ctx.fill_preserve()


def stroke(ctx, rgb, w=4, a=1.0):
    ctx.set_source_rgba(*rgb, a)
    ctx.set_line_width(w)
    ctx.stroke()


def circle(ctx, x, y, r):
    ctx.new_sub_path()
    ctx.arc(x, y, r, 0, 2 * math.pi)


def ellipse(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def vgrad(ctx, x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for off, rgb, *a in stops:
        g.add_color_stop_rgba(off, *rgb, a[0] if a else 1)
    return g


def soft_shadow(ctx, x, y, rx, ry, a=0.25):
    g = cairo.RadialGradient(x, y, 0, x, y, rx)
    g.add_color_stop_rgba(0, 0, 0, 0, a)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(1, ry / rx)
    ctx.translate(-x, -y)
    ctx.set_source(g)
    circle(ctx, x, y, rx)
    ctx.fill()
    ctx.restore()


def text(ctx, s, x, y, size=60, rgb=WHITE, a=1.0, font=FONT, bold=True, align="center", shadow=True):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    w = ext[4]
    tx = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    ty = y + size * 0.36
    if shadow:
        ctx.move_to(tx + 3, ty + 4)
        ctx.set_source_rgba(0, 0, 0, 0.45 * a)
        ctx.show_text(s)
    ctx.move_to(tx, ty)
    ctx.set_source_rgba(*rgb, a)
    ctx.show_text(s)
    return w


def text_width(ctx, s, size, font=FONT, bold=True):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    return ctx.text_extents(s)[4]


# ---------- fondos ----------
def bg_night(ctx, T, grid=True, stars=True):
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, NAVY), (1, NAVY2)]))
    ctx.paint()
    if stars:
        rng = np.random.default_rng(3)
        for _ in range(70):
            x, y, r = rng.uniform(-400, W + 400), rng.uniform(-400, H * 0.7), rng.uniform(1.5, 4)
            tw = 0.5 + 0.5 * math.sin(T * rng.uniform(1, 3) + rng.uniform(0, 6))
            circle(ctx, x, y, r)
            fill(ctx, WHITE, 0.25 + 0.5 * tw)
    if grid:
        bg_grid(ctx, a=0.05)


def bg_grid(ctx, step=90, a=0.06, rgb=WHITE, extent=2500):
    ctx.set_line_width(2)
    ctx.set_source_rgba(*rgb, a)
    for x in range(-extent, W + extent, step):
        ctx.move_to(x, -extent)
        ctx.line_to(x, H + extent)
    for y in range(-extent, H + extent, step):
        ctx.move_to(-extent, y)
        ctx.line_to(W + extent, y)
    ctx.stroke()


def bg_blueprint(ctx, T):
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.06, 0.16, 0.36)), (1, (0.04, 0.10, 0.25))]))
    ctx.paint()
    bg_grid(ctx, 60, 0.08)
    bg_grid(ctx, 300, 0.10)


def bg_sky(ctx, T, warm=0.0):
    top = (lerp(0.36, 0.98, warm * 0.6), lerp(0.62, 0.62, warm), lerp(0.95, 0.40, warm))
    bot = (lerp(0.75, 1.0, warm), lerp(0.88, 0.80, warm), lerp(1.0, 0.55, warm))
    ctx.set_source(vgrad(ctx, 0, -600, 0, H, [(0, top), (1, bot)]))
    ctx.paint()


def bg_dark(ctx, T):
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.06, 0.07, 0.14)), (1, (0.09, 0.10, 0.20))]))
    ctx.paint()
    bg_grid(ctx, 90, 0.05)


def ground(ctx, y, rgb=(0.20, 0.24, 0.42), extent=3000):
    ctx.rectangle(-extent, y, W + 2 * extent, H + extent)
    fill(ctx, rgb)


def sun(ctx, x, y, r, T, a=1.0):
    g = cairo.RadialGradient(x, y, r * 0.5, x, y, r * 2.6)
    g.add_color_stop_rgba(0, 1, 0.85, 0.3, 0.55 * a)
    g.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r * 2.6)
    ctx.fill()
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(T * 0.4)
    for k in range(12):
        ctx.rotate(math.pi / 6)
        rrect(ctx, r * 1.15, -9, r * 0.45, 18, 9)
        fill(ctx, (1, 0.78, 0.25), a)
    ctx.restore()
    circle(ctx, x, y, r)
    ctx.set_source(vgrad(ctx, x, y - r, x, y + r, [(0, (1, 0.92, 0.45), a), (1, (1, 0.70, 0.20), a)]))
    ctx.fill()


# ---------- personaje (original del canal) ----------
def character(ctx, x, y, s=1.0, T=0.0, mood="normal", look=(0, 0), helmet=False, shirt=BLUE, body=True, talk=False, wave=0.0):
    """Personaje propio del canal: cabeza redonda, pelo castaño, ojos grandes.
    mood: normal | feliz | sorpresa | duda | dormido
    (x, y) = centro de la cabeza; s = escala (cabeza de radio 150*s)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    R = 150
    if body:
        soft_shadow(ctx, 0, R * 2.85, R * 1.3, 40, 0.3)
        # cuerpo
        rrect(ctx, -R * 0.95, R * 0.85, R * 1.9, R * 2.0, R * 0.7)
        ctx.set_source(vgrad(ctx, 0, R, 0, R * 3, [(0, shirt), (1, tuple(c * 0.75 for c in shirt))]))
        ctx.fill()
        # brazo que saluda
        if wave:
            ctx.save()
            ctx.translate(R * 0.85, R * 1.2)
            ctx.rotate(-1.9 + 0.35 * math.sin(T * 9) * wave)
            rrect(ctx, -30, 0, 60, R * 1.1, 30)
            fill(ctx, tuple(c * 0.9 for c in shirt))
            circle(ctx, 0, R * 1.15, 38)
            fill(ctx, SKIN)
            ctx.restore()
        # cuello
        rrect(ctx, -40, R * 0.75, 80, 60, 20)
        fill(ctx, SKIN_D)
    # orejas
    for sx in (-1, 1):
        ellipse(ctx, sx * R * 0.98, R * 0.08, 32, 42)
        fill(ctx, SKIN_D)
    # cabeza
    circle(ctx, 0, 0, R)
    g = cairo.RadialGradient(-R * 0.3, -R * 0.4, R * 0.2, 0, 0, R * 1.05)
    g.add_color_stop_rgb(0, 1.0, 0.86, 0.72)
    g.add_color_stop_rgb(1, *SKIN_D)
    ctx.set_source(g)
    ctx.fill()
    # mejillas
    for sx in (-1, 1):
        circle(ctx, sx * R * 0.55, R * 0.38, 30)
        fill(ctx, (0.96, 0.55, 0.55), 0.45)
    # pelo
    ctx.move_to(-R * 1.0, -R * 0.05)
    ctx.curve_to(-R * 1.1, -R * 1.25, R * 1.1, -R * 1.3, R * 1.0, -R * 0.1)
    ctx.curve_to(R * 0.75, -R * 0.55, R * 0.3, -R * 0.5, R * 0.1, -R * 0.62)
    ctx.curve_to(-R * 0.1, -R * 0.45, -R * 0.55, -R * 0.55, -R * 0.75, -R * 0.35)
    ctx.curve_to(-R * 0.85, -R * 0.25, -R * 0.95, -R * 0.15, -R * 1.0, -R * 0.05)
    ctx.set_source(vgrad(ctx, 0, -R * 1.2, 0, -R * 0.2, [(0, (0.45, 0.31, 0.20)), (1, HAIR)]))
    ctx.fill()
    # casco
    if helmet:
        ctx.move_to(-R * 1.08, -R * 0.35)
        ctx.curve_to(-R * 1.0, -R * 1.35, R * 1.0, -R * 1.35, R * 1.08, -R * 0.35)
        ctx.close_path()
        fill(ctx, (1.0, 0.78, 0.15))
        rrect(ctx, -R * 1.25, -R * 0.42, R * 2.5, 34, 17)
        fill(ctx, (0.95, 0.66, 0.08))
        rrect(ctx, -18, -R * 1.18, 36, R * 0.8, 18)
        fill(ctx, (1.0, 0.86, 0.35))
    # ojos
    blink = 1.0
    ph = (T % 3.7)
    if mood == "dormido":
        blink = 0.0
    elif ph < 0.12:
        blink = abs(ph - 0.06) / 0.06
    big = 1.18 if mood == "sorpresa" else 1.0
    for sx in (-1, 1):
        ex, ey = sx * R * 0.38, -R * 0.02
        if blink < 0.15:
            ctx.move_to(ex - 34, ey)
            ctx.curve_to(ex - 15, ey + 18, ex + 15, ey + 18, ex + 34, ey)
            stroke(ctx, (0.25, 0.15, 0.10), 9)
        else:
            ellipse(ctx, ex, ey, 46 * big, 52 * big * blink)
            fill(ctx, WHITE)
            px, py = ex + look[0] * 14, ey + look[1] * 14
            circle(ctx, px, py, 24 * big * min(1, blink * 1.2))
            fill(ctx, (0.20, 0.12, 0.08))
            circle(ctx, px + 8, py - 9, 8)
            fill(ctx, WHITE)
        # cejas
        by = ey - 72 - (14 if mood in ("sorpresa", "duda") and (mood == "sorpresa" or sx > 0) else 0)
        ctx.move_to(ex - 34, by + (6 if mood == "duda" and sx < 0 else 0))
        ctx.curve_to(ex - 10, by - 12, ex + 10, by - 12, ex + 34, by)
        stroke(ctx, HAIR, 13)
    # boca
    mo = 0.5 + 0.5 * math.sin(T * 22) if talk else 0
    my = R * 0.45
    if mood == "sorpresa":
        ellipse(ctx, 0, my + 6, 26, 34)
        fill(ctx, (0.45, 0.10, 0.12))
        ellipse(ctx, 0, my + 22, 16, 9)
        fill(ctx, (0.95, 0.5, 0.55))
    elif mood == "feliz" or mo > 0.3:
        ctx.move_to(-48, my - 6)
        ctx.curve_to(-30, my + 40 + 20 * mo, 30, my + 40 + 20 * mo, 48, my - 6)
        ctx.close_path()
        fill(ctx, (0.45, 0.10, 0.12))
    elif mood == "duda":
        ctx.move_to(-30, my + 10)
        ctx.line_to(30, my)
        stroke(ctx, (0.40, 0.15, 0.12), 9)
    elif mood == "dormido":
        ellipse(ctx, 0, my + 8, 12, 9)
        fill(ctx, (0.45, 0.10, 0.12))
    else:
        ctx.move_to(-30, my)
        ctx.curve_to(-12, my + 20, 12, my + 20, 30, my)
        stroke(ctx, (0.40, 0.15, 0.12), 9)
    ctx.restore()


# ---------- elementos de información ----------
def pill(ctx, s, x, y, appear=1.0, size=44, rgb=YELLOW, fg=WHITE, sub=None):
    """Etiqueta con borde de color (como '1999 · ALEMANIA')."""
    if appear <= 0.01:
        return
    w = text_width(ctx, s, size) + size * 1.4
    h = size * 1.9 + (size * 0.7 if sub else 0)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(appear, appear)
    rrect(ctx, -w / 2, -h / 2, w, h, size * 0.7)
    fill_keep(ctx, (0.05, 0.06, 0.12), 0.85)
    stroke(ctx, rgb, 5)
    text(ctx, s, 0, -(size * 0.35 if sub else 0), size, fg, shadow=False)
    if sub:
        text(ctx, sub, 0, size * 0.62, size * 0.45, (0.75, 0.75, 0.85), shadow=False)
    ctx.restore()


def badge(ctx, s, x, y, appear=1.0, size=56, bg=RED, fg=WHITE):
    """Etiqueta llena (como '9:00 → 6:00')."""
    if appear <= 0.01:
        return
    w = text_width(ctx, s, size) + size * 1.2
    h = size * 1.8
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(appear, appear)
    rrect(ctx, -w / 2, -h / 2 + 6, w, h, 20)
    fill(ctx, (0, 0, 0), 0.3)
    rrect(ctx, -w / 2, -h / 2, w, h, 20)
    fill_keep(ctx, bg)
    stroke(ctx, WHITE, 5)
    text(ctx, s, 0, 0, size, fg, shadow=False)
    ctx.restore()


def digital_clock(ctx, s, x, y, scale=1.0, appear=1.0, rgb=(1, 0.18, 0.15)):
    """Reloj digital rojo (como el despertador)."""
    if appear <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale * appear, scale * appear)
    w = text_width(ctx, s, 110, "DejaVu Sans Mono") + 70
    rrect(ctx, -w / 2, -95, w, 190, 34)
    fill(ctx, (0.13, 0.14, 0.18))
    rrect(ctx, -w / 2 + 18, -75, w - 36, 150, 20)
    fill(ctx, (0.04, 0.03, 0.04))
    text(ctx, s, 0, 0, 110, rgb, font="DejaVu Sans Mono", shadow=False)
    ctx.restore()


def line_chart(ctx, x, y, w, h, ys, progress=1.0, title=None, xlabels=None, color=YELLOW, label=None):
    """Gráfica de línea que se va dibujando (progress 0..1). ys: valores 0..1."""
    ctx.save()
    ctx.set_line_width(4)
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.move_to(x, y)
    ctx.line_to(x, y + h)
    ctx.line_to(x + w, y + h)
    ctx.stroke()
    if title:
        text(ctx, title, x, y - 40, 30, (0.8, 0.8, 0.9), align="left", shadow=False)
    if xlabels:
        for k, lab in enumerate(xlabels):
            text(ctx, lab, x + w * k / (len(xlabels) - 1), y + h + 40, 30, (0.8, 0.8, 0.9), shadow=False)
    n = len(ys)
    pts = [(x + w * k / (n - 1), y + h - h * v) for k, v in enumerate(ys)]
    last = max(1, int((n - 1) * clamp(progress)))
    ctx.move_to(*pts[0])
    for k in range(1, last + 1):
        x0, y0 = pts[k - 1]
        x1, y1 = pts[k]
        ctx.curve_to((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, x1, y1)
    stroke(ctx, color, 10)
    circle(ctx, *pts[last], 14)
    fill(ctx, color)
    if label and progress >= 0.95:
        text(ctx, label, pts[-1][0], pts[-1][1] - 50, 36, color, align="right", shadow=False)
    ctx.restore()


def arrow(ctx, x0, y0, x1, y1, progress=1.0, rgb=YELLOW, w=10, dashed=False):
    xe, ye = lerp(x0, x1, progress), lerp(y0, y1, progress)
    if dashed:
        ctx.set_dash([24, 16])
    ctx.move_to(x0, y0)
    ctx.line_to(xe, ye)
    stroke(ctx, rgb, w)
    ctx.set_dash([])
    if progress > 0.9:
        ang = math.atan2(ye - y0, xe - x0)
        ctx.move_to(xe, ye)
        ctx.line_to(xe - 40 * math.cos(ang - 0.45), ye - 40 * math.sin(ang - 0.45))
        ctx.line_to(xe - 40 * math.cos(ang + 0.45), ye - 40 * math.sin(ang + 0.45))
        ctx.close_path()
        fill(ctx, rgb)


def counter(lt, a, b, d=1.0, fmt="{:.0f}"):
    return fmt.format(lerp(a, b, ease_out(lt / d)))


@lru_cache(None)
def _emoji_surface(ch, size):
    cps = [f"{ord(c):X}" for c in ch]
    for name in ("-".join(cps), "-".join(c for c in cps if c != "FE0F")):
        p = os.path.join(EMOJI_DIR, name + ".svg")
        if os.path.exists(p):
            png = cairosvg.svg2png(url=p, output_width=size, output_height=size)
            import io
            return cairo.ImageSurface.create_from_png(io.BytesIO(png))
    raise SystemExit(f"emoji no encontrado: {ch}")


def icon(ctx, ch, x, y, size=200, appear=1.0, rot=0.0):
    """Dibuja un emoji de OpenMoji (estilo plano) como icono/objeto."""
    if appear <= 0.01:
        return
    surf = _emoji_surface(ch, 512)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    k = size / 512 * appear
    ctx.scale(k, k)
    ctx.set_source_surface(surf, -256, -256)
    ctx.paint()
    ctx.restore()


# ---------- subtítulos ----------
def build_chunks(words, max_words=2):
    ws = [w for w in words if w.get("type") == "word" and not w["text"].startswith("[")]
    chunks, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= max_words or w["text"][-1] in ".?!:,":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        end = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else c[-1]["end"] + 0.3
        out.append({"words": c, "start": c[0]["start"], "end": end})
    return out


def draw_captions(ctx, chunk, T, y=1470, size=64):
    words = [w["text"] for w in chunk["words"]]
    space = text_width(ctx, " ", size)
    widths = [text_width(ctx, w, size) for w in words]
    x = W / 2 - (sum(widths) + space * (len(words) - 1)) / 2
    k = pop(T - chunk["start"], 0, 0.18)
    for w, wd, src in zip(words, widths, chunk["words"]):
        active = src["start"] <= T < max(src["end"], src["start"] + 0.2)
        ctx.save()
        ctx.translate(x + wd / 2, y)
        ctx.scale(0.9 + 0.1 * k, 0.9 + 0.1 * k)
        # contorno suave
        ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(size)
        ctx.move_to(-wd / 2, size * 0.36)
        ctx.text_path(w)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        stroke(ctx, (0, 0, 0), 10, 0.55)
        text(ctx, w, 0, 0, size, YELLOW if active else WHITE, shadow=True)
        ctx.restore()
        x += wd + space


def draw_caption_big(ctx, chunk, T, y=1060, size=150, rgb=YELLOW, edge=(0.55, 0.05, 0.05)):
    """Estilo de los Shorts de curiosidades virales: UNA palabra gigante en el centro,
    amarilla, con borde negro grueso y sombra roja oscura, que "salta" al aparecer.
    La palabra va en mayúsculas; se reduce sola si no cabe en el ancho seguro."""
    w = " ".join(x["text"] for x in chunk["words"]).upper().strip()
    if not w:
        return
    ctx.select_font_face(FONT_CAPTION, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(w)
    if ext[4] > 880:
        size = size * 880 / ext[4]
        ctx.set_font_size(size)
        ext = ctx.text_extents(w)
    lt = T - chunk["start"]
    k = ease_back(clamp(lt / 0.16))           # rebote de entrada
    s = 0.55 + 0.45 * k
    ctx.save()
    ctx.translate(W / 2, y)
    ctx.rotate(-0.035)                         # ligera inclinación, más dinámico
    ctx.scale(s, s)
    x0, y0 = -ext[4] / 2, size * 0.35
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    # sombra desplazada (rojo oscuro) + contorno negro + relleno amarillo
    for dx, dy, col, lw in ((9, 11, edge, 26), (0, 0, (0, 0, 0), 22)):
        ctx.new_path(); ctx.move_to(x0 + dx, y0 + dy); ctx.text_path(w)
        ctx.set_source_rgb(*col); ctx.set_line_width(lw); ctx.stroke_preserve(); ctx.fill()
    ctx.new_path(); ctx.move_to(x0, y0); ctx.text_path(w)
    ctx.set_source_rgb(*rgb); ctx.fill()
    ctx.restore()


def _captions(ctx, mod, ch, T):
    if getattr(mod, "ESTILO_SUBTITULO", "grande") == "grande":
        draw_caption_big(ctx, ch, T, y=getattr(mod, "Y_SUBTITULO", 1060))
    else:
        draw_captions(ctx, ch, T)


def ficha(ctx, nombre, sub, x, y, appear=1.0, emoji="⭐", accent=YELLOW, w=840):
    """Ficha de personaje famoso: marco redondo con su símbolo (bombilla, coche...) + NOMBRE grande
    + a qué se dedica / años. Sirve para que el espectador ubique al personaje al instante.
    (No se usan fotos de personas reales: solo nombre, datos y su objeto icónico.)"""
    if appear <= 0.01:
        return
    h = 210
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(appear, appear)
    rrect(ctx, -w / 2, -h / 2 + 8, w, h, 36)
    fill(ctx, (0, 0, 0), 0.35)
    rrect(ctx, -w / 2, -h / 2, w, h, 36)
    fill_keep(ctx, (0.06, 0.07, 0.14), 0.92)
    stroke(ctx, accent, 6)
    cx = -w / 2 + h / 2 + 6
    circle(ctx, cx, 0, h / 2 - 22)
    fill_keep(ctx, (0.13, 0.15, 0.28))
    stroke(ctx, accent, 6)
    icon(ctx, emoji, cx, 0, h - 80)
    tx = cx + h / 2 + 14
    ctx.select_font_face(FONT_CAPTION, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    fs = 92
    ctx.set_font_size(fs)
    adv = ctx.text_extents(nombre)[4]
    maxw = w / 2 - tx - 30
    if adv > maxw:
        fs *= maxw / adv
        ctx.set_font_size(fs)
    ctx.move_to(tx, -8)
    ctx.text_path(nombre)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(0, 0, 0); ctx.set_line_width(12); ctx.stroke_preserve()
    ctx.set_source_rgb(*accent); ctx.fill()
    text(ctx, sub, tx, 52, 34, (0.85, 0.87, 0.95), align="left", shadow=False)
    ctx.restore()


# ---------- miniaturas (pipeline/miniatura.py) ----------
def thumb_text(ctx, lines, y=330, size=170, rgb=YELLOW, rot=-0.04, gap=0.95):
    """Texto de miniatura: 1–3 líneas gigantes, fuente de cómic, borde negro grueso y sombra roja."""
    ctx.save()
    ctx.translate(W / 2, y)
    ctx.rotate(rot)
    yy = 0
    for ln in lines:
        col = rgb
        if isinstance(ln, tuple):
            ln, col = ln
        ctx.select_font_face(FONT_CAPTION, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        fs = size
        ctx.set_font_size(fs)
        adv = ctx.text_extents(ln)[4]
        if adv > 960:
            fs = fs * 960 / adv
            ctx.set_font_size(fs)
            adv = ctx.text_extents(ln)[4]
        x0, y0 = -adv / 2, yy + fs * 0.35
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        for dx, dy, c, lw in ((10, 13, (0.55, 0.05, 0.05), 30), (0, 0, (0, 0, 0), 26)):
            ctx.new_path(); ctx.move_to(x0 + dx, y0 + dy); ctx.text_path(ln)
            ctx.set_source_rgb(*c); ctx.set_line_width(lw); ctx.stroke_preserve(); ctx.fill()
        ctx.new_path(); ctx.move_to(x0, y0); ctx.text_path(ln)
        ctx.set_source_rgb(*col); ctx.fill()
        yy += fs * gap
    ctx.restore()


def thumb_circle(ctx, x, y, rx, ry, rgb=RED, w=16):
    """Círculo rojo 'a mano' alrededor del detalle intrigante."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(1, ry / rx)
    ctx.new_path()
    ctx.arc(0, 0, rx, -2.6, -2.6 + math.tau * 1.06)
    ctx.restore()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    stroke(ctx, (0, 0, 0), w + 10, 0.6)
    ctx.save(); ctx.translate(x, y); ctx.scale(1, ry / rx); ctx.new_path()
    ctx.arc(0, 0, rx, -2.6, -2.6 + math.tau * 1.06); ctx.restore()
    stroke(ctx, rgb, w)


def thumb_arrow(ctx, x0, y0, x1, y1, rgb=RED, w=34):
    """Flecha gruesa de miniatura (con borde negro)."""
    ang = math.atan2(y1 - y0, x1 - x0)
    L = math.hypot(x1 - x0, y1 - y0)
    for col, ext in (((0, 0, 0), 8), (rgb, 0)):
        ctx.save()
        ctx.translate(x0, y0)
        ctx.rotate(ang)
        ctx.new_path()
        ctx.move_to(0, -w / 2 - ext); ctx.line_to(L - w * 2.2, -w / 2 - ext); ctx.line_to(L - w * 2.2, -w * 1.6 - ext)
        ctx.line_to(L + ext * 1.5, 0); ctx.line_to(L - w * 2.2, w * 1.6 + ext); ctx.line_to(L - w * 2.2, w / 2 + ext)
        ctx.line_to(0, w / 2 + ext); ctx.close_path()
        fill(ctx, col)
        ctx.restore()


def thumb_vignette(ctx, a=0.55):
    g = cairo.RadialGradient(W / 2, H * 0.45, W * 0.35, W / 2, H * 0.45, H * 0.75)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, a)
    ctx.set_source(g)
    ctx.paint()


# ---------- render ----------
def render(workdir):
    spec_mod = importlib.util.spec_from_file_location("escenas", os.path.join(workdir, "escenas.py"))
    mod = importlib.util.module_from_spec(spec_mod)
    sys.modules["anim"] = sys.modules[__name__]
    spec_mod.loader.exec_module(mod)
    words = json.load(open(os.path.join(workdir, "words.json")))["words"]
    voz = os.path.join(workdir, "voz.mp3")
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", voz]).strip()) + getattr(mod, "COLA", 0.08)
    # COLA: silencio tras la última palabra. Casi 0 para que el final enlace con el principio (bucle).
    nframes = int(dur * FPS)
    escenas = sorted(mod.ESCENAS, key=lambda e: e[0])
    chunks = build_chunks(words, getattr(mod, "PALABRAS_POR_SUBTITULO", 1 if getattr(mod, "ESTILO_SUBTITULO", "grande") == "grande" else 2))
    # sonido: whoosh en cada cambio de escena + efectos que pida escenas.py (SFX = [(t, "pop"|"ding"|"tick"|"rise"|"whoosh"), ...])
    sys.path.insert(0, HERE)
    import sonido
    eventos = [(e[0] - 0.12, "whoosh") for e in escenas[1:]] + [x for x in getattr(mod, "SFX", []) if x[1] in ("pop", "ding")]
    fx_path = os.path.join(workdir, "fx.wav")
    sonido.mezcla(dur, eventos, fx_path, seed=abs(hash(os.path.basename(os.path.abspath(workdir)))) % 1000)

    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, OUT_W, OUT_H)
    out = os.path.join(workdir, "short.tmp.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{OUT_W}x{OUT_H}",
           "-r", str(FPS), "-i", "-", "-i", voz]
    cmd += ["-i", fx_path]
    # voz: limpieza ligera + presencia + volumen estándar; música/efectos se agachan cuando habla la voz
    filt = ("[1:a]highpass=f=70,equalizer=f=3500:t=q:w=1.2:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
            "loudnorm=I=-14:TP=-1.5:LRA=9,apad,asplit=2[v][vk];"
            "[2:a]aformat=sample_rates=44100:channel_layouts=mono,volume=4.0,equalizer=f=1200:t=q:w=1.5:g=-7,equalizer=f=350:t=q:w=1:g=-4[f];"
            "[f][vk]sidechaincompress=threshold=0.02:ratio=4:attack=15:release=500[fd];"
            "[v][fd]amix=inputs=2:duration=first:normalize=0[a]")
    cmd += ["-filter_complex", filt, "-map", "0:v", "-map", "[a]",
            "-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-crf", "16", "-profile:v", "high",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{nframes / FPS:.3f}", "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(nframes):
        T = i / FPS
        k = max([j for j, e in enumerate(escenas) if e[0] <= T] or [0])
        t0, fn = escenas[k][0], escenas[k][1]
        t1 = escenas[k + 1][0] if k + 1 < len(escenas) else dur
        ctx = cairo.Context(surf)
        ctx.set_antialias(cairo.ANTIALIAS_GOOD)
        ctx.scale(SCALE, SCALE)
        ctx.save()
        fn(ctx, T - t0 if i else max(T - t0, 0.6), t1 - t0, T)
        ctx.restore()
        # transición: destello corto al cambiar de escena
        if k > 0 and T - t0 < 0.12:
            ctx.set_source_rgba(1, 1, 1, 0.18 * (1 - (T - t0) / 0.12))
            ctx.paint()
        ch = next((c for c in chunks if c["start"] <= T < c["end"]), None)
        if ch:
            _captions(ctx, mod, ch, T)
        surf.flush()
        ff.stdin.write(bytes(surf.get_data()))
        if i == 0:
            surf.write_to_png(os.path.join(workdir, "thumb.png"))
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit("ffmpeg falló")
    os.replace(out, os.path.join(workdir, "short.mp4"))
    print("ok", workdir, f"{dur:.1f}s")


def preview(workdir, times):
    """Dibuja fotogramas sueltos (para revisar) en workdir/prev_T.png."""
    spec_mod = importlib.util.spec_from_file_location("escenas", os.path.join(workdir, "escenas.py"))
    mod = importlib.util.module_from_spec(spec_mod)
    sys.modules["anim"] = sys.modules[__name__]
    spec_mod.loader.exec_module(mod)
    words = json.load(open(os.path.join(workdir, "words.json")))["words"]
    escenas = sorted(mod.ESCENAS, key=lambda e: e[0])
    chunks = build_chunks(words, getattr(mod, "PALABRAS_POR_SUBTITULO", 1 if getattr(mod, "ESTILO_SUBTITULO", "grande") == "grande" else 2))
    paths = []
    for T in times:
        k = max([j for j, e in enumerate(escenas) if e[0] <= T] or [0])
        t1 = escenas[k + 1][0] if k + 1 < len(escenas) else T + 5
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        ctx = cairo.Context(surf)
        ctx.save()
        escenas[k][1](ctx, T - escenas[k][0], t1 - escenas[k][0], T)
        ctx.restore()
        ch = next((c for c in chunks if c["start"] <= T < c["end"]), None)
        if ch:
            _captions(ctx, mod, ch, T)
        p = os.path.join(workdir, f"prev_{T:.1f}.png")
        surf.write_to_png(p)
        paths.append(p)
    return paths


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        print(preview(sys.argv[1], [float(x) for x in sys.argv[3:]]))
    else:
        render(sys.argv[1])
