# Build prompt — Manim panel video plays the Mosaic short instead of the Manim

## Standing instructions (do these first, before any other work)

1. **Save the spec file into deepDive `defect-specs/` at the start of the job.** Copy this prompt file into the repo's `defect-specs/` folder as `deepdive-spec-h2-manim-panel-video-source.md`. (mdIngest is code-only — no spec files there.)
2. **Append the build summary to the relevant spec BEFORE any commit or push.** Append the summary to the Spec H2 file (`defect-specs/deepdive-spec-h2-composite-assembler.md`) as the next build summary (determine the next number from the repo's Spec H2 file — do NOT hardcode it). The summary travels in the same commit as the code.

## Pull all first, push all after (with the summary)

Before starting any work, pull ALL of deepDive and mdIngest (both clones). After the work is done and verified, append the build summary to the spec FIRST, then commit + push EVERYTHING (deepDive + mdIngest, code-only mirror for mdIngest) — so the spec + summary goes to GitHub in the same push as the code, never after it, never separately. The spec is posted on GitHub, not left local.

## Context

The landing fix (Spec H2 XIX, deepDive ad43c019) worked live: the 250-1 design now shows in the Beats Studio Manim panel (kind ANCHOR, label "ULTIMATE ANCHOR", hook "Clip one, the ultimate anchor.", 6 stages, playable video player, Patch enabled). The landing gate passes.

But the video player in the Manim panel plays the WRONG video. The user confirmed live (2026-11-27): it plays the MOSAIC full video (the compiled Mosaic short), identified by the footer bar. The player shows 2:20 (140s) while the storyboard says 134.65s (2:15), and the frame is a perspective grid, not the anchor design (bold "ULTIMATE ANCHOR" label + down arrow + hook at bottom, on black). The design lands; the video does not.

## Diagnosis (verified in code at ad43c019 — re-verify at the pulled head)

The Manim panel video (beats.html:520) calls `/api/beats/clip_media`, which uses `find_clip_media` (beats_server.py:407). That function returns the FIRST existing file in this candidate order:

1. hub `{ep}-{c}-manim.mp4`
2. hub `{ep}-{c}-infographic.mp4`
3. hub `{ep}-{c}-mosaic.mp4`
4. hub `{ep}-{c}.mp4` (the compiled Mosaic short)
5. local `{ep}-{c}-manim.mp4`
6. local `{ep}-{c}-infographic.mp4`
7. local `{ep}-{c}-mosaic.mp4`
8. local `{ep}-{c}.mp4`

The Manim mp4s (250-1-manim.mp4, 250-1-infographic.mp4) live ONLY in the local clone (`ddma/clips/`), not in the hub. The hub holds the compiled Mosaic short (`250-1.mp4`, candidate 4). Because candidate 4 is checked BEFORE candidates 5–6, the hub Mosaic short shadows the local Manim files and wins. The panel therefore plays the Mosaic short in the Manim video player.

## The fix

The Manim panel video must use a Manim-only lookup that returns ONLY `*-manim.mp4` and `*-infographic.mp4` (hub + local) and NEVER falls back to Mosaic/plain files. If neither Manim file exists, the panel shows no video (the existing "No Manim yet" / no-video state), never the Mosaic.

Implementation shape (design the exact mechanism — a `source=manim` parameter on `/api/beats/clip_media`, or a separate Manim-only resolver/endpoint, whichever is cleanest):

- The Manim panel (beats.html:520) requests the Manim-only source.
- The server resolves ONLY `*-manim.mp4` / `*-infographic.mp4` (hub first, then local, same hub-then-local order as today).
- A missing Manim returns 404 / no video — the panel must NOT fall back to Mosaic.

## Guardrails

- Do NOT change the landing fix (the panel read path, hasManim, has_beats). Report the landing-path diff as zero.
- Do NOT change the top player (beats.html:229). It shares `/api/beats/clip_media` and must keep its current behavior — the Manim-only lookup is for the Manim panel video only.
- Do NOT change the render (XVIII works). Do NOT re-render any clip. Do NOT touch Mosaic runs, the hub, the longform master, or Patch.
- Do NOT change the candidate order of the general `find_clip_media` for the top player — add the Manim-only path alongside it, don't reorder the shared one.
- Root plans stay uncommitted. No spec text may reference the tracker, workspace paths, or issue numbers in fix text (the spec is self-contained).

## Verification

- V1 — Diagnosis: confirm the candidate-order shadowing in code at the pulled head (hub plain file exists for 250-1, local Manim files exist, candidate 4 wins over 5–6). Report the exact files and their existence/durations.
- V2 — The fix, verified in code + a unit test: the Manim-only lookup returns the local `250-1-manim.mp4` (or infographic) for episode 250 clip 1, and returns nothing (404) when the Manim files are absent — never the Mosaic short. The panel video for 250-1 must resolve to the Manim file. State what the user must confirm live on Windows (pull + restart servers, open 250-1, play the panel video — it must show "ULTIMATE ANCHOR" in large text at top + the hook at bottom, not AI imagery / a grid, and the duration must read ~2:15, not 2:20).
- V3 — The top player is unchanged: its `/api/beats/clip_media` call still resolves as before (report the diff for the shared path as zero, or the exact lines if the handler signature changed).
- V4 — 249 regression: no 249 file, storyboard, master, or plan is touched; the 249 Manim panel still resolves its Manim files.
- V5 — Test suites green in both clones (report the counts and any pre-existing failures by name).
- V6 — Zero Mosaic runs, zero hub writes, zero auto-assemble/push, zero Patch runs.

## Deliver

- The fix, with the spec file saved in deepDive `defect-specs/` and the build summary appended to Spec H2 (next number from the repo file) BEFORE the commit.
- Commit + push all (deepDive + mdIngest, code-only mirror for mdIngest) from WSL — this posts the spec on GitHub, in the same push as the code.
- A report in this shape: the diagnosis (which file shadows which), the fix, the V1–V6 results, the exact commits (deepDive + mdIngest), and what the user must confirm live on Windows.
