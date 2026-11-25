"""v26 (EN) PRUEBA del análisis Mr omi: The Leaning Tower of Pisa was saved by a war.
Novedades frente al estilo de siempre:
- voz a ~215 ppm, "You see" + analogía (esponja), golpe de humor seco (Luckily / Unluckily)
- arco de luz: cálido (presentación) -> azul noche (explicación) -> cálido (final = principio, bucle)
- sin negros puros, sombras azul/violeta, contorno de tinta en todo
- pocos cortes secos: la cámara viaja dentro de cada "decorado"; sin destello ni whoosh automático
- fondo desenfocado en primeros planos, microanimación (parpadeo, balanceo), efecto de sonido por acción
"""
from kit import *  # noqa

FLASH = False          # sin destello blanco entre escenas
WHOOSH = False         # sin whoosh automático en cada corte (solo en los cortes grandes, vía SFX)
MUSICA_GAIN = 0.42     # música más presente (antes 0.22)
FX_GAIN = 0.30         # efectos más presentes (antes 0.14)
Y_SUBTITULO = 300      # subtítulo arriba, sobre el cielo: nunca tapa la torre
TAM_SUBTITULO = 135

INKC = (0.13, 0.08, 0.16)       # tinta: casi negro violáceo (nunca negro puro)
T_AZUL0, T_AZUL1 = 15.60, 29.30  # "You see" -> "fallen." : luz azul de explicación


def mix(a, b, x):
    return tuple(p + (q - p) * x for p, q in zip(a, b))


WARM = dict(sky0=(0.36, 0.55, 0.92), sky1=(1.00, 0.80, 0.55), grass=(0.42, 0.66, 0.30), grass_d=(0.30, 0.50, 0.26),
            marble=(1.00, 0.96, 0.88), marble_s=(0.62, 0.56, 0.78), sun=(1.0, 0.86, 0.55), far=(0.70, 0.62, 0.78))
NIGHT = dict(sky0=(0.06, 0.09, 0.26), sky1=(0.20, 0.24, 0.52), grass=(0.16, 0.26, 0.36), grass_d=(0.11, 0.18, 0.30),
             marble=(0.70, 0.76, 0.95), marble_s=(0.30, 0.30, 0.55), sun=(0.92, 0.94, 1.0), far=(0.20, 0.22, 0.42))


def luz(T):
    """0 = cálido, 1 = noche azul. Transiciones suaves de 0,6 s."""
    if T < T_AZUL0 - 0.3:
        return 0.0
    if T < T_AZUL0 + 0.3:
        return ease((T - T_AZUL0 + 0.3) / 0.6)
    if T < T_AZUL1 - 0.3:
        return 1.0
    if T < T_AZUL1 + 0.3:
        return 1 - ease((T - T_AZUL1 + 0.3) / 0.6)
    return 0.0


def pal(T):
    x = luz(T)
    return {k: mix(WARM[k], NIGHT[k], x) for k in WARM}


def ink(ctx, w=4.5):
    stroke(ctx, INKC, w)


def fill_ink(ctx, rgb, w=4.5, a=1.0):
    fill_keep(ctx, rgb, a)
    ink(ctx, w)


def blur_layer(ctx, draw, k=5):
    """Desenfoque barato: dibuja a 1/k de resolución y lo amplía con filtro suave (profundidad de campo)."""
    sw, sh = int(W / k) + 1, int(H / k) + 1
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    c = cairo.Context(s)
    c.scale(1 / k, 1 / k)
    draw(c)
    s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw // 2 + 1, sh // 2 + 1)
    c2 = cairo.Context(s2)
    c2.scale(0.5, 0.5)
    p = cairo.SurfacePattern(s)
    p.set_filter(cairo.FILTER_GOOD)
    c2.set_source(p)
    c2.paint()
    ctx.save()
    ctx.scale(k * 2, k * 2)
    p2 = cairo.SurfacePattern(s2)
    p2.set_filter(cairo.FILTER_BILINEAR)
    ctx.set_source(p2)
    ctx.paint()
    ctx.restore()


