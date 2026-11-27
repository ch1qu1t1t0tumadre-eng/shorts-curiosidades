"""v27 (EN) PRUEBA formato «historia» (referencia: You Change History, "Why He Built His Bridge Six Inches Too Short",
3,2 M en 1 día): historia inventada con física real -> por qué las aceras tienen líneas (juntas de control).
Base técnica = formato v3 (Pisa): arco de luz, tinta, pocos cortes, más sonido, subtítulo arriba sin tapar nada."""
from kit import *  # noqa

FLASH = False
WHOOSH = False
MUSICA_GAIN = 0.42
FX_GAIN = 0.30
Y_SUBTITULO = 1430     # subtítulos ABAJO (orden del dueño, 26/11/2026)
TAM_SUBTITULO = 135
CORTES = [(5.44, 7.98)]  # quitado "and the city will hire whoever builds the best sidewalk." (relleno 4-9 s)

INKC = (0.13, 0.08, 0.16)
T_AZUL0, T_AZUL1 = 33.10, 41.60   # "You see" -> "hid them."


def mix(a, b, x):
    return tuple(p + (q - p) * x for p, q in zip(a, b))


WARM = dict(sky0=(0.40, 0.62, 0.95), sky1=(1.00, 0.86, 0.62), grass=(0.45, 0.70, 0.32), grass_d=(0.32, 0.54, 0.27),
            conc=(0.86, 0.84, 0.80), conc_d=(0.66, 0.63, 0.66), road=(0.36, 0.36, 0.42), sun=(1.0, 0.88, 0.58))
NIGHT = dict(sky0=(0.06, 0.09, 0.26), sky1=(0.20, 0.25, 0.52), grass=(0.16, 0.27, 0.36), grass_d=(0.11, 0.19, 0.30),
             conc=(0.62, 0.66, 0.84), conc_d=(0.40, 0.42, 0.62), road=(0.16, 0.17, 0.30), sun=(0.92, 0.94, 1.0))


def luz(T):
    if T < T_AZUL0 - 0.3 or T > T_AZUL1 + 0.3:
        return 0.0
    if T < T_AZUL0 + 0.3:
        return ease((T - T_AZUL0 + 0.3) / 0.6)
    if T > T_AZUL1 - 0.3:
        return 1 - ease((T - T_AZUL1 + 0.3) / 0.6)
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


# ---------------- mundo ----------------
def sky(ctx, T, P):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, P["sky0"]), (0.6, P["sky1"]), (1, P["sky1"])]))
    ctx.paint()
    x = luz(T)
    spotlight(ctx, 870, 330, 380, 0.35, P["sun"])
    circle(ctx, 870, 330, 75 - 22 * x); fill(ctx, P["sun"])
    if x > 0.05:
        rng = np.random.default_rng(4)
        for k in range(40):
            circle(ctx, rng.uniform(-200, 1300), rng.uniform(-300, 900), 3 + 2 * math.sin(T * 3 + k)); fill(ctx, (1, 1, 1), 0.7 * x)


def house(ctx, x, y, s, P, col=(0.92, 0.62, 0.48)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-170, -240, 340, 240); fill_ink(ctx, mix(col, P["sky0"], 0.15 * luz(0)), 4)
    ctx.move_to(-200, -240); ctx.line_to(0, -400); ctx.line_to(200, -240); ctx.close_path(); fill_ink(ctx, (0.55, 0.28, 0.26), 4)
    rrect(ctx, -40, -130, 80, 130, 8); fill_ink(ctx, WOOD, 3)
    for sx in (-1, 1):
        rrect(ctx, sx * 110 - 40, -200, 80, 70, 6); fill_ink(ctx, (1, 0.9, 0.6), 3)
    ctx.restore()


