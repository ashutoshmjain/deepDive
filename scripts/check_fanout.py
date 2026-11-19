#!/usr/bin/env python3
"""Post-mirror drift gate for the Step-3 fan-out (see GEMINI.md Step 3).

Recomputes every workbench -> standalone pair from the Step-1 mirror list
and blob-compares them with `git hash-object`. Exit 0 = every copy is an
exact mirror (safe to commit/push). Any NON-ZERO exit (unmirrored or
modified copy) means STOP: do not commit, do not push, re-mirror first.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

WORKBENCH = Path(__file__).resolve().parent.parent
MDINGEST = WORKBENCH.parent / "mdIngest"

# Merged structure (Batch 9): the standalone ddma repo is archived and gone
# from this protocol. Every file under mdIngest/ingest/ and mdIngest/ddma/
# (except the live settings.json) must byte-match its deepDive counterpart.
SKIP_DIRS = {".git", "__pycache__", "node_modules", "target", "book"}
SKIP_FILES = {"settings.json"}


def mirror_tree_files(sub):
    files = []
    base = MDINGEST / sub
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn in SKIP_FILES or fn.endswith(".pyc"):
                continue
            files.append(Path(dirpath, fn).relative_to(base).as_posix())
    return files


PAIRS = (
    [(WORKBENCH / "ingest" / f, MDINGEST / "ingest" / f) for f in mirror_tree_files("ingest")]
    + [(WORKBENCH / "ddma" / f, MDINGEST / "ddma" / f) for f in mirror_tree_files("ddma")]
    + [(WORKBENCH / "settings.template.json", MDINGEST / "settings.template.json")]
)


def blob_sha(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "hash-object", str(path)],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        data = path.read_bytes()
        return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> int:
    failures = 0
    for src, dst in PAIRS:
        label = f"{src.relative_to(WORKBENCH)} -> {dst.parent.name}/{dst.name}"
        if not src.exists():
            print(f"FAIL (workbench source missing -- spec drift): {label}")
            failures += 1
        elif not dst.exists():
            print(f"FAIL (unmirrored -- destination missing): {label}")
            failures += 1
        elif blob_sha(src) != blob_sha(dst):
            print(f"FAIL (modified copy -- blob mismatch): {label}")
            failures += 1
        else:
            print(f"ok: {label}")
    if failures:
        print(f"{failures} pair(s) out of sync -- STOP, do not commit or push.")
        return 1
    print("All pairs in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
