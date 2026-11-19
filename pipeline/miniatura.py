#!/usr/bin/env python3
"""Miniatura vertical (1080x1920) para un Short.

El archivo .py que se le pasa define MINIATURA(ctx): dibuja la escena con las piezas del vídeo
(sus funciones de escenas.py) y encima el texto/flecha/círculo con thumb_text, thumb_arrow,
thumb_circle y thumb_vignette de anim.py.

Uso: python3 pipeline/miniatura.py work/vNN/escenas.py work/vNN/miniatura.jpg
     (o cualquier .py que importe las piezas de un vídeo antiguo, p. ej. miniaturas/gatos.py)
"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import anim  # noqa
from anim import W, H, cairo  # noqa

src, out = sys.argv[1], sys.argv[2]
sys.modules["anim"] = anim
sys.path.insert(0, os.path.dirname(os.path.abspath(src)))
sys.path.insert(0, os.path.join(HERE, "..", "ejemplos"))
spec = importlib.util.spec_from_file_location("mini_src", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
SC = 1.0
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W * SC), int(H * SC))
ctx = cairo.Context(surf)
ctx.scale(SC, SC)
ctx.save()
mod.MINIATURA(ctx)
ctx.restore()
png = out.rsplit(".", 1)[0] + ".png"
surf.write_to_png(png)
from PIL import Image, ImageEnhance  # noqa
im = Image.open(png).convert("RGB")
im = ImageEnhance.Color(im).enhance(1.15)
im = ImageEnhance.Contrast(im).enhance(1.06)
im.save(out, quality=92)
os.remove(png)
print(out, os.path.getsize(out) // 1024, "KB")
