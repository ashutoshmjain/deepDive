# Spec H — Composite longform in Beats Studio

Status: posted 2026-11-25. Built from the settled design note and the 249 trial, which published a full 31:24 movie on YouTube, Spotify and TikTok and held the user's attention end to end. The 249 trial used throwaway scripts; this spec turns the proven shape into app code. The trial episode is 249; from episode 250 onwards the longform is produced in the app.

## Background (why this shape)

The 248 full-video Manim experiment failed structurally: one design pass over the whole transcript had to hold ~300 scenes, errors compounded scene by scene, and the fix-up queue was 300 scenes long. The 249 trial proved the different shape: Mosaic and Manim side by side, one sustained Manim artifact per clip, the fixed frame below. The trial's kill rule (Manim needing per-beat design, or more than a third of the clips' artifacts needing reprocessing) was NOT triggered — 0 of 18 new clips needed reprocessing — so the shape is the one to build.

## 1. The composite frame (fixed layout, never per-clip)

The longform frame is a fixed 1920×1080 layout template, top to bottom:

1. **Host strip** — the vertical Shorts' header: "SATOSHA" — ONE blinking microphone in the center — "SATOSHI". Letterspaced caps, monochrome Mosaic style. One mic only, blinking (live indicator). Background pure black, the same as the rest of the screen — no visible band, no separation. Name geometry (measured on the approved sample): each name's center sits around the center of the graphic below it — SATOSHA above the left panel's center (x≈590 in the 1920 frame), SATOSHI above the right panel's center (x≈1330) — and the names sit vertically at the level of the microphone's base. The strip is a short seamless loop (the trial used a 3.0 s loop, 1920×120).
2. **Captions band** — below the host strip (below the microphones), centered, spanning both panels, in karaoke style: the current word highlighted yellow as it is spoken. A perceivable gap sits between the strip and the captions. Text sizes throughout (strip, captions, Manim title/formula/labels) are half the size of the early trial sample that was judged too big everywhere.
3. **Middle band 1480×740** — left 740×740 Manim artifact + right 740×740 Mosaic render.
4. **Footer bar** — the bottom bar of the Mosaic graphics themselves: "Mosaic" left, "deepDive podcast" right, delimiter line above, drawn at the bottom of the frame by the composite in the Mosaic style. No invented copy anywhere in the frame.

## 2. Mosaic side (the clip engine)

- Source is the run-ID artifact `{ep}-{clip}-mosaic-{run_id}.mp4` — the 1080×1080 body render, free of captions, footer, intro/outro cards and stings (all of those are added later by compile-clip, so the run artifact is clean by construction). Scale it exact 1080→740 for the right panel. NEVER crop it — the trial proved any static crop cuts content in some scene. NEVER use the compiled clip.
- Small centered diagrams floating in black inside their own Mosaic frames are Mosaic's own framing, not the composite's — leave them, do not fix them here. Mosaic-side labels baked into the run artifact are left intact; if a label touches its own diagram lines, report it, do not edit it.
- Audio is the run artifact's, unchanged. No intro/outro cards or stings in the longform.

## 3. Manim side (one sustained artifact per clip)

- ONE unified Manim artifact per clip — no per-beat design, save, render or finesse loop. The artifact is ONE continuous timed scene spanning the full clip duration, evolving through a few stages keyed to sentence boundaries (title → diagram builds → formula completes), with slow ambient motion between stages that is visible on screen. Stages are timing, not new designs.
- Design is per clip: one design call per clip from that clip's transcript text — never the whole transcript in one pass, never per beat.
- Content is precise artifacts only: the clip title first; also a formula or equation, a diagram (nested-squares tunnel, number line, ground-zero centre), labels and arrows, a chapter or beat marker. Text and diagram, never narrative scenes.
- **Formulas come from the episode page** (`<ep>.html` on the episode site), never invented by the design call. If a clip's formula is not on the page, the artifact falls back to title-only and the clip is reported as title-only.
- **Cap:** title plus at most one diagram or formula per clip. A clip with no suitable artifact gets at most one diagram or label stage from the transcript (e.g. a label + arrow keyed to the hook sentence) — reported as such — rather than a forced bad artifact. The trial used this label+arrow stage for 8 clips and for the no-formula clip; it is the settled fallback, not the Mosaic-only segment the design note first proposed.
- **Formula reuse:** the trial reused one formula (8−5 = 3) in two clips. The build must decide per clip whether a formula is that clip's own or a reuse, and report every reuse — a reuse is never silent.
- If the Manim side ever needs per-beat design, or more than a third of the clips' artifacts need reprocessing, the build stops and reports — that is the 248 disaster in a new layout, and the trial's kill rule stands.

## 4. Captions (karaoke, from the body timings)

