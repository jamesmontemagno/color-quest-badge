"""An offline, region-by-region coloring book for little badge artists."""

import json
import math
import os
import sys

from badgeware import State

APP_DIR = "/system/apps/color_quest"
os.chdir(APP_DIR)
sys.path.insert(0, APP_DIR)
badge.mode(HIRES | VSYNC)
screen.font = font.nope
screen.antialias = image.X2
screen.fill_rule = image.EVEN_ODD

PALETTE = (
    ("Cherry", (245, 76, 100)), ("Tangerine", (255, 157, 65)),
    ("Sunshine", (255, 215, 72)), ("Lime", (174, 218, 74)),
    ("Leaf", (56, 184, 131)), ("Lagoon", (48, 197, 200)),
    ("Sky", (75, 156, 245)), ("Blueberry", (91, 103, 221)),
    ("Grape", (160, 108, 225)), ("Candy", (243, 136, 194)),
    ("Cocoa", (170, 112, 82)), ("Snow", (255, 255, 255)),
)
PENS = tuple(color.rgb(*rgb) for _, rgb in PALETTE)
INK = color.rgb(40, 42, 69)
PAPER = color.rgb(255, 253, 247)
BG = color.rgb(238, 233, 252)
MUTED = color.rgb(104, 100, 133)
PURPLE = color.rgb(112, 75, 196)
GOLD = color.rgb(255, 202, 63)


def ellipse(name, x, y, rx, ry, anchor=None):
    cx, cy = anchor if anchor is not None else (x, y)
    return (name, cx, cy, "ellipse", (x, y, rx, ry))


def box(name, x, y, w, h, radius=5, anchor=None):
    cx, cy = anchor if anchor is not None else (x + w / 2, y + h / 2)
    return (name, cx, cy, "box", (x, y, w, h, radius))


def polygon(name, x, y, points):
    return (name, x, y, "polygon", points)


def star(name, x, y, radius):
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.48
        points.append((x + math.cos(angle) * r, y + math.sin(angle) * r))
    return polygon(name, x, y, points)


