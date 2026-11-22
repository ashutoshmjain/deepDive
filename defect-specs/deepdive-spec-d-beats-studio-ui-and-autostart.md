# Spec D — Beats Studio UI pass and Workspace auto-start

Implements the findings of a manual test session on the Beats
Studio build that landed the two-surface design (one-tab
navigation, episode dropdown, entry rules, the master-span player,
scene integrity). Read those behaviours as given; this spec changes
only what it names. Where this spec touches the studio, the file is
`ddma/beats.html` unless another file is named.

## Rules of engagement

- Work in the WSL clones of deepDive and mdIngest. Every code file
  touched here is mirrored: after each phase, run the fan-out check
  and mirror every change to mdIngest in the same commit chain.
  Commit locally per phase in each repo. After the final phase's
  Verify passes, push both repos.
- **No automated engine runs.** No real Mosaic or Manim generation
  in any test, ever. Engine-facing endpoints are stubbed at the HTTP
  boundary (a fake Curator on :8000) or bypassed with fixture media.
  Starting the application's own servers in a test is allowed;
  generating media is not.
- No test, fixture, or verification step writes settings, real plan
  files, or media into either repo tree. Fixture episodes live in a
  throwaway hub root pointed to by the servers' environment.
- Each phase opens with its premise-check. On any STOP condition,
  stop that phase, report, and continue with the next phase only if
  it does not depend on the stopped one.

## Phase 1 — Starting the Workspace starts the suite (background, no tabs)

**Finding.** The application is four servers: Workspace/landing
(:8088, which also serves the cockpit), the book server (:3000),
Cutroom (:8000), and Beats Studio (:8001). A user cannot know which
to start, and starting them is a manual ritual: in the test session
only :8001 was up, so the cockpit link refused the connection and
the studio's Switch-to-Manim failed with "curator unreachable".
Starting the Workspace must bring the suite up with it — as
background processes only. **Auto-start opens no browser tabs and
no windows**; navigation stays user-initiated, in the same tab.

**Where.** `ingest/server.py` already holds the machinery: socket
probes `is_curator_running()` (:8000) and `is_beats_running()`
(:8001), a process handle with `is_mdserve_running()` /
`kill_mdserve()` and the `/api/mdserve` toggle for the book server,
and spawn sites for the Curator and Beats processes inside its
launch request handlers. The server starts at the bottom of the
file (`serve_forever()`). The Workspace page is
`ingest/landing.html`; its app tiles link to the four surfaces.

**Premise-check.** Read the two spawn handlers and the mdserve
toggle; record the exact spawn command per server and per platform
(Windows / Linux). Confirm the probes' semantics. If a spawn command
exists only inside a request handler, note how it will be reused at
startup without duplicating it.

**Fix.**

1. On landing-server startup (before `serve_forever()` begins
   accepting requests, or as its first action), probe :8000, :8001,
   and :3000. For each that is not already serving, spawn it using
   the existing spawn code for that server. **A server that is
   already running is left completely alone** — never restarted,
   never duplicated. A spawn failure is caught, logged to the
   landing server's console with the server's name and the error,
   and never prevents the landing server (or the other spawns) from
   starting.
2. The Workspace page shows each app's state — Running, Starting,
   or Failed — derived from the same probes (poll on an interval;
   a server still coming up reads Starting until its probe passes
   or a timeout marks it Failed). Clicking a tile whose app is
   Running navigates as today. Clicking a tile whose app is Failed
   retries that server's spawn via the existing launch path, then
   navigates when healthy. No state change ever opens a tab or a
   window.
3. The stop side is explicitly out of scope: this phase starts
   servers; it does not add stop controls.

**Verify.** Against a fixture hub: (1) with all ports free, start
only the landing server; within 15 seconds all four ports answer,
and the Workspace page shows every app Running; (2) start Beats
manually first, note its PID, then start the landing server — the
Beats PID is unchanged afterwards; (3) Puppeteer: loading the
Workspace page and waiting for all-Running opens no additional
pages (page count stays 1); (4) with the book server's binary made
unreachable for the fixture run (PATH manipulation in the test
shell only), the landing still starts, the Docs tile reads Failed,
and the other tiles read Running.

