"""v13 (EN) FORMATO BUCLE: Fredric Baur, who designed the Pringles can, is buried inside one (FOOD)."""
import math
from anim import *  # noqa

CAN_R = (0.86, 0.10, 0.12)
CAN_RD = (0.50, 0.04, 0.07)
CAN_RL = (1.0, 0.42, 0.40)
CHIP = (1.0, 0.80, 0.35)
CHIP_D = (0.85, 0.55, 0.15)
SILVER = (0.82, 0.84, 0.88)
GRASS = (0.20, 0.46, 0.28)
GRASS_D = (0.10, 0.28, 0.17)
SOIL = (0.36, 0.22, 0.13)
SOIL_D = (0.20, 0.12, 0.07)
STONE = (0.62, 0.64, 0.68)
STONE_D = (0.42, 0.44, 0.50)
TEAL = (0.25, 0.85, 0.80)
ORANGE = (1.0, 0.58, 0.18)
ASH = (0.62, 0.60, 0.58)
GOLD = (1.0, 0.78, 0.30)

FICHA_SUB = "P&G CHEMIST · 1918–2008"


# ---------------- piezas ----------------
def bg_dusk(ctx, T, top=(0.10, 0.06, 0.20), mid=(0.42, 0.16, 0.30), bot=(0.95, 0.48, 0.30), stars=True):
    ctx.set_source(vgrad(ctx, 0, -700, 0, H + 300, [(0, top), (0.55, mid), (1, bot)]))
    ctx.paint()
    if stars:
        rng = np.random.default_rng(13)
        for _ in range(70):
            x, y, r = rng.uniform(-500, W + 500), rng.uniform(-700, H * 0.45), rng.uniform(1.5, 3.5)
            circle(ctx, x, y, r)
            fill(ctx, WHITE, 0.2 + 0.3 * (0.5 + 0.5 * math.sin(T * rng.uniform(1, 3) + x)))


def bg_kitchen(ctx, T, c1=(0.98, 0.93, 0.80), c2=(0.95, 0.78, 0.55)):
    """Fondo crema con baldosas (lab / tienda)."""
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, c1), (1, c2)]))
    ctx.paint()
    bg_grid(ctx, 120, 0.10, (0.55, 0.35, 0.20))


def spot(ctx, x, y, r, a=0.5, col=(1, 0.9, 0.6)):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a)
    g.add_color_stop_rgba(1, *col, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


def hill(ctx, y, T=0.0, col=GRASS, col2=GRASS_D, extent=3000, amp=30):
    ctx.move_to(-extent, y + 60)
    for k in range(-30, 31):
        xx = W / 2 + k * 100
        ctx.line_to(xx, y + amp * math.sin(k * 0.5) + 10 * math.sin(k * 1.7))
    ctx.line_to(extent, y + 60)
    ctx.line_to(extent, y + 3000)
    ctx.line_to(-extent, y + 3000)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, y - 40, 0, y + 900, [(0, col), (1, col2)]))
    ctx.fill()
    # briznas
    for k in range(-20, 21):
        xx = W / 2 + k * 55 + 10 * math.sin(k)
        yy = y + amp * math.sin((xx - W / 2) / 100 * 0.5) + 8
        ctx.move_to(xx, yy + 10)
        ctx.line_to(xx + 6 * math.sin(T * 2 + k), yy - 22)
        stroke(ctx, (0.35, 0.65, 0.38), 5, 0.8)


def soil(ctx, y, extent=3000):
    """Corte del terreno: hierba arriba y capas de tierra."""
    ctx.rectangle(-extent, y, W + 2 * extent, 3000)
    ctx.set_source(vgrad(ctx, 0, y, 0, y + 1400, [(0, SOIL), (1, SOIL_D)]))
    ctx.fill()
    ctx.rectangle(-extent, y - 40, W + 2 * extent, 60)
    fill(ctx, GRASS)
    rng = np.random.default_rng(4)
    for _ in range(60):
        px, py, r = rng.uniform(-600, W + 600), y + rng.uniform(60, 1600), rng.uniform(6, 22)
        ellipse(ctx, px, py, r, r * 0.6)
        fill(ctx, (0.48, 0.34, 0.24), 0.7)
    for k in range(4):
        ctx.move_to(-extent, y + 280 + k * 300)
        for j in range(-30, 31):
            ctx.line_to(W / 2 + j * 100, y + 280 + k * 300 + 18 * math.sin(j * 0.8 + k))
        stroke(ctx, (0.15, 0.09, 0.05), 4, 0.5)


