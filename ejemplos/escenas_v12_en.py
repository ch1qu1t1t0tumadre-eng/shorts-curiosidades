"""v12 (EN) FORMATO BUCLE: the 'cursed' Hope Diamond was mailed to the Smithsonian (1958, registered mail, $2.44 postage)."""
import math
from anim import *  # noqa

KRAFT = (0.72, 0.53, 0.33)
KRAFT_L = (0.84, 0.66, 0.44)
KRAFT_D = (0.52, 0.36, 0.21)
GEM = (0.16, 0.36, 0.92)
GEM_L = (0.55, 0.78, 1.0)
GEM_D = (0.04, 0.10, 0.40)
TEAL = (0.05, 0.22, 0.26)
TEAL2 = (0.02, 0.10, 0.13)
WINE = (0.30, 0.05, 0.10)
WINE2 = (0.12, 0.02, 0.05)
CREAM = (0.97, 0.93, 0.84)
STAMP_RED = (0.85, 0.12, 0.14)
GOLD = (1.0, 0.78, 0.30)
POST_BLUE = (0.12, 0.25, 0.55)
STONE = (0.86, 0.83, 0.76)
STONE_D = (0.62, 0.59, 0.53)


# ---------------- fondos ----------------
def bg_velvet(ctx, T, top=TEAL, bot=TEAL2, spot=(540, 600)):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, top), (1, bot)]))
    ctx.paint()
    g = cairo.RadialGradient(spot[0], spot[1], 0, spot[0], spot[1], 900)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.16)
    g.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.set_source(g)
    ctx.paint()
    rng = np.random.default_rng(12)
    for _ in range(40):  # motas de polvo brillando
        x, y = rng.uniform(-300, W + 300), rng.uniform(-400, H + 400)
        circle(ctx, x, y + 20 * math.sin(T * 0.5 + x), rng.uniform(1.5, 3.5))
        fill(ctx, WHITE, 0.15 + 0.15 * math.sin(T * 2 + y))


def bg_paper(ctx, T, col=(0.93, 0.88, 0.78), col2=(0.80, 0.72, 0.60)):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, col), (1, col2)]))
    ctx.paint()
    ctx.set_line_width(2)
    ctx.set_source_rgba(0.4, 0.3, 0.2, 0.08)
    for y in range(-600, H + 600, 70):
        ctx.move_to(-600, y)
        ctx.line_to(W + 600, y)
    ctx.stroke()


def sparkle(ctx, x, y, r, a=1.0):
    if a <= 0.01:
        return
    ctx.move_to(x, y - r); ctx.line_to(x + r * 0.18, y - r * 0.18); ctx.line_to(x + r, y)
    ctx.line_to(x + r * 0.18, y + r * 0.18); ctx.line_to(x, y + r); ctx.line_to(x - r * 0.18, y + r * 0.18)
    ctx.line_to(x - r, y); ctx.line_to(x - r * 0.18, y - r * 0.18); ctx.close_path()
    fill(ctx, WHITE, a)


# ---------------- piezas ----------------
def gem(ctx, x, y, s=1.0, T=0.0, glow=1.0, setting=True, tint=None):
    """Diamante azul talla cojín (vista frontal), con orla de brillantes blancos (colgante). r ≈ 200*s."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 0, 0, 0, 520)
        c = tint or (0.35, 0.6, 1.0)
        g.add_color_stop_rgba(0, *c, 0.55 * glow)
        g.add_color_stop_rgba(1, *c, 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, 520)
        ctx.fill()
    if setting:
        # orla de brillantes
        for k in range(16):
            ang = k / 16 * math.tau
            bx, by = math.cos(ang) * 250, math.sin(ang) * 225
            circle(ctx, bx, by, 34)
            ctx.set_source(vgrad(ctx, bx - 30, by - 30, bx + 30, by + 30, [(0, WHITE), (1, (0.70, 0.74, 0.82))]))
            ctx.fill()
            circle(ctx, bx, by, 34)
            stroke(ctx, (0.55, 0.58, 0.66), 3)
            sparkle(ctx, bx - 8, by - 8, 14, 0.5 + 0.5 * math.sin(T * 3 + k))
        # aro superior
        ellipse(ctx, 0, -300, 40, 50)
        stroke(ctx, (0.9, 0.9, 0.95), 12)
    # cuerpo: cojín (octógono redondeado)
    pts = []
    for k in range(8):
        ang = k / 8 * math.tau + math.pi / 8
        pts.append((math.cos(ang) * 205, math.sin(ang) * 185))
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, -200, -190, 200, 190, [(0, GEM_L), (0.45, GEM), (1, GEM_D)]))
    ctx.fill()
    # tabla
    tab = [(px * 0.48, py * 0.48) for px, py in pts]
    ctx.move_to(*tab[0])
    for p in tab[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, -100, -90, 100, 90, [(0, (0.70, 0.86, 1.0)), (1, (0.20, 0.40, 0.95))]))
    ctx.fill()
    # facetas
    for k in range(8):
        a, b = pts[k], pts[(k + 1) % 8]
        ta, tb = tab[k], tab[(k + 1) % 8]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ctx.move_to(*ta); ctx.line_to(mx, my); ctx.line_to(*tb)
        ctx.close_path()
        sh = 0.5 + 0.5 * math.sin(k * 1.7 + T * 1.5)
        fill(ctx, WHITE, 0.08 + 0.18 * sh)
        ctx.move_to(*ta); ctx.line_to(*a); ctx.line_to(mx, my)
        stroke(ctx, (0.75, 0.88, 1.0), 2.5, 0.6)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    stroke(ctx, (0.85, 0.92, 1.0), 4)
    # brillo
    ellipse(ctx, -70, -80, 55, 22)
    fill(ctx, WHITE, 0.5)
    sparkle(ctx, 90 + 20 * math.sin(T), -60, 46 + 10 * math.sin(T * 4), 0.9)
    sparkle(ctx, -110, 70, 30 + 8 * math.sin(T * 3 + 1), 0.7)
    ctx.restore()


def stamp(ctx, x, y, s=1.0, rgb=STAMP_RED, rot=0.0, label="2¢"):
    """Sello de correos con borde dentado."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    w, h = 110, 130
    rrect(ctx, -w / 2 - 6, -h / 2 - 6, w + 12, h + 12, 4)
    fill(ctx, WHITE)
    for k in range(9):  # perforaciones
        for (px, py) in ((-w / 2 - 6 + k * (w + 12) / 8, -h / 2 - 6), (-w / 2 - 6 + k * (w + 12) / 8, h / 2 + 6)):
            circle(ctx, px, py, 5)
            fill(ctx, KRAFT_D)
    for k in range(10):
        for (px, py) in ((-w / 2 - 6, -h / 2 - 6 + k * (h + 12) / 9), (w / 2 + 6, -h / 2 - 6 + k * (h + 12) / 9)):
            circle(ctx, px, py, 5)
            fill(ctx, KRAFT_D)
    rrect(ctx, -w / 2 + 6, -h / 2 + 6, w - 12, h - 12, 3)
    fill(ctx, rgb)
    circle(ctx, 0, -10, 28)
    fill(ctx, WHITE, 0.35)
    text(ctx, label, 0, 38, 24, WHITE, shadow=False)
    ctx.restore()


