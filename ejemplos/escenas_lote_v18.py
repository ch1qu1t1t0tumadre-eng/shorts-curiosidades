"""v18 (EN) FORMATO BUCLE: Mark Twain predicted the year he would die (Halley's Comet 1835/1910)."""
from kit import *  # noqa

ICE = (0.70, 0.90, 1.0)


def starfield(ctx, T, top=(0.01, 0.02, 0.08), bot=(0.08, 0.06, 0.22)):
    ctx.set_source(vgrad(ctx, 0, -500, 0, H + 500, [(0, top), (1, bot)])); ctx.paint()
    rng = np.random.default_rng(21)
    for _ in range(150):
        x, y, r = rng.uniform(-300, W + 300), rng.uniform(-500, H + 500), rng.uniform(1.5, 4.5)
        circle(ctx, x, y, r); fill(ctx, WHITE, 0.4 + 0.4 * math.sin(T * 2 + x))


def comet(ctx, x, y, s=1.0, ang=2.5, T=0.0):
    """Cometa: núcleo brillante + cola larga en dirección 'ang' (radianes)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(6):
        L = 700 - k * 80
        w = 90 - k * 12
        ctx.save(); ctx.rotate(ang)
        ctx.move_to(0, -w * 0.5); ctx.curve_to(L * 0.5, -w, L, -w * 0.2 + math.sin(T * 3 + k) * 10, L, 0)
        ctx.curve_to(L, w * 0.2, L * 0.5, w, 0, w * 0.5); ctx.close_path()
        fill(ctx, ICE, 0.10 + 0.05 * k); ctx.restore()
    spotlight(ctx, 0, 0, 160, 0.9, ICE)
    circle(ctx, 0, 0, 34); fill(ctx, WHITE)
    ctx.restore()


def sun(ctx, x, y, r, T):
    spotlight(ctx, x, y, r * 2.4, 0.5, (1, 0.8, 0.3))
    circle(ctx, x, y, r); fill(ctx, (1, 0.85, 0.35))


def calendar(ctx, x, y, s, month, day, year):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -200, 460, 420, 24); fill(ctx, WHITE)
    rrect(ctx, -230, -200, 460, 100, 24); fill(ctx, RED)
    text(ctx, month, 0, -150, 50, WHITE, shadow=False)
    text(ctx, str(day), 0, 20, 150, INK, shadow=False)
    text(ctx, str(year), 0, 160, 46, (0.4, 0.4, 0.45), shadow=False)
    ctx.restore()


def book(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -260, -170, 520, 340, 14); fill(ctx, (0.45, 0.18, 0.12))
    rrect(ctx, -240, -150, 480, 300, 10); fill(ctx, (0.94, 0.90, 0.78))
    ctx.move_to(0, -150); ctx.line_to(0, 150); stroke(ctx, (0.6, 0.5, 0.4), 4)
    for k in range(6):
        ctx.rectangle(-210, -110 + k * 40, 170, 10); fill(ctx, (0.6, 0.57, 0.5))
        ctx.rectangle(40, -110 + k * 40, 170, 10); fill(ctx, (0.6, 0.57, 0.5))
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 880)
    starfield(ctx, T)
    comet(ctx, 380, 560, 1.0, -0.5 + math.pi, T)
    book(ctx, W / 2, 1180, 0.9, T)
    ctx.restore(); ctx.save()
    ficha(ctx, "MARK TWAIN", "AUTHOR · 1835–1910", W / 2, 1600, 1.0, "📚", YELLOW)


# 0.0 "Mark Twain predicted the year he would die."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 2.9 "And he was right."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.25, 1.05), (dur, 1.1)]), W / 2, 880)
    starfield(ctx, T)
    comet(ctx, W / 2 - 100, 600, 1.1, -0.5 + math.pi, T)
    stamp(ctx, "RIGHT", W / 2, 1400, lt / 0.25, size=110, col=GREEN)


# 3.9 "Twain was born in 1835,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    icon(ctx, "👶", W / 2, 660, 360, pop(lt, 0.0))
    pill(ctx, counter(lt - 0.3, 1800, 1835, 0.9), W / 2, 1350, pop(lt, 0.2), size=90, rgb=GOLD)


# 6.2 "just weeks after Halley's Comet swung past the Sun."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.0)]), W / 2, 900)
    starfield(ctx, T)
    sun(ctx, W / 2, 800, 150, T)
    a = -1.4 + 2.4 * ease(clamp(lt / 2.6))
    cx, cy = W / 2 + math.cos(a) * 380, 800 + math.sin(a) * 520
    comet(ctx, cx, cy, 0.6, a, T)
    pill(ctx, "HALLEY'S COMET", W / 2, 300, pop(lt, 0.8), rgb=TEAL)


# 9.2 "That comet only comes back about every seventy-six years."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 900)
    starfield(ctx, T)
    ctx.save(); ctx.translate(W / 2, 760); ctx.scale(1, 1.9); circle(ctx, 0, 0, 260); ctx.restore()
    stroke(ctx, WHITE, 4, 0.4)
    sun(ctx, W / 2, 420, 60, T)
    a = T * 1.2
    comet(ctx, W / 2 + math.cos(a) * 260, 760 + math.sin(a) * 494, 0.4, a + math.pi, T)
    pill(ctx, "EVERY 76 YEARS", W / 2, 1450, pop(lt, 1.6), size=60, rgb=GOLD)


# 12.6 "So in 1909, Twain wrote:"
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.14, 0.08))
    spotlight(ctx, W / 2, 700, 600, 0.3, (1, 0.85, 0.6))
    book(ctx, W / 2, 760, 1.4, T)
    icon(ctx, "🖋️", 760, 520, 180, pop(lt, 0.3))
    pill(ctx, "1909", W / 2, 1450, pop(lt, 0.2), size=80, rgb=GOLD)


# 14.8 "I came in with Halley's Comet. It is coming again next year, and I expect to go out with it."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.14, 0.08))
    rrect(ctx, 90, 200, 900, 760, 24); fill(ctx, PAPER)
    text(ctx, "“", 170, 290, 160, (0.6, 0.5, 0.4), shadow=False)
    lines = [("I CAME IN WITH", 0.0), ("HALLEY'S COMET.", 0.6), ("IT IS COMING AGAIN", 1.7), ("NEXT YEAR,", 2.4),
             ("AND I EXPECT TO", 3.4), ("GO OUT WITH IT.", 4.1)]
    for k, (ln, t0) in enumerate(lines):
        a = clamp((lt - t0) / 0.3)
        text(ctx, ln, W / 2, 330 + k * 95, 56, INK, a=a, shadow=False)
    text(ctx, "— MARK TWAIN, 1909", W / 2, 910, 40, (0.45, 0.4, 0.35), a=clamp((lt - 4.5) / 0.3), shadow=False)


# 19.9 "In other words, he bet his life on a comet."  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    starfield(ctx, T, top=(0.10, 0.02, 0.10), bot=(0.20, 0.04, 0.20))
    rays(ctx, W / 2, 700, T, ICE, 0.05)
    comet(ctx, W / 2 + 120, 640, 1.2, -0.4 + math.pi, T)
    icon(ctx, "🎲", 300, 1000, 220, pop(lt, 0.3))
    stamp(ctx, "BET HIS LIFE", W / 2, 1420, (lt - 0.8) / 0.3, size=80)


# 22.9 "The next spring, the comet returned."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    starfield(ctx, T)
    p = ease(clamp(lt / 1.8))
    comet(ctx, lerp(1250, 420, p), lerp(200, 700, p), 1.0, math.pi * 0.85 - math.pi, T)
    ctx.move_to(-100, 1500); ctx.curve_to(300, 1380, 700, 1420, 1200, 1500); ctx.line_to(1200, 2200); ctx.line_to(-100, 2200)
    fill(ctx, (0.04, 0.05, 0.10))
    pill(ctx, "1910", W / 2, 1650, pop(lt, 0.4), size=80, rgb=GOLD)


# 24.9 "It reached its closest point to the Sun on April twentieth, 1910."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    starfield(ctx, T)
    sun(ctx, 300, 420, 110, T)
    comet(ctx, 520, 520, 0.55, 0.2, T)
    calendar(ctx, W / 2, 1150, 1.1, "APRIL", 20, 1910)


# 28.9 "And the very next day, Mark Twain died of a heart attack."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.04, 0.03, 0.06), mid=(0.10, 0.07, 0.12))
    day = 20 if lt < 0.6 else 21
    calendar(ctx, W / 2, 700, 1.2, "APRIL", day, 1910)
    icon(ctx, "🕯️", W / 2, 1300, 220, pop(lt, 1.2))


# 32.0 "He came in with the comet, and he went out with it."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 900)
    starfield(ctx, T)
    ctx.move_to(160, 900); ctx.line_to(920, 900); stroke(ctx, WHITE, 8, 0.6)
    comet(ctx, 180, 760, 0.5, -0.6 + math.pi, T)
    comet(ctx, 900, 760, 0.5, -0.6 + math.pi, T) if lt > 1.2 else None
    pill(ctx, "1835", 180, 1020, pop(lt, 0.0), size=60, rgb=GOLD)
    pill(ctx, "1910", 900, 1020, pop(lt, 1.2), size=60, rgb=GOLD)
    arrow(ctx, 280, 1180, 800, 1180, ease((lt - 0.3) / 1.0), YELLOW, 8)


# 34.6 "Its next visit is in 2061."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    starfield(ctx, T)
    icon(ctx, "🔭", 300, 1200, 300, pop(lt, 0.0))
    comet(ctx, 760, 520, 0.7, -0.5 + math.pi, T)
    pill(ctx, counter(lt - 0.6, 2026, 2061, 1.2), W / 2, 1550, pop(lt, 0.5), size=90, rgb=TEAL)


# 36.9 "So if you ever see it in the sky, just remember that" -> vuelve a e1
def e14(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.9, e2), (3.9, e3), (6.2, e4), (9.2, e5), (12.6, e6), (14.8, e7), (19.9, e8),
           (22.9, e9), (24.9, e10), (28.9, e11), (32.0, e12), (34.6, e13), (36.9, e14)]
SFX = [(2.95, "pop"), (19.95, "ding"), (29.5, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    starfield(ctx, T)
    comet(ctx, 620, 1050, 1.6, -0.5 + math.pi, T)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["THIS COMET", ("KNEW", WHITE)], y=260, size=200)
    thumb_text(ctx, ["WHEN HE'D DIE"], y=1700, size=130, rot=0.03)
    thumb_circle(ctx, 620, 1050, 150, 150)
