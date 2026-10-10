# Laminar shower bar for the JOBO 1500 drum

A 200 mm printed bar that sits above a JOBO 1500-series drum and pours warm bath water over it as a row of calm, separate streams, without spray. It is fed by the ROTEK A01VP circulation pump through 6 × 9 mm silicone tube.

**Status: prototype, not print-tested.** Print a 60 mm test section first (`len = 60` in the `params` sheet; hole counts follow automatically).

## How it works
Water enters a feed chamber through a barb on one end face. A V-shaped partition with small metering holes (Ø1.4) spreads it evenly along the bar into a calming chamber. From there it leaves through 27 Ø2.4 holes in short nozzle stubs along the bottom ridge. The outlet area is about five times the tube bore, so the water leaves slowly and falls as clean streams. The stubs keep each stream at its own drip point.

## Parts
| Part | Print | Notes |
|---|---|---|
| Shower bar | Upside down, top face on the bed, no supports | Internal roofs at 40° from vertical |
| Barb | Upright, small cone end on the bed | Glue into the conical seat in the end face with epoxy |

Material: PETG. Model: [`cad/JOBO_Laminar_Shower.FCStd`](cad/JOBO_Laminar_Shower.FCStd).

## Open points
- Mounting above the drum (separate part, not designed yet).
- Outlet hole size to be tuned on the test section with the real pump flow.
