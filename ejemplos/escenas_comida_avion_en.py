"""v05 (EN): Why airplane food tastes bland — cabin air + engine noise + the tomato juice twist."""
import math
from anim import *  # noqa

TOMATO = (0.90, 0.20, 0.16)
TOMATO_D = (0.66, 0.10, 0.10)
LEAF = (0.25, 0.70, 0.30)
ORANGE = (1.0, 0.55, 0.20)
SAND = (0.95, 0.76, 0.45)
SAND_D = (0.85, 0.60, 0.32)
TRAY = (0.80, 0.82, 0.88)
CANDY = (1.0, 0.45, 0.75)


def bg_warm(ctx, T):
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, (0.20, 0.08, 0.18)), (1, (0.08, 0.05, 0.14))]))
    ctx.paint()
    bg_grid(ctx, 90, 0.04)


def tray(ctx, x, y, s, T, steam=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    soft_shadow(ctx, 0, 230, 420, 50, 0.35)
    rrect(ctx, -400, -230, 800, 460, 50)
    ctx.set_source(vgrad(ctx, 0, -230, 0, 230, [(0, (0.86, 0.88, 0.93)), (1, (0.68, 0.70, 0.78))]))
    ctx.fill()
    # main dish
    rrect(ctx, -360, -180, 420, 360, 40)
    fill(ctx, WHITE)
    ellipse(ctx, -150, 0, 150, 110)
    fill(ctx, (0.85, 0.75, 0.55))
    for k in range(5):
        circle(ctx, -230 + k * 40, -30 + (k % 2) * 40, 26)
        fill(ctx, (0.45, 0.65, 0.30))
    ellipse(ctx, -80, 40, 70, 45)
    fill(ctx, (0.65, 0.40, 0.25))
    # bread roll + cup
    ellipse(ctx, 200, -110, 110, 70)
    fill(ctx, (0.88, 0.66, 0.38))
    circle(ctx, 210, 90, 90)
    fill(ctx, WHITE)
    circle(ctx, 210, 90, 70)
    fill(ctx, (0.45, 0.28, 0.18))
    # steam
    for k in range(3):
        ph = T * 1.6 + k * 2.1
        xx = -200 + k * 70
        ctx.move_to(xx, -200)
        ctx.curve_to(xx + 30 * math.sin(ph), -260, xx - 30 * math.sin(ph), -320, xx + 10, -380 - 20 * math.sin(ph))
        stroke(ctx, WHITE, 12, 0.45 * steam)
    ctx.restore()


def glass(ctx, x, y, s, level=1.0, liquid=TOMATO, mystery=False, glow=0.0, T=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 40, 0, 0, 360)
        g.add_color_stop_rgba(0, 1.0, 0.45, 0.30, 0.55 * glow)
        g.add_color_stop_rgba(1, 1.0, 0.45, 0.30, 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, 360)
        ctx.fill()
    soft_shadow(ctx, 0, 250, 170, 30, 0.35)
    # liquid
    top = 230 - 430 * level
    ctx.save()
    ctx.move_to(-150, -200)
    ctx.line_to(150, -200)
    ctx.line_to(115, 240)
    ctx.line_to(-115, 240)
    ctx.close_path()
    ctx.clip()
    if mystery:
        ctx.set_source(vgrad(ctx, 0, -200, 0, 240, [(0, (0.25, 0.25, 0.40)), (1, (0.12, 0.12, 0.25))]))
        ctx.paint()
    else:
        ctx.rectangle(-200, top, 400, 600)
        ctx.set_source(vgrad(ctx, 0, top, 0, 240, [(0, liquid), (1, tuple(c * 0.7 for c in liquid))]))
        ctx.fill()
    ctx.restore()
    # glass outline + shine
    ctx.move_to(-150, -200)
    ctx.line_to(-115, 240)
    ctx.line_to(115, 240)
    ctx.line_to(150, -200)
    stroke(ctx, WHITE, 12, 0.85)
    rrect(ctx, -110, -150, 22, 300, 11)
    fill(ctx, WHITE, 0.25)
    if mystery:
        text(ctx, "?", 0, 20, 220, YELLOW, font=FONT_TITLE)
    elif level > 0.5:
        # celery stick
        ctx.save()
        ctx.rotate(0.25)
        rrect(ctx, 30, -360, 34, 330, 17)
        fill(ctx, LEAF)
        ctx.restore()
    ctx.restore()


def tomato(ctx, x, y, r, T=0.0):
    soft_shadow(ctx, x, y + r * 0.95, r * 0.9, r * 0.18, 0.3)
    circle(ctx, x, y, r)
    g = cairo.RadialGradient(x - r * 0.35, y - r * 0.35, r * 0.1, x, y, r)
    g.add_color_stop_rgb(0, 1.0, 0.45, 0.35)
    g.add_color_stop_rgb(1, *TOMATO_D)
    ctx.set_source(g)
    ctx.fill()
    for k in range(5):
        a = k * 2 * math.pi / 5 - math.pi / 2
        ctx.move_to(x, y - r * 0.92)
        ctx.line_to(x + r * 0.42 * math.cos(a), y - r * 0.92 + r * 0.22 * math.sin(a))
        stroke(ctx, LEAF, r * 0.12)
    ellipse(ctx, x - r * 0.38, y - r * 0.38, r * 0.16, r * 0.10)
    fill(ctx, WHITE, 0.6)


def candy(ctx, x, y, r, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    for sx in (-1, 1):
        ctx.move_to(sx * r * 0.8, 0)
        ctx.line_to(sx * r * 1.6, -r * 0.55)
        ctx.line_to(sx * r * 1.6, r * 0.55)
        ctx.close_path()
        fill(ctx, (0.95, 0.70, 0.90))
    circle(ctx, 0, 0, r)
    fill(ctx, CANDY)
    for k in range(3):
        ctx.move_to(-r * 0.6 + k * r * 0.5, -r * 0.8)
        ctx.line_to(-r * 0.2 + k * r * 0.5, r * 0.8)
        stroke(ctx, WHITE, r * 0.12, 0.7)
    ctx.restore()


def cross(ctx, x, y, r, a=1.0, rgb=RED):
    if a <= 0.01:
        return
    ctx.move_to(x - r, y - r)
    ctx.line_to(x + r, y + r)
    ctx.move_to(x + r, y - r)
    ctx.line_to(x - r, y + r)
    stroke(ctx, rgb, r * 0.35, a)


def check(ctx, x, y, r, a=1.0, rgb=GREEN):
    if a <= 0.01:
        return
    ctx.move_to(x - r, y)
    ctx.line_to(x - r * 0.3, y + r * 0.7)
    ctx.line_to(x + r, y - r * 0.7)
    stroke(ctx, rgb, r * 0.35, a)


def fuselage(ctx, x, y, r, T, dry=1.0):
    """Corte del fuselaje: dentro hay un desierto."""
    ctx.save()
    circle(ctx, x, y, r)
    ctx.clip()
    ctx.set_source(vgrad(ctx, 0, y - r, 0, y + r, [(0, (1.0, 0.72, 0.40)), (1, (1.0, 0.88, 0.60))]))
    ctx.paint()
    sun(ctx, x + r * 0.45, y - r * 0.40, 70, T, a=dry)
    for k, (yy, col) in enumerate(((y + r * 0.30, SAND), (y + r * 0.50, SAND_D))):
        ctx.move_to(x - r - 50, yy)
        for i in range(9):
            xx = x - r + i * r / 4
            ctx.curve_to(xx + r / 12, yy - 60 + 20 * k, xx + r / 6, yy - 60 + 20 * k, xx + r / 4, yy)
        ctx.line_to(x + r + 50, y + r + 50)
        ctx.line_to(x - r - 50, y + r + 50)
        ctx.close_path()
        fill(ctx, col)
    # cactus
    cx0, cy0 = x - r * 0.45, y + r * 0.32
    rrect(ctx, cx0 - 22, cy0 - 200, 44, 200, 22)
    rrect(ctx, cx0 - 80, cy0 - 140, 30, 80, 15)
    rrect(ctx, cx0 + 50, cy0 - 170, 30, 80, 15)
    rrect(ctx, cx0 - 80, cy0 - 80, 80, 28, 14)
    rrect(ctx, cx0, cy0 - 110, 80, 28, 14)
    fill(ctx, (0.30, 0.65, 0.35))
    ctx.restore()
    # skin of the plane
    circle(ctx, x, y, r)
    stroke(ctx, (0.92, 0.93, 0.97), 46)
    circle(ctx, x, y, r + 23)
    stroke(ctx, (0.55, 0.58, 0.70), 6)
    # seats silhouettes at the floor
    for k in range(3):
        rrect(ctx, x - 200 + k * 140, y + r * 0.55, 100, 140, 24)
        fill(ctx, (0.24, 0.36, 0.78))


def bars(ctx, x, y, drop, T, appear=1.0):
    labels = [("SALTY", (0.85, 0.88, 0.95)), ("SWEET", CANDY)]
    for i, (lab, col) in enumerate(labels):
        bx = x + (i - 0.5) * 300
        full = 560
        h = full * (1 - 0.30 * drop) * appear
        rrect(ctx, bx - 100, y - full, 200, full, 24)
        fill(ctx, WHITE, 0.08)
        ctx.set_dash([18, 14])
        ctx.move_to(bx - 110, y - full)
        ctx.line_to(bx + 110, y - full)
        stroke(ctx, WHITE, 5, 0.5 * drop)
        ctx.set_dash([])
        rrect(ctx, bx - 100, y - h, 200, h, 24)
        ctx.set_source(vgrad(ctx, 0, y - h, 0, y, [(0, col), (1, tuple(c * 0.65 for c in col))]))
        ctx.fill()
        text(ctx, lab, bx, y + 60, 54, WHITE, font=FONT_TITLE)


def engine(ctx, x, y, r, T, waves=1.0):
    # sound waves
    for k in range(4):
        ph = (T * 0.9 + k * 0.25) % 1.0
        rr = r * 1.05 + ph * 520
        ctx.new_sub_path()
        ctx.arc(x, y, rr, -0.7, 0.7)
        stroke(ctx, YELLOW, 12, (1 - ph) * 0.8 * waves)
        ctx.new_sub_path()
        ctx.arc(x, y, rr, math.pi - 0.7, math.pi + 0.7)
        stroke(ctx, YELLOW, 12, (1 - ph) * 0.8 * waves)
    circle(ctx, x, y, r)
    ctx.set_source(vgrad(ctx, 0, y - r, 0, y + r, [(0, (0.85, 0.87, 0.93)), (1, (0.55, 0.58, 0.68))]))
    ctx.fill()
    circle(ctx, x, y, r * 0.82)
    fill(ctx, (0.10, 0.11, 0.18))
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(T * 9)
    for k in range(14):
        ctx.rotate(2 * math.pi / 14)
        ctx.move_to(0, 0)
        ctx.curve_to(r * 0.25, -r * 0.1, r * 0.6, -r * 0.05, r * 0.78, r * 0.12)
        ctx.line_to(r * 0.75, r * 0.25)
        ctx.curve_to(r * 0.5, r * 0.15, r * 0.2, r * 0.1, 0, 0)
        fill(ctx, (0.65, 0.68, 0.78))
    ctx.restore()
    circle(ctx, x, y, r * 0.16)
    fill(ctx, (0.90, 0.92, 0.97))


def red_nose(ctx, x, y, s):
    circle(ctx, x, y + 40 * s, 30 * s)
    fill(ctx, (0.95, 0.30, 0.30))
    circle(ctx, x - 8 * s, y + 30 * s, 9 * s)
    fill(ctx, WHITE, 0.6)


# ---------------- escenas ----------------
# 0.0 HOOK "Airline food isn't that bad. At thirty-five thousand feet, you taste like you have a cold."
def e1(ctx, lt, dur, T):
    punch = keyframes(lt, [(0, 1.45), (0.35, 1.0), (dur, 1.12)])
    camera(ctx, punch, W / 2, keyframes(lt, [(0, 900), (dur, 960)]))
    bg_sky(ctx, T)
    for k in range(4):
        x = (k * 330 - T * 160) % 1600 - 260
        for dx, rr in ((0, 80), (70, 110), (150, 75)):
            circle(ctx, x + dx, 380 + k * 90, rr)
        fill(ctx, WHITE, 0.7)
    tray(ctx, W / 2, 1040, 0.82, T)
    character(ctx, W / 2, 640, 0.75, T, mood="duda" if lt < 2.0 else "sorpresa", body=False)
    if lt > 2.1:
        red_nose(ctx, W / 2, 640, 0.75 * pop(lt, 2.1))
    pill(ctx, "35,000 FT", 250, 330, pop(lt, 2.3), rgb=YELLOW)
    badge(ctx, "LIKE A COLD", 790, 330, pop(lt, 4.3), size=54)
    icon(ctx, "🤧", 880, 820, 170, pop(lt, 4.4))


# 5.35 LOOP "Stay to the end for the one drink that actually tastes better up there."
def e2(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.25), (dur, 1.0)]), W / 2, 920, rot=0.02 * math.sin(T * 2))
    bg_warm(ctx, T)
    for k in range(10):
        a = T * 0.6 + k * 0.63
        circle(ctx, W / 2 + 420 * math.cos(a), 900 + 420 * math.sin(a), 10)
        fill(ctx, YELLOW, 0.5)
    glass(ctx, W / 2, 920, 1.25, mystery=True, glow=0.6 + 0.4 * math.sin(T * 4), T=T)
    pill(ctx, "ONE DRINK WINS", W / 2, 330, pop(lt, 1.2), rgb=ORANGE)


