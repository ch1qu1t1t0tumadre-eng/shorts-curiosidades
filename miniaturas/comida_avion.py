"""Miniatura: Why airplane food tastes so bland (youtube.com/shorts/rThYV9s7zHA).
No desvela la causa (aire seco/ruido) ni la bebida (zumo de tomate): bandeja de avión + vaso misterioso."""
from escenas_comida_avion_en import *  # noqa


def MINIATURA(ctx):
    T = 0.9
    ctx.save()
    camera(ctx, 1.0, W / 2, 960)
    bg_sky(ctx, T)
    for k in range(3):
        x = k * 420 - 80
        for dx, rr in ((0, 80), (70, 110), (150, 75)):
            circle(ctx, x + dx, 560 + k * 70, rr)
        fill(ctx, WHITE, 0.7)
    tray(ctx, W / 2 - 60, 1240, 0.95, T, steam=1.0)
    glass(ctx, 860, 1060, 0.9, mystery=True, glow=1.0, T=T)
    ctx.restore()
    thumb_vignette(ctx, 0.45)
    thumb_text(ctx, ["IT'S NOT", ("THE CHEF", WHITE)], y=270, size=190)
    thumb_circle(ctx, 860, 1060, 170, 230)
    thumb_arrow(ctx, 520, 1720, 760, 1310)
