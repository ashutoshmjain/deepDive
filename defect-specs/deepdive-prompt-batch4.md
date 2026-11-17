# Batch 4 — Round 4 remainder (ingest hardening + ddma code + repo data cleanup)

## Scope and head

- Repo: deepDive, head `839ca629` (master). All line numbers below were verified at this head.
- **Repo layout note:** `ddma.py`, `run_curator.py`, `test_curator.js` live under `ddma/` (top level), NOT `src/ddma/`. Use `ddma/ddma.py`, `ddma/scratch/run_curator.py`, `ddma/scratch/test-env/test_curator.js` in this spec. The canonical docs publication is `src/ddma/docs/episodes/`. The widget is `theme/book.js` AND `ingest/lightning-widget.js`, mirrored to `mdIngest/ui/lightning-widget.js`.
- This batch is 16 items, grouped by theme. Execute them in order. Report PASS/FAIL per verify step, then STOP with a full summary.

## Guardrails

- Fix in deepDive where the file lives there. Three files exist ONLY in the mdIngest repo (`Cargo.toml`, `CHANGELOG.md`, `start_ui.bat`) — edit those in mdIngest directly; there is no deepDive copy to fan out from. Do not edit any other standalone-repo file directly.
- No Mosaic runs. No keys in git. No commit/push (fan-out is a separate human step). Deletions and `git rm --cached` leave changes uncommitted for review.
- Do not refactor beyond what each item names. Do not touch the compile, the plan generation, the Mosaic modal, or any other dialog.
- For every deletion item: grep for references BEFORE deleting; if a live reference exists, do NOT delete — report it instead.
- If an item's fix is ambiguous, verify and report rather than guessing — do not invent a behaviour.

## Part A — ingest code (`ingest/server.py` + tests)

### A1. `update_title` ignores the `title_word_limit` setting

- **Where:** `ingest/server.py:4507` (the `/api/episode/update_title` handler branch; there is no standalone `update_title` function). The hardcoded truncation is at `:4524`: `clean_title_text = " ".join(title_words[:5]) if len(title_words) > 5 else raw_new_title`. The handler never calls `load_settings()`. The setting exists and is honored everywhere else: default `"title_word_limit": 5` at `server.py:156`, also `book.toml:22`; honored via `settings.get("title_word_limit", 5)` at `:3446`, `:3655`, `:4214`, `:4240`, `:4314`, `:4603`.
- **Finding:** One handler hardcodes a 5-word truncation while the setting it should honor exists and is used at six other sites.
- **Fix:** In the update_title handler, read the limit from settings (`word_limit = load_settings().get("title_word_limit", 5)`) and use `title_words[:word_limit]` instead of the hardcoded `[:5]`.
- **Verify:** With `title_word_limit` set to 3, update a long title and confirm it truncates to 3 words; with the default 5, confirm it truncates to 5. Confirm the other six call sites are untouched.

### A2. `sync_summary_file` silently drops unrecognized sections

- **Where:** `ingest/server.py:3160` (`def sync_summary_file`). It rebuilds SUMMARY.md from exactly 4 preserved parts: header lines (everything before the first mempool/template/chain link), regenerated mempool, regenerated template, and chain lines (everything from `- [chain` to EOF). Any other section is dropped. Today's live `src/SUMMARY.md` contains exactly those 4 top-level sections (`- [deepDive](./cover.md)` :3, mempool :44, template :49, chain :61) — so nothing is being dropped today; the hazard is latent. A new section inserted between the end of template (:60) and chain (:61) would be silently deleted on the next sync.
- **Finding:** The sync is a lossy rebuild from a fixed 4-section template. Any future section is silently deleted.
- **Fix:** Parse SUMMARY.md generically and carry forward any unrecognized sections verbatim (in their original position relative to the known sections) instead of rebuilding from the fixed template.
- **Verify:** Build a test SUMMARY.md with an extra section inserted between template and chain, run `sync_summary_file` on the COPY, and confirm the extra section survives byte-identical. Do NOT test on the live `src/SUMMARY.md`.

