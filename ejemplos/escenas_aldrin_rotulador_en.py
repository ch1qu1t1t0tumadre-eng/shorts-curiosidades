"""v11 (EN) FORMATO BUCLE: Buzz Aldrin got off the Moon with a cheap felt-tip pen (Apollo 11, ENG ARM breaker)."""
import math
from anim import *  # noqa

GOLD = (1.0, 0.76, 0.22)
FOIL = (0.93, 0.70, 0.20)
FOIL_D = (0.70, 0.48, 0.10)
SUIT = (0.94, 0.94, 0.96)
SUIT_D = (0.76, 0.77, 0.82)
MOON = (0.62, 0.62, 0.66)
MOON_D = (0.42, 0.42, 0.47)
ALU = (0.78, 0.80, 0.84)
PANEL = (0.36, 0.38, 0.42)
CYAN = (0.35, 0.85, 1.0)
ORANGE = (1.0, 0.55, 0.15)


# ---------------- piezas ----------------
def bg_space(ctx, T, tint=(0.02, 0.03, 0.09), tint2=(0.06, 0.05, 0.16)):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, tint), (1, tint2)]))
    ctx.paint()
    rng = np.random.default_rng(11)
    for _ in range(140):
        x, y, r = rng.uniform(-500, W + 500), rng.uniform(-700, H + 700), rng.uniform(1.2, 3.6)
        circle(ctx, x, y, r)
        fill(ctx, WHITE, 0.35 + 0.35 * math.sin(T * rng.uniform(1, 3) + x))


def moon_ground(ctx, y, T=0.0, extent=3000):
    ctx.move_to(-extent, y + 40)
    for k in range(-30, 31):
        xx = W / 2 + k * 100
        ctx.line_to(xx, y + 25 * math.sin(k * 0.9) + 15 * math.sin(k * 2.3))
    ctx.line_to(extent, y + 40)
    ctx.line_to(extent, y + 2500)
    ctx.line_to(-extent, y + 2500)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, y - 40, 0, y + 700, [(0, MOON), (1, MOON_D)]))
    ctx.fill()
    rng = np.random.default_rng(5)
    for _ in range(18):
        cx, cy, r = rng.uniform(-400, W + 400), y + rng.uniform(60, 650), rng.uniform(20, 70)
        ellipse(ctx, cx, cy, r, r * 0.32)
        fill(ctx, MOON_D, 0.8)
        ellipse(ctx, cx + r * 0.1, cy - r * 0.06, r * 0.8, r * 0.22)
        fill(ctx, (0.33, 0.33, 0.38), 0.7)


def earth(ctx, x, y, r, T=0.0):
    g = cairo.RadialGradient(x, y, r, x, y, r * 1.6)
    g.add_color_stop_rgba(0, 0.4, 0.7, 1, 0.35)
    g.add_color_stop_rgba(1, 0.4, 0.7, 1, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r * 1.6)
    ctx.fill()
    circle(ctx, x, y, r)
    fill(ctx, (0.15, 0.40, 0.85))
    ctx.save()
    circle(ctx, x, y, r)
    ctx.clip()
    for k, (dx, dy, rx, ry) in enumerate(((-0.3, -0.2, 0.35, 0.25), (0.25, 0.15, 0.3, 0.4), (-0.1, 0.5, 0.25, 0.15))):
        ellipse(ctx, x + (dx + 0.05 * math.sin(T * 0.3)) * r, y + dy * r, rx * r, ry * r)
        fill(ctx, (0.25, 0.70, 0.40))
    ellipse(ctx, x + 0.1 * r, y - 0.5 * r, 0.5 * r, 0.1 * r)
    fill(ctx, WHITE, 0.7)
    circle(ctx, x + r * 0.45, y + r * 0.1, r * 1.05)  # sombra (fase)
    fill(ctx, (0, 0, 0.05), 0.0)
    ctx.restore()


