"""v14 (EN) FORMATO BUCLE: Paul the Octopus was never wrong (8/8, 2010 World Cup) and it got him death threats."""
import math
from anim import *  # noqa

OCTO = (0.96, 0.47, 0.30)
OCTO_D = (0.78, 0.30, 0.20)
OCTO_L = (1.0, 0.72, 0.55)
GOLDC = (1.0, 0.80, 0.25)
GOLD_D = (0.78, 0.55, 0.10)
AQUA = (0.25, 0.85, 0.85)
TEAL = (0.05, 0.38, 0.45)
DEEP = (0.02, 0.12, 0.22)
SAND = (0.93, 0.80, 0.55)
SAND_D = (0.78, 0.63, 0.38)
GER = [(0.08, 0.08, 0.08), (0.86, 0.10, 0.10), (1.0, 0.80, 0.0)]
ESP = [(0.78, 0.07, 0.12), (1.0, 0.77, 0.0), (1.0, 0.77, 0.0), (0.78, 0.07, 0.12)]
NED = [(0.70, 0.12, 0.16), (1, 1, 1), (0.13, 0.28, 0.55)]
FLAGS = {"GER": GER, "ESP": ESP, "NED": NED}


# ---------------- piezas ----------------
def bg_water(ctx, T, top=(0.05, 0.45, 0.55), bot=DEEP, rays=True, bubbles=True, seed=4):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, top), (1, bot)]))
    ctx.paint()
    if rays:  # haces de luz desde la superficie
        for k in range(6):
            x = -200 + k * 300 + 60 * math.sin(T * 0.4 + k)
            ctx.move_to(x, -700)
            ctx.line_to(x + 140, -700)
            ctx.line_to(x + 420, H + 600)
            ctx.line_to(x + 160, H + 600)
            ctx.close_path()
            fill(ctx, (0.75, 1.0, 1.0), 0.05 + 0.03 * math.sin(T * 0.8 + k * 1.7))
    if bubbles:
        rng = np.random.default_rng(seed)
        for _ in range(26):
            x0, r, sp = rng.uniform(-300, W + 300), rng.uniform(5, 18), rng.uniform(60, 160)
            y = (rng.uniform(0, 3000) - T * sp) % 3000 - 600
            x = x0 + 14 * math.sin(T * 2 + x0)
            circle(ctx, x, y, r)
            stroke(ctx, (0.85, 1, 1), 3, 0.45)
            circle(ctx, x - r * 0.3, y - r * 0.3, r * 0.25)
            fill(ctx, WHITE, 0.5)


def sand(ctx, y, T=0.0, extent=3000):
    ctx.move_to(-extent, y + 30)
    for k in range(-30, 31):
        ctx.line_to(W / 2 + k * 100, y + 18 * math.sin(k * 0.8) + 8 * math.sin(k * 2.1))
    ctx.line_to(extent, y + 30)
    ctx.line_to(extent, y + 2500)
    ctx.line_to(-extent, y + 2500)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, y - 30, 0, y + 600, [(0, SAND), (1, SAND_D)]))
    ctx.fill()
    rng = np.random.default_rng(9)
    for _ in range(30):
        ellipse(ctx, rng.uniform(-400, W + 400), y + rng.uniform(40, 600), rng.uniform(8, 26), rng.uniform(5, 12))
        fill(ctx, SAND_D, 0.7)


def seaweed(ctx, x, y, h, T, rgb=(0.15, 0.65, 0.40), w=26):
    ctx.move_to(x, y)
    n = 10
    for i in range(1, n + 1):
        f = i / n
        ctx.line_to(x + 40 * f * math.sin(T * 1.3 + f * 4 + x), y - h * f)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    stroke(ctx, rgb, w)


def rock(ctx, x, y, r, rgb=(0.35, 0.40, 0.48)):
    ctx.move_to(x - r, y)
    ctx.curve_to(x - r, y - r * 0.9, x + r * 0.8, y - r, x + r, y)
    ctx.close_path()
    fill(ctx, rgb)
    ellipse(ctx, x - r * 0.3, y - r * 0.55, r * 0.3, r * 0.12)
    fill(ctx, WHITE, 0.15)


def tank_frame(ctx, x0=60, y0=230, x1=1020, y1=1600):
    """Marco del acuario (cristal con bordes negros)."""
    rrect(ctx, x0, y0, x1 - x0, y1 - y0, 30)
    stroke(ctx, (0.05, 0.06, 0.08), 26)
    rrect(ctx, x0, y0, x1 - x0, y1 - y0, 30)
    stroke(ctx, (0.6, 0.85, 0.9), 4, 0.6)
    ctx.move_to(x0 + 40, y0 + 60)
    ctx.line_to(x0 + 140, y0 + 40)
    stroke(ctx, WHITE, 8, 0.4)


