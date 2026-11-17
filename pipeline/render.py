#!/usr/bin/env python3
"""Render a YouTube Short (1080x1920) from spec.json + voz.mp3 + words.json.

Usage: python3 render.py work/v01
Outputs: work/v01/short.mp4 and work/v01/thumb.jpg
"""
import json, math, os, subprocess, sys
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import cairosvg, io

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(HERE, "assets/Anton.ttf")
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
INTER_K = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
EMOJI_DIR = os.path.join(HERE, "assets/package/color/svg")
YELLOW = (255, 214, 10)


@lru_cache(None)
def font(path, size):
    return ImageFont.truetype(path, size)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


@lru_cache(None)
def emoji_img(ch, size):
    cps = [f"{ord(c):X}" for c in ch]
    cands = ["-".join(cps), "-".join(c for c in cps if c != "FE0F")]
    for name in cands:
        p = os.path.join(EMOJI_DIR, name + ".svg")
        if os.path.exists(p):
            png = cairosvg.svg2png(url=p, output_width=size, output_height=size)
            return Image.open(io.BytesIO(png)).convert("RGBA")
    raise SystemExit(f"emoji not found: {ch} {cands}")


def ease_out_back(x):
    x = max(0.0, min(1.0, x))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def fit_font(path, text, max_w, start):
    s = start
    while s > 40:
        f = font(path, s)
        if f.getlength(text) <= max_w:
            return f
        s -= 4
    return font(path, s)


