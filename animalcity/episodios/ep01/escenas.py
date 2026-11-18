from sitcom import *

# EP01 · "Never ask Nana for the Wi-Fi password"
# Planos: salón noche var0 · puerta var1 · ráfagas amarilla y rosa · pantalla de tablet a pantalla completa.

PASS = "TeddyStillSleepsWithANightlight"


def e1(ctx, lt, dur, T, L):  # GANCHO: primer plano de Teddy desesperado, ya hablando
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.2, 330, 1060)), (dur, (2.5, 330, 1080))])
    salon(ctx, T, var=0)
    nana(ctx, 900, 1420, 0.95, T, "smug", 0.0, gafas="puestas", typing=True)
    teddy(ctx, 330, 1560, 1.0, T, "panico", L.talk("teddy", T), arms="movil")
    ctx.restore()
    impacto(ctx, "NOW.", 300, 1250, 200, PJ["teddy"]["color"], pop(lt, 1.7, 0.25), T, 5)


def e2(ctx, lt, dur, T, L):  # Nana baja las gafas muy despacio
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.9, 900, 1000)), (dur, (2.15, 900, 980))])
    salon(ctx, T, var=0)
    nana(ctx, 900, 1420, 0.95, T, "smug", L.talk("nana", T), gafas="puestas" if lt < 0.35 else "bajadas", prop="tablet")
    ctx.restore()


def e3(ctx, lt, dur, T, L):  # PLEASE! en ráfaga
    ctx.save()
    dx, dy = shake(T, 10)
    zoom_cam(ctx, lt, [(0, (1.5, 540 + dx, 1100 + dy)), (dur, (1.65, 540 + dx, 1100 + dy))])
    rafaga(ctx, T, var=0)
    teddy(ctx, 540, 1650, 1.25, T, "panico", L.talk("teddy", T), arms="arriba", bounce=False)
    ctx.restore()
    impacto(ctx, "PLEASE.", 540, 560, 210, WHITE, pop(lt, 0.05, 0.2), T, 8)


def e4(ctx, lt, dur, T, L):  # Nana teclea rapidísimo: la contraseña aparece en la tablet
    if lt < 2.4:
        ctx.save()
        zoom_cam(ctx, lt, [(0, (2.0, 900, 1250)), (2.4, (2.4, 900, 1280))])
        salon(ctx, T, var=0)
        nana(ctx, 900, 1420, 0.95, T, "smug", L.talk("nana", T), gafas="bajadas", typing=True)
        ctx.restore()
        return
    # pantalla de la tablet a pantalla completa
    ctx.rectangle(0, 0, W, H)
    fill(ctx, (0.08, 0.07, 0.12))
    k = keyframes(lt, [(2.4, 0.92), (dur, 1.0)])
    ctx.save()
    ctx.translate(W / 2, H / 2)
    ctx.scale(k, k)
    rrect(ctx, -480, -330, 960, 660, 50)
    fill_keep(ctx, (0.15, 0.14, 0.2))
    stroke(ctx, INK, 10)
    rrect(ctx, -430, -280, 860, 560, 24)
    fill(ctx, hexc("#E9F4FF"))
    text(ctx, "Wi-Fi password", 0, -190, 46, (0.35, 0.4, 0.55), shadow=False)
    n = int(clamp((lt - 2.5) / 1.6) * len(PASS))
    shown = PASS[:n]
    rrect(ctx, -390, -110, 780, 230, 20)
    fill_keep(ctx, WHITE)
    stroke(ctx, hexc("#5EB8F2"), 6)
    text(ctx, shown[:16], 0, -40, 60, INK, shadow=False)
    text(ctx, shown[16:], 0, 50, 60, INK, shadow=False)
    if n >= len(PASS):
        badge(ctx, "SAVED", 0, 200, pop(lt, 4.2, 0.3), 48, hexc("#7CE38B"), INK)
    ctx.restore()


def e5(ctx, lt, dur, T, L):  # Moe escupe el zumo en el sofá
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.3, 420, 1180)), (dur, (2.1, 420, 1200))])
    salon(ctx, T, var=0)
    moe(ctx, 420, 1400, 0.9, T, "sorpresa" if lt < 0.6 else "panico", L.talk("moe", T), arms="taza")
    for k in range(14):  # espurreo
        p = clamp((lt - 0.05) / 0.5)
        if 0 < p < 1:
            a = -0.6 + k * 0.09
            circle(ctx, 450 + math.cos(a) * 320 * p, 1060 + math.sin(a) * 120 * p + 200 * p * p, 9 * (1 - p) + 3)
            fill(ctx, hexc("#FF9F43"), 1 - p)
    ctx.restore()


def e6(ctx, lt, dur, T, L):  # Teddy susurra con rabia; suena el timbre
    ctx.save()
    sx, sy = shake(T, 7) if lt > dur - 0.5 else (0, 0)
    zoom_cam(ctx, lt, [(0, (2.6, 330 + sx, 1090 + sy)), (dur, (2.8, 330 + sx, 1100 + sy))])
    salon(ctx, T, var=0, noche=True)
    teddy(ctx, 330, 1560, 1.0, T, "enfado", L.talk("teddy", T), arms="abajo", look=(0.6, 0))
    ctx.restore()


