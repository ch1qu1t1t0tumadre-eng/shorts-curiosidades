"""v22 (EN) FORMATO BUCLE: Isaac Newton stuck a needle (bodkin) into his own eye, ca. 1669 (Cambridge, MS Add. 3975)."""
from kit import *  # noqa

IRIS = (0.30, 0.55, 0.95)
STEEL = (0.78, 0.80, 0.86)
SCLERA = (0.97, 0.96, 0.93)
BONE = (0.92, 0.86, 0.72)
PURPLE_TOP = (0.10, 0.05, 0.18)
PURPLE_MID = (0.22, 0.10, 0.34)


def eyeball(ctx, x, y, r, T, look=(0.0, 0.0), glow=0.0, wobble=0.0):
    """Ojo de dibujo (de frente): esclera, iris azul, pupila, brillo y venitas suaves."""
    ox = look[0] * r * 0.25 + wobble * math.sin(T * 30) * r * 0.05
    oy = look[1] * r * 0.25
    if glow > 0:
        spotlight(ctx, x, y, r * 2.0, 0.35 * glow, (0.7, 0.85, 1.0))
    soft_shadow(ctx, x, y + r * 1.02, r * 0.8, r * 0.12, 0.35)
    circle(ctx, x, y, r)
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.35, r * 0.1, x, y, r)
    g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(0.75, *SCLERA); g.add_color_stop_rgb(1, 0.78, 0.74, 0.72)
    ctx.set_source(g); ctx.fill()
    for k in range(5):  # venitas
        a = 0.6 + k * 1.15
        ctx.move_to(x + math.cos(a) * r * 0.97, y + math.sin(a) * r * 0.97)
        ctx.curve_to(x + math.cos(a + 0.15) * r * 0.85, y + math.sin(a + 0.15) * r * 0.85,
                     x + math.cos(a - 0.1) * r * 0.78, y + math.sin(a - 0.1) * r * 0.78,
                     x + math.cos(a + 0.05) * r * 0.7, y + math.sin(a + 0.05) * r * 0.7)
        stroke(ctx, (0.85, 0.35, 0.35), 3, 0.35)
    ix, iy = x + ox, y + oy
    circle(ctx, ix, iy, r * 0.45)
    gi = cairo.RadialGradient(ix, iy, r * 0.05, ix, iy, r * 0.45)
    gi.add_color_stop_rgb(0, 0.55, 0.80, 1.0); gi.add_color_stop_rgb(1, 0.10, 0.25, 0.60)
    ctx.set_source(gi); ctx.fill()
    for k in range(18):
        a = k * math.tau / 18
        ctx.move_to(ix + math.cos(a) * r * 0.22, iy + math.sin(a) * r * 0.22)
        ctx.line_to(ix + math.cos(a) * r * 0.43, iy + math.sin(a) * r * 0.43)
    stroke(ctx, (0.75, 0.90, 1.0), 2, 0.35)
    circle(ctx, ix, iy, r * 0.20); fill(ctx, (0.02, 0.02, 0.05))
    circle(ctx, ix - r * 0.14, iy - r * 0.16, r * 0.08); fill(ctx, WHITE, 0.9)
    circle(ctx, ix + r * 0.10, iy + r * 0.10, r * 0.035); fill(ctx, WHITE, 0.6)


