"""
Migration helper: import original assets into repository structure

Usage:
  python scripts/migrate_assets.py --src /path/to/original_repo_archive --dry-run

This script copies CAD, STLs, images, and reports into the new repository layout and records provenance entries.
"""

import argparse
import shutil
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROV_FILE = ROOT / 'PROVENANCE.md'

EXT_CAD = ['.f3d', '.sldprt', '.sldasm', '.step', '.stp', '.iges', '.igs']
EXT_STL = ['.stl']
EXT_IMG = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.tiff']
EXT_DOC = ['.pdf', '.docx']

COPY_MAP = [
    (EXT_CAD, ROOT / 'cad' / 'fusion360'),
    (['.step', '.stp', '.iges', '.igs'], ROOT / 'cad' / 'step'),
    (EXT_STL, ROOT / 'cad' / 'stl'),
    (EXT_IMG, ROOT / 'assets' / 'photos'),
    (EXT_DOC, ROOT / 'assets' / 'reports'),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def ensure_dirs():
    for _, dst in COPY_MAP:
        dst.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path, dry_run: bool=False) -> dict:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return {'path': str(dst), 'checksum': None}
    shutil.copy2(src, dst)
    return {'path': str(dst), 'checksum': sha256(dst)}


def append_provenance(entry: dict):
    with PROV_FILE.open('a', encoding='utf-8') as f:
        f.write('\npath: {}\n'.format(entry['path']))
        f.write('origin: {}\n'.format(entry['origin']))
        f.write('checksum: {}\n'.format(entry.get('checksum',''))) 
        f.write('author: {}\n'.format(entry.get('author',''))) 
        f.write('date: {}\n'.format(entry.get('date',''))) 
        f.write('notes: {}\n'.format(entry.get('notes',''))) 
        f.write('\n')


def migrate(src_dir: Path, dry_run: bool=False):
    ensure_dirs()
    files = list(src_dir.rglob('*'))
    for f in files:
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        for exts, dst_folder in COPY_MAP:
            if ext in exts:
                dst = dst_folder / f.name
                info = copy_file(f, dst, dry_run=dry_run)
                entry = {
                    'path': info['path'],
                    'origin': str(f),
                    'checksum': info.get('checksum'),
                    'author': '',
                    'date': '',
                    'notes': 'Imported by migrate_assets.py'
                }
                if not dry_run:
                    append_provenance(entry)
                print('Imported:', f, '->', dst)
                break


def main():
    p = argparse.ArgumentParser(description='Migrate original assets into structured repo')
    p.add_argument('--src', required=True, help='Path to original repository or archive extracted folder')
    p.add_argument('--dry-run', action='store_true', help='Show what would be copied')
    args = p.parse_args()

    src = Path(args.src)
    if not src.exists():
        print('Source path does not exist:', src)
        return

    migrate(src, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
