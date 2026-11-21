# Spec C — Beats Studio, the Longform Engineering Surface (DESIGN)

**Status:** Design document, written 2026-11-20 from the user's manual
testing session on Windows and the design discussion that followed it.
Design only — no code changes. An implementation spec is written
separately, after the user reviews this design.

**Relationship to earlier work:** Spec B1 (repo hygiene) and the Spec B
build (hub-canonical plan, personal beats, three-pane layout, per-clip
`visual_source`) are landed and verified. This design supersedes the
Spec B design's layout and player provisions where they conflict. The
Spec B rulings D1 (hub plan canonical), D2 (personal beats: right pane,
copy visual only), D4(b) (template cache split) and D6 (no automated
engine runs) stand. D3 (layout) and D5 (engine choice) are amended as
recorded here.

---

## 1. The two-app model

Cutroom and Beats Studio are two surfaces over the same clips:

- **Cutroom is where clips are born and published.** Clips are rendered
  there, judged there as standalones, and published there. Publishing
  exists only in Cutroom; the studio has no publish control.
- **Beats Studio is where rendered clips are engineered for the
  longform, beat by beat.** Its product is the horizontal YouTube
  longform. Everything it previews is previewed in horizontal form.
- **One beats source per clip.** A clip's beats live in the workspace
  (`episodes/<ep>/beats/`, per Spec B1) and are read and written by both
  apps. A beat edited in the studio is the same beat Cutroom sees; if a
  clip becomes publishable during studio engineering, it is published
  from Cutroom.

The production flow this design serves, in the user's words and order:
render all clips in Cutroom, one after another; watch them there;
publish the ones that stand alone (for Mosaic clips, most publishing
happens at this stage); then open the studio and engineer every clip
for the longform, beat by beat. On the Manim route, most publishing is
expected to need beats-level engineering first, so the studio sits
before publication for those clips, not after it.

## 2. Entry rules — rendered clips only

- The studio's left pane lists **every** clip of the episode, in order,
  each row showing its engine and its published state. The list is the
  episode map; it never hides a clip.
- Only a clip with a **rendered baseline** opens a workspace. A clip
  with no render is a greyed, non-openable row.
- An episode with no rendered clips shows an empty state — "No clips
  rendered. Go to Cutroom." — with a link to Cutroom (same tab, §5).
- **Published clips are not excluded.** A published clip can be opened
  and reworked in the studio like any other. There is no freeze:
  rework after publication is normal, especially on the Manim route.
  Republishing after rework is a deliberate Cutroom act, as all
  publishing is.

## 3. The middle pane — player first, then the engine's surface

Selecting an openable clip shows, top to bottom:

### 3.1 The video player (clip level, horizontal, with controls)

- The video is at **clip level** — Manim and Mosaic renders are
  per-clip artifacts, and the player honours that. There is no
  segment-level video.
- The player is a **horizontal** player. It shows how the clip plays
  out in the horizontal longform frame.
- Source for **Play Clip**: the clip's **pre-cast horizontal render**.
  Clips are cast at production time in both forms — vertical (the
  short) and horizontal (the longform chapter form), under the rules
  in GEMINI.md — so the studio never renders on demand and never
  waits: it plays the horizontal form that already exists. The
  master's span for the clip is the same chapter in context; that
  view is Play Full with the span shaded, below.
- A player toggle offers **Play Clip / Play Full**. Play Full plays the
  longform master; the current clip's span is shaded on the full
  timeline so the clip can be found in context. Play Full is disabled,
  with a hint, when no master exists. Play Clip is the working default.
- On a Manim clip, beat boundaries are marked on the clip timeline.

### 3.2 Below the player — exactly one surface, chosen by what exists

- **Clip with beats → the Scene Editor**, for the whole clip: the beat
  strip, the selected beat's detail, preview compiles, and the
  personal-beats copy-in from the right pane (Spec B D2: the copy
  carries the visual only; the target beat keeps its own text and
  timing). There is no segment level in the studio: segmentation
  belongs to Cutroom's casting (audio segments and music stings); the
  studio manages the whole clip's beats.
