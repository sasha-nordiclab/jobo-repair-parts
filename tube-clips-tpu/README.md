# TPU tube clips for JOBO

[Editable FreeCAD model](cad/JOBO_TPU_Tube_Clips.FCStd) with two separate glue-on snap clips for silicone tubes. The 9 mm and 12 mm sizes refer to the **outside** diameter of the tubes. Each clip supports 15 mm of tube length.

| Dimension | 9 mm tube | 12 mm tube |
|---|---:|---:|
| Nominal tube seat diameter | 9 mm | 12 mm |
| Snap opening before edge fillets | 6.3 mm | 8.4 mm |
| Adhesive pad, width × length | 20.2 × 15 mm | 23.2 × 15 mm |
| Overall height above the wall | 14.4 mm | 17.4 mm |

Both clips use a 2.4 mm thick adhesive pad, 3 mm side walls, and 0.8 mm fillets at the entry lips and the symmetric outer edges of the walls and pad. The flat face of the pad is for gluing. **Print on one C-shaped end face**, as confirmed by the user; both bodies are oriented with one end at Z=0. Each end has a 0.6 mm edge inset and a 40° slope from the print vertical. FreeCAD represents the two opposite end chamfers with angle properties of 50° and 40° respectively.

The FreeCAD file contains two PartDesign bodies, **one fully constrained profile sketch per body**, and a shared `params` spreadsheet. Each sketch is padded 15 mm; the fillets and end chamfers follow as editable PartDesign features. Change the named dimensions in `params` and recompute. [The rebuild script](cad/rebuild_clips.py) creates the same constrained sketches and verifies the solids before saving.

Print a short fit test in the intended TPU and print profile before gluing the clips into the JOBO. Check that the real tubing snaps in and out without flattening, and that the selected adhesive bonds to both TPU and the JOBO wall under the bath's operating conditions.
