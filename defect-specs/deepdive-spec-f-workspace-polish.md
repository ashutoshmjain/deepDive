# Spec F — Workspace & studios polish: deliberate transcription, mempool-aware picker, one theme, one header, one pane pattern

Source: the user's manual test of the Workspace page and both studios (2026-11-23) and his rulings the same day. This spec collects the workspace findings from that test — transcription must never start itself, the slug picker must see the mempool, the folder switch needs its caution — and the cross-app consistency items: the landing page joins the application theme, the Docs entry points at the application help, both studios share one header pattern, and both use one pane-collapse pattern.

**Terms (the user's model):** the **Workspace** is the envelope — the landing page. **Cockpit, Cutroom and Beats Studio are the apps** inside it. Whether two of them happen to be served by the same process is an implementation detail the user never sees; specs and UI copy use the envelope/apps language.

## Grounding (verified at deepDive `99695908`)

- The audio branch of `handle_unified_drop` in `ingest/server.py` saves the dropped audio and immediately calls `start_auto_transcription_pipeline(..., force=True)` — force bypasses the pipeline's own "transcription already exists" guard. `sync_dd_hub_inputs` also fires the pipeline for synced audio that has no transcription yet. The deliberate trigger exists separately: `POST /api/audio/transcribe`, an explicit endpoint that starts (or re-starts, with force) transcription for one episode.
- `list_dd_hub_inputs` builds its slug list only from subfolders of `dd_hub/inputs/`; mempool drafts live in the summary structure (`src/_<slug>.md`, enumerated by `parse_summary_structure`) and never appear in the Workspace slug picker.
- The landing page H1 reads "🏠 mdIngest Workspace" (`ingest/landing.html`). Choosing a folder in the Workspace card saves it immediately; the card carries no caution about switching.
- The landing page still has its own palette (14 distinct hex colours) while `ddma/curator.html` and `ddma/beats.html` share the Warm Sand Editorial token set (`:root` tokens + `applyTheme` reading the `ddma-theme` preference).
- The Workspace Apps tile "Docs" links to `http://localhost:3000/` (the mdBook book site). The application help is a different page: `/docs/documentation.html`, served by the Curator on :8000 — the page Cutroom's own Docs button already opens (`ddma/curator.html`, the header Docs link).
- Cutroom's top-right header holds a Docs link, a Settings button, and a Workspace link. The Settings button and the sidebar footer's "System Settings" entry open the same settings modal — two doors, two positions, one app. Beats Studio has no settings door at all today; the Cockpit's settings doors are inventoried in Phase 5.
- Beats Studio's top-right holds plain links (Workspace, cockpit, Cutroom) with inconsistent label casing.
- Cutroom collapses its sidebar via a `.collapsed` class on `.sidebar-panel` (an icon rail remains). Beats Studio collapses panes via `toggleSidePane` — a collapse button in each pane header and an 18px expand edge tab, session-only state. Two patterns for the same gesture.

## The rulings this spec implements

1. **Transcription is never automatic.** It starts only from the deliberate trigger in the Cockpit. Filing audio — by drop or by sync — never starts it.
2. Replacing the audio of an episode that **already has a transcription** is a deliberate, confirmed act; the pair must never be desynced silently.
3. The slug picker lists the **mempool**, not just input folders.
4. One application, one styling: the landing page adopts the shared theme; both studios share one header link pattern; both use one pane-collapse pattern (Beats Studio's, the purpose-built one).
5. "Docs" everywhere means the **application help** — the Curator-served documentation page — not the book site.
6. **Settings: one source, one position, every app.** The same settings (one saved source) are reachable from the **bottom of the left pane** in each of the three working apps — Cockpit, Cutroom, Beats Studio — and from **no** top-right header. This is the one-path rule applied to position: the door is in the same place on every screen, not a different path per screen. No app grows its own settings store or its own field set; each door opens the same settings.

## Rules (every phase)

- Work in the WSL clones (`~/github/deepDive`, `~/github/mdIngest`); pull both before starting.
- The fix lands in deepDive first and is mirrored to mdIngest in the same phase; run the fan-out parity check after each phase and include its output in the report. The plan data files (`ddma/plan.json`, `ddma/docs/plan.json`) are deepDive-only and are never mirrored; if the fan-out check flags them, report the flag and leave them.
- One local commit per phase per repo. Push both repos only after the final phase's Verify passes.
- Tests use a fixture hub and fixture files only. Starting the app's own servers in a test is fine; no transcription, Mosaic, or Manim run is triggered by any test — stub the pipeline entry point where a code path would call it.
- If a phase's premise check contradicts this spec's grounding, STOP that phase and report what the code actually shows; do not improvise a redesign.

## Phase 1 — Transcription only by deliberate trigger

**Fix (ingest/server.py; ingest/landing.html for the confirm):**

- Inventory every caller of `start_auto_transcription_pipeline`. Callers that fire as a side effect of a file landing or syncing lose the call — at minimum the audio branch of `handle_unified_drop` and the audio handling in `sync_dd_hub_inputs`. The deliberate `POST /api/audio/transcribe` endpoint keeps its behaviour exactly (including its force semantics — it is the deliberate re-transcribe door). Any other caller the inventory finds is classified in the report as side-effect (call removed) or deliberate (kept, with the reason).
- The audio drop then only files the audio (hub inputs copy + local episode copy, as today) and reports: "Audio saved for episode N — transcription starts from the Cockpit podcast tab." Sync reports the audio as ingested, untranscribed.
- Overwrite guard: `list_dd_hub_inputs` episode entries become objects carrying `has_audio` and `has_transcription` alongside the number (the landing page is the endpoint's only consumer; slugs stay plain strings). When the selected episode `has_transcription`, the page asks before uploading — "Episode N already has a transcription based on its current audio. Replace the audio? The transcription will no longer match until you re-transcribe from the Cockpit." — and sends an explicit `force` flag only on confirmation. Server-side, independent of the page: an audio drop for an episode with an existing transcription and no `force` in the request writes nothing and returns an error naming the state and the remedy. An episode with audio but no transcription, or no audio at all, ingests without any prompt.

**Verify:** with the pipeline entry point stubbed and counted: (1) dropping audio on a fresh fixture episode saves both copies, the stub count stays 0, and the response carries the cockpit-pointer message; (2) syncing an inputs folder containing new audio likewise starts nothing; (3) dropping on an episode with a fixture transcription, without force: nothing is written (both copies' hashes unchanged) and the named error returns; with force after the page confirm: the audio is replaced and the stub count still stays 0; (4) `POST /api/audio/transcribe` still invokes the pipeline exactly once per call.

## Phase 2 — The slug picker sees the mempool

**Fix (ingest/server.py, `list_dd_hub_inputs`):**

- The slugs list merges the mempool draft slugs from `parse_summary_structure` (the `_`-prefixed drafts, prefix stripped) with the `inputs/` slug folders — deduplicated, sorted. Episodes behaviour unchanged (beyond Phase 1's entry objects).

**Verify:** against a fixture hub whose summary holds a mempool draft with NO corresponding inputs folder: the endpoint's slugs include that draft's slug alongside a fixture inputs slug; a draft that also has an inputs folder appears once; calling the endpoint writes nothing (hub + summary hashes unchanged).

## Phase 3 — Workspace page: plain title, folder-switch caution

**Fix (ingest/landing.html):**

- The H1 loses the emoji: "mdIngest Workspace". (The `<title>` already has none.)
- Under the folder controls, a standing caution line: "Choosing a folder switches the whole workspace to it. Restart the apps afterwards so every app reads the same folder — your previous folder is not changed."
- Selecting a folder different from the current one asks first (a confirm naming the picked path and the restart consequence, same words as the caution); selecting the current folder again, or cancelling the browser, saves nothing.

**Verify:** (1) the rendered H1 contains no emoji; (2) the caution line is present in the Workspace card; (3) in a fixture run, picking a different folder shows the confirm and only saves after acceptance; cancelling leaves the saved hub path unchanged.

## Phase 4 — The Workspace page adopts the application theme

**Fix (ingest/landing.html):**

- Inventory every colour on the page (14 distinct hexes at the grounding head) and produce the colour→token mapping table against the shared set in `ddma/curator.html`'s `:root`, in the report, before editing.
- Replace the page's palette with the shared tokens: the same `:root` variable definitions, the same `applyTheme` + `ddma-theme` localStorage contract, body and components reading variables — the treatment Beats Studio received, applied to the landing page. Semantic colours (success/error states) map to the shared semantic tokens; genuinely page-specific decoration may stay literal only if listed as an exemption with a reason.

**STOP rule:** if the mapping is not at least ~90% mechanical, stop this phase and report the table. `ddma/curator.html` and `ddma/beats.html` diffs stay empty in this phase either way.

**Verify:** (1) computed body background and text colour on the landing page equal Cutroom's (`#fbf9f5` / `#1c1917` family via the tokens); (2) the hex audit: outside `:root`, only exempted literals remain; (3) the page's cards, tiles, pickers and drop zones render in the shared palette with no layout change (DOM structure diff is styling-only); (4) Phases 1–3 behaviours on the page still pass (picker lists, confirm, caution line).

## Phase 5 — One header pattern; Docs means the application help

**Fix (ingest/landing.html, ddma/curator.html, ddma/beats.html):**

- The Workspace "Docs" tile now opens the application help: `http://localhost:8000/docs/documentation.html` — the same page Cutroom's Docs link opens. The tile's state badge follows the **Cutroom** entry of `/api/suite/status` (the app that serves the page), and its click handler treats a failed Cutroom state the way the other tiles treat theirs (retry, then open). The mdBook server stays in the auto-start suite unchanged — the book remains reachable at its own address; only the tile's target changes.
- Both studios get the same top-right link set, each omitting the link to itself, labels identical in wording and casing on both pages: **Workspace, Cockpit, Cutroom, Beats Studio, Docs**. Docs on both pages opens the same application-help URL as above. Link styling uses each page's existing header-link appearance (post-Phase 4, both are on the shared theme).
- Cutroom's top-right **Settings button is removed**, and so is any top-right settings entry the premise inventory finds on the Cockpit. The settings door pattern is then normalized across the three working apps:
  - Premise inventory, in the report before editing: every current settings door on the Cockpit, Cutroom and Beats Studio (position + what it opens + what it writes).
  - Each of the three apps ends with exactly **one** settings door: a "System Settings" entry at the **bottom of the left pane** (Cutroom's sidebar-footer entry is the model — it stays; the Cockpit's door is moved/kept there per the inventory; Beats Studio gains the entry at the bottom of its clips pane).
  - Every door opens **the same settings**: the same fields, the same modal behaviour, and the same saved source (the hub vault settings) — a change saved through one app's door reads back identically through the others. No app stores its own copy of any setting.
  - The Workspace envelope has no left pane and is not a fourth door: its existing pointer line ("in the app's Settings") stays as is.

**Verify:** (1) the Workspace Docs tile's href is the help URL, and with a fixture suite its badge mirrors the Cutroom state; clicking it lands on the help page served on :8000; (2) Cutroom's header contains the four links (no Cutroom link, no Settings button) and Beats' header contains its four (no Beats link), with identical labels; (3) settings doors: no top-right settings entry remains on any app; each of Cockpit, Cutroom and Beats shows its single "System Settings" entry at the left pane bottom; with a fixture vault, a harmless field changed and saved through Beats' door reads back with the new value through Cutroom's door and in the vault file itself (one source, three doors); (4) no other header element moved on either studio page.

## Phase 6 — One pane-collapse pattern (Cutroom adopts Beats')

**Fix (ddma/curator.html):**

- Premise inventory, in the report before editing: how Cutroom's `.sidebar-panel.collapsed` rail behaves today (what stays visible/clickable when collapsed — including the sidebar footer's System Settings), how the right-side transcript pane (if separately collapsible) behaves, and how Beats' `toggleSidePane` pattern works (header collapse buttons `btn-collapse-left/right`, 18px expand edge tabs `tab-expand-left/right`, `lfPaneState` session state).
- Cutroom's collapsible panes adopt the Beats pattern: a collapse button in the pane header, an 18px expand edge tab when collapsed, session-only state, the same dimensions and glyphs. The settings entry and every other function the panes carry remain reachable in both states — collapsed, they live behind the edge tab exactly as Beats' pane contents do.

**STOP rule:** if the inventory shows the rail's collapsed state carries functions that must stay one-click reachable (i.e., collapsing-to-gone would remove a working surface rather than hide a pane), stop this phase and report both inventories instead of removing function.

**Verify:** (1) collapsing Cutroom's left pane hides it fully and the player/list area grows by the pane's width minus the 18px tab (the Beats measurement); the edge tab restores it; (2) the same for any second collapsible pane; (3) post-cycle, the pane's contents (project list, System Settings entry) work as before; (4) Beats Studio is untouched in this phase (its diff is empty) and its collapse still measures as before.

## Report

Per phase: the premise check (what the code showed, with file/line sites — Phase 1 must include the full caller inventory of the transcription pipeline with its side-effect/deliberate classification; Phase 4 the mapping table; Phase 6 the two-pattern inventory), files changed, the fan-out check output, the Verify outcomes, and the two commit hashes. Then: the final heads of both repos, `git status` of both clones (any residue named, never silently left), and any divergence from this spec stated plainly with its reason.