def chip_side(ctx, x, y, s=1.0, rot=0.0):
    """Patata en forma de silla de montar vista de lado (arco grueso)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.move_to(-95, -6)
    ctx.curve_to(-45, 22, 45, 22, 95, -6)
    ctx.curve_to(45, 2, -45, 2, -95, -6)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -10, 0, 22, [(0, CHIP), (1, CHIP_D)]))
    ctx.fill_preserve()
    ctx.set_line_width(3)
    ctx.set_source_rgba(0.6, 0.35, 0.05, 0.8)
    ctx.stroke()
    ctx.restore()


def chip_top(ctx, x, y, s=1.0, rot=0.0):
    """Patata vista de frente: óvalo con ondulación de silla."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ellipse(ctx, 0, 0, 80, 56)
    ctx.set_source(vgrad(ctx, 0, -56, 0, 56, [(0, (1.0, 0.88, 0.50)), (1, CHIP_D)]))
    ctx.fill()
    ctx.move_to(-70, -10)
    ctx.curve_to(-30, 20, 30, -30, 70, 0)
    stroke(ctx, (1, 0.95, 0.7), 6, 0.7)
    for (dx, dy) in ((-30, 20), (25, 15), (5, -25), (40, -20)):
        circle(ctx, dx, dy, 4)
        fill(ctx, (0.75, 0.45, 0.10), 0.6)
    ctx.restore()


def can(ctx, x, y, s=1.0, rot=0.0, glow=0.0, lid=1.0, open_=0.0, ghost=0.0, label="CHIPS", col=CAN_R, cold=CAN_RD):
    """Bote cilíndrico genérico (sin marca). (x, y) = centro; alto 640*s, ancho 240*s.
    open_ 0..1 levanta la tapa; ghost>0 muestra el interior (corte) con patatas apiladas."""
    w, h = 240, 640
    ry = 34
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    if glow > 0:
        spot(ctx, 0, 0, 560, 0.55 * glow, (1, 0.85, 0.45))
    soft_shadow(ctx, 0, h / 2 + 10, w * 0.75, 30, 0.35)
    # cuerpo
    ctx.new_path()
    ctx.move_to(-w / 2, -h / 2)
    ctx.line_to(-w / 2, h / 2)
    ctx.save(); ctx.translate(0, h / 2); ctx.scale(1, ry / (w / 2)); ctx.arc_negative(0, 0, w / 2, math.pi, 0); ctx.restore()
    ctx.line_to(w / 2, -h / 2)
    ctx.close_path()
    g = cairo.LinearGradient(-w / 2, 0, w / 2, 0)
    g.add_color_stop_rgb(0, *cold)
    g.add_color_stop_rgb(0.28, *col)
    g.add_color_stop_rgb(0.40, *tuple(min(1, c + 0.25) for c in col))
    g.add_color_stop_rgb(0.62, *col)
    g.add_color_stop_rgb(1, *cold)
    ctx.set_source(g)
    ctx.fill()
    if ghost > 0:
        # interior: pila de patatas
        ctx.save()
        rrect(ctx, -w / 2 + 16, -h / 2 + 30, w - 32, h - 50, 20)
        fill(ctx, (0.15, 0.05, 0.05), 0.8 * ghost)
        for k in range(17):
            chip_side(ctx, 0, h / 2 - 40 - k * 32, 1.05, 0)
        ctx.restore()
    else:
        # etiqueta: banda clara con patata + texto genérico
        ctx.rectangle(-w / 2, -90, w, 180)
        g2 = cairo.LinearGradient(-w / 2, 0, w / 2, 0)
        g2.add_color_stop_rgb(0, 0.80, 0.70, 0.50)
        g2.add_color_stop_rgb(0.4, 1.0, 0.96, 0.86)
        g2.add_color_stop_rgb(1, 0.78, 0.68, 0.48)
        ctx.set_source(g2)
        ctx.fill()
        chip_top(ctx, 0, -30, 0.75, -0.15)
        if label:
            text(ctx, label, 0, 52, 40, CAN_RD, shadow=False)
        for yy in (-150, 150):
            ctx.rectangle(-w / 2, yy - 6, w, 12)
            fill(ctx, (1, 0.95, 0.8), 0.85)
    # aro inferior
    ellipse(ctx, 0, h / 2, w / 2, ry)
    stroke(ctx, (0.6, 0.62, 0.66), 8)
    # boca + tapa
    ellipse(ctx, 0, -h / 2, w / 2, ry)
    fill(ctx, (0.25, 0.08, 0.06))
    ellipse(ctx, 0, -h / 2 + 4, w / 2 - 16, ry - 6)
    fill(ctx, CHIP)
    if lid > 0:
        oy = -h / 2 - 160 * ease(open_)
        ctx.save()
        ctx.translate(0, oy)
        ctx.rotate(-0.5 * ease(open_))
        ellipse(ctx, 0, 6, w / 2 + 8, ry + 6)
        fill(ctx, (0.9, 0.92, 0.95), 0.85 * lid)
        ellipse(ctx, 0, 0, w / 2 + 8, ry + 6)
        ctx.set_source(vgrad(ctx, 0, -ry, 0, ry, [(0, (1, 1, 1)), (1, SILVER)]))
        ctx.fill()
        ellipse(ctx, 0, 0, w / 2 - 14, ry - 8)
        stroke(ctx, (0.7, 0.72, 0.78), 4)
        ctx.restore()
    # brillo vertical
    rrect(ctx, -w / 2 + 34, -h / 2 + 30, 18, h - 70, 9)
    fill(ctx, WHITE, 0.30)
    ctx.restore()


