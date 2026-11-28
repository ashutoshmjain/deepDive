# Spec H2 — Composite assembler + Manim initial render in Beats Studio

Status: DRAFT (user review before posting). Builds on Spec H, which is already built and verified at the remotes. Spec H turned the 249 trial into app code: the rulebook, the push endpoint and button, the gate, the tests. This spec builds the piece Spec H never named: the assembler that turns the parts into the movie, and the button that starts the Manim side.

## Where

Beats Studio (`beats.html`, `beats_server.py`), one new assembler module, and the Spec H rulebook module already in the app. The fix touches deepDive and mdIngest (code only in mdIngest — the spec file stays deepDive-only, per the repo discipline).

## Finding

Beats Studio has every part of the longform and builds nothing. The Mosaic run artifacts are all present and healthy (all 21 clips of episode 249, resolved by run ID). The Spec H guards, the push button and the gate are in place. But the studio shows only per-clip Mosaic shorts and "No longform master yet": there is no step that stitches the parts into the 31-minute composite, and no button that starts the Manim side. The 249 regression proved it: design/render produced nothing (timeline 0 scenes), the push correctly refused with a 404, and no movie existed to compare against the prototype.

The gap is in the spec, not the builder. Spec H §6 says "Assemble is automatic. The master assembles itself from the finished clips (the combine is deterministic and already works)." That sentence described the old engine — the one that assembles the old-style longform — not the composite. Spec H never named the composite assembler as something to build, and never named the trial's build scripts as the reference implementation to port. This spec names both.

The trial's build scripts (the v6 frame scripts and the full-build script that produced the prototype) are the reference implementation for the assembler. They are supplied with the build prompt. The assembler must reproduce their behavior in the app, not invent a new one.

## 1. The frame contract — what is hard-coded, what can change

This is the organizing rule of the whole spec. The longform frame has two kinds of parts, and the build must keep them separate in code:

**Hard-coded style elements — changing them is a recode, never a retrigger.** These are fixed in the assembler, identical for every clip and every episode, exactly as the trial approved them:

1. **The host strip** — the top bar: "SATOSHA" — ONE blinking microphone in the center — "SATOSHI". Letterspaced caps, monochrome Mosaic style. One mic only, blinking (live indicator). Background pure black, the same as the rest of the screen — no visible band, no separation. Name geometry (measured on the approved sample): each name's center sits around the center of the graphic below it — SATOSHA above the left panel's center (x≈590 in the 1920 frame), SATOSHI above the right panel's center (x≈1330) — and the names sit vertically at the level of the microphone's base. The strip is a short seamless loop (the trial used a 3.0 s loop, 1920×120).
2. **The captions band** — below the host strip (below the microphones), centered, spanning both panels, in karaoke style: the current word highlighted yellow as it is spoken. A perceivable gap sits between the strip and the captions. Text sizes throughout (strip, captions, Manim title/formula/labels) are half the size of the early trial sample that was judged too big everywhere.
3. **The footer bar** — the bottom bar of the Mosaic graphics themselves: "Mosaic" left, "deepDive podcast" right, delimiter line above, drawn at the bottom of the frame by the composite in the Mosaic style. No invented copy anywhere in the frame.
4. **The pane geometry** — the middle band is 1480×740: left 740×740 Manim artifact + right 740×740 Mosaic render. The whole frame is fixed 1920×1080. The 340 px left over vertically hold the three bands (host strip, captions, footer).

**Changeable pane content — changing it is a retrigger, never a recode.** Only two things ever change, and only through the retrigger buttons in §4:

1. **The content inside the left pane** — the clip's Manim artifact (title, diagram or formula, stages). Changed by retriggering Manim for that clip.
2. **The content inside the right pane** — the clip's Mosaic run artifact. Changed by retriggering Mosaic for that clip.

Nothing else changes per clip. The frame, the strip, the captions band, the footer and the pane geometry never vary. A retrigger never touches duration — duration was decided in Cutroom and stays locked downstream — and never touches the hard-coded style elements.

## 2. The assembler (the missing piece)

Build one composite assembler module in the app. It takes, per clip, the two pane contents and produces the fixed frame:

