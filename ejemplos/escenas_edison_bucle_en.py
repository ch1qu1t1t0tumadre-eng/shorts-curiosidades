"""v10 (EN) FORMATO BUCLE: Thomas Edison's last breath is sealed in a test tube in Michigan."""
import math
from anim import *  # noqa

GLASS = (0.75, 0.88, 1.0)
WAX = (0.80, 0.12, 0.14)
BREATH = (0.65, 0.95, 1.0)
WOOD = (0.45, 0.28, 0.16)
WOOD_D = (0.32, 0.19, 0.10)
GOLD = (1.0, 0.78, 0.30)
TEAL = (0.30, 0.85, 0.85)


# ---------------- piezas ----------------
def bg_lab(ctx, T, hue=0.0):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, (0.05 + hue, 0.06, 0.16)), (0.55, (0.10, 0.12, 0.28)),
                                                     (1, (0.03, 0.03, 0.08))]))
    ctx.paint()
    rng = np.random.default_rng(3)
    for _ in range(40):  # motas de polvo flotando
        x, y, r = rng.uniform(-400, W + 400), rng.uniform(-600, H + 600), rng.uniform(2, 5)
        y = (y - T * 25 * rng.uniform(0.5, 1.5)) % (H + 1200) - 600
        circle(ctx, x, y, r)
        fill(ctx, WHITE, 0.10 + 0.10 * math.sin(T * 1.7 + x))