def pen(ctx, x, y, s=1.0, rot=0.0, glow=0.0, cap=True):
    """Rotulador de aluminio cepillado (punta hacia la derecha). (x, y) = centro; largo 520*s."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 420)
        g.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.55 * glow)
        g.add_color_stop_rgba(1, 1, 0.9, 0.5, 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, 420)
        ctx.fill()
    L, R = 520, 34
    # cuerpo
    rrect(ctx, -L / 2, -R, L * 0.78, 2 * R, R)
    ctx.set_source(vgrad(ctx, 0, -R, 0, R, [(0, (0.95, 0.96, 0.98)), (0.45, ALU), (1, (0.50, 0.52, 0.58))]))
    ctx.fill()
    for k in range(12):  # cepillado
        ctx.move_to(-L / 2 + 20, -R + 8 + k * 5)
        ctx.line_to(-L / 2 + L * 0.74, -R + 8 + k * 5)
        stroke(ctx, WHITE, 1, 0.15)
    # anillo + capuchón / cono
    ctx.rectangle(L * 0.26, -R - 2, 18, 2 * R + 4)
    fill(ctx, (0.15, 0.15, 0.18))
    ctx.move_to(L * 0.29, -R + 6)
    ctx.line_to(L * 0.45, -10)
    ctx.line_to(L * 0.45, 10)
    ctx.line_to(L * 0.29, R - 6)
    ctx.close_path()
    fill(ctx, (0.55, 0.57, 0.62))
    rrect(ctx, L * 0.44, -9, 40, 18, 8)  # punta de fieltro
    fill(ctx, (0.05, 0.05, 0.08))
    if cap:  # clip
        rrect(ctx, -L / 2 + 40, -R - 16, 170, 14, 6)
        fill(ctx, (0.62, 0.64, 0.70))
    rrect(ctx, -L / 2 + 30, -R + 10, L * 0.6, 10, 5)  # brillo
    fill(ctx, WHITE, 0.55)
    ctx.restore()


def astronaut(ctx, x, y, s=1.0, T=0.0, arm=0.0, pen_glow=0.0, hold_pen=True):
    """Astronauta genérico (sin rasgos: visor dorado). (x, y) = centro del casco. arm 0..1 = brazo derecho arriba."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    bob = 6 * math.sin(T * 1.6)
    ctx.translate(0, bob)
    # mochila
    rrect(ctx, -230, 90, 460, 520, 40)
    fill(ctx, SUIT_D)
    # cuerpo
    rrect(ctx, -200, 140, 400, 560, 120)
    ctx.set_source(vgrad(ctx, 0, 140, 0, 700, [(0, SUIT), (1, SUIT_D)]))
    ctx.fill()
    # panel del pecho
    rrect(ctx, -110, 280, 220, 130, 20)
    fill(ctx, (0.55, 0.58, 0.66))
    for k, c in enumerate((RED, CYAN, GREEN, YELLOW)):
        circle(ctx, -70 + k * 47, 345, 14)
        fill(ctx, c)
    # brazo izquierdo
    rrect(ctx, -300, 190, 120, 380, 60)
    fill(ctx, SUIT)
    circle(ctx, -240, 590, 62)
    fill(ctx, (0.85, 0.86, 0.90))
    # brazo derecho (gira hacia arriba con arm)
    ctx.save()
    ctx.translate(240, 230)
    ctx.rotate(-2.4 * arm)
    rrect(ctx, -60, -20, 120, 380, 60)
    fill(ctx, SUIT)
    circle(ctx, 0, 380, 62)
    fill(ctx, (0.85, 0.86, 0.90))
    if hold_pen:
        pen(ctx, 0, 380, 0.75, math.pi / 2 + 0.3, glow=pen_glow)
    ctx.restore()
    # casco
    circle(ctx, 0, 0, 200)
    fill(ctx, SUIT)
    ellipse(ctx, 0, 10, 150, 125)
    g = cairo.LinearGradient(-150, -120, 150, 130)
    g.add_color_stop_rgb(0, 1.0, 0.88, 0.45)
    g.add_color_stop_rgb(0.5, 0.85, 0.55, 0.12)
    g.add_color_stop_rgb(1, 0.45, 0.25, 0.05)
    ctx.set_source(g)
    ctx.fill()
    ellipse(ctx, -60, -40, 50, 28)  # reflejo
    fill(ctx, WHITE, 0.55)
    ellipse(ctx, 40, 50, 70, 20)
    fill(ctx, (0.25, 0.45, 0.9), 0.35)  # reflejo de la Tierra
    circle(ctx, 0, 0, 200)
    stroke(ctx, (0.7, 0.72, 0.78), 10)
    ctx.restore()