def street(ctx, T, P, horizon=700, houses=True):
    sky(ctx, T, P)
    if houses:
        for k, (hx, hs, hc) in enumerate(((120, 0.55, (0.92, 0.62, 0.48)), (420, 0.45, (0.55, 0.70, 0.88)),
                                          (700, 0.5, (0.95, 0.82, 0.48)), (980, 0.55, (0.70, 0.86, 0.62)))):
            house(ctx, hx, horizon, hs, P, hc)
    ctx.rectangle(-800, horizon, W + 1600, 2400)
    ctx.set_source(vgrad(ctx, 0, horizon, 0, horizon + 1100, [(0, P["grass"]), (1, P["grass_d"])])); ctx.fill()
    ctx.move_to(-800, horizon); ctx.line_to(W + 800, horizon); ink(ctx, 4)


def persp_walk(ctx, cx, P, top=720, bot=2000, wt=90, wb=620, joints=True, cut_upto=1.0, shine=0.0, T=0.0,
               wet=0.0, cracks=0.0, seed=1):
    """Acera en perspectiva (se aleja hacia el horizonte). joints = líneas cortadas; cut_upto = hasta dónde (0..1 desde abajo)."""
    ctx.move_to(cx - wb / 2, bot); ctx.line_to(cx - wt / 2, top); ctx.line_to(cx + wt / 2, top); ctx.line_to(cx + wb / 2, bot)
    ctx.close_path()
    col = mix(P["conc"], (0.55, 0.55, 0.62), wet * 0.5)
    fill_ink(ctx, col, 4)
    rng = np.random.default_rng(seed)
    for k in range(60):  # granulado
        u, v = rng.uniform(0, 1), rng.uniform(0.05, 1)
        yy = top + (bot - top) * v ** 1.6
        ww = wt + (wb - wt) * ((yy - top) / (bot - top))
        circle(ctx, cx + (u - 0.5) * ww * 0.9, yy, 2 + 3 * v); fill(ctx, P["conc_d"], 0.5)
    if joints:
        for k in range(1, 9):
            v = 1 - (k / 9) ** 0.65            # 1 = abajo
            if (1 - v) > cut_upto + 1e-6 and cut_upto < 1:
                continue
            yy = top + (bot - top) * v
            ww = wt + (wb - wt) * v
            ctx.move_to(cx - ww / 2, yy); ctx.line_to(cx + ww / 2, yy); stroke(ctx, mix(P["conc_d"], INKC, 0.5), 3 + 7 * v)
    if shine > 0:
        x0 = cx - wb / 2 + (wb + 400) * ((T * 0.45) % 1.0) - 200
        ctx.save()
        ctx.move_to(cx - wb / 2, bot); ctx.line_to(cx - wt / 2, top); ctx.line_to(cx + wt / 2, top); ctx.line_to(cx + wb / 2, bot); ctx.close_path()
        ctx.clip()
        ctx.move_to(x0, bot); ctx.line_to(x0 + 160, bot); ctx.line_to(x0 + 260, top); ctx.line_to(x0 + 200, top); ctx.close_path()
        fill(ctx, WHITE, 0.35 * shine)
        ctx.restore()


def worker(ctx, x, y, s, T, col=(0.25, 0.50, 0.85), mood="normal", k=0, hat=(1.0, 0.80, 0.20), boss=False, look=0.0,
           arm=0.0):
    """Personaje plano propio con parpadeo y balanceo. boss=True: más grande, bigote."""
    bob = 5 * math.sin(T * 5 + k)
    ctx.save(); ctx.translate(x, y + bob); ctx.scale(s, s)
    soft_shadow(ctx, 0, 300 - bob / s, 85, 16, 0.35)
    for sx in (-1, 1):
        ctx.move_to(sx * 22, 170); ctx.line_to(sx * 30, 300); stroke(ctx, INKC, 12)
    rrect(ctx, -62 - 12 * boss, 40, 124 + 24 * boss, 140, 40); fill_ink(ctx, col, 4)
    ctx.move_to(-55, 70); ctx.line_to(-95, 150 + 10 * math.sin(T * 4 + k)); stroke(ctx, INKC, 10)
    ctx.move_to(55, 70); ctx.line_to(95 + 30 * arm, 150 - 90 * arm + 10 * math.sin(T * 4 + k + 1)); stroke(ctx, INKC, 10)
    ctx.save(); ctx.scale(1, 1.1); circle(ctx, 0, -10, 62); ctx.restore()
    fill_ink(ctx, (0.98, 0.84, 0.70), 4)
    ctx.new_path(); ctx.arc(0, -34, 68, math.pi, 0); ctx.close_path(); fill_ink(ctx, hat, 4)
    ctx.rectangle(-86, -38, 172, 14); fill_ink(ctx, hat, 3)
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