def headstone(ctx, x, y, s=1.0, txt="1918 – 2008"):
    """Lápida genérica. (x, y) = base."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-170, 0)
    ctx.line_to(-170, -300)
    ctx.arc(0, -300, 170, math.pi, 0)
    ctx.line_to(170, 0)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, -170, 0, 170, 0, [(0, STONE), (1, STONE_D)]))
    ctx.fill()
    rrect(ctx, -60, -380, 120, 22, 8)
    fill(ctx, STONE_D)
    rrect(ctx, -11, -430, 22, 120, 8)
    fill(ctx, STONE_D)
    if txt:
        text(ctx, txt, 0, -230, 40, (0.25, 0.26, 0.30), shadow=False)
    rrect(ctx, -200, -20, 400, 40, 10)
    fill(ctx, STONE_D)
    ctx.restore()


def urn(ctx, x, y, s=1.0, col=(0.30, 0.38, 0.55)):
    """Urna funeraria genérica. (x, y) = centro."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-60, -170)
    ctx.curve_to(-170, -120, -170, 110, -80, 160)
    ctx.line_to(80, 160)
    ctx.curve_to(170, 110, 170, -120, 60, -170)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, -160, 0, 160, 0, [(0, tuple(c * 0.6 for c in col)), (0.4, tuple(min(1, c + 0.25) for c in col)),
                                                (1, tuple(c * 0.5 for c in col))]))
    ctx.fill()
    rrect(ctx, -110, 150, 220, 40, 10)
    fill(ctx, GOLD)
    rrect(ctx, -75, -200, 150, 40, 12)
    fill(ctx, GOLD)
    circle(ctx, 0, -225, 22)
    fill(ctx, GOLD)
    ctx.rectangle(-150, -20, 300, 16)
    fill(ctx, GOLD, 0.8)
    ctx.restore()


def person(ctx, x, y, s=1.0, col=(0.12, 0.10, 0.18), hat=False):
    """Silueta genérica sin rasgos. (x, y) = centro de la cabeza."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -140, 120, 280, 480, 110)
    fill(ctx, col)
    circle(ctx, 0, 0, 95)
    fill(ctx, col)
    if hat:
        rrect(ctx, -140, -70, 280, 26, 13)
        fill(ctx, col)
        rrect(ctx, -85, -170, 170, 115, 26)
        fill(ctx, col)
    ctx.restore()


def bubble(ctx, x, y, w, h, tail_x, tail_y, a=1.0, col=WHITE):
    if a <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(a, a)
    rrect(ctx, -w / 2, -h / 2, w, h, 40)
    fill(ctx, col)
    ctx.move_to(-30, h / 2 - 2)
    ctx.line_to(tail_x - x, tail_y - y)
    ctx.line_to(30, h / 2 - 2)
    ctx.close_path()
    fill(ctx, col)
    ctx.restore()


def car(ctx, x, y, s=1.0, T=0.0, col=(0.22, 0.24, 0.32)):
    """Coche genérico de perfil hacia la derecha. (x, y) = suelo bajo el centro."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    bob = 3 * math.sin(T * 18)
    ctx.translate(0, bob)
    rrect(ctx, -300, -150, 600, 110, 40)
    fill(ctx, col)
    ctx.move_to(-190, -150); ctx.line_to(-120, -250); ctx.line_to(110, -250); ctx.line_to(190, -150); ctx.close_path()
    fill(ctx, col)
    ctx.move_to(-165, -155); ctx.line_to(-110, -232); ctx.line_to(-10, -232); ctx.line_to(-10, -155); ctx.close_path()
    fill(ctx, (0.55, 0.75, 0.95), 0.8)
    ctx.move_to(10, -155); ctx.line_to(10, -232); ctx.line_to(100, -232); ctx.line_to(165, -155); ctx.close_path()
    fill(ctx, (0.55, 0.75, 0.95), 0.8)
    # faro
    ctx.move_to(295, -110); ctx.line_to(900, -230); ctx.line_to(900, 20); ctx.close_path()
    fill(ctx, (1, 0.95, 0.6), 0.18)
    ellipse(ctx, 290, -110, 16, 20)
    fill(ctx, (1, 0.95, 0.6))
    ctx.restore()
    for wx in (-180, 180):
        ctx.save(); ctx.translate(x + wx * s, y - 30 * s + bob * s); ctx.rotate(T * 8)
        circle(ctx, 0, 0, 62 * s); fill(ctx, (0.06, 0.06, 0.08))
        circle(ctx, 0, 0, 28 * s); fill(ctx, SILVER)
        ctx.rectangle(-4 * s, -28 * s, 8 * s, 56 * s); fill(ctx, (0.3, 0.3, 0.35))
        ctx.restore()


