"""v23 (EN) FORMATO BUCLE: Einstein's brain was kept in a cider box in Kansas (Thomas Harvey, 1955-1978)."""
from kit import *  # noqa

PINK = (0.96, 0.62, 0.66)
PINK_D = (0.78, 0.38, 0.46)
FORMOL = (0.95, 0.88, 0.55)
CRATE = (0.62, 0.42, 0.22)
CRATE_D = (0.42, 0.27, 0.13)
GREEN_TOP = (0.03, 0.10, 0.10)
GREEN_MID = (0.07, 0.22, 0.22)


def brain(ctx, x, y, s=1.0, T=0.0, glow=0.0, a=1.0):
    """Cerebro de dibujo (de lado): dos lóbulos rosas con circunvoluciones."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if glow > 0:
        spotlight(ctx, 0, 0, 360, 0.35 * glow, (1.0, 0.75, 0.85))
    soft_shadow(ctx, 0, 190, 210, 30, 0.3 * a)
    ctx.new_path()
    ctx.move_to(-230, 40)
    ctx.curve_to(-260, -120, -120, -210, 0, -190)
    ctx.curve_to(150, -215, 270, -110, 240, 30)
    ctx.curve_to(260, 120, 170, 170, 60, 150)
    ctx.curve_to(20, 200, -60, 190, -90, 150)
    ctx.curve_to(-200, 160, -240, 110, -230, 40)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -200, 0, 180, [(0, (1.0, 0.76, 0.78)), (1, PINK_D)]))
    ctx.fill_preserve(); stroke(ctx, (0.55, 0.22, 0.30), 7, a)
    rng = np.random.default_rng(3)
    for k in range(11):  # circunvoluciones
        cx, cy = rng.uniform(-180, 180), rng.uniform(-140, 110)
        ctx.new_path(); ctx.move_to(cx - 50, cy)
        ctx.curve_to(cx - 25, cy - 40, cx + 5, cy + 35, cx + 30, cy - 5)
        ctx.curve_to(cx + 45, cy - 25, cx + 60, cy + 10, cx + 70, cy - 10)
        stroke(ctx, (0.62, 0.26, 0.36), 6, 0.75 * a)
    ctx.new_path(); ctx.move_to(-10, -185); ctx.curve_to(20, -100, -30, -20, 10, 60); stroke(ctx, (0.55, 0.22, 0.30), 8, a)
    ctx.restore()


def jar(ctx, x, y, s=1.0, T=0.0, content=True, label=None):
    """Tarro de cristal con líquido amarillento y trozos de cerebro."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -150, -230, 300, 460, 50); fill(ctx, FORMOL, 0.35)
    if content:
        for k, (bx, by, bs) in enumerate(((-50, 90, 0.28), (60, 40, 0.24), (-20, -60, 0.22), (55, 130, 0.2))):
            brain(ctx, bx + 6 * math.sin(T * 1.3 + k), by + 5 * math.cos(T + k), bs, T)
    for k in range(5):  # burbujas
        yy = 200 - ((T * 60 + k * 90) % 400)
        circle(ctx, -90 + k * 45, yy, 7); fill(ctx, WHITE, 0.35)
    rrect(ctx, -150, -230, 300, 460, 50); stroke(ctx, GLASS, 8, 0.85)
    rrect(ctx, -165, -290, 330, 70, 16); fill(ctx, STONE)
    rrect(ctx, -165, -290, 330, 20, 10); fill(ctx, WHITE, 0.25)
    rrect(ctx, -110, -180, 26, 330, 13); fill(ctx, WHITE, 0.3)
    if label:
        rrect(ctx, -100, -30, 200, 80, 8); fill(ctx, PAPER)
        text(ctx, label, 0, 10, 36, INK, shadow=False)
    ctx.restore()