# 9.12 PROBLEMA "Cabin air is drier than most deserts. It dries out your nose."
def e3(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 0.9), (dur, 1.05)]), W / 2, 930)
    bg_blueprint(ctx, T)
    fuselage(ctx, W / 2, 900, 430, T)
    hum = counter(lt, 40, 12, 1.6)
    pill(ctx, hum + "% HUMIDITY", W / 2, 300, pop(lt, 0.3), rgb=SAND)
    badge(ctx, "DRIER THAN A DESERT", W / 2, 1420 - 60, pop(lt, 1.5), size=50)


# 13.19 "And no smell means almost no flavor."
def e4(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.2)]), W / 2, 860)
    bg_warm(ctx, T)
    character(ctx, W / 2, 780, 1.05, T, mood="duda", body=True, shirt=(0.85, 0.35, 0.30))
    red_nose(ctx, W / 2, 780, 1.05)
    # smell waves fading before reaching the nose
    for k in range(4):
        ph = (T * 0.8 + k * 0.25) % 1.0
        xx = lerp(980, 640, ph)
        ctx.move_to(xx, 760 + k * 22)
        ctx.curve_to(xx - 40, 720, xx - 80, 820, xx - 120, 770)
        stroke(ctx, (0.75, 0.90, 0.60), 10, (1 - ph) * 0.9 * clamp(1.6 - lt))
    icon(ctx, "👃", 230, 520, 160, pop(lt, 0.2))
    cross(ctx, 230, 520, 70, pop(lt, 0.7))
    pill(ctx, "NO SMELL = NO FLAVOR", W / 2, 330, pop(lt, 1.0), rgb=GREEN)


