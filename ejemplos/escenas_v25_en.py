"""v25 (EN) FORMATO BUCLE: Nikola Tesla and the white pigeon he loved (O'Neill; died 1922)."""
from kit import *  # noqa

ELEC = (0.45, 0.85, 1.0)
GREY = (0.55, 0.58, 0.66)
PIGEON_W = (0.97, 0.97, 1.0)
BRICK = (0.45, 0.22, 0.18)


def pigeon(ctx, x, y, s=1.0, T=0.0, col=GREY, flip=False, flap=0.0, glow=0.0, eye_beam=0.0):
    """Paloma de perfil. flap 0..1 = alas abiertas (volando)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    if glow > 0:
        spotlight(ctx, 0, 0, 320, 0.4 * glow, (1, 1, 0.9))
    dark = tuple(c * 0.75 for c in col)
    # cola
    ctx.move_to(-110, 10); ctx.line_to(-230, -10); ctx.line_to(-230, 50); ctx.close_path(); fill(ctx, dark)
    # cuerpo
    ellipse(ctx, 0, 20, 140, 90); fill(ctx, col)
    # ala
    ctx.save(); ctx.translate(-10, 0); ctx.rotate(-1.4 * flap * (0.6 + 0.4 * math.sin(T * 18)))
    ctx.move_to(60, 0); ctx.curve_to(20, -60, -120, -40, -170, 10); ctx.curve_to(-90, 50, 20, 50, 60, 0); fill(ctx, dark)
    for k in range(3):
        ctx.move_to(-60 - k * 35, 10); ctx.line_to(-90 - k * 35, 35); stroke(ctx, tuple(c * 0.6 for c in col), 4)
    ctx.restore()
    # cuello y cabeza
    ellipse(ctx, 95, -50, 55, 70); fill(ctx, col)
    if col == GREY:
        ellipse(ctx, 100, -15, 45, 30); fill(ctx, (0.35, 0.60, 0.55), 0.8)
    circle(ctx, 120, -100, 52); fill(ctx, col)
    ctx.move_to(165, -105); ctx.line_to(215, -92); ctx.line_to(165, -82); ctx.close_path(); fill(ctx, (0.95, 0.70, 0.45))
    circle(ctx, 135, -112, 12); fill(ctx, (0.95, 0.45, 0.15)); circle(ctx, 137, -112, 6); fill(ctx, (0.05, 0.05, 0.05))
    if eye_beam > 0:
        for k in range(3):
            ctx.move_to(140, -112); ctx.line_to(900, -112 - 160 + k * 160); ctx.line_to(900, -112 - 100 + k * 160); ctx.close_path()
            fill(ctx, (1, 0.95, 0.55), 0.55 * eye_beam)
        spotlight(ctx, 137, -112, 120, 0.9 * eye_beam, (1, 1, 0.9))
    # patas
    for px in (-20, 30):
        ctx.move_to(px, 100); ctx.line_to(px, 140); stroke(ctx, (0.95, 0.45, 0.45), 8)
    ctx.restore()


def bulb(ctx, x, y, s=1.0, on=1.0, T=0.0, col=YELLOW):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if on > 0:
        spotlight(ctx, 0, -40, 360, 0.5 * on, (1, 0.95, 0.7))
    circle(ctx, 0, -60, 150)
    ctx.set_source_rgba(*(c * (0.4 + 0.6 * on) for c in col), 0.95); ctx.fill()
    ctx.move_to(-60, 60); ctx.line_to(60, 60); ctx.line_to(55, 110); ctx.line_to(-55, 110); ctx.close_path(); fill(ctx, (1, 0.95, 0.8), 0.7)
    for k in range(4):
        rrect(ctx, -65, 110 + k * 26, 130, 20, 8); fill(ctx, STONE)
    ctx.move_to(-40, 60); ctx.line_to(-30, -60); ctx.line_to(-10, -30); ctx.line_to(10, -70); ctx.line_to(30, -30); ctx.line_to(40, 60)
    stroke(ctx, (1, 1, 1) if on > 0.5 else (0.4, 0.35, 0.3), 6)
    circle(ctx, -60, -120, 35); fill(ctx, WHITE, 0.4)
    ctx.restore()


def tesla_coil(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -110, 0, 220, 60, 10); fill(ctx, WOOD)
    rrect(ctx, -45, -420, 90, 420, 20); fill(ctx, (0.75, 0.45, 0.20))
    for k in range(22):
        ctx.move_to(-45, -410 + k * 18); ctx.line_to(45, -405 + k * 18); stroke(ctx, (0.95, 0.65, 0.30), 4)
    ellipse(ctx, 0, -470, 120, 55); fill(ctx, (0.78, 0.80, 0.86))
    rng = np.random.default_rng(int(T * 12))
    for k in range(5):
        ctx.move_to(0, -470); a = rng.uniform(math.pi, math.tau); px, py = 0, -470
        for j in range(5):
            px += math.cos(a) * 50 + rng.uniform(-25, 25); py += math.sin(a) * 50 + rng.uniform(-25, 25); ctx.line_to(px, py)
        stroke(ctx, ELEC, 5, 0.9)
    ctx.restore()


def outlet(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -170, -250, 340, 500, 30); fill_keep(ctx, (0.95, 0.94, 0.90)); stroke(ctx, (0.7, 0.7, 0.68), 6)
    for yy in (-110, 110):
        rrect(ctx, -110, yy - 80, 220, 160, 60); fill(ctx, (0.88, 0.87, 0.83))
        rrect(ctx, -60, yy - 45, 22, 70, 6); fill(ctx, INK); rrect(ctx, 38, yy - 45, 22, 70, 6); fill(ctx, INK)
        circle(ctx, 0, yy + 45, 16); fill(ctx, INK)
    ctx.restore()
    rng = np.random.default_rng(int(T * 10))
    for k in range(4):
        px, py = x + 60 * s, y - 110 * s
        ctx.move_to(px, py)
        for j in range(4):
            px += rng.uniform(20, 60); py += rng.uniform(-50, 50); ctx.line_to(px, py)
        stroke(ctx, ELEC, 6, 0.85)


def skyline(ctx, T, y0=1300, col=(0.10, 0.10, 0.20)):
    rng = np.random.default_rng(4)
    x = -200
    while x < W + 200:
        w = rng.uniform(90, 180); h = rng.uniform(250, 700)
        ctx.rectangle(x, y0 - h, w, h + 600); fill(ctx, col)
        for wy in range(int(y0 - h + 30), y0, 60):
            for wx in range(int(x + 15), int(x + w - 20), 40):
                if rng.random() < 0.35:
                    ctx.rectangle(wx, wy, 18, 26); fill(ctx, (1, 0.85, 0.5), 0.6)
        x += w + 10


def hotel_facade(ctx, x, y, s, T, label="HOTEL", open_win=True, col=BRICK):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-330, -600, 660, 1200); fill(ctx, col)
    rrect(ctx, -200, -700, 400, 90, 14); fill(ctx, (0.10, 0.08, 0.10))
    text(ctx, label, 0, -655, 58, GOLD, shadow=False)
    for r in range(4):
        for c in range(3):
            wx, wy = -220 + c * 220, -480 + r * 260
            rrect(ctx, wx - 70, wy - 90, 140, 180, 8); fill(ctx, (1, 0.85, 0.5), 0.75)
            if open_win and (r, c) == (1, 1):
                ctx.move_to(wx - 70, wy - 90); ctx.line_to(wx - 150, wy - 70); ctx.line_to(wx - 150, wy + 110); ctx.line_to(wx - 70, wy + 90)
                ctx.close_path(); fill_keep(ctx, GLASS, 0.4); stroke(ctx, WHITE, 5)
                rrect(ctx, wx - 70, wy - 90, 140, 180, 8); fill(ctx, (0.15, 0.12, 0.10))
            ctx.rectangle(wx - 80, wy + 90, 160, 14); fill(ctx, (0.85, 0.82, 0.78))
    ctx.restore()


def nest(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 330, 110); fill(ctx, (0.45, 0.32, 0.18))
    rng = np.random.default_rng(2)
    for k in range(40):
        a = rng.uniform(0, math.tau); r = rng.uniform(0.6, 1.0)
        ctx.move_to(math.cos(a) * 330 * r, math.sin(a) * 110 * r)
        ctx.line_to(math.cos(a + 0.5) * 330 * r, math.sin(a + 0.5) * 110 * r)
        stroke(ctx, (0.65, 0.48, 0.26), 6)
    ctx.restore()


def heart(ctx, x, y, s=1.0, col=RED, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 60); ctx.curve_to(-160, -40, -90, -170, 0, -80); ctx.curve_to(90, -170, 160, -40, 0, 60)
    fill(ctx, col, a)
    ctx.restore()


def quote_card(ctx, x, y, lines, appear=1.0, size=58):
    if appear <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(appear, appear)
    h = len(lines) * size * 1.3 + 90
    rrect(ctx, -440, -h / 2, 880, h, 30); fill_keep(ctx, PAPER); stroke(ctx, GOLD, 6)
    text(ctx, "“", -380, -h / 2 + 70, 140, GOLD, shadow=False)
    for i, ln in enumerate(lines):
        text(ctx, ln, 0, -h / 2 + 75 + i * size * 1.3, size, INK, shadow=False)
    ctx.restore()


def bg_elec(ctx, T):
    bg_dark(ctx, T, top=(0.02, 0.05, 0.12), mid=(0.05, 0.14, 0.28))


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): paloma blanca brillando + bobina de Tesla + ficha."""
    camera(ctx, zoom, W / 2, 760)
    bg_elec(ctx, T)
    rays(ctx, W / 2 + 80, 560, T, (0.8, 0.95, 1.0), 0.05)
    tesla_coil(ctx, 200, 1080, 0.9, T)
    pigeon(ctx, W / 2 + 120, 640, 1.5, T, col=PIGEON_W, glow=1.0)
    heart(ctx, W / 2 + 300, 330 + 10 * math.sin(T * 4), 0.7 + 0.05 * math.sin(T * 8))
    ctx.restore(); ctx.save()
    ficha(ctx, "NIKOLA TESLA", "INVENTOR · 1856–1943", W / 2, 1470, 1.0, "⚡", ELEC)


