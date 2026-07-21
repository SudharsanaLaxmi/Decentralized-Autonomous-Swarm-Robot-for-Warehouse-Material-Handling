# Provenance Manifest

This file records the origin, checksum, and notes for every third-party or original asset migrated into this repository. Maintain an entry for each file copied from the original project repository.

Columns:
- `path`: repository-relative path to the file
- `origin`: original source (original-repo-name, filename or archive path)
- `checksum`: SHA256 checksum of the file as imported
- `author`: original author or owner
- `date`: original creation or extraction date
- `notes`: short notes on edits/processing

Example entry:

```
path: assets/photos/robot_front.jpg
origin: original_repo/figures/robot_front_original.jpg
checksum: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
author: S. Researcher
date: 2023-08-14
notes: Extracted from Phase1_report.pdf using pdfimages. Cropped for focus; original stored in assets/reports/Phase1_report.pdf
```

Migration policy
1. Do not alter original filenames unless necessary. If renaming, document mapping in `PROVENANCE.md`.
2. Keep original report PDFs in `assets/reports/` and include extracted images in `assets/photos/`.
3. For CAD files, record native format location and export steps in `cad/CAD_README.md`.
4. For firmware and scripts, preserve original commit hashes and authors in Git history. If files are refactored, record the reason and diff summary.

How to add an entry
- Compute SHA256: `sha256sum <file>`
- Add a YAML-like block in this file for each asset (see example above).