def blade(ctx, x, y, s, rot=0.0):
    """Herramienta de cortar juntas (mango + hoja)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, -170); stroke(ctx, WOOD, 16); ctx.move_to(0, 0); ctx.line_to(0, -170); ink(ctx, 3)
    rrect(ctx, -70, -6, 140, 26, 8); fill_ink(ctx, (0.76, 0.78, 0.86), 4)
    ctx.move_to(-10, 20); ctx.line_to(0, 40); ctx.line_to(10, 20); ctx.close_path(); fill_ink(ctx, (0.76, 0.78, 0.86), 3)
    ctx.restore()


def bubble(ctx, s, x, y, a, size=46, tail=(-1, 1)):
    if a <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(a, a)
    w = text_width(ctx, s, size) + 70
    rrect(ctx, -w / 2, -60, w, 120, 40); fill_ink(ctx, WHITE, 5)
    ctx.move_to(tail[0] * 40, 55); ctx.line_to(tail[0] * 90, 120); ctx.line_to(tail[0] * 10, 58); fill(ctx, WHITE)
    ctx.move_to(tail[0] * 40, 58); ctx.line_to(tail[0] * 90, 120); ctx.line_to(tail[0] * 10, 60); ink(ctx, 5)
    text(ctx, s, 0, 0, size, INKC, shadow=False)
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
    """Primeros p (0..1) del recorrido."""
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


def slab_top(ctx, x, y, w, h, P, joints=0, crack=0.0, kind="random", seed=3, T=0.0, snow=0.0):
    """Losa vista desde arriba (rectángulo). joints = nº de juntas. crack 0..1 = cuánto se ha agrietado."""
    rrect(ctx, x - w / 2, y - h / 2, w, h, 10); fill_ink(ctx, P["conc"], 5)
    rng = np.random.default_rng(seed + 10)
    for k in range(40):
        circle(ctx, x + rng.uniform(-w / 2 + 10, w / 2 - 10), y + rng.uniform(-h / 2 + 10, h / 2 - 10), 3); fill(ctx, P["conc_d"], 0.5)
    for j in range(1, joints + 1):
        jy = y - h / 2 + h * j / (joints + 1)
        ctx.move_to(x - w / 2, jy); ctx.line_to(x + w / 2, jy); stroke(ctx, mix(P["conc_d"], INKC, 0.45), 10)
    if crack > 0:
        if kind == "random":
            paths = [zig(x - w / 2, y - h * 0.3, x + w / 2, y + h * 0.1, 9, 40, seed),
                     zig(x - w * 0.1, y - h / 2, x + w * 0.15, y + h / 2, 10, 45, seed + 1),
                     zig(x - w / 2, y + h * 0.25, x + w * 0.35, y - h * 0.05, 8, 40, seed + 2),
                     zig(x + w * 0.2, y - h / 2, x + w / 2, y - h * 0.1, 6, 30, seed + 3)]
            for i, pth in enumerate(paths):
                p = clamp(crack * len(paths) - i)
                if p > 0:
                    crack_path(ctx, partial(pth, p), 7)
        else:  # dentro de las juntas
            for j in range(1, joints + 1):
                jy = y - h / 2 + h * j / (joints + 1)
                pth = zig(x - w / 2, jy, x + w / 2, jy, 10, 5, seed + j)
                crack_path(ctx, partial(pth, clamp(crack * 1.2 - 0.1 * j)), 6)
    if snow > 0:
        rng2 = np.random.default_rng(12)
        for k in range(40):
            circle(ctx, x + rng2.uniform(-w / 2, w / 2), y + rng2.uniform(-h / 2, h / 2), 8); fill(ctx, WHITE, 0.75 * snow)


def section(ctx, x, y, w, h, P, grooves=(), crack_at=None, crack=0.0, random_crack=0.0, seed=5):
    """Corte de la losa (de lado). grooves = posiciones x (0..1) de las juntas."""
    ctx.move_to(x - w / 2, y - h / 2)
    for gx in sorted(grooves):
        px = x - w / 2 + w * gx
        ctx.line_to(px - 45, y - h / 2); ctx.line_to(px, y - h / 2 + h * 0.25); ctx.line_to(px + 45, y - h / 2)
    ctx.line_to(x + w / 2, y - h / 2); ctx.line_to(x + w / 2, y + h / 2); ctx.line_to(x - w / 2, y + h / 2); ctx.close_path()
    fill_ink(ctx, P["conc"], 5)
    rng = np.random.default_rng(seed)
    for k in range(50):
        circle(ctx, x + rng.uniform(-w / 2 + 12, w / 2 - 12), y + rng.uniform(-h / 2 + 30, h / 2 - 12), rng.uniform(3, 9))
        fill(ctx, P["conc_d"], 0.6)
    if crack_at is not None and crack > 0:
        px = x - w / 2 + w * crack_at
        pth = zig(px, y - h / 2 + h * 0.25, px + 6, y + h / 2, 6, 10, seed + 3)
        crack_path(ctx, partial(pth, crack), 7)
    if random_crack > 0:
        pth = zig(x - w * 0.12, y - h / 2, x + w * 0.05, y + h / 2, 7, 26, seed + 7)
        crack_path(ctx, partial(pth, random_crack), 7)


def choco(ctx, x, y, s, T, snap=0.0):
    """Tableta de chocolate 2x3 que se parte por el surco."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for half, dx in ((0, -1), (1, 1)):
        ctx.save()
        off = 50 * snap * dx
        ctx.translate(off, 0); ctx.rotate(0.12 * snap * dx)
        x0 = -240 if half == 0 else 0
        rrect(ctx, x0 + (6 if half else 0), -180, 234, 360, 18); fill_ink(ctx, (0.45, 0.25, 0.14), 5)
        for r in range(3):
            rrect(ctx, x0 + 26 + (6 if half else 0), -160 + r * 115, 190, 95, 14); fill_ink(ctx, (0.56, 0.33, 0.19), 3)
        ctx.restore()
    if snap <= 0.02:
        ctx.move_to(0, -180); ctx.line_to(0, 180); stroke(ctx, (0.28, 0.14, 0.07), 10)
    ctx.restore()