# 0.00 "Nikola Tesla fell in love with a pigeon."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 2.78 "A white one."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (dur, 1.45)]), W / 2 + 100, 600)
    bg_dark(ctx, T, top=(0.06, 0.06, 0.12), mid=(0.14, 0.14, 0.26))
    pigeon(ctx, W / 2, 680, 1.6, T, col=PIGEON_W, glow=1.0)


# 3.48 "And it's real."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 760)
    bg_dark(ctx, T)
    newspaper(ctx, W / 2, 640, 0.9, "TESLA\nAND THE\nPIGEONS", "", rot=0.04, date="NEW YORK")
    badge(ctx, "100% REAL", W / 2, 1400, pop(lt, 0.2), size=70)


# 4.57 "Tesla, the genius behind the AC power in your walls,"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.80, 0.74, 0.62)), (1, (0.62, 0.55, 0.45))])); ctx.paint()
    outlet(ctx, W / 2, 620, 1.1, T)
    pill(ctx, "AC POWER", W / 2, 230, pop(lt, 1.5), size=60, rgb=ELEC)
    ctx.restore(); ctx.save()
    ficha(ctx, "NIKOLA TESLA", "INVENTOR · AC ELECTRICITY", W / 2, 1470, pop(lt, 0.2), "⚡", ELEC)


