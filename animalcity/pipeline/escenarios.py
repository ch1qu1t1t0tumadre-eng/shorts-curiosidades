"""Decorados con ambiente propio para AnimalCity TV (coordenadas del mundo 1080x1920; la cámara ya está puesta).

    rincon_nana(ctx, T, var)            rincón cálido de Nana: chimenea encendida, estantería, lámpara, cesta de lana
    cocina_noche(ctx, T, var)           cocina de noche: ventana con luna, sartenes colgadas, lámpara de techo
    pasillo(ctx, T, var, timbre)        pasillo en perspectiva hacia la puerta de la calle (timbre 0..1 = brilla)
    entrada_noche(ctx, T, var, abierta) desde dentro: puerta abierta a la calle de noche (luna, farola, luciérnagas)
    edificio(ctx, T, encendidas, var)   el edificio de noche visto desde la calle; las ventanas se van encendiendo
    escenario_foco(ctx, T, rgb)         escenario oscuro con cortinas y un foco (momentos dramáticos)
Suelo: 1440 en casi todos (los pies de los personajes van entre 1450 y 1650).
"""
import math
import numpy as np
from anim import *  # noqa: F401,F403
import cairocffi as cairo
from efectos import luciernagas, motas, destello, _nube, nube_pintada, INK

FLOOR_Y = 1440


def _fondo(ctx, rgb, y1=FLOOR_Y):
    ctx.rectangle(-3000, -3000, W + 6000, 3000 + y1)
    fill(ctx, rgb)


def _suelo_madera(ctx, rgb, y0=FLOOR_Y, vp=None):
    ctx.rectangle(-3000, y0, W + 6000, 3000)
    fill(ctx, rgb)
    for k in range(-24, 34):
        x = k * 120
        ctx.move_to(x, y0)
        ctx.line_to(x + (x - (vp or 540)) * 1.4, y0 + 1600)
    stroke(ctx, INK, 3, 0.22)
    for j, yy in enumerate((y0 + 70, y0 + 170, y0 + 310, y0 + 500)):
        ctx.move_to(-3000, yy)
        ctx.line_to(W + 3000, yy)
    stroke(ctx, INK, 2, 0.12)
    ctx.move_to(-3000, y0)
    ctx.line_to(W + 3000, y0)
    stroke(ctx, INK, 7)


def _vga(y0, y1, stops):
    """Degradado vertical con transparencia: stops = [(pos, (r, g, b, a)), ...]."""
    g = cairo.LinearGradient(0, y0, 0, y1)
    for off, c in stops:
        g.add_color_stop_rgba(off, *c)
    return g