def spotlight(ctx, x, y, r, a=0.5, col=(1, 0.95, 0.8)):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a)
    g.add_color_stop_rgba(1, *col, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


def wisp(ctx, x, y, w, h, T, a=1.0):
    """'Aliento' dentro del tubo: volutas brillantes que se mueven."""
    if a <= 0.01:
        return
    for k in range(4):
        ctx.move_to(x + math.sin(T * 2 + k) * w * 0.25, y + h * 0.5)
        for j in range(1, 13):
            yy = y + h * 0.5 - h * j / 12
            xx = x + math.sin(T * 2.4 + j * 0.7 + k * 1.6) * w * (0.18 + 0.05 * k)
            ctx.line_to(xx, yy)
        stroke(ctx, BREATH, 6 - k, a * (0.55 - k * 0.1))
    spotlight(ctx, x, y, w * 0.9, 0.25 * a, BREATH)


def tube(ctx, x, y, s=1.0, T=0.0, wax=1.0, breath=0.0, label=None, glow=0.0, tilt=0.0):
    """Tubo de ensayo vertical. (x, y) = centro; alto 700*s, ancho 150*s. wax 0..1 = tapón de cera."""
    w, h = 150 * s, 700 * s
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(tilt)
    if glow > 0:
        spotlight(ctx, 0, 0, h * 0.8, 0.35 * glow, BREATH)
    # cuerpo de cristal (forma de U)
    def body():
        ctx.new_path()
        ctx.move_to(-w / 2, -h / 2)
        ctx.line_to(-w / 2, h / 2 - w / 2)
        ctx.arc_negative(0, h / 2 - w / 2, w / 2, math.pi, 0)
        ctx.line_to(w / 2, -h / 2)
        ctx.close_path()
    body()
    ctx.set_source(cairo.LinearGradient(-w / 2, 0, w / 2, 0))
    g = cairo.LinearGradient(-w / 2, 0, w / 2, 0)
    g.add_color_stop_rgba(0, *GLASS, 0.30)
    g.add_color_stop_rgba(0.3, *GLASS, 0.08)
    g.add_color_stop_rgba(0.8, *GLASS, 0.15)
    g.add_color_stop_rgba(1, *GLASS, 0.35)
    ctx.set_source(g)
    ctx.fill()
    if breath > 0:
        ctx.save()
        body()
        ctx.clip()
        wisp(ctx, 0, h * 0.05, w, h * 0.8, T, breath)
        ctx.restore()
    body()
    stroke(ctx, GLASS, 7 * s + 2, 0.9)
    # reflejo
    rrect(ctx, -w * 0.30, -h * 0.40, w * 0.12, h * 0.62, w * 0.06)
    fill(ctx, WHITE, 0.45)
    # borde
    rrect(ctx, -w / 2 - 14 * s, -h / 2 - 16 * s, w + 28 * s, 30 * s, 12 * s)
    fill(ctx, GLASS, 0.9)
    # tapón de cera
    if wax > 0.01:
        hh = 120 * s * wax
        rrect(ctx, -w / 2 - 6 * s, -h / 2 - 16 * s - hh + 14 * s, w + 12 * s, hh, 26 * s)
        ctx.set_source(vgrad(ctx, 0, -h / 2 - hh, 0, -h / 2, [(0, (0.95, 0.25, 0.25)), (1, WAX)]))
        ctx.fill()
        for k in (-0.3, 0.1, 0.35):  # goterones
            rrect(ctx, k * w - 10 * s, -h / 2 - 10 * s, 20 * s, (40 + 30 * abs(k)) * s * wax, 10 * s)
            fill(ctx, WAX)
    if label:
        ctx.save()
        ctx.rotate(-0.06)
        rrect(ctx, -w * 0.9, h * 0.08, w * 1.8, 74 * s, 10 * s)
        fill_keep(ctx, (0.96, 0.92, 0.80))
        stroke(ctx, (0.55, 0.45, 0.30), 3)
        fs = min(40 * s, 40 * s * (w * 1.6) / max(text_width(ctx, label, 40 * s), 1))
        text(ctx, label, 0, h * 0.08 + 37 * s, fs, (0.25, 0.18, 0.10), shadow=False)
        ctx.restore()
    ctx.restore()


def hero_tube(ctx, T, zoom, cy=900):
    """Plano del gancho (inicio y final del bucle): tubo gigante brillando en la oscuridad."""
    camera(ctx, zoom, W / 2, cy)
    bg_lab(ctx, T)
    spotlight(ctx, W / 2, 700, 900, 0.18, (0.8, 0.9, 1.0))
    tube(ctx, W / 2, 820, 1.25, T, wax=1.0, breath=1.0, glow=1.0, tilt=0.06)


def rack(ctx, x, y, n_show, T, wax=None, sc=1.0):
    """Gradilla de madera con 8 tubos. n_show = cuántos tubos se ven (0..8). wax = lista 0..1."""
    for k in range(8):
        if k >= n_show:
            continue
        tx = x - 3.5 * 120 * sc + k * 120 * sc
        p = clamp(n_show - k)
        tube(ctx, tx, y - 150 * sc * p - 60 * sc + 150 * sc, 0.55 * sc, T + k, wax=(wax[k] if wax else 0.0), breath=0.0)
    rrect(ctx, x - 520 * sc, y + 80 * sc, 1040 * sc, 70 * sc, 14 * sc)
    fill(ctx, WOOD)
    rrect(ctx, x - 520 * sc, y - 40 * sc, 1040 * sc, 40 * sc, 10 * sc)
    fill(ctx, WOOD_D)
    for sx in (-1, 1):
        rrect(ctx, x + sx * 500 * sc - 20 * sc, y - 40 * sc, 40 * sc, 190 * sc, 8 * sc)
        fill(ctx, WOOD_D)


def bedroom(ctx, T, lamp=1.0):
    ctx.set_source(vgrad(ctx, 0, -300, 0, H + 300, [(0, (0.10, 0.08, 0.20)), (1, (0.05, 0.04, 0.10))]))
    ctx.paint()
    # papel pintado
    for k in range(-6, 14):
        ctx.rectangle(k * 110, -400, 50, 1700)
        fill(ctx, WHITE, 0.025)
    # ventana con luna
    rrect(ctx, 640, 260, 340, 440, 16)
    fill_keep(ctx, (0.08, 0.12, 0.30))
    stroke(ctx, WOOD, 18)
    circle(ctx, 860, 380, 60)
    fill(ctx, (0.95, 0.93, 0.80))
    ctx.move_to(810, 260); ctx.line_to(810, 700)
    ctx.move_to(640, 480); ctx.line_to(980, 480)
    stroke(ctx, WOOD, 12)
    # suelo
    ctx.rectangle(-500, 1300, W + 1000, 1200)
    fill(ctx, (0.18, 0.11, 0.07))
    # cama
    rrect(ctx, 80, 980, 560, 300, 30)
    fill(ctx, (0.85, 0.85, 0.92))
    rrect(ctx, 60, 760, 60, 600, 20)
    fill(ctx, WOOD)
    rrect(ctx, 600, 960, 50, 400, 20)
    fill(ctx, WOOD)
    rrect(ctx, 120, 930, 200, 110, 50)  # almohada
    fill(ctx, WHITE)
    rrect(ctx, 260, 1000, 380, 180, 40)  # manta
    fill(ctx, (0.35, 0.40, 0.75))
    # mesilla + lámpara con bombilla (parpadea)
    rrect(ctx, 720, 1080, 260, 240, 14)
    fill(ctx, WOOD)
    flick = lamp * (0.75 + 0.25 * math.sin(T * 23) * math.sin(T * 7))
    spotlight(ctx, 850, 900, 420, 0.45 * flick, (1, 0.85, 0.5))
    bulb(ctx, 850, 930, 0.7, flick)
    rrect(ctx, 830, 990, 40, 90, 8)
    fill(ctx, (0.3, 0.3, 0.35))


def bulb(ctx, x, y, s=1.0, on=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if on > 0:
        spotlight(ctx, 0, 0, 260, 0.6 * on, (1, 0.9, 0.5))
    circle(ctx, 0, -20, 95)
    fill(ctx, (1, 0.92, 0.55) if on > 0.3 else (0.7, 0.72, 0.78), 0.95)
    ctx.move_to(-40, 60); ctx.line_to(-40, 20); ctx.curve_to(-30, -40, 30, -40, 40, 20); ctx.line_to(40, 60)
    stroke(ctx, (0.85, 0.55, 0.15), 6)
    rrect(ctx, -50, 60, 100, 70, 12)
    fill(ctx, (0.65, 0.65, 0.70))
    for k in range(3):
        ctx.move_to(-50, 78 + k * 18); ctx.line_to(50, 78 + k * 18)
        stroke(ctx, (0.45, 0.45, 0.50), 5)
    ctx.restore()


def gent(ctx, x, y, s=1.0, col=(0.10, 0.10, 0.16)):
    """Silueta genérica de un caballero de los años 30 con sombrero (sin rasgos)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -150, 120, 300, 520, 110)
    fill(ctx, col)
    circle(ctx, 0, 0, 100)
    fill(ctx, col)
    rrect(ctx, -150, -80, 300, 30, 15)
    fill(ctx, col)
    rrect(ctx, -90, -190, 180, 130, 30)
    fill(ctx, col)
    ctx.restore()


def house(ctx, x, y, s, T, lit=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-420, -250); ctx.line_to(0, -560); ctx.line_to(420, -250); ctx.close_path()
    fill(ctx, (0.20, 0.14, 0.22))
    ctx.rectangle(-380, -260, 760, 560)
    fill(ctx, (0.30, 0.24, 0.34))
    for wx in (-260, 0, 260):
        for wy in (-180, 60):
            rrect(ctx, wx - 70, wy - 70, 140, 150, 10)
            on = lit if (wx, wy) == (0, 60) else 0.25
            fill(ctx, (1, 0.82, 0.45), on)
    ctx.rectangle(-60, 170, 120, 130)
    fill(ctx, WOOD_D)
    ctx.restore()


def museum_case(ctx, x, y, s, T, appear=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # haz de foco
    ctx.move_to(-60, -900); ctx.line_to(60, -900); ctx.line_to(330, 350); ctx.line_to(-330, 350); ctx.close_path()
    g = cairo.LinearGradient(0, -900, 0, 350)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.0)
    g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.20 * appear)
    ctx.set_source(g)
    ctx.fill()
    # pedestal
    rrect(ctx, -260, 380, 520, 520, 10)
    ctx.set_source(vgrad(ctx, 0, 380, 0, 900, [(0, (0.30, 0.30, 0.38)), (1, (0.15, 0.15, 0.20))]))
    ctx.fill()
    tube(ctx, 0, 70, 0.75, T, wax=1.0, breath=0.7, glow=0.5)
    # vitrina
    rrect(ctx, -240, -380, 480, 760, 8)
    fill_keep(ctx, GLASS, 0.06)
    stroke(ctx, GLASS, 6, 0.6)
    ctx.move_to(-200, -340); ctx.line_to(-120, -340); ctx.line_to(-200, -200)
    fill(ctx, WHITE, 0.15)
    ctx.restore()


def mitten_map(ctx, x, y, s, T):
    """Michigan (la 'manopla') estilizada + pin."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-120, 300)
    ctx.curve_to(-200, 120, -210, -120, -120, -260)
    ctx.curve_to(-60, -330, 20, -300, 40, -200)
    ctx.curve_to(60, -120, 60, -60, 90, -40)
    ctx.curve_to(150, -120, 220, -90, 210, 0)
    ctx.curve_to(200, 120, 160, 220, 120, 300)
    ctx.close_path()
    fill_keep(ctx, (0.25, 0.65, 0.45))
    stroke(ctx, WHITE, 8, 0.8)
    # península superior
    ctx.move_to(-420, -420); ctx.curve_to(-300, -470, -120, -470, 40, -420)
    ctx.curve_to(-20, -380, -200, -360, -420, -360); ctx.close_path()
    fill_keep(ctx, (0.25, 0.65, 0.45))
    stroke(ctx, WHITE, 8, 0.8)
    ctx.restore()


def pin(ctx, x, y, s=1.0, drop=1.0):
    yy = y - 200 * (1 - ease_back(drop))
    ctx.save()
    ctx.translate(x, yy)
    ctx.scale(s, s)
    ctx.move_to(0, 0)
    ctx.curve_to(-70, -90, -70, -170, 0, -170)
    ctx.curve_to(70, -170, 70, -90, 0, 0)
    fill(ctx, RED)
    circle(ctx, 0, -115, 28)
    fill(ctx, WHITE)
    ctx.restore()


def box(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -130, -100, 260, 200, 14)
    fill(ctx, (0.78, 0.58, 0.36))
    ctx.rectangle(-130, -20, 260, 40)
    fill(ctx, (0.62, 0.44, 0.26))
    ctx.rectangle(-20, -100, 40, 200)
    fill(ctx, (0.62, 0.44, 0.26))
    text(ctx, "FRAGILE", 0, 60, 30, RED, shadow=False)
    ctx.restore()


# ---------------- escenas (Y del subtítulo gigante ≈ 1060: dejar libre ~950–1170) ----------------
# 0.0 "Thomas Edison's last breath is sealed inside a glass tube"
def e1(ctx, lt, dur, T):
    hero_tube(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.18)]))