# 7.83 "spent hours every week feeding pigeons in New York."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 820)
    bg_sky(ctx, T, warm=0.5)
    skyline(ctx, T, 1150, (0.30, 0.32, 0.45))
    ground(ctx, 1150, (0.30, 0.50, 0.30))
    gent(ctx, 260, 620, 0.85, hat=True)
    for k in range(int(7 * clamp(lt / 1.2))):
        circle(ctx, 360 + k * 60, 1170 + 20 * math.sin(k * 2), 8); fill(ctx, (0.9, 0.8, 0.5))
    for k, (px, fl) in enumerate(((520, False), (720, True), (880, False))):
        pigeon(ctx, px, 1080 + 10 * math.sin(T * 6 + k), 0.55, T, flip=fl)
    pill(ctx, "NEW YORK", W / 2, 300, pop(lt, 1.8), size=56, rgb=GOLD)


# 10.61 "He left his hotel windows open, so the birds could fly in."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.25)]), W / 2, 700)
    bg_night(ctx, T, grid=False)
    hotel_facade(ctx, W / 2, 960, 1.0, T)
    for k in range(3):
        p = clamp((lt - 0.5 - k * 0.5) / 1.2)
        if p > 0:
            pigeon(ctx, 1150 - 600 * p, 300 + k * 70 + 140 * p, 0.45, T + k, flip=True, flap=1.0)