def _glow(ctx, x, y, r, rgb, a):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *rgb, a)
    g.add_color_stop_rgba(1, *rgb, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


def llamas(ctx, x, y, w, h, T):
    """Fuego animado de dibujos (3 capas)."""
    for capa, (col, k) in enumerate(((hexc("#E8462E"), 1.0), (hexc("#FF9F1C"), 0.72), (hexc("#FFE45E"), 0.45))):
        ctx.move_to(x - w / 2 * k, y)
        n = 5
        for i in range(n):
            fx = x - w / 2 * k + (i + 0.5) * w * k / n
            fh = h * k * (0.65 + 0.35 * math.sin(T * (7 + i * 1.3) + i * 2 + capa))
            ctx.curve_to(fx - w * k / n * 0.5, y - fh * 0.5, fx - w * k / n * 0.1, y - fh, fx, y - fh)
            ctx.curve_to(fx + w * k / n * 0.1, y - fh, fx + w * k / n * 0.5, y - fh * 0.5, fx + w * k / n * 0.5, y)
        ctx.close_path()
        fill(ctx, col)


# ---------------------------------------------------------------- rincón de Nana
def rincon_nana(ctx, T, var=0):
    pared = [hexc("#6E3F63"), hexc("#7A4A3A"), hexc("#3F4F6E")][var % 3]
    ctx.rectangle(-3000, -3000, W + 6000, 3000 + FLOOR_Y)
    ctx.set_source(vgrad(ctx, 0, 0, 0, FLOOR_Y, [(0, tuple(c * 0.75 for c in pared)), (1, pared)]))
    ctx.fill()
    # papel pintado de florecitas
    for gx in range(-12, 24):
        for gy in range(-6, 16):
            px, py = gx * 110 + (55 if gy % 2 else 0), gy * 110
            for a in range(5):
                ang = a * 2 * math.pi / 5
                circle(ctx, px + math.cos(ang) * 11, py + math.sin(ang) * 11, 8)
            fill(ctx, WHITE, 0.07)
    # zócalo
    ctx.rectangle(-3000, FLOOR_Y - 90, W + 6000, 90)
    fill_keep(ctx, hexc("#4A2C2A"))
    stroke(ctx, INK, 5)
    # chimenea (izquierda)
    rrect(ctx, 30, 860, 470, 600, 14)
    fill_keep(ctx, hexc("#B5523B"))
    stroke(ctx, INK, 7)
    for row in range(10):  # ladrillos
        for col in range(6):
            bx = 40 + col * 80 + (40 if row % 2 else 0)
            if bx < 470:
                ctx.rectangle(bx, 880 + row * 58, 72, 50)
                fill(ctx, hexc("#C9654A") if (row + col) % 3 else hexc("#A8462F"), 0.9)
    rrect(ctx, 10, 830, 510, 52, 8)  # repisa
    fill_keep(ctx, hexc("#6B3E2A"))
    stroke(ctx, INK, 6)
    rrect(ctx, 120, 1110, 290, 350, 140)  # hueco del fuego
    fill_keep(ctx, hexc("#1E1418"))
    stroke(ctx, INK, 7)
    ctx.save()
    rrect(ctx, 120, 1110, 290, 350, 140)
    ctx.clip()
    _glow(ctx, 265, 1440, 260, (1, 0.55, 0.15), 0.75)
    llamas(ctx, 265, 1440, 240, 230, T)
    ctx.restore()
    # leña
    for i, (lx, ang) in enumerate(((210, -0.15), (320, 0.18))):
        ctx.save()
        ctx.translate(lx, 1430)
        ctx.rotate(ang)
        rrect(ctx, -80, -22, 160, 44, 20)
        fill_keep(ctx, hexc("#6B4423"))
        stroke(ctx, INK, 5)
        ctx.restore()
    # cosas en la repisa: reloj, foto de familia, vela
    circle(ctx, 120, 760, 62)
    fill_keep(ctx, hexc("#F2E3C6"))
    stroke(ctx, INK, 6)
    ang = T * 0.8
    ctx.move_to(120, 760)
    ctx.line_to(120 + math.cos(ang) * 40, 760 + math.sin(ang) * 40)
    ctx.move_to(120, 760)
    ctx.line_to(120, 725)
    stroke(ctx, INK, 6)
    rrect(ctx, 230, 690, 120, 140, 8)
    fill_keep(ctx, hexc("#E0B04A"))
    stroke(ctx, INK, 6)
    rrect(ctx, 248, 708, 84, 104, 4)
    fill(ctx, hexc("#9FD4E8"))
    circle(ctx, 290, 770, 22)
    fill(ctx, hexc("#F08A3C"))  # foto de Teddy de pequeño
    ctx.rectangle(420, 730, 34, 100)
    fill_keep(ctx, hexc("#F7F1E3"))
    stroke(ctx, INK, 5)
    fl = 1 + 0.15 * math.sin(T * 13)
    ellipse(ctx, 437, 712, 12 * fl, 22 * fl)
    fill(ctx, hexc("#FFB238"))
    _glow(ctx, 437, 712, 90, (1, 0.8, 0.4), 0.35)
    # cuadro grande
    rrect(ctx, 600, 420, 300, 230, 10)
    fill_keep(ctx, hexc("#C99A3A"))
    stroke(ctx, INK, 7)
    ctx.rectangle(625, 445, 250, 180)
    ctx.set_source(vgrad(ctx, 0, 445, 0, 625, [(0, hexc("#8FD0F0")), (1, hexc("#CFEFD8"))]))
    ctx.fill()
    ctx.move_to(625, 625)
    ctx.line_to(700, 540)
    ctx.line_to(760, 590)
    ctx.line_to(820, 520)
    ctx.line_to(875, 625)
    ctx.close_path()
    fill(ctx, hexc("#5E9E62"))
    # estantería (derecha)
    rrect(ctx, 930, 560, 260, 880, 10)
    fill_keep(ctx, hexc("#7A4B2E"))
    stroke(ctx, INK, 7)
    rng = np.random.default_rng(31 + var)
    for sy in (760, 980, 1200):
        ctx.rectangle(930, sy, 260, 24)
        fill_keep(ctx, hexc("#5A3420"))
        stroke(ctx, INK, 4)
        bx = 945
        while bx < 1170:
            bw, bh = rng.uniform(26, 44), rng.uniform(120, 190)
            ctx.rectangle(bx, sy - bh, bw, bh)
            fill_keep(ctx, hexc(rng.choice(["#E04A3A", "#3E7CC4", "#F4D35E", "#7FD1B9", "#B07CE8"])))
            stroke(ctx, INK, 3)
            bx += bw + 3
    # suelo y alfombra
    _suelo_madera(ctx, hexc("#7A5236"))
    ellipse(ctx, 640, 1600, 520, 120)
    fill_keep(ctx, hexc("#9C4A7E"), 0.9)
    stroke(ctx, INK, 6)
    ellipse(ctx, 640, 1600, 400, 85)
    stroke(ctx, hexc("#F4D35E"), 8, 0.7)
    # cesta de lana con ovillos
    rrect(ctx, 470, 1380, 170, 110, 30)
    fill_keep(ctx, hexc("#C98C4A"))
    stroke(ctx, INK, 6)
    for (bx, by, col) in ((510, 1380, "#FF5FA2"), (575, 1372, "#5EB8F2"), (545, 1350, "#FFD23F")):
        circle(ctx, bx, by, 36)
        fill_keep(ctx, hexc(col))
        stroke(ctx, INK, 4)
    # luz cálida del fuego sobre todo
    _glow(ctx, 265, 1280, 900, (1, 0.6, 0.25), 0.22 + 0.04 * math.sin(T * 9))
    motas(ctx, 0, 700, 700, 800, T, 16, 14)


# ---------------------------------------------------------------- cocina de noche
def cocina_noche(ctx, T, var=0):
    pared = [hexc("#2F5D62"), hexc("#3A4F7A")][var % 2]
    _fondo(ctx, pared)
    for gx in range(-20, 30):  # azulejos detrás de la encimera
        for gy in range(10, 15):
            rrect(ctx, gx * 70 + 3, gy * 70 + 3 + 60, 64, 64, 6)
            fill(ctx, WHITE, 0.1 if (gx + gy) % 2 else 0.05)
    # ventana con luna
    rrect(ctx, 90, 330, 400, 430, 14)
    fill_keep(ctx, hexc("#EDE6D6"))
    stroke(ctx, INK, 7)
    ctx.rectangle(115, 355, 350, 380)
    ctx.set_source(vgrad(ctx, 0, 355, 0, 735, [(0, hexc("#141846")), (1, hexc("#3D2E6E"))]))
    ctx.fill()
    ctx.save()
    ctx.rectangle(115, 355, 350, 380)
    ctx.clip()
    _glow(ctx, 360, 460, 160, (1, 0.97, 0.8), 0.35)
    circle(ctx, 360, 460, 62)
    fill(ctx, hexc("#FFF4C9"))
    circle(ctx, 384, 444, 62)
    fill(ctx, hexc("#141846"))  # luna creciente
    rng = np.random.default_rng(5)
    for i in range(14):
        px, py = 115 + rng.uniform(0, 350), 355 + rng.uniform(0, 250)
        destello(ctx, px, py, 9 * (0.6 + 0.4 * math.sin(T * 3 + i)), WHITE, 0.9)
    ctx.restore()
    ctx.move_to(290, 355)
    ctx.line_to(290, 735)
    stroke(ctx, hexc("#EDE6D6"), 10)
    # cortinas
    for side in (-1, 1):
        cx = 290 + side * 225
        ctx.move_to(cx, 310)
        ctx.curve_to(cx - side * 80, 500, cx + side * 10, 650, cx - side * 40, 800)
        ctx.line_to(cx + side * 40, 800)
        ctx.line_to(cx + side * 40, 310)
        ctx.close_path()
        fill_keep(ctx, hexc("#F2C14E"))
        stroke(ctx, INK, 6)
    # muebles altos y sartenes
    rrect(ctx, 560, 300, 520, 300, 10)
    fill_keep(ctx, hexc("#E9DCC3"))
    stroke(ctx, INK, 7)
    ctx.move_to(820, 300)
    ctx.line_to(820, 600)
    stroke(ctx, INK, 5)
    ctx.move_to(-200, 800)
    ctx.line_to(520, 800)
    stroke(ctx, hexc("#9AA3AD"), 10)
    for i, px in enumerate((40, 190, 340)):
        sw = 0.08 * math.sin(T * 1.5 + i)
        ctx.save()
        ctx.translate(px, 800)
        ctx.rotate(sw)
        ctx.move_to(0, 0)
        ctx.line_to(0, 70)
        stroke(ctx, INK, 6)
        circle(ctx, 0, 140, 60 - i * 8)
        fill_keep(ctx, hexc("#3B3F47"))
        stroke(ctx, INK, 5)
        ctx.restore()
    # nevera
    rrect(ctx, 830, 640, 280, 800, 22)
    fill_keep(ctx, hexc("#DDE7F0"))
    stroke(ctx, INK, 7)
    ctx.move_to(830, 940)
    ctx.line_to(1110, 940)
    stroke(ctx, INK, 6)
    for (mx, my, col) in ((880, 720, "#FF5FA2"), (960, 800, "#FFD23F"), (900, 1050, "#7CE38B")):
        circle(ctx, mx, my, 18)
        fill_keep(ctx, hexc(col))
        stroke(ctx, INK, 3)
    # encimera
    ctx.rectangle(-3000, 1180, 3830, 60)
    fill_keep(ctx, hexc("#D9A066"))
    stroke(ctx, INK, 7)
    ctx.rectangle(-3000, 1240, 3830, 200)
    fill_keep(ctx, hexc("#6E8FA6"))
    stroke(ctx, INK, 6)
    for dx in range(-10, 12):
        ctx.rectangle(dx * 150 + 10, 1260, 130, 160)
        stroke(ctx, INK, 4, 0.6)
    # frutero
    ellipse(ctx, 640, 1170, 110, 30)
    fill_keep(ctx, hexc("#C98C4A"))
    stroke(ctx, INK, 5)
    for (fx, col) in ((590, "#E04A3A"), (650, "#F4D35E"), (700, "#7CE38B")):
        circle(ctx, fx, 1135, 34)
        fill_keep(ctx, hexc(col))
        stroke(ctx, INK, 4)
    _suelo_madera(ctx, hexc("#4E5D6C"))
    for gx in range(-20, 30):  # baldosas
        for gy in range(0, 6):
            if (gx + gy) % 2:
                ctx.rectangle(gx * 120, FLOOR_Y + gy * 120, 120, 120)
                fill(ctx, WHITE, 0.08)
    # lámpara de techo con cono de luz
    ctx.move_to(540, -400)
    ctx.line_to(540, 220)
    stroke(ctx, INK, 6)
    ctx.move_to(450, 290)
    ctx.curve_to(450, 200, 630, 200, 630, 290)
    ctx.close_path()
    fill_keep(ctx, hexc("#FFD23F"))
    stroke(ctx, INK, 6)
    ctx.move_to(450, 290)
    ctx.line_to(140, 1440)
    ctx.line_to(940, 1440)
    ctx.line_to(630, 290)
    ctx.close_path()
    ctx.set_source(_vga(290, 1440, [(0, (1, 0.93, 0.6, 0.35)), (1, (1, 0.93, 0.6, 0.05))]))
    ctx.fill()


# ---------------------------------------------------------------- pasillo
def pasillo(ctx, T, var=0, timbre=0.0):
    vx, vy = 540, 930
    pared = [hexc("#E9C46A"), hexc("#9AD1D4")][var % 2]
    oscuro = tuple(c * 0.72 for c in pared)
    _fondo(ctx, oscuro, 3000)
    # pared del fondo con la puerta de la calle
    ctx.rectangle(300, 520, 480, 820)
    fill_keep(ctx, pared)
    stroke(ctx, INK, 6)
    # paredes laterales (perspectiva)
    for side in (-1, 1):
        xe = 300 if side < 0 else 780
        xo = -600 if side < 0 else 1680
        ctx.move_to(xe, 520)
        ctx.line_to(xo, -500)
        ctx.line_to(xo, 2400)
        ctx.line_to(xe, 1340)
        ctx.close_path()
        fill_keep(ctx, tuple(c * (0.86 if side < 0 else 0.8) for c in pared))
        stroke(ctx, INK, 6)
        for k, f in enumerate((0.35, 0.62)):  # cuadros en las paredes laterales
            px = xe + (xo - xe) * f
            top = 520 + (-500 - 520) * f * 0.55
            hgt = 240 * (1 + f * 1.6)
            wdt = 150 * (1 + f * 1.6)
            ctx.move_to(px, top + 200)
            ctx.line_to(px + side * wdt, top + 200 - side * 0 - wdt * 0.25)
            ctx.line_to(px + side * wdt, top + 200 + hgt - wdt * 0.25)
            ctx.line_to(px, top + 200 + hgt)
            ctx.close_path()
            fill_keep(ctx, hexc(["#FF8A3D", "#5EB8F2", "#7CE38B", "#FF5FA2"][(k + (side > 0) * 2 + var) % 4]))
            stroke(ctx, INK, 6)
    # suelo en perspectiva
    ctx.move_to(300, 1340)
    ctx.line_to(780, 1340)
    ctx.line_to(1680, 2400)
    ctx.line_to(-600, 2400)
    ctx.close_path()
    fill_keep(ctx, hexc("#8B5A3C"))
    stroke(ctx, INK, 6)
    for k in range(-6, 7):
        ctx.move_to(540 + k * 40, 1340)
        ctx.line_to(540 + k * 330, 2400)
    stroke(ctx, INK, 3, 0.25)
    # alfombra larga
    ctx.move_to(450, 1345)
    ctx.line_to(630, 1345)
    ctx.line_to(900, 2400)
    ctx.line_to(180, 2400)
    ctx.close_path()
    fill_keep(ctx, hexc("#C0392B"), 0.9)
    stroke(ctx, hexc("#F4D35E"), 8, 0.8)
    # puerta de la calle
    rrect(ctx, 400, 700, 280, 640, 8)
    fill_keep(ctx, hexc("#2F6690"))
    stroke(ctx, INK, 7)
    for (px, py) in ((430, 740), (560, 740), (430, 1000), (560, 1000)):
        rrect(ctx, px, py, 100, 220, 8)
        stroke(ctx, INK, 4, 0.6)
    circle(ctx, 640, 1030, 14)
    fill(ctx, hexc("#F4D35E"))
    circle(ctx, 540, 800, 12)  # mirilla
    fill_keep(ctx, hexc("#BFD7EA"))
    stroke(ctx, INK, 4)
    # timbre que se ilumina
    circle(ctx, 730, 990, 20)
    fill_keep(ctx, hexc("#F4D35E") if timbre > 0.3 else hexc("#C9B48C"))
    stroke(ctx, INK, 4)
    if timbre > 0.01:
        _glow(ctx, 730, 990, 160, (1, 0.9, 0.3), 0.6 * timbre)
        for i in range(3):
            r = 50 + i * 40 + 30 * ((T * 3) % 1)
            ctx.arc(730, 990, r, -0.9, 0.9)
            ctx.new_sub_path()
            ctx.arc(730, 990, r, math.pi - 0.9, math.pi + 0.9)
            ctx.new_sub_path()
        stroke(ctx, INK, 7, timbre)
    # perchero y apliques
    ctx.move_to(170, 1500)
    ctx.line_to(170, 800)
    stroke(ctx, hexc("#5A3420"), 18)
    for i, col in enumerate(("#E04A3A", "#3E7CC4")):
        ellipse(ctx, 170 + (i * 2 - 1) * 60, 900 + i * 40, 60, 110)
        fill_keep(ctx, hexc(col))
        stroke(ctx, INK, 5)
    for px in (230, 850):
        _glow(ctx, px, 520, 200, (1, 0.9, 0.6), 0.4)
        ellipse(ctx, px, 520, 34, 46)
        fill_keep(ctx, hexc("#FFE08A"))
        stroke(ctx, INK, 5)


# ---------------------------------------------------------------- entrada: puerta abierta a la calle de noche
def entrada_noche(ctx, T, var=0, abierta=1.0):
    pared = [hexc("#F2C46D"), hexc("#E8A9A9")][var % 2]
    _fondo(ctx, pared, 3000)
    for k in range(-20, 30):  # rayas del papel
        ctx.rectangle(k * 80, -3000, 26, 6000)
        fill(ctx, WHITE, 0.08)
    fx0, fy0, fx1, fy1 = 250, 360, 830, 1460
    # exterior (dentro del marco)
    ctx.save()
    ctx.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0)
    ctx.clip()
    ctx.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0)
    ctx.set_source(vgrad(ctx, 0, fy0, 0, fy1, [(0, hexc("#0E1440")), (0.6, hexc("#3B2C6E")), (1, hexc("#6B3F7A"))]))
    ctx.fill()
    rng = np.random.default_rng(21)
    for i in range(30):
        px, py = fx0 + rng.uniform(0, 580), fy0 + rng.uniform(0, 520)
        destello(ctx, px, py, 10 * (0.5 + 0.5 * math.sin(T * 2.5 + i)), WHITE, 0.9)
    _glow(ctx, 700, 520, 180, (1, 0.97, 0.8), 0.3)
    circle(ctx, 700, 520, 66)
    fill_keep(ctx, hexc("#FFF4C9"))
    stroke(ctx, INK, 5)
    for (cx, cy, cr) in ((680, 500, 12), (720, 545, 9), (690, 555, 6)):
        circle(ctx, cx, cy, cr)
        fill(ctx, hexc("#E8D9A0"))
    # casas de enfrente
    for i, (bx, bw, bh, col) in enumerate(((240, 220, 380, "#2A2552"), (450, 180, 300, "#352E63"), (620, 260, 420, "#241F49"))):
        ctx.rectangle(bx, 1180 - bh, bw, bh)
        fill(ctx, hexc(col))
        for wx in range(bx + 25, bx + bw - 30, 55):
            for wy in range(1180 - bh + 30, 1150, 70):
                if (wx * 7 + wy * 3 + i) % 5 < 2:
                    ctx.rectangle(wx, wy, 26, 34)
                    fill(ctx, hexc("#FFD46B"), 0.9)
    # acera, valla y arbustos
    ctx.rectangle(fx0, 1180, 580, 300)
    fill(ctx, hexc("#4A4560"))
    for px in range(fx0, fx1, 46):
        ctx.rectangle(px, 1120, 24, 120)
        fill_keep(ctx, hexc("#E8E1F0"))
        stroke(ctx, INK, 3)
    ctx.rectangle(fx0, 1150, 580, 16)
    fill(ctx, hexc("#E8E1F0"))
    for bx in (300, 780):
        nube_pintada(ctx, bx, 1270, 110, hexc("#2F6B3F"), 1.0, 5, 6, bx)
    # farola
    ctx.move_to(360, 1480)
    ctx.line_to(360, 760)
    stroke(ctx, hexc("#2B2B3A"), 16)
    rrect(ctx, 320, 700, 80, 80, 16)
    fill_keep(ctx, hexc("#FFE08A"))
    stroke(ctx, INK, 5)
    _glow(ctx, 360, 740, 300, (1, 0.9, 0.5), 0.45)
    ctx.move_to(330, 780)
    ctx.line_to(220, 1460)
    ctx.line_to(500, 1460)
    ctx.line_to(390, 780)
    ctx.close_path()
    ctx.set_source(_vga(780, 1460, [(0, (1, 0.9, 0.5, 0.3)), (1, (1, 0.9, 0.5, 0.02))]))
    ctx.fill()
    luciernagas(ctx, fx0, 900, 580, 400, T, 10, 4)
    ctx.restore()
    # marco y puerta abierta (hacia dentro)
    k = clamp(abierta)
    pw = 580 * (1 - 0.86 * k)
    ctx.rectangle(fx0, fy0, pw, fy1 - fy0)
    fill_keep(ctx, hexc("#8C3B2E"))
    stroke(ctx, INK, 7)
    circle(ctx, fx0 + pw - 34, 940, 16)
    fill(ctx, hexc("#F4D35E"))
    rrect(ctx, fx0 - 40, fy0 - 40, fx1 - fx0 + 80, fy1 - fy0 + 40, 10)
    ctx.rectangle(fx0, fy0, fx1 - fx0, fy1 - fy0 + 10)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    fill_keep(ctx, hexc("#F7F1E3"))
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    stroke(ctx, INK, 7)
    # aplique de pared con luz cálida
    _glow(ctx, 960, 760, 260, (1, 0.85, 0.5), 0.5)
    rrect(ctx, 925, 700, 70, 110, 30)
    fill_keep(ctx, hexc("#FFE08A"))
    stroke(ctx, INK, 5)
    # cuadro con llaves
    rrect(ctx, 40, 760, 150, 110, 10)
    fill_keep(ctx, hexc("#C98C4A"))
    stroke(ctx, INK, 5)
    for i in range(3):
        circle(ctx, 75 + i * 40, 820, 10)
        fill(ctx, hexc("#F4D35E"))
    # suelo interior y felpudo
    _suelo_madera(ctx, hexc("#9C6B47"), fy1)
    rrect(ctx, 330, fy1 + 20, 420, 80, 16)
    fill_keep(ctx, hexc("#C98C4A"))
    stroke(ctx, INK, 5)
    text(ctx, "HI!", 540, fy1 + 60, 40, hexc("#6B4423"), shadow=False)


