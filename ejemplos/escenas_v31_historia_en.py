"""v31 (EN) formato «historia» (inventada, física real): por qué los cables eléctricos cuelgan flojos
(el metal encoge con el frío; un cable tenso no tiene margen y tira de los postes hasta romperse)."""
from kit import *  # noqa
from estilo_v3 import *  # noqa

FLASH = False
WHOOSH = False
MUSICA_GAIN = 0.42
FX_GAIN = 0.30
Y_SUBTITULO = 1430     # subtítulos ABAJO
TAM_SUBTITULO = 135
set_azul(26.60, 37.03)  # "You see" -> "nowhere to go."

KID = (0.25, 0.50, 0.85)
RIV = (0.88, 0.25, 0.25)
POLE = (0.55, 0.38, 0.24)
WIRE = (0.12, 0.10, 0.16)
SNOW = (0.94, 0.96, 1.0)


def pole(ctx, x, yb, h, lean=0.0, s=1.0):
    """Poste de madera con cruceta; devuelve el punto de enganche del cable (x, y)."""
    ctx.save(); ctx.translate(x, yb); ctx.rotate(lean); ctx.scale(s, s)
    rrect(ctx, -14, -h, 28, h, 6); fill_ink(ctx, POLE, 4)
    rrect(ctx, -70, -h + 30, 140, 18, 5); fill_ink(ctx, mix(POLE, (0, 0, 0), 0.2), 3)
    for dx in (-55, 55):
        circle(ctx, dx, -h + 24, 9); fill_ink(ctx, (0.55, 0.80, 0.70), 2)
    ctx.restore()
    ang = lean
    return (x + math.sin(ang) * (h - 24) * s, yb - math.cos(ang) * (h - 24) * s)


def wire(ctx, a, b, sag, col=WIRE, w=6, broken=0.0, tension=0.0):
    """Cable entre a y b con flecha 'sag' (px). broken 0..1: se parte por el centro y cae. tension: brillo rojo."""
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + sag
    c = mix(col, (1.0, 0.2, 0.15), clamp(tension))
    if broken <= 0:
        ctx.move_to(x0, y0); ctx.curve_to(x0 + (mx - x0) * 0.6, my, x1 - (x1 - mx) * 0.6, my, x1, y1)
        stroke(ctx, c, w)
        return
    f = ease(clamp(broken))
    for (xa, ya), sgn in (((x0, y0), 1), ((x1, y1), -1)):
        ex, ey = mx - sgn * 10, my + 260 * f
        ctx.move_to(xa, ya); ctx.curve_to(xa + sgn * 30, ya + 60 * f, ex, ey - 80, ex - sgn * 40 * f, ey)
        stroke(ctx, c, w)
    if broken < 0.5:
        for k in range(6):
            ang = k * 1.1 + broken * 9
            ctx.move_to(mx, my); ctx.line_to(mx + 40 * math.cos(ang), my + 40 * math.sin(ang)); stroke(ctx, YELLOW, 5)


def thermo(ctx, x, y, s, temp, a=1.0):
    """Termómetro: temp en ºF (de 40 a -25)."""
    if a <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * a, s * a)
    rrect(ctx, -40, -230, 80, 330, 40); fill_ink(ctx, WHITE, 4)
    circle(ctx, 0, 110, 60); fill_ink(ctx, (0.25, 0.55, 1.0), 4)
    lvl = clamp((temp + 25) / 65)
    ctx.rectangle(-16, 100 - 300 * lvl, 32, 300 * lvl); fill(ctx, (0.25, 0.55, 1.0))
    ctx.restore()
    label(ctx, f"{int(temp)}°", x, y + 210 * s, a, rgb=(0.45, 0.72, 1.0), size=46)


def town(ctx, T, P, y=1000, lights=1.0, snow=0.0):
    sky(ctx, T, P)
    for k, hx in enumerate((150, 420, 690, 960)):
        house2(ctx, hx, y, 0.9, col=[(0.92, 0.62, 0.48), (0.62, 0.72, 0.90), (0.95, 0.80, 0.45), (0.70, 0.85, 0.60)][k])
        if lights < 1:
            ctx.rectangle(hx - 70, y - 120, 140, 120); fill(ctx, (0.05, 0.06, 0.15), 0.55 * (1 - lights))
    ground(ctx, y, P, col=mix(P["grass"], SNOW, snow))


