"""Efectos de dibujos animados para AnimalCity TV (cairo).

Movimiento (devuelven números para pasar a la marioneta):
    salto(lt, t0, d, alto)      -> (dy, sq)        anticipación, vuelo estirado y aplastón al caer
    toma(lt, t0)                -> (dy, sq)        "take" de sorpresa: se encoge, se estira hacia arriba y rebota
    entrada(lt, t0, d, desde)   -> (dx, sq, vel)   llega disparado con rebote final (vel para la estela)
    salida(lt, t0, d, hacia)    -> (dx, sq, vel)   anticipación hacia atrás y sale disparado
    carrera(T, ancho, vel)      -> (dx, flip, vel) corre de lado a lado (pánico)
Dibujo (coordenadas del mundo 1080x1920):
    lineas_velocidad, lineas_foco, nube_poof, polvo, destello, destellos, estallido, nube_lluvia,
    emote ("!", "?", "♥"), gotas_sudor, vapor, rodador (tumbleweed), confeti, luciernagas, corazones,
    estrellas_mareo, ambiente (calida, noche, drama, gris, rosa) y transiciones (ver sitcom._frame).
"""
import math
import numpy as np
from anim import *  # noqa: F401,F403
import cairocffi as cairo

INK = (0.08, 0.07, 0.12)


# ---------------------------------------------------------------- easings
def e_back(p, s=1.9):
    p = clamp(p) - 1
    return p * p * ((s + 1) * p + s) + 1


def e_elastic(p):
    p = clamp(p)
    if p in (0, 1):
        return p
    return 2 ** (-10 * p) * math.sin((p - 0.075) * 2 * math.pi / 0.3) + 1


