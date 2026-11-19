"""Kit de piezas reutilizables para escenas (formato bucle). Uso en escenas.py:  from kit import *
Todo dibuja en el lienzo 1080x1920 de anim.py. Nada de fotos de personas reales: siluetas genéricas + ficha()."""
import math
from anim import *  # noqa

GLASS = (0.75, 0.88, 1.0)
GOLD = (1.0, 0.78, 0.30)
TEAL = (0.30, 0.85, 0.85)
WOOD = (0.45, 0.28, 0.16)
WOOD_D = (0.32, 0.19, 0.10)
STONE = (0.55, 0.55, 0.60)
PAPER = (0.95, 0.92, 0.82)
INK = (0.15, 0.12, 0.10)
NIGHT = ((0.04, 0.05, 0.14), (0.10, 0.12, 0.28))


def bg_dark(ctx, T, top=(0.05, 0.06, 0.16), mid=(0.10, 0.12, 0.28), bot=(0.03, 0.03, 0.08), motes=True):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, top), (0.55, mid), (1, bot)]))
    ctx.paint()
    if motes:
        rng = np.random.default_rng(3)
        for _ in range(40):
            x, y, r = rng.uniform(-400, W + 400), rng.uniform(-600, H + 600), rng.uniform(2, 5)
            y = (y - T * 25 * rng.uniform(0.5, 1.5)) % (H + 1200) - 600
            circle(ctx, x, y, r)
            fill(ctx, WHITE, 0.10 + 0.10 * math.sin(T * 1.7 + x))


def spotlight(ctx, x, y, r, a=0.5, col=(1, 0.95, 0.8)):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a)
    g.add_color_stop_rgba(1, *col, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


def rays(ctx, x, y, T, col=WHITE, a=0.05, n=16):
    for k in range(n):
        ctx.save(); ctx.translate(x, y); ctx.rotate(k * math.tau / n + T * 0.2)
        ctx.move_to(0, 0); ctx.line_to(1500, -90); ctx.line_to(1500, 90); ctx.close_path()
        fill(ctx, col, a); ctx.restore()


def punch(lt, big=1.6, rest=1.0, end=1.08, dur=3.0):
    """Zoom de golpe para el 2.º gancho ('In other words')."""
    return keyframes(lt, [(0, big), (0.3, rest), (dur, end)])


def gent(ctx, x, y, s=1.0, col=(0.10, 0.10, 0.16), hat=True, a=1.0):
    """Silueta genérica de persona (sin rasgos). (x, y) = centro de la cabeza."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -150, 120, 300, 520, 110); fill(ctx, col, a)
    circle(ctx, 0, 0, 100); fill(ctx, col, a)
    if hat:
        rrect(ctx, -150, -80, 300, 30, 15); fill(ctx, col, a)
        rrect(ctx, -90, -190, 180, 130, 30); fill(ctx, col, a)
    ctx.restore()


def house(ctx, x, y, s, T, lit=1.0, wall=(0.30, 0.24, 0.34), roof=(0.20, 0.14, 0.22)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-420, -250); ctx.line_to(0, -560); ctx.line_to(420, -250); ctx.close_path(); fill(ctx, roof)
    ctx.rectangle(-380, -260, 760, 560); fill(ctx, wall)
    for wx in (-260, 0, 260):
        for wy in (-180, 60):
            rrect(ctx, wx - 70, wy - 70, 140, 150, 10)
            fill(ctx, (1, 0.82, 0.45), lit if (wx, wy) == (0, 60) else 0.25)
    ctx.rectangle(-60, 170, 120, 130); fill(ctx, WOOD_D)
    ctx.restore()


def pedestal(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -260, 0, 520, 520, 10)
    ctx.set_source(vgrad(ctx, 0, 0, 0, 520, [(0, (0.30, 0.30, 0.38)), (1, (0.15, 0.15, 0.20))])); ctx.fill()
    ctx.restore()


def museum_case(ctx, x, y, s, T, content=None, appear=1.0):
    """Vitrina con foco. content(ctx, T) dibuja el objeto con origen en el centro de la vitrina."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-60, -900); ctx.line_to(60, -900); ctx.line_to(330, 350); ctx.line_to(-330, 350); ctx.close_path()
    g = cairo.LinearGradient(0, -900, 0, 350)
    g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.0); g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.20 * appear)
    ctx.set_source(g); ctx.fill()
    pedestal(ctx, 0, 380)
    if content:
        ctx.save(); content(ctx, T); ctx.restore()
    rrect(ctx, -240, -380, 480, 760, 8); fill_keep(ctx, GLASS, 0.06); stroke(ctx, GLASS, 6, 0.6)
    ctx.move_to(-200, -340); ctx.line_to(-120, -340); ctx.line_to(-200, -200); fill(ctx, WHITE, 0.15)
    ctx.restore()