def flag(ctx, x, y, w, h, kind, wave=0.0, T=0.0):
    """Bandera de franjas horizontales (GER, ESP, NED). (x, y) = centro."""
    cols = FLAGS[kind]
    n = len(cols)
    ctx.save()
    ctx.translate(x, y)
    for i, c in enumerate(cols):
        y0 = -h / 2 + i * h / n
        ctx.move_to(-w / 2, y0)
        for k in range(0, 11):
            xx = -w / 2 + w * k / 10
            ctx.line_to(xx, y0 + wave * 8 * math.sin(T * 5 + k * 0.8) * (k / 10))
        for k in range(10, -1, -1):
            xx = -w / 2 + w * k / 10
            ctx.line_to(xx, y0 + h / n + wave * 8 * math.sin(T * 5 + k * 0.8) * (k / 10) + 0.5)
        ctx.close_path()
        fill(ctx, c)
    rrect(ctx, -w / 2, -h / 2, w, h, 4)
    stroke(ctx, (0, 0, 0), 4, 0.5)
    ctx.restore()


def mussel(ctx, x, y, s=1.0, rot=-0.3, open_=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    if open_ > 0:
        ellipse(ctx, 0, 0, 52, 22)
        fill(ctx, (1.0, 0.62, 0.35))
    for sgn in (1, -1) if open_ <= 0 else (-1,):
        ctx.move_to(-60, 0)
        ctx.curve_to(-40, -40 * sgn, 50, -36 * sgn, 64, 0)
        ctx.curve_to(40, 14 * sgn, -30, 14 * sgn, -60, 0)
        ctx.close_path()
        ctx.set_source(vgrad(ctx, 0, -40, 0, 40, [(0, (0.20, 0.24, 0.45)), (1, (0.06, 0.06, 0.14))]))
        ctx.fill()
    ctx.move_to(-40, -10)
    ctx.curve_to(-10, -26, 20, -26, 46, -8)
    stroke(ctx, WHITE, 4, 0.35)
    ctx.restore()


def food_box(ctx, x, y, s=1.0, kind="GER", lid=0.0, glow=0.0, T=0.0, mussel_out=0.0):
    """Caja de plástico transparente con un mejillón dentro y bandera delante. (x, y) = centro de la base."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, -130, 0, 0, -130, 300)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.6 * glow)
        g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        ctx.set_source(g)
        circle(ctx, 0, -130, 300)
        ctx.fill()
    soft_shadow(ctx, 0, 6, 150, 22, 0.3)
    # caja (cubo transparente)
    rrect(ctx, -130, -260, 260, 260, 18)
    fill_keep(ctx, (0.85, 0.97, 1.0), 0.22)
    stroke(ctx, (0.9, 1, 1), 6, 0.9)
    ctx.move_to(-130, -260); ctx.line_to(-90, -300); ctx.line_to(170, -300); ctx.line_to(130, -260)
    ctx.close_path()
    fill_keep(ctx, (0.85, 0.97, 1.0), 0.18)
    stroke(ctx, (0.9, 1, 1), 5, 0.8)
    ctx.move_to(130, -260); ctx.line_to(170, -300); ctx.line_to(170, -40); ctx.line_to(130, 0)
    stroke(ctx, (0.9, 1, 1), 5, 0.6)
    mussel(ctx, 0 + 60 * mussel_out, -120 - 220 * mussel_out, 1.0, -0.3 + 0.8 * mussel_out)
    # tapa (se abre girando)
    ctx.save()
    ctx.translate(-130, -268)
    ctx.rotate(-1.9 * ease(lid))
    rrect(ctx, 0, -14, 300, 28, 10)
    fill_keep(ctx, (0.9, 0.98, 1.0), 0.75)
    stroke(ctx, (0.6, 0.8, 0.9), 4)
    ctx.restore()
    # bandera pegada delante
    flag(ctx, 0, -60, 150, 90, kind, 0.0, T)
    ctx.move_to(-110, -230); ctx.line_to(-110, -150)
    stroke(ctx, WHITE, 10, 0.35)
    ctx.restore()


def _tentacle_pts(bx, by, a0, L, T, k, n=16, curl=1.0, reach=None, reach_p=0.0):
    pts = []
    x, y, a = bx, by, a0
    seg = L / n
    side = 1 if math.cos(a0) >= 0 else -1
    for i in range(n + 1):
        pts.append((x, y))
        f = i / n
        a += 0.10 * math.sin(T * 1.7 + k * 0.9 + i * 0.45) + side * curl * 0.05 * f * f * 3
        x += seg * math.cos(a)
        y += seg * math.sin(a)
    if reach is not None and reach_p > 0:
        tx, ty = reach
        p = ease(reach_p)
        out = []
        for i, (px, py) in enumerate(pts):
            f = i / n
            lx, ly = lerp(bx, tx, f), lerp(by, ty, f) - 60 * math.sin(f * math.pi)
            out.append((lerp(px, lx, p), lerp(py, ly, p)))
        pts = out
    return pts


def _draw_tentacle(ctx, pts, w0, w1, rgb, rgb_d, suckers=True):
    n = len(pts) - 1
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        j0, j1 = max(i - 1, 0), min(i + 1, n)
        dx, dy = pts[j1][0] - pts[j0][0], pts[j1][1] - pts[j0][1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = lerp(w0, w1, i / n) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    ctx.move_to(*left[0])
    for p in left[1:]:
        ctx.line_to(*p)
    ex, ey = pts[-1]
    ctx.line_to(ex, ey)
    for p in reversed(right):
        ctx.line_to(*p)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, pts[0][1] - 50, 0, pts[-1][1] + 50, [(0, rgb), (1, rgb_d)]))
    ctx.fill()
    if suckers:
        for i in range(2, n, 2):
            sx, sy = right[i]
            circle(ctx, lerp(sx, pts[i][0], 0.35), lerp(sy, pts[i][1], 0.35), lerp(w0, w1, i / n) * 0.2)
            fill(ctx, OCTO_L if rgb == OCTO else (1, 0.95, 0.7))


def octopus(ctx, x, y, s=1.0, T=0.0, mood="normal", look=(0, 0), reach=None, reach_p=0.0, gold=False,
            glow=0.0, hug=None, alpha_dim=0.0):
    """Pulpo (Paul). (x, y) = centro de la cabeza; cabeza de ~200 de ancho*s. reach=(x, y) en coordenadas del mundo."""
    body, body_d = (GOLDC, GOLD_D) if gold else (OCTO, OCTO_D)
    if glow > 0:
        g = cairo.RadialGradient(x, y + 100 * s, 0, x, y + 100 * s, 520 * s)
        g.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.45 * glow)
        g.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
        ctx.set_source(g)
        circle(ctx, x, y + 100 * s, 520 * s)
        ctx.fill()
    bob = 10 * s * math.sin(T * 1.4)
    yy = y + bob
    # tentáculos (8): los de atrás primero
    order = [0, 7, 1, 6, 2, 5, 3, 4]
    for k in order:
        a0 = math.pi / 2 + (k - 3.5) * 0.36
        bx = x + (k - 3.5) * 34 * s
        by = yy + 120 * s
        L = 430 * s
        r = reach if (k == 5 and reach is not None) else None
        if hug is not None and k in (2, 5):
            continue
        pts = _tentacle_pts(bx, by, a0, L, T, k, curl=1.0, reach=r, reach_p=reach_p if r else 0.0)
        shade = 0.85 if k in (0, 7, 1, 6) else 1.0
        _draw_tentacle(ctx, pts, 86 * s, 14 * s, tuple(c * shade for c in body), tuple(c * shade for c in body_d))
    # cabeza (manto)
    ctx.move_to(x - 150 * s, yy + 110 * s)
    ctx.curve_to(x - 230 * s, yy - 60 * s, x - 170 * s, yy - 330 * s, x, yy - 330 * s)
    ctx.curve_to(x + 170 * s, yy - 330 * s, x + 230 * s, yy - 60 * s, x + 150 * s, yy + 110 * s)
    ctx.curve_to(x + 80 * s, yy + 160 * s, x - 80 * s, yy + 160 * s, x - 150 * s, yy + 110 * s)
    ctx.close_path()
    g = cairo.RadialGradient(x - 60 * s, yy - 200 * s, 20 * s, x, yy - 60 * s, 280 * s)
    g.add_color_stop_rgb(0, *(1.0, 0.92, 0.6) if gold else OCTO_L)
    g.add_color_stop_rgb(0.5, *body)
    g.add_color_stop_rgb(1, *body_d)
    ctx.set_source(g)
    ctx.fill()
    # manchas
    for dx, dy, r in ((-70, -230, 22), (60, -260, 16), (95, -170, 26), (-110, -120, 14), (20, -190, 12)):
        circle(ctx, x + dx * s, yy + dy * s, r * s)
        fill(ctx, body_d, 0.5)
    ellipse(ctx, x - 70 * s, yy - 250 * s, 50 * s, 26 * s)
    fill(ctx, WHITE, 0.35)
    # ojos
    big = 1.2 if mood == "sorpresa" else 1.0
    blink = 1.0
    ph = T % 4.1
    if ph < 0.12:
        blink = abs(ph - 0.06) / 0.06
    for sx in (-1, 1):
        ex, ey = x + sx * 72 * s, yy + 20 * s
        if mood == "dormido" or blink < 0.15:
            ctx.move_to(ex - 36 * s, ey)
            ctx.curve_to(ex - 15 * s, ey + 20 * s, ex + 15 * s, ey + 20 * s, ex + 36 * s, ey)
            stroke(ctx, (0.3, 0.08, 0.05), 9 * s)
        else:
            ellipse(ctx, ex, ey, 48 * s * big, 54 * s * big * blink)
            fill(ctx, WHITE)
            px, py = ex + look[0] * 14 * s, ey + look[1] * 14 * s
            circle(ctx, px, py, 26 * s * big)
            fill(ctx, (0.1, 0.06, 0.05))
            circle(ctx, px + 9 * s, py - 10 * s, 9 * s)
            fill(ctx, WHITE)
        if mood == "duda" or mood == "sorpresa":
            ctx.move_to(ex - 30 * s, ey - 75 * s - (sx > 0) * 12 * s)
            ctx.line_to(ex + 30 * s, ey - 80 * s)
            stroke(ctx, body_d, 10 * s)
    # mejillas + boca
    for sx in (-1, 1):
        circle(ctx, x + sx * 125 * s, yy + 75 * s, 22 * s)
        fill(ctx, (1, 0.45, 0.45), 0.45)
    if mood == "sorpresa":
        ellipse(ctx, x, yy + 105 * s, 20 * s, 26 * s)
        fill(ctx, (0.4, 0.08, 0.08))
    elif mood != "dormido":
        ctx.move_to(x - 30 * s, yy + 95 * s)
        ctx.curve_to(x - 10 * s, yy + 118 * s, x + 10 * s, yy + 118 * s, x + 30 * s, yy + 95 * s)
        stroke(ctx, (0.4, 0.1, 0.08), 8 * s)
    if alpha_dim > 0:
        pass


def soccer_ball(ctx, x, y, r, rot=0.0, gold=False, cut=False):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    base = (1.0, 0.88, 0.45) if gold else (0.97, 0.97, 0.97)
    dark = GOLD_D if gold else (0.08, 0.08, 0.10)
    circle(ctx, 0, 0, r)
    g = cairo.RadialGradient(-r * 0.35, -r * 0.4, r * 0.1, 0, 0, r)
    g.add_color_stop_rgb(0, 1, 1, 1)
    g.add_color_stop_rgb(1, *(c * 0.8 for c in base))
    ctx.set_source(g)
    ctx.fill()
    ctx.save()
    circle(ctx, 0, 0, r)
    ctx.clip()

    def pent(cx, cy, pr, a):
        for i in range(5):
            ang = a + i * math.tau / 5 - math.pi / 2
            (ctx.move_to if i == 0 else ctx.line_to)(cx + pr * math.cos(ang), cy + pr * math.sin(ang))
        ctx.close_path()
        fill(ctx, dark)
    pent(0, 0, r * 0.32, 0)
    for i in range(5):
        ang = i * math.tau / 5 - math.pi / 2
        ctx.move_to(r * 0.32 * math.cos(ang), r * 0.32 * math.sin(ang))
        ctx.line_to(r * 0.72 * math.cos(ang), r * 0.72 * math.sin(ang))
        stroke(ctx, dark, r * 0.04)
        ang2 = ang + math.tau / 10
        pent(r * 0.95 * math.cos(ang2), r * 0.95 * math.sin(ang2), r * 0.3, ang2 + math.pi)
    ctx.restore()
    circle(ctx, 0, 0, r)
    stroke(ctx, (0, 0, 0), r * 0.04, 0.5)
    ctx.restore()


def urn(ctx, x, y, s=1.0, glow=0.0):
    """Urna dorada con forma de pulpo (simplificada)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 220)
        g.add_color_stop_rgba(0, 1, 0.85, 0.3, 0.7 * glow)
        g.add_color_stop_rgba(1, 1, 0.85, 0.3, 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, 220)
        ctx.fill()
    for k in range(5):
        ctx.move_to(-50 + k * 25, 20)
        ctx.curve_to(-70 + k * 35, 60, -50 + k * 25, 90, -60 + k * 30, 100)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        stroke(ctx, GOLD_D, 16)
    ellipse(ctx, 0, -20, 70, 80)
    ctx.set_source(vgrad(ctx, 0, -100, 0, 60, [(0, (1, 0.95, 0.6)), (1, GOLD_D)]))
    ctx.fill()
    for sx in (-1, 1):
        circle(ctx, sx * 24, 0, 10)
        fill(ctx, (0.45, 0.30, 0.05))
    ellipse(ctx, -24, -60, 18, 10)
    fill(ctx, WHITE, 0.6)
    ctx.restore()


