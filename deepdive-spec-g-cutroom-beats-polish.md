# Spec G — Infographic render runs in the background, the publish gate compares against the draft, Beats switches atomically, one settings screen

Source: the user's manual test of Cutroom and Beats Studio on the Spec F build (2026-11-23) and his rulings the same day. This spec collects the four findings from that test: the infographic render locks the whole Cutroom screen while it works; a published clip once shipped the black draft compile instead of the good render; switching episodes in Beats Studio leaves the old episode's media on screen beside the new episode's clip list; and the two studios still show two different settings screens. The user's pick for the infographic fix is the Mosaic-parity background job — the render runs behind the screen with a progress sign on its own button, plus a plain-language progress line.

**Terms (the user's model):** the **Workspace** is the envelope — the landing page. **Cockpit, Cutroom and Beats Studio are the apps** inside it. Whether two of them happen to be served by the same process is an implementation detail the user never sees; specs and UI copy use the envelope/apps language.

## Grounding (verified at deepDive `8e9d923d`)

- The infographic render in Cutroom is a blocking, full-screen modal overlay: while it runs (about a minute), the header links are unclickable and no other clip can be touched. The Mosaic render in the same page already does it right — it runs as a background job, the screen stays free, the button carries a progress sign (`.btn-mosaic-progress`), and status is polled.
- The infographic endpoint is `/render-local-infographic` (`ddma/scratch/run_curator.py`, around line 4543). It stitches pre-compiled archetypes first; failing that, it falls back to storyboard/plan scenes; failing that, it asks Gemini to design scenes. It has no skip-on-existing-draft behaviour. The modal then plays the COMPILED clip — which stays black canvas whenever no infographic file got composited in. Nothing in the flow reports how many scenes were stitched or designed, or that none were.
- The Draft button compiles the "1-click Black Canvas Baseline preview (Intro + Black Canvas Audio Body + Outro)" via `/compile-clip?draft=true` — black with captions, by design. A black canvas preview and an infographic preview are currently indistinguishable in the player.
- The publish endpoint is `/publish-clip` (`ddma/scratch/run_curator.py`), whose file-selection step resolves local cache, then hub primary, then a fresh compile. A publish replaced a 4.2 MB black draft compile with an 11.3 MB render carrying the full visuals — the publish flow itself carried the good file. A brightness-based check on the file about to be published is NOT a valid gate: the renderer's style is thin white line art on black, and a real scene reads about 1% bright pixels — the same as an empty frame under a brightness threshold.
- In Beats Studio, selecting a different episode re-rendered the clip list with the new episode's clips, while the player, the timeline strip and the master badge kept the previous episode's media. The switch is split across two paths: `initLongformBeatStudio()` in `ddma/beats.html` returns silently (`if (!res.ok) return;`, around line 412) after the `/api/beats/index` fetch fails, while the clip list renders from a separate path (`beatsLoad()`, around line 1011; `beatsEpisode()`, around line 986, reads the dropdown value).
- Settings already share one source (the vault settings file, unified in Spec F) and one door position (bottom of the left pane, every app). The modal CONTENTS still differ: Beats Studio's System Settings is the flat vault-fields list (keys, agent ID, tips address, show URLs — the Cockpit shape); Cutroom's is the tabbed Studio Settings (music sting library, Gemini Co-Pilot Prompts, Mosaic Motion Design).

## The rulings this spec implements

1. **A long render never locks the screen.** The infographic render becomes a background job like Mosaic's: the screen stays free, the button carries the progress sign, and a plain-language progress line says what is happening — no technical terms.
2. **A render reports its outcome.** The infographic flow says how many scenes it stitched or designed, or that it failed and why. A preview that contains no infographic is labelled as a draft, never presented as the infographic.
3. **A publish verifies the file it is about to ship, against the draft — not against an absolute brightness number.** The file must differ from the black-canvas draft by structure; a file that is the draft in substance is refused with a named reason. The publish prefers the verified good local master and never silently substitutes a fresh compile.
4. **An episode switch is atomic.** The player, timeline, master badge and clip list all move to the new episode together, or the page says plainly that the episode has no data yet. A half-switched page never appears.
5. **One settings screen.** The same modal, with the same sections, opens from every app's left-pane-bottom door — Keys & Accounts, Music & Stings, Prompts & Motion — over the one vault source.

## Rules (every phase)

- Work in the WSL clones (`~/github/deepDive`, `~/github/mdIngest`); pull both before starting.
- The fix lands in deepDive first and is mirrored to mdIngest in the same phase; run the fan-out parity check after each phase and include its output in the report. The plan data files (`ddma/plan.json`, `ddma/docs/plan.json`) are deepDive-only and are never mirrored; if the fan-out check flags them, report the flag and leave them.
- One local commit per phase per repo. Push both repos only after the final phase's Verify passes.
- Tests use a fixture hub and fixture files only. Starting the app's own servers in a test is fine; no transcription, Mosaic, or Manim run is triggered by any test — stub the render and transcription entry points where a code path would call them.
- If a phase's premise check contradicts this spec's grounding, STOP that phase and report what the code actually shows; do not improvise a redesign.

## Phase 1 — The infographic render runs in the background and reports its outcome

**Fix (`ddma/curator.html`, `ddma/scratch/run_curator.py`):**

- The infographic render becomes a background job on the Mosaic pattern: the request returns immediately with a job identity, the screen stays fully usable (header links clickable, other clips openable) while it runs, and the page polls the job's status. The Manim button carries a progress sign while its job runs, the way the Mosaic button already does (`.btn-mosaic-progress`).
- Under the Manim window, a plain-language progress line narrates the job in the user's words, not the engine's: while designing, "Designing your infographic…"; while building, "Building the video…"; on success, "Ready — your infographic is in the preview." No file names, no function names, no engine jargon anywhere in the line.
- The render reports its outcome to the page and to the server log: how many scenes were stitched from pre-compiled archetypes, how many were designed (by storyboard/plan or by Gemini), or FAILED with the reason (which source was empty, which call failed). A run that produced zero scenes is a failure, not a silent success.
- The preview distinguishes the two things it can show: if the compiled clip contains no infographic file, the player labels it "Draft — no infographic yet" and does not present it as the infographic. The black-canvas draft keeps its own label as the baseline preview.

**Verify:** with the render entry point stubbed to a controllable fixture (fast success, slow success, zero-scene failure): (1) starting a render returns immediately and the page stays interactive — a header link click and another clip's open both work while the stub is still running; (2) the Manim button shows the progress sign for the job's duration and clears it on completion; (3) the progress line shows the plain-language states in order and never a technical string; (4) a zero-scene stub run reports FAILED with its reason in the log and the page shows the failure, not a black preview passed off as the infographic; (5) a successful stub run shows the infographic label and the scene counts (stitched/designed) in the report; (6) the Mosaic background job is unchanged (its button sign, polling and screen freedom still pass).

## Phase 2 — The publish gate compares against the draft

**Fix (`ddma/scratch/run_curator.py`, the publish path):**

- Before the publish writes or pushes anything, the gate probes the file ABOUT TO BE PUBLISHED — the resolved file, after the local-cache / hub-primary / compile selection — and compares it against the black-canvas draft baseline for the same clip, by structure, not by brightness. The comparison must detect the renderer's own content (line art, shapes, scene changes across time) against the draft's near-identical frames; an absolute brightness or bright-pixel threshold is not acceptable anywhere in the gate, because the renderer's real scenes read the same as an empty frame under one.
- If the file is the draft in substance (no structural difference from the baseline), the publish refuses with a named reason ("the file to publish matches the black-canvas draft — no infographic/render content detected") and writes nothing. It never falls back to a different file silently.
- Master selection: the publish prefers the verified good local master. If the resolved file and the local master disagree (different size, different duration, different hash), the publish reports the mismatch and stops instead of pushing the worse file. A fresh compile is never substituted for an existing good master without that report.
- Duration diagnostic: the gate logs the container duration and the video-stream duration of the file about to be published; if they disagree, the log names both numbers. A disagreement is a warning in the log, not a refusal.

**Verify:** on fixture files only (a fixture draft compile, a fixture render with sparse line art, a fixture render with rich visuals, and a fixture master): (1) the gate ACCEPTS the sparse-line-art fixture and the rich fixture — both pass, proving the check is not a brightness threshold; (2) the gate REFUSES the draft fixture itself with the named reason and writes nothing; (3) a fixture where the resolved file differs from the local master (different hash) stops with the mismatch report and pushes nothing; (4) a fixture with disagreeing container/video durations logs both numbers and still publishes when the structure check passes; (5) the existing publish behaviour for a good file is unchanged (same endpoints, same plan writes).

## Phase 3 — Beats Studio switches episodes atomically

**Fix (`ddma/beats.html`):**

- The episode switch becomes one atomic operation: the clip list, the player, the timeline strip and the master badge all load from the same fetch, and the page updates them together only after that fetch succeeds.
- The silent return goes. On any load failure — the index fetch fails, the episode has no Beats data, or the data is malformed — the page shows an explicit empty state naming the episode: "Episode N has no Beats data yet." The previous episode's media never stays on screen beside the new episode's list.
- The dropdown value, the list and the player all read from the same resolved episode after the switch; no path renders the list from one episode while another path holds the player on the old one.

**Verify:** against a fixture hub with one episode that has Beats data and one that has none: (1) switching to the episode with data moves the list, player, timeline and master badge together to that episode's media; (2) switching to the episode without data shows the "has no Beats data yet" empty state with no leftover media from the previous episode; (3) a simulated index-fetch failure shows the same empty state (never a half-switched page); (4) switching back and forth twice leaves no stale state (player, badge and list all agree on the current episode).

## Phase 4 — One settings screen

**Fix (the settings modal in all three apps; the vault source is unchanged from Spec F):**

- There is one settings screen, opened by the same left-pane-bottom door in Cockpit, Cutroom and Beats Studio. It has three sections, in this order: **Keys & Accounts** (the vault fields — Gemini/Mosaic keys, agent ID, Lightning tips address, show URLs), **Music & Stings** (the music sting library), **Prompts & Motion** (Gemini Co-Pilot Prompts, Mosaic Motion Design). The section contents are the union of the two screens that exist today — nothing is dropped, nothing is duplicated.
- The screen reads and writes the one vault source. A change saved from any app's door reads back the same from every other app's door. The door position and the source do not change in this phase (Spec F already settled both); only the modal's contents are consolidated.
- The old tabbed Studio Settings screen and the old flat vault-fields screen are both retired; no app keeps its own field set.

**Verify:** (1) the same three-section screen opens from the left-pane-bottom door in all three apps, with identical section order and contents; (2) a change made through the Beats door (a key, a sting, a prompt) reads back through the Cutroom door and the Cockpit door, and lands in the vault file; (3) no top-right settings entry exists in any app; (4) the old tabbed screen and the old flat screen are gone — no code path opens either.
