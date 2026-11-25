"""v24 (EN) FORMATO BUCLE: Tycho Brahe's metal nose (duel 1566, Rostock; 2010 exhumation in Prague: brass, not silver)."""
from kit import *  # noqa

BRASS = (0.86, 0.68, 0.30)
SILVER = (0.82, 0.84, 0.90)
SKIN = (0.96, 0.80, 0.66)
SKIN_D = (0.82, 0.62, 0.48)
HAIR = (0.80, 0.52, 0.24)
VERDIGRIS = (0.30, 0.75, 0.55)
NAVY_TOP = (0.02, 0.03, 0.10)
NAVY_MID = (0.06, 0.08, 0.24)


def metal_grad(ctx, x, y, r, col):
    g = cairo.LinearGradient(x - r, y - r, x + r, y + r)
    hi = tuple(min(1, c + 0.25) for c in col)
    lo = tuple(c * 0.55 for c in col)
    g.add_color_stop_rgb(0, *hi); g.add_color_stop_rgb(0.45, *col); g.add_color_stop_rgb(1, *lo)
    return g


def nose_piece(ctx, x, y, s=1.0, col=BRASS, T=0.0, shine=True):
    """Prótesis de nariz (puente metálico)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-40, -130); ctx.curve_to(-20, -150, 20, -150, 40, -130)
    ctx.curve_to(60, -40, 90, 40, 70, 90); ctx.curve_to(40, 120, -40, 120, -70, 90)
    ctx.curve_to(-90, 40, -60, -40, -40, -130); ctx.close_path()
    ctx.set_source(metal_grad(ctx, 0, 0, 120, col)); ctx.fill_preserve()
    stroke(ctx, tuple(c * 0.45 for c in col), 6)
    if shine:
        a = 0.5 + 0.4 * math.sin(T * 3)
        ctx.move_to(-15, -110); ctx.curve_to(-25, -40, -30, 20, -40, 70); stroke(ctx, WHITE, 10, a)
    ctx.restore()


def tycho_head(ctx, x, y, s=1.0, T=0.0, nose=BRASS, nose_on=1.0, look_up=0.0, cut=False):
    """Cabeza de dibujo GENÉRICA (personaje de caricatura, no retrato): de frente, bigote largo, gorguera, nariz metálica."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # gorguera (cuello de lechuguilla)
    for k in range(16):
        a = math.pi * 0.05 + k * math.pi * 0.9 / 15
        circle(ctx, math.cos(a) * 250, 290 + math.sin(a) * 60, 70); fill_keep(ctx, (0.97, 0.96, 0.92)); stroke(ctx, (0.75, 0.74, 0.72), 3)
    # cara
    ctx.save(); ctx.scale(1, 1.15); circle(ctx, 0, 0, 230); ctx.restore()
    ctx.set_source(vgrad(ctx, 0, -260, 0, 260, [(0, SKIN), (1, SKIN_D)])); ctx.fill()
    # pelo (calvo arriba, pelo a los lados)
    for sx in (-1, 1):
        ellipse(ctx, sx * 215, -30, 50, 110); fill(ctx, HAIR)
    # ojos
    for sx in (-1, 1):
        ellipse(ctx, sx * 85, -50 - 20 * look_up, 34, 22); fill(ctx, WHITE)
        circle(ctx, sx * 85, -52 - 30 * look_up, 15); fill(ctx, (0.12, 0.10, 0.10))
        ctx.move_to(sx * 130, -110); ctx.line_to(sx * 40, -100); stroke(ctx, HAIR, 12)
    # bigote enorme
    for sx in (-1, 1):
        ctx.move_to(0, 115); ctx.curve_to(sx * 80, 90, sx * 180, 120, sx * 260, 60 + 8 * math.sin(T * 2))
        ctx.curve_to(sx * 190, 150, sx * 80, 150, 0, 135); ctx.close_path(); fill(ctx, HAIR)
    # nariz
    if cut:
        ctx.move_to(-60, 20); ctx.curve_to(-30, 60, 30, 60, 60, 20); stroke(ctx, SKIN_D, 10)
    if nose_on > 0:
        nose_piece(ctx, 0, 10 - 300 * (1 - ease_back(clamp(nose_on))), 0.85, nose, T)
    ctx.restore()


