# Fix: Publish button falsely reports "already published" after a failed push

## Where

`ddma/scratch/run_curator.py`, the `/publish-clip` handler, step (e) — the scoped git add + commit + push block (around lines 4225–4255 at deepDive head `a6b4b7c8`). The handler is the per-clip Publish endpoint (Issue 80). The relevant code:

- `git add <clip> <both manifests>` then `git diff --cached --name-only` to see if anything staged.
- If nothing staged, `git diff --quiet HEAD -- <clip> <manifests>`; if that returns 0 (working files match HEAD), it sets `already = True` and skips the commit AND the push.
- If not already, it commits and pushes (`git push`, `check=True`).
- On success it sets `target_clip["published"] = True` and `published_url`, then returns `{"success": True, "already_published": already, ...}`.

## Finding

The "already published" idempotency check only compares the working files to the LOCAL HEAD. It never checks whether the local HEAD has been pushed to the remote. So a clip whose publish commit exists locally but was never pushed is reported as "already published."

Reproduction — live right now, clip 249-15 (episode_249, clip 15):

1. First Publish: `git add` staged the clip + manifests, so `already` stayed False. It committed locally, then `git push` FAILED with "fetch first" (the remote had commits the workbench did not have). The handler raised a 500. But the local commit EXISTS.
2. The user pulled the remote (syncing those commits), then clicked Publish a second time.
3. Second Publish: `git add` staged nothing (the clip + manifests already match the local HEAD, because the first Publish committed them), and `git diff --quiet HEAD` returned 0. So `already = True` — it reported success with `already_published: true` WITHOUT pushing.
4. Result: the clip is still NOT on GitHub (249-15 404s, remote head still `a6b4b7c8`), the local branch is still "ahead of 'origin/master' by 1 commit" (the 249-15 publish commit sits local, unpushed), yet the button said "already published."

Contrast: for 249-13 the same "Already published" response was CORRECT, because that push had succeeded. The check cannot tell the two cases apart — it conflates "files match the local HEAD" with "files are on the remote."

## Fix

Make the "already published" determination remote-aware. In step (e), when the files match HEAD (the current `already` condition), ALSO check whether the local branch is ahead of the remote before reporting "already published":

1. Determine if the local HEAD is ahead of the remote tracking branch (for example, fetch the remote ref and count `origin/master..HEAD`, or equivalent). Do this AFTER the `git add` / `git diff --cached` / `git diff --quiet HEAD` checks, only on the path where `already` would be True.
2. If the local HEAD is ahead (unpushed commits exist), the clip is NOT actually published: do NOT set `already = True`. Instead, run `git push` (the same push the fresh path runs) and report success only if the push succeeds. If the push fails, raise the error exactly as the fresh path does (500, "Git publish failed: ...") — do not report success.
3. Only report "already published" (`already = True`, no commit, no push) when the files match HEAD AND the local HEAD is not ahead of the remote (the remote already has the clip).
4. Confirm the plan-persist step (f2) still runs only on the success path: `target_clip["published"] = True` and `published_url` must NOT be set when the push fails. (At head the exception in step (e) skips (f2), so this should already hold — verify it, do not change it unless it does not hold.)
5. Do not change the scoped behavior: ONLY the clip + both manifests are ever added/committed/pushed. Do not broaden the pathspec. Do not auto-lock, do not change the lock gate, and do not change the compile/compile-clip fallback in step (b).

Guardrails: pull the latest deepDive first. Edit only `ddma/scratch/run_curator.py` (the handler lives there; the fan-out mirrors it to ddma). No Mosaic runs. No commit-or-push beyond the fix itself (commit the fix, push it, and fan it out per the repo's GEMINI.md push protocol). Do not run the 249-15 publish yourself as part of the fix — the user will re-Publish 249-15 after restarting :8000 to verify.

## Verify

Verify against the LIVE 249-15 state (do not stage a fake failure — the reproduction is already on the workbench):

1. **The false "already published" is gone.** After the fix is in and :8000 is restarted (the server loads `run_curator.py` at startup, so a restart is required to pick up the change), the user re-Publishes clip 249-15 (POST `/publish-clip?id=episode_249&num=15` or the Publish button). It must actually PUSH — the response must have `already_published: false` — and 249-15 must become reachable on GitHub (HTTP 200 at `https://github.com/ashutoshmjain/deepDive/blob/master/src/ddma/docs/episodes/249/clips/249-15.mp4`), and the local branch must no longer be ahead. If it still reports `already_published: true` while the clip is not on the remote, the fix did not work.
2. **True idempotency still works.** After a clip IS on the remote, a re-Publish must still return "Already published" with `already_published: true` and must NOT create a duplicate commit or push. Use 249-13 (already published and on the remote) as the control: re-Publish it and confirm `already_published: true`, no new commit, no push.
3. **Push failure still fails loudly.** By code inspection (do not stage a fake remote failure): confirm that a `git push` failure in the new "ahead" path raises the 500 with "Git publish failed: ..." and does NOT set `published = True` in the plan. Report the lines that establish this.
4. **No regression in the scoped publish.** Confirm the pathspec is still ONLY the clip + both manifests, and that the lock gate, the compile fallback, and the manifest regeneration are untouched. Report PASS/FAIL per verify step, then STOP with a full summary.