def parcel(ctx, x, y, s=1.0, T=0.0, stamps=1.0, fragile=1.0, reg=1.0, rot=0.0, w=620, h=420):
    """Paquete de papel marrón con cordel, sellos, 'FRAGILE' en rojo y sello de 'REGISTERED'."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    soft_shadow(ctx, 0, h / 2 + 20, w * 0.55, 40, 0.35)
    rrect(ctx, -w / 2, -h / 2, w, h, 14)
    ctx.set_source(vgrad(ctx, 0, -h / 2, 0, h / 2, [(0, KRAFT_L), (1, KRAFT)]))
    ctx.fill()
    rng = np.random.default_rng(4)  # arrugas
    for _ in range(9):
        x0, y0 = rng.uniform(-w / 2, w / 2), rng.uniform(-h / 2, h / 2)
        ctx.move_to(x0, y0)
        ctx.line_to(x0 + rng.uniform(-90, 90), y0 + rng.uniform(-60, 60))
        stroke(ctx, KRAFT_D, 2, 0.45)
    # pliegue de la solapa
    ctx.move_to(-w / 2, -h / 2 + 30); ctx.line_to(-w / 2 + 90, -h / 2); ctx.close_path()
    stroke(ctx, KRAFT_D, 3, 0.6)
    # cordel
    ctx.move_to(-w / 2, 20); ctx.line_to(w / 2, 20)
    ctx.move_to(-60, -h / 2); ctx.line_to(-60, h / 2)
    stroke(ctx, (0.95, 0.92, 0.85), 7)
    # dirección (garabatos)
    for k, ww in enumerate((260, 210, 240)):
        ctx.move_to(-w / 2 + 50, 80 + k * 40)
        for j in range(12):
            ctx.line_to(-w / 2 + 50 + ww * j / 11, 80 + k * 40 + 6 * math.sin(j * 2.1 + k))
        stroke(ctx, (0.15, 0.12, 0.10), 4, 0.8)
    # sellos
    cols = [STAMP_RED, POST_BLUE, (0.20, 0.55, 0.30), (0.55, 0.20, 0.55), STAMP_RED, POST_BLUE]
    n = int(round(stamps * 6))
    for k in range(n):
        r, c = divmod(k, 3)
        stamp(ctx, w / 2 - 70 - c * 95, -h / 2 + 80 + r * 115, 0.68, cols[k], rot=0.06 * math.sin(k * 3))
    # FRAGILE
    if fragile > 0.01:
        ctx.save()
        ctx.translate(-w / 2 + 160, -h / 2 + 90)
        ctx.rotate(-0.12)
        ctx.scale(fragile, fragile)
        text(ctx, "FRAGILE", 0, 0, 52, STAMP_RED, shadow=False)
        ctx.restore()
    # sello REGISTERED
    if reg > 0.01:
        ctx.save()
        ctx.translate(w / 2 - 160, h / 2 - 80)
        ctx.rotate(-0.18)
        k = 1 + 1.5 * (1 - ease(reg))
        ctx.scale(k, k)
        rrect(ctx, -150, -38, 300, 76, 10)
        stroke(ctx, STAMP_RED, 7, min(1, reg * 1.5))
        text(ctx, "REGISTERED", 0, 2, 40, STAMP_RED, a=min(1, reg * 1.5), shadow=False)
        ctx.restore()
    ctx.restore()


def envelope(ctx, x, y, s=1.0, rot=0.0, rgb=(0.98, 0.84, 0.88), heart=True):
    """Sobre de tarjeta de cumpleaños."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    soft_shadow(ctx, 0, 190, 300, 30, 0.3)
    rrect(ctx, -300, -180, 600, 360, 14)
    fill(ctx, rgb)
    ctx.move_to(-300, -180); ctx.line_to(0, 40); ctx.line_to(300, -180)
    stroke(ctx, tuple(c * 0.8 for c in rgb), 5)
    ctx.move_to(-300, 180); ctx.line_to(-60, 0)
    ctx.move_to(300, 180); ctx.line_to(60, 0)
    stroke(ctx, tuple(c * 0.85 for c in rgb), 4)
    if heart:
        icon(ctx, "🎂", -200, 100, 110)
    stamp(ctx, 220, -100, 0.6, STAMP_RED, rot=0.05)
    ctx.restore()


