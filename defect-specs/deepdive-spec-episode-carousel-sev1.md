# Prompt: Fix the episode-page clip carousels — SEV 1 (stale / incomplete)

Copy this file into `defect-specs/` as `deepdive-spec-episode-carousel-sev1.md` (freshness check: read the current spec file first if it exists; append the build summary to it instead of overwriting). Then implement it exactly as written. Episodes 248, 249, 250 only. No Mosaic runs. No substitutions. No auto-assemble, no auto-push.

## Context

The public episode pages on deepdive.shutri.com show incomplete clip carousels. Verified on the live pages: 248 shows 7 clips, 249 shows 10, 250 shows none. The true clip counts (from the episode plans, `ddma/projects/episode_<ep>/plan.json`) are 248: 23 clips (nums 1–23), 249: 21 clips (0–20), 250: 14 clips (0–13).

Root cause: the carousel is hand-maintained inline HTML inside the episode markdown source (`src/<ep>.md` — a `video-carousel-container` div; each card is a `<video src="ddma/docs/episodes/<ep>/clips/<ep>-<n>.mp4">` plus a label bar reading `<ep>-<n> <Title>` plus a mute-toggle button). The source files carry the same gaps as the live pages (src/248.md: 7 clip links; src/249.md: 10; src/250.md: 0), so the live site is faithfully rendering stale source — the carousel was never updated as clips were published. The fix is to fill in the missing cards in the source and rebuild + redeploy the site.

## The fix

- In `src/248.md`, add carousel cards for clips 8–23 (the existing 1–7 stay exactly as they are). In `src/249.md`, add cards for clips 10–20 (the existing 0–9 stay exactly as they are). In `src/250.md`, add the whole carousel (clips 0–13), placed where the other pages' carousels sit.
- Copy the existing card markup exactly — same div, same video attributes, same label-bar style, same mute-toggle button — changing only the clip number, the video src, and the label text. Use the plan titles below verbatim (do not invent or improve titles; 250-3 "Part 3" and 250-6 "Part 6" are the plan titles as they stand).
- 248 (add 8–23): 8 "It's Mathematically Guaranteed to Fail", 9 "But We Are Talking About a Neural Network", 10 "The Ai Observes the Token Congestion Internally", 11 "I Love the Mechanics of a Waterfall Structure", 12 "It Doesn't Have a Social Security Number", 13 "And it Achieves This by Utilizing the Lightning Network", 14 "And the Network Generates This Unique", 15 "What Does it Actually Do with the Money", 16 "Why Not Accumulate Stable Coins Like Usdt or Usdc", 17 "But the Crypto Ecosystem is Vast", 18 "No Matter How Autonomous Its Code is", 19 "Level Rude Access to the Operating System", 20 "Nonstop Demand Hitting the Bitcoin Network", 21 "They Introduced the Concept of Community Intelligence", 22 "It Paints a Picture of Intense Systemic Turbulence", 23 "It is a Radical Reframing of What Intelligence".
- 249 (add 10–20): 10 "Color Confinement", 11 "Anticolors", 12 "Electric Charge", 13 "Chiral Mirror", 14 "Spin One Half", 15 "Arrows Of Time", 16 "Chiral Equilibrium", 17 "Imbalance Delta", 18 "The Observer", 19 "Infinite Creation", 20 "State Zero".
- 250 (add the carousel, 0–13): 0 "What Exactly is Infinity?", 1 "Ultimate Anchor", 2 "Logic Bomb", 3 "Part 3", 4 "Absolute Indeterminate Infinity", 5 "Terminal Boundary", 6 "Part 6", 7 "Hitting The Hardware", 8 "Cost Of Nullity", 9 "Sacred Four", 10 "Building Reality", 11 "16-Dimensional Collapse", 12 "Quantum Black Holes", 13 "Boundless Horizon, Concluding".
- Do not touch anything else on these pages (no wording, equation, or section changes). Do not touch any other episode page. The .md changes go to deepDive only — mdIngest is code-only and holds no episode markdown.
- Rebuild + redeploy the mdbook site using the repo's existing build/deploy path, so the live pages pick up the change.

## Build summary I - clip carousels filled (2026-11-26)

