# Two-piece tube clip for JOBO — handoff

## Purpose

A rigid PETG holder is glued to the JOBO wall. A removable TPU C-clip holds a silicone tube and slides into the holder. The earlier one-piece glued TPU clips peeled off the wall. FEM showed the cause: spreading the arms for the tube put about 57 N of peel on the glue edges.

## Current model (2026-10-13)

File `cad/JOBO_Tube_Clips_Two_Piece.FCStd` is **one parametric pair** driven by `od` (tube OD, default 9). The 12 mm bodies were deleted; set `od=12` for that size. Body object Names keep a `9` suffix (`Tube9Body`, `WallHolder9`, `Profile9`, ...) because FreeCAD Names cannot be renamed. Labels are clean: "TPU clip" and "Wall holder PETG". Both bodies have Placement 0, so the model is assembled. Older files: `cad/JOBO_TPU_Tube_Clips.FCStd` (original one-piece), `*_v1.FCStd` (first rejected two-piece) and `.pre-two-piece` (backup).

### TPU clip (`Tube9Body`): the user likes it, so do not change its look

`Profile9` (DoF 0, 30 constraints) is a C outline. The flange edge (W=od/2+wall+plate_margin, y=0) runs as one slope to the arm face (Wa=od/2+wall, y=`root_slope_height`=plate_margin/tan(dt_angle)). `wall_height` = plate_t+od+wall−root_slope_height. Tree: Pad (clip_len) → Mouth fillet (lip_r) → Arm top fillet (outer_r, top outer corners only) → lower and upper end chamfers on the whole end faces (end_bevel_size, 38° from vertical). It prints on a C end face (model Z → print Z).

### PETG holder (`WallHolder9`): prints standing on the outer face of the end stop (model Z → print Z)

The user selected this print face. The user rejected the earlier constant-3 mm band, whose outer side followed the slope and left a 0.66 mm sliver: it looked like a strange chamfer. The outer side is now plain vertical from the glue face to the top. The thickest section is 5.6 mm, which is still ≤ 2 × 5 perimeters of 0.6, so it prints as perimeters only.

- `CradleProfile9` (DoF 0, 50 constraints): the inner contour is offset from the TPU by `dt_clear=0.3`. It has a floor at y=0, a 25° undercut slope and a vertical wall up to H, with a `lip_r` fillet at the top inner edge. The outer side is x=±(W+dt_clear+holder_wall) from y=−holder_wall to H, with an `outer_r` fillet on the top outer corners. H = max(plate_t+od/2−cradle_drop, root_slope_height+lip_r+0.1).
- `pad007` "Cradle" runs from z=−(stop_gap+stop_t)+end_bevel_size to clip_len.
- `CradleStop9` / `pad008` "End stop": the full outer outline minus a U channel for the tube. The channel has a bar `stop_low=1.2` under the tube and side blocks up to H at |x| ≥ od/2+`stop_tube_gap`(0.6). Thickness is stop_t−end_bevel_size.
- `BedProfile` / `pad` "Bed chamfer": the same U outline, with the outer_r top corners. It is padded Reversed by end_bevel_size with TaperAngle = −print_overhang. This is the elephant-foot chamfer: all bed faces have a 38° overhang, and it does not depend on edge names. Do **not** go back to PartDesign Chamfer with edge links there. The chamfer direction differed per edge, and the links broke on any parameter change.

### Verified (od=9)

- All four sketches have DoF 0. Both bodies are single valid solids.
- The clip and holder do not intersect. Play: Y 0.6 mm, X 0.3 mm per side. The clip slides along +Z, and the stop engages at 0.3 mm. The tube clears the holder by 0.6 mm.
- Volumes: TPU 2133.8 mm³, holder 2791.3 mm³. Holder bbox 26.8 × 9.9 × 18.3 mm.
- Parametric tests passed (all valid, zero intersection): od=10, 12, 16; holder_wall=3.6; dt_clear=0.2. Only od=12 was re-tested after the outer side became vertical.
- **od=8 segfaults FreeCAD** in recompute. The cause was not investigated.
- No Orca slice has been done yet for this revision.

## Params (sheet `params`, rows in this order, column C = note)

od=9, clip_len=15, wall=3, plate_t=2.4, plate_margin=2.6, mouth_ratio=0.7, lip_r=0.8, outer_r=0.8, end_bevel_size=0.6, print_overhang=38°, dt_angle=25°, dt_clear=0.3, holder_wall=3, cradle_drop=0, stop_t=3, stop_gap=0.3, stop_low=1.2, stop_tube_gap=0.6.

## FEM summary (plane-strain slice, CalculiX NLGEOM, TPU 95A E=26 MPa, rigid PETG, lips spread to pass the tube, 9 N down)

At dt_clear=0.1:

| Case | Flange lift Ø12 / Ø9 |
| --- | --- |
| Free on the wall | 1.36 / 1.03 mm (centre bows up) |
| Glued | ≈57 / 59 N peel on the glue |
| Cradle | 0.46 / 0.41 mm centre, 0.27 / 0.13 mm edge |
| Zero clearance | 0.27 mm centre, 0.20 mm edge |
| Horizontal T-slot | 0.38 / 0.15 mm |
| Centre held down | ≤0.10 mm |

The residual bow comes from the arm roots squeezing the flange. Proposed, not built or approved: a central T-rail on the holder floor and a T-groove in the TPU flange, which would probably need plate_t 3.0. The holder now prints upright, so this profile is printable.

## Working rules learned here

- Save after every significant operation (user rule). Delete bodies in a call of their own, then `save(); clearUndos()`, then recompute in the next call. Otherwise FreeCAD segfaults in `enforceRecompute`.
- Removing a spreadsheet alias rewrites expressions to `params.B<n>`. Map them back to aliases right away.
- After any change: return to axonometric Fit All with both bodies visible.

## Resume

Open the file and use `mcp__fdmkit__run`. Run `why('<sketch>')` for DoF. Check both bodies, not only the active one.