def store(ctx, x, y, s=1.0, T=0.0, lit=1.0):
    """Farmacia genérica (sin marca real). (x, y) = base centrada."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-480, -620, 960, 620)
    fill(ctx, (0.88, 0.86, 0.82))
    ctx.rectangle(-500, -760, 1000, 160)
    fill(ctx, (0.80, 0.12, 0.14))
    text(ctx, "PHARMACY", 40, -680, 96, WHITE, shadow=False)
    rrect(ctx, -440, -740, 120, 120, 14)
    fill(ctx, WHITE)
    ctx.rectangle(-395, -725, 30, 90); fill(ctx, (0.80, 0.12, 0.14))
    ctx.rectangle(-425, -695, 90, 30); fill(ctx, (0.80, 0.12, 0.14))
    for wx in (-300, 300):
        rrect(ctx, wx - 150, -520, 300, 330, 10)
        fill(ctx, (1, 0.93, 0.70), 0.6 + 0.4 * lit)
        for k in range(3):
            ctx.rectangle(wx - 140, -430 + k * 100, 280, 8)
            fill(ctx, (0.6, 0.5, 0.4), 0.6)
            for j in range(5):
                rrect(ctx, wx - 125 + j * 55, -480 + k * 100, 36, 50, 6)
                fill(ctx, (CAN_R, TEAL, ORANGE, BLUE, GREEN)[(j + k) % 5], 0.85)
    rrect(ctx, -110, -460, 220, 460, 10)
    fill(ctx, (0.55, 0.75, 0.85), 0.8)
    ctx.rectangle(-4, -460, 8, 460)
    fill(ctx, (0.3, 0.3, 0.35))
    ctx.restore()
    spot(ctx, x, y - 400 * s, 700 * s, 0.25 * lit, (1, 0.95, 0.7))


def ash_pour(ctx, x0, y0, x1, y1, T, a=1.0, n=60):
    if a <= 0.01:
        return
    rng = np.random.default_rng(8)
    for k in range(n):
        ph = (T * 0.9 + rng.uniform(0, 1)) % 1.0
        xx = lerp(x0, x1, ph) + rng.uniform(-20, 20) * ph
        yy = lerp(y0, y1, ph) + 40 * math.sin(ph * math.pi) * 0
        circle(ctx, xx, yy, rng.uniform(4, 9))
        fill(ctx, ASH, a * (0.9 - 0.4 * ph))


def rays(ctx, x, y, T, col=RED, a=0.07, n=16):
    for k in range(n):
        ctx.save(); ctx.translate(x, y); ctx.rotate(k * math.tau / n + T * 0.2)
        ctx.move_to(0, 0); ctx.line_to(1500, -100); ctx.line_to(1500, 100); ctx.close_path()
        fill(ctx, col, a); ctx.restore()


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): el bote brillando sobre una tumba al atardecer."""
    camera(ctx, zoom, W / 2, 900)
    bg_dusk(ctx, T)
    spot(ctx, W / 2, 1080, 800, 0.35, (1, 0.6, 0.3))
    headstone(ctx, 230, 1010, 0.62)
    headstone(ctx, 900, 990, 0.5, None)
    hill(ctx, 980, T)
    can(ctx, W / 2, 640 + 8 * math.sin(T * 1.5), 0.95, -0.06, glow=1.0 + 0.15 * math.sin(T * 3))
    ctx.restore()
    ctx.save()
    ficha(ctx, "FREDRIC BAUR", FICHA_SUB, W / 2, 1450, 1.0, "🧪", CAN_RL)


# ---------------- escenas (subtítulo gigante en y≈1060: dejar libre ~950–1170) ----------------
# 0.00 "Fredric Baur, the man who designed the"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.1)]))


# 2.10 "Pringles can, is buried inside one."
def e2(ctx, lt, dur, T):
    down = keyframes(lt, [(0, 0.0), (1.2, 0.0), (2.0, 1.0), (dur, 1.0)])
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, lerp(620, 900, down))
    bg_dusk(ctx, T, (0.08, 0.05, 0.16), (0.30, 0.12, 0.25), (0.6, 0.3, 0.25))
    soil(ctx, 700)
    headstone(ctx, W / 2, 700, 0.75)
    can(ctx, W / 2, 1300, 0.62, 0.0, glow=0.5 + 0.5 * down)
    ctx.restore()
    ctx.save()
    pill(ctx, "PRINGLES CAN", W / 2, 270, pop(lt, 0.1), size=56, rgb=CAN_RL)
    badge(ctx, "BURIED INSIDE", W / 2, 420, pop(lt, 1.35), size=60, bg=CAN_R)


