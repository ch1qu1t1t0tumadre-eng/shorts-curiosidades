"""v04 (EN): Why airlines dim the lights before landing. Guion con estructura hook/loop/cuerpo/CTA."""
import math
from anim import *  # noqa

SEAT = (0.24, 0.36, 0.78)
SEAT_D = (0.16, 0.25, 0.58)
WALL = (0.86, 0.87, 0.92)
FLOOR = (0.30, 0.30, 0.42)
EXIT_G = (0.20, 0.95, 0.45)
VP = (540, 700)  # punto de fuga del pasillo


def lerp_c(a, b, x):
    return tuple(lerp(p, q, clamp(x)) for p, q in zip(a, b))


def dark(ctx, a):
    if a > 0:
        ctx.rectangle(-3000, -3000, 9000, 9000)
        fill(ctx, (0.01, 0.02, 0.06), a)


def cabin(ctx, T, light=1.0, path=0.0, rows=7, smoke=0.0):
    """Vista del pasillo de un avión en perspectiva. light 1=encendida, 0=a oscuras. path = luces de suelo."""
    vx, vy = VP
    # paredes y techo
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.80, 0.82, 0.88)), (1, (0.62, 0.64, 0.72))]))
    ctx.paint()
    # techo curvo
    ctx.move_to(-200, -100)
    ctx.curve_to(200, 520, 880, 520, 1280, -100)
    ctx.close_path()
    fill(ctx, (0.93, 0.93, 0.96))
    # tira de luz del techo
    ctx.move_to(vx - 18, vy - 60)
    ctx.line_to(vx - 260, -100)
    ctx.line_to(vx + 260, -100)
    ctx.line_to(vx + 18, vy - 60)
    ctx.close_path()
    fill(ctx, (1, 0.97, 0.85), 0.9 * light)
    # suelo / pasillo
    ctx.move_to(vx - 40, vy + 40)
    ctx.line_to(vx + 40, vy + 40)
    ctx.line_to(760, H + 200)
    ctx.line_to(320, H + 200)
    ctx.close_path()
    fill(ctx, FLOOR)
    # filas de asientos (de atrás hacia delante)
    for k in range(rows, 0, -1):
        d = k / rows          # 1 lejos .. 1/rows cerca
        s = 1 / (0.35 + d * 1.6)
        y = vy + 60 + 900 * s * 0.55
        for side in (-1, 1):
            x0 = vx + side * (70 + 300 * s)
            w, h = 300 * s, 360 * s
            rrect(ctx, x0 - w / 2, y - h, w, h, 40 * s)
            ctx.set_source(vgrad(ctx, 0, y - h, 0, y, [(0, SEAT), (1, SEAT_D)]))
            ctx.fill()
            rrect(ctx, x0 - w * 0.35, y - h + 18 * s, w * 0.7, 60 * s, 20 * s)
            fill(ctx, WHITE, 0.85)
            # ventanilla
            wx = vx + side * (300 + 520 * s)
            ellipse(ctx, wx, y - h * 1.15, 60 * s, 90 * s)
            fill(ctx, (0.25, 0.35, 0.60))
    # luces de suelo hacia la salida
    if path > 0:
        for k in range(14):
            u = k / 13
            for side in (-1, 1):
                x = lerp(vx + side * 34, 540 + side * 200, u ** 1.4)
                y = lerp(vy + 50, H + 60, u ** 1.4)
                r = lerp(4, 16, u)
                g = cairo.RadialGradient(x, y, 0, x, y, r * 4)
                g.add_color_stop_rgba(0, 1.0, 0.85, 0.35, 0.9 * path)
                g.add_color_stop_rgba(1, 1.0, 0.85, 0.35, 0)
                ctx.set_source(g)
                circle(ctx, x, y, r * 4)
                ctx.fill()
    dark(ctx, 0.82 * (1 - light))
    # cartel EXIT al fondo
    rrect(ctx, vx - 70, vy - 150, 140, 60, 10)
    fill(ctx, (0.05, 0.05, 0.05))
    text(ctx, "EXIT", vx, vy - 120, 38, EXIT_G, shadow=False)
    if path > 0 or light < 0.5:
        g = cairo.RadialGradient(vx, vy - 120, 10, vx, vy - 120, 160)
        g.add_color_stop_rgba(0, *EXIT_G, 0.35)
        g.add_color_stop_rgba(1, *EXIT_G, 0)
        ctx.set_source(g)
        circle(ctx, vx, vy - 120, 160)
        ctx.fill()
    if smoke > 0:
        smoke_layer(ctx, T, smoke)


