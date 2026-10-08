"""Strength check of one CPE2 hanger module (2 sections, 4 screws: two per section), default sizes. Run from the repository root:

    python3 cpe2-bottle-hanger/fem/hanger_fem.py Hanger_2.step <work dir>

Hanger_2.step = the `Hanger_Final` shape (placement reset) of cad/JOBO_CPE2_Bottle_Hanger.FCStd in model coordinates.
The part prints frame face down, so the layers are normal to model Z (flipping does not change σzz).

Supports: the 4 M4 screw seats (bore + countersink) bonded, as a tightened joint.
The tank wall pushes on the mount face but cannot pull: each case supports only the wall segment
that is pressed into the tank (lower segment for a hit from above, upper one for buoyancy).
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'fem'))
import femkit as fk                                                       # noqa: E402

P = dict(D_X0=-55.0, D_XK=-49.8026, D_XB=-42.7592, D_ZK=17.0, WALL_H=70.5, TILT=17.0, TILT2=7.5,
         BOLT_S=10.3369, BOLT_Y=26.0, PITCH=80.0, SECTIONS=2, D_XF=46.6, LIP_T=2.4, LIP_H=1.0,
         FRAME_T=3.0, FRAME_X=110.0, WALL_T=6.0)
BUOY_N = 5.9                     # empty 600 ml bottle pushing up (per section)
E_IMPACT = 0.5 * 0.7 * 500 ** 2 / 1000 / 1000 * 1000   # 0.7 kg at 0.5 m/s = 87.5 N*mm


def main(step, work):
    m = fk.Mesh(step, f'{work}/hanger', clmax=2.5, clmin=0.7)
    t1, t2 = np.radians(P['TILT']), np.radians(P['TILT2'])
    n_up = np.array([-np.cos(t1), 0, -np.sin(t1)])         # outward normal, upper wall segment (to the tank)
    n_lo = np.array([-np.cos(t2), 0, -np.sin(t2)])
    x_face = lambda z: P['D_X0'] + (-z) * np.tan(t1) if z > -P['D_ZK'] else P['D_XK'] + (-z - P['D_ZK']) * np.tan(t2)
    upper = m.nodes_on(lambda c, n: n @ n_up > 0.99 and abs(c[0] - x_face(c[2])) < 0.3 and c[2] > -P['D_ZK'])
    lower = m.nodes_on(lambda c, n: n @ n_lo > 0.99 and abs(c[0] - x_face(c[2])) < 0.3 and c[2] < -P['D_ZK'])
    o = np.array([P['D_X0'] + P['BOLT_S'] * np.sin(t1), 0, -P['BOLT_S'] * np.cos(t1)])   # bolt row on the face
    axes = [o + [0, s * P['BOLT_Y'] + k * P['PITCH'], 0] for k in range(P['SECTIONS']) for s in (1, -1)]
    def seat(c, n):
        for a in axes:
            d = c - a; t = -(d @ n_up); r = np.linalg.norm(d + t * n_up)
            if -0.3 < t < P['WALL_T'] + 0.6 and r < 4.9:
                return True
        return False
    seats = m.nodes_on(seat)
    print('nodes: upper face', len(upper), 'lower face', len(lower), 'screw seats', len(seats))
    mid = (P['SECTIONS'] - 1) * P['PITCH'] / 2      # between the sections, farthest from both screws
    lips = [m.patch(lambda c, n, y0=k * P['PITCH']: n[2] < -0.9 and abs(c[2] + P['LIP_H']) < 0.25
                    and P['D_XF'] - 0.1 < c[0] < P['D_XF'] + P['LIP_T'] + 0.1 and abs(c[1] - y0) < 30)
            for k in range(P['SECTIONS'])]
    buoy = fk.Case('BUOY', 'creep', f'{BUOY_N} N up on the front lip of every section')
    buoy.fix(seats).slide(upper, n_up)
    for p in lips:
        buoy.load(p, [0, 0, BUOY_N])
    hit = fk.Case('HIT_TOP', 'impact', 'full 0.7 kg bottle at 0.5 m/s onto the front edge, middle section (solved at 100 N)')
    hit.fix(seats).slide(lower, n_lo)
    hit.load(m.patch(lambda c, n: n[2] > 0.9 and abs(c[2] - P['FRAME_T']) < 0.2
                     and P['D_XF'] + 1 < c[0] < P['FRAME_X'] / 2 - 0.6 and abs(c[1] - mid) < 15), [0, 0, -100.0])
    res = fk.solve(m, [buoy, hit], f'{work}/hanger',
                   skip_near=lambda c: min(np.linalg.norm((c - a) + ((c - a) @ -n_up) * n_up) for a in axes) < 6)
    r = res['HIT_TOP']; k = 100.0 / r['load_disp_mm']; F = (2 * E_IMPACT * k) ** 0.5
    r.update(k_N_per_mm=round(k, 1), impact_force_N=round(F, 1), util=round(r['util'] * F / 100, 2))
    print(f"HIT_TOP scaled: k {k:.1f} N/mm  F {F:.0f} N  FI/allow {r['util']}")
    json.dump(res, open(f'{work}/hanger_fem.json', 'w'), indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:3])