def hero(ctx, lt, T, dur, z0, z1):
    """Plano del gancho (inicio y final del bucle)."""
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2, 1400)
    street(ctx, T, P, horizon=700)
    persp_walk(ctx, W / 2, P, wet=0.6, cut_upto=0.45, seed=1)
    # línea que se está cortando ahora
    v = 0.55
    yy, ww = 720 + (2000 - 720) * v, 90 + (620 - 90) * v
    p = (T * 0.6) % 1.0
    ctx.move_to(W / 2 - ww / 2, yy); ctx.line_to(W / 2 - ww / 2 + ww * p, yy); stroke(ctx, mix(P["conc_d"], INKC, 0.5), 9)
    worker(ctx, W / 2 - ww / 2 + ww * p + 50, yy - 265, 0.85, T, k=1, mood="feliz", arm=0.6)
    blade(ctx, W / 2 - ww / 2 + ww * p + 10, yy - 2, 0.9, rot=0.3)
    ctx.restore()


# ---------------- escenas ----------------
# 0.00 "This guy cut lines into his brand-new sidewalk on purpose."
def e1(ctx, lt, dur, T):
    from estilo_v3 import gancho
    if T < 2.10:
        hero(ctx, lt, T, dur, 1.75, 1.6)
    else:   # "sidewalk" -> corte seco: lisa y rota ✗ contra con líneas ✓
        P = pal(T)
        ctx.save()
        camera(ctx, keyframes(lt - 2.1, [(0, 1.08), (dur - 2.1, 1.0)]), W / 2, 800)
        sky(ctx, T, P)
        ctx.restore()
        slab_top(ctx, 290, 820, 360, 620, P, joints=0, crack=1.0, kind="random", seed=3, T=T)
        slab_top(ctx, 790, 820, 360, 620, P, joints=3, crack=0.0, T=T)
        check(ctx, 290, 1230, 0.9, pop(lt, 2.15), ok=False)
        check(ctx, 790, 1230, 0.9, pop(lt, 2.35), ok=True)
    gancho(ctx, ["WHY DO SIDEWALKS", ("HAVE LINES?", WHITE)], T, t_fin=3.2, size=100)


