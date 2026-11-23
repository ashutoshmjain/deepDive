# Spec E — Workspace inputs: two drop flows, folder pickers, deliberate mempool promotion, local-folder workspaces

Source: the user's manual test of the Workspace page (2026-11-22) and his rulings the same day. The Workspace "Inputs — one drop point" card serves two different flows through one drop zone and two free-text fields; a new user cannot tell what to fill for which file. The workspace card likewise assumes a synced-folder URL and offers no route to a plain local folder.

## Grounding (verified at deepDive `b706180f`)

- The Inputs card lives in `ingest/landing.html` (the `#drop-card` section): one episode-number input, one slug input, one drop zone accepting `.py,.md,.m4a,.mp3,.wav,.ogg,.aac`, posting to `/api/dd_hub/unified_drop` → `handle_unified_drop` in `ingest/server.py`.
- `handle_unified_drop` already branches by kind: research payloads (.py/.md) are filed under `dd_hub/inputs/<slug>/` (slug from the field, else derived from the filename); audio is filed under an episode number. The page, however, gates both flows behind "Enter the episode number first" when both fields are empty — an episode number a research drop never needs.
- The audio branch silently promotes research: if the active episode is a Mempool draft (`src/_<slug>.md` in the summary structure parsed by `parse_summary_structure`), dropping audio "auto-mines" the draft to the next episode number and files the audio under it (the CASE 2 resolution in `handle_unified_drop`, and its docstring).
- Workspace resolution is URL-centric: `GET /api/settings` parses the configured `workspace_url` for a Drive folder id and checks the local sync path is readable; its own failure message falls back to "Mount dd_hub / set DD_HUB_ROOT" — an environment variable is the only non-URL route today, invisible inside the app.
- There is no read-only endpoint listing the hub's `inputs/` folders; `/api/dd_hub/sync_inputs` is a sync action, not a listing.

## The rulings this spec implements

1. The two flows are separated into two cards, each with its own drop zone and its own single picker.
2. The research flow takes **text files** — `.py`, `.md`, `.txt` (any text payload) — filed under a **slug**, stored verbatim (no content transformation at drop time). The audio flow takes audio files, filed under an **episode chosen from a list**; the episode selection is mandatory.
3. Movement from mempool to template is a **deliberate action — no automation**. Dropping audio never creates an episode.
4. A workspace is a **plain local folder**, chosen through a folder picker served by the app itself. The synced-folder URL concept is retired: syncing a folder across devices is the sync service's job (Drive for Desktop, OneDrive, Dropbox — any folder can be synced by its owner), not the app's. If the picked folder is not inside a recognisably synced location, the card nudges: to use the app on separate devices, here is the recommended setup — put the workspace folder inside a synced folder.
5. The Apps card is **one row**: the four live status tiles are also the open/start controls. The separate launch-button row underneath them is a pre-auto-start leftover and goes away; the Docs tile stays as the workspace's help-docs entry point.

## Rules (every phase)

- Work in the WSL clones (`~/github/deepDive`, `~/github/mdIngest`); pull both before starting.
- The fix lands in deepDive first and is mirrored to mdIngest in the same phase; run the fan-out parity check after each phase and include its output in the report.
- One local commit per phase per repo. Push both repos only after the final phase's Verify passes.
- Tests use a fixture hub (a throwaway DD_HUB_ROOT) and fixture files only. Starting the app's own servers in a test is fine; no transcription, Mosaic, or Manim run is triggered by any test — stub at the HTTP boundary where a drop would trigger one, or verify up to the trigger point and say so.
- If a phase's premise check contradicts this spec's grounding, STOP that phase and report what the code actually shows; do not improvise a redesign.

## Phase 1 — Two drop cards with pickers