def cider_box(ctx, x, y, s=1.0, T=0.0, lid=0.0, jars=True):
    """Caja de madera de sidra; lid 0..1 levanta la tapa y asoman los tarros."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    soft_shadow(ctx, 0, 250, 380, 40, 0.4)
    if jars:
        rise = 140 * ease(clamp(lid))
        jar(ctx, -120, -90 - rise, 0.62, T)
        jar(ctx, 120, -90 - rise, 0.62, T + 1.5)
    ctx.rectangle(-360, -60, 720, 310)
    ctx.set_source(vgrad(ctx, 0, -60, 0, 250, [(0, CRATE), (1, CRATE_D)])); ctx.fill()
    for k in range(3):
        ctx.rectangle(-360, -60 + k * 104, 720, 8); fill(ctx, CRATE_D)
    for sx in (-1, 1):
        ctx.rectangle(sx * 330 - 22, -60, 44, 310); fill(ctx, CRATE_D)
    rrect(ctx, -190, 40, 380, 110, 12); fill(ctx, PAPER, 0.9)
    text(ctx, "CIDER", 0, 98, 78, (0.55, 0.12, 0.10), shadow=False)
    # tapa
    ctx.save(); ctx.translate(-360, -60); ctx.rotate(-1.1 * ease(clamp(lid)))
    ctx.rectangle(0, -36, 720, 36); fill(ctx, CRATE)
    ctx.rectangle(0, -8, 720, 8); fill(ctx, CRATE_D)
    ctx.restore()
    ctx.restore()


def beer_cooler(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -320, -200, 640, 360, 40)
    ctx.set_source(vgrad(ctx, 0, -200, 0, 160, [(0, (0.85, 0.20, 0.20)), (1, (0.55, 0.08, 0.10))])); ctx.fill()
    rrect(ctx, -340, -230, 680, 80, 30); fill(ctx, WHITE)
    rrect(ctx, -120, -290, 240, 50, 20); stroke(ctx, (0.85, 0.85, 0.9), 14)
    text(ctx, "BEER", 0, 0, 90, WHITE)
    ctx.restore()


def hospital(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-420, -420, 840, 620); fill(ctx, (0.80, 0.82, 0.88))
    ctx.rectangle(-420, -460, 840, 50); fill(ctx, (0.55, 0.58, 0.68))
    for r in range(3):
        for c in range(5):
            rrect(ctx, -360 + c * 150, -360 + r * 150, 110, 100, 8)
            fill(ctx, (1, 0.85, 0.5), 0.8 if (r + c) % 3 else 0.3)
    rrect(ctx, -90, 60, 180, 140, 10); fill(ctx, (0.25, 0.30, 0.45))
    rrect(ctx, -70, -620, 140, 140, 16); fill(ctx, WHITE)
    ctx.rectangle(-18, -600, 36, 100); fill(ctx, RED); ctx.rectangle(-50, -568, 100, 36); fill(ctx, RED)
    ctx.restore()


def coat_man(ctx, x, y, s=1.0, T=0.0):
    """Silueta genérica con bata blanca (patólogo), sin rasgos."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -160, 120, 320, 540, 110); fill(ctx, (0.93, 0.94, 0.97))
    ctx.move_to(0, 130); ctx.line_to(-40, 300); ctx.line_to(0, 640); ctx.line_to(40, 300); ctx.close_path(); fill(ctx, (0.25, 0.28, 0.40))
    circle(ctx, 0, 0, 100); fill(ctx, (0.18, 0.18, 0.26))
    rrect(ctx, -80, 210, 70, 90, 8); stroke(ctx, (0.7, 0.72, 0.8), 4)
    ctx.restore()


def eyeball(ctx, x, y, r, T, look=(0.0, 0.0)):
    ox, oy = look[0] * r * 0.25, look[1] * r * 0.25
    soft_shadow(ctx, x, y + r * 1.02, r * 0.8, r * 0.12, 0.35)
    circle(ctx, x, y, r)
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.35, r * 0.1, x, y, r)
    g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(1, 0.80, 0.76, 0.74)
    ctx.set_source(g); ctx.fill()
    circle(ctx, x + ox, y + oy, r * 0.45); fill(ctx, (0.45, 0.32, 0.18))
    circle(ctx, x + ox, y + oy, r * 0.2); fill(ctx, (0.02, 0.02, 0.05))
    circle(ctx, x + ox - r * 0.14, y + oy - r * 0.16, r * 0.08); fill(ctx, WHITE, 0.9)


