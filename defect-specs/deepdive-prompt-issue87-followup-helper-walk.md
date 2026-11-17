# Follow-up: helper backward walk stops at intra-word stop closures

## Where

- `ddma/ddma.py` — `resolve_acoustic_word_start()` at :325. This is the
  helper the clip-start back-off (Issue 87) calls to extend a Whisper word
  start backward into the preceding silence. It is also called by
  `resolve_segment_boundary()` at :372 (intra-clip boundaries).
- `ddma/ddma.py` — the backward walk inside that helper, at :352–362
  (the `while cur >= frame_len:` loop). It walks backward in 10ms frames
  (160 samples at 16kHz), and BREAKS at the first frame whose RMS is at or
  below 0.0020:
  ```
  cur = start_sample
  while cur >= frame_len:
      frame = arr[cur - frame_len : cur]
      rms = float(np.sqrt(np.mean(frame ** 2)))
      if rms > 0.0020:
          cur -= frame_len
          onset_sample = cur
      else:
          break
  ```
  After the loop it subtracts a 30ms pre-attack cushion (:364) and clamps
  the result to `win_start` / `raw_start` (:366–367).
- `ddma/ddma.py` — `cut()` at :1272, which now calls this helper for the
  first audio segment's start (:1393–1397, Issue 87 fix) and in the
  non-music path (:1472–1474). The Issue 87 fix is already in place and is
  NOT to be changed — only the helper's walk is fixed here.

## Finding

The backward walk breaks at the FIRST sub-threshold frame, so it cannot
cross a brief silence INSIDE a word — a stop closure. A stop consonant
(/p/, /t/, /k/) has a brief silence (the closure) before its release, and
if Whisper's timestamp sits inside that closure, the walk stops there and
never reaches the word's true onset. Concrete case, clip 249-13 ("Clip"):

- The spoken word "Clip" starts at ~1082.35 (the /k/ burst). Whisper's
  timestamp is 1082.462, which sits INSIDE the word — in the /p/ stop
  closure, a ~40ms near-silence at 1082.44–1082.48.