def fan(ctx, x, y, s=1.0, T=0.0, rgb=(0.10, 0.10, 0.14), arm=1.0, k=0):
    """Silueta genérica de aficionado enfadado (puño en alto)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    up = 20 * math.sin(T * 7 + k * 1.3)
    circle(ctx, 0, -230, 70)
    fill(ctx, rgb)
    rrect(ctx, -95, -160, 190, 300, 70)
    fill(ctx, rgb)
    ctx.move_to(60, -120)
    ctx.line_to(120, -260 - up * arm)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    stroke(ctx, rgb, 46)
    circle(ctx, 125, -280 - up * arm, 34)
    fill(ctx, rgb)
    # bufanda (colores de Alemania)
    for i, c in enumerate(GER):
        ctx.rectangle(-80, -165 + i * 14, 160, 14)
        fill(ctx, c)
    ctx.restore()


def checkmark(ctx, x, y, r, a=1.0, rgb=GREEN):
    if a <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(a, a)
    circle(ctx, 0, 0, r)
    fill_keep(ctx, rgb)
    stroke(ctx, WHITE, 5)
    ctx.move_to(-r * 0.45, 0)
    ctx.line_to(-r * 0.1, r * 0.35)
    ctx.line_to(r * 0.5, -r * 0.35)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    stroke(ctx, WHITE, r * 0.22)
    ctx.restore()


def underwater_set(ctx, T, sand_y=1420):
    bg_water(ctx, T)
    seaweed(ctx, 110, sand_y + 20, 420, T)
    seaweed(ctx, 160, sand_y + 30, 300, T + 1, (0.10, 0.55, 0.35))
    seaweed(ctx, 960, sand_y + 20, 380, T + 2)
    sand(ctx, sand_y, T)
    rock(ctx, 880, sand_y + 40, 110)
    rock(ctx, 230, sand_y + 50, 80, (0.30, 0.34, 0.42))


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): Paul sobre las dos cajas, ficha abajo."""
    camera(ctx, zoom, W / 2, 900)
    underwater_set(ctx, T)
    food_box(ctx, 290, 1440, 0.85, "GER", T=T)
    food_box(ctx, 790, 1440, 0.85, "ESP", T=T, glow=0.6 + 0.3 * math.sin(T * 3))
    octopus(ctx, W / 2, 560, 1.0, T, look=(0.5, 0.6), glow=0.5)
    tank_frame(ctx, -20, 160, 1100, 1700)
    ctx.restore()
    ctx.save()
    ficha(ctx, "PAUL THE OCTOPUS", "WORLD CUP ORACLE · 2008–2010", W / 2, 1640, 1.0, "🐙", AQUA, w=900)


