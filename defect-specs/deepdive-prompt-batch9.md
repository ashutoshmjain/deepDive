# deepdive-prompt-batch9.md

## Batch 9 — Merge ddma into mdIngest (one repo to fork), mdbook infrastructure in the template, Issue 6 publish remote, Issue 34 workspace paths

Ten items. Execute them in order (M10 last). Report PASS/FAIL per verify step, then STOP with a full summary.

Context for all items: the standalone `ddma` repo is being retired. Its CODE moves into the `mdIngest` repo as a `ddma/` folder, so mdIngest becomes the only repo a user forks: base app + ddma extension + mdbook infrastructure. The servers remain separate processes on the same ports (cockpit :8088, mdbook :3000, Curator :8000, Beats Studio :8001). No git history is carried over — this is a clean copy. The `ddma` repo is archived at the end.

---

## M1 — Copy the ddma code into mdIngest as `ddma/`

### Where

- Source: the standalone `ddma` repo (branch `main`), at its current head.
- Destination: a new top-level `ddma/` folder in the `mdIngest` repo, mirroring the layout deepDive already uses (`deepDive/ddma/`).

### Fix

1. Copy the ddma CODE into `mdIngest/ddma/`: the Curator (`curator.html`, `scratch/run_curator.py`), Beats Studio (`beats.html`, `beats_server.py`), `ddma.py`, the archetype/Manim pipeline (`archetype_studio.py`, `batch_archetype_pipeline.py`, `compile_all_archetypes.py`, `mosaic_runner.py`, `longform_video_engine.py`, `render_longform_parallel.py`, `combine_clips_demuxer.py`, `archetypes/`), `requirements.txt`, `workspace-link.js`, and the test files (excluding test-env, below).
2. EXCLUDE, without exception:
   - `docs/` — the published docs site and published episode content. It does not move.
   - `settings.json` — never copied, in any folder.
   - `scratch/test-env/` — contains a hardcoded credential in a test file. It must NOT be copied, in whole or in part.
   - Any seed episode data (`episodes.json`, `episodes/`, `plan.json` seed copies), any media files (`*.mp4`, `*.mp3`, `*.wav`), and any logs.
   - The ddma repo's own `README.md` and `LICENSE` — mdIngest's govern the merged repo.
3. After copying, grep the whole `mdIngest/ddma/` tree for `settings.json` files and for the test-env directory name — both must be absent.

### Verify

1. `mdIngest/ddma/` contains the Curator, Beats Studio, `ddma.py`, the pipeline scripts, and `requirements.txt`.
2. No `settings.json`, no `test-env`, no `docs/`, no media files anywhere under `mdIngest/ddma/`.
3. Report PASS/FAIL per verify step.

---

## M2 — Rename mdIngest `ui/` to `ingest/`

### Where

- `mdIngest/ui/` (server.py, cockpit.html, landing page, workspace-link.js, lightning-widget.js, requirements.txt, settings.template.json, start assets) and every reference to the `ui/` path: `start.sh`, the README 1-Prompt Setup text, and any code that builds a path containing `ui/`.
- deepDive already calls this folder `ingest/`; the merged mdIngest adopts `ingest/` so the upstream and the reference instance share one layout.

### Fix

1. Rename `mdIngest/ui/` to `mdIngest/ingest/`.
2. Update every internal reference from `ui/` to `ingest/` (start scripts, README text, code paths). No functional change beyond the rename.

### Verify

1. `mdIngest/ingest/server.py` exists; `mdIngest/ui/` no longer exists.
2. Grep finds no remaining `ui/server.py` or `ui/` path references in mdIngest code, scripts, or README (historical prose mentions are acceptable only if they cannot be mistaken for a current path).
3. Report PASS/FAIL per verify step.

---

## M3 — Bring mdIngest's book up to the full pipeline configuration

### Where