# ---------------------------------------------------------------- edificio desde la calle
def edificio(ctx, T, encendidas=0.0, var=0, ondas=0.0):
    ctx.rectangle(-3000, -3000, W + 6000, 6000)
    ctx.set_source(vgrad(ctx, 0, -200, 0, 1700, [(0, hexc("#0B1035")), (1, hexc("#4B2F6E"))]))
    ctx.fill()
    rng = np.random.default_rng(41)
    for i in range(60):
        px, py = rng.uniform(-200, 1280), rng.uniform(-200, 900)
        destello(ctx, px, py, 9 * (0.5 + 0.5 * math.sin(T * 2 + i)), WHITE, 0.9)
    _glow(ctx, 880, 260, 220, (1, 0.97, 0.8), 0.3)
    circle(ctx, 880, 260, 80)
    fill(ctx, hexc("#FFF4C9"))
    # edificios vecinos
    for (bx, bw, bh, col) in ((-200, 330, 900, "#211B45"), (900, 400, 1000, "#1B163D")):
        ctx.rectangle(bx, 1700 - bh, bw, bh)
        fill(ctx, hexc(col))
    # nuestro edificio
    bx0, bx1, by0 = 170, 910, 380
    ctx.rectangle(bx0, by0, bx1 - bx0, 1700 - by0)
    fill_keep(ctx, hexc("#B5523B"))
    stroke(ctx, INK, 8)
    ctx.rectangle(bx0 - 20, by0 - 40, bx1 - bx0 + 40, 50)
    fill_keep(ctx, hexc("#7A3324"))
    stroke(ctx, INK, 6)
    # antena y gato en el tejado
    ctx.move_to(780, by0 - 40)
    ctx.line_to(780, by0 - 190)
    ctx.move_to(730, by0 - 160)
    ctx.line_to(830, by0 - 160)
    stroke(ctx, INK, 7)
    salto_gato = -110 * math.sin(math.pi * clamp((encendidas - 0.15) / 0.35)) if encendidas > 0.15 else 0
    ctx.save()
    ctx.translate(330, by0 - 40 + salto_gato)
    ellipse(ctx, 0, -40, 50, 36)
    fill(ctx, INK)
    circle(ctx, 40, -82, 30)
    fill(ctx, INK)
    for ex in (-14, 14):
        ctx.move_to(40 + ex - 12, -102)
        ctx.line_to(40 + ex, -128)
        ctx.line_to(40 + ex + 12, -102)
        fill(ctx, INK)
    for ex in (30, 52):
        circle(ctx, ex, -84, 6)
        fill(ctx, hexc("#FFE24A"))
    ctx.restore()
    # ventanas: 5 pisos x 4
    cols = [hexc(c) for c in ("#FFD46B", "#FFB86B", "#B8F0FF", "#FFE9A8")]
    k = 0
    order = np.random.default_rng(7).permutation(20)
    for fila in range(5):
        for col in range(4):
            wx = bx0 + 60 + col * 175
            wy = by0 + 80 + fila * 245
            idx = fila * 4 + col
            nuestra = (fila == 2 and col == 1)
            on = nuestra or (encendidas * 20 > list(order).index(idx))
            rrect(ctx, wx, wy, 120, 160, 8)
            fill_keep(ctx, cols[idx % 4] if on else hexc("#2A2552"))
            stroke(ctx, INK, 6)
            if on and not nuestra:
                ctx.save()
                ctx.rectangle(wx, wy, 120, 160)
                ctx.clip()
                circle(ctx, wx + 60, wy + 120, 44)  # vecino asomado (silueta con ojos)
                fill(ctx, INK, 0.85)
                ellipse(ctx, wx + 60, wy + 190, 70, 50)
                fill(ctx, INK, 0.85)
                for ex in (-14, 14):
                    ellipse(ctx, wx + 60 + ex, wy + 112, 9, 13)
                    fill(ctx, WHITE)
                ctx.restore()
            if nuestra:
                circle(ctx, wx + 60, wy + 120, 40)
                fill(ctx, hexc("#F08A3C"))
            ctx.move_to(wx + 60, wy)
            ctx.line_to(wx + 60, wy + 160)
            stroke(ctx, INK, 4, 0.5)
            k += 1
    # ondas del grito saliendo de nuestra ventana
    if ondas > 0:
        cx, cy = bx0 + 60 + 175 + 60, by0 + 80 + 2 * 245 + 80
        for i in range(4):
            r = 90 + ((T * 1.8 + i * 0.25) % 1) * 700
            ctx.arc(cx, cy, r, 0, 2 * math.pi)
            stroke(ctx, WHITE, 10, ondas * (1 - r / 790))
    # calle
    ctx.rectangle(-3000, 1700, W + 6000, 3000)
    fill(ctx, hexc("#2B2840"))
    ctx.rectangle(-3000, 1700, W + 6000, 40)
    fill(ctx, hexc("#5A5570"))
    rrect(ctx, 470, 1520, 140, 180, 10)  # portal
    fill_keep(ctx, hexc("#3E2A1F"))
    stroke(ctx, INK, 6)
    _glow(ctx, 540, 1500, 200, (1, 0.85, 0.5), 0.4)


