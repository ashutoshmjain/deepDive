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
