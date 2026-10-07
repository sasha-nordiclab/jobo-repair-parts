# Jobo CPE2 Drum Roller Support: snap-on, self-clamping

A printable roller support for the far end of the drum in a Jobo CPE2 processor. It clicks onto the 10 × 5 mm rib in the water bath, and a pair of rollers carries a Ø95 mm drum at the right height. It needs no screws or tools. You can move it along the rib to suit the length of your tank.

## How it works
- **Self-clamping jaws.** The stand is a compliant "pliers" mechanism with a flexure hinge on each side. Each half is modelled pre-rotated by about 1.4°, so the jaws print slightly closed. When you push the stand onto the rib, they spread and grip it on both sides.
- **The drum makes the grip tighter.** Its weight presses the rollers down and out, and the arms turn that into more jaw pressure. The FEM analysis (CalculiX) gives about 70 N per jaw with no drum and about 90 N per jaw with a 1.5 kg drum.
- **Snap-in rollers.** The original Jobo rollers (Ø20 × 20 mm body, Ø4.8 mm pins) click into the cheeks from above and spin freely, so they are easy to swap.
- **Drum height.** The bottom of the drum sits 35 mm above the bath platform, in line with the magnetic coupling.

## Material
Print it in **PETG or ABS only**. The part sits in a warm water bath at around 38–40 °C, where PLA softens and creeps. Once PLA creeps, the clamp loses its grip.

## Printing
The file is a single part. The roller slots are in the middle of its thickness, so it has to be **split in half** to print without supports. In Bambu Studio or OrcaSlicer:

1. **Lay it flat.** Put the part on the bed on its large flat side.
2. **Cut it.** Open the Cut tool (C) and cut exactly through the middle of the thickness, parallel to the bed. Each half is 15.5 mm tall.
3. **Add dowels.** Under *Connectors*, choose **Dowel**, **Circle**, about Ø5 × 10 mm. Place 4–6 of them in the solid areas: the lower corners of the arms, the outer walls and the bottom rail.
   Keep them away from:
   - the thin arc spring in the middle;
   - the hinge necks above the jaws;
   - the jaws.
4. **Orient both halves.** Print them with the cut face up, so the half roller slots become open pockets.

**Settings:**
- **Layer:** 0.2 mm.
- **Walls:** 4.
- **Infill:** 25–30 % gyroid.
- **Supports:** none.
- **Bed:** use a smooth PEI plate or a brim for PETG. For ABS, use a brim and an enclosure.
- **Scale:** keep it at 100 %. The spring and hinges are tuned to the printed size.

## Assembly
1. Push the printed dowels into one half, then press the second half on.
2. Glue the halves with a thin layer of CA (superglue) or epoxy for PETG. For ABS, use ABS slurry (ABS dissolved in acetone). Keep glue out of the spring, the hinge slots and the jaws: they must stay free to flex.
3. Clamp the halves, or press them flat, until the glue is set.
4. Snap the two rollers in from the top.
5. Press the stand down onto the rib in the bath. It stays in place on its own.

## Tips
- If it grips too hard or too softly, check how wide your rib really is. The clamp relies on a 10.0 mm rib.
- Take the stand off the rib when you are not using the processor. The spring then relaxes and holds its tension for longer.

Happy developing! 🎞️