def bodkin(ctx, x, y, L, rot=0.0, s=1.0):
    """Bodkin: aguja gruesa y ROMA (punta redondeada) con ojo grande. (x, y) = punta."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(0, -9); ctx.line_to(L, -14); ctx.arc(L, 0, 14, -math.pi / 2, math.pi / 2); ctx.line_to(0, 9)
    ctx.arc(0, 0, 9, math.pi / 2, 3 * math.pi / 2)
    ctx.close_path()
    ctx.set_source(vgrad(ctx, 0, -14, 0, 14, [(0, (0.95, 0.96, 1.0)), (0.5, STEEL), (1, (0.45, 0.47, 0.55))]))
    ctx.fill()
    rrect(ctx, L - 60, -5, 44, 10, 5); fill(ctx, (0.10, 0.10, 0.15))  # ojo de la aguja
    ctx.move_to(20, -5); ctx.line_to(L - 80, -8); stroke(ctx, WHITE, 3, 0.6)
    ctx.restore()


def bg_purple(ctx, T):
    bg_dark(ctx, T, top=PURPLE_TOP, mid=PURPLE_MID)


def hero(ctx, T, zoom):
    """Plano del gancho (inicio y final del bucle): ojo gigante + bodkin acercándose + ficha de Newton."""
    camera(ctx, zoom, W / 2, 760)
    bg_purple(ctx, T)
    rays(ctx, W / 2 - 110, 560, T, (0.6, 0.8, 1.0), 0.05)
    eyeball(ctx, W / 2 - 110, 560, 270, T, look=(0.7, -0.1), glow=1.0)
    bodkin(ctx, W / 2 + 200 + 12 * math.sin(T * 3), 500, 300, rot=-0.45, s=1.3)
    ctx.restore(); ctx.save()
    ficha(ctx, "ISAAC NEWTON", "PHYSICIST · 1643–1727", W / 2, 1460, 1.0, "🍎", YELLOW)


def notebook(ctx, x, y, s, T, draw=1.0, page="15", rot=-0.04):
    """Cuaderno abierto con el dibujo del experimento (ojo de perfil + aguja detrás) que se va dibujando."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -430, -330, 860, 660, 18); fill(ctx, (0.35, 0.22, 0.12))
    rrect(ctx, -410, -310, 405, 620, 8); fill(ctx, PAPER)
    rrect(ctx, 5, -310, 405, 620, 8); fill(ctx, PAPER)
    ctx.move_to(0, -310); ctx.line_to(0, 310); stroke(ctx, (0.6, 0.55, 0.45), 4)
    for k in range(10):  # renglones escritos a mano
        ww = 300 if k % 3 else 220
        p = clamp(draw * 12 - k)
        if p > 0:
            ctx.move_to(-380, -250 + k * 52)
            n = int(ww * p / 10)
            for j in range(n):
                ctx.line_to(-380 + j * 10, -250 + k * 52 + 4 * math.sin(j * 1.7 + k))
            stroke(ctx, INK, 3, 0.7)
    # dibujo: ojo de perfil (circulo) + hueso + aguja pasando por detrás
    p = clamp(draw * 1.4 - 0.2)
    ctx.new_path(); ctx.arc(210, -40, 120, -math.pi / 2, -math.pi / 2 + math.tau * p); stroke(ctx, INK, 5)
    if p > 0.5:
        ctx.new_path(); ctx.arc(210, -40, 175, 2.2, 4.3); stroke(ctx, INK, 5)
        ctx.move_to(60, 160); ctx.line_to(60 + 220 * clamp(p * 2 - 1), 160 - 230 * clamp(p * 2 - 1))
        stroke(ctx, INK, 5)
    text(ctx, page, 380, 280, 34, INK, shadow=False, align="right")
    ctx.restore()


def calendar(ctx, x, y, s, top, big, small):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -230, -200, 460, 420, 24); fill(ctx, WHITE)
    rrect(ctx, -230, -200, 460, 100, 24); fill(ctx, IRIS)
    text(ctx, top, 0, -150, 50, WHITE, shadow=False)
    text(ctx, big, 0, 20, 140, INK, shadow=False)
    text(ctx, small, 0, 160, 40, (0.4, 0.4, 0.45), shadow=False)
    ctx.restore()


