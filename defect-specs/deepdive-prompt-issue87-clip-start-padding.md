# Fix: first word of a clip truncated at the clip-start boundary

## Where

- `ddma/ddma.py` — `cut()` at :1272 (the audio slicer that cuts each clip's
  audio from the source file). The per-segment start times come from the plan
  (`segments[i]["start"]`); the first audio segment's start is the clip's
  `source_start`, which comes from the transcription segment start.
- `ddma/ddma.py` — `resolve_acoustic_word_start()` at :325. This helper
  ALREADY EXISTS and does exactly what is needed: it extends a Whisper word
  start timestamp backward into the preceding breath/silence pause "so
  initial consonants, plosives, and attack transients (e.g., 'Cl-' in
  'Clip', 'P', 'T', 'S', 'Th-') are never cut in half", using a 120ms attack
  safety cushion clamped 40ms after `prev_word_end`, refined by 16kHz PCM RMS
  energy when `audio_path` is given.
- `ddma/ddma.py` — `resolve_segment_boundary()` at :372. Already used inside
  `cut()` for boundaries BETWEEN consecutive audio segments within a clip
  (called at :1387, only when `s_end > next_s_start`).
- `ddma/ddma.py` — the `resolved_bounds` loop in `cut()` at :1377–1389. It
  resolves boundaries between consecutive audio segments, but it NEVER touches
  the FIRST audio segment's start (`a_pos == 0`): that `s_start` is used
  exactly as the plan states it, at :1402 and :1411
  (`inputs.extend(["-ss", f"{s_start:.3f}", "-t", f"{s_dur:.3f}", "-i", audio])`).
- `ddma/ddma.py` — the non-music path in `cut()` (the `else` branch, single
  ffmpeg `-ss start_str -to end_str`, ~:1460). It cuts from `start_val`
  directly, with no back-off either.

## Finding

Whisper's segment start can lag the true speech onset by ~0.1s, and the clip
cut starts exactly at that (late) timestamp, so the first word's onset is
cut off. Concrete case, clip 249-13 ("Clip thirteen"):

- The spoken word "Clip" starts at ~1082.35 in the source audio (a loud /k/
  burst, RMS 2145, after 0.52s of silence following the previous phrase
  "paper." which ends at 1081.94).
- Whisper's transcription places the "Clip 13." segment at [1082.462–
  1083.022] and gives the word "Clip" a ZERO-duration timestamp
  (start = end = 1082.462) — it could not resolve the "Clip"/"13." boundary.
- Clip 13's `source_start` is 1082.46 (taken from Whisper's segment start).
  The audio cut at 1082.46 removes the first ~0.11s of "Clip" (the /k/ burst
  at 1082.35 and the /l/ onset at 1082.40), leaving the vowel + "p" — so the
  finished video sounds like "p thirteen" instead of "clip thirteen".
- The onset (1082.35–1082.46) falls in the gap between clip 12's end
  (source_end 1082.26) and clip 13's start (1082.46): it belongs to NEITHER
  clip's audio.
- The compile is NOT at fault: the published master's body audio is a
  sample-accurate copy of the slice (energy envelopes match at the aligned
  offsets). The truncation is in the SOURCE CUT boundary, not the compile.
- The caption word "Clip" is timed at 0.0–0.04s in the plan (clip-local),
  which is the same degenerate Whisper timestamp — the caption timing is
  also wrong for this word, but only by ~0.1s, which is below the
  perceptual threshold once the audio is fixed.

This is the START-boundary version of the known last-word-splitting
observation: a word at a segment boundary gets truncated because the
boundary timestamp is imprecise. The intra-clip version is already handled
by `resolve_segment_boundary()`; the clip-start version is not.

## Fix

Apply the existing `resolve_acoustic_word_start()` to the FIRST audio
segment's start in `cut()`, so the cut backs off into the preceding silence
and captures the true word onset. Do NOT invent a new mechanism — reuse the
helper at :325.

1. In the `resolved_bounds` loop (:1377–1389), for the first audio segment
   (`a_pos == 0`), replace its `s_start` with
   `resolve_acoustic_word_start(s_start, prev_word_end=<end of the previous
   speech>, audio_path=audio)`.
   - `prev_word_end` must be the end of the speech BEFORE this clip, so the
     back-off is clamped to the silence gap and never eats into the previous
     clip's speech. Use the previous clip's `end` from the plan (the clip
     before this one in `plan_data`), or the previous audio segment's end
     when one exists in the same clip. For the 249-13 case the previous
     clip's end is 1082.26 and the previous phrase ends at 1081.94, so the
     helper's clamp (40ms after `prev_word_end`, max back-off 0.35s, 120ms
     default cushion) lands the cut at ~1082.34 — capturing the /k/ burst
     at 1082.35.
   - Do NOT change the plan's stored `start`/`source_start` (the plan is the
     record of Whisper's segmentation). Only the CUT start is backed off.
     The caption word timings stay as they are — the resulting misalignment
     is bounded by the back-off (~0.12s) and is imperceptible; verify it
     (see Verify step 3).
