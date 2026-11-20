# Batch 10 — Post-merge cleanup: the Cutroom rename, the landing page, the READMEs, the install prompt

Five items, executed in order. All work happens in the local deepDive workbench; shared files are mirrored to the local mdIngest clone exactly as the fan-out protocol prescribes, but nothing is committed or pushed (see G2).

## Guardrails — read first; they bind every item

- **G1. Order.** Execute B1 → B5 in sequence. Several items touch the same files (landing.html in B1 and B2; curator.html in B1 and B2; the mdIngest README in B4 and B5). Never edit the same file from two items at once.
- **G2. STOP before any commit or push.** Do the edits locally, run every Verify step, mirror the shared files to the local mdIngest clone, run `python scripts/check_fanout.py` (it must exit green), then write the final report and STOP. No `git commit`, no `git push`, no fan-out until a separate instruction says so.
- **G3. No scope extension.** If you find something related but not listed in an item, report it in the final report — do not fix it. If a named string or file is not found where an item says it is, stop that item, report what you found instead, and move to the next item only if it does not depend on the failed one. Do not improvise substitute edits.
- **G4. Branding rule.** Rename ONLY human-readable display strings listed in the items. Internal identifiers stay byte-identical: the `ddma/` folder name, variable and constant names (e.g. `DDMA_DIR`), endpoint paths (e.g. `/api/ddma/launch`), storage and settings keys, JSON field names, code comments, log tags (e.g. `[DDMA SEED]`), music file names (e.g. `deepDive-soft-ok.mp3`), and the browser window-target string `deepdive-workspace`. If a string an item lists turns out to also be a functional identifier (matched against in code, used as a key), stop and report it instead of renaming it.
- **G5. Protected content.** Never stage, modify, or delete: any `settings.json`, episode content (`src/<episode>.md`, `src/ddma/docs/episodes/**`), clips, or any media file. This batch touches code, UI text, and documentation only.
- **G6. Secrets.** Do not read, copy, or print any live `settings.json` or API key values during this batch.
- **G7. Parity.** Every shared file must remain byte-identical between the deepDive workbench and the local mdIngest clone when you finish (the checker in G2 is the judge).
- **G8. Final report.** Per item: PASS or FAIL, the Verify evidence (grep outputs, page-load results), and a complete list of changed files per repo. Attach the audit tables the items require. Report any item you stopped under G3 and why.

## B1 — Rename DDMA → Cutroom on every user-visible surface

