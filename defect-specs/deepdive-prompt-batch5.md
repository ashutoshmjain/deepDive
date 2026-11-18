# Batch 5 — C3 redo + Issue 90 + Issue 88 + cockpit/ddma fixes + verify-only confirmations

## Scope and head

- Repo: deepDive, head `7061d4e7` (master). All line numbers below were verified at this head.
- **Repo layout note:** `ddma.py`, `run_curator.py`, `test_curator.js` live under `ddma/` (top level), NOT `src/ddma/`. Use `ddma/ddma.py`, `ddma/scratch/run_curator.py`, `ddma/scratch/test-env/test_curator.js` in this spec. The canonical docs publication is `src/ddma/docs/episodes/`. The widget is `theme/book.js` AND `ingest/lightning-widget.js`, mirrored to `mdIngest/ui/lightning-widget.js`.
- This batch is 14 entries, grouped by theme. Parts A–D are fixes; Part E is verify-only (items already resolved in code — confirm and report, do NOT change code). Execute them in order. Report PASS/FAIL per verify step, then STOP with a full summary.
- Coverage note (for the human reader, not part of any Fix): A1 is the C3 redo, A2 is the caption-dialog simplification, B1 removes the "Social Prose & Nostr" sub-tab, B2 gives mempool items a path, B3 runs the Listen-buttons updater for episode 250, C1 removes a stale hardcoded episode title from compile-clip, C2 makes settings load fail loudly on corrupt files, D1 adds the missing GET-side-effects test, and E1–E6 confirm six items that verification found already resolved. Security items (dev-server hardening) are explicitly OUT of this batch — they go in a later batch.

## Guardrails

- Fix in deepDive where the file lives there. Three files exist ONLY in the mdIngest repo (`Cargo.toml`, `CHANGELOG.md`, `start_ui.bat`) — edit those in mdIngest directly; there is no deepDive copy to fan out from. Do not edit any other standalone-repo file directly.
- No Mosaic runs. No keys in git. No commit/push (fan-out is a separate human step). Deletions and `git rm --cached` leave changes uncommitted for review.
- Do not refactor beyond what each item names. Do not touch the compile, the plan generation, the Mosaic modal, or any other dialog — except where an item explicitly names it.
- For every deletion item: grep for references BEFORE deleting; if a live reference exists, do NOT delete — report it instead.
- If an item's fix is ambiguous, verify and report rather than guessing — do not invent a behaviour.
- **Workflow file note (not a code item):** `.github/workflows/e2e.yml` is written but untracked on disk. Include it in the Batch 5 push IF a workflow-scope token is available; otherwise leave it untracked and report that. Do not write or change any workflow file as part of this batch.
- **Verify-only items (Part E):** do NOT change code for these. Confirm the stated facts in code and data, then report PASS/FAIL. If a stated fact does NOT hold, report it as a FAIL with the evidence — do not silently "fix" it.

## Part A — Included by reference (execute the referenced spec exactly as written)

### A1. Untrack the stale job/progress snapshots (C3 redo)

- **Where:** Execute `defect-specs/deepdive-prompt-c3-redo-untrack-mosaic-jobs.md` exactly as written. It is included here by reference, not rewritten.
- **Verified at this head:** the 7 files it names are still tracked at `7061d4e7` — `ddma/projects/episode_245/mosaic_jobs.json`, `episode_246/mosaic_jobs.json`, `episode_247/mosaic_jobs.json`, `episode_248/mosaic_jobs.json`, `episode_249/mosaic_jobs.json`, plus `ddma/projects/episode_245/ingestion_progress.json` and `episode_246/ingestion_progress.json`. The root `.gitignore` still has no rule for either filename.
- **Verify:** per the referenced spec (git ls-files clean, files still on disk, `.gitignore` covers both patterns, heal still writes at runtime).

### A2. Simplify the clip text dialog to captions-only