def car(ctx, x, y, s=1.0, T=0.0, col=(0.20, 0.45, 0.80)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -260, -60, 520, 120, 40); fill(ctx, col)
    ctx.move_to(-150, -60); ctx.line_to(-90, -150); ctx.line_to(110, -150); ctx.line_to(170, -60); ctx.close_path(); fill(ctx, col)
    ctx.move_to(-120, -65); ctx.line_to(-80, -130); ctx.line_to(0, -130); ctx.line_to(0, -65); ctx.close_path(); fill(ctx, GLASS, 0.8)
    ctx.move_to(20, -65); ctx.line_to(20, -130); ctx.line_to(100, -130); ctx.line_to(140, -65); ctx.close_path(); fill(ctx, GLASS, 0.8)
    for wx in (-150, 150):
        ctx.save(); ctx.translate(wx, 60); ctx.rotate(T * 8)
        circle(ctx, 0, 0, 55); fill(ctx, (0.08, 0.08, 0.1)); circle(ctx, 0, 0, 24); fill(ctx, STONE)
        ctx.rectangle(-4, -24, 8, 48); fill(ctx, (0.3, 0.3, 0.35))
        ctx.restore()
    ctx.restore()


def road_sign(ctx, x, y, s, label, sub=""):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-14, 0, 28, 380); fill(ctx, STONE)
    rrect(ctx, -230, -170, 460, 190, 20); fill_keep(ctx, (0.10, 0.45, 0.25)); stroke(ctx, WHITE, 8)
    text(ctx, label, 0, -80, 80, WHITE, shadow=False)
    if sub:
        text(ctx, sub, 0, -20, 36, WHITE, shadow=False)
    ctx.restore()


def slide(ctx, x, y, s=1.0, rot=0.0):
    """Portaobjetos con una lámina fina de cerebro."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -220, -70, 440, 140, 10); fill_keep(ctx, GLASS, 0.35); stroke(ctx, WHITE, 4, 0.8)
    rrect(ctx, -200, -55, 110, 110, 6); fill(ctx, PAPER)
    ctx.save(); ctx.translate(60, 0); ctx.scale(0.3, 0.22); brain(ctx, 0, 0, 1.0); ctx.restore()
    ctx.restore()


def bg_green(ctx, T):
    bg_dark(ctx, T, top=GREEN_TOP, mid=GREEN_MID)


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): caja de sidra abierta con los tarros + ficha de Einstein."""
    camera(ctx, zoom, W / 2, 760)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.13, 0.08))
    rays(ctx, W / 2, 520, T, (1.0, 0.85, 0.5), 0.05)
    spotlight(ctx, W / 2, 640, 520, 0.35, (1, 0.9, 0.6))
    cider_box(ctx, W / 2, 900, 1.05, T, lid=1.0)
    ctx.restore(); ctx.save()
    ficha(ctx, "ALBERT EINSTEIN", "PHYSICIST · 1879–1955", W / 2, 1470, 1.0, "🧠", PINK)


# 0.00 "Albert Einstein's brain was kept in a cider box in Kansas."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 2.86 "Kansas."  (+ "In two jars." a 3.55 en e3)
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 760)
    bg_sky(ctx, T, warm=0.3)
    ground(ctx, 1250, (0.55, 0.48, 0.20))
    for k in range(8):
        ctx.rectangle(-200, 1270 + k * 45, W + 400, 14); fill(ctx, (0.70, 0.60, 0.25), 0.6)
    # silueta simple de Kansas (rectángulo con esquina NE recortada)
    ctx.save(); ctx.translate(W / 2, 640)
    ctx.move_to(-380, -200); ctx.line_to(300, -200); ctx.line_to(340, -150); ctx.line_to(380, -110)
    ctx.line_to(380, 200); ctx.line_to(-380, 200); ctx.close_path()
    fill_keep(ctx, (0.35, 0.65, 0.40)); stroke(ctx, WHITE, 8)
    ctx.restore()
    pin(ctx, W / 2 + 60, 650, 1.0, drop=lt / 0.4)
    pill(ctx, "KANSAS, USA", W / 2, 400, pop(lt, 0.1), size=56, rgb=GOLD)