**Fix (landing.html; the drop endpoint's contract unchanged except as noted):**

- Replace the single Inputs card with two cards:
  - **Research — save to mempool.** A drop zone accepting text files (`.py`, `.md`, `.txt`). Above it, a slug picker: a `<select>` listing the slug folders currently in `dd_hub/inputs/` (from the Phase 3 endpoint), plus a "New slug…" entry that reveals a text input. The drop is disabled until a slug is selected or a new slug is typed. When "New slug…" is used and the input is left empty, the existing filename-derivation applies as today. The selected/typed slug is sent as the drop's `slug`, exactly as the current field is.
  - **Audio — add to an episode.** A drop zone accepting the audio extensions the current zone accepts. Above it, an episode picker: a `<select>` listing existing episode numbers (from the Phase 3 endpoint). The drop is disabled until an episode is selected, with the hint "Audio belongs to an episode — pick the episode it belongs to." The selected episode is authoritative for where the file lands (the current behaviour of renaming digit-named files toward the typed episode becomes: the picker wins; no other routing).
- Neither card shows the other flow's field. The shared "Enter the episode number first" gate is removed; each card validates only its own requirement and says what is missing in its own words.
- The research drop stores the file's content verbatim, as the current research branch does; no KaTeX or markdown processing is added at drop time.

**Verify:** against a fixture hub with one slug folder and one episode folder: (1) the research card lists the existing slug; dropping a `.md` with it selected lands the file under that slug, content byte-identical; (2) "New slug…" + a typed name creates and files under the new slug; (3) the audio card's drop control is disabled with its hint before a selection, enabled after; dropping an `.m4a` files it under the selected episode (transcription stubbed); (4) dropping an audio file on the research card and a text file on the audio card each produce that card's own unsupported-type message and write nothing.

## Phase 2 — Remove the audio auto-promotion

**Fix (ingest/server.py, `handle_unified_drop` audio branch):**

- Delete the auto-mine resolution: an audio drop resolves ONLY to the episode the caller selected (Phase 1's picker). If that episode does not exist as an episode (no episode folder / not a template episode in the summary structure), the drop fails with an error that names the remedy: the episode must be created first by moving the draft from mempool to template — the existing deliberate action, wherever it lives today — and the drop changes nothing.
- The digit-filename shortcut (`250.m4a` → episode 250) no longer routes server-side; it may pre-select the picker in the page, nothing more.
- Nothing about the mempool→template promotion itself changes: it stays exactly the deliberate act it is today, in the place it lives today.
- Update the `handle_unified_drop` docstring so it no longer describes mining.

**Verify:** with a fixture hub whose summary structure holds a mempool draft and no matching episode: (1) an audio drop aimed at the draft (or with no valid episode) returns the named-remedy error; the draft file and SUMMARY.md are byte-identical afterwards and no episode folder was created; (2) after performing the deliberate promotion through its existing path, the same drop succeeds; (3) the research branch's behaviour is unchanged (Phase 1 verifies still pass).

## Phase 3 — The inputs listing endpoint

**Fix (ingest/server.py):**

- Add a read-only `GET /api/dd_hub/inputs` returning the current hub's `inputs/` folders split into `slugs` (non-numeric folder names) and `episodes` (numeric folder names), plus the template episode numbers from the summary structure merged into `episodes` without duplicates, each list sorted (episodes numerically). This endpoint feeds both pickers in Phase 1; it writes nothing.
- An empty or missing `inputs/` folder returns two empty lists, not an error — the pickers render their empty states from it (research: only "New slug…"; audio: "No episodes yet" and the drop stays disabled).

**Verify:** against the fixture hub: the endpoint returns exactly the fixture's folders, correctly split and sorted; calling it twice changes no file (hub tree hashes identical); with `inputs/` absent it returns the two empty lists with success.

## Phase 4 — The workspace is a local folder (URL retired, sync nudged)

**Fix (landing.html + ingest/server.py settings):**

- The Workspace card's input becomes a **folder picker**: a "Choose folder…" control opens a folder browser served by a new read-only endpoint (`GET /api/workspace/browse?path=<dir>` returning the sub-directories of a directory on this machine; with no path, it starts from the current hub path if set, else the user's home, and on Windows also offers the drive roots). The user navigates and picks a folder; the picked absolute path is saved through the settings endpoint as the workspace (a path setting).
- The URL field, its folder-id parsing, and the "matches the configured workspace" comparison leave the card. An existing `workspace_url` in settings becomes inert (ignored, not deleted). **Migration:** on first run of the new code, if no path setting exists, the current effective hub path — however it was resolved (URL mapping or `DD_HUB_ROOT`) — is adopted as the saved path, so an existing workspace keeps working with no user action and no data movement. Resolution thereafter: the saved path is the hub; `DD_HUB_ROOT` remains the fallback only when no path has ever been saved.
- The card's status lines show the effective path and whether it is readable, as today ("Talking to: <path>"), with the existing Test action verifying the picked folder the same way it verified the URL mode.
- **The nudge:** the card classifies the picked path by its components. If it contains a known synced-location marker (`My Drive`, `Google Drive`, `OneDrive`, `Dropbox`, `iCloud Drive`), the card notes that the folder is synced by that service and other devices sharing it will see the same workspace. If it does not, the card shows a short recommendation: using this app on more than one device? Put the workspace folder inside a synced folder (Google Drive, OneDrive, Dropbox…) — the sync service keeps the copies in step; this app only reads the folder. Display only; the classification never blocks a pick.

**STOP rule:** if the settings/vault resolution cannot accept a path setting without restructuring how settings are stored, stop this phase and report the obstacle with the relevant code sites. Do not redesign the settings system inside this spec.

**Verify:** (1) in a fixture environment, pick a plain local folder through the browser endpoint flow: the settings save, the status lines show the path, Test passes, and a research drop (Phase 1) lands inside the picked folder's `inputs/`; (2) migration: starting the new code against settings that hold only a `workspace_url` (fixture Drive-style mapping) adopts the previously effective path — the hub is unchanged and drops land where they landed before; (3) the nudge renders in both directions (a fixture path under a `OneDrive` component vs a plain path); (4) the browse endpoint refuses a file path (returns an error) and no endpoint in this phase writes or deletes anything on disk outside the settings save.

## Phase 5 — Apps card: one row of tiles

**Fix (landing.html):**

- Remove the second row of the Apps card — the "Open mdIngest Cockpit", "Launch Cutroom", and "Launch Beats Studio" buttons — together with the page-level JS that only they call (`launchDdMa`, `launchBeats`) and the launcher status line if nothing else uses it. The launch endpoints themselves stay; the tiles' start/retry path uses them.
- The four suite tiles remain as the single row, unchanged in behaviour: each shows its live state (Running / Starting / Failed) and a click opens the app when it is running and starts/retries it when it is not — the behaviour the auto-start build already gives them. The Docs tile keeps its current target; it is the workspace's help-docs entry point and stays first-class among the tiles.
- Nothing else on the page moves; the card keeps its heading and position.

**Verify:** (1) the Apps card renders exactly one row of four tiles and no launch buttons (DOM check for the removed buttons' handlers returns nothing); (2) with all servers running (fixture), each tile shows Running and clicking Docs lands on the docs site; (3) with Beats stopped (fixture), its tile shows the stopped/failed state and clicking it starts the server and then opens it — one click, no separate launch step; (4) the rest of the page (Workspace card, Inputs cards) is functionally unchanged.

## Report

Per phase: the premise check (what the code showed, with file/line sites), files changed, the fan-out check output, the Verify outcomes, and the two commit hashes. Then: the final heads of both repos, `git status` of both clones (any residue named, never silently left), and any divergence from this spec stated plainly with its reason.
