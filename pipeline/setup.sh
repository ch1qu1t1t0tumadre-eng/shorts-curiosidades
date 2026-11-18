#!/usr/bin/env bash
# Prepara el entorno para render.py (emojis OpenMoji, fuente Anton, librerías Python).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets
cd assets
if [ ! -d package/color/svg ]; then
  npm pack openmoji@17 --silent >/dev/null 2>&1
  tar xzf openmoji-*.tgz package/color/svg
fi
if [ ! -f Anton.ttf ]; then
  npm pack @fontsource/anton --silent >/dev/null 2>&1
  tar xzf fontsource-anton-*.tgz package/files/anton-latin-400-normal.woff --transform 's|package/files/||'
fi
pip install --break-system-packages -q cairosvg fonttools brotli pillow numpy 2>/dev/null
python3 -c "
import os
from fontTools.ttLib import TTFont
if not os.path.exists('Anton.ttf'):
    f = TTFont('anton-latin-400-normal.woff'); f.flavor = None; f.save('Anton.ttf')
"
echo "setup ok"