def hero(ctx, lt, T, dur, z0, z1, gancho_on=False):
    """Primer plano: dos postes con el cable flojo y el chico en la escalera."""
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2, 760)
    sky(ctx, T, P)
    ground(ctx, 1250, P)
    a = pole(ctx, 170, 1250, 760)
    b = pole(ctx, 910, 1250, 760)
    wire(ctx, a, b, 190 + 8 * math.sin(T * 2), w=8)
    wire(ctx, (a[0] - 55, a[1]), (b[0] - 55, b[1]), 200 + 8 * math.sin(T * 2 + 1), w=8)
    worker(ctx, 300, 850, 0.7, T, col=KID, k=1, mood="feliz", hat=YELLOW)
    ctx.restore()


# 0.00 "This guy hung his power lines loose on purpose."
def e1(ctx, lt, dur, T):
    if T < 1.63:
        hero(ctx, lt, T, dur, 1.3, 1.15)
    else:   # "loose" -> corte seco: flojo ✓ contra tenso y roto ✗
        P = pal(T)
        ctx.save()
        camera(ctx, keyframes(lt - 1.63, [(0, 1.06), (dur - 1.63, 1.0)]), W / 2, 820)
        sky(ctx, T, P)
        ground(ctx, 1150, P, col=mix(P["grass"], SNOW, 0.7))
        a, b = pole(ctx, 80, 1150, 520, s=0.9), pole(ctx, 470, 1150, 520, s=0.9)
        wire(ctx, a, b, 130, w=7)
        c, d = pole(ctx, 610, 1150, 520, lean=0.12, s=0.9), pole(ctx, 1000, 1150, 520, lean=-0.12, s=0.9)
        wire(ctx, c, d, 0, w=7, broken=clamp((T - 1.9) / 0.5), tension=1.0)
        ctx.restore()
        check(ctx, 275, 1240, 0.9, pop(lt, 1.7), ok=True)
        check(ctx, 805, 1240, 0.9, pop(lt, 2.0), ok=False)
    gancho(ctx, ["WHY DO POWER LINES", ("HANG LOOSE?", WHITE)], T, t_fin=2.8, size=96)


# 2.85 "See, two crews are wiring the same town."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 850)
    town(ctx, T, P, 900)
    for k in range(3):
        p0, p1 = pole(ctx, 60 + k * 170, 1250, 450, s=0.8), pole(ctx, 230 + k * 170, 1250, 450, s=0.8)
        wire(ctx, p0, p1, 70, w=5)
    for k in range(3):
        p0, p1 = pole(ctx, 600 + k * 150, 1250, 450, s=0.8), pole(ctx, 750 + k * 150, 1250, 450, s=0.8)
        if k < 2:
            wire(ctx, p0, p1, 4, w=5)
    worker(ctx, 260, 1000, 0.55, T, col=KID, k=1, mood="feliz", hat=YELLOW)
    worker(ctx, 820, 1000, 0.55, T, col=RIV, k=2, mood="normal", hat=WHITE)
    ctx.restore()
    label(ctx, "THE KID", 260, 300, pop(lt, 0.2), rgb=KID, size=46)
    label(ctx, "RIVAL CREW", 820, 300, pop(lt, 0.4), rgb=RIV, size=46)


# 4.99 "His boss sees the cables drooping between the poles. Kid, it looks lazy."
def e3(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.1)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 900), sky(c, T, P), ground(c, 1250, P)))
    ctx.save()
    camera(ctx, z, W / 2, 900)
    a, b = pole(ctx, 450, 1250, 700), pole(ctx, 1020, 1250, 700)
    wire(ctx, a, b, 200, w=8)
    worker(ctx, 200, 860, 1.0, T, col=(0.55, 0.42, 0.30), boss=True, k=3,
           mood="shock" if T > 7.4 else "normal", tie=RED, hat_kind="none")
    ctx.restore()
    label(ctx, "BOSS", 200, 560, pop(lt, 0.2), rgb=GOLD, size=42)
    if T > 6.15:
        cota(ctx, 735, 600, 735, 760, pop(lt, 6.15 - 4.99), "DROOPING", rgb=YELLOW, size=40, dy=-120)
    bubble(ctx, "KID, IT LOOKS LAZY!", W / 2, 300, pop(lt, 7.44 - 4.99), size=50)


