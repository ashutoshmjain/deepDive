# Prompt: Manim footer V2 — final templates + re-render all 21 clips + re-assemble the 249 master

Copy this file into `defect-specs/` as `deepdive-spec-manim-footer-v2.md` (freshness check: read the current spec file first if it exists; append the build summary to Spec H2 instead of overwriting). Then implement it exactly as written. No Mosaic runs. No substitutions. No auto-assemble, no auto-push (this job IS the authorised re-assemble — see below).

## Context

The 249 longform master is published and user-approved, but its Manim side was rendered with the V1 templates. V2 is the final-template rebuild: re-render all 21 clips with the settled footer and archetype rules, re-assemble the local master, re-gate it, and report the archetype state. The point of this job is to see where the Manim archetypes stand — the summary must include a per-clip archetype table (see Verify).

Settled rulings (do not re-litigate; implement exactly):
- **Manim pane footer:** the clip's PLAN title above the divider line. Below the line, LEFT = the clip's ARCHETYPE TYPE (the design kind, constant through the clip: ANCHOR / FORMULA / DIAGRAM). RIGHT = exactly `deepDive podcast · Ep {ep}` — fixed literal, mixed case, middle-dot separator, episode number always present, never truncated, never derived from clip data. The below-left archetype type SUPERSEDES the earlier focus rule (equation name / anchor label / diagram title) — the footer no longer shows the focus below-left.
- **Composite footer (bottom bar of the 1920×1080 frame):** center = `N/21` where N is the clip number. Clip 0 shows NO center text (it is the intro). Clips 1–20 show `1/21` … `20/21`. This replaces the V1 code's `Part {clip_num}`.
- **Spoken sentences stay on the Manim pane.** The fresh templates currently do NOT draw the stage `text` — V2 must add it: render each stage's sentence text on the pane alongside the artifact, with placement following the current renders (the build verifies against them). Words appear twice by design: the sentence on the pane + karaoke in the captions band.
- **TITLE-ONLY is dropped.** Remove `title-only` from the design kinds (`FRESH_KINDS` and the design prompt). The fallback when a clip has no suitable equation/diagram/anchor becomes an ANCHOR (label = the title words), not a separate kind.
- **Diagram rules (user, 2026-11-26).** (a) A diagram MUST fit in the box: the whole shape (tunnel / numberline / groundzero) fits fully within the 740×740 Manim pane — no overflow, no clipping. The diagram builder must fit the shape to the pane bounds. (b) NO repetition of a diagram across clips unless essential: each clip's diagram is cast afresh; if the same diagram shape is genuinely the right one for two clips, it is built fresh from the fixed shape each time (never copied from the other clip's artifact), and the reuse must be REPORTED, never silent. This is the same rule as for formulas (a shared equation is taken from the episode page each time, never copied; the design is independent per clip).
- **Clip 0's long title must fit in full** in the footer title — shrink-to-fit, never clip or truncate, never ellipsis.
- **Font sizes stay at the V1 values** (already in the committed code; do not change them).

## What this job does NOT do (read this first)

