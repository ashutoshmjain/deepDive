# Batch 3 — Round 4 hardening (Tier 4 UI + fix-up Items 3–6 + backlog + Issue 89)

## Scope and head

- Repo: deepDive, head `e16f21f4` (master). All line numbers below were verified at this head.
- **Repo layout note:** `ddma.py`, `run_curator.py`, `test_curator.js` now live under `ddma/` (top level), NOT `src/ddma/`. Use `ddma/ddma.py`, `ddma/scratch/run_curator.py`, `ddma/scratch/test-env/test_curator.js` in this spec. The canonical docs publication is `src/ddma/docs/episodes/`.
- This batch is 22 items, grouped by theme. Execute them in order. Report PASS/FAIL per verify step, then STOP with a full summary.

## Guardrails

- deepDive only. No Mosaic runs. No keys in git. No commit/push (fan-out is a separate human step).
- Do not refactor beyond what each item names. Do not touch the compile, the plan generation, the Mosaic modal, or any other dialog.
- If an item's fix is ambiguous, verify and report rather than guessing — do not invent a behaviour.

## Part A — Tier 4 UI fixes

### A1. Issue 12 — `@shutosha@bot` typo in server defaults

- **Where:** `ingest/server.py:139-140` (`tiktok_handle` and `instagram_handle` are both `"@shutosha@bot"`). The correct handle `"@shutoshabot"` is confirmed at `:648` (the actual TikTok/Instagram links). Note: `settings.template.json` already has the correct `"@shutoshabot"` — only the server.py defaults carry the typo.
- **Finding:** The default settings ship a misspelled social handle (an extra `@` in the middle).
- **Fix:** Change both `"@shutosha@bot"` values at `:139-140` to `"@shutoshabot"`.
- **Verify:** Grep server.py for `shutosha@bot` — zero matches. Grep for `shutoshabot` — the defaults now match the links at `:648`.

### A2. Issue 14 — `review_podcast_with_gemini` calls no Gemini

- **Where:** `ingest/server.py:1654` (function defined here; body `:1654–1876` has zero Gemini API calls — it is deterministic, per its docstring).
- **Finding:** The function name promises a Gemini call it never makes. The name is misleading.
- **Fix:** Rename the function so it no longer claims to call Gemini. Choose the new name from what the function actually does (per its docstring — a deterministic review step). Update every caller and every doc reference (including GEMINI.md) to the new name. Do NOT wire it to Gemini — that is a different feature, not this fix.
- **Verify:** Grep the repo for `review_podcast_with_gemini` — zero matches. The renamed function is called from the same places as before and the server starts.

### A3. Issue 16 — `kill_mdserve` is too broad

