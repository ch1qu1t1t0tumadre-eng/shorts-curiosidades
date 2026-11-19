"""v14 (EN) FORMATO BUCLE: Abraham Lincoln is in the Wrestling Hall of Fame (≈300 matches, 1 loss)."""
from kit import *  # noqa

MAT = (0.70, 0.12, 0.14)
HAT = (0.06, 0.06, 0.10)


def ring(ctx, T, cy=1250, crowd=True):
    bg_dark(ctx, T, top=(0.03, 0.03, 0.08), mid=(0.08, 0.06, 0.16), bot=(0.02, 0.02, 0.05), motes=False)
    for k in range(3):
        spotlight(ctx, 200 + k * 340, 200, 700, 0.18, (1, 0.95, 0.8))
    if crowd:
        for k in range(12):
            circle(ctx, k * 100 - 20 + (k % 2) * 30, cy - 470 + (k % 3) * 18, 46)
            fill(ctx, (0.08, 0.08, 0.14))
            rrect(ctx, k * 100 - 70 + (k % 2) * 30, cy - 430 + (k % 3) * 18, 100, 200, 40)
            fill(ctx, (0.08, 0.08, 0.14))
    ctx.move_to(-200, cy + 400); ctx.line_to(140, cy - 200); ctx.line_to(940, cy - 200); ctx.line_to(1280, cy + 400)
    ctx.close_path(); fill(ctx, MAT)
    for k in range(3):
        y = cy - 200 - 60 - k * 70
        ctx.move_to(100, y + 30); ctx.line_to(980, y + 30); stroke(ctx, WHITE, 8, 0.9)
    for x in (110, 970):
        rrect(ctx, x - 16, cy - 470, 32, 300, 8); fill(ctx, (0.75, 0.75, 0.8))


def belt(ctx, x, y, s=1.0, T=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    spotlight(ctx, 0, 0, 420, 0.35, GOLD)
    rrect(ctx, -420, -70, 840, 140, 60); fill(ctx, (0.12, 0.10, 0.10))
    ctx.save(); ctx.scale(1, 0.8); circle(ctx, 0, 0, 190); ctx.restore()
    ctx.set_source(vgrad(ctx, 0, -160, 0, 160, [(0, (1, 0.9, 0.5)), (1, (0.78, 0.55, 0.15))])); ctx.fill()
    ctx.save(); ctx.scale(1, 0.8); circle(ctx, 0, 0, 150); ctx.restore(); stroke(ctx, (0.6, 0.42, 0.1), 8)
    text(ctx, "CHAMP", 0, 0, 56, (0.45, 0.28, 0.05), shadow=False)
    for sx in (-1, 1):
        circle(ctx, sx * 300, 0, 50); fill(ctx, GOLD)
    ctx.restore()


def five_bill(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -470, -210, 940, 420, 20); fill(ctx, (0.80, 0.86, 0.74))
    rrect(ctx, -440, -180, 880, 360, 14); stroke(ctx, (0.25, 0.40, 0.30), 8)
    ctx.save(); ctx.scale(0.8, 1); circle(ctx, 0, 0, 150); ctx.restore(); fill(ctx, (0.65, 0.74, 0.62))
    gent(ctx, 0, -20, 0.38, col=(0.20, 0.32, 0.24))
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        text(ctx, "5", sx * 370, sy * 120, 90, (0.20, 0.32, 0.24), shadow=False)
    text(ctx, "FIVE DOLLARS", 0, 160, 34, (0.20, 0.32, 0.24), shadow=False)
    ctx.restore()


def wrestlers(ctx, x, y, s, T):
    """Dos siluetas forcejeando: la alta con chistera (Lincoln) y otra sin sombrero."""
    sw = math.sin(T * 3) * 0.08
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.translate(-150, 0); ctx.rotate(0.18 + sw); gent(ctx, 0, -560, 0.9, col=HAT); ctx.restore()
    ctx.save(); ctx.translate(170, 60); ctx.rotate(-0.25 - sw); gent(ctx, 0, -470, 0.8, col=(0.25, 0.12, 0.10), hat=False); ctx.restore()
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 880)
    ring(ctx, T)
    belt(ctx, W / 2, 720, 1.0, T)
    ctx.restore(); ctx.save()
    ficha(ctx, "ABRAHAM LINCOLN", "16TH U.S. PRESIDENT · 1809–1865", W / 2, 1560, 1.0, "🇺🇸", YELLOW)


