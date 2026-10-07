"""Small linear-elastic FEM kit for printed parts: Gmsh mesh, CalculiX solve, layered-PETG check.

Units: N, mm, MPa. The part must be exported in its print orientation (layers normal to Z),
because the failure criterion splits the stress into in-plane, layer-peel and layer-shear parts.

    import femkit as fk
    m = fk.Mesh('part.step', 'work/part')                  # meshes once (cached)
    case = fk.Case('WEIGHT', kind='creep')
    case.fix(m.nodes_on(lambda p, n: ...))                 # all three DOF
    case.slide(m.nodes_on(...), normal)                    # zero displacement along `normal` only
    case.load(m.patch(lambda c, n: ...), vector_N)         # force spread over a surface patch
    case.move(m.nodes_on(...), vector_mm)                  # prescribed displacement
    res = fk.solve(m, [case, ...], 'work/part')            # prints a line per case, returns dicts
"""
import collections
import json
import os
import subprocess
from pathlib import Path

import numpy as np

FC = '/Applications/FreeCAD.app/Contents/Resources/bin'
GMSH = os.environ.get('GMSH', FC + '/gmsh')
CCX = os.environ.get('CCX', FC + '/ccx')

E, NU = 2200.0, 0.38                 # PETG
X, Z, S = 40.0, 20.0, 15.0           # strength (MPa): in-plane, interlayer tension, interlayer shear
TEMP = 0.85                          # 38-40 degC bath
SF = {'impact': 2.0, 'creep': 4.0, 'assembly': 1.5}
MODES = ('in-plane', 'layer peel', 'layer shear')


def fi_parts(v):
    sx, sy, sz, txy, txz, tyz = v
    szc = min(sz, 0.0)
    vm = np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - szc) ** 2 + (szc - sx) ** 2) + 3 * txy ** 2)
    return np.array([vm / X, max(sz, 0.0) / Z, np.hypot(txz, tyz) / S])


class Mesh:
    def __init__(self, step, prefix, clmax=2.0, clmin=0.6):
        inp = prefix + '.inp'
        Path(prefix).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(inp) or os.path.getmtime(inp) < os.path.getmtime(step):
            subprocess.run([GMSH, step, '-3', '-order', '2', '-setnumber', 'Mesh.SecondOrderLinear', '1',
                            '-clmax', str(clmax), '-clmin', str(clmin), '-format', 'inp', '-o', inp],
                           check=True, capture_output=True)
        self.nodes, self.tets, self.tris = self._read(inp)
        self.ids = np.array(sorted(self.nodes))
        self.xyz = np.array([self.nodes[n] for n in self.ids])
        # outward normals of the skin triangles (from the owning tet)
        corner = {}
        for t in self.tets.values():
            for f in ((0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 3, 1), (1, 2, 3, 0)):
                corner[frozenset(t[i] for i in f[:3])] = t[f[3]]
        self.skin = []
        for t in self.tris:
            p = np.array([self.nodes[n] for n in t[:3]])
            n = np.cross(p[1] - p[0], p[2] - p[0]); a = np.linalg.norm(n) / 2
            if a == 0:
                continue
            n /= 2 * a
            opp = corner.get(frozenset(t[:3]))
            if opp is not None and n @ (self.nodes[opp] - p[0]) > 0:
                n = -n
            self.skin.append((t, p.mean(axis=0), n, a))
        bb = self.xyz.min(0), self.xyz.max(0)
        print(f'mesh {Path(step).name}: {len(self.nodes)} nodes, {len(self.tets)} tets, '
              f'bb {np.round(bb[0], 1)} .. {np.round(bb[1], 1)}', flush=True)

    @staticmethod
    def _read(path):
        nodes, tets, tris, kind = {}, {}, [], None
        for line in Path(path).read_text().splitlines():
            if not line.strip() or line.startswith('**'):
                continue
            if line.startswith('*'):
                u = line.upper().replace(' ', '')
                kind = 'N' if u.startswith('*NODE') else 'T' if 'TYPE=C3D10' in u else \
                    'S' if 'TYPE=CPS6' in u else None
                continue
            v = [x for x in line.replace(' ', '').split(',') if x]
            if kind == 'N':
                nodes[int(v[0])] = np.array(list(map(float, v[1:4])))
            elif kind == 'T':
                tets[int(v[0])] = list(map(int, v[1:11]))
            elif kind == 'S':
                tris.append(list(map(int, v[1:7])))
        used = {n for t in tets.values() for n in t}
        return {n: p for n, p in nodes.items() if n in used}, tets, tris

    def nodes_on(self, pick):
        """Skin nodes of every triangle with pick(centroid, outward normal) true."""
        out = set()
        for t, c, n, a in self.skin:
            if pick(c, n):
                out.update(t)
        assert out, 'nodes_on: nothing selected'
        return sorted(out)

    def patch(self, pick):
        """Consistent quadratic-triangle load weights (area/3 on midside nodes), summing to 1."""
        w, area = collections.defaultdict(float), 0.0
        for t, c, n, a in self.skin:
            if pick(c, n):
                for k in t[3:6]:
                    w[k] += a / 3
                area += a
        assert area > 0.5, f'patch: area {area:.2f} mm2'
        return {k: v / area for k, v in w.items()}, area


