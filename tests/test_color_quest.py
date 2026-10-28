"""Host-side Color Quest state, control, and artwork regression checks."""

import builtins
import copy
import io
import json
from pathlib import Path
import types
import unittest
from unittest.mock import Mock


APP = Path(__file__).resolve().parents[1] / "badge/apps/color_quest/__init__.py"
BUTTONS = ("UP", "DOWN", "LEFT", "RIGHT", "SELECT", "BACK", "MENU", "HOME")


class Geometry:
    def __init__(self, *args):
        self.outlined = False

    def stroke(self, *args):
        self.outlined = True
        return self


def contains(region, x, y):
    kind, data = region[3:]
    if kind == "ellipse":
        cx, cy, rx, ry = data
        return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1
    if kind == "box":
        bx, by, w, h, radius = data
        if not (bx < x < bx + w and by < y < by + h):
            return False
        cx = max(bx + radius, min(x, bx + w - radius))
        cy = max(by + radius, min(y, by + h - radius))
        return (x - cx) ** 2 + (y - cy) ** 2 < radius ** 2
    inside = False
    for i, (ax, ay) in enumerate(data):
        bx, by = data[i - 1]
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            inside = not inside
    return inside


class ColorQuestTests(unittest.TestCase):
    def load_app(self, saved=None, fail_save=False):
        self.saved = copy.deepcopy(saved)
        self.fail_save = fail_save
        self.buttons = set()
        self.badge = types.SimpleNamespace(
            mode=Mock(), ticks_delta=16,
            pressed=lambda button: button in self.buttons,
        )
        self.screen = Mock(width=320, height=240)
        self.screen.measure_text.side_effect = lambda text: (len(text) * 6, 8)

        def load(key, target):
            if self.saved is not None:
                target.update(copy.deepcopy(self.saved))

        def save(key, state):
            if self.fail_save:
                # Models the event firmware's swallowed write error.
                return
            self.saved = copy.deepcopy(state)

        self.state = types.SimpleNamespace(load=load, save=Mock(side_effect=save))
        modules = {
            "os": types.SimpleNamespace(chdir=Mock()),
            "sys": types.SimpleNamespace(path=[]),
            "badgeware": types.SimpleNamespace(State=self.state),
        }

        def import_module(name, globals=None, locals=None, fromlist=(), level=0):
            if name in modules:
                return modules[name]
            return builtins.__import__(name, globals, locals, fromlist, level)

        def open_saved(path):
            self.assertEqual(path, "/state/color_quest.json")
            if self.saved is None:
                raise OSError("no saved file")
            return io.StringIO(json.dumps(self.saved))

        self.app = {
            "__name__": "color_quest_under_test",
            "__builtins__": dict(vars(builtins), __import__=import_module, open=open_saved),
            "badge": self.badge, "screen": self.screen, "image": Mock(),
            "shape": types.SimpleNamespace(
                ellipse=Geometry, rounded_rectangle=Geometry, custom=Geometry,
                circle=Geometry,
            ),
            "vec2": lambda x, y: (x, y),
            "color": Mock(), "font": Mock(), "HIRES": 1, "VSYNC": 2, "run": Mock(),
            **{"BUTTON_" + name: name for name in BUTTONS},
        }
        exec(compile(APP.read_text(), str(APP), "exec"), self.app)
        return self.app

    def setUp(self):
        self.load_app()

    def press(self, button):
        self.buttons = {button}
        self.app["update"]()
        self.buttons = set()

    def test_book_wraps_and_opens_all_pages(self):
        self.press("LEFT")
        self.assertEqual(self.app["page"], 3)
        self.press("RIGHT")
        self.assertEqual(self.app["page"], 0)
        for page in range(4):
            self.assertEqual(self.app["page"], page)
            self.press("SELECT")
            self.assertEqual(self.app["mode"], "paint")
            self.press("MENU")
            self.assertEqual(self.app["mode"], "book")
            self.press("RIGHT")

    def test_palette_cancel_fill_recolor_and_undo(self):
        self.press("SELECT")
        self.press("SELECT")
        self.assertEqual(self.app["mode"], "palette")
        self.press("LEFT")
        self.assertEqual(self.app["swatch"], 3)
        self.press("UP")
        self.assertEqual(self.app["swatch"], 11)
        self.press("BACK")
        self.assertEqual(self.app["colors"]()[0], -1)
        self.press("SELECT")
        self.press("SELECT")
        self.assertEqual(self.app["colors"]()[0], 11)
        self.assertEqual(self.saved["pages"]["Rainbow Rocket"][0], 11)
        self.press("SELECT")
        self.press("RIGHT")
        self.press("SELECT")
        self.assertEqual(self.app["colors"]()[0], 8)
        self.press("BACK")
        self.press("DOWN")
        self.press("SELECT")
        self.assertEqual(self.app["colors"]()[0], 11)
        self.app["undo"]()
        self.assertEqual(self.app["colors"]()[0], -1)

    def test_every_region_reachable_using_only_dpad(self):
        for page, (_, _, regions) in enumerate(self.app["PAGES"]):
            self.app["page"] = page
            self.app["open_page"]()
            for start in range(len(regions)):
                reached, pending = {start}, [start]
                while pending:
                    source = pending.pop()
                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        self.app["selected"] = source
                        self.app["move_region"](dx, dy)
                        result = self.app["selected"]
                        if result not in reached:
                            reached.add(result)
                            pending.append(result)
                self.assertEqual(reached, set(range(len(regions))), (page, start))

    def test_fill_geometry_is_not_mutated_into_an_outline(self):
        for page in range(4):
            self.app["page"] = page
            self.app["cache_art"]()
            for tile, outline in self.app["shape_cache"]:
                self.assertIsNot(tile, outline)
                self.assertFalse(tile.outlined)
                self.assertTrue(outline.outlined)

    def test_selection_anchors_are_inside_visible_regions(self):
        for title, _, regions in self.app["PAGES"]:
            for i, region in enumerate(regions):
                x, y = region[1:3]
                self.assertTrue(contains(region, x, y), (title, region[0]))
                for later in regions[i + 1:]:
                    self.assertFalse(contains(later, x, y),
                                     (title, region[0], later[0]))

    def test_fill_all_pages_and_reopen_saved_book(self):
        for page, (title, _, regions) in enumerate(self.app["PAGES"]):
            self.app["page"] = page
            self.app["open_page"]()
            for selected in range(len(regions)):
                self.app["selected"] = selected
                self.app["swatch"] = selected % 12
                self.app["paint"]()
            self.assertGreater(self.app["celebrate_left"], 0)
            self.assertEqual(self.app["filled"](), len(regions))
            self.app["swatch"] = (self.app["swatch"] + 1) % 12
            self.app["celebrate_left"] = 0
            self.app["paint"]()
            self.assertEqual(self.app["celebrate_left"], 0)
        saved = copy.deepcopy(self.saved)
        self.load_app(saved)
        self.assertEqual(self.app["state"], saved)
        self.assertEqual(self.app["page"], 3)
        self.assertEqual(len(self.app["history"]), 0)

    def test_clear_requires_opt_in_and_only_clears_current_page(self):
        self.press("SELECT")
        self.app["paint"]()
        self.press("BACK")
        for _ in range(3):
            self.press("DOWN")
        self.press("SELECT")
        self.assertEqual(self.app["mode"], "confirm")
        self.press("SELECT")
        self.assertEqual(self.app["filled"](), 1)
        other_title = self.app["PAGES"][1][0]
        self.app["state"]["pages"][other_title][0] = 4
        self.press("BACK")
        for _ in range(3):
            self.press("DOWN")
        self.press("SELECT")
        self.press("RIGHT")
        self.press("SELECT")
        self.assertEqual(self.app["filled"](), 0)
        self.assertEqual(self.app["state"]["pages"][other_title][0], 4)

    def test_corrupt_state_is_sanitized(self):
        for saved in ({"pages": None, "page": "bad"},
                      {"pages": {"Rainbow Rocket": "bad"}, "page": -1},
                      {"pages": {"Rainbow Rocket": [True, 99, -2, "red"] + [0] * 7},
                       "page": True}):
            with self.subTest(saved=saved):
                self.load_app(saved)
                self.assertEqual(self.app["page"], 0)
                self.assertTrue(all(type(v) is int and -1 <= v < 12
                                    for v in self.app["colors"]()))

    def test_save_failure_is_visible_and_retry_preserves_artwork(self):
        self.fail_save = True
        self.press("SELECT")
        self.app["paint"]()
        self.assertTrue(self.app["save_failed"])
        self.assertEqual(self.app["colors"]()[0], 0)
        self.press("BACK")
        self.press("UP")
        self.fail_save = False
        self.press("SELECT")
        self.assertFalse(self.app["save_failed"])
        self.assertEqual(self.saved["pages"]["Rainbow Rocket"][0], 0)

    def test_undo_is_bounded_and_empty_undo_is_safe(self):
        self.app["open_page"]()
        self.app["undo"]()
        for i in range(45):
            self.app["swatch"] = i % 12
            self.app["paint"]()
        self.assertEqual(len(self.app["history"]), 40)
        for _ in range(41):
            self.app["undo"]()
        self.assertEqual(len(self.app["history"]), 0)

    def test_draw_every_screen_and_page_without_saving_each_frame(self):
        for page in range(4):
            self.app["page"] = page
            self.app["open_book"]()
            self.app["update"]()
            self.app["open_page"]()
            for mode in ("paint", "palette", "options", "confirm"):
                self.app["mode"] = mode
                self.app["update"]()
        saves = self.state.save.call_count
        self.app["celebrate_left"] = 3500
        for _ in range(10):
            self.app["update"]()
        self.assertEqual(self.state.save.call_count, saves)


if __name__ == "__main__":
    unittest.main()
