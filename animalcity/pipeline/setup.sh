#!/usr/bin/env bash
# Prepara el entorno de AnimalCity TV (usa también los recursos de ../../pipeline).
set -euo pipefail
cd "$(dirname "$0")"
bash ../../pipeline/setup.sh
pip install --break-system-packages -q cairocffi pillow numpy 2>/dev/null
mkdir -p ~/.local/share/fonts
cp ../../pipeline/assets/Anton.ttf ~/.local/share/fonts/ 2>/dev/null || true
cp assets/LilitaOne-Regular.ttf ~/.local/share/fonts/ 2>/dev/null || true
fc-cache -f >/dev/null 2>&1 || true
python3 -c "import cairocffi, cairosvg, numpy, PIL; print('animalcity setup ok')"