# ---------------- mundo ----------------
def sky(ctx, T, P):
    ctx.set_source(vgrad(ctx, 0, -600, 0, H + 600, [(0, P["sky0"]), (0.62, P["sky1"]), (1, P["sky1"])]))
    ctx.paint()
    x = luz(T)
    sx, sy = 860, 360
    spotlight(ctx, sx, sy, 420, 0.35, P["sun"])
    circle(ctx, sx, sy, 80 - 25 * x)
    fill(ctx, P["sun"])
    if x > 0.05:  # estrellas en la noche
        rng = np.random.default_rng(4)
        for k in range(40):
            circle(ctx, rng.uniform(-200, 1300), rng.uniform(-300, 900), 3 + 2 * math.sin(T * 3 + k))
            fill(ctx, (1, 1, 1), 0.7 * x)


def cathedral(ctx, x, y, s, P):
    """Silueta de catedral románica al fondo (Piazza dei Miracoli)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    col = P["far"]
    ctx.rectangle(-420, -260, 840, 260); fill_ink(ctx, col, 3)
    ctx.move_to(-440, -260); ctx.line_to(0, -420); ctx.line_to(440, -260); ctx.close_path(); fill_ink(ctx, col, 3)
    ctx.move_to(-110, -420); ctx.arc(0, -420, 110, math.pi, 0); ctx.close_path(); fill_ink(ctx, mix(col, (1, 1, 1), 0.08), 3)
    for k in range(7):
        ctx.new_path(); ctx.arc(-300 + k * 100, -120, 28, math.pi, 0); ctx.line_to(-272 + k * 100, -40); ctx.line_to(-328 + k * 100, -40)
        ctx.close_path(); fill(ctx, mix(col, INKC, 0.45))
    ctx.restore()


def lawn(ctx, y, P):
    ctx.rectangle(-800, y, W + 1600, 2400)
    ctx.set_source(vgrad(ctx, 0, y, 0, y + 900, [(0, P["grass"]), (1, P["grass_d"])]))
    ctx.fill()
    ctx.move_to(-800, y); ctx.line_to(W + 800, y); ink(ctx, 4)
    for k in range(-6, 22):
        ctx.move_to(k * 90, y + 40 + (k % 3) * 30); ctx.line_to(k * 90 + 14, y + 22 + (k % 3) * 30)
        stroke(ctx, P["grass_d"], 4)


def world(ctx, T, P, ground_y=1240, far=True):
    sky(ctx, T, P)
    if far:
        for k, (hx, hs) in enumerate(((-200, 1.3), (500, 1.0), (1200, 1.4))):
            ctx.new_path(); ctx.arc(hx, ground_y + 60, 420 * hs, math.pi, 0); fill(ctx, mix(P["far"], P["grass_d"], 0.3))
        cathedral(ctx, 120, ground_y + 8, 0.75, P)
    lawn(ctx, ground_y, P)


def floor_block(ctx, w, h, P, top=False, hi=0.0):
    """Un piso de la torre (columnas y arcos), con contorno de tinta. Base en y=0, crece hacia arriba."""
    rrect(ctx, -w / 2, -h, w, h, 6)
    g = cairo.LinearGradient(-w / 2, 0, w / 2, 0)
    g.add_color_stop_rgb(0, *mix(P["marble"], P["marble_s"], 0.15))
    g.add_color_stop_rgb(0.45, *P["marble"])
    g.add_color_stop_rgb(1, *P["marble_s"])
    ctx.set_source(g); ctx.fill_preserve(); ink(ctx, 4)
    if hi > 0:
        rrect(ctx, -w / 2, -h, w, h, 6); fill(ctx, YELLOW, 0.55 * hi)
    n = 5
    for k in range(n):
        ax = -w / 2 + w * (k + 0.5) / n
        aw = w / n * 0.55
        ctx.new_path(); ctx.arc(ax, -h * 0.62, aw / 2, math.pi, 0); ctx.line_to(ax + aw / 2, -h * 0.12); ctx.line_to(ax - aw / 2, -h * 0.12); ctx.close_path()
        fill(ctx, mix(P["marble_s"], INKC, 0.35))
    ctx.rectangle(-w / 2 - 8, -h - 6, w + 16, 12); fill_ink(ctx, P["marble"], 3)


def tower(ctx, x, y, T, P, floors=8.0, tilt=0.0, curve=0.0, s=1.0, wobble=0.0, hi_top=0.0, bell=True):
    """Torre de Pisa: 'floors' pisos (admite fracción = el piso que se está construyendo), inclinación 'tilt' (grados)
    y 'curve' (grados que corrige cada piso nuevo -> forma de plátano)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    soft_shadow(ctx, 40 * math.sin(math.radians(tilt)) * 3, 8, 210, 26, 0.45)
    ctx.rotate(math.radians(tilt + wobble * math.sin(T * 9)))
    w, h = 230, 92
    # base más alta
    full = int(floors)
    for i in range(full + 1):
        frac = 1.0 if i < full else floors - full
        if frac <= 0.01:
            break
        hh = (h * 1.35 if i == 0 else h) * frac
        floor_block(ctx, w if i else w + 16, hh, P, hi=(hi_top if i >= 4 else 0.0))
        ctx.translate(0, -hh)
        if i >= 3:
            ctx.rotate(-math.radians(curve))
    if bell and floors >= 7.99:
        floor_block(ctx, w * 0.72, h * 0.9, P)
        ctx.translate(0, -h * 0.9)
        ctx.new_path(); ctx.arc(0, 0, w * 0.36, math.pi, 0); ctx.close_path(); fill_ink(ctx, P["marble_s"], 3)
    ctx.restore()