# 4.66 "And it's real."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (0.25, 1.0), (dur, 1.06)]), W / 2, 860)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.04, 0.20, 0.22)), (1, (0.02, 0.08, 0.12))]))
    ctx.paint()
    rays(ctx, W / 2, 600, T, TEAL, 0.07)
    character(ctx, W / 2, 540, 1.0, T, mood="sorpresa", body=True)
    ctx.restore()
    ctx.save()
    badge(ctx, "100% REAL", W / 2, 1400, pop(lt, 0.25), size=76, bg=GREEN, fg=(0.05, 0.15, 0.08))


# 5.48 "Baur was a chemist at Procter and Gamble in Cincinnati."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), keyframes(lt, [(0, 540), (dur, 600)]), 820)
    bg_kitchen(ctx, T, (0.86, 0.94, 0.98), (0.62, 0.78, 0.90))
    # mesa de laboratorio
    ctx.rectangle(-600, 880, W + 1200, 60)
    fill(ctx, (0.25, 0.30, 0.40))
    ctx.rectangle(-600, 940, W + 1200, 900)
    fill(ctx, (0.40, 0.46, 0.58))
    person(ctx, 280, 520, 0.85, (0.20, 0.24, 0.34))
    rrect(ctx, 280 - 130, 620, 260, 330, 60)  # bata
    fill(ctx, WHITE, 0.92)
    icon(ctx, "🧪", 640, 760, 230, 1.0, rot=0.1 * math.sin(T * 2))
    icon(ctx, "⚗️", 860, 760, 230, 1.0)
    chip_top(ctx, 760, 520, 0.9, 0.2 * math.sin(T))
    ctx.restore()
    ctx.save()
    ficha(ctx, "FREDRIC BAUR", "ORGANIC CHEMIST", W / 2, 300, pop(lt, 0.0), "🧪", CAN_RL, w=820)
    pill(ctx, "PROCTER & GAMBLE", W / 2, 1360, pop(lt, 1.2), size=50, rgb=BLUE)
    pill(ctx, "CINCINNATI, OHIO", W / 2, 1500, pop(lt, 2.2), size=42, rgb=ORANGE)


# 8.40 "In 1966, he figured out how to"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 0.95)]), W / 2, keyframes(lt, [(0, 760), (dur, 820)]))
    bg_blueprint(ctx, T)
    # plano técnico del bote
    p = ease(clamp(lt / 1.6))
    ctx.save()
    ctx.translate(W / 2, 640)
    w, h = 240 * 1.2, 640 * 1.0
    ctx.rectangle(-w / 2, -h / 2, w, h * p)
    stroke(ctx, WHITE, 5)
    ellipse(ctx, 0, -h / 2, w / 2, 40)
    stroke(ctx, WHITE, 5)
    if p > 0.95:
        ellipse(ctx, 0, h / 2, w / 2, 40)
        stroke(ctx, WHITE, 5)
    for k in range(int(14 * p)):
        chip_side(ctx, 0, h / 2 - 30 - k * 40, 1.25)
    ctx.restore()
    arrow(ctx, W / 2 + 230, 330, W / 2 + 230, 950, ease(clamp((lt - 0.4) / 0.8)), WHITE, 5)
    arrow(ctx, W / 2 + 230, 950, W / 2 + 230, 330, ease(clamp((lt - 0.4) / 0.8)), WHITE, 5)
    ctx.restore()
    ctx.save()
    pill(ctx, counter(lt, 1900, 1966, 0.7), W / 2, 260, pop(lt, 0.0), size=96, rgb=TEAL)
    pill(ctx, "THE TUBE", W / 2, 1420, pop(lt, 1.2), size=56, rgb=YELLOW)


# 10.92 "stack curved chips inside a tube."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, keyframes(lt, [(0, 640), (dur, 760)]))
    bg_kitchen(ctx, T, (1.0, 0.90, 0.62), (0.98, 0.62, 0.30))
    # cara frontal de la patata grande + pila cayendo
    chip_top(ctx, 220, 360, 1.3, 0.3 + 0.1 * math.sin(T))
    ctx.save()
    ctx.translate(680, 720)
    rrect(ctx, -150, -360, 300, 720, 30)
    fill_keep(ctx, CAN_RD, 0.25)
    stroke(ctx, CAN_R, 8)
    n = 14
    for k in range(n):
        tk = 0.1 + k * 0.1
        a = clamp((lt - tk) / 0.25)
        if a <= 0:
            continue
        ty = 330 - k * 46
        chip_side(ctx, 0, lerp(-700, ty, ease_out(a)), 1.3)
    ctx.restore()
    ctx.restore()
    ctx.save()
    pill(ctx, "SADDLE-SHAPED", 300, 620, pop(lt, 0.3), size=40, rgb=CAN_R)
    badge(ctx, "STACKED", 300, 1400, pop(lt, 1.2), size=60, bg=ORANGE)


