"""Escenas del vídeo v02: La Torre Eiffel crece en verano."""
import math
from anim import *  # noqa

IRON = (0.48, 0.31, 0.20)
IRON_D = (0.33, 0.20, 0.13)


def tower(ctx, x, y, h, stretch=1.0, tilt=0.0, sun_side=0.0, outline=False, a=1.0):
    """Torre estilizada. (x, y) = centro de la base. sun_side: 0..1 tiñe de naranja el lado izquierdo."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(tilt)
    ctx.scale(1, stretch)
    hb = h * 0.24  # media anchura de la base

    def half(yy):  # media anchura a la altura yy (0 base, h cima)
        u = yy / h
        return hb * (1 - u) ** 2.4 + 6

    def body_path():
        n = 40
        ctx.move_to(-half(0), 0)
        for k in range(1, n + 1):
            yy = h * 0.93 * k / n
            ctx.line_to(-half(yy), -yy)
        ctx.line_to(0, -h)
        for k in range(n, -1, -1):
            yy = h * 0.93 * k / n
            ctx.line_to(half(yy), -yy)
        ctx.close_path()

    body_path()
    if outline:
        stroke(ctx, WHITE, 5, 0.85 * a)
    else:
        ctx.set_source(vgrad(ctx, 0, 0, 0, -h, [(0, IRON_D), (1, IRON)]))
        ctx.fill()
        if sun_side > 0:
            ctx.save()
            body_path()
            ctx.clip()
            ctx.rectangle(-h, -h * 1.1, h, h * 1.2)
            fill(ctx, (1.0, 0.55, 0.15), 0.55 * sun_side)
            ctx.rectangle(0, -h * 1.1, h, h * 1.2)
            fill(ctx, (0.25, 0.35, 0.75), 0.45 * sun_side)
            ctx.restore()
    col = WHITE if outline else IRON_D
    # arco de la base
    ctx.move_to(-half(0) * 0.62, 0)
    ctx.curve_to(-half(0) * 0.5, -h * 0.13, half(0) * 0.5, -h * 0.13, half(0) * 0.62, 0)
    ctx.close_path()
    if outline:
        stroke(ctx, WHITE, 4, 0.7 * a)
    else:
        fill(ctx, (0.15, 0.17, 0.30), 0.9)
    # plataformas
    for u, extra in ((0.19, 1.25), (0.38, 1.25), (0.70, 1.4)):
        yy = h * u
        w = half(yy) * extra
        rrect(ctx, -w, -yy - 12, 2 * w, 24, 6)
        if outline:
            stroke(ctx, WHITE, 4, 0.8 * a)
        else:
            fill(ctx, IRON_D)
    # celosía
    ctx.set_line_width(3)
    ctx.set_source_rgba(*(col), 0.35 * a if outline else 0.5)
    n = 14
    for k in range(n):
        y0, y1 = h * 0.9 * k / n, h * 0.9 * (k + 1) / n
        for s in (-1, 1):
            ctx.move_to(s * half(y0) * 0.95, -y0)
            ctx.line_to(s * half(y1) * 0.2, -y1)
            ctx.move_to(s * half(y0) * 0.2, -y0)
            ctx.line_to(s * half(y1) * 0.95, -y1)
    ctx.stroke()
    # antena
    rrect(ctx, -5, -h - 60, 10, 70, 5)
    fill(ctx, WHITE if outline else IRON_D)
    ctx.restore()
    return (x + math.sin(tilt) * h * stretch, y - math.cos(tilt) * h * stretch - 60)


def cloud(ctx, x, y, s, a=0.9):
    for dx, dy, r in ((0, 0, 60), (60, -20, 70), (125, 0, 55), (60, 15, 60)):
        circle(ctx, x + dx * s, y + dy * s, r * s)
    fill(ctx, WHITE, a)


# --- 0.0  "¿Sabías que la Torre Eiffel no mide lo mismo en verano que en invierno?"
def e1(ctx, lt, dur, T):
    z = keyframes(lt, [(0, 1.6), (dur, 1.0)])
    cy = keyframes(lt, [(0, 650), (dur, 960)])
    camera(ctx, z, W / 2, cy)
    bg_sky(ctx, T)
    cloud(ctx, 80 + T * 12, 420, 1.0)
    cloud(ctx, 700 - T * 8, 260, 0.8)
    ground(ctx, 1560, (0.32, 0.55, 0.38))
    tower(ctx, W / 2, 1560, 1150)
    character(ctx, 210, 1300, 0.55, T, mood="duda", look=(1, -1))
    pill(ctx, "VERANO ≠ INVIERNO", W / 2, 1720, pop(lt, 2.2))


# --- 3.9  "Con el calor, su hierro se dilata y puede crecer hasta unos quince centímetros."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    warm = ease(lt / 1.2)
    bg_sky(ctx, T, warm)
    sun(ctx, 860, 330 + 60 * (1 - ease_out(lt / 1.0)), 95, T, a=ease(lt / 0.6))
    ground(ctx, 1560, (0.45, 0.50, 0.30))
    st = 1 + 0.06 * ease((lt - 1.4) / 2.0)
    top = tower(ctx, W / 2 - 60, 1560, 1100, stretch=st)
    # regla de medir a la derecha
    x = 820
    y_top0 = 1560 - 1100
    y_top = 1560 - 1100 * st
    arrow(ctx, x, 1560, x, y_top, progress=ease(lt / 1.0), rgb=WHITE, w=6)
    ctx.set_line_width(4)
    ctx.set_dash([14, 10])
    ctx.move_to(x - 120, y_top0)
    ctx.line_to(x + 60, y_top0)
    stroke(ctx, WHITE, 4, 0.6)
    ctx.set_dash([])
    icon(ctx, "🌡", 180, 760, 230, pop(lt, 0.2), rot=0.15 * math.sin(T * 3))
    badge(ctx, "+" + counter(lt - 2.4, 0, 15, 1.0) + " CM", 840, y_top - 120, pop(lt, 2.4), size=62)


# --- 8.7  "Pero hay más:"
def e3(ctx, lt, dur, T):
    dx, dy = shake(T, 3 * (1 - clamp(lt / 0.5)))
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.25)]), W / 2 + dx, 900 + dy)
    bg_dark(ctx, T)
    soft_shadow(ctx, W / 2, 960, 520, 520, 0.0)
    character(ctx, W / 2, 820, 1.35, T, mood="sorpresa", talk=False)
    icon(ctx, "❗", 850, 430, 320, pop(lt, 0.3), rot=0.2)
    icon(ctx, "❓", 230, 470, 240, pop(lt, 0.6), rot=-0.25)


# --- 11.0 "en un día de sol, el lado que recibe la luz se estira más que el de la sombra"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 960)
    bg_sky(ctx, T, 0.5)
    sun(ctx, 120, 300, 80, T)
    ground(ctx, 1560, (0.40, 0.48, 0.30))
    # rayos de luz
    for k in range(5):
        ctx.move_to(160, 340)
        ctx.line_to(400 + k * 30, 700 + k * 160)
        stroke(ctx, (1, 0.85, 0.4), 6, 0.35 * ease(lt / 0.8))
    tower(ctx, W / 2 + 40, 1560, 1100, sun_side=ease((lt - 0.4) / 1.0))
    pill(ctx, "SOL ☀", 300, 1700, pop(lt, 0.9), rgb=(1, 0.6, 0.2))
    pill(ctx, "SOMBRA", 800, 1700, pop(lt, 2.2), rgb=(0.5, 0.6, 1.0))
    arrow(ctx, 330, 1100, 330, 760, ease((lt - 1.2) / 0.8), rgb=(1, 0.6, 0.2), w=12)
    arrow(ctx, 770, 1100, 770, 950, ease((lt - 2.6) / 0.8), rgb=(0.6, 0.7, 1.0), w=12)


# --- 15.6 "así que la punta se inclina y va dibujando un pequeño círculo en el cielo."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (dur * 0.6, 1.9)]), W / 2, keyframes(lt, [(0, 900), (dur * 0.6, 700)]))
    bg_sky(ctx, T, 0.35)
    ground(ctx, 1560, (0.40, 0.48, 0.30))
    ang = lt * 2.2
    tilt = 0.035 * math.sin(ang)
    tip = tower(ctx, W / 2, 1560, 1100, tilt=tilt, sun_side=0.6)
    # círculo que dibuja la punta
    cx, cy, r = W / 2, 1560 - 1100 - 60, 70
    prog = clamp(lt / 2.6)
    ctx.set_dash([12, 10])
    ctx.new_sub_path()
    ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * prog)
    stroke(ctx, YELLOW, 7)
    ctx.set_dash([])
    px = cx + r * math.cos(-math.pi / 2 + 2 * math.pi * prog)
    py = cy + r * math.sin(-math.pi / 2 + 2 * math.pi * prog)
    circle(ctx, px, py, 14)
    fill(ctx, YELLOW)
    pill(ctx, "≈ 15 CM", cx - 190, cy - 110, pop(lt, 0.8), size=34)


# --- 18.4 "Sus ingenieros ya lo tuvieron en cuenta en 1889."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_blueprint(ctx, T)
    tower(ctx, 690, 1500, 1050, outline=True, a=ease(lt / 0.8))
    character(ctx, 280, 1120, 0.75, T, mood="feliz", helmet=True, shirt=(0.95, 0.45, 0.15))
    pill(ctx, "1889 · PARÍS", W / 2, 360, pop(lt, 1.6), sub="EXPOSICIÓN UNIVERSAL")
    icon(ctx, "📐", 870, 1180, 170, pop(lt, 0.6), rot=-0.2)


# --- 22.3 "Síguenos para más curiosidades."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 980)
    bg_night(ctx, T)
    character(ctx, W / 2, 820, 1.0, T, mood="feliz", wave=1.0)
    badge(ctx, "SÍGUENOS", W / 2, 360, pop(lt, 0.3), size=70, bg=RED)


ESCENAS = [(0.0, e1), (3.9, e2), (8.7, e3), (11.0, e4), (15.6, e5), (18.4, e6), (22.3, e7)]
PALABRAS_POR_SUBTITULO = 2

SFX = [(2.2, "pop"), (5.3, "rise"), (6.3, "ding"), (9.0, "pop"), (12.0, "pop"), (13.2, "pop"),
       (16.4, "pop"), (20.0, "pop"), (20.4, "ding"), (22.6, "pop")]
