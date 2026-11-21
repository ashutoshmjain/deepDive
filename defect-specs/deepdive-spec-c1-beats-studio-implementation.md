# Spec C1 — Beats Studio implementation

Implements the design in
`defect-specs/deepdive-spec-c-beats-studio-design.md` (referred to
below as "the design", by section). Read it first; where this spec
and the design differ in wording, the design's intent governs.

## Rules of engagement

- Work in the WSL clones of deepDive and mdIngest. Every code file
  touched here is mirrored: after each phase, run the fan-out check
  and mirror every change to mdIngest in the same commit chain.
  Commit locally per phase in each repo. After Phase 4's Verify
  passes, push both repos — a fresh-clone test of mdIngest follows
  in the same session and must include this work.
- **No automated engine runs.** No real Mosaic or Manim generation
  in any test, ever. Engine-facing endpoints are stubbed at the HTTP
  boundary (a fake Curator on :8000) or bypassed with fixture media.
  Engine runs happen only on a human's manual trigger outside this
  spec.
- No test, fixture, or verification step writes settings, real plan
  files, or media into either repo tree. Fixture episodes live in a
  throwaway hub root pointed to by the server's environment.
- Premise-checks (P0) come first. On any STOP condition, stop and
  report; do not improvise around a false premise.

## P0 — Premise-checks (report all four before Phase 1)

- **P0(a) The pre-cast horizontal form.** The design (§3.1) says
  clips are cast at production time in both a vertical and a
  horizontal form. Locate the per-clip horizontal artifact: start
  from GEMINI.md's staging rules and the clip-stitching document it
  points to, and from `archetype_studio.resolve_mosaic_body` and
  `beats_server.find_clip_media`. Report the exact path pattern of
  the horizontal per-clip file for each engine. If no per-clip
  horizontal artifact exists, **STOP** and report what does exist —
  Phase 3 depends on this answer.
- **P0(b) Writers of `visual_source`.** Grep both repos for every
  write of the plan's `visual_source` field. Classify each writer as
  *explicit selection* (a control whose purpose is choosing the
  longform source) or *production side-effect* (a render, retrigger,
  or compile path that also moves the field). Report the list.
- **P0(c) The storyboard casting site.** Locate where a clip's
  storyboard (its scene specs) is generated — the Gemini call whose
  output becomes the beats. Report the file and function. Phase 4
  adds a constraint at that site.
- **P0(d) Test-suite tripwires.** Grep the e2e suites for assertions
  on link `target` attributes, the beats header, or the episode
  input, and report any that Phases 1–2 would legitimately change.

## Phase 1 — One-tab navigation and the episode dropdown (design §5)

**Where.** `ddma/beats.html` (header, ~line 30), `ddma/curator.html`
(~line 1539), `ingest/cockpit.html` (~line 1550) each carry a
cross-surface anchor with `target="deepdive-workspace"`;
`ddma/workspace-link.js` and `ingest/workspace-link.js` document
that target in their usage comment. `ddma/beats.html` (~lines
23–27) holds the episode selector: a free-text `<input id="beats-ep">`
plus a Load button.

**Fix.**

1. Remove the `target="deepdive-workspace"` attribute from every
   cross-surface anchor (the three sites above and any other the
   grep finds). All Workspace / cockpit / Cutroom links across the
   four surfaces navigate in the same tab; browser Back/Forward is
   the return path. External links (`target="_blank"` to outside
   sites) are untouched. Update the usage comment in both copies of
   `workspace-link.js` to match (the files stay byte-identical).
2. Episode dropdown: add `GET /api/beats/episodes` to
   `ddma/beats_server.py`, returning the episode numbers that have a
   resolvable plan in the current workspace (hub-first, matching the
   plan resolution the server already uses), sorted ascending.
   Replace the text input with `<select id="beats-ep">` populated
   from that endpoint; changing the selection loads the episode (the
   existing `beatsLoad()` path). A `?ep=` deep link still preselects.
   If the endpoint fails, the select falls back to the current
   episode only — never a free-text field again.

**Verify.** Puppeteer against the Beats server with a fixture hub
holding two episodes: (1) clicking Workspace, cockpit, and Cutroom
from the studio never opens a second page (page count stays 1) and
Back returns to the studio; (2) the dropdown lists exactly the
fixture episodes; (3) selecting the other episode loads its
chapters; (4) `?ep=<n>` preselects. `git grep` shows no remaining
`target="deepdive-workspace"` outside documentation of this change.

## Phase 2 — Entry rules, engine surfaces, selection discipline (design §2, §3.2, §7)

**Where.** `ddma/archetype_studio.py`:
`get_longform_all_chapter_mappings` already computes per-chapter
`visual_source` and `mosaic_body` and a `locked` flag derived from
the selection; `get_longform_timeline_index` serves it to
`ddma/beats.html`, whose chapter buttons (~line 292) open every
chapter, whose beat editor disables itself for Mosaic-selected
chapters with strings directing the user to Cutroom (~lines
409/417/423), and whose engine buttons call
`/api/beats/set_engine`. In `ddma/beats_server.py`,
`/api/beats/manim_retrigger` (~line 441) first calls
`set_clip_visual_source(ep, clip_num, "manim")` and only then
forwards the generation request — a production action moving the
selection, which the design (§7) forbids: the selection is manual,
full stop.

**Fix.**

