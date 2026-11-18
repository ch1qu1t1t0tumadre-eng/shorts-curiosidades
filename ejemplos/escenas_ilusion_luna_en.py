"""v06 (EN): Why the Moon looks huge on the horizon — the Moon illusion + the pinky test."""
import math
from anim import *  # noqa

MOON_O = (1.0, 0.70, 0.35)      # rising moon, orange
MOON_W = (0.96, 0.95, 0.88)     # high moon, white
CITY = (0.06, 0.06, 0.14)
TEAL = (0.30, 0.85, 0.85)
EARTH_B = (0.20, 0.45, 0.85)


def bg_dusk(ctx, T):
    ctx.set_source(vgrad(ctx, 0, -400, 0, H, [(0, (0.10, 0.08, 0.28)), (0.65, (0.45, 0.20, 0.40)), (1, (0.95, 0.55, 0.35))]))
    ctx.paint()
    rng = np.random.default_rng(11)
    for _ in range(45):
        x, y, r = rng.uniform(-300, W + 300), rng.uniform(-400, 800), rng.uniform(1.5, 3.5)
        circle(ctx, x, y, r)
        fill(ctx, WHITE, 0.3 + 0.4 * (0.5 + 0.5 * math.sin(T * 2 + x)))


def moon(ctx, x, y, r, col=MOON_O, glow=1.0):
    if glow > 0:
        g = cairo.RadialGradient(x, y, r * 0.8, x, y, r * 2.0)
        g.add_color_stop_rgba(0, *col, 0.35 * glow)
        g.add_color_stop_rgba(1, *col, 0)
        ctx.set_source(g)
        circle(ctx, x, y, r * 2.0)
        ctx.fill()
    circle(ctx, x, y, r)
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgb(0, *[min(1, c * 1.08) for c in col])
    g.add_color_stop_rgb(1, *[c * 0.82 for c in col])
    ctx.set_source(g)
    ctx.fill()
    for dx, dy, rr in ((-0.35, -0.2, 0.18), (0.25, 0.1, 0.24), (-0.05, 0.45, 0.13), (0.4, -0.4, 0.1), (-0.5, 0.3, 0.09)):
        circle(ctx, x + dx * r, y + dy * r, rr * r)
        fill(ctx, tuple(c * 0.78 for c in col), 0.6)


def skyline(ctx, base, T, col=CITY):
    rng = np.random.default_rng(4)
    x = -300
    while x < W + 300:
        w = rng.uniform(70, 150)
        h = rng.uniform(120, 420)
        ctx.rectangle(x, base - h, w, h + 2000)
        fill(ctx, col)
        for wy in range(int(base - h + 30), int(base - 20), 50):
            for wx in range(int(x + 15), int(x + w - 20), 35):
                if rng.random() < 0.35:
                    ctx.rectangle(wx, wy, 14, 20)
                    fill(ctx, (1.0, 0.85, 0.45), 0.8)
        x += w + rng.uniform(4, 20)


def tree(ctx, x, base, s, col=CITY):
    rrect(ctx, x - 12 * s, base - 120 * s, 24 * s, 120 * s, 8 * s)
    fill(ctx, col)
    for dx, dy, r in ((0, -200, 90), (-60, -150, 70), (60, -150, 70), (0, -280, 60)):
        circle(ctx, x + dx * s, base + dy * s, r * s)
        fill(ctx, col)


def arm_pinky(ctx, tip_x, tip_y, s=1.0, ang=-1.2):
    """Arm with a clear 'pinky out' fist: thin short pinky at the OUTER edge, other fingers curled,
    thumb wrapped across. (tip_x, tip_y) = pinky tip."""
    ctx.save()
    ctx.translate(tip_x, tip_y)
    ctx.rotate(ang + math.pi / 2)
    ctx.scale(s, s)
    # forearm + sleeve (behind the fist)
    rrect(ctx, 30, 230, 150, 700, 65)
    fill(ctx, SKIN)
    rrect(ctx, 15, 500, 180, 620, 65)
    fill(ctx, BLUE)
    # pinky: thin, short, at the outer edge (x = 0 is the pinky line)
    rrect(ctx, -17, 0, 34, 130, 17)
    fill(ctx, SKIN)
    ctx.move_to(-10, 40)
    ctx.line_to(10, 40)
    stroke(ctx, SKIN_D, 4, 0.7)
    # fist, extending to the right of the pinky
    rrect(ctx, -30, 105, 250, 170, 70)
    fill(ctx, SKIN)
    # curled fingers (three knuckles) next to the pinky
    for k in range(3):
        rrect(ctx, 30 + k * 58, 108, 54, 92, 27)
        fill(ctx, SKIN_D, 0.55)
    # thumb wrapped across the front, far from the pinky
    rrect(ctx, 90, 200, 150, 52, 26)
    fill(ctx, SKIN_D)
    rrect(ctx, 95, 196, 140, 46, 23)
    fill(ctx, SKIN)
    ctx.restore()


