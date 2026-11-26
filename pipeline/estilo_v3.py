"""Piezas comunes del FORMATO v3 / formato «historia» (25-26/11/2026). Uso en escenas.py:
    from kit import *
    from estilo_v3 import *
    set_azul(t_you_see, t_fin_explicacion)   # arco de luz cálido -> azul -> cálido
Incluye: paleta con arco de luz (pal), tinta (ink/fill_ink), desenfoque (blur_layer), cielo, calle con casas,
personaje plano con parpadeo (worker), bocadillo (bubble), ✓/✗ (check), calendario (cal), etiquetas (label),
grietas (zig/partial/crack_path) y flechas de cota (cota).
Subtítulos ABAJO por defecto (orden del dueño, 26/11/2026): Y_SUBTITULO = 1430 -> lo esencial va entre y 250 y 1300."""
from kit import *  # noqa

INKC = (0.13, 0.08, 0.16)
_AZ = [10_000.0, 10_001.0]


def set_azul(t0, t1):
    _AZ[0], _AZ[1] = t0, t1


def mix(a, b, x):
    return tuple(p + (q - p) * x for p, q in zip(a, b))


WARM = dict(sky0=(0.40, 0.62, 0.95), sky1=(1.00, 0.86, 0.62), grass=(0.45, 0.70, 0.32), grass_d=(0.32, 0.54, 0.27),
            conc=(0.86, 0.84, 0.80), conc_d=(0.66, 0.63, 0.66), road=(0.36, 0.36, 0.42), sun=(1.0, 0.88, 0.58),
            metal=(0.86, 0.88, 0.94), metal_d=(0.58, 0.60, 0.72))
NIGHT = dict(sky0=(0.06, 0.09, 0.26), sky1=(0.20, 0.25, 0.52), grass=(0.16, 0.27, 0.36), grass_d=(0.11, 0.19, 0.30),
             conc=(0.62, 0.66, 0.84), conc_d=(0.40, 0.42, 0.62), road=(0.16, 0.17, 0.30), sun=(0.92, 0.94, 1.0),
             metal=(0.66, 0.72, 0.92), metal_d=(0.38, 0.42, 0.64))


def luz(T):
    t0, t1 = _AZ
    if T < t0 - 0.3 or T > t1 + 0.3:
        return 0.0
    if T < t0 + 0.3:
        return ease((T - t0 + 0.3) / 0.6)
    if T > t1 - 0.3:
        return 1 - ease((T - t1 + 0.3) / 0.6)
    return 1.0


def pal(T):
    x = luz(T)
    return {k: mix(WARM[k], NIGHT[k], x) for k in WARM}


def ink(ctx, w=4.5):
    stroke(ctx, INKC, w)


def fill_ink(ctx, rgb, w=4.5, a=1.0):
    fill_keep(ctx, rgb, a)
    ink(ctx, w)


def blur_layer(ctx, draw, k=5):
    """Fondo desenfocado: draw(c) dibuja (con su propia cámara) a baja resolución y se amplía suavizado."""
    sw, sh = int(W / k) + 1, int(H / k) + 1
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    c = cairo.Context(s); c.scale(1 / k, 1 / k); draw(c)
    s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw // 2 + 1, sh // 2 + 1)
    c2 = cairo.Context(s2); c2.scale(0.5, 0.5)
    p = cairo.SurfacePattern(s); p.set_filter(cairo.FILTER_GOOD); c2.set_source(p); c2.paint()
    ctx.save(); ctx.scale(k * 2, k * 2)
    p2 = cairo.SurfacePattern(s2); p2.set_filter(cairo.FILTER_BILINEAR); ctx.set_source(p2); ctx.paint()
    ctx.restore()


def label(ctx, s, x, y, a, rgb=YELLOW, size=50):
    pill(ctx, s, x, y, a, size=size, rgb=rgb)


def check(ctx, x, y, s, a=1.0, ok=True):
    if a <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * a, s * a)
    circle(ctx, 0, 0, 60); fill_ink(ctx, (0.30, 0.78, 0.40) if ok else RED, 5)
    if ok:
        ctx.move_to(-28, 2); ctx.line_to(-6, 24); ctx.line_to(30, -22)
    else:
        ctx.move_to(-24, -24); ctx.line_to(24, 24); ctx.move_to(24, -24); ctx.line_to(-24, 24)
    stroke(ctx, WHITE, 12)
    ctx.restore()


