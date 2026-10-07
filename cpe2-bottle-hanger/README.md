# JOBO CPE2 bottle hanger

A printed hanger for JOBO bottles in the water bath of a **JOBO CPE2 / CPE2+** processor. A module holds 2 bottles (2–4 if you change one parameter). It mounts on the tilted tank wall with four countersunk M4 screws. On the outside of the tank a printed backplate holds the nuts, and a TPU gasket seals the screw holes.

<p align="center"><img src="docs/img/hanger_1.png" width="420" alt="Hanger, 3 sections"> <img src="docs/img/hanger_2.png" width="420" alt="Hanger from below"></p>

## How it works

- Each bottle drops through a 93 × 70 mm window in the frame. A small bump on the bottle side catches under the **front lip**, so an empty bottle cannot float up.
- The **mount wall** follows the CPE2 tank wall, which kinks 17 mm below the rim: 17° lean above the kink, 7.5° below (relative to the frame).
- Two **M4 countersunk screws per bottle** go through the hanger wall and the 1 mm tank wall into M4 nuts held in one printed **backplate** per module on the outside of the tank.
- A 1 mm **TPU gasket** with the same outline lies between the tank and the backplate; its holes are smaller than the screw, so it closes around it and keeps the bath water in.
- **Gussets** between the sections carry the load from the frame into the wall. Neighbouring sections share one gusset.

## Files

| Path | What |
|---|---|
| `cad/JOBO_CPE2_Bottle_Hanger.FCStd` | Parametric FreeCAD model |
| `step/JOBO_CPE2_Hanger_{2,3,4}_Sections.step` | Hanger for 2, 3 or 4 bottles |
| `step/JOBO_CPE2_Hanger_2_Sections_Spacer30_Left.step` | 2-bottle hanger with a 30 mm top-plate extension on the left: the third module of the standard set |
| `step/JOBO_CPE2_Backplate_M4_2_Sections.step` | Backplate for a 2-bottle module: 4 M4 nut pockets |
| `step/JOBO_CPE2_Gasket_TPU_2_Sections.step` | TPU gasket under the backplate |
| `fem/hanger_fem.py`, `docs/fem_results.json` | Strength check and its results |

## Model

- `Parameters` (spreadsheet): every size, with a comment per row. Derived rows are marked *do not edit*.
The tree is a short build chain; only the two parts in capitals are printed:

- `Cell` (PartDesign body, label *Step 1*): **one section** with all its features.
- `Array` (Draft array, label *Step 2*): `SECTIONS` cells at `PITCH` = 80 mm, fused into one solid. Each cell is `PITCH + G_T` long, so the end gussets of neighbours coincide and become one shared gusset.
- `Hanger_Final` (**HANGER — standard module**): PartDesign body on top of Step 2. It is identical to Step 2 and exists so the printed part has its own name.
- `Hanger_Spacer` (**HANGER + SPACER — module 3**): Step 2 plus the `SPACER_W` (30 mm) top plate on the left.
- `Module_Backplate` (**BACKPLATE — one per module**): `BP_LEN` × 16.8 × 8 mm (152 mm for 2 bottles), 2 × `SECTIONS` Ø 4.4 holes and 7.3 mm hex pockets. Placed in the model where it sits: outside the tank, on the upper flat part of the wall, coaxial with the screws.
- `Module_Gasket` (**GASKET — one per module**): same outline, `SEAL_T` = 1 mm, holes `SEAL_ID` = 3.8 mm.
- Group **Standard set**: modules 1, 2, 3 with their backplates and gaskets as they sit in the tank (links, view only).

Change `SECTIONS` (2, 3, 4…), `SPACER_W`, `TANK_T` or `BOLT_LEN` and recompute. Other useful values: `WIN_Y` (window width), `TANK_TILT`, `TANK_TILT2`, `KINK_Z` (tank wall shape), `BOLT_Y`, `NUT_AF`, `NUT_DEPTH`.

## Standard set

The tank is filled with **2-bottle modules** (each fits the bed easily):

