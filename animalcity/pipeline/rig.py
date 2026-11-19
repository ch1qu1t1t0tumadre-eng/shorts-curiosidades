"""Esqueletos articulados (muñeco recortable) para los dibujos oficiales de AnimalCity TV.

Cada dibujo (assets/personajes/*.png) se separa en piezas: cabeza, mandíbula, orejas, brazos, piernas, cola...
Cada pieza tiene su textura (sacada del propio dibujo, sin redibujar) y su malla de triángulos unida a los huesos
(hombro, codo, muñeca, cadera, rodilla, cuello, mandíbula, cola). Al girar los huesos las piezas se doblan con
suavidad en las articulaciones. Debajo de las piezas que se mueven por encima del cuerpo (brazos cruzados, la taza)
se rellena el cuerpo (inpainting) para que nunca se vea un hueco; debajo de la mandíbula queda el interior de la boca.

Zona: (nombre, polígono en px del recorte, cadena de huesos, capa, tipo)
  tipo "pegada": unida al hueso padre de la cadena en su articulación (no se separa nunca)
  tipo "suelta": pieza por encima del cuerpo (se rellena lo de debajo)
  tipo "boca":   como "pegada", y debajo queda el interior oscuro de la boca
La última zona es el cuerpo (todo lo demás).
"""
import math, os
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
_DIR = os.path.join(HERE, "assets", "personajes")