def cal(ctx, x, y, s, top, big, col=RED):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -220, -150, 440, 300, 26); fill_ink(ctx, PAPER, 5)
    rrect(ctx, -220, -150, 440, 80, 26); fill(ctx, col)
    ctx.rectangle(-220, -100, 440, 30); fill(ctx, col)
    text(ctx, top, 0, -110, 40, WHITE, shadow=False)
    text(ctx, big, 0, 45, 96, INKC, shadow=False)
    ctx.restore()


def bubble(ctx, s, x, y, a, size=46, tail=-1):
    """Bocadillo de diálogo; tail=-1 cola a la izquierda abajo, 1 a la derecha."""
    if a <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(a, a)
    w = text_width(ctx, s, size) + 70
    rrect(ctx, -w / 2, -60, w, 120, 40); fill_ink(ctx, WHITE, 5)
    ctx.move_to(tail * 40, 55); ctx.line_to(tail * 90, 120); ctx.line_to(tail * 10, 58); fill(ctx, WHITE)
    ctx.move_to(tail * 40, 58); ctx.line_to(tail * 90, 120); ctx.line_to(tail * 10, 60); ink(ctx, 5)
    text(ctx, s, 0, 0, size, INKC, shadow=False)
    ctx.restore()


def sky(ctx, T, P, sun=True):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, P["sky0"]), (0.6, P["sky1"]), (1, P["sky1"])]))
    ctx.paint()
    x = luz(T)
    if sun:
        spotlight(ctx, 870, 330, 380, 0.35, P["sun"])
        circle(ctx, 870, 330, 75 - 22 * x); fill(ctx, P["sun"])
    if x > 0.05:
        rng = np.random.default_rng(4)
        for k in range(40):
            circle(ctx, rng.uniform(-200, 1300), rng.uniform(-300, 900), 3 + 2 * math.sin(T * 3 + k)); fill(ctx, (1, 1, 1), 0.7 * x)


def house2(ctx, x, y, s, col=(0.92, 0.62, 0.48)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-170, -240, 340, 240); fill_ink(ctx, col, 4)
    ctx.move_to(-200, -240); ctx.line_to(0, -400); ctx.line_to(200, -240); ctx.close_path(); fill_ink(ctx, (0.55, 0.28, 0.26), 4)
    rrect(ctx, -40, -130, 80, 130, 8); fill_ink(ctx, WOOD, 3)
    for sx in (-1, 1):
        rrect(ctx, sx * 110 - 40, -200, 80, 70, 6); fill_ink(ctx, (1, 0.9, 0.6), 3)
    ctx.restore()


def ground(ctx, y, P, col=None):
    ctx.rectangle(-800, y, W + 1600, 2600)
    if col is None:
        ctx.set_source(vgrad(ctx, 0, y, 0, y + 1100, [(0, P["grass"]), (1, P["grass_d"])])); ctx.fill()
    else:
        fill(ctx, col)
    ctx.move_to(-800, y); ctx.line_to(W + 800, y); ink(ctx, 4)