# 0.0 "Abraham Lincoln is in the Wrestling Hall of Fame."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 2.9 "Not as a fan."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    ring(ctx, T, 1350)
    icon(ctx, "🍿", W / 2, 700, 300, pop(lt, 0.0))
    stamp(ctx, "NOT A FAN", W / 2, 700, (lt - 0.3) / 0.25, size=100)


# 3.7 "As a fighter."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.25, 1.05), (dur, 1.1)]), W / 2, 900)
    ring(ctx, T, 1350, crowd=False)
    wrestlers(ctx, W / 2, 1250, 1.0, T)


# 4.5 "Before he was president, young Lincoln was six foot four, with unusually long arms."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 900)
    bg_blueprint(ctx, T)
    for k in range(8):
        y = 1500 - k * 140
        ctx.move_to(820, y); ctx.line_to(900, y); stroke(ctx, WHITE, 5, 0.7)
        text(ctx, f"{k}'", 960, y, 40, WHITE, shadow=False)
    grow = ease(clamp((lt - 1.0) / 1.5))
    gent(ctx, 450, lerp(1300, 520, grow), 1.0, col=HAT)
    pill(ctx, "6'4\"", 450, 300, pop(lt, 2.4), size=80, rgb=GOLD)
    if lt > 3.4:
        arrow(ctx, 260, 980, 90, 980, ease((lt - 3.4) / 0.4), YELLOW, 10)
        arrow(ctx, 640, 980, 810, 980, ease((lt - 3.4) / 0.4), YELLOW, 10)


# 9.2 "And on the Illinois frontier, wrestling was how men proved themselves."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    ctx.set_source(vgrad(ctx, 0, 0, 0, 1200, [(0, (0.95, 0.65, 0.35)), (1, (0.85, 0.45, 0.30))])); ctx.paint()
    circle(ctx, 780, 600, 160); fill(ctx, (1, 0.85, 0.5))
    ground(ctx, 1150, (0.35, 0.30, 0.15))
    ctx.save(); ctx.translate(320, 1150)
    for k in range(7):
        rrect(ctx, -230, -60 - k * 52, 460, 48, 20); fill(ctx, WOOD if k % 2 else WOOD_D)
    ctx.move_to(-270, -400); ctx.line_to(0, -560); ctx.line_to(270, -400); ctx.close_path(); fill(ctx, (0.30, 0.18, 0.10))
    ctx.restore()
    wrestlers(ctx, 780, 1300, 0.55, T)
    pill(ctx, "ILLINOIS · 1830s", W / 2, 300, pop(lt, 0.3), rgb=TEAL)


