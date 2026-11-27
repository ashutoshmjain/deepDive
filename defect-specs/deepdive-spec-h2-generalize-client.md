## Standing instructions — apply to every job from this prompt file

1. **Save the spec.** At the start of the job, copy this prompt file into the repo's `defect-specs/` folder (deepDive only — mdIngest is code-only, no spec files there), using the target filename in the first line below. The spec is tracked in the repo alongside the code.
2. **Update the summary before pushing.** After the work is done and verified, append the build summary to the relevant spec (here: Spec H2, as the next numbered summary — determine the number from the current Spec H2 file in the repo, do NOT hardcode it) BEFORE any commit or push — the summary travels in the same commit as the code, never after it, never separately.

# Prompt: Generalize the Beats Studio client-side 249-only checks (unlock "Design this clip" for 250)

Copy this file into `defect-specs/` as `deepdive-spec-h2-generalize-client.md` (freshness check: read the current Spec H2 file first; if a newer Spec H2 summary exists, append this as the next build summary instead of overwriting). Then implement it exactly as written. This job is the follow-up to the server-side lock removal (Spec H2 Summaries XV–XVI, deepDive head 5df19a37): the server already accepts any episode, but the page's own JavaScript still refuses 250 before the request ever reaches the server. GOAL: make "Design this clip" work for episode 250. After this job lands and the servers restart, the USER manually validates it by pressing "Design this clip" for clip 250-1 himself (with the Anchor sample prompt) — that manual validation is NOT part of this job.

## Constraint — clip 250-1 is the user's manual validation, not this job's

Muse Code must NOT run any design, render, compile, or Patch for clip 250-1. No acceptance run on 250-1, no "Design this clip" for 250-1 that is confirmed, no render of `250-1-infographic.mp4` or `250-1-manim.mp4`, no Patch for 250-1. The unlock is verified WITHOUT running 250-1 (see V1 below — the confirm dialog appearing, then cancelled, proves the client check is gone without designing anything). After this job lands and the servers restart, the user presses "Design this clip" for 250-1 himself to validate the Manim generation of kind Anchor. If a verification step below would require running 250-1, skip that step and report it as not-run-by-design instead of running it.

## Context (verified in code at deepDive 5df19a37; re-verify at the pulled head — paths and names may have moved)

The server-side lock removal (XV–XVI) generalized the server: `_h2_refused(ep)` in `ddma/beats_server.py` now always returns None ("H2 wiring serves any episode (generalized from 249-only)"), the design endpoint accepts any episode, and Patch is parameterized. The servers were restarted from the pulled tree (singles on every port, 4x200 liveness) — the new server code IS running. But pressing "Design this clip" for 250-1 still shows a toast: "Design artifacts serves episode 249 only." That toast does NOT come from the server (the string occurs 0 times in beats_server.py, old or new). It comes from the page's own JavaScript in `ddma/beats.html` — a FIFTH lock spot, client-side, that the server-side job did not cover. There are two of them:

1. `designArtifacts(scope)` — the function behind both "Design this clip" (per-clip) and the episode-scope "Design artifacts" button. It reads the episode, then refuses before sending anything:
   `const cleanId = beatsEpisode(); if (cleanId !== '249') { showToast('Design artifacts serves episode 249 only.'); return; }`
   The directive IS read from the box and sent as `body.directive` (so a typed Anchor rule would reach the server) — but the check above fires first and the request never leaves the page. The confirm text for the episode scope also hardcodes "all 21 clips of ep 249".
2. `compositeRetrigger(side)` — the function behind "Retrigger Manim-only" and "Retrigger Mosaic-only". Same shape:
   `const cleanId = beatsEpisode(); if (cleanId !== '249') { showToast('Composite retrigger serves episode 249 only.'); return; }`
   The " Design artifacts" button's title attribute also still says "(Spec H2 s3, ep 249 only)", and a comment near the H2 sections reads "// Ep 249 only."

## The fix