def worker(ctx, x, y, s, T, col=(0.25, 0.50, 0.85), mood="normal", k=0, hat=(1.0, 0.80, 0.20), boss=False, look=0.0,
           arm=0.0, tie=None, hat_kind="helmet"):
    """Personaje plano propio (no representa a nadie real): parpadeo y balanceo. (x, y) = centro de la cabeza; pies en y+300*s.
    mood: normal | feliz | triste | shock. boss=True: más ancho y con bigote. hat_kind: helmet | cap | none."""
    bob = 5 * math.sin(T * 5 + k)
    ctx.save(); ctx.translate(x, y + bob); ctx.scale(s, s)
    soft_shadow(ctx, 0, 300 - bob / s, 85, 16, 0.35)
    for sx in (-1, 1):
        ctx.move_to(sx * 22, 170); ctx.line_to(sx * 30, 300); stroke(ctx, INKC, 12)
    rrect(ctx, -62 - 12 * boss, 40, 124 + 24 * boss, 140, 40); fill_ink(ctx, col, 4)
    if tie:
        ctx.move_to(-10, 46); ctx.line_to(10, 46); ctx.line_to(6, 120); ctx.line_to(0, 132); ctx.line_to(-6, 120); ctx.close_path(); fill_ink(ctx, tie, 3)
    ctx.move_to(-55, 70); ctx.line_to(-95, 150 + 10 * math.sin(T * 4 + k)); stroke(ctx, INKC, 10)
    ctx.move_to(55, 70); ctx.line_to(95 + 30 * arm, 150 - 90 * arm + 10 * math.sin(T * 4 + k + 1)); stroke(ctx, INKC, 10)
    ctx.save(); ctx.scale(1, 1.1); circle(ctx, 0, -10, 62); ctx.restore()
    fill_ink(ctx, (0.98, 0.84, 0.70), 4)
    if hat_kind == "helmet":
        ctx.new_path(); ctx.arc(0, -34, 68, math.pi, 0); ctx.close_path(); fill_ink(ctx, hat, 4)
        ctx.rectangle(-86, -38, 172, 14); fill_ink(ctx, hat, 3)
    elif hat_kind == "cap":
        ctx.new_path(); ctx.arc(0, -34, 64, math.pi, 0); ctx.close_path(); fill_ink(ctx, hat, 4)
        rrect(ctx, 0, -44, 100, 16, 8); fill_ink(ctx, hat, 3)
    else:
        ctx.new_path(); ctx.arc(0, -40, 60, math.pi * 1.05, -0.05); ctx.close_path(); fill_ink(ctx, (0.45, 0.30, 0.18), 4)
    ph = (T * 0.7 + k * 0.37) % 1.0
    blink = 0.12 if ph < 0.05 else 1.0
    big = 1.6 if mood == "shock" else 1.0
    for sx in (-1, 1):
        ellipse(ctx, sx * 22 + look * 10, -2, 7 * big, 9 * blink * big); fill(ctx, INKC)
    if boss:
        ctx.move_to(-40, 22); ctx.curve_to(-20, 8, 20, 8, 40, 22); ctx.curve_to(20, 34, -20, 34, -40, 22); fill(ctx, (0.40, 0.26, 0.16))
    if mood == "triste":
        ctx.new_path(); ctx.arc(0, 46, 16, math.pi * 1.15, math.pi * 1.85); ink(ctx, 4)
    elif mood == "feliz":
        ctx.new_path(); ctx.arc(0, 30, 16, 0.15 * math.pi, 0.85 * math.pi); ink(ctx, 4)
    elif mood == "shock":
        ellipse(ctx, 0, 40, 12, 16); fill(ctx, INKC)
    else:
        ctx.move_to(-12, 36); ctx.line_to(12, 36); ink(ctx, 4)
    ctx.restore()


def crack_path(ctx, pts, w, col=INKC, a=1.0):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    stroke(ctx, col, w, a)


def zig(x0, y0, x1, y1, n, amp, seed):
    rng = np.random.default_rng(seed)
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t + (rng.uniform(-amp, amp) if 0 < i < n else 0),
                    y0 + (y1 - y0) * t + (rng.uniform(-amp, amp) if 0 < i < n else 0)))
    return pts


def partial(pts, p):
    if p <= 0:
        return pts[:1]
    n = len(pts) - 1
    k = int(p * n)
    out = pts[:k + 1]
    if k < n:
        f = p * n - k
        a, b = pts[k], pts[k + 1]
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return out


def cota(ctx, x0, y0, x1, y1, a, txt, rgb=YELLOW, size=50, dy=-70):
    """Flecha de medida de doble punta + etiqueta."""
    if a <= 0.01:
        return
    arrow(ctx, x0, y0, x1, y1, a, rgb=rgb, w=10); arrow(ctx, x1, y1, x0, y0, a, rgb=rgb, w=10)
    label(ctx, txt, (x0 + x1) / 2, (y0 + y1) / 2 + dy, a, rgb=rgb, size=size)


def rain(ctx, T, a=1.0, n=70, seed=3):
    rng = np.random.default_rng(seed)
    for k in range(n):
        x = (rng.uniform(-200, 1300) + T * 180) % 1400 - 160
        y = (rng.uniform(0, 1920) + T * 1700) % 2000 - 40
        ctx.move_to(x, y); ctx.line_to(x - 12, y + 46); stroke(ctx, (0.75, 0.85, 1.0), 4, 0.6 * a)


def gancho(ctx, lineas, T, t_fin=2.8, y=200, size=110):
    """Texto de GANCHO fijo arriba desde el fotograma 0 (análisis 26/11/2026: los Shorts que más gente
    retiene enseñan la pregunta/contradicción en grande antes de que hable la voz). lineas = ["WHY", ("ROUND?", WHITE)].
    Se va con un fundido rápido en t_fin. Los subtítulos van abajo, así que no chocan."""
    a = 1.0 if T < t_fin else max(0.0, 1 - (T - t_fin) / 0.25)
    if a <= 0.01:
        return
    ctx.push_group()
    thumb_text(ctx, lineas, y=y, size=size)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(a)