def e7(ctx, lt, dur, T, L):  # Puerta: Mia, simpática, con el móvil
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.15, 540, 1000)), (dur, (1.3, 560, 1020))])
    puerta(ctx, T, var=1, abierta=ease(lt / 0.5))
    mia(ctx, 560, 1520, 1.0, T, "feliz", L.talk("mia", T), arms="movil")
    ctx.restore()


def e8(ctx, lt, dur, T, L):  # Teddy congelado: mira a Nana... y lo dice entre dientes
    ctx.save()
    if lt < 0.6:  # mirada a Nana
        zoom_cam(ctx, lt, [(0, (2.6, 900, 1000)), (0.6, (2.9, 900, 990))])
        salon(ctx, T, var=0)
        nana(ctx, 900, 1420, 0.95, T, "smug", 0, gafas="bajadas", look=(-0.6, 0))
    else:
        zoom_cam(ctx, lt, [(0.6, (1.2, 500, 1050)), (dur, (1.3, 470, 1060))])
        puerta(ctx, T, var=1, abierta=1.0)
        mia(ctx, 700, 1520, 0.95, T, "normal", 0, arms="movil")
        teddy(ctx, 260, 1620, 0.95, T, "cansado", L.talk("teddy", T), arms="abajo", look=(1, 0), bounce=False)
    ctx.restore()


def e9(ctx, lt, dur, T, L):  # "Sorry?"
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.2, 560, 1090)), (dur, (2.35, 560, 1090))])
    puerta(ctx, T, var=1, abierta=1.0)
    ctx.translate(560, 1100)
    ctx.rotate(0.12)
    ctx.translate(-560, -1100)
    mia(ctx, 560, 1520, 1.0, T, "sospecha", L.talk("mia", T), arms="movil")
    ctx.restore()


def e10(ctx, lt, dur, T, L):  # EL GRITO
    ctx.save()
    dx, dy = shake(T, 12)
    zoom_cam(ctx, lt, [(0, (1.4, 540 + dx, 1150 + dy)), (dur, (1.7, 540 + dx, 1100 + dy))])
    rafaga(ctx, T, var=1)
    teddy(ctx, 540, 1650, 1.25, T, "panico", L.talk("teddy", T), arms="arriba", bounce=False)
    ctx.restore()
    impacto(ctx, "TEDDY STILL SLEEPS", 540, 470, 112, WHITE, pop(lt, 0.0, 0.2), T, 7)
    impacto(ctx, "WITH A NIGHTLIGHT!", 540, 600, 112, hexc("#FFD23F"), pop(lt, 0.9, 0.2), T, 7)


def e11(ctx, lt, dur, T, L):  # Mia teclea... incorrecto
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.5, 560, 1100)), (dur, (1.7, 560, 1080))])
    puerta(ctx, T, var=1, abierta=1.0)
    mia(ctx, 560, 1520, 1.0, T, "sospecha", L.talk("mia", T), arms="movil")
    ctx.restore()
    badge(ctx, "INCORRECT", 540, 1150, pop(lt, 1.25, 0.25), 70, hexc("#FF5A5A"))


def e12(ctx, lt, dur, T, L):  # Nana, sin levantar la vista
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.5, 900, 1000)), (dur, (2.7, 900, 990))])
    salon(ctx, T, var=0)
    nana(ctx, 900, 1420, 0.95, T, "smug", L.talk("nana", T), gafas="puestas", typing=True)
    ctx.restore()


def e13(ctx, lt, dur, T, L):  # Mia lee la tablet de Nana: conectada, choque de puños
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.35, 760, 1080)), (dur, (1.45, 760, 1060))])
    salon(ctx, T, var=0)
    nana(ctx, 900, 1420, 0.95, T, "feliz" if lt > 2.6 else "smug", 0, gafas="frente", screen_text="MiaCanDoBetter")
    mia(ctx, 560, 1560, 0.95, T, "feliz", L.talk("mia", T), arms="puno" if lt > 2.6 else "abajo", look=(0.8, 0.4))
    ctx.restore()
    badge(ctx, "CONNECTED", 540, 1180, pop(lt, 2.9, 0.25), 70, hexc("#7CE38B"), INK)


def e14(ctx, lt, dur, T, L):  # Teddy mira a cámara, derrotado... y vuelve a empezar (bucle)
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.3, 330, 1060)), (dur, (2.2, 330, 1060))])
    salon(ctx, T, var=0)
    teddy(ctx, 330, 1560, 1.0, T, "cansado", L.talk("teddy", T), arms="movil", look=(0, 0), bounce=False)
    ctx.restore()


ESCENAS = [(0.0, e1), (2.9, e2), (4.52, e3), (5.6, e4), (11.15, e5), (12.6, e6), (15.6, e7), (17.7, e8),
           (19.95, e9), (20.72, e10), (23.4, e11), (25.25, e12), (26.5, e13), (30.6, e14)]
SFX = [(1.7, "pop"), (3.3, "ding"), (4.55, "whoosh"), (5.7, "typing"), (11.2, "spit"), (15.15, "doorbell"),
       (17.7, "whoosh"), (20.75, "whoosh"), (23.2, "crickets"), (24.6, "typing"), (25.0, "error"), (29.4, "connect"),
       (29.6, "sting")]
COLA = 0.15
