from sitcom import *

# EP01 · "Never ask Nana for the Wi-Fi password" (versión cartoon para todos los públicos)
# Ambientes: rincón de Nana con chimenea · escenario con foco · móvil a pantalla completa · cocina de noche ·
# pasillo con timbre · puerta abierta a la calle de noche · ráfaga · edificio de noche · salón gris con nube de lluvia.
# Personajes: dibujos oficiales (assets/personajes) como muñecos articulados (pipeline/rig.py): brazos, piernas, cola,
# orejas y boca se mueven por separado; además squash & stretch, estelas, saltos y "takes".
# Los tiempos van por líneas del diálogo ("L6" = empieza la línea 6), así se recolocan solos si cambia el audio.

PASS = "TeddyStillSleepsWithANightlight"
NANA = (800, 1545, 1.0)  # pies de Nana en su rincón


def e1(ctx, lt, dur, T, L):  # GANCHO: Teddy entra disparado en el rincón de Nana
    dx, sq, vel = entrada(lt, -0.1, 0.3, -1000)
    jy, jsq = salto(lt, 1.95, 0.32, 120)
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.55, 470, 1170)), (dur, (1.85, 420, 1130))])
    rincon_nana(ctx, T)
    nana(ctx, *NANA, T, "smug", 0.0, typing=True)
    lineas_velocidad(ctx, 0, 900, 900, 600, 1, T, 12, WHITE, 0.8 * clamp(1 - (lt - 0.1) / 0.25))
    teddy(ctx, 330, 1610, 1.0, T, "panico", L.boca("teddy", T), arms="movil", dx=dx, dy=jy, sq=sq * jsq,
          smear=vel, lean=0.08 * clamp(1 - lt / 0.6), gesto="correr" if lt < 0.3 else "agitar",
          ene=L.energia("teddy", T))
    polvo(ctx, 330, 1610, (lt - 0.18) / 0.5)
    ctx.restore()
    ambiente(ctx, "calida")
    if lt > 1.9:
        lineas_foco(ctx, W / 2, H * 0.45, T, 0.35 * clamp(1 - (lt - 1.95) / 0.5))


def e2(ctx, lt, dur, T, L):  # Nana, despacito: "Say please."
    hx, hy = cabeza("nana", *NANA)
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.2, hx + 30, hy + 120)), (dur, (2.55, hx + 20, hy + 100))])
    rincon_nana(ctx, T)
    o = nana(ctx, *NANA, T, "smug", L.boca("nana", T), lean=-0.03 * smooth(lt / 0.6))
    ctx.restore()
    # brillo en las gafas
    p = clamp((lt - 0.35) / 0.5)
    if 0 < p < 1:
        k = math.sin(math.pi * p)
        destello(ctx, W * 0.42, H * 0.37, 70 * k, WHITE, k)
    ambiente(ctx, "calida")


def e3(ctx, lt, dur, T, L):  # "PLEASE!" en el escenario con foco, suplicando
    dy, sq = toma(lt, 0.05, 0.9)
    sx, sy = temblor(T, 5 * clamp(lt - 0.2))
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.35, 540 + sx, 1150 + sy)), (dur, (1.55, 540 + sx, 1130 + sy))])
    escenario_foco(ctx, T, hexc("#3A1550"))
    destellos(ctx, 150, 500, 780, 900, T, 16, hexc("#FFE6F2"), 1, 3, 30)
    teddy(ctx, 540, 1640, 1.1, T, "triste", L.boca("teddy", T), bounce=False, dy=dy, sq=sq,
          blush=0.7, head_dy=-40, lean=0.03 * math.sin(T * 9), gesto="suplicar", rot=0)
    ctx.restore()
    corazones(ctx, 540, 620, T, 5, 1.2, hexc("#FF7AB6"))
    ambiente(ctx, "rosa", 0.8)


