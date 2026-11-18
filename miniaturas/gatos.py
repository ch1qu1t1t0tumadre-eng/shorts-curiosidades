"""Miniatura: Why your cat never bumps into things in the dark (youtube.com/shorts/iz6iLIY8lpc).
No desvela el secreto (bigotes): solo la habitación a oscuras, obstáculos y el gato pasando entre ellos."""
from escenas_gatos_oscuridad_en import *  # noqa


def MINIATURA(ctx):
    T = 0.7
    ctx.save()
    camera(ctx, 1.12, W / 2, 1150)
    room_dark(ctx, T)
    chair(ctx, 250, 1520)
    chair(ctx, 900, 1520)
    cat(ctx, W / 2, 1120, 1.25, T, eyes="glow", pupil=1.0, look=(0, 0))
    ctx.restore()
    thumb_vignette(ctx, 0.7)
    thumb_text(ctx, ["LIGHTS OFF.", ("ZERO CRASHES.", WHITE)], y=290, size=165)
    thumb_text(ctx, ["HOW?!"], y=1720, size=190, rot=0.03)