Cards added exactly as specified, markup byte-copied from the
existing cards (only clip number, src, label differ): 248 clips
8-23 (16 cards, titles verbatim incl. "Level Rude Access to the
Operating System"), 249 clips 10-20 (11 cards), 250 full block of
14 cards (0-13) placed after SIDEBAR_TITLE where 248/249 sit, with
the VIDEO_STRIP_START marker, social center, and toggle script
copied byte-exact from 249.md. Pure additions: 228 insertions, 0
deletions across the three files (one seam extra-close fixed
before commit; final 226 insertions, div-balance verified
23/21/14 cards inside their containers). All three sources stay
CRLF. Plan titles re-verified against
`ddma/projects/episode_<ep>/plan.json` (248: 23 nums 1-23; 249: 21
nums 0-20; 250: 14 nums 0-13) -- all spec titles match verbatim.

V1 PASS (source): 248.md 23 links (1-23), 249.md 21 (0-20),
250.md 14 (0-13) plus the carousel container.
V2 PASS on local build (`mdbook build` clean apart from
pre-existing katex matrix warnings and a pre-existing 248
footnote warning; book/248.html 23 cards, 249.html 21, 250.html
14). Live check runs after the deploy this push triggers
(GitHub Actions -> Pages); pre-deploy live baseline 7/10/0
recorded 2026-11-26.
V3 PARTIAL, reported honestly: 249's new videos resolve
(249-10.mp4 HTTP 200 live). Missing mp4s -- reported, not
substituted, not skipped: 248 clips 8-23 (no local file, hub has
no clips dir for 248, live 404) and 250 clips 3-13 (only 250-0..2
published; hub 250 holds mp3/mosaic only). The new cards link the
canonical paths and resolve when Cutroom publishes those clips.
V4 PASS: diff is the 3 .md files only (plus this spec); book/
output is gitignored; no other page touched.
V5 PASS: deepDive suite 84 tests, 1 error = the known
pre-existing `test_mosaic_pipeline_recovery` corrupt.json error
in an untouched file. mdIngest suite identical (84/1 same
pre-existing error). mdIngest carries no markdown change
(code-only clone) -- push there is a no-op verify.

Missing-mp4 report (27 files, see V3): 248-8..248-23,
250-3..250-13 absent from `src/ddma/docs/episodes/<ep>/clips/`
(the path the carousel src resolves against) and from
`ddma/clips/`. Publishing them is Cutroom work, out of scope.

Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) and the
pending TeX/V2 batch files stay uncommitted. Servers restarted
from the pulled tree before implementing (8088/3000/8000/8001 all
200); one duplicate-listener pair on :8000/:8001 from an
absolute-path supervisor spawn was killed, singles verified.

V2-live CONFIRMED post-deploy (2026-11-26, ~4 min after push
9682aed7): 248.html 23 cards, 249.html 21, 250.html 14; new
249 videos 200 (249-10, 249-15 probed); 248-8..23 still 404 as
reported in V3.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (deepDive carries the .md changes; mdIngest only if code changed, which it should not).
- No Mosaic runs. No substitutions: a clip whose mp4 is not present at `ddma/docs/episodes/<ep>/clips/<ep>-<n>.mp4` is reported, not skipped silently and not linked to a different file. Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Source: `src/248.md` contains 23 clip links (1–23), `src/249.md` contains 21 (0–20), `src/250.md` contains 14 (0–13) plus the carousel container. Show the counts.
- V2 — Live: fetch https://deepdive.shutri.com/248.html, /249.html and /250.html after the deploy and count the carousel cards on each live page (expect 23 / 21 / 14). Show the counts.
- V3 — Spot-check: at least three of the newly added clip videos resolve (HTTP 200 on the video URL) — one per episode.
- V4 — No collateral: the diff shows only the three .md files (plus the built site output) — no other page's content changed.
- V5 — Tests: the existing suites still pass (report the count).

## Deliver

- Commit + push all (deepDive + mdIngest as above).
- Append the build summary to this spec file (at the end, as the next numbered summary if one exists), with the V1–V5 results and the commit hashes.
- Reply with the summary only — one short message, no extra commentary.