# 12.98 "Baur was so proud, he wanted to be buried in it."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.14)]), W / 2, 820)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.30, 0.10, 0.25)), (1, (0.10, 0.03, 0.10))]))
    ctx.paint()
    rays(ctx, W / 2, 620, T, GOLD, 0.08)
    can(ctx, W / 2, 620, 0.85, 0.05 * math.sin(T * 2), glow=1.0)
    # medalla
    ap = pop(lt, 0.5)
    if ap > 0.01:
        ctx.save(); ctx.translate(760, 820); ctx.scale(ap, ap)
        ctx.move_to(-40, -120); ctx.line_to(-10, 0); ctx.line_to(10, 0); ctx.line_to(40, -120)
        fill(ctx, BLUE)
        circle(ctx, 0, 40, 70); fill(ctx, GOLD)
        circle(ctx, 0, 40, 50); stroke(ctx, (0.8, 0.55, 0.1), 6)
        text(ctx, "#1", 0, 42, 44, (0.6, 0.35, 0.05), shadow=False)
        ctx.restore()
    ctx.restore()
    ctx.save()
    pill(ctx, "SO PROUD", W / 2, 280, pop(lt, 0.2), size=56, rgb=GOLD)
    badge(ctx, "BURY ME IN IT", W / 2, 1420, pop(lt, 2.0), size=60, bg=CAN_R)


# 15.83 "In the 1980s, he told his kids."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), keyframes(lt, [(0, 600), (dur, 500)]), 860)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.95, 0.75, 0.45)), (1, (0.80, 0.42, 0.30))]))
    ctx.paint()
    # sala: lámpara + sofá
    ctx.rectangle(-600, 1180, W + 1200, 900)
    fill(ctx, (0.45, 0.22, 0.18))
    rrect(ctx, 520, 860, 640, 260, 60)
    fill(ctx, (0.30, 0.45, 0.42))
    person(ctx, 250, 520, 0.95, (0.22, 0.12, 0.16))
    for k, (kx, ks) in enumerate(((620, 0.6), (790, 0.66), (950, 0.56))):
        person(ctx, kx, 700 + (0.66 - ks) * 250, ks, (0.30, 0.15, 0.20))
    bubble(ctx, 440, 300, 300, 230, 300, 430, pop(lt, 0.6))
    if pop(lt, 0.6) > 0.5:
        can(ctx, 440, 300, 0.26, 0.2)
    ctx.restore()
    ctx.save()
    pill(ctx, "1980s", W / 2, 1400, pop(lt, 0.15), size=70, rgb=ORANGE)


# 18.01 "His oldest son just chuckled."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 820)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.95, 0.75, 0.45)), (1, (0.80, 0.42, 0.30))]))
    ctx.paint()
    ctx.rectangle(-600, 1180, W + 1200, 900)
    fill(ctx, (0.45, 0.22, 0.18))
    sh = 8 * abs(math.sin(T * 14))
    person(ctx, 330, 560 - sh, 0.9, (0.30, 0.15, 0.20))
    character(ctx, 820, 700, 0.6, T, mood="feliz", body=True)
    for k, (hx, hy) in enumerate(((520, 330), (610, 230), (450, 200))):
        a = pop(lt, 0.2 + k * 0.25)
        if a > 0.01:
            ctx.save(); ctx.translate(hx, hy); ctx.rotate(-0.15 + 0.1 * k); ctx.scale(a, a)
            text(ctx, "HA", 0, 0, 70, WHITE)
            ctx.restore()
    ctx.restore()
    ctx.save()
    pill(ctx, "OLDEST SON", W / 2, 1400, pop(lt, 0.1), size=56, rgb=YELLOW)


# 19.83 "Then Baur died in 2008, at 89."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, keyframes(lt, [(0, 820), (dur, 760)]))
    bg_dusk(ctx, T, (0.03, 0.03, 0.08), (0.10, 0.08, 0.20), (0.22, 0.14, 0.30))
    spot(ctx, W / 2, 620, 600, 0.25, (0.7, 0.8, 1.0))
    hill(ctx, 900, T, (0.12, 0.25, 0.20), (0.05, 0.12, 0.10))
    headstone(ctx, W / 2, 920, 1.2, "1918 – 2008")
    # vela
    rrect(ctx, 840, 820, 50, 100, 8); fill(ctx, (0.95, 0.92, 0.85))
    fl = 1 + 0.15 * math.sin(T * 13)
    ellipse(ctx, 865, 790, 14, 30 * fl); fill(ctx, (1, 0.75, 0.25))
    spot(ctx, 865, 790, 120, 0.4, (1, 0.7, 0.3))
    ctx.restore()
    ctx.save()
    pill(ctx, "2008", W / 2, 290, pop(lt, 1.0), size=80, rgb=STONE)
    pill(ctx, "AGE 89", W / 2, 1420, pop(lt, 2.1), size=64, rgb=ORANGE)