def smoke_layer(ctx, T, a):
    rng = np.random.default_rng(5)
    for _ in range(40):
        x = rng.uniform(-200, W + 200) + 40 * math.sin(T * 0.6 + rng.uniform(0, 6))
        y = rng.uniform(0, H) - (T * 30 % 200)
        r = rng.uniform(140, 320)
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        g.add_color_stop_rgba(0, 0.55, 0.56, 0.60, 0.35 * a)
        g.add_color_stop_rgba(1, 0.55, 0.56, 0.60, 0)
        ctx.set_source(g)
        circle(ctx, x, y, r)
        ctx.fill()


def plane_top(ctx, x, y, s=1.0, exits_red=0.0, T=0.0):
    """Avión visto desde arriba, morro hacia arriba. exits_red: 0..1 (la mitad de salidas bloqueadas)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    body = (0.92, 0.93, 0.97)
    # alas
    ctx.move_to(-40, -40)
    ctx.line_to(-520, 160)
    ctx.line_to(-520, 220)
    ctx.line_to(-40, 120)
    ctx.close_path()
    ctx.move_to(40, -40)
    ctx.line_to(520, 160)
    ctx.line_to(520, 220)
    ctx.line_to(40, 120)
    ctx.close_path()
    fill(ctx, (0.75, 0.78, 0.86))
    # cola
    ctx.move_to(-30, 560)
    ctx.line_to(-200, 680)
    ctx.line_to(-200, 710)
    ctx.line_to(0, 660)
    ctx.line_to(200, 710)
    ctx.line_to(200, 680)
    ctx.line_to(30, 560)
    ctx.close_path()
    fill(ctx, (0.75, 0.78, 0.86))
    # fuselaje
    rrect(ctx, -90, -720, 180, 1400, 90)
    fill(ctx, body)
    ellipse(ctx, 0, -640, 50, 30)
    fill(ctx, (0.25, 0.35, 0.60))
    # salidas: 4 por lado
    ys = [-520, -160, 200, 470]
    for i, yy in enumerate(ys):
        for side in (-1, 1):
            bad = (i + (side > 0)) % 2 == 0
            col = lerp_c(EXIT_G, RED, exits_red if bad else 0)
            rrect(ctx, side * 90 - 14, yy - 34, 28, 68, 8)
            fill(ctx, col)
            if bad and exits_red > 0.5:
                ctx.move_to(side * 130 - 22, yy - 22)
                ctx.line_to(side * 130 + 22, yy + 22)
                ctx.move_to(side * 130 + 22, yy - 22)
                ctx.line_to(side * 130 - 22, yy + 22)
                stroke(ctx, RED, 10)
    ctx.restore()


def big_eye(ctx, x, y, s, pupil, T):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-330, 0)
    ctx.curve_to(-150, -230, 150, -230, 330, 0)
    ctx.curve_to(150, 230, -150, 230, -330, 0)
    ctx.close_path()
    fill_keep(ctx, WHITE)
    stroke(ctx, (0.20, 0.15, 0.20), 14)
    ctx.save()
    ctx.move_to(-330, 0)
    ctx.curve_to(-150, -230, 150, -230, 330, 0)
    ctx.curve_to(150, 230, -150, 230, -330, 0)
    ctx.clip()
    circle(ctx, 0, 0, 160)
    g = cairo.RadialGradient(0, 0, 20, 0, 0, 160)
    g.add_color_stop_rgb(0, 0.30, 0.55, 0.85)
    g.add_color_stop_rgb(1, 0.10, 0.25, 0.55)
    ctx.set_source(g)
    ctx.fill()
    circle(ctx, 0, 0, lerp(35, 120, pupil))
    fill(ctx, (0.03, 0.03, 0.05))
    circle(ctx, 50, -55, 26)
    fill(ctx, WHITE, 0.9)
    ctx.restore()
    ctx.restore()


def loading_bar(ctx, x, y, w, prog, label):
    rrect(ctx, x - w / 2, y - 26, w, 52, 26)
    fill(ctx, (1, 1, 1), 0.15)
    rrect(ctx, x - w / 2, y - 26, max(52, w * prog), 52, 26)
    fill(ctx, YELLOW)
    text(ctx, label, x, y - 70, 40, WHITE)


def flames(ctx, x, y, s, T, a=1.0):
    for k in range(7):
        ph = T * 9 + k * 1.7
        hgt = (120 + 60 * math.sin(ph)) * s
        cx = x + (k - 3) * 38 * s
        ctx.move_to(cx - 30 * s, y)
        ctx.curve_to(cx - 40 * s, y - hgt * 0.5, cx - 6 * s, y - hgt * 0.7, cx + 4 * math.sin(ph) * s, y - hgt)
        ctx.curve_to(cx + 10 * s, y - hgt * 0.6, cx + 40 * s, y - hgt * 0.4, cx + 30 * s, y)
        ctx.close_path()
        fill(ctx, (1.0, 0.45 + 0.2 * (k % 2), 0.10), 0.85 * a)


# ---------------- escenas ----------------
# 0.0 HOOK "Airlines turn off the lights before landing... and it's not so you can sleep."
def e1(ctx, lt, dur, T):
    off = ease((lt - 0.9) / 0.12)  # ¡clack! en el primer segundo
    z = keyframes(lt, [(0, 1.0), (1.0, 1.0), (1.3, 1.35), (dur, 1.5)])
    camera(ctx, z, W / 2, keyframes(lt, [(0, 960), (1.3, 1050), (dur, 1080)]))
    cabin(ctx, T, light=1 - off, path=off * 0.6)
    character(ctx, W / 2, 1180, 0.8, T, mood="sorpresa" if lt > 1.1 else "dormido", body=True, shirt=(0.85, 0.30, 0.35))
    if lt < 1.1:  # antifaz
        rrect(ctx, W / 2 - 150, 1150, 300, 70, 30)
        fill(ctx, (0.20, 0.20, 0.30))
    badge(ctx, "NOT FOR SLEEP", W / 2, 520, pop(lt, 3.0), size=60)


# 4.76 LOOP "Stay till the end, because there's one thing you should do in the last ten minutes of every flight."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_night(ctx, T)
    # nubes
    for k in range(5):
        x = (k * 260 - T * 120) % 1500 - 200
        for dx, r in ((0, 70), (60, 90), (130, 65)):
            circle(ctx, x + dx, 1250 + k * 40, r)
        fill(ctx, (0.25, 0.30, 0.50), 0.6)
    py = keyframes(lt, [(0, 820), (dur, 1000)])
    ctx.save()
    ctx.translate(W / 2, py)
    ctx.rotate(0.22)
    plane_top(ctx, 0, 0, 0.32)
    ctx.restore()
    secs = max(0, 600 - int(lt * 40))
    digital_clock(ctx, f"{secs // 60:02d}:{secs % 60:02d}", W / 2, 470, 1.05, pop(lt, 0.2))
    pill(ctx, "LAST 10 MIN", W / 2, 640, pop(lt, 2.2), rgb=RED)
    icon(ctx, "⏱", 870, 1180, 180, pop(lt, 1.2), rot=0.15 * math.sin(T * 4))


# 9.92 PROBLEMA "Your eyes need minutes to adjust to the dark. Minutes you don't have."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.18)]), W / 2, 900)
    bg_dark(ctx, T)
    big_eye(ctx, W / 2, 820, 1.25, ease(lt / (dur * 2.5)), T)
    loading_bar(ctx, W / 2, 1260, 640, clamp(lt / 14), "EYES ADJUSTING...")
    badge(ctx, "BLIND FOR MINUTES", W / 2, 400, pop(lt, 2.7), size=56)


# 14.32 DATO "Every plane must get everyone out in ninety seconds, using half the exits."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 980)
    bg_blueprint(ctx, T)
    plane_top(ctx, W / 2, 1070, 0.72, exits_red=ease((lt - 2.9) / 0.6), T=T)
    digital_clock(ctx, counter(lt - 0.6, 90, 0, 3.4) + "s", W / 2, 300, 0.9, pop(lt, 0.3))
    pill(ctx, "HALF THE EXITS", W / 2, 470, pop(lt, 3.1), rgb=RED)


# 18.6 EXPLICACIÓN "So the crew dims the cabin early. If the power dies, your eyes are already ready."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.25)]), W / 2, keyframes(lt, [(0, 960), (dur, 900)]))
    dim = ease(lt / 1.2)
    cabin(ctx, T, light=1 - 0.75 * dim, path=dim)
    pill(ctx, "EYES PRE-ADJUSTED", W / 2, 360, pop(lt, 2.6), rgb=EXIT_G)


# 23.52 GIRO "That's also why the shades go up: they need to see fire before opening a door."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 920)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.82, 0.83, 0.89)), (1, (0.66, 0.67, 0.75))]))
    ctx.paint()
    cx, cy = W / 2, 860
    # exterior por la ventanilla
    ctx.save()
    rrect(ctx, cx - 250, cy - 360, 500, 720, 230)
    ctx.clip()
    ctx.set_source(vgrad(ctx, 0, cy - 360, 0, cy + 360, [(0, (0.12, 0.14, 0.30)), (1, (0.35, 0.25, 0.35))]))
    ctx.paint()
    ctx.move_to(cx - 300, cy + 120)
    ctx.line_to(cx + 300, cy + 40)
    ctx.line_to(cx + 300, cy + 110)
    ctx.line_to(cx - 300, cy + 200)
    ctx.close_path()
    fill(ctx, (0.70, 0.72, 0.80))
    flames(ctx, cx + 60, cy + 90, 1.2, T, ease((lt - 2.2) / 0.5))
    # persiana que sube
    up = ease((lt - 0.3) / 1.2)
    ctx.rectangle(cx - 260, cy - 370, 520, 740 * (1 - up))
    fill(ctx, (0.92, 0.92, 0.95))
    ctx.restore()
    rrect(ctx, cx - 250, cy - 360, 500, 720, 230)
    stroke(ctx, (0.55, 0.57, 0.66), 40)
    pill(ctx, "SHADES UP", W / 2, 250, pop(lt, 0.8))
    badge(ctx, "= SEE FIRE", W / 2, 390, pop(lt, 2.6), size=60)
    icon(ctx, "🚪", 900, 1200, 160, pop(lt, 3.4))


# 27.92 CONSEJO "So here's the move. Before landing, count the rows to your nearest exit."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    # filas vistas desde arriba
    n = 5
    k_on = int(clamp((lt - 1.6) / 1.9) * n + 0.0001)
    for i in range(n):
        y = 1300 - i * 190
        for side in (-1, 1):
            for j in range(3):
                x = W / 2 + side * (120 + j * 120)
                rrect(ctx, x - 50, y - 60, 100, 120, 24)
                fill(ctx, YELLOW if i < k_on else SEAT)
        if i < k_on:
            text(ctx, str(i + 1), W / 2, y, 70, YELLOW)
    rrect(ctx, W / 2 - 110, 1300 - n * 190 - 40, 220, 80, 14)
    fill(ctx, (0.05, 0.05, 0.05))
    text(ctx, "EXIT", W / 2, 1300 - n * 190, 52, EXIT_G, shadow=False)
    badge(ctx, "COUNT THE ROWS", W / 2, 330, pop(lt, 0.4), size=58)


# 32.08 "In smoke, you can't see signs. But you can feel seats."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.2)]), W / 2, 980)
    cabin(ctx, T, light=0.35, path=0.4, smoke=ease(lt / 1.0))
    # mano tocando respaldos
    k = int(lt * 2.2) % 4
    hx = [380, 700, 420, 680][k]
    hy = [1350, 1230, 1120, 1030][k]
    icon(ctx, "✋", hx, hy, 230, 1.0, rot=-0.2)
    pill(ctx, "CAN'T SEE SIGNS", W / 2, 360, pop(lt, 0.4), rgb=(0.7, 0.7, 0.75))
    badge(ctx, "FEEL THE SEATS", W / 2, 500, pop(lt, 2.2), size=56)


# 36.0 CTA "Tell me below if you knew this, and follow for what airlines never explain."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 980)
    bg_night(ctx, T)
    ctx.save()
    ctx.translate(820, keyframes(lt, [(0, 600), (dur, 700)]))
    ctx.rotate(0.5)
    plane_top(ctx, 0, 0, 0.18)
    ctx.restore()
    character(ctx, W / 2, 900, 0.95, T, mood="feliz", wave=1.0)
    icon(ctx, "💬", 230, 600, 200, pop(lt, 0.3), rot=-0.15)
    pill(ctx, "DID YOU KNOW?", W / 2, 400, pop(lt, 0.2))
    badge(ctx, "FOLLOW", W / 2, 1590 - 300, pop(lt, 1.6), size=72)


ESCENAS = [(0.0, e1), (4.76, e2), (9.92, e3), (14.32, e4), (18.6, e5), (23.52, e6), (27.92, e7), (32.08, e8), (36.0, e9)]
PALABRAS_POR_SUBTITULO = 2
SFX = [(0.9, "pop"), (3.0, "pop"), (17.5, "ding"), (26.3, "pop"), (31.4, "ding")]