class Case:
    def __init__(self, name, kind='creep', note=''):
        self.name, self.kind, self.note = name, kind, note
        self.fixed, self.slides, self.loads, self.moves, self.holds = set(), [], [], [], []

    def fix(self, nodes):
        self.fixed.update(nodes); return self

    def slide(self, nodes, normal):
        self.slides.append((list(nodes), np.asarray(normal, float) / np.linalg.norm(normal))); return self

    def load(self, patch, force):
        self.loads.append((patch[0], np.asarray(force, float))); return self

    def move(self, nodes, disp, dofs=(1, 2, 3)):
        """disp: vector or callable(xyz) -> vector; only `dofs` are prescribed."""
        self.moves.append((list(nodes), disp if callable(disp) else np.asarray(disp, float), tuple(dofs))); return self

    def hold(self, nodes, dofs):
        """zero displacement on some DOF only (1 = x, 2 = y, 3 = z)"""
        self.holds.append((list(nodes), tuple(dofs))); return self


def _write(path, m, c):
    held = set(c.fixed) | {n for ns, *_ in c.moves for n in ns} | {n for ns, _ in c.holds for n in ns}
    with open(path + '.inp', 'w') as f:
        f.write('*HEADING\nfemkit\n*NODE,NSET=ALLN\n')
        for n in m.ids:
            p = m.nodes[n]; f.write(f'{n},{p[0]:.9g},{p[1]:.9g},{p[2]:.9g}\n')
        f.write('*ELEMENT,TYPE=C3D10,ELSET=SOLID\n')
        for e, t in m.tets.items():
            f.write(f'{e},' + ','.join(map(str, t)) + '\n')
        f.write(f'*MATERIAL,NAME=PETG\n*ELASTIC\n{E},{NU}\n*SOLID SECTION,ELSET=SOLID,MATERIAL=PETG\n')
        eq = []
        for ns, nv in c.slides:
            for n in ns:
                if n in held:
                    continue
                k = int(np.argmax(np.abs(nv)))          # dependent DOF = largest normal component
                terms = [(n, k + 1, nv[k])] + [(n, j + 1, nv[j]) for j in range(3) if j != k and abs(nv[j]) > 1e-9]
                eq.append(terms); held.add(n)
        if eq:
            f.write('*EQUATION\n')
            for terms in eq:
                f.write(f'{len(terms)}\n' + ','.join(f'{n},{d},{a:.9g}' for n, d, a in terms) + '\n')
        f.write('*BOUNDARY\n')
        for n in sorted(c.fixed):
            f.write(f'{n},1,3\n')
        for ns, dofs in c.holds:
            for n in ns:
                for j in dofs:
                    f.write(f'{n},{j},{j}\n')
        f.write('*STEP\n*STATIC\n')
        if c.moves:
            f.write('*BOUNDARY\n')
            for ns, d, dofs in c.moves:
                for n in ns:
                    if n in c.fixed:
                        continue
                    v = d(m.nodes[n]) if callable(d) else d
                    for j in dofs:
                        f.write(f'{n},{j},{j},{v[j - 1]:.9g}\n')
        if c.loads:
            acc = collections.defaultdict(float)
            for w, F in c.loads:
                for n, x in w.items():
                    for j in range(3):
                        acc[(n, j + 1)] += F[j] * x
            f.write('*CLOAD\n' + ''.join(f'{n},{j},{v:.9g}\n' for (n, j), v in acc.items() if abs(v) > 0))
        f.write('*NODE PRINT,NSET=ALLN,GLOBAL=YES\nU,RF\n*EL PRINT,ELSET=SOLID\nS\n*END STEP\n')