## Phase 2 — One toast system, bottom-right; header declutter

**Finding.** Studio messages render into `<span id="beats-toast">`
in the header bar (line ~34). A long message — the Switch-to-Manim
error naming the unreachable Curator, with its OS error text — is
squished unreadable into the header's right corner, exactly where a
user needs to read it. Two header elements are also pure noise: the
persistent engine-set confirmation text at the top right (the same
span), and the "RAM Cache" pill (`#lf-studio-mem-badge`), which
mislabels what it counts — it caches chapter data whether or not
the episode has any beats at all.

**Fix.**

1. Replace the header span with a floating toast container fixed to
   the **bottom-right** of the viewport, above the page content,
   minimum width 320px, wrapping long text. `showToast` appends a
   toast there; toasts auto-dismiss after a few seconds (errors
   stay longer), and stack if several fire. This follows the
   message pattern Cutroom already uses.
2. Delete `#lf-studio-mem-badge` and the code that updates it.
3. Nothing else in the header changes: the episode dropdown, the
   three surface links, and the layout stay.

**Verify.** Puppeteer with the Curator stubbed down: (1) clicking
Switch this clip to Manim produces a toast whose bounding box is in
the viewport's bottom-right quadrant, at least 320px wide, with the
full error text visible (no clipped overflow); (2) a set_engine
flip confirms through the same toast and the header contains no
`#beats-toast` element and no RAM-cache pill; (3) two rapid actions
stack two toasts; both dismiss.

## Phase 3 — The longform selection can only name an existing product

**Finding.** The "Use in longform: Mosaic | Manim" toggle calls
`/api/beats/set_engine` unconditionally. In the test session a clip
with a Mosaic render and no Manim product of any kind was flipped
to Manim, and the studio confirmed the set — leaving the longform
pointed at a source that does not exist. The selection is a pointer
to an *existing* product; a side with no product must not be
selectable.

**Where.** `ddma/beats.html`: the toggle buttons
(`#btn-engine-mosaic`, `#btn-engine-manim`) and `setClipEngine`.
The chapter data the page already loads carries `has_beats` per
chapter; the mappings in `ddma/archetype_studio.py` know whether a
Mosaic body resolves for the chapter.

**Fix.**

1. The timeline index passes one more per-chapter fact through:
   `has_mosaic` (a Mosaic body resolves for the chapter), alongside
   the existing `has_beats`.
2. For the active chapter: the Manim button is disabled when
   `has_beats` is false, with the hint "No Manim yet — switch this
   clip to Manim first" beside the toggle; the Mosaic button is
   disabled when `has_mosaic` is false, with the hint "No Mosaic
   render yet — render it in Cutroom". A disabled side renders
   visibly disabled and clicking it issues no request. The enabled
   side and the current selection display behave as today.

**Verify.** Fixture chapters — Mosaic-only, beats-only, both,
neither: (1) the disabled/hint state matches the fixture for each;
(2) clicking a disabled side sends no `set_engine` request and the
plan file is byte-identical afterwards; (3) `set_engine` on an
enabled side still flips the selection and the chapter button's
effective-selection label updates.

## Phase 4 — One retrigger path; equal-width span strip

**Finding.** Two identical actions share the screen: the header
strip's Mosaic Retrigger button (`#btn-beats-mosaic-retry`) and the
below-player panel's Retrigger Mosaic for a beats-less clip. One
screen, one path. Separately, the span strip sizes each segment by
its span duration (`flex: <spanDur>`), which makes the strip only
as honest as the span data — in the test session the final clip
(under 3 minutes) rendered wider than the rest of the episode
combined. The ruling: **all clips get equal width**; duration
sizing goes away entirely.

**Fix.**

1. Remove `#btn-beats-mosaic-retry` from the header strip. Confirm
   first that the panel's Retrigger Mosaic button calls the same
   handler (`beatsMosaicRetrigger`); it becomes the single path.
   The Patch button and everything else in the strip stay.
2. Span-strip segments render with equal flex (every segment the
   same width). Shading of the active span, click behaviour in both
   playback modes, and the beat ticks in Clip mode are unchanged.

