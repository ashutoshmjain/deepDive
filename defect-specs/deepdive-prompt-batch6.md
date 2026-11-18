# Batch 6 — Caption dialog + B1 test fallout + decision + verify-only confirmations

## Scope and head

- Repo: deepDive, head `d6fece9a` (master). All line numbers below were verified at this head.
- **Repo layout note:** `ddma.py`, `run_curator.py`, `test_curator.js` live under `ddma/` (top level), NOT `src/ddma/`. Use `ddma/ddma.py`, `ddma/scratch/run_curator.py`, `ddma/scratch/test-env/test_curator.js` in this spec. The canonical docs publication is `src/ddma/docs/episodes/`. The widget is `theme/book.js` AND `ingest/lightning-widget.js`, mirrored to `mdIngest/ui/lightning-widget.js`.
- This batch is 6 entries, grouped by theme. Part A is by reference; Part B is a test fix; Part C is a decision item (report only, no change); Part D is verify-only (items already resolved in code — confirm and report, do NOT change code). Execute them in order. Report PASS/FAIL per verify step, then STOP with a full summary.
- Coverage note (for the human reader, not part of any Fix): A1 is the caption-dialog simplification (by reference), B1 deletes the three e2e tests that assert the removed "Social Prose & Nostr" sub-tab, C1 is the Workspace home link keep-vs-revert decision (no change), D1 confirms the Article command bar already hides on Podcast/Reels, D2 confirms the mdIngest README already has the dd_hub setup section, D3 confirms the DDMA launch seed never re-transcribes. Security items (dev-server hardening) are explicitly OUT of this batch — they go in a later batch, on hold until 100 users.

## Guardrails

- Fix in deepDive where the file lives there. Three files exist ONLY in the mdIngest repo (`Cargo.toml`, `CHANGELOG.md`, `start_ui.bat`) — edit those in mdIngest directly; there is no deepDive copy to fan out from. Do not edit any other standalone-repo file directly.
- No Mosaic runs. No keys in git. No commit/push (fan-out is a separate human step). Deletions leave changes uncommitted for review.
- Do not refactor beyond what each item names. Do not touch the compile, the plan generation, the Mosaic modal, or any other dialog — except where an item explicitly names it.
- For every deletion item: grep for references BEFORE deleting; if a live reference exists, do NOT delete — report it instead.
- If an item's fix is ambiguous, verify and report rather than guessing — do not invent a behaviour.
- **Workflow file note (not a code item):** `.github/workflows/e2e.yml` is written but untracked on disk. Include it in the Batch 6 push IF a workflow-scope token is available; otherwise leave it untracked and report that. Do not write or change any workflow file as part of this batch.
- **Verify-only items (Part D):** do NOT change code for these. Confirm the stated facts in code and data, then report PASS/FAIL. If a stated fact does NOT hold, report it as a FAIL with the evidence — do not silently "fix" it.
- **Decision item (Part C):** report the current state neutrally and STOP on that item. Do NOT change code for it. The human decides.

## Part A — Included by reference (execute the referenced spec exactly as written)

### A1. Simplify the clip text dialog to captions-only