# 3.55 "In two jars."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 700)
    bg_green(ctx, T)
    spotlight(ctx, W / 2, 600, 600, 0.3)
    jar(ctx, W / 2 - 210, 640, 1.0 * pop(lt, 0.0), T)
    jar(ctx, W / 2 + 210, 640, 1.0 * pop(lt, 0.3), T + 2)
    badge(ctx, "2 JARS", W / 2, 260, pop(lt, 0.4), size=70)


# 4.62 "And it's real."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 760)
    bg_dark(ctx, T)
    newspaper(ctx, W / 2, 660, 0.95, "EINSTEIN'S\nBRAIN\nFOUND", "IN A CIDER BOX", rot=-0.05, date="1978")
    badge(ctx, "100% REAL", W / 2, 1420, pop(lt, 0.2), size=70)


# 5.54 "April 18, 1955."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.04, 0.04, 0.10), mid=(0.10, 0.10, 0.22))
    ctx.save(); ctx.translate(W / 2, 620); ctx.scale(1.2, 1.2)
    rrect(ctx, -230, -200, 460, 420, 24); fill(ctx, WHITE)
    rrect(ctx, -230, -200, 460, 100, 24); fill(ctx, RED)
    text(ctx, "APRIL", 0, -150, 54, WHITE, shadow=False)
    text(ctx, "18", 0, 20, 160, INK, shadow=False)
    text(ctx, str(int(counter(lt, 1900, 1955, 0.8))), 0, 160, 54, (0.4, 0.4, 0.45), shadow=False)
    ctx.restore()


# 7.45 "Einstein dies at Princeton Hospital."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 760)
    bg_night(ctx, T, grid=False)
    ground(ctx, 1150, (0.10, 0.10, 0.18))
    hospital(ctx, W / 2, 900, 1.0, T)
    pill(ctx, "PRINCETON HOSPITAL", W / 2, 250, pop(lt, 0.9), size=46, rgb=TEAL)
    ctx.restore(); ctx.save()
    ficha(ctx, "ALBERT EINSTEIN", "DIED · APRIL 18, 1955 · AGE 76", W / 2, 1480, pop(lt, 0.2), "🧠", PINK)


# 9.35 "The pathologist on duty is Thomas Harvey."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.04, 0.08, 0.12), mid=(0.08, 0.16, 0.24))
    spotlight(ctx, W / 2, 520, 450, 0.3, (0.8, 0.95, 1.0))
    coat_man(ctx, W / 2, 380, 1.0, T)
    pill(ctx, "ON DUTY", 860, 300, pop(lt, 0.3), size=44, rgb=TEAL)
    ctx.restore(); ctx.save()
    ficha(ctx, "THOMAS HARVEY", "PATHOLOGIST · 1912–2007", W / 2, 1470, pop(lt, 0.9), "🔬", TEAL)


# 11.60 "During the autopsy, Harvey takes out Einstein's brain."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.04, 0.08, 0.12), mid=(0.08, 0.16, 0.24))
    # lámpara quirúrgica
    ctx.move_to(W / 2 - 160, 180); ctx.line_to(W / 2 + 160, 180); ctx.line_to(W / 2 + 90, 120); ctx.line_to(W / 2 - 90, 120); ctx.close_path()
    fill(ctx, (0.7, 0.75, 0.85))
    spotlight(ctx, W / 2, 620, 500, 0.45, (0.9, 0.97, 1.0))
    # bandeja metálica
    rrect(ctx, W / 2 - 330, 800, 660, 70, 30); fill(ctx, (0.7, 0.72, 0.78))
    up = ease(clamp((lt - 1.0) / 1.2))
    brain(ctx, W / 2, 700 - 120 * up, 1.0, T, glow=up)