- **Where:** Execute `defect-specs/deepdive-prompt-caption-dialog-simplify.md` exactly as written. It is included here by reference, not rewritten.
- **Fix direction (summary):** replace the two-pane dialog with a single captions box — timestamps display-only, text editable; on Save, pair each line's text with the ORIGINAL chunk's start/end by line position (timestamps from the textarea are ignored entirely); keep Save + Revert + Cancel; remove the script pane, Auto-Align, Whisper Sync, Copy .ASS, stats, and the Mosaic "Edit Clip Text" button.
- **Verified at this head:** the dialog is still the old two-pane version — modal `#clipTextModalOverlay` at `ddma/curator.html:1662`, script textarea `clipTextInput` at `:1691`, Whisper Sync button `whisperResyncCaptionsBtn` at `:1703`. **Note:** the referenced spec's line numbers were written against an earlier head and have shifted by ~5 lines — re-verify every line number at the current head before editing; the element IDs and structure are unchanged.
- **Verify:** per the referenced spec (one captions box, timestamps unchanged after a text edit and after a deliberate timestamp edit, Revert restores saved text, Cancel saves nothing, Mosaic modal has no "Edit Clip Text" button, suites pass).

## Part B — Cockpit fixes (`ingest/cockpit.html` + `ingest/server.py`)

### B1. Remove the "Social Prose & Nostr" sub-tab

- **Where:** `ingest/cockpit.html`, Podcast tab (`#tab-view-narrative`, :1619). The mode switcher is at :1620–1628 (two buttons: `btn-submode-podcast` at :1622, `btn-submode-nostr` at :1625, labelled "📝 Social Prose & Nostr"). The sub-tab pane is `<div id="submode-view-nostr">` at :1677–1735 (comment "SUBMODE B: SOCIAL PROSE & NOSTR (PRESERVED)" at :1676). The switcher function `switchPodcastSubmode` is at :3015–3033; the `podcastSubmode` variable is at :3006. Two handlers exist only for this sub-tab: `streamlineNarrative` (called from the sub-tab toolbar at :1681, defined at :4739) and `openExternalVim` (called at :1690, defined at :4790) — verified to have no other callers.
- **Finding:** The sub-tab's purpose (edit the transcript into a long-form article) is obsolete — that job belongs to the distribution agent now. The sub-tab is also the broken view: it shows "No transcript loaded" for episodes whose transcript exists and displays fine in the adjacent "Podcast Studio & Cuts" sub-tab. Keeping it means keeping a dead editor and a misleading error.
- **Fix:** (1) Remove the mode-switcher div (:1620–1628) entirely and make the Podcast Studio view (`#submode-view-podcast`, :1631) always visible — with one sub-mode left, there is nothing to switch. (2) Remove the SUBMODE B div (:1677–1735) entirely. (3) Remove `switchPodcastSubmode` (:3015–3033) and the `podcastSubmode` variable (:3006). (4) Remove `streamlineNarrative` (:4739) and `openExternalVim` (:4790) ONLY after confirming they have no other callers (verified above — if a caller appears, do NOT remove that function; report it instead). Do NOT remove the Nostr Long-Form Publication Pipeline preview card (`#narrative-nostr-preview`, :2007+) or the server-side Nostr helpers (`streamline` / `extract_nostr_metadata` in `ingest/server.py`) — those serve article publication, not this editing sub-tab, and are a different feature.
- **Verify:** The Podcast tab loads with only "Podcast Studio & Cuts" visible and no "Social Prose & Nostr" tab or button. Episode 249's transcript displays in Podcast Studio. No console errors on load. Grep for `btn-submode-nostr`, `submode-view-nostr`, `switchPodcastSubmode`, `streamlineNarrative`, `openExternalVim` — zero matches. The Nostr publication preview card still renders where it did before.

### B2. Mempool items carry no path