def e4(ctx, lt, dur, T, L):  # Nana teclea rapidísimo... y la contraseña aparece en su móvil
    if lt < 1.6:
        hx, hy = cabeza("nana", *NANA)
        ctx.save()
        zoom_cam(ctx, lt, [(0, (1.7, 700, 1260)), (1.6, (2.3, 640, 1300))])
        rincon_nana(ctx, T)
        nana(ctx, *NANA, T, "smug", L.boca("nana", T), typing=True, nod=0.01 * math.sin(T * 40))
        ctx.restore()
        ambiente(ctx, "calida")
        return
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hexc("#2A1B3D")), (1, hexc("#120C1E"))]))
    ctx.fill()
    destellos(ctx, 0, 0, W, H, T, 18, hexc("#B07CE8"), 0.6, 9, 22)
    k = e_back(clamp((lt - 1.6) / 0.35))
    ctx.save()
    ctx.translate(W / 2, H / 2 - 40)
    ctx.rotate(0.03 * math.sin(T * 2))
    ctx.scale(k * 0.84, k * 0.84)
    rrect(ctx, -380, -700, 760, 1400, 90)
    fill_keep(ctx, (0.15, 0.14, 0.2))
    stroke(ctx, INK, 12)
    rrect(ctx, -340, -650, 680, 1300, 64)
    fill(ctx, hexc("#E9F4FF"))
    text(ctx, "Wi-Fi password", 0, -400, 54, (0.35, 0.4, 0.55), shadow=False)
    n = int(clamp((lt - 1.9) / 1.7) * len(PASS))
    shown = PASS[:n]
    rrect(ctx, -300, -300, 600, 330, 26)
    fill_keep(ctx, WHITE)
    stroke(ctx, hexc("#5EB8F2"), 6)
    for i, part in enumerate((shown[:11], shown[11:21], shown[21:])):
        text(ctx, part, 0, -220 + i * 95, 64, INK, shadow=False)
    ctx.restore()
    if n >= len(PASS):
        estallido(ctx, W / 2, H / 2 + 120, 115, clamp((lt - 3.7) / 0.3), hexc("#7CE38B"), 14, T * 0.5)
        badge(ctx, "SAVED!", W / 2, H / 2 + 120, pop(lt, 3.7, 0.3), 64, hexc("#7CE38B"), INK)


def e5(ctx, lt, dur, T, L):  # Moe en la cocina: escupe el chocolate y "Oh no."
    t_esc = 0.15
    dy, sq = toma(lt, t_esc, 1.0)
    hx, hy = cabeza("moe", 540, 1600, 1.15)
    ctx.save()
    sx, sy = temblor(T, 6 * clamp(1 - (lt - t_esc) / 0.4)) if lt > t_esc else (0, 0)
    zoom_cam(ctx, lt, [(0, (1.95, hx + sx, hy + 260 + sy)), (dur, (2.15, hx + sx, hy + 230 + sy))])
    cocina_noche(ctx, T)
    if lt < t_esc:  # vapor de la taza
        vapor(ctx, 600, 1280, T, 0.6)
    moe(ctx, 540, 1600, 1.15, T, "sorpresa" if lt < 0.9 else "panico", L.boca("moe", T), dy=dy, sq=sq,
        gesto="sorber" if lt < t_esc - 0.02 else None)
    for i in range(22):  # espurreo de chocolate
        p = clamp((lt - t_esc) / 0.7)
        if 0 < p < 1:
            a = -1.25 + i * 0.11
            v = 520 + (i % 5) * 60
            circle(ctx, hx + 40 + math.cos(a) * v * p, hy + 120 + math.sin(a) * v * 0.6 * p + 500 * p * p, 11 * (1 - p) + 4)
            fill_keep(ctx, hexc("#7A4A2A"), 1 - p * 0.7)
            stroke(ctx, INK, 2, 1 - p)
    ctx.restore()
    if lt > 0.9:
        emote(ctx, "!", W * 0.7, H * 0.28, clamp((lt - 0.9) / 0.3), hexc("#FFD23F"), 170, T)
    ambiente(ctx, "noche", 0.45)


