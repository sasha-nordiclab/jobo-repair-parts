"""Deformation pictures for femkit results: white background, pastel, no text or scale bars.
Shows the part, load arrows and the exaggerated deformation over a faint ghost of the undeformed part.
Colour = deflection of that load case.

Run with FreeCAD's bundled Python (has VTK):
  /Applications/FreeCAD.app/Contents/Resources/bin/python tools/fem/stories.py <prefix>_run.npz out_dir [elev azim]
"""
import math
import sys
from pathlib import Path

import numpy as np
import vtk
from vtk.util import numpy_support as ns

W, H = 1200, 1200
ARROW = (0.50, 0.40, 0.88)      # violet


def lut():
    ctf = vtk.vtkColorTransferFunction()
    for x, c in ((0.0, (0.60, 0.77, 0.94)), (0.3, (0.55, 0.86, 0.72)),
                 (0.6, (1.00, 0.80, 0.42)), (1.0, (0.96, 0.42, 0.47))):
        ctf.AddRGBPoint(x, *c)
    t = vtk.vtkLookupTable(); t.SetNumberOfTableValues(256); t.Build()
    for i in range(256):
        t.SetTableValue(i, *ctf.GetColor(i / 255), 1.0)
    t.SetRange(0, 1); t.SetAboveRangeColor(0.86, 0.30, 0.40, 1.0); t.UseAboveRangeColorOn()
    return t


def surface(xyz, skin):
    pd = vtk.vtkPolyData()
    pts = vtk.vtkPoints(); pts.SetData(ns.numpy_to_vtk(xyz.astype(np.float64), deep=True)); pd.SetPoints(pts)
    cells = np.hstack([np.full((len(skin), 1), 3), skin]).astype(np.int64).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(len(skin), ns.numpy_to_vtkIdTypeArray(cells, deep=True))
    pd.SetPolys(ca)
    return pd


def actor_of(pd, scalars=True):
    nrm = vtk.vtkPolyDataNormals(); nrm.SetInputData(pd); nrm.SetFeatureAngle(35)
    nrm.AutoOrientNormalsOn(); nrm.ConsistencyOn(); nrm.SplittingOn()
    mp = vtk.vtkPolyDataMapper(); mp.SetInputConnection(nrm.GetOutputPort())
    if scalars:
        mp.SetLookupTable(lut()); mp.SetScalarRange(0, 1); mp.SetScalarModeToUsePointData()
    else:
        mp.ScalarVisibilityOff()
    a = vtk.vtkActor(); a.SetMapper(mp)
    p = a.GetProperty(); p.SetAmbient(0.32); p.SetDiffuse(0.75); p.SetSpecular(0.12); p.SetSpecularPower(15)
    return a


def transformed(src, m):
    tr = vtk.vtkTransform(); tr.SetMatrix(m)
    f = vtk.vtkTransformFilter(); f.SetTransform(tr); f.SetInputConnection(src.GetOutputPort())
    mp = vtk.vtkPolyDataMapper(); mp.SetInputConnection(f.GetOutputPort())
    a = vtk.vtkActor(); a.SetMapper(mp)
    return a


def frame(x_axis, origin, scale):
    x = np.array(x_axis, float) / np.linalg.norm(x_axis)
    h = np.array([0, 0, 1.0]) if abs(x[2]) < 0.9 else np.array([1.0, 0, 0])
    y = np.cross(x, h); y /= np.linalg.norm(y); z = np.cross(x, y)
    m = vtk.vtkMatrix4x4()
    for i in range(3):
        m.SetElement(i, 0, x[i] * scale[0]); m.SetElement(i, 1, y[i] * scale[1])
        m.SetElement(i, 2, z[i] * scale[2]); m.SetElement(i, 3, origin[i])
    return m


def arrow(ren, tip, d, length=46):
    d = np.array(d, float) / np.linalg.norm(d)
    src = vtk.vtkArrowSource(); src.SetTipLength(0.3); src.SetTipRadius(0.11); src.SetShaftRadius(0.04)
    src.SetTipResolution(48); src.SetShaftResolution(48)
    a = transformed(src, frame(d, np.array(tip) - d * (length + 2), (length,) * 3))
    p = a.GetProperty(); p.SetColor(*ARROW); p.SetAmbient(0.4); p.SetDiffuse(0.7); p.SetSpecular(0.1)
    ren.AddActor(a)
    return a


