"""v30 (EN) formato «historia» (inventada, física real): por qué las ventanillas de avión son redondas (concentración de tensiones)."""
from kit import *  # noqa
from estilo_v3 import *  # noqa

FLASH = False
WHOOSH = False
MUSICA_GAIN = 0.42
FX_GAIN = 0.30
Y_SUBTITULO = 1430     # subtítulos ABAJO
TAM_SUBTITULO = 135
set_azul(27.06, 41.13)  # "You see" -> "Their corners were."
CORTES = [(4.96, 7.52)]  # quitado "and the airline will buy whichever one looks the most modern." (relleno en el tramo 4-9 s)

KID = (0.25, 0.50, 0.85)
RIV = (0.88, 0.25, 0.25)
BODY = (0.93, 0.94, 0.97)
FLOW = (0.40, 0.85, 1.0)
HOT = (1.0, 0.25, 0.20)


def window(ctx, x, y, w, h, rnd=True, a=1.0):
    r = min(w, h) * 0.48 if rnd else 2
    rrect(ctx, x - w / 2, y - h / 2, w, h, r); fill_ink(ctx, (0.55, 0.58, 0.66), 4, a)
    rrect(ctx, x - w / 2 + 8, y - h / 2 + 8, w - 16, h - 16, max(r - 8, 1)); fill(ctx, GLASS, a)