# Back-to-front regions; each anchor is inside its visible, fillable area.
PAGES = (
    ("Rainbow Rocket", "Can your rocket fly to a candy moon?", (
        ellipse("Moon", 177, 27, 21, 21),
        star("Big star", 35, 29, 15),
        star("Tiny star", 185, 90, 12),
        star("Space sparkle", 48, 99, 10),
        polygon("Left fin", 76, 86, ((88, 59), (61, 93), (62, 108), (90, 96))),
        polygon("Right fin", 137, 86, ((123, 59), (150, 93), (149, 108), (122, 96))),
        polygon("Flame", 106, 115, ((91, 99), (122, 99), (117, 118), (107, 130), (97, 118))),
        box("Rocket body", 85, 39, 43, 62, 9, (106, 77)),
        polygon("Nose cone", 106, 25, ((85, 40), (106, 7), (128, 40))),
        ellipse("Window", 106, 59, 13, 13),
        box("Rocket stripe", 86, 82, 41, 12, 2),
    )),
    ("Dino Picnic", "Give this dino a rainbow picnic!", (
        ellipse("Sun", 32, 24, 17, 17),
        ellipse("Cloud", 158, 18, 30, 11),
        polygon("Tail", 51, 84, ((78, 70), (18, 65), (35, 91), (79, 104))),
        polygon("Spikes", 104, 45, ((70, 63), (76, 39), (90, 52), (99, 30),
                                  (113, 48), (129, 32), (138, 64))),
        box("Back foot", 75, 92, 24, 29, 7),
        box("Front foot", 120, 92, 24, 29, 7),
        ellipse("Dino body", 103, 78, 48, 28, (76, 72)),
        box("Neck", 133, 34, 20, 49, 8),
        ellipse("Head", 153, 40, 29, 19),
        ellipse("Tummy", 103, 85, 24, 16),
        ellipse("Cheek", 169, 45, 6, 5),
        polygon("Sandwich", 184, 105, ((163, 119), (181, 90), (204, 119))),
        ellipse("Apple", 30, 115, 13, 12),
    )),
    ("Bubble Buddies", "A purple turtle? Anything is possible!", (
        ellipse("Big bubble", 31, 26, 16, 16),
        ellipse("Little bubble", 182, 20, 10, 10),
        ellipse("Tiny bubble", 198, 47, 7, 7),
        polygon("Seaweed", 25, 100, ((14, 129), (14, 91), (23, 80), (20, 105),
                                    (32, 88), (36, 97), (27, 115), (28, 129))),
        ellipse("Left flipper", 67, 102, 22, 12),
        ellipse("Right flipper", 136, 102, 22, 12),
        ellipse("Top flipper", 74, 44, 18, 10),
        ellipse("Head", 168, 68, 23, 21),
        ellipse("Shell", 105, 72, 49, 34, (65, 72)),
        polygon("Shell gem", 104, 69, ((85, 54), (115, 49), (132, 70),
                                     (115, 91), (85, 87), (76, 70))),
        star("Starfish", 181, 115, 15),
        ellipse("Pearl", 49, 125, 7, 6),
    )),
    ("Party Bot", "Dress your robot for a space party!", (
        star("Party star", 25, 22, 13),
        star("Sparkle", 190, 32, 11),
        box("Left arm", 40, 67, 27, 15, 6),
        box("Right arm", 147, 67, 27, 15, 6),
        box("Left boot", 69, 108, 30, 18, 5),
        box("Right boot", 115, 108, 30, 18, 5),
        box("Robot body", 64, 65, 87, 47, 9, (85, 99)),
        box("Robot head", 70, 26, 75, 38, 10),
        polygon("Party hat", 107, 15, ((88, 27), (106, 2), (125, 27))),
        ellipse("Left ear", 62, 44, 8, 12),
        ellipse("Right ear", 153, 44, 8, 12),
        ellipse("Heart button", 107, 86, 12, 12),
        ellipse("Balloon", 193, 91, 14, 19),
    )),
)

SAVE_KEY = "color_quest"
state = {"pages": {}, "page": 0}
State.load(SAVE_KEY, state)


def clean_state():
    raw = state.get("pages")
    if not isinstance(raw, dict):
        print("Color Quest: invalid saved pages; starting a fresh book.")
        raw = {}
    pages = {}
    for title, _, regions in PAGES:
        values = raw.get(title)
        if not isinstance(values, list) or len(values) != len(regions):
            if values is not None:
                print("Color Quest: ignoring invalid saved page:", title)
            values = [-1] * len(regions)
        cleaned = [
            v if type(v) is int and -1 <= v < len(PALETTE) else -1
            for v in values
        ]
        if any(type(v) is not int or not -1 <= v < len(PALETTE) for v in values):
            print("Color Quest: repaired invalid saved colors:", title)
        pages[title] = cleaned
    state["pages"] = pages
    page = state.get("page")
    if type(page) is int and 0 <= page < len(PAGES):
        state["page"] = page
    else:
        print("Color Quest: invalid saved page number; opening the first page.")
        state["page"] = 0


clean_state()
page = state["page"]
selected = 0
swatch = 0
mode = "book"
option = 0
history = []
notice = ""
notice_left = 0
celebrate_left = 0
elapsed = 0
save_failed = False
shape_cache = []


def colors():
    return state["pages"][PAGES[page][0]]


def filled():
    return sum(value >= 0 for value in colors())


def say(text):
    global notice, notice_left
    notice = text
    notice_left = 2200


def save():
    global save_failed
    state["page"] = page
    try:
        State.save(SAVE_KEY, state)
        # State.save on event firmware can swallow write errors.
        with open("/state/" + SAVE_KEY + ".json") as saved:
            if json.load(saved) != state:
                raise ValueError("saved book did not match")
    except (OSError, ValueError) as error:
        save_failed = True
        print("Color Quest: could not save:", error)
        say("Not saved! Back > Retry save")
    else:
        save_failed = False


