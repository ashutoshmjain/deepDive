# Prompt: Redesign both footers — Manim pane footer + composite footer (re-render, no re-design)

Copy this file into `defect-specs/` as `deepdive-spec-h2-footer-redesign.md` (freshness check: read the current Spec H2 file first; if a newer Spec H2 summary exists, append this as the next build summary instead of overwriting). Then implement it exactly as written. Episode 249 only. Do not touch episode 250. No Mosaic runs. No substitutions. No auto-assemble, no auto-push.

## Context

Beats Studio, ep 249. The user reversed the earlier footer-removal decision: the Manim bottom bar stays — it is a cleaner design — but it gets redesigned, and the whole clip's bottom bar gets redesigned too. Both decisions are the user's, settled:

- **Manim pane footer (inside the left 740x740 pane):** the clip title ABOVE the divider line; BELOW the line, left side = what is being shown above in the Manim (the design's focus: equation name for formula clips, anchor label for anchor clips, diagram title for diagram clips); below the line, right side = "deepDive podcast · Ep 249".
- **Composite footer (bottom bar of the whole 1920x1080 frame):** "Manim" on the left (under the Manim pane), "Mosaic" on the right (under the Mosaic pane), "Part N of 21" in the center (N = the clip's position, 1-based). This replaces the current "Mosaic" left / "deepDive podcast" right — which mislabels, since "Mosaic" sits under the Manim pane. The "deepDive podcast" name does not leave the frame: it lives on in the Manim pane's footer, right side.
- **Font:** the Manim display text still drops two notches from the current sizes (52, 44, 30, 24), hierarchy kept. (Kept from the earlier job; the user did not retract it.)

This job changes templates and re-renders. It is a re-render, not a re-design.

## What the code shows (verify each claim in the tree before changing it)

1. **Manim footer** — `_chrome_bottom(title)` in `ddma/manim_fresh_design.py` (line ~571) draws the current chrome: a `Text` of the title at font_size=22 at y=-2.95, plus a divider `Line` at y=-3.35, appended in `_render_stage_body` (line ~599) on every stage. The frame spans y=-4..4, so only ~0.65 units sit below the line today — there is no room for a sub-row yet. The layout must shift (title up, line lower, sub-row below the line) to fit the new row.
2. **Composite footer** — it is NOT drawn by ffmpeg text filters. It is baked into the static frame image `ddma/assets/chrome_249.png` (1920x1080, pure black): a delimiter line near the bottom, "Mosaic" bottom-left, "deepDive podcast" bottom-right. `segment_filter` in `ddma/spec_h2_composite_assembler.py` (line ~378) overlays the chrome image, then the strip loop, then the Manim art at 220:230 and the Mosaic run at 960:230. The footer spec also lives in the module's frame-contract dict (lines ~110-111: `"footer": {"style": "Mosaic", "left": "Mosaic", "right": "deepDive podcast", "rule": "delimiter line above"}`).
3. **The center "Part N of 21" varies per clip**, so it CANNOT be baked into the static chrome image. It must be drawn per segment in the filter graph. `segment_filter` currently takes only `clip_num`; the total clip count must be threaded through from the caller (`build_segment_cmd` → `segment_filter`), derived from the episode plan — never hardcode 21.

## The fix

### A. Manim pane footer (fresh templates only)

- In `ddma/manim_fresh_design.py` ONLY, redesign `_chrome_bottom` into a two-row footer:
  - Above the divider line: the clip title (the same title the chrome shows today).
  - Below the line, left-aligned: the design's focus — the equation's human-readable name for formula clips, the anchor label for anchor clips, the diagram title for diagram clips. For title-only clips (no focus), leave the below-left blank.
  - Below the line, right-aligned: `deepDive podcast · Ep {ep}`, with the episode number passed through the design/render path from the episode being rendered — never hardcode 249 in the template module.
  - Shift the layout to fit: title up, line lower, sub-row below the line in a smaller font than the title (the builder picks the exact y positions and sub-row size; clip 1 is the legibility check). Stage content otherwise unchanged; the sub-row must not collide with stage content or the frame edge.
- Drop the fresh templates' display text by two notches from the current sizes (52, 44, 30, 24), keeping the relative hierarchy. Report the exact new sizes in the summary.
- Do NOT touch the old Manim engine (`manim_infographic_engine.py`), the Mosaic side, or the design layer. No design call anywhere in this job.

### B. Composite footer (frame template + per-clip center)

- Regenerate `ddma/assets/chrome_249.png` with the new footer: "Manim" bottom-left, "Mosaic" bottom-right, same delimiter line above. Measure the current image first (label font, size, baseline y, left x, right x, rule y and thickness) and reproduce them exactly — only the two words change. Verify by visual diff against the old image: same black frame, same rule, only the words differ.
- Add the center "Part N of 21" as a per-clip drawtext in `segment_filter` (in `ddma/spec_h2_composite_assembler.py`): centered horizontally, same baseline and same font/size/style as the chrome labels, reading `Part {clip_num + 1} of {total}` where total is the episode's clip count from the plan. Thread the total through from the caller — `build_segment_cmd` and its callers — never hardcode 21.
- Update the frame-contract dict in the assembler to the new footer: left "Manim", center "Part N of 21" (per-clip), right "Mosaic", same style, delimiter line above, no invented copy.

### C. Re-render from the existing storyboards — no re-design

- Re-render all 21 of ep 249's Manim artifacts from the EXISTING storyboards (`projects/episode_249/storyboards/clip_N_storyboard.json`) using the updated templates, through the existing storyboard-to-render-to-compile path. No design call, no fresh cast, no storyboard edit.
- The storyboards and the plan's `infographic_scenes` must be byte-identical before and after. Hash them first; if any storyboard or plan scene changes, stop and report — that means a design step ran by accident.
- Then manually re-assemble the local master from the re-rendered artifacts via the existing H2 assembler path (which now uses the regenerated chrome image and the new per-clip center text), and re-gate it (the existing duration gate). No push to dd_hub — the push stays manual via the Push button, as always.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (push all / pull all; mdIngest is code-only, so a code change fans out to both).
- Episode 249 only. Do not touch 250. No Mosaic runs. No substitutions: a missing input is a reported refusal, never a fallback. No auto-assemble, no auto-push.
- Clip 1 first, then the rest (see Verify). Do not fold in the Patch-reload fix or the Manim prompt inspector — those are separate jobs with their own prompts.
- Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Clip 1 first: re-render clip 1 only, then patch it into a test segment (do not touch the live master yet). The new clip-1 Manim footer reads: title above the line; below the line, left "ULTIMATE ANCHOR" (clip 1's anchor label), right "deepDive podcast · Ep 249"; no collision with stage content or the frame edge; text smaller but legible. The composite footer on that segment reads "Manim" left, "Part 1 of 21" center, "Mosaic" right, same style as before. The clip-1 storyboard and the plan's clip-1 `infographic_scenes` are byte-identical to before (show the hashes). Stop here and show clip 1 to the user before doing the other 20 — if the sizes or positions are wrong, fix them on clip 1 only.
- V2 — All 21: re-render the remaining 20 the same way. Every artifact carries the new Manim footer with the correct focus for its kind (equation name / anchor label / diagram title / blank for title-only); every storyboard and every plan scene is byte-identical to before. Every segment's composite footer shows the correct "Part N of 21" for its clip (spot-check at least clips 1, 10, and 20).
- V3 — Spot-check clips 1 and 19 in the re-assembled master: both footers correct, text legible, strip and captions unchanged.
- V4 — Master: duration still ~1883.7 s (re-gated); 248 untouched; 250 untouched; no Mosaic run was triggered (check the fresh logs for Mosaic/push/hub lines: none).
- V5 — Tests: the existing suites still pass (report the count). Add a test that the fresh templates emit the new two-row footer (no title-only chrome without the sub-row) and that `segment_filter` emits the center drawtext with the right "Part N of total" for a sample clip/total, otherwise verify live and say so.

## Deliver

- Commit + push all (deepDive + mdIngest, code-only mirror for mdIngest). The regenerated `chrome_249.png` is a binary asset — commit it in deepDive.
- Append the build summary to Spec H2 as the next numbered summary, with the new font sizes, the new footer geometry, the V1–V5 results, and the commit hashes.
- Reply with the summary only — one short message, no extra commentary.