# 15.88 DATO "In a Lufthansa study, salty and sweet dropped up to thirty percent. That's why airlines add extra salt."
def e5(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    bg_dark(ctx, T)
    drop = ease((lt - 1.8) / 1.4)
    bars(ctx, W / 2, 1180, drop, T, ease_out(lt / 0.6))
    if drop > 0.6:
        badge(ctx, "-30%", W / 2, 470, pop(lt, 3.0), size=110)
    pill(ctx, "LAB STUDY · 2010", W / 2, 300, pop(lt, 0.2), rgb=YELLOW)
    # salt shaker pouring at the end
    a = pop(lt, 4.6)
    if a > 0.01:
        ctx.save()
        ctx.translate(860, 760)
        ctx.rotate(2.5)
        ctx.scale(a, a)
        rrect(ctx, -60, -110, 120, 220, 40)
        fill(ctx, WHITE)
        rrect(ctx, -60, -150, 120, 60, 24)
        fill(ctx, (0.7, 0.72, 0.8))
        ctx.restore()
        for k in range(10):
            yy = 760 + ((T * 400 + k * 47) % 300)
            circle(ctx, 900 + (k % 3) * 18, yy, 6)
            fill(ctx, WHITE, 0.9)
        pill(ctx, "EXTRA SALT", 820, 600, a, size=40, rgb=WHITE)


# 22.18 GIRO "But here's the crazy part... the engine noise. It mutes sweetness even more."
def e6(ctx, lt, dur, T):
    sx, sy = shake(T, 5 * clamp((lt - 1.7) * 2))
    camera(ctx, keyframes(lt, [(0, 1.3), (1.8, 1.0), (dur, 1.05)]), W / 2 + sx, 900 + sy)
    bg_night(ctx, T, stars=False)
    engine(ctx, W / 2, 740, 290, T, waves=clamp((lt - 1.6) * 2))
    digital_clock(ctx, counter(lt - 1.8, 0, 85, 1.0) + " dB", W / 2, 300, 0.85, pop(lt, 1.8), rgb=YELLOW)
    shrink = 1 - 0.6 * ease((lt - 4.2) / 1.0)
    candy(ctx, W / 2, 1160, 80 * shrink * pop(lt, 4.0), rot=0.3 * math.sin(T * 3))
    cross(ctx, W / 2, 1160, 90, ease((lt - 4.9) / 0.3))


# 27.38 "Yet it boosts one taste: umami. Savory."
def e7(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.0), (dur, 1.18)]), W / 2, 900)
    bg_warm(ctx, T)
    grow = ease_back((lt - 1.4) / 0.6)
    for k in range(12):
        a = k * math.pi / 6 + T * 0.4
        ctx.move_to(W / 2 + 260 * math.cos(a), 900 + 260 * math.sin(a))
        ctx.line_to(W / 2 + 420 * math.cos(a), 900 + 420 * math.sin(a))
        stroke(ctx, YELLOW, 14, 0.5 * clamp(grow))
    tomato(ctx, W / 2, 900, lerp(110, 230, clamp(grow)), T)
    badge(ctx, "UMAMI", W / 2, 330, pop(lt, 1.6), size=90, bg=TOMATO)
    pill(ctx, "SAVORY", W / 2, 1300, pop(lt, 3.0), rgb=TOMATO)


