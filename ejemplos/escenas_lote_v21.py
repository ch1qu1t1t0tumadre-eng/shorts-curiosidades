"""v21 (EN) FORMATO BUCLE: Napoleon was not short (French inches + British propaganda)."""
from kit import *  # noqa

BLUE = (0.12, 0.18, 0.45)


def napoleon(ctx, x, y, s=1.0, col=BLUE, a=1.0):
    """Silueta genérica con bicornio y casaca (sin rasgos). (x, y) = centro de la cabeza."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -150, 120, 300, 520, 110); fill(ctx, col, a)
    rrect(ctx, -150, 520, 300, 120, 30); fill(ctx, (0.92, 0.92, 0.90), a)  # pantalón
    circle(ctx, 0, 0, 100); fill(ctx, (0.85, 0.70, 0.58), a)
    ctx.move_to(-230, -40); ctx.curve_to(-120, -230, 120, -230, 230, -40); ctx.curve_to(100, -90, -100, -90, -230, -40)
    fill(ctx, (0.06, 0.06, 0.08), a)  # bicornio
    circle(ctx, 0, -95, 22); fill(ctx, RED, a)
    for k in range(4):
        circle(ctx, 0, 220 + k * 70, 10); fill(ctx, GOLD, a)
    ctx.restore()


def ruler(ctx, x, y0, y1, unit_px, label_every=1, labels=None, col=WHITE):
    ctx.move_to(x, y0); ctx.line_to(x, y1); stroke(ctx, col, 6, 0.8)
    n = int((y0 - y1) / unit_px)
    for k in range(n + 1):
        yy = y0 - k * unit_px
        ctx.move_to(x, yy); ctx.line_to(x + (50 if k % 12 == 0 else 22), yy); stroke(ctx, col, 4, 0.7)


def cartoon_frame(ctx, x, y, s, T):
    """Viñeta de periódico antiguo con una figura diminuta enfadada (genérica)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -380, -460, 760, 920, 10); fill(ctx, (0.93, 0.88, 0.74))
    rrect(ctx, -350, -430, 700, 860, 6); stroke(ctx, INK, 6)
    jump = abs(math.sin(T * 8)) * 30
    napoleon(ctx, 0, 160 - jump, 0.45, col=(0.55, 0.20, 0.20))
    for k in range(3):
        ctx.move_to(-120 + k * 120, -40 - jump); ctx.line_to(-140 + k * 120, -120 - jump); stroke(ctx, INK, 5)
    text(ctx, '"LITTLE BONEY"', 0, 380, 46, INK, shadow=False)
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 880)
    bg_dark(ctx, T, top=(0.05, 0.06, 0.16), mid=(0.12, 0.14, 0.32))
    spotlight(ctx, W / 2, 700, 700, 0.3, (1, 0.9, 0.7))
    ruler(ctx, 880, 1450, 350, 16.5)
    napoleon(ctx, W / 2 - 60, 430, 1.05)
    ctx.restore(); ctx.save()
    ficha(ctx, "NAPOLEON", "EMPEROR OF FRANCE · 1769–1821", W / 2, 1600, 1.0, "🇫🇷", YELLOW)


# 0.0 "Napoleon was not short."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 1.9 "That's a lie that's more than two hundred years old."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (0.3, 1.05), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.15, 0.04, 0.05), mid=(0.28, 0.06, 0.08))
    stamp(ctx, "LIE", W / 2, 640, lt / 0.25, size=220)
    pill(ctx, "200+ YEARS OLD", W / 2, 1450, pop(lt, 1.2), size=56, rgb=GOLD)


# 4.2 "When Napoleon died, French doctors measured him at five feet two."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.06, 0.06, 0.08), mid=(0.14, 0.14, 0.18))
    rrect(ctx, 140, 380, 800, 620, 14); fill(ctx, PAPER)
    text(ctx, "1821", W / 2, 470, 60, INK, shadow=False)
    text(ctx, "5 PIEDS 2 POUCES", W / 2, 640, 66, INK, shadow=False)
    for k in range(4):
        ctx.rectangle(220, 740 + k * 50, 640 if k % 2 else 480, 12); fill(ctx, (0.6, 0.57, 0.5))
    pill(ctx, "5'2\"", W / 2, 1450, pop(lt, 2.6), size=90, rgb=RED)