def builder(ctx, x, y, s, T, col=(0.85, 0.35, 0.30), mood="normal", look=0.0, k=0, helmet=False):
    """Personaje plano propio (sin rasgos de nadie): cabeza ovalada, extremidades finas, parpadeo y balanceo."""
    bob = 6 * math.sin(T * 5 + k)
    ctx.save(); ctx.translate(x, y + bob); ctx.scale(s, s)
    soft_shadow(ctx, 0, 300 - bob / s, 80, 16, 0.35)
    for sx in (-1, 1):  # piernas
        ctx.move_to(sx * 22, 170); ctx.line_to(sx * 30, 300); stroke(ctx, INKC, 12)
    rrect(ctx, -60, 40, 120, 140, 40); fill_ink(ctx, col, 4)
    for sx in (-1, 1):  # brazos
        ctx.move_to(sx * 55, 70); ctx.line_to(sx * 95, 150 + 10 * math.sin(T * 4 + k + sx)); stroke(ctx, INKC, 10)
    ctx.save(); ctx.scale(1, 1.1); circle(ctx, 0, -10, 62); ctx.restore()
    fill_ink(ctx, (0.98, 0.84, 0.70), 4)
    if helmet:
        ctx.new_path(); ctx.arc(0, -30, 66, math.pi, 0); ctx.close_path(); fill_ink(ctx, (0.72, 0.74, 0.80), 4)
    else:
        ctx.new_path(); ctx.arc(0, -40, 60, math.pi * 1.05, -0.05); ctx.close_path(); fill_ink(ctx, (0.55, 0.38, 0.22), 4)
    ph = (T * 0.7 + k * 0.37) % 1.0
    blink = 0.12 if ph < 0.05 else 1.0
    for sx in (-1, 1):
        ellipse(ctx, sx * 22 + look * 10, -2, 7, 9 * blink); fill(ctx, INKC)
    if mood == "triste":
        ctx.new_path(); ctx.arc(0, 40, 18, math.pi * 1.15, math.pi * 1.85); ink(ctx, 4)
    elif mood == "feliz":
        ctx.new_path(); ctx.arc(0, 18, 18, 0.15 * math.pi, 0.85 * math.pi); ink(ctx, 4)
    else:
        ctx.move_to(-12, 28); ctx.line_to(12, 28); ink(ctx, 4)
    ctx.restore()


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
    rrect(ctx, -200, -170, 400, 340, 26); fill_ink(ctx, PAPER, 5)
    rrect(ctx, -200, -170, 400, 90, 26); fill(ctx, col)
    ctx.rectangle(-200, -110, 400, 30); fill(ctx, col)
    text(ctx, top, 0, -125, 46, WHITE, shadow=False)
    text(ctx, big, 0, 55, 130, INKC, shadow=False)
    ctx.restore()


def label(ctx, s, x, y, a, rgb=YELLOW, size=50):
    pill(ctx, s, x, y, a, size=size, rgb=rgb)


