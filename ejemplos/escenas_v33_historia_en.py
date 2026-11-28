"""v33 (EN) formato «historia» (inventada, física real): por qué los rascacielos esconden una bola gigante
(amortiguador de masa sintonizada: el péndulo se mueve al revés que el edificio y frena el balanceo)."""
from kit import *  # noqa
from estilo_v3 import *  # noqa

FLASH = False
WHOOSH = False
MUSICA_GAIN = 0.42
FX_GAIN = 0.30
Y_SUBTITULO = 1430     # subtítulos ABAJO
TAM_SUBTITULO = 135
set_azul(25.11, 34.0)   # "You see" -> "counterweight."

KID = (0.25, 0.50, 0.85)
RIV = (0.88, 0.25, 0.25)
GLASSB = (0.62, 0.80, 0.95)
STEEL = (0.70, 0.72, 0.80)
BALL = (0.95, 0.75, 0.25)


def tower(ctx, x, yb, w, h, sway=0.0, col=GLASSB, ball=None, cracks=0.0, cut=False, floors=14):
    """Torre que se balancea (sway en radianes, gira desde la base). ball = desplazamiento del péndulo (-1..1) o None.
    cut = corte para ver el interior arriba."""
    ctx.save(); ctx.translate(x, yb); ctx.rotate(sway)
    rrect(ctx, -w / 2, -h, w, h, 8); fill_ink(ctx, col, 5)
    for f in range(1, floors):
        fy = -h + f * h / floors
        ctx.move_to(-w / 2, fy); ctx.line_to(w / 2, fy); stroke(ctx, mix(col, (0.2, 0.3, 0.5), 0.35), 3)
    ctx.move_to(0, -h); ctx.line_to(0, -h - 60); stroke(ctx, INKC, 6)
    if cracks > 0:
        for k in range(3):
            pts = zig(-w / 2 + 20 + k * w / 3, -h * (0.55 + 0.12 * k), -w / 2 + 70 + k * w / 3, -h * (0.45 + 0.12 * k), 4, 10, k + 2)
            crack_path(ctx, partial(pts, cracks), 4)
    if ball is not None:
        top = -h + 40
        if cut:
            rrect(ctx, -w / 2 + 14, top - 10, w - 28, h * 0.30, 6); fill_ink(ctx, (0.95, 0.93, 0.88), 3)
        L = h * 0.20
        bx, by = ball * w * 0.22, top + L
        for sx in (-1, 0, 1):
            ctx.move_to(sx * 30, top); ctx.line_to(bx + sx * 10, by); stroke(ctx, INKC, 4)
        circle(ctx, bx, by, w * 0.17); fill_ink(ctx, BALL, 4)
    ctx.restore()


def wind(ctx, T, a=1.0, strength=1.0, y0=300, y1=1200):
    for k in range(int(8 * strength) + 3):
        ph = (T * (0.8 + 0.8 * strength) + k * 0.37) % 1.0
        y = y0 + (k * 97) % (y1 - y0)
        x = -200 + 1400 * ph
        ctx.move_to(x, y); ctx.curve_to(x + 60, y - 20, x + 120, y + 20, x + 180, y); stroke(ctx, WHITE, 5, 0.7 * a * (1 - abs(ph - 0.5) * 1.6))


def city_ground(ctx, T, P, y=1250):
    sky(ctx, T, P)
    for k, (hx, hh) in enumerate(((60, 300), (180, 420), (900, 380), (1010, 260))):
        rrect(ctx, hx - 55, y - hh, 110, hh, 4); fill_ink(ctx, mix(P["sky1"], (0.4, 0.45, 0.6), 0.5), 3)
    ground(ctx, y, P, col=P["conc"])


def hero(ctx, lt, T, dur, z0, z1):
    """Primer plano: la parte alta del rascacielos en corte, con la bola gigante balanceándose y el chico al lado."""
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2, 760)
    sky(ctx, T, P)
    rrect(ctx, 120, 300, 840, 1500, 10); fill_ink(ctx, GLASSB, 6)
    rrect(ctx, 160, 340, 760, 760, 8); fill_ink(ctx, (0.95, 0.93, 0.88), 4)
    sw = math.sin(T * 1.6)
    bx, by = 540 + 170 * sw, 820
    for sx in (-1, 0, 1):
        ctx.move_to(540 + sx * 60, 360); ctx.line_to(bx + sx * 20, by - 150); stroke(ctx, INKC, 6)
    circle(ctx, bx, by, 190); fill_ink(ctx, BALL, 6)
    circle(ctx, bx - 60, by - 60, 40); fill(ctx, WHITE, 0.35)
    ctx.rectangle(160, 1060, 760, 40); fill_ink(ctx, STEEL, 4)
    worker(ctx, 830, 780, 0.75, T, col=KID, k=1, mood="feliz", hat=YELLOW)
    ctx.restore()