- **Where:** `ingest/server.py:3077` (`def parse_summary_structure`). It builds mempool/template/chain items with `filename`, `slug`, `title`, `has_image`, `vid_count`, `is_locked`, `exists`, `number` — no `path` field. The episode loader `GET /api/episode` at :3798 resolves `SRC_DIR / filename` and returns `filename`, `title`, `content`, `word_count`, `has_cover`, `videos`, `is_draft` — no `path`; on a miss it sends a bare 404 "Episode not found" with no indication of where it looked. The mine handler `POST /api/template/mine` at :4330 resolves `SRC_DIR / filename` the same way.
- **Finding:** The slug-to-file mapping is reconstructed in every consumer from `filename` alone. A slug that does not resolve fails with a bare 404 that does not say where it looked, so a missing or misplaced draft is undebuggable from the UI.
- **Fix:** (1) Add a `"path"` field to each item returned by `parse_summary_structure` — the resolved relative path `src/<filename>`. (2) Add the same `"path"` field to the `/api/episode` response. (3) Include the resolved path in the 404 error message (e.g. "Episode not found at src/<filename>"). Do NOT change how the file is resolved — only make the resolved path explicit and visible.
- **Verify:** Fetch the status endpoint and confirm each mempool item carries a `"path"` starting with `"src/"`. Request `/api/episode` with a nonexistent filename and confirm the 404 names the resolved path. Mine a draft end-to-end and confirm it still works unchanged.

### B3. Episode-specific Listen buttons — run for episode 250, verify the trigger

- **Where:** `ingest/update_listen_buttons.py` (the deterministic updater — exists and implements exactly three buttons, the `<!-- LISTEN_BUTTONS_START -->` / `<!-- LISTEN_BUTTONS_END -->` markers, per-platform fallback to the show URL, and never constructs or guesses a URL). Cockpit button "Update Listen Buttons" at `ingest/cockpit.html:2109` (`triggerUpdateListenButtons` at :4972) calling `POST /api/episode/update_listen_buttons` (`ingest/server.py:5117`). `src/249.md` already carries the markers (:235–237) with the three episode URLs. `src/250.md` has NO markers and NO episode URLs yet.
- **Finding:** The updater and the manual trigger exist and episode 249 is done, but episode 250's page still shows the generic show buttons. The automated watcher trigger belongs to the Docker watcher (a separate, deferred effort) and is out of scope here.
- **Fix:** (1) Using the cockpit "Update Listen Buttons" action (or the CLI one-liner), run the updater for episode 250 — but ONLY if `dd_hub/episodes/250/podcast_urls.json` exists; if it does not exist, do NOT guess any URL — report that 250 is pending the JSON and stop. (2) Confirm the output: exactly three buttons (Spotify, Apple Podcasts, Fountain.fm) in that order, wrapped in the markers, per-platform fallback to the show URL where an episode URL is missing, and NO YouTube Music button on the page. (3) Do NOT build the watcher; do NOT change the updater's logic.
- **Verify:** Read the updated `src/250.md` (and fetch the live page once rebuilt) and confirm the three hrefs equal the episode URLs from the JSON (or the show-URL fallback where an episode URL is missing); confirm the markers are present and nothing else on the page changed; confirm there is no YouTube Music button. If the JSON was absent, report that instead of a page change.

## Part C — ddma / Curator fixes

### C1. Compile-clip falls back to a stale hardcoded episode title

- **Where:** `ddma/ddma.py:2252` — the compile-clip command defaults `episode_title` to `"Life, Death and the Lysosome"` (a stale episode's title). The plan's clip 0 title is already correct (episode 250 clip 0 is `'What Exactly is Infinity?'`), and compile resolves the title from `project_info.json` at :2342–2352 and again at :2589–2601 — but if `project_info.json` is missing or lacks a title, the title card falls back to the hardcoded stale title. The title card for clip 0 uses the episode title at :2606 (`title_text = title if title else (ep_title if num == 0 else f"Part {num}")`), and :2599 carries a special case that compares against the hardcoded string.
- **Finding:** A hardcoded title from an old episode is the fallback for every episode's title card. The plan generation already sets clip 0's title correctly, but the compile path can still surface the wrong episode's title on screen.
- **Fix:** Change the compile-clip `episode_title` default from `"Life, Death and the Lysosome"` to `None`. Resolve the episode title in this order: explicit `--episode-title` flag → `project_info.json` `"title"` → the plan's clip 0 title. Remove the special-case check at :2599 that compares against the hardcoded string. Never fall back to a hardcoded episode title; if none of the three sources resolves, use the episode number (e.g. `"EPISODE 250"`) on the title card. Do NOT change the plan generation (it already sets clip 0's title correctly).
- **Verify:** Grep `ddma/ddma.py` for `"Life, Death and the Lysosome"` — zero matches. Compile a test clip 0 (or dry-run the title resolution) and confirm the title card reads the episode title from `project_info.json` / the plan, not the stale default. Confirm the plan's clip 0 title is unchanged.

