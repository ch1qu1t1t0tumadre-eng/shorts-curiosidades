"""v29 (EN) formato «historia» (inventada, física real): por qué los neumáticos tienen surcos (aquaplaning)."""
from kit import *  # noqa
from estilo_v3 import *  # noqa

FLASH = False
WHOOSH = False
MUSICA_GAIN = 0.42
FX_GAIN = 0.30
Y_SUBTITULO = 1430     # subtítulos ABAJO
TAM_SUBTITULO = 135
set_azul(33.80, 44.48)  # "You see" -> "They lost the road."
CORTES = [(6.52, 9.07)]  # quitado "and the winner gets every car company in the country." (relleno 4-9 s)

KID = (0.25, 0.50, 0.85)
RIV = (0.88, 0.25, 0.25)
RUB = (0.16, 0.16, 0.20)
WAT = (0.35, 0.65, 1.0)


def tire(ctx, x, y, r, T, grooves=True, spin=0.0, a=1.0):
    """Neumático visto de lado: dibujo de surcos en la banda si grooves."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(spin)
    circle(ctx, 0, 0, r); fill_ink(ctx, RUB, 5)
    if grooves:
        for k in range(24):
            ang = k * math.tau / 24
            ctx.save(); ctx.rotate(ang)
            ctx.rectangle(r - 0.16 * r, -0.035 * r, 0.16 * r, 0.07 * r); fill(ctx, (0.45, 0.45, 0.52))
            ctx.restore()
    circle(ctx, 0, 0, r * 0.62); fill_ink(ctx, (0.28, 0.28, 0.33), 4)
    circle(ctx, 0, 0, r * 0.45); fill_ink(ctx, (0.78, 0.80, 0.85), 4)
    for k in range(5):
        ctx.save(); ctx.rotate(k * math.tau / 5)
        ctx.rectangle(-0.05 * r, -0.42 * r, 0.1 * r, 0.3 * r); fill(ctx, (0.55, 0.57, 0.62))
        ctx.restore()
    circle(ctx, 0, 0, r * 0.1); fill_ink(ctx, (0.4, 0.4, 0.45), 3)
    ctx.restore()


def tread(ctx, x, y, w, h, grooves=True, col=RUB):
    """Neumático visto de frente/desde abajo: rectángulo de goma con surcos verticales."""
    rrect(ctx, x - w / 2, y - h / 2, w, h, 26); fill_ink(ctx, col, 5)
    if grooves:
        for k in range(1, 4):
            gx = x - w / 2 + k * w / 4
            ctx.rectangle(gx - 14, y - h / 2 + 8, 28, h - 16); fill(ctx, (0.50, 0.52, 0.60))
            for j in range(6):
                yy = y - h / 2 + 30 + j * (h - 60) / 5
                ctx.move_to(gx - w / 8 + 10, yy); ctx.line_to(gx - 14, yy + 18); stroke(ctx, (0.50, 0.52, 0.60), 7)


def car(ctx, x, y, s, T, col=KID, num="7", grooves=True, rot=0.0, wheel_spin=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(-300, -40); ctx.line_to(-280, -110); ctx.line_to(-120, -120); ctx.line_to(-60, -190)
    ctx.line_to(80, -190); ctx.line_to(150, -110); ctx.line_to(300, -90); ctx.line_to(320, -30); ctx.line_to(300, 0)
    ctx.line_to(-300, 0); ctx.close_path(); fill_ink(ctx, col, 5)
    ctx.rectangle(-320, -170, 60, 20); fill_ink(ctx, mix(col, (0, 0, 0), 0.3), 3)  # alerón
    ctx.move_to(-40, -180); ctx.line_to(70, -180); ctx.line_to(120, -120); ctx.line_to(-40, -120); ctx.close_path()
    fill_ink(ctx, GLASS, 3)
    circle(ctx, -150, -60, 42); fill_ink(ctx, WHITE, 3)
    text(ctx, num, -150, -60, 52, col, shadow=False)
    sp = -T * 14 if wheel_spin else 0.0
    tire(ctx, -190, 0, 72, T, grooves, sp)
    tire(ctx, 200, 0, 72, T, grooves, sp)
    ctx.restore()


def trophy(ctx, x, y, s, a=1.0):
    if a <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * a, s * a)
    rrect(ctx, -90, 120, 180, 50, 8); fill_ink(ctx, WOOD, 4)
    ctx.rectangle(-25, 40, 50, 80); fill_ink(ctx, GOLD, 4)
    ctx.move_to(-110, -140); ctx.line_to(110, -140); ctx.curve_to(110, 0, 50, 50, 0, 50)
    ctx.curve_to(-50, 50, -110, 0, -110, -140); ctx.close_path(); fill_ink(ctx, GOLD, 5)
    for sx in (-1, 1):
        ctx.arc(sx * 120, -80, 40, 0, math.tau); stroke(ctx, INKC, 14); ctx.arc(sx * 120, -80, 40, 0, math.tau); stroke(ctx, GOLD, 8)
    text(ctx, "1", 0, -60, 90, WHITE)
    ctx.restore()


def track(ctx, T, P, y=1150, speed=900, wet=0.0):
    ground(ctx, y, P, col=P["road"])
    for k in range(-2, 12):
        ctx.rectangle(k * 220 - (T * speed) % 220, y + 70, 110, 14); fill(ctx, WHITE, 0.8)
    if wet > 0.01:
        ctx.rectangle(0, y, W, 50); fill(ctx, WAT, 0.45 * wet)


def speedo(ctx, x, y, s, v, a=1.0):
    if a <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * a, s * a)
    circle(ctx, 0, 0, 150); fill_ink(ctx, (0.12, 0.12, 0.18), 5)
    ctx.arc(0, 0, 120, math.pi * 0.75, math.pi * 2.25); stroke(ctx, (0.45, 0.45, 0.55), 12)
    f = clamp(v / 100)
    ctx.arc(0, 0, 120, math.pi * 0.75, math.pi * (0.75 + 1.5 * f)); stroke(ctx, RED if v >= 50 else YELLOW, 14)
    ang = math.pi * (0.75 + 1.5 * f)
    ctx.move_to(0, 0); ctx.line_to(95 * math.cos(ang), 95 * math.sin(ang)); stroke(ctx, WHITE, 8)
    text(ctx, f"{int(v)}", 0, 55, 64, WHITE)
    text(ctx, "MPH", 0, 105, 30, (0.75, 0.75, 0.8), shadow=False)
    ctx.restore()


def hero(ctx, lt, T, dur, z0, z1, labels=True):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, z0), (dur, z1)]), W / 2 - 60, 780)
    sky(ctx, T, P)
    ground(ctx, 1150, P, col=P["conc"])
    # neumático gigante a medio tallar
    ctx.save(); ctx.translate(W / 2 - 80, 760)
    circle(ctx, 0, 0, 330); fill_ink(ctx, RUB, 6)
    for k in range(24):
        ang = -math.pi / 2 + k * math.tau / 24
        if ang > -math.pi / 2 + math.pi * 1.1:
            continue
        ctx.save(); ctx.rotate(ang)
        ctx.rectangle(330 - 60, -12, 60, 24); fill(ctx, (0.50, 0.50, 0.58))
        ctx.restore()
    circle(ctx, 0, 0, 200); fill_ink(ctx, (0.28, 0.28, 0.33), 5)
    circle(ctx, 0, 0, 140); fill_ink(ctx, (0.78, 0.80, 0.85), 5)
    ctx.restore()
    worker(ctx, 960, 860, 0.75, T, col=KID, k=1, mood="feliz", hat_kind="cap", hat=KID, arm=0.6 + 0.3 * math.sin(T * 8))
    ctx.restore()
    if labels:
        label(ctx, "SMOOTH", 260, 330, 1.0, rgb=(0.75, 0.75, 0.8), size=46)
        label(ctx, "GROOVES", 700, 330, 1.0, rgb=YELLOW, size=46)


# 0.03 "This guy cut grooves into a perfectly smooth tire on purpose."
def e1(ctx, lt, dur, T):
    if T < 2.13:   # primer plano del neumático a medio tallar, con la cámara entrando
        hero(ctx, lt, T, dur, 1.35, 1.12, labels=False)
    else:          # "smooth tire" -> corte seco: lisa ✗ en lluvia contra surcos ✓
        P = pal(T)
        ctx.save()
        camera(ctx, keyframes(lt - 2.13, [(0, 1.08), (dur - 2.13, 1.0)]), W / 2, 800)
        sky(ctx, T, P, sun=False)
        ctx.set_source_rgba(0.15, 0.18, 0.28, 0.35); ctx.paint()
        tread(ctx, 300, 800, 300, 560, grooves=False)
        tread(ctx, 780, 800, 300, 560, grooves=True)
        ctx.restore()
        rain(ctx, T, 1.0, 50, 4)
        check(ctx, 300, 1200, 0.9, pop(lt, 2.13 + 0.25), ok=False)
        check(ctx, 780, 1200, 0.9, pop(lt, 2.13 + 0.05), ok=True)
    gancho(ctx, ["WHY DO TIRES", ("HAVE GROOVES?", WHITE)], T, t_fin=3.0, size=100)


# 3.79 "See, two teams are racing for one giant trophy, and the winner gets every car company in the country."
def e2(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 0.98)]), W / 2, 820)
    sky(ctx, T, P)
    track(ctx, T, P, 1150)
    car(ctx, 330, 1080, 0.75, T, col=KID, num="7")
    car(ctx, 830, 1080, 0.75, T, col=RIV, num="1", grooves=False)
    trophy(ctx, W / 2, 560, 1.3, pop(lt, 5.69 - 3.79))
    ctx.restore()
    label(ctx, "THE KID", 330, 900, pop(lt, 0.2), rgb=KID, size=40)
    label(ctx, "RIVAL", 830, 900, pop(lt, 0.4), rgb=RIV, size=40)
    a = pop(lt, 7.39 - 3.79)
    if a > 0.01:
        label(ctx, "EVERY CAR COMPANY", W / 2, 260, a, rgb=YELLOW, size=46)


# 9.10 "His boss sees him carving lines into the rubber. Kid, you're throwing away grip."
def e3(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 900), sky(c, T, P), ground(c, 1150, P, col=P["conc"])))
    ctx.save()
    camera(ctx, z, W / 2, 900)
    tire(ctx, 720, 800, 260, T, grooves=lt > 0.6, spin=0.0)
    worker(ctx, 230, 760, 1.0, T, col=(0.55, 0.42, 0.30), boss=True, k=3, mood="shock" if T > 11.4 else "normal",
           tie=RED, hat_kind="none")
    ctx.restore()
    label(ctx, "BOSS", 230, 470, pop(lt, 0.2), rgb=GOLD, size=42)
    if T > 10.43:
        label(ctx, "LINES?!", 720, 420, pop(lt, 10.43 - 9.10), rgb=YELLOW, size=50)
    bubble(ctx, "KID, YOU'RE THROWING AWAY GRIP!", W / 2, 1230, pop(lt, 11.44 - 9.10), size=40)


# 12.87 "And he's right. On a dry road, smooth tires grip better. More rubber touches the road."
def e4(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.08)]), W / 2, 800)
    sky(ctx, T, P, sun=True)
    ctx.restore()
    # huellas sobre el asfalto (vista desde abajo)
    rrect(ctx, 60, 450, W - 120, 760, 40); fill_ink(ctx, (0.42, 0.42, 0.46), 5)
    a1 = pop(lt, 14.69 - 12.87)
    if a1 > 0.01:
        ctx.save(); ctx.translate(330, 830); ctx.scale(a1, a1); tread(ctx, 0, 0, 300, 520, grooves=False); ctx.restore()
        ctx.save(); ctx.translate(790, 830); ctx.scale(a1, a1); tread(ctx, 0, 0, 300, 520, grooves=True); ctx.restore()
    label(ctx, "DRY ROAD", W / 2, 300, pop(lt, 13.76 - 12.87), rgb=YELLOW, size=54)
    label(ctx, "SMOOTH", 330, 520, a1, rgb=WHITE, size=40)
    label(ctx, "GROOVED", 790, 520, a1, rgb=WHITE, size=40)
    if T > 15.90:
        a = pop(lt, 15.90 - 12.87)
        label(ctx, "MORE RUBBER", 330, 1150, a, rgb=(0.30, 0.78, 0.40), size=40)
        check(ctx, 330, 1290, 0.8, a, ok=True)


# 17.24 "The other team runs perfectly smooth tires. They win lap after lap. Everybody laughs at the kid."
def e5(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 860)
    sky(ctx, T, P)
    track(ctx, T, P, 1150, speed=1400)
    car(ctx, 760, 1080, 0.85, T, col=RIV, num="1", grooves=False)
    car(ctx, 220, 1080, 0.7, T, col=KID, num="7")
    ctx.restore()
    label(ctx, "SMOOTH TIRES", 760, 880, pop(lt, 18.72 - 17.24), rgb=RIV, size=40)
    if T > 19.67:
        n = 1 + int(clamp((T - 19.89) / 1.0) * 4)
        trophy(ctx, 900, 520, 0.8, pop(lt, 19.89 - 17.24))
        label(ctx, f"WIN x{n}", 900, 300, 1.0, rgb=YELLOW, size=54)
    if T > 21.17:
        for k in range(3):
            icon(ctx, "😂", 140 + k * 140, 560 - 20 * math.sin(T * 5 + k), 110, pop(lt, 21.4 - 17.24 + 0.12 * k))


# 22.74 "Then, on race day, it rains. Past fifty miles an hour, the smooth tires start floating."
def e6(ctx, lt, dur, T):
    P = pal(T)
    dark = ease(clamp((T - 23.6) / 0.6))
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 900)
    sky(ctx, T, P, sun=dark < 0.5)
    ctx.set_source_rgba(0.15, 0.18, 0.28, 0.45 * dark); ctx.paint()
    track(ctx, T, P, 1150, speed=1500, wet=dark)
    lift = 30 * ease(clamp((T - 26.6) / 0.6))
    car(ctx, W / 2 + 60, 1080 - lift, 0.95, T, col=RIV, num="1", grooves=False)
    ctx.restore()
    if dark > 0.01:
        rain(ctx, T, dark, 80, 5)
    label(ctx, "RACE DAY", W / 2, 260, pop(lt, 0.25), rgb=YELLOW, size=50)
    v = 10 + 55 * ease(clamp((T - 24.63) / 1.2))
    speedo(ctx, 270, 600, 0.95, v, pop(lt, 24.63 - 22.74))
    if T > 26.6:
        label(ctx, "FLOATING!", 820, 620, pop(lt, 27.0 - 22.74), rgb=RED, size=56)


# 27.49 "A thin sheet of water lifts them off the road. The cars spin like hockey pucks."
def e7(ctx, lt, dur, T):
    P = pal(T)
    if T < 29.68:
        # corte: rueda lisa sobre lámina de agua
        ctx.save()
        camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.06)]), W / 2, 800)
        sky(ctx, T, P, sun=False)
        ctx.set_source_rgba(0.15, 0.18, 0.28, 0.45); ctx.paint()
        ctx.rectangle(0, 1000, W, 400); fill(ctx, (0.30, 0.30, 0.34))
        sh = 60 * ease(clamp((T - 27.9) / 0.6))
        ctx.rectangle(0, 1000 - sh, W, sh); fill_ink(ctx, WAT, 3, a=0.85)
        lift = sh + 10 * math.sin(T * 9)
        tire(ctx, W / 2, 1000 - 260 - lift, 260, T, grooves=False, spin=-T * 10)
        ctx.restore()
        rain(ctx, T, 1.0, 70, 6)
        label(ctx, "WATER", 200, 1260, pop(lt, 28.38 - 27.49), rgb=WAT, size=44)
        if T > 28.64:
            a = pop(lt, 28.64 - 27.49)
            arrow(ctx, 1000, 1050, 1000, 830, a, rgb=WAT, w=12)
            arrow(ctx, 80, 1050, 80, 830, a, rgb=WAT, w=12)
            label(ctx, "LIFTED OFF THE ROAD", W / 2, 300, a, rgb=YELLOW, size=46)
    else:
        ctx.save()
        camera(ctx, 1.0, W / 2, 900)
        sky(ctx, T, P, sun=False)
        ctx.set_source_rgba(0.15, 0.18, 0.28, 0.45); ctx.paint()
        track(ctx, T, P, 1150, speed=600, wet=1.0)
        # vista cenital simulada: coche girando sobre sí mismo
        ctx.restore()
        rot = (T - 29.68) * 7
        car(ctx, W / 2, 820, 0.95, T, col=RIV, num="1", grooves=False, rot=rot)
        rain(ctx, T, 1.0, 70, 7)
        a = pop(lt, 30.76 - 27.49)
        if a > 0.01:
            ellipse(ctx, 230, 1270, 90 * a, 30 * a); fill_ink(ctx, (0.08, 0.08, 0.1), 4)
            label(ctx, "HOCKEY PUCK", W / 2, 300, a, rgb=YELLOW, size=50)


# 31.52 "The kid's grooved tires slice right through."
def e8(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.12)]), W / 2, 900)
    sky(ctx, T, P, sun=False)
    ctx.set_source_rgba(0.15, 0.18, 0.28, 0.40); ctx.paint()
    track(ctx, T, P, 1150, speed=1600, wet=1.0)
    car(ctx, W / 2, 1080, 0.95, T, col=KID, num="7")
    for k in range(8):  # salpicaduras hacia los lados
        ph = (T * 2.5 + k / 8) % 1.0
        for bx in (W / 2 - 190 * 0.95, W / 2 + 200 * 0.95):
            circle(ctx, bx - 160 * ph, 1130 - 120 * ph + 160 * ph * ph, 12 * (1 - ph) + 4); fill(ctx, WAT, 0.8 * (1 - ph))
    ctx.restore()
    rain(ctx, T, 1.0, 60, 8)
    label(ctx, "GROOVES", W / 2, 300, pop(lt, 31.96 - 31.52), rgb=KID, size=56)
    if T > 32.96:
        stamp(ctx, "SLICE!", W / 2, 640, (T - 32.96) / 0.25, col=(0.30, 0.78, 0.40), size=100)


# 33.80 "You see, every groove is a tiny gutter. It squeezes the water out from under the tire, so the rubber can still touch the road."  (luz azul)
def e9(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.08), (dur, 1.0)]), W / 2, 800)
    sky(ctx, T, P, sun=True)
    ctx.restore()
    # vista desde abajo: neumático pisando agua
    rrect(ctx, 60, 420, W - 120, 840, 40); fill_ink(ctx, mix(WAT, (0.3, 0.3, 0.35), 0.35), 5)
    tread(ctx, W / 2, 830, 520, 700, grooves=True)
    if T > 35.93:
        for k in range(1, 4):
            gx = W / 2 - 260 + k * 130
            for j in range(5):
                ph = (T * 1.2 + j / 5 + k * 0.13) % 1.0
                circle(ctx, gx, 830 + 350 - 700 * ph, 11); fill(ctx, WAT)
            arrow(ctx, gx, 470, gx, 400, pop(lt, 36.11 - 33.80), rgb=WAT, w=9)
        for sx in (-1, 1):
            for j in range(3):
                ph = (T * 1.4 + j / 3) % 1.0
                circle(ctx, W / 2 + sx * (290 + 120 * ph), 650 + 180 * j, 14 * (1 - ph) + 4); fill(ctx, WAT, 0.9)
    label(ctx, "TINY GUTTER", W / 2, 300, pop(lt, 35.28 - 33.80), rgb=WAT, size=52)
    if T > 38.51:
        a = pop(lt, 38.51 - 33.80)
        label(ctx, "RUBBER TOUCHES ROAD", W / 2, 1300, a, rgb=(0.30, 0.78, 0.40), size=40)


# 39.92 "Like the drains in a street."
def e10(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 850)
    sky(ctx, T, P)
    house2(ctx, 260, 900, 1.0)
    house2(ctx, 900, 900, 0.9, col=(0.62, 0.72, 0.90))
    ctx.rectangle(0, 900, W, 420); fill_ink(ctx, P["road"], 4)
    ctx.rectangle(0, 900, W, 60); fill_ink(ctx, P["conc"], 4)
    # rejilla
    rrect(ctx, W / 2 - 160, 1000, 320, 150, 10); fill_ink(ctx, (0.12, 0.12, 0.15), 5)
    for k in range(7):
        ctx.rectangle(W / 2 - 140 + k * 42, 1015, 18, 120); fill(ctx, (0.45, 0.45, 0.5))
    for sx in (-1, 1):
        for j in range(6):
            ph = (T * 1.1 + j / 6) % 1.0
            circle(ctx, W / 2 + sx * (560 - 420 * ph), 1075 + 20 * math.sin(j), 12); fill(ctx, WAT, 0.9)
    ctx.restore()
    label(ctx, "STREET DRAIN", W / 2, 300, pop(lt, 40.14 - 39.92), rgb=WAT, size=52)


# 41.07 "In other words, the smooth tires didn't lose grip. They lost the road."
def e11(ctx, lt, dur, T):
    P = pal(T)
    ctx.save()
    camera(ctx, punch(lt, big=1.4, end=1.08, dur=dur), W / 2, 820)
    sky(ctx, T, P)
    ctx.set_source_rgba(0.55, 0.05, 0.12, 0.22); ctx.paint()
    tire(ctx, W / 2, 780, 300, T, grooves=False, spin=T * 0.5)
    ctx.restore()
    if T > 42.66:
        stamp(ctx, "NOT GRIP", W / 2, 300, (T - 42.66) / 0.25, size=100)
    if T > 43.78:
        stamp(ctx, "THE ROAD", W / 2, 1250, (T - 43.78) / 0.25, col=(0.30, 0.78, 0.40), size=110)


# 44.63 "That's why the tires on your car have grooves."
def e12(ctx, lt, dur, T):
    P = pal(T)
    z = keyframes(lt, [(0, 1.0), (dur, 1.12)])
    blur_layer(ctx, lambda c: (camera(c, z, W / 2, 860), sky(c, T, P), house2(c, 300, 1100, 1.2), ground(c, 1100, P)))
    ctx.save()
    camera(ctx, z, W / 2, 860)
    tire(ctx, W / 2, 800, 330, T, grooves=True, spin=T * 0.3)
    ctx.restore()
    label(ctx, "YOUR CAR", W / 2, 300, pop(lt, 45.56 - 44.63), rgb=YELLOW, size=54)
    a = pop(lt, 46.30 - 44.63)
    if a > 0.01:
        label(ctx, "GROOVES", 880, 380, a, rgb=WAT, size=40)
        arrow(ctx, 880, 420, 820, 520, a, rgb=WAT, w=10)


# 46.78 "Because, just like" -> bucle
def e13(ctx, lt, dur, T):
    hero(ctx, lt, T, dur, 1.12, 1.35, labels=False)   # acaba en el mismo plano que el fotograma 0


ESCENAS = [(0.0, e1), (3.79, e2), (9.10, e3), (12.87, e4), (17.24, e5), (22.74, e6), (27.49, e7), (31.52, e8),
           (33.80, e9), (39.92, e10), (41.07, e11), (44.63, e12), (46.78, e13)]

SFX = [(0.1, "squish"), (2.13, "thud"), (2.4, "pop"), (3.75, "whoosh"), (5.7, "ding"), (7.4, "pop"), (9.05, "whoosh"), (10.4, "crack"), (11.4, "drum"),
       (12.85, "whoosh"), (14.7, "pop"), (15.9, "ding"), (17.2, "whoosh"), (19.9, "bell"), (21.2, "pop"),
       (22.7, "whoosh"), (23.96, "thud"), (24.7, "rise"), (27.0, "squish"), (27.45, "whoosh"), (28.6, "rise"),
       (29.7, "crack"), (30.76, "thud"), (31.5, "whoosh"), (32.96, "crack"), (33.75, "whoosh"), (35.54, "pop"),
       (36.1, "squish"), (39.6, "ding"), (39.9, "whoosh"), (41.03, "thud"), (42.66, "thud"), (43.78, "thud"),
       (44.6, "whoosh"), (46.3, "pop"), (46.7, "whoosh")]


def MINIATURA(ctx):
    T = 0.5
    P = pal(0.0)
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    sky(ctx, T, P)
    ground(ctx, 1500, P, col=P["road"])
    tire(ctx, W / 2, 1030, 430, T, grooves=True)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["WHY DO TIRES", ("HAVE GROOVES?", WHITE)], y=260, size=150)
    thumb_circle(ctx, W / 2 + 330, 760, 200, 140)