# 3.7 "in Michigan."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    bg_lab(ctx, T)
    mitten_map(ctx, 560, 640, 1.05, T)
    pin(ctx, 600, 640, 1.1, clamp(lt / 0.35))
    pill(ctx, "MICHIGAN, USA", W / 2, 1380, pop(lt, 0.15), rgb=GREEN)


# 4.4 "And it's real."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.35), (0.25, 1.1), (dur, 1.15)]), W / 2, 900)
    bg_lab(ctx, T)
    tube(ctx, W / 2, 760, 0.95, T, wax=1.0, breath=1.0, glow=0.8, label="1931")
    badge(ctx, "REAL", 760, 380, pop(lt, 0.1), size=80)


# 5.2 "In 1931, Edison was dying in his bedroom."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), keyframes(lt, [(0, 520), (dur, 600)]), 900)
    bedroom(ctx, T)
    pill(ctx, counter(lt, 1900, 1931, 0.6), 360, 470, pop(lt, 0.0), size=70, rgb=GOLD)
    pill(ctx, "WEST ORANGE, NJ", 360, 610, pop(lt, 1.3), size=34, rgb=TEAL)


# 8.1 "Next to his bed sat a rack of eight empty test tubes."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 820)
    bg_lab(ctx, T)
    spotlight(ctx, W / 2, 700, 700, 0.2)
    n = clamp((lt - 0.2) / 1.1) * 8
    rack(ctx, W / 2, 820, n, T)
    pill(ctx, "8 EMPTY TUBES", W / 2, 1380, pop(lt, 1.4), rgb=GLASS)