# 3.44 "See, two crews are paving the same street, and the city will hire whoever builds the best sidewalk."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 0.98)]), W / 2, 1050)
    street(ctx, T, P, horizon=700)
    ctx.move_to(W / 2 - 300, 2000); ctx.line_to(W / 2 - 40, 720); ctx.line_to(W / 2 + 40, 720); ctx.line_to(W / 2 + 300, 2000); ctx.close_path()
    fill_ink(ctx, P["road"], 4)
    for k in range(6):
        v = 1 - (k / 6) ** 0.7
        yy = 720 + 1280 * v
        ctx.move_to(W / 2, yy); ctx.line_to(W / 2, yy - 60 * v - 10); stroke(ctx, YELLOW, 4 + 8 * v)
    persp_walk(ctx, W / 2 - 330, P, top=720, wt=60, wb=420, joints=False, seed=2)
    persp_walk(ctx, W / 2 + 330, P, top=720, wt=60, wb=420, joints=False, seed=3)
    worker(ctx, 170, 1040, 0.7, T, col=(0.25, 0.50, 0.85), k=1)
    worker(ctx, 910, 1040, 0.7, T, col=(0.85, 0.25, 0.25), k=2, hat=(0.95, 0.95, 0.95))
    ctx.restore()
    label(ctx, "THE KID'S CREW", 230, 640, pop(lt, 0.4), rgb=(0.35, 0.60, 1.0), size=40)
    label(ctx, "RIVAL CREW", 850, 640, pop(lt, 0.7), rgb=RED, size=40)
    a = pop(lt, 5.74 - 3.44)
    if a > 0.01:
        ctx.save(); ctx.translate(W / 2, 1460); ctx.scale(a, a)
        rrect(ctx, -330, -80, 660, 160, 30); fill_ink(ctx, PAPER, 5)
        text(ctx, "CITY: BEST ONE WINS", 0, 0, 50, INKC, shadow=False)
        ctx.restore()


# 8.02 "His boss sees him dragging a blade through the wet concrete. Kid, you're ruining it."
def e3(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 1000), street(c, T, P)))
    ctx.save()
    camera(ctx, z, W / 2, 1000)
    persp_walk(ctx, W / 2 + 120, P, top=900, bot=2100, wt=240, wb=900, wet=0.7, cut_upto=0.25, seed=4)
    p = clamp((T - 8.86) / 1.6)
    worker(ctx, 600 + 160 * p, 980, 0.95, T, k=1, mood="feliz", arm=0.5)
    blade(ctx, 560 + 160 * p, 1300, 1.0, rot=0.3)
    ctx.move_to(420, 1300); ctx.line_to(560 + 160 * p, 1300); stroke(ctx, mix(P["conc_d"], INKC, 0.5), 12)
    worker(ctx, 200, 930, 1.05, T, col=(0.55, 0.42, 0.30), k=3, boss=True, mood="shock" if T > 9.4 else "normal")
    ctx.restore()
    label(ctx, "BOSS", 200, 600, pop(lt, 0.3), rgb=GOLD, size=42)
    label(ctx, "THE KID", 760, 640, pop(lt, 0.6), rgb=(0.35, 0.60, 1.0), size=42)
    bubble(ctx, "KID, YOU'RE RUINING IT!", W / 2, 300, pop(lt, 10.78 - 8.02), size=46)


