# TPU tube clips for JOBO

## Purpose
Two separate flexible, glue-on clips hold silicone tubes with confirmed outer diameters of 9 mm and 12 mm on JOBO interior walls. Each clip is 15 mm long along the tube.

## Design intent
- Editable native FreeCAD PartDesign bodies with fully constrained sketches and named driving parameters.
- Flat adhesive pad under each C-shaped snap clip. Mount to a cleaned, dry wall with adhesive suitable for TPU and the JOBO wall material and operating conditions.
- Initial geometry: 2.4 mm base thickness, 3 mm radial side wall, entry width about 70% of tube outer diameter. These are prototype dimensions; confirm fit with a short test print.
- The tubes must remain removable without kinking or crushing.

## Current state
Saved FreeCAD document `cad/JOBO_TPU_Tube_Clips.FCStd` has two native PartDesign bodies: `Tube12Body` and `Tube9Body`. **Each Body has one fully constrained profile sketch** (`Profile12`, `Profile9`, DoF 0), one 15 mm Pad, two 0.8 mm PartDesign fillets and two end chamfers. Each profile is a single closed C-shaped outline with a two-arc circular tube seat; geometrical coincident, horizontal, vertical and symmetry constraints establish the relationships, with only named driving dimensions. There are no Block or Fixed constraints. The two new final solids exactly match the previous four-sketch designs (Boolean difference volume zero in both directions for each size). The user confirmed **printing on a C-shaped end face**. Both bodies are placed side by side with that end face at Z=0. The lower FreeCAD chamfer `Angle` is `90 deg - params.print_overhang` (50°) with `Size=0.6 mm`; the upper `Angle` is 40° with `Size=0.6/tan(40°)=0.715 mm`. These produce symmetric 40° slopes from print vertical. Both end-face areas match within each body: 118.92 mm² for Ø12 and 90.17 mm² for Ø9. Both tips are valid single solids, pass `Shape.check(True)` and remain visible in contrasting colours. Both sketches have no conflicting or redundant constraints. Changing `wall` from 3 to 3.6 mm updated both profiles and solids with DoF 0 and valid shapes; 3 mm was restored and saved. The GUI is in axonometric Fit All with the corresponding end faces selected; a rendered preview was inspected.

## Driving parameters
The shared `params` spreadsheet holds `clip_len=15`, `wall=3`, `plate_t=2.4`, `od12=12`, `od9=9`, `mouth_ratio=0.7`, `plate_margin=2.6`, `lip_r=0.8`, `outer_r=0.8`, `print_overhang=40 deg`, and `end_bevel_size=0.6`. Adhesive plate widths are 23.2 mm and 20.2 mm. Current entry widths are 8.4 mm and 6.3 mm.

## Resume
Use the connected `mcp__fdmkit__run` FreeCAD MCP. `cad/rebuild_clips.py` exposes `build_document(output_path)` for a full rebuild inside FreeCAD Python; it creates and saves all constraints, checks both sketches and solids, and saves only after validation. `tree(); P(); chk()` checks only the active Body, so check both Bodies. After changes, update this file and return the FreeCAD view to axonometric Fit All with both final Bodies visible.

## Open questions
- Exact JOBO wall material/curvature, adhesive choice, and preferred print profile are not yet specified.
- Silicone tube wall thickness and tolerance are unknown. Nominal clip bores should be checked with the actual tubes.
