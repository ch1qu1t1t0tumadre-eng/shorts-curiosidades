"""v19 (EN) FORMATO BUCLE: Gustave Eiffel's secret apartment at the top of the Eiffel Tower."""
from kit import *  # noqa

IRON = (0.55, 0.38, 0.28)
IRON_D = (0.36, 0.24, 0.18)


def tower(ctx, x, base_y, h, T, lit=1.0):
    """Torre de celosía estilizada. base_y = suelo, h = altura total."""
    w = h * 0.36
    def side(sx):
        ctx.move_to(x + sx * w / 2, base_y)
        ctx.curve_to(x + sx * w * 0.22, base_y - h * 0.30, x + sx * w * 0.08, base_y - h * 0.65, x + sx * 6, base_y - h * 0.92)
    for sx in (-1, 1):
        side(sx); stroke(ctx, IRON, max(6, h * 0.018))
    # celosía
    for k in range(1, 24):
        f = k / 24
        yy = base_y - h * 0.92 * f
        ww = w / 2 * (1 - f) ** 1.6 + 6
        ctx.move_to(x - ww, yy); ctx.line_to(x + ww, yy - h * 0.02); stroke(ctx, IRON_D, 3, 0.8)
        ctx.move_to(x + ww, yy); ctx.line_to(x - ww, yy - h * 0.02); stroke(ctx, IRON_D, 3, 0.8)
    # arco
    ctx.arc(x, base_y, w * 0.28, math.pi, 0); stroke(ctx, IRON, max(5, h * 0.012))
    # plataformas
    for f, ww in ((0.30, w * 0.40), (0.56, w * 0.22), (0.86, w * 0.09)):
        rrect(ctx, x - ww, base_y - h * f, ww * 2, h * 0.018, 3); fill(ctx, IRON_D)
    # apartamento arriba (ventana encendida) + aguja
    top_y = base_y - h * 0.90
    rrect(ctx, x - w * 0.06, top_y - h * 0.035, w * 0.12, h * 0.035, 3); fill(ctx, IRON_D)
    rrect(ctx, x - w * 0.045, top_y - h * 0.028, w * 0.09, h * 0.018, 2); fill(ctx, (1, 0.85, 0.45), lit)
    if lit > 0:
        spotlight(ctx, x, top_y - h * 0.02, h * 0.10, 0.6 * lit, (1, 0.85, 0.45))
    ctx.move_to(x, top_y - h * 0.035); ctx.line_to(x, base_y - h); stroke(ctx, IRON_D, max(3, h * 0.006))


def paris_night(ctx, T, ground_y=1500):
    bg_dark(ctx, T, top=(0.04, 0.04, 0.14), mid=(0.14, 0.10, 0.30), bot=(0.30, 0.15, 0.30), motes=False)
    rng = np.random.default_rng(9)
    for _ in range(80):
        circle(ctx, rng.uniform(-300, W + 300), rng.uniform(-400, 900), rng.uniform(1.5, 4)); fill(ctx, WHITE, 0.6)
    for k in range(-3, 16):
        bh = 120 + (k * 37 % 5) * 40
        ctx.rectangle(k * 90, ground_y - bh, 86, bh + 800); fill(ctx, (0.08, 0.06, 0.14))
        for j in range(3):
            ctx.rectangle(k * 90 + 20, ground_y - bh + 30 + j * 40, 14, 18); fill(ctx, (1, 0.85, 0.5), 0.5 if (k + j) % 3 else 0)