# ---------------- escenas (subtítulo gigante en y≈1060: dejar libre ~950–1170) ----------------
# 0.00 "Paul the Octopus was never wrong, and it got him"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.1)]))


# 2.58 "death threats. And it's real."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.4, 1.05), (dur, 1.0)]) + 0.006 * math.sin(T * 45) * (lt < 0.5),
           W / 2, 820)
    bg_water(ctx, T, (0.25, 0.05, 0.08), (0.06, 0.02, 0.05))
    for k in range(14):
        ctx.save(); ctx.translate(W / 2, 640); ctx.rotate(k * math.pi / 7 + T * 0.15)
        ctx.move_to(0, 0); ctx.line_to(1500, -100); ctx.line_to(1500, 100); ctx.close_path()
        fill(ctx, RED, 0.07); ctx.restore()
    octopus(ctx, W / 2, 560, 1.05, T, mood="sorpresa")
    icon(ctx, "📰", 190, 330, 190, pop(lt, 0.05), rot=-0.2)
    icon(ctx, "😡", 900, 360, 170, pop(lt, 0.25), rot=0.15)
    badge(ctx, "DEATH THREATS", W / 2, 1310, pop(lt, 0.1), size=66)
    pill(ctx, "TRUE STORY", W / 2, 1470, pop(lt, 1.0), size=50, rgb=GREEN)