def sword(ctx, x, y, L, rot=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(0, -10); ctx.line_to(L, -4); ctx.line_to(L + 30, 0); ctx.line_to(L, 4); ctx.line_to(0, 10); ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -10, 0, 10, [(0, WHITE), (1, (0.55, 0.58, 0.66))])); ctx.fill()
    rrect(ctx, -14, -60, 28, 120, 10); fill(ctx, GOLD)
    rrect(ctx, -110, -14, 100, 28, 12); fill(ctx, WOOD)
    circle(ctx, -120, 0, 20); fill(ctx, GOLD)
    ctx.restore()


def calendar(ctx, x, y, s, top, big, small, col=RED):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -200, 460, 420, 24); fill(ctx, PAPER)
    rrect(ctx, -230, -200, 460, 100, 24); fill(ctx, col)
    text(ctx, top, 0, -150, 50, WHITE, shadow=False)
    text(ctx, big, 0, 30, 150, INK, shadow=False)
    text(ctx, small, 0, 165, 40, (0.4, 0.4, 0.45), shadow=False)
    ctx.restore()


def star_map(ctx, T, a=1.0):
    rng = np.random.default_rng(11)
    pts = [(rng.uniform(120, 960), rng.uniform(250, 1500)) for _ in range(26)]
    for k in range(0, 24, 3):
        ctx.move_to(*pts[k]); ctx.line_to(*pts[k + 1]); ctx.line_to(*pts[k + 2])
        stroke(ctx, (0.6, 0.75, 1.0), 3, 0.5 * a)
    for k, (px, py) in enumerate(pts):
        r = 8 + 5 * math.sin(T * 3 + k)
        circle(ctx, px, py, r); fill(ctx, (1, 0.95, 0.75), a)


def quadrant(ctx, x, y, s, T):
    """Cuadrante astronómico (arco graduado con alidada)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 380, -math.pi / 2, 0); stroke(ctx, BRASS, 26)
    ctx.move_to(0, 0); ctx.line_to(0, -380); stroke(ctx, BRASS, 18); ctx.move_to(0, 0); ctx.line_to(380, 0); stroke(ctx, BRASS, 18)
    for k in range(19):
        a = -math.pi / 2 + k * math.pi / 36
        ctx.move_to(math.cos(a) * 350, math.sin(a) * 350); ctx.line_to(math.cos(a) * 395, math.sin(a) * 395); stroke(ctx, INK, 3)
    a = -0.9 + 0.15 * math.sin(T * 1.5)
    ctx.move_to(0, 0); ctx.line_to(math.cos(a) * 420, math.sin(a) * 420); stroke(ctx, GOLD, 12)
    circle(ctx, 0, 0, 24); fill(ctx, GOLD)
    ctx.restore()


def tyn_church(ctx, x, y, s, T):
    """Silueta de iglesia gótica de dos torres (Praga)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    col = (0.22, 0.18, 0.34)
    ctx.rectangle(-300, -250, 600, 500); fill(ctx, col)
    ctx.move_to(-300, -250); ctx.line_to(0, -420); ctx.line_to(300, -250); fill(ctx, col)
    for sx in (-1, 1):
        ctx.rectangle(sx * 190 - 70, -650, 140, 600); fill(ctx, col)
        ctx.move_to(sx * 190 - 90, -650); ctx.line_to(sx * 190, -900); ctx.line_to(sx * 190 + 90, -650); fill(ctx, col)
        for k in (-1, 1):
            ctx.move_to(sx * 190 + k * 70 - 18, -650); ctx.line_to(sx * 190 + k * 70, -740); ctx.line_to(sx * 190 + k * 70 + 18, -650); fill(ctx, col)
        circle(ctx, sx * 190, -910, 12); fill(ctx, GOLD)
    for k in range(3):
        rrect(ctx, -170 + k * 130, -120, 80, 200, 40); fill(ctx, (1, 0.8, 0.45), 0.55 + 0.3 * math.sin(T * 2 + k))
    ctx.restore()