### C2. Settings load swallows a corrupt-file error instead of failing loudly

- **Where:** `ddma/scratch/run_curator.py:93` (`def safe_load_json`) — already logs and raises `RuntimeError` when a file exists but is unreadable after retries (verified). `run_curator.py:115` (`def load_settings`) — catches the exception from `safe_load_json` and falls back to empty settings (`{}`) with only a printed message: vault corrupt at :122–124 ("ERROR: vault settings.json … is corrupt … using empty settings"), local corrupt at :130–132. Bare `except:` count is 0 (verified). The `small.en` comment is gone from `ddma/ddma.py` (verified).
- **Finding:** `safe_load_json` raises, but `load_settings` catches it and continues with empty settings — so a corrupt settings file is silently papered over and the app runs with missing keys and paths. The failure-loudness rule requires log + raise, not silent fallback.
- **Fix:** In `load_settings`, do NOT swallow `safe_load_json`'s `RuntimeError` when the settings file EXISTS but is corrupt — log the error and re-raise it. Keep the existing fallback when NO settings file exists at all (fresh clone: vault missing → try local; local missing → `{}` + env vars is fine, because `safe_load_json` returns `None` for a missing file and does not raise). Only the corrupt-file path changes: corrupt vault → log + raise; corrupt local (when the vault is missing) → log + raise. Do not change the env-var overrides or the vault-first / local-fallback order.
- **Verify:** With a corrupt vault `settings.json` (a file that exists but is not valid JSON), starting the Curator fails loudly with the `RuntimeError` instead of running on empty settings. With NO settings file at all, the Curator still starts (fresh-clone path). With a valid settings file, behaviour is unchanged.

## Part D — Tests

### D1. Missing test for the GET-endpoint write-side-effects fix