RIGS = {
    "teddy": {
        "huesos": {
            "raiz": {"padre": None, "pivote": (1000, 1620), "fin": (1000, 1150)},
            "pecho": {"padre": "raiz", "pivote": (990, 1150), "fin": (985, 720)},
            "cabeza": {"padre": "pecho", "pivote": (980, 700), "fin": (950, 330)},
            "mandibula": {"padre": "cabeza", "pivote": (820, 490), "fin": (1060, 620)},
            "oreja_i": {"padre": "cabeza", "pivote": (640, 290), "fin": (560, 560)},
            "oreja_d": {"padre": "cabeza", "pivote": (1110, 170), "fin": (1350, 210)},
            "brazo_i": {"padre": "pecho", "pivote": (630, 830), "fin": (300, 880)},
            "antebrazo_i": {"padre": "brazo_i", "pivote": (300, 880), "fin": (180, 1110)},
            "mano_i": {"padre": "antebrazo_i", "pivote": (180, 1110), "fin": (70, 1230)},
            "brazo_d": {"padre": "pecho", "pivote": (1180, 790), "fin": (1420, 690)},
            "antebrazo_d": {"padre": "brazo_d", "pivote": (1420, 690), "fin": (1580, 900)},
            "mano_d": {"padre": "antebrazo_d", "pivote": (1580, 900), "fin": (1730, 960)},
            "muslo_i": {"padre": "raiz", "pivote": (880, 1650), "fin": (900, 1950)},
            "pierna_i": {"padre": "muslo_i", "pivote": (900, 1950), "fin": (1000, 2280)},
            "pie_i": {"padre": "pierna_i", "pivote": (1000, 2280), "fin": (960, 2390)},
            "muslo_d": {"padre": "raiz", "pivote": (1170, 1650), "fin": (1480, 1740)},
            "pierna_d": {"padre": "muslo_d", "pivote": (1480, 1740), "fin": (1260, 1890)},
            "pie_d": {"padre": "pierna_d", "pivote": (1260, 1890), "fin": (1430, 2080)},
            "cola": {"padre": "raiz", "pivote": (790, 1720), "fin": (480, 1880)},
            "cola2": {"padre": "cola", "pivote": (480, 1880), "fin": (230, 1690)},
        },
        "zonas": [
            ("oreja_d", [(1090, 20), (1420, 60), (1420, 280), (1180, 270), (1080, 160)], ["oreja_d"], 8, "pegada"),
            ("oreja_i", [(430, 270), (640, 240), (690, 620), (560, 650), (420, 520)], ["oreja_i"], 7, "pegada"),
            ("cabeza", [(380, 0), (1460, 0), (1460, 560), (1240, 600), (1120, 650), (1060, 700), (900, 720), (720, 690), (560, 650), (380, 650)], ["cabeza"], 6, "pegada"),
            ("brazo_i", [(650, 720), (655, 1000), (560, 1070), (360, 1010), (230, 1300), (0, 1320), (0, 1040), (190, 760), (420, 700)], ["brazo_i", "antebrazo_i", "mano_i"], 4, "pegada"),
            ("brazo_d", [(1170, 690), (1330, 590), (1560, 590), (1720, 780), (1824, 860), (1824, 1110), (1560, 1020), (1430, 930), (1300, 1020), (1200, 980)], ["brazo_d", "antebrazo_d", "mano_d"], 4, "pegada"),
            ("cola", [(0, 1580), (800, 1660), (790, 1900), (520, 2060), (240, 2010), (0, 1820)], ["cola", "cola2"], 0, "pegada"),
            ("pierna_d", [(1030, 1640), (1330, 1600), (1580, 1740), (1540, 1830), (1480, 2140), (1260, 2010), (1110, 1820)], ["muslo_d", "pierna_d", "pie_d"], 1, "pegada"),
            ("pierna_i", [(740, 1640), (1030, 1650), (1080, 2396), (840, 2396), (780, 2010)], ["muslo_i", "pierna_i", "pie_i"], 1, "pegada"),
            ("cuerpo", None, ["raiz", "pecho"], 2, "cuerpo"),
        ],
        "boca_rgb": (60, 18, 30),
        # su boca dibujada está abierta con la lengua fuera: se tapa (queda la línea del labio) y se dibuja al hablar
        "tapar_auto": {"caja": (770, 470, 1112, 724), "labio": [(812, 488), (965, 526), (1095, 550)]},
        # los dedos del dibujo miran a la izquierda: se da la vuelta a la pierna para que miren hacia donde anda
        "espejos": {"pierna_i": 960},
        # pierna de atrás = copia de su pierna recta (el dibujo original tiene una pierna levantada, de baile)
        "clones": {"pierna_d": {"de": "pierna_i", "dx": 170, "dy": -12, "capa": 0.5, "luz": 0.86,
                                "huesos": {"muslo_d": "muslo_i", "pierna_d": "pierna_i", "pie_d": "pie_i"}}},
    },
    "moe": {
        "huesos": {
            "raiz": {"padre": None, "pivote": (590, 1360), "fin": (590, 900)},
            "pecho": {"padre": "raiz", "pivote": (590, 900), "fin": (590, 720)},
            "cabeza": {"padre": "pecho", "pivote": (590, 740), "fin": (590, 420)},
            "brazos": {"padre": "pecho", "pivote": (590, 900), "fin": (600, 960)},
            "pie_i": {"padre": "raiz", "pivote": (440, 1340), "fin": (420, 1490)},
            "pie_d": {"padre": "raiz", "pivote": (760, 1340), "fin": (780, 1490)},
        },
        "zonas": [
            ("labios", [(468, 596), (762, 596), (762, 684), (468, 684)], ["cabeza"], 9, "labios"),
            ("taza", [(410, 785), (790, 785), (830, 880), (820, 1075), (390, 1075), (370, 880)], ["brazos"], 5, "suelta"),
            ("cabeza", [(0, 0), (1184, 0), (1184, 600), (950, 650), (800, 700), (590, 730), (380, 700), (230, 650), (0, 600)], ["cabeza"], 4, "pegada"),
            ("pie_i", [(330, 1300), (560, 1300), (560, 1492), (330, 1492)], ["pie_i"], 1, "pegada"),
            ("pie_d", [(640, 1300), (880, 1300), (880, 1492), (640, 1492)], ["pie_d"], 1, "pegada"),
            ("cuerpo", None, ["raiz", "pecho"], 2, "cuerpo"),
        ],
    },
    "nana": {
        "huesos": {
            "raiz": {"padre": None, "pivote": (850, 1560), "fin": (800, 1150)},
            "pecho": {"padre": "raiz", "pivote": (800, 1150), "fin": (620, 880)},
            "cabeza": {"padre": "pecho", "pivote": (640, 880), "fin": (450, 520)},
            "brazo_i": {"padre": "pecho", "pivote": (440, 980), "fin": (240, 1270)},
            "antebrazo_i": {"padre": "brazo_i", "pivote": (240, 1270), "fin": (150, 1060)},
            "brazo_d": {"padre": "pecho", "pivote": (1060, 1130), "fin": (880, 1220)},
            "mano_d": {"padre": "brazo_d", "pivote": (880, 1220), "fin": (640, 1320)},
            "pie_i": {"padre": "raiz", "pivote": (680, 1570), "fin": (680, 1840)},
            "pie_d": {"padre": "raiz", "pivote": (1010, 1530), "fin": (1010, 1840)},
        },
        "zonas": [
            ("labios", [(318, 638), (504, 638), (504, 724), (318, 724)], ["cabeza"], 9, "labios"),
            ("cabeza", [(60, 0), (900, 0), (1000, 300), (1130, 450), (1130, 700), (850, 720), (700, 860), (520, 900), (300, 860), (100, 760), (60, 400)], ["cabeza"], 5, "pegada"),
            ("brazo_i", [(0, 830), (330, 820), (420, 900), (470, 1000), (420, 1330), (200, 1360), (0, 1300)], ["brazo_i", "antebrazo_i"], 4, "pegada"),
            ("mano_d", [(570, 1150), (1100, 1080), (1140, 1200), (900, 1300), (720, 1420), (560, 1360)], ["brazo_d", "mano_d"], 4, "suelta"),
            ("pie_i", [(540, 1560), (840, 1560), (840, 1844), (540, 1844)], ["pie_i"], 1, "pegada"),
            ("pie_d", [(870, 1480), (1170, 1460), (1190, 1844), (870, 1844)], ["pie_d"], 1, "pegada"),
            ("cuerpo", None, ["raiz", "pecho"], 2, "cuerpo"),
        ],
    },
    "mia": {
        "huesos": {
            "raiz": {"padre": None, "pivote": (450, 1650), "fin": (450, 1250)},
            "pecho": {"padre": "raiz", "pivote": (450, 1250), "fin": (450, 960)},
            "cabeza": {"padre": "pecho", "pivote": (450, 970), "fin": (380, 650)},
            "coleta": {"padre": "cabeza", "pivote": (620, 380), "fin": (880, 300)},
            "oreja_i": {"padre": "cabeza", "pivote": (200, 470), "fin": (160, 230)},
            "oreja_d": {"padre": "cabeza", "pivote": (640, 470), "fin": (690, 260)},
            "brazos": {"padre": "pecho", "pivote": (430, 1150), "fin": (430, 1350)},
            "muslo_i": {"padre": "raiz", "pivote": (350, 1680), "fin": (360, 2020)},
            "pierna_i": {"padre": "muslo_i", "pivote": (400, 2040), "fin": (330, 2220)},
            "muslo_d": {"padre": "raiz", "pivote": (530, 1700), "fin": (520, 2000)},
            "pierna_d": {"padre": "muslo_d", "pivote": (600, 2030), "fin": (610, 2220)},
            "cola": {"padre": "raiz", "pivote": (700, 1720), "fin": (1050, 1500)},
            "cola2": {"padre": "cola", "pivote": (1050, 1500), "fin": (1060, 1000)},
        },
        "zonas": [
            ("labios", [(268, 788), (502, 788), (502, 862), (268, 862)], ["cabeza"], 9, "labios"),
            ("oreja_i", [(110, 170), (330, 230), (330, 500), (60, 520)], ["oreja_i"], 7, "pegada"),
            ("oreja_d", [(560, 210), (740, 190), (770, 500), (580, 520)], ["oreja_d"], 7, "pegada"),
            ("coleta", [(470, 0), (1000, 0), (1000, 620), (760, 640), (640, 500), (470, 260)], ["coleta"], 5, "pegada"),
            ("cabeza", [(0, 150), (760, 150), (800, 760), (700, 900), (520, 990), (300, 980), (60, 880), (0, 760)], ["cabeza"], 6, "pegada"),
            ("brazos", [(90, 1000), (720, 1000), (740, 1470), (560, 1560), (200, 1500), (80, 1400)], ["brazos"], 4, "suelta"),
            ("cola", [(700, 920), (1304, 920), (1304, 1950), (880, 1960), (690, 1820), (690, 1650)], ["cola", "cola2"], 0, "pegada"),
            ("pierna_i", [(200, 1630), (440, 1630), (445, 1990), (465, 2060), (445, 2244), (190, 2244), (210, 2050)], ["muslo_i", "pierna_i"], 2, "pegada"),
            ("pierna_d", [(440, 1660), (690, 1640), (720, 1720), (715, 2244), (500, 2244), (490, 2100), (450, 2030)], ["muslo_d", "pierna_d"], 1, "pegada"),
            ("cuerpo", None, ["raiz", "pecho"], 3, "cuerpo"),
        ],
    },
}