# 11.92 "But the kid keeps going. A line every ten feet, one inch deep."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.15)]), W / 2, 900)
    sky(ctx, T, P)
    ctx.rectangle(-800, 1040, W + 1600, 1600); fill_ink(ctx, mix(P["grass_d"], (0.45, 0.32, 0.22), 0.6), 4)
    n = int(clamp((T - 12.2) / 1.3) * 3 + 0.999)
    section(ctx, W / 2, 900, 1000, 260, P, grooves=[(0.2, 0.5, 0.8)[i] for i in range(min(n, 3))])
    ctx.restore()
    # medidas
    if T > 13.95:
        a = pop(lt, 13.95 - 11.92)
        arrow(ctx, 215, 680, 540, 680, a, rgb=YELLOW, w=10); arrow(ctx, 540, 680, 215, 680, a, rgb=YELLOW, w=10)
        label(ctx, "10 FT", 378, 590, a, rgb=YELLOW, size=56)
    if T > 14.66:
        a = pop(lt, 14.66 - 11.92)
        label(ctx, "1 IN DEEP", 760, 1240, a, rgb=RED, size=50)
        arrow(ctx, 740, 1180, 690, 900, a, rgb=RED, w=10)
    label(ctx, "CONCRETE", W / 2, 300, pop(lt, 0.4), rgb=STONE, size=48)


# 15.13 "The other crew pours theirs perfectly smooth. Like a mirror. Everybody loves the smooth one."
def e5(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 1000)
    street(ctx, T, P)
    persp_walk(ctx, W / 2, P, joints=False, shine=clamp((T - 17.3) / 0.4), T=T, seed=5)
    if T > 18.17:  # gente caminando (siluetas genéricas)
        for k in range(3):
            px = W / 2 - 160 + k * 150 + 20 * math.sin(T * 2 + k)
            gent(ctx, px, 980 + k * 40, 0.42, col=(0.20, 0.20, 0.30), hat=(k == 1))
            icon(ctx, "❤️", px + 40, 870 + k * 40, 90, pop(lt, 18.73 - 15.13 + 0.15 * k))
    worker(ctx, 930, 1010, 0.7, T, col=(0.85, 0.25, 0.25), k=2, hat=(0.95, 0.95, 0.95), mood="feliz")
    ctx.restore()
    label(ctx, "RIVAL CREW", 880, 640, pop(lt, 0.2), rgb=RED, size=40)
    label(ctx, "PERFECTLY SMOOTH", W / 2, 300, pop(lt, 17.10 - 15.13), rgb=YELLOW, size=50)