def gent(ctx, x, y, s=1.0, col=(0.06, 0.06, 0.10), hat=True):
    """Silueta genérica de un caballero con sombrero (sin rasgos)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -150, 120, 300, 520, 110)
    fill(ctx, col)
    circle(ctx, 0, 0, 100)
    fill(ctx, col)
    if hat:
        rrect(ctx, -150, -80, 300, 30, 15)
        fill(ctx, col)
        rrect(ctx, -90, -190, 180, 130, 30)
        fill(ctx, col)
    ctx.restore()


def mailman(ctx, x, y, s=1.0, T=0.0, col=(0.14, 0.20, 0.36)):
    """Cartero genérico (silueta azul con gorra de visera y bolsa de cartas)."""
    ctx.save()
    ctx.translate(x, y + 5 * math.sin(T * 2))
    ctx.scale(s, s)
    rrect(ctx, -150, 120, 300, 520, 110)
    fill(ctx, col)
    circle(ctx, 0, 0, 100)
    fill(ctx, col)
    # gorra
    rrect(ctx, -105, -120, 210, 90, 30)
    fill(ctx, (0.10, 0.14, 0.26))
    rrect(ctx, -20, -50, 180, 26, 13)
    fill(ctx, (0.05, 0.06, 0.10))
    rrect(ctx, -30, -105, 60, 30, 8)
    fill(ctx, GOLD)
    # bandolera y bolsa
    ctx.move_to(-120, 160); ctx.line_to(140, 470)
    stroke(ctx, (0.45, 0.30, 0.16), 26)
    rrect(ctx, 60, 400, 220, 190, 24)
    fill(ctx, (0.55, 0.37, 0.20))
    rrect(ctx, 60, 400, 220, 70, 24)
    fill(ctx, (0.45, 0.30, 0.16))
    ctx.restore()


def museum(ctx, x, y, s=1.0, T=0.0, lit=0.0):
    """Edificio neoclásico con columnas y cúpula. (x, y) = base."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # cúpula
    ctx.arc(0, -600, 170, math.pi, 0)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -770, 0, -600, [(0, (0.80, 0.82, 0.78)), (1, STONE_D)]))
    ctx.fill()
    ctx.rectangle(-200, -620, 400, 50)
    fill(ctx, STONE)
    # frontón
    ctx.move_to(-420, -440); ctx.line_to(0, -580); ctx.line_to(420, -440); ctx.close_path()
    fill(ctx, STONE)
    ctx.move_to(-420, -440); ctx.line_to(0, -580); ctx.line_to(420, -440); ctx.close_path()
    stroke(ctx, STONE_D, 5)
    ctx.rectangle(-440, -440, 880, 60)
    fill(ctx, STONE_D)
    # columnas
    ctx.rectangle(-420, -380, 840, 330)
    fill(ctx, (0.30, 0.26, 0.22))
    for k in range(8):
        cx = -380 + k * 108.5
        ctx.rectangle(cx - 26, -380, 52, 330)
        ctx.set_source(vgrad(ctx, cx - 26, 0, cx + 26, 0, [(0, (1, 0.98, 0.93)), (1, STONE_D)]))
        ctx.fill()
    if lit > 0:
        ctx.rectangle(-60, -300, 120, 250)
        fill(ctx, (1, 0.85, 0.5), lit)
    # escalinata
    for k in range(4):
        ctx.rectangle(-460 - k * 20, -50 + k * 18, 920 + k * 40, 18)
        fill(ctx, STONE if k % 2 == 0 else STONE_D)
    ctx.restore()


