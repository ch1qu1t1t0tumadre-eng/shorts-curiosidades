"""v13 (EN) FORMATO BUCLE: Charlie Chaplin's coffin was stolen (1978) and held for ransom."""
from kit import *  # noqa

DIRT = (0.30, 0.20, 0.12)


def open_grave(ctx, x, y, s, T, empty=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-330, 0); ctx.line_to(330, 0); ctx.line_to(290, 220); ctx.line_to(-290, 220); ctx.close_path()
    fill(ctx, (0.05, 0.03, 0.02))
    ctx.move_to(-330, 0); ctx.line_to(330, 0); stroke(ctx, DIRT, 12)
    # montón de tierra
    ctx.move_to(360, 10); ctx.curve_to(420, -170, 600, -170, 660, 10); ctx.close_path(); fill(ctx, DIRT)
    # pala clavada
    ctx.save(); ctx.translate(540, -120); ctx.rotate(0.35)
    rrect(ctx, -10, -330, 20, 300, 8); fill(ctx, WOOD)
    ctx.move_to(-55, -40); ctx.line_to(55, -40); ctx.line_to(40, 60); ctx.line_to(0, 90); ctx.line_to(-40, 60); ctx.close_path()
    fill(ctx, (0.6, 0.62, 0.68))
    ctx.restore()
    if not empty:
        coffin(ctx, 0, 110, 0.5, math.pi / 2)
    ctx.restore()


def scene_grave(ctx, T, ground=1250):
    cemetery(ctx, T, ground)
    tombstone(ctx, W / 2, ground - 300, 1.2, "CHAPLIN")
    open_grave(ctx, W / 2 - 60, ground + 80, 1.0, T)


def hero(ctx, T, zoom):
    camera(ctx, zoom, W / 2, 1000)
    scene_grave(ctx, T)
    icon(ctx, "❓", W / 2 - 60, 1430, 130)
    ctx.restore(); ctx.save()
    ficha(ctx, "CHARLIE CHAPLIN", "FILM LEGEND · 1889–1977", W / 2, 1640, 1.0, "🎬", YELLOW)


def digger(ctx, x, y, s, T, ph=0.0):
    gent(ctx, x, y, s, hat=False, col=(0.04, 0.04, 0.08))
    a = 0.4 + 0.35 * math.sin(T * 6 + ph)
    ctx.save(); ctx.translate(x + 60 * s, y + 250 * s); ctx.rotate(a)
    rrect(ctx, -8 * s, 0, 16 * s, 360 * s, 6); fill(ctx, WOOD)
    rrect(ctx, -40 * s, 340 * s, 80 * s, 110 * s, 14); fill(ctx, (0.6, 0.62, 0.68))
    ctx.restore()


# 0.0 "Charlie Chaplin's coffin was stolen."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.15)]))


# 2.5 "With Charlie Chaplin still inside."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (0.3, 1.05), (dur, 1.1)]), W / 2, 880)
    bg_dark(ctx, T, top=(0.04, 0.04, 0.10), mid=(0.10, 0.08, 0.20))
    spotlight(ctx, W / 2, 760, 600, 0.35, (1, 0.85, 0.6))
    coffin(ctx, W / 2, 760, 1.0, 0.0)
    pill(ctx, "STILL INSIDE", W / 2, 1450, pop(lt, 0.6), rgb=RED)


# 4.5 "Chaplin died on Christmas Day, 1977,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    icon(ctx, "🎄", W / 2, 640, 420, pop(lt, 0.0))
    pill(ctx, "DEC 25", W / 2, 280, pop(lt, 0.6), size=60, rgb=RED)
    pill(ctx, counter(lt - 1.4, 1889, 1977, 0.9), W / 2, 1350, pop(lt, 1.4), size=80, rgb=GOLD)


# 7.5 "at his home in Switzerland."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 900)
    bg_night(ctx, T, grid=False)
    for mx, mh in ((150, 520), (540, 700), (930, 560)):
        ctx.move_to(mx - 380, 1200); ctx.line_to(mx, 1200 - mh); ctx.line_to(mx + 380, 1200); ctx.close_path()
        fill(ctx, (0.25, 0.30, 0.45))
        ctx.move_to(mx - 90, 1200 - mh + 120); ctx.line_to(mx, 1200 - mh); ctx.line_to(mx + 90, 1200 - mh + 120)
        ctx.close_path(); fill(ctx, WHITE, 0.9)
    ground(ctx, 1200)
    house(ctx, W / 2, 1420, 0.55, T)
    pill(ctx, "SWITZERLAND", W / 2, 330, pop(lt, 0.2), rgb=RED)


# 8.8 "He was buried in a small village cemetery."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    cemetery(ctx, T, 1450)
    tombstone(ctx, W / 2, 1230, 1.3, "CHAPLIN")
    icon(ctx, "💐", W / 2, 1480, 140)


# 11.0 "Two months later, on a dark night in March 1978,"
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 850)
    bg_dark(ctx, T, top=(0.01, 0.01, 0.04), mid=(0.04, 0.04, 0.10), bot=(0.0, 0.0, 0.02))
    circle(ctx, W / 2, 520, 200); fill(ctx, (0.95, 0.93, 0.8))
    circle(ctx, W / 2 + 70, 480, 200); fill(ctx, (0.01, 0.01, 0.04))
    rrect(ctx, W / 2 - 230, 1200, 460, 330, 24); fill(ctx, WHITE)
    rrect(ctx, W / 2 - 230, 1200, 460, 90, 24); fill(ctx, RED)
    text(ctx, "MARCH", W / 2, 1245, 50, WHITE, shadow=False)
    text(ctx, "1978", W / 2, 1410, 110, INK, shadow=False)