# 14.62 "Nobody asked his family first."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.08, 0.06, 0.12), mid=(0.16, 0.12, 0.22))
    for k, (gx, gs) in enumerate(((W / 2 - 280, 0.8), (W / 2, 0.95), (W / 2 + 280, 0.75))):
        gent(ctx, gx, 520 + (1 - gs) * 200, gs, hat=(k == 1))
        icon(ctx, "❓", gx, 280 + (1 - gs) * 200, 170, pop(lt, 0.2 + 0.2 * k))
    stamp(ctx, "NO PERMISSION", W / 2, 1300, (lt - 0.4) / 0.3, size=80)


# 16.22 "In other words,"  (2.º gancho)
def e10(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur), W / 2, 700)
    bg_dark(ctx, T, top=(0.22, 0.03, 0.06), mid=(0.12, 0.02, 0.05))
    rays(ctx, W / 2, 640, T, RED, 0.08)
    brain(ctx, W / 2, 640, 1.25 + 0.03 * math.sin(T * 20), T, glow=0.6)


# 17.05 "he stole Einstein's brain."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.15)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.22, 0.03, 0.06), mid=(0.12, 0.02, 0.05))
    brain(ctx, W / 2, 640, 1.15, T, glow=0.4)
    stamp(ctx, "STOLEN", W / 2, 640, (lt - 0.2) / 0.3, size=140)
    character(ctx, 170, 1380, 0.6, T, mood="sorpresa")


# 18.75 "Harvey cut it into 240 pieces."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 700)
    bg_blueprint(ctx, T)
    n = int(counter(lt, 1, 240, 1.4))
    for i in range(240):
        r, c = divmod(i, 16)
        x0, y0 = W / 2 - 16 * 28 + c * 56, 330 + r * 56
        if i < n:
            rrect(ctx, x0, y0, 48, 48, 8); fill(ctx, PINK if (r + c) % 2 else PINK_D)
    pill(ctx, f"{n} PIECES", W / 2, 1300, 1.0, size=70, rgb=PINK)


# 21.13 "He even took Einstein's eyes,"
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 720)
    bg_dark(ctx, T, top=(0.06, 0.04, 0.14), mid=(0.14, 0.08, 0.26))
    spotlight(ctx, W / 2, 620, 520, 0.3, (0.8, 0.85, 1.0))
    eyeball(ctx, W / 2 - 200, 620, 170, T, look=(math.sin(T * 2), 0))
    eyeball(ctx, W / 2 + 200, 620, 170, T, look=(math.sin(T * 2), 0))
    badge(ctx, "HIS EYES TOO", W / 2, 1380, pop(lt, 0.4), size=70)


# 23.02 "and gave them to Einstein's eye doctor."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.04, 0.08, 0.12), mid=(0.08, 0.16, 0.24))
    # optotipo
    rrect(ctx, 560, 260, 380, 560, 16); fill(ctx, WHITE)
    for k, (ltr, sz) in enumerate((("E", 150), ("F P", 90), ("T O Z", 64), ("L P E D", 46), ("P E C F D", 34))):
        text(ctx, ltr, 750, 350 + sum((150, 90, 64, 46, 34)[:k]) * 1.25 + sz * 0.2, sz, INK, shadow=False)
    gent(ctx, 300, 480, 0.85, hat=False, col=(0.16, 0.16, 0.26))
    eyeball(ctx, 300 + 300 * ease(clamp(lt / 0.8)), 1000, 70, T)
    pill(ctx, "EYE DOCTOR", 300, 300, pop(lt, 0.6), size=48, rgb=YELLOW)


