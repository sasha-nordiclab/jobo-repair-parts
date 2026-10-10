# Laminar shower bar for the JOBO 1500 drum

## Purpose
A printed 200 mm bar that lies above a JOBO 1500-series drum and pours warm water evenly along its length as calm, separate streams, without spray. Water comes from the ROTEK A01VP pump (rated 6.7 L/min open flow, 10 m head) through silicone tube 6 mm ID / 9 mm OD. Mounting above the drum is not designed yet and will be a separate part.

## Design intent
- Two-chamber manifold. Inlet: barb on the +X end face (user choice 2026-10-10), axial, feeding chamber A. In use, from top to bottom: feed chamber A → V-shaped partition with metering holes Ø1.4 (total area ≈ tube bore, ~28 mm²) that equalise flow along the length → calming chamber B → V-shaped bottom with a row of outlet holes in short nozzle stubs (drip points).
- Metering holes are offset sideways (y = ±meter_y, alternating), so the metering jets do not point straight at an outlet.
- Low outlet velocity: total outlet area ≈ 5× the tube bore (≈0.6 m/s at 5 L/min).
- Print orientation: upside down, the in-use top face on the bed. Internal V roofs are 50° from horizontal (40° from print vertical), so no supports and no bridges. Outlet stubs face up in print.
- The barb is a separate part printed upright and glued (epoxy) into a 40° conical seat in the +X end face. In print the seat axis is horizontal, so the top of its 2 mm deep cone overhangs ~50° from vertical; accepted as it is a short glue seat.
- Material PETG (warm water bath).

## Coordinates
Model coordinates are the print coordinates: Z = 0 is the bed (in-use top face), X along the bar, Y across. The Barb Body is placed in its assembled position.

## Current state (2026-10-10)
`cad/JOBO_Laminar_Shower.FCStd`, two Bodies, both `chk()` OK, zero intersection, colours set, saved.

**Body `Shower`** (Name `Body`, light blue), 200 × 18.8 × 31.2 mm, V 48 787.1 mm³:
`s_outer` (YZ, pentagon; bed bevels 0.6 wide × 0.6·k tall = 40° from vertical) → `pad` sym `len` → `s_cav` (YZ, cavities A and B) → `pocket` sym `len-2*end_t` → `s_meter` (XY, AttachmentOffset z = zA1+0.5, 2 circles at ±meter_y) → `pocket001` reversed (cuts only the partition) → `s_stub` (XY, z = `zs`, 1 circle) → `pad001` (stubs, length zOap+stub_h−zs) → `s_out` (XY, z = zOap+stub_h) → `pocket002` (outlet bores into B, depth stub_h+vwr+2) → `lp_meter` (LinearPattern of pocket001, meter_n/2 occurrences, step 2·meter_pitch) → `lp_out` (LinearPattern of pad001 + pocket002, out_n occurrences) → `s_seat` (XZ, AttachmentOffset x = len/2, y = zin; half profile about the sketch H_Axis) → `groove` (conical seat Ø10→Ø6.64 over 2 mm in the +X end face, bore through the end wall into A) → `s_tear_seat` / `s_tear_bore` (YZ, AttachmentOffset z = len/2+1, teardrop quads with 40° flanks above the seat cone and the bore) → `pocket003` (depth 1+cone_h) / `pocket004` (depth end_t+2) = Tip. The centre seat in the top face was removed; the top face is closed.
`zin` = midpoint of the range where the Ø6.64 bore fits inside chamber A below the partition (7.15).
Counts follow `len` automatically: len 200 → 27 outlets, 18 metering holes (len 60 → 7 outlets, 4 metering holes; rebuild checked, Barb follows, then restored to 200).
Verified with vertical probe lines: metering holes pierce only the partition, the bed wall is intact under them, outlets open into chamber B, end positions ±85 / ±90 are cut and x=93 is solid.