# 13.0 "Historians count around three hundred matches."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_blueprint(ctx, T)
    n = int(clamp(lt / 2.0) * 60)
    for k in range(n):
        gx, gy = 140 + (k % 10) * 85, 360 + (k // 10) * 110
        for j in range(4):
            ctx.move_to(gx + j * 14, gy); ctx.line_to(gx + j * 14, gy + 70); stroke(ctx, WHITE, 5, 0.8)
        ctx.move_to(gx - 8, gy + 60); ctx.line_to(gx + 54, gy + 10); stroke(ctx, YELLOW, 5, 0.9)
    pill(ctx, counter(lt, 0, 300, 2.0) + " MATCHES", W / 2, 1450, pop(lt, 0.0), size=60, rgb=GOLD)


# 15.4 "And Lincoln lost only one."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (0.3, 1.0), (dur, 1.05)]), W / 2, 900)
    bg_dark(ctx, T, motes=False)
    rrect(ctx, 140, 380, 800, 520, 30); fill_keep(ctx, (0.05, 0.05, 0.08)); stroke(ctx, GOLD, 8)
    text(ctx, "WINS", 340, 470, 50, GREEN)
    text(ctx, "LOSSES", 740, 470, 50, RED)
    text(ctx, "299", 340, 700, 170, WHITE)
    text(ctx, "1", 740, 700, 170, WHITE)
    thumb_circle(ctx, 740, 700, 130, 140) if lt > 0.8 else None


# 17.2 "In other words, the man on the five-dollar bill was almost unbeatable."  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.04, 0.12, 0.06), mid=(0.08, 0.22, 0.10))
    rays(ctx, W / 2, 700, T, GREEN, 0.06)
    five_bill(ctx, W / 2, 700, 1.0, -0.06)
    stamp(ctx, "UNBEATABLE", W / 2, 1420, (lt - 2.2) / 0.3, size=85)


# 21.0 "Legend says that after one win, he turned to the crowd and challenged anyone else to try him."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    ring(ctx, T, 1350)
    gent(ctx, W / 2, 620, 0.9, col=HAT)
    for sx in (-1, 1):
        ctx.save(); ctx.translate(W / 2 + sx * 120, 780); ctx.rotate(sx * 2.4)
        rrect(ctx, -30, 0, 60, 300, 30); fill(ctx, HAT); ctx.restore()
    badge(ctx, "LEGEND", W / 2, 270, pop(lt, 0.0), size=56, bg=PURPLE)
    pill(ctx, '"WHO\'S NEXT?"', W / 2, 1500, pop(lt, 2.4), size=50, rgb=WHITE)


# 25.6 "Nobody stepped up."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    ring(ctx, T, 1350)
    icon(ctx, "🦗", W / 2, 720, 260, pop(lt, 0.1))
    stamp(ctx, "NOBODY", W / 2, 380, (lt - 0.2) / 0.25, size=100, col=YELLOW)


# 26.6 "The only man known to beat him was a soldier named Thompson, in 1832."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.10, 0.10, 0.06), mid=(0.20, 0.18, 0.10))
    gent(ctx, W / 2, 520, 1.0, col=(0.20, 0.25, 0.15), hat=False)
    rrect(ctx, W / 2 - 110, 400, 220, 60, 10); fill(ctx, (0.20, 0.25, 0.15))  # gorra militar
    rrect(ctx, W / 2 - 80, 340, 160, 80, 20); fill(ctx, (0.20, 0.25, 0.15))
    pill(ctx, "SOLDIER THOMPSON", W / 2, 1300, pop(lt, 2.2), size=50, rgb=STONE)
    pill(ctx, "1832", W / 2, 1450, pop(lt, 3.0), size=70, rgb=GOLD)


# 30.7 "Then in 1992,"
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    pill(ctx, counter(lt, 1865, 1992, 1.2), W / 2, 700, pop(lt, 0.0), size=150, rgb=GOLD)


# 32.3 "the National Wrestling Hall of Fame made it official, and honored Lincoln as an Outstanding American."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.08, 0.06, 0.02), mid=(0.20, 0.15, 0.05))
    rays(ctx, W / 2, 650, T, GOLD, 0.06)
    icon(ctx, "🏆", W / 2, 640, 420, pop(lt, 0.2))
    pill(ctx, "HALL OF FAME", W / 2, 260, pop(lt, 0.4), rgb=GOLD)
    pill(ctx, "OUTSTANDING AMERICAN", W / 2, 1450, pop(lt, 3.2), size=50, rgb=RED)


# 37.1 "So next time you look at a five-dollar bill, remember:" -> vuelve a e1
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.04, 0.12, 0.06), mid=(0.08, 0.22, 0.10))
    five_bill(ctx, W / 2, 760, 1.0, 0.04)


def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.9, e2), (3.7, e3), (4.5, e4), (9.2, e5), (13.0, e6), (15.4, e7), (17.2, e8),
           (21.0, e9), (25.6, e10), (26.6, e11), (30.7, e12), (32.3, e13), (37.1, e14), (38.5, e15)]
SFX = [(3.75, "pop"), (15.45, "ding"), (17.25, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    ring(ctx, T, 1450)
    wrestlers(ctx, W / 2, 1400, 1.0, T)
    ctx.restore()
    thumb_vignette(ctx, 0.55)
    thumb_text(ctx, ["299 WINS.", ("1 LOSS.", WHITE)], y=260, size=200)
    thumb_circle(ctx, W / 2 - 140, 780, 170, 170)
    thumb_arrow(ctx, 100, 1150, 300, 900)
    badge(ctx, "WHO IS HE?", 780, 1740, 1.0, size=56)