- The mdIngest repo root. Current state (verified): mdIngest ALREADY has `book.toml` and a `src/` starter book, but its `book.toml` is a minimal stub (title + language only — no preprocessors, no `[output.html]`, deliberately plain), it has NO `theme/` folder, and NO `src/ddma/` scaffold.
- deepDive's `book.toml` is the full production configuration (katex + ingest preprocessors, `theme = "theme"`, custom CSS, fold/print settings) — but it carries user-specific values (personal machine paths in `[preprocessor.ingest]`, a personal lightning address and podcast links, a personal cname and git-repository-url). Those values must become placeholders in the template, never copied as-is.

### Fix

1. Upgrade mdIngest's `book.toml` to the deepDive STRUCTURE: `[build]`, `[preprocessor.katex]`, `[preprocessor.ingest]`, and `[output.html]` sections as in deepDive — with every user-specific value replaced by an obvious placeholder (book title, authors, `downloads_path`, `video_source`, `lightning_address`, `podcast_html`, `git-repository-url`, `cname`).
2. Add `theme/` (including `theme/book.js` and `theme/custom.css`), copied from deepDive's theme.
3. Add the `src/ddma/docs/` scaffold: an `episodes.json` containing an empty list, and an empty `episodes/` directory (keep it with a `.gitkeep` if needed). This is where the Curator publishes clips.
4. Keep mdIngest's existing `src/` starter chapters as they are — do NOT import any deepDive episode markdown or content.
5. The result: a fresh clone of mdIngest builds with mdbook and serves its book with the full pipeline configuration, and the Curator can publish a first clip into `src/ddma/docs/` with no manual setup and NO `mdbook init` step (see M7 — init must never be run against this repo; it overwrites `book.toml` with a stub).

### Verify

1. `mdbook build` succeeds in a clean mdIngest clone and produces a book.
2. `src/` contains no episode content (grep for a known episode number/title from deepDive finds nothing).
3. `src/ddma/docs/episodes.json` is an empty list.
4. Report PASS/FAIL per verify step.

---

## M4 — Make the merged repo the one runtime home

### Where

- mdIngest: `start.sh`, `ingest/server.py`, `ddma/scratch/run_curator.py` (the `/api/cockpit/launch` endpoint added in Batch 8 resolves the cockpit as `DDMA_DIR.parent / "ingest"`), `ddma/beats_server.py`, and the README 1-Prompt Setup.

### Fix

1. All four servers start from the merged mdIngest repo: cockpit from `ingest/server.py` (:8088), mdbook serve (:3000), Curator from `ddma/scratch/run_curator.py` (:8000), Beats Studio from `ddma/beats_server.py` (:8001, launched from the landing page as today).
2. `start.sh` reflects the merged layout (workspace mount check + the servers above), superseding the two-repo startup.
3. The `/api/cockpit/launch` resolution (`DDMA_DIR.parent / "ingest"`) must resolve correctly in the merged layout: `ddma/`'s parent is the repo root, and `ingest/server.py` exists there.
4. Nothing may reference the standalone ddma repo or a sibling ddma clone any more.

### Verify

1. From a clean mdIngest clone with a local workspace folder: all four endpoints answer (cockpit :8088, mdbook :3000, Curator :8000, Beats :8001 via the landing-page launch).
2. In the Curator, clicking Workspace with the cockpit down starts the cockpit and opens the landing page (the Batch 8 behaviour, now in the merged layout).
3. Grep finds no path that assumes a sibling ddma clone.
4. Report PASS/FAIL per verify step.

---

## M5 — Issue 34: ddma scripts take content locations from the workspace, not the repo layout

### Where

- `mdIngest/ddma/mosaic_runner.py`: `DOCS_PLAN_PATH` reads the episode plan from a hardcoded repo path (`<repo>/src/ddma/docs/episodes/<ep>/plan.json`), and the finished-master copy target is built from the same layout assumption.
- `mdIngest/ddma/batch_archetype_pipeline.py`: already guesses between two repo layouts for the episodes directory.

### Finding

The plan's canonical home is the workspace (`DD_HUB_ROOT/episodes/<ep>/plan.json`) — the Curator has read and written it there since the workspace became the primary store. Scripts that hunt for the plan inside a repo layout break whenever the layout differs.

### Fix

