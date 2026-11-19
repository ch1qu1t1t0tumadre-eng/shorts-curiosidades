#!/usr/bin/env python3
"""Hoja de contacto de previews: python3 pipeline/hoja.py work/vNN t1 t2 ... -> /tmp/hoja_vNN.png"""
import subprocess, sys, os, glob
from PIL import Image
d, ts = sys.argv[1], sys.argv[2:]
for f in glob.glob(os.path.join(d, "prev_*.png")):
    os.remove(f)
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "anim.py"), d, "preview", *ts], check=True,
               stdout=subprocess.DEVNULL)
fs = sorted(glob.glob(os.path.join(d, "prev_*.png")), key=lambda f: float(os.path.basename(f)[5:-4]))
ims = [Image.open(f).resize((216, 384)) for f in fs]
cols = 8
rows = (len(ims) + cols - 1) // cols
s = Image.new("RGB", (216 * cols, 384 * rows))
for i, im in enumerate(ims):
    s.paste(im, ((i % cols) * 216, (i // cols) * 384))
out = f"/tmp/hoja_{os.path.basename(d.rstrip('/'))}.png"
s.save(out)
for f in glob.glob(os.path.join(d, "prev_*.png")):
    os.remove(f)
print(out)