def soil(ctx, T, P, firm=0.0, y0=1000, water=1.0):
    """Corte del suelo: arcilla y arena con gotas de agua (menos agua = más firme)."""
    clay = mix((0.62, 0.46, 0.34), (0.48, 0.34, 0.26), firm)
    sand = mix((0.86, 0.74, 0.50), (0.74, 0.62, 0.42), firm)
    ctx.rectangle(-800, y0, W + 1600, 300); fill_ink(ctx, clay, 4)
    ctx.rectangle(-800, y0 + 300, W + 1600, 1600); fill_ink(ctx, sand, 4)
    rng = np.random.default_rng(8)
    for k in range(70):
        px, py = rng.uniform(-100, W + 100), rng.uniform(y0 + 20, y0 + 900)
        circle(ctx, px, py, 5); fill(ctx, mix(clay, INKC, 0.3), 0.5)
    for k in range(int(36 * water)):
        px, py = rng.uniform(0, W), rng.uniform(y0 + 30, y0 + 850)
        circle(ctx, px, py + 6 * math.sin(T * 3 + k), 13); fill_ink(ctx, (0.45, 0.72, 1.0), 2.5)


def sponge(ctx, x, y, w, h, T, P):
    ctx.save(); ctx.translate(x, y)
    rrect(ctx, -w / 2, -h, w, h, 30); fill_ink(ctx, (1.0, 0.84, 0.30), 5)
    rng = np.random.default_rng(6)
    for k in range(22):
        hx, hy = rng.uniform(-w / 2 + 30, w / 2 - 30), rng.uniform(-h + 25, -20)
        ellipse(ctx, hx, hy, 16, 12 * h / 300); fill(ctx, (0.80, 0.58, 0.16))
    ctx.restore()


def weight(ctx, x, y, s, P, lbl="TOWER"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-150, 0); ctx.line_to(150, 0); ctx.line_to(110, -200); ctx.line_to(-110, -200); ctx.close_path()
    fill_ink(ctx, mix((0.55, 0.56, 0.68), P["marble_s"], 0.3), 5)
    rrect(ctx, -40, -250, 80, 60, 20); ink(ctx, 10)
    text(ctx, lbl, 0, -90, 54, WHITE, shadow=False)
    ctx.restore()


def ship(ctx, x, y, s, T, col):
    ctx.save(); ctx.translate(x, y + 8 * math.sin(T * 3)); ctx.scale(s, s); ctx.rotate(0.04 * math.sin(T * 2))
    ctx.move_to(-160, 0); ctx.line_to(160, 0); ctx.line_to(110, 70); ctx.line_to(-110, 70); ctx.close_path(); fill_ink(ctx, WOOD, 5)
    ctx.move_to(0, 0); ctx.line_to(0, -230); ink(ctx, 8)
    ctx.move_to(6, -220); ctx.line_to(130, -120); ctx.line_to(6, -30); ctx.close_path(); fill_ink(ctx, col, 4)
    ctx.restore()


def hero_frame(ctx, lt, T, z0, z1, dur):
    """Plano del gancho (y del final del bucle): torre en la plaza, luz cálida, ficha."""
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2, 850)
    world(ctx, T, P)
    tower(ctx, W / 2 + 10, 1250, T, P, floors=8, tilt=4.0, curve=0.35, s=0.95)
    ctx.restore()
    ficha(ctx, "LEANING TOWER OF PISA", "ITALY · BUILT 1173–1372", W / 2, 1500, 1.0, "🔔", GOLD)


# ---------------- escenas ----------------
# 0.00 "The Leaning Tower of Pisa was saved by a war. And it's real."
def e1(ctx, lt, dur, T):
    hero_frame(ctx, lt, T, 1.0, 1.10, dur)
    badge(ctx, "100% REAL", 860, 760, pop(lt, 2.75), size=54, bg=(0.20, 0.62, 0.32))


# 3.60 "1173. Pisa starts building a bell tower. Floor one. Perfect. Floor two. Still perfect."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.7), (1.6, 1.45), (dur, 1.52)]), W / 2, keyframes(lt, [(0, 1250), (dur, 1225)]))
    world(ctx, T, P)
    tt = T
    fl = 0.0
    if tt > 5.98: fl = 0.6 * ease(clamp((tt - 5.98) / 0.3))      # "tower": arranca la base
    if tt > 6.22: fl = 0.6 + 0.4 * ease(clamp((tt - 6.22) / 0.35))  # floor one
    if tt > 7.32: fl = 1.0 + ease(clamp((tt - 7.32) / 0.35))        # floor two
    tower(ctx, W / 2, 1250, T, P, floors=fl, tilt=0.0, s=1.0, bell=False)
    builder(ctx, 230, 960, 0.75, T, col=(0.85, 0.35, 0.30), k=1, mood="feliz")
    builder(ctx, 860, 970, 0.7, T, col=(0.25, 0.50, 0.85), k=2, mood="feliz")
    ctx.restore()
    cal(ctx, W / 2, 1400, 0.8 * pop(lt, 0.0), "YEAR", "1173")
    check(ctx, 330, 1360, 1.1, pop(lt, 7.00 - 3.60), ok=True)
    check(ctx, 750, 1360, 1.1, pop(lt, 8.33 - 3.60), ok=True)
    label(ctx, "BUILDERS", 230, 840, pop(lt, 2.4), rgb=GOLD, size=36)


