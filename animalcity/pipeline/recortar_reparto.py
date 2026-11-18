#!/usr/bin/env python3
"""Recorta a los 4 personajes del lineup oficial (variante 2, ampliado x4) en PNG con transparencia.

Entrada: referencias/reparto_v2_x4.png (5504x3072, fondo blanco roto)
Salida:  assets/personajes/{teddy,moe,nana,mia}.png  (sin el nombre ni la línea del suelo)
Mia está delante del caparazón de Nana: a Mia se le quitan los trozos de caparazón y a Nana se le
quita Mia y se le cierra el borde del caparazón con un contorno nuevo.
Uso: python3 recortar_reparto.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "referencias", "reparto_v2_x4.png")
OUT = os.path.join(HERE, "assets", "personajes")
K = 4  # factor de ampliación respecto a las coordenadas medidas en 1376x768
# cajas (x0, y0, x1, y1) en coordenadas 1376x768
BOX = {"teddy": (14, 108, 470, 707), "moe": (408, 334, 704, 707), "nana": (706, 246, 1092, 707), "mia": (1030, 146, 1356, 707)}


def bg_mask(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    light = (r > 214) & (g > 210) & (b > 200) & ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 30)
    lab, n = ndi.label(light)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(border))


def largest(mask):
    lab, n = ndi.label(mask)
    if n == 0:
        return mask
    sizes = ndi.sum(mask, lab, range(1, n + 1))
    return lab == (1 + int(np.argmax(sizes)))


def hsv(a):
    im = Image.fromarray(a).convert("HSV")
    h = np.asarray(im).astype(float)
    return h[..., 0] * 360 / 255, h[..., 1] / 255, h[..., 2] / 255


def to_rgba(a, mask, bgm):
    # alfa suave en el borde: los píxeles casi blancos pegados al fondo se vuelven semitransparentes
    near = ndi.binary_dilation(bgm, iterations=3) & mask
    dist = np.sqrt(((a.astype(float) - np.array([247, 245, 238])) ** 2).sum(-1))
    alpha = mask.astype(float)
    alpha[near] = np.clip(dist[near] / 60.0, 0, 1)
    rgba = np.dstack([a, (alpha * 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA")


def crop(full, name):
    x0, y0, x1, y1 = [v * K for v in BOX[name]]
    return full[y0:y1, x0:x1].copy(), (x0, y0)


def main():
    os.makedirs(OUT, exist_ok=True)
    full = np.asarray(Image.open(SRC).convert("RGB"))
    # --- Teddy y Moe: limpios, solo hay que quitar el fondo y los trozos de vecinos
    for name in ("teddy", "moe"):
        a, _ = crop(full, name)
        bgm = bg_mask(a)
        m = largest(~bgm)
        to_rgba(a, m, bgm).save(os.path.join(OUT, f"{name}.png"))
    # --- Mia: quitar el caparazón de Nana (tonos oliva) que asoma a su izquierda
    a, (mx0, my0) = crop(full, "mia")
    bgm = bg_mask(a)
    fg = ~bgm
    H, S, V = hsv(a)
    dark = V < 0.28
    shell = (H > 35) & (H < 74) & (S > 0.2) & (V > 0.2) & (V < 0.85)
    xs = np.arange(a.shape[1])[None, :].repeat(a.shape[0], 0)
    shell &= xs < 70 * K  # el caparazón solo asoma por el borde izquierdo de la caja de Mia
    # quitar las placas del caparazón y las líneas oscuras que las rodean (no los colores de Mia)
    remove = shell | (dark & ndi.binary_dilation(shell, iterations=14))
    m = largest(fg & ~remove)
    m = ndi.binary_fill_holes(m)
    core = largest(ndi.binary_opening(m, iterations=9))  # quita restos finos (líneas del caparazón)
    m = core | (ndi.binary_dilation(core, iterations=9) & m)
    arr = np.asarray(to_rgba(a, m, bgm)).copy()
    # contorno nuevo donde se quitó el caparazón
    cut = m & ~ndi.binary_erosion(m, iterations=10) & ndi.binary_dilation(remove, iterations=12)
    arr[cut, 0:3] = (24, 22, 30)
    arr[cut, 3] = 255
    Image.fromarray(arr, "RGBA").save(os.path.join(OUT, "mia.png"))
    mia_full = np.zeros(full.shape[:2], bool)
    mia_full[my0:my0 + a.shape[0], mx0:mx0 + a.shape[1]] = m
    # --- Nana: quitar a Mia y cerrar el caparazón
    a, (nx0, ny0) = crop(full, "nana")
    bgm = bg_mask(a)
    fg = ~bgm
    mia_here = mia_full[ny0:ny0 + a.shape[0], nx0:nx0 + a.shape[1]]
    mia_here = ndi.binary_dilation(mia_here, iterations=6)
    m = fg & ~mia_here
    m = largest(ndi.binary_opening(m, iterations=2))
    m = ndi.binary_fill_holes(m)
    zone = ndi.binary_dilation(mia_here, iterations=40)  # suaviza el borde cortado del caparazón
    smooth = ndi.binary_opening(ndi.binary_closing(m, iterations=30), iterations=30)
    m = np.where(zone, smooth & fg, m)
    m = largest(m)
    rgba = to_rgba(a, m, bgm)
    arr = np.asarray(rgba).copy()
    # contorno nuevo donde se cortó (borde del recorte que toca la zona de Mia)
    cut = m & ~ndi.binary_erosion(m, iterations=10) & ndi.binary_dilation(mia_here, iterations=12)
    arr[cut, 0:3] = (24, 22, 30)
    arr[cut, 3] = 255
    img = Image.fromarray(arr, "RGBA")
    img.save(os.path.join(OUT, "nana.png"))
    for n in ("teddy", "moe", "nana", "mia"):
        im = Image.open(os.path.join(OUT, f"{n}.png"))
        print(n, im.size)


if __name__ == "__main__":
    main()
