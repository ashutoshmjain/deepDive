# Spec B1 — Beats Studio repo hygiene (URGENT — implementation)

**Executor:** agy (Antigravity CLI) on the WSL clones of `deepDive` and
`mdIngest`, under the two-repo fan-out protocol.
**Why urgent (user decision, 2026-11-20):** a new user must never be left
with a dirty clone and a cleanup chore just for opening Beats Studio. This
fix therefore runs BEFORE the new-user test, not after it. The broader
Beats Studio design (personal beats, layout, template cache, proving run)
stays in Spec B — design-only; it executes in the same engagement, after
this spec, and the new-user test follows both. This spec is the narrow
hygiene fix only.

## The problem (observed live, 2026-11-20, Windows workbench)

1. **A plain episode load rewrites 23 tracked files.** Loading episode 248
   in Beats Studio re-materialized 248's beat meta into the flat
   `ddma/archetypes/clip_XX_meta.json` files, overwriting a different
   episode's data that was committed there. The flat folder is one shared
   scratch slot for all episodes, it lives inside the tracked repo, and
   the read path writes into it.
2. **Plan saves are not byte-stable.** The working plan copies
   (`ddma/projects/<ep>/plan.json`, `ddma/plan.json`, `ddma/docs/plan.json`)
   are re-serialized on save with number-format churn (0.0 → 0), so even a
   no-op session produces diffs; and these copies are the only record of a
   clip's production state (locks, Mosaic run IDs, publish flags).
3. **Beats Studio's navigation links are dead** because the Beats server
   serves no static files (details in Spec B's first addendum).

## Required outcomes

- **O1 — Read-path purity.** No GET in the Beats path writes any file
  inside the repo tree. The timeline index, beat lists, previews, and
  video serving are reads and must behave like reads.
- **O2 — Per-episode scratch outside the tracked tree.** The beat meta
  (and any regenerated scene code) that the studio materializes for an
  episode goes to a per-episode location under the workspace:
  `DD_HUB_ROOT/episodes/<ep>/beats/`. If the workspace root is
  unavailable, fall back to a git-ignored local cache directory (add the
  ignore rule in both repos) — never the tracked flat folder. The flat
  `ddma/archetypes/` folder and `ddma/generated_archetypes.json` become
  read-only reference material at runtime: shipped starter content, never
  written by the studio.
- **O3 — Byte-stable plan saves.** Loading and re-saving a plan copy with
  no semantic change produces an empty git diff. Find the writer(s) that
  re-serialize the ddma working plan copies, and normalize number
  serialization there (whole-number floats must round-trip as written).
- **O4 — Working navigation.** The Beats server serves the static assets
  its own page needs — a narrow whitelist (at minimum
  `workspace-link.js`), not a general file server. The Workspace and
  cockpit anchors then resolve as they do on other pages. Remove the
  Docs link (its target is retired and not shipped). The Curator link
  uses the workspace-link mechanism and is labelled "Cutroom".

## Known code sites (verify before editing; report any contradiction)

- `ddma/beats_server.py` — `do_GET` serves only `/`, `/beats.html`, and
  `/api/beats/*`; everything else 404s. The index route calls
  `archetype_studio.get_longform_timeline_index(ep)`.
- `ddma/archetype_studio.py` — `ARCHETYPES_DIR` anchors to the flat
  `ddma/archetypes/` folder (~line 14). Beat-meta materialization and
  `update_single_scene_with_ai` (scene-class rewrite + clip meta update)
  write under that anchor. Meta files reference their scene code by a
  `py_file` path — trace how that path is resolved at compile/render time
  before moving anything, and keep beat preview compilation working from
  the new location.
- `ddma/beats.html` — nav anchors at lines 30–33; `workspace-link.js`
  requested at line 633. The script already exists at
  `ddma/workspace-link.js` and `ingest/workspace-link.js`.

## Guardrails

- **Fan-out discipline:** every change lands in deepDive and mdIngest,
  byte-identical in the mirrored scope; `python scripts/check_fanout.py`
  exits 0 before any push; pre-push gate (no binary media, no
  `settings.json`).
- **Scope:** no layout redesign, no personal beats, no changes to the
  content of `generated_archetypes.json`, no changes to episode data in
  the workspace. Production writes that remain (a deliberate beat edit)
  go to the O2 location and are the only writes allowed.
- **Premise check:** grep the Beats path for file writes before editing.
  If the write sites are materially more entangled than described above,
  STOP, report the map of write sites you found, and do not improvise a
  larger surgery.

## Acceptance tests (all must pass; report each)

1. In the WSL deepDive clone: start the Beats server; load episode 248's
   timeline index; fetch one clip's beats; fetch one beat preview.
   Afterwards `git status --porcelain` shows **no modifications** in the
   clone, and the materialized beat meta exists under the workspace's
   `episodes/248/beats/` (or the ignored fallback) instead.
2. A deliberate beat edit still works end to end (directive → recompiled
   preview), with its writes confined to the O2 location.
3. Load and re-save the episode 249 plan copy unedited: `git diff` for
   that file is empty.
4. `GET /workspace-link.js` on the Beats port returns 200; the Beats page
   renders its Workspace anchor with a resolved href.
5. In the mdIngest clone: the Beats server starts, the page loads, and
   `git status --porcelain` stays clean through the same read sequence
   (using any episode available there, or the index error path if none —
   report which).
6. Fan-out checker exits 0; the e2e suite's Tier-1 baseline is unchanged
   (no new failures beyond the known fixture absences).

## Report format

Per outcome (O1–O4) and per acceptance test: PASS / FAIL / STOPPED, with
the evidence named above (git status output, file locations, checker
result, commit hashes for both repos). End with anything left waiting on
a decision.
