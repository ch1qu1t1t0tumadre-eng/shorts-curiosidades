from sitcom import *

# EP01 · "Never ask Nana for the Wi-Fi password" (cartoon para todos los públicos)
# Pocas escenas y largas: los personajes ENTRAN y SALEN del plano andando o corriendo, la cámara se mueve hacia
# quien habla, y los gags (el móvil, "PLEASE!", el grito) aparecen encima sin cortar.
#   1. Rincón de Nana (líneas 1-6): Teddy entra corriendo, Moe entra con su taza, timbre, Teddy sale corriendo.
#   2. La puerta de noche (líneas 7-11): Teddy llega a la puerta, Mia llega por la acera, conversación a dos,
#      el grito (con un plano del edificio de 1 s) y el silencio incómodo. Mia entra en casa.
#   3. Rincón de Nana (líneas 12-14): Nana, Mia entra y lee el móvil, fiesta; Teddy entra arrastrando los pies.
# Personajes: dibujos oficiales como muñecos articulados (pipeline/rig.py).

PASS = "TeddyStillSleepsWithANightlight"
NANA = (800, 1545, 1.0)  # pies de Nana en su rincón


def ini(L, n):
    return L.lines[n - 1]["ini"]


def fin(L, n):
    return L.lines[n - 1]["fin"]


def cam_charla(L, T, sitios, zoom, base_y, peso=0.35):
    """Plano a dos o a tres: la cámara se desliza suavemente hacia quien habla."""
    xs = [x for x, _ in sitios.values()]
    cx = sum(xs) / len(xs)
    for pj, (x, _) in sitios.items():
        e = L.energia(pj, T, 0.5)
        cx += (x - cx) * peso * clamp(e * 3)
    return (zoom, cx, base_y)


def suave(T, puntos):
    """Interpola (zoom, cx, cy) entre puntos [(T, (z, x, y))] con aceleración suave (tiempo absoluto)."""
    pts = sorted(puntos, key=lambda p: p[0])
    if T <= pts[0][0]:
        return pts[0][1]
    for (t0, a), (t1, b) in zip(pts, pts[1:]):
        if T < t1:
            p = smooth((T - t0) / max(1e-6, t1 - t0))
            return tuple(a[i] + (b[i] - a[i]) * p for i in range(3))
    return pts[-1][1]


def movil_burbuja(ctx, T, t0, n_letras, x=W * 0.5, y=H * 0.2, k=0.55):
    """Móvil de Nana en una burbuja encima de la escena (sin cortar el plano)."""
    p = pop(T - t0, 0, 0.3)
    if p <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(-0.04 + 0.015 * math.sin(T * 2))
    ctx.scale(k * p, k * p)
    rrect(ctx, -380, -470, 760, 940, 70)
    fill_keep(ctx, (0.15, 0.14, 0.2))
    stroke(ctx, INK, 14)
    rrect(ctx, -340, -430, 680, 860, 50)
    fill(ctx, hexc("#E9F4FF"))
    text(ctx, "Wi-Fi password", 0, -300, 58, (0.35, 0.4, 0.55), shadow=False)
    shown = PASS[:n_letras]
    rrect(ctx, -300, -220, 600, 330, 26)
    fill_keep(ctx, WHITE)
    stroke(ctx, hexc("#5EB8F2"), 6)
    for i, part in enumerate((shown[:10], shown[10:21], shown[21:])):
        text(ctx, part, 0, -140 + i * 95, 66, INK, shadow=False)
    if n_letras >= len(PASS):
        badge(ctx, "SAVED!", 0, 300, 1.0, 70, hexc("#7CE38B"), INK)
    ctx.restore()


