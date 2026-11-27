# Prompt: Generalize the H2 Manim wiring from episode 249 to any episode (unlock 250)

Copy this file into `defect-specs/` as `deepdive-spec-h2-generalize-episode.md` (freshness check: read the current Spec H2 file first; if a newer Spec H2 summary exists, append this as the next build summary instead of overwriting). Then implement it exactly as written. This job runs BEFORE the design-section prompt (`deepdive-prompt-design-section-manim.md`) — the design section's 250-1 verification needs the endpoint to accept episode 250, which is what this job unlocks. The Mosaic-button removal is NOT in this job; it lives in the design-section prompt (Part B) — do not duplicate it here.

## Context (verified in code at deepDive 3c179f8; re-verify at the pulled head — paths and names may have moved)

The H2 Manim wiring (design + render + Patch) is locked to episode 249 by explicit refusals, not by structure. Everything else is already episode-generic: the design endpoint builds its paths from the episode number (`projects/<project_id>/plan.json`, `clips/<ep>-<clip>-infographic.mp4`, `clips/<ep>-<clip>-manim.mp4`), the episode-page equation catalog is fetched by episode number, and the composite footer center (N/total) is threaded from the plan (250 already reads "N/14"). The lock is in three places:

1. Beats Studio server (`ddma/beats_server.py`): `H2_EPISODE = "249"` plus a guard that refuses any other episode ("H2 wiring serves episode 249 only"). The design worker posts to the curator endpoint with the episode.
2. The design endpoint (`ddma/scratch/run_curator.py`, `/generate-manim-infographic`): a hard refusal for any episode other than 249 (HTTP 400, "Refusing: this endpoint serves episode_249 only"). The fresh-design branch also hardcodes the catalog fetch to episode 249 (`fetch_episode_equations("249")`) and gates on `== "episode_249"`.
3. Patch (`ddma/beats_server.py`, `_h2_patch_clip_249`): hardcodes the 249 plan path, the frame assets (`chrome_249.png`, `strip_249.mp4`), the infographic filename (`249-<n>-infographic.mp4`) and the 249 master. Patch for 250 does not exist yet.

Consequence today: "Design this clip" for 250-1 is enabled in the UI but the endpoint refuses it with a 400 — the button does not know about the lock, the server does. Episode 250 has no Manim designs at all (no `infographic_scenes` for any of its 14 clips), because the design step was never run for it and cannot run until this lock is gone.

## The fix

- **Beats Studio guard:** generalize the H2 wiring to accept the episode as a parameter (the episode currently selected in Beats Studio). Remove the 249-only refusal. The design worker passes the selected episode through to the curator endpoint. The default when no episode is given stays 249 (no behavior change for 249).
- **Design endpoint:** remove the `episode_249`-only refusal — accept any episode. In the fresh-design branch, fetch the equation catalog for the requested episode (`fetch_episode_equations(ep_num)`) instead of hardcoding "249", and drop the `== "episode_249"` gate. Everything downstream (storyboard, plan write, render, compile) already uses the episode number — verify that at the pulled head and fix any remaining hardcoded "249" in that path.
- **Patch:** generalize `_h2_patch_clip_249` to take the episode (plan path `projects/episode_<ep>/plan.json`, frame assets `chrome_<ep>.png` / `strip_<ep>.mp4`, infographic `<ep>-<n>-infographic.mp4`, master `<ep>-longform-master`). Rename it to `_h2_patch_clip` (keep a thin 249 wrapper only if a caller needs the old name — verify the callers at the pulled head). Patch refuses when the episode's plan or frame assets are missing — it never substitutes another episode's files.
- **Frame assets for 250:** generate `chrome_250.png` + `strip_250.mp4` (the V1 frame-asset generator, pointed at 250 — the contents are episode-independent). They live in `ddma/assets/` alongside the 249 pair.
- **No other behavior changes.** The design flow, the catalog guard (a chosen equation must be a catalog member or the clip drops to anchor), the render and compile steps, and the Patch gate are untouched. The composite footer center stays threaded from the plan.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (push all / pull all; mdIngest is code-only, so a code change fans out to both).
- Scope: the H2 wiring generalizes; VERIFY on 249 (regression — 249 design, render and Patch behave exactly as today) AND on 250-1 (the unlock — "Design this clip" now produces 250-1's Manim). No other episode touched. No Mosaic runs anywhere in this job. No substitutions (never a 249 file or asset in place of a 250 one). No auto-assemble, no auto-push. Do NOT touch the Manim templates, font sizes, or the Manim footer/bottom line. Do NOT touch the design-section panel (that is the next job) or the Mosaic side.
- Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.
- STOP rule: if the design endpoint or the Patch function has moved or changed shape at the pulled head, report the new shape and the smallest generalization before building on it — do not guess the wiring.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Endpoint accepts 250: POST `/generate-manim-infographic` for episode_250 clip 1 no longer returns the 400 refusal; it proceeds to design.
- V2 — "Design this clip" for 250-1 produces the Manim: the endpoint returns 200 with the video URL; `clips/250-1-infographic.mp4` (740x740) and `clips/250-1-manim.mp4` (1080x1920) exist and are non-empty; the 250 plan now carries `infographic_scenes` for clip 1; the design report is present (deterministic path, since the Gemini key returns 401).
- V3 — Patch generalizes: Patch for a 249 clip still works exactly as before (same master, same assets); Patch for 250-1 works with 250's plan and 250's frame assets and refuses cleanly when they are absent.
- V4 — 249 regression: a 249 clip's design, render and Patch are byte-identical in behavior to before (no 249 storyboard changed except an acceptance re-cast, if any); the 249 master is untouched.
- V5 — Frame assets: `chrome_250.png` + `strip_250.mp4` exist in `ddma/assets/`; no 249 asset was substituted anywhere in the 250 path (grep the 250 render/assemble commands for "249": zero).
- V6 — No regressions: the H3 directive behavior survives (empty directive = today's behavior; "anchor" forces anchor; an equation name picks its catalog member); the 250 catalog is 250's own episode page, not 249's; suites green (report the count; the 1 known pre-existing `test_mosaic_pipeline_recovery` error in an untouched file stays as-is — re-prove it pre-existing with the new code stashed if it is touched, otherwise leave it alone).
- V7 — No Mosaic runs, no hub writes, no auto-assemble and no auto-push anywhere in this job (check the fresh logs for Mosaic/push/hub lines: none).

## Deliver

- Commit + push all (deepDive + mdIngest, code-only mirror for mdIngest).
- Append the build summary to Spec H2 as the next numbered summary (determine the number from the current Spec H2 file — do not hardcode it), with the V1–V7 results and the commit hashes. The summary goes in BEFORE the commit/push.
- Reply with the summary only — one short message, no extra commentary.