def e6(ctx, lt, dur, T, L):  # Pasillo: Teddy corre de un lado a otro con el pánico... y suena el timbre
    t_bell = L.lines[5]["fin"] - (T - lt)
    run = lt < t_bell - 0.1
    if run:
        cx, fl, vel = carrera(lt, 230, 1.6)
        dy, sq = 0.0, 1.0
    else:
        cx, fl, vel = 0.0, False, 0.0
        dy, sq = toma(lt, t_bell, 1.1)
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.2, 540, 1250)), (dur, (1.35, 540, 1200))])
    pasillo(ctx, T, timbre=clamp((lt - t_bell) / 0.1) if lt > t_bell else 0.0)
    teddy(ctx, 540, 1740, 1.0, T, "panico" if run else "sorpresa", L.boca("teddy", T), flip=fl, dx=cx,
          smear=vel * 3 if run else 0, dy=dy, sq=sq, bounce=False, gesto="correr" if run else "arriba",
          ene=L.energia("teddy", T))
    if run:
        polvo(ctx, 540 + cx, 1740, (lt * 1.6) % 1, 0.8, int(lt * 3))
    ctx.restore()
    if lt > t_bell:
        p = clamp((lt - t_bell) / 0.25)
        estallido(ctx, W * 0.66, H * 0.42, 190, p, hexc("#FFD23F"), 16, 0.2)
        impacto(ctx, "DING DONG!", W * 0.66, H * 0.42, 74, WHITE, e_back(p), T, 3, -0.12)


def e7(ctx, lt, dur, T, L):  # La puerta se abre: Mia, de noche, con el móvil
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.15, 540, 1080)), (dur, (1.4, 560, 1120))])
    entrada_noche(ctx, T, abierta=e_out(lt / 0.45))
    jy, jsq = salto(lt, 0.55, 0.3, 70)
    mia(ctx, 580, 1495, 0.92, T, "feliz", L.boca("mia", T), arms="movil", dy=jy, sq=jsq)
    ctx.restore()
    ambiente(ctx, "noche", 0.25)


def e8(ctx, lt, dur, T, L):  # Teddy mira a Nana (ella ni se inmuta)... y lo dice entre dientes, colorado
    if lt < 0.55:
        hx, hy = cabeza("nana", *NANA)
        ctx.save()
        zoom_cam(ctx, lt, [(0, (2.7, hx + 40, hy + 60)), (0.55, (2.9, hx + 40, hy + 50))])
        rincon_nana(ctx, T)
        nana(ctx, *NANA, T, "smug", 0, lean=-0.03)
        ctx.restore()
        destello(ctx, W * 0.4, H * 0.42, 60 * math.sin(math.pi * clamp(lt / 0.5)), WHITE)
        ambiente(ctx, "calida")
        return
    ctx.save()
    zoom_cam(ctx, lt, [(0.55, (1.35, 470, 1180)), (dur, (1.5, 440, 1190))])
    entrada_noche(ctx, T, abierta=1.0)
    mia(ctx, 720, 1495, 0.88, T, "normal", 0, arms="movil")
    teddy(ctx, 250, 1720, 1.05, T, "panico", L.boca("teddy", T), arms="abajo", bounce=False, blush=1.0,
          sq=0.93, head_dy=25, lean=-0.03, gesto="encoger")
    ctx.restore()
    ambiente(ctx, "noche", 0.2)


def e9(ctx, lt, dur, T, L):  # "Sorry?" — Mia se inclina para oír
    hx, hy = cabeza("mia", 600, 1495, 0.95)
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.0, hx, hy + 200)), (dur, (2.2, hx - 20, hy + 180))])
    entrada_noche(ctx, T, abierta=1.0)
    o = mia(ctx, 600, 1495, 0.95, T, "sospecha", L.boca("mia", T), arms="movil", lean=-0.09 * e_back(clamp(lt / 0.3)))
    ctx.restore()
    emote(ctx, "?", W * 0.68, H * 0.24, clamp((lt - 0.05) / 0.3), WHITE, 190, T)
    ambiente(ctx, "noche", 0.2)