def lunar_module(ctx, x, y, s=1.0, T=0.0, lift=0.0, flame=0.0, only_top=False):
    """Módulo lunar tipo 'Eagle'. (x, y) = pie de las patas (suelo)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if not only_top:
        # patas
        for sx in (-1, 1):
            ctx.move_to(sx * 150, -260)
            ctx.line_to(sx * 330, -20)
            ctx.move_to(sx * 170, -170)
            ctx.line_to(sx * 330, -20)
            stroke(ctx, (0.75, 0.75, 0.78), 14)
            ellipse(ctx, sx * 330, -8, 60, 16)
            fill(ctx, (0.8, 0.8, 0.84))
        # etapa de descenso (dorada)
        ctx.move_to(-220, -380); ctx.line_to(220, -380); ctx.line_to(260, -300); ctx.line_to(220, -170)
        ctx.line_to(-220, -170); ctx.line_to(-260, -300); ctx.close_path()
        ctx.set_source(vgrad(ctx, 0, -380, 0, -170, [(0, (1.0, 0.85, 0.35)), (0.5, FOIL), (1, FOIL_D)]))
        ctx.fill()
        for k in range(6):  # arrugas del papel de oro
            ctx.move_to(-200 + k * 80, -370)
            ctx.line_to(-180 + k * 75, -180)
            stroke(ctx, (0.6, 0.4, 0.05), 3, 0.5)
    ctx.translate(0, -lift)
    if flame > 0:
        for k in range(3):
            ctx.move_to(-50 + k * 8, -380)
            ctx.curve_to(-60, -250, 0, -150 + 30 * math.sin(T * 30 + k), 0, -120 * flame - 140)
            ctx.curve_to(0, -150, 60, -250, 50 - k * 8, -380)
            fill(ctx, (1, 0.6 + 0.15 * k, 0.2 + 0.3 * k), 0.8)
    # etapa de ascenso (gris, angulosa)
    ctx.move_to(-200, -380); ctx.line_to(-230, -520); ctx.line_to(-150, -650); ctx.line_to(120, -660)
    ctx.line_to(220, -560); ctx.line_to(210, -380); ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -660, 0, -380, [(0, (0.86, 0.87, 0.90)), (1, (0.55, 0.56, 0.62))]))
    ctx.fill()
    ctx.move_to(-200, -380); ctx.line_to(-230, -520); ctx.line_to(-150, -650); ctx.line_to(120, -660)
    ctx.line_to(220, -560); ctx.line_to(210, -380); ctx.close_path()
    stroke(ctx, (0.3, 0.3, 0.35), 4)
    # ventanas triangulares
    for sx in (-1, 1):
        ctx.move_to(sx * 30, -560); ctx.line_to(sx * 120, -560); ctx.line_to(sx * 40, -480); ctx.close_path()
        fill(ctx, (0.08, 0.10, 0.20))
    # escotilla, antena
    rrect(ctx, -60, -470, 120, 80, 10)
    fill(ctx, (0.45, 0.46, 0.52))
    ctx.move_to(120, -660); ctx.line_to(170, -760)
    stroke(ctx, (0.8, 0.8, 0.85), 6)
    circle(ctx, 170, -770, 28)
    fill(ctx, (0.85, 0.85, 0.9))
    ctx.restore()


def breaker(ctx, x, y, s=1.0, state="ok", pen_in=0.0, armed=0.0, glow=0.0, label=None):
    """Interruptor de panel (cilindro negro saliente). state: ok / broken. pen_in 0..1 mete el rotulador."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 160)
        g.add_color_stop_rgba(0, *(GREEN if armed > 0.5 else RED), 0.6 * glow)
        g.add_color_stop_rgba(1, *(GREEN if armed > 0.5 else RED), 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, 160)
        ctx.fill()
    circle(ctx, 0, 0, 52)  # collar
    fill(ctx, (0.18, 0.18, 0.22))
    circle(ctx, 0, 0, 40)
    fill(ctx, (0.05, 0.05, 0.07))
    if state == "ok":
        rrect(ctx, -26, -110, 52, 110, 14)
        ctx.set_source(vgrad(ctx, -26, 0, 26, 0, [(0, (0.25, 0.25, 0.3)), (0.5, (0.08, 0.08, 0.1)), (1, (0.02, 0.02, 0.03))]))
        ctx.fill()
        ctx.rectangle(-26, -30, 52, 12)
        fill(ctx, WHITE, 0.85)
    else:
        # muñón roto: borde dentado
        ctx.move_to(-26, 0); ctx.line_to(-26, -30); ctx.line_to(-12, -18); ctx.line_to(0, -36)
        ctx.line_to(12, -16); ctx.line_to(26, -32); ctx.line_to(26, 0); ctx.close_path()
        fill(ctx, (0.10, 0.10, 0.12))
    if pen_in > 0:
        # el rotulador entra desde abajo a la derecha
        d = (1 - ease(pen_in)) * 380
        pen(ctx, 158 + d * 0.7, 158 + d * 0.7, 0.8, -math.pi * 0.75)
    if label:
        rrect(ctx, -90, 70, 180, 50, 8)
        fill(ctx, (0.92, 0.92, 0.88))
        text(ctx, label, 0, 95, 30, (0.1, 0.1, 0.12), shadow=False)
    ctx.restore()


