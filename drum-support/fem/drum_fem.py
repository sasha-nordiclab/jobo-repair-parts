"""Strength check of the drum supports (default sizes). Run from the repository root:

    python3 drum-support/fem/drum_fem.py <dir with the print-frame STEP files> <work dir>

The STEP files are the bodies with placement reset and rotated +90 deg about Y, so the
plate thickness (model X) is the print Z: print (x, y, z) = model (z, y, -x).
Numbers below are the default values of the Params_* sheets in cad/Jobo_Drum_Support.FCStd.

Lift supports: bonded on the two rod seats (rods Ø ROD_D at y = ±21.5, z = 0), loaded through the
two roller axle holes. The whole drum weight goes into one support (conservative), split over the
two rollers along the lines drum centre -> roller centre.
Rib stands: same roller load with the jaws held on the bath rib, plus the permanent jaw spread
on a 10 mm rib (the halves are printed pre-rotated by PRE_ANG).
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'fem'))
import femkit as fk                                                       # noqa: E402

G = 9.81
DRUM_KG = {'1500': 1.0, '2500': 2.0, 'Expert': 3.0}       # full drum with chemistry (assumed)
LIFTS = {   # name: (drum, D_AY, D_AZ, DRUM_CZ)
    'Lift_1500_A': ('1500', 32.981, 27.899, 75.0), 'Lift_1500_B': ('1500', 32.981, 27.899, 75.0),
    'Lift_2500_A': ('2500', 45.026, 10.697, 75.0), 'Lift_2500_B': ('2500', 45.026, 10.697, 75.0),
    'Lift_Expert_A': ('Expert', 65.072, 28.567, 121.5), 'Lift_Expert_B': ('Expert', 65.072, 28.567, 121.5),
}
STANDS = {  # name: (drum, D_AY, D_AZ, AXIS_H, HINGE_Z, PRE_ANG)
    'Stand_1500': ('1500', 32.981, 38.399, 85.5, 18.0, 1.4),
    'Stand_2840': ('2500', 40.0, 17.956, 85.5, 10.3, 2.5),
}
ROD_Y, ROD_R, AXLE_R, RIB_HALF, JAW_TOP = 21.5, 9.7 / 2, 6.2 / 2, 5.0, 5.5
import os
ONLY = os.environ.get('STANDS_ONLY')


def pf(v):
    """model vector (x, y, z) -> print frame (z, y, -x)"""
    return np.array([v[2], v[1], -v[0]])


def roller_loads(m, case, drum, ay, az, cz):
    W = DRUM_KG[drum] * G
    for s in (1, -1):
        d = np.array([0.0, s * ay, az - cz]); d /= np.linalg.norm(d)        # drum centre -> roller (model)
        F = W / (2 * -d[2]) * d                                             # vertical parts add up to W
        ax = pf([0, s * ay, az])
        def pick(c, n, ax=ax, d=pf(d)):
            r = np.hypot(c[0] - ax[0], c[1] - ax[1])
            return abs(r - AXLE_R) < 0.35 and (c - ax)[:2] @ d[:2] > 0     # loaded half of the hole
        case.load(m.patch(pick), pf(F))
    return W


def main(step_dir, work):
    out = {}
    for name, (drum, ay, az, cz) in (LIFTS.items() if not ONLY else []):
        m = fk.Mesh(f'{step_dir}/{name}.step', f'{work}/{name}')
        c = fk.Case('DRUM', 'creep', f'{DRUM_KG[drum]} kg drum on one support')
        for s in (1, -1):
            ax = pf([0, s * ROD_Y, 0])
            c.fix(m.nodes_on(lambda p, n, ax=ax: abs(np.hypot(p[0] - ax[0], p[1] - ax[1]) - ROD_R) < 0.6))
        roller_loads(m, c, drum, ay, az, cz)
        near = [pf([0, s * ROD_Y, 0]) for s in (1, -1)]
        out[name] = fk.solve(m, [c], f'{work}/{name}',
                             skip_near=lambda p: min(np.hypot(*(p - a)[:2]) for a in near) < ROD_R + 1.5)
    for name, (drum, ay, az, axis_h, hinge_z, pre) in STANDS.items():
        m = fk.Mesh(f'{step_dir}/{name}.step', f'{work}/{name}')
        jaws = {s: m.nodes_on(lambda p, n, s=s: abs(n[1]) > 0.9 and n[1] * s < 0 and abs(abs(p[1]) - RIB_HALF) < 0.5
                              and -0.6 < p[0] < JAW_TOP + 0.6 and p[1] * s > 0) for s in (1, -1)}
        load = fk.Case('DRUM', 'creep', f'{DRUM_KG[drum]} kg drum on one stand, jaws held on the rib')
        load.fix(jaws[1] + jaws[-1]); roller_loads(m, load, drum, ay, az, axis_h)
        # the jaws are modelled closed (halves pre-rotated by PRE_ANG); on the rib every jaw point is pushed
        # out to |y| = RIB_HALF, normal to the rib only; one node per jaw stops the rigid-body slide
        gap = min(RIB_HALF - abs(m.nodes[n][1]) for s in (1, -1) for n in jaws[s])
        clamp = fk.Case('CLAMP', 'creep', 'jaws pushed open onto the 10 mm rib (permanent), frictionless')
        for s in (1, -1):
            clamp.move(jaws[s], lambda p, s=s: [0, s * (RIB_HALF - abs(p[1])), 0], dofs=(2,))
            low = min(jaws[s], key=lambda n: m.nodes[n][0] + abs(m.nodes[n][2]))
            clamp.hold([low], (1, 3))
        at_jaw = lambda p: abs(abs(p[1]) - RIB_HALF) < 2.5 and p[0] < JAW_TOP + 2.5      # boundary peaks at the held jaw faces
        out[name] = fk.solve(m, [load, clamp], f'{work}/{name}', skip_near=at_jaw)
    json.dump(out, open(f'{work}/drum_fem.json', 'w'), indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:3])
