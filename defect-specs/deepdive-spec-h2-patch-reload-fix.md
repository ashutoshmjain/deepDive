# Prompt: Fix Patch reload (wrong episode + stale master + grey flash), honest Patch timing, episode memory

Copy this file into `defect-specs/` as `deepdive-spec-h2-patch-reload-fix.md` (freshness check: read the current Spec H2 file first; if a newer Spec H2 summary exists, append this as the next build summary instead of overwriting). Then implement it exactly as written. Episode 249 only. Do not touch episode 250. No Mosaic runs. No substitutions. No auto-assemble, no auto-push.

## Context

Beats Studio, ep 249, clip 1. The user redesigned clip 1 (design group h2-249-2), then pressed **Patch** and reported: nothing visibly changed, the whole video greyed out, a refresh defaulted the episode picker back to 248, and after re-selecting 249 and playing clip 1 there was still no visible change.

The Patch button is labelled "Patch (~8s)". That label is wrong, and the post-patch player reload has three verified defects. Fix all of them in this job.

## What the code shows (verify each claim in the tree before changing it)

1. **The "~8s" label is wrong by an order of magnitude.** `_h2_patch_clip_249` (beats_server.py) rebuilds the clip segment, then re-encodes the master head (0 to the clip start) AND the master tail (clip end to master end) with libx264 `veryfast` before the stream-copy concat. For clip 1 the tail is nearly the whole 31-minute movie, so a patch takes minutes, not ~8 seconds. The user waited ~8 seconds' worth of patience, saw nothing, and refreshed mid-patch, aborting the wait in his browser.
2. **The post-patch reload drops the episode.** `patchActiveLongformChapter` (beats.html) reloads the player with `videoEl.src.split('?')[0] + '?t=' + Date.now()`. The master URL is `/api/beats/video?ep=249`, so stripping the query produces `/api/beats/video?t=...` — and `/api/beats/video` defaults a missing `ep` to **248**. The player briefly loads the 248 master. That is the wrong episode on screen after a 249 patch.
3. **The cache-buster is defeated by the very next call.** The same handler then calls `selectLfChapter(cNum, false)`, which runs `applyPlaybackSource`, which compares `videoEl.getAttribute('src')` against the plain `video_url` (`/api/beats/video?ep=249`) and resets the src to the plain URL. The `?t=` cache-buster is gone. And `serve_media_file` sends **no cache headers at all** (no Cache-Control, no ETag, no Last-Modified), so the browser is free to serve the cached pre-patch master for the same URL. That is why "no visible change" after the patch.
4. **The seek is a race.** The handler sets `videoEl.currentTime` synchronously right after `videoEl.load()`, before metadata has loaded. The seek can be lost when the src is reset by step 3.
5. **A refresh defaults to 248.** `beatsEpisode()` returns the select value, else the `?ep=` URL param, else `'248'`, and the episode select has no memory of the last episode seen. (localStorage is already used in this page for the theme — follow the same pattern.)

## The fix

### A. Patch reload: correct episode, cache-buster that survives, seek after metadata

- After a successful patch, reload the player from the KNOWN master URL for the current episode — the timeline index `video_url`, i.e. `/api/beats/video?ep=<ep>` — with the cache-buster appended as an additional query parameter (`?ep=249&t=<timestamp>`), never by stripping the query off the current `videoEl.src`.
- The cache-buster must survive the `selectLfChapter` / `applyPlaybackSource` call that follows the reload. Either make the source comparison in `applyPlaybackSource` cache-buster-aware (compare the URL with the `t` parameter ignored), or set the reloaded src after that call. Whichever you choose, the URL the player finally settles on must still carry both `ep=<ep>` and the cache-buster.
- Seek only after metadata loads: attach a one-shot `loadedmetadata` listener and set `currentTime` inside it. Never set `currentTime` synchronously after `load()`.
- On patch failure, do not touch the video at all (this is already the behaviour — keep it). The failure toast must show the server's refusal reason (already the behaviour — keep it).

### B. Cache headers on media routes

- `serve_media_file` must send `Cache-Control: no-cache` on every response (200 and 206), so a same-URL master is always revalidated and never silently served stale after a patch. (no-cache still allows caching; it forces revalidation — that is the correct semantics for a file that changes in place.) Apply it to the routes that serve patched content: `/api/beats/video` and `/api/beats/clip_media` at minimum; the same helper serves both.
- Do not add aggressive `no-store` or versioned URLs anywhere else in this job.

### C. Honest Patch timing

- The button label and the patching toast must stop promising ~8 seconds. The "~8s" is hardcoded text in the page (`beats.html:113` — the button label and its `title` attribute — and `:736`, the in-progress `Patching (~8s)...` label). It reads like a leftover from the old beats era, when a patch touched one short beat; verify where the string lives and remove every occurrence. The patch re-encodes the head and tail of the master, so it takes minutes, and the time depends on the clip's position (longest for early clips, shortest for the last clip). Relabel the button and the in-progress toast honestly (for example "Patch (takes a few minutes)") and, while a patch is running, show the elapsed time on the button so the user can see it is working.
- Measure the actual clip-1 patch time on this machine and report it in the build summary. Do NOT change the ffmpeg re-encode to stream-copy in this job — exact cut points vs speed is a separate decision for the user.