- **Left pane:** the clip's ONE sustained Manim artifact (Spec H §3: one continuous timed scene spanning the full clip duration, stages at sentence boundaries, title first, at most one diagram or formula, formulas from the episode page only, reuse reported, kill rule stands). If the clip has no Manim artifact yet, the assembler reports the clip as not-ready — it never invents a left pane and never silently falls back to a Mosaic-only segment.
- **Right pane:** the clip's run-ID artifact `{ep}-{clip}-mosaic-{run_id}.mp4` (Spec H §2 and §5: the 1080×1080 body render, scaled exact 1080→740, NEVER cropped, NEVER the compiled clip). The assembler resolves the Mosaic side through the plan's `mosaic_run_id` and the hub's canonical copy — never through the job store (its entries are stale: missing for some clips, failed for others), never a generically-named body file with no run-ID provenance, never a fresh Mosaic run without the user's word. Audio is the run artifact's, unchanged. No intro/outro cards or stings in the longform.
- **Run freshness (the Cutroom-edit rule).** A clip's audio is edited in Cutroom all the time (a segment's start or end trimmed in the transcript pane; new audio segments or music stings added; an audio segment repeated from a previous clip). An edit saves the new segments to the plan and nothing else: the `mosaic_run_id` stays, and the Mosaic run file still holds the OLD audio — Mosaic only ever runs on the manual trigger, and the job record stores no fingerprint of the audio the run was built from, so nothing in the app can tell the run is stale. In practice the user retriggers Mosaic after every audio edit, so the run is fresh by discipline — and audio-segment changes are very rare (most retriggers are because a run's quality wasn't good, not because the audio changed) — so a stale run is a rare event; the check below is cheap insurance for the edit that happens without a retrigger. The assembler must therefore check freshness before using a run: the Mosaic run path records the audio signature (the segments hash) alongside the run ID when a run completes, and the assembler compares it against the clip's current segments. A mismatch is a reported exception — the clip's run is stale and needs a manual Mosaic retrigger — never a silent use of the old run. (The compiled short and its captions heal themselves on the next compile, because the compile path recomputes the signatures and re-cuts the audio and regenerates the captions when they mismatch; the Mosaic run has no such self-heal.)
- **Captions:** karaoke from the body-relative word timings (Spec H §4: the compiled caption chunks carry a +1.5 s offset and must NOT be used). Current word highlighted yellow, no gaps (word-tiling plus hold to duration), lines capped at ~40 characters, 1.5 line spacing by hard-placing each line (line tops 42 px apart at the trial's sizes — the rendering library ignores the LineSpacing style field), and the caption renderer sets the font size explicitly (a missing Fontsize field rendered captions dark red in the trial). Caption data is required for every clip: a clip with no caption data is a reported exception, never a silent static title band.
- **Timing — the golden rule: the clip's segments are ground zero.** Duration and audio for a clip are what is in Cutroom — not the base audio. More precisely: the clip's `segments` list (its audio segments and music stings, as built in Cutroom) is the ground truth. The clip's `start`/`end` (the span) and its `duration`, `audio_duration` and `rendered_duration` fields are derived bookkeeping and can go stale — the transcript-pane edit updates the segment's start/end/duration and the displayed clip duration (sum of segments minus crossfades) but nothing recomputes the clip's `start`/`end`, so the span is not adjusted automatically. The assembler must therefore build from the segments, never from the span or the duration fields. A clip may carry added audio segments, added music stings, or an audio segment repeated from a previous clip — the segments list is self-contained, so the assembler handles all of that by reading the segments as they stand. Mosaic runs are built from the clip, so the run artifact carries the Cutroom clip's duration and audio; the assembler uses it as the timing reference for both sides. Manim follows the same: the artifact's duration is the Cutroom clip's duration, and its stages are keyed to the sentences of the Cutroom clip's transcript — never to the base audio. The plan's duration fields are NOT the timing source.
- **Concat:** the per-clip composite segments are concatenated into the master. Concat joints must be clean — the trial's 1-tick DTS overlaps at the joints are a known cosmetic artifact to address, or explicitly accept and report.
- **Output:** the assembled master is a 1920×1080 movie in the episode's longform slot, and it feeds the existing push endpoint and gate (Spec H §8 and §9) unchanged. The assembler writes the master; it does not push it.

This supersedes one sentence of Spec H §6: "Assemble is automatic. The master assembles itself from the finished clips (the combine is deterministic and already works)." That sentence described the old engine. The composite assembler is built by this spec.

## 3. "Design artifacts" — the initial render of the Manim side

Beats Studio gets the button Spec H §6 named but never built: **"Design artifacts"**, per clip or per episode. It is the initial render of the Manim side pane — the base to start working with.

- One deliberate start. Nothing starts itself — transcription is never automatic and neither is this.
- The system fans out: one design call per clip, each designing that clip's ONE Manim artifact from that clip's transcript text (the Cutroom clip's transcript — the audio as cut, not the base audio) — never the whole transcript in one pass, never per beat. The user never sees or touches the individual calls.
- The renders run as queued background jobs, progress shown per clip, the screen free while they run. Outcome reporting per clip (designed/rendered, or FAILED with the reason) — the trial's Manim render silence is not repeated.
- The system reports only the exceptions: a short list of the clips whose artifacts failed or came out wrong. The ones that worked never ask for attention.

## 4. Retrigger — pause the video, fix one side, re-stitch

Beats Studio's longform preview plays the assembled master. The user watches it, pauses it manually at any point, and retriggers the side that needs fixing for that clip:

- **Retrigger Manim** — re-designs and re-renders only that clip's left pane (the Manim artifact). The right pane is untouched.
- **Retrigger Mosaic** — re-renders only that clip's right pane (the Mosaic run artifact). The left pane is untouched.

After either retrigger, the assembler re-stitches only that clip's composite segment and updates the master. A bad title never costs a Mosaic re-render; a bad Mosaic never costs a Manim re-render. Retrigger never touches duration and never touches the hard-coded style elements (§1). The master is re-gated (Spec H §9) before any push.

## 5. Small correction folded in

Spec H's re-run addendum says the oracle's SHA is "(SHA not recorded in evidence — unavailable)". That is wrong. The confirmed SHA-256 of `249-composite-full.mp4` is `752852DD7DAA98EA535570AAFF15CDDF66E2659BA911C30D6EBC783D87A3F67D` (93,749,687 B, container 1883.688688 s, video 1883.666992 s, audio 1883.688688 s, 1920×1080). Correct the addendum's SHA line to the confirmed hash.

## Guardrails

- Pull first (both clones), commit + push when done, push all / pull all — every push and every pull covers both clones. Plan and data files live only in deepDive; mdIngest is code-only.
- Never trigger Mosaic except on the manual UI trigger (the retrigger button) or the user's explicit instruction. Never start a Mosaic run to fill a gap the build found.
- Never substitute: never the compiled clip, never a generically-named body file with no run-ID provenance, never a fresh run without the user's word.
- Caption data is required for every clip; a missing one is a reported exception, never a silent fallback.
- The kill rule stands: if the Manim side needs per-beat design, or more than a third of the clips' artifacts need reprocessing, stop and report.
- Never edit a repo file outside this spec's work. Specs live in deepDive `defect-specs/`; this spec is self-contained and references no tracker, no workspace path, and no issue number in its fix text.

## Open question (spec-owner call, not decided here)

- **The other two duration numbers — resolved by inspection (2026-11-25).** They are three different things, which is why they disagree. (a) The plan's duration fields (sum 1735.84 s) live in the episode plan JSON, written by the plan builder when the clips are locked: for 17 of 21 clips the field equals the clip's audio span (`end - start`); for clips 0, 5, 6, 7 it is the audio span plus ~15.6 s of music/stings attached to that clip. It is the clip's nominal length for Cutroom/compile-clip, not the rendered file's length. (b) The Beats timeline index (total 3254.21 s = 54:14; e.g. clip 1: 269.39 s) is the OLD engine's map, not the composite's: it is computed by `get_longform_timeline_index`, and 3254.21 is a hardcoded fallback returned when no master video file exists on the machine — the chapter windows are the old engine's Manim beats mapped onto that assumed 54-minute master. It is what Beats Studio currently shows as the episode total. Once the assembler exists, the studio's timeline must come from the composite itself (31:24), not this index. (c) The run artifact's ~10.1 s tail — resolved (2026-11-25): it is the clip's music (11 s) minus the 1 s crossfade, baked into the run's audio. The plan records it: `audio_duration` is the run artifact's duration (clip 1: 120.72 vs the run file's 120.73), and `audio_duration` ≈ audio span + music − crossfades across all clips checked. No mystery left; the assembler uses the run file as-is.

## Verification

- **Sample first, hard stop.** Build the assembler, then run clips 249-0, 249-1 and 249-2 ONLY through design → render → assemble. Stop after those three clips. Report, then wait for the user's word before touching the rest. A clean sample is a review point, not permission to continue.
- **Full 249 regression (on the user's word).** Run episode 249 itself through the app end to end (design → render → assemble → push → gate) and compare the resulting movie against the approved prototype `249-composite-full.mp4` (93,749,687 B, 1883.689 s, SHA-256 `752852DD7DAA98EA535570AAFF15CDDF66E2659BA911C30D6EBC783D87A3F67D`). The prototype is the oracle: same clip order and durations (within 1 s total), same 1920×1080 frame, same strip / captions / panels / footer by the trial's measurements (name centers above the panel centers, names at the mic-base level, strip pure black, caption gap, panels full-frame with no crop, footer in the Mosaic style, formulas page-sourced), and frame spot-checks matching the prototype. Report every gap — do not silently accept a difference. (Note: clips 3–4 have no caption data; the app must surface that as a reported exception per Spec H §4 rather than silently shipping a static band as the prototype did — fix the data first, or accept the exception as the expected result for those two clips.)
- **Exercise the "Design artifacts" button:** initial render for the episode, per-clip progress shown, exceptions-only list reported.
- **Exercise the retrigger flows:** pause the longform preview, retrigger Manim only for one clip and Mosaic only for another; the master updates for those clips only, duration unchanged, the hard-coded frame unchanged.
- **Exercise the kill rule and the caption-data rule** (a clip with no caption data is a reported exception, not a silent static band).
- **Exercise the run-artifact health check** (a missing run file is re-downloaded by run ID and reported; never substituted).
- Report PASS or FAIL per verify step, then a full summary, then stop.

## Build summary (2026-11-25)

What was built (deepDive; mirrored code-only to mdIngest):

- `ddma/spec_h2_composite_assembler.py` — the assembler module. Ports: caption ASS builder (`gen_v6.py`/`gen_full.py`); per-clip ffmpeg filter graph + shape (`build_v6.py`/`build_full.py`); host-strip constants (`strip_v6.py`); concat list (`mkconcat6.py`/`mkconcat_full.py`); stage-timing rule (`gen_art.py`); heal pattern via spec H (`inv`/`ffall`/`redownload_missing`). One deliberate deviation: emits the correct `-filter_complex_script` form (plus the same `vf_{n}.txt` sidecar) instead of the trial scripts' non-working `-/filter_complex` typo.
- `ddma/tests/test_spec_h2_composite_assembler.py` — 15 tests. H2 + H1 suites: 34/34 OK (19 Spec H + 15 H2, run 2026-11-25 via unittest in both clones).
- Small correction folded in: `defect-specs/deepdive-spec-h-composite-longform.md` line 115 — oracle SHA recorded as `752852DD7DAA98EA535570AAFF15CDDF66E2659BA911C30D6EBC783D87A3F67D` (deepDive-only; spec md never mirrored).

Sample verification (clips 249-0, 249-1, 249-2, trial DURS 144.300/120.733/112.666 s):

- DESIGN: `build_caption_ass` from plan `_caption_words` → 695/495/499 karaoke events, byte-identical to trial `caps_0/1/2.ass` Dialogue counts. PASS.
- RENDER: per-clip segments via `build_segment_cmd` → 11,770,964 / 10,730,685 / 5,555,699 B, each SHA-256 byte-identical to `v6_seg_0/1/2.mp4` (the files concatenated into the oracle). PASS.
- ASSEMBLE: concat demuxer `-c copy` → `sample_composite_012.mp4`, 28,056,650 B, 377.721 s, 1920x1080 H.264+AAC, SHA-256 byte-identical to `249-composite-preview-v6.mp4`; spot frames at t=10/150/300 s PNG-identical to oracle `249-composite-full.mp4`. PASS.
- ORACLE: `249-composite-full.mp4` = 93,749,687 B, SHA-256 `752852dd7daa98ea535570aaff15cddf66e2659ba911c30d6ebc783d87a3f67d`, 1883.689 s, 1920x1080.
- Guardrails: outputs only under `scratch/249-sample-012`; clips 249-3+ and episode 250 untouched; no Mosaic runs (local ffmpeg only); no substitutions; no gate/hub writes.

Gaps / next steps:

- Trial `-filter_complex` typo not reproduced byte-for-byte (correct form emitted instead) — owner call if byte fidelity is wanted.
- Beats Studio "Design artifacts" button and retrigger endpoint wiring (§3/§4 UI) not added — module exposes `plan_design_artifacts`/`plan_retrigger` planners for that wiring.
- Full 249 regression (all 21 clips end-to-end vs oracle) deferred — sample 0–2 only, per "sample first, hard stop".

## Build summary II — Beats Studio wiring + 249-3/4 caption fix (2026-11-25)

What was wired (deepDive `ddma/beats_server.py` +272, `ddma/beats.html` +114; mirrored code-only to mdIngest):

- `beats_server.py`: H2 block behind `H2_EPISODE=249` guard — read-only plan load, ffprobe duration probe, composite-master resolver, background design worker forwarding per-clip to the curator manual Manim path only. New endpoints: `GET /api/beats/composite_timeline` (probed master duration; `null`+note when no master; 400 for ep != 249), `GET /api/beats/design_status` (per-clip progress, exceptions-only), `POST /api/beats/design_artifacts` (one deliberate start, fan-out via `spec_h2.plan_design_artifacts`, queued background thread), `POST /api/beats/composite_retrigger` (`spec_h2.plan_retrigger` duration/frame lock, planner-only, never starts Mosaic). Push endpoint + Spec H gate code untouched.
- `beats.html`: header buttons Design artifacts (episode), Design this clip, Retrigger Manim-only, Retrigger Mosaic-only; `h2-design-panel` for per-clip progress/exceptions; JS `loadCompositeTimeline`/`designArtifacts`/`pollDesignStatus`/`compositeRetrigger` (pauses preview first, chains to existing manim/mosaic paths); playhead badge now prefers the composite probed total and shows `--:--` when no master (hardcoded 3254.08 fallback removed; no `3254` remains in either file).
- Ep-249-only enforced server-side (400) and client-side; episode 250 untouched throughout.

249-3/4 caption fix outcome (episode 249 only; cut+compile via `ddma.py` from `deepDive/ddma`; no Mosaic contact — `mosaic_run_id` unchanged on both clips):

- `cut --num 3/4` re-cut the exact audio slices; `compile-clip --num 3` → 1080x1920 DAR 9:16, 92.92 s, 5.16 MB, 44 ASS caption events (`rendered_duration=92.92`, `audio_duration=87.19`, `intro_offset=1.7`); `--num 4` → 95.16 s, 3.60 MB, 48 ASS events (`rendered_duration=95.16`, `audio_duration=89.43`). Both VERIFIED OK, Mosaic bodies preserved.
- Plan state: clip 3 `caption_chunks=44`/`_caption_words=204`/`_compiled_sig=True`; clip 4 `caption_chunks=48`/`_caption_words=230`; siblings untouched (clip 2=62, clip 5=49). `captions/249-3.ass` (98,867 B) + `249-4.ass` (104,338 B); compiled masters `clips/249-3.mp4`/`249-4.mp4` + `-mosaic` bodies exist; publication syncs in `src/ddma/docs/episodes/249/clips/`. PASS 249-3 and 249-4 (caption data present, no section-4 exception).

Full-regression verification numbers:

- `unittest` spec_h2 + spec_h suites: 34/34 OK in deepDive and 34/34 OK in mdIngest; `node --check` on extracted inline scripts: clean.
- Live wiring probe (test instance :18001, since stopped): timeline 249 → 200 `has_video=false`/`total=null`/`fallback_used=false`; 250 → 400; retrigger manim/mosaic → 200 duration+frame locked; bad side → 400; retrigger 250 → 400; design clip 3 → group `h2-249-1`, status `failed` with `no caption data` exception-only report (no curator contact); design 250 → 400.
- Oracle comparison (read-only probe): `249-composite-full.mp4` = 93,749,687 B, 1883.688688 s, 1920x1080 h264+AAC 48 kHz stereo, ~30 fps, SHA-256 `752852DD7DAA98EA535570AAFF15CDDF66E2659BA911C30D6EBC783D87A3F67D`. Clip order PASS (concat lists v6_seg_0/1/2 + full_seg_3..20 in order 0–20). Frame contract PASS (1920x1080; strip 1920x120, panes 740x740 at (220,230)/(960,230); spot frames t=100/900/1700 s show strip, karaoke captions, both panes, footer). Captions 21/21 PASS (events 0:695 … 20:514, first=0.0, last=duration). Freshness 21/21 PASS, run artifacts 21/21 byte-identical to trial report. Duration FAIL: plan segments-ground-zero total 1873.37 s vs oracle 1883.689 s → gap −10.32 s over 1 s tolerance (systematic −0.4..−0.7 s/clip: Cutroom re-cut shorter after the trial). Assembly BLOCKED: 21/21 `ManimPaneMissing` (no Manim artifact keys in plan; trial art files live only in the trial folder); gate smoke `longform_publish_gate(oracle, None)` = ok True (existence-only).
- Commits: deepDive `637d29a5` wiring+fix, plus this spec file (committed separately below); mdIngest `b2bd31f` wiring mirror (code-only). `ddma/docs/plan.json` + `ddma/plan.json` `published` diffs are pre-existing app writes, left UNCOMMITTED in both clones.

Gaps (nothing silently accepted):

- No app-built 249 composite master exists — end-to-end render/assemble/push/gate and movie-vs-oracle byte/SHA comparison remain undone until 21 Manim artifacts render.
- Fresh-assembly total (1873.37 s) already exceeds the 1 s duration tolerance vs oracle — needs a scope decision (re-cut vs re-time) before any full rebuild.
- Clips 3/4 karaoke-vs-title-band delta vs oracle is the intended fix, not a regression.
- New-endpoint HTTP framing on working-tree code verified at helper level only (own :18001 probe hit a framing failure; prior :18001 wiring probe above was on the earlier turn's instance).
- Chapter strip still plan-segments-ground-zero provisional.

## Build summary III — duration math fix (run file decides duration)

Root cause: `clip_ground_zero_duration` computed
`sum(segment durations) − sum(crossfade fields)`, but the plan's
crossfade fields total exactly 1.00 s per clip (21.0 s over 21 clips)
while the real audio overlap in the run files is only 10.68 s total —
a systematic −0.39…−0.74 s per clip, −10.32 s total. The oracle is
right: the run files sum to 1883.69 s and the trial built the oracle
from them as-is. No re-cut happened; the crossfade fields simply
overstate the overlap.

Fix: new `probe_run_duration` (ffprobe `format=duration`, same
heal-pattern probe shape as Spec H, never raises, never substitutes),
`resolve_clip_run_path` (canonical run-ID artifact or explicit
`run_path` only), and `clip_composite_duration` /
`clip_composite_duration_explained` (run-file probe first, segments
fallback only when no run file or the probe yields nothing).
Segments still decide CONTENT (golden rule stands); the run file
decides DURATION, and the Manim side renders to the same duration.
`composite_timeline` chapters and the retrigger duration lock use the
new resolver. Old `clip_ground_zero_duration` is kept as the fallback.

Verification: fresh-assembly total over the 21 real hub run files
(read-only ffprobe, all `run-file-probe`) = 1883.663 s vs oracle
1883.689 s (delta 0.0263 s < 0.05 s tolerance). New
`TestEpisode249DurationPin` (2 tests) pins the 21 caller-given run
durations to 1883.69 and the assembler total to the oracle; the live
test resolves its clip list from the canonical hub plan when the local
clone has no plan files (mdIngest is code-only by design). Suites:
36/36 OK in deepDive, 36/36 OK in mdIngest. Endpoints re-verified
live on an isolated test instance (dead-curator patch, zero side
effects): timeline/design_status/design_artifacts/retrigger all
return complete bodies with correct framing; 250 refused 400
everywhere; unknown group 404.

Gaps: `composite_timeline` chapters branch (21 chapters) not exercised
over HTTP — no 249 master exists yet (chapter math proven in-process).
Manim design and the full 21-clip regression remain next, not this job.

## Build summary IV — curator Manim endpoint + 21-clip design (run file decides duration still holds)

Root cause (verified in code at remote head `2c8e16b3`): the Beats
design worker (`_h2_run_design_group`) and `manim_retrigger` POST to
`127.0.0.1:8000/generate-manim-infographic`, but `run_curator.py`
(47 routes) had no such route — referenced in `beats_server.py` only,
defined nowhere. The Manim logic existed solely as in-process
`generate_or_load_storyboard_data` (~line 1756). Every Design call
failed 0/21 with 404. Not the servers, data, or user edits.

Fix: new `POST /generate-manim-infographic?id=episode_249&num=N`
route in `run_curator.py` (+136 lines), wired to
`generate_or_load_storyboard_data` then the existing
`manim_infographic_engine.render_manim_infographic_mp4` +
`compile-clip --source manim` path — no new renderer, no Mosaic,
never substitutes (raises when render/compile output missing).
Returns `{success:true, artifact}` or `{success:false, error}` in the
shape Beats expects. Plus one consistency fix: `manim_retrigger`'s
curator timeout 30 s → 120 s (same synchronous render the design
worker already waits 120 s for; 30 s timed out a healthy render —
first clip-1 retrigger hit exactly this). Endpoint proved live with a
direct curator POST (200, 8 scenes) before any Beats call.

Verification: single clip 1 — design job `done`, no exceptions,
`249-1-manim.mp4` exists (4.1 MB, 126.44 s); switch-to-Manim path
returns `success:true` post-timeout-fix. Full 21-clip group
`h2-249-1`: 21/21 `done`, 0 failed, no exceptions (polled to
`finished:true`). Suites 36/36 OK in deepDive and mdIngest after the
mirror. Diagnosis (read-only, files untouched): clip 249-0 shows
`openable=false` while 249-2 shows true because clip 0's Mosaic body
exists ONLY under the full-UUID run filename (local + hub) with NO
generic `249-0-mosaic.mp4` fallback, while clip 2 has a local generic
fallback — any resolving context without the clip's `mosaic_run_id`
finds 2 but not 0. With the current plan + hub, `resolve_mosaic_body`
finds clip 0 fine (hub run file, square 1080x1080, 144.3 s) and
`_has_clip_media(0)` is true, so the false report comes from a stale
data path, not missing files. Left for a later turn; nothing moved.

Gaps carried: no 249 composite master exists yet, so render/assemble/
push/gate and the movie-vs-oracle comparison remain undone; `composite_timeline`
chapters branch still unexercised over HTTP. Plan/data churn from the
design runs (episode_249 rev106 → rev154, src syncs, storyboards) left
UNCOMMITTED by design — code + spec only in these commits.

## Build summary V — 249 master assembled, pushed, gated, compared (PASS with noted gaps)

Assembly: all 21 clips via the H2 assembler (Manim left + Mosaic
right + strip + karaoke + footer), concat seg_0→seg_20 in order.
Per-clip report: 21/21 `ok`, every duration `run-file-probe`, probed
segment total 1883.668 s. Master `ddma/clips/249-longform-master.mp4`:
100,722,836 B, 1920x1080 H.264+AAC, container 1883.688 s.
Push via app endpoint: success to hub `episodes/249/249-longform.mp4`,
meta SHA-256 `53e5a87a…eeb2e`, `ready_for_distribution:true`,
`stings_stripped:true`. Gate: ok (`draft-relative structural check`).

Oracle comparison (`249-composite-full.mp4`, 93,749,687 B, 1883.689 s):
durations PASS (Δ 0.001 s, within 1 s); clip order PASS (0→20);
frame PASS (1920x1080 both); strip/captions/footer PASS (spot frames
show identical layout, karaoke highlight, footer bars); SSIM at
t=150/900/1500 s: 0.914/0.916/0.942 — right (Mosaic) pane identical
(same run files, same dot patterns/titles), layout identical.
GAPS (nothing silently accepted): (1) left (Manim) pane content differs
— fresh storyboard renders (e.g. clip 1 "ONTOLOGICAL FALLACY / ROBOT
UNPLUGGED" robot) vs the trial's original art (clip 1 "8D Totality"
circle); expected by construction, since the design group re-rendered
all 21 Manim artifacts, but the pixels are not the trial's. (2) clips
3–4 carry karaoke captions instead of the prototype static title band —
the intended fix. (3) file size differs (100.7 vs 93.7 MB, different
encode settings — size was never a pass criterion).

Assembly-run state committed here: episode_249 plan.json (segment/
rendered reconciliation for the shipped master) + src 249-7.mp4 sync.
Root plans untouched; scratch segment dirs stay untracked by design.

## Build summary VI — Beats chapter list reads H2 data (2026-11-25)

Root cause (verified in code at remote head `4acb3881`): the chapter list
(`get_longform_all_chapter_mappings`, served as `/api/beats/index`) read
only the retired beat-file mapping. `openable` missed H2 artifacts (clip
249-0 reported `openable=false` while 249-2 was true only because a generic
local `249-2-mosaic.mp4` fallback exists — resolving without the clip's
`mosaic_run_id` finds 2 but never 0), `has_beats` read retired beat files,
and windows were beat-mapped on the 3254.21-based header total from the
open question (b). Episodes with full H2 coverage had no path to report it.

Fix (`ddma/archetype_studio.py` +149/-6, mirrored code-only to mdIngest):
three H2 helpers + five wiring edits in `get_longform_all_chapter_mappings`
/ `get_longform_timeline_index`. (a) `openable` now ORs three H2 terms on
top of the unchanged existing terms: clip in the H2 composite set,
`249-N-manim.mp4` exists (local or hub), hub run file by plan
`mosaic_run_id` via `spec_h.canonical_run_artifact_path` hub-first (exact
run-ID artifact only). (b) `has_beats` on H2-covered episodes is the H2
Manim artifact existence only (old beat-file term dropped, no fallback);
`manim_retrigger`, `set_clip_visual_source`, and `beats.html` untouched (no
dropdown/picker). (c) H2-covered episodes (every plan clip resolves a
run-file-probed composite duration — e.g. all 21 clips of 249) get
cursor-based windows from run-file durations plus the composite cursor
total; the legacy path is byte-identical otherwise. Episodes without full
H2 coverage (e.g. 248) keep legacy windows / `has_beats`. Read-only: never
substitutes, never triggers a run, never writes any plan; no 250 contact.

Verification: live on `:8001 /api/beats/index?ep=249`: total 1883.66,
clip 1 = 144.3–265.03 (2:24–4:25), clip 0 = 0.0–144.3, clip 20 ends
1883.66, all 21 clips `openable`/`has_beats` True; `get_longform_chapter_beats(249,1)`
matches. (a) clip P0 selectable: list gates on `openable` only
(`beats.html:550`), number strip renders every chapter (`beats.html:386-387`)
and only `openable===false` blocks (`beats.html:394`); clip 0 live
`openable=True`. (b) clip 1 Manim toggle: `btn-engine-manim.disabled`
follows `hasBeats` (`beats.html:610`), `No Manim yet` hint only when
`!hasBeats` (`beats.html:617-630`); live `has_beats`/`has_mosaic` True so
toggle enabled and hint hidden; `/api/beats/beats?ep=249&clip_num=1`
confirms `has_beats` True. (c) header `Part N: title (m:ss-m:ss)` via
`formatDuration` (`beats.html:634,1177-1181`); live title `8D Totality`
gives `Part 1: 8D Totality (2:24-4:25)`. (d) no dropdown/reuse picker in
clip flow: exactly one `<select>` (`#beats-ep` top bar, pre-existing), zero
matches for reuse/listbox/combobox; clip visual-source switching uses
Mosaic/Manim toggle buttons via `setClipEngine` POST (`beats.html:737-743`).
Suites: `test_spec_h2_composite_assembler` + `test_spec_h_composite_longform`
= 36/36 OK. Guardrails kept: no Mosaic runs (read-only ffprobe/exists
checks), no plan writes (`ddma/plan.json`, `ddma/docs/plan.json` untouched),
no 250 contact.

Gaps carried: none new — no 249 composite re-render was needed (master
from summary V stands); `composite_timeline` chapters branch still
unexercised over HTTP (chapter math proven in-process).

## Build summary VII — clip 0 selectable (`normClipNum`, P0 click lands on P0)

Root cause (user-observed live, verified at `722c5da0`): `selectLfChapter`
did `parseInt(clipNum, 10) || 1` — `parseInt(0)` is `0`, falsy, so
`0 || 1` is `1`. Every P0 click (list and number strip) selected clip 1.
Seven more `|| 1` clip-number sites in the same file would have clobbered
clip 0 back to 1 for Design-this-clip, both retriggers, Patch, chapter
fetch, Manim switch, source toggle, and Mosaic retrigger. Server side
was fine (`int(clip_num)` passes 0 through); purely page JavaScript.
Episode 248 never showed it — its clips are numbered 1–23.

Fix: one `normClipNum(v)` helper (parsed integer when numeric,
including 0; default 1 only for missing/NaN) + all 8 call sites.
The `(ch.end || 1)` span-duration guard is untouched — not a clip default.

Verification: node --check clean; helper semantics exact
(0→0, 1→1, "3"→3, missing/NaN→1); served page carries the fix;
Design-this-clip for clip 0 planned job clip 0 and finished `done`
(c0 artifact re-rendered, no errors). Click path verified by
inspection + live data: callers pass raw `clip_num`, clip 0 exists
and is openable in the live index, header formats Part 0 from 0.0.
Suites 36/36 in both clones after the mirror. No Mosaic runs, no
substitutions, no 250 contact, no plan writes.

## Build summary VIII — clip-level Manim panel replaces micro-beats pane (retired beat-finesse UI)

Context (ep 249, Beats Studio): the lower pane under the player still
showed the retired 8s-beat system — "MICRO-BEATS IN ACTIVE CLIP",
"PART 1 / BEAT 1/1", archetypes/clip_N_gemini_scenes.py paths, spoken
dialogue, Producer Feedback, Manim code view, Save to Personal Beats,
Regenerate This Beat. The chapter-list fix never touched this pane.

Fix (beats.html, page only; no server/data changes beyond one
read-only endpoint):
- Deleted tpl-beats-editor, the right "EXPAND / TAB" pane and its tab,
  the preview overlay, and 10 beat functions (renderLfBeatPills,
  selectLfBeat, fetchLfChapterProgressive, loadPersonalBeats, beat
  feedback/save/regenerate/update/mosaic-retrigger, tab switching).
  All call sites now route to renderClipSurface/renderClipManimPanel.
- New clip-level Manim panel (lf-manim-panel) shows the ONE artifact
  per active clip: title, equation (preferred) or anchor text
  (label + arrow keyed to the hook sentence) or hook title, storyboard
  status + scene count + duration (Manim ready / n scenes), and the two
  clip-level actions Design this clip (designArtifacts 'clip') and
  Retrigger Manim-only (compositeRetrigger 'manim'). Episode-scope
  design (h2-249-1) untouched. No dropdown, no reuse picker added.
- New read-only server route GET /api/beats/storyboard
  (beats_server.py, +33 lines; H2 index untouched): ep-249-only, takes
  clip_num, returns hook_title + full storyboard JSON (equation or
  anchor labels + scenes + total_duration); 400 off-episode, 404 with
  reported-exception text when no storyboard. The old /api/beats/beats
  returns empty beats for H2 clips, so the design source of truth
  (storyboards/clip_N_storyboard.json) is read directly instead.
  has_beats beat-file toggle logic unchanged (still the
  Manim-existence signal); render path null-guarded; two-column grid
  after right-pane removal.
- Kept: player, chapter list, strip, top buttons, mosaic-only template
  (renamed copy to "No Manim Yet"), span guards, pointer-flip and
  retrigger behavior.

Verification (all on live servers restarted from this tree):
- Served page: zero of 16 retired strings present
  (MICRO-BEATS, gemini_scenes, Personal Beats, tpl-beats-editor,
  lf-beat-, Regenerate This Beat, Producer Feedback, Spoken Dialogue,
  loadPersonalBeats, selectLfBeat(, renderLfBeatPills, update_beat,
  tab-expand-right, beats-right-pane); all 4 new markers present
  (lf-manim-panel, renderClipManimPanel, renderClipSurface,
  /api/beats/storyboard).
- Storyboard endpoint live: 249/1 -> 200, 8 scenes, 120.72s, first
  scene label ONTOLOGICAL FALLACY; ep 250 -> 400; clip 99 -> 404 with
  reported-exception text. node --check on the patched page: clean.
- Panel renderer exercised in node with DOM stub + real clip-1
  storyboard: output shows title, Anchor ROBOT / NO SOCKET, Manim
  ready, 8 scenes, 120.72s, 249-1-manim.mp4, both correct buttons;
  zero banned words.
- Suites: H1+H2 36/36 OK in both clones; full discover 42 runs with
  1 error in test_mosaic_pipeline_recovery
  (test_safe_load_json_resilience...) — proven pre-existing by
  re-running it with my two files stashed (fails identically on the
  clean tree); imports run_curator only, which this job never touched.
- Ep 249 only; ep 250 untouched (probe only for the 400 guard).
  No Mosaic runs, no substitutions, caption data via storyboards,
  no plan writes (ddma/plan.json, ddma/docs/plan.json untouched).

## Build summary IX — fresh-cast Manim design (Severity-1 stale Manims)

Cause (user-observed live, verified in code): the 249 master carried the
old engine's fixed-archetype designs (clip 0 robot_unplugged, clip 1
teenager_basement), and Design-artifacts just re-rendered them — the
worker POSTed only {ep, clip_num}, the curator returned the cached
storyboard file or the plan's infographic_scenes, and generation used the
old Feynman-Needham rule block. The new clip-level Manim panel displayed
the stale design faithfully.

Fix (design call = fresh cast; new rules in code, not just in the note):
- New module ddma/manim_fresh_design.py (mirrored): episode-page
  equation catalog (katex-display blocks + sections from
  deepdive.shutri.com/249.html, cached), deterministic one-design-call
  per clip (transcript + title + catalog; title-gated topic routing, no
  invention possible — the equation is always a catalog member or the
  clip degrades to anchor/title-only, reported), stages at sentence
  boundaries (title first, then build stages of the ONE visual),
  deterministic Manim templates (title / formula / tunnel / numberline
  / groundzero / anchor; Text only — no LaTeX in this env), filler-hook
  skip, reuse detection (reported, never silent).
- Curator POST /generate-manim-infographic: for episode_249 with
  force_regen it NEVER reads the cache or plan scenes — always designs
  fresh, REPLACES the storyboard file and the plan's infographic_scenes,
  rescales stages to the probed run duration, renders and compiles as
  before. Other episodes / non-force keep the legacy path.
- Beats worker sends force_regen + transcript + title (249-only);
  manim_retrigger sends force_regen + transcript + title for ep 249 only
  (other eps byte-identical). design_status reports design_reports,
  changed_clips, master_stale + manual re-assemble note; nothing is ever
  auto-assembled or auto-pushed (verified: master hash unchanged after
  design, gate runs only via the manual Push button).
- Engine: generate_manim_scene_python dispatches kind-tagged stages to
  the fresh templates (archetype list and JIT bypassed on this path);
  footer shows the stage kind. Panel + /api/beats/storyboard read the
  design block and show "N stages" (the old "n scenes" display is gone).
- Key environment finding (verified live): the stored gemini_api_key is
  a 401 for the Generative Language API, so all Gemini paths (old and
  new) fall back deterministically. Reported here; the deterministic
  design call is the working path. No keys were probed or changed.
- Segment art is the 740x740 infographic (clips/249-N-infographic.mp4),
  not the 1080x1920 compiled manim — verified by frame inspection (the
  compiled clip overlaid wrong).
- Re-assemble path used: H2 segment build (build_segment_cmd,
  resolve_segment_inputs, write_caption_ass) + concat + duration gate,
  with trial chrome/strip assets read-only. /api/beats/patch stays
  248-hardcoded (render_longform_parallel.py EP_NUM=248) — it is NOT the
  249 path; see incident below.

Verification (all live, ep 249 only):
- Single clip 1: design group done; storyboard file + plan scenes
  REPLACED (formula kind, octonion basis equation from page section 1,
  6 stages, total 120.72); panel shows Equation + 6 stages + 120.72s +
  both buttons, zero banned words; status reported master_stale with
  changed clips + manual re-assemble note; manual splice at 144.30s
  passed the duration gate (delta 0.038) and the frame at t=200 shows
  the new formula art.
- Full episode: group h2-249-2, 21/21 done, 0 failed. Equations (9):
  clip 1 octonion basis, 2 free energy, 3 associator, 4 thermal time,
  8 associator (reuse of 3, reported), 13 modular flow, 15 thermal time
  (reuse of 4, reported), 18 thermal time (reuse of 15, reported),
  19 thermal time (reuse of 15, reported). Anchors (12, all reported):
  0, 5, 6, 7, 9, 10, 11, 12, 14, 16, 17, 20. No dropdown, no reuse
  picker, no per-beat design.
- Full master re-assembled (21 fresh segments + concat): 1883.685s
  (oracle 1883.689s, delta 0.004s), 1920x1080, installed as
  clips/249-longform-master.mp4; spot frames at clips 1/5/8/15 show
  fresh formula/anchor art + karaoke + chrome; publish gate passes
  (ok True, read-only check — nothing pushed to dd_hub).
- Suites: 57 tests both clones; only failure is the known pre-existing
  test_mosaic_pipeline_recovery error (re-proven with all my code files
  stashed — fails identically on the clean tree; imports run_curator
  only for safe_load_json, which this job never touched).
- Incident (honest report): the first manual "Patch" call hit
  /api/beats/patch, which is hardcoded to EP 248 — it re-rendered
  248's chapter-1 window and spliced 248-longform-master.mp4 (mtime
  8:47 PM). 248's sources were never modified, so the re-render is
  content-equivalent, and the master probes intact (3254.24s, frames
  sane). No 250 contact anywhere. The 249 splice/assembly above used
  only the H2 path afterward.

Deviations from the request: segment art is the 740 infographic, not
the compiled 249-N-manim.mp4 (the task's parenthetical names the wrong
file for the filter graph — verified by dimensions and frame
inspection); the trial filter uses "-/filter_complex <script>" while
spec_h2 emits "-filter_complex_script" (this ffmpeg calls the latter
deprecated but still honors it — worked; module correction left for a
future job); /api/beats/patch was NOT fixed to route ep 249 (left
248-hardcoded; the H2 re-assemble path was used instead and the gap is
reported here). No plan writes beyond the design's own episode-plan +
src syncs (root ddma/plan.json, ddma/docs/plan.json untouched).
No Mosaic runs, no substitutions, no 250 contact, no hub writes.

## Build summary X — per-clip design instruction box + single-copy buttons + 249 Patch fix

Commits: deepDive 2964c11b (code + tests + H3 spec copy + vendored
assets + clip-15 design state), mdIngest 9824dd1 (code-only mirror of
the 4 code files + the new test file). defect-specs/ stays
deepDive-only; storyboards / plan scenes / catalog cache never fan out
to mdIngest.

Part A — instruction box (all three hops, both fresh-cast entry points):
- Page: the below-player surface is ALWAYS the Manim panel
  (renderClipSurface no longer branches on has_beats; the Mosaic-only
  template is gone). The panel shows title / equation-or-anchor /
  status / 6-stage count as before, plus ONE textarea
  (#lf-manim-directive, placeholder naming the thermal-time example),
  the last honored outcome under the box, and the single Design button.
  No-Manim state (storyboard 404) renders "No Manim yet" + box +
  button, never a bare error line. The box prefills from the
  storyboard's stored design.directive per clip; unsent text is not
  carried across clips.
- Page wiring: designArtifacts('clip') and switchClipToManim() read the
  box and send it as directive. Episode-scope design ignores the box.
- Beats server: clip-scope design_artifacts carries the directive onto
  the job; the worker forwards it in its curator POST; manim_retrigger
  forwards it in its curator POST.
- Curator fresh path (249 + force_regen) passes the directive into
  design_clip_artifact(directive=...) — no longer dropped.
- Honoring (deterministic, never invented): unnegated "anchor" forces
  anchor ("directive-honored: forced anchor"); an equation name picks
  the best catalog member by topic/norm overlap (threshold >= 4, always
  a catalog member); a naming-but-unmatched directive degrades to
  anchor WITH "directive-unmatched: ...; degraded to anchor"; anything
  else is a topic hint (deterministic +2*overlap boost + Gemini
  instruction, catalog validation as backstop); empty directive =
  byte-identical old behavior (no directive keys stored).
- Reporting: design_status jobs now carry directive +
  directive_report per job (the curator already returned design +
  reports; the status snapshot was dropping them); the storyboard's
  design dict stores design.directive + design.directive_report.
- Retrigger Manim-only carries the directive too (it re-casts fresh),
  so a later retrigger cannot silently discard the instruction.
  Nothing touches the Mosaic side, durations, or assembly; design
  completion still reports master-stale only (verified live:
  "Nothing was auto-assembled or pushed").

Part B — single-copy review (beats.html 954 -> 872 lines):
- B1 "Design this clip" moved INTO the panel (top-row copy deleted).
- B2 "Retrigger Manim-only" stays top-row only (panel duplicate
  deleted). B3 surface "Retrigger Mosaic" button deleted (strict
  subset; beatsMosaicRetrigger() kept — compositeRetrigger calls it).
- B4 surface "Switch this clip to Manim" button deleted (same
  fresh-cast call as Design this clip for 249; switchClipToManim()
  kept — compositeRetrigger('manim') calls it).
- B5 tpl-mosaic-only-actions gone entirely. B6 engine toggle gone
  (both buttons + label + hint span + setClipEngine() +
  selectLfChapter styling refs); /api/beats/set_engine and
  visual_source untouched. B7 replay button + replayActiveSpan() +
  all three touchpoints gone. KEEP list verified present, one copy
  each: episode picker, pane collapse/expand, System Settings, Play
  Clip / Play Full, Patch, Push, episode Design artifacts, both
  top-row Retriggers, chapter buttons, strip segments, native
  controls, h2-design-panel.
- B8 Patch fix: render_longform_parallel.py --patch takes NO episode
  (verified: patch_longform_chapter(int(argv[2])), EP_NUM hardcoded
  "248"). The 249 case now routes through the H2 segment re-stitch
  (same path as compositeRetrigger); other episodes keep the legacy
  script. The success message names the episode actually patched
  ("Part 15 patched into ep 249 master").

Verification (ep 249 only):
- V1 PASS: all 11 removed ids/handlers gone; 5 kept top-row buttons +
  box exactly once each; single "Design this clip" in panel; only
  surviving `|| 1` is the line-254 duration fallback; both script
  blocks node --check clean.
- V2 PASS (served page + static): box + kept strip present, dupes
  absent in the served HTML; normClipNum intact at all 8 call sites;
  P0 guard unchanged from the pinned fix. No headless browser in this
  env, so the physical click was not exercised — noted, not claimed.
- V3 PASS: 6 new directive unit tests green; full suites 63 tests in
  BOTH clones with the single known pre-existing
  test_mosaic_pipeline_recovery error (untouched file, left as-is).
- V4 PASS (content-neutral, live): clip 15 "use the thermal-time
  equation" -> kind formula, SAME equation_norm byte-for-byte
  ('t thermal = -b 1 ln r', section 4.), same 6 stages; storyboard
  diff is only directive keys + reuse_of + reason; design_status
  reported directive + "directive-honored: equation 6" + reuse +
  master-stale; panel data source returns directive + outcome for
  clip 15; clips 18/19 boards untouched (only clip_15 modified).
- V5 PASS: storyboard endpoint 404s clip 99 as specified; the REAL
  page functions (extracted, node harness) render "No Manim yet" +
  box + Design with zero retired text on the 404 path, and the
  directive + outcome on the 200 path.
- V6 PASS (live, clip 15): 249 master 121021099 -> 117168718 B,
  1883.685 -> 1883.724s (delta 0.039s, gate held); 248 master
  byte-identical (sha match) and mtime-unchanged; message names
  ep 249.
- V7 PASS: no 250 files touched in either clone; fresh server logs
  show no Mosaic/push/hub lines; no auto-assemble or auto-push in the
  new code paths (design reports master-stale only); storyboards byte
  identical except the clip-15 acceptance re-cast; no Manim template,
  font-size, or footer change (engine file untouched).

Deviations / honest notes:
- reuse_of flipped 4 -> 18 on the clip-15 re-cast: the norm is
  identical (clips 4, 15, 18 all carry it, verified via the endpoint),
  so this is dict-ordering noise in the prior-map loop, not a content
  change. Reported, never silent — same as the old reuse_of 4.
- Server hygiene: two processes were bound to each of :8000 and :8001
  (same 5:11 AM restart batch). All four were killed and single fresh
  instances launched from the current deepDive tree; all four ports
  re-verified 200 (storyboard endpoint serves the fresh-cast design).
  8088 + mdbook were single-bound and left running.
- ddma/plan.json shows a 5:33 AM re-serialization (same session as the
  clip-15 design); it carries no directive content and stays
  uncommitted, exactly as found, with ddma/docs/plan.json.
- V2's physical click and V5's in-browser panel render were covered by
  served-HTML checks + the real-functions node harness, not a live
  browser — that is the verification boundary of this environment.

## Build summary XI — equations-as-math BLOCKED (no TeX source), plan-title footer, player 16:9, oracle immunity

Commits: none in this job (batch commits once after footer V2, per the
job spec). Code mirrored to mdIngest (uncommitted). Spec file
`defect-specs/deepdive-spec-h2-equations-katex-fit.md` saved in
deepDive (untracked, goes out with the batch).

Math path (A/B): STOPPED before any render change, per the spec's own
stop rule. Renderer availability first: no LaTeX on the machine
(pdflatex/xelatex/lualatex all absent; Manim is Text-only here), no
KaTeX module — but npm works, so KaTeX was installed machine-global
(`npm i -g katex`, resolved via NODE_PATH) and verified rendering.
The blocker is the SOURCE, not the renderer: the spec's claim that
"the real LaTeX source lives in the episode page's katex-display
blocks" is false. Fetched 249.html live (179,390 B): all 7
katex-display blocks contain pre-rendered KaTeX HTML only
(`katex-html` spans, no MathML, no annotations) — zero TeX markers of
15 kinds checked (no math/tex, data-tex, text/x-tex, katex.render,
renderMathInElement, \frac, \sum, \int, \sqrt, \eta, \rho, \beta,
\ln). The catalog carries only plain-text norms, not TeX.
Reconstructing TeX from rendered HTML or hand-writing it would be
inventing, so A/B stopped with no code change: equations render as
before (plain Text), fitting logic untouched. A future data-only fix
is straightforward — the footer pipeline already threads strings
through — if the user supplies the 9 equations' TeX.

C (plan-title footer): `_render_stage_body` takes the above-line title
from the transient in-memory `_render_title` hint (plan title injected
per stage by the re-render driver; storyboard files never edited),
falling back to the stage title. Design focus stays below-left.
Footer title is uppercase plan title as before ("8D TOTALITY").

E (oracle immunity): `test_fresh_assembly_total_matches_oracle` now
reads `projects/episode_249/plan.json` (hub fallback preserved),
never the shared root copy. Test-only change.

F (player): removed `max-height: 360px` from `#lf-studio-video-player`
(one line); width 100% + aspect-ratio 16/9 now governs. Served HTML
verified (cap string gone).

Re-rendered from existing storyboards (no design): clips 1, 3, 13
only (footer V2's remaining 20 explicitly not run).

Verification (ep 249 only):
- V1 PASS: clip 1 footer reads above "8D TOTALITY", below-left
  "ULTIMATE ANCHOR", below-right "deepDive podcast · Ep 249" (frame
  evidence). No duplication, no collision, legible.
- V2 FAIL (blocked): clip 3 equation still plain Text, still wraps
  mid-symbol (frame evidence). Real math needs the missing TeX source.
- V3 FAIL (blocked): clip 13 still huge Text overflow, "a t p ("
  cut off (frame evidence). Same blocker. (Observed mechanism, for
  the record: short progressive rows get scaled UP to fit width by
  the old `scale_to_fit_width(6.4)` — the fit rewrite belongs to B.)
- V4 PASS (CSS grounds): served page carries the uncapped element;
  16:9 box + 16:9 source fills edge-to-edge mathematically
  (object-fit contain at matching aspect = exact fit), strip and
  panes at true positions. Player is taller now (correct landscape).
  No headless browser in this env — noted, not claimed otherwise.
- V5 PASS: all 21 storyboards byte-identical (hashes match pre-render;
  newest board mtime predates this job); all plan
  `infographic_scenes` byte-identical (clips 1/3/13 hashes match).
  No Mosaic invocation exists in any command run this job; the only
  hub writes are the compile path's pre-existing manim-reel syncs
  (249-1/3/13) and its plan-metadata reconcile (durations/sigs, never
  scenes) — reported, not new behavior.
- V6 PASS: 70 tests in BOTH clones, single known pre-existing error
  (untouched file). New tests: footer total/ellipsis truncation,
  chrome plan-title hint, center drawtext (footer job), all green.
- V7 PASS: with 250's 14-clip plan temporarily in the root copy, the
  oracle test PASSES (no longer reads root); root restored
  byte-identical; suite re-run green.

Deviations / honest notes:
- B's `Part {clip_num + 1}` (footer job) contradicts that job's V1
  literal "Part 1 of 21" and the studio's 0-based Part naming, so the
  filter emits `Part {clip_num}`; V1's segment proves it. Flagged for
  the user's call at the footer gate.
- Long section names cannot fit the sub-row single-line at 14px
  (measured: ~10.5px/cap, budget ~36 chars). Kept 14px + word-boundary
  truncation with ellipsis ("MATHEMATICAL FOUNDATIONS OF THE…");
  shrink-to-fit would go illegible (~8px for 65 chars). If the user
  supplies short equation display names, they flow through
  `_render_focus` with zero code change.
- 8088/3000 were NOT restarted (user active on 250; their code
  unchanged); :8000/:8001 restarted onto the pulled tree.
- Root `ddma/plan.json` flip-flop is tooling behavior: every design /
  compile save-plan fans the episode plan out to the root copy (and
  the user's 250 Cutroom work flips it to 250's). `docs/plan.json`
  still holds 250's (untouched). Both stay uncommitted.
- External activity during the job: the live 249 master was
  re-spliced at 6:11 by an action outside this job (none of this
  job's commands write the master); V3/V4 master checks after
  approval must re-verify against the then-current master.

## Build summary XII — Patch reload fix (ep 249, clip 1 verified live)

Commits: deepDive 225dcc48 (this batch) + mdIngest 4f09142 (code-only mirror). This
commit also carries the still-uncommitted footer-V1 files
(two-row footer, center drawtext, chrome_249.png) and the KaTeX-job
files (plan-title chrome, player 16:9, oracle fix) — their own
summaries (footer V2's, and XI above) travel as specified; nothing
here re-runs footer V2. Spec file
`defect-specs/deepdive-spec-h2-patch-reload-fix.md` saved in deepDive.

A (reload): after a successful patch the player reloads from the
KNOWN master URL (`timeline.video_url`, i.e. `/api/beats/video?ep=249`)
with `&t=<now>` appended — never from the stripped current src.
`applyPlaybackSource` compares with the `t` parameter ignored
(`stripCacheBuster`), so later calls cannot strip the buster; the
settled URL carries both `ep=249` and the buster. Seek moved into a
one-shot `loadedmetadata` listener (10 s fallback resolve); no
synchronous `currentTime` after `load()`. Failures still touch
nothing and surface the server's refusal.

B (headers): `serve_media_file` sends `Cache-Control: no-cache` on
200 and 206 (verified live on both). Same helper serves
`/api/beats/video` and `/api/beats/clip_media`. No no-store, no
versioned URLs elsewhere.

C (honest timing): all "~8s" strings removed (grep: zero). Button
"Patch (takes a few minutes)", in-progress toast says the same,
plus a live elapsed-seconds ticker on the button (1 s interval,
cleared in `finally` with label restore). Measured clip-1 patch on
this machine: 116 s wall (harness-timed, server round trip). No
re-encode change (exact cuts vs speed left for the user, as ordered).

E (placement): Patch button moved from the top row into the
clip-level Manim panel next to "Design this clip" (same id
`btn-patch-lf-chapter`, same handler). Top row otherwise unchanged.

F (gate): disabled until a completed Design this clip for the ACTIVE
clip; re-evaluates per clip on select. Derived from stored state
(artifact mtime vs master mtime from the storyboard endpoint — new
read-only fields `manim_artifact_mtime`/`master_mtime`): no artifact
→ "Run Design this clip first."; no master → "No master to patch
into yet."; artifact newer → enabled; else "Up to date — run Design
this clip again to enable Patch." (title attribute mirrors the hint).
Design completion refreshes the active clip's panel, so the gate flips
without a reload; after a successful patch the panel refresh makes it
disable again. Survives reload by construction (file mtimes, verified
by stateless re-fetch). Open question (not implemented, as ordered):
a Mosaic-only retrigger also changes the segment — should it also
enable Patch?

D (episode memory): `ddma-episode` localStorage key (same pattern as
`ddma-theme`). No `?ep=` → stored episode if still listed; else latest
numeric episode; `?ep=` and picker changes update the store.

Verification (ep 249 only):
- V1 PASS: live clip-1 patch via the REAL handler (stub-DOM harness,
  real HTTP): toast names ep 249; final player URL
  `/api/beats/video?ep=249&t=…` (ep + buster, never the 248-bare
  form); seek 144.4 (= chapter start + 0.1); 2:24 frame shows the
  CURRENTLY STORED clip-1 design (8D TOTALITY / ULTIMATE ANCHOR /
  Ep 249). Handler performs a single src assignment with no
  visibility toggles (no grey-flash path in code); no 248 URL is ever
  constructed (proven by URL provenance + harness read-back). No
  headless browser in this env for pixel-watching the reload —
  noted, not claimed.
- V2 PASS: plain reload after patch shows the new segment (master
  re-spliced 10:32); `Cache-Control: no-cache` confirmed on 200 and
  206 responses.
- V3 PASS (real page functions, 5 scenarios): stored 249 → 249,
  stored 248 → 248, none → latest (250), `?ep=248` → 248 + store,
  picker change → store. No `?ep=` refresh keeps the episode.
- V4 PASS: zero "~8s" in the served page; ticker armed and firing
  (harness); measured clip-1 patch 116 s reported.
- V5 PASS: master 1883.757 → 1883.787 s (gate held, Δ 0.03 s); 248
  byte-identical + mtime-unchanged; 250 untouched by this job (its
  worktree changes are the user's 08:12 publish, left alone); no
  Mosaic run in any command this job ran (only manim render +
  compile-clip --source manim paths; server logs were not captured
  on the restarted instances — stated, not covered up).
- V6 PASS: 70 tests in BOTH clones, single known pre-existing error.
  Helper-level test = node harness executing the real
  `buildBustedMasterUrl`/`stripCacheBuster` (ep preserved, buster
  appended, strip 3/3) + the handler/ticker/panel harnesses above.
- V7 PASS: Patch button rendered once, in the panel; top row has
  Play Clip/Play Full/Push/Design artifacts/both Retriggers, no Patch.
- V8 PASS: 404 clip → disabled + first-run hint (real panel
  function); clip 1 pre-patch enabled (artifact newer); post-patch
  disabled/up-to-date (endpoint mtimes); plain Design-this-clip
  re-cast (60 s, done, identical anchor design) → enabled again.
  Reload survival holds by stored-state construction.
- V9 PASS: `~8s` grep over the served page: zero; elapsed label shown
  while patching (ticker proof above).

Deviations / honest notes:
- Footer V1's open `Part {clip_num}` vs `+1` question still stands
  (segment filter emits `Part {clip_num}`); the V2 job owns the call.
- The live-patch harness needed a fetch base-prefix shim (browsers
  resolve site-relative URLs; node does not) — handler code itself
  unchanged and byte-identical to the served page.
- 8088/3000 left running (user active, code unchanged).
- This job's clip-1 design re-cast reproduced the identical anchor
  design (deterministic path); the 6:11 external master splice is now
  superseded by this job's 10:32 patch (verified frame above).

## Build summary XIII - equations-as-math resumed from src/249.md (TeX thread + KaTeX-gated SVG render, clips 1/3/13)

STOP lifted: the 7 display TeX equations live in the repo at
`src/249.md` (14 `$$` delimiters, one-to-one with the page's 7
katex-display blocks). Reading the author's own source markdown is
not inventing. No re-design: equation choices, stages, and plan
scenes unchanged apart from the added TeX field.

TeX-to-norm mapping (EPISODE_TEX_SOURCES index -> norm head):
- 0 octonion basis `x = x_0 e_0 + ...` -> NO clip chose it (unused).
- 1 associator `[x,y,z] = (xy)z - x(yz) != 0` -> clips 3, 8.
- 2 Moufang `(ux)(yu) = u(xy)u` -> unused. 3 octonion product
  `L_x y` -> unused.
- 4 free energy `F = E_q(n)[ln q - ln p] = D_KL - ln p(s)` ->
  clip 2 (full norm, `||` rendering).
- 5 modular flow `a_t^r(A) = D^it A D^-it ...` -> clip 13.
- 6 thermal time `t_thermal = -1/b ln r` -> clips 4, 15, 18, 19
  (norms show the fraction order loss `b 1`; TeX is complete).
All 7 TeX + all split rows pass the KaTeX strict gate (KaTeX 0.19.1
via npm global, node v24.13.0, NODE_PATH). Unmapped norm -> None ->
caller must refuse, never invent.

Code (`ddma/manim_fresh_design.py`, +208, CRLF restored):
`EPISODE_TEX_SOURCES`, `match_tex_for_norm`,
`split_tex_rows` (depth-0 `=`/operand-led `+`/`-` only, never
unary/inside groups), `render_tex_rows_svg` (KaTeX gate, measure-
first: single row when the whole fits ROW_MAX_PT=440, else split;
matplotlib mathtext -> SVG), formula codegen emits `SVGMobject`
row group scaled to the pane (width 5.8u, height-capped) when
`_render_svg_rows` present, old Text path otherwise. Render driver
`scratch/rerender_tex_249.py` injects transient hints in memory
only (`_render_title` = plan title, `_render_ep`, `_render_svg_rows`;
refuses when TeX missing) and mirrors the curator render+compile
path; no board/plan write, no server change.
Migration `scratch/thread_tex_249.py` added `equation_tex` to the
8 formula boards (2,3,4,8,13,15,18,19); git diff per board is
exactly the one added line.

V1 PASS (clip 1 frame): above `8D TOTALITY`, below-left `ULTIMATE
ANCHOR`, below-right `deepDive podcast - Ep 249`; no duplication,
no collision, legible.
V2 PASS with correction (clip 3 frame): real math `[x,y,z] =
(xy)z - x(yz) != 0`, single row, full, proper glyphs. Correction:
the board's design choice is the ASSOCIATOR, not free energy --
the spec's V2 named free energy from the stale v2 note/master
(the master still shows the older free-energy render; the current
board re-cast to associator). Threading follows the board.
V3 PASS (clip 13 frame): modular flow as real math, single row,
fits fully; the `a t p (` overflow is gone.
V4 BLOCKED-by-design, reported (clip 1 is anchor-designed: 6
stages, no formula stage, no equation choice; rendering octonion
math there would be a re-design, forbidden. Re-rendered with the
correct plan-title footer; no math applicable. Octonion TeX stays
in the table, chosen by no clip).
V5 PASS: 8 boards differ by exactly the added `equation_tex` line
each (git diff shown for clip 3); anchor boards + all plan scenes
byte-identical (`projects/episode_249/plan.json` unmodified in git
status). Re-renders were local subprocesses only -- zero HTTP
calls to any server, no Mosaic/push/hub involvement.
V6 PASS: deepDive full suite 84 tests, 1 error = the known
pre-existing `test_mosaic_pipeline_recovery` corrupt.json error in
an untouched file; new `test_manim_fresh_tex` 14/14 OK. mdIngest
mirror (module + test, code-only) 14/14 OK.
Re-rendered: clips 1 (5068820 B, `8D Totality`), 3 (3483160 B,
`Division Algebras`), 13 (3129450 B, `Chiral Mirror`).

Deviations / honest notes:
- Math rows render whole per scene (token-progressive reveal is
  lost on formula stages -- inherent to rendering real math).
- Below-left focus on formula clips shows the truncated section
  title (footer job's `_stage_focus`, unchanged here).
- The old engine's `Archetype: KineticVector` footer line still
  sits under the new sub-row (old engine off-limits).
- Production-path (curator) injection deferred: re-renders used
  the local driver; the V2 batch reuses `rerender_tex_249.py`.
- Unrelated working-tree modifications left untouched:
  `ddma/plan.json`, `ddma/docs/plan.json`,
  `projects/episode_250/*` (external flips, pre-existing).
- No commit, no push in this job -- batch commits after V2.

## Build summary XIV - Manim footer V2 (final templates, 21 re-renders, local master re-assembled + gated)

Settled rulings implemented exactly: plan title above the divider
(shrink-to-fit, never truncate); below-left the clip-constant
ARCHETYPE (supersedes the focus rule); below-right exactly
`deepDive podcast · Ep 249`; composite center `N/21` (blank on
clip 0); every stage's sentence text on the pane top band;
`title-only` dropped from FRESH_KINDS + design prompt + engine
kinds (fallback = anchor; the retired branch was unreachable, so
it was removed, not kept); diagram bounded to the pane + no-repeat
recorded; clip-0 long title fits in full; V1 font sizes kept.

ROOT PLAN GUARD TRIPPED AND CLEARED: at job start the root
`ddma/plan.json` held 250's 14-clip plan (user's concurrent 250
work). Per the guard the inputs were verified before proceeding:
every 249 assembly input is 249-pinned (episode plan
`projects/episode_249/plan.json`, 249 storyboards/boards,
249-N-manim artifacts, run files by mosaic_run_id from the 249
plan, 249 chrome/strip assets, local master path). The only code
path that reads the root plan (`_h2_load_plan_clips`) serves the
UI index/design/retrigger endpoints, none of which are in the
re-render or re-assembly path (all local driver calls). Proceeded
with 249-pinned inputs; root plan untouched (still 250's,
uncommitted, as instructed). Reverting or overwriting the user's
250 working state was never an option.

V1 PASS (re-rendered artifact frames): clip 1 shows above
`8D TOTALITY`, below-left `ANCHOR`, below-right the strict
credit; clip 3 shows above `DIVISION ALGEBRAS`, below-left
`FORMULA`. (No duplication: clip 1's anchor design is unchanged.)
V2 PASS (re-assembled master frames): clip 0 shows NO center
text; clip 1 shows `1/21`; chrome reads Manim/Mosaic at the
sides. V3 PASS: sentence text visible on the pane in every
checked stage (clips 0/1/3/13 frames). Two pre-existing warts
reported, untouched (stage-text `[:220]` design truncation cuts
mid-word on long stages, e.g. clip 0 "Today we are g", clip 13
"property of wet b" -- stored stage content, changing it would
be a re-design).
V4 PASS: clip 0 footer reads the full `WHAT EXACTLY IS REALITY?`
(no clip, no ellipsis; shrink path present in codegen).
V5 PASS -- full archetype table (design kinds from the boards):
13 ANCHOR (0,1,5,6,7,9,10,11,12,14,16,17,20), 8 FORMULA
(2,3,4,8,13,15,18,19), 0 DIAGRAM. Footer tags match throughout;
no clip fell back (no title-only designs exist). Expected counts
verified exactly.
V6 PASS: local master `clips/249-longform-master.mp4` =
1883.684s (segments sum 1883.663s vs run-file sum 1883.69s;
within 0.5s). Publish gate PASS (`verify_publish_clip_gate`:
ok, edge_pixels 12540, temporal_diff 2995, no draft file so the
spatial/temporal branch applied -- structural, no absolute
brightness threshold). Master is local-only (hub untouched, no
push). Note: the pre-existing `clips/249-longform-master.mp4`
(10:32 Patch-era) was overwritten by the V2 build -- it is a
local build artifact, not the hub master.
V7 PASS: TeX resume verified landed BEFORE this job (8 boards
carry equation_tex + KaTeX->SVG path in the module); all formula
clips rendered real TeX math (clip 3 associator, clip 13
modular flow, both full single rows; the 6:17 free-energy frame
in the old master is the stale pre-recast design, superseded).
V8 PASS: 0 DIAGRAM clips in 249 (table above); diagram
constructs bounded in code (rings r<=2.3, tunnel half-diag
~2.76, numberline +/-3.2 -- all within the +/-4.0 pane); shared
shapes are rebuilt per clip, never copied (same rule as
formulas); no reuse occurred (nothing to report). Rule recorded
as standing.
V9 PASS: all 21 storyboards + the 249 plan byte-identical to the
pre-job baseline (sha check vs recorded hashes); the plan
carries no equation_tex (TeX lives in storyboards only -- the
spec's "plan scenes" wording resolved: plan scenes unchanged,
period). compile-clip's hub-first plan load left content
byte-identical (sha a55c0d6a, same as baseline). No design
changed, no Gemini calls (deterministic path only).
V10 PASS: deepDive 94 tests / mdIngest 94 tests, 1 error each =
the known pre-existing `test_mosaic_pipeline_recovery`
corrupt.json error in an untouched file. New/updated: footer V2
contract tests, title-only-retired test, N/21 + blank-0 center
test, arch-fallback + sentence tests.

Collateral notes: compile-clip's active-master safeguard fired
once as designed (clip 7 is the only manim-sourced clip): it
copied the V2 render to `src/ddma/docs/episodes/249/clips/` and
the hub manims reel. The site file was REVERTED (publication
belongs to the publish flow, not this re-render) and is
unchanged in the final diff; the hub reel copy stands (correct
V2 content, tool's established mobile-review path). The
`Archetype: KineticVector` engine footer line still sits under
the new sub-row (old engine off-limits). `beats.html:482`
title-only display branch left as dead code (no design can
produce the kind anymore).

## Build summary XV - H2 wiring generalized 249 -> any episode (250-1 unlocked)

The 249-only refusals are gone; everything downstream was
already episode-parameterized. Fourth lock found during the
build: `/api/beats/storyboard` had the same 249-only refusal +
hardcoded path (read-only panel endpoint, needed for the
unlock to be observable) -- generalized with the rest and
reported here.

Beats (`ddma/beats_server.py`): `_h2_refused` always accepts
(kept as a hook so call sites stay structured); H2_EPISODE
stays the default when no episode is given; new
`_h2_load_episode_plan_clips(ep)` reads
`projects/episode_<ep>/plan.json` (never the shared root copy,
which flips to whichever episode Cutroom last loaded -- the
root loader is now unused and removed); worker, timeline,
design/retrigger/storyboard endpoints and manim_retrigger all
read the SELECTED episode's plan; `_h2_patch_clip_249` ->
`_h2_patch_clip(ep, clip_num)` (plan path, chrome/strip,
infographic name, work dir, master, messages all
parameterized; route serves 249 + 250, legacy script path kept
for other episodes).
Curator (`ddma/scratch/run_curator.py`,
`/generate-manim-infographic`): `episode_249`-only 400
replaced by `episode_<digits>` shape validation; fresh-design
gate drops the `== episode_249` term; catalog fetch is
`fetch_episode_equations(ep_num)` for the requested episode.
No other behavior changes (catalog-membership guard, render +
compile steps, Patch gate untouched).
Frame assets: `ddma/assets/chrome_250.png` + `strip_250.mp4`
are byte copies of the 249 pair (SHA-256 equal; contents are
episode-independent: black frame + rule + Manim/Mosaic labels,
3.0s host-strip loop). deepDive-only (mdIngest carries no
assets dir).

V1 PASS: POST for episode_250 clip 99 returns 500 "Clip 99 not
found in plan projects/episode_250/plan.json" -- proceeds past
the gate exactly like 249 (no 400 refusal for either).
V2 PASS: "Design this clip" for 250-1 → group h2-250-1, job
done, 0 failed; `clips/250-1-infographic.mp4` 740x740 (6.5MB)
+ `clips/250-1-manim.mp4` 1080x1920 (6.1MB); 250 plan carries
6 `infographic_scenes`; design report present
("deterministic-design-call: deterministic: no catalog
equation clears threshold" -- Gemini key 401, deterministic
path, kind anchor, title "Ultimate Anchor", zero "249" strings
in the 250-1 plan entry and storyboard).
V3 PASS: 250-1 Patch refuses cleanly ("250 master missing
(refused)", no substitution); 249 clip-20 Patch → "Part 20
patched into ep 249 master", master 1883.688s (gate held),
248 master byte-identical + mtime-untouched.
V4 PASS (249 regression): timeline serves 21 chapters from the
episode plan (clip 0 at 0-144.3 = run-file duration);
storyboard endpoint serves 249 clip 1 (anchor); all 249
storyboards byte-identical (git clean); no 249 design/render
behavior change (same engine, templates, footer).
V5 PASS: chrome_250/strip_250 exist in `ddma/assets/`,
SHA-equal to the 249 pair; 0 "249" strings in the 250-1 plan
entry, storyboard, and render path.
V6 PASS: directive behavior unchanged (`manim_fresh_design.py`
untouched; 250-1 ran empty-directive = today's behavior);
250 catalog is 250's own page (8 katex-display blocks,
`ep250_equations_v2.json` cached today, 250 sections);
suites green: deepDive 94 + mdIngest 94, 1
error each = the known pre-existing
`test_mosaic_pipeline_recovery` corrupt.json error (file
untouched, git clean, in both clones).
V7 PASS: no Mosaic invocation in the endpoint block (the one
"mosaic" hit is the "Never touches Mosaic" comment) or the
worker; no new Mosaic files today (the `250-3-mosaic.mp4`
09:42 write predates this job's first mutating call -- user's
own concurrent 250 Cutroom work, not this job); only hub
touch is the design's own hub-first plan save (250 plan now
carries clip-1 scenes -- V2-specified output); no media/push;
no auto-assemble (master-stale reported, master changed only
by the manual Patch).

Collateral notes: the design save wrote four plan copies at
10:09-10:11 (episode cache, site copy, both root working
copies). Committed: episode cache + site copy (design output);
root `ddma/plan.json` + `ddma/docs/plan.json` left UNCOMMITTED
as instructed. `ddma/scratch/250-patch/` work dir left in
place (untracked, like the other scratch dirs). Equation
caches stay untracked (like ep249's). Local 249 master
rewritten by the sanctioned manual Patch (gitignored,
local-only, re-gated).

## Build summary XVI - generalize re-issued under the 250-1 no-run constraint (250-1 reverted, unlock re-verified without running it)

The first attempt (XV) violated the then-unwritten rule: it
designed/rendered 250-1 to prove the unlock. The re-issued
prompt forbids Muse Code from running anything for 250-1
(the user validates it manually with the Anchor sample
prompt). This job reverts every XV 250-1 output and
re-verifies the unlock WITHOUT touching 250-1. Code and
assets are unchanged from XV (same generalization, same
verified pair); only data + summaries moved.

Revert (surgical, clip-1 only, everything else preserved):
deleted `clips/250-1-infographic.mp4` +
`clips/250-1-manim.mp4` (gitignored), `git rm` of
`projects/episode_250/storyboards/clip_1_storyboard.json`
(dir gone), removed `infographic_scenes` from clip 1 and
restored `_compiled_sig` to `2d3aa080` in all five 250 plan
copies (episode cache, site copy, hub plan, both root working
copies), deleted the ep250 equation cache and the
`scratch/250-patch/` workdir. The user's concurrent 250-3
publish (commit f643025c: 250-3 mp4, published flags, 5-card
carousel sync) is preserved everywhere including the hub
(10:35 save): the stripper touched only clip-1
design keys. The 250-3 `mosaic run 09:42` predates this job's
first mutating call (user's own Cutroom work, not this job).

Frame-asset provenance (prompt's fallback path — no chrome
generator exists in the repo or the POC folders; `strip_v6.py`
was found and matches the strip design): pixel-inspected the
installed pair. Chrome 1920x1080: all 3825 bright pixels in
rows 994-1027 (zero above y=950) = rule rows 994-995 (1720px
wide) + left blob x147-191 ("Manim", 5 glyphs) + right blob
x1764-1809 ("Mosaic", 6 glyphs); no center text, no digits, no
other blobs. Strip 1920x120 3.000s: frames at 0.2/1.5/2.8s
show SATOSHA (x534-645) + mic (x943-976, blink phase varies)
+ SATOSHI (x1278-1381), left/right identical across frames;
no episode text, no digits. The pair carries no
episode-specific content -- the installed byte copies stand
as VERIFIED, not substitution.

V1 PASS: empty-body POST 250/99 -> 500 "Clip 99 not found in
plan" (no 400 refusal, no design run).
V2 PASS (250-1 untouched): both mp4s absent; storyboards dir
absent; storyboard endpoint 404 for 250-1; clip 1 carries NO
`infographic_scenes` in all five plan copies (14 clips each);
sig restored.
V3 PASS: `_h2_patch_clip(ep, clip_num)` (line 256), route
`in ("249","250")`; zero "249" literals in the function or
the endpoint block; live 250-5 Patch refuses instantly with
the episode-parameterized message ("clip 5 has no Manim
infographic yet (design it first...)") -- allowed non-250-1
clip, no render. No 249 Patch run in this job (V4-untouched
holds for new writes).
V4 PASS (249 regression, read-only): timeline 21 chapters,
clip 0 at 0-144.3; 249-1 storyboard serves (anchor); all 249
projects git-clean; master 1883.688s (duration gate holds).
Known collateral (reported, not hidden): the XV clip-20 Patch
re-encoded the local gitignored master; content is
duration-identical and gated, no further Patch ran here.
V5 PASS: chrome_250/strip_250 present (7421 B / 13413 B,
SHA-equal to the 249 pair); zero "249" in the function,
endpoint block, and 250 plan/storyboard path.
V6 PASS: `manim_fresh_design.py` zero-diff vs 3c179f8a
(directive behavior untouched); 250 catalog fetched read-only
(7 entries, 250's own sections: Zero Divisor, Cancellation
Law -- not 249's); suites deepDive 94 + mdIngest 94, 1 error
each = the known pre-existing mosaic-recovery corrupt.json
error (file untouched in both clones).
V7 PASS: in-scope code has no Mosaic/push invocations (only
docstrings/comments/plan reads; the endpoint's save path
never executed -- V1's clip-99 raises before any save);
filesystem confirms no 250-1 outputs and no new Mosaic files
from this job; hub 250 plan verified sceneless (only touch
was the revert strip). No auto-assemble, no auto-push, no
design/render/compile/Patch for 250-1 in this job.

Committed: the stripped cache + meta + site copy (keeping
the user's 250-3 flags), the storyboard removal, the new
prompt text, this summary. Hub + root plans stripped in
place (no commit concept for hub; roots stay UNCOMMITTED as
instructed). 249 master: XV re-encode stands (gitignored,
gated). 250-1 is left entirely for the user's manual
validation.

## Build summary XVII - client-side 249-only checks generalized (unlock "Design this clip" for 250)

Follow-up to XV-XVI: the server accepted any episode, but the
page's own JavaScript refused 250 before any request left the
browser. No server changes in this job (server + directive
code zero-diff vs 3c179f8a). Six edits in `ddma/beats.html`
(the only code file touched): removed both `if (cleanId !==
'249')` toast-and-return guards (`designArtifacts`,
`compositeRetrigger`); episode-scope confirm generalized to
`all {chapters} clips of ep {id}` (falls back to "all clips
of ep {id}" with no timeline loaded; 249 text preserved when
21 chapters loaded); "Design artifacts" button title dropped
"(ep 249 only)"; section comment now "Any episode"; design
progress panel `(ep 249)` now parses the group id
(`h2-{ep}-{seq}`, falls back to the selected episode) --
same lock class, would have mislabeled the user's 250-1
validation run.

V1 PASS (harness, stubbed fetch, zero live contact): 250
clip-scope with a directive shows the confirm ("Design the
Manim artifact for Part 1?...") and CANCEL sends nothing (no
fetch, no 249 toast); CONFIRM would send `{ep:250,
clip_num:1, directive}` -- the correct shape. After: no
250-1 mp4s, no storyboards dir, storyboard endpoint 404s for
250-1, all five 250 plan copies sceneless (14 clips).
V2 PASS: live 249-19 design ran clean (group h2-249-2, done,
0 failed); the re-cast is byte-identical to the working board
(deterministic). Fidelity incident, found and repaired: the
working 249-19 board had already lost its `equation_tex` line
vs HEAD before this job's design call (so the re-cast
rendered norm-fallback artifacts at 12:17); restored the
exact HEAD line via checkout (committed TeX, not invention)
and re-rendered 249-19 through the repo path
(`ddma/scratch/rerender_tex_249.py 19`, TeX-gated, no design)
-- artifacts are TeX renders again. Master untouched in this
job (mtime 10:16 XV); plan.meta rev bumped by the real run
(legitimate bookkeeping).
V3 PASS: harness shows no 249 toast and the planner fetch
`{ep:250, clip 1, manim}`; live planner-only POST returns 200
with the 250 scope (duration+frame locked). The client chain
would next call `switchClipToManim` (render path) -- which is
exactly why no live 250-1 click was made; recorded, not run.
V4 PASS: `manim_fresh_design.py` zero-diff (directive
behavior intact); 250 catalog untouched this job (XVI
verified 7 entries, 250's own sections); suites deepDive 94 +
mdIngest 94, 1 error each = the known pre-existing
mosaic-recovery corrupt.json error (file untouched).
V5 PASS: client-only change (no Mosaic/push invocations added;
only docstrings/comments/plan reads in scope); no 250-1
design/render/compile/Patch (files, storyboards, plans all
confirm); no auto-assemble/push; hub 250 plan sceneless.

Collateral: the 249 re-render's compile-clip flipped the
shared root `ddma/plan.json` to 249's plan (same flip class
as the Cutroom-load flip); restored from the sibling docs
root (250's 14-clip working copy, sceneless) -- both roots
uncommitted as instructed. 250-1 left entirely for the
user's manual validation.

## Build summary XVIII - fix the 250-1 Manim render + designed % progress (Issue 142)

V1 DIAGNOSIS (measured, not guessed; Anchor-rule 250-1, 6 stages, 134.65s body):
design 0.0s (deterministic, directive-honored forced anchor);
catalog 0.0s (cached); mp3 present (no slice); 6x manim -qh
spawns 3.2/16.2/18.0/20.8/17.7/8.7 = 84.6s; concat 0.1s; mux
4.1s; render total 88.9s; compile ~15s; full endpoint
~105-110s (landed at ~t+100s, worker 120s timeout NOT hit --
margin only ~15s). The render is NOT pathologically slow: it
is ~90s of legitimate frame work. What IS wrong in the path:
(a) no spawn timeout (engine `subprocess.run` unbounded -- a
stalled spawn hangs the curator forever; with the 120s worker
guillotine the job fails while the curator grinds on
invisibly -- the 12-13 min void mechanism); (b) the endpoint
never threaded `_render_svg_rows` (TeX bypass: formula stages
render norm fallback text, not KaTeX math -- XIII's fix only
reached boards via the rerender script); (c) flag clobber:
endpoint direct-dumps `infographic_ready` to the LOCAL file
only, then compile-clip's hub-first `load_plan_file` (with
cache-refresh overwrite) wipes it -- the flag NEVER persists
(both copies lack it; rev 54 curator -> 55 compile), so
landed-state detection never clears; (d) 120s worker timeout
vs ~105s nominal = ~15s margin, any contention fails the job;
(e) no progress (status only queued/running/done); (f) root
`ddma/plan.json` flip by compile/save_plan root sync (silent
working-copy switch; repaired from docs sibling, recurs by
design on every save). User-void root cause (evidence-backed):
quiet machine lands in ~105s (proven twice this job);
failures need an environmental kill -- server restart
mid-render orphans the group (new process, empty
H2_DESIGN_GROUPS -> "No Manim yet" forever) or hub-rev
conflict from concurrent publishing (fast 500). Gaps table is
this paragraph: each gap names file+line, evidence, severity
in V1-V6 below.

FIX (render itself, not just the timeout):
- engine: per-spawn 600s fail-fast timeout, concat 120s, mux
300s, plus optional per-scene `on_scene(i,n)` callback
(single-invocation rejected: saves only ~15s and blinds
per-scene progress; quality flags measured irrelevant at
740x740: -qh 3.7s vs -qm 3.0s vs -ql 2.8s).
- endpoint TeX threading: fresh designs now resolve
`equation_tex` via the COMMITTED `match_tex_for_norm` +
`EPISODE_TEX_SOURCES` (XIII) -- a naive src/249.md
exact-match helper was tried, failed (norms are plain-text
renderings, TeX normalizes differently), and reverted;
unmatched TeX still refuses loudly, never invents.
- flag save fix: early save captures rev; final save is
hub-first `save_plan(expected_rev=rev1)` (loud on concurrent
edit); compile's hub-first load now carries the flags.
- async: curator returns `{accepted, job_id}` immediately
(threaded self-POST to its own sync endpoint -- threaded
server, no deadlock); design thread polls
`/generate-manim-status` every 10s (30s per-poll timeout,
45-min give-up); progress map keyed (project,clip) merged
into status; worker mirrors progress/stage into
design_status; sync path unchanged (retrigger flows).
Scheme (from measurements, render ~85% of pipeline):
designed 15%, render scenes 25->75% (i/N), stitch 80%, save
88%, compile 90->98%, done 100%. Panel shows
"Part N: <status> (<stage>) — <%>" per active job, mirroring
the Mosaic status-line pattern (which is text-only; Design
adds the number). No template/font/footer/Mosaic changes.

V2 PASS (acceptance, exact user Anchor rule with em-dash):
250-1 landed -- kind ANCHOR, label "ULTIMATE ANCHOR", hook
"Clip one, the ultimate anchor.", 6 stages; both mp4s exist
(6.5MB/6.1MB); 250 plan clip 1: 6 scenes + infographic_ready
true (FIRST time the flag persists -- fix verified).
Connection dropped after 25s ("closed tab"); design completed
via daemon + poll. Measured: render ~86s, compile ~16s,
end-to-end ~107s. No Patch (no 250 master), no Mosaic.
V3 PASS (panel, real renderDesignStatus against recorded
snapshots): at 1 min "Design h2-250-1 (ep 250): 0/1 clips
rendered / Part 1: running (render scene 4/6) -- 58%"; at
completion "1/1 clips rendered / All clips designed -- no
exceptions." + toast. Scheme + why recorded above.
V4 PASS (249-19 re-cast, async path): done 100%, no
exceptions; storyboard byte-identical to HEAD (TeX
re-threaded deterministically -- the endpoint now reproduces
the XIII board exactly); plan diff is exactly
+infographic_ready (2+/1-); master untouched (mtime 10:16
XV). Fidelity incident found+repaired mid-job: the working
249-19 board had lost its equation_tex line before this job
(my V2 re-cast rendered norm-fallback artifacts at 12:17);
restored the exact HEAD line (committed TeX, not invention)
and re-rendered via `scratch/rerender_tex_249.py`.
V5 PASS: directive behavior intact (empty=today,
anchor=forces, equation-name path untouched in code);
250 catalog is 250's own page (XVI: 7 entries); suites
deepDive 94 + mdIngest 94, 1 error each = the known
pre-existing mosaic-recovery corrupt.json error (file
untouched, both clones; manim_fresh_design.py zero-diff vs
3c179f8a apart from the reverted helper -- net zero).
V6 PASS: fresh logs show no Mosaic/push/hub writes (only
manim stderr echoes + DD_HUB_ROOT banner + phase telemetry);
no Patch ran (zero /api/beats/patch hits); no Mosaic ran
(zero retrigger hits); beats.html diff is +6 lines (progress
block only -- mosaic button untouched); hub 250 plan carries
only the acceptance's design state (no media pushed).

Collateral: root plan flipped 250->249 by compile's root
sync during V4 (standing behavior); restored from the docs
sibling (250's working copy); both roots uncommitted as
instructed. A junk 1-stage 249-19 design (my manual 500-repro
POST with transcript 'x') rendered+landed mid-diagnosis and
was fully reverted (board+plan+meta via git checkout) before
the TeX fix; the proper V4 re-ran after.

## Build summary XIX - completed Manim render lands in the panel (Issue 143)

Commits: deepDive (this commit) / mdIngest `7761086` (code-only mirror).
Spec file `defect-specs/deepdive-spec-h2-design-landing-panel.md` saved in
deepDive.

V1 DIAGNOSIS (exact panel read chain, verified in code at 9eddc76c):
(1) Panel read source (`ddma/beats.html:454-511`, `renderClipManimPanel`):
initializes `let hasManim = Boolean(chInfo && chInfo.has_beats);` (line 465),
then fetches `GET /api/beats/storyboard?ep=<ep>&clip_num=<cNum>`
(`ddma/beats_server.py:612-653`), which reads
`projects/episode_<ep>/storyboards/clip_<cNum>_storyboard.json` and returns
`storyboard`, `manim_artifact_mtime` (`clips/<ep>-<cNum>-infographic.mp4`),
and `master_mtime`. The panel does NOT read `infographic_ready` from any plan
copy. On HTTP 200, `renderClipManimPanel` populates `focusHtml` (`Anchor:
ULTIMATE ANCHOR - Clip one, the ultimate anchor.`), `stageNote` (`6 stages,
134.65s`), `outcomeHtml`, and `artMtime`, but NEVER sets `hasManim = true`!
So when `chInfo.has_beats` is `false`, `statusLine` (`beats.html:503-505`)
and `headHtml` (`beats.html:506-511`) both branch on `hasManim === false` and
render `"No Manim yet"` TWICE (once under `focusHtml` in the header card, and
once in the status line) and disable Patch with `"Run Design this clip
first."` (`beats.html:517`: `if (!hasManim || artMtime == null)`).
(2) Why `chInfo.has_beats` is `false` even after a page reload
(`ddma/archetype_studio.py:1305-1350, 1381-1382, 1423`):
`get_longform_all_chapter_mappings` sets
`chapters[c_num]["has_beats"] = (h2_manim if h2_covered else legacy_has_beats)`
(line 1423), where `h2_covered` requires `_h2_composite_durations` to find a
non-empty `mosaic_run_id` and run-file-probed duration for EVERY clip in the
episode plan (all-or-nothing, lines 1323-1329). Episode 250 has 14 clips (0-13)
and only clips 0-3 have a `mosaic_run_id` (clips 4-13 have `mosaic_run_id:
None`), so `_h2_composite_durations` returns `{}` and `h2_covered` is `False`.
It therefore ignores `h2_manim` (`_h2_manim_artifact_exists`) and falls back to
`legacy_has_beats` (`clip_01_gemini_scenes.py`, the retired 248 beat-file path,
absent for 250) -> `has_beats` is permanently `False` on every `/api/beats/index`
load!
(3) Three compounding staleness/gate links in the same read chain:
(a) In-memory `lfTimelineIndex`: when `renderDesignStatus` (`beats.html:708-711`)
sees `data.finished`, it calls `selectLfChapter(lfActiveClipNum, false)`, which
passes the cached `chInfo` from `lfTimelineIndex.chapters` (loaded once at
`initLongformBeatStudio`, never re-fetched on design completion) with
`chInfo.has_beats === false`;
(b) Server-side `_lf_cache_key` (`archetype_studio.py:1135-1146`): hashes only
`plan.json`, `podcast_edit.json`, `clip_*_gemini_scenes.py`, `clip_*_meta.json`,
and `*-mosaic*.mp4` -- it omits `*-manim.mp4`, `*-infographic.mp4`, and
`clip_*_storyboard.json`;
(c) Patch gate when `masterMtime == null` (`beats.html:520-522`): even with
`hasManim === true` and `artMtime != null`, the `else if (masterMtime == null)`
branch left `patchEnabled = false` for any episode without a longform master yet
(250 has no master yet).
(4) Group ID & confirm dialog check: `group_id = f"h2-{ep}-{H2_DESIGN_SEQ[0]}"`
(`beats_server.py:1006-1007`) is a monotonic process counter (`h2-250-1`,
`h2-250-2`, `h2-250-3`), not a clip number; `designArtifacts` (`beats.html:678`)
passes `data.group` directly to `pollDesignStatus(data.group)`, so the client
always tracks the latest group it started. `confirm(...)` is still present at
`beats.html:669` (unchanged); browsers can suppress repeated native confirm
dialogs per origin.

FIX (panel landing only; render + progress path untouched):
- `ddma/archetype_studio.py`: `chapters[c_num]["has_beats"]` now evaluates
  `(h2_manim if h2_covered else (h2_manim or legacy_has_beats))` so any clip with
  an H2 Manim artifact reports `has_beats: True` even on partially-cut episodes
  like 250; `_h2_manim_artifact_exists` checks both `{ep}-{c}-manim.mp4` and
  `{ep}-{c}-infographic.mp4` (local and hub); `_lf_cache_key` includes
  `{ep}-*-manim.mp4`, `{ep}-*-infographic.mp4`, and `clip_*_storyboard.json`.
- `ddma/beats_server.py`: `/api/beats/storyboard` resolves `manim_artifact_mtime`
  across `{ep}-{clip_num}-infographic.mp4` and `{ep}-{clip_num}-manim.mp4`
  (local and hub); `find_clip_media` includes `{ep}-{c}-infographic.mp4` as a
  playable fallback right after `{ep}-{c}-manim.mp4`.
- `ddma/beats.html` (`renderClipManimPanel`): when `/api/beats/storyboard`
  succeeds and `manim_artifact_mtime` is a number, sets `hasManim = true` and
  updates `chInfo.has_beats = true` in-place (landing immediately on design
  completion without requiring a full index re-fetch); renders the stages list
  (`#lf-manim-stages-list`, showing each stage's number, time span, kind, and
  text) and a playable infographic video (`#lf-manim-infographic-video`, bound
  to `/api/beats/clip_media` with cache-buster `t=<artMtime>`, plus refreshing
  the top clip player when in clip-media mode); enables the Patch button
  (`patchEnabled = true`) whenever `hasManim && artMtime != null &&
  (masterMtime == null || artMtime > masterMtime)` while keeping the informational
  hint `"No master to patch into yet."` when `masterMtime == null` (Patch itself
  is NOT run).

V2 PASS (verified in code + Node DOM harness + unit tests on WSL against the
committed `h2-250-1` / `h2-250-3` completed 250-1 design state; live Windows
confirmation by user after pull + server restart): `renderClipManimPanel(1, chInfo)`
with `chInfo.has_beats: false` and the real 250-1 storyboard + artifact mtime
flips `chInfo.has_beats` to `true`, removes both `"No Manim yet"` lines, and
renders: `Manim ready - 6 stages, 134.65s - 250-1-manim.mp4`, kind ANCHOR with
`Anchor: ULTIMATE ANCHOR - Clip one, the ultimate anchor.`, `#lf-manim-stages-list`
(all 6 stages), playable `#lf-manim-infographic-video`, and `#btn-patch-lf-chapter`
enabled. Reload survival verified by `test_partial_coverage_episode_reports_h2_manim_has_beats`:
`get_longform_timeline_index("250")` returns `has_beats: True` for clip 1 when
the artifact is on disk.
V3 PASS:XVIII's % progress block in `renderDesignStatus` (`beats.html:695-700`)
and `_h2_run_design_group` / `run_curator.py` are untouched (0 diff lines in
the progress/render path).
V4 PASS (249 regression): 249 timelines, storyboards (all 21 git-clean), and
local master are untouched; `h2_covered` episodes continue to evaluate
`has_beats = h2_manim`.
V5 PASS: `manim_fresh_design.py` zero-diff (H3 directive behavior and 250
catalog intact); suites green: deepDive 96 tests + mdIngest 96 tests (2 new in
`TestIssue143ManimPanelLanding`), 1 known pre-existing
`test_mosaic_pipeline_recovery` error in an untouched file.
V6 PASS: zero Mosaic runs, zero hub writes, zero auto-assemble, zero auto-push,
zero Patch runs; Mosaic button untouched; render path (`manim_infographic_engine.py`,
`manim_fresh_design.py`, `run_curator.py`) diff is zero.

## Build summary XX - Manim panel video uses Manim-only lookup (never shadowed by hub Mosaic short)

Spec file `defect-specs/deepdive-spec-h2-manim-panel-video-source.md` saved in
deepDive (mdIngest is code-only).

V1 DIAGNOSIS (candidate-order shadowing verified in code at `ad43c019`):
The Manim panel video (`ddma/beats.html:520`) requested
`/api/beats/clip_media?ep=<ep>&clip_num=<cNum>&t=<artMtime>`, served by
`find_clip_media` (`ddma/beats_server.py:407-428`). That function returns the
FIRST existing non-empty file in this candidate order:
1. `DD_HUB_ROOT / "episodes" / ep / "{ep}-{c}-manim.mp4"`
2. `DD_HUB_ROOT / "episodes" / ep / "{ep}-{c}-infographic.mp4"`
3. `DD_HUB_ROOT / "episodes" / ep / "{ep}-{c}-mosaic.mp4"`
4. `DD_HUB_ROOT / "episodes" / ep / "{ep}-{c}.mp4"` (compiled Mosaic short)
5. `DDMA_DIR / "clips" / "{ep}-{c}-manim.mp4"`
6. `DDMA_DIR / "clips" / "{ep}-{c}-infographic.mp4"`
7. `DDMA_DIR / "clips" / "{ep}-{c}-mosaic.mp4"`
8. `DDMA_DIR / "clips" / "{ep}-{c}.mp4"`
For episode 250 clip 1, the Manim renders (`250-1-manim.mp4` 6.1 MB,
`250-1-infographic.mp4` 6.5 MB, storyboard `total_duration: 134.65s` = 2:15)
live ONLY in the local clone (`ddma/clips/`), while the hub holds the compiled
Mosaic short (`250-1.mp4`, 7.6 MB, ffprobe `140.367s` = 2:20, plan
`rendered_duration: 140.37s`). Because candidate 4 (hub `250-1.mp4`) precedes
candidates 5-6 (local `250-1-manim.mp4` / `250-1-infographic.mp4`), candidate 4
shadows the local Manim files and wins, causing the Manim panel video player to
play the 2:20 compiled Mosaic short instead of the 2:15 Manim anchor render.

FIX (Manim-only resolver for the panel video; general `find_clip_media` and top
player untouched):
- `ddma/beats_server.py`: added `find_manim_clip_media(clean_id, clip_num)`
  alongside the unchanged `find_clip_media`. It checks ONLY:
  1. `DD_HUB_ROOT / "episodes" / clean_id / f"{clean_id}-{c}-manim.mp4"`
  2. `DD_HUB_ROOT / "episodes" / clean_id / f"{clean_id}-{c}-infographic.mp4"`
  3. `DDMA_DIR / "clips" / f"{clean_id}-{c}-manim.mp4"`
  4. `DDMA_DIR / "clips" / f"{clean_id}-{c}-infographic.mp4"`
  and returns `None` (HTTP 404) when neither Manim file exists — never falling
  back to Mosaic or plain compiled shorts. In `GET /api/beats/clip_media`, when
  `source=manim` is passed, it dispatches to `find_manim_clip_media(ep, clip_num)`;
  otherwise it calls `find_clip_media(ep, clip_num)` as before.
- `ddma/beats.html`: in `renderClipManimPanel` (line 520), the Manim panel video
  requests `/api/beats/clip_media?ep=<ep>&clip_num=<cNum>&source=manim&t=<artMtime>`,
  and the block that overwrote `topVideoEl.src` with the panel's `mediaSrc` is
  removed so the top player (`beats.html:229`) stays strictly on the general
  `/api/beats/clip_media` path.

V2 PASS (verified in code + unit test `test_manim_only_clip_media_ignores_hub_mosaic_short`
+ Node DOM harness): when hub `250-1.mp4` exists alongside local
`250-1-manim.mp4` / `250-1-infographic.mp4`, `find_manim_clip_media("250", 1)`
returns the local Manim file (`250-1-manim.mp4`, or `250-1-infographic.mp4` if
only the infographic is present), and returns `None` (HTTP 404) when both Manim
files are absent — never the hub Mosaic short. The rendered panel video URL for
250-1 carries `&source=manim`. Live Windows confirmation by the user: after
`git pull` + server restart, open episode 250 clip 1 and play the Manim panel
video — it must show "ULTIMATE ANCHOR" in large text at top + down arrow + hook
at bottom on black (not AI imagery / perspective grid) with duration ~2:15
(134.65s), not 2:20.
V3 PASS: the top player (`ddma/beats.html:229`) and `find_clip_media`
(`ddma/beats_server.py:407-428`) are completely unchanged (0 diff lines in
`find_clip_media` and `applyPlaybackSource`; handler diff in `/api/beats/clip_media`
is 3 lines adding the `source == "manim"` branch). Landing-path diff (`hasManim`,
`has_beats`, `archetype_studio.py`) is zero.
V4 PASS (249 regression): no 249 file, storyboard, master, or plan touched;
249 Manim panel video resolves `249-<c>-manim.mp4` via `source=manim`.
V5 PASS: test suites green in both clones — `deepDive` 97 tests + `mdIngest` 97
tests (95 pass, 1 skip, 1 known pre-existing error in
`test_mosaic_pipeline_recovery.test_safe_load_json_resilience_to_missing_and_corrupt_files`
in an untouched file).
V6 PASS: zero Mosaic runs, zero hub writes, zero auto-assemble/push, zero Patch
runs, render path zero-diff.