def movil_nuevo(ctx, T, t0):
    k = pop(T - t0, 0, 0.3)
    if k <= 0:
        return
    ctx.save()
    ctx.translate(W * 0.5, H * 0.22)
    ctx.rotate(-0.05 + 0.02 * math.sin(T * 3))
    ctx.scale(k * 0.8, k * 0.8)
    rrect(ctx, -190, -320, 380, 640, 54)
    fill_keep(ctx, (0.15, 0.14, 0.2))
    stroke(ctx, INK, 10)
    rrect(ctx, -165, -292, 330, 584, 36)
    fill(ctx, hexc("#E9F4FF"))
    text(ctx, "Wi-Fi password", 0, -180, 38, (0.35, 0.4, 0.55), shadow=False)
    for i, wd in enumerate(("Nana", "IsThe", "Best")):
        text(ctx, wd, 0, -70 + i * 80, 66, hexc("#6A3590"), shadow=False)
    ctx.restore()


# ------------------------------------------------------------------ 1. Rincón de Nana
def s1(ctx, lt, dur, T, L):
    tbell = fin(L, 6) + 0.1
    # Teddy: entra corriendo, suplica, corre con el pánico y sale corriendo cuando suena el timbre
    if T < ini(L, 6):
        tx, tpaso, tder, tmueve = recorrido(T, [(-0.2, -260), (0.5, 300)], 300)
    elif T < tbell + 0.2:
        cx, fl, vel = carrera(T - ini(L, 6), 130, 0.9)
        tx, tpaso, tder, tmueve = 190 + cx, (T - ini(L, 6)) * 2.4, not fl, True
    else:
        tx, tpaso, tder, tmueve = recorrido(T, [(tbell + 0.2, 190), (tbell + 0.8, -320)], 300)
    # Moe: entra andando con su taza durante la contraseña, bebe... y la escupe
    t_esc = ini(L, 5) - 0.35
    mx, mpaso, mder, mmueve = recorrido(T, [(ini(L, 4) + 0.8, -200), (ini(L, 4) + 2.6, 500)], 150)
    if T > ini(L, 4) + 1.4 and T < ini(L, 6):  # Teddy le hace sitio a Moe
        tx, tpaso, tder, tmueve = recorrido(T, [(ini(L, 4) + 1.4, 300), (ini(L, 4) + 2.2, 190)], 300)
        tder = True
    cam = suave(T, [(0.0, (1.3, 500, 1230)), (ini(L, 2) - 0.2, (1.3, 520, 1220)),
                    (ini(L, 2) + 0.3, (1.75, 700, 1160)), (ini(L, 3) - 0.1, (1.75, 700, 1160)),
                    (ini(L, 3) + 0.15, (1.85, 330, 1180)), (fin(L, 3) + 0.2, (1.85, 330, 1180)),
                    (ini(L, 4) + 0.4, (1.2, 540, 1250)), (t_esc - 0.3, (1.1, 540, 1260)),
                    (t_esc, (1.7, 520, 1280)), (fin(L, 5), (1.7, 520, 1280)),
                    (ini(L, 6) + 0.2, (1.2, 520, 1250))])
    sx, sy = temblor(T, 8 * clamp(1 - abs(T - t_esc) / 0.4)) if abs(T - t_esc) < 0.4 else (0, 0)
    ctx.save()
    zoom_cam(ctx, 0, [(0, (cam[0], cam[1] + sx, cam[2] + sy))])
    rincon_nana(ctx, T)
    nana(ctx, *NANA, T, "smug", L.boca("nana", T), typing=not L.speaking("nana", T),
         escucha=L.energia("teddy", T) * 2, mira=1, ene=L.energia("nana", T))
    # Moe (delante de Nana)
    if T > ini(L, 4) + 0.8:
        dy, sq = toma(T, t_esc, 1.0)
        moe(ctx, mx, 1600, 0.85, T, "sorpresa" if T < t_esc + 0.5 else "panico", L.boca("moe", T),
            paso=mpaso if mmueve else None, dy=dy, sq=sq,
            gesto="sorber" if t_esc - 0.5 < T < t_esc else None,
            escucha=L.energia("nana", T) * 2 if T < t_esc else 0.0, mira=1)
        if T < t_esc:
            vapor(ctx, mx + 30, 1400, T, 0.5)
        hx, hy = cabeza("moe", mx, 1600, 0.85)
        for i in range(22):  # espurreo de chocolate
            p = clamp((T - t_esc) / 0.7)
            if 0 < p < 1:
                a = -1.25 + i * 0.11
                v = 520 + (i % 5) * 60
                circle(ctx, hx + 30 + math.cos(a) * v * p, hy + 110 + math.sin(a) * v * 0.6 * p + 500 * p * p,
                       9 * (1 - p) + 3)
                fill_keep(ctx, hexc("#7A4A2A"), 1 - p * 0.7)
                stroke(ctx, INK, 2, 1 - p)
    # Teddy
    gesto = None
    if ini(L, 3) - 0.1 < T < fin(L, 3) + 0.4:
        gesto = "suplicar"
    elif not tmueve and T < ini(L, 2) + 0.3:
        gesto = "agitar"
    teddy(ctx, tx, 1620, 1.0, T, "panico" if T < ini(L, 4) or T > ini(L, 6) else "normal", L.boca("teddy", T),
          paso=tpaso if tmueve else None, correr=True, flip=not tder, bounce=False,
          ene=L.energia("teddy", T), gesto=gesto, blush=0.6 if gesto == "suplicar" else 0.0,
          escucha=L.energia("nana", T) * 2 if T > ini(L, 2) else 0.0, mira=1)
    if tmueve and T < ini(L, 6):
        lineas_velocidad(ctx, tx - 600, 1050, 520, 520, 1, T, 10, WHITE, 0.6)
    polvo(ctx, 300, 1620, (T - 0.45) / 0.5)
    ctx.restore()
    ambiente(ctx, "calida")
    # gags encima del plano (sin cortar)
    if ini(L, 3) - 0.1 < T < fin(L, 3) + 0.5:  # suplica: luz rosa, corazones y destellos
        a = clamp((T - ini(L, 3) + 0.1) / 0.2) * clamp((fin(L, 3) + 0.5 - T) / 0.2)
        ambiente(ctx, "rosa", a)
        corazones(ctx, 380, 700, T, 5, 1.2, hexc("#FF7AB6"))
        destellos(ctx, 100, 400, 880, 900, T, 12, hexc("#FFE6F2"), a, 3, 30)
    if ini(L, 4) + 0.3 < T < fin(L, 4) + 0.6:  # el móvil de Nana, en burbuja
        n = int(clamp((T - ini(L, 4) - 0.6) / 2.6) * len(PASS))
        movil_burbuja(ctx, T, ini(L, 4) + 0.3, n, W * 0.5, H * 0.21, 0.5)
    if t_esc + 0.4 < T < fin(L, 5) + 0.3:
        emote(ctx, "!", W * 0.52, H * 0.3, clamp((T - t_esc - 0.4) / 0.3), hexc("#FFD23F"), 150, T)
    if T > tbell:
        p = clamp((T - tbell) / 0.25)
        estallido(ctx, W * 0.2, H * 0.35, 170, p, hexc("#FFD23F"), 16, 0.2)
        impacto(ctx, "DING DONG!", W * 0.2, H * 0.35, 66, WHITE, e_back(p), T, 3, -0.12)
    if 0.55 < T < 1.15:
        lineas_foco(ctx, W / 2, H * 0.45, T, 0.3 * clamp(1 - (T - 0.55) / 0.6))