# 11.1 "When Edison died, his son Charles had the doctor seal those tubes with wax."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.06)]), W / 2, keyframes(lt, [(0, 860), (dur, 780)]))
    bg_lab(ctx, T, 0.04)
    spotlight(ctx, W / 2, 700, 700, 0.2)
    wax = [clamp((lt - 2.2 - k * 0.12) / 0.3) for k in range(8)]
    rack(ctx, W / 2, 820, 8, T, wax=wax)
    pill(ctx, "SEALED WITH WAX", W / 2, 1380, pop(lt, 2.4), rgb=RED)


# 15.2 "Trapping the air of the room where Edison breathed his last."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bedroom(ctx, T, lamp=0.4)
    ctx.rectangle(-500, -500, W + 1000, H + 1000)
    fill(ctx, (0.02, 0.02, 0.08), 0.45)
    # el aire de la habitación se arremolina hacia el tubo
    for k in range(26):
        a = k * 2.4 + T * 1.3
        r = 520 * (1 - ((lt * 0.35 + k / 26) % 1))
        circle(ctx, 540 + math.cos(a) * r, 520 + math.sin(a) * r * 0.8, 10)
        fill(ctx, BREATH, 0.7)
    tube(ctx, 540, 560, 0.75, T, wax=0, breath=clamp(lt / 1.5), glow=0.6)
    pill(ctx, "THE AIR OF THE ROOM", W / 2, 1420, pop(lt, 0.6), rgb=TEAL)


