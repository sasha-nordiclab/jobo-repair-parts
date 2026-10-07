# JOBO CPE2 Bottle Hanger — design notes

## Release

- Version: `1.1.0`
- Main project: `cad/JOBO_CPE2_Bottle_Hanger.FCStd`
- FreeCAD release property: `Project_Info.ReleaseVersion = 1.1.0`
- Geometry: native Sketcher and Part Design features
- Variants: independent 2, 3 and 4-section parameter sets and bodies
- Backplates: independent native Part Design bodies for all three variants

The release project is self-contained. It does not require the original
development documents.

## Geometry validation

| Sections | Envelope, mm | CAD volume, mm³ | Bed contact, mm² | Overhang above 40° | A1 256 × 256 |
| ---: | --- | ---: | ---: | ---: | --- |
| 2 | 123 × 159.5 × 73.5 | 142721.75 | 6153.31 | 0.0 mm² | Fits |
| 3 | 123 × 239.5 × 73.5 | 215947.21 | 9300.29 | 0.0 mm² | Fits |
| 4 | 123 × 319.5 × 73.5 | 289172.66 | 12447.27 | 0.0 mm² | Does not fit |

Each printable body is one closed valid solid. The exported STL files are
watertight, consistently wound and contain one connected component with no
boundary, nonmanifold, duplicate or degenerate triangles.

The strict OpenCascade BOP diagnostic reports inherited
`BOPAlgo_InvalidCurveOnSurface` warnings on lofted edges. Normal FreeCAD
shape validity and the exported mesh checks pass.

## Print geometry

The broad frame face at `Z = 3 mm` is placed on the bed, so the build
direction in model coordinates is `−Z`.

- Frame taper: 33°
- Joint plate taper: 33°
- Entry transition bottom corner radius: 2.5 mm at Z = 1.9 mm
- Entry transition top corner radius: 3.2 mm at Z = 3.1 mm
- Printed height: 73.5 mm
- Maximum tested unsupported-angle threshold: 40° from vertical

## Backplates

Each hanger has a separate full-length backing plate. The plate is installed
on the opposite side of the mounting surface so the screw load is distributed
along the complete mounting strip.

| Sections | Plate envelope, mm | Thickness | Through holes | Flat-print overhang |
| ---: | --- | ---: | ---: | ---: |
| 2 | 17.78 × 159.5 × 2.4 | 2.4 mm | 2 × Ø4.4 mm | 0.0 mm² |
| 3 | 17.78 × 239.5 × 2.4 | 2.4 mm | 4 × Ø4.4 mm | 0.0 mm² |
| 4 | 17.78 × 319.5 × 2.4 | 2.4 mm | 6 × Ø4.4 mm | 0.0 mm² |

Hole centers were derived from the actual mounting-hole axes of each hanger.
The backplates are laid flat beside their hanger bodies in the FreeCAD project,
so their STL files require no orientation change. The four-section backplate
fits a 256 × 256 mm bed at 45° with a measured planar footprint of
238.49 × 238.49 mm.

## Construction

The lightweight seam pockets and decorative panel windows are suppressed.
Mounting panels and internal seams remain continuous. Every cell retains its
underside frame reinforcement and rounded bottle-entry transition.

Modules meet end-to-end along the Y axis. The connection is a plain butt joint
without clips, dovetails, slots or protrusions. For the three-section variant,
two identical bodies translated by 239.5 mm have zero intersection, zero
minimum distance and 6017.38 mm² of calculated end contact.

## Strength scope

The geometry retains the reinforced load paths intended for a 600 g bottle and
manual insertion. CAD and mesh validation do not certify mechanical capacity.
Material, perimeter count, layer height, extrusion width, temperature and
layer bonding must be confirmed with a physical proof load using the intended
print profile.