1. `mosaic_runner.py`: read the episode plan from the workspace, resolving the root with the same resolver the Curator uses (`resolve_dd_hub_root()` semantics: env `DD_HUB_ROOT` → settings `dd_hub_root` → local default). Keep writing finished masters to the repo's published clips folder (`src/ddma/docs/episodes/<ep>/clips/` relative to the repo root) — in the merged repo that layout is fixed and known.
2. `batch_archetype_pipeline.py`: replace the multi-layout guessing with the same two sources — plan/data from the workspace, published output to the repo's `src/ddma/docs/`.
3. Do not change what either script renders or which clips it processes.

### Verify

1. Grep: neither script builds a plan READ path from a repo layout; both resolve the workspace root.
2. A dry run of `mosaic_runner.py` against a test episode in a local workspace finds the plan (no file-not-found).
3. Report PASS/FAIL per verify step.

---

## M6 — Issue 6: publish remote is the fork's own remote, shown and editable in the cockpit

### Where

- `mdIngest/ingest/server.py` `/api/git/push` (git add `src/` + `book.toml`, commit, push, with `cwd=PROD_ROOT`) and the cockpit's right-hand side panel (`ingest/cockpit.html`, the PUBLISHING ACTIONS section under the PUBLISH button).

### Finding

In the merged repo, `PROD_ROOT` is simply the mdIngest repo root, and a user who forked mdIngest has `origin` pointing at their own fork — so PUBLISH already pushes to the right place for a fork user. What is missing is visibility: the user cannot see which remote PUBLISH will push to, nor change it without leaving the app.

### Fix

1. `/api/git/push` keeps its current behaviour and scope (`src/` + `book.toml`, cwd = repo root). No change to what is committed.
2. In the cockpit's right-hand panel, add a small "Publish remote" row in the PUBLISHING ACTIONS section: it shows the current `origin` URL of the repo (read via `git remote get-url origin`), and lets the user edit it and save (which runs `git remote set-url origin <url>`, or `git remote add origin <url>` when none exists). Validate the input is a non-empty URL-like string; show a clear error otherwise.
3. Add the backing endpoint(s) in `ingest/server.py` (GET the current origin, POST to set it), following the file's existing endpoint patterns.
4. Do NOT add any other remote-management UI. One row: current remote, edit, save.

### Verify

1. The right-hand panel shows the repo's actual origin URL.
2. Editing and saving updates `git remote get-url origin` to the new value; an invalid value is rejected with a clear message and the remote is unchanged.
3. PUBLISH still commits only `src/` + `book.toml` and pushes.
4. Report PASS/FAIL per verify step.

---

## M7 — README 1-Prompt Setup describes the one-repo flow

### Where

- `mdIngest/README.md` — the Installation (1-Prompt Setup) section and any text describing ddma as a separate install.

### Fix

1. The setup flow becomes: fork mdIngest (one repo), clone the fork, run the one prompt. Remove the ddma clone/install steps and any mdbook init step (the book ships configured, per M3).
2. The README must state plainly, near the setup: the book infrastructure is included — do NOT run `mdbook init` in this repo. (Verified behaviour of mdbook v0.5.3: init does not detect an existing book and does not stop; it overwrites `book.toml` with a minimal stub, wiping the theme/preprocessor/output configuration. If it happens, the recovery is `git checkout -- book.toml`.)
2. Describe ddma as what it now is: the extension inside the repo (`ddma/` folder) providing the Curator (Clip Studio) and Beats Studio, started by the same setup.
3. Keep the rest of the README's framing and structure unchanged (what the user does and gets, minimum configuration, state of the app).

### Verify

1. The README contains no instruction to clone a second repo and no mdbook init step.
2. The setup prompt's steps match the merged layout (paths under `ingest/` and `ddma/`).
3. Report PASS/FAIL per verify step.

---

## M8 — Archive the standalone ddma repo

### Where

- The standalone `ddma` repo (branch `main`).

### Fix

1. Replace the ddma repo's `README.md` with a short pointer: development has moved into the mdIngest repo (the `ddma/` folder there); this repo is archived. Commit and push that as the repo's final commit.
2. Archive the repo on GitHub. If the available tooling cannot archive a repo, report that as a remaining user step (GitHub repo Settings → Archive) instead of failing the item.

### Verify

