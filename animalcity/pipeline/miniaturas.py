#!/usr/bin/env python3
"""Mesa de Miniaturas: crea 10 versiones de la miniatura de un episodio y una hoja de contacto para puntuarlas.

Entrada: work/epNN/miniaturas.json  (10 variantes)
  [{"id": "A", "t": 3.2,                 # instante del episodio que sirve de fondo (fotograma real)
    "texto": "NEVER ASK NANA", "color": "#FFD23F", "pos": "arriba"|"centro"|"abajo",
    "zoom": 1.25, "cx": 540, "cy": 900,   # reencuadre del fotograma (zoom sobre el punto cx,cy)
    "borde": "#B07CE8",                   # opcional: marco de color del personaje
    "pegatina": "💀"}]                    # opcional: un emoji grande de OpenMoji
Salida: work/epNN/thumbs/A.png ... J.png (1080x1920), thumbs/hoja.png (las 10 a tamaño de móvil) y
        thumbs/A_small.png ... (a 180 px de ancho: así se ven en búsqueda y en la página del canal).
Uso: python3 miniaturas.py work/epNN
Después: mirar thumbs/hoja.png, puntuar con la rúbrica de oficina/MINIATURAS.md y copiar la ganadora a thumb_final.jpg:
        python3 miniaturas.py work/epNN elegir C
"""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sitcom as S
from PIL import Image, ImageDraw, ImageFont


def build(workdir):
    specs = json.load(open(os.path.join(workdir, "miniaturas.json")))
    td = os.path.join(workdir, "thumbs")
    os.makedirs(td, exist_ok=True)
    mod, tl = S._load(workdir)
    L = S.Dialogo(tl)
    escenas = sorted(mod.ESCENAS, key=lambda e: e[0])
    cairo = S.cairo
    paths = []
    for sp in specs:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S.W, S.H)
        ctx = cairo.Context(surf)
        z = float(sp.get("zoom", 1.0))
        ctx.translate(S.W / 2, S.H / 2)
        ctx.scale(z, z)
        ctx.translate(-float(sp.get("cx", S.W / 2)), -float(sp.get("cy", S.H / 2)))
        T = float(sp["t"])
        k = max([j for j, e in enumerate(escenas) if e[0] <= T] or [0])
        t1 = escenas[k + 1][0] if k + 1 < len(escenas) else tl["dur"]
        ctx.save()
        S._MUTE["impacto"] = True  # fondo limpio: sin los textos de impacto del propio vídeo
        escenas[k][1](ctx, T - escenas[k][0], t1 - escenas[k][0], T, L)
        S._MUTE["impacto"] = False
        ctx.restore()
        ctx.identity_matrix()
        if sp.get("borde"):
            S.rrect(ctx, 18, 18, S.W - 36, S.H - 36, 40)
            S.stroke(ctx, S.hexc(sp["borde"]), 28)
        y = {"arriba": 420, "centro": 900, "abajo": 1380}.get(sp.get("pos", "arriba"), 420)
        lines = sp["texto"].split("\n")
        size = 190 if max(len(l) for l in lines) <= 10 else 150 if max(len(l) for l in lines) <= 14 else 120
        for i, ln in enumerate(lines):
            S.impacto(ctx, ln, S.W / 2, y + i * size * 1.05, size, S.hexc(sp.get("color", "#FFFFFF")), 1.0, 0.0, 0, -0.03)
        if sp.get("pegatina"):
            S.icon(ctx, sp["pegatina"], 860, y - size * 0.9, 240, 1.0, 0.15)
        p = os.path.join(td, f'{sp["id"]}.png')
        surf.write_to_png(p)
        Image.open(p).resize((180, 320), Image.LANCZOS).save(os.path.join(td, f'{sp["id"]}_small.png'))
        paths.append((sp["id"], p))
    # hoja de contacto: 5 x 2 a tamaño "móvil" (216x384) con su letra
    cols, cw, chh = 5, 216, 384
    hoja = Image.new("RGB", (cols * cw + (cols + 1) * 16, 2 * chh + 3 * 16 + 60), (24, 22, 40))
    d = ImageDraw.Draw(hoja)
    try:
        f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 30)
    except Exception:
        f = ImageFont.load_default()
    for i, (vid, p) in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((cw, chh), Image.LANCZOS)
        x = 16 + (i % cols) * (cw + 16)
        y = 16 + (i // cols) * (chh + 46)
        hoja.paste(im, (x, y))
        d.text((x + cw // 2 - 10, y + chh + 4), vid, fill=(255, 210, 63), font=f)
    hoja.save(os.path.join(td, "hoja.png"))
    print("ok", len(paths), "miniaturas ->", os.path.join(td, "hoja.png"))


def elegir(workdir, vid):
    src = os.path.join(workdir, "thumbs", f"{vid}.png")
    Image.open(src).convert("RGB").save(os.path.join(workdir, "thumb_final.jpg"), quality=92)
    print("ganadora", vid, "-> thumb_final.jpg")


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[2] == "elegir":
        elegir(sys.argv[1], sys.argv[3])
    else:
        build(sys.argv[1])
