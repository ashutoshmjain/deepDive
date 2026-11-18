# C3 redo — untrack the actual mosaic_jobs.json / ingestion_progress.json

## Scope and head

- Repo: deepDive, head `0d52bb8a` (master). All facts below were verified at this head.
- This is a REDO of Batch 4 item C3. The Batch 4 agent untracked the WRONG files: it untracked `plan.json.bak`, `transcribe_gold.txt`, and 5× `podcast_edit.json` (those are now gone from the tree at `0d52bb8a`, and `.gitignore` gained `**/podcast_edit.json` + `**/transcribe_gold.txt` at lines 49–50). It did NOT untrack the files the C3 spec named. This spec fixes that — nothing else.
- Do NOT revert the agent's other untrackings. Do NOT touch `plan.json.bak`, `transcribe_gold.txt`, or `podcast_edit.json`. Do NOT touch `src/SUMMARY.md`.

## Where

- The 7 files are STILL tracked at head `0d52bb8a` (verified via the GitHub tree):
  - `ddma/projects/episode_245/mosaic_jobs.json`
  - `ddma/projects/episode_246/mosaic_jobs.json`
  - `ddma/projects/episode_247/mosaic_jobs.json`
  - `ddma/projects/episode_248/mosaic_jobs.json`
  - `ddma/projects/episode_249/mosaic_jobs.json`
  - `ddma/projects/episode_245/ingestion_progress.json`
  - `ddma/projects/episode_246/ingestion_progress.json`
- The root `.gitignore` has NO rule for `mosaic_jobs.json` or `ingestion_progress.json` (verified — the only nearby entries are `**/podcast_edit.json` and `**/transcribe_gold.txt` at lines 49–50).
- These files are derived runtime state: the heal rewrites `mosaic_jobs.json` on project load (`ddma/scratch/run_curator.py:5156` calls `heal_mosaic_project_state()`), and writes go through `update_mosaic_job_state` → `save_mosaic_jobs`. The tracked copies are stale partial snapshots (e.g. episode_249 has only keys 0, 2, 3, 4, 13, 14) — neither the source of truth nor kept current.

## Finding

Batch 4's C3 untracked 7 files, but they were the wrong 7. The spec's 7 files (`mosaic_jobs.json` ×5, `ingestion_progress.json` ×2) are still tracked, still churn on every heal/test-run, and still show as "modified" in git status. The `.gitignore` still does not cover them.

## Fix

1. Add to the root `.gitignore` (near the existing `**/podcast_edit.json` / `**/transcribe_gold.txt` lines):
   - `ddma/projects/*/mosaic_jobs.json`
   - `ddma/projects/*/ingestion_progress.json`
2. Run `git rm --cached` on exactly the 7 files listed above (enumerate with `git ls-files` first to confirm the list matches — if the count differs, STOP and report instead of guessing). Do NOT delete the working-tree files.
3. Do NOT commit — leave the untracking staged for review, per the Batch 4 convention. Only these two filenames get ignored; `ddma/projects/` stays tracked.

## Guardrails

- No Mosaic runs. No keys in git. No commit/push (fan-out is a separate human step).
- Do not touch any other file. Do not refactor. If the `git ls-files` count differs from 5 + 2, STOP and report — do not invent a file list.

## Verify

1. `git ls-files` no longer lists any `mosaic_jobs.json` or `ingestion_progress.json` under `ddma/projects/`.
2. All 7 files still exist on disk (working tree untouched).
3. `.gitignore` covers both patterns (`ddma/projects/*/mosaic_jobs.json` and `ddma/projects/*/ingestion_progress.json`).
4. The heal still writes `mosaic_jobs.json` at runtime (derived state, local-only now) — confirm by loading a project and checking the file's mtime bumps.
5. Report PASS/FAIL per verify step, then STOP with a full summary.
