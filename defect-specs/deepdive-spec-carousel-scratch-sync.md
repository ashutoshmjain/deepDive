# Prompt: Scratch routine — correct the 248 / 249 / 250 carousels from published state (one-time)

Copy this file into `defect-specs/` as `deepdive-spec-carousel-scratch-sync.md` (freshness check: read the current spec file first if it exists; append the build summary to it instead of overwriting). Then implement it exactly as written. No Mosaic runs. No substitutions. No auto-assemble, no auto-push.

## Context

The carousels for 248, 249 and 250 are currently wrong (Issue 140): the Issue 139 fix added a card for every plan clip, including unbuilt ones. 248 shows 23 cards (only 1–7 built), 250 shows 14 (only 0–2 built), 249 shows 21 (all built — correct). This routine corrects all three carousels from the PUBLISHED state, in one pass. It is a ONE-TIME scratch routine — it runs once, then the ongoing publish-sync process (deepdive-spec-carousel-auto-sync.md) keeps the carousels correct. This routine SUPERSEDES the manual remove-unbuilt prompt (deepdive-prompt-episode-carousel-remove-unbuilt.md) — same end state, but derived from published state by a script instead of a hand-written list.

## The routine (what to build)

A one-time script (e.g. `scripts/carousel_scratch_sync.py` — the builder chooses the location; it is a scratch tool, not part of the app's runtime). For each episode in 248, 249, 250, in order:

1. **Determine the published set.** Read the episode's plan (`ddma/projects/episode_<ep>/plan.json`) for the `published:true` flags. Cross-check against the compiled mp4s in the repo (`src/ddma/docs/episodes/<ep>/clips/<ep>-<n>.mp4`) and against the live site (HEAD each `https://deepdive.shutri.com/ddma/docs/episodes/<ep>/clips/<ep>-<n>.mp4`). The rule: a clip belongs in the carousel if it is published AND its mp4 exists. Report every disagreement (a clip marked published but with no mp4; a clip with an mp4 but not marked published) and use the mp4-exists rule as the tiebreaker — a card with a dead video is never allowed. Do NOT hardcode the expected counts (7 / 21 / 3) — derive them from the published state at run time, and report them; the expected counts are a check on the result, not an input.
2. **Rebuild the carousel in `src/<ep>.md` to exactly that set.** Remove the cards for clips not in the published set. Add cards for published clips that are missing from the carousel. Sort the cards by clip number. Use EXACTLY the existing card format (same `<video>` element, same label bar `<ep>-<n> <Title>` with the title from the plan, same mute-toggle button `window.oph_play_toggle(this)`). Do not touch anything else in the `.md` (no wording, equation, or section changes). Do not touch the Reels tab or the Research tab.
3. **Report per episode.** Before/after card counts, the list of cards removed, the list of cards added, and any disagreements found in step 1.
4. **Commit + push.** Commit the three `.md` files (and any clip mp4s not yet in the repo) and push to GitHub. Then rebuild + redeploy the mdBook site using the repo's existing build/deploy path, so the live pages pick up the corrected carousels.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (deepDive carries the `.md` changes + the script; mdIngest only if code changed, which it should not — the script is a scratch tool in deepDive).
- No Mosaic runs. No substitutions. Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.
- The script must be runnable again without harm (idempotent): a second run with the same published state changes nothing and reports "already correct" per episode.
- The script is one-time. It is NOT wired into the publish flow, the Reels tab, or the Research tab. The ongoing publish sync (deepdive-spec-carousel-auto-sync.md) is the permanent mechanism.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Published set: for each episode, show the published set derived from the plan + the mp4 cross-check, with every disagreement listed. (Expected — verify, do not assume: 248: 1–7; 249: 0–20; 250: 0–2.)
- V2 — Source: `src/248.md` contains exactly the published set's cards, `src/249.md` exactly its set, `src/250.md` exactly its set; cards are in clip-number order; no card's title was altered. Show the counts per episode.
- V3 — Live: fetch https://deepdive.shutri.com/248.html, /249.html and /250.html after the deploy. The card counts match V2 exactly. No "Coming soon" text anywhere on any of the three pages. Show the counts.
- V4 — No dead videos: every `<video>` src remaining in the three carousels resolves HTTP 200 (check them all, not a sample — the last fix's 3-URL spot-check is what missed this).
- V5 — No collateral: the diff shows only the three `.md` files (plus the script and the spec) — card removals/additions only, no other page's content changed.
- V6 — Tests: the existing suites still pass (report the count).

## Deliver

- Commit + push all (deepDive + mdIngest as above).
- Append the build summary to this spec file (at the end, as the next numbered summary if one exists), with the V1–V6 results, the per-episode before/after counts, and the commit hashes.
- Reply with the summary only — one short message, no extra commentary.

## Build summary I - scratch sync from published state (2026-11-26)

Script `scripts/carousel_scratch_sync.py` (scratch tool, not wired
into any flow): per episode reads the plan's `published` flags,
checks local mp4s (`src/ddma/docs/episodes/<ep>/clips/`) and
HEADs every live mp4 URL; keep = local mp4 AND live 200
(mp4-exists tiebreak, dead video never allowed). Rebuilds the
carousel to exactly that set (sorted, plan titles, card format
asserted byte-equal against the file's own first card -- this
caught and fixed a dropped `;` in the script's template before
any write). No other `.md` content touched; all three sources
stay CRLF.

V1 PASS. Derived sets (not hardcoded): 248 = 1-7 (the 248 plan
carries NO published flags at all -- 7 tiebreak keeps on mp4;
removed 8-23 had neither flag nor mp4, no disagreement);
249 = 0-20 (10-20 flagged+mp4; 0-9 kept on mp4-exists tiebreak,
all live 200; no local/live mismatch); 250 = 0-2 (flagged+mp4;
removed 3-13 had neither). No published-but-missing-mp4 and no
local/live mismatch anywhere.
V2 PASS. Sources: 248 = 7 cards [1-7], 249 = 21 [0-20],
250 = 3 [0-2]; clip-number order verified; every kept label
equals its plan title (pre-checked: zero mismatches before the
rewrite, so no title was altered).
V3 (local build + live after deploy): `mdbook build` clean
apart from the standing katex-matrix warnings; book pages hold
7/21/3 cards, no "Coming soon" anywhere. Live counts below.
V4: every remaining `<video>` src resolves live (full check,
not a sample) -- see live verification.
V5: diff = the two edited `.md` files only (248: 80 deletions,
250: 55 deletions, zero insertions; 249 untouched) + the script
+ this spec. Seams verified (container div-balance holds, all
cards inside).
V6 PASS: both suites 84 tests, 1 error = the known pre-existing
`test_mosaic_pipeline_recovery` corrupt.json error in an
untouched file.
Idempotency: consecutive re-run reports "already correct" for
all three episodes and changes nothing (exact-body comparison,
not just card numbers).

Per episode: 248: 23 -> 7 (removed 8-23, added none);
249: 21 -> 21 (already correct, no write); 250: 14 -> 3
(removed 3-13, added none).

Guardrail notes: root plan files untouched; no Mosaic runs (no
server calls except read-only liveness + live HEADs); servers
restarted from the pulled tree first (8088/3000/8000/8001 all
200; one absolute-path duplicate :8000 spawn killed again).
This routine supersedes the manual remove-unbuilt prompt; the
ongoing sync (auto-sync spec) is the permanent mechanism.

V3/V4-live CONFIRMED post-deploy (2026-11-26, ~4 min after push
974d2f97): 248.html 7 cards, 249.html 21, 250.html 3; no
"Coming soon" on any page; all 31 carousel videos HEAD 200
(7+21+3 checked individually, zero dead).