# ------------------------------------------------------------------ 2. La puerta de noche
def s2(ctx, lt, dur, T, L):
    t0 = T - lt
    grito0, grito1 = ini(L, 10), fin(L, 10)
    # plano del edificio durante el eco del grito (único corte de la escena)
    if grito0 + 0.85 < T < grito1 + 0.25:
        p = clamp((T - grito0 - 0.85) / 0.9)
        ctx.save()
        sx, sy = temblor(T, 4)
        zoom_cam(ctx, 0, [(0, (1.0 - 0.06 * p, 540 + sx, 1000 + sy))])
        edificio(ctx, T, p, ondas=1 - p * 0.5)
        ctx.restore()
        ambiente(ctx, "noche", 0.15)
        return
    tx, tpaso, tder, tmueve = recorrido(T, [(t0, -260), (t0 + 0.55, 250)], 300)
    mx, mpaso, mder, mmueve = recorrido(T, [(t0 + 0.45, 1000), (t0 + 1.35, 660)], 260)
    salida = fin(L, 11) + 0.35  # al final Mia entra en casa pasando por delante de Teddy
    if T > salida:
        mx, mpaso, mder, mmueve = recorrido(T, [(salida, 660), (salida + 1.1, -250)], 260)
    sitios = {"teddy": (250, 1720), "mia": (680, 1495)}
    if grito0 - 0.05 < T < grito0 + 0.85:  # el grito: cámara encima de Teddy, temblando
        sx, sy = temblor(T, 14)
        cam = (1.75, 320 + sx, 1170 + sy)
    else:
        z = 1.2 if T < t0 + 1.4 else 1.35
        cam = cam_charla(L, T, sitios, z, 1170)
    ctx.save()
    zoom_cam(ctx, 0, [(0, cam)])
    entrada_noche(ctx, T, abierta=e_out((T - t0 - 0.35) / 0.45))
    rodando = fin(L, 10) + 0.3 < T < ini(L, 11) + 0.2
    s_mia = 0.8 + 0.1 * clamp((1000 - mx) / 340)
    mia(ctx, mx, 1495, s_mia, T, "sospecha" if T > grito1 else "normal", L.boca("mia", T), arms="movil",
        paso=mpaso if mmueve else None, flip=(T < salida) or not mder, ene=L.energia("mia", T),
        escucha=L.energia("teddy", T) * 2, mira=1, lid=0.35 if (rodando or T > grito1) else None)
    dy, sq = toma(T, grito0, 1.2)
    if grito0 - 0.05 < T < grito0 + 0.85:
        g_t = "arriba"
    elif T < ini(L, 8) - 0.3:
        g_t = None
    else:
        g_t = "encoger"
    teddy(ctx, tx, 1720, 1.05, T, "panico", L.boca("teddy", T), paso=tpaso if tmueve else None, correr=True,
          bounce=False, dy=dy, sq=sq, gesto=g_t, blush=1.0 if ini(L, 8) - 0.3 < T < grito0 else 0.4,
          escucha=L.energia("mia", T) * 2, mira=1, ene=L.energia("teddy", T))
    if rodando or ini(L, 11) - 0.1 < T < fin(L, 11):
        rodador(ctx, -250 + (T - fin(L, 10) - 0.3) * 900, 1730, 90, T)
    ctx.restore()
    ambiente(ctx, "noche", 0.25)
    if grito0 - 0.05 < T < grito0 + 0.85:
        lineas_foco(ctx, W / 2, H * 0.4, T, 0.55)
        flash(ctx, 0.5 * clamp(1 - (T - grito0) / 0.15))
    if ini(L, 9) - 0.05 < T < fin(L, 9) + 0.4:
        emote(ctx, "?", W * 0.72, H * 0.3, clamp((T - ini(L, 9) + 0.05) / 0.3), WHITE, 170, T)
    t_wrong = fin(L, 11) - 0.3
    if t_wrong < T < salida + 0.6:
        estallido(ctx, W * 0.66, H * 0.3, 190, clamp((T - t_wrong) / 0.3), hexc("#FF5A5A"), 14, -0.1)
        badge(ctx, "WRONG!", W * 0.66, H * 0.3, pop(T - t_wrong, 0, 0.3), 100, hexc("#FF5A5A"))


