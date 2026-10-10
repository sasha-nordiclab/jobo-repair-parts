"""Build the two JOBO TPU clips in FreeCAD from one constrained profile per clip.

Run inside FreeCAD Python, then call build_document(output_path). Each Body has
one profile sketch, one Pad, two edge fillets and two end chamfers. No Block or
Fixed constraints are used. The function validates both sketches and solids
before saving.
"""

import math
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher


VALUES = {
    'clip_len': 15,
    'wall': 3,
    'plate_t': 2.4,
    'od12': 12,
    'od9': 9,
    'mouth_ratio': 0.7,
    'plate_margin': 2.6,
    'lip_r': 0.8,
    'outer_r': 0.8,
    'print_overhang': '40 deg',
    'end_bevel_size': 0.6,
}


def _check_feature(feature):
    shape = feature.Shape
    if shape.isNull() or not shape.isValid() or len(shape.Solids) != 1:
        raise RuntimeError(f'{feature.Name}: {feature.getStatusString()}')


def _long_edges(shape, targets, length):
    names = []
    for x, y in targets:
        matches = [i + 1 for i, e in enumerate(shape.Edges)
                   if abs(e.CenterOfMass.x - x) < 1e-4
                   and abs(e.CenterOfMass.y - y) < 1e-4
                   and abs(e.BoundBox.ZLength - length) < 1e-4
                   and e.BoundBox.XLength < 1e-4
                   and e.BoundBox.YLength < 1e-4]
        if len(matches) != 1:
            raise RuntimeError(f'long edge at ({x}, {y}): {matches}')
        names.append(f'Edge{matches[0]}')
    return names


def _end_face(shape, z):
    matches = [i + 1 for i, f in enumerate(shape.Faces)
               if f.Vertexes and all(abs(v.Point.z - z) < 1e-5 for v in f.Vertexes)]
    if len(matches) != 1:
        raise RuntimeError(f'end face at z={z}: {matches}')
    return f'Face{matches[0]}'