This job RE-RENDERS the existing designs — it does NOT re-design anything, does NOT create new Manims, and does NOT call Gemini. The designs are already in the plan (`infographic_scenes` per clip: which clips are ANCHOR / FORMULA / DIAGRAM, which equation / diagram / anchor each clip uses). The build draws the same content again with the final templates. Do NOT call Gemini, do NOT re-cast any clip's design, do NOT change any clip's archetype or content. (The design path is deterministic — the fresh-cast — not Gemini; the stored Gemini key returns 401. The design note's "Gemini designs the clip" wording is trial-era and stale.)

## Math (PRECONDITION — TeX must have landed first)

The TeX resume (KaTeX→SVG→Manim `SVGMobject`, real TeX from `src/249.md`) is a PRECONDITION for this job, not an option. Before starting, verify it has landed: the plan's formula clips carry TeX alongside the norm AND `manim_fresh_design.py` has the KaTeX→SVG render path. If it has NOT landed, STOP and report — do not proceed with norm math. Run the TeX resume prompt (`deepdive-prompt-equations-tex-resume.md`) first, then re-run this job. The order is: TeX resume first, V2 second. The real math fits fully, with splits ONLY at top-level `=`/`+`/`−`.

## The job

1. **Final templates.** Change the Manim footer template (`ddma/manim_fresh_design.py`, `_chrome_bottom`) to draw the archetype type below-left (from the clip's `archetype` field) and the strict right side. Change the composite footer center drawtext (`ddma/spec_h2_composite_assembler.py`, `segment_filter`) to `N/21` with clip 0 blank. Add the stage sentence text to the template (render it on the pane). Drop `title-only` from `FRESH_KINDS` and the design prompt (fallback = anchor). Make the footer title shrink-to-fit for clip 0's long title.
2. **Re-render all 21 clips** (including clip 1) with the final templates, from their CURRENT designs. Do NOT re-design any clip (re-render = draw the same content again; the storyboard/plan scenes are untouched). Clip 1 keeps its current design (anchor); the formula-vs-anchor design question for clip 1 is out of scope. Clips 18/19 keep the thermal-time equation unless the user has changed them via the instruction box — do not change any clip's design in this job.
3. **Re-assemble the local master** from the re-rendered Manim artifacts + the existing Mosaic run files (the H2 assembler / Patch flow). GUARD: re-verify the root plan (`ddma/plan.json`) is 249's before re-assembling (the root plan is a working copy that flips when another episode is loaded — if it is not 249's, stop and report). The re-assembled master is local-only; the push to dd_hub is a separate manual step (do NOT push it).
4. **Re-gate** the re-assembled master with the draft-relative publish gate (structural comparison vs the black-canvas draft baseline, never an absolute brightness threshold).

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (deepDive + mdIngest, code-only mirror for mdIngest; plan files go to deepDive only).
- No Mosaic runs. No substitutions. Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.
- No episode hardcoding beyond the 249-specific artifacts this job touches (the 249 plan, `chrome_249.png`); the template changes themselves are structural and apply to all episodes.
- The design report must list the master as stale + which clips changed (the manual-trigger rule); this job is the authorised re-assemble, so it proceeds.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Footer: on the re-rendered clips, the Manim pane footer shows the plan title above the divider, the archetype type below-left (ANCHOR / FORMULA / DIAGRAM, matching the clip's `archetype` field), and exactly `deepDive podcast · Ep 249` below-right, mixed case, never truncated. Show frame evidence for at least one ANCHOR clip (clip 1) and one FORMULA clip (clip 3).
- V2 — Composite footer: the re-assembled master's bottom bar shows NO center text on clip 0 and `N/21` on clips 1–20. Show frame evidence for clip 0 and at least one other clip.
- V3 — Sentences: each stage's sentence text is visible on the Manim pane alongside the artifact. Show frame evidence for at least two clips.
- V4 — Clip 0 title: clip 0's full title fits in the footer title (shrink-to-fit, no clipping, no ellipsis). Show frame evidence.
- V5 — Archetype table: the summary lists every clip 0–20 with its archetype (expected: 13 ANCHOR, 8 FORMULA, 0 DIAGRAM — verify, do not assume), the footer tag shown, and any clip that fell back to anchor. The table is the point of this job — include it in full.
- V6 — Master: the re-assembled local master duration is ~1883.7 s (matching the run-file sum 1883.69 s within 0.5 s); the gate passes; the master is local-only (not pushed to dd_hub). Report the duration and the gate result.
- V7 — Math: the TeX resume had landed BEFORE this job started (verified in the precondition check) and the real TeX math was used for all formula clips. Show frame evidence for clip 3 and clip 13 (the previously failing fits — both must now fit fully).
- V8 — Diagrams: the diagram builder fits the whole shape within the 740×740 pane (verified in the template code — the diagram construct is bounded to the pane). 249 has no DIAGRAM clips, so there is no frame to show; the archetype table (V5) must confirm 0 DIAGRAM clips and list any diagram reuse (expected: none). The no-repetition rule is recorded as a standing design rule.
- V9 — No re-design: no clip's design changed (no new Manims, no Gemini calls). The plan's `infographic_scenes` are byte-identical to before the job except for the TeX threading from the TeX resume (which landed first) — show the diff (or confirm no diff) for the scenes.
- V10 — Tests: the existing suites still pass (report the count; the only known pre-existing error is `test_mosaic_pipeline_recovery`).

## Deliver

- Commit + push all (deepDive + mdIngest as above).
- Append the build summary to Spec H2 (at the end, as the next numbered summary), with the V1–V10 results, the full per-clip archetype table, the master duration + gate result, and the commit hashes.
- Reply with the summary only — one short message, no extra commentary.