def post_office(ctx, x, y, s=1.0, T=0.0):
    """Fachada de oficina de correos (ladrillo) con letrero 'U.S. POST OFFICE'."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-460, -760, 920, 760)
    ctx.set_source(vgrad(ctx, 0, -760, 0, 0, [(0, (0.62, 0.30, 0.22)), (1, (0.45, 0.20, 0.15))]))
    ctx.fill()
    for r in range(25):  # ladrillos
        ctx.move_to(-460, -760 + r * 30)
        ctx.line_to(460, -760 + r * 30)
    stroke(ctx, (0.35, 0.15, 0.10), 2, 0.5)
    rrect(ctx, -400, -720, 800, 110, 10)
    fill(ctx, STONE)
    text(ctx, "U.S. POST OFFICE", 0, -665, 64, (0.12, 0.14, 0.25), shadow=False)
    for wx in (-300, 300):  # ventanas
        rrect(ctx, wx - 90, -560, 180, 260, 90)
        fill(ctx, (1, 0.88, 0.55), 0.85)
        ctx.move_to(wx, -560); ctx.line_to(wx, -300)
        ctx.move_to(wx - 90, -420); ctx.line_to(wx + 90, -420)
        stroke(ctx, (0.30, 0.15, 0.10), 8)
    rrect(ctx, -110, -480, 220, 480, 110)  # puerta
    fill(ctx, (0.20, 0.13, 0.09))
    rrect(ctx, -90, -460, 180, 440, 90)
    fill(ctx, (1, 0.85, 0.5), 0.55)
    # bandera
    ctx.move_to(380, -760); ctx.line_to(380, -980)
    stroke(ctx, (0.8, 0.8, 0.82), 8)
    wav = 8 * math.sin(T * 4)
    for k in range(5):
        ctx.rectangle(380, -980 + k * 22, 170, 22)
        fill(ctx, STAMP_RED if k % 2 == 0 else WHITE)
    ctx.rectangle(380, -980, 70, 66)
    fill(ctx, POST_BLUE)
    _ = wav
    ctx.restore()


def skyline(ctx, ybase, T, col=(0.10, 0.14, 0.24), a=1.0):
    rng = np.random.default_rng(8)
    x = -500
    while x < W + 500:
        w = rng.uniform(80, 170)
        h = rng.uniform(250, 750)
        ctx.rectangle(x, ybase - h, w, h + 400)
        fill(ctx, col, a)
        for wy in range(int(ybase - h + 30), int(ybase), 60):
            for wx in range(int(x + 15), int(x + w - 20), 40):
                if rng.random() < 0.35:
                    ctx.rectangle(wx, wy, 16, 24)
                    fill(ctx, (1, 0.85, 0.45), 0.6 * a)
        x += w + 10


def train(ctx, x, y, s=1.0, T=0.0):
    """Tren de correo (locomotora + vagón 'U.S. MAIL'). (x, y) = raíles."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # vagón de correo
    rrect(ctx, -820, -300, 560, 250, 20)
    fill(ctx, (0.55, 0.12, 0.12))
    text(ctx, "U.S. MAIL", -540, -200, 54, CREAM, shadow=False)
    text(ctx, "RAILWAY POST OFFICE", -540, -130, 26, CREAM, shadow=False)
    # locomotora
    rrect(ctx, -240, -280, 440, 230, 30)
    fill(ctx, (0.12, 0.12, 0.15))
    rrect(ctx, 80, -420, 160, 370, 20)
    fill(ctx, (0.18, 0.18, 0.22))
    rrect(ctx, 110, -390, 100, 80, 10)
    fill(ctx, (1, 0.85, 0.5), 0.9)
    rrect(ctx, -180, -380, 70, 110, 10)
    fill(ctx, (0.12, 0.12, 0.15))
    ctx.move_to(200, -50); ctx.line_to(320, -50); ctx.line_to(200, -200); ctx.close_path()
    fill(ctx, (0.3, 0.3, 0.34))
    # ruedas
    for wx in (-760, -620, -400, -170, 0, 140):
        circle(ctx, wx, -40, 52)
        fill(ctx, (0.08, 0.08, 0.1))
        ctx.save(); ctx.translate(wx, -40); ctx.rotate(T * 8)
        ctx.move_to(-40, 0); ctx.line_to(40, 0); ctx.move_to(0, -40); ctx.line_to(0, 40)
        stroke(ctx, (0.6, 0.6, 0.65), 6); ctx.restore()
    # humo
    for k in range(5):
        ph = (T * 0.8 + k * 0.2) % 1
        circle(ctx, -145 - 300 * ph, -420 - 260 * ph, 40 + 70 * ph)
        fill(ctx, (0.85, 0.85, 0.88), 0.5 * (1 - ph))
    ctx.restore()


def mail_truck(ctx, x, y, s=1.0, T=0.0):
    """Furgoneta de correos años 50. (x, y) = suelo."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -340, -360, 520, 300, 30)
    fill(ctx, (0.92, 0.92, 0.90))
    rrect(ctx, 150, -300, 200, 240, 40)
    fill(ctx, (0.92, 0.92, 0.90))
    rrect(ctx, 190, -280, 120, 100, 14)
    fill(ctx, (0.45, 0.65, 0.85))
    ctx.rectangle(-340, -200, 690, 34)
    fill(ctx, STAMP_RED)
    ctx.rectangle(-340, -166, 690, 20)
    fill(ctx, POST_BLUE)
    text(ctx, "U.S. MAIL", -90, -280, 56, POST_BLUE, shadow=False)
    for wx in (-200, 230):
        circle(ctx, wx, -50, 62)
        fill(ctx, (0.08, 0.08, 0.1))
        circle(ctx, wx, -50, 26)
        fill(ctx, (0.7, 0.7, 0.74))
    ctx.restore()


def wrap_box(ctx, x, y, s=1.0, T=0.0, p=0.0):
    """Cajita con el diamante que se envuelve en papel marrón (p 0..1)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # papel extendido debajo
    rrect(ctx, -420, -300, 840, 600, 10)
    ctx.set_source(vgrad(ctx, 0, -300, 0, 300, [(0, KRAFT_L), (1, KRAFT)]))
    ctx.fill()
    # caja abierta con el diamante
    rrect(ctx, -170, -150, 340, 300, 16)
    fill(ctx, (0.10, 0.10, 0.16))
    rrect(ctx, -140, -120, 280, 240, 12)
    fill(ctx, (0.85, 0.85, 0.90))
    gem(ctx, 0, 0, 0.42, T, glow=0.6, setting=False)
    # solapas que se cierran
    a = ease(clamp(p * 2))
    b = ease(clamp(p * 2 - 1))
    ctx.rectangle(-420, -300, 840, 300 * a + 1)
    ctx.set_source(vgrad(ctx, 0, -300, 0, 0, [(0, KRAFT_L), (1, KRAFT)]))
    ctx.fill()
    ctx.rectangle(-420, 300 - 310 * b, 840, 310 * b + 1)
    ctx.set_source(vgrad(ctx, 0, 0, 0, 300, [(0, KRAFT), (1, KRAFT_D)]))
    ctx.fill()
    if a > 0.05:
        ctx.move_to(-420, -300 + 300 * a); ctx.line_to(420, -300 + 300 * a)
        stroke(ctx, KRAFT_D, 4)
    if b > 0.95:
        ctx.move_to(-420, 20); ctx.line_to(420, 20)
        ctx.move_to(-60, -300); ctx.line_to(-60, 300)
        stroke(ctx, (0.95, 0.92, 0.85), 8)
    ctx.restore()