CELDA = 28      # px del recorte por celda de la malla
SIGMA = 26      # suavizado entre huesos de una misma cadena (px)
COSTURA = 60    # en esta distancia (px) a la pieza padre, la pieza se mueve como el padre (no se abre la costura)
_CACHE = {}


def _seg_dist(P, a, b):
    a, b = np.array(a, float), np.array(b, float)
    ab = b - a
    t = np.clip(((P - a) @ ab) / max(1e-6, ab @ ab), 0, 1)
    return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)


def _grid(mask, w, h):
    nx, ny = int(math.ceil(w / CELDA)), int(math.ceil(h / CELDA))
    xs = np.linspace(0, w, nx + 1)
    ys = np.linspace(0, h, ny + 1)
    small = cv2.resize(mask.astype(np.uint8) * 255, (nx, ny), interpolation=cv2.INTER_AREA) > 0
    small = cv2.dilate(small.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    X, Y = np.meshgrid(xs, ys)
    V = np.stack([X.ravel(), Y.ravel()], 1)
    tris = []
    for j in range(ny):
        for i in range(nx):
            if small[j, i]:
                a = j * (nx + 1) + i
                b, c, d = a + 1, a + nx + 1, a + nx + 2
                tris += [(a, b, c), (b, d, c)]
    tris = np.array(tris, np.int64)
    used = np.unique(tris)
    remap = -np.ones(len(V), np.int64)
    remap[used] = np.arange(len(used))
    return V[used].astype(np.float64), remap[tris].astype(np.int32)


def _padre_de(rig, bone):
    return rig["huesos"][bone]["padre"]


def malla(nombre):
    """Piezas del personaje: [{nombre, capa, rgba, V, W, T}] (se calcula una vez)."""
    if nombre in _CACHE:
        return _CACHE[nombre]
    from PIL import Image
    rig = RIGS[nombre]
    im = np.asarray(Image.open(os.path.join(_DIR, f"{nombre}.png")).convert("RGBA")).copy()
    h, w = im.shape[:2]
    alpha = im[..., 3] > 8
    names = list(rig["huesos"].keys())
    bi = {n: k for k, n in enumerate(names)}
    # máscaras de cada zona (prioridad = orden de la lista)
    ocupado = np.zeros((h, w), bool)
    masks = []
    for (zn, poly, cadena, capa, tipo) in rig["zonas"]:
        if poly is None:
            m = ~ocupado
        else:
            m = np.zeros((h, w), np.uint8)
            cv2.fillPoly(m, [np.array(poly, np.int32)], 1)
            m = m.astype(bool) & ~ocupado
        masks.append(m)
        ocupado |= m
    # cada trocito suelto (fuera de la pieza principal de su zona) pasa a la zona más cercana
    from scipy import ndimage as ndi
    principal = []
    for zi, m in enumerate(masks):
        lab, n = ndi.label(m & alpha)
        if n == 0:
            principal.append(np.zeros_like(m))
            continue
        sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
        principal.append(lab == (1 + int(np.argmax(sizes))))
    dist = np.stack([ndi.distance_transform_edt(~pm) if pm.any() else np.full((h, w), 1e9) for pm in principal])
    sueltos = alpha & ~np.any(np.stack(principal), 0)
    if sueltos.any():
        dest = dist[:, sueltos].argmin(0)
        for zi in range(len(masks)):
            masks[zi] = principal[zi].copy()
        ys_, xs_ = np.nonzero(sueltos)
        for zi in range(len(masks)):
            sel = dest == zi
            masks[zi][ys_[sel], xs_[sel]] = True
    zona_de_hueso = {}
    for zi, z in enumerate(rig["zonas"]):
        for b in z[2]:
            zona_de_hueso[b] = zi
    # texturas: cada zona con sus píxeles y un margen de 12 px por debajo de las vecinas (sin grietas al doblar)
    tex = [np.zeros_like(im) for _ in rig["zonas"]]
    k12 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    for zi, (zn, poly, cadena, capa, tipo) in enumerate(rig["zonas"]):
        m = masks[zi]
        if tipo != "suelta":
            m = (cv2.dilate(m.astype(np.uint8), k12) > 0) & alpha
        tex[zi][m] = im[m]
    for zi, (zn, poly, cadena, capa, tipo) in enumerate(rig["zonas"]):
        if tipo in ("cuerpo", "labios"):
            continue
        padre = _padre_de(rig, cadena[0])
        pz = zona_de_hueso.get(padre, len(rig["zonas"]) - 1)
        m = masks[zi] & alpha
        if tipo == "suelta":  # se rellena el cuerpo de debajo
            rgb = cv2.cvtColor(im[..., :3], cv2.COLOR_RGB2BGR)
            fillm = (cv2.dilate(m.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0) & alpha
            inp = cv2.inpaint(rgb, fillm.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
            inp = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)
            tex[pz][fillm, :3] = inp[fillm]
            tex[pz][fillm, 3] = 255
        elif tipo == "boca":  # interior de la boca debajo de la mandíbula
            tex[pz][m, :3] = rig.get("boca_rgb", (60, 18, 30))
            tex[pz][m, 3] = 255
    zidx = {z[0]: i for i, z in enumerate(rig["zonas"])}
    rgb_bgr = cv2.cvtColor(im[..., :3], cv2.COLOR_RGB2BGR)

    def _inpaint_en(ti, m):
        base = cv2.cvtColor(tex[ti][..., :3], cv2.COLOR_RGB2BGR)
        base[~(tex[ti][..., 3] > 0)] = rgb_bgr[~(tex[ti][..., 3] > 0)]
        # fuera del dibujo no hay color que copiar: se rellena con el color medio del borde de la zona
        borde = cv2.dilate(m.astype(np.uint8), np.ones((15, 15), np.uint8)).astype(bool) & ~m & alpha
        if borde.any():
            base[~alpha] = np.median(base[borde], axis=0).astype(np.uint8)
        out = cv2.inpaint(base, m.astype(np.uint8) * 255, 15, cv2.INPAINT_TELEA)
        tex[ti][m, :3] = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)[m]
        tex[ti][m, 3] = 255
    def _rellenar(ti, m):
        """Rellena con el color plano de la piel de alrededor y suaviza sólo el borde (el dibujo es de colores planos)."""
        anillo = cv2.dilate(m.astype(np.uint8), np.ones((25, 25), np.uint8)).astype(bool) & ~m & alpha
        pix = im[anillo][:, :3].astype(np.float32)
        v = pix.max(1)
        pix = pix[v > np.percentile(v, 35)]  # sin los trazos oscuros
        col = np.median(pix, axis=0)
        tex[ti][m, :3] = col.astype(np.uint8)
        tex[ti][m, 3] = 255
        banda = cv2.dilate(m.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool) & ~cv2.erode(m.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
        bl = cv2.GaussianBlur(tex[ti][..., :3], (9, 9), 0)
        tex[ti][banda & alpha, :3] = bl[banda & alpha]
    # Teddy: se quita su boca abierta (interior, lengua, barbilla) y queda la línea del labio de arriba
    ta = rig.get("tapar_auto")
    if ta:
        x0, y0, x1, y1 = ta["caja"]
        hsv = cv2.cvtColor(im[..., :3], cv2.COLOR_RGB2HSV)
        caja = np.zeros((h, w), bool)
        caja[y0:y1, x0:x1] = True
        piel = (hsv[..., 0] > 8) & (hsv[..., 0] < 25) & (hsv[..., 1] > 90) & (hsv[..., 2] > 170)
        m = caja & alpha & ~piel
        lab = np.zeros((h, w), np.uint8)
        cv2.polylines(lab, [np.array(ta["labio"], np.int32)], False, 1, 20)
        m &= ~lab.astype(bool)
        m &= ~(np.arange(h)[:, None] < np.interp(np.arange(w), [p_[0] for p_ in ta["labio"]], [p_[1] for p_ in ta["labio"]])[None, :] + 6)
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool) & caja & alpha
        m = cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & caja & alpha & ~lab.astype(bool)
        _rellenar(zidx["cabeza"], m)
    for zi, z in enumerate(rig["zonas"]):
        if z[4] == "labios":
            m = cv2.dilate(masks[zi].astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & alpha
            _rellenar(zidx["cabeza"], m)
            tex[zi] = np.zeros_like(im)
            tex[zi][masks[zi]] = im[masks[zi]]
    # piernas dadas la vuelta (espejo sobre un eje vertical): textura y huesos de la cadena
    for zn, ax in rig.get("espejos", {}).items():
        zi = zidx[zn]
        src = tex[zi]
        out_ = np.zeros_like(src)
        xs = np.arange(w)
        xm = (2 * ax - xs).astype(int)
        ok = (xm >= 0) & (xm < w)
        out_[:, xs[ok]] = src[:, xm[ok]]
        tex[zi] = out_
        masks[zi] = out_[..., 3] > 0
        for b in rig["zonas"][zi][2]:
            hb = rig["huesos"][b]
            hb["pivote"] = (2 * ax - hb["pivote"][0], hb["pivote"][1])
            hb["fin"] = (2 * ax - hb["fin"][0], hb["fin"][1])
    # piezas clonadas: la textura de otra pieza desplazada (y sus huesos, desplazados igual)
    clones = rig.get("clones", {})
    for zn, c in clones.items():
        # fuera de todas las piezas lo que quedaba de la pieza original (p. ej. la pierna levantada)
        poly = rig["zonas"][zidx[zn]][1]
        borra = np.zeros((h, w), np.uint8)
        cv2.fillPoly(borra, [np.array(poly, np.int32)], 1)
        borra = borra.astype(bool)
        borra[:min(p_[1] for p_ in poly) + c.get("respeta", 8), :] = False
        for ti in range(len(tex)):
            if ti != zidx[c["de"]]:
                tex[ti][borra] = 0
        src = tex[zidx[c["de"]]].copy()
        dx, dy = c["dx"], c["dy"]
        sh = np.zeros_like(src)
        ys0, ys1 = max(0, dy), h + min(0, dy)
        xs0, xs1 = max(0, dx), w + min(0, dx)
        sh[ys0:ys1, xs0:xs1] = src[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
        sh[..., :3] = (sh[..., :3].astype(np.float32) * c.get("luz", 1.0)).astype(np.uint8)
        tex[zidx[zn]] = sh
        masks[zidx[zn]] = sh[..., 3] > 0
        for bd, bs in c["huesos"].items():
            hs = rig["huesos"][bs]
            rig["huesos"][bd]["pivote"] = (hs["pivote"][0] + dx, hs["pivote"][1] + dy)
            rig["huesos"][bd]["fin"] = (hs["fin"][0] + dx, hs["fin"][1] + dy)
    # distancia (px) de cada punto a cada zona: las piezas "pegadas" se mueven como su padre junto a la costura
    dist_z = [ndi.distance_transform_edt(~mm) for mm in masks]
    piezas = []
    for zi, (zn, poly, cadena, capa, tipo) in enumerate(rig["zonas"]):
        a = tex[zi][..., 3] > 0
        if not a.any():
            continue
        V, T = _grid(a, w, h)
        D = np.stack([_seg_dist(V, rig["huesos"][b]["pivote"], rig["huesos"][b]["fin"]) for b in cadena], 1)
        E = np.exp(-(D - D.min(1, keepdims=True)) / SIGMA)
        E /= E.sum(1, keepdims=True)
        Wt = np.zeros((len(V), len(names)))
        for k, b in enumerate(cadena):
            Wt[:, bi[b]] = E[:, k]
        if tipo == "labios":
            Wt[:] = 0
            Wt[:, bi["cabeza"]] = 1.0
        if tipo in ("pegada", "boca"):
            padre = _padre_de(rig, cadena[0])
            pz = zona_de_hueso.get(padre, len(rig["zonas"]) - 1)
            vx = np.clip(V[:, 0].astype(int), 0, w - 1)
            vy = np.clip(V[:, 1].astype(int), 0, h - 1)
            d = dist_z[pz][vy, vx]
            wp = np.exp(-(d / COSTURA) ** 2)
            pw = np.zeros(len(names))  # cómo se mueve el padre en la costura (sus mismos pesos de cadena)
            pcad = rig["zonas"][pz][2]
            Dp = np.stack([_seg_dist(V, rig["huesos"][b]["pivote"], rig["huesos"][b]["fin"]) for b in pcad], 1)
            Ep = np.exp(-(Dp - Dp.min(1, keepdims=True)) / SIGMA)
            Ep /= Ep.sum(1, keepdims=True)
            Wp = np.zeros_like(Wt)
            for k, b in enumerate(pcad):
                Wp[:, bi[b]] = Ep[:, k]
            Wt = Wt * (1 - wp)[:, None] + Wp * wp[:, None]
        # textura premultiplicada BGRA (lo que esperan skia y cairo)
        t = tex[zi].astype(np.float32)
        al = t[..., 3:4] / 255.0
        bgra = np.concatenate([t[..., 2:3] * al, t[..., 1:2] * al, t[..., 0:1] * al, t[..., 3:4]], 2).astype(np.uint8)
        piezas.append({"nombre": zn, "capa": capa, "bgra": np.ascontiguousarray(bgra), "V": V, "W": Wt, "T": T})
    for p_ in piezas:
        if p_["nombre"] in clones:
            p_["capa"] = clones[p_["nombre"]].get("capa", p_["capa"])
    piezas.sort(key=lambda p: p["capa"])
    out = {"piezas": piezas, "names": names, "w": w, "h": h}
    _CACHE[nombre] = out
    return out


def _rot(a, p, t=(0.0, 0.0)):
    c, s = math.cos(a), math.sin(a)
    px, py = p
    return np.array([[c, -s, px + t[0] - c * px + s * py],
                     [s, c, py + t[1] - s * px - c * py],
                     [0, 0, 1.0]])


def matrices(nombre, pose):
    """Matriz (3x3, px del recorte) de cada hueso. pose = {hueso: ángulo | (ángulo, tx, ty)}."""
    rig = RIGS[nombre]
    M = {}
    for n, b in rig["huesos"].items():
        v = pose.get(n, 0.0)
        a, tx, ty = (v, 0.0, 0.0) if not isinstance(v, (tuple, list)) else (v[0], v[1], v[2])
        loc = _rot(a, b["pivote"], (tx, ty))
        M[n] = loc if b["padre"] is None else M[b["padre"]] @ loc
    return M


def deformar(nombre, pose):
    """Posiciones deformadas de cada pieza + matrices de los huesos."""
    m = malla(nombre)
    M = matrices(nombre, pose)
    Ms = np.stack([M[n] for n in m["names"]])
    out = []
    for p in m["piezas"]:
        Vh = np.concatenate([p["V"], np.ones((len(p["V"]), 1))], 1)
        P = np.einsum("bij,nj->nbi", Ms, Vh)[..., :2]
        out.append((p, (p["W"][..., None] * P).sum(1)))
    return out, M
