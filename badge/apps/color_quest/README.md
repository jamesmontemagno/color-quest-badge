# Color Quest

Color Quest is a cheerful offline coloring book where kids fill rockets, dinosaurs, turtles, and robots with their favorite colors.

## Play

Choose a page with the D-pad and press **Select** to start or resume it.
There are four original drawings: **Rainbow Rocket**, **Dino Picnic**,
**Bubble Buddies**, and **Party Bot**. Every part is outlined, so paint
always stays inside the lines. There are no wrong colors, timers, ads, or
locked pages.

| Screen | Controls |
| --- | --- |
| Sketchbook | D-pad browses pages; Select opens a page. |
| Coloring | D-pad jumps to a nearby part in that direction; the pulsing ring marks it. Select opens the colors. |
| Colors | D-pad chooses one of 12 named colors; Select fills the part; Back cancels. |
| Toolbox | Back while coloring opens the toolbox. Up/Down chooses; Select confirms; Back returns to coloring. |
| Start over | Choose **Clear page** and Select to erase only the current page. **Keep it** is selected by default. |

The toolbox has **Keep coloring**, **Undo last color**, **My sketchbook**,
**Start page over**, and **Retry save**. Undo remembers the last 40 color
changes during the current page visit. Snow counts as a color, not an eraser;
undo can return a newly colored part to uncolored paper.

Fill every part to earn a star and a confetti celebration! Recoloring a
finished picture is welcome. The sketchbook shows a star for each currently
complete picture; undoing a fill or clearing the picture removes its star.

**Menu** is a shortcut back to the sketchbook. **Home** remains the badge
launcher button. All controls use orientation-aware logical actions.

## Saved artwork

Colors and the last opened page save locally after each change in
`/state/color_quest.json`, using the firmware's Badgeware State helper.
Artwork survives leaving the app or rebooting; undo history does not.
Malformed saved colors are replaced with uncolored paper.
If saving fails, the app keeps the artwork in memory and shows a persistent
warning. Use **Back > Retry save** before exiting or restarting.

## Requirements and inspiration

Requires GitHub Universe **2026** firmware. No Wi-Fi, backend, accounts,
credentials, camera, or extra hardware is required.

Inspired by [Pierce Boggan's ColoringBook.AI](https://github.com/pierceboggan/coloring-book)
and its playful coloring-page idea. This is a new, standalone badge game:
the drawings and code are original, and it does not copy or connect to that
app's photo generation, Supabase backend, or family albums.

## Try it

Run static checks from the repository root:

```powershell
python .github\skills\hyb26-skill\scripts\validate_app.py badge\apps\color_quest --target emulator
python -m unittest discover -s tests -p test_color_quest.py
```

In the Badge Simulator canvas, open `color_quest`. Alternatively open
<https://badger.github.io/editor>, name the app `color_quest`, open this
directory's `__init__.py`, and select **Run**. The single Python file contains
all drawing data; the icon is used by the physical badge launcher.
Simulator artwork storage may reset when its runtime is restarted.

For physical acceptance, install through USB Disk Mode following
`hardware/USB_SERIAL.md`, verify the menu supports custom icons and displays
this app's icon, then open each page and exercise all D-pad directions, color
selection, cancel, undo, completion, safe clear, and page switching.
Leave with Home and reopen, then reboot and verify saved colors.
Repeat the controls with the badge upside down. Simulator checks do not prove
physical performance, persistence, touch behavior, or icon rendering.