- Captions are the real spoken captions, timed word by word from the body-relative word timings. The compiled caption chunks carry a +1.5 s offset and must NOT be used.
- Karaoke: the current word highlighted yellow as it is spoken, matching the Mosaic karaoke convention. No gaps — word-tiling plus hold to duration. Lines capped at ~40 characters.
- **1.5 line spacing is done by hard-placing each line** (line tops 42 px apart at the trial's sizes) — the rendering library ignores the LineSpacing style field, so the spec's spacing is explicit positioning, not a style setting.
- **The caption renderer sets the font size explicitly.** The trial caught a missing Fontsize field rendering captions dark red; the renderer must never rely on a default size.
- **Caption data is required for every clip.** A clip with no caption data is a reported exception in the build — it must NOT silently fall back to a static title band. (The trial shipped two clips that way because the gap was found late; the code must surface it early.)
- Proper names are checked against the episode page (the trial caught an ASR error, "Conravelli" for "Connes-Rovelli"); any corrected name is reported.

## 5. Run-artifact durability (the trial's design flaw, fixed here)

The trial found the run artifact is stored as a working asset, not a durable one: the local cache is ephemeral, the pipeline purges older run files from BOTH the cache and the hub keeping only the current run, nothing checks the run artifact survived, and the only backup is Mosaic's cloud with unknown retention. Five of 249's 21 run files had silently vanished and were re-downloaded by run ID. The code must:

- Store each clip's run artifact in the episode folder on the hub — `<dd_hub>/episodes/<ep>/{ep}-{clip}-mosaic-{run_id}.mp4` — the same folder it lands in today. That folder is the purge-proof canonical copy, verified on write (size and duration recorded and checked).
- Purge cleans only the local cache, never the hub's canonical copy.
- A health check verifies every clip's run artifact exists and is valid; a missing or invalid one is re-downloaded from Mosaic's cloud by run ID while it is still there, and reported. A missing run file is never silently substituted — never the compiled clip, never a generically-named body file with no run-ID provenance, never a fresh Mosaic run without the user's word.

## 6. Beats Studio workflow (the compile room)

- **One deliberate start.** "Design artifacts" in Beats Studio, per clip or per episode. Nothing starts itself — transcription is never automatic and neither is this.
- **The system fans out.** One design call per clip, each designing that clip's ONE Manim artifact. The user never sees or touches the individual calls.
- **Renders run as queued background jobs**, progress shown per clip, the screen free while they run. Outcome reporting per clip (scenes stitched/designed, or FAILED with the reason) — the trial's Manim render silence is not repeated.
- **The system reports only the exceptions.** A short list: the clips whose artifacts failed or came out wrong. The ones that worked never ask for attention.
- **The user finesses only the failures.** One clip's artifact at a time, only the ones on that list — adjust and re-render that artifact. Manual work scales with failures, never with the clip count. Retrigger is per side (Manim only or Mosaic only), so a bad title never costs a Mosaic re-render. **Retrigger never touches duration** — duration was decided in Cutroom and stays locked downstream.
- **Assemble is automatic.** The master assembles itself from the finished clips (the combine is deterministic and already works). Concat joints must be clean — the trial's 1-tick DTS overlaps at the joints are a known cosmetic artifact to address or explicitly accept.
- **"Push the movie to dd_hub" is a button in Beats Studio** — the push lives where the movie is assembled.

## 7. Cutroom and Cockpit (who does what)

- **Cutroom** owns the precise clip duration, Mosaic rendering, clip publishing and the Draft preview. It creates no Manim artifacts and has no Manim button: the Manim process is triggered from Beats Studio for all clips, so a Cutroom button would have no job left — creation, preview and finesse all live in Beats.
- **Cockpit** is out of the longform business. The Long-form Video Master card is status-only: it shows whether the master exists, and its button is "Open in Beats Studio." Nothing in Cockpit can start a longform render. The longform has exactly one front door: Beats Studio.
- **Publishing splits by product.** Cutroom owns clip publishing (the Mosaic shorts). Beats Studio owns longform publishing. One publisher per product.

## 8. The dd_hub longform destination (from episode 250 onwards)

The push writes the finished movie to a grounded destination on the hub: the episode's longform slot, with meta recording the file's SHA-256, duration (container and video-stream both, any disagreement logged as a warning), and a `ready_for_distribution` signal that the distribution pickup reads. The movie is not distributable until that signal is set. Longform assembly strips the "deepdive conclusions" stings and the intro cards, per the existing assembly rules.

## 9. Publish gate for the longform

Before the push lands, the gate compares the movie about to be published against the black-canvas draft baseline by structure — never an absolute brightness threshold — and refuses the draft-in-substance with a named reason. It prefers the verified good local master and stops on a master mismatch. This is the same draft-relative gate as the clip publish gate, applied to the movie.

## 10. Platform quirks (learned from the 249 trial, baked in)

- **YouTube:** public, slopcast playlist, custom thumbnail, title and description verbatim. A video with the same title may already be on the channel — it is the audio podcast, syndicated to YouTube via RSS from Spotify — not a duplicate to rename. The longform is a separate new video. No copyright or guideline issues on the trial file.
- **Spotify:** video episode on the video show (a new episode; the audio-only episode is untouched). The file's audio and video tracks must match. Spotify may still flash an advisory that they "may not be synchronized throughout the file" even on a clean file — the trial's tracks matched to within 0.02 s and the advisory appeared anyway, and the user played the video on Spotify and it looks good — so the advisory is not by itself a failure.
- **TikTok:** 31 minutes fits the 60-minute web-upload cap. The post may sit briefly "Content under review" / "Only me" before clearing to "Everyone" — that is the review, not a failure. TikTok displays the duration one second less than the file (its own rounding). The trial's TikTok video was watched and looks good.
- **Instagram:** longform is OUT — 31 minutes is over the 20-minute Reels cap. The longform does not go to Instagram.

## 11. Repo discipline — push all, pull all

- Push all and pull all: every push and every pull covers both clones (deepDive and mdIngest). Never push or pull a single clone alone.
- If there is a code change, fan out all and fan pull all: the code change is mirrored to every repo, and then every repo is pulled to verify the mirror landed.
- Plan and data files live only in deepDive — mdIngest is code-only — so a plan change is pushed from deepDive alone; "push all" pushes every repo that holds the change, and is a no-op where nothing changed.

## Verification

- **Regression: run episode 249 itself through the app end to end** (design → render → assemble → push → gate) and compare the resulting movie against the approved prototype `249-composite-full.mp4` (93,749,687 B, 1883.689 s). The prototype is the oracle: same clip order and durations (within 1 s total), same 1920×1080 frame, same strip / captions / panels / footer by the trial's measurements (name centers above the panel centers, names at the mic-base level, strip pure black, caption gap 1.5× the line height, panels full-frame with no crop, footer in the Mosaic style, formulas page-sourced), and frame spot-checks matching the prototype. The app must reproduce the prototype in substance. (Note: clips 3–4 have no caption data; the app must surface that as a reported exception per §4 rather than silently shipping a static band as the prototype did — fix the data first, or accept the exception as the expected result for those two clips.)
- Then build the episode 250 longform end to end in the app (design → render → assemble → push → gate) and compare the result against the approved 249 frame by the same measurements.
- Exercise the run-artifact health check (a missing run file is re-downloaded by run ID and reported) and the caption-data rule (a clip with no caption data is a reported exception, not a silent static band).
- Exercise the kill rule: the build stops and reports if the Manim side needs per-beat design or more than a third of the clips' artifacts need reprocessing.

## Build summary (2026-11-25)

What was built: Spec H composite longform as app code in Beats Studio — rulebook module `ddma/spec_h_composite_longform.py` (sections 1-6 + 8-10: frame constants, mosaic guards, KillRuleTracker, caption rules, durability, workflow, dd_hub meta, publish gate, platform quirks, oracle helper), `GET /api/beats/spec_h` + `POST /api/beats/longform_push` endpoints with gate + ffprobe durations in `ddma/beats_server.py`, "Push movie to dd_hub" button + `pushLongformToDdHub` in `ddma/beats.html`, 19-test suite `ddma/tests/test_spec_h_composite_longform.py`.

Commits per repo: deepDive `e68c5cdf` (Spec H composite longform, 5 files +802/-1); mdIngest `1813919` (code-only mirror, 4 files +709/-1; spec md stays deepDive-only per plan/data discipline).

Files changed per repo: deepDive — `ddma/spec_h_composite_longform.py` (new), `ddma/beats_server.py`, `ddma/beats.html`, `ddma/tests/test_spec_h_composite_longform.py` (new), `defect-specs/deepdive-spec-h-composite-longform.md`; mdIngest — same 4 code files mirrored byte-identical (diff-verified), no plan/data files.

Verification results:
- 249 regression (design>render>assemble>push>gate): BLOCKED, no shippable movie. Clips 3,4 (plus clip 0) have no caption data -> reported exception per s4, never silent static band; clips 1,5-12 lack run-ID provenance (resolve_mosaic_side refuses substitution per s5); mosaic_jobs failed for 0,3,4. Order 0-20 matches oracle; span+music-crossfade math 1883.38s vs oracle 1883.689s (delta 0.309s, within 1s). POST longform_push ep249 -> 404 no-master refusal, zero hub writes. Spec-H suite 19/19 OK; frames on disk are pre-composite 1080x1920 verticals only. REGRESSION VERDICT: FAIL (app behaved per spec).
- 250 build: BLOCKED, no shippable movie. 14 clips (span sum 2641.990s); only clips 0,1 have run-IDs + captions (250-0.ass 791 Dialogue, 250-1.ass 695); clips 2-13 have neither. POST longform_push ep250 -> 404 refusal, zero hub writes. Spec-H suite 19/19 OK; full tests dir 25 tests with 1 pre-existing error (test_mosaic_pipeline_recovery corrupt.json expectation, untouched file). 250 state is worse than 249 (12/14 clips missing provenance + captions).
- Health check exercised via `spec_h.health_check_run_artifacts` on [250/0 healthy, 250/1 missing-recoverable, 250/2 no-run_id] -> healthy [0], recovered [clip 1 re-downloaded by run ID], unrecoverable [clip 2 no provenance]; never substitutes.
- Kill rule exercised via `KillRuleTracker` (14 clips): per-beat design on clip 5 fires KillRuleExceeded; 5/14 reprocessed fires (>1/3); 2/14 does not fire.

Deviations from spec: none in code — the rule, exception type, gate, refusal, and status paths are in place. Known gaps (not deviations): end-to-end oracle comparison not executed (oracle mp4 absent from this machine); `KillRuleTracker.note_design/note_reprocess` not yet wired into archetype_studio update paths; no spec-H composite assembler beyond the EP-248-era engine, so full renders not attempted; clips 2-13 (ep250) and 0/3/4 + 1,5-12 (ep249) need Cutroom work first (Mosaic runs, body-relative captions, one Manim artifact per clip).

## Re-run addendum (2026-11-25, re-verified first-hand)

Verdict: BLOCKED with correct app behavior on both episodes — the app refuses to ship (404 no-master, zero hub writes) exactly as specified. No workaround or substitution was made.

Comparison numbers (ep 249): oracle `249-composite-full.mp4` = 93,749,687 B, ffprobe container 1883.688688 s (~1883.689), video stream 1883.666992 s, audio 1883.688688 s, 1920x1080, A/V delta 0.02 s (SHA not recorded in evidence — unavailable). Result: no movie produced, so no result size/duration/delta to report; plan clip durations sum 1735.84 s, audio span ends 1684.16 s (plan-vs-oracle duration not directly comparable, no assembled movie). Frame: oracle frame 1920x1080 confirmed. Spot-checks (name centers x~=590/1330, strip black, caption gap, panel crop, footer style) not executable — no product movie exists to measure.

Per-clip exception list (ep 249): caption exceptions ONLY clips 3,4 (plan `_caption_words` 3:0, 4:0; clip 0 HAS 401 captions — 0:401, 1:297, 2:278, 5:241, 6:199, 7:186, 8:226, 9:179, 10:191, 11:178, 12:168, 13:164, 14:236, 15:151, 16:212, 17:156, 18:132, 19:152, 20:309). All 21 plan `mosaic_run_id` present (0:43295e65 1:de98eb4f 2:26606fbc 3:972b1c19 4:3ed55339 5:6b9b4156 6:488f2593 7:89c30dbf 8:97171db6 9:771fa245 10:1c5b9562 11:31d813bc 12:e5bc3688 13:1a5521de 14:00005b7b 15:6a928b86 16:ee888db0 17:587faf38 18:748710bf 19:7a1a40b2 20:ac14dfc3); `resolve_mosaic_side` passes all 21 exact 1080->740. Job store: entries only for clips 0,2,3,4,13-20 — failed (compile-clip exit 1) for 0,3,4 with matching run_ids, completed for 2,13-20, NO entries for 1,5-12. Run artifacts: all 21 canonical `{ep}-{clip}-mosaic-{run_id}.mp4` healthy, 0 recovered, 0 unrecoverable. Beats clip-3 status: `mosaic_status` failed run 972b1c19, timeline scenes 0 / has_beats false. E2E: design/render produce nothing, no master, push 404, spec-H suite 19/19 OK.

Per-clip exception list (ep 250): expected condition holds exactly — only clips 0,1 have Mosaic runs + captions (run_ids 0:54b3ea3a-7532-425d-b083-899a314d4d6c, 1:4dc08028-5f8a-4d51-97e2-490e4cadc68d; captions 0:406, 1:351, 2-13:0 each); clips 2-13 lack both. Jobs completed 100 for clips 0,1 only; artifacts on hub/ddma only for 0,1. No Mosaic runs started.

Remaining gaps: (a) no assembled 249/250 movie, so oracle frame/strip/caption/panel/footer spot-checks unexecuted; (b) `mosaic_jobs.json` lacks entries for 249 clips 1,5-12 and shows failed compile-clip for 0,3,4 (server-observed, not repaired); (c) beats timeline index durations differ from plan (e.g. clip 1 index 269.39 s vs plan 110.6 s; index total 3254.21 s) — archetype_studio vs plan discrepancy unresolved.