# 4.33 "Summer 2010, Sea Life Oberhausen, Germany."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), keyframes(lt, [(0, W / 2 - 40), (dur, W / 2 + 40)]), 820)
    bg_sky(ctx, T, 0.25)
    sun(ctx, 860, 330, 90, T)
    ground(ctx, 1250, (0.35, 0.60, 0.35))
    # edificio del acuario
    rrect(ctx, 170, 640, 740, 610, 30)
    ctx.set_source(vgrad(ctx, 0, 640, 0, 1250, [(0, (0.20, 0.55, 0.75)), (1, (0.10, 0.32, 0.50))]))
    ctx.fill()
    ctx.arc(W / 2, 660, 300, math.pi, 0)
    ctx.close_path()
    fill(ctx, (0.15, 0.45, 0.65))
    for i in range(4):  # ventanas-ola
        rrect(ctx, 230 + i * 160, 860, 120, 160, 20)
        fill(ctx, (0.55, 0.90, 0.95), 0.8)
    rrect(ctx, 470, 1070, 140, 180, 16)
    fill(ctx, (0.08, 0.15, 0.25))
    octopus(ctx, W / 2, 520, 0.42, T)  # cartel del pulpo en el tejado
    flag(ctx, 220, 470, 170, 105, "GER", 1.0, T)
    ctx.move_to(135, 420); ctx.line_to(135, 640)
    stroke(ctx, (0.3, 0.3, 0.3), 8)
    pill(ctx, counter(lt, 2000, 2010, 0.7), W / 2, 300, pop(lt, 0.0), size=86, rgb=YELLOW, sub="SUMMER")
    pill(ctx, "SEA LIFE OBERHAUSEN", W / 2, 1390, pop(lt, 0.9), size=46, rgb=AQUA, sub="GERMANY")


# 6.93 "Before every World Cup match,"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 820)
    ctx.set_source(vgrad(ctx, 0, -300, 0, H + 300, [(0, (0.05, 0.30, 0.12)), (1, (0.02, 0.12, 0.05))]))
    ctx.paint()
    for k in range(-6, 8):  # franjas del césped
        ctx.rectangle(-400, 200 + k * 180, W + 800, 90)
        fill(ctx, WHITE, 0.04)
    ctx.arc(W / 2, 1400, 260, 0, math.tau)
    stroke(ctx, WHITE, 8, 0.5)
    ctx.move_to(-400, 1400); ctx.line_to(W + 400, 1400)
    stroke(ctx, WHITE, 8, 0.5)
    yb = 640 + 40 * abs(math.sin(T * 3))
    soccer_ball(ctx, W / 2, yb, 200, T * 1.2)
    icon(ctx, "🏆", 860, 340, 200, pop(lt, 0.3))
    pill(ctx, "WORLD CUP 2010", W / 2, 1300, pop(lt, 0.25), size=58, rgb=YELLOW, sub="SOUTH AFRICA")