# 8.73 "The other crew pulls every wire tight. Straight as a ruler. The whole town loves it."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 850)
    town(ctx, T, P, 1000)
    a, b = pole(ctx, 120, 1250, 700), pole(ctx, 960, 1250, 700)
    sag = 140 * (1 - ease(clamp((T - 9.44) / 0.8)))
    wire(ctx, a, b, sag, w=8)
    worker(ctx, 540, 1000, 0.7, T, col=RIV, k=2, mood="feliz", hat=WHITE, arm=0.5)
    if T > 10.91:  # regla
        ax = pop(lt, 10.91 - 8.73)
        ctx.save(); ctx.translate(540, a[1] - 60); ctx.scale(ax, ax)
        rrect(ctx, -380, -30, 760, 60, 8); fill_ink(ctx, (0.98, 0.85, 0.35), 4)
        for k in range(-18, 19):
            ctx.move_to(k * 20, -30); ctx.line_to(k * 20, -30 + (24 if k % 5 == 0 else 12)); stroke(ctx, INKC, 3)
        ctx.restore()
    ctx.restore()
    label(ctx, "RIVAL: TIGHT", W / 2, 300, pop(lt, 0.3), rgb=RIV, size=50)
    if T > 12.47:
        for k in range(3):
            icon(ctx, "❤️", 260 + k * 280, 1200 - 30 * math.sin(T * 3 + k), 100, pop(lt, 12.47 - 8.73 + 0.15 * k))


# 12.95 "Then winter comes. And cold metal shrinks."
def e5(ctx, lt, dur, T):
    P = pal(T)
    sn = ease(clamp((T - 13.2) / 0.8))
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 850)
    town(ctx, T, P, 1000, snow=sn)
    a, b = pole(ctx, 120, 1250, 700), pole(ctx, 960, 1250, 700)
    wire(ctx, a, b, 0, w=8, tension=0.5 * ease(clamp((T - 14.7) / 0.5)))
    ctx.restore()
    for k in range(40):
        fx = (k * 137 + T * 60) % 1100 - 10
        fy = (k * 211 + T * 220) % 1500
        circle(ctx, fx, fy, 6); fill(ctx, WHITE, 0.8 * sn)
    thermo(ctx, 900, 560, 0.8, 40 - 40 * sn, pop(lt, 0.3))
    label(ctx, "WINTER", 300, 300, pop(lt, 13.38 - 12.95), rgb=(0.45, 0.72, 1.0), size=56)
    if T > 14.69:
        a2 = pop(lt, 14.69 - 12.95)
        arrow(ctx, 120, 420, 380, 420, a2, rgb=RED, w=12)
        arrow(ctx, 960, 420, 700, 420, a2, rgb=RED, w=12)
        label(ctx, "METAL SHRINKS", 540, 500, a2, rgb=RED, size=44)


# 15.64 "Every night, the tight wires get a little shorter, pulling harder and harder on the poles."
def e6(ctx, lt, dur, T):
    P = pal(T)
    p = ease(clamp((T - 16.4) / 3.0))
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 850)
    town(ctx, T, P, 1000, snow=1.0)
    a, b = pole(ctx, 150, 1250, 700, lean=0.10 * p), pole(ctx, 930, 1250, 700, lean=-0.10 * p)
    wire(ctx, a, b, -4, w=8, tension=0.5 + 0.5 * p)
    ctx.restore()
    n = 1 + int(p * 29)
    cal(ctx, 540, 330, 0.7, "NIGHT", str(n), col=(0.30, 0.45, 0.85))
    if T > 17.92:
        a2 = pop(lt, 17.92 - 15.64)
        arrow(ctx, 300, 640, 180, 600, a2, rgb=RED, w=12)
        arrow(ctx, 780, 640, 900, 600, a2, rgb=RED, w=12)
        label(ctx, "PULLING HARDER", 540, 1200, a2, rgb=RED, size=46)