def _profile(body, tag, od, od_alias):
    d = body.Document
    plate_t = VALUES['plate_t']
    wall = VALUES['wall']
    margin = VALUES['plate_margin']
    ratio = VALUES['mouth_ratio']
    p = od + 2 * wall + 2 * margin
    outer = od + 2 * wall
    top = plate_t + od + wall
    gap = od * ratio
    cy = plate_t + od / 2
    radius = od / 2
    intersect_y = cy + math.sqrt(radius * radius - (gap / 2) ** 2)
    V = App.Vector
    pts = [V(-p/2, 0, 0), V(p/2, 0, 0), V(p/2, plate_t, 0),
           V(outer/2, plate_t, 0), V(outer/2, top, 0),
           V(gap/2, top, 0), V(gap/2, intersect_y, 0),
           V(-gap/2, intersect_y, 0), V(-gap/2, top, 0),
           V(-outer/2, top, 0), V(-outer/2, plate_t, 0),
           V(-p/2, plate_t, 0)]
    theta = math.acos(gap / (2 * radius))
    mid_right = V(radius * math.cos((theta - math.pi/2) / 2),
                  cy + radius * math.sin((theta - math.pi/2) / 2), 0)
    mid_left = V(radius * math.cos((-math.pi/2 - math.pi - theta) / 2),
                 cy + radius * math.sin((-math.pi/2 - math.pi - theta) / 2), 0)
    geo = [Part.LineSegment(pts[i], pts[i+1]) for i in range(6)]
    geo += [Part.Arc(pts[6], mid_right, V(0, plate_t, 0)),
            Part.Arc(V(0, plate_t, 0), mid_left, pts[7])]
    geo.extend(Part.LineSegment(pts[i], pts[(i+1) % 12]) for i in range(7, 12))

    xy = next(o for o in body.Origin.OriginFeatures if o.Role == 'XY_Plane')
    sketch = body.newObject('Sketcher::SketchObject', f'Profile{tag}')
    sketch.Label = f'One profile Ø{tag}'
    sketch.AttachmentSupport = [(xy, '')]
    sketch.MapMode = 'FlatFace'
    sketch.addGeometry(geo, False)
    C = Sketcher.Constraint
    for i in range(5):
        sketch.addConstraint(C('Coincident', i, 2, i+1, 1))
    sketch.addConstraint(C('Coincident', 5, 2, 6, 2))
    sketch.addConstraint(C('Coincident', 6, 1, 7, 2))
    sketch.addConstraint(C('Coincident', 7, 1, 8, 1))
    for i in range(8, 12):
        sketch.addConstraint(C('Coincident', i, 2, i+1, 1))
    sketch.addConstraint(C('Coincident', 12, 2, 0, 1))
    for i in (2, 4, 11):
        sketch.addConstraint(C('Horizontal', i))
    for i in (1, 3, 5, 8, 10):
        sketch.addConstraint(C('Vertical', i))
    sketch.addConstraint(C('PointOnObject', 0, 1, -1))
    sketch.addConstraint(C('Symmetric', 0, 1, 0, 2, -2))

    def dim(constraint, name, expr):
        ci = sketch.addConstraint(constraint)
        sketch.renameConstraint(ci, name)
        sketch.setExpression('Constraints.' + name, expr)

    O = f'params.{od_alias}'
    dim(C('Distance', 0, p), 'plate_width',
        f'{O} + 2*params.wall + 2*params.plate_margin')
    dim(C('DistanceY', 1, 1, 1, 2, plate_t), 'plate_thickness', 'params.plate_t')
    dim(C('Distance', 2, margin), 'plate_margin_right', 'params.plate_margin')
    dim(C('DistanceY', 3, 1, 3, 2, od+wall), 'wall_height', f'{O} + params.wall')
    dim(C('Distance', 4, (outer-gap)/2), 'top_arm_width',
        f'({O} + 2*params.wall - {O}*params.mouth_ratio)/2')
    sketch.addConstraint(C('Symmetric', 4, 2, 9, 1, -2))
    sketch.addConstraint(C('Symmetric', 3, 2, 9, 2, -2))
    sketch.addConstraint(C('Symmetric', 1, 2, 11, 2, -2))
    sketch.addConstraint(C('Coincident', 6, 3, 7, 3))
    sketch.addConstraint(C('PointOnObject', 6, 3, -2))
    dim(C('DistanceY', -1, 1, 6, 3, cy), 'bore_center_y',
        f'params.plate_t + {O}/2')
    dim(C('Radius', 6, radius), 'bore_radius', f'{O}/2')
    sketch.addConstraint(C('PointOnObject', 6, 1, -2))
    d.recompute()
    sketch.solve()
    if (sketch.DoF != 0 or sketch.ConflictingConstraints
            or sketch.RedundantConstraints or sketch.PartiallyRedundantConstraints
            or sketch.MalformedConstraints or sketch.Shape.isNull()):
        raise RuntimeError(f'{sketch.Name}: {sketch.getStatusString()}, DoF={sketch.DoF}')
    return sketch, (p, outer, top, gap, intersect_y)