| Position | Part | STEP |
|---|---|---|
| 1 | 2-bottle module | `JOBO_CPE2_Hanger_2_Sections.step` |
| 2 | 2-bottle module | `JOBO_CPE2_Hanger_2_Sections.step` |
| 3 | 2-bottle module with a **30 mm spacer plate** on the left | `JOBO_CPE2_Hanger_2_Sections_Spacer30_Left.step` |

<p align="center"><img src="docs/img/standard_set.png" width="640" alt="Standard set: modules 1, 2 and 3 with the spacer"></p>

The spacer is only the top plate (3 mm, `FRAME_T`), no wall or gussets under it. It bridges the 30 mm gap between module 2 and module 3. *Left* = seen from the bottle side, looking at the tank wall (model −Y). For a spacer on the right, mirror the part in the slicer; the hanger is symmetric.

<p align="center"><img src="docs/img/hanger_spacer.png" width="420" alt="2-bottle module with the 30 mm spacer plate"></p>

## Printing

| Part | Qty | Orientation | Time / mass (PETG, A1) |
|---|---|---|---|
| Hanger, 2 sections | 1 | frame face down, no supports | ≈ 3 h 34 min, 151 g |
| Hanger, 2 sections + 30 mm spacer | 1 | frame face down, no supports | ≈ 3 h 50 min, 165 g |
| Hanger, 3 sections | 1 | frame face down, no supports | ≈ 4 h 59 min, 213 g |
| Hanger, 4 sections | 1 | 323.6 mm long: does not fit a 256 mm bed | — |
| Backplate (2-bottle module) | 1 per module | flat face down, pockets up | ≈ 45 min, 24 g |
| Gasket, TPU 95A | 1 per module | flat, 100 % | ≈ 26 min, 3 g |

Profile: 0.4 mm nozzle, 0.6 mm lines, 0.2 mm layers, 5 walls, 100 % rectilinear infill. PETG or ABS; not PLA, because the bath is warm.

<p align="center"><img src="docs/img/module_backplate_gasket.png" width="520" alt="Backplate and gasket on the outside of the tank"></p>

## Mounting

Per 2-bottle module: **4 × M4 × 16** countersunk screws (ISO 10642 or ISO 14581, head Ø ≤ 9 mm), 4 × M4 nuts (7 mm AF), 1 backplate, 1 gasket.

Stack along a screw: hanger wall 6 mm + tank 1 mm + gasket 1 mm + backplate 8 mm = 16 mm. The nut pocket depth follows `BOLT_LEN` (3.7 mm for M4 × 16), so the screw end comes flush with the outer face of the backplate. `D_SCREW` shows the shortest screw that fills the nut. If your tank wall is thinner or thicker, set `TANK_T`.

1. Put the nuts into the backplate pockets.
2. Hold the gasket and the backplate against the outside of the tank.
3. Insert the screws from the bottle side and tighten gently: the gasket only needs to be compressed, and PETG creeps under high pressure.

## Strength (FEM, 3 sections)

CalculiX, second-order tetrahedra, layered PETG (40 / 20 / 15 MPa in-plane / layer peel / layer shear, × 0.85 for the warm bath). The screw seats are bonded; the tank wall pushes on the part but cannot pull, so each case is supported only on the wall segment that is pressed into the tank.

| Case | Load | Load / allowable (≤ 1 passes) |
|---|---|---|
| Empty bottles floating (sustained, safety factor 4) | 5.9 N up on the lip of every section | **0.36** ✅ |
| Full 0.7 kg bottle knocked onto the front edge at 0.5 m/s (safety factor 2) | 187 N (stiffness 199 N/mm) | 1.08 |

The knock uses part of the safety factor of 2 but stays below the material strength. Forces balance in both cases (residual 0.0 N).

<p align="center"><img src="docs/img/fem_buoyancy.png" width="400" alt="Floating bottles"> <img src="docs/img/fem_hit_top.png" width="400" alt="Knock from above"></p>

## History

Release `v1.1.0` built 2-, 3- and 4-section hangers by joining copies of one section with seam patches. This version rebuilds them as one parametric cell plus an array, uses one M4 nut backplate and a TPU gasket per module, and keeps the geometry of the printed and tested section (hook, tilted wall with the kink, gussets, countersinks).