### E. Move Patch into the design area

- Remove the Patch button (`#btn-patch-lf-chapter`) from the top button row and place it in the clip-level Manim design panel (the lower pane, next to "Design this clip"). Patch belongs to the design workflow — design a clip, then patch it into the master — not to the top playback row. Keep the same handler (`patchActiveLongformChapter`) and the same `id` unless the move requires a new one; if the id changes, say so in the summary.
- The top row keeps everything else unchanged (Play Clip, Play Full, Push, Design artifacts, Retrigger Manim-only, Retrigger Mosaic-only). Nothing else moves in this job.

### F. Patch is clickable only after Design this clip

- Patch starts DISABLED (greyed out, with a plain-language hint such as "Run Design this clip first" — a `title` attribute and/or a small hint line in the panel, not a toast).
- It becomes enabled only after "Design this clip" has run for the ACTIVE clip (a completed design job for that clip). The enabled state follows the active clip: selecting a different clip re-evaluates it — enabled only if that clip has had Design this clip run and has not yet been patched.
- After a successful Patch for a clip, Patch disables again for that clip until the next design run (there is nothing new to patch).
- The gate must survive a page reload for the common case: derive it from the same stored per-clip design state the design panel already reads, not from in-memory-only flags. If the stored state cannot tell "designed but not yet patched" from "already patched", say so in the summary and implement the session-only version (enabled after a design run in this session) — and report that a reload resets it.
- Open question to REPORT, not decide: a Mosaic-only retrigger also changes the clip's segment, so it arguably should also enable Patch. Do NOT silently extend the gate. Report it in the summary as an open question for the user.

### D. Episode memory

- Persist the last-selected episode in localStorage (same pattern as the existing `ddma-theme` key). On page load, when no `?ep=` parameter is present, default the episode select to the stored episode; fall back to the latest episode available. A plain refresh must keep 249 selected. Changing the episode (picker or `?ep=`) updates the stored value.
- This is the deferred "episode picker remembers the last episode" item. Build it now; it is part of this fix because it is what the user hit.

## Guardrails

- Pull all first (both deepDive and mdIngest clones), restart all four servers from the pulled tree, then implement. Commit + push all when done (push all / pull all; mdIngest is code-only, so a code change fans out to both).
- Episode 249 only. Do not touch 250. No Mosaic runs. No substitutions: a missing input is a reported refusal, never a fallback. No auto-assemble, no auto-push. The master is re-gated by the existing duration gate (unchanged).
- Do not re-design clip 1 in this job. The patched segment must match clip 1's currently stored Manim design, whatever it is — the design itself (formula vs anchor) is a separate open question, not this job. The footer/equations work is in separate jobs — do not fold it in.
- Root plan files (`ddma/plan.json`, `ddma/docs/plan.json`) stay uncommitted, as instructed.

## Verify (report PASS/FAIL per step, with the evidence)

- V1 — Patch clip 1 end-to-end live: the success toast names ep 249; the player reloads with a URL that still carries `ep=249` plus a cache-buster (read the URL back from the player); the video shows the clip-1 segment matching the currently stored Manim design at 2:24 with no grey/black flash and without ever showing 248's content; the seek lands at the chapter start.
- V2 — No stale master: after the patch, a plain page reload (no hard refresh) shows the new segment, not the cached old one. Confirm the `Cache-Control: no-cache` header on a `/api/beats/video?ep=249` response.
- V3 — Episode memory: select 249, plain-refresh the page, the picker still shows 249 (no `?ep=` in the URL). Select 248, refresh, it shows 248.
- V4 — Timing honesty: the button/toast no longer promise ~8s; the elapsed time shows while patching; report the measured clip-1 patch time in the summary.
- V5 — Regression: the master duration is still ~1883.7 s (duration gate held); the 248 master is byte-identical and untouched; the 250 episode is untouched; no Mosaic run was triggered (check the fresh logs for Mosaic/push/hub lines: none).
- V6 — Tests: the existing suites still pass (report the count); add a test for the reload-URL construction if it can be unit-tested at the helper level, otherwise verify live and say so.
- V7 — Patch placement: the Patch button sits in the Manim design panel next to "Design this clip" and is absent from the top row; the top row is otherwise unchanged.
- V8 — Patch gate: on load with no design run, Patch is disabled with the hint; run "Design this clip" for clip 1 → Patch enables; run Patch → it succeeds and disables again; select a clip with no design run → Patch disabled. Report whether the gate survives a plain refresh.
- V9 — Label: no "~8s" anywhere in the button, its title, or the in-progress text (grep the served page); the button shows elapsed time while patching.

## Deliver

- Commit + push all (deepDive + mdIngest, code-only mirror for mdIngest).
- Append the build summary to Spec H2 as the next numbered summary, with the measured patch time, the V1–V9 results, the new Patch placement, the gate behavior (including whether it survives a refresh) and the Mosaic open question, and the commit hashes.
- Reply with the summary only — one short message, no extra commentary.
