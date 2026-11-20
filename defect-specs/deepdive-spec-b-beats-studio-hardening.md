# Spec B — Beats Studio Hardening (DESIGN ONLY — no code)

**Executor:** agy (Antigravity CLI) on the WSL clones.
**Deliverable:** ONE design document, committed to **deepDive only** at
`defect-specs/beats-studio-hardening-design.md`. No code changes anywhere. No
changes to mdIngest. No other commits.
**Sequencing:** this design runs only after the WSL new-user test (fresh
fork-clone, corrected install prompt) has passed. Implementation specs are
written later, separately, after the user reviews this design. Nothing in
this spec authorizes implementation.

## Background (self-contained)

The pipeline turns a 40–60 minute podcast episode into clips and longform
video. A **clip** is a transcript-delimited segment of the episode. A clip is
assembled from audio segments and music segments (recorded segments may come
later), and its visuals come from one of two engines:

- **Mosaic** (external API): polished abstract infographics. Right for short
  reels, where a viewer's first ~20 seconds go to placing attention, split
  across captions, the host strip, and the visuals — the punch lands and they
  swipe on.
- **Manim beats** (in-house): a clip is storyboarded into **beats** — scenes
  of roughly 7.5–15 seconds, each a small Manim scene class that *explains*
  one piece of the spoken content. In longform, the viewer's attention
  settles fully on the graphic; repeated abstract visuals become hard to
  watch, and the audience needs full representation of the content. Beats
  exist for that mode. Whether they are worth their cost at longform scale
  is an open question this design must help answer honestly — the whole
  beats direction may yet prove to be a pipe dream, and the design must
  include the exit ramp, not just the road.

Verified mechanics of the current system (re-verify against the code before
designing on them; cite file:line for every claim in the design):

- Transcription is local (faster-whisper), once per episode, word-level.
  The audio is never sent to Gemini; Gemini works from transcript text.
- Storyboarding is **one Gemini call per clip**: the clip's caption chunks
  and duration go in; 5–12 scene specs come out; the result is cached on
  the clip object.
- Scene code is **per beat, local-first**: a beat whose archetype matches
  the template cache (`ddma/generated_archetypes.json`, ~22 parameterized
  templates) is instantiated with no AI call; on a cache miss, a Gemini
  "JIT auto-coder" call generates the scene class and the result is cached.
- Beat editing exists: a producer directive rewrites ONE scene class
  (default beat duration 7.5s), recompiles that scene in seconds, and
  updates the clip's meta.
- Rendering and stitching are local. Beat renders are 740×740 at 15fps,
  kept in a local `media/` folder — regenerable intermediates, never in git.
- Generated scene files currently accumulate in a flat working folder
  (`ddma/archetypes/`) that each production overwrites; episode 248's
  bundle was archived to the workspace (`episodes/248/manim_bundle/`) and
  removed from both repos on 2026-11-20.

Decisions already made by the user (2026-11-20) — design within them, do
not re-open them:

1. The idea of a reusable beats library shipped to every user is dropped.
2. A beats library will **never** be part of mdIngest. mdIngest ships the
   capability (engine + Beats Studio) only.
3. Instead, the user can **deliberately save individual beats** into a
   personal beats list inside their own implementation (deepDive). Saved
   beats are the user's production material, not a shipped feature.
4. Episode 250 may be dedicated to proving (or disproving) the beats
   approach for longform.
5. Beats Studio layout direction: episode selector at top; clips in the
   left pane; the audio segment in the middle pane; beats editing and
   management below the audio segment; personal beats selection in the
   right pane; clip-level video playback to check flow.

## Design questions the document must answer

- **D1 — Storage map.** For each artifact type — engine code, Beats Studio
  UI, per-episode generated scene files + beat meta, the template cache,
  personal beats, rendered beat MP4s, the per-clip engine choice — state
  where it lives (deepDive / mdIngest / the dd_hub workspace under
  `episodes/<N>/` / local-only), what mirrors it, and the mechanism. In
  particular: how the engine should locate a per-episode bundle in the
  workspace instead of the flat working folder, and how personal beats are
  kept out of the mdIngest mirror (the fan-out checker enumerates its pairs
  from the mdIngest side — propose the exact mechanism and justify it).
- **D2 — Personal beats.** Define the save unit (a single scene class plus
  its beat meta: spoken text, target duration, archetype id, provenance —
  episode/clip/beat it came from — and a user title/tags). Define the save
  flow from Beats Studio, the browse flow, and the instantiate flow (into
  a clip's storyboard at a chosen position; what happens when the target
  clip's durations differ; how a saved beat interacts with the storyboard
  cache).
- **D3 — Beats Studio layout.** Realize the layout in decision 5 above:
  per pane, its contents, its actions, and the existing endpoints and code
  each pane maps to. Flag anything in the current UI the layout makes
  obsolete, and anything the layout needs that does not exist yet.
- **D4 — Template cache disposition (user decision required).** For
  `generated_archetypes.json`, present the options — (a) stays mirrored in
  both repos as today, (b) deepDive-only, with mdIngest shipping an empty
  cache, (c) mdIngest ships a small generic starter set — with trade-offs
  and a recommendation. The decision itself is the user's; the design
  presents it, it does not settle it.
- **D5 — Per-clip engine choice.** Design the `engine: mosaic | manim`
  choice on the clip's plan entry: who sets it, the default, and the
  retrigger path — a clip produced with Mosaic can later be re-produced
  with Manim through the same code path if the Mosaic treatment proves too
  coarse in longform. State how longform assembly consumes the choice.
- **D6 — Episode 250 proving run.** Entry criteria, the run's shape (how
  many clips, what mix of engines), and exit criteria split into WORTH IT
  vs NOT WORTH IT with observable measures: producer time per clip against
  the Mosaic baseline, an explanatory-quality judgement method, failure
  modes encountered. State the fallback if NOT WORTH IT (Mosaic-only
  longform stays the default; the beats code remains as-is with no further
  investment) with the same concreteness as the success path.
- **D7 — Risks and unknowns.** Include at least: Gemini cost and latency
  at longform scale; Manim render time; and read side-effects — a Beats
  Studio read is known to rewrite archetype meta flags, so the design must
  state how hardening makes reads side-effect-free as a general property,
  not a one-off fix.

## Deliverable format

The design document contains: (1) a decisions table — every D-item with a
recommendation, the alternatives considered, and what the user must decide;
(2) the D1 storage map as a table; (3) an implementation-spec outline —
the future specs this design would spawn, in dependency order, each scoped
in one line — so the user can approve the design and the spec sequence in
a single review.

## Guardrails

- **Design only.** Read-only code inspection is expected; no code, test, or
  config file is modified. The only file created is the design document.
- **Premise check.** If any statement in this spec's Background contradicts
  the code as you find it, STOP, report the contradiction with file:line
  evidence, and do not design on a false premise.
- **Commit discipline.** One commit, deepDive only, the design document
  only. Pre-push gate: no binary media, no `settings.json`. Do not touch
  mdIngest, the archived ddma repo, or the workspace (dd_hub).
- **Report.** On completion: the design document's path, its size, the
  commit hash, and a one-line-per-D-item summary of the recommendations,
  ending with the list of decisions the user must make.