def bell_jar(ctx, x, y, w, h, a=1.0):
    """Campana/huevo de cristal (dibujar el objeto antes)."""
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.move_to(-w / 2, h / 2); ctx.line_to(-w / 2, -h / 2 + w / 2)
    ctx.arc(0, -h / 2 + w / 2, w / 2, math.pi, 0); ctx.line_to(w / 2, h / 2)
    fill_keep(ctx, GLASS, 0.10 * a); stroke(ctx, GLASS, 6, 0.7 * a)
    rrect(ctx, -w * 0.32, -h / 2 + w * 0.25, w * 0.1, h * 0.55, w * 0.05); fill(ctx, WHITE, 0.35 * a)
    ctx.restore()


def pin(ctx, x, y, s=1.0, drop=1.0, col=RED):
    yy = y - 200 * (1 - ease_back(clamp(drop)))
    ctx.save(); ctx.translate(x, yy); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.curve_to(-70, -90, -70, -170, 0, -170); ctx.curve_to(70, -170, 70, -90, 0, 0)
    fill(ctx, col); circle(ctx, 0, -115, 28); fill(ctx, WHITE)
    ctx.restore()


def map_card(ctx, x, y, w, h, T, label=None, land=(0.25, 0.60, 0.42), sea=(0.12, 0.30, 0.55)):
    """Mapa genérico estilizado (mar + costa) con pin opcional en el centro."""
    rrect(ctx, x - w / 2, y - h / 2, w, h, 30); fill_keep(ctx, sea); stroke(ctx, WHITE, 6, 0.7)
    ctx.save(); rrect(ctx, x - w / 2, y - h / 2, w, h, 30); ctx.clip()
    rng = np.random.default_rng(7)
    ctx.move_to(x - w / 2 - 10, y + h / 2 + 10)
    for k in range(12):
        ctx.line_to(x - w / 2 + k * w / 11, y - h * 0.1 + rng.uniform(-h * 0.25, h * 0.25))
    ctx.line_to(x + w / 2 + 10, y + h / 2 + 10); ctx.close_path(); fill(ctx, land)
    ctx.restore()
    if label:
        pill(ctx, label, x, y + h / 2 + 70, 1.0, size=40, rgb=GOLD)


def newspaper(ctx, x, y, s, headline, sub="", rot=0.0, date=""):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -340, -440, 680, 880, 8); fill(ctx, (0, 0, 0), 0.3)
    rrect(ctx, -350, -450, 680, 880, 8); fill(ctx, PAPER)
    text(ctx, "LE PETIT JOURNAL" if not date else date, -10, -380, 40, INK, shadow=False)
    ctx.rectangle(-320, -345, 620, 6); fill(ctx, INK)
    words = headline.split("\n")
    for i, wl in enumerate(words):
        text(ctx, wl, -10, -260 + i * 86, 72, INK, shadow=False)
    if sub:
        text(ctx, sub, -10, -260 + len(words) * 86 + 10, 32, (0.4, 0.35, 0.3), shadow=False)
    for k in range(9):
        ctx.rectangle(-320, 60 + k * 38, 280 if k % 3 else 200, 14); fill(ctx, (0.6, 0.57, 0.5))
        ctx.rectangle(0, 60 + k * 38, 300, 14); fill(ctx, (0.6, 0.57, 0.5))
    ctx.restore()


def coffin(ctx, x, y, s=1.0, rot=0.0, col=(0.42, 0.25, 0.14)):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(-110, -330); ctx.line_to(110, -330); ctx.line_to(170, -160); ctx.line_to(120, 330)
    ctx.line_to(-120, 330); ctx.line_to(-170, -160); ctx.close_path()
    fill_keep(ctx, col); stroke(ctx, (0.25, 0.14, 0.08), 10)
    ctx.rectangle(-12, -200, 24, 200); fill(ctx, GOLD); ctx.rectangle(-70, -130, 140, 24); fill(ctx, GOLD)
    ctx.restore()


def tombstone(ctx, x, y, s=1.0, label="", a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-130, 200); ctx.line_to(-130, -60); ctx.arc(0, -60, 130, math.pi, 0); ctx.line_to(130, 200)
    ctx.close_path(); fill_keep(ctx, STONE, a); stroke(ctx, (0.3, 0.3, 0.35), 6, a)
    if label:
        text(ctx, label, 0, 10, 34, (0.25, 0.25, 0.3), shadow=False)
    ctx.restore()