def e_out(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def e_in(p):
    p = clamp(p)
    return p ** 3


def smooth(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


# ---------------------------------------------------------------- movimiento
def salto(lt, t0, d=0.45, alto=160):
    """Salto completo: 0,08 s de anticipación (aplastado), vuelo en parábola estirado, aplastón al aterrizar."""
    if lt < t0 - 0.09 or lt > t0 + d + 0.25:
        return 0.0, 1.0
    if lt < t0:  # anticipación
        p = (lt - (t0 - 0.09)) / 0.09
        return 0.0, 1 - 0.18 * smooth(p)
    if lt < t0 + d:
        p = (lt - t0) / d
        dy = -alto * 4 * p * (1 - p)
        sq = 1 + 0.22 * (1 - p) - 0.05 * p
        return dy, sq
    p = (lt - t0 - d) / 0.25  # aterrizaje: aplastón y rebote
    return 0.0, 1 - 0.2 * math.exp(-p * 5) * math.cos(p * 9)


def toma(lt, t0, fuerza=1.0):
    """Reacción de sorpresa de cartoon: se encoge, sale disparado hacia arriba estirado y rebota al volver."""
    p = lt - t0
    if p < -0.08 or p > 0.9:
        return 0.0, 1.0
    if p < 0:
        return 0.0, 1 - 0.2 * fuerza * smooth((p + 0.08) / 0.08)
    if p < 0.18:
        q = p / 0.18
        return -120 * fuerza * e_out(q), 1 + 0.38 * fuerza * (1 - q * 0.4)
    q = (p - 0.18) / 0.72
    dy = -120 * fuerza * (1 - e_elastic(q))
    sq = 1 + 0.23 * fuerza * math.exp(-q * 4) * math.cos(q * 14)
    return dy, sq


def entrada(lt, t0, d=0.28, desde=-900):
    """Entra disparado desde `desde` (unidades del mundo, relativo a su sitio) con rebote al frenar."""
    if lt < t0:
        return float(desde), 1.0, 0.0
    p = (lt - t0) / d
    if p >= 1:
        q = (lt - t0 - d) / 0.3
        sq = 1 + 0.12 * math.exp(-q * 6) * math.cos(q * 12) if q < 1 else 1.0
        return 0.0, sq, 0.0
    x = desde * (1 - e_back(p, 1.4))
    vel = -desde * (1 - p) * 3.0 / d * 0.12
    return x, 0.84 + 0.16 * p, vel


def salida(lt, t0, d=0.22, hacia=1000):
    """Anticipación (se echa atrás 0,12 s) y sale disparado hacia `hacia`."""
    if lt < t0 - 0.12:
        return 0.0, 1.0, 0.0
    if lt < t0:
        p = (lt - (t0 - 0.12)) / 0.12
        return -0.07 * hacia * smooth(p), 1 - 0.12 * smooth(p), 0.0
    p = clamp((lt - t0) / d)
    return -0.07 * hacia + hacia * 1.07 * e_in(p), 0.82, hacia * 0.12 / d * (0.2 + p)


def carrera(T, ancho=260, vel=2.2):
    """Corre de lado a lado sin parar (pánico). Devuelve (dx, flip, velocidad)."""
    ph = T * vel
    dx = ancho * math.sin(ph * math.pi)
    v = math.cos(ph * math.pi)
    return dx, v < 0, ancho * v * 0.18


def temblor(T, amp):
    return amp * math.sin(T * 61.0), amp * 0.7 * math.cos(T * 47.0)


# ---------------------------------------------------------------- piezas de dibujo
def _rng(seed):
    return np.random.default_rng(seed)


def lineas_velocidad(ctx, x, y, w, h, direccion=1, T=0.0, n=14, rgb=WHITE, a=0.85, seed=1):
    """Rayas horizontales de velocidad dentro del rectángulo (x, y, w, h)."""
    if a <= 0.01:
        return
    r = _rng(seed)
    for i in range(n):
        yy = y + r.uniform(0, h)
        ln = r.uniform(0.25, 0.7) * w
        ph = (T * r.uniform(3, 6) + r.uniform(0, 1)) % 1
        xx = x + (ph * (w + ln)) - ln if direccion > 0 else x + w - ph * (w + ln)
        ctx.move_to(xx, yy)
        ctx.line_to(xx + ln, yy)
        stroke(ctx, rgb, r.uniform(4, 11), a * r.uniform(0.4, 1))


def lineas_foco(ctx, cx, cy, T=0.0, a=0.8, rgb=WHITE, n=46, r0=360, seed=2):
    """Líneas de enfoque que apuntan al centro (para gritos y momentos de impacto). Coordenadas de pantalla."""
    if a <= 0.01:
        return
    r = _rng(seed + int(T * 24))
    for i in range(n):
        ang = i * 2 * math.pi / n + r.uniform(-0.05, 0.05)
        ri = r0 + r.uniform(0, 260)
        wdt = r.uniform(0.008, 0.022)
        ctx.move_to(cx + math.cos(ang) * ri, cy + math.sin(ang) * ri)
        ctx.line_to(cx + math.cos(ang - wdt) * 2400, cy + math.sin(ang - wdt) * 2400)
        ctx.line_to(cx + math.cos(ang + wdt) * 2400, cy + math.sin(ang + wdt) * 2400)
        ctx.close_path()
        fill(ctx, rgb, a)


def _nube(ctx, x, y, r, n=7, seed=0, rot=0.0):
    rr = _rng(seed)
    ctx.new_sub_path()
    for i in range(n):
        ang = rot + i * 2 * math.pi / n
        rx, ry = x + math.cos(ang) * r * 0.62, y + math.sin(ang) * r * 0.5
        ctx.new_sub_path()
        ctx.arc(rx, ry, r * rr.uniform(0.42, 0.58), 0, 2 * math.pi)
    ctx.new_sub_path()
    ctx.arc(x, y, r * 0.7, 0, 2 * math.pi)


def nube_pintada(ctx, x, y, r, rgb, a=1.0, lw=6, n=7, seed=0, rot=0.0):
    """Nube rellena con contorno solo por fuera (sin círculos por dentro)."""
    _nube(ctx, x, y, r, n, seed, rot)
    stroke(ctx, INK, lw * 2, a)
    _nube(ctx, x, y, r, n, seed, rot)
    fill(ctx, rgb, a)


def nube_poof(ctx, x, y, r, p, rgb=(0.97, 0.97, 1.0), seed=3):
    """Nube de humo ¡POOF! (p 0..1: crece y se desvanece) con estrellitas."""
    if p <= 0 or p >= 1:
        return
    k = e_out(min(1, p * 2.2))
    a = 1 - smooth((p - 0.55) / 0.45)
    ctx.save()
    ctx.push_group()
    for j in range(3):
        rr = r * k * (1 - j * 0.18)
        nube_pintada(ctx, x + (j - 1) * r * 0.25 * k, y - j * r * 0.12 * k, rr, rgb, 1.0, max(2, r * 0.03), 8,
                     seed + j, p * 0.6)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)
    for i in range(6):
        ang = i * math.pi / 3 + 0.4
        d = r * (0.9 + 0.9 * p)
        destello(ctx, x + math.cos(ang) * d, y + math.sin(ang) * d, r * 0.13 * (1 - p), (1, 0.92, 0.4), a)
    ctx.restore()


def polvo(ctx, x, y, p, s=1.0, seed=4):
    """Nubecitas de polvo a los pies (al frenar, aterrizar o salir corriendo)."""
    if p <= 0 or p >= 1:
        return
    r = _rng(seed)
    for i in range(6):
        side = -1 if i % 2 else 1
        d = (40 + i * 22) * s * e_out(p)
        rr = (26 + r.uniform(0, 22)) * s * (1 - p * 0.6)
        circle(ctx, x + side * d, y - 12 * s - i * 6 * s * p, rr)
        fill_keep(ctx, (0.93, 0.9, 0.84), 1 - p)
        stroke(ctx, INK, 3 * s, (1 - p) * 0.8)


def destello(ctx, x, y, r, rgb=WHITE, a=1.0):
    """Estrellita de 4 puntas."""
    if a <= 0.01 or r <= 0.5:
        return
    ctx.move_to(x, y - r)
    ctx.curve_to(x + r * 0.12, y - r * 0.12, x + r * 0.12, y - r * 0.12, x + r, y)
    ctx.curve_to(x + r * 0.12, y + r * 0.12, x + r * 0.12, y + r * 0.12, x, y + r)
    ctx.curve_to(x - r * 0.12, y + r * 0.12, x - r * 0.12, y + r * 0.12, x - r, y)
    ctx.curve_to(x - r * 0.12, y - r * 0.12, x - r * 0.12, y - r * 0.12, x, y - r)
    ctx.close_path()
    fill(ctx, rgb, a)


def destellos(ctx, x, y, w, h, T, n=12, rgb=WHITE, a=1.0, seed=5, size=26):
    """Destellos que parpadean repartidos por un rectángulo."""
    r = _rng(seed)
    for i in range(n):
        px, py = x + r.uniform(0, w), y + r.uniform(0, h)
        ph = (T * r.uniform(0.8, 1.6) + r.uniform(0, 1)) % 1
        k = math.sin(ph * math.pi)
        destello(ctx, px, py, size * r.uniform(0.6, 1.3) * k, rgb, a * k)


def estallido(ctx, x, y, r, p=1.0, rgb=hexc("#FFD23F"), puntas=12, rot=0.0, borde=True):
    """Estrella de cómic (¡POW!) detrás de un golpe o de un texto."""
    if p <= 0:
        return
    k = max(0.02, e_back(min(1, p * 3))) if p < 1 else 1
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(k, k)
    for i in range(puntas * 2):
        ang = i * math.pi / puntas
        rr = r if i % 2 == 0 else r * 0.62
        (ctx.move_to if i == 0 else ctx.line_to)(math.cos(ang) * rr, math.sin(ang) * rr)
    ctx.close_path()
    fill_keep(ctx, rgb)
    if borde:
        stroke(ctx, INK, max(3, r * 0.05))
    ctx.restore()


def nube_lluvia(ctx, x, y, s=1.0, T=0.0, a=1.0, trueno=False):
    """Nubecita gris que llueve encima de un personaje triste."""
    if a <= 0.01:
        return
    bob = math.sin(T * 2.2) * 8 * s
    r = _rng(9)
    ctx.save()
    ctx.rectangle(x - 260 * s, y + 30 * s + bob, 520 * s, 900 * s)
    ctx.clip()
    for i in range(26):
        dx = r.uniform(-170, 170) * s
        ph = (T * r.uniform(1.6, 2.2) + r.uniform(0, 1)) % 1
        yy = y + 50 * s + bob + ph * 620 * s
        ctx.move_to(x + dx, yy)
        ctx.line_to(x + dx - 6 * s, yy + 36 * s)
        stroke(ctx, hexc("#7FB7F2"), 7 * s, a * 0.9)
    ctx.restore()
    nube_pintada(ctx, x, y + bob, 150 * s, hexc("#8A8FA3"), a, 6 * s, 7, 11)
    _nube(ctx, x - 30 * s, y - 25 * s + bob, 80 * s, 6, 12)
    fill(ctx, hexc("#A9AEC0"), a * 0.8)
    if trueno and (T * 1.3) % 1 < 0.08:
        ctx.move_to(x + 20 * s, y + 40 * s)
        for px, py in ((-30, 120), (10, 120), (-40, 230)):
            ctx.line_to(x + px * s, y + py * s)
        stroke(ctx, hexc("#FFE24A"), 12 * s, a)


def emote(ctx, ch, x, y, p, rgb=WHITE, size=150, T=0.0):
    """Signo que salta encima de una cabeza: "!", "?", "!?", "♥"."""
    if p <= 0:
        return
    k = max(0.02, e_back(min(1, p * 3.3)))
    wob = 0.08 * math.sin(T * 9)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(wob)
    ctx.scale(k, k)
    ctx.select_font_face("Lilita One", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ex = ctx.text_extents(ch)
    ctx.move_to(-ex[4] / 2, size * 0.36)
    ctx.text_path(ch)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*INK, 1)
    ctx.set_line_width(size * 0.16)
    ctx.stroke_preserve()
    ctx.set_source_rgba(*rgb, 1)
    ctx.fill()
    ctx.restore()


def gotas_sudor(ctx, x, y, T, s=1.0, n=4):
    """Gotas de sudor que saltan a los lados de la cabeza (pánico)."""
    for i in range(n):
        ph = (T * 2.4 + i / n) % 1
        side = -1 if i % 2 else 1
        gx = x + side * (60 + 170 * ph) * s
        gy = y - 40 * s - 180 * ph * s + 330 * ph * ph * s
        r = 18 * s * (1 - 0.4 * ph)
        ctx.save()
        ctx.translate(gx, gy)
        ctx.rotate(side * (0.5 + ph))
        ctx.move_to(0, -r * 1.8)
        ctx.curve_to(r, -r * 0.4, r, r, 0, r)
        ctx.curve_to(-r, r, -r, -r * 0.4, 0, -r * 1.8)
        fill_keep(ctx, hexc("#9FD8FF"), 1 - ph * 0.5)
        stroke(ctx, INK, 3 * s, 1 - ph * 0.5)
        ctx.restore()


def vapor(ctx, x, y, T, s=1.0, rgb=WHITE):
    """Nubecitas de vapor que salen de la cabeza (enfado)."""
    for i in range(3):
        ph = (T * 1.8 + i / 3) % 1
        for side in (-1, 1):
            circle(ctx, x + side * (40 + 90 * ph) * s, y - 160 * ph * s, (20 + 34 * ph) * s)
            fill_keep(ctx, rgb, 0.9 * (1 - ph))
            stroke(ctx, INK, 3 * s, 0.7 * (1 - ph))


def rodador(ctx, x, y, r, T):
    """Planta rodadora (tumbleweed) que cruza en los silencios incómodos."""
    ctx.save()
    ctx.translate(x, y - r - abs(math.sin(T * 5)) * r * 0.5)
    ctx.rotate(T * 5)
    rr = _rng(13)
    for i in range(30):
        a0 = rr.uniform(0, 2 * math.pi)
        ctx.arc(0, 0, r * rr.uniform(0.35, 1), a0, a0 + rr.uniform(1.5, 3.5))
        ctx.new_sub_path()
    stroke(ctx, hexc("#9C7A4B"), r * 0.06)
    circle(ctx, 0, 0, r)
    stroke(ctx, hexc("#6E532E"), r * 0.05, 0.8)
    ctx.restore()


def confeti(ctx, T, t0, x=540, y=900, n=70, seed=6, a=1.0):
    """Explosión de confeti que cae (desde t0)."""
    p = T - t0
    if p < 0 or p > 3.0:
        return
    r = _rng(seed)
    cols = [hexc(c) for c in ("#FF5FA2", "#FFD23F", "#5EB8F2", "#7CE38B", "#B07CE8", "#FF8A3D")]
    for i in range(n):
        ang = r.uniform(-math.pi, 0)
        v = r.uniform(600, 1500)
        px = x + math.cos(ang) * v * p * 0.8
        py = y + math.sin(ang) * v * p + 900 * p * p
        ctx.save()
        ctx.translate(px, py)
        ctx.rotate(p * r.uniform(4, 10))
        ctx.scale(1, abs(math.sin(p * r.uniform(5, 12))) + 0.15)
        ctx.rectangle(-14, -8, 28, 16)
        fill(ctx, cols[i % len(cols)], a * (1 - smooth((p - 2.2) / 0.8)))
        ctx.restore()


def corazones(ctx, x, y, T, n=4, s=1.0, rgb=hexc("#FF5FA2")):
    for i in range(n):
        ph = (T * 0.9 + i / n) % 1
        px = x + math.sin(ph * 6 + i) * 60 * s
        py = y - ph * 260 * s
        k = 26 * s * math.sin(ph * math.pi)
        ctx.save()
        ctx.translate(px, py)
        ctx.scale(k / 26 if k > 0 else 0.01, k / 26 if k > 0 else 0.01)
        ctx.move_to(0, 22)
        ctx.curve_to(-40, -6, -18, -36, 0, -14)
        ctx.curve_to(18, -36, 40, -6, 0, 22)
        fill_keep(ctx, rgb)
        stroke(ctx, INK, 4)
        ctx.restore()


def estrellas_mareo(ctx, x, y, T, s=1.0):
    for i in range(5):
        ang = T * 4 + i * 2 * math.pi / 5
        destello(ctx, x + math.cos(ang) * 120 * s, y + math.sin(ang) * 36 * s, 26 * s, hexc("#FFD23F"))


def luciernagas(ctx, x, y, w, h, T, n=14, seed=8):
    r = _rng(seed)
    for i in range(n):
        px = x + (r.uniform(0, w) + 40 * math.sin(T * r.uniform(0.5, 1.2) + i)) % w
        py = y + (r.uniform(0, h) + 30 * math.cos(T * r.uniform(0.6, 1.1) + i * 2))
        a = 0.5 + 0.5 * math.sin(T * r.uniform(2, 4) + i)
        g = cairo.RadialGradient(px, py, 0, px, py, 26)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.9 * a)
        g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        ctx.set_source(g)
        circle(ctx, px, py, 26)
        ctx.fill()