def make_shape(region, x, y):
    kind, data = region[3], region[4]
    if kind == "ellipse":
        cx, cy, rx, ry = data
        return shape.ellipse(x + cx, y + cy, rx, ry)
    if kind == "box":
        bx, by, w, h, radius = data
        return shape.rounded_rectangle(x + bx, y + by, w, h, radius)
    return shape.custom([vec2(x + px, y + py) for px, py in data])


def cache_art():
    global shape_cache
    x = 54 if mode == "book" else 13
    shape_cache = []
    for region in PAGES[page][2]:
        tile = make_shape(region, x, 51)
        outline = make_shape(region, x, 51).stroke(2)
        shape_cache.append((tile, outline))


cache_art()


def open_page():
    global mode, selected, history, celebrate_left
    mode = "paint"
    selected = 0
    history = []
    celebrate_left = 0
    cache_art()
    save()


def open_book():
    global mode, celebrate_left
    mode = "book"
    celebrate_left = 0
    cache_art()
    save()


def move_region(dx, dy):
    global selected
    regions = PAGES[page][2]
    _, x, y, _, _ = regions[selected]
    best = None
    score = None
    for i, region in enumerate(regions):
        if i == selected:
            continue
        vx, vy = region[1] - x, region[2] - y
        forward = vx * dx + vy * dy
        if forward <= 0:
            continue
        sideways = abs(vx * dy - vy * dx)
        candidate = forward + sideways * 2 + sideways * sideways / forward
        if score is None or candidate < score:
            best, score = i, candidate
    if best is not None:
        selected = best


def paint():
    global mode, celebrate_left
    old = colors()[selected]
    was_complete = filled() == len(colors())
    if old != swatch:
        history.append((selected, old))
        if len(history) > 40:
            history.pop(0)
        colors()[selected] = swatch
        save()
    mode = "paint"
    if not was_complete and filled() == len(colors()):
        celebrate_left = 3500
        if not save_failed:
            say("A masterpiece! Star earned!")
    elif not save_failed:
        say(("Wow! ", "Lovely! ", "So bright! ", "Great choice! ")[selected % 4]
            + PALETTE[swatch][0])


def undo():
    global celebrate_left
    if not history:
        say("Nothing to undo yet.")
        return
    index, old = history.pop()
    colors()[index] = old
    celebrate_left = 0
    save()
    if not save_failed:
        say("Undone. Try another color!")


