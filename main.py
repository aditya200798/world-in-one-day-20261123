#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261123.

The poster image (entry.png, composed by compose_entry.py from the
illustrated artwork in candidates/) sits beside this file in the
repository. The grader runs this program twice in a sandbox with no
network; each run copies the same image bytes to /output/entry.png,
so both runs produce byte-identical output.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Python 3.13, standard library only.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"entry image missing beside main.py: {SOURCE}")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if target.read_bytes() != SOURCE.read_bytes():
        raise SystemExit("copied image differs from the repository image")


if __name__ == "__main__":
    main()