def cemetery(ctx, T, ground_y=1350):
    bg_night(ctx, T, grid=False)
    circle(ctx, 820, 330, 90); fill(ctx, (0.95, 0.93, 0.8))
    spotlight(ctx, 820, 330, 300, 0.25, (0.9, 0.9, 1.0))
    ctx.rectangle(-500, ground_y, W + 1000, 1200); fill(ctx, (0.10, 0.16, 0.12))
    for gx, gs in ((140, 0.7), (380, 0.9), (930, 0.75)):
        tombstone(ctx, gx, ground_y - 120 * gs, gs)
    for k in range(-2, 12):  # valla
        ctx.rectangle(k * 110, ground_y - 230, 14, 240); fill(ctx, (0.05, 0.06, 0.08))
    ctx.rectangle(-300, ground_y - 200, W + 600, 12); fill(ctx, (0.05, 0.06, 0.08))


def money_bag(ctx, x, y, s=1.0, label="$"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    circle(ctx, 0, 40, 150); fill(ctx, (0.55, 0.45, 0.25))
    ctx.move_to(-60, -100); ctx.line_to(60, -100); ctx.line_to(30, -60); ctx.line_to(-30, -60); ctx.close_path()
    fill(ctx, (0.55, 0.45, 0.25))
    rrect(ctx, -70, -80, 140, 26, 10); fill(ctx, (0.35, 0.25, 0.12))
    text(ctx, label, 0, 60, 120, GOLD)
    ctx.restore()


def phone(ctx, x, y, s=1.0, ring=0.0, T=0.0):
    """Teléfono antiguo de disco."""
    ctx.save(); ctx.translate(x + math.sin(T * 60) * 6 * ring, y); ctx.scale(s, s)
    rrect(ctx, -170, -40, 340, 200, 40); fill(ctx, (0.12, 0.12, 0.14))
    circle(ctx, 0, 60, 80); fill(ctx, (0.85, 0.85, 0.8))
    circle(ctx, 0, 60, 30); fill(ctx, (0.12, 0.12, 0.14))
    rrect(ctx, -210, -120, 420, 70, 35); fill(ctx, (0.12, 0.12, 0.14))
    if ring > 0:
        for k in (1, 2):
            ctx.arc(0, -40, 220 + k * 50, -2.4, -0.7); stroke(ctx, WHITE, 8, 0.6 * ring)
    ctx.restore()


def cornfield(ctx, T, y0=1100):
    ctx.set_source(vgrad(ctx, 0, 0, 0, y0, [(0, (0.10, 0.12, 0.30)), (1, (0.30, 0.25, 0.40))])); ctx.paint()
    ctx.rectangle(-500, y0, W + 1000, 1500); fill(ctx, (0.20, 0.16, 0.08))
    for row in range(5):
        yy = y0 + 40 + row * 140
        for k in range(-2, 14):
            xx = k * 95 + (row % 2) * 45
            sw = math.sin(T * 2 + k + row) * 10
            ctx.move_to(xx, yy + 120); ctx.curve_to(xx + sw, yy + 40, xx + sw * 2, yy - 60, xx + sw * 3, yy - 160 + row * 10)
            stroke(ctx, (0.75, 0.65, 0.25), 12)
            rrect(ctx, xx + sw * 2 - 12, yy - 120, 24, 70, 12); fill(ctx, (0.95, 0.80, 0.30))


def bars(ctx, x, y, w, h, a=1.0):
    """Barrotes de cárcel."""
    for k in range(7):
        ctx.rectangle(x - w / 2 + k * w / 6 - 12, y - h / 2, 24, h); fill(ctx, (0.25, 0.25, 0.30), a)
    ctx.rectangle(x - w / 2 - 20, y - h / 2, w + 40, 30); fill(ctx, (0.25, 0.25, 0.30), a)
    ctx.rectangle(x - w / 2 - 20, y + h / 2 - 30, w + 40, 30); fill(ctx, (0.25, 0.25, 0.30), a)


def stamp(ctx, label, x, y, appear=1.0, col=RED, rot=-0.18, size=90):
    """Sello de goma ('STOLEN', 'DEAD?'...) que cae con golpe."""
    if appear <= 0.01:
        return
    s = 1.6 - 0.6 * ease_out(clamp(appear))
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    w = text_width(ctx, label, size) + 60
    rrect(ctx, -w / 2, -size * 0.75, w, size * 1.5, 16); stroke(ctx, col, 10, clamp(appear * 2))
    text(ctx, label, 0, 0, size, col, a=clamp(appear * 2), shadow=False)
    ctx.restore()