def panel(ctx, x, y, s, T, broken_k=5, pen_in=0.0, armed=0.0, glow=0.0, label=True):
    """Panel de interruptores (3 filas x 6); uno roto (ENG ARM)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -520, -420, 1040, 840, 30)
    ctx.set_source(vgrad(ctx, 0, -420, 0, 420, [(0, (0.46, 0.48, 0.53)), (1, PANEL)]))
    ctx.fill()
    for sx in (-490, 490):
        for sy in (-390, 390):
            circle(ctx, sx, sy, 12)
            fill(ctx, (0.25, 0.26, 0.3))
    names = ["CABIN", "COMM", "RADAR", "LIGHTS", "FUEL", "ENG ARM", "PUMP", "HEAT", "DISPLAY", "GUIDE", "O2", "VENT",
             "BATT", "RCS", "DATA", "LAMP", "TEMP", "AUX"]
    for k in range(18):
        r, c = divmod(k, 6)
        bx, by = -425 + c * 170, -250 + r * 260
        if k == broken_k:
            breaker(ctx, bx, by, 1.0, "broken", pen_in, armed, glow)
            rrect(ctx, bx - 78, by + 66, 156, 44, 8)
            fill(ctx, YELLOW if label else (0.9, 0.9, 0.86))
            text(ctx, names[k], bx, by + 88, 26, (0.1, 0.1, 0.12), shadow=False)
        else:
            breaker(ctx, bx, by, 1.0, "ok")
            rrect(ctx, bx - 70, by + 66, 140, 44, 8)
            fill(ctx, (0.9, 0.9, 0.86))
            text(ctx, names[k], bx, by + 88, 24, (0.1, 0.1, 0.12), shadow=False)
    ctx.restore()


def glove_finger(ctx, x, y, s=1.0, rot=0.0):
    """Mano con guante blanco señalando (dedo hacia arriba-izquierda)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -90, 0, 180, 360, 70)
    fill(ctx, SUIT_D)
    rrect(ctx, -110, -120, 220, 190, 70)
    fill(ctx, SUIT)
    rrect(ctx, -40, -330, 80, 260, 40)
    fill(ctx, SUIT)
    rrect(ctx, -40, -330, 80, 260, 40)
    stroke(ctx, SUIT_D, 5)
    ctx.restore()