# 13.82 "Hotels kicked Tesla out, one after another."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_night(ctx, T, grid=False)
    for k, (hx, lab, col) in enumerate(((180, "HOTEL", (0.40, 0.20, 0.22)), (540, "HOTEL", BRICK), (900, "HOTEL", (0.30, 0.26, 0.40)))):
        hotel_facade(ctx, hx, 1050, 0.5, T, lab, open_win=False, col=col)
        stamp(ctx, "OUT", hx, 700, (lt - 0.4 - 0.6 * k) / 0.25, size=90)
    gent(ctx, W / 2, 1220, 0.45, hat=True)


# 16.64 "In other words,"  (2.º gancho)
def e8(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur), W / 2, 700)
    bg_dark(ctx, T, top=(0.22, 0.03, 0.06), mid=(0.12, 0.02, 0.05))
    rays(ctx, W / 2, 640, T, RED, 0.08)
    bulb(ctx, W / 2, 700, 1.4, 1.0, T)


# 17.52 "the man who lit up the world"
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_night(ctx, T, grid=False)
    circle(ctx, W / 2, 680, 360); fill(ctx, (0.10, 0.22, 0.45))
    rng = np.random.default_rng(9)
    n = int(40 * clamp(lt / 1.2))
    for k in range(40):
        a = rng.uniform(0, math.tau); r = math.sqrt(rng.uniform(0, 1)) * 330
        if k < n:
            circle(ctx, W / 2 + math.cos(a) * r, 680 + math.sin(a) * r, 9); fill(ctx, (1, 0.9, 0.5))
    ctx.new_path(); ctx.arc(W / 2, 680, 360, 0, math.tau); stroke(ctx, ELEC, 6, 0.6)
    pill(ctx, "LIT UP THE WORLD", W / 2, 230, pop(lt, 0.3), size=50, rgb=YELLOW)


# 19.12 "lived in a pigeon nest."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.2)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.10, 0.08, 0.04), mid=(0.20, 0.16, 0.08))
    nest(ctx, W / 2, 700, 1.2, T)
    character(ctx, W / 2, 600, 0.75, T, mood="sorpresa")
    for k, (px, py, fl) in enumerate(((220, 420, False), (860, 470, True), (300, 300, True))):
        pigeon(ctx, px, py + 15 * math.sin(T * 5 + k), 0.5, T, flip=fl, flap=1.0 if k == 2 else 0.0)
    stamp(ctx, "PIGEON NEST", W / 2, 1150, (lt - 0.5) / 0.3, size=90)


# 20.69 "But one bird was special. A white pigeon."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.25)]), W / 2, 680)
    bg_dark(ctx, T, top=(0.04, 0.04, 0.10), mid=(0.10, 0.10, 0.20))
    for k, (px, py, fl) in enumerate(((180, 820, False), (900, 800, True), (260, 400, True), (850, 380, False))):
        pigeon(ctx, px, py, 0.5, T + k, flip=fl)
    pigeon(ctx, W / 2, 620, 1.1, T, col=PIGEON_W, glow=clamp(lt / 1.0))
    if lt > 1.3:
        thumb_circle(ctx, W / 2 + 20, 600, 300, 220, YELLOW, 12)


# 22.96 "Tesla told his biographer,"
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.12), mid=(0.14, 0.12, 0.24))
    gent(ctx, 300, 440, 0.9, hat=False, col=(0.12, 0.12, 0.20))
    gent(ctx, 780, 460, 0.85, hat=True, col=(0.16, 0.14, 0.24))
    icon(ctx, "📝", 780, 820, 180, pop(lt, 0.3))
    icon(ctx, "💬", 420, 250, 160, pop(lt, 0.1))
    ctx.restore(); ctx.save()
    ficha(ctx, "JOHN J. O'NEILL", "TESLA'S BIOGRAPHER · JOURNALIST", W / 2, 1470, pop(lt, 0.5), "📖", GOLD)


# 24.49 "I loved that pigeon as a man loves a woman."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.18, 0.04, 0.12), mid=(0.32, 0.08, 0.22))
    for k in range(6):
        hy = 1500 - ((T * 140 + k * 260) % 1400)
        heart(ctx, 120 + k * 170, hy, 0.4, (1, 0.45, 0.6), 0.5)
    pigeon(ctx, W / 2, 1220, 0.8, T, col=PIGEON_W, glow=0.6)
    quote_card(ctx, W / 2, 480, ["I LOVED THAT PIGEON", "AS A MAN", "LOVES A WOMAN"], pop(lt, 0.1), size=58)


