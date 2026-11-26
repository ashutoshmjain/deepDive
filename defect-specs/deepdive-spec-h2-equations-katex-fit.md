# Prompt: Equations as real math (KaTeX/LaTeX) + fit fully + footer title = clip title + player true 16:9

Copy this file into `defect-specs/` as `deepdive-spec-h2-equations-katex-fit.md` (freshness check: read the current Spec H2 file first; if a newer Spec H2 summary exists, append this as the next build summary instead of overwriting). Then implement it exactly as written. Episode 249 only. Do not touch episode 250. No Mosaic runs. No substitutions. No auto-assemble, no auto-push. Do NOT run the footer V2 (remaining 20 re-renders) in this job — that has its own go-ahead, pending the concurrent-activity investigation.

## Context

Beats Studio, ep 249. The user reviewed the master at clips 3, 7 and 13 and found four visual defects (screenshots 2026-11-26):

- Clip 3 (Division Algebras, 6:17): the equation renders as plain `Text` — ASCII-looking, broken across lines mid-symbol (`F = Eq(η)[lnq(η) − lnp(η` / `s)] = …`), ugly and hard to read.
- Clip 13 (Chiral Mirror, 20:22): the equation renders so large it overflows the pane — only the first glyphs are visible ("a t p ("), the rest is cut off.
- Clip 1 / 7 (anchor clips): the Manim footer shows the anchor label twice — "ULTIMATE ANCHOR" above the line and again below-left — because the above-line title is taken from the design's label instead of the clip title.
- The player: the video is letterboxed inside a too-wide player box, so the two panes look bunched in the center of a wide black canvas (see §D for the verified cause).

## What the code shows (verify each claim in the tree before changing it)

- Equations are rendered as Manim `Text` from the stored equation text (`manim_fresh_design.py` render path). The stored equation norms are plain-text approximations (e.g. `x = x 0 e 0 + i = 1 ∑ 7 x i e i`) — they are NOT valid LaTeX. The real LaTeX source lives in the episode page's katex-display blocks (`deepdive.shutri.com/249.html`), which is where the equation catalog was built from.
- Manim rendering in this environment is Text-only — no LaTeX/Tex is known to be installed. Check before choosing a path.
- The player element is `beats.html:119`: `<video id="lf-studio-video-player" style="width: 100%; max-height: 360px; aspect-ratio: 16/9; …">`. The `max-height: 360px` cap overrides the 16/9 aspect ratio, making the box ~3.7:1, so the 16:9 video letterboxes inside it with wide black side bars. That is the whole cause — the video itself is a true 1920×1080 landscape.

## The fix

### A. Equations as real math — KaTeX or LaTeX

- Render every formula-stage equation as real mathematical typesetting (proper glyphs, spacing, sub/superscripts) instead of plain `Text`.
- First check what exists on this machine: is LaTeX (`pdflatex` / `xelatex`) installed? If yes, Manim `MathTex` is an option. Preferred path (no new install): KaTeX renders the equation to SVG, and the SVG is embedded in the Manim scene via `SVGMobject`. Pick the path that works on this machine and report which one you used and why.
- The equation source must be the episode page's KaTeX/LaTeX source, not the stored plain-text norm. Thread the LaTeX source from the catalog into the design: store it alongside the norm in the storyboard/design (a data addition, not a re-design — the equation CHOICE for every clip stays exactly as designed). If the catalog does not already carry the LaTeX source, re-read it from the episode page for the 21 chosen equations. If neither KaTeX nor LaTeX is available on the machine, report that and STOP — do not invent a third renderer.
- Do NOT re-design any clip in this job. The equation choices, the storyboards' stages and the plan scenes stay as they are, apart from the added LaTeX-source field (list exactly which fields change in the summary — the design choice and norm must be unchanged).

### B. Equations must fit fully — scale to fit, break at operators

- The rendered equation must fit inside the 740-wide Manim pane IN FULL — never clipped, never overflowing. Scale the rendered math to fit the pane width; when it is still too wide, split it into multiple rows breaking ONLY at appropriate points: `=` signs, `+` / `−` and other binary operators — never mid-symbol, never mid-number, never inside a bracket group.
- Verify on the worst cases: clip 3 (currently wraps mid-symbol) and clip 13 (currently shows only "a t p ("). Both must render in full, legible, as real math.