- **Where:** `ddma/scratch/test-env/test_curator.js` already has TEST 22 (settings-import guard, :1120), TEST 23 (Curator CWD-independence, :1142), and TEST 24 (cast-tripartite registration, :1152). There is NO test asserting the remaining fix: that GET endpoints no longer trigger a sync/write (the sync moved to POST `/api/episode/sync_clips` and POST `/api/git/push` only; `do_GET` in `ingest/server.py` has no sync call). TEST 21 (music-dropdown basename match, :1053) is a different item and does not cover this.
- **Finding:** Three of the four items have tests; the GET-side-effects fix has neither a test nor a report note.
- **Fix:** Add a test (in `test_curator.js` or `ingest/tests/cockpit_e2e.js`, whichever fits the existing pattern) that performs a GET on an episode/status endpoint and asserts no sync/write occurred (for example, the plan file's mtime/content is unchanged and no sync endpoint was invoked). A test is preferred; if a test genuinely cannot express this, add an explicit report note stating the fix is covered by code inspection (`do_GET` has no sync call) instead. Do not change the server code.
- **Verify:** The new test exists and passes; the full suite still passes (report the counts).

## Part E — Verify-only: already resolved, confirm and report (do NOT change code)

### E1. Publish button state survives a refresh

- **Verified at this head:** the server persists `published=True` + `published_url` on the clip (`ddma/scratch/run_curator.py:4285–4287`), the card renderer reads `clip.published` and shows "✅ Published" (green) vs "🚀 Publish" (purple) (`ddma/curator.html:6708–6714`), and the plan carries `published: True` for clips 13, 15, and 16 in BOTH the project plan (`ddma/projects/episode_249/plan.json`) and the published plan (`src/ddma/docs/episodes/249/plan.json`).
- **Verify:** Confirm all three facts above in code and data, then report PASS. Do NOT change code. If any fact does NOT hold, report it as FAIL with the evidence.

### E2. Music dropdown matches the clip sting by basename

- **Verified at this head:** the dropdown computes the basename of `seg.music_file` (splitting on `/` and `\`) and selects the matching file (`ddma/curator.html:6511–6519`); the plan stores `'music/<name>'` (e.g. `'music/Bluesy Vibes (Sting) - Doug Maxwell_Media Right Productions.mp3'`) and the code strips the prefix before comparing against the bare filenames from `/list-music`. TEST 21 in `test_curator.js` (:1053) already asserts this behaviour.
- **Verify:** Confirm the basename-matching code is present and TEST 21 passes, then report PASS. Do NOT change code. Note: if a clip's `music_file` matches no file in `/list-music`, "Digital Silence" is the correct fallback (a data issue, not a code bug) — report that if observed.

### E3. Export-to-Mosaic reads the plan through load_plan

- **Verified at this head:** the `/export-to-mosaic` handler reads the plan via `load_plan(project_id, writer="curator")` — hub-first, failing loudly when unreachable (`ddma/scratch/run_curator.py:3740`, comment "Hub-first plan read … never export from a stale cache"). The only direct `plan.json` file access left in `run_curator.py` is a WRITE at :2514, not a read.
- **Verify:** Confirm the handler uses `load_plan` and that no direct plan read exists in that handler, then report PASS. Do NOT change code. Note: `project_info.json` is still read directly from the local projects dir (metadata, not the plan) — that is out of scope for this item.

### E4. Episode 249 clips 2, 3, 4 carry their Mosaic run_ids

- **Verified at this head:** clips 2, 3, and 4 carry `mosaic_run_id` in BOTH the published plan (`src/ddma/docs/episodes/249/plan.json`: clip 2 `26606fbc-…`, clip 3 `972b1c19-…`, clip 4 `3ed55339-…`) and the local project plan (`ddma/projects/episode_249/plan.json`, same values), and all three are locked.
- **Verify:** Confirm the three run_ids are present in both plans, then report PASS. Do NOT fresh-run any published clip. Do NOT change code.

### E5. Settings template has the env-var mapping and placeholder paths

- **Verified at this head:** `settings.template.json` (1,837 bytes) has a `_comment` field mapping each key to its env var (`gemini_api_key` via `GEMINI_API_KEY`, `mosaic_api_key` via `MOSAIC_API_KEY`, `dd_hub_root` via `DD_HUB_ROOT`, `gdrive_pickup_path` via `GDRIVE_PICKUP_PATH`, `gdrive_video_pickup_path` via `GDRIVE_VIDEO_PICKUP_PATH`, `port` via `INGEST_PORT`, `external_editor` via `VISUAL` then `EDITOR`; the Mosaic IDs/prompt come from the file only), and the paths are placeholders (`C:/path/to/downloads`, `/path/to/dd_hub`, `/path/to/dd_hub/audio`, `/path/to/dd_hub/video`).
- **Verify:** Confirm the `_comment` mapping and the placeholder paths, then report PASS. Do NOT change code.

### E6. Trigger contract names the canonical renderer and a failure notification

- **Verified at this head:** `TRIGGER_CONTRACT.md:73` names `render_longform_parallel.py` as the canonical renderer (no "or"), and section 4 (:92–104) defines the failure-notification mechanism (`notify_failure` → server log + `dd_hub/logs/notifications.log`) with the wired W3 paths (mosaic-run, compile-clip, and export failures).
- **Verify:** Confirm the renderer line has no "or" and the failure-notification section exists with the wired paths, then report PASS. Do NOT change code.

## Global verify (run after all items)

1. Run the existing test suites and report the counts (`test_compile_scope.py`, `test_canonical_audio_compile.py`, `test_plan_clip0_title.py`, `test_mosaic_mux_integrity.py`, `test_curator.js` — do NOT run TEST 20 without first confirming its `finally` restore is intact; also `ingest/tests/cockpit_e2e.js` with its self-contained setup). Report PASS/FAIL per suite.
2. Start the Curator (`:8000`) and the cockpit (`:8088`) and confirm both load with no console errors.
3. Confirm the fan-out diff check (`scripts/check_fanout.py`) passes with the files in sync.
4. Do NOT publish any clip as part of this verify. Do NOT trigger a Mosaic run. Do NOT commit or push (fan-out is a separate human step).
5. Report PASS/FAIL per item (A1–A2, B1–B3, C1–C2, D1, E1–E6), then STOP with a full summary.
