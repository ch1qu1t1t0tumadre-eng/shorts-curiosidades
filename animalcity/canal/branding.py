"""Banner (2560x1440) y foto de perfil (800x800) del canal AnimalCity TV.
Usa solo los dibujos oficiales del reparto (pipeline/assets/personajes)."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
P = BASE / "pipeline/assets/personajes"
FONT = str(BASE / "pipeline/assets/LilitaOne-Regular.ttf")
OUT = BASE / "canal"
random.seed(7)

def personaje(n, crop_frac=1.0):
    im = Image.open(P / f"{n}.png").convert("RGBA"); im = im.crop(im.getbbox())
    if crop_frac < 1: im = im.crop((0, 0, im.width, int(im.height * crop_frac)))
    return im

def contorno(im, w=14, col=(255, 255, 255, 255)):
    a = im.split()[3].filter(ImageFilter.MaxFilter(w * 2 + 1))
    bg = Image.new("RGBA", im.size, col); out = Image.new("RGBA", im.size, (0,0,0,0))
    out.paste(bg, (0, 0), a); out.alpha_composite(im); return out

def pad(im, p):
    o = Image.new("RGBA", (im.width + 2*p, im.height + 2*p), (0,0,0,0)); o.paste(im, (p, p)); return o

def sombra(im, off=(0, 18), blur=18, alpha=110):
    a = im.split()[3].point(lambda v: v * alpha // 255)
    s = Image.new("RGBA", im.size, (40, 10, 60, 255)); s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(blur)); o = Image.new("RGBA", im.size, (0,0,0,0))
    o.alpha_composite(s, off); o.alpha_composite(im); return o

def rayos(W, H, cx, cy, c1, c2, n=28):
    im = Image.new("RGBA", (W, H), c1); d = ImageDraw.Draw(im); R = max(W, H) * 1.5
    for i in range(n):
        if i % 2: continue
        a0, a1 = 2*math.pi*i/n, 2*math.pi*(i+1)/n
        d.polygon([(cx, cy), (cx + R*math.cos(a0), cy + R*math.sin(a0)), (cx + R*math.cos(a1), cy + R*math.sin(a1))], fill=c2)
    return im

def degradado_radial(W, H, cx, cy, inner, outer, r):
    g = Image.new("L", (W, H), 0); d = ImageDraw.Draw(g)
    for k in range(60, 0, -1):
        rr = r * k / 60; d.ellipse((cx-rr, cy-rr, cx+rr, cy+rr), fill=int(255 * (1 - k/60)))
    g = g.filter(ImageFilter.GaussianBlur(r/20))
    a = Image.new("RGBA", (W, H), outer); b = Image.new("RGBA", (W, H), inner); a.paste(b, (0,0), g); return a

def texto(d, xy, s, size, fill, stroke=(40, 20, 70), sw=None, anchor="mm"):
    f = ImageFont.truetype(FONT, size); sw = sw or max(4, size // 9)
    x, y = xy
    d.text((x, y + size*0.08), s, font=f, fill=stroke, anchor=anchor, stroke_width=sw, stroke_fill=stroke)
    d.text((x, y), s, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=stroke)

def estrella(d, cx, cy, r, col, rot=0):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45; a = rot + math.pi * i / 5 - math.pi/2
        pts.append((cx + rr*math.cos(a), cy + rr*math.sin(a)))
    d.polygon(pts, fill=col, outline=(40,20,70), width=max(2, int(r/7)))

def confeti(im, area, n, cols, rmin=10, rmax=26, evitar=None):
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = area
    for _ in range(n):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1)
        if evitar and evitar[0] < x < evitar[2] and evitar[1] < y < evitar[3]: continue
        r = random.uniform(rmin, rmax); c = random.choice(cols)
        if random.random() < 0.45: estrella(d, x, y, r, c, random.uniform(0, 6))
        else: d.ellipse((x-r*0.5, y-r*0.5, x+r*0.5, y+r*0.5), fill=c, outline=(40,20,70), width=3)

def ciudad(W, H, y_base, col, seed=3):
    r = random.Random(seed); im = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(im); x = 0
    while x < W:
        w = r.randint(90, 200); h = r.randint(120, 330)
        d.rounded_rectangle((x, y_base - h, x + w, H), radius=14, fill=col)
        for wy in range(y_base - h + 30, y_base - 20, 48):
            for wx in range(x + 22, x + w - 30, 42):
                if r.random() < 0.55: d.rounded_rectangle((wx, wy, wx + 20, wy + 26), radius=4, fill=(255, 226, 120, 230))
        x += w + r.randint(4, 20)
    return im

COLS = [(240,138,60), (91,143,224), (176,124,232), (108,194,106), (255,214,64), (255,95,120)]

def logo(width):
    """Logo 'ANIMAL CITY' + chapa 'TV' como imagen RGBA."""
    target = width; width = 2400; H = 700; im = Image.new("RGBA", (width, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    size = 240; f = ImageFont.truetype(FONT, size)
    letras = "ANIMAL CITY"; cols = [COLS[i % 4] for i in range(len(letras))]
    sw = size // 8; ws = [d.textlength(c, font=f) for c in letras]; tw = sum(ws) - 0  # sin tracking extra
    tv_w = size * 1.35; total = tw + size * 0.25 + tv_w; x = (width - total) / 2; y = H * 0.5
    pos = []
    for i, (c, w) in enumerate(zip(letras, ws)):
        pos.append((x, y + (-size * 0.06 if i % 2 else size * 0.04), c, cols[i])); x += w
    for px, py, c, col in pos:   # sombra y contorno primero, para que no tapen la letra de al lado
        if c != " ": d.text((px, py + size*0.09), c, font=f, fill=(40,20,70), anchor="lm", stroke_width=sw, stroke_fill=(40,20,70))
    for px, py, c, col in pos:
        if c != " ": d.text((px, py), c, font=f, fill=(255,255,255), anchor="lm", stroke_width=sw, stroke_fill=(40,20,70))
    for px, py, c, col in pos:
        if c != " ": d.text((px, py), c, font=f, fill=col, anchor="lm", stroke_width=max(2, sw//4), stroke_fill=(255,255,255))
    x += size * 0.25; bx0, by0, bx1, by1 = x, y - size*0.62, x + tv_w, y + size*0.58
    d.rounded_rectangle((bx0, by0 + size*0.09, bx1, by1 + size*0.09), radius=size*0.22, fill=(40,20,70))
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=size*0.22, fill=(255,70,90), outline=(40,20,70), width=sw)
    # antenas de tele
    d.line((bx0 + tv_w*0.35, by0, bx0 + tv_w*0.18, by0 - size*0.38), fill=(40,20,70), width=sw)
    d.line((bx0 + tv_w*0.65, by0, bx0 + tv_w*0.82, by0 - size*0.38), fill=(40,20,70), width=sw)
    for ax in (bx0 + tv_w*0.18, bx0 + tv_w*0.82):
        r = size*0.09; d.ellipse((ax-r, by0 - size*0.38 - r, ax+r, by0 - size*0.38 + r), fill=(255,214,64), outline=(40,20,70), width=sw//2)
    f2 = ImageFont.truetype(FONT, int(size * 0.78))
    d.text(((bx0+bx1)/2, (by0+by1)/2), "TV", font=f2, fill=(255,255,255), anchor="mm", stroke_width=sw//2, stroke_fill=(40,20,70))
    im = im.crop(im.getbbox()); return im.resize((target, int(im.height * target / im.width)), Image.LANCZOS)

def banner():
    W, H = 2560, 1440; sx0, sy0, sx1, sy1 = 507, 508, 2053, 931   # zona segura (todos los dispositivos)
    bg = degradado_radial(W, H, W/2, H/2, (255, 226, 92, 255), (255, 150, 60, 255), 1500)
    r = rayos(W, H, W/2, H/2 - 40, (0,0,0,0), (255, 255, 255, 55), n=36); bg.alpha_composite(r)
    bg.alpha_composite(ciudad(W, H, 1440 - 330, (120, 70, 190, 150), seed=5))
    bg.alpha_composite(ciudad(W, H, 1440 - 220, (90, 50, 150, 210), seed=11))
    confeti(bg, (0, 0, W, H), 160, COLS, 12, 30, evitar=(sx0 - 40, sy0 - 40, sx1 + 40, sy1 + 40))
    confeti(bg, (sx0 - 300, sy0 - 10, sx1 + 300, sy1 + 10), 26, COLS, 10, 20, evitar=(sx0 + 360, sy0, sx1 - 360, sy1))
    # personajes de busto, salen de abajo de la franja visible y se asoman a los lados del logo
    def busto(n, frac, h, flip=False):
        im = personaje(n, frac)
        if n == "mia": im = im.crop((0, 0, int(im.width * 0.74), im.height)); im = im.crop(im.getbbox())
        im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        return sombra(contorno(pad(im, 20), 10), (0, 14), 14, 120)
    teddy = busto("teddy", 0.62, 560); moe = busto("moe", 0.75, 400)
    nana = busto("nana", 0.72, 460); mia = busto("mia", 0.56, 530)
    y_bot = sy1 + 110
    bg.alpha_composite(teddy, (int(370 - teddy.width/2), y_bot - teddy.height + 50))
    bg.alpha_composite(moe, (int(610 - moe.width/2), y_bot - moe.height + 40))
    bg.alpha_composite(nana, (int(1975 - nana.width/2), y_bot - nana.height + 30))
    bg.alpha_composite(mia, (int(2290 - mia.width/2), y_bot - mia.height + 10))
    lg = logo(900); bg.alpha_composite(lg, (int(W/2 - lg.width/2), int(sy0 + 40)))
    d = ImageDraw.Draw(bg)
    # cinta con el lema
    cy = sy0 + 40 + lg.height + 75; tw = 760
    d.rounded_rectangle((W/2 - tw/2, cy - 48 + 10, W/2 + tw/2, cy + 48 + 10), radius=48, fill=(40,20,70))
    d.rounded_rectangle((W/2 - tw/2, cy - 48, W/2 + tw/2, cy + 48), radius=48, fill=(255,255,255), outline=(40,20,70), width=8)
    f = ImageFont.truetype(FONT, 62)
    d.text((W/2, cy + 2), "NEW CARTOON EVERY DAY!", font=f, fill=(255, 70, 90), anchor="mm")
    bg.convert("RGB").save(OUT / "banner.png", optimize=True)
    return bg

def avatar():
    S = 800; bg = degradado_radial(S, S, S/2, S/2, (255, 230, 100, 255), (255, 140, 50, 255), 560)
    bg.alpha_composite(rayos(S, S, S/2, S/2, (0,0,0,0), (255,255,255,60), n=24))
    confeti(bg, (40, 40, 760, 300), 14, COLS, 12, 22, evitar=(200, 60, 600, 800))
    t = personaje("teddy", 0.40)  # cabeza y hombros de Teddy
    t = t.resize((int(t.width * 700 / t.height), 700), Image.LANCZOS)
    t = sombra(contorno(pad(t, 20), 12), (0, 12), 12, 120)
    bg.alpha_composite(t, (int(S/2 - t.width/2 + 10), S - t.height + 150))
    d = ImageDraw.Draw(bg)
    # chapa TV abajo
    bx0, by0, bx1, by1 = 280, 662, 520, 772
    d.rounded_rectangle((bx0, by0 + 10, bx1, by1 + 10), radius=40, fill=(40,20,70))
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=40, fill=(255,70,90), outline=(40,20,70), width=10)
    texto(d, ((bx0+bx1)/2, (by0+by1)/2 + 2), "TV", 92, (255,255,255), sw=7)
    bg.convert("RGB").save(OUT / "avatar.png", optimize=True)
    m = Image.new("L", (S, S), 0); ImageDraw.Draw(m).ellipse((0, 0, S, S), fill=255)
    prev = Image.new("RGBA", (S, S), (0,0,0,0)); prev.paste(bg, (0, 0), m); return prev

if __name__ == "__main__":
    b = banner(); a = avatar()
    b.convert("RGB").resize((1280, 720)).save("/tmp/claude-0/-home-claude-shorts-curiosidades/c27c0128-e45f-51f8-8d4f-0c5f2c29b600/scratchpad/banner_prev.png")
    # previsualizacion con las zonas visibles
    p = b.copy(); d = ImageDraw.Draw(p)
    d.rectangle((0, 508, 2559, 931), outline=(0, 200, 255), width=6); d.rectangle((507, 508, 2053, 931), outline=(255, 0, 0), width=6)
    p.convert("RGB").resize((1280, 720)).save("/tmp/claude-0/-home-claude-shorts-curiosidades/c27c0128-e45f-51f8-8d4f-0c5f2c29b600/scratchpad/banner_zonas.png")
    a.save("/tmp/claude-0/-home-claude-shorts-curiosidades/c27c0128-e45f-51f8-8d4f-0c5f2c29b600/scratchpad/avatar_prev.png")