### A3. Import-time side effects: directory creation + silent re-root

- **Where:** `ingest/server.py:37-38` (`candidate_roots = [PROJECT_ROOT, PROJECT_ROOT.parent / "deepDive"]` + `PROD_ROOT = next((r for r in candidate_roots if (r / "src" / "SUMMARY.md").exists() …), PROJECT_ROOT)`) silently re-roots to a sibling deepDive checkout if its SUMMARY.md is >1000 bytes. `server.py:46-47` (`IMG_DIR.mkdir(parents=True, exist_ok=True)` / `VID_DIR.mkdir(...)`) creates `src/img` + `src/vid` in whichever root was just auto-discovered. Both run at module top level — they execute on `import server`.
- **Finding:** Importing the module has filesystem side effects: it creates directories and can silently switch the project root to a sibling checkout.
- **Fix:** (1) Move the `IMG_DIR`/`VID_DIR` mkdir calls out of import time — create the directories in the server startup path instead, so importing the module creates nothing. (The `IMG_DIR`/`VID_DIR` constants themselves stay at module level; only the mkdir calls move.) (2) When the PROD_ROOT auto-discovery selects the sibling checkout instead of PROJECT_ROOT, log a loud warning naming both paths instead of silently re-rooting. Do NOT change which root is selected — only make the selection visible.
- **Verify:** Import `server.py` from a clean checkout and confirm no `src/img` or `src/vid` directories are created. Run with a sibling checkout present and confirm the warning names the chosen root.

### A4. E2E test assumes a running server; puppeteer version skew; no CI runs it

- **Where:** `ingest/tests/cockpit_e2e.js:21` (`const BASE_URL = process.env.TEST_URL || 'http://localhost:8088'`) — the test assumes a server is already running. No `child_process`/`spawn` of the server anywhere in the file (its only contact with `server.py` is a static source read at `:176`). `ingest/tests/package.json`: `"puppeteer": "^24.4.0"` vs `"puppeteer-core": "^24.43.1"` — skewed. No workflow runs the E2E: the only workflow in deepDive is `.github/workflows/mdbook.yml` (mdBook deploy only, no E2E step).
- **Finding:** The E2E suite cannot run on its own (it needs a manually started server), its two puppeteer packages disagree on version, and nothing in CI runs it.
- **Fix:** (1) Make `cockpit_e2e.js` self-contained — spawn the server (`python ingest/server.py`) on a test port in the test setup (or a `pretest` script) instead of assuming `:8088` is already running. (2) Pin `puppeteer` and `puppeteer-core` to the same version in `ingest/tests/package.json`. (3) Add a CI workflow (e.g., `.github/workflows/e2e.yml`) that runs the E2E suite.
- **Verify:** Run the E2E suite from a clean state with no server running — it starts its own server and passes. `package.json` shows matching puppeteer versions. The workflow file exists and names the E2E job.

## Part B — ingest launchers, version, sync check

### B1. `start_ingest.bat` is not layout-tolerant; bare `python`

- **Where:** deepDive's `start_ingest.bat` exists only at the repo root (no `ingest/start_ingest.bat`). It does `cd /d "%~dp0"` then bare `python ingest/server.py` — hardcoded to the `ingest/` layout, not layout-tolerant. mdIngest's launcher is `start_ui.bat` at the mdIngest repo root, and it IS layout-tolerant (`if exist "ingest\server.py" (python ingest\server.py) else if exist "ui\server.py" (python ui\server.py)`), but it also uses bare `python`.
- **Finding:** deepDive's launcher breaks if the layout differs, and both launchers use bare `python` with no version fallback.
- **Fix:** Make deepDive's `start_ingest.bat` layout-tolerant like mdIngest's: probe for `ingest\server.py`, fall back to `ui\server.py` if present, else print an error and stop. Use `py -3` with a fallback to bare `python` (not bare `python` alone). Apply the same `py -3` fallback to mdIngest's `start_ui.bat` (that file exists only in mdIngest — edit it there directly).
- **Verify:** Run the deepDive launcher from the deepDive checkout — the server starts. Confirm the probe/fallback logic is present in both launchers and neither uses bare `python` alone.