- **Where:** `ingest/server.py:112` (`pkill -f "mdbook serve"`); `kill_mdserve` is defined at `:90`.
- **Finding:** `pkill -f "mdbook serve"` matches any process whose command line contains that string — it can kill the wrong mdbook process (e.g., another project's server).
- **Fix:** Narrow the match to this project's mdbook serve process only (match the full command line including the project path and/or port, not just the bare `"mdbook serve"` string).
- **Verify:** Start this project's mdbook serve and a second dummy process whose command line contains `mdbook serve`; run `kill_mdserve`; confirm only this project's server is stopped and the dummy survives.

### A4. Issue 17 — Range parse crashes on bad input, no 416

- **Where:** `ingest/server.py:4099-4100` (bare `int()` Range parse; `bytes_range` is at `:4098`). There is no `416` anywhere in the file.
- **Finding:** A malformed `Range` header raises an uncaught exception (bare `int()` with no `try`) and the server never returns a proper `416 Range Not Satisfiable`.
- **Fix:** Wrap the Range parse in `try/except`; on invalid input return HTTP `416` (Range Not Satisfiable) with a valid `Content-Range` header.
- **Verify:** Send a request with a malformed `Range` header (e.g., `Range: bytes=abc-def`) — the server returns `416`, not a `500`/crash. Send a valid `Range` — it still returns `206` with the correct bytes.

### A5. Issue 18 — transcript save overwrites with no backup

- **Where:** `ingest/server.py:4776` (`/api/transcript/save` endpoint); the overwrite (`open(t_path, "w")`, no backup) is at `:4782`.
- **Finding:** Saving a transcript destroys the previous version with no backup — an accidental or bad save loses work.
- **Fix:** Before overwriting, write a backup copy of the existing transcript (e.g., `t_path + ".bak"`, or a timestamped backup alongside it). Then write the new content.
- **Verify:** Save a transcript twice with different content; confirm a backup file exists containing the first version, and the live file contains the second version.

### A6. Issue 19 — `do_HEAD` returns a full body

- **Where:** `ingest/server.py:3708-3709` (`do_HEAD` is defined at `:3708`; `return self.do_GET()` at `:3709`).
- **Finding:** A `HEAD` request returns the full response body, violating HTTP (HEAD must return headers only, no body).
- **Fix:** Implement `do_HEAD` to send the same headers as `do_GET` (including a correct `Content-Length`) but no body.
- **Verify:** Send a `HEAD` request — the response has the correct headers and an empty body. Send a `GET` to the same URL — the body is present and the `Content-Length` matches the HEAD response.

### A7. Issue 20 — cockpit loads the dead twentyuno script; widget missing there

- **Where:** `ingest/cockpit.html:22` (`<script src="https://embed.twentyuno.net/js/app.js"></script>`). That URL returns 0 bytes / is unreachable (the twentyuno embed is discontinued). The self-hosted `<lightning-widget>` is defined in `theme/book.js:860-1324` (`customElements.define('lightning-widget')` at `:1324`). `cockpit.html` has NO reference to `theme/book.js`.
- **Finding:** The cockpit loads a dead external script and never loads the file that actually defines the widget. So the wallet's yellow card renders on the live site (book.js defines it) but NOT in the cockpit (the widget element is undefined there — only the Tips text and audio pills show). Note: the live site has the widget tag but no script tag of its own — it renders only because book.js (loaded as `book-*.js`) defines the element.
- **Fix:** (1) Remove the dead twentyuno `<script>` tag from `cockpit.html:22`. (2) Load the self-hosted widget definition in the cockpit so the yellow card renders there — either load `theme/book.js` or extract the widget (book.js:860–1324) to a shared file and load that. Choose the approach that does not break the cockpit's own scripts.
- **Verify:** Open the cockpit preview for an episode — the yellow donation card renders (Ganesha image, "Thanks for supporting the publication", address pill, "Donate sats" button). Confirm the dead twentyuno script tag is gone from cockpit.html. Confirm the live site still renders the card.

### A8. Issue 30 — settings template has real machine paths

- **Where:** `settings.template.json` (repo root). It contains real machine paths (`downloads_path` = `C:/Users/ashut/Downloads`, `dd_hub_root` and gdrive paths = `G:/My Drive/dd_hub`). It has no `_comment` (0 matches). (This is the same file as Item 4 in Part B — fix both in one edit.)
- **Finding:** A template meant to be copied by other users ships the author's real machine paths.
- **Fix:** Replace the real machine paths with placeholders (e.g., `C:/path/to/downloads`, `/path/to/dd_hub`). Do NOT change the handles — they are already correct (`"@shutoshabot"`) in this file.
- **Verify:** Grep `settings.template.json` for `C:/Users/ashut` and `G:/My Drive` — zero matches. The file still parses as valid JSON.

### A9. Issue 36 — stale `ddma/docs/` mirror

- **Where:** `ddma/docs/` has NO `episodes/` directory (confirmed by tree listing). The canonical publication is `src/ddma/docs/episodes/`. `ddma/docs/` is not in the fan-out list.
- **Finding:** A stale docs mirror sits in the repo with no episodes — it is not the canonical publication and is not fanned out, so it drifts.
- **Fix:** Delete the stale `ddma/docs/` mirror. The canonical publication stays at `src/ddma/docs/episodes/`.
- **Verify:** `ddma/docs/` no longer exists in the repo. `src/ddma/docs/episodes/` is untouched. No code or doc references `ddma/docs/` (grep — zero matches, or update any that exist).

### A10. Issue 38 — clips incomplete vs plans (verify, do not render)

- **Where:** Episode 248 has 7 mp4s vs a 23-clip plan (7/23). Episode 249 has 14 mp4s (249-0–249-13) vs a 21-clip plan (14/21 — NOT 11/21; clips 249-11/12/13 were published since Round 4).
- **Finding:** The counts lag the plans. These are episodes in progress — the missing clips are unrendered, not lost. This is NOT a code bug to fix by rendering clips.
- **Fix:** Do NOT render missing clips. Verify the counts (248: 7/23, 249: 14/21) and confirm the missing clips are unrendered (no plan entry claims a file exists that is gone). Report the counts and, for each missing clip, whether it is "not yet rendered" or "plan says rendered but file missing" (the latter would be a real loss — report it as such).
- **Verify:** Report the two counts and the status of each missing clip. No clip files are created or deleted by this item.

### A11. Issue 40 — ingestion log lies on re-runs

- **Where:** `ddma/ddma.py:3283` — the line `"Transcription complete with word-level timestamps."` is logged unconditionally. The transcribe step runs only `if not os.path.exists(trans_path)`, but the log line sits OUTSIDE that guard, so it prints even when the cached `transcription.json` was reused.
- **Finding:** On a re-run that reuses the cached transcription, the log claims a fresh transcription completed — misleading.
- **Fix:** Move the "Transcription complete" log inside the guard so it only prints when a transcription actually ran; when the cached file is reused, log "Reused cached transcription" (or equivalent) instead.
- **Verify:** Run ingestion twice on the same episode. First run logs "Transcription complete". Second run logs the reuse message and does NOT log "Transcription complete".

### A12. Issue 34 (partial) — hardcoded deepDive paths break the standalone clone

- **Where:** `ddma/batch_archetype_pipeline.py:12` (`GITHUB_ROOT` is now script-relative — that half is fixed). The hardcoded deepDive layout remains at `:21`, `:25–27` (`"src","ddma","docs","episodes"`) and `:28–30` (`"ddma",...`), so the script still assumes the deepDive `src/ddma/...` layout and breaks a standalone ddma clone.
- **Finding:** The path construction still hardcodes the deepDive layout, so the script fails when ddma is checked out standalone.
- **Fix:** Make the path construction clone-agnostic (derive the docs/episodes path relative to the script's own location, not from a hardcoded `src/ddma` layout). The script must work both in the deepDive checkout and in a standalone ddma clone.
- **Verify:** Run the script (or its path-resolution function) from a deepDive checkout and from a standalone ddma clone — both resolve the correct episodes directory. Grep for the hardcoded `"src","ddma"` path segments — zero matches in the path construction.

## Part B — Fix-up Items 3–6 (Round 3 leftovers)

### B1. Item 3 — missing test/report notes for Round 2 items 33, 35, 32

- **Where:** `ddma/scratch/test-env/test_curator.js`. Item 10 ALREADY has a note (TEST 21 at `:1120`). Only Items 33, 35, 32 are missing notes.
- **Finding:** The Round 2 fixes for Items 33, 35, 32 have no test/report note in `test_curator.js`, so there is no regression coverage proving they work.
- **Fix:** Add a TEST block (or report note) for each of Items 33, 35, 32 in `test_curator.js`, following the existing TEST-block pattern (TEST 21 for Item 10 is the model). Do NOT re-add Item 10 — it is already covered.
- **Verify:** `test_curator.js` runs and the new TEST blocks pass. Grep for the Item 33/35/32 notes — all three are present.

### B2. Item 4 — settings template: no env-var mapping, real machine paths

- **Where:** `settings.template.json` (same file as A8 / Issue 30 — fix both in one edit). It has no `_comment` and still contains real machine paths.
- **Finding:** The template has no documented env-var mapping, so users cannot tell which settings come from the environment, and it ships real machine paths.
- **Fix:** (1) Add a `_comment` (or equivalent) mapping each setting to its env var, where one exists. (2) Replace the real machine paths with placeholders (same edit as A8 — do not do this twice; A8 and B2 are one change to one file).
- **Verify:** The file has a `_comment`/env-var mapping. Grep for `C:/Users/ashut` and `G:/My Drive` — zero matches. The file still parses as valid JSON. (A8's verify covers the paths; this item's verify covers the mapping.)

### B3. Item 5 — silent failures and bare excepts

- **Where:** `ddma/scratch/run_curator.py:93` (`safe_load_json` returns `None` on failure, no logging); `:113` (`load_settings` — it prints a `WARNING` when the vault is missing, so that path is NOT silent; only a `None`/corrupt result is silently coerced to `{}`); bare `except:` count in `run_curator.py` is exactly 9. `ddma/ddma.py:1885` (the `small.en` comment) and `:840` (the help text) still mention `small.en`.
- **Finding:** Failures are swallowed silently (a JSON load failure returns `None` with no log; a corrupt settings result becomes `{}` with no log), and 9 bare `except:` blocks hide errors. The `small.en` references are stale.
- **Fix:** (1) `safe_load_json` (`:93`): on failure, log the error (file + reason) and raise instead of returning `None`. (2) `load_settings` (`:113`): when the result is `None`/corrupt and is coerced to `{}`, log a warning/error (do not change the vault-missing `WARNING` — that one already logs). (3) Replace the 9 bare `except:` blocks in `run_curator.py` with explicit exception handling (log + raise, or log + a named fallback — do not swallow). (4) Remove/refresh the stale `small.en` comment at `ddma/ddma.py:1885` and the help text at `:840`.
- **Verify:** A corrupt JSON file passed to `safe_load_json` raises (with a log line) instead of returning `None`. A corrupt settings file logs a warning/error instead of silently becoming `{}`. Grep `run_curator.py` for bare `except:` — zero matches. Grep `ddma/ddma.py` for `small.en` — zero matches in the comment/help text.

### B4. Item 6 — TRIGGER_CONTRACT W4 "or" unresolved; no failure notification

- **Where:** `TRIGGER_CONTRACT.md:74` — W4 Canonical Renderer lists `combine_clips_demuxer.py` **or** `render_longform_parallel.py` (the "or" is unresolved). Failure notification is missing — there is only a telemetry log to `dd_hub/logs/<slug>.log` at `:91`.
- **Finding:** The contract does not name ONE canonical renderer for W4, and when a workflow fails there is no notification — only a log file the user must go read.
- **Fix:** (1) Resolve the W4 "or" to a single canonical renderer. Note the interaction with Part C's combine removal: if the combine feature is removed (Phase 5 decided NO clip combine), then W4's renderer is `render_longform_parallel.py` for longform, and the `combine_clips_demuxer.py` option is removed from the contract. Pick the resolution consistent with the combine decision in this batch. (2) Add a failure-notification mechanism for the four workflows (not just a telemetry log) — e.g., a notification on failure naming the workflow, the step, and the error. Keep the telemetry log; add the notification alongside it.
- **Verify:** `TRIGGER_CONTRACT.md:74` names ONE renderer (no "or"). Trigger a workflow failure (or simulate one) and confirm a notification is produced naming the workflow, step, and error. The telemetry log is still written.

## Part C — Other backlog

### C1. 249-0 local master (verify; the stale job is local-only)

- **Where:** The published master `249-0.mp4` exists at `src/ddma/docs/episodes/249/clips/249-0.mp4` on GitHub. There is NO `projects/` directory and NO `episode_249` anywhere in the repo tree — the stale job is local-only (on the workbench), not visible in the repo.
- **Finding:** The published 249-0 master is intact on GitHub. The "stale job" is a workbench-local issue, not a repo defect.
- **Fix:** Do NOT change the repo. Verify the published `249-0.mp4` on GitHub is intact (correct file, playable, correct duration). Then report: the published master is fine, and the stale local job is a workbench cleanup (clear it or restore from the published copy — that step is on the workbench, not in this repo change). Do not delete or re-upload the published master.
- **Verify:** Report the published 249-0's size/duration and confirm it plays. No repo files are changed by this item.

### C2. Dead combine code removal (endpoints are still wired — remove the feature)

- **Where:** `/combine-project-video` is still wired in `ddma/scratch/run_curator.py:3362` and invokes `scratch/combine_clips_demuxer.py` at `:3383–3386`. `/combine-project-audio` is wired at `:2841`. `ddma/ddma.py` has zero combine references. `render_longform_parallel.py` exists but is unreferenced by code (only `TRIGGER_CONTRACT.md:45` and `:74` mention it).
- **Finding:** The combine code is NOT fully dead — the demuxer endpoints are still wired. Phase 5 decided NO clip combine, so the feature should be removed, not just the unreferenced file. Removing only `render_longform_parallel.py` would leave the wired endpoints calling a demuxer that is also being removed.
- **Fix:** Remove the combine feature entirely: (1) remove the `/combine-project-video` and `/combine-project-audio` endpoints from `run_curator.py`; (2) remove `scratch/combine_clips_demuxer.py` and `render_longform_parallel.py`; (3) remove the combine references from `TRIGGER_CONTRACT.md` (`:45`, `:74` — consistent with B4's W4 resolution). Do NOT remove anything else.
- **Verify:** Grep the repo for `combine` (endpoints, scripts, contract) — zero matches in code and contract (docs may mention the removal). The server starts cleanly and the Curator/Beats pages load. No other endpoint is affected.

### C3. `.gitignore` cleanup (so "commit all" actually backs up source)

- **Where:** `.gitignore` (repo root). Current state: `ddma/scratch/` is ignored except 4 whitelisted entries (`run_curator.py`, `review_episode_bridges.py`, `combine_clips_demuxer.py`, `test-env/**`); `ddma/projects/` is ignored entirely; `ddma/docs/episodes/` is ignored but `src/ddma/docs/episodes/**` is explicitly tracked; `settings.json` and global audio (`*.mp3`/`*.m4a`/…) are ignored.
- **Finding:** The standing rule is "commit all" (GitHub mirrors local exactly, except large media files and intermediate manim-production artifacts). The current `.gitignore` hides source files — `ddma/projects/` and non-whitelisted scratch files are missed by `git add -A`, so "commit all" does not actually back everything up.
- **Fix:** Update `.gitignore` so source files are tracked: un-ignore `ddma/projects/` (plan.jsons and source) and the non-whitelisted `ddma/scratch/` source files. Keep ignoring only large media files and intermediate manim-production artifacts (and `settings.json` / secrets — those stay ignored). Note: if C2 removes `combine_clips_demuxer.py`, remove it from the whitelist at the same time (it will no longer exist).
- **Verify:** Run `git add -A --dry-run` (or `git status`) and confirm the previously-hidden source files (`ddma/projects/`, scratch test files) are now staged/tracked, while large media/intermediates and `settings.json` remain ignored. No secrets are staged.

### C4. Clip-0-visuals question (open question — verify and report)

- **Where:** No clip-0-visuals note exists in the repo docs (GEMINI.md, TRIGGER_CONTRACT.md) or code. This is an open question with no code location.
- **Finding:** There is an open question about clip 0's visuals, but it is not recorded as a code defect anywhere.
- **Fix:** Do NOT invent a fix. Determine what clip 0's visuals currently are (from the plan/episode — clip 0 carries the episode title) and report: what the visuals are, and what the open question is (e.g., should clip 0 have visuals, or is the title card sufficient?). Present the finding so the user can decide.
- **Verify:** Report the current clip-0 visuals and the precise open question. No code is changed by this item.

### C5. Beats Studio UI pattern (lowest priority — align with Curator)

- **Where:** `ddma/beats.html` (622 lines) and `ddma/beats_server.py` (391 lines). The UI pattern lives in `beats.html` (Beats Studio page: archetype badge, beat inspection), served by `beats_server.py`.
- **Finding:** Beats Studio's UI does not follow the Curator UI pattern. This is the lowest-priority item in the batch.
- **Fix:** Review `beats.html` against the Curator page's UI pattern and align the shared elements (layout, controls, styling) so the two pages present consistently. Keep the Beats-specific content (archetype badge, beat inspection) — only align the shared pattern, do not redesign Beats Studio.
- **Verify:** Open Beats Studio and the Curator side by side — the shared UI elements (header, controls, layout) match the Curator pattern. Beats-specific content is intact and functional.

## Part D — Issue 89 (the "?" in the Lightning widget)

### D1. Issue 89 — literal "?" where "⚡" belongs

- **Where:** `theme/book.js:1015` (`<div class="addr-pill">? ${this.to}</div>`) and `:946` (`label: '? ' + formatAmount(n)`). This is the SELF-HOSTED `<lightning-widget>` (defined in `theme/book.js:860–1324`, commit 2026-11-06) — NOT the twentyuno widget. Do not call it the twentyuno widget.
- **Finding:** The widget hardcodes a literal "?" where the lightning-bolt symbol belongs. The live card reads "? shutosha@primal.net" and the amount buttons read "? 100", "? 1,000", "? 10,000". This is NOT Issue 12 (the `@shutosha@bot` social-handle typo) — the widget never uses those handles; it uses `lightning_address` (`shutosha@primal.net`).
- **Fix:** Replace the literal `"?"` with `"⚡"` at both lines (`:1015` and `:946`).
- **Verify:** Open the live site (or rebuild and open the episode page) — the card reads "⚡ shutosha@primal.net" and the amount buttons read "⚡ 100", "⚡ 1,000", "⚡ 10,000". No other "?" remains in the widget's rendered output.

## Global verify (run after all items)

1. Run the existing test suites and report the counts (`test_compile_scope.py`, `test_canonical_audio_compile.py`, `test_plan_clip0_title.py`, `test_mosaic_mux_integrity.py`, `test_curator.js` — do NOT run TEST 20 without first confirming its `finally` restore at `test_curator.js:1108` is intact). Report PASS/FAIL per suite.
2. Start the Curator (`:8000`) and the cockpit (`:8088`) and confirm both load with no console errors and no missing-widget errors.
3. Confirm the cockpit preview renders the yellow donation card (A7) and the live site still renders it (D1).
4. Do NOT publish any clip as part of this verify. Do NOT trigger a Mosaic run. Do NOT commit or push (fan-out is a separate human step).
5. Report PASS/FAIL per item (A1–A12, B1–B4, C1–C5, D1), then STOP with a full summary.

## Outcome (executed 2026-11-16/17, head 028aa331, uncommitted)

Per-item result. Verifies marked [live] were executed; [static] by read/grep; [suite] by repo suites.

- A1 PASS [static]. A2 PASS [static+server-up]. A3 PASS [live: dummy pid 36924 with `mdbook serve` in cmdline survived `kill_mdserve()`].
- A4 PASS [live: bad Range -> 416 + `Content-Range: bytes */size`; `bytes=0-99` -> 206 + correct Content-Range].
- A5 PASS [live: two fixture POSTs -> live=v2, `.bak`=v1; fixture + two zero-byte root strays from first curl attempts removed].
- A6 PASS-after-fix [live]. The prior discard-wrapper dropped headers too (HEAD returned nothing). Fixed `_DiscardBody` (first write passes, rest dropped). HEAD -> 200 + matching Content-Length, empty body; HEAD+range -> 206.
- A7 PASS [browser: twentyuno gone, widget defined, 2 tags render, addr-pill present, zero page errors].
- A8/B2 PASS [static: valid JSON, env map, zero real paths].
- A9 NO-CHANGE, premise false: `ddma/docs/` has zero TRACKED episodes but is a live tracked docs site (player.js/index.html served at /docs/, covered by TEST 18). Not deleted.
- A10 PASS [verify-only]: 248: 7/23 (missing 8-23 unrendered). 249: 15/21 as executed (0-14 present; missing 15-20 unrendered). No loss.
- A11 CODE-PASS, live double-ingest DEFERRED (would re-run Gemini plan-gen twice = API spend). Log inside guard + else-branch reuse message verified by region read.
- A12 PASS [live probes]: hub-first resolves on workbench; fake-root probes prove deepDive-shape -> `src/ddma/docs/episodes/` and standalone-shape -> `docs/episodes/` both resolve with plan present. Full pipeline NOT run (Gemini spend).
- B1 PASS [suite]: TEST 22/23/24 added, standalone probe 3/3, full suite green.
- B3 PASS [live probes + greps]: corrupt JSON -> ERROR + RuntimeError; corrupt settings -> ERROR + {}; zero bare `except:`; zero `small.en`.
- B4 MECHANISM-PASS, endpoint-trigger PENDING USER RESTART: contract W4 = `render_longform_parallel.py` alone + section 4 notification spec; `notify_failure()` + 3 W3 wirings in code; live direct call wrote the NOTIFY line to stdout AND `dd_hub/logs/notifications.log`. :8000 was a stale pre-batch server (pid 13932, not restarted by agent); restart it, then re-POST `/compile-clip?id=episode_249&num=999` to see the trigger fire. `watcher.py` does not exist in tree (telemetry future).
- C1 PASS [ffprobe]: 249-0 = 12.5 MB, h264 1080x1920 + aac, 149.85 s. No repo change.
- C2 PASS with 2 deviations: (1) KEPT `render_longform_parallel.py` (beats_server.py:314 uses it; it is the Beats engine, not combine). (2) Removed dead combine UI + TEST 17 + docs-player export button/handler (they 500'd after endpoint removal); TEST 15/18 assert absence as removal guards. Grep `combine` (case-sensitive): zero in code + contract. Also renamed bare `combined` vars (substring hit) in the two clip-test files + `archetype_studio.py`.
- C3 PASS [dry-run]: projects plans/transcripts/meta + scratch sources stage; no settings.json/audio/pycache/bak. Two fixes while verifying: anchored root `scratch/` -> `/scratch/` (was swallowing `ddma/scratch/`), removed dead demuxer whitelist line.
- C4 REPORTED, no change: clip 0 (249) = intro card + Mosaic body + outro bridge, title "What Exactly Is Reality?". Open: full clip vs pure title card? User decides.
- C5 PASS [browser]: beats header rebuilt on curator `.app-topbar` pattern; studio intact; no errors.
- D1 NAMED-LINES PASS [browser: addr-pill `⚡ shutosha@primal.net`, pills `⚡ 100 | ⚡ 1k | ⚡ 10k`; live site loads `book-0c7842ec.js`, picks up fix on next mdbook build]. 4 residual literal `?` NOT fixed (need user glyph call): back button `>?</button>`, `Done ?`, `? Thank you!`, `Copied! ?` (both files).
- Global: compile_scope 3/3, canonical_audio 2/2, clip0_title 2/2, mux_integrity 2/2, test_curator.js 100% PASS (TEST 15/18/20/21/22/23/24 all green). Suite ran against stale :8000 for serving; DOM/file asserts fully valid, behavioral paths unchanged by this batch (verified separately). No publish, no Mosaic spend, no commit/push.
- Fan-out note: `ingest/lightning-widget.js` (new) + `scratch/test-env/test_compile_scope.py` must be added to the GEMINI.md Step-1 mirror list with this round (done in the fan-out commit).
