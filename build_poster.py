#!/usr/bin/env python3
"""Build the entry image for make.fun news-image-20261123.

Draws a one-page newspaper poster that sums up the world news of
Monday 23 November 2026 and writes it to entry.png beside this file.

Layout (1024 x 1024):
  masthead  - "THE WORLD IN ONE DAY" + the date, spelled out in full
  lead      - COP31 in Antalya ends with no climate pact
  grid      - six tiles: NATO, Hormuz/Bahrain, Cikande, Seoul,
              Nepal-India, Wellington cricket
  ticker    - three one-line stories along the bottom

Only used at build time on the author's machine (needs Pillow and
system fonts). The submitted program, main.py, uses the standard
library only and simply copies the finished entry.png to /output.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28

PAPER = (247, 242, 231)
INK = (20, 26, 38)
MUTED = (84, 90, 102)
RED = (178, 30, 30)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    """Greedy word wrap so no headline ever overflows its panel."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_width, line_gap=4):
    x, y = xy
    ascent, descent = fnt.getmetrics()
    step = ascent + descent + line_gap
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def draw_block(draw, xy, text, font_path, size, fill, max_width, max_height,
               line_gap=3, min_size=16):
    """Draw wrapped text, shrinking the font until the block fits the box.

    Returns the y just past the last line. This is the guard that keeps
    every headline and sub-line inside its panel at any text length.
    """
    size_now = size
    while size_now > min_size:
        fnt = font(font_path, size_now)
        lines = wrap(draw, text, fnt, max_width)
        ascent, descent = fnt.getmetrics()
        step = ascent + descent + line_gap
        if step * len(lines) <= max_height:
            break
        size_now -= 1
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


# ---------------------------------------------------------------- icons

