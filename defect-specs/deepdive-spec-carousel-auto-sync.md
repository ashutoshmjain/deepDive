# Prompt: Automate the episode carousel — update it at publish time (publish sync)

Copy this file into `defect-specs/` as `deepdive-spec-carousel-auto-sync.md` (freshness check: read the current spec file first if it exists; append the build summary to it instead of overwriting). Then implement it exactly as written. No Mosaic runs. No substitutions. No auto-assemble, no auto-push.

## Context

The episode-page carousel is hand-maintained inline HTML in `src/<ep>.md` (a `video-carousel-container` div; each card = `<video src="ddma/docs/episodes/<ep>/clips/<ep>-<n>.mp4">` + a label bar `<ep>-<n> <Title>` + a mute-toggle button `window.oph_play_toggle(this)`). It went stale because updating it was a manual step that got skipped (after 249-9, clips 10–20 were published but the carousel was never synced), and the manual fix then overcorrected by adding every plan clip, built or not (Issues 139/140). The fix is to make the carousel update part of the publish itself: when a clip is published, its card is added to `src/<ep>.md` automatically, and the `.md` is pushed to GitHub along with the clip.

Out of scope (do not touch): the Reels tab in Cockpit and the Research tab — this job covers only the episode-page carousel in `src/<ep>.md` and the publish flow. Do not remove cards for hidden/deleted clips (that case is explicitly out of scope — removal is a manual decision, not part of this automation).

## The process (what to build)

A carousel-sync step that runs as part of every clip publish in Cutroom:

1. **Trigger.** A clip publish succeeds in Cutroom (the per-clip Publish — the platforms post and the publish is recorded in the plan as `published:true` + `published_url`). The sync runs immediately after the publish, before the publish commit.
2. **Preconditions (both must hold, or the card is NOT added and the reason is reported):**
   - The clip's compiled mp4 exists in the repo at `src/ddma/docs/episodes/<ep>/clips/<ep>-<n>.mp4`.
   - The plan marks the clip `published:true`.
   If either is missing, the sync does nothing to the carousel and reports which precondition failed. A card with a dead video is never allowed.