# 30.92 "That's why people order tomato juice on planes... and never on the ground."
def e8(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.1), (dur, 1.0)]), W / 2, 960)
    # sky half
    ctx.rectangle(0, 0, W, 960)
    ctx.set_source(vgrad(ctx, 0, 0, 0, 960, [(0, (0.30, 0.55, 0.95)), (1, (0.70, 0.85, 1.0))]))
    ctx.fill()
    # ground half
    ctx.rectangle(0, 960, W, H)
    ctx.set_source(vgrad(ctx, 0, 960, 0, H, [(0, (0.35, 0.65, 0.40)), (1, (0.20, 0.42, 0.28))]))
    ctx.fill()
    ctx.move_to(0, 960)
    ctx.line_to(W, 960)
    stroke(ctx, WHITE, 8)
    icon(ctx, "✈️", 250, 300 + 20 * math.sin(T * 2), 220, pop(lt, 0.1), rot=-0.2)
    glass(ctx, 700, 560, 0.75, level=1.0, glow=0.7, T=T)
    check(ctx, 900, 380, 60, ease((lt - 0.8) / 0.3))
    icon(ctx, "🏠", 250, 1170, 200, pop(lt, 2.4))
    glass(ctx, 700, 1150, 0.55, level=ease_out((lt - 2.6) / 0.4), T=T)
    cross(ctx, 900, 1010, 60, ease((lt - 3.6) / 0.3))
    pill(ctx, "UP THERE", 700, 870, pop(lt, 0.6), size=40, rgb=GREEN)