def house(ctx, x, y, s, T, fire=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-420, -250); ctx.line_to(0, -560); ctx.line_to(420, -250); ctx.close_path()
    fill(ctx, (0.25, 0.15, 0.15))
    ctx.rectangle(-380, -260, 760, 560)
    fill(ctx, (0.85, 0.80, 0.70))
    for wx in (-240, 240):
        for wy in (-150, 80):
            rrect(ctx, wx - 70, wy - 70, 140, 140, 10)
            fill(ctx, (1, 0.55, 0.15) if fire > 0.3 else (0.30, 0.40, 0.55), 0.9)
    ctx.rectangle(-60, 140, 120, 160)
    fill(ctx, (0.35, 0.22, 0.14))
    if fire > 0:
        for k in range(7):
            fx = -330 + k * 110
            hgt = (220 + 90 * math.sin(T * 9 + k * 1.7)) * fire
            ctx.move_to(fx - 70, -250 + abs(fx) * 0.7)
            ctx.curve_to(fx - 60, -350 - hgt * 0.5, fx + 10, -380 - hgt * 0.6, fx, -300 - hgt)
            ctx.curve_to(fx + 20, -380 - hgt * 0.4, fx + 70, -330, fx + 70, -250 + abs(fx) * 0.7)
            ctx.close_path()
            fill(ctx, (1, 0.45 + 0.1 * (k % 3), 0.1), 0.9)
    ctx.restore()


def display_case(ctx, x, y, s=1.0, T=0.0):
    """Vitrina de museo con el envoltorio marrón dentro."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-60, -1100); ctx.line_to(60, -1100); ctx.line_to(380, 0); ctx.line_to(-380, 0); ctx.close_path()
    g = cairo.LinearGradient(0, -1100, 0, 0)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.30)
    g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.0)
    ctx.set_source(g)
    ctx.fill()
    rrect(ctx, -330, 0, 660, 380, 10)  # pedestal
    ctx.set_source(vgrad(ctx, 0, 0, 0, 380, [(0, (0.25, 0.20, 0.18)), (1, (0.12, 0.10, 0.09))]))
    ctx.fill()
    parcel(ctx, 0, -190, 0.80, T, stamps=1.0, fragile=1.0, reg=1.0, rot=-0.03, w=600, h=400)
    rrect(ctx, -360, -470, 720, 480, 8)  # cristal
    fill_keep(ctx, (0.75, 0.9, 1.0), 0.10)
    stroke(ctx, (0.85, 0.95, 1.0), 5, 0.7)
    ctx.move_to(-300, -440); ctx.line_to(-180, -440 + 0); ctx.line_to(-330, -150); ctx.close_path()
    fill(ctx, WHITE, 0.12)
    ctx.restore()


def speech(ctx, s, x, y, appear=1.0, size=44, w=760, lines=None):
    if appear <= 0.01:
        return
    lines = lines or [s]
    h = len(lines) * size * 1.3 + size
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(appear, appear)
    rrect(ctx, -w / 2, -h / 2, w, h, 40)
    fill_keep(ctx, CREAM)
    stroke(ctx, (0.1, 0.1, 0.12), 6)
    ctx.move_to(-w / 4, h / 2 - 3); ctx.line_to(-w / 4 - 70, h / 2 + 80); ctx.line_to(-w / 4 + 50, h / 2 - 3)
    fill_keep(ctx, CREAM)
    stroke(ctx, (0.1, 0.1, 0.12), 6)
    rrect(ctx, -w / 4 - 10, h / 2 - 14, 80, 14, 0)
    fill(ctx, CREAM)
    for k, ln in enumerate(lines):
        text(ctx, ln, 0, -h / 2 + size * 1.15 + k * size * 1.3, size, (0.1, 0.1, 0.14), shadow=False)
    ctx.restore()


def cross(ctx, x, y, r, a=1.0, rgb=RED):
    if a <= 0.01:
        return
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for sgn in (1, -1):
        ctx.move_to(x - r * a, y - sgn * r * a)
        ctx.line_to(x + r * a, y + sgn * r * a)
        stroke(ctx, (0, 0, 0), 46, 0.5)
        ctx.move_to(x - r * a, y - sgn * r * a)
        ctx.line_to(x + r * a, y + sgn * r * a)
        stroke(ctx, rgb, 34)


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): el diamante sobre el paquete marrón con sellos."""
    camera(ctx, zoom, W / 2, 900)
    bg_velvet(ctx, T)
    parcel(ctx, W / 2, 1400, 1.05, T, stamps=1.0, fragile=1.0, reg=1.0, rot=-0.04)
    gem(ctx, W / 2, 620 + 10 * math.sin(T * 1.5), 1.0, T, glow=1.0 + 0.2 * math.sin(T * 3))
    ctx.restore()
    ctx.save()
    pill(ctx, "THE HOPE DIAMOND", W / 2, 230, 1.0, size=52, rgb=GEM_L, sub="45.52 CARATS")