# 19.82 "Then the concrete dries, and drying concrete shrinks."
def e6(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    sky(ctx, T, P)
    ctx.rectangle(-800, 1040, W + 1600, 1600); fill_ink(ctx, mix(P["grass_d"], (0.45, 0.32, 0.22), 0.6), 4)
    sh = ease(clamp((T - 21.6) / 0.8))
    w = 1000 - 120 * sh
    section(ctx, W / 2, 900, w, 260, P, grooves=())
    for k in range(5):  # vapor que sale
        ph = (T * 0.7 + k * 0.2) % 1.0
        sx = W / 2 - 360 + k * 180
        ctx.move_to(sx, 760 - 200 * ph); ctx.curve_to(sx + 30, 720 - 200 * ph, sx - 30, 680 - 200 * ph, sx, 640 - 200 * ph)
        stroke(ctx, WHITE, 8, 0.6 * (1 - ph))
    ctx.restore()
    if sh > 0.05:
        arrow(ctx, 40, 900, 170, 900, sh, rgb=RED, w=14); arrow(ctx, 1040, 900, 910, 900, sh, rgb=RED, w=14)
    label(ctx, "SHRINKS", W / 2, 1300, pop(lt, 22.08 - 19.82), rgb=RED, size=64)
    label(ctx, "DRYING", W / 2, 520, pop(lt, 0.6), rgb=(0.45, 0.72, 1.0), size=48)


# 22.61 "Week one, a hairline. Month one, a zigzag. By winter, the perfect sidewalk looks like a broken plate."
def e7(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 920)
    snow = ease(clamp((T - 25.2) / 0.6))
    sky(ctx, T, P)
    ctx.rectangle(-800, 0, W + 1600, H); fill(ctx, (0.75, 0.82, 0.95), 0.35 * snow)
    ctx.rectangle(-800, 1150, W + 1600, 1600); fill_ink(ctx, mix(P["grass"], WHITE, 0.6 * snow), 4)
    c = 0.0
    if T > 23.35: c = 0.12 * ease(clamp((T - 23.35) / 0.4))
    if T > 24.51: c = 0.12 + 0.30 * ease(clamp((T - 24.51) / 0.5))
    if T > 26.3: c = 0.42 + 0.58 * ease(clamp((T - 26.3) / 1.4))
    slab_top(ctx, W / 2, 900, 820, 560, P, joints=0, crack=c, kind="random", seed=7, snow=snow)
    ctx.restore()
    label(ctx, "RIVAL'S PERFECT SIDEWALK", W / 2, 530, 1.0, rgb=RED, size=40)
    step = "WEEK 1" if T < 23.80 else ("MONTH 1" if T < 25.09 else "WINTER")
    cal(ctx, W / 2, 300, 0.7, "TIME", step, col=(0.30, 0.45, 0.85) if step == "WINTER" else RED)


# 28.01 "His boss runs to check theirs. Cracks too. But every single crack is hiding at the bottom of a line."
def e8(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 920)
    sky(ctx, T, P)
    ctx.rectangle(-800, 1150, W + 1600, 1600); fill_ink(ctx, mix(P["grass"], WHITE, 0.6), 4)
    c = ease(clamp((T - 29.48) / 1.2))
    slab_top(ctx, W / 2 + 60, 900, 760, 560, P, joints=3, crack=c, kind="joints", seed=9, snow=0.6)
    worker(ctx, 150, 800, 0.62, T, col=(0.55, 0.42, 0.30), k=3, boss=True, mood="shock" if T < 31 else "feliz", look=1)
    ctx.restore()
    label(ctx, "THE KID'S SIDEWALK", W / 2 + 40, 530, 1.0, rgb=(0.35, 0.60, 1.0), size=40)
    if T > 31.5:
        check(ctx, W / 2, 300, 1.2, pop(lt, 31.5 - 28.01), ok=True)
        label(ctx, "ONLY IN THE LINES", W / 2, 1300, pop(lt, 31.7 - 28.01), rgb=(0.30, 0.78, 0.40), size=44)


# 33.10 "You see, concrete always cracks. So he picked where."  (luz azul)
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 960)
    sky(ctx, T, P)
    rc = ease(clamp((T - 34.0) / 0.6))
    section(ctx, W / 2, 700, 820, 200, P, grooves=(), random_crack=rc, seed=11)
    section(ctx, W / 2, 1180, 820, 200, P, grooves=(0.5,), crack_at=0.5, crack=rc, seed=12)
    ctx.restore()
    label(ctx, "NO LINE: ANYWHERE", W / 2, 520, pop(lt, 0.4), rgb=RED, size=42)
    check(ctx, 960, 700, 0.8, pop(lt, 34.5 - 33.10), ok=False)
    label(ctx, "LINE: RIGHT HERE", W / 2, 300, pop(lt, 34.93 - 33.10), rgb=(0.30, 0.78, 0.40), size=42)
    check(ctx, 960, 1180, 0.8, pop(lt, 35.4 - 33.10), ok=True)
    if T > 35.3:
        arrow(ctx, W / 2 + 200, 1330, W / 2 + 20, 1110, clamp((T - 35.3) / 0.4), rgb=YELLOW, w=12)