# 7.9 "But those were French inches, and French inches were longer than English ones."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_blueprint(ctx, T)
    for k, (lab, w, col) in enumerate((("FRENCH INCH", 760 * 1.066, GOLD), ("ENGLISH INCH", 760, RED))):
        y = 520 + k * 330
        p = ease(clamp((lt - 0.3) / 0.8))
        rrect(ctx, 140, y, w * p * 0.95, 110, 20); fill(ctx, col)
        text(ctx, lab, 160, y - 40, 44, WHITE, align="left")
    pill(ctx, "LONGER", W / 2, 1450, pop(lt, 2.2), size=60, rgb=GOLD)


# 11.9 "Converted, he was about five foot seven. That was average for a Frenchman back then."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.05, 0.06, 0.16), mid=(0.12, 0.14, 0.32))
    for k, xx in enumerate((220, 860)):
        gent(ctx, xx, 560, 0.85, col=(0.25, 0.25, 0.35), hat=False)
    napoleon(ctx, W / 2, 560, 0.88)
    pill(ctx, "5'7\" (170 cm)", W / 2, 300, pop(lt, 0.8), size=70, rgb=GREEN)
    pill(ctx, "AVERAGE", W / 2, 1600, pop(lt, 2.0), size=60, rgb=TEAL)


# 15.9 "So where did the myth come from? British cartoonists."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.14, 0.08))
    icon(ctx, "🖋️", W / 2, 640, 340, pop(lt, 1.4))
    pill(ctx, "BRITISH CARTOONISTS", W / 2, 1450, pop(lt, 1.6), size=50, rgb=RED)


# 18.6 "During the wars, an artist named James Gillray drew him as a tiny, screaming man throwing tantrums."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.14, 0.08))
    cartoon_frame(ctx, W / 2, 700, 0.9, T)
    ficha(ctx, "JAMES GILLRAY", "BRITISH CARTOONIST · 1756–1815", W / 2, 1600, pop(lt, 0.4), "🖋️", YELLOW)


# 24.4 "They called him Little Boney."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.14, 0.08))
    cartoon_frame(ctx, W / 2, 760, 1.05, T)


# 26.1 "In other words, the most famous fact about Napoleon is enemy propaganda."  (2.º gancho)
def e9(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.20, 0.03, 0.05), mid=(0.10, 0.02, 0.04))
    rays(ctx, W / 2, 700, T, RED, 0.06)
    icon(ctx, "📢", W / 2, 680, 380, pop(lt, 0.0))
    stamp(ctx, "PROPAGANDA", W / 2, 1420, (lt - 2.6) / 0.3, size=90)


# 30.4 "And it worked so well that two centuries later,"
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    pill(ctx, counter(lt, 1803, 2026, 1.6), W / 2, 700, pop(lt, 0.0), size=150, rgb=GOLD)


# 33.0 "we still call short, angry men Napoleons."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.10), mid=(0.14, 0.10, 0.20))
    character(ctx, W / 2, 640, 0.9, T, mood="sorpresa", body=True)
    pill(ctx, '"NAPOLEON COMPLEX"', W / 2, 300, pop(lt, 1.2), size=50, rgb=RED)


# 35.7 "So the next time someone makes fun of a short guy, tell them:" -> vuelve a e1
def e12(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (1.9, e2), (4.2, e3), (7.9, e4), (11.9, e5), (15.9, e6), (18.6, e7), (24.4, e8),
           (26.1, e9), (30.4, e10), (33.0, e11), (35.7, e12)]
SFX = [(1.95, "pop"), (26.15, "ding"), (28.9, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_dark(ctx, T, top=(0.05, 0.06, 0.16), mid=(0.12, 0.14, 0.32))
    spotlight(ctx, W / 2, 1000, 800, 0.3, (1, 0.9, 0.7))
    ruler(ctx, 900, 1800, 600, 16.5)
    napoleon(ctx, W / 2 - 60, 800, 1.1)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["HOW TALL", ("WAS HE?", WHITE)], y=260, size=200)
    thumb_circle(ctx, 900, 820, 110, 200)