# ---------------- escenas (subtítulo gigante en y≈1060: dejar libre ~950–1170) ----------------
# 0.00 "The Hope Diamond was mailed to the Smithsonian"
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.10)]))


# 2.20 "like a birthday card. Brown paper and stamps."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), keyframes(lt, [(0, 470), (dur, 600)]), 860)
    bg_paper(ctx, T, (0.98, 0.86, 0.88), (0.86, 0.66, 0.72))
    envelope(ctx, W / 2, 620, 1.2, -0.06 + 0.02 * math.sin(T))
    gem(ctx, W / 2 + 230, 470, 0.38, T, glow=0.8, setting=False)
    badge(ctx, "BIRTHDAY CARD?", W / 2, 280, pop(lt, 0.2), size=58, bg=(0.85, 0.25, 0.50))
    # sellos que caen al decir "stamps"
    for k in range(3):
        stamp(ctx, 250 + k * 290, 1400, 1.1 * pop(lt, 2.4 + k * 0.12), [STAMP_RED, POST_BLUE, (0.20, 0.55, 0.30)][k],
              rot=0.1 * (k - 1))
    pill(ctx, "BROWN PAPER", W / 2, 1580, pop(lt, 1.2), size=46, rgb=KRAFT_L)


# 4.82 "November 1958."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, keyframes(lt, [(0, 860), (dur, 800)]))
    bg_velvet(ctx, T, (0.20, 0.10, 0.06), (0.06, 0.03, 0.02), spot=(540, 560))
    # hoja de calendario
    rrect(ctx, 260, 280, 560, 600, 30)
    fill(ctx, CREAM)
    rrect(ctx, 260, 280, 560, 150, 30)
    fill(ctx, STAMP_RED)
    ctx.rectangle(260, 380, 560, 50)
    fill(ctx, STAMP_RED)
    text(ctx, "NOVEMBER", W / 2, 355, 70, WHITE, shadow=False)
    text(ctx, counter(lt, 1900, 1958, 0.9), W / 2, 640, 190, (0.15, 0.12, 0.10), shadow=False)
    for k in range(2):
        circle(ctx, 360 + k * 360, 280, 22)
        fill(ctx, (0.3, 0.3, 0.32))
    gem(ctx, 860, 1420, 0.45, T, glow=0.6, setting=False)
    parcel(ctx, 380, 1450, 0.55, T)


# 6.64 "Legend says the Hope Diamond is cursed."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]) + 0.004 * math.sin(T * 30), W / 2, 820)
    bg_velvet(ctx, T, WINE, WINE2, spot=(540, 600))
    for k in range(12):  # rayos oscuros
        ctx.save(); ctx.translate(W / 2, 600); ctx.rotate(k * math.pi / 6 - T * 0.15)
        ctx.move_to(0, 0); ctx.line_to(1500, -100); ctx.line_to(1500, 100); ctx.close_path()
        fill(ctx, (0, 0, 0), 0.18); ctx.restore()
    gem(ctx, W / 2, 600, 0.9, T, glow=1.2, tint=(0.9, 0.15, 0.25))
    badge(ctx, "LEGEND", W / 2, 260, pop(lt, 0.1), size=64, bg=(0.15, 0.05, 0.08))
    pill(ctx, "CURSED?", 330, 1420, pop(lt, 1.6), size=64, rgb=RED)
    icon(ctx, "💀", 330, 1260, 150, pop(lt, 1.5))
    character(ctx, 800, 1390, 0.6, T, mood="duda", body=True)


# 8.88 "Its owner, jeweler Harry Winston,"
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.10)]), keyframes(lt, [(0, 520), (dur, 560)]), 820)
    bg_velvet(ctx, T, (0.08, 0.10, 0.18), (0.02, 0.03, 0.07), spot=(540, 500))
    # mostrador de joyería
    rrect(ctx, -200, 720, W + 400, 900, 20)
    ctx.set_source(vgrad(ctx, 0, 720, 0, 1400, [(0, (0.30, 0.18, 0.10)), (1, (0.12, 0.07, 0.04))]))
    ctx.fill()
    rrect(ctx, -200, 700, W + 400, 40, 10)
    fill(ctx, GOLD)
    gent(ctx, 300, 330, 0.85)
    gem(ctx, 720, 520, 0.55, T, glow=1.0)
    ficha(ctx, "HARRY WINSTON", "JEWELER · 1896–1978", W / 2, 1420, pop(lt, 0.6), "💎", GEM_L)


# 10.78 "donates it to the Smithsonian."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.06)]), W / 2, keyframes(lt, [(0, 820), (dur, 780)]))
    bg_sky(ctx, T, warm=0.35)
    ground(ctx, 940, (0.35, 0.50, 0.30))
    museum(ctx, W / 2, 950, 1.0, T, lit=0.6)
    # lazo de regalo sobre el diamante
    gem(ctx, W / 2, 1380, 0.45, T, glow=0.9, setting=False)
    icon(ctx, "🎁", 790, 1420, 170, pop(lt, 0.3))
    pill(ctx, "SMITHSONIAN", W / 2, 230, pop(lt, 0.6), size=56, rgb=POST_BLUE, sub="WASHINGTON, D.C.")
    badge(ctx, "DONATED", 270, 1420, pop(lt, 0.2), size=46, bg=(0.15, 0.55, 0.35))