# 20.06 "Ten below, the poles start to lean. Twenty below, snap. The whole street goes dark."
def e7(ctx, lt, dur, T):
    P = pal(T)
    br = clamp((T - 22.69) / 0.6)
    dark = ease(clamp((T - 23.6) / 0.6))
    lean = 0.10 + 0.08 * ease(clamp((T - 20.6) / 1.2)) - 0.08 * ease(br)
    ctx.save()
    camera(ctx, punch(lt - 2.6, big=1.25, end=1.05, dur=dur - 2.6) if T > 22.69 else keyframes(lt, [(0, 1.0), (2.6, 1.08)]), W / 2, 850)
    town(ctx, T, P, 1000, lights=1 - dark, snow=1.0)
    ctx.set_source_rgba(0.05, 0.06, 0.18, 0.45 * dark); ctx.paint()
    a, b = pole(ctx, 150, 1250, 700, lean=lean), pole(ctx, 930, 1250, 700, lean=-lean)
    wire(ctx, a, b, -4, w=8, tension=1.0, broken=br)
    ctx.restore()
    temp = -10 if T < 21.97 else -20
    thermo(ctx, 900, 560, 0.75, temp, 1.0)
    if T > 22.69:
        stamp(ctx, "SNAP!", 420, 330, (T - 22.69) / 0.25, size=110)
    if T > 23.77:
        label(ctx, "BLACKOUT", 420, 1250, pop(lt, 24.0 - 20.06), rgb=RED, size=52)


# 24.63 "The kid's wires just lose a little droop."
def e8(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.12)]), W / 2, 850)
    town(ctx, T, P, 1000, snow=1.0)
    a, b = pole(ctx, 120, 1250, 700), pole(ctx, 960, 1250, 700)
    sag = 200 - 70 * ease(clamp((T - 25.6) / 0.8))
    wire(ctx, a, b, sag, w=8)
    worker(ctx, 540, 1000, 0.7, T, col=KID, k=1, mood="feliz", hat=YELLOW)
    ctx.restore()
    label(ctx, "THE KID'S WIRES", W / 2, 300, pop(lt, 0.2), rgb=KID, size=48)
    check(ctx, 900, 480, 1.0, pop(lt, 26.25 - 24.63), ok=True)


# 26.60 "You see, a sagging wire has room to shrink. A tight wire doesn't."  (luz azul)
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 800)
    sky(ctx, T, P)
    ctx.restore()
    # arriba: cable flojo que encoge sin problema; abajo: cable tenso que ya no tiene margen
    sh = 0.5 + 0.5 * math.sin(T * 2.2)
    a, b = (120, 480), (960, 480)
    for x in (a, b):
        circle(ctx, *x, 16); fill_ink(ctx, POLE, 3)
    wire(ctx, a, b, 160 - 70 * sh, w=9)
    cota(ctx, 540, 485, 540, 485 + 160 - 70 * sh, pop(lt, 27.6 - 26.6), "ROOM TO SHRINK", rgb=(0.30, 0.78, 0.40), size=40, dy=-150)
    if T > 28.79:
        a2 = pop(lt, 28.79 - 26.6)
        c, d = (120, 1000), (960, 1000)
        for x in (c, d):
            circle(ctx, *x, 16 * a2); fill_ink(ctx, POLE, 3)
        wire(ctx, c, d, 0, w=9, tension=0.6 + 0.4 * sh)
        label(ctx, "NO ROOM", 540, 1120, a2, rgb=RED, size=50)
        check(ctx, 540, 1240, 0.9, pop(lt, 29.67 - 26.6), ok=False)


# 30.02 "Like a rubber band already stretched all the way, one more pull and it breaks."
def e10(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 800)
    sky(ctx, T, P)
    ctx.restore()
    st = ease(clamp((T - 30.6) / 1.4))
    br = clamp((T - 33.38) / 0.4)
    L = 140 + 300 * st + 40 * ease(clamp((T - 32.83) / 0.5))
    for sgn in (-1, 1):
        circle(ctx, W / 2 + sgn * L, 800, 60); fill_ink(ctx, (0.96, 0.78, 0.62), 4)
    if br <= 0:
        ctx.move_to(W / 2 - L, 780); ctx.line_to(W / 2 + L, 780); ctx.move_to(W / 2 - L, 820); ctx.line_to(W / 2 + L, 820)
        stroke(ctx, mix((0.95, 0.55, 0.25), RED, st), 18 - 8 * st)
    else:
        for sgn in (-1, 1):
            ctx.move_to(W / 2 + sgn * L, 800); ctx.line_to(W / 2 + sgn * (L - 160 * (1 - br) - 40), 800 + 60 * br)
            stroke(ctx, (0.95, 0.55, 0.25), 14)
        stamp(ctx, "SNAP!", W / 2, 560, (T - 33.38) / 0.25, size=100)
    label(ctx, "RUBBER BAND", W / 2, 300, pop(lt, 30.24 - 30.02), rgb=YELLOW, size=52)
    if T > 31.22:
        label(ctx, "STRETCHED ALL THE WAY", W / 2, 1050, pop(lt, 31.22 - 30.02), rgb=RED, size=42)