# 0.00 "This guy hung a giant steel ball inside his skyscraper on purpose."
def e1(ctx, lt, dur, T):
    if T < 1.67:
        hero(ctx, lt, T, dur, 1.2, 1.08)
    else:   # "ball" -> corte seco: con bola apenas se mueve ✓ / sin bola se balancea y se raja ✗
        P = pal(T)
        ctx.save()
        camera(ctx, keyframes(lt - 1.67, [(0, 1.06), (dur - 1.67, 1.0)]), W / 2, 820)
        city_ground(ctx, T, P, 1250)
        tower(ctx, 290, 1250, 220, 880, sway=0.01 * math.sin(T * 2.5), ball=-0.8 * math.sin(T * 2.5), cut=True)
        tower(ctx, 790, 1250, 220, 880, sway=0.09 * math.sin(T * 2.5), col=mix(GLASSB, RIV, 0.15),
              cracks=clamp((T - 2.3) / 0.8))
        ctx.restore()
        wind(ctx, T, 1.0, 1.5)
        check(ctx, 290, 1320, 0.8, pop(lt, 1.75), ok=True)
        check(ctx, 790, 1320, 0.8, pop(lt, 2.1), ok=False)
    gancho(ctx, ["WHY IS THERE A GIANT", ("BALL IN THIS TOWER?", WHITE)], T, t_fin=3.0, size=88)


# 4.15 "See, two companies are building towers in a windy city."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.12), (dur, 1.0)]), W / 2, 850)
    city_ground(ctx, T, P, 1250)
    g = ease(clamp(lt / 1.8))
    tower(ctx, 320, 1250, 200, 300 + 520 * g, ball=0.0 if g > 0.9 else None)
    tower(ctx, 760, 1250, 200, 300 + 520 * g, col=mix(GLASSB, RIV, 0.15))
    ctx.restore()
    wind(ctx, T, 0.8, 0.8)
    label(ctx, "THE KID", 320, 300, pop(lt, 0.2), rgb=KID, size=48)
    label(ctx, "RIVAL", 760, 300, pop(lt, 0.4), rgb=RIV, size=48)
    if T > 6.01:
        label(ctx, "WINDY CITY", W / 2, 420, pop(lt, 6.01 - 4.15), rgb=WHITE, size=44)


# 6.59 "His boss sees the ball. Kid, that's six hundred tons of dead weight."
def e3(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.1)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 900), sky(c, T, P)))
    ctx.save()
    camera(ctx, z, W / 2, 900)
    rrect(ctx, 420, 420, 600, 900, 8); fill_ink(ctx, (0.95, 0.93, 0.88), 5)
    sw = math.sin(T * 1.6)
    for sx in (-1, 0, 1):
        ctx.move_to(720 + sx * 50, 440); ctx.line_to(720 + 120 * sw + sx * 15, 760); stroke(ctx, INKC, 5)
    circle(ctx, 720 + 120 * sw, 900, 160); fill_ink(ctx, BALL, 5)
    worker(ctx, 200, 860, 1.0, T, col=(0.55, 0.42, 0.30), boss=True, k=3,
           mood="shock" if T > 7.8 else "normal", tie=RED, hat_kind="none")
    ctx.restore()
    label(ctx, "BOSS", 200, 560, pop(lt, 0.2), rgb=GOLD, size=42)
    bubble(ctx, "KID, THAT'S DEAD WEIGHT!", W / 2, 300, pop(lt, 7.88 - 6.59), size=46)
    if T > 8.71:
        label(ctx, "600 TONS", 720, 1200, pop(lt, 8.71 - 6.59), rgb=YELLOW, size=56)