def apartment(ctx, T, figures=False, phono=0.0):
    """Interior del apartamento: papel pintado, muebles de madera, piano."""
    ctx.set_source(vgrad(ctx, 0, -300, 0, H + 300, [(0, (0.45, 0.18, 0.16)), (1, (0.25, 0.08, 0.08))])); ctx.paint()
    for k in range(-6, 16):
        for j in range(-3, 22):
            circle(ctx, k * 120 + (j % 2) * 60, j * 110, 14); fill(ctx, GOLD, 0.15)
    ctx.rectangle(-500, 1350, W + 1000, 1200); fill(ctx, (0.35, 0.20, 0.10))
    rrect(ctx, 620, 380, 340, 360, 16); fill_keep(ctx, (0.10, 0.12, 0.30)); stroke(ctx, WOOD, 16)  # ventana
    for k in range(10):
        circle(ctx, 660 + (k * 53) % 280, 420 + (k * 37) % 280, 3); fill(ctx, (1, 0.85, 0.5), 0.8)
    # piano
    rrect(ctx, 80, 980, 460, 380, 16); fill(ctx, (0.10, 0.06, 0.04))
    rrect(ctx, 100, 1100, 420, 60, 6); fill(ctx, WHITE)
    for k in range(14):
        ctx.rectangle(110 + k * 30, 1100, 3, 60); fill(ctx, (0.2, 0.2, 0.2))
    # mesa
    rrect(ctx, 640, 1150, 360, 40, 10); fill(ctx, WOOD)
    rrect(ctx, 680, 1190, 30, 170, 8); fill(ctx, WOOD_D); rrect(ctx, 930, 1190, 30, 170, 8); fill(ctx, WOOD_D)
    if phono > 0:
        ctx.save(); ctx.translate(820, 1080); ctx.scale(phono, phono)
        rrect(ctx, -90, -10, 180, 80, 10); fill(ctx, WOOD)
        ctx.move_to(-10, -10); ctx.curve_to(0, -120, 80, -170, 160, -200); ctx.line_to(170, -100); ctx.curve_to(90, -110, 30, -60, 20, -10)
        ctx.close_path(); fill(ctx, GOLD)
        ctx.restore()
    if figures:
        gent(ctx, 360, 640, 0.75, col=(0.35, 0.30, 0.28), hat=False)
        gent(ctx, 780, 660, 0.72, col=(0.30, 0.28, 0.34), hat=True)


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 760)
    paris_night(ctx, T)
    tower(ctx, W / 2, 1650, 1500, T, lit=1.0)
    ctx.restore(); ctx.save()
    ficha(ctx, "GUSTAVE EIFFEL", "ENGINEER · 1832–1923", W / 2, 1640, 1.0, "🗼", YELLOW)


# 0.0 "Gustave Eiffel built a secret apartment at the top of the Eiffel Tower."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 4.0 "Just for himself."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 2.6), (dur, 3.0)]), W / 2, 330)
    paris_night(ctx, T)
    tower(ctx, W / 2, 1650, 1500, T, lit=1.0)
    ctx.restore(); ctx.save()
    stamp(ctx, "PRIVATE", W / 2, 1450, lt / 0.25, size=100)


# 5.0 "When the tower opened in 1889, it was the tallest structure on Earth."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    paris_night(ctx, T, 1600)
    tower(ctx, 700, 1600, 1300, T)
    for k, hh in enumerate((320, 480, 260)):
        rrect(ctx, 120 + k * 130, 1600 - hh, 100, hh, 6); fill(ctx, (0.20, 0.18, 0.28))
    pill(ctx, "1889", 240, 360, pop(lt, 0.8), size=80, rgb=GOLD)
    pill(ctx, "TALLEST ON EARTH", W / 2, 1720, pop(lt, 2.4), size=50, rgb=RED)


# 9.1 "The public could climb to the top platform."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 700)
    paris_night(ctx, T)
    tower(ctx, W / 2, 1650, 1500, T)
    for k in range(7):
        circle(ctx, 470 + k * 22, 330 + 6 * math.sin(T * 4 + k), 9); fill(ctx, WHITE)
    pill(ctx, "PUBLIC", 780, 360, pop(lt, 0.3), size=46, rgb=TEAL)


# 11.1 "But right above them, Eiffel kept a private apartment,"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 3.0), (dur, 3.6)]), W / 2, 300)
    paris_night(ctx, T)
    tower(ctx, W / 2, 1650, 1500, T, lit=1.0)
    ctx.restore(); ctx.save()
    arrow(ctx, 200, 1500, 420, 1150, ease(lt / 0.6), YELLOW, 14)
    pill(ctx, "SECRET APARTMENT", W / 2, 1650, pop(lt, 0.5), size=50, rgb=GOLD)


