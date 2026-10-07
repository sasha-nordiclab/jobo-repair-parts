# JOBO Repair Parts

3D-printable replacement and add-on parts for **JOBO** film processors (CPE2 / CPE2+, the JOBO lift). Each part is a parametric FreeCAD model with STEP files, printing notes and, where the part carries load, a strength check.

| Part | What it does | Folder |
|---|---|---|
| **Bottle hanger** | Holds 2–4 JOBO bottles in the CPE2 water bath; screws to the tank wall with M4 screws into a printed nut backplate. | [`cpe2-bottle-hanger/`](cpe2-bottle-hanger/) |
| **Drum supports** | Roller supports for the far end of the drum: stands that clip onto the bath rib, and supports for the lift rods (1500, 2500 and Expert drums). | [`drum-support/`](drum-support/) |
| **Control knob** | Replacement knob for the CPE2 / CPE2+, Ø 33 mm, with multicolour marking inserts and laser-engraving files. | [`knob/`](knob/) |

<table align="center">
  <tr><td align="center"><img src="cpe2-bottle-hanger/docs/img/hanger_1.png" width="260" alt="Bottle hanger"><br><b>Bottle hanger</b></td>
      <td align="center"><img src="drum-support/docs/img/Stand_1500.png" width="260" alt="Drum support"><br><b>Drum supports</b></td>
      <td align="center"><img src="knob/renders/ko-fi/jobo-knob-01-scale-iso.jpg" width="260" alt="Control knob"><br><b>Control knob</b></td></tr>
</table>

## Common notes

- **Material:** PETG, ABS or ASA for anything that goes near the water bath. PLA softens and creeps at 38–40 °C.
- **Models:** FreeCAD 1.x (made with a 26.3 development build; the knob with 1.1). The STEP files open in any CAD or slicer.
- **Parameters:** every model is driven by spreadsheets. Change the values there and recompute.
- **Strength checks:** `tools/fem/femkit.py` (Gmsh + CalculiX, layered-PETG criterion) and one script per part in its `fem/` folder.
- **Readable diffs:** `.FCStd` files are zip archives. After cloning, run this once so `git diff` shows the parameters:

      git config diff.fcstd.textconv "python3 tools/fcstd-textconv.py"

## License

[CC BY-NC-SA 4.0](LICENSE). You may share and adapt these designs with attribution, not for commercial use, and under the same license.