- **Clip with only a Mosaic render (no beats) → no scene editor.**
  Exactly two actions:
  **Retrigger Mosaic**, and **Switch this clip to Manim**. Switching
  creates the clip's storyboard working set and reveals the scene
  editor over it.
  A clip without beats never presents beats as an editable surface, and never
  presents an empty player or an empty editor: if something has no
  content, the surface says what is missing and what to do instead
  (compare §2's empty state).

### 3.3 The right pane — personal beats

Unchanged from Spec B D2: deliberately saved beats, filterable,
deepDive-only storage, copy-visual-only into the beat being edited.

### 3.4 Scene integrity

The studio exists to reach the scene level — that depth is what
holds a longform viewer's attention. A scene must be a real scene:

- A beat boundary never cuts a word.
- A beat boundary never splits a sentence across two beats, leaving
  half a thought hanging in the next beat. A beat carries complete
  sentences.

Storyboard casting validates its boundaries against the word-level
transcript (the one transcription made at the podcast stage) and
must not emit a violating boundary. If a violating boundary exists
in a clip's beats, the scene editor surfaces it as a defect to
repair; it is never presented as a normal state.

## 4. What the studio is not

- Not a publisher (no publish control anywhere in it).
- Not a renderer of first resort: first renders happen in Cutroom.
  (Retrigger and beat preview compiles are re-renders of existing
  work, and remain manual, per D6.)
- Not a segment editor: no segment list, no segment-level casting.
  Storyboard casting stays per clip, as built.

## 5. Navigation — the application lives in one tab

- **One-tab rule:** every link between the four surfaces — Workspace
  (landing), cockpit, Cutroom, Beats Studio — navigates in the **same
  browser tab**, regardless of which port serves the target. No
  `target` attributes that spawn a new tab or address a named tab.
  The user's back/forward buttons are the navigation model.
  This supersedes the earlier two-tab Workspace-link behaviour and
  the named-target reuse shipped in Spec B1; B1's working links stay,
  only their tab behaviour changes.
- **The studio's episode selector is a dropdown** of the workspace's
  episodes, not a free-text field with a Load button.

## 6. Data and invariants

- `visual_source` per clip is the longform's selection pointer
  (§7), read by the longform chapter mapping as built and shown in
  the studio as a selection control. The studio's §3.2 surface is
  chosen by whether the clip has beats, not by the selection.
- Beats, plan, and renders resolve through the workspace (hub) paths
  established in Spec B1 and the Spec B build; the studio adds no new
  storage.
- Acceptance testing stubs the engines (D6): no automated Manim or
  Mosaic runs. Engine behaviour is verified by the user's manual
  sessions.

## 7. Resolved — renders record themselves; `visual_source` is a selection

Two different facts were being conflated in one field. They are kept
separate:

- **Production facts — what exists.** Rendering is the act of compiling
  a video with an engine; it is a production event, never a viewing.
  A clip can hold both products at once: a Mosaic render (recorded by
  its `mosaic_run_id` in the plan) and Manim beats with their renders
  (in the workspace beats directory). Producing one never touches,
  replaces, or re-labels the other. Nothing is recorded when a render
  is merely viewed or previewed.
- **Selection — what the longform uses.** `visual_source` is a
  pointer, not a stamp: it names which existing source the longform
  chapter takes. Flipping it renders nothing and deletes nothing; it
  is the `set_engine` action. Rendering a clip with the other engine
  does **not** move the selection — the longform keeps the source it
  was pointed at until the user flips the pointer.

The user's scenario, walked through: render Mosaic (Mosaic render
exists; selection is Mosaic, the only product) → render Manim (Manim
beats and renders now also exist; the Mosaic render is untouched; the
selection is still Mosaic until flipped) → look at the Mosaic again
(a preview of an existing artifact; nothing is recorded, nothing
moves).

Consequences for the earlier sections: the §3.2 surface follows the
**existence of beats**, not the selection — a clip with beats offers
the scene editor whatever the selection says, and a clip with only a
Mosaic render offers the two Mosaic actions. The selection itself is
shown in the studio as a control (Use in longform: Mosaic | Manim),
because the studio is where the longform is engineered.

**The selection is manual, full stop.** No render, no beat edit, and
no product's existence ever moves it; only the user's explicit flip
does. Working through a clip's beats and then selecting Mosaic
anyway — accepting the Mosaic render as that clip's fate in the
longform — is a first-class outcome: the beats stay in the workspace,
unused by this longform, and the pointer can be flipped back at any
time. A longform freely mixes sources per clip: some chapters from
Mosaic renders, others from Manim, each by its own pointer. An unset
`visual_source` reads as the only product when exactly one exists,
and as `"mosaic"` when both exist (as built); the studio always
displays the effective selection, so an unset pointer is never a
silent surprise.

## 8. Acceptance sketch (for the implementation spec)

1. An episode with no rendered clips shows the §2 empty state; a
   mixed episode lists unrendered clips as greyed, non-openable rows.
2. A published clip opens and is reworkable; the studio exposes no
   publish control.
3. A Mosaic clip shows the player and exactly two actions; the scene
   editor's DOM is absent, not hidden.
4. A Manim clip shows the player and the scene editor; beat markers
   appear on the clip timeline; switching a Mosaic clip to Manim
   reveals the editor without leaving the page.
5. Play Clip plays the clip's pre-cast horizontal render; Play Full
   shades the clip's span and is disabled with a hint when no master
   exists.
6. Every header link across the four surfaces navigates in the same
   tab (no `target` attributes on cross-surface links).
7. The episode selector is a dropdown populated from the workspace.
8. A storyboard cast for a fixture clip produces no beat boundary
   inside a word or mid-sentence; a seeded violating boundary is
   flagged in the scene editor.

## 9. Explicitly out of scope

- Issue 112 (the local fallback synthesizer's `get_footer` /
  `get_footer_bar` mismatch) — a separate micro-spec.
- Issue 113 (Cutroom's premature Mosaic "ready" toast) — a separate
  micro-fix in Cutroom.
- Any change to Cutroom's rendering, casting, or publishing behaviour.
