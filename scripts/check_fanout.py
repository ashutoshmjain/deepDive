#!/usr/bin/env python3
"""Post-mirror drift gate for the Step-3 fan-out (see GEMINI.md Step 3).

Recomputes every workbench -> standalone pair from the Step-1 mirror list
and blob-compares them with `git hash-object`. Exit 0 = every copy is an
exact mirror (safe to commit/push). Any NON-ZERO exit (unmirrored or
modified copy) means STOP: do not commit, do not push, re-mirror first.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

WORKBENCH = Path(__file__).resolve().parent.parent
DDMA = WORKBENCH.parent / "ddma"
MDINGEST = WORKBENCH.parent / "mdIngest"

INGEST_FILES = [
    "server.py",
    "cockpit.html",
    "landing.html",
    "lightning-widget.js",
    "tests/cockpit_e2e.js",
]
DDMA_FILES = [
    "ddma.py",
    "curator.html",
    "beats.html",
    "scratch/run_curator.py",
    "scratch/review_episode_bridges.py",
    "scratch/test-env/test_curator.js",
    "scratch/test-env/test_canonical_audio_compile.py",
    "scratch/test-env/test_compile_scope.py",
    "scratch/test-env/test_no_auto_mosaic.js",
    "scratch/test-env/test_plan_clip0_title.py",
]

PAIRS = (
    [(WORKBENCH / "ingest" / f, MDINGEST / "ui" / f) for f in INGEST_FILES]
    + [(WORKBENCH / "ddma" / f, DDMA / f) for f in DDMA_FILES]
    + [(WORKBENCH / "settings.template.json", DDMA / "settings.template.json"),
       (WORKBENCH / "settings.template.json", MDINGEST / "settings.template.json")]
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
