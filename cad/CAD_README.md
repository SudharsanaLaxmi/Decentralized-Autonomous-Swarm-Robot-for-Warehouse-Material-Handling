# CAD Assets Guide

This directory is the canonical home for all CAD-related files from the original project. The goal is to preserve every original CAD file and present them in a clear, engineering-friendly layout.

Structure (recommended):

cad/
  fusion360/
    project_archive.f3d
  step/
    lower_deck.step
    upper_deck.step
  stl/
    lower_deck.stl
    gripper.stl
  drawings/
    exploded_view.pdf
  renders/
    lower_deck_render.png

What to add here
- Place original native CAD files (Fusion360 `.f3d`, SolidWorks `.sldprt`, etc.) in `fusion360/` or a vendor-specific folder.
- Add STEP/IGES exports into `step/` for cross-CAD compatibility.
- Add printable `.stl` files into `stl/` for 3D printing.
- Add manufacturing drawings and exploded views into `drawings/`.
- Add high-quality renders into `renders/`.

Assembly and BOM
- Include a `BOM.md` in this folder listing part numbers, fasteners, materials, and vendors.
- Provide printing settings (infill, layer height, supports) for each STL.

Preview renders and GIFs
- Where possible create preview renders (PNG) and short GIF assembly animations and place them in `renders/`.

CAD migration checklist
1. Collect original CAD files from project archive.
2. Export STEP and STL files for each major subassembly.
3. Generate renders and exploded drawings.
4. Place all files into the folders above and record provenance in `PROVENANCE.md` at the repository root.

Notes
- Do NOT delete original files. Copy them into this repository and record their origin.
- Keep filenames as close to original as possible; if renaming is required add an entry to `PROVENANCE.md`.

References
- See `docs/guides/HARDWARE_ELECTRICAL.md` for electrical integration notes.