# 12.22 "So Winston wraps the Hope Diamond in plain brown paper"
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.18), (dur, 1.0)]), W / 2, 760)
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, (0.28, 0.18, 0.12)), (1, (0.12, 0.08, 0.05))]))
    ctx.paint()
    for k in range(-6, 12):  # vetas de la mesa
        ctx.move_to(-600, k * 180 + 30 * math.sin(k)); ctx.line_to(W + 600, k * 180 + 60)
        stroke(ctx, (0.40, 0.27, 0.17), 4, 0.5)
    wrap_box(ctx, W / 2, 620, 1.0, T, p=clamp((lt - 1.0) / 1.8))
    ficha(ctx, "HARRY WINSTON", "JEWELER · 1896–1978", W / 2, 1430, pop(lt, 0.0), "💎", GEM_L)
    pill(ctx, "PLAIN BROWN PAPER", W / 2, 230, pop(lt, 1.9), size=48, rgb=KRAFT_L)


# 15.37 "and takes it to a New York post office."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), keyframes(lt, [(0, 600), (dur, 520)]), 860)
    bg_sky(ctx, T, warm=0.8)
    skyline(ctx, 1000, T, (0.30, 0.25, 0.38), 0.9)
    ground(ctx, 1000, (0.30, 0.28, 0.32))
    post_office(ctx, W / 2, 1000, 0.9, T)
    parcel(ctx, keyframes(lt, [(0, -200), (1.2, 300)]), 1420, 0.5, T, reg=0.0, rot=-0.08)
    pill(ctx, "NEW YORK", 780, 1420, pop(lt, 1.0), size=56, rgb=YELLOW)


# 17.29 "Registered mail. The postage? Two dollars and forty-four cents."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (1.3, 1.0), (1.4, 1.08), (dur, 1.0)]), W / 2, 820)
    bg_paper(ctx, T, (0.95, 0.90, 0.80), (0.78, 0.68, 0.54))
    parcel(ctx, W / 2, 560, 1.15, T, stamps=clamp((lt - 1.4) / 0.9), fragile=1.0, reg=clamp(lt / 0.35))
    character(ctx, 850, 1410, 0.55, T, mood="duda", body=True)
    badge(ctx, "?", 850, 1200, pop(lt, 0.7) * (1 - pop(lt, 1.35)), size=60, bg=RED)
    pill(ctx, counter(lt - 1.35, 0, 2.44, 0.6, "${:.2f}"), 380, 1400, pop(lt, 1.35), size=110, rgb=GREEN,
         sub="POSTAGE")


# 20.43 "In other words, a million-dollar diamond"
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.6), (0.3, 1.0), (dur, 1.1)]) + 0.012 * math.sin(T * 40) * (lt < 0.4),
           W / 2, 820)
    bg_velvet(ctx, T, (0.04, 0.08, 0.30), (0.01, 0.02, 0.10), spot=(540, 600))
    for k in range(16):
        ctx.save(); ctx.translate(W / 2, 600); ctx.rotate(k * math.pi / 8 + T * 0.2)
        ctx.move_to(0, 0); ctx.line_to(1400, -90); ctx.line_to(1400, 90); ctx.close_path()
        fill(ctx, GEM_L, 0.07); ctx.restore()
    gem(ctx, W / 2, 600, 1.05, T, glow=1.3)
    pill(ctx, counter(lt - 0.9, 0, 1000000, 0.8, "${:,.0f}"), W / 2, 1400, pop(lt, 0.9), size=80, rgb=GOLD,
         sub="VALUE IN 1958")
    character(ctx, 170, 1380, 0.45, T, mood="sorpresa", body=True)


# 22.70 "rode the mail like a phone bill."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 0.92)]), W / 2, keyframes(lt, [(0, 760), (dur, 820)]))
    bg_paper(ctx, T, (0.86, 0.90, 0.95), (0.62, 0.68, 0.78))
    # montón de cartas y facturas, el paquete en medio
    rng = np.random.default_rng(21)
    for k in range(14):
        x, y = rng.uniform(60, 1020), rng.uniform(250, 880)
        ctx.save(); ctx.translate(x, y + 20 * math.sin(T + k)); ctx.rotate(rng.uniform(-0.5, 0.5))
        rrect(ctx, -130, -80, 260, 160, 8); fill(ctx, WHITE)
        rrect(ctx, -130, -80, 260, 160, 8); stroke(ctx, (0.6, 0.6, 0.65), 3)
        ctx.move_to(-90, 0); ctx.line_to(60, 0); ctx.move_to(-90, 30); ctx.line_to(30, 30)
        stroke(ctx, (0.4, 0.4, 0.45), 4)
        ctx.restore()
    parcel(ctx, W / 2, 560, 0.8, T, rot=0.05)
    badge(ctx, "$2.44", 300, 1400, pop(lt, 0.0), size=70, bg=(0.15, 0.55, 0.35))
    text(ctx, "=", W / 2, 1400, 90, (0.15, 0.15, 0.2))
    icon(ctx, "🧾", 780, 1380, 300, pop(lt, 0.9))
    pill(ctx, "PHONE BILL", 780, 1580, pop(lt, 1.0), size=40, rgb=RED)


# 24.40 "It reaches Washington on a mail train."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.02)]), keyframes(lt, [(0, 560), (dur, 520)]), 900)
    bg_sky(ctx, T, warm=1.0)
    sun(ctx, 860, 420, 120, T)
    ground(ctx, 1500, (0.25, 0.35, 0.22))
    ctx.rectangle(-1000, 1500, W + 2000, 22)
    fill(ctx, (0.35, 0.30, 0.28))
    for k in range(-20, 30):
        ctx.rectangle(k * 70 - (T * 300) % 70, 1522, 30, 20)
        fill(ctx, (0.40, 0.27, 0.17))
    train(ctx, keyframes(lt, [(0, 520), (dur, 760)]), 1500, 0.85, T)
    pill(ctx, "MAIL TRAIN", W / 2, 240, pop(lt, 0.9), size=52, rgb=STAMP_RED, sub="NEW YORK → WASHINGTON")


