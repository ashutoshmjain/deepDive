# Batch 7 — Curator fixes + fresh-install fixes + ddma clean slate

## Scope

Five items across the ddma and mdIngest repos. Do NOT touch the security items or any other repo. Do NOT change any other file beyond what each item names.

## A1 — Stale "244" episode fallback mislabels clips

### Where

- `ddma/curator.html` at four places: lines 2654, 4936, 4952, 6034. All four read identically:
  `const episodeNum = (projectInfo && projectInfo.name) ? (projectInfo.name.match(/\d+/)?.[0] || projectInfo.name) : "244";`

### Finding

When a clip is opened without a project name (`projectInfo` is null or has no name), the episode number falls back to the hardcoded string `"244"`. Any clip opened without a project name is therefore labelled episode 244, even when it belongs to a different episode. The fallback is a leftover from when 244 was the only episode.

### Fix

1. Remove the hardcoded `"244"` fallback at all four sites. The episode number must be derived from the current project: use `projectInfo.name` when present; otherwise derive it from the current project identifier available in the page (the URL `?project=` / `?id=` parameter, e.g. `episode_244` → `244`, or the active project id). If no episode number can be determined from any of these, do not label it `244` — leave it unknown/empty rather than inventing an episode number.
2. Prefer a single shared helper that all four sites call, so the fallback cannot drift apart again. Do not hardcode any episode number anywhere.
3. Do not change what is shown when the project name IS present.

### Verify

1. The string `"244"` no longer appears as a fallback in `curator.html` (a search for `"244"` returns no `episodeNum` fallback).
2. Opening a clip with a project name still shows that episode's number.
3. Opening a clip without a project name shows the episode number derived from the current project (URL/active project), and never shows `244` unless the current project actually is episode 244.
4. Report PASS/FAIL per verify step, then STOP with a full summary.

## A2 — Save failure still closes the caption modal showing "Saved"

### Where

- `ddma/curator.html`, the caption-modal save button handler (around lines 2719–2750): the `saveBtn` click handler calls `await savePlanToServer()` inside a `try`, logs any error in `catch`, and then — regardless of success or failure — runs `updateStateBar('Saved captions for Clip ...!')` and `closeClipTextModal()`.
- `savePlanToServer` is defined around line 5777.

### Finding

When saving the plan to the server fails (for example a stale-revision refusal), the error is only logged to the console. Execution then falls through to the success path: the status bar says "Saved captions for Clip N!" and the caption modal closes. The user is told the captions were saved when they were not, and the modal is gone so there is no chance to retry. This is a false success.

### Fix

1. Move the success status update (`Saved captions for Clip N!`) and the modal close (`closeClipTextModal()`) inside the success path — they must run ONLY after `await savePlanToServer()` resolves without throwing.
2. In the `catch` (save failure): show a failure message in the status bar (for example that the save failed and the captions were NOT saved) and KEEP the caption modal open so the user can retry. Do not show "Saved" and do not close the modal on failure.
3. The save button's disabled / "Saving..." state must still reset in all cases (success and failure).
4. Do not change the caption editing itself (the `caption_chunks` update) or the revert behaviour.

### Verify

1. Saving captions successfully still shows "Saved captions for Clip N!" and closes the modal.
2. Simulating a save failure (make `savePlanToServer` throw, e.g. by pointing it at an unreachable server or a stale revision) shows a failure message in the status bar, does NOT show "Saved", and leaves the caption modal open with the edited text intact so the user can retry.
3. After a failure, the save button is re-enabled and no longer shows "Saving...".
4. Report PASS/FAIL per verify step, then STOP with a full summary.

## A3 — manim cannot install: av version conflict in requirements

### Where

- `ddma/requirements.txt` (pins `av==14.2.0`) and `mdIngest/ui/requirements.txt` (also pins `av==14.2.0`). `ddma/requirements.txt` also lists `manim==0.22.0`.

### Finding

On a fresh install, `pip install -r requirements.txt` in ddma cannot install manim: manim 0.22.0 requires `av>=15.0`, but the requirements file pins `av==14.2.0` (a pin shared with mdIngest). The install fails, manim is left out, and Beats Studio Manim rendering is unavailable. The system dependencies (pkg-config, libcairo2-dev, libpango1.0-dev) are NOT the blocker — the av version pin is.

### Fix