- **Where:** Execute `defect-specs/deepdive-prompt-caption-dialog-simplify.md` exactly as written. It is included here by reference, not rewritten.
- **Fix direction (summary):** replace the two-pane dialog with a single captions box — timestamps display-only, text editable; on Save, pair each line's text with the ORIGINAL chunk's start/end by line position (timestamps from the textarea are ignored entirely); keep Save + Revert + Cancel; remove the script pane, Auto-Align, Whisper Sync, Copy .ASS, stats, and the Mosaic "Edit Clip Text" button.
- **Verified at this head:** the dialog is still the old two-pane version — modal `#clipTextModalOverlay` at `ddma/curator.html:1662`, script textarea `clipTextInput` at `:1691`, Whisper Sync button `whisperResyncCaptionsBtn` at `:1703`, `parseChunksFromTextarea()` at `:2603`.
- **PRECONDITION — read this first:** the referenced spec file must exist at `defect-specs/deepdive-prompt-caption-dialog-simplify.md` in the repo before executing this item. If it is absent (404), STOP on this item and report BLOCKED — do NOT invent the spec, do NOT reconstruct it from memory, do NOT execute from a local copy. (This exact failure blocked Batch 5's A2: the file was local-only and not in the tree.)
- **Note:** the referenced spec's line numbers were written against an earlier head and have shifted — re-verify every line number at the current head before editing; the element IDs and structure are unchanged.
- **Verify:** per the referenced spec (one captions box, timestamps unchanged after a text edit and after a deliberate timestamp edit, Revert restores saved text, Cancel saves nothing, Mosaic modal has no "Edit Clip Text" button, suites pass).

## Part B — Test fix

### B1. Delete the three e2e tests that assert the removed "Social Prose & Nostr" sub-tab

- **Where:** `ingest/tests/cockpit_e2e.js`. Batch 5's B1 removed the "Social Prose & Nostr" sub-tab from `ingest/cockpit.html` (147 lines). Three tests assert UI that no longer exists and now fail:
  - Test 5, "Narrative Tab: Read-Only Paper Sheet, Sats Wallet & Audio Syndication Parity" (`:758`, block `:756–778`): waits for `#narrative-paper-sheet` (`:770`) and reads its HTML for the lightning-widget and the Spotify/Apple pills.
  - Test 6, "AI Paragraph Streamliner & Promotion Quote Isolation" (`:782`, block `:780–804`): looks up `#btn-submode-nostr` (`:784`) and requires `#btn-streamline-ai` to exist (`:787–788`), then clicks it and waits for a toast.
  - Test 7, "Narrative Tab: Clean Paper Sheet, Canonical Preview, Vim Bridge & RHS Nostr Pipeline" (`:808`, block `:806–856`): requires `#btn-streamline-ai` (`:811`), `#btn-open-vim` (`:819`), `#narrative-toolbar` (`:823`), and `#narrative-rendered-body` (`:829`).
- **Finding:** every element ID these three tests assert is gone from `ingest/cockpit.html` at this head — `#narrative-paper-sheet`, `#btn-streamline-ai`, `#btn-open-vim`, `#narrative-toolbar`, `#narrative-rendered-body`, `#btn-submode-nostr`, `#submode-view-nostr` all return zero matches. There is no surviving equivalent to repoint them at: the Podcast Studio tab that replaced the sub-tab carries none of these elements. The only remaining `#btn-submode-nostr` reference in the whole test file is Test 6's line `:784`.
- **Fix:** Delete all three test blocks entirely — Test 5 (`:756–778`), Test 6 (`:780–804`), Test 7 (`:806–856`), including their comment headers and the blank separator lines between them, so the file stays clean. Do NOT invent replacement assertions. Do NOT repoint them at the Podcast Studio tab (it has no equivalent elements). Do NOT touch any other test. After the deletion, grep the test file for `btn-submode-nostr`, `submode-view-nostr`, `narrative-paper-sheet`, `btn-streamline-ai`, `btn-open-vim`, `narrative-toolbar`, `narrative-rendered-body`, `streamlineNarrative`, `openExternalVim` — zero matches expected.
- **Verify:** The three tests are gone (their names no longer appear in the file). The full `cockpit_e2e.js` suite runs and the only remaining failure is the known environmental 1h curator-click assertion (cross-origin tab reuse — changing the assertion or app code is forbidden, so that failure is expected and is not this item). Grep for the removed selectors returns zero matches. No other test was changed (report the test count before and after).

## Part C — Decision item (report only, no change)

### C1. Workspace home link — keep or revert? (human decides)

- **Where (current state, verified at this head):** all three apps carry a "🏠 Workspace" home link pointing at the landing page on `:8088`, using the named target `deepdive-workspace` (first click opens the workspace tab, later clicks reuse it):
  - Cockpit header: `ingest/cockpit.html:1547–1551` — `<a href="http://127.0.0.1:8088/" target="deepdive-workspace" id="btn-workspace">` (comment "Workspace home page (landing page, named target reuses the tab)" at :1547).
  - Curator header: `ddma/curator.html:1539–1540` — `<a href="http://127.0.0.1:8088/" target="deepdive-workspace" id="topWorkspaceBtn">`.
  - Beats Studio header: `ddma/beats.html:31` — `<a href="http://127.0.0.1:8088/" target="deepdive-workspace">`.
- **Finding:** the links are committed and working. The open question is whether they should stay (they give every app a way back to the workspace home) or be reverted (they were called premature polish — the UI is still evolving and navigation chrome may change). Neither option has been decided.
- **Fix:** NONE. Do NOT keep-or-revert on your own. Do NOT change any of the three links, their targets, or their labels.
- **Verify (report only):** confirm the three links above exist with the stated `href` and `target`, and that clicking one opens/reuses the `deepdive-workspace` tab. Report the current state neutrally with the two options (keep as-is vs revert all three links) and STOP on this item. The human decides.

## Part D — Verify-only: already resolved, confirm and report (do NOT change code)

### D1. Article command bar hides on Podcast/Reels tabs

- **Verified at this head:** the hiding logic is in `switchMiddleTab(tabName)` (`ingest/cockpit.html:2597`), with an explicit comment at `:2630–2633` ("Article-only commands: Preview/Publish apply to the Article tab; hide them on Podcast/Reels. The header (with the tab switcher) stays visible so the user can always switch back."). It sets `showArticleCmds = (tabName === 'research') ? '' : 'none'` (`:2636`) and applies it to `#btn-serve` (`:1533`, Preview) and `#btn-push` (`:1538`, Publish) at `:2638–2644`. It runs on every tab click (buttons at `:1521–1523`) AND on load/restore (`:2273`, `switchMiddleTab(savedTab)`), so a reloaded Podcast tab stays hidden. Test 2b, "Article command bar hides on Podcast/Reels tabs" (`ingest/tests/cockpit_e2e.js:608`), already asserts all of it: Article visible, Podcast hidden + switcher stays, Reels hidden + switcher stays, reload-on-Podcast still hidden, back-to-Article visible again with handlers wired (`toggleMdServe`, `triggerPush`).
- **Verify:** Confirm the hiding logic is present in `switchMiddleTab` and is wired on tab click + load/restore, and that Test 2b exists and passes, then report PASS. Do NOT change code. If any fact does NOT hold, report it as FAIL with the evidence.

### D2. mdIngest README already has the dd_hub setup section

- **Verified at this head:** the mdIngest README at head `4649734` carries the full "## 🗄️ Setting up dd_hub (the workspace)" section at lines `:66–120` (55 lines, ending before "## 🤖 1-Prompt Setup for Antigravity & AI Assistants" at `:121`). It is the canonical full section — it states "mdIngest is the main app and the entry point" and covers the Drive folder, the local-mount-only rule (`DD_HUB_ROOT`, never the Drive web API), the Windows path, the Linux/rclone mount, the no-FUSE `rclone copy` fallback, the vault, and verification. The ddma README carries a short pointer section at `:63–73` that says "Set up dd_hub by following the install instructions in the mdIngest README" — the ddma section deliberately defers to mdIngest's. The deepDive mirror `ddma/README.md` also carries the section (`:63`).
- **Verify:** Confirm the full section exists in the mdIngest README (`:66–120`) with the mount-only rule and the rclone + no-FUSE fallback, confirm the ddma README pointer section exists, then report PASS. Do NOT change any README. If any fact does NOT hold, report it as FAIL with the evidence.

### D3. DDMA launch seed never re-transcribes

- **Verified at this head:** `seed_ddma_project_if_missing` (`ingest/server.py:2690`) reads the podcast stage's base transcription and never transcribes — the comment in the code states it explicitly ("One-transcription rule: read the podcast stage's base transcription (src copy first via discovery, else the hub copy) — the seed NEVER transcribes. Canonical writer is the unified-drop / auto-transcription path."). There is no faster-whisper or transcribe call anywhere in the seed function. When no base transcription exists anywhere, it fails LOUDLY instead of transcribing: it raises `RuntimeError` ("no base transcription for episode N — run the podcast stage first (expected transcription.json in src/ddma/docs/episodes/N/ or dd_hub/episodes/N/)"). The `/api/ddma/launch` handler (`ingest/server.py:5021`) catches the seed exception and returns it promptly as JSON (`{"success": false, "error": ...}`) instead of hanging on "Launching DDMA…". Note: the seed has an emergency fallback that synthesizes segments from existing transcript text distributed over the audio duration when segments are missing but transcript text exists — that distributes text the podcast stage already produced; it does not run Whisper and is not a re-transcription.
- **Verify:** Confirm the seed function contains no transcribe call, confirm the loud `RuntimeError` on missing base transcription, confirm the launch handler returns the seed error as JSON, then report PASS. Do NOT change code. If any fact does NOT hold, report it as FAIL with the evidence.

## Global verify (run after all items)

1. Run the existing test suites and report the counts (`test_compile_scope.py`, `test_canonical_audio_compile.py`, `test_plan_clip0_title.py`, `test_mosaic_mux_integrity.py`, `test_curator.js` — do NOT run TEST 20 without first confirming its `finally` restore is intact; also `ingest/tests/cockpit_e2e.js` with its self-contained setup). Report PASS/FAIL per suite. Expected after B1: the only `cockpit_e2e.js` failure is the known environmental 1h curator-click assertion.
2. Start the Curator (`:8000`) and the cockpit (`:8088`) and confirm both load with no console errors.
3. Confirm the fan-out diff check (`scripts/check_fanout.py`) passes with the files in sync (note: it will STOP on the unfanned Batch 6 pairs before fan-out — that is correct; report the named pairs).
4. Do NOT publish any clip as part of this verify. Do NOT trigger a Mosaic run. Do NOT commit or push (fan-out is a separate human step).
5. Report PASS/FAIL per item (A1, B1, C1, D1–D3), then STOP with a full summary.