### B2. Version skew across the mdIngest files

- **Where:** These files exist only in the mdIngest repo (no deepDive mirror) — edit them in mdIngest directly. `mdIngest/VERSION` = `0.3.0`; `mdIngest/Cargo.toml:3` `version = "0.1.0"`; `mdIngest/CHANGELOG.md` top entry is already `[0.3.0] - 2026-08-28`, but its roadmap footer still says `v0.1.0 (Current)` (and `v0.1.0 (Current Alpha)`). `mdIngest/README.md` states no version at all — do not add one.
- **Finding:** The crate version, the VERSION file, and the changelog roadmap disagree about the current version.
- **Fix:** Bump `Cargo.toml` to `0.3.0` (matching VERSION) and change the CHANGELOG roadmap footer from `v0.1.0 (Current)` to `v0.3.0 (Current)` (including the `v0.1.0 (Current Alpha)` line). Do NOT touch README.md.
- **Verify:** `Cargo.toml`, `VERSION`, and `CHANGELOG.md` all agree on `0.3.0`. README.md is unchanged.

### B3. No fan-out diff check (manual copy only)

- **Where:** All six mirrored files are byte-identical between `deepDive/ingest/` and `mdIngest/ui/` at the heads (`server.py`, `cockpit.html`, `landing.html`, `lightning-widget.js`, `requirements.txt`, `update_listen_buttons.py`, plus `tests/cockpit_e2e.js` and `tests/package.json`). `GEMINI.md:21-40` (deepDive) is current: it states the canonical direction (deepDive → mdIngest/ui), lists the mirrored files including `tests/cockpit_e2e.js`, and documents a manual blob-compare step (`git hash-object`) after mirroring. But there is no sync script or diff check anywhere: no `scripts/` dir, no `.sh` file, and the only workflow is `.github/workflows/mdbook.yml` (docs deploy only — no diff step). The protocol is purely manual.
- **Finding:** The mirror is in sync today only because a human remembers to copy and compare. There is no automated check that catches drift.
- **Fix:** Add a fan-out diff-check script in deepDive (e.g., `scripts/check_fanout.py`) that hash-compares the GEMINI.md Step 1 ingest-side files between `deepDive/ingest/` and the sibling `mdIngest/ui/` checkout, exits non-zero naming any mismatch, and exits 0 when in sync. Document it as a step in GEMINI.md's push protocol (run the check before pushing).
- **Verify:** Run the script with the files in sync — exit 0. Touch one copy so the hashes differ — exit non-zero, naming the differing file. Restore the copy.

## Part C — ddma code (`ddma/ddma.py` + `ddma/scratch/run_curator.py`)

### C1. Silent Gemini skip + `--mode` help mismatch

- **Where:** `ddma/ddma.py:700` — `if api_key and not api_key.startswith("AQ."):` guards the whole Gemini loop. A missing key or an `AQ.`-prefixed key skips it with no message; the only output is the fallback line at `:723`, `"[Tripartite Caster] Utilizing deterministic sentence snapping fallback..."`, which never says Gemini was skipped or why. There is no `get_gemini_api_key` definition in `ddma.py` (only a guarded `globals()` check at `:643`); the key comes from env or `settings.json`. `ddma/ddma.py:3238` — `mode: str = typer.Option("tripartite", help="Ingestion mode: 'structured' (fast uniform sentence snapping) or 'unstructured' (Gemini AI topic discovery)")`. The default is `tripartite`, which the help never mentions; the handler at `:3294` only branches on `mode == "tripartite"`, everything else falls through to the uniform fallback at `:3300`.
- **Finding:** Two small honesty gaps in the same CLI: a skipped Gemini run is silent, and the `--mode` help describes two modes while the default is a third one it never names.
- **Fix:** (1) At `:700`, when the Gemini key is missing or starts with `AQ.`, emit a warning naming the reason (missing key / placeholder key) before falling back — do not silently skip. (2) At `:3238`, correct the `--mode` help to list all three modes (`tripartite`/`structured`/`unstructured`) and state the true default (`tripartite`).
- **Verify:** Run ingest-episode with no Gemini key set and confirm a warning names the missing key. Run `ddma.py ingest-episode --help` and confirm the help lists `tripartite` as the default.