# 14.4 "two men dug up his grave."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 950)
    cemetery(ctx, T, 1300)
    open_grave(ctx, W / 2, 1380, 1.0, T, empty=False)
    digger(ctx, 230, 760, 0.8, T)
    digger(ctx, 850, 760, 0.8, T, 1.5)


# 16.0 "And they took the whole coffin."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    cemetery(ctx, T, 1350)
    open_grave(ctx, W / 2 - 100, 1430, 0.9, T)
    p = ease(lt / 1.6)
    coffin(ctx, lerp(W / 2 - 100, 860, p), lerp(1420, 620, p), 0.7, lerp(math.pi / 2, 0.3, p))
    pill(ctx, "THE WHOLE COFFIN", W / 2, 330, pop(lt, 0.5), rgb=RED)


# 17.9 "In other words, they kidnapped a dead man."  (2.º gancho)
def e9(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur) + 0.01 * math.sin(T * 40) * (lt < 0.4), W / 2, 880)
    bg_dark(ctx, T, top=(0.20, 0.03, 0.05), mid=(0.10, 0.02, 0.04))
    rays(ctx, W / 2, 700, T, RED, 0.06)
    coffin(ctx, W / 2, 700, 0.95, 0.12)
    rrect(ctx, W / 2 - 260, 560, 520, 50, 10); fill(ctx, (0.75, 0.70, 0.55))  # cuerda
    rrect(ctx, W / 2 - 260, 820, 520, 50, 10); fill(ctx, (0.75, 0.70, 0.55))
    stamp(ctx, "KIDNAPPED", W / 2, 1420, (lt - 0.9) / 0.3, size=90)


# 20.3 "Then they called his widow, Oona, and demanded six hundred thousand Swiss francs."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.10), mid=(0.14, 0.10, 0.20))
    phone(ctx, W / 2, 560, 1.3, ring=clamp(1 - lt / 2.0), T=T)
    money_bag(ctx, W / 2, 1330, 1.0, "₣")
    pill(ctx, "600,000 SWISS FRANCS", W / 2, 1600, pop(lt, 2.4), size=46, rgb=GOLD)


# 24.7 "She refused. She said Charlie would have found it ridiculous."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (0.3, 1.0), (dur, 1.06)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.10), mid=(0.14, 0.10, 0.20))
    money_bag(ctx, W / 2, 620, 1.2, "₣")
    stamp(ctx, "REFUSED", W / 2, 620, lt / 0.3, size=110)
    pill(ctx, '"RIDICULOUS"', W / 2, 1420, pop(lt, 1.6), size=56, rgb=WHITE)


# 27.8 "So the police tapped the phones, and caught one of them in the middle of a ransom call."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    bg_dark(ctx, T, top=(0.02, 0.04, 0.12), mid=(0.05, 0.10, 0.25))
    col = RED if int(T * 4) % 2 else (0.2, 0.4, 1.0)
    spotlight(ctx, W / 2, 300, 700, 0.30, col)
    icon(ctx, "🚓", W / 2, 400, 260, pop(lt, 0.0))
    phone(ctx, W / 2, 1300, 1.0, ring=1.0, T=T)
    icon(ctx, "🎧", 820, 1200, 180, pop(lt, 0.8))
    stamp(ctx, "CAUGHT", W / 2, 1640, (lt - 2.6) / 0.3, size=90)


# 31.7 "The thieves led them to a cornfield, where they had buried Chaplin."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 1000)
    cornfield(ctx, T, 900)
    ctx.rectangle(W / 2 - 260, 1500, 520, 260); fill(ctx, (0.12, 0.08, 0.04))
    coffin(ctx, W / 2, 1630, 0.55, math.pi / 2)
    pin(ctx, W / 2, 1460, 1.0, (lt - 0.4) / 0.3)
    pill(ctx, "CORNFIELD", W / 2, 330, pop(lt, 1.0), rgb=GOLD)


# 34.7 "He was reburied, this time under concrete, so nobody could ever do it again."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 950)
    cemetery(ctx, T, 1250)
    tombstone(ctx, W / 2, 950, 1.2, "CHAPLIN")
    drop = ease_back(clamp((lt - 1.5) / 0.5))
    rrect(ctx, W / 2 - 360, lerp(700, 1330, drop), 720, 160, 10); fill(ctx, (0.62, 0.62, 0.64))
    pill(ctx, "CONCRETE", W / 2, 1650, pop(lt, 2.0), rgb=STONE)


# 38.8 "Because, believe it or not," -> vuelve a e1
def e15(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.9), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.5, e2), (4.5, e3), (7.5, e4), (8.8, e5), (11.0, e6), (14.4, e7), (16.0, e8),
           (17.9, e9), (20.3, e10), (24.7, e11), (27.8, e12), (31.7, e13), (34.7, e14), (38.8, e15)]
SFX = [(17.95, "ding"), (24.75, "pop"), (30.5, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.05, W / 2, 1150)
    scene_grave(ctx, T, 1350)
    ctx.restore()
    thumb_vignette(ctx, 0.6)
    thumb_text(ctx, ["WHO TOOK", ("CHAPLIN?", WHITE)], y=270, size=200)
    thumb_circle(ctx, W / 2 - 60, 1390, 380, 150)
    thumb_arrow(ctx, 120, 1760, 300, 1520)
