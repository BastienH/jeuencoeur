#!/usr/bin/env python3
"""Generate PNG icons from the source SVG using Inkscape."""

import shutil
import subprocess
import sys
from pathlib import Path

ICONS_DIR = Path(__file__).resolve().parent.parent / "static" / "icons"
SOURCE_SVG = ICONS_DIR / "icon.svg"

SIZES = {
    "icon-192.png": 192,
    "icon-512.png": 512,
    "apple-touch-icon.png": 180,
}


def generate():
    shutil.copy2(SOURCE_SVG, ICONS_DIR / "favicon.svg")
    print("  favicon.svg (copy of icon.svg)")
    for filename, size in SIZES.items():
        out = ICONS_DIR / filename
        subprocess.run(
            [
                "inkscape",
                str(SOURCE_SVG),
                "--export-type=png",
                f"--export-filename={out}",
                f"-w", str(size),
                f"-h", str(size),
            ],
            check=True,
        )
        print(f"  {filename} ({size}x{size})")


if __name__ == "__main__":
    if not SOURCE_SVG.exists():
        sys.exit(f"Source SVG not found: {SOURCE_SVG}")
    print("Generating icons...")
    generate()
    print("Done.")