def handle_input():
    global page, mode, swatch, option, history
    left = badge.pressed(BUTTON_LEFT)
    right = badge.pressed(BUTTON_RIGHT)
    up = badge.pressed(BUTTON_UP)
    down = badge.pressed(BUTTON_DOWN)
    select = badge.pressed(BUTTON_SELECT)
    back = badge.pressed(BUTTON_BACK)
    if mode == "book":
        direction = int(right or down) - int(left or up)
        if direction:
            page = (page + direction) % len(PAGES)
            cache_art()
        elif select:
            open_page()
    elif mode == "paint":
        if back:
            mode, option = "options", 0
        elif badge.pressed(BUTTON_MENU):
            open_book()
        elif select:
            mode = "palette"
            current = colors()[selected]
            if current >= 0:
                swatch = current
        elif left or right or up or down:
            move_region(int(right) - int(left), int(down) - int(up))
    elif mode == "palette":
        if back:
            mode = "paint"
        elif select:
            paint()
        elif left or right:
            swatch = (swatch // 4) * 4 + (swatch % 4 + int(right) - int(left)) % 4
        elif up or down:
            swatch = (swatch + 4 * (int(down) - int(up))) % len(PALETTE)
    elif mode == "options":
        if back:
            mode = "paint"
        elif up or down:
            option = (option + int(down) - int(up)) % 5
        elif select:
            if option == 0:
                mode = "paint"
            elif option == 1:
                mode = "paint"
                undo()
            elif option == 2:
                open_book()
            elif option == 3:
                mode, option = "confirm", 0
            else:
                mode = "paint"
                save()
                if not save_failed:
                    say("Your book is saved!")
    elif mode == "confirm":
        if back:
            mode = "options"
            option = 3
        elif left or right or up or down:
            option = 1 - option
        elif select:
            if option == 1:
                history = []
                state["pages"][PAGES[page][0]] = [-1] * len(colors())
                save()
                if not save_failed:
                    say("Fresh paper. Let's play!")
            mode = "paint"


def text(label, x, y, pen=INK):
    screen.pen = pen
    screen.text(label, x, y)


def center(label, y, pen=INK):
    w, _ = screen.measure_text(label)
    text(label, (screen.width - w) / 2, y, pen)


def panel(x, y, w, h, pen=PAPER, radius=8):
    screen.pen = pen
    screen.shape(shape.rounded_rectangle(x, y, w, h, radius))


def line(x1, y1, x2, y2, pen=INK):
    screen.pen = pen
    screen.line(x1, y1, x2, y2)


def dot(x, y, radius, pen=INK):
    screen.pen = pen
    screen.shape(shape.circle(x, y, radius))


def face(x, y, gap=9):
    dot(x - gap, y, 2.4)
    dot(x + gap, y, 2.4)
    line(x - 5, y + 6, x, y + 9)
    line(x, y + 9, x + 5, y + 6)


def draw_art():
    x, y = (54 if mode == "book" else 13), 51
    for i, (tile, outline) in enumerate(shape_cache):
        value = colors()[i]
        screen.pen = PAPER if value == -1 else PENS[value]
        screen.shape(tile)
        screen.pen = INK
        screen.shape(outline)
    if page == 0:
        face(x + 106, y + 57, 5)
        dot(x + 171, y + 18, 3, MUTED)
        dot(x + 184, y + 32, 4, MUTED)
        line(x + 99, y + 108, x + 106, y + 120)
        line(x + 106, y + 120, x + 113, y + 108)
    elif page == 1:
        dot(x + 154, y + 35, 2.5)
        line(x + 174, y + 39, x + 178, y + 37)
        line(x + 176, y + 51, x + 166, y + 53)
        line(x + 30, y + 104, x + 33, y + 99)
        line(x + 171, y + 113, x + 195, y + 113)
        for bx in (83, 91, 128, 136):
            line(x + bx, y + 115, x + bx, y + 120)
    elif page == 2:
        face(x + 172, y + 63, 7)
        line(x + 65, y + 67, x + 77, y + 70)
        line(x + 132, y + 70, x + 151, y + 70)
        line(x + 115, y + 49, x + 121, y + 41)
        line(x + 115, y + 91, x + 124, y + 102)
        for bx, by in ((26, 20), (179, 17), (196, 44)):
            dot(x + bx, y + by, 2, PAPER)
    else:
        face(x + 107, y + 41, 17)
        line(x + 193, y + 110, x + 182, y + 129)
        dot(x + 107, y + 86, 4, PAPER)
        for bx in (78, 135):
            line(x + bx, y + 78, x + bx, y + 93)
    if mode != "book":
        region = PAGES[page][2][selected]
        cx, cy = x + region[1], y + region[2]
        radius = 8 + math.sin(elapsed / 220) * 1.5
        screen.pen = INK
        screen.shape(shape.circle(cx, cy, radius + 2).stroke(2))
        screen.pen = PAPER
        screen.shape(shape.circle(cx, cy, radius).stroke(2))
        dot(cx, cy, 2, PURPLE)


def draw_confetti():
    if celebrate_left <= 0:
        return
    for i in range(24):
        x = (i * 47 + 13) % screen.width
        y = int((3500 - celebrate_left) * (0.025 + (i % 5) * 0.009) + i * 19) % screen.height
        panel(x, y, 4, 7, PENS[i % len(PENS)], 1)


def draw_book():
    text("COLOR QUEST", 12, 10, PURPLE)
    stars = sum(all(v >= 0 for v in values) for values in state["pages"].values())
    text("%d/4 stars" % stars, screen.width - 85, 10, PURPLE)
    panel(8, 34, screen.width - 16, 155)
    draw_art()
    text("%d/%d colored" % (filled(), len(colors())), 18, 41, MUTED)
    text("Page %d/4" % (page + 1), screen.width - 80, 41, MUTED)
    text("<", 17, 105, PURPLE)
    text(">", screen.width - 24, 105, PURPLE)
    center(PAGES[page][0], 193, PURPLE)
    center(PAGES[page][1], 210, MUTED)
    center("D-pad: choose    Select: let's color!", screen.height - 14)


def draw_paint():
    text(PAGES[page][0], 12, 10, PURPLE)
    text("%d/%d" % (filled(), len(colors())), screen.width - 53, 10, PURPLE)
    panel(6, 34, 224, 155)
    draw_art()
    panel(236, 34, screen.width - 242, 155)
    text("PART", 245, 43, MUTED)
    text("%02d / %02d" % (selected + 1, len(colors())), 245, 60, PURPLE)
    value = colors()[selected]
    panel(250, 85, 46, 35, INK, 7)
    panel(252, 87, 42, 31, PAPER if value == -1 else PENS[value], 5)
    text("Select", 245, 131)
    text("to color", 245, 146, MUTED)
    text("Any color!", 241, 172, PURPLE)
    panel(6, 195, screen.width - 12, 25, PURPLE)
    message = notice if notice_left > 0 else PAGES[page][2][selected][0] + " - choose a color!"
    center(message, 203, PAPER)
    center("D-pad: part   Select: colors   Back: book/undo", screen.height - 13, MUTED)
    draw_confetti()


def draw_palette():
    panel(21, 37, screen.width - 42, 165, INK)
    panel(24, 40, screen.width - 48, 159)
    center("Pick a color. Make it yours!", 49, PURPLE)
    for i, pen in enumerate(PENS):
        x, y = 52 + (i % 4) * 56, 73 + (i // 4) * 35
        if i == swatch:
            panel(x - 4, y - 4, 47, 33, PURPLE, 7)
        panel(x, y, 39, 25, INK, 5)
        panel(x + 1, y + 1, 37, 23, pen, 4)
        if i == swatch:
            dot(x + 19, y + 12, 5, INK)
            dot(x + 19, y + 12, 2, PAPER)
    center(PALETTE[swatch][0], 181, PURPLE)
    panel(6, 222, screen.width - 12, 18, BG, 0)
    center("D-pad: color   Select: fill   Back: cancel", 227)


OPTIONS = ("Keep coloring", "Undo last color", "My sketchbook", "Start page over", "Retry save")


def draw_options():
    panel(35, 35, screen.width - 70, 173, INK)
    panel(38, 38, screen.width - 76, 167)
    center("Little artist's toolbox", 48, PURPLE)
    for i, label in enumerate(OPTIONS):
        if i == option:
            panel(49, 69 + i * 25, screen.width - 98, 23, PURPLE, 5)
        text(label, 61, 76 + i * 25, PAPER if i == option else INK)


def draw_confirm():
    panel(27, 66, screen.width - 54, 105, INK)
    panel(30, 69, screen.width - 60, 99)
    center("Start this page over?", 82, PURPLE)
    center("Your other pictures stay safe.", 102, MUTED)
    for i, label in enumerate(("Keep it", "Clear page")):
        panel(47 + i * 116, 128, 106, 26, PURPLE if option == i else BG, 5)
        text(label, 60 + i * 116, 137, PAPER if option == i else INK)


def update():
    global elapsed, notice_left, celebrate_left
    dt = max(0, min(badge.ticks_delta, 100))
    elapsed += dt
    notice_left = max(0, notice_left - dt)
    celebrate_left = max(0, celebrate_left - dt)
    handle_input()
    screen.pen = BG
    screen.clear()
    if mode == "book":
        draw_book()
    else:
        draw_paint()
        if mode == "palette":
            draw_palette()
        elif mode == "options":
            draw_options()
        elif mode == "confirm":
            draw_confirm()
    if save_failed:
        panel(0, 0, screen.width, 27, INK, 0)
        center("Not saved! Back > Retry save", 9, PAPER)


run(update)
