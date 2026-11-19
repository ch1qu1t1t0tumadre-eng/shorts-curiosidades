"""v20 (EN) FORMATO BUCLE: Lincoln created the Secret Service on the day he was shot (no violencia gráfica)."""
from kit import *  # noqa

BILL = (0.80, 0.86, 0.74)
BILL_D = (0.25, 0.40, 0.30)
SUIT = (0.05, 0.05, 0.08)


def badge_star(ctx, x, y, s, T, glow=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if glow > 0:
        spotlight(ctx, 0, 0, 420, 0.4 * glow, GOLD)
    ctx.new_path()
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = 230 if k % 2 == 0 else 110
        ctx.line_to(math.cos(a) * r, math.sin(a) * r)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -230, 0, 230, [(0, (1, 0.9, 0.5)), (1, (0.75, 0.52, 0.15))])); ctx.fill()
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        circle(ctx, math.cos(a) * 230, math.sin(a) * 230, 22); fill(ctx, GOLD)
    circle(ctx, 0, 0, 95); fill(ctx, (0.85, 0.65, 0.20))
    text(ctx, "SECRET", 0, -22, 30, (0.40, 0.25, 0.05), shadow=False)
    text(ctx, "SERVICE", 0, 18, 30, (0.40, 0.25, 0.05), shadow=False)
    ctx.restore()


def bill(ctx, x, y, s=1.0, rot=0.0, fake=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -300, -130, 600, 260, 14); fill(ctx, BILL)
    rrect(ctx, -280, -110, 560, 220, 10); stroke(ctx, BILL_D, 6)
    ctx.save(); ctx.scale(0.8, 1); circle(ctx, 0, 0, 80); ctx.restore(); fill(ctx, (0.65, 0.74, 0.62))
    text(ctx, "$", -220, -60, 60, BILL_D, shadow=False); text(ctx, "$", 220, 60, 60, BILL_D, shadow=False)
    if fake:
        stamp(ctx, "FAKE", 0, 0, 1.0, size=80, rot=-0.2)
    ctx.restore()


def agent(ctx, x, y, s=1.0):
    gent(ctx, x, y, s, col=SUIT, hat=False)
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -75, -25, 150, 40, 14); fill(ctx, (0.0, 0.0, 0.0))
    rrect(ctx, -70, -20, 60, 26, 10); fill(ctx, (0.25, 0.25, 0.30))
    rrect(ctx, 10, -20, 60, 26, 10); fill(ctx, (0.25, 0.25, 0.30))
    ctx.move_to(-15, 140); ctx.line_to(0, 300); ctx.line_to(15, 140); fill(ctx, WHITE, 0.9)
    ctx.restore()


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 860)
    bg_dark(ctx, T, top=(0.04, 0.05, 0.12), mid=(0.10, 0.12, 0.26))
    badge_star(ctx, W / 2, 740, 1.3, T)
    ctx.restore(); ctx.save()
    ficha(ctx, "ABRAHAM LINCOLN", "16TH U.S. PRESIDENT · 1809–1865", W / 2, 1580, 1.0, "🇺🇸", YELLOW)


def calendar(ctx, x, y, s, month, day, year):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -200, 460, 420, 24); fill(ctx, WHITE)
    rrect(ctx, -230, -200, 460, 100, 24); fill(ctx, RED)
    text(ctx, month, 0, -150, 50, WHITE, shadow=False)
    text(ctx, str(day), 0, 20, 150, INK, shadow=False)
    text(ctx, str(year), 0, 160, 46, (0.4, 0.4, 0.45), shadow=False)
    ctx.restore()


# 0.0 "Abraham Lincoln created the Secret Service on the day he was shot."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 4.1 "April fourteenth, 1865."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, 880)
    bg_night(ctx, T, grid=False)
    calendar(ctx, W / 2, 720, 1.3, "APRIL", 14, 1865)


# 6.3 "The Civil War was almost over."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.10, 0.08, 0.06), mid=(0.22, 0.18, 0.12))
    icon(ctx, "⚔️", W / 2, 680, 360, pop(lt, 0.0))
    pill(ctx, "CIVIL WAR: ENDING", W / 2, 1450, pop(lt, 0.4), rgb=STONE)


# 8.1 "But America had another enemy: fake money."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.04, 0.12, 0.06), mid=(0.08, 0.20, 0.10))
    bill(ctx, W / 2 - 60, 560, 1.0, -0.12)
    bill(ctx, W / 2 + 60, 760, 1.0, 0.08, fake=lt > 1.6)


# 10.8 "By some estimates, up to a third of the cash in circulation was counterfeit."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.04, 0.12, 0.06), mid=(0.08, 0.20, 0.10))
    circle(ctx, W / 2, 720, 320); fill(ctx, BILL)
    p = ease(clamp((lt - 0.5) / 1.4))
    ctx.move_to(W / 2, 720); ctx.arc(W / 2, 720, 320, -math.pi / 2, -math.pi / 2 + math.tau / 3 * p); ctx.close_path()
    fill(ctx, RED)
    pill(ctx, "1 IN 3 = FAKE", W / 2, 1450, pop(lt, 2.2), size=60, rgb=RED)