### C. Footer title = clip title, not the design label

- In the Manim footer (`_chrome_bottom`, fresh templates only), the above-line title must be the clip's PLAN title, uppercased as the chrome does today ("8D TOTALITY", "DIVISION ALGEBRAS", "CHIRAL MIRROR") — never the design's label. The design's focus stays below-left as specified (anchor label for anchor clips, equation name for formula clips, diagram title for diagram clips, blank for title-only).
- This fixes the V1 duplication: clip 1 reads above "8D TOTALITY", below-left "ULTIMATE ANCHOR". The big center text (the anchor visual itself) is unchanged.

### E. Oracle test must not read the shared root plan (follow-up from the 5:33 investigation)

- The 5:33 flip showed the cause: the root `plan.json` is a working copy of the currently-loaded Cutroom project — opening episode 250 in Cutroom (just looking, no edits) copies 250's plan into the root, and triggering a Mosaic run on 250 also saves 250's plan into the root (`save_plan` writes the root copy on every save). So the root plan flips to 250's whenever the user does his normal 250 work.
- `test_fresh_assembly_total_matches_oracle` (`ddma/tests/test_spec_h2_composite_assembler.py`) reads the clip list from that shared root copy and asserts 21 clips — so any 250 work breaks the 249 suite with a false failure. Change it to read `projects/episode_249/plan.json` (fall back to the canonical hub plan if the local episode plan is absent, as the code-only mirror clone has no plan files), never the root `plan.json`. Test-only change; no production code.

### F. Player shows true 16:9 landscape

- In `beats.html`, remove the `max-height: 360px` cap from the `#lf-studio-video-player` element so the `aspect-ratio: 16/9` governs the box (width 100%, height whatever 16:9 dictates at the panel width). No other player change in this job.
- Verify: the frame fills the element edge-to-edge with no side bars; SATOSHA/SATOSHI spread across the full width at their true positions; the Manim and Mosaic panes sit at their true left/right positions. (The player will get taller — that is the correct landscape display.)

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Do NOT commit or push in this job — the batch (footer V1 + this job + V2) commits once after V2. Report and stop.
- Episode 249 only. Do not touch 250. No Mosaic runs. No substitutions: a missing input is a reported refusal, never a fallback. No auto-assemble, no auto-push. Do not run the footer V2 re-renders here.
- Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Clip 1: the footer reads above "8D TOTALITY", below-left "ULTIMATE ANCHOR", below-right "deepDive podcast · Ep 249". No duplication, no collision, legible.
- V2 — Clip 3: the equation renders as real math, in full, split across rows only at `=` / `+` / `−` (show the rendered rows). Nothing clipped, nothing wrapped mid-symbol.
- V3 — Clip 13: the equation renders as real math and fits fully inside the pane (show it). The previous "a t p (" overflow is gone.
- V4 — Player: the master fills the player edge-to-edge at true 16:9; no side bars; strip and panes at their true positions (check the SATOSHA/SATOSHI spread against the frame geometry).
- V5 — Data integrity: every storyboard is byte-identical to before apart from the added LaTeX-source field (show the diff of the changed fields — choice and norm unchanged); every plan scene is byte-identical. No Mosaic run was triggered (check the fresh logs for Mosaic/push/hub lines: none).
- V6 — Tests: the existing suites still pass (report the count). Add a test that the equation renderer fits a wide equation inside the pane (scale/break logic) and that the footer title uses the plan title, otherwise verify live and say so.
- V7 — Oracle test immune to the root plan: with the root `plan.json` temporarily holding 250's 14-clip data, run `test_fresh_assembly_total_matches_oracle` — it must PASS (it no longer reads the root copy). Then restore the root plan to 249's and re-run the suite green.

## Deliver

- No commit, no push in this job. Append the build summary to Spec H2 as the next numbered summary, with the chosen math path (KaTeX→SVG or MathTex) and why, the V1–V7 results, and the re-rendered clip list (1, 3, 13 only).
- Reply with the summary only — one short message, no extra commentary.
