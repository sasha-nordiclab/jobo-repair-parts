# JOBO CPE2 backplates with M4 nut pockets

This is a separate `1.2.0-draft` model. The `1.1.0` release file and exports remain unchanged.

The backplates for 2, 3 and 4 sections have rounded outer corners (R3 mm).
Their width remains 17.7768 mm, but the long edges have shifted so the
existing mounting-hole axes run down the centre. The Y coordinates of those
holes remain unchanged and mirror about each plate's midpoint, so they still
match the hanger mounting pattern.

| Sections | Plate size, mm | Through holes | Hex pockets |
| ---: | --- | ---: | ---: |
| 2 | 17.7768 × 159.5 × 5.6 | 2 × Ø4.4 | 2 |
| 3 | 17.7768 × 239.5 × 5.6 | 4 × Ø4.4 | 4 |
| 4 | 17.7768 × 319.5 × 5.6 | 6 × Ø4.4 | 6 |

Each pocket is a 7.3 mm across-flats hexagon, 3.5 mm deep, concentric with a
through hole. This gives 0.3 mm nominal clearance across flats for an ordinary
7 mm M4 hex nut with about 3.2 mm height. The remaining plate thickness below
the pocket is 2.1 mm. Check the dimensions of the actual nuts before printing
the full-length plate; lock nuts and flange nuts may require different pockets.

Print with the broad unpocketed face on the bed. Insert nuts into the pockets
from the exposed outer face before tightening the screws. The 4-section
`*_PRINT.stl` is rotated 45° in the XY plane and has a measured 236.01 × 236.01
mm footprint on a 256 × 256 mm bed.

The three FreeCAD bodies passed CAD validity and BOP checks as one closed solid
each. Their STL files are watertight, one-component meshes with no boundary or
nonmanifold edges. CAD and mesh checks do not verify the fit of physical nuts;
test one nut with the intended printer and material first.
