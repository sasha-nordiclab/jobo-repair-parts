# Tube clips for JOBO: TPU clip + PETG wall holder

[Editable FreeCAD model](cad/JOBO_Tube_Clips_Two_Piece.FCStd) of a two-piece clip for a silicone tube. The rigid PETG holder is glued to the JOBO wall. The flexible TPU clip slides into the holder from one end until it reaches the end stop. Then the tube is pushed into the clip.

The model is driven by one parameter, `od`, the tube's **outside** diameter. The default is 9 mm. For a 12 mm tube, set `od = 12` in `params` and recompute. Tested values are 9, 10, 12 and 16 mm. `od = 8` crashes FreeCAD during recompute, so 9 mm is the lower limit.

| Dimension (od = 9) | Value |
| --- | ---: |
| Clip length along the tube | 15 mm |
| Holder footprint on the wall | 26.8 × 18.3 mm |
| Holder height above the wall | 9.9 mm |
| Clip–holder clearance | 0.3 mm per side |
| Tube to holder clearance | ≥ 0.6 mm |

## How it holds

The TPU flange and the arm roots form one 25° slope (`dt_angle`). The PETG cradle undercuts this slope and hugs the arms up to the tube axis. When the tube spreads the arms, the force goes into the PETG walls instead of peeling anything off the wall. A U-shaped end stop holds the clip without touching the tube.

## Printing

- **TPU clip:** stand it on one C-shaped end face. Both ends have 0.6 mm chamfers at 38° from vertical.
- **PETG holder:** stand it on the outer face of the end stop, with the tube axis vertical. The base and walls are `holder_wall` = 3.0 mm (5 × 0.6 mm lines). No section is thicker than 2 × 5 perimeters, so it prints as perimeters only. The bed edges have a 0.6 mm chamfer with a 38° overhang. There are no overhangs anywhere else.

Print a fit test before gluing. Tune `dt_clear` if the clip is too loose or too tight in the holder.