def e10(ctx, lt, dur, T, L):  # EL GRITO... que se oye en todo el edificio
    corte = 1.15
    if lt < corte:
        dy, sq = toma(lt, 0.02, 1.2)
        sx, sy = temblor(T, 14)
        ctx.save()
        zoom_cam(ctx, lt, [(0, (1.35, 540 + sx, 1130 + sy)), (corte, (1.6, 540 + sx, 1090 + sy))])
        rafaga(ctx, T, var=1)
        teddy(ctx, 540, 1640, 1.2, T, "panico", L.boca("teddy", T), bounce=False, dy=dy, sq=sq, head_dy=-50,
              gesto="arriba", rot=0, pose={"brazo_i": 0.15 * math.sin(T * 17), "brazo_d": -0.15 * math.sin(T * 17 + 1)})
        ctx.restore()
        lineas_foco(ctx, W / 2, H * 0.4, T, 0.5)
        return
    p = clamp((lt - corte) / 1.0)
    ctx.save()
    sx, sy = temblor(T, 4)
    zoom_cam(ctx, lt, [(corte, (1.0, 540 + sx, 1000 + sy)), (dur, (0.92, 540 + sx, 980 + sy))])
    edificio(ctx, T, p, ondas=1 - p * 0.5)
    ctx.restore()
    ambiente(ctx, "noche", 0.15)


def e11(ctx, lt, dur, T, L):  # Silencio incómodo: grillos, planta rodadora... "Nope. Wrong password."
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.3, 560, 1150)), (dur, (1.5, 580, 1120))])
    entrada_noche(ctx, T, abierta=1.0)
    mia(ctx, 600, 1495, 0.95, T, "sospecha", L.boca("mia", T), arms="movil", lid=0.35)
    rodador(ctx, -250 + lt * 900, 1660, 90, T)
    ctx.restore()
    t_wrong = L.lines[10]["fin"] - (T - lt) - 0.3
    if lt > t_wrong:
        estallido(ctx, W * 0.66, H * 0.3, 190, clamp((lt - t_wrong) / 0.3), hexc("#FF5A5A"), 14, -0.1)
        badge(ctx, "WRONG!", W * 0.66, H * 0.3, pop(lt, t_wrong, 0.3), 100, hexc("#FF5A5A"))
    ambiente(ctx, "noche", 0.3)


def e12(ctx, lt, dur, T, L):  # Nana, sin levantar la vista: "I changed it."
    hx, hy = cabeza("nana", *NANA)
    ctx.save()
    zoom_cam(ctx, lt, [(0, (2.5, hx + 20, hy + 110)), (dur, (2.8, hx + 20, hy + 90))])
    rincon_nana(ctx, T, var=0)
    nana(ctx, *NANA, T, "smug", L.boca("nana", T), typing=True, lean=-0.04)
    ctx.restore()
    p = clamp((lt - 0.65) / 0.5)
    destello(ctx, W * 0.42, H * 0.37, 80 * math.sin(math.pi * p), WHITE, math.sin(math.pi * p))
    destellos(ctx, 80, 200, 920, 600, T, 8, hexc("#FFE24A"), 0.9, 15, 30)
    ambiente(ctx, "calida")


def e13(ctx, lt, dur, T, L):  # Mia lee el móvil de Nana: "Nana Is The Best"... ¡conectada! Fiesta.
    t_ok = L.lines[12]["fin"] - (T - lt) - 0.9
    fiesta = lt > t_ok
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.35, 600, 1180)), (dur, (1.45, 600, 1160))])
    rincon_nana(ctx, T, var=0)
    jy, jsq = salto(lt, t_ok + 0.05, 0.38, 150)
    nana(ctx, *NANA, T, "feliz" if fiesta else "smug", 0.0, screen_text="NanaIsTheBest")
    mia(ctx, 400, 1585, 0.95, T, "feliz", L.boca("mia", T), arms="cruzados", dy=jy, sq=jsq)
    ctx.restore()
    k = pop(lt, 0.3, 0.3)
    if k > 0 and not fiesta:  # inserto del móvil
        ctx.save()
        ctx.translate(W * 0.5, H * 0.24)
        ctx.rotate(-0.05 + 0.02 * math.sin(T * 3))
        ctx.scale(k * 0.85, k * 0.85)
        rrect(ctx, -190, -320, 380, 640, 54)
        fill_keep(ctx, (0.15, 0.14, 0.2))
        stroke(ctx, INK, 10)
        rrect(ctx, -165, -292, 330, 584, 36)
        fill(ctx, hexc("#E9F4FF"))
        text(ctx, "Wi-Fi password", 0, -180, 38, (0.35, 0.4, 0.55), shadow=False)
        for i, wd in enumerate(("Nana", "IsThe", "Best")):
            text(ctx, wd, 0, -70 + i * 80, 66, hexc("#6A3590"), shadow=False)
        ctx.restore()
    if fiesta:
        confeti(ctx, T, T - lt + t_ok, W / 2, H * 0.55, 90)
        estallido(ctx, W / 2, H * 0.22, 190, clamp((lt - t_ok) / 0.3), hexc("#7CE38B"), 16, T * 0.4)
        badge(ctx, "CONNECTED!", W / 2, H * 0.22, pop(lt, t_ok, 0.3), 70, hexc("#7CE38B"), INK)
        corazones(ctx, 300, 900, T, 4, 1.0)
    ambiente(ctx, "calida", 0.8)