def college(ctx, x, y, s, T):
    """Silueta de colegio de Cambridge (torres góticas)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    col = (0.20, 0.16, 0.30)
    ctx.rectangle(-420, -200, 840, 400); fill(ctx, col)
    for sx in (-1, 1):
        ctx.rectangle(sx * 330 - 60, -420, 120, 620); fill(ctx, col)
        ctx.move_to(sx * 330 - 70, -420); ctx.line_to(sx * 330, -540); ctx.line_to(sx * 330 + 70, -420); fill(ctx, col)
    ctx.move_to(-120, -200); ctx.line_to(0, -330); ctx.line_to(120, -200); fill(ctx, col)
    for k in range(6):
        rrect(ctx, -250 + k * 100, -120, 50, 110, 25); fill(ctx, (1, 0.85, 0.5), 0.6 + 0.3 * math.sin(T * 2 + k))
    rrect(ctx, -60, 40, 120, 160, 60); fill(ctx, (0.08, 0.06, 0.12))
    ctx.restore()


def prism(ctx, x, y, s, T, p=1.0):
    """Prisma con haz blanco que sale en arcoíris."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-520, -40); ctx.line_to(-60, 0); stroke(ctx, WHITE, 18, 0.9)
    cols = [(1, 0.2, 0.2), (1, 0.6, 0.1), (1, 0.95, 0.2), (0.3, 0.9, 0.3), (0.2, 0.6, 1), (0.5, 0.3, 0.9)]
    for k, c in enumerate(cols):
        ctx.move_to(60, 10)
        ctx.line_to(60 + 420 * p, -60 + k * 40 * (0.6 + 0.4 * p) + 10)
        stroke(ctx, c, 14, 0.9)
    ctx.move_to(0, -200); ctx.line_to(170, 120); ctx.line_to(-170, 120); ctx.close_path()
    fill_keep(ctx, GLASS, 0.30); stroke(ctx, WHITE, 6, 0.9)
    ctx.restore()


