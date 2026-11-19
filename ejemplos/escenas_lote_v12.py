"""v12 (EN) FORMATO BUCLE: Alfred Nobel read his own obituary (1888, 'the merchant of death is dead')."""
from kit import *  # noqa

HEAD = "ALFRED NOBEL\nIS DEAD"


def medal(ctx, x, y, s=1.0, T=0.0, label="NOBEL PRIZE"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-120, -420); ctx.line_to(-30, -150); ctx.line_to(30, -150); ctx.line_to(120, -420); ctx.close_path()
    fill(ctx, (0.15, 0.30, 0.70))
    spotlight(ctx, 0, 0, 380, 0.45, GOLD)
    circle(ctx, 0, 0, 240)
    ctx.set_source(vgrad(ctx, 0, -240, 0, 240, [(0, (1, 0.88, 0.45)), (1, (0.75, 0.52, 0.15))])); ctx.fill()
    circle(ctx, 0, 0, 200); stroke(ctx, (0.65, 0.45, 0.12), 8)
    text(ctx, label, 0, 0, 44, (0.45, 0.28, 0.05), shadow=False)
    ctx.arc(-80, -80, 60, 3.3, 4.4); stroke(ctx, WHITE, 14, 0.5)
    ctx.restore()


def scroll_will(ctx, x, y, s, T, write=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -300, -420, 600, 840, 20); fill(ctx, PAPER)
    rrect(ctx, -330, -460, 660, 70, 35); fill(ctx, (0.85, 0.80, 0.65))
    rrect(ctx, -330, 400, 660, 70, 35); fill(ctx, (0.85, 0.80, 0.65))
    text(ctx, "LAST WILL", 0, -330, 64, INK, shadow=False)
    n = int(10 * clamp(write))
    for k in range(n):
        ctx.rectangle(-240, -230 + k * 58, 480 if k % 4 != 3 else 280, 14); fill(ctx, (0.45, 0.40, 0.35))
    if 0 < write < 1:
        icon(ctx, "✒️", -240 + 480 * (write * 10 % 1), -230 + n * 58 - 40, 120)
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 860)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.05), mid=(0.22, 0.14, 0.10), bot=(0.05, 0.03, 0.02))
    spotlight(ctx, W / 2, 700, 800, 0.30, (1, 0.9, 0.7))
    newspaper(ctx, W / 2, 760, 0.95, HEAD, "PARIS, 1888", rot=-0.05)
    ctx.restore(); ctx.save()
    ficha(ctx, "ALFRED NOBEL", "INVENTOR OF DYNAMITE · 1833–1896", W / 2, 1560, 1.0, "🧨", YELLOW)


# 0.0 "Alfred Nobel read his own obituary."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 2.8 "Eight years before he died."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    icon(ctx, "⏳", W / 2, 640, 340, pop(lt, 0.0))
    pill(ctx, counter(lt, 1888, 1896, 1.2), W / 2, 1300, pop(lt, 0.1), size=90, rgb=GOLD)
    pill(ctx, "8 YEARS EARLY", W / 2, 1450, pop(lt, 0.6), size=44, rgb=RED)


# 4.3 "In 1888, his brother Ludvig died in France."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    cemetery(ctx, T, 1500)
    tombstone(ctx, W / 2, 1290, 1.4, "LUDVIG", 1.0)
    pill(ctx, "BROTHER · 1831–1888", W / 2, 1660, pop(lt, 0.4), size=40, rgb=STONE)
    pill(ctx, "CANNES, FRANCE", W / 2, 330, pop(lt, 1.4), rgb=TEAL)


# 7.3 "But a French newspaper got the wrong Nobel."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 900)
    bg_blueprint(ctx, T)
    gent(ctx, 300, 560, 0.75, col=(0.20, 0.22, 0.35))
    gent(ctx, 780, 560, 0.75, col=(0.20, 0.22, 0.35))
    pill(ctx, "LUDVIG", 300, 1120, 1.0, rgb=STONE)
    pill(ctx, "ALFRED", 780, 1120, 1.0, rgb=GOLD)
    icon(ctx, "✝️", 300, 330, 110, pop(lt, 0.2))
    arrow(ctx, 540, 1400, 760, 1200, ease((lt - 0.8) / 0.5), RED, 14)
    stamp(ctx, "WRONG ONE", 540, 1500, (lt - 1.2) / 0.3, size=70)


# 9.7 "It reported that Alfred, the inventor of dynamite, was dead."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.15, 0.05, 0.03), mid=(0.30, 0.10, 0.05))
    rays(ctx, W / 2, 650, T, (1, 0.6, 0.2), 0.06)
    icon(ctx, "🧨", W / 2, 650, 380, pop(lt, 0.0))
    stamp(ctx, "DEAD?", W / 2, 1380, (lt - 2.4) / 0.3, size=110)


# 12.9 "And the headline was brutal: The merchant of death is dead."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.3)]), W / 2, keyframes(lt, [(0, 860), (dur, 700)]))
    bg_dark(ctx, T, top=(0.10, 0.06, 0.05), mid=(0.22, 0.14, 0.10))
    newspaper(ctx, W / 2, 760, 1.05, "THE MERCHANT\nOF DEATH\nIS DEAD", "LE MARCHAND DE LA MORT EST MORT", rot=0.03)


