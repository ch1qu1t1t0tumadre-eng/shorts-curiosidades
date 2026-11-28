"""v32 (EN) formato «historia» (inventada, geometría real): por qué las tapas de alcantarilla son redondas
(un cuadrado es más ancho en diagonal que de lado y cabe por su propio agujero; un círculo mide lo mismo en todas direcciones)."""
from kit import *  # noqa
from estilo_v3 import *  # noqa

FLASH = False
WHOOSH = False
MUSICA_GAIN = 0.42
FX_GAIN = 0.30
Y_SUBTITULO = 1430     # subtítulos ABAJO
TAM_SUBTITULO = 135
CORTES = [(10.70, 12.37)]  # quitado "Clean corners, easy to stack." (relleno)
set_azul(28.66, 43.0)   # "You see" -> "wrong shape."

KID = (0.25, 0.50, 0.85)
RIV = (0.88, 0.25, 0.25)
IRON = (0.36, 0.36, 0.42)
IRON_L = (0.52, 0.52, 0.60)
HOLE = (0.08, 0.07, 0.12)


def cover_face(ctx, x, y, r, square=False, rot=0.0, a=1.0):
    """Tapa vista de frente/arriba con su dibujo. r = medio lado (cuadrada) o radio (redonda)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    if square:
        rrect(ctx, -r, -r, 2 * r, 2 * r, 6)
    else:
        circle(ctx, 0, 0, r)
    fill_ink(ctx, IRON, 5, a)
    for k in range(-3, 4):
        if square:
            ctx.move_to(-r + 14, k * r / 4); ctx.line_to(r - 14, k * r / 4)
        else:
            hw = math.sqrt(max(r * r * 0.78 - (k * r / 4) ** 2, 0))
            ctx.move_to(-hw, k * r / 4); ctx.line_to(hw, k * r / 4)
        stroke(ctx, IRON_L, 6, a)
    ctx.restore()


def street_top(ctx, P, y0=380, y1=1300):
    ctx.rectangle(-200, y0, W + 400, y1 - y0); fill(ctx, P["road"])
    for k in range(6):
        ctx.rectangle(-200, y0 + 40 + k * 160, W + 400, 3); fill(ctx, mix(P["road"], WHITE, 0.08))


def foundry(ctx, x, y, s, col, name):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-200, 0); ctx.line_to(-200, -220); ctx.line_to(-100, -160); ctx.line_to(-100, -220); ctx.line_to(0, -160)
    ctx.line_to(0, -220); ctx.line_to(200, -220); ctx.line_to(200, 0); ctx.close_path(); fill_ink(ctx, mix(col, (1, 1, 1), 0.45), 4)
    ctx.rectangle(120, -340, 50, 130); fill_ink(ctx, (0.55, 0.50, 0.55), 4)
    rrect(ctx, -160, -120, 320, 80, 16); fill_ink(ctx, col, 4)
    text(ctx, name, 0, -80, 38, WHITE, shadow=False)
    ctx.restore()


def hero(ctx, lt, T, dur, z0, z1):
    """Primer plano: el chico rueda una tapa REDONDA gigante hacia el agujero abierto (acción desde el fotograma 0)."""
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2, 860)
    sky(ctx, T, P)
    ctx.rectangle(-300, 1000, W + 600, 900); fill_ink(ctx, P["road"], 4)
    ellipse(ctx, 830, 1120, 170, 50); fill_ink(ctx, HOLE, 5)            # agujero abierto
    roll = T * 2.2
    cx = 520 + 30 * math.sin(T * 1.3)
    ctx.save(); ctx.translate(cx, 830); ctx.rotate(roll)
    circle(ctx, 0, 0, 230); fill_ink(ctx, IRON, 6)
    for k in range(-3, 4):
        hw = math.sqrt(max(230 * 230 * 0.78 - (k * 57) ** 2, 0))
        ctx.move_to(-hw, k * 57); ctx.line_to(hw, k * 57); stroke(ctx, IRON_L, 7)
    ctx.restore()
    worker(ctx, cx - 280, 760, 0.85, T, col=KID, k=1, mood="feliz", hat=YELLOW, arm=0.9)
    ctx.restore()


# 0.00 "This guy made his manhole covers round on purpose."
def e1(ctx, lt, dur, T):
    if T < 1.71:
        hero(ctx, lt, T, dur, 1.25, 1.12)
    else:   # "round" -> corte seco: redonda encima del agujero ✓, cuadrada colándose en diagonal ✗
        P = pal(T)
        ctx.save()
        camera(ctx, keyframes(lt - 1.71, [(0, 1.06), (dur - 1.71, 1.0)]), W / 2, 820)
        sky(ctx, T, P)
        street_top(ctx, P, 480, 1180)
        circle(ctx, 290, 820, 190); fill_ink(ctx, HOLE, 4)
        cover_face(ctx, 290, 820, 215)
        rrect(ctx, 610, 640, 340, 340, 4); fill_ink(ctx, HOLE, 4)
        f = ease(clamp((T - 2.0) / 0.9))
        cover_face(ctx, 780, 810 + 60 * f, 190 * (1 - 0.35 * f), square=True, rot=0.78 * f, a=1 - 0.6 * f)
        ctx.restore()
        check(ctx, 290, 1250, 0.9, pop(lt, 1.75), ok=True)
        check(ctx, 780, 1250, 0.9, pop(lt, 2.05), ok=False)
    gancho(ctx, ["WHY ARE MANHOLE", ("COVERS ROUND?", WHITE)], T, t_fin=2.8, size=100)


# 3.00 "See, two foundries are making covers for the city."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 850)
    sky(ctx, T, P)
    ground(ctx, 1000, P, col=P["conc"])
    foundry(ctx, 270, 1000, 1.0, KID, "KID'S FOUNDRY")
    foundry(ctx, 810, 1000, 1.0, RIV, "RIVAL FOUNDRY")
    cover_face(ctx, 270, 1150, 90)
    cover_face(ctx, 810, 1150, 80, square=True)
    ctx.restore()
    label(ctx, "ROUND", 270, 300, pop(lt, 0.3), rgb=KID, size=50)
    label(ctx, "SQUARE", 810, 300, pop(lt, 0.6), rgb=RIV, size=50)


# 5.36 "His boss sees the round ones. Kid, round is way harder to make."
def e3(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.1)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 900), sky(c, T, P), ground(c, 1200, P, col=P["conc"])))
    ctx.save()
    camera(ctx, z, W / 2, 900)
    cover_face(ctx, 730, 820, 230)
    worker(ctx, 220, 760, 1.0, T, col=(0.55, 0.42, 0.30), boss=True, k=3,
           mood="shock" if T > 7.0 else "normal", tie=RED, hat_kind="none")
    ctx.restore()
    label(ctx, "BOSS", 220, 470, pop(lt, 0.2), rgb=GOLD, size=42)
    bubble(ctx, "KID, ROUND IS WAY HARDER TO MAKE!", W / 2, 300, pop(lt, 7.04 - 5.36), size=40)


# 8.96 "The other foundry makes square ones. [cut] The city loves them."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 860)
    sky(ctx, T, P)
    ground(ctx, 1150, P, col=P["conc"])
    for k in range(5):   # pila de tapas cuadradas
        a = pop(lt, 1.15 + 0.12 * k)
        if a > 0.01:
            ctx.save(); ctx.translate(560, 1120 - k * 55); ctx.scale(1, 0.25)
            rrect(ctx, -230 * a, -230, 460 * a, 460, 6); fill_ink(ctx, IRON, 4)
            ctx.restore()
    worker(ctx, 870, 900, 0.75, T, col=RIV, k=2, mood="feliz", hat=WHITE)
    ctx.restore()
    label(ctx, "RIVAL: SQUARE", W / 2, 300, pop(lt, 0.3), rgb=RIV, size=50)
    if T > 12.67:
        for k in range(3):
            icon(ctx, "❤️", 260 + k * 280, 520 - 30 * math.sin(T * 3 + k), 100, pop(lt, 12.67 - 8.96 + 0.15 * k))


# 13.45 "Then the workers start lifting them. One cover, fine. Ten covers, fine."
def e5(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 860)
    sky(ctx, T, P)
    ctx.rectangle(-300, 1000, W + 600, 900); fill_ink(ctx, P["road"], 4)
    lift = 90 + 30 * math.sin(T * 4)
    ctx.save(); ctx.translate(540, 1030 - lift); ctx.scale(1, 0.3)
    rrect(ctx, -200, -200, 400, 400, 6); fill_ink(ctx, IRON, 4)
    ctx.restore()
    ctx.save(); ctx.translate(540, 1080); ctx.scale(1, 0.3); rrect(ctx, -180, -180, 360, 360, 4); fill_ink(ctx, HOLE, 4); ctx.restore()
    worker(ctx, 240, 760, 0.85, T, col=(0.95, 0.60, 0.15), k=4, mood="normal", hat=YELLOW, arm=0.9)
    worker(ctx, 840, 760, 0.85, T, col=(0.95, 0.60, 0.15), k=5, mood="normal", hat=YELLOW, arm=0.9)
    ctx.restore()
    if T > 15.06:
        label(ctx, "1 COVER", 300, 300, pop(lt, 15.06 - 13.45), rgb=WHITE, size=46)
        check(ctx, 300, 420, 0.8, pop(lt, 15.97 - 13.45), ok=True)
    if T > 16.17:
        label(ctx, "10 COVERS", 780, 300, pop(lt, 16.17 - 13.45), rgb=WHITE, size=46)
        check(ctx, 780, 420, 0.8, pop(lt, 17.08 - 13.45), ok=True)


# 17.23 "Then a worker turns one sideways. The square tips, slides down the diagonal, and drops straight into the hole. Clang. Gone, down into the sewer."
def e6(ctx, lt, dur, T):
    """Vista en corte: la calle con el agujero; la tapa cuadrada de canto gira y entra por la diagonal."""
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    sky(ctx, T, P)
    ctx.rectangle(-300, 860, 460, 90); fill_ink(ctx, P["road"], 4)
    ctx.rectangle(720, 860, 700, 90); fill_ink(ctx, P["road"], 4)
    ctx.rectangle(-300, 950, W + 600, 1200); fill_ink(ctx, (0.30, 0.26, 0.24), 4)
    ctx.rectangle(160, 950, 560, 1100); fill(ctx, HOLE)              # pozo
    ctx.rectangle(160, 860, 560, 90); fill(ctx, HOLE)
    rot = 0.0 + 0.785 * ease(clamp((T - 18.45) / 1.2))             # se pone en diagonal
    drop = 900 * clamp((T - 21.77) / 1.1) ** 2 if T > 21.77 else 0.0
    slide = 80 * ease(clamp((T - 20.63) / 0.9))
    ctx.save(); ctx.translate(440, 760 + slide + drop); ctx.rotate(rot)
    rrect(ctx, -300, -24, 600, 48, 4); fill_ink(ctx, IRON, 5)        # tapa de canto (lado 600 > hueco 560? no: entra por la diagonal)
    ctx.restore()
    ctx.restore()
    cota(ctx, 160, 820, 720, 820, pop(lt, 0.4), "HOLE", rgb=YELLOW, size=40, dy=-60)
    if T > 20.86:
        label(ctx, "DIAGONAL", 760, 430, pop(lt, 21.09 - 17.23), rgb=RED, size=48)
    if T > 23.23:
        stamp(ctx, "CLANG!", 540, 300, (T - 23.23) / 0.25, size=110)
    if T > 24.38:
        label(ctx, "SEWER", 440, 1250, pop(lt, 24.91 - 17.23), rgb=(0.55, 0.75, 0.45), size=50)


# 25.27 "The kid's round cover just won't fall in, no matter how you turn it."
def e7(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 820)
    sky(ctx, T, P)
    street_top(ctx, P, 420, 1220)
    circle(ctx, 540, 820, 250); fill_ink(ctx, HOLE, 5)
    cover_face(ctx, 540, 820, 280, rot=T * 1.6)
    ctx.restore()
    label(ctx, "THE KID'S COVER", W / 2, 300, pop(lt, 0.2), rgb=KID, size=50)
    arrow(ctx, 900, 520, 830, 600, pop(lt, 27.9 - 25.27), rgb=YELLOW, w=10)
    check(ctx, 540, 1260, 1.0, pop(lt, 26.99 - 25.27), ok=True)


# 28.66 "You see, a square is wider corner to corner than side to side, so it can slip through its own hole."  (luz azul)
def e8(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 800)
    sky(ctx, T, P)
    ctx.restore()
    cx, cy, h = 540, 800, 230
    rrect(ctx, cx - h, cy - h, 2 * h, 2 * h, 4); fill_ink(ctx, IRON, 5)
    if T > 29.97:
        a = pop(lt, 29.97 - 28.66)
        arrow(ctx, cx - h, cy + h, cx + h, cy - h, a, rgb=RED, w=12)
        arrow(ctx, cx + h, cy - h, cx - h, cy + h, a, rgb=RED, w=12)
        label(ctx, "CORNER TO CORNER", cx, 300, a, rgb=RED, size=46)
    if T > 31.33:
        cota(ctx, cx - h, cy + h + 70, cx + h, cy + h + 70, pop(lt, 31.33 - 28.66), "SIDE TO SIDE", rgb=YELLOW, size=40, dy=80)
    if T > 32.51:
        label(ctx, "1.4× WIDER", cx, 420, pop(lt, 32.51 - 28.66), rgb=RED, size=52)


# 33.67 "A circle is the same width every way."
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 800)
    sky(ctx, T, P)
    ctx.restore()
    cx, cy, r = 540, 800, 260
    circle(ctx, cx, cy, r); fill_ink(ctx, IRON, 5)
    for k in range(4):
        ang = T * 0.9 + k * math.pi / 4
        p = pop(lt, 0.3 + 0.2 * k)
        ctx.move_to(cx - r * math.cos(ang) * p, cy - r * math.sin(ang) * p); ctx.line_to(cx + r * math.cos(ang) * p, cy + r * math.sin(ang) * p)
        stroke(ctx, (0.30, 0.78, 0.40), 9)
    label(ctx, "SAME WIDTH EVERY WAY", cx, 300, pop(lt, 34.59 - 33.67), rgb=(0.30, 0.78, 0.40), size=44)


# 35.87 "Like a lid on a jar: turn it any way you want, it never drops inside."
def e10(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 820)
    sky(ctx, T, P)
    ctx.restore()
    rrect(ctx, 330, 760, 420, 460, 50); fill_ink(ctx, (0.80, 0.92, 1.0), 5, a=0.8)   # tarro
    rrect(ctx, 360, 700, 360, 80, 20); fill_ink(ctx, (0.80, 0.92, 1.0), 4, a=0.8)
    tilt = 0.5 * math.sin(T * 2.4)
    ctx.save(); ctx.translate(540, 680); ctx.rotate(tilt)
    ctx.save(); ctx.scale(1, 0.32); circle(ctx, 0, 0, 230); fill_ink(ctx, RED, 5); ctx.restore()
    ctx.restore()
    label(ctx, "LID ON A JAR", W / 2, 300, pop(lt, 36.15 - 35.87), rgb=YELLOW, size=52)
    if T > 38.29:
        label(ctx, "NEVER FALLS IN", W / 2, 1290, pop(lt, 38.29 - 35.87), rgb=(0.30, 0.78, 0.40), size=46)


# 39.53 "In other words, the square covers weren't heavy. They were the wrong shape."
def e11(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.08, dur=dur), W / 2, 820)
    sky(ctx, T, P)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.22); ctx.paint()
    cover_face(ctx, 540, 800, 240, square=True, rot=0.785)
    ctx.restore()
    if T > 41.18:
        stamp(ctx, "NOT HEAVY", W / 2, 300, (T - 41.18) / 0.25, col=(0.30, 0.78, 0.40), size=96)
    if T > 42.35:
        stamp(ctx, "WRONG SHAPE", W / 2, 1240, (T - 42.35) / 0.25, size=100)


# 43.03 "That's why the manhole cover on your street is round."
def e12(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    ctx.save()
    camera(ctx, z, W / 2, 860)
    sky(ctx, T, P)
    house2(ctx, 260, 760, 1.0); house2(ctx, 820, 760, 0.9, col=(0.62, 0.72, 0.90))
    ctx.rectangle(-300, 760, W + 600, 1000); fill_ink(ctx, P["road"], 4)
    ctx.save(); ctx.translate(540, 1020); ctx.scale(1, 0.35); cover_face(ctx, 0, 0, 260); ctx.restore()
    ctx.restore()
    label(ctx, "YOUR STREET", W / 2, 300, pop(lt, 44.63 - 43.03), rgb=YELLOW, size=54)
    if T > 45.17:
        label(ctx, "ROUND ON PURPOSE", W / 2, 1240, pop(lt, 45.17 - 43.03), rgb=(0.30, 0.78, 0.40), size=46)


# 46.01 "Because, just like" -> bucle (acaba en el encuadre del fotograma 0)
def e13(ctx, lt, dur, T):
    hero(ctx, lt, T, dur, 1.12, 1.25)


ESCENAS = [(0.0, e1), (3.00, e2), (5.36, e3), (8.96, e4), (13.45, e5), (17.23, e6), (25.27, e7), (28.66, e8),
           (33.67, e9), (35.87, e10), (39.53, e11), (43.03, e12), (46.01, e13)]

SFX = [(0.1, "squish"), (1.71, "thud"), (2.1, "whoosh"), (2.95, "whoosh"), (3.4, "pop"), (3.7, "pop"), (5.3, "whoosh"),
       (7.04, "drum"), (8.9, "whoosh"), (10.1, "thud"), (10.3, "thud"), (12.67, "pop"), (13.4, "whoosh"), (15.97, "ding"),
       (17.08, "ding"), (17.2, "whoosh"), (18.5, "squish"), (20.63, "rise"), (21.77, "whoosh"), (23.23, "bell"),
       (24.4, "thud"), (25.2, "whoosh"), (26.99, "ding"), (28.6, "whoosh"), (29.97, "pop"), (31.33, "pop"),
       (32.51, "thud"), (33.6, "whoosh"), (35.8, "whoosh"), (38.29, "ding"), (39.5, "thud"), (41.18, "thud"),
       (42.35, "thud"), (43.0, "whoosh"), (45.17, "pop"), (45.95, "whoosh")]


def MINIATURA(ctx):
    T = 0.5
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    sky(ctx, T, P)
    ctx.rectangle(-300, 700, W + 600, 1400); fill(ctx, P["road"])
    cover_face(ctx, 300, 1150, 220)
    cover_face(ctx, 790, 1150, 200, square=True, rot=0.5)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["WHY ARE THEY", ("ALWAYS ROUND?", WHITE)], y=260, size=140)
    thumb_circle(ctx, 300, 1150, 260, 260)