**Where:** `ingest/cockpit.html`, `ingest/landing.html`, `ddma/curator.html`, `ddma/beats.html`, `ddma/ddma.py`, `ddma/scratch/run_curator.py`, `ddma/beats_server.py`, `GEMINI.md` (both repos' copies of every shared file).

**Finding:** the media extension's product name is "DeepDive Media Automator (DDMA)" — the reference instance's brand inside the forkable application. The product is renamed **Cutroom**. Only display strings change (G4); the `ddma/` folder and all code identifiers keep their names.

**Fix — make these replacements:**

- `ingest/cockpit.html`: "DeepDive Media Automator (DDMA)" → "Cutroom"; "Open DDMA Studio" → "Open Cutroom" (every instance); "Launch DDMA Studio" → "Launch Cutroom"; "Launch DDMA (Port 8000)" → "Launch Cutroom (Port 8000)"; "DDMA Episode Bridge" → "Cutroom Episode Bridge"; "DDMA Media Controller" → "Cutroom Media Controller"; "Opens the DeepDive Media Automator in a new tab to curate infographic video clips." → "Opens Cutroom in a new tab to curate infographic video clips."; "Opening DDMA Studio (Port 8000)..." → "Opening Cutroom (Port 8000)..."; "Open DDMA Studio to Generate Clips" → "Open Cutroom to Generate Clips"; "DDMA video reels" → "Cutroom video reels"; "Default Whisper STT Model (DDMA Word Timestamps)" → "Default Whisper STT Model (Cutroom Word Timestamps)"; "small.en (DDMA Standard • Fast)" → "small.en (Cutroom Standard • Fast)".
- `ingest/landing.html`: the button "Launch DDMA" → "Launch Cutroom"; "Launching DDMA…" → "Launching Cutroom…"; "✓ DDMA ready:" → "✓ Cutroom ready:".
- `ddma/curator.html`: the `<title>` "SHUTRI DDMA • Media Automation Cockpit (Shutri Pillar 3)" → "Cutroom • Media Automation Cockpit"; the brand wordmark anchor reading "S H U T R I DDMA" (an `<a>` linking to https://deepdive.shutri.com) → a plain `<span>` with the same styling, reading "Cutroom", with no link; the settings-help text "top-right of DDMA Cockpit" → "top-right of Cutroom".
- `ddma/beats.html`: "Updates Shared Longform + DDMA Short Library" → "Updates Shared Longform + Cutroom Short Library"; "set Manim as Active Master in DDMA" → "set Manim as Active Master in Cutroom" (both instances).
- `ddma/ddma.py`: the CLI help "DeepDive Media Automator (DDMA) CLI Tool" → "Cutroom CLI Tool".
- `ddma/scratch/run_curator.py`: in the AI prompts and user-facing strings — "DeepDive Media Automator (DDMA)" → "Cutroom" (the Creative Remix Agent prompt, the Executive Producer prompt, and the Help Assistant prompt, including "You are the DDMA Help Assistant" → "You are the Cutroom Help Assistant"); "so DDMA snaps clip boundaries" → "so Cutroom snaps clip boundaries"; "Please set them up in DDMA first!" → "Please set them up in Cutroom first!"; "In DDMA Cockpit, click" → "In Cutroom, click" (both instances); the launcher banner "DDMA Clip Curator Launcher v2.0 (Multi-Proj)" → "Cutroom Clip Curator Launcher v2.0 (Multi-Proj)".
- `ddma/beats_server.py`: the error text "open DDMA first" → "open Cutroom first".
- `GEMINI.md` (prose only — commands, paths, and identifiers unchanged): "the DDMA extension lives in `ddma/`" → "the Cutroom extension lives in `ddma/`"; "compiled in DDMA" → "compiled in Cutroom"; "the DDMA player" → "the Cutroom player".

**Verify:** (1) `grep -rn "DeepDive Media Automator"` across both repos → zero hits. (2) `grep -rn "DDMA"` across `ingest/` and `ddma/` in both repos → attach the complete hit list to the report; every remaining hit must be an identifier, a comment, a log tag, or an endpoint path — no display string may remain. (3) `grep -c "DDMA"` on both `GEMINI.md` copies → zero, and the two copies are still byte-identical. (4) Start the servers locally and fetch the cockpit, landing, curator, and beats pages — HTTP 200 each.

## B2 — Landing page: mdIngest branding, honest workspace copy, the API-key note; Curator target name and tooltips

**Where:** `ingest/landing.html` (title :6, H1 :34, subtitle :35, field label :39, plus one new note), `ddma/curator.html` (:1740, :1759, :3868, :3871, :6352, :6379), `ddma/scratch/run_curator.py` (the workspace target's default name, wherever it is defined).

**Finding:** the landing page brands the workspace "deepDive" (the application is mdIngest), tells new users the workspace lives "on Google Drive" (it is a plain local folder; Drive is only an optional sync choice), and asks for API keys with no explanation of what they unlock. The Curator shows the reference instance's name and domain in tooltips, and its workspace target carries the old "deepdive-workspace" default name.

**Fix:**

1. `landing.html` `<title>` and `<h1>`: "deepDive Workspace" → "mdIngest Workspace" (keep the 🏠 in the H1).
2. Subtitle: replace "One plan + one settings source on Google Drive, read by every environment." with "One plan + one settings source in one workspace folder, read by every environment." The following sentence ("This page is the shell — the work happens in the apps below.") stays.
3. Field label: replace "Workspace URL (Google Drive folder — same on every environment)" with "Workspace URL (optional — only for a synced folder, e.g. Google Drive; it identifies this workspace on every machine)". The field, the Test button, and the Save URL button behave exactly as before.
4. Add this note to the landing page, directly below the Workspace card, as its own small card or paragraph with the page's existing muted styling: "New here? The workspace runs with no API keys at all. Add keys later, in the app's Settings, when you want what they unlock: a Gemini API key powers the AI assistance (co-pilot prompts, storyboard and remix agents, sting review); a Mosaic API key renders motion-graphics clips. Transcription, editing, and publishing need no key."
5. Curator workspace target: change the displayed DEFAULT name "deepdive-workspace" → "mdingest-workspace" — the tab button label (:1740), the target label default (:1759), the JS fallback (:3868), the empty-state text (:3871), and the server-side default in `run_curator.py` wherever it is defined. A target name already stored in a workspace's settings or plan data keeps working and keeps displaying — only the default changes. The browser window-target string `deepdive-workspace` (the `target=` attributes and the `window.open` call) is internal (G4) and does NOT change.
6. Tooltips: "ACTIVE MASTER for deepDive / shutri.com (synced to dd_hub/manims)" → "ACTIVE MASTER for the published book (synced to dd_hub/manims)", and the same replacement in the mosaics variant (:6379). The remainder of each tooltip is unchanged.

**Verify:** the landing page source contains "mdIngest Workspace", the new subtitle, the new label, and the note text; `grep -n "deepdive-workspace"` in curator.html → every remaining hit is a window-target attribute or usage (list them in the report); the two old tooltip strings → zero hits; landing and curator pages load with HTTP 200.

## B3 — deepDive README: stop presenting DDMA as a separate project; stop linking the archived repo

**Where:** `deepDive/README.md` — the section heading (:9), the DDMA bullet (:14), the reels sentence (:26), the bug-tracker sentence (:34).

**Finding:** the README still describes the old three-repo landscape: it links "DDMA" to the standalone ddma repository, which is archived, and lists DDMA as a separate project. DDMA is now Cutroom, the extension inside mdIngest.

**Fix:**

- :9 — "## Creation: mdIngest + DDMA" → "## Creation: mdIngest + Cutroom".
- :14 — replace the DDMA bullet with: "* **[Cutroom](https://github.com/ashutoshmjain/mdIngest/tree/master/ddma)** — the media extension inside mdIngest: cuts the podcast into fully editable clips, uses Mosaic for motion graphics, and finally compiles the clips into longform video."
- :26 — "The reels created by DDMA" → "The reels created by Cutroom".
- :34 — "Bugs and fixes for deepDive, DDMA, mdIngest, and the portfolio app" → "Bugs and fixes for deepDive, mdIngest, and the portfolio app".

Nothing else in the README changes.

**Verify:** `grep -n "ashutoshmjain/ddma"` in deepDive/README.md → zero; `grep -n "DDMA"` → zero.

## B4 — mdIngest README: the intro bullets lead with the landing page and carry no server addresses

**Where:** `mdIngest/README.md` — the three "what you do" bullets (:9–11) and the extension sentence in the Installation section (:13).

**Finding:** the bullets open with the two content flows and only then mention where the user starts; two of them carry raw `http://localhost:8088…` addresses, which are overload for a first reader (the addresses live in the setup steps, where they are actionable). The extension is also still named DDMA (:13).

**Fix:** replace the three bullets with exactly these, in this order:

- **You start at the landing page** — the drop point for new inputs and the launcher for the Cockpit, Cutroom, and Beats Studio.
- **You bring raw research → you finesse it into a polished web page.** The Cockpit is where you shape your drafts and episodes and publish them as an article on the site.
- **You bring a raw conversation (audio) → you finesse it into a podcast-quality stream.** It gets transcribed once, at the word level, and that one transcription drives everything — the article, the clips, the longform. Nothing ever re-transcribes it.

And :13 — "DDMA is the extension inside this repo" → "Cutroom is the extension inside this repo" (the rest of the sentence, including the `ddma/` folder reference, is unchanged).

**Verify:** the bullets match the text above, in that order; no "localhost" appears in them; the setup steps and the launch note keep their addresses untouched.

## B5 — One requirements file, and the install prompt rewritten

**Where:** `mdIngest/README.md` (the whole setup-prompt block: the preamble, the two guidance paragraphs, and steps 1–13), new repo-root `requirements.txt`, `ingest/requirements.txt` and `ddma/requirements.txt` (both deleted), `ingest/README.md` (:13).

**Finding:** the prompt predates the merge — it names two products, offers the agent a venv-or-system-wide choice, carries a global sudo paragraph, assumes a fork can be made without tooling, installs two requirements lists, and creates a settings file during install, before the user knows what the API keys are for. The two requirements lists overlap with identical pins, so one root list is a clean union (Manim is already pinned in the ddma list).

**Fix, part 1 — the requirements merge.** Create repo-root `requirements.txt` with exactly this content:

```
# mdIngest + Cutroom — one list for the whole app (cockpit, transcription, clips, Manim).
faster-whisper==1.2.1
av==19.0.2
openai-whisper
numpy
requests
typer
pillow
google-generativeai
pyyaml
manim==0.22.0
```

Delete `ingest/requirements.txt` and `ddma/requirements.txt`. In `ingest/README.md`, replace `pip install -r requirements.txt` with `pip install -r ../requirements.txt`.

**Fix, part 2 — the prompt.** Replace the entire setup-prompt block in `mdIngest/README.md` with exactly this text:

---

Please set up and verify the complete publishing environment (mdIngest) in this workspace. Do every step below in order. Do not skip a step. If a step fails, fix it and continue — do not stop and ask unless a step explicitly says to ask.

Use the Python virtual environment at `.venv` in the repo root for every Python command below. If a step needs sudo (only a Linux package install can), do not run sudo yourself: open a new terminal, ask the user to authenticate there, and run the install command in that terminal.

1. Verify the toolchain: Python 3.10+, Cargo/Rust, mdbook (v0.5.0+), mdbook-katex, and the GitHub CLI (`gh`) are installed and on PATH, and `gh auth status` shows an authenticated account. If mdbook or mdbook-katex are missing, install them via `cargo install mdbook mdbook-katex`. If `gh` is missing or unauthenticated, ask the user to install it and sign in before continuing.
2. Fork mdIngest and clone your fork into this workspace: `gh repo fork ashutoshmjain/mdIngest --clone`. All paths below are relative to the repo root.
3. Create the virtual environment if it does not exist (`python -m venv .venv`), activate it, and install the Python packages from the repo root: `pip install -r requirements.txt`. This one list covers the cockpit server, transcription, Cutroom, and Manim. (On Debian/Ubuntu, if venv creation fails because the venv package is missing, install it using the sudo-terminal pattern above.)
4. Verify ffmpeg is installed and on PATH (`ffmpeg -version`). If it is missing, install it (Windows: `winget install ffmpeg` or `choco install ffmpeg`; macOS: `brew install ffmpeg`; Linux: `apt install ffmpeg` or the distro equivalent, using the sudo-terminal pattern). The pipeline cannot compile audio or video without ffmpeg.
5. Build the md-publish preprocessor binary from the repo root using `cargo build --release` (the manifest is the repo-root `Cargo.toml`; the binary source is `crate/src/main.rs` — do NOT run the build inside `crate/`, there is no manifest there).
6. Verify the built binary exists at `target/release/md-publish`. The book infrastructure ships configured in the repo-root `book.toml` (full katex + ingest preprocessor sections, theme) — do NOT run `mdbook init` in this repo: it overwrites `book.toml` with a minimal stub and wipes that configuration. If it happens, recover with `git checkout -- book.toml`.
7. Set up the workspace folder. Ask the user for a path to a local folder to be the workspace — call it the dd root hub (`DD_HUB_ROOT`). This is where all episodes, audio, plans, and settings live. Create the folder if it does not exist, then create the folder structure inside it if any are missing: `episodes/`, `vault/`, `inputs/`, `audio/`, `video/`, `mosaics/`, `manims/`, `rules/`. Set the `DD_HUB_ROOT` environment variable to that path and persist it (shell profile, systemd unit, or Docker entrypoint) so it survives new shells. The app only does local file I/O against this path. If the user wants the workspace backed up and shared across machines, they can sync this folder with Google Drive (Drive for Desktop on Windows/Mac; rclone on Linux/WSL/Docker) or any other sync tool they prefer — that choice is theirs, and the app does not need it to run.
8. Settings: if the user already has a `settings.json` in an existing workspace folder, copy that file into the new workspace folder's `vault/` instead of creating one. Otherwise skip settings entirely — the user adds API keys later, inside the app, once they know what each key unlocks (the landing page explains them). Never commit settings.json.
9. Launch the mdIngest Publishing Cockpit server (`python ingest/server.py` from the repo root, using the venv) on http://localhost:8088 and verify that http://localhost:3000 is accessible via `mdbook serve`.
10. Launch the Cutroom Clip Studio (Curator) server: from the repo-root `ddma/` folder, run `python scratch/run_curator.py` using the venv, and verify http://localhost:8000/curator.html loads.
11. Launch Beats Studio from the mdIngest landing page (http://localhost:8088/, the "Launch Beats Studio" button) and verify http://localhost:8001 responds.
12. Verify: `DD_HUB_ROOT` resolves, the workspace folder structure exists, `episodes/<N>/plan.json` is readable for an existing episode (or the workspace folder is empty for a fresh workspace), and all three servers respond (cockpit :8088, Curator :8000, Beats :8001).

---

**Verify:** (1) Create a scratch virtual environment and run `pip install -r requirements.txt` against the new root file — it installs cleanly, end to end. (2) `grep -rn "ingest/requirements.txt\|ddma/requirements.txt"` across both repos → zero. (3) The README's setup-prompt block matches the supplied text exactly. (4) `grep -n "DDMA"` in `mdIngest/README.md` → zero. (5) Using the merged install and the venv, the four servers start and respond: cockpit :8088, mdbook :3000, Curator :8000, Beats :8001 (HTTP 200 each).

## Execution summary

Executed locally by agy (Antigravity CLI, Hydrogen medium) on 2026-11-19 in the WSL clones of `deepDive` and `mdIngest`. B1–B5 all PASS, and the B6 addendum (fixes (a)–(e)) all PASS. All guardrails held throughout: out-of-scope findings were reported rather than patched, and no commits or pushes occurred until the fan-out was separately authorized.

The changes fanned out as `deepDive` `fab3e3a0` and `mdIngest` `1833951` with `scripts/check_fanout.py` exiting green. Brownie's remote verification passed (zero remaining hits for the old Cutroom name, both READMEs, the merged `requirements.txt`, `ep248` parity, and 6/6 byte-identical spot-checks), and Issues 102–108 were closed.

Follow-ons spawned from this batch:
- First clean-room run of `ingest/tests/cockpit_e2e.js` (7 pass / 11 fixture failures), documented as the Tier-1 baseline in `TESTING.md` (`deepDive` `60367837` / `mdIngest` `c1256868`).
- Issue 109 (the one stale test assertion in `Context-Aware Right Studio Deck Synchronization`), assigned to the Windows side.