# 8.82 "By floor three, the tower starts sinking on one side."
def e3(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.45), (dur, 1.6)]), W / 2 + 40, 1200)
    world(ctx, T, P)
    fl = 2.0 + ease(clamp((T - 9.24) / 0.35))
    sink = ease(clamp((T - 10.2) / 1.2))
    # hundimiento: el suelo cede a la derecha
    ellipse(ctx, W / 2 + 90, 1256, 150 * sink + 1, 26 * sink + 1); fill(ctx, mix(P["grass_d"], INKC, 0.4))
    tower(ctx, W / 2, 1250 + 14 * sink, T, P, floors=fl, tilt=3.2 * sink, s=1.0, bell=False, wobble=0.25 * sink)
    builder(ctx, 200, 980, 0.72, T, col=(0.85, 0.35, 0.30), k=1, mood="triste" if sink > 0.5 else "normal", look=1)
    ctx.restore()
    arrow(ctx, 660, 1000, 660, 1300, clamp((T - 10.4) / 0.4), rgb=RED, w=16)
    label(ctx, "SINKING!", 660, 1390, pop(lt, 10.56 - 8.82), rgb=RED, size=52)
    label(ctx, "FLOOR 3", 260, 1390, pop(lt, 0.3), rgb=GOLD, size=50)


# 11.64 "Then Pisa goes to war. Construction stops. For almost a hundred years."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (1.3, 1.08), (dur, 1.16)]), W / 2, 820)
    sky(ctx, T, P)
    # mar con barcos (guerra) -> la torre a medias con un cartel STOP
    ctx.rectangle(-800, 1060, W + 1600, 1600); fill_ink(ctx, mix((0.25, 0.50, 0.78), P["grass_d"], 0.15), 4)
    for k in range(6):
        ctx.move_to(-200 + k * 260 + (T * 40) % 260, 1100 + k % 2 * 40); ctx.rel_line_to(70, 0); stroke(ctx, WHITE, 5, 0.6)
    ship(ctx, 230, 1060, 0.9, T, (0.85, 0.20, 0.22))
    ship(ctx, 850, 1070, 0.9, T + 1, (0.95, 0.95, 0.95))
    ctx.restore()
    # cartel STOP sobre la obra
    a = pop(lt, 13.54 - 11.64)
    if a > 0.01:
        ctx.save(); ctx.translate(W / 2, 650); ctx.scale(a, a)
        n = 8
        ctx.new_path()
        for k in range(n):
            ang = math.pi / n + k * math.tau / n
            ctx.line_to(150 * math.cos(ang), 150 * math.sin(ang))
        ctx.close_path(); fill_ink(ctx, RED, 6)
        text(ctx, "STOP", 0, 0, 84, WHITE, shadow=False)
        ctx.restore()
    if T > 14.05:
        yrs = int(counter(T - 14.05, 0, 94, 1.1))
        label(ctx, f"{yrs} YEARS", W / 2, 1380, 1.0, rgb=GOLD, size=62)


# 15.71 "You see, the ground under Pisa is soft clay and sand. Like a wet sponge."  (luz azul)
def e5(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, keyframes(lt, [(0, 760), (dur, 980)]))
    sky(ctx, T, P)
    lawn(ctx, 760, P)
    soil(ctx, T, P, firm=0.0, y0=800)
    tower(ctx, W / 2, 800, T, P, floors=3.0, tilt=3.2, s=0.8, bell=False)
    ctx.restore()
    label(ctx, "CLAY", 230, 1030, pop(lt, 17.69 - 15.71), rgb=(0.85, 0.55, 0.40), size=50)
    label(ctx, "SAND", 880, 1225, pop(lt, 18.24 - 15.71), rgb=(0.95, 0.82, 0.55), size=50)
    # "Like a wet sponge": la tierra se convierte en esponja
    a = ease(clamp((T - 18.80) / 0.45))
    if a > 0:
        ctx.save(); ctx.translate(W / 2, 1450); ctx.scale(a, a); ctx.translate(-W / 2, -1450)
        sponge(ctx, W / 2, 1550, 520, 260, T, P)
        ctx.restore()
        label(ctx, "= WET SPONGE", W / 2, 1180, a, rgb=(1.0, 0.84, 0.30), size=52)


