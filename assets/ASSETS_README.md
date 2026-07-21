# Assets Folder Guide

This folder documents and stores photographs, screenshots, videos and other media extracted from the original project. All images, photos and screenshots from experimental reports must be preserved here.

Recommended structure:

assets/
  photos/
    robot_front.jpg
    robot_side.jpg
    wiring.jpg
    testing/
      test_run_01.jpg
  cad/
    previews/
  screenshots/
    aruco/
    dashboard/
    calibration/
  reports/
    Phase1_report.pdf
    Phase2_report.pdf
  posters/

Guidelines
- Preserve original filenames and metadata (EXIF) when possible.
- Create subfolders for `testing`, `assembly`, `gripper`, `arena`, `dashboard`.
- Add low-resolution thumbnails for README embedding and keep high-resolution originals.
- Add an `assets/README.md` explaining provenance and any editing performed.

Embedding images in documentation
- Reference images using relative paths in README and docs, for example:
  - `![Robot Front](assets/photos/robot_front.jpg)`
- Prefer PNG or JPEG images for documentation and SVG for diagrams.

Image extraction
- Extract images from PDFs and reports using tools like `pdfimages` and place originals under `assets/reports/` and extracted images under `assets/photos/`.

Provenance
- Every image must have a provenance entry in `PROVENANCE.md` listing source file, original filename (if different), author/date, and any processing steps taken.

Do NOT use stock or placeholder imagery in place of real experimental photos. If an image is missing from this workspace, the migration script (`scripts/migrate_assets.py`) can be used to import assets from a supplied original repository archive.