# 8.32 "keepers drop two boxes into Paul's tank."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.06)]), W / 2, keyframes(lt, [(0, 820), (dur, 900)]))
    underwater_set(ctx, T)
    octopus(ctx, W / 2, 600, 0.75, T, look=(0, -1), mood="duda")
    for i, (bx, kind) in enumerate(((290, "GER"), (790, "ESP"))):
        d = ease_out(clamp((lt - 0.15 - i * 0.25) / 1.1))
        by = lerp(-200, 1440, d)
        food_box(ctx, bx, by, 0.8, kind, T=T)
        if d < 1:  # cuerda
            ctx.move_to(bx, by - 260)
            ctx.line_to(bx, -800)
            stroke(ctx, WHITE, 5, 0.6)
    tank_frame(ctx, -20, 160, 1100, 1700)
    pill(ctx, "2 BOXES", W / 2, 300, pop(lt, 0.4), size=54, rgb=AQUA)


# 10.44 "Each box holds a mussel and a team flag."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (dur, 1.1)]), W / 2, keyframes(lt, [(0, 700), (dur, 760)]))
    underwater_set(ctx, T, 1300)
    food_box(ctx, W / 2, 1250, 1.9, "GER", T=T, glow=0.4)
    pill(ctx, "MUSSEL", 280, 420, pop(lt, 0.6), size=50, rgb=AQUA)
    arrow(ctx, 330, 480, 470, 640, ease((lt - 0.7) / 0.4), AQUA, 8)
    pill(ctx, "TEAM FLAG", 800, 1430, pop(lt, 1.45), size=50, rgb=YELLOW)


# 12.55 "Whichever box Paul opens first, that team wins."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 860)
    underwater_set(ctx, T)
    lid = clamp((lt - 1.1) / 0.6)
    food_box(ctx, 290, 1440, 0.85, "GER", T=T)
    food_box(ctx, 790, 1440, 0.85, "ESP", T=T, lid=lid, glow=lid)
    octopus(ctx, W / 2, 520, 0.85, T, look=(0.7, 0.8), reach=(780, 1170), reach_p=clamp(lt / 1.1))
    tank_frame(ctx, -20, 160, 1100, 1700)
    badge(ctx, "OPENS FIRST = WINNER", W / 2, 260, pop(lt, 1.8), size=46, bg=(0.05, 0.55, 0.55))
    character(ctx, 150, 1250, 0.38, T, mood="duda", body=False, look=(1, -0.5))


# 15.11 "Germany plays seven matches. Paul calls every single one."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 0.97)]), W / 2, 860)
    bg_water(ctx, T, (0.04, 0.22, 0.32), (0.02, 0.07, 0.14), rays=True)
    flag(ctx, W / 2, 330, 240, 144, "GER", 1.0, T)
    text(ctx, "GERMANY · 2010", W / 2, 470, 44, WHITE)
    opp = ["🇦🇺", "🇷🇸", "🇬🇭", "🏴\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "🇦🇷", "🇪🇸", "🇺🇾"]
    names = ["AUS", "SRB", "GHA", "ENG", "ARG", "ESP", "URU"]
    for i, (e, nm) in enumerate(zip(opp, names)):
        r, c = divmod(i, 4)
        x = 180 + c * 240 + (120 if r == 1 else 0)
        y = 650 + r * 720
        a = pop(lt, 0.15 + i * 0.18)
        icon(ctx, e, x, y, 210, a)
        text(ctx, nm, x, y + 120, 38, WHITE, a)
        checkmark(ctx, x + 60, y - 55, 34, pop(lt, 1.65 + i * 0.16))
    pill(ctx, counter(clamp(lt - 1.6, 0, 9), 0, 7, 1.1, "{:.0f} / 7"), W / 2, 1520, pop(lt, 1.6), size=70, rgb=GREEN,
         sub="CORRECT")
    octopus(ctx, 900, 1660, 0.35, T, mood="normal", look=(-1, -1))


# 18.31 "Even the semifinal, where he picks Spain. Spain wins."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.12), (dur, 1.0)]), keyframes(lt, [(0, 620), (dur, W / 2)]), 880)
    underwater_set(ctx, T)
    lid = clamp((lt - 0.9) / 0.5)
    food_box(ctx, 290, 1440, 0.85, "GER", T=T)
    food_box(ctx, 790, 1440, 0.85, "ESP", T=T, lid=lid, glow=lid, mussel_out=clamp((lt - 1.3) / 0.6) * 0.0)
    octopus(ctx, 700, 560, 0.85, T, look=(0.4, 1), reach=(790, 1180), reach_p=clamp(lt / 0.9))
    pill(ctx, "SEMIFINAL", W / 2, 280, pop(lt, 0.0), size=54, rgb=YELLOW)
    badge(ctx, "SPAIN 1–0 GERMANY", W / 2, 1530, pop(lt, 1.8), size=50, bg=(0.78, 0.07, 0.12))


# 20.83 "In other words, an octopus predicted Germany's defeat."  (2.º gancho: golpe de zoom)
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.6), (0.3, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 860)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.10, 0.03, 0.10)), (1, (0.02, 0.02, 0.08))]))
    ctx.paint()
    for k in range(16):
        ctx.save(); ctx.translate(W / 2, 620); ctx.rotate(k * math.pi / 8 + T * 0.2)
        ctx.move_to(0, 0); ctx.line_to(1400, -90); ctx.line_to(1400, 90); ctx.close_path()
        fill(ctx, YELLOW, 0.06); ctx.restore()
    octopus(ctx, W / 2, 560, 1.15, T, glow=1.0, look=(0, 0.3))
    flag(ctx, 790, 1340, 200, 120, "GER", 1.0, T)
    cross_a = pop(lt, 1.6)
    if cross_a > 0.01:
        for sgn in (1, -1):
            ctx.move_to(790 - 120 * cross_a, 1340 - sgn * 80 * cross_a)
            ctx.line_to(790 + 120 * cross_a, 1340 + sgn * 80 * cross_a)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            stroke(ctx, RED, 26)
    character(ctx, 230, 1360, 0.55, T, mood="sorpresa", body=True)
    badge(ctx, "AN OCTOPUS!", W / 2, 270, pop(lt, 0.9), size=60, bg=PURPLE)


