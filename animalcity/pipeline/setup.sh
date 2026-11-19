#!/usr/bin/env bash
# Prepara el entorno de AnimalCity TV (usa también los recursos de ../../pipeline).
set -euo pipefail
cd "$(dirname "$0")"
bash ../../pipeline/setup.sh
pip install --break-system-packages -q cairocffi pillow numpy scipy skia-python opencv-python-headless kokoro-onnx soundfile pyworld librosa 2>/dev/null
# voces propias (Kokoro-82M, Apache 2.0): el modelo se descarga de GitHub una vez
mkdir -p modelos
[ -s modelos/kokoro-v1.0.onnx ] || curl -sSfL -o modelos/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s modelos/voices-v1.0.bin ] || curl -sSfL -o modelos/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
mkdir -p ~/.local/share/fonts
cp ../../pipeline/assets/Anton.ttf ~/.local/share/fonts/ 2>/dev/null || true
cp assets/LilitaOne-Regular.ttf ~/.local/share/fonts/ 2>/dev/null || true
fc-cache -f >/dev/null 2>&1 || true
python3 -c "import cairocffi, cairosvg, numpy, PIL, skia, cv2, scipy, kokoro_onnx, pyworld, soundfile; print('animalcity setup ok')"