1. **Chapter facts.** In the mappings, add per chapter:
   `has_beats` (the chapter has a storyboard working set),
   `openable` (a Mosaic body resolves, or clip media resolves, or
   the chapter has beats with at least one rendered preview), and
   `published` (the plan clip's published flag). The timeline index
   passes all three through.
2. **Greyed, not gone.** Chapter buttons for non-openable clips
   render greyed and non-clickable, with a tooltip: not rendered
   yet — render it in Cutroom. Published chapters carry a visible
   "Published" marker and stay fully openable.
3. **Episode empty state.** When an episode has zero openable
   chapters, the workspace grid is replaced by a single panel:
   "No clips rendered. Go to Cutroom!" with a same-tab Cutroom link.
4. **Surface by existence, not selection.** The scene-editor block
   renders only when `has_beats` is true — whatever the selection
   says. For a clip with a Mosaic body and no beats, the middle pane
   below the player shows exactly two actions: **Retrigger Mosaic**
   (the existing `/api/beats/mosaic_retry` flow) and **Switch this
   clip to Manim** (creates the storyboard working set via the
   existing generation forward, then reveals the editor). Delete the
   selection-derived disabling and the three "set Manim as Active
   Master in Cutroom" strings; the `locked` mapping value may remain
   for the compositor but no longer gates the studio UI.
5. **Selection discipline.** `/api/beats/manim_retrigger` no longer
   writes `visual_source` — it only forwards the generation request.
   Every other production side-effect writer found in P0(b) loses
   its write the same way; explicit selection controls keep theirs.
   `/api/beats/set_engine` remains the studio's one selection
   writer. The engine toggle is labelled as what it is — "Use in
   longform: Mosaic | Manim" — and the chapter button keeps showing
   the effective selection (today's "Mosaic Master"/"Manim Master").

**Verify.** Fixture episode with four clips — Mosaic-only,
beats-with-Mosaic-selected, unrendered, published: (1) the index
flags match the fixtures; (2) Puppeteer: the unrendered row is
greyed and clicking it changes nothing; the Mosaic-only clip shows
the player plus exactly two actions and no editor DOM; the
beats-with-Mosaic-selected clip shows the full editor; the
published clip opens normally with its marker; (3) a zero-openable
fixture episode shows the empty-state panel; (4) with the Curator
stubbed, calling `/api/beats/manim_retrigger` forwards the request
and the plan's `visual_source` is byte-identical afterwards;
`/api/beats/set_engine` still flips it.

## Phase 3 — The player (design §3.1)

**Where.** `ddma/beats.html`: the player element (~line 77) is
already a 16/9 horizontal frame; `lfPlaybackMode` defaults to
`'master'` (~line 187); `applyPlaybackSource` points Clip mode at
`/api/beats/clip_media`, served by `beats_server.find_clip_media`
(~line 100), whose candidate list contains only vertical/square
clip files and an audio fallback — no horizontal form.

**Fix.**

1. `find_clip_media` resolves the pre-cast horizontal artifact
   located in P0(a) ahead of the existing candidates. (If P0(a)
   found the horizontal form among the existing names, this is an
   ordering change plus the geometry assertion in Verify.)
2. Selecting a chapter starts in **Clip** mode when clip media
   resolves, else in Master mode with a visible hint that no clip
   render exists yet. The Master/Clip toggle stays; Master remains
   one click away at all times.
3. **Span shading.** Under the player, a timeline strip renders the
   episode's chapter spans (from the index's start/end values); in
   Master mode the active chapter's span is shaded and clicking a
   span seeks the master to its start. In Clip mode the strip shows
   the active clip's beat boundaries as ticks (from the chapter
   beats' offsets). Native video controls stay as they are.

**Verify.** Fixture horizontal files generated with ffmpeg
(1280×720, silent) at the P0(a) paths: (1) `/api/beats/clip_media`
returns 200 with the horizontal file for a rendered clip and 404
for an unrendered one; (2) Puppeteer: selecting a chapter sets the
player source to `clip_media` and the mode indicator to Clip; the
strip renders one span per chapter with exactly the active one
shaded; clicking another span in Master mode seeks within ±0.5s;
(3) an episode with no master disables Play Full per the design,
with its hint, while Clip mode still plays.

## Phase 4 — Scene integrity (design §3.4)

**Where.** `ddma/archetype_studio.py` already holds the mapped
word stream (`_load_mapped_longform_words`) and the chapter beats
(`get_longform_chapter_beats` via `map_clip_beats_to_longform`);
`/api/beats/beats` serves them to the editor. The casting site is
the one reported in P0(c).

**Fix.**

1. Add a boundary validator in `archetype_studio.py`: for a clip's
   beats against the episode's mapped words, a beat **violates**
   when its final word is not sentence-final — i.e. the next word
   in the stream continues the same sentence — or when a beat's
   span begins or ends inside a word's time span. Return per-beat
   `{index, ok, reason}`.
2. `/api/beats/beats` includes the flags as an additive field; the
   editor renders a visible "sentence split" marker on violating
   beats (list row and detail header). Clean beats render nothing
   extra. The marker is informational: it never blocks editing or
   saving.
3. At the casting site (P0(c)), the storyboard generation
   instruction gains the constraint in words: scene boundaries fall
   at sentence boundaries; a scene carries complete sentences; a
   sentence is never split across two scenes. Prompt text only —
   no generation runs under this spec.

**Verify.** Synthetic word streams, no engines: (1) a stream whose
sentence crosses a beat boundary flags exactly that beat; (2) a
clean stream flags none; (3) a beat ending inside a word's span
flags with the word reason; (4) Puppeteer with a seeded violating
fixture beat shows the marker in the editor, and a clean fixture
clip shows none.

## Report

Per phase, in chat: premise results (P0 once), files changed per
repo, the fan-out check output, each Verify item PASS/FAIL with the
evidence (response codes, DOM assertions, before/after field
values), local commit hashes per repo, and any divergence from this
spec stated plainly with its reason. End with `git status` from
both clones after a full manual-style session against a fixture
hub: no writes outside the fixture hub and the repos' own tracked
files.