# 19.64 "Put something heavy on a sponge, and it slowly squeezes out the water and gets firmer."
def e6(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.1), (dur, 1.22)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 800), sky(c, T, P), lawn(c, 1180, P)))
    ctx.save()
    camera(ctx, z, W / 2, 800)
    sq = ease(clamp((T - 21.0) / 2.0))
    h = 300 - 120 * sq
    sponge(ctx, W / 2, 1180, 600, h, T, P)
    drop_in = ease_back(clamp((T - 19.8) / 0.5))
    weight(ctx, W / 2, 1180 - h - 300 * (1 - drop_in), 1.0, P)
    # agua que sale por los lados
    if T > 21.3:
        for k in range(10):
            ph = ((T - 21.3) * 1.6 + k * 0.1) % 1.0
            for sx in (-1, 1):
                dx = W / 2 + sx * (300 + 120 * ph)
                dy = 1180 - h * 0.4 + 260 * ph * ph
                circle(ctx, dx, dy, 14 * (1 - ph * 0.4)); fill_ink(ctx, (0.45, 0.72, 1.0), 2.5)
    ctx.restore()
    label(ctx, "HEAVY", 230, 540, pop(lt, 20.05 - 19.64), rgb=RED, size=52)
    label(ctx, "WATER OUT", W / 2, 1420, pop(lt, 22.49 - 19.64), rgb=(0.45, 0.72, 1.0), size=56)
    label(ctx, "FIRMER", 850, 540, pop(lt, 23.18 - 19.64), rgb=(0.30, 0.78, 0.40), size=52)


# 23.63 "That long pause gave the ground time to get firm."
def e7(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.15)]), W / 2, 900)
    sky(ctx, T, P)
    lawn(ctx, 760, P)
    f = ease(clamp(lt / 1.8))
    soil(ctx, T, P, firm=f, y0=800, water=1 - f)
    tower(ctx, W / 2, 800, T, P, floors=3.0, tilt=3.2, s=0.8, bell=False)
    ctx.restore()
    yr = int(counter(lt, 1178, 1272, 1.8))
    cal(ctx, 210, 560, 0.6, "YEAR", str(yr), col=(0.30, 0.45, 0.85))
    label(ctx, "FIRM", W / 2, 1400, pop(lt, 25.75 - 23.63), rgb=(0.30, 0.78, 0.40), size=66)


# 26.07 "In other words, if Pisa had kept building, the tower would have fallen."
def e8(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.06, dur=dur), W / 2, 820)
    world(ctx, T, P, far=False)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.30); ctx.paint()
    fall = ease(clamp((T - 28.1) / 0.85)) ** 2
    tower(ctx, W / 2 - 30, 1250, T, P, floors=8, tilt=4 + 80 * fall, s=0.9, bell=True)
    ctx.restore()
    label(ctx, "NO WAR?", 230, 700, pop(lt, 0.6), rgb=RED, size=56)
    if T > 29.0:
        stamp(ctx, "FALLEN", W / 2, 640, (T - 29.0) / 0.25, size=120)


# 29.45 "Luckily for the tower, Pisa was at war. Unluckily for Pisa, Pisa was at war."  (vuelve la luz cálida)
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 0.98), (dur, 1.05)]), W / 2, 900)
    world(ctx, T, P)
    tower(ctx, 280, 1250, T, P, floors=3, tilt=3.2, s=0.8, bell=False)
    builder(ctx, 720, 980, 0.8, T, col=(0.85, 0.20, 0.22), mood="triste" if T > 31.4 else "normal", k=3, helmet=True)
    builder(ctx, 900, 990, 0.75, T, col=(0.85, 0.20, 0.22), mood="triste" if T > 31.4 else "normal", k=4, helmet=True)
    ctx.restore()
    check(ctx, 290, 470, 1.2, pop(lt, 30.04 - 29.45), ok=True)
    label(ctx, "LUCKY TOWER", 290, 300, pop(lt, 0.2), rgb=(0.30, 0.78, 0.40), size=46)
    check(ctx, 790, 470, 1.2, pop(lt, 31.98 - 29.45), ok=False)
    label(ctx, "UNLUCKY PISA", 790, 300, pop(lt, 31.84 - 29.45), rgb=RED, size=46)


