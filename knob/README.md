# Jobo Knob

A 3D-printable replacement control knob for Jobo CPE2 / CPE2+ film processors
(Ø33 × 16 mm), modelled in FreeCAD 1.1. It has a split hub with a D-shaped bore.
A DIN 472-15 internal circlip in the hub groove acts as a spring and clamps the
hub onto the shaft.

⬇️ **Download:** [Blank](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/step/jobo-knob-blank.step) · [Assembly](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/step/jobo-knob-assembly.step) · [Insert: dot + digits](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/step/jobo-knob-dot-digits.step) · [Insert: dot + indicator](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/step/jobo-knob-dot-indicator.step) · [Insert: dot + scale](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/step/jobo-knob-dot-scale.step) · [FreeCAD model](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/cad/JoboKnob.FCStd) · [Laser digits (SVG)](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/laser/jobo-knob-laser-dot-digits.svg) · [Laser digits (DXF)](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/laser/jobo-knob-laser-dot-digits.dxf) · [Laser indicator (SVG)](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/laser/jobo-knob-laser-dot-indicator.svg) · [Laser indicator (DXF)](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/laser/jobo-knob-laser-dot-indicator.dxf) · [Laser scale (SVG)](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/laser/jobo-knob-laser-dot-scale.svg) · [Laser scale (DXF)](https://github.com/sasha-nordiclab/jobo-repair-parts/raw/main/knob/laser/jobo-knob-laser-dot-scale.dxf)

The knob comes with interchangeable colour-insert "modifiers" for multicolour
printing: a red zero dot, an indicator line, the digits 1 · 2, and a temperature
scale with − / +.

## Files

| Path | Contents |
| --- | --- |
| `cad/JoboKnob.FCStd` | Parametric FreeCAD model (source of everything below) |
| `step/jobo-knob-blank.step` | Knob only |
| `step/jobo-knob-assembly.step` | Knob, all modifiers and the reference circlip |
| `step/jobo-knob-dot-indicator.step` | Knob + dot + indicator line |
| `step/jobo-knob-dot-digits.step` | Knob + dot + digits 1 and 2 |
| `step/jobo-knob-dot-scale.step` | Knob + dot + temperature scale |
| `laser/*.dxf`, `*.svg` | Top markings for laser engraving (mm, 1:1, knob centre at origin, layers `ENGRAVE` / `OUTLINE` / `CENTER`) |
| `renders/ko-fi/*.jpg` | Product images (2048 × 2048): all designs, top/iso/bottom/side views, exploded and modifier views |

In the STEP files every modifier is a separate named part, so a slicer
(Bambu Studio, OrcaSlicer) can set it as a modifier with its own filament.
The indicator line and the digit "1" overlap on purpose: they belong to
different knob variants.

## Printing

- Print upside down, with the top face on the plate. No supports are needed.
- The modifiers are one layer thick (`ModThk` = 0.2 mm). Use a 0.2 mm first layer.
- PETG or ASA is recommended. Use 3–4 walls and 25–40 % gyroid infill.

## Model structure

All key dimensions live in the **`Params`** spreadsheet. Sketches and features
reference it, and no sketch uses external geometry or face attachments. The
main groups are:

- **Body**: `KnobD`, `KnobH`, `Taper`, `FluteD`, `FluteCount`, `FluteLen`, …
- **Shaft and hub**: `BoreD`, `FlatDepth`, `HubD`, `CavityD`, `CavityDepth`,
  `CavityChamfer`, `SlotW`
- **Circlip fit**: `CirclipD3`, `CirclipB`, `CirclipA`, `CirclipPreload`,
  `GrooveHalfAngle`. The hub groove depth and the lug slots are derived from these.
- **Markings**: `IndR`, `IndLen`, `DotD`, `DigitH`, `DigitR`, `ScaleSpan`,
  `ScaleTickW`, `SignGap`, …
- **Checks**: `OuterWall`, `MarkClearance`, `EarSlotWall`, … and
  `AllChecksOK` (1 = the parameter set is valid)

Change a value in `Params`, recompute, and check that `AllChecksOK` is 1.

### Requirements

- FreeCAD 1.1
- The **Fasteners** workbench, for the reference DIN 472 circlip
- The digits use `Arial Rounded Bold.ttf` from the macOS system fonts. On
  other systems, point the `Digit 1 Text` / `Digit 2 Text` shape strings to a
  local font.

## Readable diffs for .FCStd

`.FCStd` is a zip archive, so `git diff` runs through `tools/fcstd-textconv.py` at the root of this repository.
The script prints object labels, feature parameters, sketch dimensions,
expressions and spreadsheet cells. Enable it once after cloning, from the repository root:

    git config diff.fcstd.textconv "python3 tools/fcstd-textconv.py"
    git config diff.fcstd.cachetextconv true

Product images in `renders/ko-fi/` are tracked; rendered videos in `renders/` are not.

## License

[CC BY-NC-SA 4.0](../LICENSE).