# 14.7 "So that same day, Lincoln approved a new agency to hunt down the counterfeiters."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.14, 0.08))
    ctx.save(); ctx.translate(W / 2, 680); ctx.rotate(-0.04)
    rrect(ctx, -320, -380, 640, 760, 14); fill(ctx, PAPER)
    text(ctx, "SECRET SERVICE", 0, -300, 54, INK, shadow=False)
    for k in range(7):
        ctx.rectangle(-250, -200 + k * 50, 500 if k % 3 else 340, 14); fill(ctx, (0.6, 0.57, 0.5))
    w = clamp((lt - 1.2) / 1.0)
    ctx.move_to(-200, 260)
    for j in range(int(34 * w)):
        ctx.line_to(-200 + j * 12, 260 + 22 * math.sin(j * 1.1))
    stroke(ctx, (0.1, 0.1, 0.3), 6)
    ctx.restore()
    icon(ctx, "🔎", 860, 1260, 200, pop(lt, 2.2))


# 19.1 "That night, he went to Ford's Theatre to watch a comedy."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    bg_night(ctx, T, grid=False)
    ground(ctx, 1450, (0.08, 0.08, 0.12))
    ctx.rectangle(160, 560, 760, 890); fill(ctx, (0.55, 0.30, 0.22))
    for k in range(5):
        rrect(ctx, 210 + k * 140, 700, 90, 200, 45); fill(ctx, (1, 0.85, 0.5), 0.8)
        rrect(ctx, 210 + k * 140, 1100, 90, 300, 10); fill(ctx, (0.30, 0.16, 0.12))
    rrect(ctx, 220, 590, 640, 80, 10); fill(ctx, (0.10, 0.08, 0.06))
    text(ctx, "FORD'S THEATRE", W / 2, 630, 46, GOLD, shadow=False)
    icon(ctx, "🎭", W / 2, 420, 200, pop(lt, 0.8))


# 21.8 "In other words, he created the Secret Service, and hours later, he was assassinated."  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.20, 0.03, 0.05), mid=(0.10, 0.02, 0.04))
    rays(ctx, W / 2, 700, T, RED, 0.06)
    badge_star(ctx, 300, 640, 0.6, T, glow=0.5)
    calendar(ctx, 780, 640, 0.75, "APRIL", 14, 1865)
    stamp(ctx, "SAME DAY", W / 2, 1420, (lt - 1.4) / 0.3, size=90)


# 26.3 "But here's the twist."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.0), (dur, 1.06)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.08, 0.04, 0.14), mid=(0.18, 0.08, 0.28))
    text(ctx, "?", W / 2, 700, 520, YELLOW)


# 27.4 "That Secret Service wasn't built to protect him at all."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.04, 0.05, 0.12), mid=(0.10, 0.12, 0.26))
    badge_star(ctx, W / 2, 540, 0.8, T, glow=0.4)
    gent(ctx, W / 2, 900, 0.55, col=(0.10, 0.10, 0.16))
    stamp(ctx, "NOT FOR HIM", W / 2, 1450, (lt - 0.8) / 0.3, size=80)


# 30.0 "It was built to protect the money."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.04, 0.12, 0.06), mid=(0.08, 0.20, 0.10))
    for k in range(4):
        bill(ctx, W / 2 + (k - 1.5) * 40, 820 - k * 50, 0.9, (k - 1.5) * 0.08)
    icon(ctx, "🛡️", W / 2, 470, 260, pop(lt, 0.3))
    pill(ctx, "PROTECT THE MONEY", W / 2, 1450, pop(lt, 0.8), size=50, rgb=GREEN)


# 31.7 "It took two more murdered presidents"
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 950)
    cemetery(ctx, T, 1450)
    tombstone(ctx, 330, 1220, 1.2, "1881")
    tombstone(ctx, 750, 1220, 1.2, "1901") if lt > 0.8 else None


# 35.0 "before the Secret Service started guarding the president."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    gent(ctx, W / 2, 560, 0.8, col=(0.15, 0.18, 0.30), hat=False)
    agent(ctx, 200, 620, 0.7)
    agent(ctx, 880, 620, 0.7)
    pill(ctx, "PROTECTION", W / 2, 1450, pop(lt, 0.4), rgb=TEAL)


# 36.3 "So the next time you see agents in dark suits and sunglasses, remember that"
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.04, 0.05, 0.12), mid=(0.10, 0.12, 0.26))
    for k in range(3):
        agent(ctx, 200 + k * 340, 560, 0.85)


def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (4.1, e2), (6.3, e3), (8.1, e4), (10.8, e5), (14.7, e6), (19.1, e7), (21.8, e8),
           (26.3, e9), (27.4, e10), (30.0, e11), (31.7, e12), (35.0, e13), (36.3, e14), (39.3, e15)]
SFX = [(9.7, "pop"), (21.85, "ding"), (26.35, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_dark(ctx, T, top=(0.04, 0.05, 0.12), mid=(0.10, 0.12, 0.26))
    badge_star(ctx, W / 2, 1100, 1.4, T, glow=1.3)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["CREATED THE", ("SAME DAY?!", WHITE)], y=260, size=180)
    calendar(ctx, 860, 1650, 0.5, "APRIL", 14, 1865)
    thumb_arrow(ctx, 120, 1700, 330, 1350)