1. The ddma repo's head commit is the pointer README.
2. The repo is archived, or the report names the manual archive step as outstanding.
3. Report PASS/FAIL per verify step.

---

## M9 — Re-sync deepDive from the merged mdIngest and extend the fan-out check

### Where

- deepDive's `ingest/` and `ddma/` folders (mirrors of the merged mdIngest) and the fan-out checker (`check_fanout.py`).

### Fix

1. Refresh deepDive's `ingest/` and `ddma/` copies from the merged mdIngest so the reference instance matches the new upstream exactly (code files only — deepDive's episode content, `src/`, and published clips are untouched).
2. Add the `workspace-link.js` pairs to `check_fanout.py` (it was noted as missing when Batch 8 landed) and update its pair list for the merged structure.

### Verify

1. `check_fanout.py` reports all pairs in sync, including `workspace-link.js`.
2. deepDive's episode content and published clips are byte-unchanged.
3. Report PASS/FAIL per verify step.

## M10 — Update GEMINI.md: agents stop fanning out to the standalone ddma repo

### Where

- `GEMINI.md` in deepDive (the "Primary Workbench & Fan-Out Push Invariant" section) and its mirrored copy in mdIngest. (The ddma repo carries no GEMINI.md.) This item executes LAST in the batch, after M1–M9 are complete.

### Finding

GEMINI.md currently instructs coding agents (Muse Code, Antigravity) to mirror `deepDive/ddma/` into the standalone `ddma` repo as one leg of a three-repo fan-out, and to push that repo as part of the protocol. After this batch there is no standalone ddma repo to fan out to — the ddma code lives in `mdIngest/ddma/` (mirrored from `deepDive/ddma/`). If GEMINI.md is not updated, future agent sessions will keep trying to fan out to an archived repo.

### Fix

1. Rewrite the fan-out protocol in GEMINI.md for the two-repo world:
   - Remove the `deepDive/ddma/ ⟶ ddma/` (standalone repo) mirroring step and its file list. The ddma code mirror becomes `deepDive/ddma/ ⟶ mdIngest/ddma/` (same relative paths), alongside the existing `deepDive/ingest/ ⟶ mdIngest/ingest/` leg.
   - Remove the standalone-ddma push step from the push order; the protocol now pushes deepDive and mdIngest only.
   - Update the repository-role descriptions: ddma is a folder inside both repos (the extension: Curator + Beats Studio), not a separate repository. The rule "never commit binary media or settings.json to the code repos" now applies to mdIngest (both its `ingest/` and `ddma/` parts) exactly as before.
   - Update the "keep all three repos in sync until a release candidate" phase rule to two repos (deepDive + mdIngest).
   - State explicitly, in the protocol section: "The standalone ddma repo is archived. Do NOT fan out to it, push to it, or clone it for setup."
2. Mirror the updated GEMINI.md to mdIngest so both copies are identical.
3. Do NOT rewrite unrelated GEMINI.md sections (publication rules, distribution rules, verification gates) beyond the references the merge makes stale.

### Verify

1. GEMINI.md contains no instruction to mirror, push, or commit to a standalone ddma repo, and contains the explicit archived-repo note.
2. The fan-out section lists exactly two mirror legs: `ingest/` and `ddma/`, both deepDive → mdIngest.
3. The deepDive and mdIngest copies of GEMINI.md are byte-identical.
4. Report PASS/FAIL per verify step, then STOP with a full summary.

---

## Guardrails

- Do NOT copy or commit any `settings.json`, API key, or credential into any repo. In particular, `scratch/test-env/` from the ddma repo is excluded entirely (M1).
- Do NOT move ddma's `docs/` content or any episode content/media into mdIngest.
- Do NOT change deepDive's episode content, published clips, or published plan copies, beyond the M9 code re-sync.
- The servers remain separate processes on their current ports. Do not merge server code.
- Do NOT change the per-clip Publish scope (clip + published plan copy + two manifests) or the cockpit PUBLISH scope (`src/` + `book.toml`).
- If a verify step is ambiguous, list the candidates and STOP — do not guess.
- Report PASS/FAIL per verify step, then STOP with a full summary.