# 33.35 "When they came back, they built the new floors taller on the short side."
def e10(ctx, lt, dur, T):
    P = pal(T)
    z, cy = keyframes(lt, [(0, 1.0), (dur, 1.08)]), 760
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, cy), world(c, T, P)))
    ctx.save()
    camera(ctx, z, W / 2, cy)
    fl = 3 + 2 * ease(clamp((T - 34.4) / 1.3))
    tower(ctx, W / 2, 1250, T, P, floors=fl, tilt=3.2, curve=1.2, s=0.95, bell=False, hi_top=pop(lt, 35.08 - 33.35))
    builder(ctx, 190, 980, 0.7, T, col=(0.25, 0.50, 0.85), k=5, mood="feliz")
    ctx.restore()
    label(ctx, "TALLER HERE", 260, 780, pop(lt, 35.08 - 33.35), rgb=YELLOW, size=48)
    arrow(ctx, 300, 830, 470, 1000, clamp((T - 35.2) / 0.4), rgb=YELLOW, w=12)


# 36.30 "So the tower isn't just leaning. It's curved, like a banana."
def e11(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.15), (dur, 1.0)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 780), world(c, T, P)))
    ctx.save()
    camera(ctx, z, W / 2, 780)
    tower(ctx, W / 2 - 60, 1250, T, P, floors=8, tilt=5.5, curve=1.6, s=1.0)
    ctx.restore()
    label(ctx, "CURVED", 230, 700, pop(lt, 37.85 - 36.30), rgb=YELLOW, size=60)
    icon(ctx, "🍌", 820, 560, 420, pop(lt, 38.52 - 36.30), rot=-0.5)


# 38.98 "It took 199 years to finish."
def e12(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 800)
    world(ctx, T, P)
    fl = 5 + 3.0 * ease(clamp(lt / 1.7))
    tower(ctx, W / 2, 1250, T, P, floors=fl, tilt=4.0, curve=0.35, s=1.0)
    ctx.restore()
    yr = int(counter(lt, 1173, 1372, 1.7))
    cal(ctx, 190, 620, 0.55, "YEAR", str(yr))
    label(ctx, "199 YEARS", 860, 620, pop(lt, 40.51 - 38.98), rgb=GOLD, size=56)


# 41.58 "So why is it still standing? Because"  -> bucle: "The Leaning Tower of Pisa was saved by a war."
def e13(ctx, lt, dur, T):
    hero_frame(ctx, lt, T, 0.92, 1.0, dur)


e9.cap_y = 1430  # aquí el cielo lleva las etiquetas: subtítulo sobre el césped

ESCENAS = [(0.0, e1), (3.60, e2), (8.82, e3), (11.64, e4), (15.71, e5), (19.64, e6), (23.63, e7), (26.07, e8),
           (29.45, e9), (33.35, e10), (36.30, e11), (38.98, e12), (41.58, e13)]

SFX = [(0.05, "bell"), (2.72, "pop"), (5.60, "bell"), (6.22, "thud"), (7.00, "ding"), (7.32, "thud"), (8.33, "ding"),
       (9.24, "thud"), (10.5, "crack"), (11.6, "whoosh"), (12.55, "drum"), (12.95, "drum"), (13.50, "thud"),
       (15.62, "whoosh"), (18.9, "pop"), (19.9, "thud"), (21.3, "squish"), (22.3, "squish"), (25.7, "ding"),
       (26.02, "whoosh"), (28.9, "thud"), (29.0, "crack"), (30.0, "ding"), (31.9, "drum"), (34.5, "thud"),
       (35.1, "pop"), (38.5, "pop"), (40.5, "bell"), (41.5, "whoosh")]


def MINIATURA(ctx):
    T = 1.0
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    world(ctx, T, P, ground_y=1450)
    tower(ctx, W / 2 + 20, 1460, T, P, floors=8, tilt=4.0, curve=0.35, s=0.95)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["SAVED BY", ("A WAR?!", WHITE)], y=260, size=180)
    thumb_circle(ctx, W / 2 + 120, 1350, 260, 120)
    ficha(ctx, "LEANING TOWER OF PISA", "ITALY · BUILT 1173–1372", W / 2, 1660, 1.0, "🔔", GOLD)
