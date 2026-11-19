"""v16 (EN) FORMATO BUCLE: Marie Curie's notebooks are still radioactive."""
from kit import *  # noqa

RAD = (0.45, 1.0, 0.45)
LEAD = (0.45, 0.47, 0.52)


def glow_particles(ctx, x, y, r, T, n=26, a=1.0):
    rng = np.random.default_rng(5)
    for k in range(n):
        ang = rng.uniform(0, math.tau) + T * rng.uniform(0.2, 0.6)
        d = r * ((rng.uniform(0, 1) + T * 0.25) % 1)
        circle(ctx, x + math.cos(ang) * d, y + math.sin(ang) * d * 0.9, rng.uniform(4, 10))
        fill(ctx, RAD, a * (1 - d / r) * 0.9)


def notebook(ctx, x, y, s, T, glow=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    if glow > 0:
        spotlight(ctx, 0, 0, 620, 0.45 * glow, RAD)
    for side in (-1, 1):
        ctx.move_to(0, -300); ctx.line_to(side * 400, -330); ctx.line_to(side * 400, 300); ctx.line_to(0, 330); ctx.close_path()
        fill(ctx, (0.93, 0.90, 0.78))
        for k in range(9):
            yy = -230 + k * 55
            ctx.move_to(side * 50, yy); ctx.line_to(side * (330 - (k % 3) * 60), yy - 10 * side * 0)
            stroke(ctx, (0.35, 0.30, 0.45), 4, 0.6)
    ctx.move_to(0, -300); ctx.line_to(0, 330); stroke(ctx, (0.6, 0.55, 0.45), 6)
    text(ctx, "Ra", -200, -260, 50, (0.35, 0.30, 0.45), shadow=False)
    text(ctx, "226", 200, -260, 40, (0.35, 0.30, 0.45), shadow=False)
    ctx.restore()
    if glow > 0:
        glow_particles(ctx, x, y, 520 * s, T, a=glow)


def vial(ctx, x, y, s, T, glow=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    spotlight(ctx, 0, 40, 300, 0.6 * glow, RAD)
    rrect(ctx, -45, -170, 90, 330, 45); fill_keep(ctx, GLASS, 0.15); stroke(ctx, GLASS, 6, 0.8)
    rrect(ctx, -38, 20, 76, 132, 36); fill(ctx, RAD, 0.9)
    rrect(ctx, -55, -200, 110, 40, 10); fill(ctx, (0.55, 0.4, 0.25))
    ctx.restore()


def element(ctx, x, y, sym, num, name, appear=1.0, col=RAD):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(appear, appear)
    rrect(ctx, -170, -190, 340, 380, 24); fill_keep(ctx, (0.06, 0.10, 0.08)); stroke(ctx, col, 8)
    text(ctx, str(num), -110, -130, 44, col, shadow=False)
    text(ctx, sym, 0, 10, 150, WHITE)
    text(ctx, name, 0, 140, 38, col, shadow=False)
    ctx.restore()


def lead_box(ctx, x, y, s, T, open_=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if open_ > 0:
        spotlight(ctx, 0, -200, 500, 0.5 * open_, RAD)
    rrect(ctx, -330, -160, 660, 380, 18)
    ctx.set_source(vgrad(ctx, 0, -160, 0, 220, [(0, (0.60, 0.62, 0.68)), (1, (0.35, 0.37, 0.42))])); ctx.fill()
    ctx.save(); ctx.translate(0, -160); ctx.rotate(-0.6 * open_)
    rrect(ctx, -350, -60, 700, 70, 14); fill(ctx, (0.55, 0.57, 0.62)); ctx.restore()
    circle(ctx, 0, 40, 90); fill(ctx, (1, 0.85, 0.1))
    for k in range(3):
        a0 = -math.pi / 2 + k * math.tau / 3 - 0.5
        ctx.move_to(0, 40); ctx.arc(0, 40, 80, a0, a0 + 1.0); ctx.close_path(); fill(ctx, (0.08, 0.08, 0.08))
    circle(ctx, 0, 40, 22); fill(ctx, (1, 0.85, 0.1)); circle(ctx, 0, 40, 14); fill(ctx, (0.08, 0.08, 0.08))
    text(ctx, "LEAD", 0, 180, 40, (0.2, 0.2, 0.24), shadow=False)
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 880)
    bg_dark(ctx, T, top=(0.02, 0.06, 0.04), mid=(0.04, 0.14, 0.08), bot=(0.01, 0.03, 0.02))
    notebook(ctx, W / 2, 760, 1.0, T, glow=1.0, rot=-0.06)
    ctx.restore(); ctx.save()
    ficha(ctx, "MARIE CURIE", "PHYSICIST & CHEMIST · 1867–1934", W / 2, 1560, 1.0, "🧪", RAD)


# 0.0 "Marie Curie's notebooks are still radioactive."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 2.9 "More than a hundred years later."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    icon(ctx, "⏳", W / 2, 620, 320, pop(lt, 0.0))
    pill(ctx, counter(lt, 1898, 2026, 1.2), W / 2, 1300, pop(lt, 0.1), size=90, rgb=RAD)


# 4.5 "Curie was the first woman to win a Nobel Prize,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.08, 0.06, 0.02), mid=(0.20, 0.15, 0.05))
    rays(ctx, W / 2, 680, T, GOLD, 0.06)
    icon(ctx, "🏅", W / 2, 680, 420, pop(lt, 0.0))
    pill(ctx, "FIRST WOMAN · 1903", W / 2, 1450, pop(lt, 0.6), size=50, rgb=GOLD)


# 7.5 "and the only person ever to win in two different sciences."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.08, 0.06, 0.02), mid=(0.20, 0.15, 0.05))
    icon(ctx, "🏅", 300, 660, 300, pop(lt, 0.2))
    icon(ctx, "🏅", 780, 660, 300, pop(lt, 1.2))
    pill(ctx, "PHYSICS", 300, 1350, pop(lt, 0.4), size=46, rgb=TEAL)
    pill(ctx, "CHEMISTRY", 780, 1350, pop(lt, 1.4), size=46, rgb=RAD)


# 10.4 "She discovered polonium and radium,"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.02, 0.06, 0.04), mid=(0.04, 0.14, 0.08))
    element(ctx, 300, 640, "Po", 84, "POLONIUM", pop(lt, 0.2), TEAL)
    element(ctx, 780, 640, "Ra", 88, "RADIUM", pop(lt, 1.2), RAD)


# 12.3 "and handled them with her bare hands."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.02, 0.06, 0.04), mid=(0.04, 0.14, 0.08))
    vial(ctx, W / 2, 640, 1.4, T)
    icon(ctx, "✋", W / 2 + 40, 1260, 300, pop(lt, 0.4))
    stamp(ctx, "NO GLOVES", W / 2, 300, (lt - 1.0) / 0.3, size=80)


# 14.1 "She even carried radium around in her pocket."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 850)
    bg_dark(ctx, T, top=(0.06, 0.04, 0.08), mid=(0.12, 0.08, 0.16))
    rrect(ctx, 140, 260, 800, 1200, 60); fill(ctx, (0.18, 0.15, 0.22))  # bata
    ctx.move_to(540, 260); ctx.line_to(540, 1460); stroke(ctx, (0.10, 0.08, 0.12), 8)
    vial(ctx, 720, 640, 0.9, T, glow=1.0)
    rrect(ctx, 590, 700, 260, 240, 20); fill(ctx, (0.22, 0.19, 0.27))  # bolsillo delante del vial
    pill(ctx, "IN HER POCKET", W / 2, 1600, pop(lt, 0.8), rgb=RAD)


# 16.4 "In other words, everything she touched became radioactive."  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.02, 0.12, 0.04), mid=(0.04, 0.25, 0.08))
    rays(ctx, W / 2, 680, T, RAD, 0.07)
    icon(ctx, "☢️", W / 2, 680, 460, pop(lt, 0.0))
    glow_particles(ctx, W / 2, 680, 600, T)


# 19.5 "Her notebooks. Her furniture. Even her cookbooks."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.02, 0.06, 0.04), mid=(0.04, 0.14, 0.08))
    for k, (em, lab, t0) in enumerate((("📓", "NOTEBOOKS", 0.0), ("🪑", "FURNITURE", 0.8), ("📖", "COOKBOOKS", 1.7))):
        y = 380 + k * 440
        p = pop(lt, t0)
        if p > 0.01:
            spotlight(ctx, 330, y, 220, 0.4 * p, RAD)
            icon(ctx, em, 330, y, 220, p)
            pill(ctx, lab, 760, y, p, size=46, rgb=RAD)


# 22.4 "Today, her papers are kept in lead-lined boxes at the National Library of France."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.05, 0.05, 0.08), mid=(0.12, 0.12, 0.18))
    lead_box(ctx, W / 2, 720, 1.2, T, open_=0.0)
    pill(ctx, "NATIONAL LIBRARY · PARIS", W / 2, 1450, pop(lt, 2.8), size=44, rgb=STONE)


# 26.7 "If you want to read them, you have to sign a waiver and wear protective gear."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.05, 0.05, 0.08), mid=(0.12, 0.12, 0.18))
    ctx.save(); ctx.translate(W / 2, 640); ctx.rotate(-0.05)
    rrect(ctx, -300, -360, 600, 720, 14); fill(ctx, PAPER)
    text(ctx, "WAIVER", 0, -280, 70, INK, shadow=False)
    for k in range(6):
        ctx.rectangle(-230, -180 + k * 60, 460 if k % 2 else 360, 14); fill(ctx, (0.6, 0.57, 0.5))
    w = clamp((lt - 1.0) / 0.8)
    ctx.move_to(-200, 240)
    for j in range(int(30 * w)):
        ctx.line_to(-200 + j * 13, 240 + 25 * math.sin(j * 1.3))
    stroke(ctx, (0.1, 0.2, 0.6), 6)
    ctx.restore()
    icon(ctx, "🧤", 260, 1300, 200, pop(lt, 1.8))
    icon(ctx, "🥽", 820, 1300, 200, pop(lt, 2.1))


# 30.0 "And they'll stay radioactive for about another fifteen hundred years."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.02, 0.06, 0.04), mid=(0.04, 0.14, 0.08))
    notebook(ctx, W / 2, 620, 0.7, T, glow=1.0)
    pill(ctx, "YEAR " + counter(lt - 0.3, 2026, 3500, 2.6), W / 2, 1400, pop(lt, 0.2), size=80, rgb=RAD)


# 33.6 "Even her coffin is lined with lead."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.04, 0.04, 0.06), mid=(0.10, 0.10, 0.14))
    coffin(ctx, W / 2, 700, 1.0, 0.0, col=LEAD)
    pill(ctx, "LEAD-LINED", W / 2, 1450, pop(lt, 1.2), rgb=STONE)


# 35.6 "So be careful when you say you'd love to touch history,"
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.02, 0.06, 0.04), mid=(0.04, 0.14, 0.08))
    notebook(ctx, W / 2, 620, 0.8, T, glow=0.8)
    reach = ease(clamp(lt / 2.5))
    icon(ctx, "👆", W / 2 + 60, lerp(1700, 1150, reach), 260)
    stamp(ctx, "CAREFUL", W / 2, 260, (lt - 1.0) / 0.3, size=80, col=YELLOW)


# 38.6 "because" -> vuelve a e1
def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.94), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.9, e2), (4.5, e3), (7.5, e4), (10.4, e5), (12.3, e6), (14.1, e7), (16.4, e8),
           (19.5, e9), (22.4, e10), (26.7, e11), (30.0, e12), (33.6, e13), (35.6, e14), (38.6, e15)]
SFX = [(16.45, "ding"), (19.5, "pop"), (20.3, "pop"), (21.2, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_dark(ctx, T, top=(0.02, 0.06, 0.04), mid=(0.04, 0.14, 0.08), bot=(0.01, 0.03, 0.02))
    notebook(ctx, W / 2, 1120, 1.05, T, glow=1.3, rot=-0.06)
    ctx.restore()
    thumb_vignette(ctx, 0.55)
    thumb_text(ctx, ["DON'T TOUCH", ("THIS BOOK", WHITE)], y=260, size=180)
    thumb_arrow(ctx, 120, 1700, 330, 1350)
    badge(ctx, "FROM 1898", 790, 1760, 1.0, size=50)