# 10.29 "The other company builds theirs stiff. Pure steel, no ball. Everybody loves it."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 850)
    city_ground(ctx, T, P, 1250)
    tower(ctx, 540, 1250, 300, 900, col=mix(GLASSB, STEEL, 0.5), floors=16)
    worker(ctx, 860, 1010, 0.6, T, col=RIV, k=2, mood="feliz", hat=WHITE)
    ctx.restore()
    label(ctx, "RIVAL: STIFF", W / 2, 300, pop(lt, 0.2), rgb=RIV, size=50)
    if T > 12.16:
        label(ctx, "NO BALL", 540, 700, pop(lt, 12.9 - 10.29), rgb=RED, size=52)
    if T > 13.39:
        for k in range(3):
            icon(ctx, "❤️", 200 + k * 340, 1180 - 30 * math.sin(T * 3 + k), 100, pop(lt, 13.39 - 10.29 + 0.15 * k))


# 14.56 "Then the storms come. Light wind, the tower barely moves. Strong wind, it starts to sway.
#        Typhoon, the top swings so far that people get seasick, and the windows start to crack."
def e5(ctx, lt, dur, T):
    P = pal(T)
    lvl = 0.25 if T < 17.68 else (0.6 if T < 19.18 else 1.0)
    dark = ease(clamp((T - 14.8) / 0.8))
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 850)
    city_ground(ctx, T, P, 1250)
    ctx.set_source_rgba(0.12, 0.14, 0.25, 0.45 * dark); ctx.paint()
    tower(ctx, 540, 1250, 300, 900, sway=0.13 * lvl * math.sin(T * 3.0), col=mix(GLASSB, STEEL, 0.5), floors=16,
          cracks=clamp((T - 22.56) / 0.6))
    ctx.restore()
    wind(ctx, T, dark, 2.5 * lvl)
    rain(ctx, T, dark * lvl, 60, 4)
    txt = "LIGHT WIND" if T < 17.68 else ("STRONG WIND" if T < 19.18 else "TYPHOON")
    label(ctx, txt, W / 2, 300, 1.0 if T > 15.68 else pop(lt, 15.68 - 14.56), rgb=YELLOW if lvl < 1 else RED, size=54)
    if T > 21.56:
        icon(ctx, "🤢", 870, 520, 130, pop(lt, 21.56 - 14.56))
    if T > 22.85:
        label(ctx, "CRACK!", 260, 520, pop(lt, 23.0 - 14.56), rgb=RED, size=52)


# 23.50 "The kid's tower barely moves."
def e6(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.12)]), W / 2, 820)
    city_ground(ctx, T, P, 1250)
    ctx.set_source_rgba(0.12, 0.14, 0.25, 0.4); ctx.paint()
    tower(ctx, 540, 1250, 320, 950, sway=0.012 * math.sin(T * 3.0), ball=-0.9 * math.sin(T * 3.0), cut=True, floors=16)
    ctx.restore()
    wind(ctx, T, 1.0, 2.5)
    label(ctx, "THE KID'S TOWER", W / 2, 300, pop(lt, 0.2), rgb=KID, size=50)
    check(ctx, 880, 520, 1.0, pop(lt, 24.33 - 23.50), ok=True)


# 25.11 "You see, when the wind pushes the tower one way, the ball swings the other way and pulls it back."  (luz azul)
def e7(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 760)
    sky(ctx, T, P)
    ctx.restore()
    ph = math.sin(T * 1.8)
    tower(ctx, 540, 1300, 360, 1000, sway=0.05 * ph, ball=-1.0 * ph, cut=True, floors=16)
    if T > 25.74:
        a = pop(lt, 25.74 - 25.11)
        d = 1 if ph > 0 else -1
        arrow(ctx, 540 - d * 330, 520, 540 - d * 200, 520, a, rgb=(0.85, 0.90, 1.0), w=14)
        label(ctx, "WIND", 540 - d * 330, 450, a, rgb=WHITE, size=40)
    if T > 27.52:
        a = pop(lt, 27.52 - 25.11)
        d = -1 if ph > 0 else 1
        arrow(ctx, 540, 700, 540 + d * 160, 700, a, rgb=YELLOW, w=12)
        label(ctx, "BALL: OTHER WAY", W / 2, 300, a, rgb=YELLOW, size=46)
    if T > 28.73:
        label(ctx, "PULLS IT BACK", W / 2, 1220, pop(lt, 28.73 - 25.11), rgb=(0.30, 0.78, 0.40), size=46)