# 23.81 "Angry German fans want Paul grilled, fried, or turned into sushi."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, keyframes(lt, [(0, 900), (dur, 820)]))
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.30, 0.06, 0.06)), (1, (0.08, 0.02, 0.04))]))
    ctx.paint()
    for i in range(7):  # gradas de aficionados
        fan(ctx, 80 + i * 155, 1600 + 30 * (i % 2), 0.9, T, k=i)
    octopus(ctx, W / 2, 520, 0.7, T, mood="sorpresa")
    icon(ctx, "🔥", 190, 330, 190, pop(lt, 1.35))
    pill(ctx, "GRILLED", 190, 470, pop(lt, 1.35), size=40, rgb=RED)
    icon(ctx, "🍳", 890, 330, 190, pop(lt, 1.95))
    pill(ctx, "FRIED", 890, 470, pop(lt, 1.95), size=40, rgb=RED)
    icon(ctx, "🍣", W / 2, 1340, 200, pop(lt, 2.85))
    pill(ctx, "SUSHI", W / 2, 1220, pop(lt, 2.85), size=40, rgb=RED)


# 27.40 "Spain's prime minister offers him protection."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 860)
    bg_water(ctx, T, (0.30, 0.12, 0.05), (0.08, 0.04, 0.06))
    flag(ctx, W / 2, 380, 760, 380, "ESP", 1.0, T)
    # escudo protector (burbuja)
    sh = ease(clamp((lt - 1.0) / 0.6))
    octopus(ctx, W / 2, 640, 0.6, T, look=(0, -0.6))
    if sh > 0:
        circle(ctx, W / 2, 700, 320 * sh)
        fill_keep(ctx, AQUA, 0.15)
        stroke(ctx, AQUA, 10, 0.9)
        icon(ctx, "🛡️", 860, 880, 170, sh)
    ficha(ctx, "JOSÉ LUIS ZAPATERO", "SPAIN'S PRIME MINISTER · 2004–2011", W / 2, 1380, pop(lt, 0.0), "🇪🇸",
          YELLOW, w=940)
    pill(ctx, "PROTECTION", W / 2, 1560, pop(lt, 1.1), size=44, rgb=AQUA)


# 29.28 "Paul picks Spain for the final too. Eight for eight."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (1.6, 1.1), (1.7, 1.2), (dur, 1.12)]), W / 2, 860)
    underwater_set(ctx, T)
    lid = clamp((lt - 0.7) / 0.5)
    food_box(ctx, 290, 1440, 0.85, "NED", T=T)
    food_box(ctx, 790, 1440, 0.85, "ESP", T=T, lid=lid, glow=lid)
    octopus(ctx, W / 2, 560, 0.85, T, look=(0.6, 1), reach=(780, 1170), reach_p=clamp(lt / 0.7))
    pill(ctx, "THE FINAL", 260, 280, pop(lt, 0.0), size=46, rgb=YELLOW)
    icon(ctx, "🏆", 860, 290, 150, pop(lt, 0.2))
    tank_frame(ctx, -20, 160, 1100, 1700)
    a = pop(lt, 1.6)
    if a > 0.01:
        pill(ctx, "8 / 8", W / 2, 760, a, size=130, rgb=GREEN, sub="NEVER WRONG")


# 31.68 "That October, he dies in his tank."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 880)
    bg_water(ctx, T, (0.06, 0.12, 0.18), (0.01, 0.03, 0.06), rays=False)
    seaweed(ctx, 140, 1440, 300, T * 0.4, (0.15, 0.30, 0.25))
    sand(ctx, 1420, T)
    ctx.rectangle(-500, -500, W + 1000, H + 1000)
    fill(ctx, (0.0, 0.02, 0.06), 0.35)
    octopus(ctx, W / 2, 900 + 20 * clamp(lt / dur), 0.75, T * 0.3, mood="dormido")
    ctx.save(); ctx.translate(W / 2, 560); ctx.scale(1, 0.25); ctx.arc(0, 0, 150, 0, math.tau); ctx.restore()
    stroke(ctx, GOLDC, 12, 0.85 * pop(lt, 0.8))
    ctx.new_path()
    pill(ctx, "OCTOBER 2010", W / 2, 300, pop(lt, 0.1), size=56, rgb=(0.7, 0.75, 0.85))
    pill(ctx, "AGE: ~2.5 YEARS", W / 2, 1440, pop(lt, 1.0), size=40, rgb=(0.7, 0.75, 0.85))
    character(ctx, 900, 1300, 0.35, T, mood="duda", body=False, look=(-1, 0))


