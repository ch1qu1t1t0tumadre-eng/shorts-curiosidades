"""v28 (EN) formato «historia» (inventada, física/química real): por qué las bolsas de patatas van medio vacías (nitrógeno)."""
from kit import *  # noqa
from estilo_v3 import *  # noqa

FLASH = False
WHOOSH = False
MUSICA_GAIN = 0.42
FX_GAIN = 0.30
Y_SUBTITULO = 1430     # subtítulos ABAJO (orden del dueño, 26/11/2026)
TAM_SUBTITULO = 135
set_azul(28.73, 40.13)  # "You see" -> "selling crunch."

KID = (0.25, 0.50, 0.85)
RIV = (0.88, 0.25, 0.25)
CHIP = (1.0, 0.82, 0.36)
N2C = (0.35, 0.62, 1.0)
O2C = (0.92, 0.30, 0.28)


def chip(ctx, x, y, s, rot=0.0, col=CHIP):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(-60, 0)
    ctx.curve_to(-50, -40, 50, -45, 60, -5); ctx.curve_to(55, 35, -45, 40, -60, 0); ctx.close_path()
    fill_ink(ctx, col, 3)
    for k in range(3):
        circle(ctx, -25 + k * 25, -5 + 8 * (k % 2), 4); fill(ctx, (0.85, 0.55, 0.20), 0.6)
    ctx.restore()