2. Apply the same back-off in the non-music `else` path (single ffmpeg
   `-ss start_str -to end_str`): back off `start_val` the same way before
   building `start_str`.
3. Do NOT change `resolve_segment_boundary()`, the intra-clip boundary
   handling, the music-segment handling, the compile, or the caption
   generation. Do NOT change any clip's stored plan timings.
4. Scope: `ddma/ddma.py` only (the `cut()` function). No other files.

## Verify

1. Re-cut clip 249-13 from the source audio with the fixed `cut()` (the
   source audio and the plan are already in the workspace; no new Mosaic
   run, no new transcription). Confirm the new slice contains the full
   word "Clip": extract the first 0.5s of the new slice and confirm speech
   energy starts at ~0.0s with the /k/ burst present (compare against the
   old slice, whose first 0.15s lacked the burst). The new slice should be
   ~0.12s longer than the old one (78.16s -> ~78.28s).
2. Confirm the back-off did NOT eat into the previous clip's speech: the
   new slice's first 0.1s must be silence or the "Clip" onset only — it
   must NOT contain any audio from the previous phrase ("paper."). The
   previous phrase ends at 1081.94; the cut must not start before
   1081.98.
3. Compile the re-cut clip 13 and confirm the first caption word "Clip"
   still aligns with the spoken word within ~0.15s (caption at clip-local
   0.0s, spoken onset now at ~0.01s into the slice — effectively aligned).
4. Re-cut one other already-published clip (e.g. 249-8, whose render and
   slice are already in the workspace) and confirm its slice is
   byte-identical OR differs only by a small leading pad (<= 0.35s) with
   the same speech content — i.e. the fix does not change clips whose
   first word was already fully captured.
5. Run the existing test suites and report the counts
   (`test_compile_scope.py`, `test_canonical_audio_compile.py`,
   `test_plan_clip0_title.py`, `test_mosaic_mux_integrity.py`,
   `test_curator.js` — do NOT run TEST 20 without first confirming its
   `finally` restore at `test_curator.js:1108` is intact).
6. Do NOT publish any clip as part of this verify. Do NOT trigger a Mosaic
   run. Do NOT commit or push (fan-out is a separate human step).

## Guardrails

- deepDive only. No Mosaic runs. No keys in git. No commit/push (fan-out
  is a separate human step).
- Scoped change only: the `cut()` function in `ddma/ddma.py`. Do not
  refactor, do not touch the compile, the plan generation, or the caption
  code.
- Report PASS/FAIL per verify step, then STOP with a full summary.

## Verification outcome (executed 2026-11-16, deepDive ddma/ddma.py cut() only)

- Step 1 - FAIL. New slice 78.19s (+0.03s over old 78.16s), not ~78.28s. Direct helper call returns 1082.43, not the predicted ~1082.34. Measured cause: source RMS profile shows loud speech at 1082.36-1082.43 then a 40ms near-silence at 1082.44-1082.48 (the /p/ stop closure inside Clip; Whisper zero-duration timestamp sits mid-word in it). The helper backward walk breaks at the first sub-threshold frame, so it never reaches the /k/ burst; the 30ms cushion lands at 1082.43. The no-audio default path returns exactly 1082.34. Slice-onset profiles confirm the burst hump is absent from both old and new slice starts.
- Step 2 - PASS. Cut at 1082.43 >= 1081.98 (0.45s margin); first 0.1s is low-level tail + closure only (paper. ended 1081.94).
- Step 3 - PASS. Recompiled 83.92s, 1080x1920, 39 captions, versioned render used; body speech onset at master t=1.700s (body-local 0.000s), caption clip at 1.70s - delta 0.00s.
- Step 4 - PASS. 249-8 re-cut: +480 samples (+0.03s) leading pad, cross-correlation MSE 4e-06 over 30s (identical content).
- Step 5 - PASS. test_compile_scope.py 3/3, test_canonical_audio_compile.py 3/3, test_plan_clip0_title.py 2/2, test_mosaic_mux_integrity.py 2/2, full test_curator.js 100 percent (exit 0).
- Step 6 - PASS. No publish, no Mosaic API calls, no commit; hub plan clip 13 timings unchanged (start 1082.46, duration 68.04, run_id intact).
- Correction to the Finding: the pre-fix compile used the blank generic clips/249-13-mosaic.mp4 with has_motion_source=True (83.84s of pure black per blackdetect), NOT the black draft with has_motion_source=False. Same visible symptom (blank master), different path.
- Follow-up (out of scope for this item): resolve_acoustic_word_start() backward walk cannot cross intra-word stop closures - it breaks at the first sub-threshold frame. For degenerate mid-word timestamps the no-audio default (120ms cushion, 1082.34 here) outperforms the RMS refinement (1082.43). A real fix for this clip belongs in the helper walk (e.g. tolerating brief intra-word gaps), which this item forbids changing (Scoped change only: the cut() function).
