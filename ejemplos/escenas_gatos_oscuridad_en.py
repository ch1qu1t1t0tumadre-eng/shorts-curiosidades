"""v03 (EN): Why your cat never bumps into things in the dark."""
import math
from anim import *  # noqa

FUR = (0.96, 0.62, 0.26)
FUR_D = (0.80, 0.45, 0.16)
FUR_L = (1.0, 0.86, 0.66)
GLOW = (0.55, 1.0, 0.55)


def cat(ctx, x, y, s=1.0, T=0.0, eyes="normal", pupil=0.3, whisker_glow=0.0, look=(0, 0), body=True, tail=True):
    """Gato naranja propio. (x, y) = centro de la cabeza; cabeza de radio 140*s.
    eyes: normal | glow (brillan en la oscuridad) ; pupil 0 = rendija, 1 = redonda."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    R = 140
    if body:
        soft_shadow(ctx, 0, R * 2.55, R * 1.3, 34, 0.35)
        if tail:
            ctx.move_to(R * 0.9, R * 2.3)
            sw = 0.25 * math.sin(T * 2.4)
            ctx.curve_to(R * 2.0, R * 2.4, R * (1.9 + sw), R * 1.2, R * (1.5 + sw), R * 0.7)
            stroke(ctx, FUR_D, 44)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ellipse(ctx, 0, R * 1.55, R * 1.0, R * 1.05)
        ctx.set_source(vgrad(ctx, 0, R * 0.6, 0, R * 2.6, [(0, FUR), (1, FUR_D)]))
        ctx.fill()
        ellipse(ctx, 0, R * 1.7, R * 0.5, R * 0.75)
        fill(ctx, FUR_L)
        for sx in (-1, 1):
            ellipse(ctx, sx * R * 0.42, R * 2.5, R * 0.28, R * 0.16)
            fill(ctx, FUR_L)
    # orejas
    for sx in (-1, 1):
        ctx.move_to(sx * R * 0.95, -R * 0.2)
        ctx.line_to(sx * R * 0.75, -R * 1.25)
        ctx.line_to(sx * R * 0.15, -R * 0.82)
        ctx.close_path()
        fill(ctx, FUR_D)
        ctx.move_to(sx * R * 0.78, -R * 0.35)
        ctx.line_to(sx * R * 0.70, -R * 1.0)
        ctx.line_to(sx * R * 0.32, -R * 0.75)
        ctx.close_path()
        fill(ctx, (1.0, 0.70, 0.70))
    # cabeza
    ellipse(ctx, 0, 0, R * 1.08, R * 0.95)
    g = cairo.RadialGradient(-R * 0.3, -R * 0.4, R * 0.2, 0, 0, R * 1.1)
    g.add_color_stop_rgb(0, 1.0, 0.74, 0.40)
    g.add_color_stop_rgb(1, *FUR_D)
    ctx.set_source(g)
    ctx.fill()
    # rayas
    for k in (-1, 0, 1):
        ctx.move_to(k * R * 0.28 - 14, -R * 0.92)
        ctx.line_to(k * R * 0.28, -R * 0.55)
        ctx.line_to(k * R * 0.28 + 14, -R * 0.92)
        fill(ctx, FUR_D)
    # hocico
    ellipse(ctx, 0, R * 0.42, R * 0.48, R * 0.32)
    fill(ctx, FUR_L)
    # bigotes
    for sx in (-1, 1):
        for k, dy in enumerate((-18, 4, 26)):
            ctx.move_to(sx * R * 0.35, R * 0.38 + dy * 0.4)
            wig = 6 * math.sin(T * 5 + k)
            ctx.curve_to(sx * R * 0.9, R * 0.3 + dy + wig, sx * R * 1.3, R * 0.28 + dy * 1.6 + wig,
                         sx * R * 1.7, R * 0.25 + dy * 2.2 + wig)
            if whisker_glow > 0:
                stroke(ctx, YELLOW, 18, 0.35 * whisker_glow)
                ctx.move_to(sx * R * 0.35, R * 0.38 + dy * 0.4)
                ctx.curve_to(sx * R * 0.9, R * 0.3 + dy + wig, sx * R * 1.3, R * 0.28 + dy * 1.6 + wig,
                             sx * R * 1.7, R * 0.25 + dy * 2.2 + wig)
            stroke(ctx, lerp_c(WHITE, YELLOW, whisker_glow), 5)
    # nariz y boca
    ctx.move_to(-16, R * 0.24)
    ctx.line_to(16, R * 0.24)
    ctx.line_to(0, R * 0.36)
    ctx.close_path()
    fill(ctx, (0.92, 0.42, 0.50))
    ctx.move_to(0, R * 0.36)
    ctx.curve_to(0, R * 0.48, -24, R * 0.52, -34, R * 0.44)
    ctx.move_to(0, R * 0.36)
    ctx.curve_to(0, R * 0.48, 24, R * 0.52, 34, R * 0.44)
    stroke(ctx, (0.45, 0.22, 0.12), 6)
    # ojos
    blink = 1.0
    ph = T % 4.1
    if ph < 0.12:
        blink = abs(ph - 0.06) / 0.06
    for sx in (-1, 1):
        ex, ey = sx * R * 0.42, -R * 0.12
        if eyes == "glow":
            g = cairo.RadialGradient(ex, ey, 10, ex, ey, 110)
            g.add_color_stop_rgba(0, *GLOW, 0.7)
            g.add_color_stop_rgba(1, *GLOW, 0)
            ctx.set_source(g)
            circle(ctx, ex, ey, 110)
            ctx.fill()
        ellipse(ctx, ex, ey, 46, 50 * max(blink, 0.08))
        fill(ctx, GLOW if eyes == "glow" else (0.75, 0.88, 0.35))
        if blink > 0.3:
            pw = lerp(8, 34, clamp(pupil))
            ellipse(ctx, ex + look[0] * 10, ey + look[1] * 8, pw, 42 * blink)
            fill(ctx, (0.08, 0.06, 0.06))
            circle(ctx, ex + 12, ey - 16, 8)
            fill(ctx, WHITE, 0.9)
    ctx.restore()


def lerp_c(a, b, x):
    return tuple(lerp(p, q, clamp(x)) for p, q in zip(a, b))


def room_dark(ctx, T, light=0.0):
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, lerp_c((0.04, 0.05, 0.10), (0.30, 0.32, 0.45), light)),
                                            (1, lerp_c((0.07, 0.08, 0.16), (0.35, 0.36, 0.50), light))]))
    ctx.paint()
    bg_grid(ctx, 90, 0.04)
    # ventana con luna
    rrect(ctx, 650, 260, 300, 380, 20)
    fill(ctx, (0.10, 0.13, 0.28))
    circle(ctx, 860, 360, 50)
    fill(ctx, (0.95, 0.95, 0.85), 0.9)
    ctx.rectangle(650, 440, 300, 10)
    ctx.rectangle(795, 260, 10, 380)
    fill(ctx, (0.25, 0.22, 0.38))
    # suelo
    ctx.rectangle(-3000, 1480, 9000, 3000)
    fill(ctx, (0.12, 0.10, 0.20))


def chair(ctx, x, y, s=1.0, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    col = (0.30, 0.22, 0.30)
    rrect(ctx, -110, -420, 30, 420, 12)
    rrect(ctx, -110, -200, 220, 34, 12)
    rrect(ctx, -110, -200, 24, 200, 10)
    rrect(ctx, 86, -200, 24, 200, 10)
    fill(ctx, col, a)
    ctx.restore()


# 0.0 "Ever wonder why your cat never bumps into anything in the dark?"
def e1(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (dur, 1.0)]), W / 2, keyframes(lt, [(0, 1100), (dur, 1000)]))
    room_dark(ctx, T)
    chair(ctx, 300, 1480)
    rrect(ctx, 760, 1330, 140, 150, 20)
    fill(ctx, (0.28, 0.20, 0.30))
    icon(ctx, "🪴", 830, 1260, 200)
    cx = keyframes(lt, [(0, 120), (dur, 560)])
    cat(ctx, cx, 1150 + 6 * math.sin(T * 8), 0.75, T, eyes="glow", pupil=1.0, look=(1, 0))
    pill(ctx, "LIGHTS OFF", W / 2, 520, pop(lt, 0.6), rgb=(0.6, 0.7, 1.0))
    icon(ctx, "❓", 900, 900, 170, pop(lt, 2.0), rot=0.2)


# 3.76 "First, its eyes."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.5)]), W / 2, keyframes(lt, [(0, 900), (dur, 780)]))
    room_dark(ctx, T)
    cat(ctx, W / 2, 860, 1.5, T, eyes="glow", pupil=ease(lt / 1.2), body=False)
    pill(ctx, "1. EYES", W / 2, 380, pop(lt, 0.3))


# 5.5 "Behind the retina there's a mirror-like layer that bounces light back for a second chance..."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 920)
    bg_blueprint(ctx, T)
    ex, ey, r = W / 2 + 40, 900, 330
    # globo ocular en corte
    circle(ctx, ex, ey, r)
    fill_keep(ctx, (0.95, 0.95, 0.98))
    stroke(ctx, WHITE, 6)
    # retina (fondo del ojo, a la derecha)
    ctx.new_sub_path()
    ctx.arc(ex, ey, r - 18, -1.0, 1.0)
    stroke(ctx, (0.95, 0.35, 0.40), 26)
    # tapetum (espejo) detrás de la retina
    ctx.new_sub_path()
    ctx.arc(ex, ey, r + 8, -0.8, 0.8)
    stroke(ctx, (0.75, 0.95, 1.0), 16 + 4 * math.sin(T * 6))
    # cristalino delante
    ellipse(ctx, ex - r + 40, ey, 40, 120)
    fill(ctx, (0.6, 0.8, 1.0), 0.7)
    # rayo de luz: entra y rebota
    p1 = ease((lt - 0.6) / 1.4)
    arrow(ctx, 40, ey - 60, lerp(40, ex + r - 20, 1), lerp(ey - 60, ey, 1), p1, YELLOW, 12)
    p2 = ease((lt - 2.4) / 1.2)
    if p2 > 0:
        arrow(ctx, ex + r - 20, ey + 10, ex - r + 60, ey + 110, p2, (1, 0.9, 0.5), 10, dashed=True)
    pill(ctx, "RETINA", ex + 140, ey - r - 70, pop(lt, 0.3), size=34, rgb=(0.95, 0.4, 0.45))
    pill(ctx, "MIRROR LAYER", ex + 60, ey + r + 90, pop(lt, 1.5), size=38, rgb=(0.7, 0.95, 1.0), sub="TAPETUM LUCIDUM")
    badge(ctx, "2ND CHANCE", 300, 520, pop(lt, 3.6), size=50)


# 10.56 "so cats can see in light about six times dimmer than we need."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    base = 1180
    # barras de luz necesaria
    for x, val, col, who in ((300, 1.0, (0.55, 0.65, 1.0), "human"), (780, 1 / 6, GLOW, "cat")):
        h = 760 * val * ease((lt - 0.4) / 1.2)
        rrect(ctx, x - 90, base - h, 180, h, 20)
        fill(ctx, col, 0.9)
        icon(ctx, "💡", x, base - h - 90, 120, pop(lt, 1.4))
    character(ctx, 300, 1310, 0.42, T, mood="duda", body=False)
    cat(ctx, 780, 1300, 0.48, T, eyes="glow", pupil=1.0, body=False)
    text(ctx, "LIGHT NEEDED TO SEE", W / 2, 290, 44, (0.8, 0.8, 0.9))
    badge(ctx, counter(lt - 1.8, 1, 6) + "x DIMMER", 780, 760, pop(lt, 1.8), size=56)


# 14.1 "But here's the real secret: their whiskers."
def e5(ctx, lt, dur, T):
    dx, dy = shake(T, 4 * (1 - clamp(lt / 0.4)))
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.6)]), W / 2 + dx, keyframes(lt, [(0, 900), (dur, 960)]) + dy)
    room_dark(ctx, T, 0.15)
    cat(ctx, W / 2, 880, 1.3, T, eyes="normal", pupil=0.6, whisker_glow=ease((lt - 1.4) / 0.6), body=False)
    pill(ctx, "THE REAL SECRET", W / 2, 420, pop(lt, 0.2), rgb=RED)


# 16.96 "They're so sensitive they feel tiny changes in the air around objects, like a built-in radar."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 1000)
    room_dark(ctx, T)
    chair(ctx, 760, 1480, 1.1)
    # corrientes de aire que rodean la silla
    for k in range(6):
        y0 = 980 + k * 70
        ph = (T * 220 + k * 90) % 900
        ctx.move_to(-100, y0)
        for xx in range(-100, 1200, 20):
            bump = -80 * math.exp(-((xx - 760) / 150) ** 2) * (1 if y0 < 1250 else -0.5)
            ctx.line_to(xx, y0 + bump + 10 * math.sin(xx / 60 + T * 3))
        ctx.set_dash([30, 24], ph)
        stroke(ctx, (0.6, 0.85, 1.0), 4, 0.5 * ease(lt / 0.8))
        ctx.set_dash([])
    cx = keyframes(lt, [(0, 160), (dur, 380)])
    cat(ctx, cx, 1130, 0.8, T, eyes="glow", pupil=1.0, whisker_glow=1.0, look=(1, 0))
    # radar
    for k in range(3):
        rr = ((T * 260 + k * 160) % 480)
        circle(ctx, cx + 120, 1170, rr)
        stroke(ctx, YELLOW, 5, 0.6 * (1 - rr / 480) * ease((lt - 3.0) / 0.6))
    pill(ctx, "AIR CURRENTS", W / 2, 760, pop(lt, 1.0), rgb=(0.6, 0.85, 1.0))
    badge(ctx, "BUILT-IN RADAR", W / 2, 890, pop(lt, 4.2), size=54)


# 22.7 "Follow for more curiosities."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 980)
    bg_night(ctx, T)
    character(ctx, 330, 820, 0.85, T, mood="feliz", wave=1.0)
    cat(ctx, 760, 1000, 0.75, T, eyes="normal", pupil=0.5, whisker_glow=0.3)
    badge(ctx, "FOLLOW", W / 2, 360, pop(lt, 0.2), size=74)


ESCENAS = [(0.0, e1), (3.76, e2), (5.5, e3), (10.56, e4), (14.1, e5), (16.96, e6), (22.7, e7)]
PALABRAS_POR_SUBTITULO = 2
SFX = [(4.7, "pop"), (12.4, "ding"), (16.1, "pop"), (21.8, "ding")]