# ---------------------------------------------------------------- escenario con foco
def escenario_foco(ctx, T, rgb=None):
    base = rgb or hexc("#2A1240")
    ctx.rectangle(-3000, -3000, W + 6000, 6000)
    fill(ctx, base)
    for side in (-1, 1):  # cortinas
        x0 = -200 if side < 0 else 1280
        ctx.move_to(x0, -400)
        for i in range(7):
            ctx.line_to(x0 - side * (60 + 300 * (i / 6)), -400 + i * 380)
        ctx.line_to(x0, 2400)
        ctx.close_path()
        fill_keep(ctx, hexc("#B3122E"))
        stroke(ctx, INK, 7)
        for i in range(4):
            ctx.move_to(x0 - side * (40 + i * 70), -400)
            ctx.line_to(x0 - side * (90 + i * 90), 2400)
        stroke(ctx, hexc("#7A0B1F"), 10, 0.7)
    ctx.rectangle(-3000, 1560, W + 6000, 3000)
    fill(ctx, hexc("#3B2213"))
    # foco
    ctx.move_to(470, -300)
    ctx.line_to(610, -300)
    ctx.line_to(900, 1640)
    ctx.line_to(180, 1640)
    ctx.close_path()
    ctx.set_source(_vga(-300, 1640, [(0, (1, 0.97, 0.8, 0.5)), (1, (1, 0.97, 0.8, 0.18))]))
    ctx.fill()
    ellipse(ctx, 540, 1640, 380, 70)
    fill(ctx, (1, 0.97, 0.8), 0.45)