def angle_marks(ctx, x, y, r, a=1.0, col=YELLOW):
    if a <= 0.01:
        return
    ctx.set_dash([16, 12])
    circle(ctx, x, y, r + 18)
    stroke(ctx, col, 6, a)
    ctx.set_dash([])
    for sx in (-1, 1):
        ctx.move_to(x + sx * (r + 18), y - 30)
        ctx.line_to(x + sx * (r + 18), y + 30)
        stroke(ctx, col, 6, a)


# ---------------- escenas ----------------
# 0.0 HOOK "That giant Moon on the horizon is not bigger. It's actually farther away."
def e1(ctx, lt, dur, T):
    z = keyframes(lt, [(0, 1.6), (0.4, 1.0), (dur, 1.1)])
    camera(ctx, z, W / 2, keyframes(lt, [(0, 1000), (dur, 950)]))
    bg_dusk(ctx, T)
    my = keyframes(lt, [(0, 1250), (2.2, 1000), (dur, 960)])
    moon(ctx, W / 2, my, 340)
    skyline(ctx, 1320, T)
    badge(ctx, "NOT BIGGER", W / 2, 360, pop(lt, 2.2), size=74)
    pill(ctx, "FARTHER AWAY", W / 2, 520, pop(lt, 3.8), rgb=YELLOW)


# 4.88 LOOP "Stay till the end, and you can prove it with one finger."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.2)]), W / 2, 900)
    bg_night(ctx, T)
    moon(ctx, 400, 760, 120, MOON_W)
    arm_pinky(ctx, keyframes(lt, [(0, 900), (1.2, 620)]), keyframes(lt, [(0, 1500), (1.2, 900)]), 1.0, -1.25)
    pill(ctx, "ONE FINGER TEST", W / 2, 330, pop(lt, 2.0), rgb=TEAL)
    text(ctx, "?", 250, 560, 160, YELLOW, a=pop(lt, 1.0), font=FONT_TITLE)


# 8.24 "When the Moon rises, it sits next to trees and buildings."
def e3(ctx, lt, dur, T):
    camera(ctx, 1.0, keyframes(lt, [(0, 380), (dur, 700)]), 980)
    bg_dusk(ctx, T)
    moon(ctx, 560, 1060, 230)
    skyline(ctx, 1320, T)
    for k, x in enumerate((90, 980, 1160)):
        tree(ctx, x, 1330, 1.2)
    pill(ctx, "TREES", 250, 640, pop(lt, 2.0), rgb=GREEN)
    pill(ctx, "BUILDINGS", 900, 640, pop(lt, 2.7), rgb=TEAL)
    arrow(ctx, 330, 700, 460, 900, ease((lt - 2.2) / 0.4), GREEN, 8)
    arrow(ctx, 800, 700, 680, 900, ease((lt - 2.9) / 0.4), TEAL, 8)


# 11.84 "Your brain thinks the horizon is very far away. And anything that far, looking that big... must be huge."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 900)
    ctx.set_source(vgrad(ctx, 0, 0, 0, 1000, [(0, (0.08, 0.08, 0.25)), (1, (0.40, 0.20, 0.42))]))
    ctx.paint()
    # perspective ground grid to the horizon
    hy = 960
    ctx.rectangle(-500, hy, W + 1000, 2000)
    fill(ctx, (0.12, 0.10, 0.25))
    for k in range(-12, 13):
        ctx.move_to(W / 2 + k * 18, hy)
        ctx.line_to(W / 2 + k * 260, H + 200)
        stroke(ctx, TEAL, 3, 0.35)
    for k in range(1, 9):
        yy = hy + (k / 8) ** 2 * 900
        ctx.move_to(-500, yy)
        ctx.line_to(W + 500, yy)
        stroke(ctx, TEAL, 3, 0.35)
    grow = ease((lt - 5.2) / 1.0)
    moon(ctx, W / 2, hy - 40, lerp(70, 210, grow))
    character(ctx, 230, 1180, 0.6, T, mood="duda" if lt < 5 else "sorpresa", body=True)
    pill(ctx, "VERY FAR", W / 2, 1120, pop(lt, 1.6), rgb=TEAL)
    arrow(ctx, W / 2, 1300, W / 2, 1010, ease((lt - 1.2) / 0.6), TEAL, 8)
    badge(ctx, "MUST BE HUGE", W / 2, 380, pop(lt, 6.0), size=66)


# 19.44 "So your brain inflates it."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    bg_night(ctx, T)
    pump = 0.5 + 0.5 * math.sin(lt * 9)
    r = lerp(150, 330, ease(lt / 1.5)) + 10 * pump
    moon(ctx, W / 2 + 120, 760, r)
    character(ctx, 260, 1080, 0.55, T, mood="feliz", body=True)
    # pump hose
    ctx.move_to(340, 1060)
    ctx.curve_to(450, 1000, W / 2 + 40, 1100, W / 2 + 120, 760 + r * 0.95)
    stroke(ctx, (0.85, 0.30, 0.35), 14)
    pill(ctx, "BRAIN ZOOM", W / 2, 320, pop(lt, 0.3), rgb=YELLOW)