# 36.00 "Like the grooves on a chocolate bar, it snaps right where you planned."
def e10(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 900)
    sky(ctx, T, P)
    spotlight(ctx, W / 2, 900, 500, 0.3, (1, 0.9, 0.7))
    choco(ctx, W / 2, 900, 1.3, T, snap=ease_back(clamp((T - 37.6) / 0.35)))
    ctx.restore()
    label(ctx, "SNAPS IN THE GROOVE", W / 2, 300, pop(lt, 37.7 - 36.0), rgb=YELLOW, size=46)


# 38.90 "In other words, he didn't stop the cracks. He hid them."
def e11(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.08, dur=dur), W / 2, 900)
    sky(ctx, T, P)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.22); ctx.paint()
    section(ctx, W / 2, 900, 900, 380, P, grooves=(0.5,), crack_at=0.5, crack=1.0, seed=13)
    ctx.restore()
    spotlight(ctx, W / 2, 760, 160, 0.5, (1, 0.95, 0.6))
    stamp(ctx, "HIDDEN", W / 2, 300, (T - 41.2) / 0.25, col=(0.30, 0.78, 0.40), size=110)


# 41.70 "That's why the sidewalk outside your house has lines."
def e12(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 900)
    street(ctx, T, P, houses=False)
    house(ctx, 760, 700, 0.8, P, (0.95, 0.82, 0.48))
    persp_walk(ctx, W / 2 - 120, P, seed=14)
    ctx.restore()
    label(ctx, "YOUR SIDEWALK", 300, 300, pop(lt, 42.19 - 41.70), rgb=YELLOW, size=50)
    for k, (ax, ay) in enumerate(((560, 1330), (620, 1180))):
        arrow(ctx, ax + 180, ay + 80, ax, ay, clamp((T - 43.4 - 0.15 * k) / 0.35), rgb=YELLOW, w=10)


# 44.44 "Because, just like"  -> bucle: "This guy cut lines into his brand-new sidewalk on purpose."
def e13(ctx, lt, dur, T):
    hero(ctx, lt, T, dur, 1.55, 1.75)   # acaba en el encuadre del fotograma 0 (bucle)


ESCENAS = [(0.0, e1), (3.44, e2), (8.02, e3), (11.92, e4), (15.13, e5), (19.82, e6), (22.61, e7), (28.01, e8),
           (33.10, e9), (36.00, e10), (38.90, e11), (41.70, e12), (44.44, e13)]

SFX = [(0.1, "tick"), (2.1, "thud"), (2.3, "crack"), (3.40, "whoosh"), (5.74, "pop"), (7.30, "ding"), (8.9, "tick"), (10.75, "drum"),
       (12.3, "tick"), (12.9, "tick"), (13.5, "tick"), (13.95, "pop"), (14.66, "pop"), (15.1, "whoosh"),
       (17.4, "ding"), (18.8, "pop"), (19.8, "whoosh"), (22.0, "squish"), (23.35, "crack"), (24.5, "crack"),
       (26.3, "crack"), (27.5, "thud"), (28.0, "whoosh"), (29.5, "crack"), (31.6, "ding"), (33.05, "whoosh"),
       (34.0, "crack"), (35.4, "ding"), (37.6, "crack"), (38.85, "thud"), (41.2, "thud"), (41.65, "whoosh"),
       (43.4, "pop"), (44.4, "whoosh")]


def MINIATURA(ctx):
    T = 0.5
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    street(ctx, T, P, horizon=700)
    persp_walk(ctx, W / 2, P, wet=0.6, cut_upto=0.65, seed=1)
    worker(ctx, W / 2 + 120, 1270, 1.0, T, k=1, mood="feliz", arm=0.6)
    blade(ctx, W / 2 + 70, 1600, 1.1, rot=0.3)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["HE RUINED", ("IT ON PURPOSE?", WHITE)], y=260, size=170)
    thumb_circle(ctx, W / 2 - 60, 1600, 330, 90)