# 34.92 CONSEJO "So next flight, skip the sweet stuff. Go tomato juice and savory dishes."
def e9(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 880)
    bg_dark(ctx, T)
    # drinks cart
    rrect(ctx, 180, 900, 720, 330, 30)
    ctx.set_source(vgrad(ctx, 0, 900, 0, 1230, [(0, (0.85, 0.86, 0.92)), (1, (0.60, 0.62, 0.72))]))
    ctx.fill()
    for k in range(3):
        rrect(ctx, 210, 940 + k * 95, 660, 14, 7)
        fill(ctx, (0.50, 0.52, 0.62))
    for wx in (260, 820):
        circle(ctx, wx, 1255, 34)
        fill(ctx, (0.15, 0.15, 0.20))
    icon(ctx, "🍰", 330, 760, 200, pop(lt, 0.3))
    cross(ctx, 330, 760, 90, ease((lt - 1.4) / 0.3))
    glass(ctx, 720, 700, 0.6, level=1.0, glow=ease((lt - 2.3) / 0.5), T=T)
    check(ctx, 900, 540, 60, ease((lt - 2.5) / 0.3))
    badge(ctx, "ORDER THIS", W / 2, 360, pop(lt, 2.4), size=66, bg=TOMATO)


# 39.42 CTA "Do you drink tomato juice up there? Follow for more hidden reasons behind everyday things."
def e10(ctx, lt, dur, T):
    camera(ctx, keyframes(lt, [(0, 1.15), (dur, 1.0)]), W / 2, 960)
    bg_sky(ctx, T, warm=0.7)
    icon(ctx, "✈️", (T * 180) % 1500 - 200, 300, 160, 1.0, rot=0.1)
    character(ctx, 420, 800, 0.85, T, mood="feliz", wave=1.0, shirt=(0.85, 0.35, 0.30))
    glass(ctx, 820, 960, 0.55, level=1.0, T=T)
    icon(ctx, "💬", 820, 600, 190, pop(lt, 0.3), rot=-0.12)
    pill(ctx, "DID YOU KNOW?", W / 2, 330, pop(lt, 0.2), rgb=ORANGE)
    badge(ctx, "FOLLOW", W / 2, 1250, pop(lt, 1.6), size=72)


ESCENAS = [(0.0, e1), (5.35, e2), (9.12, e3), (13.19, e4), (15.88, e5), (22.18, e6), (27.38, e7),
           (30.92, e8), (34.92, e9), (39.42, e10)]
PALABRAS_POR_SUBTITULO = 2
SFX = [(2.3, "pop"), (4.3, "pop"), (18.9, "ding"), (29.4, "ding"), (37.4, "pop")]
