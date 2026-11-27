#!/usr/bin/env python3
"""Build the 27 November 2026 one-image news poster with Pillow.

Layout: red top rule, centred masthead naming the day, six story
cards in two columns, navy footer. The canvas is 1024x1024 and the
result lands beside this script's parent directory as entry.png.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(os.path.dirname(HERE), "entry.png")

CANVAS = 1024
EDGE = 30
SPACE = 18
HEAD = 176
FOOT = 58

COLOURS = {
    "paper": (250, 248, 243),
    "card": (255, 255, 255),
    "ink": (26, 30, 40),
    "body": (54, 60, 72),
    "edge": (216, 210, 198),
    "navy": (16, 34, 66),
    "red": (178, 34, 52),
    "pale": (225, 231, 242),
}

FONT_FILES = {
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}

CARDS = [
    {
        "tag": "KOREAN PENINSULA",
        "tone": (178, 34, 52),
        "title": "Six North Korean fishermen sent home",
        "text": (
            "South Korea returned six North Korean fishermen by sea on "
            "Friday after their boat was found adrift near Ulleung "
            "Island on 3 November. A seventh man chose to stay in "
            "the South."
        ),
    },
    {
        "tag": "TAIWAN STRAIT",
        "tone": (31, 95, 168),
        "title": "China tests floating-bridge landing tactic",
        "text": (
            "Satellite images show China rehearsing a new amphibious "
            "landing method in Fujian, linking civilian vessels into "
            "an 800-metre floating bridge. The drill, 280 km from "
            "Taiwan, was still under way on Friday."
        ),
    },
    {
        "tag": "NEW ZEALAND",
        "tone": (38, 110, 84),
        "title": "Final count leaves Luxon one seat short",
        "text": (
            "Official results gave the National-led coalition 65 of "
            "130 seats, one short of a majority. Prime Minister "
            "Christopher Luxon must now win support from the centrist "
            "Opportunity Party to govern."
        ),
    },
    {
        "tag": "AUSTRALIA",
        "tone": (160, 84, 24),
        "title": "Law reserves 20% of LNG for home market",
        "text": (
            "Parliament passed a gas reservation law on Friday "
            "requiring LNG exporters to set aside up to 20% of "
            "production for domestic use from 2028, aiming to cut "
            "local prices. Western Australia is exempt."
        ),
    },
    {
        "tag": "JAPAN",
        "tone": (104, 62, 140),
        "title": "Tokyo inflation hits 16-month high of 2.9%",
        "text": (
            "Core consumer prices in Tokyo rose 2.9% in November, "
            "the fastest pace since July 2025. The data strengthen "
            "the case for the Bank of Japan to raise interest rates "
            "in December."
        ),
    },
    {
        "tag": "EUROPEAN UNION",
        "tone": (20, 110, 130),
        "title": "EU leaders end budget talks with no deal",
        "text": (
            "After more than 12 hours of talks, EU leaders failed "
            "to agree the 2028-2034 budget or a 45 billion euro "
            "loan for Ukraine. Macron set a year-end deadline; "
            "leaders meet again on 17-18 December."
        ),
    },
]


def pick(kind, size):
    return ImageFont.truetype(FONT_FILES[kind], size)


def split_lines(canvas_draw, wording, face, limit):
    rows = []
    row = ""
    for token in wording.split(" "):
        trial = token if row == "" else row + " " + token
        if canvas_draw.textlength(trial, font=face) > limit:
            rows.append(row)
            row = token
        else:
            row = trial
    rows.append(row)
    return rows


def middle(canvas_draw, wording, face, ypos, colour):
    span = canvas_draw.textlength(wording, font=face)
    canvas_draw.text(((CANVAS - span) / 2, ypos), wording,
                     font=face, fill=colour)


def render():
    picture = Image.new("RGB", (CANVAS, CANVAS), COLOURS["paper"])
    pen = ImageDraw.Draw(picture)

    pen.rectangle([0, 0, CANVAS, 10], fill=COLOURS["red"])
    middle(pen, "THE WORLD IN A DAY", pick("sansb", 22), 30,
           COLOURS["red"])
    middle(pen, "FRIDAY, 27 NOVEMBER 2026", pick("serif", 52), 62,
           COLOURS["navy"])
    middle(pen, "Six stories that shaped the day", pick("sans", 22),
           128, COLOURS["body"])
    pen.line([EDGE, HEAD - 12, CANVAS - EDGE, HEAD - 12],
             fill=COLOURS["navy"], width=3)

    grid_top = HEAD + 8
    grid_bottom = CANVAS - FOOT - 16
    cell_w = (CANVAS - 2 * EDGE - SPACE) // 2
    cell_h = (grid_bottom - grid_top - 2 * SPACE) // 3

    tag_face = pick("sansb", 19)
    title_face = pick("serif", 28)
    text_face = pick("sans", 20)

    for index, card in enumerate(CARDS):
        cx = EDGE + (index % 2) * (cell_w + SPACE)
        cy = grid_top + (index // 2) * (cell_h + SPACE)
        pen.rounded_rectangle([cx, cy, cx + cell_w, cy + cell_h],
                              radius=12, fill=COLOURS["card"])
        pen.rounded_rectangle([cx, cy, cx + cell_w, cy + cell_h],
                              radius=12, outline=COLOURS["edge"],
                              width=2)
        pen.rectangle([cx + 14, cy, cx + cell_w - 14, cy + 8],
                      fill=card["tone"])
        text_x = cx + 22
        text_w = cell_w - 44
        cursor = cy + 20
        pen.text((text_x, cursor),
                 "%d  ·  %s" % (index + 1, card["tag"]),
                 font=tag_face, fill=card["tone"])
        cursor += 30
        for row in split_lines(pen, card["title"], title_face, text_w):
            pen.text((text_x, cursor), row, font=title_face,
                     fill=COLOURS["ink"])
            cursor += 33
        cursor += 6
        for row in split_lines(pen, card["text"], text_face, text_w):
            pen.text((text_x, cursor), row, font=text_face,
                     fill=COLOURS["body"])
            cursor += 25

    foot_y = CANVAS - FOOT
    pen.rectangle([0, foot_y, CANVAS, CANVAS], fill=COLOURS["navy"])
    middle(pen, "Compiled from reports published on 27 November 2026",
           pick("sans", 20), foot_y + 17, COLOURS["pale"])

    picture.save(DEST, format="PNG", optimize=True)
    saved = os.path.getsize(DEST)
    assert saved <= 1048576, "poster exceeds the 1 MiB cap"
    print("poster saved:", DEST, saved, "bytes")


if __name__ == "__main__":
    render()