# 33.81 "In other words, the tight wires weren't strong. They had nowhere to go."
def e11(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.08, dur=dur), W / 2, 820)
    sky(ctx, T, P)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.22); ctx.paint()
    a, b = pole(ctx, 150, 1250, 700, lean=0.12), pole(ctx, 930, 1250, 700, lean=-0.12)
    wire(ctx, a, b, -4, w=9, tension=1.0)
    ctx.restore()
    if T > 35.30:
        stamp(ctx, "NOT STRONG", W / 2, 300, (T - 35.30) / 0.25, size=96)
    if T > 36.38:
        stamp(ctx, "NO ROOM", W / 2, 1200, (T - 36.38) / 0.25, col=RED, size=110)


# 37.12 "That's why the power lines on your street hang loose."
def e12(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.1)])
    ctx.save()
    camera(ctx, z, W / 2, 860)
    town(ctx, T, P, 1000)
    ps = [pole(ctx, 60 + k * 320, 1250, 650, s=0.9) for k in range(4)]
    for k in range(3):
        wire(ctx, ps[k], ps[k + 1], 90, w=6)
    ctx.restore()
    label(ctx, "YOUR STREET", W / 2, 300, pop(lt, 38.50 - 37.12), rgb=YELLOW, size=54)
    if T > 38.80:
        label(ctx, "LOOSE ON PURPOSE", W / 2, 1220, pop(lt, 38.80 - 37.12), rgb=(0.30, 0.78, 0.40), size=46)


# 39.44 "Because, just like" -> bucle (acaba en el encuadre del fotograma 0)
def e13(ctx, lt, dur, T):
    hero(ctx, lt, T, dur, 1.15, 1.3)


ESCENAS = [(0.0, e1), (2.85, e2), (4.99, e3), (8.73, e4), (12.95, e5), (15.64, e6), (20.06, e7), (24.63, e8),
           (26.60, e9), (30.02, e10), (33.81, e11), (37.12, e12), (39.44, e13)]

SFX = [(0.1, "pop"), (1.63, "thud"), (1.95, "crack"), (2.8, "whoosh"), (4.95, "whoosh"), (6.2, "pop"), (7.44, "drum"),
       (8.7, "whoosh"), (9.5, "squish"), (10.9, "ding"), (12.5, "pop"), (12.9, "whoosh"), (13.4, "rise"),
       (14.7, "squish"), (15.6, "whoosh"), (16.5, "tick"), (17.5, "tick"), (18.5, "tick"), (19.5, "tick"),
       (20.06, "thud"), (21.97, "thud"), (22.69, "crack"), (23.8, "thud"), (24.6, "whoosh"), (26.25, "ding"),
       (26.55, "whoosh"), (28.8, "pop"), (29.7, "thud"), (30.0, "whoosh"), (31.2, "rise"), (33.38, "crack"),
       (33.78, "thud"), (35.30, "thud"), (36.38, "thud"), (37.1, "whoosh"), (38.8, "pop"), (39.4, "whoosh")]


def MINIATURA(ctx):
    T = 0.5
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    sky(ctx, T, P)
    ground(ctx, 1600, P, col=mix(P["grass"], SNOW, 0.6))
    a, b = pole(ctx, 120, 1600, 900), pole(ctx, 960, 1600, 900)
    wire(ctx, a, b, 260, w=12)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["WHY ARE THEY", ("SO LOOSE?", WHITE)], y=260, size=150)
    thumb_circle(ctx, W / 2, 1000, 250, 130)