def bag(ctx, x, y, s, T, col=KID, name="CHIPS", level=0.35, puff=1.0, crumbs=False, cut=True, stale=0.0):
    """Bolsa de patatas (cutaway): level = altura de las patatas (0..1); puff = lo hinchada; cut = se ve el interior."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    w, h = 300 + 40 * puff, 440
    ctx.move_to(-w / 2, -h / 2)
    ctx.curve_to(-w / 2 - 30 * puff, -h / 4, -w / 2 - 30 * puff, h / 4, -w / 2, h / 2)
    ctx.line_to(w / 2, h / 2)
    ctx.curve_to(w / 2 + 30 * puff, h / 4, w / 2 + 30 * puff, -h / 4, w / 2, -h / 2)
    ctx.close_path()
    fill_ink(ctx, col, 5)
    for yy in (-h / 2, h / 2):  # cierres dentados
        ctx.move_to(-w / 2, yy)
        for k in range(12):
            ctx.line_to(-w / 2 + (k + 0.5) * w / 12, yy + (-12 if yy < 0 else 12)); ctx.line_to(-w / 2 + (k + 1) * w / 12, yy)
        fill_ink(ctx, mix(col, (1, 1, 1), 0.3), 3)
    if cut:
        rrect(ctx, -w / 2 + 40, -h / 2 + 40, w - 80, h - 80, 30); fill_ink(ctx, (0.92, 0.96, 1.0), 4)
        top = h / 2 - 40 - (h - 80) * level
        rng = np.random.default_rng(7)
        if crumbs:
            for k in range(90):
                circle(ctx, rng.uniform(-w / 2 + 55, w / 2 - 55), rng.uniform(h / 2 - 90, h / 2 - 50), rng.uniform(4, 10))
                fill_ink(ctx, mix(CHIP, (0.6, 0.55, 0.4), stale), 1.5)
        else:
            n = int(6 + 22 * level)
            for k in range(n):
                chip(ctx, rng.uniform(-w / 2 + 80, w / 2 - 80), rng.uniform(top + 20, h / 2 - 70), 0.75,
                     rng.uniform(-0.8, 0.8), mix(CHIP, (0.62, 0.58, 0.45), stale))
    else:
        rrect(ctx, -w / 2 + 50, -60, w - 100, 120, 20); fill_ink(ctx, WHITE, 4)
        text(ctx, name, 0, 0, 52, col, shadow=False)
    ctx.restore()


def tank(ctx, x, y, s, T, hose_to=None):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -70, -300, 140, 380, 60); fill_ink(ctx, N2C, 5)
    rrect(ctx, -30, -350, 60, 60, 12); fill_ink(ctx, (0.7, 0.72, 0.8), 4)
    text(ctx, "N₂", 0, -110, 80, WHITE)
    ctx.restore()
    if hose_to:
        ctx.move_to(x, y - 340 * s); ctx.curve_to(x + 60, y - 500 * s, hose_to[0] - 120, hose_to[1] - 140, *hose_to)
        stroke(ctx, (0.25, 0.25, 0.3), 12)


def molecule(ctx, x, y, r, col, lbl):
    circle(ctx, x - r * 0.55, y, r * 0.7); fill_ink(ctx, col, 3)
    circle(ctx, x + r * 0.55, y, r * 0.7); fill_ink(ctx, col, 3)
    text(ctx, lbl, x, y, r * 0.8, WHITE)


def truck(ctx, x, y, s, T, boxes=0, bump=0.0):
    ctx.save(); ctx.translate(x, y - 20 * bump * abs(math.sin(T * 20))); ctx.scale(s, s)
    rrect(ctx, -330, -260, 460, 260, 14); fill_ink(ctx, (0.95, 0.95, 0.92), 5)
    rrect(ctx, 140, -190, 190, 190, 30); fill_ink(ctx, RIV, 5)
    rrect(ctx, 200, -170, 100, 80, 12); fill_ink(ctx, GLASS, 3)
    for wx in (-230, 0, 240):
        ctx.save(); ctx.translate(wx, 20); ctx.rotate(T * 10)
        circle(ctx, 0, 0, 55); fill_ink(ctx, (0.18, 0.18, 0.22), 4); circle(ctx, 0, 0, 22); fill(ctx, STONE)
        ctx.restore()
    for k in range(boxes):
        bx, by = -250 + (k % 3) * 140, -40 - (k // 3) * 110
        rrect(ctx, bx, by - 100, 130, 100, 6); fill_ink(ctx, (0.76, 0.58, 0.36), 3)
    ctx.restore()


def store(ctx, x, y, s, P):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-260, -300, 520, 300); fill_ink(ctx, (0.95, 0.92, 0.84), 4)
    rrect(ctx, -280, -360, 560, 80, 16); fill_ink(ctx, (0.30, 0.66, 0.40), 4)
    text(ctx, "GROCERY", 0, -320, 48, WHITE)
    rrect(ctx, -70, -170, 140, 170, 8); fill_ink(ctx, GLASS, 3)
    ctx.restore()


def factory(ctx, x, y, s, col, name):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-200, 0); ctx.line_to(-200, -220); ctx.line_to(-100, -160); ctx.line_to(-100, -220); ctx.line_to(0, -160)
    ctx.line_to(0, -220); ctx.line_to(200, -220); ctx.line_to(200, 0); ctx.close_path(); fill_ink(ctx, mix(col, (1, 1, 1), 0.45), 4)
    ctx.rectangle(120, -340, 50, 130); fill_ink(ctx, (0.55, 0.50, 0.55), 4)
    rrect(ctx, -160, -120, 320, 80, 16); fill_ink(ctx, col, 4)
    text(ctx, name, 0, -80, 40, WHITE, shadow=False)
    ctx.restore()


def hero(ctx, lt, T, dur, z0, z1):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2, 820)
    sky(ctx, T, P)
    ground(ctx, 1150, P)
    tank(ctx, 230, 1130, 1.0, T, hose_to=(W / 2 - 150, 560))
    bag(ctx, W / 2 + 60, 760, 1.25, T, level=0.32, puff=1.0 + 0.04 * math.sin(T * 4))
    worker(ctx, 900, 860, 0.75, T, col=KID, k=1, mood="feliz", hat_kind="cap", hat=KID)
    ctx.restore()
    label(ctx, "HALF EMPTY?", W / 2, 260, 1.0, rgb=RED, size=58)
    cota(ctx, 790, 420, 790, 640, 1.0, "AIR", rgb=(0.45, 0.72, 1.0), size=40, dy=0) if False else None


# 0.00 "This guy shipped bags of chips that were half empty on purpose."
def e1(ctx, lt, dur, T):
    hero(ctx, lt, T, dur, 1.0, 1.08)
    a = pop(lt, 1.9)
    if a > 0.01:
        label(ctx, "AIR", 300, 560, a, rgb=(0.45, 0.72, 1.0), size=46)
        arrow(ctx, 360, 600, 470, 640, a, rgb=(0.45, 0.72, 1.0), w=10)


# 3.35 "See, two snack companies are fighting for the biggest grocery store in town, and only one gets the shelf."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.12), (dur, 0.98)]), W / 2, 820)
    sky(ctx, T, P)
    ground(ctx, 1000, P)
    factory(ctx, 200, 1000, 0.85, KID, "KID'S CHIPS")
    factory(ctx, 880, 1000, 0.85, RIV, "RIVAL CHIPS")
    store(ctx, W / 2, 1000, 0.75 * pop(lt, 1.8), P)
    ctx.restore()
    a = pop(lt, 7.29 - 3.35)
    if a > 0.01:
        ctx.save(); ctx.translate(W / 2, 1180); ctx.scale(a, a)
        rrect(ctx, -300, -70, 600, 140, 20); fill_ink(ctx, WOOD, 5)
        rrect(ctx, -60, -60, 120, 120, 12); fill_ink(ctx, YELLOW, 4)
        text(ctx, "?", 0, 0, 90, INKC, shadow=False)
        ctx.restore()
        label(ctx, "ONLY 1 SHELF", W / 2, 1290, a, rgb=YELLOW, size=44)


# 7.99 "His boss opens a bag and finds mostly air. Kid, we're selling air."
def e3(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 900), sky(c, T, P), ground(c, 1150, P)))
    ctx.save()
    camera(ctx, z, W / 2, 900)
    bag(ctx, 690, 760, 1.15, T, level=0.28, cut=lt > 0.8)
    worker(ctx, 220, 760, 1.0, T, col=(0.55, 0.42, 0.30), boss=True, k=3, mood="shock" if T > 9.4 else "normal", tie=RED, hat_kind="none")
    ctx.restore()
    label(ctx, "BOSS", 220, 470, pop(lt, 0.2), rgb=GOLD, size=42)
    if T > 9.9:
        label(ctx, "MOSTLY AIR", 690, 330, pop(lt, 9.94 - 7.99), rgb=(0.45, 0.72, 1.0), size=46)
    bubble(ctx, "KID, WE'RE SELLING AIR!", W / 2, 1230, pop(lt, 10.55 - 7.99), size=44)


# 12.07 "But the kid keeps filling them with gas. Nitrogen."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.15)]), W / 2, 860)
    sky(ctx, T, P)
    ground(ctx, 1150, P)
    tank(ctx, 230, 1130, 1.0, T, hose_to=(W / 2 - 120, 560))
    pf = ease(clamp((T - 12.6) / 1.4))
    bag(ctx, W / 2 + 80, 760, 1.15, T, level=0.32, puff=pf)
    worker(ctx, 930, 860, 0.7, T, col=KID, k=1, mood="feliz", hat_kind="cap", hat=KID)
    for k in range(6):  # gas entrando
        ph = (T * 1.5 + k / 6) % 1.0
        circle(ctx, W / 2 - 120 + 60 * ph, 560 + 40 * ph, 10); fill(ctx, N2C, 0.7 * (1 - ph))
    ctx.restore()
    label(ctx, "THE KID", 930, 520, pop(lt, 0.2), rgb=KID, size=40)
    label(ctx, "NITROGEN", 230, 330, pop(lt, 14.03 - 12.07), rgb=N2C, size=52)


# 14.64 "The other company packs every bag to the top. Full of chips. Customers love it."
def e5(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 860)
    sky(ctx, T, P)
    ground(ctx, 1150, P)
    lv = 0.3 + 0.62 * ease(clamp((T - 15.4) / 1.0))
    bag(ctx, W / 2 - 60, 760, 1.15, T, col=RIV, level=lv, puff=0.1)
    worker(ctx, 900, 860, 0.7, T, col=RIV, k=2, mood="feliz", hat=(0.95, 0.95, 0.95))
    if T > 17.70:
        for k in range(3):
            icon(ctx, "❤️", 180 + k * 120, 380 - 30 * math.sin(T * 3 + k), 100, pop(lt, 17.70 - 14.64 + 0.15 * k))
    ctx.restore()
    label(ctx, "RIVAL", 900, 520, pop(lt, 0.2), rgb=RIV, size=40)
    label(ctx, "FULL TO THE TOP", W / 2, 260, pop(lt, 16.46 - 14.64), rgb=YELLOW, size=50)


# 18.85 "Then the trucks start rolling. Potholes. Boxes stacked six high."
def e6(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 860)
    sky(ctx, T, P)
    ground(ctx, 1150, P, col=P["road"])
    for k in range(-2, 10):
        ctx.rectangle(k * 200 - (T * 500) % 200, 1230, 100, 14); fill(ctx, YELLOW)
    ellipse(ctx, 640 - (T * 500) % 1400 + 700, 1180, 70, 16); fill(ctx, (0.15, 0.15, 0.2))
    nb = min(6, int(clamp((T - 20.95) / 1.2) * 6 + (0.99 if T > 20.95 else 0)))
    truck(ctx, W / 2, 1150, 1.15, T, boxes=nb, bump=1.0 if T > 20.27 else 0.3)
    ctx.restore()
    label(ctx, "POTHOLES", 260, 330, pop(lt, 20.27 - 18.85), rgb=RED, size=48)
    if T > 20.95:
        label(ctx, f"{max(nb,1)} BOXES HIGH", 800, 330, 1.0, rgb=YELLOW, size=44)


# 22.56 "Their bags arrive as crumbs. And the ones that survive taste stale a few weeks later. The kid's chips still crunch like day one."
def e7(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 860)
    sky(ctx, T, P)
    ground(ctx, 1200, P)
    bag(ctx, 300, 800, 0.95, T, col=RIV, level=0.2, puff=0.0, crumbs=True, stale=ease(clamp((T - 25.2) / 0.8)))
    a = pop(lt, 26.59 - 22.56)
    if a > 0.01:
        bag(ctx, 790, 790, 0.95 * a, T, col=KID, level=0.32, puff=1.0)
    ctx.restore()
    label(ctx, "CRUMBS", 300, 330, pop(lt, 23.39 - 22.56), rgb=RED, size=48)
    if T > 25.18:
        label(ctx, "STALE", 300, 1290, pop(lt, 25.43 - 22.56), rgb=(0.62, 0.58, 0.45), size=46)
        cal(ctx, 300, 470, 0.45, "LATER", "3 WEEKS", col=RED)
    if T > 27.73:
        stamp(ctx, "CRUNCH!", 790, 330, (T - 27.73) / 0.25, col=(0.30, 0.78, 0.40), size=80)
        check(ctx, 790, 1290, 0.9, pop(lt, 27.8 - 22.56), ok=True)


# 28.73 "You see, the oxygen in air slowly ruins the oil in chips. Nitrogen pushes the oxygen out."  (luz azul)
def e8(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 820)
    sky(ctx, T, P, sun=True)
    dull = ease(clamp((T - 30.5) / 1.2)) * (1 - ease(clamp((T - 33.0) / 0.8)))
    chip(ctx, W / 2, 820, 4.0, 0.0, mix(CHIP, (0.62, 0.58, 0.45), dull))
    push = ease(clamp((T - 32.4) / 1.2))
    rng = np.random.default_rng(3)
    for k in range(7):
        ang = rng.uniform(0, math.tau); r = 250 + 40 * math.sin(T * 2 + k)
        ox, oy = W / 2 + math.cos(ang) * r * (1 + 1.6 * push), 820 + math.sin(ang) * r * (1 + 1.6 * push)
        molecule(ctx, ox, oy, 50, O2C, "O₂")
    if T > 32.12:
        for k in range(8):
            ang = k * math.tau / 8 + T * 0.3; r = 330
            molecule(ctx, W / 2 + math.cos(ang) * r * ease(clamp((T - 32.12) / 0.8)), 820 + math.sin(ang) * r * ease(clamp((T - 32.12) / 0.8)), 50, N2C, "N₂")
    ctx.restore()
    label(ctx, "OXYGEN RUINS THE OIL", W / 2, 260, pop(lt, 30.73 - 28.73), rgb=O2C, size=44)
    if T > 32.12:
        label(ctx, "NITROGEN PUSHES IT OUT", W / 2, 1290, pop(lt, 32.12 - 28.73), rgb=N2C, size=42)


# 33.97 "And the gas puffs up the bag like a pillow. Like bubble wrap around a phone."
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 860)
    sky(ctx, T, P)
    pf = ease_back(clamp((T - 34.4) / 0.8))
    bag(ctx, 330, 800, 1.0, T, level=0.32, puff=pf)
    a = pop(lt, 36.25 - 33.97)
    if a > 0.01:
        ctx.save(); ctx.translate(790, 800); ctx.scale(a, a)
        rrect(ctx, -190, -280, 380, 560, 60); fill_ink(ctx, (0.80, 0.92, 1.0), 4, a=0.5)
        for i in range(5):
            for j in range(7):
                circle(ctx, -150 + i * 75, -240 + j * 80, 26); fill_ink(ctx, (0.9, 0.97, 1.0), 2, a=0.7)
        rrect(ctx, -110, -200, 220, 400, 30); fill_ink(ctx, (0.18, 0.18, 0.24), 5)
        rrect(ctx, -90, -170, 180, 330, 16); fill(ctx, (0.35, 0.55, 0.95))
        ctx.restore()
    ctx.restore()
    label(ctx, "LIKE A PILLOW", 330, 300, pop(lt, 35.70 - 33.97), rgb=YELLOW, size=44)
    label(ctx, "BUBBLE WRAP", 790, 300, pop(lt, 36.43 - 33.97), rgb=(0.45, 0.72, 1.0), size=44)


# 37.36 "In other words, he wasn't selling air. He was selling crunch."
def e10(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.08, dur=dur), W / 2, 820)
    sky(ctx, T, P)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.22); ctx.paint()
    bag(ctx, W / 2, 800, 1.3, T, level=0.32, puff=1.0)
    ctx.restore()
    if T > 38.8:
        stamp(ctx, "NOT AIR", W / 2, 300, (T - 38.8) / 0.25, size=100)
    if T > 39.7:
        stamp(ctx, "CRUNCH", W / 2, 1260, (T - 39.7) / 0.25, col=(0.30, 0.78, 0.40), size=110)


# 40.70 "That's why every bag of chips you open feels half empty."
def e11(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 860), sky(c, T, P), house2(c, 300, 1100, 1.2), ground(c, 1100, P)))
    ctx.save()
    camera(ctx, z, W / 2, 860)
    bag(ctx, W / 2 + 40, 800, 1.2, T, col=(0.95, 0.60, 0.15), level=0.32, puff=1.0)
    ctx.restore()
    label(ctx, "YOUR CHIPS", W / 2, 280, pop(lt, 41.74 - 40.70), rgb=YELLOW, size=52)
    a = pop(lt, 42.77 - 40.70)
    if a > 0.01:
        label(ctx, "NITROGEN", 230, 560, a, rgb=N2C, size=42)
        arrow(ctx, 300, 600, 440, 620, a, rgb=N2C, w=10)


# 43.76 "Because, just like"  -> bucle
def e12(ctx, lt, dur, T):
    hero(ctx, lt, T, dur, 0.95, 1.0)


ESCENAS = [(0.0, e1), (3.35, e2), (7.99, e3), (12.07, e4), (14.64, e5), (18.85, e6), (22.56, e7), (28.73, e8),
           (33.97, e9), (37.36, e10), (40.70, e11), (43.76, e12)]

SFX = [(0.1, "squish"), (3.3, "whoosh"), (5.2, "pop"), (7.3, "ding"), (7.95, "whoosh"), (8.9, "crack"), (10.5, "drum"),
       (12.6, "squish"), (14.0, "ding"), (14.6, "whoosh"), (15.6, "pop"), (17.7, "pop"), (18.8, "whoosh"),
       (20.27, "thud"), (21.2, "tick"), (21.5, "tick"), (21.8, "tick"), (22.5, "whoosh"), (23.39, "crack"),
       (25.4, "ding"), (27.73, "crack"), (28.7, "whoosh"), (30.7, "rise"), (32.4, "squish"), (34.4, "squish"),
       (36.3, "pop"), (37.33, "thud"), (38.8, "thud"), (39.7, "thud"), (40.65, "whoosh"), (42.8, "pop"), (43.7, "whoosh")]


def MINIATURA(ctx):
    T = 0.5
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    sky(ctx, T, P)
    ground(ctx, 1500, P)
    bag(ctx, W / 2, 1050, 1.6, T, level=0.30, puff=1.0)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["WHY IS IT", ("HALF EMPTY?", WHITE)], y=260, size=170)
    thumb_circle(ctx, W / 2, 830, 260, 150)