def icon_globe_crack(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    crack = [(cx - 6, cy - r), (cx + 10, cy - r // 3), (cx - 8, cy + 2),
             (cx + 12, cy + r // 2), (cx + 2, cy + r)]
    draw.line(crack, fill=RED, width=6, joint="curve")


def icon_shield_star(draw, cx, cy, s, color):
    draw.polygon([(cx, cy - s), (cx + s // 3, cy - s // 3), (cx + s, cy),
                  (cx + s // 3, cy + s // 3), (cx, cy + s),
                  (cx - s // 3, cy + s // 3), (cx - s, cy),
                  (cx - s // 3, cy - s // 3)], fill=color)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=PAPER)


def icon_tanker(draw, cx, cy, s, color):
    hull_y = cy + 2
    draw.polygon([(cx - s, hull_y), (cx + s, hull_y), (cx + s - 10, hull_y + 15),
                  (cx - s + 10, hull_y + 15)], fill=color)
    draw.rectangle([cx - s + 12, hull_y - 11, cx - 4, hull_y], fill=color)
    draw.rectangle([cx + 12, hull_y - 18, cx + 24, hull_y], fill=color)
    for i in range(3):
        x0 = cx - s + 2 + i * 18
        draw.arc([x0, hull_y + 14, x0 + 30, hull_y + 30], 0, 180, fill=color, width=3)


def icon_factory_flame(draw, cx, cy, s, color):
    base = cy + 20
    draw.rectangle([cx - s, base - 20, cx + s, base], fill=color)
    draw.polygon([(cx - s, base - 20), (cx - s // 3, base - 36),
                  (cx + s // 4, base - 20)], fill=color)
    draw.rectangle([cx + s // 2, base - 50, cx + s // 2 + 10, base - 20], fill=color)
    flame = [(cx - 9, base - 20), (cx, base - 52), (cx + 10, base - 20),
             (cx + 4, base - 30), (cx, base - 40), (cx - 4, base - 30)]
    draw.polygon(flame, fill=RED)


def icon_phone_ai(draw, cx, cy, s, color):
    draw.rounded_rectangle([cx - 24, cy - s, cx + 24, cy + s],
                           radius=10, outline=color, width=5)
    draw.line([cx - 10, cy + s - 14, cx + 10, cy + s - 14], fill=color, width=4)
    f = font(SANS_BOLD, 30)
    draw.text((cx, cy - 26), "AI", font=f, fill=RED, anchor="ma")


def icon_mountains_flags(draw, cx, cy, s, color):
    draw.polygon([(cx - s, cy + s // 2), (cx - s // 3, cy - s // 2),
                  (cx + s // 5, cy + s // 2)], outline=color, width=5)
    draw.polygon([(cx - s // 5, cy + s // 2), (cx + s // 2, cy - s // 3),
                  (cx + s, cy + s // 2)], outline=color, width=5)
    draw.line([cx, cy - s, cx, cy - s // 4], fill=RED, width=5)
    draw.polygon([(cx, cy - s), (cx + 30, cy - s + 10), (cx, cy - s + 20)], fill=RED)


def icon_cricket(draw, cx, cy, s, color):
    draw.line([cx - 16, cy + 22, cx + 8, cy - 20], fill=color, width=11)
    draw.ellipse([cx + 8, cy + 4, cx + 30, cy + 26], fill=RED)
    draw.arc([cx + 12, cy + 7, cx + 26, cy + 23], 100, 260, fill=WHITE, width=2)


ICONS = {
    "nato": icon_shield_star,
    "hormuz": icon_tanker,
    "cikande": icon_factory_flame,
    "seoul": icon_phone_ai,
    "nepal": icon_mountains_flags,
    "cricket": icon_cricket,
}


# ---------------------------------------------------------------- tiles

TILES = [
    {
        "icon": "nato", "color": (29, 64, 140), "kicker": "BRUSSELS - NATO",
        "headline": "NATO holds emergency meeting",
        "sub": "Russian missiles fell in Poland; allies weigh eastern air defence",
    },
    {
        "icon": "hormuz", "color": (14, 99, 117), "kicker": "HORMUZ - BAHRAIN",
        "headline": "Bahrain takes Iran strike to the UN",
        "sub": "Tankers hit in the strait; Manama demands UN Security Council action",
    },
    {
        "icon": "cikande", "color": (154, 52, 18), "kicker": "CIKANDE - INDONESIA",
        "headline": "Search resumes at burned factory",
        "sub": "Candy plant fire: 3 confirmed dead, dozens of workers still missing",
    },
    {
        "icon": "seoul", "color": (88, 28, 135), "kicker": "SEOUL - S. KOREA",
        "headline": "Education minister quits over AI cheating",
        "sub": "Choi Kyo-jin resigns amid exam chaos; 111 device-cheating cases caught",
    },
    {
        "icon": "nepal", "color": (21, 101, 52), "kicker": "NEW DELHI - NEPAL",
        "headline": "Nepal PM Shah meets Modi today",
        "sub": "First bilateral visit: energy, trade and connectivity on the agenda",
    },
    {
        "icon": "cricket", "color": (161, 98, 7), "kicker": "WELLINGTON - CRICKET",
        "headline": "India pile up record 720 for 9",
        "sub": "Pant and Rahul centuries; India declare 352 runs ahead of New Zealand",
    },
]

TICKER = (
    "NIGERIA: 24 dead as funeral boat capsizes in Bayelsa  •  "
    "BALTIC: Russian cargo ship burns off Finland after drone strike  •  "
    "BANGLADESH: homes torched amid unrest and shutdown call"
)


def masthead(draw):
    draw.rectangle([0, 0, W, 148], fill=INK)
    f_kicker = font(SERIF_BOLD, 47)
    draw.text((W // 2, 16), "THE WORLD IN ONE DAY", font=f_kicker,
              fill=WHITE, anchor="ma")
    f_date = font(SANS_BOLD, 44)
    draw.text((W // 2, 84), "MONDAY  23 NOVEMBER 2026", font=f_date,
              fill=(250, 204, 21), anchor="ma")
    draw.rectangle([0, 148, W, 156], fill=RED)


def lead_story(draw):
    x0, y0, x1, y1 = MARGIN, 172, W - MARGIN, 440
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=INK, width=3)
    draw.rectangle([x0, y0, x0 + 12, y1], fill=RED)
    tx = x0 + 36
    f_kick = font(SANS_BOLD, 25)
    draw.text((tx, y0 + 18), "ANTALYA, TURKIYE - CLIMATE", font=f_kick, fill=RED)
    y = draw_block(draw, (tx, y0 + 54),
                   "COP31 climate summit ends with no pact",
                   SERIF_BOLD, 55, INK, 600, 140, line_gap=6)
    draw_block(draw, (tx, y + 8),
               "EU rejects draft that omitted fossil fuels. Longest COP "
               "ever; UN chief Guterres 'deeply disappointed'.",
               SANS, 26, MUTED, 600, 100, line_gap=4)
    icon_globe_crack(draw, 838, y0 + 130, 86, (14, 99, 117))


def tile(draw, box, item):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=WHITE, outline=(203, 196, 178), width=2)
    draw.rectangle([x0, y0, x1, y0 + 8], fill=item["color"])
    icon_fn = ICONS[item["icon"]]
    icon_fn(draw, x0 + 36, y0 + 46, 26, item["color"])
    f_kick = font(SANS_BOLD, 19)
    draw.text((x0 + 72, y0 + 34), item["kicker"], font=f_kick,
              fill=item["color"])
    inner_w = x1 - x0 - 36
    y = draw_block(draw, (x0 + 18, y0 + 86), item["headline"],
                   SANS_BOLD, 27, INK, inner_w, 74, line_gap=3)
    draw_block(draw, (x0 + 18, y + 5), item["sub"],
               SANS, 20, MUTED, inner_w, y1 - y - 22, line_gap=3)


def ticker(draw):
    y0 = 928
    draw.rectangle([0, y0, W, H], fill=INK)
    draw_block(draw, (MARGIN, y0 + 12), TICKER, SANS_BOLD, 21, WHITE,
               W - 2 * MARGIN, 76, line_gap=4)


def build() -> Path:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    lead_story(draw)
    grid_x = [MARGIN, 356, 684]
    grid_y = [456, 692]
    tile_w, tile_h = 312, 224
    for i, item in enumerate(TILES):
        x0 = grid_x[i % 3]
        y0 = grid_y[i // 3]
        tile(draw, (x0, y0, x0 + tile_w, y0 + tile_h), item)
    ticker(draw)
    out = Path(__file__).with_name("entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