def sparks(ctx, x, y, T, a=1.0, n=10):
    if a <= 0.01:
        return
    for k in range(n):
        ang = k / n * math.tau + math.sin(T * 9 + k) * 0.6
        r0, r1 = 50, 110 + 50 * abs(math.sin(T * 13 + k * 2))
        ctx.move_to(x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        ctx.line_to(x + math.cos(ang + 0.15) * (r0 + r1) * 0.6, y + math.sin(ang + 0.15) * (r0 + r1) * 0.6)
        ctx.line_to(x + math.cos(ang) * (r0 + r1), y + math.sin(ang) * (r0 + r1))
        stroke(ctx, (1, 0.95, 0.4), 7, a * 0.9)


def cross(ctx, x, y, r, a=1.0, rgb=RED):
    if a <= 0.01:
        return
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for sgn in (1, -1):
        ctx.move_to(x - r * a, y - sgn * r * a)
        ctx.line_to(x + r * a, y + sgn * r * a)
        stroke(ctx, (0, 0, 0), 46, 0.5)
        ctx.move_to(x - r * a, y - sgn * r * a)
        ctx.line_to(x + r * a, y + sgn * r * a)
        stroke(ctx, rgb, 34)


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): Aldrin en la Luna con el rotulador brillando en alto."""
    camera(ctx, zoom, W / 2, 860)
    bg_space(ctx, T)
    earth(ctx, 190, 300, 95, T)
    moon_ground(ctx, 1150, T)
    lunar_module(ctx, 870, 1210, 0.55, T)
    astronaut(ctx, 430, 560, 0.95, T, arm=1.0, pen_glow=1.0 + 0.2 * math.sin(T * 4))
    ctx.restore()
    ctx.save()
    ficha(ctx, "BUZZ ALDRIN", "APOLLO 11 ASTRONAUT", W / 2, 1480, 1.0, "👨‍🚀", GOLD)


# ---------------- escenas (subtítulo gigante en y≈1060: dejar libre ~950–1170) ----------------
# 0.00 "Buzz Aldrin got off the Moon with a"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 1.97 "cheap felt-tip pen. And it's true."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (1.3, 1.05), (dur, 1.0)]), W / 2, 820)
    bg_space(ctx, T, (0.08, 0.04, 0.12), (0.03, 0.02, 0.06))
    pen(ctx, W / 2, 640, 1.55, -0.25 + 0.04 * math.sin(T * 2), glow=1.0)
    pill(ctx, "FELT-TIP PEN", W / 2, 360, pop(lt, 0.3), size=54, rgb=GOLD)
    badge(ctx, "TRUE STORY", W / 2, 1400, pop(lt, 1.35), size=64, bg=GREEN)


# 4.13 "July 1969."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, keyframes(lt, [(0, 900), (dur, 820)]))
    bg_space(ctx, T)
    earth(ctx, 820, 1420, 230, T)
    # cohete subiendo
    y = lerp(1300, 450, ease_out(lt / dur))
    icon(ctx, "🚀", 170, y, 220, 1.0, rot=0.0)
    pill(ctx, counter(lt, 1900, 1969, 0.8), W / 2, 380, pop(lt, 0.0), size=90, rgb=GOLD)
    pill(ctx, "JULY · APOLLO 11", W / 2, 560, pop(lt, 0.5), size=40, rgb=CYAN)


# 5.59 "Aldrin and Neil Armstrong are inside the"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 880)
    bg_space(ctx, T, (0.03, 0.04, 0.12), (0.08, 0.06, 0.20))
    moon_ground(ctx, 1250, T)
    astronaut(ctx, 300, 620, 0.62, T, arm=0.0, hold_pen=False)
    astronaut(ctx, 780, 640, 0.62, T + 1.3, arm=0.35, hold_pen=False)
    ficha(ctx, "BUZZ ALDRIN", "LUNAR MODULE PILOT", W / 2, 260, pop(lt, 0.0), "👨‍🚀", GOLD, w=820)
    ficha(ctx, "NEIL ARMSTRONG", "MISSION COMMANDER · 1930–2012", W / 2, 1450, pop(lt, 0.55), "🚀", CYAN, w=900)


# 7.68 "Eagle, sitting on the Moon."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.08)]), keyframes(lt, [(0, 480), (dur, 560)]), 900)
    bg_space(ctx, T)
    earth(ctx, 830, 320, 80, T)
    moon_ground(ctx, 1150, T)
    lunar_module(ctx, W / 2, 1210, 1.05, T)
    pill(ctx, "THE EAGLE", W / 2, 1420, pop(lt, 0.0), size=60, rgb=GOLD)


# 9.17 "Then Aldrin spots something on the floor."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, keyframes(lt, [(0, 820), (dur, 960)]))
    ctx.set_source(vgrad(ctx, 0, -300, 0, H + 300, [(0, (0.14, 0.15, 0.20)), (1, (0.06, 0.06, 0.09))]))
    ctx.paint()
    # cabina: ventana triangular con estrellas y suelo con panel
    ctx.move_to(120, 220); ctx.line_to(520, 220); ctx.line_to(170, 640); ctx.close_path()
    fill(ctx, (0.02, 0.03, 0.08))
    ctx.move_to(120, 220); ctx.line_to(520, 220); ctx.line_to(170, 640); ctx.close_path()
    stroke(ctx, (0.45, 0.46, 0.52), 14)
    ctx.rectangle(-500, 1260, W + 1000, 900)
    fill(ctx, (0.22, 0.23, 0.27))
    character(ctx, 760, 620, 0.75, T, mood="duda", helmet=True, look=(0, 1), body=True)
    # algo pequeño en el suelo, con brillo
    pulse = 0.6 + 0.4 * math.sin(T * 6)
    g = cairo.RadialGradient(420, 1380, 0, 420, 1380, 120)
    g.add_color_stop_rgba(0, 1, 0.3, 0.2, 0.6 * pulse)
    g.add_color_stop_rgba(1, 1, 0.3, 0.2, 0)
    ctx.set_source(g)
    circle(ctx, 420, 1380, 120)
    ctx.fill()
    rrect(ctx, 400, 1360, 46, 34, 8)
    fill(ctx, (0.05, 0.05, 0.07))
    badge(ctx, "?", 420, 1250, pop(lt, 0.9), size=70, bg=RED)


# 11.10 "A tiny circuit breaker, snapped off."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.98), (dur, 1.06)]), W / 2, 880)
    bg_dark(ctx, T)
    panel(ctx, W / 2, 700, 0.82, T, label=False)
    # el trozo roto cae
    p = clamp((lt - 1.2) / 0.8)
    ctx.save()
    ctx.translate(W / 2 + 0.82 * 425 + 60 * p, 700 - 0.82 * 250 - 60 + 700 * p * p)
    ctx.rotate(p * 4)
    rrect(ctx, -26, -80, 52, 80, 12)
    fill(ctx, (0.08, 0.08, 0.1))
    ctx.restore()
    thumb_circle(ctx, W / 2 + 0.82 * 425, 700 - 0.82 * 250, 105, 105)
    badge(ctx, "SNAPPED OFF", W / 2, 1400, pop(lt, 1.6), size=60)


# 13.27 "The switch that arms the engine to leave the Moon."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.35), (dur, 1.15)]), keyframes(lt, [(0, 760), (dur, 620)]),
           keyframes(lt, [(0, 600), (dur, 760)]))
    bg_dark(ctx, T)
    panel(ctx, W / 2, 700, 0.95, T, label=True, glow=0.6 + 0.4 * math.sin(T * 5))
    ctx.restore()
    ctx.save()
    pill(ctx, "ENGINE ARM", W / 2, 1360, pop(lt, 0.4), size=56, rgb=ORANGE, sub="LIFTOFF SWITCH")


# 15.59 "No switch, no engine. No engine, no ride home."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 0.88)]), W / 2, 820)
    bg_space(ctx, T)
    earth(ctx, 780, 330, 120 - 20 * clamp(lt / dur), T)
    moon_ground(ctx, 1200, T)
    lunar_module(ctx, 360, 1260, 0.7, T)
    arrow(ctx, 430, 640, 700, 420, ease((lt - 0.2) / 0.8), WHITE, 8, dashed=True)
    pill(ctx, "NO ENGINE", 330, 1400, pop(lt, 0.7), size=44, rgb=RED)
    cross(ctx, 600, 520, 110, pop(lt, 1.3))
    pill(ctx, "NO RIDE HOME", 760, 1520, pop(lt, 1.9), size=44, rgb=RED)


# 18.36 "In other words, a broken button could strand two men on the Moon."  (2.º gancho: golpe de zoom)
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.6), (0.3, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 860)
    bg_space(ctx, T, (0.10, 0.02, 0.06), (0.03, 0.02, 0.08))
    for k in range(16):
        ctx.save(); ctx.translate(W / 2, 640); ctx.rotate(k * math.pi / 8 + T * 0.2)
        ctx.move_to(0, 0); ctx.line_to(1400, -90); ctx.line_to(1400, 90); ctx.close_path()
        fill(ctx, RED, 0.06); ctx.restore()
    breaker(ctx, W / 2, 560, 2.6, "broken", glow=1.0)
    character(ctx, 230, 1440, 0.55, T, mood="sorpresa", helmet=True, body=True)
    badge(ctx, "STRANDED?", 740, 1400, pop(lt, 1.6), size=60)
    pill(ctx, "2 MEN", 760, 260, pop(lt, 2.3), size=50, rgb=GOLD)


# 21.79 "Aldrin won't touch it with his finger."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, keyframes(lt, [(0, 760), (dur, 680)]))
    bg_dark(ctx, T)
    rrect(ctx, 140, 260, 800, 600, 30)
    fill(ctx, PANEL)
    breaker(ctx, W / 2, 520, 1.8, "broken", glow=0.5)
    # el dedo se acerca y se echa atrás
    a = keyframes(lt, [(0, 0.0), (0.7, 1.0), (1.1, 1.0), (1.5, 0.3), (dur, 0.3)])
    glove_finger(ctx, W / 2 + 120 + 300 * (1 - a), 760 + 300 * (1 - a), 1.0, -0.6)
    cross(ctx, 820, 380, 70, pop(lt, 1.15))


# 23.41 "It's live, and he doesn't want to get shocked."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.05)]) + 0.006 * math.sin(T * 50), W / 2, 760)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.08, 0.06, 0.02)), (1, (0.02, 0.02, 0.05))]))
    ctx.paint()
    rrect(ctx, 140, 260, 800, 600, 30)
    fill(ctx, PANEL)
    breaker(ctx, W / 2, 520, 1.8, "broken", glow=1.0)
    sparks(ctx, W / 2, 470, T, 0.6 + 0.4 * math.sin(T * 17))
    icon(ctx, "⚡", 230, 330, 180, pop(lt, 0.1))
    icon(ctx, "⚡", 850, 760, 150, pop(lt, 0.3))
    badge(ctx, "LIVE", W / 2, 1360, pop(lt, 0.15), size=80, bg=(0.9, 0.6, 0.0))


# 25.57 "So Buzz Aldrin grabs a felt-tip pen from his pocket"
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 860)
    bg_space(ctx, T, (0.05, 0.04, 0.12), (0.12, 0.08, 0.20))
    # bolsillo del traje
    rrect(ctx, 200, 540, 680, 620, 60)
    fill(ctx, SUIT)
    rrect(ctx, 300, 760, 480, 360, 40)
    fill_keep(ctx, SUIT_D)
    stroke(ctx, (0.6, 0.6, 0.66), 6)
    up = ease((lt - 0.3) / 1.2)
    ctx.save()
    rrect(ctx, -500, -800, 2100, 1560 + up * 0, 0)  # todo visible
    ctx.clip()
    pen(ctx, W / 2, 900 - 560 * up, 1.2, -math.pi / 2 + 0.25 * up, glow=up)
    ctx.restore()
    rrect(ctx, 300, 900, 480, 220, 30)  # tapa del bolsillo delante
    fill(ctx, SUIT_D)
    ficha(ctx, "BUZZ ALDRIN", "APOLLO 11 ASTRONAUT", W / 2, 1450, pop(lt, 0.0), "👨‍🚀", GOLD)


# 28.30 "and jams it in. Click. The engine is armed."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (1.1, 1.25), (1.2, 1.12), (dur, 1.0)]), W / 2, 700)
    bg_dark(ctx, T)
    rrect(ctx, 140, 200, 800, 700, 30)
    fill(ctx, PANEL)
    armed = 1.0 if lt > 1.1 else 0.0
    breaker(ctx, W / 2, 460, 1.6, "broken", pen_in=clamp(lt / 1.0), armed=armed, glow=armed * 1.0 + 0.2)
    badge(ctx, "CLICK!", 300, 300, pop(lt, 1.1), size=60, bg=YELLOW, fg=(0.1, 0.1, 0.1))
    pill(ctx, "ENGINE ARMED", W / 2, 1380, pop(lt, 1.5), size=58, rgb=GREEN)


# 30.54 "Aldrin kept that pen for decades."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.08)]), W / 2, 820)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.10, 0.07, 0.04)), (1, (0.04, 0.03, 0.02))]))
    ctx.paint()
    # caja-expositor con el rotulador y el interruptor
    rrect(ctx, 150, 380, 780, 560, 30)
    fill_keep(ctx, (0.35, 0.10, 0.12))
    stroke(ctx, GOLD, 8)
    rrect(ctx, 190, 420, 700, 480, 20)
    fill(ctx, (0.55, 0.15, 0.18))
    pen(ctx, W / 2, 560, 1.15, -0.05, glow=0.5)
    breaker(ctx, W / 2 + 200, 800, 0.8, "ok")
    breaker(ctx, W / 2 - 200, 800, 0.8, "broken")
    pill(ctx, counter(lt, 1969, 2026, 1.4), W / 2, 1400, pop(lt, 0.0), size=80, rgb=GOLD)


# 32.45 "This July, it sold at Sotheby's for"
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 820)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.12, 0.05, 0.08)), (1, (0.04, 0.02, 0.05))]))
    ctx.paint()
    for k in range(-3, 4):  # cortinas
        ctx.rectangle(W / 2 + k * 160 - 60, -400, 120, 2600)
        fill(ctx, (0.45, 0.08, 0.12), 0.25)
    rrect(ctx, 260, 760, 560, 380, 20)  # atril
    fill(ctx, (0.35, 0.22, 0.12))
    pen(ctx, W / 2, 680, 0.9, 0.0, glow=0.6)
    hit = keyframes(lt, [(0, -0.9), (0.9, -0.9), (1.1, 0.25), (1.4, -0.2), (dur, -0.2)])
    icon(ctx, "🔨", 790, 470, 260, 1.0, rot=hit)
    pill(ctx, "SOTHEBY'S · NEW YORK", W / 2, 280, pop(lt, 0.9), size=46, rgb=GOLD)
    pill(ctx, "JULY 2026", W / 2, 1400, pop(lt, 0.1), size=56, rgb=CYAN)


# 34.33 "857,600 dollars."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.0), (dur, 1.1)]), W / 2, 820)
    bg_space(ctx, T, (0.02, 0.10, 0.06), (0.01, 0.04, 0.03))
    for k in range(14):  # billetes cayendo
        x = (k * 173) % 1180 - 50
        y = ((lt * 420 + k * 260) % 2300) - 400
        ctx.save(); ctx.translate(x, y); ctx.rotate(math.sin(T * 2 + k))
        rrect(ctx, -70, -35, 140, 70, 8); fill(ctx, (0.45, 0.75, 0.45))
        circle(ctx, 0, 0, 18); fill(ctx, (0.3, 0.55, 0.3))
        ctx.restore()
    pen(ctx, W / 2, 620, 1.2, -0.2, glow=1.2)
    pill(ctx, counter(lt, 0, 857600, 1.6, "${:,.0f}"), W / 2, 330, pop(lt, 0.0), size=96, rgb=GREEN)
    badge(ctx, "FOR A MARKER", W / 2, 1400, pop(lt, 1.7), size=58, bg=PURPLE)


# 37.01 "All because, in 1969" -> vuelve a e1 (mismo plano, termina donde e1 empieza)
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (1.97, e2), (4.13, e3), (5.59, e4), (7.68, e5), (9.17, e6), (11.10, e7), (13.27, e8),
           (15.59, e9), (18.36, e10), (21.79, e11), (23.41, e12), (25.57, e13), (28.30, e14), (30.54, e15),
           (32.45, e16), (34.33, e17), (37.01, e18)]
SFX = [(12.95, "pop"), (18.40, "ding"), (29.41, "pop"), (34.40, "ding")]


# ---------------- miniatura (no desvela que el rotulador arregló el interruptor) ----------------
def MINIATURA(ctx):
    T = 1.3
    ctx.save()
    camera(ctx, 1.0, W / 2, 960)
    bg_space(ctx, T)
    earth(ctx, 200, 520, 90, T)
    moon_ground(ctx, 1350, T)
    lunar_module(ctx, 820, 1420, 0.55, T)
    astronaut(ctx, 360, 820, 0.95, T, arm=1.0, pen_glow=1.4)
    ctx.restore()
    thumb_vignette(ctx, 0.55)
    thumb_circle(ctx, 880, 740, 175, 150)
    thumb_arrow(ctx, 640, 1250, 800, 920)
    thumb_text(ctx, ["A PEN", ("ON THE MOON?", WHITE)], y=230, size=170)
    ficha(ctx, "BUZZ ALDRIN", "APOLLO 11 ASTRONAUT", W / 2, 1640, 1.0, "👨‍🚀", GOLD)