3. **The sync.** A small function/module (name it `carousel_sync`, placed where the publish flow can call it — the builder chooses the file, e.g. alongside the publish handler in `ddma/scratch/run_curator.py` or a new `ddma/carousel_sync.py`):
   - Opens `src/<ep>.md` and finds the `video-carousel-container` div.
   - If a card for this clip is already present (same `<video src>`), do nothing and report "already present" (idempotent — re-running a publish must never duplicate a card).
   - Otherwise, inserts the card in clip-number order (after the previous clip's card, before the next). The card uses EXACTLY the existing card format (same `<video>` element, same label bar `<ep>-<n> <Title>` with the title from the plan, same mute-toggle button `window.oph_play_toggle(this)`). Do not change the format of any existing card.
   - Never removes a card, never reorders existing cards, never touches any other episode's page, never touches the Reels tab or the Research tab.
4. **Commit + push together.** The `.md` change rides in the SAME commit/push as the clip (the clip mp4 + the plan updates + the `.md` change travel together to GitHub). If the builder finds the publish flow does not itself commit (i.e. the user/Muse Code commits the publish manually), the sync still updates the `.md` and reports it as a pending change to be included in the publish commit — do NOT invent a new commit path or a separate push.
5. **Deploy.** After the push, rebuild + redeploy the mdBook site using the repo's existing build/deploy path, so the live episode page shows the new card.
6. **Report.** The publish report now includes the carousel sync outcome: "card added" / "already present" / "not added (reason)". A publish that adds no card for a reason must say so in the report, never silently.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (deepDive carries the code + `.md`; mdIngest only the code files, code-only mirror).
- No Mosaic runs. No substitutions. Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.
- The sync must work for any episode (248, 249, 250 and future ones) — no episode-specific hardcoding. The clip number, title and mp4 path come from the plan and the repo, never from a hardcoded list.
- The sync must not depend on the Reels tab or the Research tab, and must not change them.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Unit: the sync adds a card for a published clip with an existing mp4; is a no-op (no duplicate) when the card is already present; refuses (no card, reason reported) when the mp4 is missing; refuses when the plan does not mark the clip published; inserts the new card in clip-number order. Show the test results.
- V2 — End to end (dry run): re-run the sync for a clip that is already published and already in the carousel (e.g. 249-20 or 250-2) and confirm it is a no-op with "already present" reported, and that `src/<ep>.md` is unchanged (no diff).
- V3 — Live: after the build is deployed, publish a test clip (or use the next real publish) and confirm the live episode page shows the new card and its `<video src>` resolves HTTP 200.
- V4 — No collateral: the diff shows only the intended code files (plus the spec) — no other page's content changed, no card removed, no existing card reformatted.
- V5 — Tests: the existing suites still pass (report the count).

## Deliver

- Commit + push all (deepDive + mdIngest as above).
- Append the build summary to this spec file (at the end, as the next numbered summary if one exists), with the V1–V5 results and the commit hashes.
- Reply with the summary only — one short message, no extra commentary.

## Build summary I - publish-time carousel sync (2026-11-26)

New module `ddma/carousel_sync.py` (`sync_carousel_card`, CRLF to
match ddma convention): preconditions = repo mp4 exists AND plan
`published:true` (else "not added (reason)", never a dead-video
card); idempotent "already present" check on `<video src>`;
insertion in clip-number order with the card template asserted
byte-equal against the page's own first card (the drift guard that
caught the scratch script's dropped `;`); add-only, other
episodes/Reels/Research untouched; carousel-level problems return
a status, never raise. Wired into the Cutroom publish handler in
`ddma/scratch/run_curator.py`: runs after `save_plan` (d2) as new
step (d3, non-fatal), the episode page joins the scoped publish
commit (`rel_page`, git-add no-ops when already present), and the
publish response JSON carries the outcome as `"carousel"`
("card added" / "already present" / "not added (reason)").

V1 PASS: 7/7 new unit tests
(`ddma/tests/test_carousel_sync.py`, tmp fixture repos) -- add,
already-present no-duplicate, mp4-missing refusal, unpublished
refusal, append-after-last + middle insertion order, CRLF purity,
format-equals-existing.
V2 PASS (dry run, real repo): 249-20 and 250-2 report "already
present", `git diff src/` empty. 248-7 reports "not added (plan
does not mark clip 248-7 published)" -- the refusal path working
on real data (248 carries no published flags).
V3 NOT RUN by design: no test clip was published (a publish posts
to platforms and pushes -- never triggered unilaterally); the add
path is unit-covered and the wiring runs inside the next real
publish, whose response will carry the carousel outcome. Live
confirmation deferred to the next real publish.
V4 PASS: diff is `ddma/carousel_sync.py` (new),
`ddma/scratch/run_curator.py` (+24/-3: d3 step, rel_page,
response field), `ddma/tests/test_carousel_sync.py` (new) and
this spec. No page touched (V2 proved no diff), no card removed,
no Reels/Research contact (module imports nothing of them).
V5 PASS: both suites 91 tests, 1 error = the known pre-existing
`test_mosaic_pipeline_recovery` corrupt.json error in an
untouched file (deepDive and mdIngest identical).
mdIngest mirror: the three code files only (byte copies).

Guardrail notes: no Mosaic runs (only read-only liveness + the
unit/dry-run calls); root plan files untouched; no episode
hardcoding (everything from plan + repo); the running :8000/:8001
were restarted from the pulled tree first -- note the servers
held this working tree's pre-edit code during the dry run, which
is fine because the dry run called the module directly, not the
endpoint. The duplicate absolute-path :8000/:8001 spawns were
killed again (third job in a row -- something re-spawns them;
worth one investigation, out of scope here).