**Body `Barb`** (orange), V 371.2 mm³, height 12.8 mm. Revolution of `s_barb` (XZ): bottom cone fits the seat (radial clearance `barb_c`=0.2), Ø9.6 collar 1.2 mm, shank Ø6.4, two ridges Ø7.4 with 40° undersides, chamfered tip, bore Ø4. Printed upright with the small cone end on the bed. In the document its Body Placement is rotated +90° about Y (axis along +X) with Base.x = `len/2 - cone_h`, Base.z = `zin`, i.e. the assembled position on the end face; it follows `len` (checked at len 60, zero intersection).

Flow areas: barb bore 12.6 mm² (the main restriction), metering 18 × Ø1.4 = 27.7 mm², outlets 27 × Ø2.4 = 122 mm² (≈0.7 m/s at 5 L/min).

**Printability check (2026-10-10, after fixes):** an automatic face scan finds no downward face steeper than 40° from print vertical except the bed face (roofs exactly 40°). Walls: bed/sides/ends 2.4, outer roof `roof_wall`=3.0 (thickened so the Ø6 stubs sit fully inside it: stub base `zs` is midway between the inner apex and the outer surface at the stub rim, margin ≈0.55 mm each side), partition 1.8 normal, stub walls 1.8. Probes confirm stubs are fused to the roof without gaps, outlets open into B, the partition is intact near the inlet, the inlet axis is clear, Barb/Shower intersection 0. Accepted deviations: Barb walls 1.1–1.2 mm (bore Ø4; print it solid) and a 0.2 mm length of the Ø6.64 bore between the seat teardrop and chamber A. Chamber A keeps ≈3 ml in the V below the metering holes after the pump stops (harmless for bath water). Barb has 18 mm² bed contact for 12.8 mm height: print with a brim. Slicer: ≥ 4 walls, ≥ 12 top/bottom layers, PETG.

## Driving parameters
`params` (unitless; trig in degrees): `len=200`, `wall=2.4`, `end_t=2.4`, `part_t=1.8`, `w_in=14`, `hA=3`, `hB=8`, `roof_ang=50`, `bev=0.6`; metering `meter_d=1.4`, `meter_y=4.5`, `meter_pitch=10`; outlets `hole_d=2.4`, `stub_wall=1.8`, `stub_h=2`, `out_pitch=7`, `roof_wall=3`; seat `seat_d=10`, `cone_h=2`, derived `zin`; barb `barb_bore=4`, `shank_d=6.4`, `ridge_d=7.4`, `collar_h=1.2`, `ridge_len=3`, `barb_c=0.2`. Derived: `k`, `vw`, `vwr`, `zs`, `vp`, `t40`, `hw`, `yo`, `zA1`, `zAap`, `zB0`, `zB1`, `zBap`, `zOap`, `zO1`, `stub_d`, `seat_rb`, `zc`, `dr`, `out_n`, `meter_n`.

## Resume
Model through the `fdmkit` MCP `run(expr)` (skill `fdmkit`). Document: `cad/JOBO_Laminar_Shower.FCStd`. `chk()` checks only the active Body: switch the active Body to check `Barb`. fdmkit has no LinearPattern wrapper; the two patterns were created with the native PartDesign API and expression-driven Occurrences/Length. Not yet sliced. After changes, update this file and return the GUI to axonometric Fit All.

## Open questions
- JOBO 1500 drum diameter, bar height above the drum (target gap 10–20 mm), whether to offset the streams from the drum axis.
- Real pump flow through this circuit. Plan: print a 60 mm test section (`len=60`) with hole_d variants 2.0 / 2.4 / 3.0 and test with the pump before the full 200 mm bar.
- Mounting above the drum: user chose a tool-free clip-on mount in the JOBO CPE2/CPE2+ bath (like the `drum-support` stands, which clip onto the 10 × 5 mm bath rib). 1500 drum Ø95. Bath geometry relative to the drum still has to be measured.