# 26.28 "Then mailman James Todd drives the Hope Diamond to the museum."
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), keyframes(lt, [(0, 560), (dur, 520)]), 860)
    bg_sky(ctx, T, warm=0.2)
    museum(ctx, 820, 800, 0.65, T)
    ground(ctx, 800, (0.42, 0.42, 0.44))
    mail_truck(ctx, keyframes(lt, [(0, 260), (dur, 560)]), 800, 0.8, T)
    mailman(ctx, 90, 560, 0.36, T)
    ficha(ctx, "JAMES G. TODD", "LETTER CARRIER · NOV 10, 1958", 590, 1440, pop(lt, 0.4), "📬", YELLOW, w=800)
    pill(ctx, "NOV 10, 1958", W / 2, 240, pop(lt, 2.4), size=48, rgb=GOLD)


# 29.61 "Within a year, Todd crushes his leg in a car crash,"
def e14(ctx, lt, dur, T):
    hit = lt > 1.9
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]) + (0.01 * math.sin(T * 50) if hit and lt < 2.3 else 0),
           W / 2, 800)
    bg_velvet(ctx, T, (0.18, 0.06, 0.06), (0.05, 0.02, 0.02), spot=(540, 560))
    pill(ctx, "WITHIN 1 YEAR", W / 2, 250, pop(lt, 0.0), size=56, rgb=RED)
    x = keyframes(lt, [(0, -200), (1.9, 470), (dur, 500)])
    icon(ctx, "🚗", x, 620, 360, 1.0, rot=0.3 if hit else 0.0)
    icon(ctx, "💥", 700, 560, 300, pop(lt, 1.9))
    mailman(ctx, 870, 1320, 0.33, T)
    badge(ctx, "CAR CRASH", 380, 1400, pop(lt, 2.0), size=58)


# 32.55 "his wife dies, and a fire hits his house."
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 0.98)]), W / 2, 820)
    bg_velvet(ctx, T, (0.10, 0.04, 0.04), (0.02, 0.01, 0.02), spot=(540, 640))
    ground(ctx, 900, (0.10, 0.08, 0.08))
    house(ctx, W / 2, 600, 0.95, T, fire=clamp((lt - 1.0) / 0.5))
    badge(ctx, "WIFE DIES", 300, 1360, pop(lt, 0.4), size=50, bg=(0.25, 0.25, 0.30))
    badge(ctx, "HOUSE FIRE", 760, 1500, pop(lt, 1.3), size=50, bg=(0.95, 0.45, 0.10))
    icon(ctx, "🔥", 160, 300, 170, pop(lt, 1.2))


# 35.04 "Todd said he didn't believe in curses."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), keyframes(lt, [(0, 560), (dur, 520)]), 860)
    bg_paper(ctx, T, (0.90, 0.92, 0.96), (0.68, 0.74, 0.84))
    mailman(ctx, 300, 760, 0.7, T)
    speech(ctx, "", 560, 400, pop(lt, 0.3), size=46, w=820,
           lines=["“I DON'T BELIEVE", "ANY OF THAT STUFF.”"])
    character(ctx, 820, 1390, 0.55, T, mood="feliz", body=True)
    pill(ctx, "NO CURSE?", 330, 1450, pop(lt, 1.0), size=52, rgb=GREEN)


# 36.91 "And that brown wrapper is still at the Smithsonian."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.95), (dur, 1.05)]), W / 2, 820)
    bg_velvet(ctx, T, (0.10, 0.10, 0.14), (0.03, 0.03, 0.05), spot=(540, 500))
    display_case(ctx, W / 2, 700, 1.0, T)
    pill(ctx, "NATIONAL POSTAL MUSEUM", W / 2, 1420, pop(lt, 1.0), size=44, rgb=GOLD, sub="SMITHSONIAN")
    badge(ctx, "STILL THERE", W / 2, 240, pop(lt, 1.8), size=52, bg=(0.15, 0.55, 0.35))


# 39.44 "Because in 1958" -> vuelve a e1 (mismo plano)
def e18(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.92), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (2.20, e2), (4.82, e3), (6.64, e4), (8.88, e5), (10.78, e6), (12.22, e7), (15.37, e8),
           (17.29, e9), (20.43, e10), (22.70, e11), (24.40, e12), (26.28, e13), (29.61, e14), (32.55, e15),
           (35.04, e16), (36.91, e17), (39.44, e18)]
SFX = [(18.70, "pop"), (21.35, "ding"), (31.55, "pop"), (37.95, "ding")]


# ---------------- miniatura (no desvela cómo llegó el diamante) ----------------
def MINIATURA(ctx):
    T = 1.3
    ctx.save()
    camera(ctx, 1.0, W / 2, 960)
    bg_velvet(ctx, T, spot=(540, 900))
    parcel(ctx, W / 2, 1460, 1.2, T, stamps=1.0, fragile=1.0, reg=1.0, rot=-0.05)
    gem(ctx, W / 2, 900, 1.0, T, glow=1.4)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_circle(ctx, 760, 1340, 200, 120)
    thumb_arrow(ctx, 200, 1760, 560, 1500)
    thumb_text(ctx, ["$1,000,000", ("IN THE MAIL?", WHITE)], y=250, size=160)
