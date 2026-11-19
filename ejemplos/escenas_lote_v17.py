"""v17 (EN) FORMATO BUCLE: the inventor of the Pringles can is buried in one. (Sin logo ni mascota: lata genérica.)"""
from kit import *  # noqa

CAN_RED = (0.85, 0.12, 0.14)
CHIP = (0.98, 0.80, 0.35)


def chip(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 0.42); circle(ctx, 0, 0, 120); ctx.restore()
    ctx.set_source(vgrad(ctx, 0, -50, 0, 50, [(0, (1, 0.88, 0.5)), (1, (0.90, 0.65, 0.20))])); ctx.fill()
    ctx.move_to(-110, -5); ctx.curve_to(-40, 25, 40, 25, 110, -5); stroke(ctx, (0.8, 0.55, 0.15), 5, 0.7)
    ctx.restore()


def can(ctx, x, y, s=1.0, col=CAN_RED, lid=1.0, glow=0.0, label="CHIPS"):
    """Lata de tubo genérica (sin marca). (x, y) = centro."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if glow > 0:
        spotlight(ctx, 0, 0, 600, 0.35 * glow, GOLD)
    rrect(ctx, -150, -420, 300, 840, 30)
    g = cairo.LinearGradient(-150, 0, 150, 0)
    g.add_color_stop_rgb(0, col[0] * 0.6, col[1] * 0.6, col[2] * 0.6); g.add_color_stop_rgb(0.4, *col)
    g.add_color_stop_rgb(1, col[0] * 0.55, col[1] * 0.55, col[2] * 0.55)
    ctx.set_source(g); ctx.fill()
    rrect(ctx, -110, -300, 220, 90, 20); fill(ctx, WHITE, 0.9)
    text(ctx, label, 0, -255, 50, col, shadow=False)
    chip(ctx, 0, 40, 1.0)
    rrect(ctx, -158, 400, 316, 40, 12); fill(ctx, (0.75, 0.75, 0.8))
    if lid > 0:
        ctx.save(); ctx.translate(0, -420 - 200 * (1 - lid)); ctx.scale(1, 0.25)
        circle(ctx, 0, 0, 160); fill(ctx, (0.95, 0.95, 0.95)); ctx.restore()
    rrect(ctx, -110, -400, 30, 760, 15); fill(ctx, WHITE, 0.18)
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 900)
    cemetery(ctx, T, 1250)
    tombstone(ctx, W / 2, 900, 1.3, "")
    can(ctx, W / 2, 1060, 0.55, glow=1.0)
    ctx.restore(); ctx.save()
    ficha(ctx, "FREDRIC BAUR", "INVENTOR OF THE CAN · 1918–2008", W / 2, 1600, 1.0, "🧪", YELLOW)


# 0.0 "The man who invented the Pringles can is buried in one."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 3.1 "And it's real."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.25, 1.05), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.15, 0.04, 0.05), mid=(0.28, 0.06, 0.08))
    can(ctx, W / 2, 760, 0.95, glow=1.0)
    stamp(ctx, "REAL", 800, 360, lt / 0.25, size=90, col=YELLOW)


# 4.0 "His name was Fredric Baur, a chemist at Procter and Gamble."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_blueprint(ctx, T)
    gent(ctx, W / 2, 520, 0.9, col=(0.15, 0.20, 0.35), hat=False)
    icon(ctx, "🥼", W / 2, 900, 260, pop(lt, 0.3))
    ficha(ctx, "FREDRIC BAUR", "CHEMIST · PROCTER & GAMBLE", W / 2, 1450, pop(lt, 0.6), "🧪", YELLOW)


# 7.4 "He solved a big problem: chips breaking and going stale in the bag."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.10), mid=(0.14, 0.10, 0.20))
    ctx.move_to(250, 300); ctx.line_to(830, 300); ctx.line_to(870, 1200); ctx.line_to(210, 1200); ctx.close_path()
    fill(ctx, (0.75, 0.75, 0.82))
    for k in range(10):  # trozos rotos
        chip(ctx, 330 + (k % 4) * 140, 760 + (k // 4) * 140, 0.35, k * 0.9)
    stamp(ctx, "BROKEN", W / 2, 1400, (lt - 1.5) / 0.3, size=90)
    stamp(ctx, "STALE", W / 2, 1560, (lt - 2.8) / 0.3, size=70, col=STONE)


# 11.3 "So he stacked identical curved chips,"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.02), mid=(0.22, 0.14, 0.04))
    n = int(clamp(lt / 2.4) * 14)
    for k in range(n):
        chip(ctx, W / 2, 1300 - k * 45, 1.2)
    pill(ctx, "IDENTICAL", W / 2, 330, pop(lt, 1.2), rgb=GOLD)


# 14.1 "and designed that famous tube to hold them."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.02), mid=(0.22, 0.14, 0.04))
    for k in range(14):
        chip(ctx, W / 2, 1150 - k * 45, 1.0)
    p = ease(clamp(lt / 1.2))
    ctx.save(); ctx.rectangle(-500, -500, W + 1000, H + 1000); ctx.clip()
    can(ctx, W / 2, lerp(-400, 860, p), 0.95, lid=0.0)
    ctx.restore()
    pill(ctx, "THE TUBE", W / 2, 1500, pop(lt, 1.2), rgb=RED)


# 16.1 "He was so proud of it that he told his family one thing:"
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.08, 0.06, 0.02), mid=(0.20, 0.15, 0.05))
    rays(ctx, W / 2, 760, T, GOLD, 0.07)
    can(ctx, W / 2, 800, 0.85, glow=1.0)
    icon(ctx, "👑", W / 2, 330, 200, pop(lt, 0.4))


# 19.1 "when I die, put me in that can."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    gent(ctx, 300, 600, 0.8, col=(0.15, 0.20, 0.35), hat=False)
    can(ctx, 800, 900, 0.6)
    pill(ctx, '"PUT ME IN THAT CAN"', W / 2, 1450, pop(lt, 0.6), size=50, rgb=WHITE)


# 21.0 "In other words, he wanted to be buried in his own invention."  (2.º gancho)
def e9(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.20, 0.03, 0.05), mid=(0.10, 0.02, 0.04))
    rays(ctx, W / 2, 700, T, RED, 0.06)
    can(ctx, W / 2, 760, 0.95, glow=0.6)
    stamp(ctx, "HIS OWN INVENTION", W / 2, 1450, (lt - 1.6) / 0.3, size=64)


# 24.4 "In 2008, Baur died at eighty-nine."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 950)
    cemetery(ctx, T, 1500)
    tombstone(ctx, W / 2, 1250, 1.5, "F. BAUR")
    pill(ctx, "1918 – 2008", W / 2, 1700, pop(lt, 0.3), size=60, rgb=STONE)
    pill(ctx, "AGE 89", W / 2, 330, pop(lt, 1.2), size=60, rgb=GOLD)


# 26.8 "On the way to the funeral home, his kids stopped at a drugstore and bought a can."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    bg_night(ctx, T, grid=False)
    ground(ctx, 1350, (0.12, 0.12, 0.16))
    ctx.rectangle(140, 650, 800, 700); fill(ctx, (0.85, 0.85, 0.88))
    rrect(ctx, 180, 560, 720, 140, 16); fill(ctx, (0.15, 0.45, 0.80))
    text(ctx, "DRUGSTORE", W / 2, 630, 70, WHITE)
    rrect(ctx, 220, 760, 300, 360, 10); fill(ctx, (1, 0.95, 0.75), 0.9)
    rrect(ctx, 600, 760, 250, 590, 10); fill(ctx, (0.3, 0.5, 0.7), 0.8)
    can(ctx, 370, 1000, 0.25)
    icon(ctx, "🚗", lerp(-200, 300, ease(lt / 1.5)), 1450, 260)


# 30.6 "They even argued about the flavor, and went with the original."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.10), mid=(0.14, 0.10, 0.20))
    for k, col in enumerate(((0.15, 0.55, 0.25), CAN_RED, (0.20, 0.35, 0.80))):
        sel = k == 1 and lt > 2.0
        can(ctx, 240 + k * 300, 760 - (60 if sel else 0), 0.5, col=col, glow=1.0 if sel else 0.0, label="?" if not sel else "CHIPS")
    pill(ctx, "ORIGINAL", W / 2, 1450, pop(lt, 2.0), rgb=RED)


# 33.3 "Part of his ashes went inside, and it was buried with him in Ohio."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    cemetery(ctx, T, 1300)
    ctx.rectangle(W / 2 - 220, 1300, 440, 300); fill(ctx, (0.08, 0.05, 0.03))
    p = ease(clamp((lt - 0.4) / 1.8))
    can(ctx, W / 2, lerp(900, 1450, p), 0.4)
    pill(ctx, "OHIO", W / 2, 330, pop(lt, 2.2), rgb=GOLD)


# 36.8 "So next time you finish a can, remember:" -> vuelve a e1
def e14(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (3.1, e2), (4.0, e3), (7.4, e4), (11.3, e5), (14.1, e6), (16.1, e7), (19.1, e8),
           (21.0, e9), (24.4, e10), (26.8, e11), (30.6, e12), (33.3, e13), (36.8, e14)]
SFX = [(3.15, "pop"), (21.05, "ding"), (32.6, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1100)
    cemetery(ctx, T, 1450)
    tombstone(ctx, W / 2, 1100, 1.4, "")
    can(ctx, W / 2, 1270, 0.6, glow=1.3)
    ctx.restore()
    thumb_vignette(ctx, 0.55)
    thumb_text(ctx, ["WHAT'S IN", ("THIS CAN?", WHITE)], y=260, size=195)
    thumb_circle(ctx, W / 2, 1270, 160, 290)
    thumb_arrow(ctx, 110, 1700, 350, 1450)