# 22.57 "On the way to the funeral home, his children"
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 820)
    bg_dusk(ctx, T, (0.05, 0.05, 0.14), (0.20, 0.12, 0.30), (0.50, 0.25, 0.30))
    # ciudad de fondo
    for k in range(9):
        bx = -100 + k * 160
        bh = 260 + 140 * ((k * 37) % 5) / 4
        ctx.rectangle(bx, 900 - bh, 130, bh)
        fill(ctx, (0.12, 0.10, 0.22))
        for j in range(int(bh / 70)):
            rrect(ctx, bx + 25, 900 - bh + 30 + j * 70, 30, 34, 4)
            fill(ctx, (1, 0.85, 0.5), 0.5 if (j + k) % 3 else 0.1)
    ctx.rectangle(-600, 900, W + 1200, 900)
    fill(ctx, (0.15, 0.15, 0.20))
    off = (lt * 600) % 240
    for k in range(-4, 8):
        rrect(ctx, k * 240 - off, 1240, 120, 18, 9)
        fill(ctx, (1, 0.85, 0.3), 0.8)
    car(ctx, 430, 1220, 0.85, T)
    # señal
    rrect(ctx, 640, 520, 300, 120, 14); fill(ctx, (0.15, 0.45, 0.30))
    rrect(ctx, 648, 528, 284, 104, 10); stroke(ctx, WHITE, 4)
    text(ctx, "FUNERAL", 790, 560, 36, WHITE, shadow=False)
    text(ctx, "HOME →", 790, 604, 36, WHITE, shadow=False)
    ctx.rectangle(780, 640, 20, 260); fill(ctx, (0.5, 0.5, 0.55))
    ctx.restore()
    ctx.save()
    pill(ctx, "THE KIDS", W / 2, 1420, pop(lt, 1.4), size=56, rgb=TEAL)


# 24.69 "stopped at a Walgreens."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 780)
    bg_dusk(ctx, T, (0.05, 0.05, 0.14), (0.20, 0.12, 0.30), (0.50, 0.25, 0.30), stars=False)
    ctx.rectangle(-600, 1000, W + 1200, 900)
    fill(ctx, (0.18, 0.18, 0.22))
    store(ctx, W / 2, 1000, 0.95, T)
    car(ctx, 200, 1180, 0.55, 0)
    ctx.restore()
    ctx.save()
    pill(ctx, "WALGREENS", W / 2, 1420, pop(lt, 0.4), size=70, rgb=CAN_RL)


# 25.82 "They debated the flavor, and picked original."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 760)
    bg_kitchen(ctx, T, (0.95, 0.95, 0.92), (0.80, 0.82, 0.80))
    for sy in (900,):
        ctx.rectangle(-600, sy, W + 1200, 40)
        fill(ctx, (0.55, 0.45, 0.35))
    cols = [(CAN_R, CAN_RD), ((0.15, 0.60, 0.30), (0.05, 0.30, 0.15)), ((0.95, 0.50, 0.10), (0.55, 0.25, 0.05)),
            ((0.45, 0.25, 0.65), (0.22, 0.10, 0.35))]
    for k, (c, cd) in enumerate(cols):
        x = 270 + k * 230
        lift = 0.0
        if k == 0:
            lift = ease(clamp((lt - 1.6) / 0.4))
        can(ctx, x, 620 - 80 * lift, 0.45, 0.0, glow=lift, label=None, col=c, cold=cd)
    character(ctx, 150, 1290, 0.40, T, mood="duda" if lt < 1.6 else "feliz", body=True)
    ctx.restore()
    ctx.save()
    pill(ctx, "WHICH FLAVOR?", W / 2, 280, pop(lt, 0.15), size=54, rgb=TEAL)
    badge(ctx, "ORIGINAL", W / 2, 420, pop(lt, 1.7), size=70, bg=CAN_R)


# 28.07 "In other words, they bought his coffin at a drugstore."  (2.º gancho)
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.6), (0.3, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 40) * (lt < 0.4), W / 2, 800)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.20, 0.02, 0.05)), (1, (0.05, 0.01, 0.03))]))
    ctx.paint()
    rays(ctx, W / 2, 620, T, RED, 0.08)
    # bolsa de papel
    ctx.move_to(250, 900); ctx.line_to(830, 900); ctx.line_to(800, 470); ctx.line_to(280, 470); ctx.close_path()
    fill(ctx, (0.78, 0.62, 0.42))
    can(ctx, W / 2, 520, 0.75, -0.05, glow=0.8, lid=1.0)
    ctx.move_to(250, 900); ctx.line_to(830, 900); ctx.line_to(815, 700); ctx.line_to(265, 700); ctx.close_path()
    fill(ctx, (0.70, 0.55, 0.36))
    text(ctx, "PHARMACY", W / 2, 800, 46, (0.45, 0.30, 0.18), shadow=False)
    ctx.restore()
    ctx.save()
    badge(ctx, "HIS COFFIN", W / 2, 280, pop(lt, 1.6), size=70, bg=RED)
    pill(ctx, "FROM A DRUGSTORE", W / 2, 1420, pop(lt, 2.6), size=50, rgb=YELLOW)