# 21.30 GIRO "But here's the crazy part. At moonrise, the Moon is about four thousand miles farther from you than when it's high overhead."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (1.6, 1.0), (dur, 1.0)]), W / 2, 920)
    bg_night(ctx, T, grid=False)
    ex, ey, er = 300, 920, 210
    # earth
    circle(ctx, ex, ey, er)
    g = cairo.RadialGradient(ex - 60, ey - 60, 20, ex, ey, er)
    g.add_color_stop_rgb(0, 0.40, 0.70, 1.0)
    g.add_color_stop_rgb(1, 0.12, 0.30, 0.65)
    ctx.set_source(g)
    ctx.fill()
    for dx, dy, rx, ry in ((-60, -40, 80, 50), (70, 60, 60, 80), (-20, 110, 70, 35)):
        ellipse(ctx, ex + dx, ey + dy, rx, ry)
        fill(ctx, (0.30, 0.75, 0.40))
    mx, my = 900, 920
    moon(ctx, mx, my, 70, MOON_W, glow=0.6)
    # observer A at the top (Moon on horizon), observer B facing the Moon (overhead)
    ax, ay = ex, ey - er
    bx, by = ex + er, ey
    show_a = ease((lt - 1.8) / 0.6)
    show_b = ease((lt - 3.6) / 0.6)
    circle(ctx, ax, ay, 16)
    fill(ctx, YELLOW, show_a)
    circle(ctx, bx, by, 16)
    fill(ctx, GREEN, show_b)
    arrow(ctx, ax, ay, mx - 70, my - 10, show_a, YELLOW, 7, dashed=True)
    arrow(ctx, bx + 20, by, mx - 75, my, show_b, GREEN, 7)
    pill(ctx, "MOONRISE", ax, ay - 90, pop(lt, 2.0), size=36, rgb=YELLOW)
    pill(ctx, "OVERHEAD", 640, by + 110, pop(lt, 6.0), size=36, rgb=GREEN)
    badge(ctx, "+" + counter(lt - 3.0, 0, 4000, 1.4, "{:,.0f}") + " MILES", W / 2, 360, pop(lt, 3.0), size=62)
    pill(ctx, "1 EARTH RADIUS", W / 2, 1300, pop(lt, 4.6), rgb=TEAL)


# 28.56 CONSEJO "So here's the test. Tonight, stretch out your arm. Cover the rising Moon with your pinky."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dusk(ctx, T)
    moon(ctx, 460, 1030, 70)
    skyline(ctx, 1240, T)
    reach = ease((lt - 1.4) / 1.4)
    arm_pinky(ctx, lerp(900, 460, reach), lerp(1600, 985, reach), 0.9, -1.2)
    badge(ctx, "PINKY TEST", W / 2, 360, pop(lt, 0.3), size=70, bg=(0.20, 0.55, 0.85))
    pill(ctx, "ARM STRAIGHT", W / 2, 520, pop(lt, 1.9), rgb=TEAL)
    angle_marks(ctx, 460, 1030, 70, ease((lt - 3.6) / 0.4))


# 33.96 RESOLUCIÓN "Try again when it's high in the sky. Same size. Every time."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 920)
    bg_night(ctx, T)
    moon(ctx, 540, 640, 70, MOON_W)
    reach = ease((lt - 0.4) / 1.0) * (1 - ease((lt - 1.7) / 0.5))
    if reach > 0.01:
        arm_pinky(ctx, lerp(950, 540, reach), lerp(1700, 595, reach), 0.9, -1.35)
    angle_marks(ctx, 540, 640, 70, ease((lt - 1.4) / 0.4), GREEN)
    # two identical moons side by side
    if lt > 1.9:
        a = ease((lt - 1.9) / 0.4)
        moon(ctx, 300, 1180, 70 * a, MOON_O, glow=0)
        moon(ctx, 780, 1180, 70 * a, MOON_W, glow=0)
        text(ctx, "=", 540, 1180, 120, YELLOW, a=a, font=FONT_TITLE)
    badge(ctx, "SAME SIZE", W / 2, 360, pop(lt, 2.0), size=74, bg=(0.15, 0.65, 0.40))
    pill(ctx, "EVERY TIME", W / 2, 1340, pop(lt, 3.3), size=40, rgb=GREEN)


# 38.16 CTA "Did your brain fool you too? Follow for more hidden reasons behind everyday things."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_dusk(ctx, T)
    moon(ctx, 780, 560, 190)
    skyline(ctx, 1380, T)
    character(ctx, 380, 860, 0.85, T, mood="feliz", wave=1.0, shirt=(0.20, 0.55, 0.85))
    icon(ctx, "💬", 820, 960, 180, pop(lt, 0.3), rot=-0.12)
    pill(ctx, "FOOLED YOU?", W / 2, 320, pop(lt, 0.2), rgb=YELLOW)
    badge(ctx, "FOLLOW", W / 2, 1240, pop(lt, 1.6), size=72)


ESCENAS = [(0.0, e1), (4.88, e2), (8.24, e3), (11.84, e4), (19.44, e5), (21.30, e6), (28.56, e7),
           (33.96, e8), (38.16, e9)]
PALABRAS_POR_SUBTITULO = 2
SFX = [(2.2, "pop"), (17.84, "pop"), (24.3, "ding"), (36.0, "ding")]