# 24.64 "Then Harvey lost his job and moved to Wichita."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 800)
    bg_sky(ctx, T, warm=0.8)
    sun(ctx, 860, 330, 100, T)
    ground(ctx, 1000, (0.62, 0.52, 0.24))
    ctx.rectangle(-300, 1000, W + 600, 160); fill(ctx, (0.25, 0.25, 0.30))
    for k in range(-2, 10):
        ctx.rectangle(k * 200 - (T * 400) % 200, 1070, 100, 16); fill(ctx, YELLOW)
    road_sign(ctx, 840, 620, 0.9, "WICHITA", "KANSAS")
    car(ctx, 330 + 60 * ease(clamp(lt / dur)), 960, 0.9, T)
    badge(ctx, "FIRED", 300, 380, pop(lt, 0.2), size=70)


# 27.14 "Einstein's brain went with him, in a cider box, under a beer cooler."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.13, 0.08))
    ground(ctx, 1150, (0.20, 0.14, 0.10))
    cider_box(ctx, W / 2, 900, 0.9, T, lid=0.0)
    drop = ease_back(clamp((lt - 1.3) / 0.6))
    beer_cooler(ctx, W / 2, 380 + 260 * drop - 600 * (1 - clamp((lt - 1.3) * 5)), 0.85)
    pill(ctx, "UNDER A BEER COOLER", W / 2, 1360, pop(lt, 2.0), size=44, rgb=RED)


# 30.45 "A reporter found it there in 1978."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.05, 0.05, 0.12), mid=(0.12, 0.10, 0.22))
    cider_box(ctx, W / 2 + 120, 880, 0.75, T, lid=clamp(lt / 0.8))
    gent(ctx, 230, 560, 0.75, hat=True, col=(0.20, 0.20, 0.30))
    icon(ctx, "📝", 360, 520, 130, pop(lt, 0.3))
    badge(ctx, "1978", W / 2, 300, pop(lt, 0.9), size=90)


# 33.07 "Today, slices of Einstein's brain sit in a museum in Philadelphia."
def e18(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 820)
    bg_dark(ctx, T, top=(0.05, 0.05, 0.12), mid=(0.12, 0.10, 0.22))
    museum_case(ctx, W / 2, 760, 1.0, T, content=lambda c, t: [slide(c, 0, -200 + k * 170, 0.85, 0.05 * (k - 1)) for k in range(3)])
    pill(ctx, "PHILADELPHIA MUSEUM", W / 2, 1440, pop(lt, 1.6), size=44, rgb=GOLD)


# 36.34 "But for more than twenty years,"  → bucle: "Albert Einstein's brain was kept in a cider box…"
def e19(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.92), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.86, e2), (3.55, e3), (4.62, e4), (5.54, e5), (7.45, e6), (9.35, e7), (11.60, e8),
           (14.62, e9), (16.22, e10), (17.05, e11), (18.75, e12), (21.13, e13), (23.02, e14), (24.64, e15),
           (27.14, e16), (30.45, e17), (33.07, e18), (36.34, e19)]
SFX = [(3.6, "pop"), (16.25, "ding"), (19.7, "pop"), (28.6, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_dark(ctx, T, top=(0.10, 0.06, 0.04), mid=(0.22, 0.13, 0.08))
    rays(ctx, W / 2, 1000, T, (1.0, 0.85, 0.5), 0.07)
    spotlight(ctx, W / 2, 950, 600, 0.45, (1, 0.9, 0.6))
    cider_box(ctx, W / 2, 1150, 1.2, T, lid=0.55, jars=False)
    text(ctx, "?", W / 2, 900, 380, YELLOW)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["EINSTEIN IN", ("A CIDER BOX?", WHITE)], y=270, size=170)
    thumb_circle(ctx, W / 2, 900, 230, 170)
    ficha(ctx, "ALBERT EINSTEIN", "PHYSICIST · 1879–1955", W / 2, 1620, 1.0, "⚛️", PINK)