# 33.41 "In 2011, Paul's ashes are sealed inside a soccer ball,"
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.18)]), W / 2, keyframes(lt, [(0, 860), (dur, 760)]))
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.12, 0.10, 0.20)), (1, (0.04, 0.04, 0.10))]))
    ctx.paint()
    g = cairo.RadialGradient(W / 2, 680, 0, W / 2, 680, 600)
    g.add_color_stop_rgba(0, 1, 0.85, 0.4, 0.35)
    g.add_color_stop_rgba(1, 1, 0.85, 0.4, 0)
    ctx.set_source(g)
    ctx.paint()
    soccer_ball(ctx, W / 2, 680, 300, 0.1 * math.sin(T))
    # el balón se vuelve transparente y deja ver la urna
    xr = clamp((lt - 1.0) / 0.8)
    if xr > 0:
        circle(ctx, W / 2, 680, 300)
        fill(ctx, (0.08, 0.08, 0.16), 0.75 * xr)
        circle(ctx, W / 2, 680, 300)
        stroke(ctx, GOLDC, 8, xr)
        urn(ctx, W / 2, 680, 1.3 * xr + 0.01, glow=xr)
    pill(ctx, counter(lt, 2010, 2011, 0.5), W / 2, 280, pop(lt, 0.0), size=80, rgb=GOLDC)
    pill(ctx, "ASHES INSIDE", W / 2, 1400, pop(lt, 1.3), size=52, rgb=GOLDC, sub="GOLDEN URN")


# 36.39 "hugged by a six-foot octopus."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 0.98)]), W / 2, keyframes(lt, [(0, 760), (dur, 880)]))
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.08, 0.30, 0.38)), (1, (0.03, 0.10, 0.16))]))
    ctx.paint()
    ctx.rectangle(-500, 1400, W + 1000, 900)
    fill(ctx, (0.25, 0.25, 0.30))
    rrect(ctx, 260, 1300, 560, 140, 14)  # pedestal
    fill(ctx, (0.55, 0.55, 0.60))
    octopus(ctx, 560, 470, 0.95, 0.0, look=(0, 0.2), hug=(560, 1060, 170), glow=0.4)
    soccer_ball(ctx, 560, 1060, 170, 0.2)
    # para que los tentáculos del abrazo queden delante del balón
    for sgn in (-1, 1):
        ctx.move_to(560 + sgn * 170 * 1.05, 1060 - 40)
        ctx.curve_to(560 + sgn * 170 * 0.9, 1060 + 130, 560 + sgn * 60, 1060 + 120, 560 + sgn * 10, 1060 + 90)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        stroke(ctx, OCTO_D, 56)
        ctx.move_to(560 + sgn * 170 * 1.05, 1060 - 40)
        ctx.curve_to(560 + sgn * 170 * 0.9, 1060 + 130, 560 + sgn * 60, 1060 + 120, 560 + sgn * 10, 1060 + 90)
        stroke(ctx, OCTO, 42)
    # regla de altura
    a = ease(clamp((lt - 0.3) / 0.6))
    ctx.move_to(950, 1400); ctx.line_to(950, lerp(1400, 160, a))
    stroke(ctx, YELLOW, 8)
    for k in range(7):
        yk = 1400 - k * (1240 / 6)
        if yk >= lerp(1400, 160, a) - 1:
            ctx.move_to(925, yk); ctx.line_to(975, yk)
            stroke(ctx, YELLOW, 6)
    pill(ctx, "6 FT", 950, 120 + 40, pop(lt, 0.9), size=50, rgb=YELLOW)
    character(ctx, 160, 1240, 0.42, T, mood="sorpresa", body=True, look=(1, -1))


# 38.11 "All because, in 2010" -> vuelve a e1
def e17(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.92), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.58, e2), (4.33, e3), (6.93, e4), (8.32, e5), (10.44, e6), (12.55, e7), (15.11, e8),
           (18.31, e9), (20.83, e10), (23.81, e11), (27.40, e12), (29.28, e13), (31.68, e14), (33.41, e15),
           (36.39, e16), (38.11, e17)]
SFX = [(2.62, "pop"), (16.75, "ding"), (20.90, "pop"), (30.90, "ding")]


# ---------------- miniatura (no desvela que acertó todo ni lo de las amenazas) ----------------
def MINIATURA(ctx):
    T = 1.3
    ctx.save()
    camera(ctx, 1.0, W / 2, 960)
    underwater_set(ctx, T, 1500)
    food_box(ctx, 290, 1520, 0.9, "GER", T=T)
    food_box(ctx, 790, 1520, 0.9, "ESP", T=T, glow=0.9)
    octopus(ctx, W / 2, 860, 0.95, T, look=(0.6, 0.8), glow=0.6)
    tank_frame(ctx, -20, 160, 1100, 1800)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_circle(ctx, 790, 1400, 200, 210)
    thumb_arrow(ctx, 560, 1180, 690, 1300)
    thumb_text(ctx, ["NEVER WRONG", ("ONCE?", WHITE)], y=270, size=150)