def section(ctx, x, y, s, T, slide=1.0, press=0.0):
    """Corte lateral (esquema, sin gore): hueso de la órbita, globo ocular y bodkin que se desliza por detrás."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # hueso (arco grueso detrás del ojo)
    ctx.new_path(); ctx.arc(0, 0, 330, 2.0, 4.6); stroke(ctx, BONE, 60)
    ctx.new_path(); ctx.arc(0, 0, 330, 2.0, 4.6); stroke(ctx, (0.6, 0.52, 0.38), 4, 0.6)
    # ojo de perfil (deformado al presionar)
    ctx.save(); ctx.scale(1 - 0.06 * press, 1 + 0.03 * press)
    circle(ctx, 0, 0, 240)
    g = cairo.RadialGradient(-60, -60, 30, 0, 0, 240)
    g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(1, 0.86, 0.82, 0.80)
    ctx.set_source(g); ctx.fill()
    ctx.new_path(); ctx.arc(0, 0, 240, -0.55, 0.55); stroke(ctx, IRIS, 26)
    ctx.restore()
    # aguja entre ojo y hueso (de abajo a arriba por la parte de atrás)
    L = 560
    tip_y = 420 - 520 * slide
    bodkin(ctx, -272 + 10 * press * math.sin(T * 12), tip_y, L, rot=math.pi / 2, s=1.0)
    if press > 0:
        for k in range(3):  # ondas de presión
            rr = 260 + ((T * 160 + k * 60) % 180)
            ctx.new_path(); ctx.arc(0, 0, rr, -0.9, 0.9); stroke(ctx, YELLOW, 5, 0.5 * (1 - (rr - 260) / 180) * press)
    ctx.restore()


def color_rings(ctx, x, y, T, p=1.0):
    cols = [WHITE, (0.08, 0.08, 0.12), (1, 0.3, 0.3), (1, 0.8, 0.2), (0.3, 0.9, 0.4), (0.3, 0.6, 1), (0.7, 0.4, 1)]
    for k in range(len(cols) - 1, -1, -1):
        r = (60 + k * 62) * (0.85 + 0.15 * math.sin(T * 3 - k * 0.6)) * p
        circle(ctx, x, y, r)
        fill(ctx, cols[k], 0.95)


def mirror(ctx, x, y, s, T):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 1.35); circle(ctx, 0, 0, 200); ctx.restore()
    fill(ctx, WOOD)
    ctx.save(); ctx.scale(1, 1.35); circle(ctx, 0, 0, 170); ctx.restore()
    ctx.set_source(vgrad(ctx, 0, -230, 0, 230, [(0, (0.85, 0.95, 1.0)), (1, (0.55, 0.70, 0.85))])); ctx.fill()
    circle(ctx, 20, -40, 70 + 6 * math.sin(T * 5)); fill(ctx, (1, 0.95, 0.6))
    spotlight(ctx, 20, -40, 200, 0.6, (1, 0.95, 0.6))
    ctx.move_to(-110, -150); ctx.line_to(-40, -150); ctx.line_to(-110, -40); fill(ctx, WHITE, 0.4)
    rrect(ctx, -20, 260, 40, 140, 10); fill(ctx, WOOD_D)
    ctx.restore()


# 0.00 "Isaac Newton stuck a needle into his own eye."
def e1(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 1.0), (dur, 1.12)]))


# 3.37 "On purpose."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (dur, 1.05)]), W / 2, 760)
    bg_purple(ctx, T)
    bodkin(ctx, 180, 560, 720, rot=-0.1, s=1.0)
    stamp(ctx, "ON PURPOSE", W / 2, 1420, (lt - 0.15) / 0.3, size=100)


# 4.32 "And it's real."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.06, 0.05, 0.10), mid=(0.16, 0.12, 0.20))
    notebook(ctx, W / 2, 620, 1.0, T, draw=1.0, page="")
    badge(ctx, "100% REAL", W / 2, 1420, pop(lt, 0.3), size=70)


# 5.41 "Around 1669,"
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 820)
    bg_night(ctx, T, grid=False)
    ground(ctx, 1500, (0.10, 0.08, 0.16))
    college(ctx, W / 2, 1150, 1.0, T)
    calendar(ctx, W / 2, 400, 0.8, "AROUND", str(int(counter(lt, 1600, 1669, 0.9))), "CAMBRIDGE")


# 7.07 "Newton wanted to know how we see color."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.03, 0.04, 0.10), mid=(0.06, 0.08, 0.20))
    prism(ctx, W / 2, 560, 1.0, T, p=ease(clamp(lt / 1.0)))
    character(ctx, 230, 1380, 0.75, T, mood="duda", look=(1, -1))
    pill(ctx, "HOW DO WE SEE COLOR?", 640, 1480, pop(lt, 0.8), size=42, rgb=TEAL)


# 9.35 "So he grabbed a bodkin, a thick blunt needle."
def e6(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.15)]), W / 2, 700)
    bg_blueprint(ctx, T)
    bodkin(ctx, 170, 660, 480, rot=-0.18 + 0.03 * math.sin(T * 2), s=1.6)
    pill(ctx, "BODKIN", 300, 380, pop(lt, 0.3), size=60, rgb=YELLOW)
    pill(ctx, "THICK · BLUNT", W / 2, 1420, pop(lt, 1.6), size=50, rgb=STEEL)
    arrow(ctx, 300, 430, 240, 600, clamp((lt - 0.5) / 0.4))


# 12.31 "He slid it behind his eyeball,"
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 720)
    bg_dark(ctx, T, top=(0.04, 0.10, 0.12), mid=(0.08, 0.20, 0.24))
    section(ctx, W / 2 + 60, 620, 1.0, T, slide=ease(clamp(lt / 1.8)))
    badge(ctx, "SIDE VIEW", 250, 280, pop(lt, 0.1), size=40, bg=(0.2, 0.3, 0.5))


# 14.39 "between the eye and the bone."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.3)]), W / 2 - 120, 640)
    bg_dark(ctx, T, top=(0.04, 0.10, 0.12), mid=(0.08, 0.20, 0.24))
    section(ctx, W / 2 + 60, 620, 1.0, T, slide=1.0)
    pill(ctx, "EYE", 640, 380, pop(lt, 0.2), size=44, rgb=IRIS)
    pill(ctx, "BONE", 300, 300, pop(lt, 0.9), size=44, rgb=BONE, fg=INK)


# 16.00 "Then he pressed, and moved it around."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]) + 0.004 * math.sin(T * 25), W / 2, 680)
    bg_dark(ctx, T, top=(0.12, 0.05, 0.10), mid=(0.24, 0.10, 0.18))
    section(ctx, W / 2 + 60, 620, 1.0, T, slide=1.0, press=clamp(lt / 0.4))
    pill(ctx, "PRESS", 820, 300, pop(lt, 0.2), size=50, rgb=RED)


# 18.29 "In other words,"  (2.º gancho)
def e10(ctx, lt, dur, T):
    camera(ctx, punch(lt, dur=dur), W / 2, 760)
    bg_dark(ctx, T, top=(0.22, 0.03, 0.06), mid=(0.12, 0.02, 0.05))
    rays(ctx, W / 2, 640, T, RED, 0.08)
    eyeball(ctx, W / 2, 640, 330, T, look=(0, 0), glow=0.6, wobble=1.0)


# 19.19 "Newton used his own eyeball as a lab rat."
def e11(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.05), (dur, 1.15)]), W / 2, 760)
    bg_dark(ctx, T, top=(0.04, 0.12, 0.06), mid=(0.10, 0.24, 0.14))
    # matraz de laboratorio con el ojo dentro
    ctx.move_to(W / 2 - 90, 220); ctx.line_to(W / 2 - 90, 420); ctx.line_to(W / 2 - 330, 860)
    ctx.line_to(W / 2 + 330, 860); ctx.line_to(W / 2 + 90, 420); ctx.line_to(W / 2 + 90, 220); ctx.close_path()
    fill_keep(ctx, GLASS, 0.12); stroke(ctx, GLASS, 8, 0.9)
    eyeball(ctx, W / 2, 700, 150, T, look=(math.sin(T * 2), 0.3))
    icon(ctx, "🐀", 860, 1360, 210, pop(lt, 1.6))
    stamp(ctx, "LAB RAT", 380, 1400, (lt - 1.7) / 0.3, size=90)
    character(ctx, 170, 520, 0.55, T, mood="sorpresa")


# 22.12 "He saw white, dark and colored circles."
def e12(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.2), (dur, 1.0)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.02, 0.02, 0.05), mid=(0.05, 0.05, 0.10))
    color_rings(ctx, W / 2, 650, T, p=ease_back(clamp(lt / 0.6)))


# 24.74 "And he wrote it all down,"
def e13(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 700)
    bg_dark(ctx, T, top=(0.10, 0.07, 0.04), mid=(0.20, 0.14, 0.08))
    notebook(ctx, W / 2, 640, 1.0, T, draw=clamp(lt / 1.8) * 0.75, page="")
    icon(ctx, "🪶", 900, 330, 200, pop(lt, 0.1), rot=0.2 + 0.1 * math.sin(T * 6))


# 26.52 "with a drawing of the needle inside his eye."
def e14(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.3), (dur, 1.55)]), W / 2 + 140, 620)
    bg_dark(ctx, T, top=(0.10, 0.07, 0.04), mid=(0.20, 0.14, 0.08))
    notebook(ctx, W / 2, 640, 1.0, T, draw=0.75 + 0.25 * clamp(lt / 1.0), page="")
    thumb_circle(ctx, W / 2 + 205, 600, 150, 150) if lt > 0.9 else None


# 28.61 "Newton also stared at the sun in a mirror"
def e15(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 760)
    bg_sky(ctx, T, warm=0.7)
    sun(ctx, 860, 260, 120, T)
    mirror(ctx, 330, 700, 1.0, T)
    eyeball(ctx, 780, 760, 140, T, look=(-1, 0), glow=0.8)
    arrow(ctx, 820, 380, 420, 600, clamp(lt / 0.6), rgb=(1, 0.85, 0.2))
    arrow(ctx, 420, 650, 700, 740, clamp((lt - 0.6) / 0.6), rgb=(1, 0.85, 0.2))


# 30.86 "until he had to hide in a dark room for days."
def e16(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.12)]), W / 2, 820)
    ctx.set_source_rgb(0.02, 0.02, 0.04); ctx.paint()
    rrect(ctx, W / 2 - 200, 380, 400, 760, 12); fill(ctx, (0.10, 0.08, 0.10))
    rrect(ctx, W / 2 - 200, 380, 400 * (1 - ease(clamp(lt / 0.8))) + 6, 760, 12); fill(ctx, (1, 0.9, 0.6), 0.5)
    character(ctx, W / 2, 1250, 0.6, T, mood="dormido") if lt > 0.8 else None
    pill(ctx, "DARK ROOM · DAYS", W / 2, 260, pop(lt, 1.2), size=48, rgb=STONE)


# 33.77 "His notebook is still at Cambridge."
def e17(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.1)]), W / 2, 820)
    bg_dark(ctx, T, top=(0.05, 0.05, 0.12), mid=(0.12, 0.10, 0.22))
    museum_case(ctx, W / 2, 760, 1.0, T, content=lambda c, t: notebook(c, 0, 20, 0.5, t, draw=1.0, page="", rot=0.0))
    pill(ctx, "CAMBRIDGE UNIVERSITY LIBRARY", W / 2, 1440, pop(lt, 0.4), size=38, rgb=GOLD)


# 35.48 "On page 15"
def e18(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.3)]), W / 2 + 200, 760)
    bg_dark(ctx, T, top=(0.10, 0.07, 0.04), mid=(0.20, 0.14, 0.08))
    notebook(ctx, W / 2, 640, 1.0, T, draw=1.0, page="p. 15")
    badge(ctx, "PAGE 15", 760, 300, pop(lt, 0.2), size=60)


# 36.58 "you can read how"  → bucle: "Isaac Newton stuck a needle into his own eye."
def e19(ctx, lt, dur, T):
    hero(ctx, T, keyframes(lt, [(0, 0.92), (dur, 1.0)]))


ESCENAS = [(0.0, e1), (3.37, e2), (4.32, e3), (5.41, e4), (7.07, e5), (9.35, e6), (12.31, e7), (14.39, e8),
           (16.00, e9), (18.29, e10), (19.19, e11), (22.12, e12), (24.74, e13), (26.52, e14), (28.61, e15),
           (30.86, e16), (33.77, e17), (35.48, e18), (36.58, e19)]
SFX = [(3.45, "pop"), (18.31, "ding"), (36.0, "pop")]


def MINIATURA(ctx):
    T = 1.0
    ctx.save()
    camera(ctx, 1.0, W / 2, 1000)
    bg_purple(ctx, T)
    rays(ctx, W / 2, 1050, T, (0.6, 0.8, 1.0), 0.07)
    eyeball(ctx, W / 2 - 40, 1050, 330, T, look=(0.6, -0.1), glow=1.3)
    bodkin(ctx, W / 2 + 260, 930, 300, rot=-0.45, s=1.3)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["NEWTON DID", ("WHAT?!", WHITE)], y=270, size=180)
    thumb_circle(ctx, W / 2 + 330, 880, 150, 130)
    ficha(ctx, "ISAAC NEWTON", "PHYSICIST · 1643–1727", W / 2, 1620, 1.0, "🍎", YELLOW)