1. Resolve the conflict in the requirements file(s) so that a fresh `pip install -r requirements.txt` in ddma succeeds WITH manim installed. Acceptable resolutions (pick the one that keeps mdIngest working): upgrade `av` to a version satisfying manim (≥15.0) in both ddma and mdIngest requirements files and verify mdIngest transcription still works; OR pin manim to a version compatible with `av==14.2.0`; OR move manim out of the main requirements into an optional install that is clearly documented.
2. Do NOT force-upgrade av at install time and do NOT edit the prompt/README — the fix must be in the requirements file(s).
3. Do NOT change any other pinned version unless the conflict requires it.

### Verify

1. In a fresh virtual environment, `pip install -r requirements.txt` in ddma completes with no error and manim is importable.
2. mdIngest transcription still works with the resulting av version (run the existing transcription test or a short transcription if one exists; otherwise report that no transcription test was run).
3. Report PASS/FAIL per verify step, then STOP with a full summary.

## A4 — Add a Linux/WSL start script (start.sh) to mdIngest

### Where

- New file: `start.sh` at the mdIngest repo root (next to `start_ui.bat`).
- One-line change: `mdIngest/README.md`, the line after the 1-Prompt Setup code block that reads `After setup, launch with \`python ui/server.py\` (or \`start_ui.bat\` on Windows). The landing page is at http://localhost:8088/.`

### Finding

There is no script to start the mdIngest + DDMA stack on Linux or WSL. Every time WSL restarts, the rclone FUSE mount dies with it, and the user must run four commands by hand, in order: the rclone mount first, then the Cockpit server, the Curator server, and `mdbook serve`. If the mount is not up first, the servers start against an empty local folder (or fail to see the workspace). Windows already has `start_ui.bat`; Linux/WSL has no equivalent.

### Fix

1. Create `start.sh` at the mdIngest repo root with exactly the following content. It must be executable (`chmod +x start.sh`, committed as mode 100755).

```bash
#!/bin/bash
# Start the mdIngest + DDMA stack (Linux / WSL).
# Mounts the Google Drive workspace with rclone (if not already mounted),
# then starts the Cockpit, Curator, and mdbook servers in the background.
#
# Usage: ./start.sh
#   - Set DD_HUB_ROOT to the workspace path (default: /mnt/gdrive/workspace).
#   - If the workspace is not yet mounted, set DD_HUB_FOLDER_ID to the
#     Google Drive folder ID so rclone can mount it.
#   - Python: uses a virtual environment if one exists (.venv in this repo
#     or ../.venv), otherwise the system python3.

set -e
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${DD_HUB_ROOT:-/mnt/gdrive/workspace}"
FOLDER_ID="${DD_HUB_FOLDER_ID:-}"

# The ddma repo must sit next to this repo (the 1-Prompt Setup clones both
# side by side). Fail early with a clear message if it is missing.
if [ ! -d "$REPO_ROOT/../ddma" ]; then
  echo "ERROR: ddma repo not found at $REPO_ROOT/../ddma. Clone it next to mdIngest, then run ./start.sh again."
  exit 1
fi

# 1. Mount the Drive workspace if it isn't already mounted.
if mountpoint -q "$WORKSPACE" 2>/dev/null; then
  echo "Workspace already mounted at $WORKSPACE"
elif [ -n "$FOLDER_ID" ]; then
  echo "Mounting Google Drive workspace..."
  rclone mount gdrive: "$WORKSPACE" --drive-root-folder-id "$FOLDER_ID" --vfs-cache-mode full --daemon
  for i in $(seq 1 10); do
    if mountpoint -q "$WORKSPACE" 2>/dev/null; then
      echo "Mounted at $WORKSPACE"
      break
    fi
    sleep 1
  done
  if ! mountpoint -q "$WORKSPACE" 2>/dev/null; then
    echo "ERROR: mount did not come up. Run 'rclone config' and check the gdrive remote, then try again."
    exit 1
  fi
else
  echo "Workspace at $WORKSPACE is not mounted and DD_HUB_FOLDER_ID is not set."
  echo "Mount it first (rclone mount) or set DD_HUB_FOLDER_ID to the Drive folder ID, then run ./start.sh again."
  exit 1
fi

export DD_HUB_ROOT="$WORKSPACE"

# 2. Pick a Python (venv preferred, system python3 as fallback).
if [ -x "$REPO_ROOT/.venv/bin/python" ]; then
  PY="$REPO_ROOT/.venv/bin/python"
elif [ -x "$REPO_ROOT/../.venv/bin/python" ]; then
  PY="$REPO_ROOT/../.venv/bin/python"
else
  PY="python3"
fi
echo "Using Python: $PY"

# 3. Start the servers in the background (logs go to ~/logs/).
mkdir -p ~/logs
cd "$REPO_ROOT" && DD_HUB_ROOT="$WORKSPACE" nohup "$PY" ui/server.py > ~/logs/cockpit.log 2>&1 &
cd "$REPO_ROOT/../ddma" && DD_HUB_ROOT="$WORKSPACE" nohup "$PY" scratch/run_curator.py > ~/logs/curator.log 2>&1 &
cd "$REPO_ROOT" && nohup mdbook serve --port 3000 > ~/logs/mdbook.log 2>&1 &

sleep 3
echo ""
echo "Servers starting:"
echo "  Cockpit:  http://localhost:8088/"
echo "  mdbook:   http://localhost:3000/"
echo "  Curator:  http://localhost:8000/curator.html"
echo "  Beats:    launch from the landing page (http://localhost:8088/ -> Launch Beats Studio)"
echo "Logs: ~/logs/cockpit.log, ~/logs/curator.log, ~/logs/mdbook.log"
```

