#!/usr/bin/env python3
"""Descarga una foto de Wikimedia Commons para cada beat de spec.json.

Cada beat puede llevar:
  "foto":   título exacto de un archivo de Commons ("File:Tour Eiffel ....jpg")  -> se usa ese
  "buscar": términos de búsqueda (mejor en inglés)                              -> se elige el mejor resultado
Guarda work/vNN/img/beat_K.jpg y work/vNN/creditos.json (autor, licencia, url) para la descripción.

Uso: python3 fetch_images.py work/v02
"""
import json, os, sys, time, urllib.parse, urllib.request, re

API = "https://commons.wikimedia.org/w/api.php"
UA = "ShortsCuriosidadesBot/1.0 (https://github.com/ch1qu1t1t0tumadre-eng/shorts-curiosidades)"
OK_LIC = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? ?[0-9.]*)", re.I)


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except Exception as e:
            if i == 2:
                raise
            time.sleep(2)


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def candidates(beat):
    base = {"action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url|size|extmetadata|mime", "iiurlwidth": "1600"}
    if beat.get("foto"):
        q = dict(base, titles=beat["foto"])
    else:
        q = dict(base, generator="search", gsrnamespace="6", gsrlimit="20",
                 gsrsearch=beat["buscar"] + " filetype:bitmap")
    d = get(API + "?" + urllib.parse.urlencode(q))
    pages = list(d.get("query", {}).get("pages", {}).values())
    pages.sort(key=lambda p: p.get("index", 0))
    out = []
    for p in pages:
        if "imageinfo" not in p:
            continue
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = strip_html(m.get("LicenseShortName", {}).get("value", ""))
        if ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        if not OK_LIC.match(lic):
            continue
        if ii.get("width", 0) < 900 and not beat.get("foto"):
            continue
        out.append({
            "title": p["title"], "url": ii.get("thumburl") or ii["url"], "page": ii.get("descriptionurl"),
            "license": lic, "author": strip_html(m.get("Artist", {}).get("value", ""))[:80],
            "w": ii["width"], "h": ii["height"],
        })
    return out


def main(workdir):
    spec_path = os.path.join(workdir, "spec.json")
    spec = json.load(open(spec_path))
    os.makedirs(os.path.join(workdir, "img"), exist_ok=True)
    creditos, used = [], set()
    for k, b in enumerate(spec["beats"]):
        if not (b.get("foto") or b.get("buscar")):
            continue
        cands = [c for c in candidates(b) if c["title"] not in used]
        if not cands:
            print(f"beat {k}: sin resultados para {b.get('foto') or b.get('buscar')!r}")
            continue
        c = cands[0]
        used.add(c["title"])
        dst = os.path.join(workdir, "img", f"beat_{k}.jpg")
        open(dst, "wb").write(get(c["url"], binary=True))
        b["img"] = f"img/beat_{k}.jpg"
        creditos.append({"beat": k, **c})
        print(f"beat {k}: {c['title']} [{c['license']}] {c['author']}")
        time.sleep(0.5)
    json.dump(spec, open(spec_path, "w"), ensure_ascii=False, indent=2)
    json.dump(creditos, open(os.path.join(workdir, "creditos.json"), "w"), ensure_ascii=False, indent=2)
    # texto de créditos para la descripción (obligatorio en CC BY / CC BY-SA)
    lines = [f"Imagen: {c['author'] or 'Wikimedia Commons'} / {c['license']} / Wikimedia Commons"
             for c in creditos if not re.match(r"^(cc0|public domain|pd)", c["license"], re.I)]
    open(os.path.join(workdir, "creditos.txt"), "w").write("\n".join(dict.fromkeys(lines)))


if __name__ == "__main__":
    main(sys.argv[1])