def element(ctx, x, y, sym, name, num, col, appear=1.0):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(appear, appear)
    rrect(ctx, -170, -190, 340, 380, 24); fill_keep(ctx, col); stroke(ctx, WHITE, 6)
    text(ctx, str(num), -120, -140, 40, WHITE, shadow=False, align="left")
    text(ctx, sym, 0, 30, 170, WHITE)
    text(ctx, name, 0, 140, 46, WHITE, shadow=False)
    ctx.restore()


def bg_navy(ctx, T):
    bg_night(ctx, T, grid=False)


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): Tycho (caricatura) con nariz de metal brillante + ficha."""
    camera(ctx, zoom, W / 2, 820)
    bg_navy(ctx, T)
    rays(ctx, W / 2, 620, T, (1.0, 0.85, 0.5), 0.05)
    spotlight(ctx, W / 2, 620, 520, 0.35, (1, 0.9, 0.6))
    tycho_head(ctx, W / 2, 560, 1.05, T)
    ctx.restore(); ctx.save()
    ficha(ctx, "TYCHO BRAHE", "ASTRONOMER · 1546–1601", W / 2, 1470, 1.0, "🔭", GOLD)


# 0.00 "Tycho Brahe's nose was made of metal."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 2.64 "And it's real."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.05)]), W / 2, 760)
    bg_navy(ctx, T)
    spotlight(ctx, W / 2, 560, 400, 0.4, (1, 0.9, 0.6))
    nose_piece(ctx, W / 2, 560, 2.2, BRASS, T)
    badge(ctx, "100% REAL", W / 2, 1380, pop(lt, 0.2), size=70)


# 3.84 "In 1566,"
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.14, 0.08))
    calendar(ctx, W / 2, 400, 1.2, "YEAR", str(int(counter(lt, 1500, 1566, 0.9))), "A YOUNG STUDENT")


# 5.40 "in Rostock,"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 760)
    bg_sky(ctx, T, warm=0.2)
    map_card(ctx, W / 2, 640, 820, 620, T)
    pin(ctx, W / 2 + 40, 640, 1.0, drop=lt / 0.35)
    pill(ctx, "ROSTOCK · GERMANY", W / 2, 300, pop(lt, 0.1), size=52, rgb=GOLD)


# 6.21 "Tycho Brahe fought a sword duel"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]) + 0.004 * math.sin(T * 20), W / 2, 760)
    bg_dark(ctx, T, top=(0.14, 0.04, 0.06), mid=(0.26, 0.08, 0.10))
    ground(ctx, 1250, (0.12, 0.06, 0.08))
    gent(ctx, 240, 560, 0.95, hat=True, col=(0.06, 0.05, 0.08))
    gent(ctx, 840, 560, 0.95, hat=True, col=(0.06, 0.05, 0.08))
    sw = 0.25 * math.sin(T * 9)
    sword(ctx, 360, 760, 420, -0.55 + sw, 1.0)
    sword(ctx, 720, 760, 420, math.pi + 0.55 - sw, 1.0)
    for k in range(6):
        a = k * math.tau / 6 + T * 4
        ctx.move_to(W / 2 + math.cos(a) * 30, 560 + math.sin(a) * 30); ctx.line_to(W / 2 + math.cos(a) * 80, 560 + math.sin(a) * 80)
        stroke(ctx, YELLOW, 6, 0.8)
    badge(ctx, "SWORD DUEL", W / 2, 260, pop(lt, 0.4), size=64)


# 8.17 "with his own cousin, Manderup Parsberg."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.14, 0.04, 0.06), mid=(0.26, 0.08, 0.10))
    gent(ctx, W / 2, 420, 1.1, hat=True, col=(0.08, 0.06, 0.10))
    sword(ctx, W / 2 + 120, 760, 380, -0.9, 1.0)
    pill(ctx, "HIS OWN COUSIN", W / 2, 230, pop(lt, 0.2), size=50, rgb=RED)
    ctx.restore(); ctx.save()
    ficha(ctx, "MANDERUP PARSBERG", "TYCHO'S COUSIN · DANISH NOBLE", W / 2, 1470, pop(lt, 0.9), "⚔️", RED)


# 10.35 "The blade sliced off the bridge of Tycho's nose."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.14, 0.04, 0.06), mid=(0.26, 0.08, 0.10))
    tycho_head(ctx, W / 2, 560, 1.0, T, nose_on=0.0, cut=True)
    p = clamp((lt - 0.3) / 0.35)
    if 0 < p < 1:
        sword(ctx, 100 + 900 * p, 400 + 300 * p, 380, 0.3, 0.9)
    if p >= 1:
        ctx.move_to(W / 2 - 220, 500); ctx.line_to(W / 2 + 220, 640); stroke(ctx, WHITE, 8, 0.6 * (1 - clamp((lt - 0.7) / 0.6)))
    pill(ctx, "THE BRIDGE OF HIS NOSE", W / 2, 230, pop(lt, 1.0), size=44, rgb=YELLOW)


# 13.25 "In other words,"  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur), W / 2, 700)
    bg_dark(ctx, T, top=(0.22, 0.03, 0.06), mid=(0.12, 0.02, 0.05))
    rays(ctx, W / 2, 620, T, RED, 0.08)
    tycho_head(ctx, W / 2, 560, 1.05, T, nose_on=0.0, cut=True)


# 14.07 "the man who mapped the stars"
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_dark(ctx, T, top=NAVY_TOP, mid=NAVY_MID)
    star_map(ctx, T, a=ease(clamp(lt / 0.8)))
    quadrant(ctx, 260, 1300, 0.8, T)
    pill(ctx, "HE MAPPED THE STARS", W / 2, 260, pop(lt, 0.5), size=50, rgb=GOLD)


# 15.75 "lost his nose in a fight."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.2)]), W / 2, 640)
    bg_dark(ctx, T, top=(0.22, 0.03, 0.06), mid=(0.12, 0.02, 0.05))
    tycho_head(ctx, W / 2, 560, 1.0, T, nose_on=0.0, cut=True)
    stamp(ctx, "NO NOSE", W / 2, 1150, (lt - 0.3) / 0.3, size=110)
    character(ctx, 170, 1120, 0.5, T, mood="sorpresa")


# 17.45 "So Tycho Brahe wore a fake nose, for the rest of his life."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_navy(ctx, T)
    spotlight(ctx, W / 2, 600, 500, 0.3, (1, 0.9, 0.6))
    tycho_head(ctx, W / 2, 560, 1.0, T, nose_on=clamp((lt - 0.4) / 0.6))
    pill(ctx, "FOR THE REST OF HIS LIFE", W / 2, 1420, pop(lt, 1.8), size=44, rgb=GOLD)


# 20.87 "For centuries, everyone said it was silver and gold."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.12), mid=(0.14, 0.12, 0.26))
    spotlight(ctx, W / 2, 620, 600, 0.3)
    nose_piece(ctx, W / 2 - 210, 620, 1.6 * pop(lt, 1.8), SILVER, T)
    nose_piece(ctx, W / 2 + 210, 620, 1.6 * pop(lt, 2.2), GOLD, T)
    pill(ctx, "SILVER?", W / 2 - 210, 300, pop(lt, 1.9), size=50, rgb=SILVER)
    pill(ctx, "GOLD?", W / 2 + 210, 300, pop(lt, 2.3), size=50, rgb=GOLD)
    pill(ctx, "THE LEGEND", W / 2, 1420, pop(lt, 0.2), size=50, rgb=STONE)


# 23.80 "In 2010, scientists opened his grave in Prague."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 820)
    bg_night(ctx, T, grid=False)
    ground(ctx, 1300, (0.08, 0.08, 0.14))
    tyn_church(ctx, W / 2, 1050, 0.95, T)
    badge(ctx, "2010", 230, 300, pop(lt, 0.1), size=80)
    pill(ctx, "PRAGUE", W / 2, 1420, pop(lt, 1.6), size=60, rgb=GOLD)


# 26.99 "Around the nose, they found green stains."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 700)
    bg_blueprint(ctx, T)
    # placa de muestra con manchas verdes
    rrect(ctx, W / 2 - 330, 360, 660, 560, 30); fill(ctx, (0.88, 0.84, 0.74))
    rng = np.random.default_rng(5)
    for k in range(int(9 * clamp(lt / 1.2))):
        circle(ctx, W / 2 + rng.uniform(-220, 220), 640 + rng.uniform(-170, 170), rng.uniform(25, 60)); fill(ctx, VERDIGRIS, 0.8)
    mx, my = W / 2 + 120 * math.sin(T * 1.5), 600 + 60 * math.cos(T * 1.5)
    circle(ctx, mx, my, 150); fill_keep(ctx, GLASS, 0.15); stroke(ctx, (0.15, 0.15, 0.2), 22)
    ctx.move_to(mx + 105, my + 105); ctx.line_to(mx + 250, my + 250); stroke(ctx, WOOD, 40)
    pill(ctx, "GREEN STAINS", W / 2, 1420, pop(lt, 1.2), size=56, rgb=VERDIGRIS)


# 29.39 "Copper and zinc."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.04, 0.10, 0.10), mid=(0.08, 0.20, 0.20))
    element(ctx, W / 2 - 200, 640, "Cu", "COPPER", 29, (0.80, 0.45, 0.25), pop(lt, 0.0))
    element(ctx, W / 2 + 200, 640, "Zn", "ZINC", 30, (0.45, 0.52, 0.62), pop(lt, 0.45))


# 30.50 "It was brass."
def e16(ctx, lt, dur, T):
    camera(ctx, punch(lt, big=1.3, end=1.1, dur=dur), W / 2, 640)
    bg_dark(ctx, T, top=(0.12, 0.08, 0.02), mid=(0.26, 0.18, 0.04))
    rays(ctx, W / 2, 600, T, GOLD, 0.08)
    nose_piece(ctx, W / 2, 600, 2.3, BRASS, T)
    badge(ctx, "BRASS", W / 2, 1400, pop(lt, 0.1), size=90, bg=(0.65, 0.48, 0.12))


# 31.44 "The famous silver nose of Tycho Brahe was never silver."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.12), mid=(0.14, 0.12, 0.26))
    nose_piece(ctx, W / 2, 700, 1.8, SILVER, T)
    if lt > 2.3:
        p = clamp((lt - 2.3) / 0.25)
        for sx in (-1, 1):
            ctx.move_to(W / 2 - 260, 700 - 260 * sx); ctx.line_to(W / 2 - 260 + 520 * p, 700 - 260 * sx + 520 * p * sx)
            stroke(ctx, RED, 34)
    stamp(ctx, "NEVER SILVER", W / 2, 1420, (lt - 2.4) / 0.3, size=90)
    ctx.restore(); ctx.save()
    ficha(ctx, "TYCHO BRAHE", "ASTRONOMER · 1546–1601", W / 2, 300, pop(lt, 0.6), "🔭", GOLD)


# 34.83 "So the next time you look up at the stars,"
def e18(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 820)
    bg_night(ctx, T, grid=False)
    star_map(ctx, T, a=0.8)
    ground(ctx, 1300, (0.06, 0.07, 0.14))
    character(ctx, W / 2, 1300, 0.9, T, mood="sorpresa", look=(0, -1))


# 36.72 "remember that"  → bucle: "Tycho Brahe's nose was made of metal."
def e19(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.92), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.64, e2), (3.84, e3), (5.40, e4), (6.21, e5), (8.17, e6), (10.35, e7), (13.25, e8),
           (14.07, e9), (15.75, e10), (17.45, e11), (20.87, e12), (23.80, e13), (26.99, e14), (29.39, e15),
           (30.50, e16), (31.44, e17), (34.83, e18), (36.72, e19)]
SFX = [(10.7, "pop"), (13.28, "ding"), (30.55, "ding"), (33.8, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_navy(ctx, T)
    rays(ctx, W / 2, 1000, T, (1.0, 0.85, 0.5), 0.07)
    spotlight(ctx, W / 2, 980, 600, 0.45, (1, 0.9, 0.6))
    tycho_head(ctx, W / 2, 1000, 1.25, T, nose=SILVER)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["HIS NOSE", ("WAS FAKE?!", WHITE)], y=270, size=180)
    thumb_circle(ctx, W / 2, 1010, 170, 190)
    ficha(ctx, "TYCHO BRAHE", "ASTRONOMER · 1546–1601", W / 2, 1640, 1.0, "🔭", GOLD)