def _make_clip(d, tag, od_alias, x_shift, color):
    od = float(VALUES[od_alias])
    body = d.addObject('PartDesign::Body', f'Tube{tag}Body')
    body.Label = f'Tube {tag} mm'
    body.ViewObject.ShapeColor = color
    sketch, (plate_width, outer, top, gap, intersect_y) = _profile(body, tag, od, od_alias)
    length = float(VALUES['clip_len'])

    pad = body.newObject('PartDesign::Pad', f'Pad{tag}')
    pad.Label = f'15 mm profile Ø{tag}'
    pad.Profile = sketch
    pad.setExpression('Length', 'params.clip_len')
    d.recompute()
    _check_feature(pad)
    sketch.ViewObject.Visibility = False

    lip = body.newObject('PartDesign::Fillet', f'LipFillet{tag}')
    lip.Label = f'Soft entry edges Ø{tag}'
    lip.Base = (pad, _long_edges(pad.Shape,
                                [(gap/2, top), (gap/2, intersect_y),
                                 (-gap/2, top), (-gap/2, intersect_y)], length))
    lip.setExpression('Radius', 'params.lip_r')
    d.recompute()
    _check_feature(lip)
    pad.ViewObject.Visibility = False

    outer_fillet = body.newObject('PartDesign::Fillet', f'OuterFillet{tag}')
    outer_fillet.Label = f'Rounded outside edges Ø{tag}'
    outer_fillet.Base = (lip, _long_edges(lip.Shape,
                                         [(outer/2, top), (outer/2, VALUES['plate_t']),
                                          (plate_width/2, VALUES['plate_t']),
                                          (-outer/2, top), (-outer/2, VALUES['plate_t']),
                                          (-plate_width/2, VALUES['plate_t'])], length))
    outer_fillet.setExpression('Radius', 'params.outer_r')
    d.recompute()
    _check_feature(outer_fillet)
    lip.ViewObject.Visibility = False

    bottom = body.newObject('PartDesign::Chamfer', f'BottomChamfer{tag}')
    bottom.Label = f'40° lower end Ø{tag}'
    bottom.Base = (outer_fillet, [_end_face(outer_fillet.Shape, 0)])
    bottom.ChamferType = 'Distance and Angle'
    bottom.setExpression('Angle', '90 deg - params.print_overhang')
    bottom.setExpression('Size', 'params.end_bevel_size')
    d.recompute()
    _check_feature(bottom)
    outer_fillet.ViewObject.Visibility = False

    upper = body.newObject('PartDesign::Chamfer', f'TopChamfer{tag}')
    upper.Label = f'40° upper end Ø{tag}'
    upper.Base = (bottom, [_end_face(bottom.Shape, length)])
    upper.ChamferType = 'Distance and Angle'
    upper.setExpression('Angle', 'params.print_overhang')
    upper.setExpression('Size', 'params.end_bevel_size / tan(params.print_overhang)')
    d.recompute()
    _check_feature(upper)
    bottom.ViewObject.Visibility = False
    body.Tip = upper
    body.Placement = App.Placement(App.Vector(x_shift, 0, 0), App.Rotation())
    body.ViewObject.ShapeColor = color
    upper.ViewObject.ShapeColor = color
    body.ViewObject.Visibility = True
    d.recompute()
    if body.Shape.check(True) is not None:
        raise RuntimeError(f'{body.Name}: BOP check reported an issue')
    return body


def build_document(output_path=None):
    """Create and validate a new document; save only when output_path is given."""
    d = App.newDocument('JOBO_TPU_Tube_Clips_OneSketch')
    d.Label = 'JOBO TPU tube clips — one profile sketch per clip'
    d.UndoMode = 1
    sheet = d.addObject('Spreadsheet::Sheet', 'params')
    for row, (key, value) in enumerate(VALUES.items(), 1):
        sheet.set(f'A{row}', key)
        sheet.set(f'B{row}', f'={value}')
        sheet.setAlias(f'B{row}', key)
    d.recompute()
    bodies = [_make_clip(d, '12', 'od12', -16, (0.96, 0.58, 0.48)),
              _make_clip(d, '9', 'od9', 16, (0.49, 0.77, 0.97))]
    if len([o for o in d.Objects if o.TypeId == 'Sketcher::SketchObject']) != 2:
        raise RuntimeError('unexpected extra sketches')
    for body in bodies:
        sketches = [o for o in body.Group if o.TypeId == 'Sketcher::SketchObject']
        if len(sketches) != 1 or sketches[0].DoF != 0:
            raise RuntimeError(f'{body.Name}: sketch verification failed')
        _check_feature(body.Tip)
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().fitAll()
    if output_path:
        d.saveAs(output_path)
    return d
