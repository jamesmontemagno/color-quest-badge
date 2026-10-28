"""Rebuild Color Quest's original palette-and-sparkle launcher icon."""

from pathlib import Path

from PIL import Image, ImageDraw


def build():
    scale = 4
    icon = Image.new("RGB", (48 * scale, 48 * scale), (238, 233, 252))
    draw = ImageDraw.Draw(icon)

    def ellipse(bounds, fill):
        draw.ellipse(tuple(int(v * scale) for v in bounds), fill=fill)

    draw.rounded_rectangle((0, 0, 47 * scale, 47 * scale), 10 * scale,
                           fill=(112, 75, 196))
    ellipse((5, 7, 42, 43), (40, 42, 69))
    ellipse((7, 9, 40, 41), (255, 253, 247))
    ellipse((27, 24, 42, 39), (112, 75, 196))
    for bounds, color in (
        ((13, 14, 21, 22), (245, 76, 100)),
        ((24, 13, 32, 21), (255, 215, 72)),
        ((10, 25, 18, 33), (75, 156, 245)),
        ((20, 29, 27, 36), (56, 184, 131)),
    ):
        ellipse(bounds, color)
    draw.polygon([(35 * scale, 3 * scale), (38 * scale, 9 * scale),
                  (44 * scale, 12 * scale), (38 * scale, 15 * scale),
                  (35 * scale, 21 * scale), (32 * scale, 15 * scale),
                  (26 * scale, 12 * scale), (32 * scale, 9 * scale)],
                 fill=(255, 215, 72))
    target = Path(__file__).resolve().parents[1] / "badge/apps/color_quest/icon.png"
    icon.resize((24, 24), Image.Resampling.LANCZOS).quantize(colors=64).save(target)
    print(target)


if __name__ == "__main__":
    build()