def plane(ctx, x, y, s, T, col=KID, rnd=True, stretch=1.0, n=5):
    """Fuselaje de lado con ventanillas; stretch hincha el cuerpo (presurización)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s * stretch)
    # cola
    ctx.move_to(-380, -40); ctx.line_to(-470, -230); ctx.line_to(-400, -230); ctx.line_to(-300, -60); ctx.close_path()
    fill_ink(ctx, col, 4)
    # ala (detrás)
    ctx.move_to(-60, 40); ctx.line_to(-200, 210); ctx.line_to(-120, 210); ctx.line_to(80, 40); ctx.close_path()
    fill_ink(ctx, mix(BODY, (0.5, 0.5, 0.6), 0.25), 4)
    # cuerpo
    ctx.move_to(-440, -70); ctx.line_to(330, -80); ctx.curve_to(460, -80, 480, 30, 440, 60)
    ctx.line_to(-400, 80); ctx.curve_to(-470, 60, -470, -50, -440, -70); ctx.close_path()
    fill_ink(ctx, BODY, 5)
    ctx.rectangle(-430, 30, 860, 18); fill(ctx, col)
    ctx.move_to(360, -60); ctx.curve_to(410, -60, 430, -30, 430, -20); ctx.line_to(360, -20); ctx.close_path()
    fill_ink(ctx, (0.25, 0.30, 0.40), 3)
    for k in range(n):
        window(ctx, -300 + k * 130, -20, 56, 62 if rnd else 70, rnd)
    ctx.restore()


def flow_lines(ctx, cx, cy, hw, hh, T, rnd=True, a=1.0, n=11, span=440):
    """Líneas de fuerza que rodean una ventana (como agua alrededor de una roca)."""
    for i in range(n):
        y0 = -span / 2 + i * span / (n - 1)
        if abs(y0) < 4:
            continue
        sgn = 1 if y0 > 0 else -1
        ctx.new_path()
        for j in range(0, 101):
            x = -500 + j * 10
            if rnd:
                g = math.exp(-(x / (hw * 1.25)) ** 2)
            else:
                g = 1.0 if abs(x) < hw + 6 else math.exp(-((abs(x) - hw) / 18) ** 2)
            push = max(0.0, (hh + 22) - abs(y0) * 0.55)
            yy = y0 + sgn * push * g * (1 - abs(y0) / (span / 2 + 40))
            if j == 0:
                ctx.move_to(cx + x, cy + yy)
            else:
                ctx.line_to(cx + x, cy + yy)
        stroke(ctx, FLOW, 6, 0.85 * a)
        # partículas
        ph = (T * 0.6 + i * 0.13) % 1.0
        x = -500 + 1000 * ph
        if rnd:
            g = math.exp(-(x / (hw * 1.25)) ** 2)
        else:
            g = 1.0 if abs(x) < hw + 6 else math.exp(-((abs(x) - hw) / 18) ** 2)
        push = max(0.0, (hh + 22) - abs(y0) * 0.55)
        circle(ctx, cx + x, cy + y0 + sgn * push * g * (1 - abs(y0) / (span / 2 + 40)), 9); fill(ctx, WHITE, a)


def hot(ctx, x, y, r, T, a=1.0):
    for k in range(4, 0, -1):
        circle(ctx, x, y, r * k / 4 * (1 + 0.08 * math.sin(T * 9))); fill(ctx, HOT, 0.22 * a)


def hero(ctx, lt, T, dur, z0, z1):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2, 820)
    sky(ctx, T, P)
    ground(ctx, 1150, P, col=P["conc"])
    # pared del fuselaje gigante con ventanilla redonda
    rrect(ctx, 120, 420, 700, 640, 40); fill_ink(ctx, BODY, 6)
    window(ctx, 470, 740, 300, 400, rnd=True)
    worker(ctx, 940, 860, 0.75, T, col=KID, k=1, mood="feliz", hat_kind="cap", hat=KID)
    ctx.restore()
    label(ctx, "ROUND", 470, 330, 1.0, rgb=YELLOW, size=54)


# 0.03 "This guy made the windows on his airplane round on purpose."
def e1(ctx, lt, dur, T):
    if T < 1.95:   # 0-1.95: primer plano de la ventanilla redonda, entrando con la cámara (nada estático)
        P = pal(T)
        ctx.save()
        camera(ctx, keyframes(lt, [(0, 1.35), (1.95, 1.15)]), 470, 760)
        sky(ctx, T, P)
        ground(ctx, 1150, P, col=P["conc"])
        rrect(ctx, 120, 420, 700, 640, 40); fill_ink(ctx, BODY, 6)
        window(ctx, 470, 740, 300, 400, rnd=True)
        ctx.restore()
    else:          # "round" -> corte seco: redonda ✓ contra cuadrada con grieta ✗
        P = pal(T)
        ctx.save()
        camera(ctx, keyframes(lt - 1.95, [(0, 1.08), (dur - 1.95, 1.0)]), W / 2, 800)
        sky(ctx, T, P)
        rrect(ctx, 60, 470, W - 120, 640, 40); fill_ink(ctx, BODY, 6)
        window(ctx, 300, 790, 250, 340, rnd=True)
        window(ctx, 780, 790, 270, 330, rnd=False)
        crack_path(ctx, zig(915, 625, 1010, 520, 4, 10, 2), 6)
        hot(ctx, 915, 625, 45, T)
        ctx.restore()
        check(ctx, 300, 1230, 0.9, pop(lt, 1.95 + 0.05), ok=True)
        check(ctx, 780, 1230, 0.9, pop(lt, 1.95 + 0.25), ok=False)
    gancho(ctx, ["WHY ARE PLANE", ("WINDOWS ROUND?", WHITE)], T, t_fin=2.9, size=100)


# 3.21 "See, two companies are building jets, and the airline will buy whichever one looks the most modern."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 0.98)]), W / 2, 820)
    sky(ctx, T, P)
    ground(ctx, 1150, P, col=P["conc"])
    plane(ctx, 300, 640, 0.55, T, col=KID, rnd=True, n=4)
    plane(ctx, 780, 980, 0.55, T, col=RIV, rnd=False, n=4)
    ctx.restore()
    label(ctx, "THE KID", 300, 470, pop(lt, 0.2), rgb=KID, size=40)
    label(ctx, "RIVAL", 780, 810, pop(lt, 0.4), rgb=RIV, size=40)
    a = pop(lt, 5.24 - 3.21)
    if a > 0.01:
        icon(ctx, "💰", 880, 470, 150, a)
        label(ctx, "AIRLINE", 880, 330, a, rgb=YELLOW, size=42)
    if T > 6.95:
        label(ctx, "MOST MODERN WINS", W / 2, 1270, pop(lt, 6.95 - 3.21), rgb=YELLOW, size=44)


# 7.56 "His boss sees the round windows. Kid, it looks like a washing machine."
def e3(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 900), sky(c, T, P), ground(c, 1150, P, col=P["conc"])))
    ctx.save()
    camera(ctx, z, W / 2, 900)
    rrect(ctx, 480, 520, 520, 520, 30); fill_ink(ctx, BODY, 5)
    window(ctx, 740, 780, 220, 290, rnd=True)
    worker(ctx, 230, 760, 1.0, T, col=(0.55, 0.42, 0.30), boss=True, k=3, mood="shock" if T > 9.4 else "normal",
           tie=RED, hat_kind="none")
    ctx.restore()
    label(ctx, "BOSS", 230, 470, pop(lt, 0.2), rgb=GOLD, size=42)
    a = pop(lt, 10.46 - 7.56)
    if a > 0.01:
        ctx.save(); ctx.translate(820, 360); ctx.scale(a * 0.8, a * 0.8)
        rrect(ctx, -110, -130, 220, 260, 16); fill_ink(ctx, WHITE, 4)
        circle(ctx, 0, 20, 75); fill_ink(ctx, (0.6, 0.62, 0.7), 4); circle(ctx, 0, 20, 55); fill(ctx, GLASS)
        ctx.restore()
    bubble(ctx, "KID, IT LOOKS LIKE A WASHING MACHINE!", W / 2, 1230, pop(lt, 9.42 - 7.56), size=36)


# 11.16 "The other company goes square. Big, sharp, beautiful windows. Passengers love them."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 860)
    sky(ctx, T, P)
    ground(ctx, 1150, P, col=P["conc"])
    rrect(ctx, 100, 480, 880, 600, 30); fill_ink(ctx, BODY, 5)
    g = ease_back(clamp((T - 12.2) / 0.6))
    if g > 0.01:
        for k in range(2):
            window(ctx, 320 + k * 440, 780, 330 * g, 380 * g, rnd=False)
    ctx.restore()
    label(ctx, "RIVAL", W / 2, 260, pop(lt, 0.2), rgb=RIV, size=44)
    if T > 12.42:
        label(ctx, "SQUARE", 320, 520, pop(lt, 12.42 - 11.16), rgb=YELLOW, size=46)
    if T > 13.20:
        label(ctx, "SHARP CORNERS", 760, 520, pop(lt, 13.20 - 11.16), rgb=YELLOW, size=40)
    if T > 14.69:
        for k in range(3):
            icon(ctx, "❤️", 260 + k * 280, 1180 - 30 * math.sin(T * 3 + k), 110, pop(lt, 15.23 - 11.16 + 0.15 * k))


# 15.87 "Then the planes start flying. Every flight, the cabin is pumped full of air, and the whole body stretches like a balloon. Then it lands and shrinks back."
def e5(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 820)
    sky(ctx, T, P, sun=True)
    for k in range(4):  # nubes
        cx = (k * 400 - T * 160) % 1500 - 200
        for d in (-50, 0, 50):
            circle(ctx, cx + d, 1150 + 40 * (k % 2) - (30 if d == 0 else 0), 60); fill(ctx, WHITE, 0.9)
    ctx.restore()
    inflate = ease(clamp((T - 18.3) / 1.6)) * (1 - ease(clamp((T - 21.7) / 0.7)))
    # sección del fuselaje: círculo que se hincha
    r = 260 * (1 + 0.16 * inflate)
    circle(ctx, W / 2, 760, r); fill_ink(ctx, BODY, 7)
    circle(ctx, W / 2, 760, r - 34); fill(ctx, (0.80, 0.88, 1.0))
    ctx.rectangle(W / 2 - r + 40, 860, 2 * r - 80, 18); fill(ctx, (0.55, 0.55, 0.62))
    for k in range(int(6 * clamp((T - 17.8) / 0.8))):  # aire entrando
        ang = k * math.tau / 6 + T
        arrow(ctx, W / 2 + math.cos(ang) * 60, 760 + math.sin(ang) * 60,
              W / 2 + math.cos(ang) * (r - 60), 760 + math.sin(ang) * (r - 60), inflate, rgb=FLOW, w=9)
    label(ctx, "CABIN", W / 2, 420 - 40 * inflate, pop(lt, 17.82 - 15.87), rgb=WHITE, size=42)
    if T > 20.17:
        icon(ctx, "🎈", 900, 330, 160, pop(lt, 20.6 - 15.87) * (1 - ease(clamp((T - 21.7) / 0.5))))
        label(ctx, "STRETCH", 240, 330, pop(lt, 20.17 - 15.87) * (1 - ease(clamp((T - 21.7) / 0.5))), rgb=YELLOW, size=46)
    if T > 21.71:
        label(ctx, "SHRINK", W / 2, 1210, pop(lt, 22.14 - 15.87), rgb=(0.75, 0.75, 0.85), size=46)


# 22.86 "Flight one, nothing. Flight one thousand, a hairline crack. Right at a sharp corner."
def e6(ctx, lt, dur, T):
    P = pal(T)
    zoom = keyframes(lt, [(0, 1.0), (24.8 - 22.86, 1.0), (26.4 - 22.86, 1.8), (dur, 1.9)])
    ctx.save()
    camera(ctx, zoom, 630, 640)
    sky(ctx, T, P)
    rrect(ctx, 120, 360, 840, 820, 30); fill_ink(ctx, BODY, 5)
    window(ctx, 540, 780, 380, 440, rnd=False)
    if T > 25.03:
        p = ease(clamp((T - 25.03) / 1.3))
        crack_path(ctx, partial(zig(730, 560, 900, 400, 7, 14, 4), p), 6)
        hot(ctx, 730, 560, 50, T, p)
    ctx.restore()
    n = "1" if T < 23.84 else f"{int(1 + 999 * ease(clamp((T - 23.84) / 0.6))):,}"
    label(ctx, f"FLIGHT {n}", W / 2, 260, 1.0, rgb=YELLOW, size=54)
    if T < 23.84:
        check(ctx, W / 2, 1270, 0.9, pop(lt, 23.43 - 22.86), ok=True)
    if T > 25.03:
        label(ctx, "HAIRLINE CRACK", W / 2, 1270, pop(lt, 25.03 - 22.86), rgb=HOT, size=46)


# 27.06 "You see, when metal stretches, the force flows around a window like water around a rock."  (luz azul)
def e7(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 760)
    sky(ctx, T, P, sun=True)
    rrect(ctx, 40, 420, W - 80, 680, 30); fill_ink(ctx, mix(BODY, (0.3, 0.32, 0.5), 0.55), 5)
    window(ctx, W / 2, 760, 200, 250, rnd=True)
    flow_lines(ctx, W / 2, 760, 100, 125, T, rnd=True, a=pop(lt, 28.82 - 27.06))
    ctx.restore()
    label(ctx, "FORCE FLOWS", W / 2, 300, pop(lt, 28.82 - 27.06), rgb=FLOW, size=50)
    a = pop(lt, 30.31 - 27.06)
    if a > 0.01:
        ctx.save(); ctx.translate(W / 2, 1240); ctx.scale(a, a)
        rrect(ctx, -300, -60, 600, 120, 30); fill_ink(ctx, (0.20, 0.45, 0.80), 4)
        ellipse(ctx, 0, 0, 70, 40); fill_ink(ctx, (0.55, 0.52, 0.50), 4)
        for k in range(3):
            ph = (T * 0.8 + k / 3) % 1.0
            x = -280 + 560 * ph
            ctx.move_to(x - 40, -30 - 20 * math.exp(-(x / 90) ** 2)); ctx.line_to(x, -30 - 20 * math.exp(-(x / 90) ** 2))
            stroke(ctx, WHITE, 5)
        ctx.restore()
        label(ctx, "WATER AROUND A ROCK", W / 2, 1110, a, rgb=WHITE, size=38)


# 31.44 "A round window lets it flow. A sharp corner traps it all in one tiny point."
def e8(ctx, lt, dur, T):
    P = pal(T)
    sq = T > 32.95
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 760)
    sky(ctx, T, P, sun=True)
    rrect(ctx, 40, 420, W - 80, 680, 30); fill_ink(ctx, mix(BODY, (0.3, 0.32, 0.5), 0.55), 5)
    if not sq:
        window(ctx, W / 2, 760, 200, 250, rnd=True)
        flow_lines(ctx, W / 2, 760, 100, 125, T, rnd=True)
    else:
        window(ctx, W / 2, 760, 220, 260, rnd=False)
        flow_lines(ctx, W / 2, 760, 110, 130, T, rnd=False)
        hp = ease(clamp((T - 33.74) / 0.5))
        for sx in (-1, 1):
            for sy in (-1, 1):
                hot(ctx, W / 2 + sx * 110, 760 + sy * 130, 70, T, hp)
    ctx.restore()
    if not sq:
        label(ctx, "ROUND = IT FLOWS", W / 2, 300, pop(lt, 0.15), rgb=(0.30, 0.78, 0.40), size=48)
        check(ctx, W / 2, 1220, 0.9, pop(lt, 32.2 - 31.44), ok=True)
    else:
        label(ctx, "CORNER = TRAPPED", W / 2, 300, pop(lt, 32.95 - 31.44), rgb=HOT, size=48)
        if T > 34.88:
            label(ctx, "ONE TINY POINT", W / 2, 1220, pop(lt, 34.88 - 31.44), rgb=HOT, size=44)
            arrow(ctx, W / 2 + 260, 1170, W / 2 + 130, 910, pop(lt, 34.95 - 31.44), rgb=HOT, w=10)


# 35.62 "Like ripping paper, it always tears at the notch."
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 780)
    sky(ctx, T, P, sun=True)
    ctx.restore()
    p = ease(clamp((T - 36.6) / 0.9))
    gap = 50 * ease(clamp((T - 37.5) / 0.4))
    pts = zig(W / 2, 470, W / 2 - 30, 1130, 9, 22, 11)
    PAPER = (0.98, 0.96, 0.90)
    if gap < 0.5:
        ctx.move_to(W / 2 - 330, 420); ctx.line_to(W / 2 - 36, 420); ctx.line_to(W / 2, 470); ctx.line_to(W / 2 + 36, 420)
        ctx.line_to(W / 2 + 330, 420); ctx.line_to(W / 2 + 330, 1130); ctx.line_to(W / 2 - 330, 1130); ctx.close_path()
        fill_ink(ctx, PAPER, 4)
        crack_path(ctx, partial(pts, p), 7)
    else:
        for side in (-1, 1):
            ctx.save(); ctx.translate(side * gap / 2, 0)
            ctx.move_to(W / 2 + side * 330, 420); ctx.line_to(W / 2 + side * 36, 420)
            for q in pts:
                ctx.line_to(*q)
            ctx.line_to(W / 2 + side * 330, 1130); ctx.close_path()
            fill_ink(ctx, PAPER, 4)
            ctx.restore()
    # dedos tirando
    for side in (-1, 1):
        circle(ctx, W / 2 + side * (360 + gap / 2), 800, 60); fill_ink(ctx, (0.96, 0.78, 0.62), 4)
    label(ctx, "NOTCH", W / 2 + 190, 330, pop(lt, 37.64 - 35.62 - 1.2), rgb=HOT, size=46)
    arrow(ctx, W / 2 + 130, 370, W / 2 + 20, 450, pop(lt, 37.64 - 35.62 - 1.2), rgb=HOT, w=9)
    label(ctx, "RIP!", W / 2 - 250, 1220, pop(lt, 36.34 - 35.62), rgb=YELLOW, size=50)


# 38.08 "In other words, the square windows weren't weak. Their corners were."
def e10(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.08, dur=dur), W / 2, 780)
    sky(ctx, T, P)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.22); ctx.paint()
    rrect(ctx, 190, 480, 700, 600, 30); fill_ink(ctx, BODY, 5)
    window(ctx, W / 2, 780, 360, 400, rnd=False)
    if T > 40.30:
        for sx in (-1, 1):
            for sy in (-1, 1):
                hot(ctx, W / 2 + sx * 180, 780 + sy * 200, 80, T, pop(lt, 40.44 - 38.08))
    ctx.restore()
    if T > 39.64:
        stamp(ctx, "NOT WEAK", W / 2, 300, (T - 39.64) / 0.25, col=(0.30, 0.78, 0.40), size=96)
    if T > 40.44:
        stamp(ctx, "CORNERS", W / 2, 1240, (T - 40.44) / 0.25, size=110)


# 41.25 "That's why the window next to your airplane seat is round."
def e11(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    ctx.save()
    camera(ctx, z, W / 2, 800)
    ctx.rectangle(-600, -600, W + 1200, H + 1200); fill(ctx, (0.88, 0.88, 0.92))
    rrect(ctx, 300, 420, 420, 560, 200); fill_ink(ctx, (0.80, 0.80, 0.86), 5)
    rrect(ctx, 360, 480, 300, 440, 150); fill_ink(ctx, P["sky0"], 4)
    circle(ctx, 420 + (T * 40) % 300, 760, 40); fill(ctx, WHITE, 0.8)
    # asiento
    rrect(ctx, 650, 640, 300, 560, 60); fill_ink(ctx, (0.25, 0.35, 0.65), 5)
    rrect(ctx, 680, 600, 240, 120, 40); fill_ink(ctx, (0.95, 0.95, 0.98), 4)
    ctx.restore()
    label(ctx, "YOUR SEAT", 800, 300, pop(lt, 42.33 - 41.25), rgb=YELLOW, size=48)
    if T > 43.29:
        label(ctx, "ROUND", 510, 1100, pop(lt, 43.29 - 41.25), rgb=(0.30, 0.78, 0.40), size=50)


# 43.72 "Because, just like" -> bucle
def e12(ctx, lt, dur, T):
    # termina en el mismo plano que el fotograma 0 (bucle)
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.35)]), 470, 760)
    sky(ctx, T, P)
    ground(ctx, 1150, P, col=P["conc"])
    rrect(ctx, 120, 420, 700, 640, 40); fill_ink(ctx, BODY, 6)
    window(ctx, 470, 740, 300, 400, rnd=True)
    ctx.restore()


ESCENAS = [(0.0, e1), (3.21, e2), (7.56, e3), (11.16, e4), (15.87, e5), (22.86, e6), (27.06, e7), (31.44, e8),
           (35.62, e9), (38.08, e10), (41.25, e11), (43.72, e12)]

SFX = [(0.1, "pop"), (1.95, "thud"), (2.3, "crack"), (3.2, "whoosh"), (5.2, "ding"), (7.0, "pop"), (7.5, "whoosh"), (9.4, "drum"), (10.5, "squish"),
       (11.1, "whoosh"), (12.3, "pop"), (13.2, "pop"), (14.7, "ding"), (15.8, "whoosh"), (18.3, "rise"),
       (20.6, "squish"), (21.7, "squish"), (22.8, "whoosh"), (23.4, "ding"), (23.84, "tick"), (24.0, "tick"),
       (24.2, "tick"), (25.03, "crack"), (26.5, "thud"), (27.0, "whoosh"), (28.8, "rise"), (30.3, "pop"),
       (31.4, "whoosh"), (32.2, "ding"), (32.95, "whoosh"), (33.74, "thud"), (35.6, "whoosh"), (36.6, "crack"),
       (37.64, "thud"), (38.05, "thud"), (39.64, "thud"), (40.44, "thud"), (41.2, "whoosh"), (43.29, "pop"),
       (43.7, "whoosh")]


def MINIATURA(ctx):
    T = 0.5
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    sky(ctx, T, P)
    rrect(ctx, 90, 620, 900, 1000, 40); fill_ink(ctx, BODY, 6)
    window(ctx, 310, 1120, 300, 420, rnd=True)
    window(ctx, 770, 1120, 320, 420, rnd=False)
    hot(ctx, 930, 910, 70, T)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["WHY ARE PLANE", ("WINDOWS ROUND?", WHITE)], y=260, size=140)
    thumb_circle(ctx, 310, 1120, 210, 260)