- The helper is called with raw_start=1082.46, prev_word_end=1082.26
  (previous clip's end). max_backup is 0.16s, so the window starts at
  1082.30. Walking backward from 1082.46, the very first frame
  (1082.45–1082.46) is already inside the /p/ closure (RMS below 0.0020),
  so the walk BREAKS immediately. It returns 1082.43 (onset 1082.46 minus
  the 30ms cushion) — still after the /k/ burst at 1082.35.
- The no-audio default path (120ms cushion, no RMS refinement) returns
  1082.34 and WOULD have captured the burst — but the RMS refinement
  overrides it whenever audio_path is given, and the RMS refinement is
  the part that is broken for this case.
- Verified result: the re-cut 249-13 slice is 78.19s (only +0.03s over the
  old 78.16s), and the /k/ burst is still absent from its start. The
  Issue 87 fix works for normal clips (249-8 re-cut clean: +0.03s pad,
  identical content) but NOT for degenerate mid-word timestamps.
- The same walk is used by `resolve_segment_boundary()` for intra-clip
  boundaries, so the same failure can occur there whenever a segment
  boundary timestamp sits inside a stop closure.

## Fix

Make the backward walk tolerate brief intra-word silences instead of
breaking at the first sub-threshold frame. Only the walk loop changes;
everything else (threshold, cushion, clamps, default fallback) stays.

1. In the `while cur >= frame_len:` loop (:352–362), keep a count of
   CONSECUTIVE silent frames. When a frame's RMS is above 0.0020, move
   back, record `onset_sample`, and RESET the silent count to 0. When a
   frame's RMS is at or below 0.0020, increment the silent count and keep
   walking back; BREAK only when the silent count EXCEEDS the tolerance.
   - Tolerance: 8 consecutive silent frames (80ms at 10ms/frame). This
     covers the 40ms /p/ closure in the 249-13 case with margin, and is
     well under a real inter-word / inter-phrase pause (the pause before
     "Clip" is 0.52s). A stop closure is typically 30–100ms; 80ms covers
     the common case without bridging a real pause.
   - The existing clamps still bound the result: the walk cannot go before
     `win_start` (which is `raw_start - max_backup`, itself clamped to
     40ms after `prev_word_end`), and the result is still clamped to
     `win_start` / `raw_start` at :366–367. So even with the tolerance, the
     walk cannot eat into the previous word's speech.
2. Do NOT change the RMS threshold (0.0020), the 30ms cushion, the
   `max_backup` computation, the `default_start` fallback, or the
   exception fallback (`except Exception: return default_start`).
3. Do NOT change `cut()`, `resolve_segment_boundary()`, or
   `resolve_acoustic_word_end()`. Do NOT change any clip's stored plan
   timings or any caption code. Scope: the walk loop inside
   `resolve_acoustic_word_start()` ONLY.
4. Expected result for the 249-13 case: the walk tolerates the 40ms /p/
   closure (4 silent frames, under the 8-frame tolerance), continues back
   through the speech at 1082.36–1082.43, finds the /k/ burst at 1082.35,
   then stops at the real inter-phrase silence (0.52s, far over the
   tolerance). Onset ~1082.35, minus the 30ms cushion = ~1082.32
   (clamped to win_start 1082.30). The helper should return ~1082.32,
   not 1082.43.

## Verify

1. Direct helper test: call `resolve_acoustic_word_start(1082.46,
   prev_word_end=1082.26, audio_path=<the 249 source audio>)` and confirm
   it returns ~1082.32 (within 0.03s), NOT 1082.43. Also confirm the
   no-audio call (no `audio_path`) still returns 1082.34 (the 120ms
   cushion default, unchanged).
2. Re-cut clip 249-13 from the source audio with the fixed helper (via
   the existing `cut()` — no change to `cut()` itself). Confirm the new
   slice contains the full word "Clip": extract the first 0.5s and confirm
   a loud burst is present in the first ~0.1s (the /k/ burst at source
   1082.35, which is now ~0.03s into the slice). The new slice should be
   ~78.30s (about 0.14s longer than the old 78.16s).
3. Confirm the back-off did NOT eat into the previous clip's speech: the
   new slice's first 0.1s must be silence or the "Clip" onset only — it
   must NOT contain any audio from the previous phrase ("paper.", which
   ends at 1081.94). The cut must not start before 1081.98.
4. Regression — re-cut one already-published clip with a normal Whisper
   timestamp (e.g. 249-8, whose render and slice are already in the
   workspace) and confirm its slice is byte-identical OR differs only by
   a small leading pad (<= 0.35s) with the same speech content. The helper
   change must not alter clips whose first word was already fully
   captured. Also confirm the intra-clip boundary path still works (a
   clip with multiple audio segments still cuts cleanly — the
   `resolve_segment_boundary()` caller uses the same helper).
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
- Scoped change only: the backward-walk loop inside
  `resolve_acoustic_word_start()` in `ddma/ddma.py`. Do not refactor, do
  not touch `cut()`, the compile, the plan generation, or the caption
  code.
- Report PASS/FAIL per verify step, then STOP with a full summary.

## Verification outcome (executed 2026-11-16, deepDive ddma/ddma.py helper walk only)

- Step 1 - PASS. Helper returns 1082.30 (within +-0.03 of ~1082.32); the walk crossed the 40ms closure, found the /k/ burst, and stopped at win_start. No-audio default unchanged at 1082.34.
- Step 2 - PASS. New slice 78.32s (+0.16s over old 78.16s, ~78.30s expected). First 0.5s opens with a loud burst (XxxxxxXXXXXXX...); cut at ~1082.30 >= 1081.98.
- Step 3 - PASS. Cut starts 0.36s after paper. ends (1081.94); first 0.1s is the Clip onset only.
- Step 4 - PASS. 249-8 re-cut differs by exactly +2080 samples (+0.13s, <= 0.35s); cross-correlation MSE 2.9e-05 over 30s (identical content, uniform shift), so intra-clip boundaries are preserved and the resolve_segment_boundary() path is unaffected.
- Step 5 - PASS. test_compile_scope.py 3/3, test_canonical_audio_compile.py 3/3, test_plan_clip0_title.py 2/2, test_mosaic_mux_integrity.py 2/2, full test_curator.js 100 percent (exit 0, TEST 20 restore logged).
- Step 6 - PASS. No publish, no Mosaic API calls (local ffmpeg/ffprobe only), no commit; only ddma/ddma.py modified, nothing staged.
- Change shape: the loop counts consecutive silent frames, resets on speech, breaks only past 8 (80ms). Threshold, cushion, clamps, and fallback untouched; cut(), resolve_segment_boundary(), resolve_acoustic_word_end() not modified.
