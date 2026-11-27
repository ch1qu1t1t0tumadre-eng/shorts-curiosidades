"""Análisis de retención de UN Short ya publicado: mejores y peores momentos, con lo que se decía y se veía.

Uso:
  python3 pipeline/analizar_retencion.py work/vNN curva.json [ID_YOUTUBE] [stayed%] [vistas]
    curva.json = lista de % de retención en puntos equiespaciados de 0 % a 100 % del vídeo
                 (sale de pipeline/studio_curva.js pegado en la página de Estadísticas del vídeo en Studio).
Escribe analisis/vNN.md y añade una fila a analisis/registro.md.

Qué mide (por cada segundo):
  caída = retención(t) - retención(t+1)   (puntos que se van en ese segundo)
  - PEORES momentos: los 3 segundos con más caída (sin contar el segundo 0, donde siempre cae, ni el final).
  - MEJORES momentos: las 3 ventanas de 3 s (sin gancho ni final) donde menos gente se va (o la curva sube).
Para cada momento da: frase dicha (words.json), escena activa (con su comentario de escenas.py) y tipo de tramo
(gancho, planteamiento, burla, rival, escalada, explicación, analogía, in-other-words, cierre/bucle).
"""
import json
import os
import re
import sys

d = sys.argv[1]
curva = json.load(open(sys.argv[2]))
vid = sys.argv[3] if len(sys.argv) > 3 else ""
stayed = sys.argv[4] if len(sys.argv) > 4 else ""
vistas = sys.argv[5] if len(sys.argv) > 5 else ""
name = os.path.basename(os.path.normpath(d))
words = [w for w in json.load(open(os.path.join(d, "words.json")))["words"] if w.get("type", "word") == "word"
         and not w["text"].startswith("[")]
dur = words[-1]["end"]
src = open(os.path.join(d, "escenas.py")).read()

# escenas (en tiempo original) + CORTES
m = re.search(r"ESCENAS\s*=\s*\[(.*?)\]\s*\n", src, re.S)
esc = [(float(t), f) for t, f in re.findall(r"\(([\d.]+),\s*(e\d+)\)", m.group(1))] if m else []
cortes = [(float(a), float(b)) for a, b in re.findall(r"\(([\d.]+),\s*([\d.]+)\)", (re.search(r"CORTES\s*=\s*\[(.*?)\]", src) or [None, ""])[1] if re.search(r"CORTES\s*=\s*\[(.*?)\]", src) else "")]


def old_t(t):
    for a, b in sorted(cortes):
        if t >= a:
            t += b - a
    return t


def comentario(fn):
    mm = re.search(r"#\s*([\d.]+)\s+(\"[^\n]*)\n(?:@[^\n]*\n)*def " + fn + r"\(", src)
    return mm.group(2)[:110] if mm else ""


def escena(t):
    to = old_t(t)
    act = [e for e in esc if e[0] <= to]
    return act[-1][1] if act else "e1"


def frase(t0, t1):
    return " ".join(w["text"] for w in words if w["end"] > t0 and w["start"] < t1)


TIPOS = [("gancho", r"on purpose|^This"), ("planteamiento", r"\bSee,|two (companies|crews|teams)"),
         ("burla", r"\bKid,|boss"), ("rival", r"other (company|crew|team)|loves|perfect"),
         ("explicación", r"You see"), ("analogía", r"\bLike\b|just like"), ("in-other-words", r"In other words"),
         ("cierre/bucle", r"That's why|Because")]


def tipo(t):
    # último marcador dicho antes de t
    best, bt = "escalada", -1
    for w_i, w in enumerate(words):
        if w["start"] > t + 0.3:
            break
        ctx = " ".join(x["text"] for x in words[max(0, w_i - 1):w_i + 2])
        for nom, rx in TIPOS:
            if re.search(rx, ctx) and w["start"] >= bt:
                best, bt = nom, w["start"]
    if t < 3.2:
        return "gancho"
    return best


n = len(curva)
seg = []  # retención por segundo
for s in range(int(dur) + 1):
    x = min(s / dur, 1.0) * (n - 1)
    i = int(x); f = x - i
    seg.append(curva[i] if i + 1 >= n else curva[i] * (1 - f) + curva[i + 1] * f)
caidas = [(seg[s] - seg[s + 1], s) for s in range(len(seg) - 1)]
peores = sorted([c for c in caidas if 1 <= c[1] <= len(seg) - 4], reverse=True)[:3]
# mejores tramos: ventanas de 3 s (sin el gancho ni el final) donde menos gente se va, sin solaparse
ventanas = sorted((seg[s] - seg[s + 3], s) for s in range(3, len(seg) - 6))
buenos = []
for drop, s in ventanas:
    if all(abs(s - a) >= 3 for a, _ in buenos):
        buenos.append((s, s + 3))
    if len(buenos) == 3:
        break
L = [f"# Retención de {name} {('(' + vid + ')') if vid else ''}", "",
     f"Duración {dur:.1f} s · se quedaron {stayed or '?'} % · vistas {vistas or '?'} · retención en 3 s {seg[3]:.0f} % · "
     f"a mitad {seg[len(seg) // 2]:.0f} % · al final {seg[-2]:.0f} %", "", "## Peores momentos (más gente se va)"]
for drop, s in peores:
    fn = escena(s + 0.5)
    L.append(f"- **s{s}–{s + 1}: −{drop:.1f} puntos** · tramo *{tipo(s)}* · voz: “{frase(s - 0.5, s + 1.5)}” · escena {fn} {comentario(fn)}")
L += ["", "## Mejores momentos (la curva aguanta o sube)"]
for a, b in buenos:
    fn = escena((a + b) / 2)
    L.append(f"- **s{a}–{b}: pierde {seg[a] - seg[b]:.1f} puntos en {b - a} s** · tramo *{tipo(a)}* · voz: “{frase(a, b)[:160]}” · escena {fn} {comentario(fn)}")
if not buenos:
    L.append("- (ningún tramo de ≥3 s aguanta: la curva cae todo el rato)")
L += ["", "## Retención por segundo", "", " ".join(f"{s}:{v:.0f}" for s, v in enumerate(seg)), ""]
os.makedirs("analisis", exist_ok=True)
open(f"analisis/{name}.md", "w").write("\n".join(L))
reg = "analisis/registro.md"
if not os.path.exists(reg):
    open(reg, "w").write("# Registro de retención (una fila por Short publicado)\n\n| vídeo | ID | se quedaron | vistas | ret. 3 s | ret. final | peor tramo | mejor tramo |\n|---|---|---|---|---|---|---|---|\n")
pt = f"s{peores[0][1]} {tipo(peores[0][1])} (−{peores[0][0]:.0f})" if peores else ""
bt = f"s{buenos[0][0]}–{buenos[0][1]} {tipo(buenos[0][0])}" if buenos else "—"
open(reg, "a").write(f"| {name} | {vid} | {stayed} | {vistas} | {seg[3]:.0f} | {seg[-2]:.0f} | {pt} | {bt} |\n")
print("\n".join(L))
