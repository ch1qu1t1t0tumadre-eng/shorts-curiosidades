"""Miniatura: The giant Moon on the horizon is a lie (youtube.com/shorts/7KQSDqq4Xj8).
No desvela la explicación (cerebro/test del meñique): Luna gigante + 'IT'S A LIE'."""
from escenas_ilusion_luna_en import *  # noqa


def MINIATURA(ctx):
    T = 0.5
    ctx.save()
    camera(ctx, 1.0, W / 2, 960)
    bg_dusk(ctx, T)
    moon(ctx, W / 2, 1060, 420)
    skyline(ctx, 1420, T)
    ctx.restore()
    thumb_vignette(ctx, 0.5)
    thumb_text(ctx, ["THIS MOON", ("IS A LIE", WHITE)], y=280, size=180)
    thumb_arrow(ctx, 110, 1640, 330, 1030)
    thumb_text(ctx, ["LOOK AGAIN"], y=1740, size=130, rot=0.03)
