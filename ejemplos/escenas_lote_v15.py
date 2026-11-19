"""v15 (EN) FORMATO BUCLE: Teddy Roosevelt was shot in the chest (1912) and still gave his speech."""
from kit import *  # noqa

SUIT = (0.08, 0.08, 0.12)


def speech_stack(ctx, x, y, s=1.0, hole=0.0, T=0.0):
    """Discurso de 50 páginas doblado; hole 0..1 = agujero de bala."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(9, -1, -1):
        rrect(ctx, -260 + k * 3, -340 + k * 6, 520, 620, 10); fill(ctx, PAPER if k % 2 else (0.88, 0.85, 0.75))
    text(ctx, "SPEECH", 0, -240, 60, INK, shadow=False)
    text(ctx, "50 PAGES", 0, -170, 34, (0.45, 0.4, 0.35), shadow=False)
    for k in range(7):
        ctx.rectangle(-200, -90 + k * 50, 400 if k % 3 else 260, 14); fill(ctx, (0.6, 0.57, 0.5))
    ctx.move_to(-270, 0); ctx.line_to(280, 0); stroke(ctx, (0.6, 0.55, 0.45), 4, 0.6)
    if hole > 0:
        circle(ctx, 60, 60, 26 * hole); fill(ctx, (0.05, 0.03, 0.02))
        for k in range(8):
            a = k * math.pi / 4
            ctx.move_to(60 + math.cos(a) * 26 * hole, 60 + math.sin(a) * 26 * hole)
            ctx.line_to(60 + math.cos(a + 0.2) * 48 * hole, 60 + math.sin(a + 0.2) * 48 * hole)
            stroke(ctx, (0.25, 0.2, 0.15), 4)
    ctx.restore()


def glasses_case(ctx, x, y, s=1.0, hole=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -80, 460, 160, 80)
    ctx.set_source(vgrad(ctx, 0, -80, 0, 80, [(0, (0.80, 0.82, 0.88)), (1, (0.45, 0.48, 0.55))])); ctx.fill()
    rrect(ctx, -200, -60, 120, 30, 15); fill(ctx, WHITE, 0.5)
    if hole > 0:
        circle(ctx, 40, 0, 24 * hole); fill(ctx, (0.08, 0.08, 0.1))
    ctx.restore()


def podium(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-200, 0); ctx.line_to(200, 0); ctx.line_to(160, 420); ctx.line_to(-160, 420); ctx.close_path()
    fill(ctx, WOOD)
    rrect(ctx, -230, -30, 460, 50, 10); fill(ctx, WOOD_D)
    rrect(ctx, -60, 120, 120, 120, 60); fill(ctx, GOLD)
    ctx.move_to(0, -30); ctx.line_to(0, -240); stroke(ctx, (0.3, 0.3, 0.35), 10)
    rrect(ctx, -40, -330, 80, 110, 40); fill(ctx, (0.25, 0.25, 0.28))
    ctx.restore()


def old_car(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -400, -120, 800, 160, 40); fill(ctx, (0.12, 0.12, 0.16))
    rrect(ctx, -380, -230, 260, 130, 20); fill(ctx, (0.12, 0.12, 0.16))
    for wx in (-260, 260):
        circle(ctx, wx, 60, 100); fill(ctx, (0.05, 0.05, 0.06)); circle(ctx, wx, 60, 40); fill(ctx, (0.6, 0.6, 0.65))
    circle(ctx, 380, -60, 30); fill(ctx, (1, 0.9, 0.6))
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 880)
    bg_dark(ctx, T, top=(0.06, 0.04, 0.10), mid=(0.16, 0.10, 0.22))
    spotlight(ctx, W / 2, 700, 750, 0.35, (1, 0.9, 0.7))
    speech_stack(ctx, W / 2, 760, 1.05, hole=1.0, T=T)
    ctx.restore(); ctx.save()
    ficha(ctx, "TEDDY ROOSEVELT", "26TH U.S. PRESIDENT · 1858–1919", W / 2, 1560, 1.0, "🐻", YELLOW)


# 0.0 "Teddy Roosevelt was shot in the chest."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 2.5 "And then he gave a speech for almost ninety minutes."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    podium(ctx, W / 2, 700, 1.0)
    pill(ctx, counter(lt - 0.6, 0, 90, 1.8) + " MIN", W / 2, 330, pop(lt, 0.4), size=80, rgb=GOLD)


# 5.4 "October 1912, Milwaukee."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    rrect(ctx, W / 2 - 230, 380, 460, 380, 24); fill(ctx, WHITE)
    rrect(ctx, W / 2 - 230, 380, 460, 100, 24); fill(ctx, RED)
    text(ctx, "OCTOBER", W / 2, 430, 50, WHITE, shadow=False)
    text(ctx, "1912", W / 2, 620, 130, INK, shadow=False)
    pill(ctx, "MILWAUKEE", W / 2, 1450, pop(lt, 1.3), rgb=TEAL)


# 7.4 "Roosevelt was running for president again."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.05, 0.08, 0.20), mid=(0.12, 0.10, 0.30))
    icon(ctx, "🗳️", W / 2, 640, 380, pop(lt, 0.0))
    pill(ctx, "3RD TERM?", W / 2, 1450, pop(lt, 0.8), rgb=RED)


# 9.4 "As he stood up in his car to wave to the crowd,"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 950)
    bg_night(ctx, T, grid=False)
    ground(ctx, 1350, (0.10, 0.10, 0.16))
    gent(ctx, W / 2 + 60, 650, 0.75, col=SUIT)
    ctx.save(); ctx.translate(W / 2 + 160, 800); ctx.rotate(-2.6 + 0.25 * math.sin(T * 6))
    rrect(ctx, -25, 0, 50, 260, 25); fill(ctx, SUIT); ctx.restore()
    old_car(ctx, W / 2, 1250, 1.0)
    for k in range(9):
        circle(ctx, k * 130, 1560, 60); fill(ctx, (0.05, 0.05, 0.08))


# 11.9 "a man fired a revolver at him, from about five feet away."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.12, 0.04, 0.04), mid=(0.25, 0.06, 0.06))
    gent(ctx, 220, 600, 0.8, col=(0.06, 0.04, 0.06), hat=False)
    gent(ctx, 860, 600, 0.8, col=SUIT)
    arrow(ctx, 360, 1250, 720, 1250, ease((lt - 0.4) / 0.8), WHITE, 8)
    arrow(ctx, 720, 1250, 360, 1250, ease((lt - 0.4) / 0.8), WHITE, 8)
    pill(ctx, "5 FEET", W / 2, 1360, pop(lt, 2.4), size=70, rgb=GOLD)
    if 1.0 < lt < 1.25:
        ctx.rectangle(-500, -500, W + 1000, H + 1000); fill(ctx, WHITE, 0.5)


# 15.2 "The bullet hit him right in the chest."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.25)]), W / 2, keyframes(lt, [(0, 900), (dur, 760)]))
    bg_dark(ctx, T, top=(0.12, 0.04, 0.04), mid=(0.25, 0.06, 0.06))
    gent(ctx, W / 2, 420, 1.2, col=SUIT)
    k = pop(lt, 1.3)
    if k > 0:
        circle(ctx, W / 2 + 70, 780, 70 * k); stroke(ctx, RED, 10)
        ctx.move_to(W / 2 + 70 - 100 * k, 780); ctx.line_to(W / 2 + 70 + 100 * k, 780)
        ctx.move_to(W / 2 + 70, 780 - 100 * k); ctx.line_to(W / 2 + 70, 780 + 100 * k); stroke(ctx, RED, 6)


# 17.2 "In other words, he was shot almost point-blank."  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.20, 0.03, 0.05), mid=(0.10, 0.02, 0.04))
    rays(ctx, W / 2, 700, T, RED, 0.06)
    icon(ctx, "💥", W / 2, 680, 420, pop(lt, 0.0))
    stamp(ctx, "POINT-BLANK", W / 2, 1420, (lt - 1.6) / 0.3, size=80)


# 20.0 "But in his pocket was a fifty-page speech, folded in half."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (0.4, 1.0), (dur, 1.06)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.06, 0.04, 0.10), mid=(0.16, 0.10, 0.22))
    speech_stack(ctx, W / 2, 760, 1.0)
    pill(ctx, "FOLDED IN HALF", W / 2, 1450, pop(lt, 2.6), rgb=GOLD)


# 23.7 "And a steel glasses case."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.06, 0.06, 0.10), mid=(0.14, 0.14, 0.22))
    spotlight(ctx, W / 2, 700, 500, 0.35)
    glasses_case(ctx, W / 2, 700, 1.4)
    icon(ctx, "👓", W / 2, 420, 200, pop(lt, 0.3))
    pill(ctx, "STEEL", W / 2, 1450, pop(lt, 0.6), rgb=STONE)


# 25.5 "The bullet punched through both, and stopped near his rib."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.06, 0.04, 0.10), mid=(0.16, 0.10, 0.22))
    speech_stack(ctx, W / 2 - 120, 620, 0.7, hole=pop(lt, 0.3))
    glasses_case(ctx, W / 2 + 180, 1000, 0.8, hole=pop(lt, 0.7))
    stamp(ctx, "STOPPED", W / 2, 1420, (lt - 1.9) / 0.3, size=90, col=GREEN)


# 28.4 "Roosevelt coughed, saw no blood in his mouth, and decided he was fine."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    gent(ctx, W / 2, 480, 1.0, col=SUIT)
    icon(ctx, "👍", 820, 780, 220, pop(lt, 2.6))
    pill(ctx, '"I\'M FINE"', W / 2, 1450, pop(lt, 2.8), size=60, rgb=WHITE)


# 32.3 "He walked on stage and told the crowd: it takes more than that to kill a Bull Moose."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    bg_dark(ctx, T, top=(0.05, 0.03, 0.08), mid=(0.12, 0.06, 0.16))
    spotlight(ctx, W / 2, 500, 700, 0.4, (1, 0.9, 0.7))
    gent(ctx, W / 2, 360, 0.75, col=SUIT)
    podium(ctx, W / 2, 760, 1.0)
    for k in range(10):
        circle(ctx, k * 120, 1620, 70); fill(ctx, (0.03, 0.03, 0.06))
    pill(ctx, '"IT TAKES MORE THAN THAT"', W / 2, 1420, pop(lt, 2.0), size=40, rgb=GOLD)


# 36.7 "He carried that bullet in his chest for the rest of his life."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.02, 0.06, 0.10)), (1, (0.05, 0.15, 0.22))])); ctx.paint()
    gent(ctx, W / 2, 420, 1.2, col=(0.35, 0.65, 0.80), hat=False, a=0.35)
    for k in range(5):  # costillas estilo rayos X
        ctx.move_to(W / 2 - 150, 700 + k * 60); ctx.curve_to(W / 2 - 60, 680 + k * 60, W / 2 + 60, 680 + k * 60, W / 2 + 150, 700 + k * 60)
        stroke(ctx, (0.75, 0.95, 1.0), 10, 0.6)
    rrect(ctx, W / 2 + 70, 760, 24, 44, 12); fill(ctx, WHITE)
    thumb_circle(ctx, W / 2 + 82, 782, 70, 70) if lt > 0.6 else None
    pill(ctx, counter(lt - 0.5, 1912, 1919, 1.4), W / 2, 1450, pop(lt, 0.4), size=70, rgb=GOLD)


# 40.0 "Because" -> vuelve a e1
def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.92), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.5, e2), (5.4, e3), (7.4, e4), (9.4, e5), (11.9, e6), (15.2, e7), (17.2, e8),
           (20.0, e9), (23.7, e10), (25.5, e11), (28.4, e12), (32.3, e13), (36.7, e14), (40.0, e15)]
SFX = [(17.25, "ding"), (25.8, "pop"), (26.2, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_dark(ctx, T, top=(0.06, 0.04, 0.10), mid=(0.16, 0.10, 0.22))
    spotlight(ctx, W / 2, 1100, 800, 0.35, (1, 0.9, 0.7))
    speech_stack(ctx, W / 2, 1130, 1.15, hole=1.0)
    ctx.restore()
    thumb_vignette(ctx, 0.55)
    thumb_text(ctx, ["WHO SHOT", ("THIS SPEECH?", WHITE)], y=260, size=185)
    thumb_circle(ctx, W / 2 + 70, 1200, 120, 120)
    thumb_arrow(ctx, 120, 1700, 420, 1300)