def motas(ctx, x, y, w, h, T, n=20, seed=12, rgb=(1, 0.95, 0.8)):
    """Motas de polvo flotando en la luz de una lámpara."""
    r = _rng(seed)
    for i in range(n):
        px = x + (r.uniform(0, w) + T * r.uniform(-10, 10)) % w
        py = y + (r.uniform(0, h) - T * r.uniform(5, 18)) % h
        circle(ctx, px, py, r.uniform(2, 5))
        fill(ctx, rgb, 0.35 + 0.3 * math.sin(T * 3 + i))


def ambiente(ctx, tipo, a=1.0, cx=W / 2, cy=H * 0.45):
    """Capa de luz encima de la escena (coordenadas de pantalla): calida, noche, drama, gris, rosa, frio."""
    if a <= 0.01:
        return
    ctx.save()
    if tipo == "calida":
        g = cairo.RadialGradient(cx, cy, 100, cx, cy, 1300)
        g.add_color_stop_rgba(0, 1, 0.75, 0.4, 0.10 * a)
        g.add_color_stop_rgba(1, 0.35, 0.12, 0.05, 0.35 * a)
        ctx.set_source(g)
        ctx.paint()
    elif tipo == "noche":
        ctx.set_operator(cairo.OPERATOR_MULTIPLY)
        ctx.set_source_rgba(0.55, 0.62, 1.0, 0.55 * a)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)
        g = cairo.RadialGradient(cx, cy, 300, cx, cy, 1300)
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0.02, 0.02, 0.1, 0.45 * a)
        ctx.set_source(g)
        ctx.paint()
    elif tipo == "drama":
        g = cairo.RadialGradient(cx, cy, 200, cx, cy, 1100)
        g.add_color_stop_rgba(0, 0, 0, 0, 0)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.7 * a)
        ctx.set_source(g)
        ctx.paint()
    elif tipo == "gris":
        ctx.set_operator(cairo.OPERATOR_HSL_SATURATION)
        ctx.set_source_rgba(0.5, 0.5, 0.5, 0.8 * a)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.set_source_rgba(0.2, 0.25, 0.35, 0.25 * a)
        ctx.paint()
    elif tipo == "rosa":
        g = cairo.RadialGradient(cx, cy, 100, cx, cy, 1200)
        g.add_color_stop_rgba(0, 1, 0.5, 0.8, 0.0)
        g.add_color_stop_rgba(1, 1, 0.35, 0.65, 0.35 * a)
        ctx.set_source(g)
        ctx.paint()
    elif tipo == "frio":
        ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT)
        ctx.set_source_rgba(0.3, 0.6, 1.0, 0.5 * a)
        ctx.paint()
    ctx.restore()


def flash(ctx, a, rgb=WHITE):
    if a > 0.01:
        ctx.save()
        ctx.identity_matrix()
        ctx.set_source_rgba(*rgb, a)
        ctx.paint()
        ctx.restore()


def estrella_path(ctx, cx, cy, r, puntas=5, rot=-math.pi / 2):
    for i in range(puntas * 2):
        ang = rot + i * math.pi / puntas
        rr = r if i % 2 == 0 else r * 0.45
        (ctx.move_to if i == 0 else ctx.line_to)(cx + math.cos(ang) * rr, cy + math.sin(ang) * rr)
    ctx.close_path()