### C2. `snap_quote_to_words` exposed as a CLI command

- **Where:** `ddma/ddma.py:3198` `@app.command()` directly above `:3199` `def snap_quote_to_words(quote, words, search_start_sec=0.0):` — exposed as `snap-quote-to-words`. Internal callers (`:751, :757, :765, :770, :772`) pass real word-lists. From the CLI, Typer would pass `words` as a string, and `:3211` (`w.get(...)`) would raise `AttributeError: 'str' object has no attribute 'get'` — it crashes.
- **Finding:** An internal helper is exposed as a CLI command it cannot serve — invoking it from the CLI crashes.
- **Fix:** Remove the `@app.command()` decorator at `ddma/ddma.py:3198`. Do NOT change the function itself or its internal callers.
- **Verify:** `ddma.py --help` no longer lists `snap-quote-to-words`. The internal callers still work (run the existing test suite / a quick import check).

### C3. Stale `mosaic_jobs.json` / `ingestion_progress.json` snapshots are tracked

- **Where:** `ddma/projects/episode_245/mosaic_jobs.json` has only keys 15–18; `episode_246` has 1–10, 12–17 (missing 11 and 18); `episode_247` has only 1, 3, 4; `episode_248` only 1–5; `episode_249` only 0, 2, 3, 4, 13, 14. The heal still rewrites the file: `ddma/scratch/run_curator.py:5156` calls `heal_mosaic_project_state()` on project load, and Case 3 (`:655-660`) only upgrades an existing non-completed entry to completed — it never creates entries for missing clips, so the gaps persist. Writes go through `update_mosaic_job_state` (`:454-456` → `save_mosaic_jobs`). The root `.gitignore` has NO rule for `mosaic_jobs.json` or `ingestion_progress.json`, and `ddma/projects/` is not ignored.
- **Finding:** Committed job/progress snapshots are stale partial state, and the heal rewrites them at runtime — so the tracked copies are neither the source of truth nor kept current. They are derived state that should not be in git.
- **Fix:** Add `ddma/projects/*/mosaic_jobs.json` and `ddma/projects/*/ingestion_progress.json` to the root `.gitignore`, then `git rm --cached` the tracked copies (5 mosaic_jobs.json + 2 ingestion_progress.json — enumerate with `git ls-files`; do NOT delete the working-tree files). Do NOT commit — leave the untracking staged for review. Only these two filenames get ignored; `projects/` stays tracked.
- **Verify:** `git ls-files` no longer lists any `mosaic_jobs.json` or `ingestion_progress.json`; the files still exist on disk; `.gitignore` covers both patterns; the heal still writes them at runtime (derived state, local-only now).

### C4. `start_curator.bat` ignores the venv; RUN_GUIDE has stale paths

- **Where:** `ddma/start_curator.bat` still runs bare `python scratch/run_curator.py` with no `.venv` activation (full file is 8 lines; no activation). `ddma/RUN_GUIDE.md` still says "Open the `Longs` folder in Windows File Explorer" and still links `[plan.json](file:///c:/Users/ashut/OneDrive/Documents/Longs/plan.json)`. Note: no "Track B installs into .venv" text exists in any README at this head, so do NOT assume a venv exists — activate one only if present.
- **Finding:** The Curator launcher never activates the venv, and the run guide points at a stale personal folder that no longer holds the plan.
- **Fix:** In `ddma/start_curator.bat`, activate the venv if one exists next to the script (`.venv\Scripts\activate.bat`), otherwise fall back to bare `python`. In `ddma/RUN_GUIDE.md`, replace the `Longs` folder references and the `file:///c:/Users/ashut/OneDrive/Documents/Longs/plan.json` link with the corresponding paths inside the repo (the plan lives at `ddma/projects/episode_<N>/plan.json`).
- **Verify:** The launcher activates the venv when `.venv` exists and still starts the Curator when it does not. Grep RUN_GUIDE.md for `Longs` and `file:///c:/Users/ashut` — zero matches.