# ------------------------------------------------------------------ 3. Rincón de Nana: la contraseña nueva
def s3(ctx, lt, dur, T, L):
    t_ok = fin(L, 13) - 0.9
    fiesta = T > t_ok
    mx, mpaso, mder, mmueve = recorrido(T, [(fin(L, 12) - 0.2, -220), (fin(L, 12) + 1.0, 400),
                                            (fin(L, 13) + 0.15, 400), (fin(L, 13) + 0.75, 590)], 270)
    mira_teddy = T > fin(L, 13) + 0.75
    tx, tpaso, tder, tmueve = recorrido(T, [(fin(L, 13) + 0.1, -260), (ini(L, 14) - 0.05, 200)], 200)
    hx, hy = cabeza("nana", *NANA)
    cam = suave(T, [(T - lt, (2.3, hx + 20, hy + 120)), (fin(L, 12) - 0.1, (2.5, hx + 20, hy + 100)),
                    (fin(L, 12) + 0.6, (1.35, 600, 1190)), (fin(L, 13), (1.4, 600, 1180)),
                    (fin(L, 13) + 0.6, (1.15, 480, 1240)), (ini(L, 14) + 0.5, (1.3, 380, 1220))])
    ctx.save()
    zoom_cam(ctx, 0, [(0, cam)])
    rincon_nana(ctx, T, var=0)
    jy, jsq = salto(T, t_ok + 0.05, 0.38, 150)
    nana(ctx, *NANA, T, "feliz" if fiesta and T < fin(L, 13) + 0.4 else "smug", L.boca("nana", T),
         screen_text="NanaIsTheBest", typing=T < fin(L, 12) - 0.3 and not L.speaking("nana", T),
         escucha=L.energia("mia", T) * 2, mira=1, ene=L.energia("nana", T))
    if T > fin(L, 12) - 0.2:
        mia(ctx, mx, 1585, 0.95, T, "feliz" if fiesta else "normal", L.boca("mia", T), arms="cruzados", dy=jy,
            sq=jsq, paso=mpaso if mmueve else None, ene=L.energia("mia", T), flip=mira_teddy,
            escucha=L.energia("teddy", T) * 2, mira=1)
    if T > fin(L, 13) + 0.1:
        o = teddy(ctx, tx, 1660, 1.0, T, "triste", L.boca("teddy", T), bounce=False, sq=0.92, head_dy=40, lean=0.04,
                  gesto="caido", paso=tpaso if tmueve else None)
        nube_lluvia(ctx, o["top"][0], o["top"][1] - 190, 0.9, T, 1.0, trueno=True)
    ctx.restore()
    ambiente(ctx, "calida", 0.8)
    if fin(L, 12) + 0.9 < T < t_ok:  # el móvil de Nana, en burbuja
        movil_nuevo(ctx, T, fin(L, 12) + 0.9)
    if fiesta and T < fin(L, 13) + 0.45:
        confeti(ctx, T, t_ok, W / 2, H * 0.55, 90)
        estallido(ctx, W / 2, H * 0.22, 190, clamp((T - t_ok) / 0.3), hexc("#7CE38B"), 16, T * 0.4)
        badge(ctx, "CONNECTED!", W / 2, H * 0.22, pop(T - t_ok, 0, 0.3), 70, hexc("#7CE38B"), INK)