# 27.18 "In 1922, she flew into his room to die."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.04, 0.04, 0.10), mid=(0.10, 0.10, 0.20))
    rrect(ctx, W / 2 - 260, 360, 520, 640, 10); fill(ctx, (0.15, 0.20, 0.40))
    for k in range(20):
        circle(ctx, W / 2 - 240 + (k * 97) % 480, 380 + (k * 61) % 600, 4); fill(ctx, WHITE, 0.7)
    ctx.rectangle(W / 2 - 280, 360, 20, 640); fill(ctx, WOOD); ctx.rectangle(W / 2 + 260, 360, 20, 640); fill(ctx, WOOD)
    ctx.rectangle(W / 2 - 280, 670, 560, 20); fill(ctx, WOOD); ctx.rectangle(W / 2 - 300, 1000, 600, 40); fill(ctx, WOOD_D)
    p = ease_out(clamp(lt / 1.6))
    pigeon(ctx, W / 2 - 60 + 120 * p, 520 + 400 * p, 0.6, T, col=PIGEON_W, flip=False, flap=1 - p, glow=0.5)
    badge(ctx, "1922", W / 2, 260, pop(lt, 0.1), size=90)


# 30.10 "Tesla said a light came from her eyes, brighter than any lamp he ever built."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.02, 0.02, 0.05), mid=(0.05, 0.05, 0.10))
    pigeon(ctx, 260, 640, 1.0, T, col=PIGEON_W, eye_beam=ease(clamp((lt - 0.6) / 0.8)))
    bulb(ctx, 860, 1330, 0.45, 1.0 - 0.7 * clamp((lt - 2.2) / 0.6), T)
    pill(ctx, "BRIGHTER THAN HIS LAMPS", W / 2, 230, pop(lt, 2.4), size=42, rgb=YELLOW)


# 34.49 "Then he said, I knew my life's work was finished."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.03, 0.03, 0.06), mid=(0.07, 0.07, 0.12))
    bulb(ctx, W / 2, 1230, 0.7, 1.0 - clamp((lt - 1.2) / 1.0), T)
    quote_card(ctx, W / 2, 480, ["I KNEW", "MY LIFE'S WORK", "WAS FINISHED"], pop(lt, 0.6), size=62)


# 37.29 "Tesla never married."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.12), mid=(0.14, 0.12, 0.24))
    sc = pop(lt, 0.0)
    ctx.new_path(); ctx.arc(W / 2, 680, 190 * sc, 0, math.tau); stroke(ctx, GOLD, 46 * sc)
    ctx.move_to(W / 2, 400); ctx.line_to(W / 2 + 90 * sc, 470); ctx.line_to(W / 2, 560); ctx.line_to(W / 2 - 90 * sc, 470); ctx.close_path()
    fill_keep(ctx, (0.80, 0.95, 1.0)); stroke(ctx, WHITE, 6)
    p = clamp((lt - 0.4) / 0.25)
    for sx in (-1, 1):
        ctx.move_to(W / 2 - 230, 620 - 230 * sx); ctx.line_to(W / 2 - 230 + 460 * p, 620 - 230 * sx + 460 * p * sx)
        stroke(ctx, RED, 30)
    pill(ctx, "NEVER MARRIED", W / 2, 1400, pop(lt, 0.5), size=56, rgb=RED)


# 38.48 "Maybe because"  → bucle: "Nikola Tesla fell in love with a pigeon."
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.92), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.78, e2), (3.48, e3), (4.57, e4), (7.83, e5), (10.61, e6), (13.82, e7), (16.64, e8),
           (17.52, e9), (19.12, e10), (20.69, e11), (22.96, e12), (24.49, e13), (27.18, e14), (30.10, e15),
           (34.49, e16), (37.29, e17), (38.48, e18)]
SFX = [(14.3, "pop"), (16.66, "ding"), (31.0, "ding"), (37.8, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_elec(ctx, T)
    rays(ctx, W / 2, 1000, T, (0.8, 0.95, 1.0), 0.07)
    tesla_coil(ctx, 210, 1450, 0.9, T)
    pigeon(ctx, W / 2 + 80, 1050, 1.7, T, col=PIGEON_W, glow=1.2)
    heart(ctx, W / 2 + 280, 720, 0.9)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["TESLA'S", ("TRUE LOVE?", WHITE)], y=270, size=180)
    thumb_circle(ctx, W / 2 + 90, 1000, 330, 230)
    ficha(ctx, "NIKOLA TESLA", "INVENTOR · 1856–1943", W / 2, 1640, 1.0, "⚡", ELEC)