## Part D — repo data cleanup

### D1. Incomplete `episode_244` project (dead auto-repair)

- **Where:** `ddma/projects/episode_244/` still has exactly 3 files: `plan.json`, `plan_snapshot.json`, `project_info.json` — no `.m4a`, no `transcription.json`. `project_info.json` still claims `"status": "ready"` with `"audio_filename": "244.m4a"`, and no `244.m4a` exists anywhere in the repo (only `245.m4a`/`246.m4a` are tracked). Both repair paths are dead and can never fire: migration (`ddma/scratch/run_curator.py:1270-1297`) requires `transcription.json` + `plan.json` + `244.m4a` in the `ddma/` root; auto-seed (`:1298-1330`) reads `docs/episodes/<ep>/plan.json`, but `ddma/docs/episodes/` does not exist at all in the tree (the plans live at `src/ddma/docs/episodes/<ep>/plan.json`). Both branches are also gated on the project dir NOT existing — it exists — so they are no-ops. (`migrate_legacy_files()` does run at server startup, `main()` at `:5662`.)
- **Finding:** A project entry that can never work: its audio and transcription are gone, and both repair paths are dead. The published episode lives independently at `src/ddma/docs/episodes/244/` (19 entries: `plan.json` + 16 clips), `episodes.json`'s 244 entry points at that published copy, and the project `plan.json` (69,810 B) differs from the published plan (69,342 B) — the project copy is a stale fork.
- **Fix:** Delete `ddma/projects/episode_244/` (3 files). Before deleting, confirm the published episode at `src/ddma/docs/episodes/244/` is intact (plan.json + clips present) and grep the repo for references to `projects/episode_244` (expect none outside the generic migration/seed code). Do NOT touch the migration/seed code (it is generic, not 244-specific) and do NOT touch the published copy. Do not commit.
- **Verify:** The project dir is gone; the Curator's project list no longer shows 244; the published 244 still plays.

### D2. Stale `plan.json.bak` + `remix_plan.json`