class Scene:
    def __init__(self, xyz, skin):
        self.xyz0 = xyz
        self.pd = surface(xyz, skin)
        self.ren = vtk.vtkRenderer(); self.ren.SetBackground(1, 1, 1)
        ghost = actor_of(surface(xyz, skin), scalars=False)
        g = ghost.GetProperty(); g.SetColor(0.70, 0.72, 0.76); g.SetOpacity(0.10)
        self.ren.AddActor(ghost)
        fe = vtk.vtkFeatureEdges(); fe.SetInputData(surface(xyz, skin)); fe.SetFeatureAngle(40)
        fe.BoundaryEdgesOn(); fe.FeatureEdgesOn(); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff()
        fe.ColoringOff()
        em = vtk.vtkPolyDataMapper(); em.SetInputConnection(fe.GetOutputPort()); em.ScalarVisibilityOff()
        self.outline = vtk.vtkActor(); self.outline.SetMapper(em)
        op = self.outline.GetProperty(); op.SetColor(0.45, 0.47, 0.52); op.SetLineWidth(2.2); op.SetOpacity(0.75)
        self.ren.AddActor(self.outline)
        self.part = actor_of(self.pd)
        self.ren.AddActor(self.part)
        kit = vtk.vtkLightKit(); kit.SetKeyLightIntensity(1.0); kit.AddLightsToRenderer(self.ren)
        self.ren.SetUseDepthPeeling(1); self.ren.SetMaximumNumberOfPeels(8)
        self.win = vtk.vtkRenderWindow(); self.win.SetOffScreenRendering(1); self.win.SetSize(W, H)
        self.win.SetMultiSamples(0); self.win.SetAlphaBitPlanes(1); self.win.AddRenderer(self.ren)
        self.ren.UseFXAAOn()
        self.center = (xyz.min(0) + xyz.max(0)) / 2
        self.diag = float(np.linalg.norm(xyz.max(0) - xyz.min(0)))

    def set(self, vals, disp=None, scale=0.0):
        xyz = self.xyz0 + (disp * scale if disp is not None else 0)
        self.pd.GetPoints().SetData(ns.numpy_to_vtk(xyz.astype(np.float64), deep=True))
        self.pd.GetPointData().SetScalars(ns.numpy_to_vtk(vals.astype(np.float64), deep=True))
        self.pd.Modified()

    def camera(self, elev, azim, dist=None):
        dist = dist or 2.1 * self.diag
        e, a = math.radians(elev), math.radians(azim)
        d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
        cam = self.ren.GetActiveCamera()
        cam.SetFocalPoint(*self.center)
        cam.SetPosition(*(self.center + d * dist)); cam.SetViewUp(0, 0, 1); cam.SetViewAngle(30)
        self.ren.ResetCameraClippingRange()

    def png(self, path):
        self.win.Render()
        w2i = vtk.vtkWindowToImageFilter(); w2i.SetInput(self.win); w2i.ReadFrontBufferOff(); w2i.Update()
        wr = vtk.vtkPNGWriter(); wr.SetFileName(str(path)); wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()


def main(npz, out, elev=30.0, azim=-35.0):
    d = np.load(npz, allow_pickle=True)
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    names = list(d['names']); comps, signs, pc = d['comps'], d['signs'], d['pc']
    sc = Scene(d['xyz'], d['skin'])
    for k, name in enumerate(names):
        mag = np.linalg.norm(d['disp'][k], axis=1)
        dvec = np.zeros(3); dvec[comps[k] - 1] = signs[k]
        a = arrow(sc.ren, pc[k], dvec, length=0.22 * sc.diag)
        sc.set(mag / mag.max(), d['disp'][k], 0.06 * sc.diag / mag.max()); sc.camera(float(elev), float(azim))
        sc.png(out / f'fem_{k + 1}_{name.lower()}.png')
        sc.ren.RemoveActor(a)
    print('ok', sorted(p.name for p in out.iterdir()))


if __name__ == '__main__':
    main(*sys.argv[1:])