# 31.35 "Part of Fredric Baur's ashes went into that can."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, keyframes(lt, [(0, 800), (dur, 720)]))
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.14, 0.16, 0.22)), (1, (0.05, 0.06, 0.10))]))
    ctx.paint()
    spot(ctx, 600, 650, 650, 0.25, (0.9, 0.9, 1.0))
    ctx.save()
    ctx.translate(330, 380)
    ctx.rotate(1.9)
    urn(ctx, 0, 0, 0.75)
    ctx.restore()
    ash_pour(ctx, 420, 420, 660, 560, T, ease(clamp((lt - 0.2) / 0.4)))
    can(ctx, 660, 860, 0.62, 0.0, lid=1.0, open_=1.0)
    ctx.restore()
    ctx.save()
    ficha(ctx, "FREDRIC BAUR", FICHA_SUB, W / 2, 1450, pop(lt, 0.2), "🧪", CAN_RL)
    pill(ctx, "PART OF HIS ASHES", W / 2, 260, pop(lt, 1.2), size=46, rgb=STONE)


# 33.96 "The rest went into an urn, buried with it in Cincinnati."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.9), (dur, 1.02)]), W / 2, keyframes(lt, [(0, 760), (dur, 900)]))
    bg_dusk(ctx, T, (0.10, 0.06, 0.20), (0.42, 0.16, 0.30), (0.95, 0.48, 0.30))
    soil(ctx, 620)
    headstone(ctx, W / 2, 620, 0.7)
    ctx.rectangle(150, 1180, 780, 470)
    fill(ctx, (0.12, 0.07, 0.04), 0.6)
    can(ctx, 380, 1400, 0.5, 0.0, glow=0.5)
    urn(ctx, 720, 1440, 0.7)
    ctx.restore()
    ctx.save()
    pill(ctx, "URN", 760, 1450 - 140, pop(lt, 0.9), size=44, rgb=STONE)
    pill(ctx, "CINCINNATI, OHIO", W / 2, 280, pop(lt, 2.6), size=54, rgb=ORANGE)


# 36.94 "And the can is still down there."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, keyframes(lt, [(0, 700), (dur, 880)]))
    bg_dusk(ctx, T, (0.04, 0.03, 0.10), (0.15, 0.08, 0.22), (0.35, 0.18, 0.30))
    soil(ctx, 760)
    headstone(ctx, 330, 760, 0.6)
    can(ctx, W / 2, 1360, 0.5, 0.0, glow=0.9 + 0.2 * math.sin(T * 4))
    character(ctx, 840, 520, 0.42, T, mood="sorpresa", body=True)
    arrow(ctx, 900, 1280, 680, 1360, ease(clamp((lt - 0.3) / 0.5)), YELLOW, 10)
    ctx.restore()
    ctx.save()
    badge(ctx, "STILL THERE", W / 2, 300, pop(lt, 0.6), size=64, bg=TEAL, fg=(0.02, 0.12, 0.12))


# 38.49 "Because, at his own request," -> vuelve a e1
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.10, e2), (4.66, e3), (5.48, e4), (8.40, e5), (10.92, e6), (12.98, e7), (15.83, e8),
           (18.01, e9), (19.83, e10), (22.57, e11), (24.69, e12), (25.82, e13), (28.07, e14), (31.35, e15),
           (33.96, e16), (36.94, e17), (38.49, e18)]
SFX = [(8.45, "pop"), (25.10, "ding"), (27.55, "pop"), (28.10, "ding")]


# ---------------- miniatura (no desvela que está enterrado en el bote) ----------------
def MINIATURA(ctx):
    T = 1.3
    ctx.save()
    camera(ctx, 1.0, W / 2, 960)
    bg_dusk(ctx, T)
    spot(ctx, W / 2, 1150, 800, 0.35, (1, 0.6, 0.3))
    headstone(ctx, 200, 1150, 0.62)
    headstone(ctx, 900, 1130, 0.5, None)
    hill(ctx, 1120, T)
    can(ctx, W / 2, 1000, 0.95, -0.06, glow=1.3, open_=0.0)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_circle(ctx, W / 2 - 15, 690, 200, 110)
    badge(ctx, "?", 800, 600, 1.0, size=90, bg=RED)
    thumb_text(ctx, ["WHAT'S INSIDE", ("THIS CAN?", WHITE)], y=230, size=160)
    ficha(ctx, "FREDRIC BAUR", FICHA_SUB, W / 2, 1620, 1.0, "🧪", CAN_RL)