# 18.2 "In other words, he bottled his father's final breath."  (2.º gancho: golpe de zoom)
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.6), (0.3, 1.0), (dur, 1.08)]) + 0.01 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 900)
    bg_lab(ctx, T, 0.06)
    for k in range(16):  # rayos
        ctx.save(); ctx.translate(W / 2, 640); ctx.rotate(k * math.pi / 8 + T * 0.2)
        ctx.move_to(0, 0); ctx.line_to(1400, -90); ctx.line_to(1400, 90); ctx.close_path()
        fill(ctx, BREATH, 0.05); ctx.restore()
    tube(ctx, W / 2, 620, 0.95, T, wax=1.0, breath=1.0, glow=1.2, label="LAST BREATH?")
    character(ctx, 230, 1420, 0.55, T, mood="sorpresa", body=True)
    pill(ctx, "HIS FATHER'S", 780, 1400, pop(lt, 1.1), size=44, rgb=RED)


# 21.5 "Then he sent one tube to Edison's best friend, Henry Ford."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 900)
    bg_blueprint(ctx, T)
    pill(ctx, "EDISON", 230, 420, pop(lt, 0.1), rgb=GOLD)
    pill(ctx, "FORD", 850, 1500, pop(lt, 2.4), rgb=TEAL)
    arrow(ctx, 230, 500, 850, 1400, ease((lt - 0.3) / 2.0), WHITE, 8, dashed=True)
    p = ease((lt - 0.3) / 2.0)
    box(ctx, lerp(230, 850, p), lerp(560, 1340, p) - 60 * math.sin(p * math.pi), 1.1, 0.15 * math.sin(T * 5))


# 24.9 "Ford idolized Edison."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.20, 0.12, 0.30)), (1, (0.06, 0.04, 0.12))]))
    ctx.paint()
    bulb(ctx, W / 2, 520, 1.7, 1.0)
    for k in range(7):
        a = k / 7 * math.tau + T
        icon(ctx, "⭐", W / 2 + math.cos(a) * 330, 520 + math.sin(a) * 260, 70, pop(lt, 0.1 * k))
    gent(ctx, W / 2, 1480, 1.0)
    pill(ctx, "HIS HERO", W / 2, 1300, pop(lt, 0.5), rgb=GOLD)