def _run(path):
    r = subprocess.run([CCX, '-i', os.path.basename(path)], cwd=os.path.dirname(path) or '.',   # ccx: <=127-char names
                       capture_output=True, env={'OMP_NUM_THREADS': '8'})
    out = r.stdout.decode(errors='ignore')
    if r.returncode or '*ERROR' in out:
        raise RuntimeError(out[-1500:])
    U, RF, FI, MODE, blk = {}, {}, collections.defaultdict(float), {}, None
    for line in open(path + '.dat'):
        if 'displacements' in line:
            blk = 'U'; continue
        if 'forces' in line:
            blk = 'F'; continue
        if 'stresses' in line:
            blk = 'S'; continue
        v = line.split()
        if not v or not v[0].isdigit():
            continue
        if blk == 'U':
            U[int(v[0])] = np.array(list(map(float, v[1:4])))
        elif blk == 'F':
            RF[int(v[0])] = np.array(list(map(float, v[1:4])))
        elif blk == 'S':
            e = int(v[0]); p = fi_parts(list(map(float, v[2:8]))); fv = float(np.sqrt((p ** 2).sum()))
            if fv > FI[e]:
                FI[e] = fv; MODE[e] = int(p.argmax())
    return U, RF, FI, MODE


def solve(m, cases, prefix, skip_near=None):
    """skip_near(centroid) -> True excludes elements from the peak search (e.g. right at a clamp)."""
    eids = np.array(sorted(m.tets))
    cent = np.array([np.mean([m.nodes[n] for n in m.tets[e][:4]], axis=0) for e in eids])
    keep = np.array([not (skip_near and skip_near(c)) for c in cent])
    res, rend = {}, collections.defaultdict(list)
    for c in cases:
        path = f'{prefix}_{c.name}'
        _write(path, m, c)
        U, RF, FI, MODE = _run(path)
        util = np.array([FI[e] for e in eids]) * SF[c.kind] / TEMP
        j = int(np.argmax(np.where(keep, util, 0)))
        applied = sum((F for _, F in c.loads), np.zeros(3))
        react = sum(RF.values(), np.zeros(3))            # CalculiX RF includes the applied loads
        dmax = max(np.linalg.norm(u) for u in U.values())
        load_disp = sum(sum(x * U[n] for n, x in w.items()) @ (F / np.linalg.norm(F)) for w, F in c.loads) / max(len(c.loads), 1) if c.loads else 0.0
        held_rf = [np.round(sum((RF.get(n, np.zeros(3)) for n in ns), np.zeros(3)), 1).tolist() for ns, *_ in c.moves]
        r = dict(kind=c.kind, note=c.note, sf=SF[c.kind], load_N=np.round(applied, 2).tolist(),
                 util=round(float(util[j]), 2), mode=MODES[MODE[eids[j]]], at=np.round(cent[j], 1).tolist(),
                 max_disp_mm=round(float(dmax), 3), residual_N=np.round(react, 3).tolist(),
                 reaction_on_moved_N=held_rf, load_disp_mm=round(float(load_disp), 4))
        res[c.name] = r
        print(f"{c.name:14s} {c.kind:8s} load {r['load_N']} N  FI/allow {r['util']:5.2f} ({r['mode']}) at {r['at']}  "
              f"max |u| {r['max_disp_mm']} mm  residual {r['residual_N']}" + (f"  moved-set reactions {held_rf}" if held_rf else ''), flush=True)
        rend['disp'].append(np.array([U.get(n, np.zeros(3)) for n in m.ids]))
        lp = [m.nodes[n] for w, _ in c.loads for n in w] or [m.nodes[n] for ns, *_ in c.moves for n in ns]
        rend['pc'].append(np.mean(lp, axis=0))
        dirv = applied if np.linalg.norm(applied) > 0 else np.array([0, 1.0, 0])
        k = int(np.argmax(np.abs(dirv))); rend['comps'].append(k + 1); rend['signs'].append(float(np.sign(dirv[k])))
    nix = {n: i for i, n in enumerate(m.ids)}
    skin = np.array([[nix[n] for n in t[:3]] for t, *_ in m.skin])
    np.savez(prefix + '_run.npz', xyz=m.xyz, skin=skin, names=[c.name for c in cases],
             **{k: np.array(v) for k, v in rend.items()})
    json.dump(res, open(prefix + '_results.json', 'w'), indent=1)
    return res
