# One-shot fixer batch — 11 items (head `390e0a1a`)

Fix these 11 items in deepDive only (workbench: `deepDive/ddma/`, test on `localhost:8000`). Work through them IN ORDER, one at a time, in a single run. Each item is self-contained — its own Where / Finding / Fix / Verify — and each was verified against head `390e0a1a`.

**How to run this batch:** fix ITEM 1, report PASS / FAIL for it with file:line evidence, then CONTINUE to ITEM 2. Do the same for each item in turn. Do NOT stop after any single item — "Report and STOP" inside an item means report that item and move on. Only STOP after ITEM 11 is reported.

**Guardrails for the whole batch:**
- Fix only the items below. One fix at a time, no refactors of working code, no batch rewrites.
- Do NOT trigger any Mosaic run. Do NOT spend any Mosaic API cost.
- No keys in git. `git diff` must show only the intended files.
- Do not commit or push. Stage nothing. The user commits. Fan-out to standalone ddma / mdIngest is a separate, human-initiated step after this lands.
- Report PASS / FAIL per item with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.
- At the very end, give a one-line summary per item (PASS / FAIL) and STOP.

---

## ITEM 1 of 11 — TEST 20 poisoned the live Mosaic prompt

# Fixer prompt — Issue 65: TEST 20 poisoned the live Mosaic prompt (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ddma/`, test on `localhost:8000`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

The Curator's Mosaic prompt — the motion-design instructions that get Mosaic to produce the right flow and pace — was overwritten by a test. The Mosaic Prompt Editor now shows `Test Prompt Persistence 1794368449602` as the base rules instead of the real prompt. The user has no backup. "Reset to Default" in Settings restores the same test string.

## Item 1 — TEST 20 must restore the prompt it overwrites

**Where:** `ddma/scratch/test-env/test_curator.js`, TEST 20 ("Issue 64 — Curator Settings Save & Persist Invariant"), around line 985. The live server is `ddma/scratch/run_curator.py`; the live page is `ddma/curator.html`.

**Finding:** TEST 20 writes `` `Test Prompt Persistence ${Date.now()}` `` into `#settingsMosaicDefaultPrompt`, clicks `#saveSettingsBtn`, reloads the page, and asserts the value persisted — and never restores the original value. The test runs against the LIVE Curator at `http://127.0.0.1:8000/curator.html`, not an isolated instance. The Save handler (`curator.html:3233-3243`) writes `localStorage['ddma-mosaic-default-prompt']` and calls `saveSettingsToServer()` (`:2426`), which POSTs `mosaic_default_prompt` to `/save-settings`; that handler (`run_curator.py:2187`) overwrites `settings.json` wholesale. So the marker value landed in BOTH stores — browser localStorage and `settings.json` on disk — and every later page load re-copies it (initApp, `curator.html:2518`). Timestamp `1794368449602` is the 2026-11-10 fix-up test run.

**Fix:** in TEST 20, capture the original prompt value BEFORE overwriting (read `#settingsMosaicDefaultPrompt` after opening Settings), and restore it in a `finally` block via the same UI path the test already uses: set the textarea back to the original value, click Save, reload, and assert the reloaded value equals the original. The test must pass AND leave the settings exactly as it found them. Do not leave any marker value behind under any outcome — including a test failure mid-way, which is what `finally` is for.

**Verify:** run the full `test_curator.js` suite against the live Curator; after it finishes, open Settings and confirm the Mosaic Default Prompt is the value it held before the run (NOT a `Test Prompt Persistence` string); confirm `settings.json` on disk holds the same value. Also verify the failure path: temporarily force TEST 20's persist assertion to fail and confirm the original value is still restored.

## Item 2 — Reset to Default must return the shipped fallback, not the stored value

**Where:** `ddma/scratch/run_curator.py` `/get-settings` handler (around line 5362) and `ddma/curator.html` Reset handler (around line 3218).

**Finding:** `/get-settings` computes `def_mosaic = get_mosaic_default_prompt()` and returns it as `default_mosaic_prompt`. But `get_mosaic_default_prompt()` reads `settings.json`'s `mosaic_default_prompt` FIRST and returns it when present — so the "default" is whatever is currently stored, poisoned or not. Reset fetches `/get-settings` and takes `d.default_mosaic_prompt`, so after any poisoning Reset is a no-op loop that restores the poison. That is why Reset did not help here.

**Fix:** in `/get-settings`, expose the shipped hardcoded fallback as a separate field (e.g. `factory_mosaic_prompt`) — the literal fallback string already returned by `get_mosaic_default_prompt()` when no stored value exists. Do NOT change what `get_mosaic_default_prompt()` or `default_mosaic_prompt` return (the stored value is a legitimate user customization and the export flow depends on it). Change only the Reset handler to use the new factory field. Reset then always restores the shipped default, regardless of what is stored.

**Verify:** with a poisoned stored value in place, click Reset to Default → the textarea shows the shipped fallback text (starting `MOTION DESIGN INSTRUCTIONS (YOUTUBE SHORTS - around 150 to 180 seconds long)`); Save → reload → the Mosaic Prompt Editor for a clip shows the fallback as its base rules. Normal stored-value behaviour unchanged: a custom stored prompt still flows into the editor when Reset is not clicked.

## Item 3 — Keep a tracked backup of the shipped default prompt (linked from GEMINI.md)

**Where:** new file `deepDive/.agents/rules/default-prompts.md` (tracked), plus one line in `deepDive/GEMINI.md` under "## Detail guides (`.agents/rules/` — `trigger: model_decision`, read on demand)" (around line 91), alongside the existing `clip-dynamics.md` / `clip-stitching-acoustics.md` / `distribution-strategy.md` / `visual-standards.md` entries.