# 26.1 "Legend says Ford believed the soul leaves the body with the last breath."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.02, 0.03, 0.08)), (1, (0.06, 0.08, 0.16))]))
    ctx.paint()
    tube(ctx, W / 2, 1420, 0.55, T, wax=1.0, breath=1.0, glow=0.6)
    # el "alma" sube como un humo luminoso
    up = clamp((lt - 1.0) / 2.5)
    for k in range(5):
        y0 = 1180 - up * 700 - k * 90
        ctx.move_to(W / 2, 1220)
        ctx.curve_to(W / 2 - 160 * math.sin(T + k), lerp(1220, y0, 0.33), W / 2 + 160 * math.sin(T * 1.3 + k),
                     lerp(1220, y0, 0.66), W / 2, y0)
        stroke(ctx, BREATH, 26 - k * 4, 0.18 + 0.1 * k)
    spotlight(ctx, W / 2, 1180 - up * 700, 260, 0.5 * up, BREATH)
    badge(ctx, "LEGEND", W / 2, 300, pop(lt, 0.0), size=60, bg=PURPLE)


# 29.9 "Ford kept that tube at his house until he died."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, keyframes(lt, [(0, 900), (dur, 820)]))
    bg_night(ctx, T, grid=False)
    ground(ctx, 1320)
    house(ctx, W / 2, 1020, 1.05, T)
    tube(ctx, W / 2, 1060, 0.18, T, wax=1.0, breath=1.0, glow=0.8)
    pill(ctx, counter(lt - 0.6, 1931, 1947, 1.4), W / 2, 360, pop(lt, 0.2), size=70, rgb=GOLD)


# 32.2 "Today it's still sealed, on display at the Henry Ford Museum."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.12)]), W / 2, 880)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.03, 0.03, 0.06)), (1, (0.10, 0.09, 0.14))]))
    ctx.paint()
    museum_case(ctx, W / 2, 620, 0.95, T, 1.0)
    pill(ctx, "STILL SEALED", W / 2, 1380, pop(lt, 0.8), rgb=RED)
    pill(ctx, "HENRY FORD MUSEUM", W / 2, 1530, pop(lt, 2.0), size=38, rgb=GOLD)


# 35.8 "So next time someone says save your breath, remember:"
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T)
    character(ctx, W / 2, 620, 0.9, T, mood="duda", body=True)
    pill(ctx, '"SAVE YOUR BREATH"', W / 2, 300, pop(lt, 0.9), size=50, rgb=WHITE)


# 38.5 "Henry Ford actually did. He saved" -> vuelve a e1 (mismo plano, termina donde e1 empieza)
def e15(ctx, lt, dur, T):
    hero_tube(ctx, T, keyframes(lt, [(0, 0.86), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (3.7, e2), (4.4, e3), (5.2, e4), (8.1, e5), (11.1, e6), (15.2, e7), (18.2, e8),
           (21.5, e9), (24.9, e10), (26.1, e11), (29.9, e12), (32.2, e13), (35.8, e14), (38.5, e15)]
SFX = [(4.45, "pop"), (18.25, "ding"), (32.3, "pop")]


# ---------------- miniatura (no desvela que es el "último aliento") ----------------
def MINIATURA(ctx):
    T = 1.3
    ctx.save()
    camera(ctx, 1.05, W / 2, 1000)
    bg_lab(ctx, T)
    spotlight(ctx, W / 2, 1050, 900, 0.25, (0.8, 0.9, 1.0))
    tube(ctx, W / 2 + 40, 1200, 1.15, T, wax=1.0, breath=1.0, glow=1.3, label="1931", tilt=0.08)
    ctx.restore()
    thumb_vignette(ctx, 0.6)
    thumb_circle(ctx, W / 2 + 60, 1250, 185, 290)
    thumb_arrow(ctx, 140, 1640, 380, 1420)
    thumb_text(ctx, ["WHAT'S", ("INSIDE?", WHITE)], y=250, size=200)
    badge(ctx, "STILL SEALED", 780, 1700, 1.0, size=50)
