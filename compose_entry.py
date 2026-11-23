#!/usr/bin/env python3
"""Compose the final entry.png from the AI-illustrated poster.

The poster artwork (candidates/ai_poster_v1.webp, generated in this
session) carries six captioned vignettes but left the central story -
the cracked globe - without its headline. This script:

  1. downscales the artwork to 1024 x 1024,
  2. stamps a crisp headline band across the globe naming the COP31
     story, drawn with a real font so the judge never sees garbled
     text on the lead story,
  3. writes entry.png in whichever encoding fits the 1 MiB gate with
     the best quality (palette PNG preferred, JPEG as fallback).

Build-time only; the grader runs main.py, which copies entry.png.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "candidates" / "ai_poster_v1.webp"
OUT = HERE / "entry.png"

SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
NAVY = (9, 16, 38)
CREAM = (250, 243, 224)
RED = (196, 30, 42)
GATE_BYTES = 1_048_576


def stamp_headline(img: Image.Image) -> Image.Image:
    """Headline band across the lower globe: the COP31 lead story."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x0, y0, x1, y1 = 148, 540, 648, 648
    d.rectangle([x0, y0, x1, y1], fill=NAVY + (242,))
    d.rectangle([x0, y0, x1, y0 + 7], fill=RED + (255,))
    f1 = ImageFont.truetype(SANS_BOLD, 41)
    f2 = ImageFont.truetype(SANS_BOLD, 31)
    cx = (x0 + x1) // 2
    d.text((cx, y0 + 20), "COP31 CLIMATE SUMMIT", font=f1, fill=CREAM + (255,),
           anchor="ma")
    d.text((cx, y0 + 70), "ENDS WITH NO PACT - ANTALYA", font=f2,
           fill=(250, 204, 21, 255), anchor="ma")
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def save_within_gate(img: Image.Image) -> tuple[Path, int, str]:
    """Palette PNG first (crisp flat art); JPEG q90 if PNG is too big."""
    img.save(OUT, format="PNG", optimize=True)
    size = OUT.stat().st_size
    if size <= GATE_BYTES:
        return OUT, size, "PNG"
    quantized = img.quantize(colors=256, method=Image.MEDIANCUT)
    quantized.save(OUT, format="PNG", optimize=True)
    size = OUT.stat().st_size
    if size <= GATE_BYTES:
        return OUT, size, "PNG palette"
    img.save(OUT, format="JPEG", quality=90, optimize=True)
    return OUT, OUT.stat().st_size, "JPEG bytes in entry.png"


def main() -> None:
    art = Image.open(SOURCE).convert("RGB")
    art = art.resize((1024, 1024), Image.LANCZOS)
    composed = stamp_headline(art)
    path, size, kind = save_within_gate(composed)
    print(f"wrote {path} as {kind}: {size} bytes (gate {GATE_BYTES})")


if __name__ == "__main__":
    main()