ESCENAS = [
    (0.0, s1),
    ("F6+0.75", s2),
    ("L12-1.0", s3),
]
TRANS = {1: ("whip", 0.25), 2: ("iris", 0.45)}
SFX = [(0.0, "zip"), (0.45, "whoosh"), ("L2+0.3", "twinkle"), ("L3-0.1", "slide_up"),
       ("L4+0.3", "pop"), ("L4+0.7", "typing"), ("L4+1.6", "typing"), ("L4+2.5", "typing"), ("L4+3.3", "tada"),
       ("L5-0.35", "spit"), ("L5-0.3", "boing"), ("L6+0.2", "zip"), ("F6+0.1", "doorbell"), ("F6+0.3", "zip_out"),
       ("F6+0.75", "whoosh"), ("F6+1.1", "zip"), ("F6+1.2", "whoosh"), ("L9-0.05", "slide_up"),
       ("L10-0.1", "scratch"), ("L10+0.9", "gasp"), ("F10+0.3", "crickets"), ("F10+0.3", "wind"),
       ("F11-0.3", "error"), ("F11+0.4", "zip"), ("L12-1.0", "whoosh"), ("L12+0.6", "twinkle"),
       ("F13-0.9", "tada"), ("F13-0.85", "connect"), ("F13+0.2", "slide_down"), ("L14+0.4", "thunder")]
MUSICA = [(0.0, "L10-0.1", "alegre"), ("L12-1.0", "F13+0.1", "alegre"), ("F13+0.1", 99, "triste")]
FINAL = (W * 0.33, H * 0.36, 0.6)
COLA = 0.9