# 13.7 "with wallpaper, wooden furniture, and even a piano."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    apartment(ctx, T)
    icon(ctx, "🎹", 310, 860, 160, pop(lt, 2.0))


# 16.5 "Wealthy Parisians offered him fortunes to spend just one night up there."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    paris_night(ctx, T, 1700)
    for k in range(4):
        money_bag(ctx, 200 + k * 230, 720 + 40 * math.sin(T * 3 + k), 0.7 * pop(lt, 0.3 * k + 0.4), "$")
    pill(ctx, "ONE NIGHT?", W / 2, 1420, pop(lt, 2.6), size=60, rgb=GOLD)


# 20.2 "In other words, it was the most exclusive address in Paris."  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 760)
    paris_night(ctx, T)
    rays(ctx, W / 2, 330, T, GOLD, 0.06)
    tower(ctx, W / 2, 1650, 1500, T, lit=1.3)
    badge(ctx, "No. 1 ADDRESS IN PARIS", W / 2, 1420, pop(lt, 1.0), size=48)


# 23.6 "And he said no to every single offer."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    paris_night(ctx, T, 1700)
    for k in range(3):
        money_bag(ctx, 250 + k * 290, 760, 0.75, "$")
    stamp(ctx, "NO", W / 2, 760, (lt - 0.4) / 0.25, size=220)


# 25.9 "But in September 1889, he made one famous exception."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    rrect(ctx, W / 2 - 230, 380, 460, 380, 24); fill(ctx, WHITE)
    rrect(ctx, W / 2 - 230, 380, 460, 100, 24); fill(ctx, RED)
    text(ctx, "SEPTEMBER", W / 2, 430, 46, WHITE, shadow=False)
    text(ctx, "1889", W / 2, 620, 130, INK, shadow=False)
    pill(ctx, "ONE EXCEPTION", W / 2, 1450, pop(lt, 2.0), rgb=GOLD)


# 29.5 "Thomas Edison came up for cognac and cigars,"
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    apartment(ctx, T)
    gent(ctx, 780, 600, 0.7, col=(0.08, 0.08, 0.12))
    icon(ctx, "🥃", 700, 1100, 120, pop(lt, 1.0))
    ficha(ctx, "THOMAS EDISON", "INVENTOR · 1847–1931", W / 2, 1600, pop(lt, 0.1), "💡", YELLOW)


# 31.8 "and gave Eiffel one of his brand-new phonographs."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.4, 1.0), (dur, 1.06)]), W / 2, 900)
    apartment(ctx, T, phono=pop(lt, 0.3))
    spotlight(ctx, 820, 1000, 300, 0.4, GOLD)
    pill(ctx, "PHONOGRAPH", W / 2, 1600, pop(lt, 1.2), rgb=GOLD)


# 34.4 "Today you can still peek inside, where wax figures of Eiffel and Edison sit frozen in that moment."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 900)
    apartment(ctx, T, figures=True, phono=1.0)
    rrect(ctx, 40, 240, 1000, 1180, 30); fill(ctx, GLASS, 0.10)  # cristal
    ctx.move_to(100, 300); ctx.line_to(300, 300); ctx.line_to(100, 600); fill(ctx, WHITE, 0.12)
    pill(ctx, "WAX FIGURES", W / 2, 1600, pop(lt, 1.8), rgb=STONE)


# 39.7 "Because hidden at the very top of Paris," -> vuelve a e1
def e14(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (4.0, e2), (5.0, e3), (9.1, e4), (11.1, e5), (13.7, e6), (16.5, e7), (20.2, e8),
           (23.6, e9), (25.9, e10), (29.5, e11), (31.8, e12), (34.4, e13), (39.7, e14)]
SFX = [(4.05, "pop"), (20.25, "ding"), (24.0, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    paris_night(ctx, T, 1900)
    tower(ctx, W / 2, 1900, 1550, T, lit=1.5)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["WHO LIVES", ("UP HERE?", WHITE)], y=1520, size=180, rot=0.03)
    thumb_circle(ctx, W / 2, 470, 120, 90)
    thumb_arrow(ctx, 160, 820, 420, 520)
