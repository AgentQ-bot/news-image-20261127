#!/usr/bin/env python3
"""Render a one-page poster summing up Friday 27 November 2026.

Pure Pillow build: a light masthead naming the day, six numbered
story cards in a 2x3 grid, and a footer strip. Writes a 1024x1024
PNG to entry.png in the repository root.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "entry.png"

SIZE = 1024
MARGIN = 30
GUTTER = 18
HEADER_H = 176
FOOTER_H = 58

PAPER = (250, 248, 243)
CARD_BG = (255, 255, 255)
INK = (26, 30, 40)
BODY = (54, 60, 72)
RULE = (216, 210, 198)
NAVY = (16, 34, 66)
RED = (178, 34, 52)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

STORIES = [
    (
        "KOREAN PENINSULA",
        (178, 34, 52),
        "Six North Korean fishermen sent home",
        "South Korea returned six North Korean fishermen by sea on "
        "Friday after their boat was found adrift near Ulleung Island "
        "on 3 November. A seventh man chose to stay in the South.",
    ),
    (
        "TAIWAN STRAIT",
        (31, 95, 168),
        "China tests floating-bridge landing tactic",
        "Satellite images show China rehearsing a new amphibious "
        "landing method in Fujian, linking civilian vessels into an "
        "800-metre floating bridge. The drill, 280 km from Taiwan, "
        "was still under way on Friday.",
    ),
    (
        "NEW ZEALAND",
        (38, 110, 84),
        "Final count leaves Luxon one seat short",
        "Official results gave the National-led coalition 65 of 130 "
        "seats, one short of a majority. Prime Minister Christopher "
        "Luxon must now win support from the centrist Opportunity "
        "Party to govern.",
    ),
    (
        "AUSTRALIA",
        (160, 84, 24),
        "Law reserves 20% of LNG for home market",
        "Parliament passed a gas reservation law on Friday requiring "
        "LNG exporters to set aside up to 20% of production for "
        "domestic use from 2028, aiming to cut local prices. "
        "Western Australia is exempt.",
    ),
    (
        "JAPAN",
        (104, 62, 140),
        "Tokyo inflation hits 16-month high of 2.9%",
        "Core consumer prices in Tokyo rose 2.9% in November, the "
        "fastest pace since July 2025. The data strengthen the case "
        "for the Bank of Japan to raise interest rates in December.",
    ),
    (
        "EUROPEAN UNION",
        (20, 110, 130),
        "EU leaders end budget talks with no deal",
        "After more than 12 hours of talks, EU leaders failed to "
        "agree the 2028-2034 budget or a 45 billion euro loan for "
        "Ukraine. Macron set a year-end deadline; leaders meet "
        "again on 17-18 December.",
    ),
]


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    lines = []
    line = ""
    for word in text.split():
        candidate = word if not line else line + " " + word
        if draw.textlength(candidate, font=fnt) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centred(draw, text, fnt, y, fill):
    width = draw.textlength(text, font=fnt)
    draw.text(((SIZE - width) / 2, y), text, font=fnt, fill=fill)


def draw_header(draw):
    draw.rectangle([0, 0, SIZE, 10], fill=RED)
    kicker_f = load_font(SANS_BOLD, 22)
    centred(draw, "THE WORLD IN A DAY", kicker_f, 30, RED)
    date_f = load_font(SERIF_BOLD, 52)
    centred(draw, "FRIDAY, 27 NOVEMBER 2026", date_f, 62, NAVY)
    sub_f = load_font(SANS, 22)
    centred(draw, "Six stories that shaped the day", sub_f, 128, BODY)
    draw.line([MARGIN, HEADER_H - 12, SIZE - MARGIN, HEADER_H - 12],
              fill=NAVY, width=3)


def draw_card(draw, x, y, w, h, number, story):
    kicker, accent, headline, summary = story
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=CARD_BG)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12,
                           outline=RULE, width=2)
    draw.rectangle([x + 14, y, x + w - 14, y + 8], fill=accent)
    pad = 22
    inner_w = w - 2 * pad
    kicker_f = load_font(SANS_BOLD, 19)
    head_f = load_font(SERIF_BOLD, 28)
    body_f = load_font(SANS, 20)
    cy = y + 20
    draw.text((x + pad, cy), f"{number}  ·  {kicker}",
              font=kicker_f, fill=accent)
    cy += 30
    for line in wrap_text(draw, headline, head_f, inner_w):
        draw.text((x + pad, cy), line, font=head_f, fill=INK)
        cy += 33
    cy += 6
    for line in wrap_text(draw, summary, body_f, inner_w):
        draw.text((x + pad, cy), line, font=body_f, fill=BODY)
        cy += 25


def draw_footer(draw):
    y = SIZE - FOOTER_H
    draw.rectangle([0, y, SIZE, SIZE], fill=NAVY)
    f = load_font(SANS, 20)
    centred(draw, "Compiled from reports published on 27 November 2026",
            f, y + 17, (225, 231, 242))


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    top = HEADER_H + 8
    bottom = SIZE - FOOTER_H - 16
    card_w = (SIZE - 2 * MARGIN - GUTTER) // 2
    card_h = (bottom - top - 2 * GUTTER) // 3
    for i, story in enumerate(STORIES):
        x = MARGIN + (i % 2) * (card_w + GUTTER)
        y = top + (i // 2) * (card_h + GUTTER)
        draw_card(draw, x, y, card_w, card_h, i + 1, story)
    draw_footer(draw)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