# 16.4 "In other words, a newspaper celebrated his death."  (2.º gancho)
def e7(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.20, 0.03, 0.05), mid=(0.10, 0.02, 0.04))
    rays(ctx, W / 2, 700, T, RED, 0.06)
    newspaper(ctx, W / 2, 720, 0.8, HEAD, rot=-0.08)
    for k in range(10):
        a = k * 0.63 + T
        rrect(ctx, W / 2 + math.cos(a) * 470, 700 + math.sin(a * 1.3) * 650, 26, 46, 6)
        fill(ctx, [GOLD, RED, TEAL][k % 3], 0.9)
    stamp(ctx, "CELEBRATED", W / 2, 1420, (lt - 1.2) / 0.3, size=80)


# 19.3 "And he was still alive to read it."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.05), mid=(0.22, 0.14, 0.10))
    spotlight(ctx, W / 2, 600, 700, 0.3, (1, 0.85, 0.6))
    gent(ctx, W / 2, 420, 0.9, col=(0.10, 0.08, 0.10))
    newspaper(ctx, W / 2, 900, 0.62, HEAD, rot=0.02)
    pill(ctx, "STILL ALIVE", W / 2, 1450, pop(lt, 0.4), rgb=GREEN)


# 21.2 "Historians still argue about the details, but the story goes that Nobel was horrified."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.05, 0.05, 0.12), mid=(0.12, 0.10, 0.24))
    for k in range(5):
        icon(ctx, "📚", 160 + k * 190, 330 + 30 * math.sin(T * 2 + k), 110, pop(lt, 0.1 * k))
    character(ctx, W / 2, 700, 0.9, T, mood="sorpresa" if lt > 2.0 else "duda", body=True)
    badge(ctx, "THE STORY GOES", W / 2, 1450, pop(lt, 1.6), size=50, bg=PURPLE)


# 25.8 "He didn't want to be remembered as the man who made killing easier."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    cemetery(ctx, T, 1560)
    tombstone(ctx, W / 2, 1300, 1.7)
    text(ctx, "MERCHANT", W / 2, 1250, 50, (0.25, 0.25, 0.3), shadow=False)
    text(ctx, "OF DEATH", W / 2, 1310, 50, (0.25, 0.25, 0.3), shadow=False)
    stamp(ctx, "NO WAY", W / 2, 420, (lt - 1.0) / 0.3, size=100)


# 29.0 "So he rewrote his will,"
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.05), mid=(0.22, 0.14, 0.10))
    scroll_will(ctx, W / 2, 800, 0.9, T, write=clamp(lt / 1.5))


# 30.6 "and left most of his fortune to reward the people who help humanity the most."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    p = ease((lt - 0.6) / 2.0)
    for k in range(3):
        money_bag(ctx, lerp(200 + k * 120, 760 + (k - 1) * 120, p), lerp(560 + k * 60, 820, p), lerp(0.75, 0.3, p))
    icon(ctx, "🌍", 760, 820, 300, pop(lt, 0.2))
    pill(ctx, "FOR HUMANITY", W / 2, 1450, pop(lt, 1.6), rgb=GREEN)


# 34.4 "That's why the most famous prize on Earth carries his name."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.4, 1.0), (dur, 1.08)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.08, 0.06, 0.02), mid=(0.20, 0.15, 0.05))
    rays(ctx, W / 2, 760, T, GOLD, 0.07)
    medal(ctx, W / 2, 760, 1.15, T)


# 37.4 "All because of one newspaper's mistake."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 860)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.05), mid=(0.22, 0.14, 0.10))
    newspaper(ctx, W / 2, 760, 0.9, HEAD, rot=0.04)
    thumb_circle(ctx, W / 2, 540, 330, 150)
    stamp(ctx, "MISTAKE", W / 2, 1400, (lt - 0.8) / 0.3, size=90)


# 39.5 "That's how" -> vuelve a e1
def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.8, e2), (4.3, e3), (7.3, e4), (9.7, e5), (12.9, e6), (16.4, e7), (19.3, e8),
           (21.2, e9), (25.8, e10), (29.0, e11), (30.6, e12), (34.4, e13), (37.4, e14), (39.5, e15)]
SFX = [(16.45, "ding"), (34.45, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.05), mid=(0.22, 0.14, 0.10), bot=(0.05, 0.03, 0.02))
    spotlight(ctx, W / 2, 1100, 800, 0.35, (1, 0.9, 0.7))
    newspaper(ctx, W / 2, 1120, 1.0, HEAD, "PARIS, 1888", rot=-0.05)
    ctx.restore()
    thumb_vignette(ctx, 0.55)
    thumb_text(ctx, ["HE READ", ("THIS. ALIVE.", WHITE)], y=260, size=190)
    thumb_circle(ctx, W / 2 - 20, 880, 330, 150)
    thumb_arrow(ctx, 120, 1640, 330, 1350)