- **designArtifacts:** remove the `if (cleanId !== '249') { showToast('Design artifacts serves episode 249 only.'); return; }` check so the design call is sent for the selected episode. Generalize the episode-scope confirm text from "all 21 clips of ep 249" to the selected episode's actual clip count (or "all clips of ep {cleanId}"). Leave the rest of the function untouched (the directive read, the body shape, the confirm, the polling).
- **compositeRetrigger:** remove the `if (cleanId !== '249') { showToast('Composite retrigger serves episode 249 only.'); return; }` check so the retrigger call is sent for the selected episode. Leave the rest untouched.
- **Labels:** update the " Design artifacts" button's title attribute (drop "ep 249 only") and the "// Ep 249 only" comment to reflect the generalization.
- **No server changes.** The server already accepts any episode; the server-side refusal hook (`_h2_refused`) already always accepts. Do not touch the server, the Manim templates, font sizes, the Manim footer/bottom line, or the Mosaic side.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (push all / pull all; mdIngest is code-only, so a code change fans out to both).
- Scope: the two client-side checks + the labels. VERIFY on 249 (regression) and verify the unlock WITHOUT running clip 250-1 (see V1 — the confirm dialog appearing, then cancelled). No other episode touched. Clip 250-1 is NEVER run in this job — no design, no render, no compile, no Patch for 250-1; the user validates 250-1 manually after the job lands. No Mosaic runs anywhere in this job. No substitutions. No auto-assemble, no auto-push.
- Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.
- STOP rule: if `designArtifacts` or `compositeRetrigger` has moved or changed shape at the pulled head, report the new shape and the smallest generalization before building on it — do not guess the wiring.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Client check gone, 250-1 untouched (the unlock, WITHOUT designing): press "Design this clip" for 250-1 (with a directive in the box) → the confirm dialog APPEARS (proving the client-side `if (cleanId !== '249')` check no longer blocks) → click CANCEL on the confirm → no design runs. After this, `clips/250-1-infographic.mp4` and `clips/250-1-manim.mp4` do NOT exist, and the 250 plan still has NO `infographic_scenes` for clip 1. Muse Code ran nothing for 250-1. The user validates 250-1 manually after the job lands (pressing "Design this clip" himself, with the Anchor sample prompt).
- V2 — 249 regression: "Design this clip" for a 249 clip behaves exactly as before (the confirm dialog appears, the design call is sent, the design runs); no 249 storyboard changed except an acceptance re-cast, if any; the 249 master is untouched.
- V3 — Composite retrigger client check gone: press "Retrigger Manim-only" for 250-1 → the "Composite retrigger serves episode 249 only" toast does NOT appear (the client check is gone). Record what the server then returns (it may refuse for a different, legitimate reason — e.g. no Manim design exists for 250-1 yet — and that is acceptable; the point is the client check no longer blocks). Do NOT run a retrigger that renders 250-1.
- V4 — No regressions: the H3 directive behavior survives (empty directive = today's behavior; "anchor" forces anchor; an equation name picks its catalog member); the 250 catalog is 250's own episode page, not 249's; suites green (report the count; the 1 known pre-existing `test_mosaic_pipeline_recovery` error in an untouched file stays as-is — re-prove it pre-existing with the new code stashed if it is touched, otherwise leave it alone).
- V5 — No Mosaic runs, no hub writes, no auto-assemble and no auto-push anywhere in this job (check the fresh logs for Mosaic/push/hub lines: none). AND no 250-1 design, render, compile, or Patch was run by this job (check the fresh logs for "250-1": none; V1 confirms the files and plan entries).

## Deliver

- Commit + push all (deepDive + mdIngest, code-only mirror for mdIngest).
- Append the build summary to Spec H2 as the next numbered summary (determine the number from the current Spec H2 file — do not hardcode it), with the V1–V5 results and the commit hashes. The summary goes in BEFORE the commit/push. The summary must record that clip 250-1 was NOT run in this job and is left for the user's manual validation.
- Reply with the summary only — one short message, no extra commentary.