# 29.41 "Like leaning into someone who's pushing you."
def e8(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 820)
    sky(ctx, T, P)
    ground(ctx, 1150, P)
    worker(ctx, 360, 800, 0.95, T, col=KID, k=1, mood="feliz", hat=YELLOW, arm=0.9, look=0.4)
    worker(ctx, 720, 800, 0.95, T, col=RIV, k=2, mood="normal", hat=WHITE, arm=0.9, look=-0.4)
    ctx.restore()
    a = pop(lt, 29.62 - 29.41)
    arrow(ctx, 850, 650, 620, 650, a, rgb=RED, w=14)
    arrow(ctx, 230, 700, 460, 700, pop(lt, 30.0 - 29.41), rgb=(0.30, 0.78, 0.40), w=14)
    label(ctx, "LEAN INTO THE PUSH", W / 2, 300, a, rgb=YELLOW, size=48)


# 31.04 "In other words, the ball wasn't dead weight. It was a counterweight."
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.08, dur=dur), W / 2, 820)
    sky(ctx, T, P)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.22); ctx.paint()
    circle(ctx, 540, 800, 260); fill_ink(ctx, BALL, 6)
    circle(ctx, 460, 720, 60); fill(ctx, WHITE, 0.35)
    ctx.restore()
    if T > 32.19:
        stamp(ctx, "NOT DEAD WEIGHT", W / 2, 300, (T - 32.19) / 0.25, size=84)
    if T > 33.39:
        stamp(ctx, "COUNTERWEIGHT", W / 2, 1240, (T - 33.39) / 0.25, col=(0.30, 0.78, 0.40), size=96)


# 34.05 "That's why the tallest towers hide giant balls inside."
def e10(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 860)
    city_ground(ctx, T, P, 1250)
    for k, (tx, th) in enumerate(((220, 760), (540, 980), (860, 820))):
        tower(ctx, tx, 1250, 220, th, ball=0.6 * math.sin(T * 1.5 + k), cut=True, floors=12)
    ctx.restore()
    label(ctx, "THE TALLEST TOWERS", W / 2, 300, pop(lt, 34.59 - 34.05), rgb=YELLOW, size=50)


# 37.14 "Because, just like" -> bucle (acaba en el encuadre del fotograma 0)
def e11(ctx, lt, dur, T):
    hero(ctx, lt, T, dur, 1.08, 1.2)


ESCENAS = [(0.0, e1), (4.15, e2), (6.59, e3), (10.29, e4), (14.56, e5), (23.50, e6), (25.11, e7), (29.41, e8),
           (31.04, e9), (34.05, e10), (37.14, e11)]

SFX = [(0.1, "squish"), (1.67, "thud"), (2.3, "crack"), (4.1, "whoosh"), (4.6, "rise"), (6.55, "whoosh"), (7.88, "drum"),
       (8.71, "thud"), (10.25, "whoosh"), (12.9, "pop"), (13.4, "pop"), (14.5, "whoosh"), (15.68, "tick"),
       (17.68, "rise"), (19.18, "thud"), (21.56, "squish"), (22.85, "crack"), (23.45, "whoosh"), (24.33, "ding"),
       (25.05, "whoosh"), (25.74, "whoosh"), (27.52, "pop"), (28.73, "ding"), (29.35, "whoosh"), (30.0, "pop"),
       (31.0, "thud"), (32.19, "thud"), (33.39, "thud"), (34.0, "whoosh"), (36.6, "pop"), (37.1, "whoosh")]


def MINIATURA(ctx):
    T = 0.5
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    sky(ctx, T, P)
    rrect(ctx, 140, 620, 800, 1400, 10); fill_ink(ctx, GLASSB, 6)
    rrect(ctx, 180, 660, 720, 760, 8); fill_ink(ctx, (0.95, 0.93, 0.88), 4)
    for sx in (-1, 0, 1):
        ctx.move_to(540 + sx * 60, 680); ctx.line_to(600 + sx * 20, 960); stroke(ctx, INKC, 6)
    circle(ctx, 600, 1120, 200); fill_ink(ctx, BALL, 6)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["WHY IS THIS", ("BALL INSIDE?", WHITE)], y=260, size=150)
    thumb_circle(ctx, 600, 1120, 250, 250)