def e14(ctx, lt, dur, T, L):  # Teddy solo, en gris, con su nube de lluvia: "Nana..."
    ctx.save()
    zoom_cam(ctx, lt, [(0, (1.55, 540, 1230)), (dur, (1.75, 540, 1180))])
    salon(ctx, T, var=0)
    o = teddy(ctx, 540, 1620, 1.0, T, "triste", L.boca("teddy", T), arms="abajo", bounce=False, sq=0.9, head_dy=40,
              lean=0.04, gesto="caido")
    nube_lluvia(ctx, o["top"][0], o["top"][1] - 190, 1.0, T, 1.0, trueno=True)
    ctx.restore()
    ambiente(ctx, "gris")


ESCENAS = [
    (0.0, e1),
    ("L2-0.2", e2),
    ("L3-0.08", e3),
    ("L4-0.12", e4),
    ("L5-0.55", e5),
    ("L6-0.15", e6),
    ("L7-0.45", e7),
    ("L8-0.65", e8),
    ("L9-0.1", e9),
    ("L10-0.08", e10),
    ("L11-0.85", e11),
    ("L12-0.15", e12),
    ("L13-0.2", e13),
    ("L14-0.35", e14),
]
TRANS = {1: ("whip", 0.22), 2: ("zoom", 0.2), 3: ("whip", 0.22), 4: ("poof", 0.4), 5: ("whip", 0.22),
         6: ("iris", 0.35), 9: ("flash", 0.18), 10: ("whip", 0.22), 11: ("estrella", 0.45), 12: ("whip", 0.22),
         13: ("poof", 0.4)}
SFX = [(0.0, "zip"), (0.3, "whoosh"), ("L1+1.7", "boing"), ("L2-0.2", "whoosh"), ("L2+0.3", "twinkle"),
       ("L3-0.08", "slide_up"), ("L4-0.12", "whoosh"), ("L4+1.0", "typing"), ("L4+1.9", "typing"),
       ("L4+2.9", "typing"), ("L4+3.8", "tada"), ("L5-0.55", "poof"), ("L5-0.4", "spit"), ("L5-0.3", "boing"),
       ("L6-0.15", "whoosh"), ("L6+0.3", "zip"), ("L6+1.1", "zip_out"), ("F6", "doorbell"), ("F6+0.05", "boing"),
       ("L7-0.45", "whoosh"), ("L8-0.6", "twinkle"), ("L9-0.1", "slide_up"), ("L10-0.1", "scratch"),
       ("L10+1.1", "gasp"), ("F10+0.1", "crickets"), ("L11-0.85", "wind"), ("F11-0.3", "error"),
       ("L12-0.15", "twinkle"), ("L13-0.2", "whoosh"), ("F13-0.9", "tada"), ("F13-0.85", "connect"),
       ("L14-0.35", "poof"), ("L14-0.2", "slide_down"), ("L14+0.4", "thunder")]
MUSICA = [(0.0, "L10-0.1", "alegre"), ("L12-0.15", "L14-0.35", "alegre"), ("L14-0.35", 99, "triste")]
FINAL = (W / 2, H * 0.36, 0.55)
COLA = 0.7