- **Where:** All three still tracked: `ddma/plan.json.bak` still opens with `"title": "Einstein's Magnet-Conductor Paradox", "start": 2430.36`; `ddma/remix_plan.json` still the same title, start 2477.24; `ddma/plan.json` is the 249 plan (`"What Exactly Is Reality?"`, clip 0). No code reads `remix_plan.json` or `plan.json.bak` (grep across `run_curator.py`, `ddma.py`, `beats_server.py`, `test_curator.js` — only the unrelated `/remix-clip` endpoint mentions "remix"). The root `.gitignore` already has `*.bak`, but tracked files stay tracked.
- **Finding:** Two stale plan files for an older episode sit at the ddma root, unread by any code. The third file, `ddma/plan.json`, is NOT stale — it is live regenerated state (the Curator copies the active project's plan there on project load, `run_curator.py` ~`:5115`).
- **Fix:** Delete `ddma/plan.json.bak` and `ddma/remix_plan.json` only. Do NOT delete `ddma/plan.json`. Before deleting, grep the repo for reads of `plan.json.bak` / `remix_plan.json` (expect none). Do not commit.
- **Verify:** The two files are gone; `ddma/plan.json` is still present and still gets refreshed on project load.

### D3. `episodes.json` social handles point at the wrong account

- **Where:** Both copies are byte-identical (same blob SHA): `ddma/docs/episodes.json` and `src/ddma/docs/episodes.json`. Episode 244's links still read `https://www.instagram.com/deepdivegemini` and `https://www.tiktok.com/@deepdivegemini`; every other episode (245–250) has empty `links: {}`. The standing accounts are `@shutoshabot`.
- **Finding:** The 244 entry links to the wrong social accounts; the rest have no links at all.
- **Fix:** In BOTH `episodes.json` copies, change episode 244's links from `instagram.com/deepdivegemini` and `tiktok.com/@deepdivegemini` to `instagram.com/shutoshabot` and `tiktok.com/@shutoshabot`. Do NOT touch other episodes' links.
- **Verify:** Both files read `@shutoshabot` for 244; both files remain byte-identical; no other links changed.

### D4. Duplicated `archetypes/ep248/` directory

- **Where:** `ddma/archetypes/ep248/` still exists with 46 files; 42 of the 46 shared basenames are byte-identical to the top-level set (blob-SHA comparison); only 4 differ: `clip_01/02_gemini_scenes.py` + `clip_01/02_meta.json`. The top level has 48 blobs (the 46 shared + `chapter_01_scenes_strict.py`, `manim_compat.py`); `ep248/` has no unique basenames. Nothing reads it: zero references to `ep248` in `run_curator.py`, `ddma.py`, or `beats_server.py`, and `ddma/archetype_studio.py:14` sets `ARCHETYPES_DIR` to top-level `ddma/archetypes/`, with all lookups using `archetypes/clip_XX_gemini_scenes.py` paths only.
- **Finding:** A near-complete duplicate of the archetype set sits in an unread directory. The 4 differing clip_01/02 files are orphaned variants nothing reads — deleting them is part of this item.
- **Fix:** Delete `ddma/archetypes/ep248/` (46 files). Before deleting, grep the repo for references to `ep248` (expect zero in code). Do not commit.
- **Verify:** The `ep248/` dir is gone; the top-level `archetypes/` set is intact; the Curator/Beats still resolve archetypes.

### D5. Triplicated music directories + duplicate `(1).mp3`

- **Where:** All three dirs still exist with the same counts: `ddma/music/` 29 files, `ddma/docs/assets/music/` 27, `src/ddma/docs/assets/music/` 27. All 27 shared filenames are byte-identical across all three (blob SHAs equal), including `deepDive-strong.mp3`; the `Sour Tennessee Red (Sting)… (1).mp3` duplicate is present in all three. `ddma/music/` is canonical: it holds 2 files the mirrors lack (`deepDive-conclusion.mp3`, `deepDive-title-music.mp3`), which `ddma.py` references (`:524, :605, :808`); playback resolves via `get_music_path` (`run_curator.py:1098-1109`, `ddma.py:1376-1390`), which tries `music/` first. The published site files (`src/ddma/docs/index.html`, `player.js`, `documentation.html`) contain zero references to `assets/music`.
- **Finding:** The same music is stored three times, plus a stray `(1).mp3` duplicate in each copy. Only `ddma/music/` is read by the code.
- **Fix:** Delete both `docs/assets/music/` mirrors (`ddma/docs/assets/music/` and `src/ddma/docs/assets/music/`, 27 files each) and the duplicate `Sour Tennessee Red (Sting)… (1).mp3` in `ddma/music/` (so the canonical dir keeps 28 files). Keep `ddma/music/` — it is canonical. BEFORE deleting either mirror, grep the whole repo for `assets/music` references — if any live reference exists to a mirror, do NOT delete that mirror; report it instead. Do not commit.
- **Verify:** Both mirrors gone (or reported with the blocking reference); `ddma/music/` intact with 28 files and no `(1).mp3` duplicate; the Curator still resolves music.

## Global verify (run after all items)

1. Run the existing test suites and report the counts (`test_compile_scope.py`, `test_canonical_audio_compile.py`, `test_plan_clip0_title.py`, `test_mosaic_mux_integrity.py`, `test_curator.js` — do NOT run TEST 20 without first confirming its `finally` restore at `test_curator.js:1108` is intact; also `ingest/tests/cockpit_e2e.js` with its new self-contained setup from A4). Report PASS/FAIL per suite.
2. Start the Curator (`:8000`) and the cockpit (`:8088`) and confirm both load with no console errors.
3. Confirm the fan-out diff check (B3) passes with the files in sync.
4. Do NOT publish any clip as part of this verify. Do NOT trigger a Mosaic run. Do NOT commit or push (fan-out is a separate human step).
5. Report PASS/FAIL per item (A1–A4, B1–B3, C1–C4, D1–D5), then STOP with a full summary.