**Verify.** (1) On a beats-less clip's screen, a DOM query finds
exactly one control that invokes the Mosaic retrigger handler, and
it still fires the (stubbed) retry request; (2) for a fixture
episode whose chapter durations vary by 10×, every strip segment's
computed flex-grow is identical, the active span is still the only
shaded one, and clicking a span still seeks/loads as before.

## Phase 5 — Collapsible side panes

**Finding.** The three-pane layout cannot fold: with the Muse
window beside the browser (split screen), the left clip list and
the right personal-beats pane squeeze the player until the centre
graphics cannot be judged at full density. The user needs the
player at full width on demand.

**Fix.** Add a collapse toggle to the left pane and to the right
pane (a small chevron control on each pane's inner edge, or in the
pane header). Collapsing a pane hides it entirely and the middle
pane takes the freed width; expanding restores it. Both panes may
be collapsed at once. The toggles remain reachable while collapsed
(a slim edge tab where the pane was). Collapse state is
session-only (page state; no persistence required).

**Verify.** Puppeteer at a 1000px-wide viewport: (1) collapsing the
left pane increases the player element's width by at least the
pane's former width minus the edge tab; (2) collapsing both panes
leaves the player within 5% of the full content width; (3)
expanding both restores the original three-pane widths; (4) the
clip list and personal-beats pane still function after an
expand/collapse cycle.

## Phase 6 — One theme: Beats Studio adopts Cutroom's theme

**Finding.** The two surfaces look like two alien applications.
Cutroom (`ddma/curator.html`) runs a theme system: a saved
preference (`localStorage` key `ddma-theme`, applied on load by its
`applyTheme`) driving CSS custom properties (its warm light
palette, `--bg-color: #fbf9f5`, among them). Beats Studio is
hard-coded dark slate throughout — dozens of distinct hex colours
across its stylesheet, inline styles, and some set from JavaScript
— with no theme layer at all. Direction: **Beats Studio adopts
Cutroom's theme system; Cutroom is not modified in any way.**

**Premise-check (STOP rule).** Inventory: (a) Cutroom's theme
tokens and their values per theme, and how `applyTheme` applies
them; (b) every distinct colour in `ddma/beats.html`, including
colours set from JavaScript (the span strip's segment backgrounds
are computed in JS). Produce the mapping table — Beats colour →
theme token — in the report. If the mapping is not mechanical for
at least 90% of occurrences, or a Beats colour has no token
counterpart and no obvious new-token home, **STOP** and report the
table before restyling anything.

**Fix.**

1. `ddma/beats.html` defines/uses the same theme custom properties
   as Cutroom and applies the saved `ddma-theme` preference on
   load, the same way Cutroom does — so one preference themes both
   surfaces identically. Hard-coded colours in the stylesheet and
   inline styles are replaced by the tokens per the mapping table;
   JavaScript-set colours read the same tokens (computed-style
   lookup or a JS mirror of the token values defined in one place).
2. Exempt by nature: the video element's black background, and
   purely semantic status colours (success green, error red) if
   Cutroom's tokens carry no counterpart — each exemption is listed
   in the report with its reason.
3. No layout, behaviour, or content changes in this phase; only
   colour sourcing. `ddma/curator.html` is untouched.

**Verify.** (1) With the theme preference set as Cutroom sets it,
the studio's computed body background and panel backgrounds equal
Cutroom's token values for that theme; switching the preference
and reloading re-themes the studio to match Cutroom's other theme;
(2) a grep inventory shows every pre-phase Beats colour either
replaced by a token or on the report's exemption list; (3) the
phase's diff for `ddma/curator.html` is empty, and the studio's
prior Verify behaviours (Phases 2–5) still pass in the new theme.

## Report

Per phase, in chat: premise results where a phase requires them,
files changed per repo, the fan-out check output, each Verify item
PASS/FAIL with the evidence (response codes, DOM assertions,
bounding boxes, before/after values), local commit hashes per repo,
and any divergence from this spec stated plainly with its reason.
End with `git status` from both clones after a full manual-style
session against a fixture hub: no writes outside the fixture hub
and the repos' own tracked files.