2. In `mdIngest/README.md`, extend the launch line after the 1-Prompt Setup code block to read: `After setup, launch with \`python ui/server.py\` (or \`start_ui.bat\` on Windows, or \`./start.sh\` on Linux/WSL — it mounts the Drive workspace if needed and starts all three servers). The landing page is at http://localhost:8088/.`

### Verify

1. `start.sh` exists at the mdIngest repo root and is executable (mode 100755).
2. Running `./start.sh` with the workspace already mounted prints `Workspace already mounted` and starts the three servers (Cockpit :8088, mdbook :3000, Curator :8000) — verify each responds on its port.
3. Running `./start.sh` with the workspace NOT mounted and `DD_HUB_FOLDER_ID` unset exits with the `not mounted and DD_HUB_FOLDER_ID is not set` message and does NOT start any server.
4. The README launch line mentions `./start.sh` for Linux/WSL.
5. Report PASS/FAIL per verify step, then STOP with a full summary.

## A5 — Remove committed episode data from ddma (clean slate)

### Where

- `ddma/docs/episodes.json`, `ddma/docs/episodes/244/`, `ddma/docs/episodes/245/`, `ddma/docs/episodes/246/`, `ddma/docs/episodes/247/`, `ddma/docs/plan.json`, and the repo-root `ddma/plan.json`.
- `ddma/scratch/run_curator.py`, the auto-seed block ("Auto-seed published episodes from docs/episodes/ for fresh git clones", around line 1298).

### Finding

The ddma repo ships committed episode data: `docs/episodes.json` lists episodes 244, 245, 246, 247; `docs/episodes/` holds their plan folders; `docs/plan.json` and the root `plan.json` hold episode 249's 21-clip plan. The Curator auto-seeds starter projects from `docs/episodes/` on a fresh clone, so a new user with a BLANK workspace still sees episodes 244–247. The repos are meant to be code-only — working episode data belongs in the workspace (DD_HUB_ROOT), and the published site gets its data via Publish. A fresh clone must start clean.

### Fix

1. Delete the committed seed episode data from the ddma repo: `docs/episodes.json`, the whole `docs/episodes/` folder (244, 245, 246, 247), `docs/plan.json`, and the repo-root `plan.json`. These are data, not code.
2. Ensure the auto-seed in `run_curator.py` does not restore them: with the seed files gone it must be a no-op (add a guard if the code would otherwise fail or re-create them). Do not remove the auto-seed mechanism's ability to seed from a workspace that actually has episodes — only stop it from pulling episode data out of the repo.
3. Do NOT change the Publish flow and do NOT change the sync that writes published data in this item — the goal here is only that a fresh clone starts with no episodes. Do NOT touch the deepDive repo.
4. Do NOT delete any code file, test, or documentation. Only the listed data files go.

### Verify

1. The listed data files are gone from the ddma repo (a fresh clone contains no `docs/episodes.json`, no `docs/episodes/`, no `docs/plan.json`, no root `plan.json`).
2. A fresh clone with a blank workspace shows NO episodes in the Curator (empty episode list / only the "Ingest New Episode" option).
3. Creating a new episode in the Curator still works and writes to the workspace.
4. Report PASS/FAIL per verify step, then STOP with a full summary.

## Guardrails

- Do NOT change any other file beyond what each item names. Do NOT touch the security items, the server code beyond the named handlers, or any other repo.
- Do NOT hardcode any episode number, API key, or credential.
- Do NOT change the caption editing, the revert button, the settings modal, the Publish flow, or the 1-Prompt Setup code block (except the one README launch line in A4).
- If a verify step is ambiguous, list the candidates and STOP — do not guess.
- Report PASS/FAIL per verify step, then STOP with a full summary.
