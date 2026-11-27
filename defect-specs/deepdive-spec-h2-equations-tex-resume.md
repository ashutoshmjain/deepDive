# Prompt: Resume equations-as-math — the TeX source is in src/249.md

Copy this file into `defect-specs/` as `deepdive-spec-h2-equations-tex-resume.md` (freshness check: read the current Spec H2 file first; if a newer Spec H2 summary exists, append this as the next build summary instead of overwriting). Then implement it exactly as written. Episode 249 only. Do not touch episode 250. No Mosaic runs. No substitutions. No auto-assemble, no auto-push. Do NOT run the footer V2 (remaining 20 re-renders) in this job — that has its own go-ahead.

## Context

The previous job (Summary XI) STOPPED the equations-as-math work: KaTeX installs and renders, but the rendered episode page (`deepdive.shutri.com/249.html`) carries no TeX source — its 7 katex-display blocks are pre-rendered HTML with zero TeX markers. That part is correct and was verified independently (0 `application/x-tex` annotations, 0 MathML, no `$$` delimiters on the page).

What the previous job missed: **the TeX source is in the repo, in the markdown the page was built from — `src/249.md`.** It holds exactly 7 display equations (`$$...$$`, 14 delimiters), matching the page's 7 katex-display blocks one-to-one. Two of them are already verified as the clips' equations: the free-energy TeX (`F = \mathbb{E}_{q(\eta)}...`) is clip 3's 6:17 frame equation, and the modular-flow TeX (`\alpha_t^\rho(A) = \Delta^{it} A \Delta^{-it}...`) is clip 13's overflowing equation. Reading TeX from the author's own source markdown is NOT inventing — it is the original source. So the STOP is lifted: resume the math rendering from `src/249.md`.

## The fix

### A. Thread the TeX from src/249.md into the design

- Read the 7 display TeX equations from `src/249.md`. Match each one to its catalog entry by equation content — the stored plain-text norms are renderings of these same equations (list the full TeX↔norm mapping in the build summary; every catalog equation used by a clip must map to exactly one TeX source, or report which one does not and stop).
- Store the TeX alongside the norm in the storyboard/design (a data addition, not a re-design — the equation CHOICE for every clip stays exactly as designed; the norm stays as it is). If a clip's equation has no TeX source in `src/249.md`, report it and do not render that clip as math.

### B. Render as real math, fit fully

- Render each formula-stage equation via the already-installed KaTeX (npm global) to SVG, embedded in the Manim scene via `SVGMobject` — the path the previous job proved installs and renders on this machine. Report the KaTeX version used.
- The rendered math must fit inside the 740-wide Manim pane IN FULL — never clipped, never overflowing. Scale the rendered math to fit the pane width; when it is still too wide, split it into multiple rows breaking ONLY at top-level `=` / `+` / `−` (split the TeX at those operators and render each part), never mid-symbol, never mid-number, never inside a bracket group.
- Verify on the worst cases: clip 3 (previously wrapped mid-symbol) and clip 13 (previously showed only "a t p ("). Both must render as real math, in full, legible. Clip 1 (octonion basis) must render as real math too.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Do NOT commit or push in this job — the TeX resume + V2 commit as a batch after V2 (footer V1 + the XI equations are already committed, at 5658fd5d). Report and stop.
- Episode 249 only. Do not touch 250. No Mosaic runs. No re-design: equation choices, storyboards' stages and plan scenes stay as they are, apart from the added TeX field. No substitutions: a missing TeX source is a reported refusal for that clip, never a reconstructed equation. Do not run the footer V2 re-renders here.
- Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — TeX↔norm mapping: all 7 display TeX equations from `src/249.md` listed with their matching catalog norm (show the mapping). Any unmapped equation is reported, not silently dropped.
- V2 — Clip 3: the free-energy equation renders as real math, in full, split across rows only at `=` / `+` / `−` (show the rendered rows). Nothing clipped, nothing wrapped mid-symbol.
- V3 — Clip 13: the modular-flow equation renders as real math and fits fully inside the pane (show it). The previous "a t p (" overflow is gone.
- V4 — Clip 1: the octonion-basis equation renders as real math, in full.
- V5 — Data integrity: every storyboard is byte-identical to before apart from the added TeX field (show the diff of the changed fields — choice and norm unchanged); every plan scene is byte-identical. No Mosaic run was triggered (check the fresh logs for Mosaic/push/hub lines: none). Only clips 1, 3, 13 were re-rendered.
- V6 — Tests: the existing suites still pass (report the count).

## Deliver

- No commit, no push in this job. Append the build summary to Spec H2 as the next numbered summary (determine the number from the current Spec H2 file — do not hardcode it; XII was taken by the Patch job), with the TeX↔norm mapping, the KaTeX version, the V1–V6 results, and the re-rendered clip list (1, 3, 13 only).
- Reply with the summary only — one short message, no extra commentary.