def text_layer(text, f, fill, stroke=0, stroke_fill=(0, 0, 0), shadow=True):
    bbox = f.getbbox(text, stroke_width=stroke)
    w, h = bbox[2] - bbox[0] + 40, bbox[3] - bbox[1] + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((20 - bbox[0], 28 - bbox[1]), text, font=f, fill=(0, 0, 0, 150),
                                stroke_width=stroke, stroke_fill=(0, 0, 0, 150))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(8)))
        d = ImageDraw.Draw(im)
    d.text((20 - bbox[0], 20 - bbox[1]), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im


def paste_center(base, layer, cx, cy, scale=1.0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01:
        return
    if abs(scale - 1) > 1e-3:
        layer = layer.resize((max(1, int(layer.width * scale)), max(1, int(layer.height * scale))), Image.BICUBIC)
    if alpha < 0.999:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer = layer.copy()
        layer.putalpha(a)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def make_background(palette):
    c0, c1, c2 = (np.array(hexrgb(c), dtype=np.float32) for c in palette)
    y = np.linspace(0, 1, H + 200)[:, None, None]
    grad = c0 * (1 - y) + c1 * y
    bg = np.repeat(grad, W + 200, axis=1)
    img = Image.fromarray(bg.astype(np.uint8)).convert("RGBA")
    blobs = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(blobs)
    rng = np.random.default_rng(7)
    for _ in range(7):
        x, yy, r = rng.integers(0, W + 200), rng.integers(0, H + 200), rng.integers(180, 420)
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=tuple(int(v) for v in c2) + (60,))
    blobs = blobs.filter(ImageFilter.GaussianBlur(120))
    img = Image.alpha_composite(img, blobs)
    # subtle dotted grid
    g = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for gx in range(0, img.width, 60):
        for gy in range(0, img.height, 60):
            gd.ellipse((gx - 2, gy - 2, gx + 2, gy + 2), fill=(255, 255, 255, 18))
    return Image.alpha_composite(img, g)


def build_caption_chunks(words, max_chars=16):
    chunks, cur = [], []
    for w in words:
        if w.get("type") != "word" or w["text"].startswith("["):
            continue
        txt = w["text"]
        if cur and (sum(len(x["text"]) + 1 for x in cur) + len(txt) > max_chars or len(cur) >= 3):
            chunks.append(cur)
            cur = []
        cur.append(w)
        if txt[-1] in ".?!:,":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        end = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else c[-1]["end"] + 0.6
        out.append({"words": c, "start": c[0]["start"], "end": end})
    return out


def clean(t):
    return t.strip(".,:;").upper()


def draw_captions(frame, chunk, t):
    f = font(ANTON, 118)
    words = [clean(w["text"]) for w in chunk["words"]]
    space = f.getlength(" ") * 1.6
    widths = [f.getlength(w) for w in words]
    total = sum(widths) + space * (len(words) - 1)
    if total > W - 120:
        f = font(ANTON, int(118 * (W - 120) / total))
        space = f.getlength(" ") * 1.6
        widths = [f.getlength(w) for w in words]
        total = sum(widths) + space * (len(words) - 1)
    x = (W - total) / 2
    cy = 1430
    pop = ease_out_back((t - chunk["start"]) / 0.18)
    for w, wd, src in zip(words, widths, chunk["words"]):
        active = src["start"] <= t < max(src["end"], src["start"] + 0.15)
        spoken = t >= src["start"]
        fill = YELLOW if active else ((255, 255, 255) if spoken else (255, 255, 255))
        lay = text_layer(w, f, fill, stroke=9)
        sc = 0.85 + 0.15 * pop
        paste_center(frame, lay, x + wd / 2, cy, scale=sc)
        x += wd + space


def render(workdir):
    spec = json.load(open(os.path.join(workdir, "spec.json")))
    words = json.load(open(os.path.join(workdir, "words.json")))["words"]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", os.path.join(workdir, "voz.mp3")]).strip()) + 0.4
    nframes = int(dur * FPS)
    bg = make_background(spec["palette"])
    accent = hexrgb(spec["palette"][2])
    chunks = build_caption_chunks(words)
    beats = spec["beats"]

    # pre-render beat layers
    beat_layers = []
    for b in beats:
        big = text_layer(b["big"], fit_font(ANTON, b["big"], W - 140, 190), YELLOW, stroke=10)
        small = text_layer(b["small"].upper(), fit_font(INTER_K, b["small"].upper(), W - 160, 58), (255, 255, 255), stroke=5)
        beat_layers.append((emoji_img(b["emoji"], 470), big, small))

    cat_f = font(INTER_K, 42)
    cat_txt = "¿SABÍAS QUE...?  ·  " + spec["categoria"]
    cat_w = int(cat_f.getlength(cat_txt)) + 70
    pill = Image.new("RGBA", (cat_w, 86), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle((0, 0, cat_w - 1, 85), radius=43, fill=(0, 0, 0, 130), outline=accent + (255,), width=4)
    pd.text((35, 18), cat_txt, font=cat_f, fill=(255, 255, 255))

    out = os.path.join(workdir, "short.tmp.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", os.path.join(workdir, "voz.mp3"),
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-af", "apad", "-c:a", "aac", "-b:a", "160k", "-t", f"{nframes / FPS:.3f}", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    thumb_frame = None
    for i in range(nframes):
        t = i / FPS
        ox = 100 + 60 * math.sin(t * 0.25)
        oy = 100 + 80 * math.cos(t * 0.18)
        frame = bg.crop((int(ox), int(oy), int(ox) + W, int(oy) + H))

        paste_center(frame, pill, W / 2, 230)

        # current beat
        bi = max([k for k, b in enumerate(beats) if b["t"] <= t] or [0])
        b = beats[bi]
        lt = t - b["t"] if t >= b["t"] else 1.0
        if i == 0:
            lt = 1.0  # first frame fully drawn (it is the Shorts preview)
        em, big, small = beat_layers[bi]
        glow_r = 300 + 12 * math.sin(t * 3)
        glow = Image.new("RGBA", (int(glow_r * 2.4), int(glow_r * 2.4)), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse((glow.width / 2 - glow_r, glow.height / 2 - glow_r,
                                      glow.width / 2 + glow_r, glow.height / 2 + glow_r), fill=accent + (70,))
        glow = glow.filter(ImageFilter.GaussianBlur(50))
        paste_center(frame, glow, W / 2, 640)
        float_y = 12 * math.sin(t * 2.2)
        paste_center(frame, em, W / 2, 640 + float_y, scale=ease_out_back(lt / 0.45), alpha=min(1, lt / 0.15))
        paste_center(frame, big, W / 2, 1000 + 40 * (1 - ease_out(lt / 0.35)), scale=0.7 + 0.3 * ease_out_back((lt - 0.08) / 0.35),
                     alpha=min(1, max(0, (lt - 0.05) / 0.2)))
        paste_center(frame, small, W / 2, 1150, alpha=min(1, max(0, (lt - 0.2) / 0.25)))

        # captions
        ch = next((c for c in chunks if c["start"] <= t < c["end"]), None)
        if ch:
            draw_captions(frame, ch, t)

        # progress bar
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((80, 1600, W - 80, 1612), radius=6, fill=(255, 255, 255, 60))
        d.rounded_rectangle((80, 1600, 80 + (W - 160) * (i / nframes), 1612), radius=6, fill=YELLOW + (255,))

        rgb = frame.convert("RGB")
        if i == 0:
            thumb_frame = rgb
        ff.stdin.write(rgb.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit("ffmpeg failed")
    os.replace(out, os.path.join(workdir, "short.mp4"))
    make_thumb(spec, bg, beat_layers[0][0], workdir)
    print("ok", workdir, f"{dur:.1f}s")


def make_thumb(spec, bg, em, workdir):
    """Vertical thumbnail with the hook, for review / custom thumbnail."""
    im = bg.crop((100, 100, 100 + W, 100 + H))
    paste_center(im, em.resize((620, 620)), W / 2, 760)
    words = spec["hook"].upper().split()
    lines, cur = [], ""
    f = font(ANTON, 150)
    for w in words:
        test = (cur + " " + w).strip()
        if f.getlength(test) > W - 120 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    lines.append(cur)
    y = 1220
    for k, ln in enumerate(lines):
        paste_center(im, text_layer(ln, f, YELLOW if k == len(lines) - 1 else (255, 255, 255), stroke=12), W / 2, y)
        y += 170
    im.convert("RGB").save(os.path.join(workdir, "thumb.jpg"), quality=92)


def preview(workdir, times):
    """Debug: render single frames at given times to PNGs (no video)."""
    raise NotImplementedError


if __name__ == "__main__":
    render(sys.argv[1])