**Finding (user's call, 2026-11-11):** the gold prompt survives in exactly one place — the hardcoded fallback inside `get_mosaic_default_prompt()`. The stored copy in gitignored `settings.json` had no backup anywhere, which is why this incident was a near-loss. GEMINI.md itself is a slim always-on core (11,875 bytes, must stay under 24,000 or Antigravity truncates it) and carries no prompt text — the deep specs live in linked `.agents/rules/` files read on demand. That is the right shape for critical default prompts too: a linked file, not inline text.

**Fix:** create `.agents/rules/default-prompts.md` (frontmatter `trigger: model_decision`, same as the other guides) holding the canonical default prompt texts verbatim — the Mosaic motion-design prompt (the hardcoded fallback text, quoted below) and, for completeness, the three Gemini defaults (`get_gemini_default_prompt`, `get_gemini_episode_default_prompt`, and the bridge prompt as documented in Issue 55 — note the bridge prompt is dead, so record it as historical, not live). Add one line to GEMINI.md's Detail guides list pointing at it (e.g. `default-prompts.md` — canonical default prompt texts: Mosaic motion design + Gemini remix/episode prompts). Keep GEMINI.md under 24,000 bytes. Do NOT change how the server reads settings — the code fallback stays the runtime source; this file is the tracked, reviewable backup. Secondarily, check whether `settings.template.json` already carries the mosaic default; if it does not, add it there too.

**Verify:** the new file exists and is tracked; its Mosaic prompt value equals the hardcoded fallback string character-for-character; GEMINI.md lists it and is still under 24,000 bytes; the Mosaic editor still builds from the code fallback unchanged.

## The gold prompt text (for reference — this is the shipped fallback, byte-identical at head `c4f7d68f` and at `6037166d`)

```
MOTION DESIGN INSTRUCTIONS (YOUTUBE SHORTS - around 150 to 180 seconds long)

- Cover the entire timeline of the video with Dan Koe-style motion graphics. Visual coverage must be active and persistent from 0:00 to the very last second with ZERO blank frames.

- Maintain uniform graphic density across all segments.

- Plan 10 to 12 continuous segments of roughly ~ 15 seconds each, perfectly mapped to the clip length. Each segment renders a dynamic diagrammatic graphic with changing visual steps and text reveals.

- Assume background video is a blank black glossy screen (#000000). Keep persistent visuals (animations, conceptual geometry, or text) throughout. Segments must hand off to each other seamlessly like a relay race.

--------------------------------------------------
PACING & ANIMATION RULES
--------------------------------------------------
- No static holds beyond 6 seconds. Introduce visual changes or step reveals every 2-4 seconds.
- Use only basic transforms: opacity, position, scale. Keep animations single-property per element.
- Prefer step-based reveals over continuous complex motion. Avoid preset/template animations.
- No gaps in infographic coverage. Zero external asset dependencies.
```

## Guardrails

- Fix only the three items above. Do not rebuild earlier features.
- Every fix must expand `test_curator.js` to assert that exact behaviour BEFORE declaring success (Item 1's restore assertion IS the test expansion; Item 2 needs its own assertion — poison the stored value, click Reset, assert the factory text).
- Do not run the suite against the live Curator's real settings without the restore in place — that is the bug being fixed.
- Report PASS / FAIL per item with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.
- Do not commit or push. Stage nothing. The user commits.

---

## ITEM 2 of 11 — Settings silently discard unsaved changes

# Fixer prompt — Issue 66: Settings silently discards the Mosaic prompt (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ddma/`, test on `localhost:8000`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

Right after the Issue 65 restore, the user pasted the gold Mosaic prompt into Settings, closed the dialog, reopened Settings — and the box was back to the one-line test string. The save path is NOT missing: all six fields the handler reads exist in the markup, and the handler writes localStorage and POSTs to `/save-settings`. The loss is silent, through two paths below. Which close button the user used cannot be determined from the repo — fix both paths.

## Item 1 — Closing Settings with unsaved changes must ask, never silently discard

**Where:** `ddma/curator.html` — settings modal open/close: `openSettingsModal` (around line 3172), ✖ close (around line 3191), Cancel button (around line 1893, inline onclick), Save handler (around line 3233).

**Finding:** the ✖ button and the Cancel button close the modal WITHOUT saving and WITHOUT any warning — there is no dirty check and no "unsaved changes" signal anywhere in the file. The only path that saves is the gradient Save Settings button. Closing the dialog any other way discards the edit, and nothing tells the user. (Ruled out as causes: no missing element — all six field IDs exist in the markup, so the handler cannot throw on a null read; no duplicate textarea; tab switching only toggles display.)

**Fix:** snapshot the settings field values when the modal opens (the six fields the Save handler reads: Mosaic API key, Agent ID, MOGR Node ID, Captions Node ID, Gemini API key, Mosaic Default Prompt). On ✖ / Cancel / backdrop close, if any field differs from the snapshot, show a confirm dialog: "You have unsaved settings. Save them?" with three choices — Save (run the normal save path, then close), Discard (close without saving), Cancel/Stay (keep the modal open). If nothing changed, close immediately as today. Keep the existing Save Settings button behaviour, only with the Item 2 verification added. Also fix the layout that caused this exact miss: the Save/Cancel buttons currently render dangling outside the visible dialog area — keep them visibly inside the dialog footer (no overflow/positioning that pushes them outside the modal box).

**Verify:** open Settings, edit the Mosaic Default Prompt, click ✖ → confirm appears; choose Discard → reopen Settings, the stored value is unchanged. Repeat, choose Save → reopen Settings, the new value is there. Repeat with no edits → ✖ closes immediately, no confirm. Puppeteer: assert all three branches in `test_curator.js`.

## Item 2 — Save must verify the server round-trip; no more false "saved successfully"

**Where:** `ddma/curator.html` `saveSettingsToServer()` (around line 2426) and the Save handler (around line 3233); server side `ddma/scratch/run_curator.py` `/save-settings` (around line 2187) and `/get-settings` (around line 5362).

**Finding:** `saveSettingsToServer()` swallows server failures — its `.catch` only `console.warn`s — and the handler shows "Settings saved successfully!" regardless of whether the POST worked. If the POST fails and the page is later reloaded, initApp (`curator.html:2518`) re-syncs localStorage from `settings.json`, which still holds the old (poisoned) value, and the paste is gone with no trace. The user cannot tell a failed save from a successful one.

**Fix:** make `saveSettingsToServer()` return its fetch promise and reject on a non-OK response or a network error (no silent swallow). In the Save handler, await it, then re-fetch `/get-settings` and confirm the stored `mosaic_default_prompt` equals the value just saved. Only then show "Settings saved successfully!" and close the modal. On any failure (POST rejects, or the round-trip value mismatches), show an error toast naming the failure, keep the modal open, and do NOT show the success message. Do not change the `/save-settings` or `/get-settings` server behaviour.

**Verify:** save a marker prompt value → reload the page → open Settings → the marker is there AND `/get-settings` returns it as `mosaic_default_prompt` (assert the server value, not just the textarea — the existing TEST 20 only asserts the textarea). Failure path: intercept the `/save-settings` request in Puppeteer (route it to a 500 / abort it) → click Save → an error is shown, the modal stays open, no success toast. Puppeteer: assert both in `test_curator.js`.

## Guardrails

- Fix only the two items above. Do not rebuild earlier features. Do not change the save path's restore behaviour: any test that overwrites the Mosaic prompt must restore the original value in a finally block. If you edit `test_curator.js`, keep the existing TEST 20 restore assertion passing.
- Every fix must expand `test_curator.js` to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do not run the suite against the live Curator's real settings without the Issue 65 restore in place — that is the bug being fixed next door.
- Report PASS / FAIL per item with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.
- Do not commit or push. Stage nothing. The user commits.

---

## ITEM 3 of 11 — Abrupt Intro Card → Mosaic body transition

# Fixer prompt — Issue 67: abrupt Intro Card → Mosaic body transition (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ddma/`, test on `localhost:8000`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what the user reported, so you don't re-diagnose it)

While smoke-testing clip 249-8, the user found the transition from the Intro Card (1.5s title card, soft title-card chime) to the main Mosaic body video abrupt: the chime ends and the punchline hook starts at full volume on the very next sample, with a simultaneous hard visual cut from the static card to kinetic Mosaic graphics. He wants a short silence while the title card still persists but audio stops. (Correction from the user, 2026-11-11: his first suggestion of 10–20ms is NOT sacrosanct — he suggested it without knowing the frame constraint. Use the established 0.2s beat instead; do not implement 10–20ms.)

## Finding (verified in spec + code — this is specified behaviour, not a compile bug)

- The spec says hard concat: `.agents/rules/clip-stitching-acoustics.md:48-49` — Stage 3 is "[Intro Card (1.5s, Pure #000000, dedicated soft title-card audio)] -> Hard concat into [Mosaic/Manim Body Video]". No gap, no fade at this boundary anywhere in `GEMINI.md` or the four `.agents/rules/` files.
- The silence rule covers stings only: `silence_before: 0.2s` is specified for the Mid-Sting and Outro-Sting (`clip-dynamics.md:14-15`; `clip-stitching-acoustics.md:20,33,87-88`) and between speech segments and stings in Stage 1. Nothing specifies a gap before the first speech (the punchline hook) or at the intro→body boundary.
- The code implements the spec exactly: `compile_clip` (`ddma/ddma.py:2909`, `build_concat_cmd`) joins intro→body with a hard video concat (`[v0][v1]concat=n=2:v=1:a=0`) and a hard audio concat (`[0:a][1:a]concat=n=2:v=0:a=1`) — no silence, no fade. Contrast the outro boundary in the same command, which gets a 1.0s `xfade` + `acrossfade`. The intro chime does fade out over its last 0.2s (`afade=t=out:st={intro_duration - 0.2}:d=0.2` — st=1.3, around line 2720), but the body audio starts at full volume immediately: the body assembly starts `t_cursor = 0.0` (around line 1361) and the first audio segment is placed at 0 with no `silence_before` — the 0.2 default applies to music segments only (`ddma.py:1413`, in the `elif seg_type == "music"` branch; same in `scratch/run_curator.py:1007`, `compile_segments_helper`). `intro_duration = 1.5` (around line 2712).

## Fix

Introduce one constant, e.g. `INTRO_BODY_GAP_S = 0.2` (0.2s — the established sting beat, per the user's correction; do NOT use 10–20ms), and apply it at the intro→body splice in `build_concat_cmd`:

1. **Audio:** insert 0.2s of digital silence into the audio at the splice — pad the intro audio's tail with silence (e.g. an `anullsrc` silence segment in the audio concat, making it a 3-input concat), so the chime ends, 0.2s of silence follows, then the body audio starts.
2. **Video:** hold the title card for the same 0.2s — extend the intro video's duration by the gap, so the card is still on screen while the audio is silent.
3. **Keep A/V in sync:** pad the INTRO side (video + audio tail). Do NOT delay the body audio alone — that would drift everything after the splice by the gap.
4. **Captions:** caption chunks are offset by `intro_offset=intro_duration` — account for the gap there so captions don't land early. If `intro_duration` grows by the gap, the existing offset must follow the same variable; verify rather than assume.
5. **Spec update (the "adjust GEMINI.md" part):** update `.agents/rules/clip-stitching-acoustics.md` Stage 3, which currently says "Hard concat" from Intro Card into Mosaic/Manim Body Video — change it to specify the 0.2s silence gap at the intro→body join, so the rule lives in the spec, not just in code. Do NOT edit the slim `GEMINI.md` core itself (it must stay under 24,000 bytes; it already links that rules file under Detail guides).
6. **Do not touch** the outro boundary (1.0s xfade/acrossfade stays), the sting gaps (0.2s stays), or the intro chime's own 0.2s fade-out.

**Why 0.2s:** it is the existing beat everywhere else (sting `silence_before`), and it is cleanly renderable — 5 frames at the concat's forced `fps=25` — so there is no sub-frame quantization problem (the 10–20ms first suggestion would have been sub-frame at 40ms/frame, which is why the user corrected it).

## Verify

- Recompile clip 249-8 after the fix (its Mosaic render was already started before this fix — the gap applies at compile time, so a recompile is required to hear it).
- Measure the splice in the compiled mp4: the first ~0.2s after t=1.5s are digital silence (check with ffmpeg `astats`/`volumedetect` on that window), the hook starts clean with no pop/click, and the title card is still the visible frame during the gap.
- Captions still land on time (spot-check the first caption event against the hook start).
- Outro transition unchanged (still the 1.0s fade), sting gaps unchanged (0.2s).
- Report PASS / FAIL with the measured silence window and the A/B listen result. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Touch only the files and lines named in this prompt. Do not rebuild earlier features.
- Report PASS / FAIL with file:line evidence and the exact commands run.
- Do not commit or push. Stage nothing. The user commits.

---

## ITEM 4 of 11 — /export-to-mosaic reads the local plan directly

# Fixer prompt — /export-to-mosaic reads the local plan directly (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ddma/`, test on `localhost:8000`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

The plan is hub-first: the canonical plan lives in the workspace (dd_hub), and `load_plan()` reads it (with a revision check and a loud warning if the hub is unreachable). The per-clip Publish endpoint already uses `load_plan()`. The Mosaic export handler does not — it reads the local plan file directly. A stale local copy could trigger a fresh PAID Mosaic run against the wrong clip data.

## 1 — Where

**Where:** `ddma/scratch/run_curator.py` — the `/export-to-mosaic` handler (around line 3701); the plan read at lines 3741-3745; `load_plan()` at line 208.

**Finding:** the handler reads the plan straight off local disk:

```python
plan_path = os.path.join(project_dir, "plan.json")
if not os.path.exists(plan_path):
    raise Exception(f"plan.json for project {project_id} not found.")

with open(plan_path, "r", encoding="utf-8") as f:
    plan = json.load(f)
```

It never calls `load_plan(project_id, writer="curator")`, which is the hub-first reader (revision-checked, loud warning on hub-unreachable, local-cache fallback). The local `plan.json` can be stale — the hub copy is the primary store, and the local copy is only a cache that is re-synced on read. If the local copy is behind (e.g. a clip's title, segments, or prompt changed on the hub after the last local sync), the export builds its Mosaic prompt from the stale data and spends a real Mosaic run on it. Contrast the `/publish-clip` endpoint in the same file (around line 4122), which verifies the lock against `load_plan()` at line 4131.

## 2 — Fix

Route the `/export-to-mosaic` handler through `load_plan()`:

1. Replace the local `plan_path` open (lines 3741-3745) with `plan = load_plan(project_id, writer="curator")`. Keep the rest of the handler unchanged — the clip lookup, the prompt building, the Mosaic run call, the job-state handling.
2. Do NOT change lock semantics, the Mosaic flow, or hub-first routing. Do NOT trigger any Mosaic run while fixing or testing this.
3. If `load_plan()` raises (hub unreachable and no usable cache), let that error surface as the handler's error — do not fall back to reading the local file directly, because that is exactly the stale-copy path being removed.

## 3 — Verify

- With a deliberately stale local plan (edit the local `plan.json` for a fixture episode so a clip's title differs from the hub plan, or remove a clip's `mosaic_run_id` locally while the hub still has it), call `/export-to-mosaic` with the Mosaic call intercepted/stubbed so no real run is spent, and confirm the prompt/run uses the hub plan's data, not the stale local copy.
- Add/extend a test asserting the handler reads via `load_plan()` (e.g. in `test_curator.js`: a test that makes the local plan differ from the hub plan, calls the export endpoint with the Mosaic call stubbed, and asserts the data used matches the hub plan). The test must NOT spend a Mosaic run.
- Confirm the normal export path still works end-to-end (prompt, lock check, job state) with the hub plan in place.
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not change the save path's restore behaviour: any test that overwrites the Mosaic prompt must restore the original value in a finally block.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report PASS / FAIL for this item with file:line evidence, then continue to the next ITEM.

---

## ITEM 5 of 11 — No way back to the workspace from the apps

# Fixer prompt — no way back to the workspace from the apps (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/`, test on `localhost:8088` and `localhost:8000`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

The landing page (served on port 8088) is the workspace home: it holds the workspace definition, the launcher for mdIngest + ddma (+ Beats Studio), and the single drop point for input assets. Once you click into the cockpit, the curator, or Beats Studio, there is no way back to that home page except the browser Back button. The three apps each have a different broken or missing path home.

## 1 — Where

**Where:**
- `ingest/cockpit.html` lines 1782 and 1845 — the cockpit's only way back is two small text links reading "Drop new inputs on the home page →" (both `href="/"`). There is no home link in the cockpit header.
- `ddma/beats.html` line 21 — the Beats Studio header has `<a href="/">landing</a>`. The Beats Studio server runs on port 8001, so `href="/"` resolves to the 8001 home, not the landing page — it reloads episode 248 instead of going home.
- `ddma/curator.html` line 1767 — the curator's "📂 Workspace Root" button is a workspace-selector control, not a link back to the landing page.
- `ingest/landing.html` — the landing page itself, served on port 8088 (home route serves `/landing.html`).

**Finding:** once in the cockpit there is no way back to the workspace except the browser Back button. Beats Studio's "Landing" link reloads episode 248 (its `href="/"` resolves to the 8001 home). The curator's "Workspace Root" is a selector, not a link back. A plain link would navigate the current tab away from the app; `target="_blank"` would open a new tab every time. The right shape is a NAMED target, which reuses the already-open workspace tab.

## 2 — Fix

Add a "Workspace" home link on every app, pointing at the landing page on port 8088 (`http://127.0.0.1:8088/`), using a NAMED target so it reuses the already-open workspace tab:

1. **Cockpit header** (`ingest/cockpit.html`): add a visible "Workspace" link in the header (same pattern as the existing header buttons), `href="http://127.0.0.1:8088/"` with `target="deepdive-workspace"` (or the equivalent `window.open(url, "deepdive-workspace")` call). Keep the two existing small "Drop new inputs on the home page →" links as secondary links — they are fine, the header link is the primary way back.
2. **Curator header** (`ddma/curator.html`): add the same "Workspace" link in the header, same href and same named target. Do not repurpose the "📂 Workspace Root" selector (line 1767) — leave it as it is.
3. **Beats Studio header** (`ddma/beats.html` line 21): change the "landing" link so it points at `http://127.0.0.1:8088/` with `target="deepdive-workspace"` instead of `href="/"`. It must go to the 8088 landing page, not the 8001 home.
4. The named target must be the same string on all three apps (`deepdive-workspace`), so clicking it from any app reuses the one already-open workspace tab instead of opening a new tab each time or navigating the current tab away.

## 3 — Verify

- From the cockpit, click the Workspace link → the landing page opens in the already-open workspace tab (not a new tab, and the cockpit tab stays on the cockpit).
- From Beats Studio, click the Landing link → it lands on the 8088 landing page (not the 8001 home, not episode 248).
- From the curator, click the Workspace link → it lands on the 8088 landing page.
- Add/extend a test asserting the link on each page (e.g. a Puppeteer/static check that the header link on the cockpit, curator, and Beats Studio has `href="http://127.0.0.1:8088/"` and `target="deepdive-workspace"`).
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not change the landing page itself, the launcher buttons, or the drop endpoint.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report PASS / FAIL for this item with file:line evidence, then continue to the next ITEM.

---

## ITEM 6 of 11 — DDMA launch hangs on its own re-transcription

# Fixer prompt — DDMA launch hangs on its own re-transcription (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ingest/`, test on `localhost:8088`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

Launching DDMA from the landing page sticks on "Launching DDMA…" while a full large-v3-turbo transcription runs in the request handler. The One-transcription rule is: ONE transcription, done at the podcast stage — the clips (ddma) use the same base transcription, never re-transcribe. The launch handler's own comment says "zero re-transcription", but the code does not enforce it: when the seed cannot find acoustic segments with words, it transcribes the whole episode itself, synchronously, inside the HTTP request.

## 1 — Where

**Where:** `ingest/server.py` — the `/api/ddma/launch` handler (around line 4936; it calls `seed_ddma_project_if_missing(clean_id)` at line 4950, in the request path, synchronously); `seed_ddma_project_if_missing()` (line 2676); the transcription fallback at lines 2754-2760; `run_faster_whisper_transcription()` (line 963).

**Finding:** the launch handler calls the seed in the request path, and the seed runs its OWN transcription when acoustic segments with words are missing:

```python
# If true acoustic segments with words are missing, transcribe with Whisper (word_timestamps=True)
has_valid_words = bool(segments and any(s.get("words") for s in segments))
if not has_valid_words and audio_path and audio_path.exists():
    try:
        settings = load_settings()
        mname = settings.get("whisper_model", "large-v3-turbo")
        res_obj = run_faster_whisper_transcription(audio_path, model_name=mname, word_timestamps=True)
```

The seed does first check the existing transcription file (`SRC_DIR/ddma/docs/episodes/<id>/transcription.json`, around lines 2743-2747) and uses it when it has segments with words — but when that file is missing or has no words, it transcribes the episode itself instead of using the podcast stage's base transcription. The server is threaded, but that does not help: the launch request itself is the one running the transcription, so the launch hangs until it finishes. That is why the UI sticks on "Launching DDMA…".

## 2 — Fix

Per the One-transcription rule, the seed must use the podcast stage's base transcription and never re-transcribe:

1. Remove the synchronous `run_faster_whisper_transcription()` call from `seed_ddma_project_if_missing()` (lines 2754-2760). The seed must never call it.
2. Instead, read the base transcription the podcast stage already produced. Locate where the podcast stage writes it (the unified drop handler triggers transcription on audio drop and saves the base transcription — find that canonical location; the seed already reads the `transcription.json` under `SRC_DIR/ddma/docs/episodes/<id>/`, so check whether the podcast stage's output is that file, a workspace copy of it, or a separate path, and read the canonical one). Use that base transcription's segments for the plan.
3. If no base transcription exists for the episode, the seed (and therefore the launch) must fail LOUDLY with a clear error naming the missing base transcription ("no base transcription for this episode — run the podcast stage first"), instead of transcribing. The launch handler must return promptly with that error.
4. Do NOT change the launch handler's other behaviour (curator spawn, URL return). Do NOT change the podcast stage or the unified drop handler.

## 3 — Verify

- Launch DDMA for an episode that HAS a base transcription → the launch returns promptly (seconds, not the minutes a transcription takes), no transcription runs, and the curator opens with the plan built from the base transcription.
- Launch DDMA for an episode with NO base transcription → a clear error is returned, and no transcription process starts (verify by log/grep that `run_faster_whisper_transcription` is never called from the seed path).
- Add/extend a test asserting the seed never transcribes (e.g. a test that removes/renames the transcription file, calls `seed_ddma_project_if_missing`, and asserts it returns a clear error instead of transcribing — and that no transcription process starts).
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not change the podcast stage, the unified drop handler, or the curator spawn.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. Do NOT run a transcription as part of testing this fix (that is the behaviour being removed). No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report PASS / FAIL for this item with file:line evidence, then continue to the next ITEM.

---

## ITEM 7 of 11 — Workspace drop needs a slug input, not only an episode number

# Fixer prompt — workspace drop needs a slug input, not only an episode number (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ingest/`, test on `localhost:8088`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

The workspace drop is the single drop point for input assets (Python payload + base audio). Today it only takes an episode number, so a payload can only go to `dd_hub/inputs/<episode-number>/`. But the server already accepts a slug — a named input folder — and saves to `dd_hub/inputs/<slug>/` when one is given. The missing piece is only the UI: there is no slug field on the landing-page drop.

## 1 — Where

**Where:** `ingest/landing.html` drop handler (around lines 241-249); `ingest/server.py` `handle_unified_drop()` (line 3582).

**Finding:** the landing-page drop requires an episode number and always uses it as the folder name:

```js
const ep = (document.getElementById('landing-ep').value || '').trim();
if (!ep) {
  setStatus('drop-status', 'Enter the episode number first.', 'err');
  return;
}
let sendFile = file;
let slugChoice = '';
if (isResearch) {
  slugChoice = ep;
} else {
  // The drop endpoint routes digit-named audio to that episode; rename so the
  // target is always the episode typed above, whatever the file was called.
  const stem = file.name.replace(/\.[^.]+$/, '');
  if (!/^\d+$/.test(stem)) {
    sendFile = new File([file], ep + '.' + ext, { type: file.type });
```

Meanwhile the server already accepts a slug override — `handle_unified_drop()` at line 3582 reads `slug_override = str(data.get("slug", "")).strip()` and saves inputs to `dd_hub/inputs/<slug_or_ep>/`, deriving a slug from the payload filename stem when none is given. So the server side is done; only the landing-page UI lacks a slug field.

## 2 — Fix

UI-only — add a slug input to the landing-page drop. Do NOT change `handle_unified_drop()` or any server behaviour:

1. Add a slug text field next to the episode-number field on the landing-page drop (label it clearly, e.g. "Slug (optional — named input folder)").
2. If a slug is entered, pass it as `slug` in the drop payload, so the file goes to `dd_hub/inputs/<slug>/` instead of `dd_hub/inputs/<episode-number>/`. If no slug is entered, keep the current behaviour exactly (episode number required, slug = episode number for research payloads, digit-named audio renamed to the episode number).
3. Validate the slug on the client before sending: reject empty-after-trim (treat as "no slug"), path separators (`/` or `\`), and leading `.` — show a clear error in the drop status and send nothing. Keep the existing "Enter the episode number first" error when neither a slug nor an episode number is given.
4. Show the resolved target folder in the drop status after a successful drop (e.g. "Saved to inputs/<slug>/"), so the user can see where it went.

## 3 — Verify

- Drop a research payload with a slug (e.g. `test-slug`) → it lands in `dd_hub/inputs/test-slug/` (verify via the workspace listing), and the status shows that target folder.
- Drop with only an episode number (no slug) → it lands in `dd_hub/inputs/<episode-number>/` as today, unchanged.
- Drop with an invalid slug (e.g. containing `/`) → a clear error is shown and nothing is written.
- Add/extend a test asserting the slug is passed through (e.g. assert the JS sends `slug` in the drop payload when the slug field is filled, and sends no slug / the episode-number slug when it is empty). Clean up any fixture folder written to the workspace during testing.
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not change the server, the drop endpoint, or the episode-number path.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report PASS / FAIL for this item with file:line evidence, then continue to the next ITEM.

---

## ITEM 8 of 11 — Clip 0 carries the wrong episode's title

# Fixer prompt — clip 0 carries the wrong episode's title (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ddma/`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

Episode 250's clip 0 is titled "What Exactly Is Reality?" while the podcast tab shows the right title ("What Exactly is Infinity?"). "What Exactly Is Reality?" is episode 249's title. Every new episode's clip 0 gets 249's title, because the title is hardcoded in the plan-generation code. The seed generates the plan via the `ddma.py plan` CLI, so every episode seeded since inherits the wrong title.

## 1 — Where

**Where:** `ddma/ddma.py` line 500, in the preamble clip 0 creation (the `clips.append` for `num: 0`, created when the first spoken cue starts after 20.0 seconds).

**Finding:** clip 0's title is a hardcoded string:

```python
clips.append({
    "num": 0,
    "title": "What Exactly Is Reality?",
    "start": 0.0,
    ...
```

The docstring in the same file (around line 669) already states the intent: "For Clip 0 (`num == 0`): The overarching Episode Title". The code contradicts it — it writes 249's title into every episode's clip 0. Only the title is hardcoded: the bridge text is dynamic (`"bridge_text": [f"What Is Clip {cues[0]['num']} ?"]`), and the clip 0 segments are built from the episode's own audio. The same wrong title shows on the Intro Clip Title Card, which reads the plan's clip 0 title.

## 2 — Fix

Clip 0's title must come from the episode title:

1. Find where the episode title is available in the plan-generation code (the episode title lives in the episode markdown / summary — the seed passes the episode id, and the `ddma.py plan` command has the episode context). Use that episode title for clip 0's `"title"` at line 500.
2. Keep the bridge text dynamic as it is — only the title changes. Do not change the clip 0 segments, the `first_cue_start > 20.0` preamble condition, or any other clip's title.
3. Update the docstring around line 669 if it still cites the old title as its example — the example should be generic (e.g. "the episode title"), not 249's title.
4. Do NOT touch existing plans on disk (249's plan keeps its own correct title; 250's clip 0 gets fixed the next time its plan is regenerated — do not rewrite stored plans as part of this fix).

## 3 — Verify

- Generate a plan for an episode with a distinct title (episode 250, or a fixture episode titled something unmistakable like "Test Episode Title") and confirm clip 0's `"title"` equals the episode title — NOT "What Exactly Is Reality?".
- Confirm the other clips' titles are unchanged, and the bridge text is still dynamic.
- Add/extend a test asserting clip 0's title comes from the episode title (e.g. in the plan-generation tests: generate a plan for a fixture episode with a distinct title and assert `clips[0]["title"] == <episode title>`).
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not rewrite stored plans.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report PASS / FAIL for this item with file:line evidence, then continue to the next ITEM.

---

## ITEM 9 of 11 — Hide the article command bar on the Podcast and Reels tabs

# Fixer prompt — hide the article command bar on the Podcast and Reels tabs (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ingest/`, test on `localhost:8088`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what was decided, so you don't re-diagnose it)

The cockpit's top command bar shows Preview and Publish on ALL tabs. Both are article-centric: Preview starts the mdBook article preview, Publish commits and publishes the episode/article. On the Podcast tab the workflow is audio (render the master, push it to the audio store); on the Reels tab it is clips. The article Preview/Publish do not apply there, and showing them on every tab invites clicking the wrong action. The decision is: hide the article command buttons on the Podcast and Reels tabs, keep them on the Article tab.

## 1 — Where

**Where:** `ingest/cockpit.html` — the top command bar (comment at line 1513, `<header class="top-command-bar">` at line 1514); the tab switcher inside it (lines 1520-1524); the command-center div (line 1526); the Preview button (line 1533) and the Publish button (line 1538); the tab-switch function `switchMiddleTab()` (line 2657).

**Finding:** the bar is global — Preview and Publish show on all three tabs:

```html
<button class="btn-cmd" onclick="toggleMdServe()" id="btn-serve" title="Start mdBook Preview Server on Port 3000">
    <span>📖</span> Preview
</button>

<button class="btn-cmd emerald" onclick="triggerPush()" id="btn-push" title="Commit and publish episode to remote repository">
    <span>🚀</span> Publish
</button>
```

Preview is `toggleMdServe()` (line 4223, mdBook preview server on port 3000); Publish is `triggerPush()` (line 4254, commit and publish the episode/article). The tabs are switched by `switchMiddleTab(tabName)` (line 2657): `'research'` is the Article tab (Research — the article/template work), `'narrative'` is the Podcast tab, `'media'` is the Reels tab. The active tab defaults to `'research'` (line 2655), and `switchMiddleTab` already toggles each tab's view, right deck, and channel-actions row by tab name. Nothing in it touches the command bar.

One structural constraint: the tab switcher itself lives INSIDE the same `<header>` (lines 1520-1524 — the Research / Podcast / Reels buttons). Hiding the whole header would hide the tab switcher too, and the user could not switch back. So the fix must hide only the article-centric command buttons, not the header.

## 2 — Fix

Hide the article command buttons on the Podcast and Reels tabs, show them on the Article tab:

1. In `switchMiddleTab()` (line 2657), toggle the visibility of the Preview button (`#btn-serve`, line 1533) and the Publish button (`#btn-push`, line 1538): hide them when `tabName` is `'narrative'` (Podcast) or `'media'` (Reels), show them when `tabName` is `'research'` (Article). Use the same display toggling the function already uses for the channel-actions rows.
2. Apply the same visibility on initial load, so the bar matches the restored tab (the active tab is restored from `localStorage` — if the restored tab is Podcast or Reels, the buttons start hidden).
3. Do NOT hide the whole `<header>` — the tab switcher (lines 1520-1524) must stay visible on all tabs so the user can always switch back to the Article tab. Do NOT hide the Mine or Settings buttons — the decision names Preview and Publish only; leave the rest of the command center as it is.
4. Do NOT change what Preview or Publish do — only when they are visible.

## 3 — Verify

- Load the cockpit (Article tab active by default) → Preview and Publish are visible.
- Click the Podcast tab → Preview and Publish are hidden; the tab switcher is still visible.
- Click the Reels tab → Preview and Publish are hidden; the tab switcher is still visible.
- Click back to the Article tab → Preview and Publish are visible again.
- Reload the page while on the Podcast tab (the tab is restored from storage) → Preview and Publish are still hidden on load.
- Confirm Preview and Publish still work from the Article tab (click Preview → the mdBook preview starts on port 3000; click Publish → the article publish flow runs as before).
- Add/extend a test asserting the visibility toggles with the active tab (e.g. a Puppeteer check that clicks each tab and asserts `#btn-serve` / `#btn-push` are visible on the Article tab and hidden on the Podcast and Reels tabs — add it to the existing test suite, or verify by hand in the browser if there is no cockpit test harness).
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not change the tab switcher, the tab views, or what Preview/Publish do.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report PASS / FAIL for this item with file:line evidence, then continue to the next ITEM.

---

## ITEM 10 of 11 — Music dropdown always shows 'Digital Silence'

# Fixer prompt — music dropdown always shows "Digital Silence" (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ddma/`, test on `localhost:8000`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

The curator's music-segment dropdown shows "Digital Silence" for the clips of 249 and 250, but the audio is the real sting — pressing the Audio button plays the correct sting (e.g. "Howling"). The audio is right and the label is wrong: the dropdown's selection never matches, so the browser falls back to the first option. This is a UI-label bug only.

## 1 — Where

**Where:** `ddma/curator.html` lines 6532 and 6534 (the music dropdown options); `ddma/scratch/run_curator.py` `/list-music` handler (line 5272); playback at `ddma/curator.html` line 7158.

**Finding:** the dropdown's first option is "Digital Silence", and an option is selected only on an EXACT match:

```js
let musicOptionsHtml = `<option value="none">Digital Silence</option>`;
...
const isSelected = seg.music_file === f ? 'selected' : '';
```

But the two sides store different forms of the same filename: the plan stores `music_file` WITH a `music/` prefix (e.g. `music/Bluesy Vibes (Sting) - Doug Maxwell_Media Right Productions.mp3`, `music/deepDive-conclusion.mp3`), while `/list-music` returns BARE filenames — `os.listdir("music")` at line 5276, filtered to `.mp3`/`.wav`/`.m4a`:

```python
elif parsed_url.path == '/list-music':
    music_dir = "music"
    files = []
    if os.path.exists(music_dir):
        files = sorted([f for f in os.listdir(music_dir) if f.lower().endswith((".mp3", ".wav", ".m4a"))])
```

So `seg.music_file === f` compares `"music/Bluesy Vibes ...mp3"` against `"Bluesy Vibes ...mp3"` — it never matches, no option is selected, and the browser shows the first option ("Digital Silence"). Playback is unaffected because it uses `seg.music_file` directly (`playMusicSegment(seg.music_file, seg.duration, seg.volume)` at line 7158).

## 2 — Fix

Match by basename:

1. When building the dropdown options (around line 6534), compare the BASENAME of `seg.music_file` against each filename `f` — strip the `music/` prefix (or compare basenames on both sides) so `"music/Bluesy Vibes ...mp3"` matches `"Bluesy Vibes ...mp3"`. The selected option must be the clip's actual sting.
2. Do NOT change what `/list-music` returns (bare filenames), do NOT change what the plan stores (the `music/`-prefixed path), and do NOT change playback (it already uses `seg.music_file` directly and is correct).
3. Keep "Digital Silence" as the first option and keep it selected only when the segment genuinely has no music (`music_file` is `"none"` or empty).

## 3 — Verify

- Open the curator for an episode whose clips have a music sting set (e.g. 249 clip 10, whose plan stores a `music/...` sting) and confirm the dropdown shows the actual sting name, not "Digital Silence". Check at least two clips with different stings.
- Confirm a segment with genuinely no music still shows "Digital Silence" selected.
- Confirm playback is unchanged (the Audio button still plays the same sting as before).
- Add/extend a test asserting the basename match (e.g. in `test_curator.js`: set a segment's `music_file` to `"music/<name>.mp3"` and assert the dropdown selects the `<name>.mp3` option, not "Digital Silence").
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not change the plan format, the `/list-music` response, or playback.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report PASS / FAIL for this item with file:line evidence, then continue to the next ITEM.

---

## ITEM 11 of 11 — Publish button loses its '✅ Published' state on refresh

# Fixer prompt — Publish button loses its "✅ Published" state on refresh (head `390e0a1a`)

Fix in deepDive only (workbench: `deepDive/ddma/`, test on `localhost:8000`). Fan-out to standalone ddma is a separate, human-initiated step after this lands — do not push to mdIngest/ddma from this prompt. One fix at a time, no refactors of working code, no batch rewrites.

## Background (what happened, so you don't re-diagnose it)

After publishing a clip, the Publish button shows "✅ Published" (green, with a checkmark). On page refresh the checkmark and color go away — the button reverts to plain "Publish", even though the clip IS published (it is on GitHub and listed in the episode index). The Mosaic button does not have this problem: it persists as "Mosaic ✓" (green) after a refresh, because the plan stores the mosaic state. The Publish button has no equivalent persisted state.

## 1 — Where

**Where:** `ddma/curator.html` `publishClip()` (line 5747) and the card render (lines 6716-6721); `ddma/scratch/run_curator.py` `/publish-clip` endpoint (line 4122); `save_plan()` at line 243.

**Finding:** the "✅ Published" state is set only in the browser (in-memory/DOM) after a successful POST and is never persisted:

```js
btnEl.innerHTML = '✅ Published';
```

On refresh, the curator re-renders the clip cards from the plan — and the card render checks ONLY the lock:

```js
let publishBtnHtml = "";
if (isLocked) {
    publishBtnHtml = `<button ...>🚀 Publish</button>`;
} else {
    publishBtnHtml = `<button ... disabled ...>🚀 Publish</button>`;
}
```

It always renders "🚀 Publish" (or the greyed version when unlocked) — it never checks any published state. Meanwhile the `/publish-clip` endpoint (line 4122) loads the plan via `load_plan()` at line 4131, verifies the lock, copies the master, regenerates the manifest, does the scoped git add/commit/push, and returns success with the clip's GitHub URL at line 4254 — but it never writes anything back to the plan. The Mosaic button is the parallel that works: the render checks `clip.mosaic_run_id` plus the local mosaic file (`curator.html:6650`, `const hasMosaicRender = Boolean(clip.mosaic_run_id) && Boolean(statusInfo.has_mosaic_file)`), so its state survives a refresh.

## 2 — Fix

Persist the published state — store it in the plan when the Publish succeeds, and render from it on load:

1. In the `/publish-clip` endpoint, after the successful scoped push, set a published flag on the clip in the plan (e.g. `published_url` = the GitHub URL already returned in the response, and/or `published: true`) and save the plan via `save_plan()` (line 243). Do this for both the fresh-publish and the already-published (`already_published: true`) paths, so a re-publish also lands the flag.
2. In the card render (around lines 6716-6721), if the clip has the published flag, render "✅ Published" (green, same styling as the post-publish state) instead of "🚀 Publish". Keep the lock gating: an unlocked clip still shows the greyed button — the published flag must never bypass the lock check.
3. Do NOT change the Publish endpoint's other behaviour (scoped commit of clip + both episode-index copies only, idempotency, the `already_published` response). Do NOT change the Mosaic button.

## 3 — Verify

- Publish a clip, refresh the page, and confirm the button still shows "✅ Published" (green) — the checkmark and color survive the refresh.
- Re-publish the same clip (already-published path) → the response returns `already_published: true` and the button still shows "✅ Published" after a refresh.
- Confirm an unpublished locked clip still shows "🚀 Publish", and an unlocked clip still shows the greyed button.
- Add/extend a test asserting the persisted state (e.g. in `test_publish_clip.js`: publish a fixture clip, reload the plan, assert the published flag/URL is set; and assert the card render shows "✅ Published" when the flag is present). No Mosaic runs.
- Report PASS / FAIL with file:line evidence and the exact commands run. Do not over-claim: if a Verify step did not run, say so.

## Guardrails

- Fix only the item above. Do not rebuild earlier features. Do not change the Publish endpoint's scoped commit, idempotency, or lock semantics.
- Every fix must expand the tests to assert that exact behaviour BEFORE declaring success. A fix without its test is not done.
- Do NOT trigger any Mosaic run. No keys in git. Git diff only the intended files.
- Do not commit or push. Stage nothing. The user commits.
- Report and STOP.

---

## After ITEM 11

Give a one-line summary per item (PASS / FAIL), listing the files changed. Then STOP. Do not commit or push.
