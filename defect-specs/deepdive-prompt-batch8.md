# deepdive-prompt-batch8.md

## Batch 8 — Workspace link component, Drive-free workspace, Workspace button down-case, published-plan bookkeeping

Four items. Execute them in order. Report PASS/FAIL per verify step, then STOP with a full summary.

---

## B1 — Issue 74: Extract the Workspace home link into one shared component

### Where

The Workspace home link is hardcoded in three places (verified at deepDive head `a6ec71d9`):

- `ingest/cockpit.html:1549` — `<a class="btn-cmd" href="http://127.0.0.1:8088/" target="deepdive-workspace" id="btn-workspace" title="Open the Workspace home page">`
- `ddma/curator.html:1539` — `<a href="http://127.0.0.1:8088/" target="deepdive-workspace" id="topWorkspaceBtn" class="btn btn-secondary btn-mini" ... title="Open the Workspace home page (landing page)">`
- `ddma/beats.html:31` — `<a class="btn-mini" href="http://127.0.0.1:8088/" target="deepdive-workspace" title="Open the Workspace home page (landing page)">🏠 Workspace</a>`

The same absolute URL (`http://127.0.0.1:8088/`) and the same named target (`deepdive-workspace`) are repeated in all three files. The fan-out copies (`mdIngest/ui/cockpit.html`, standalone `ddma/curator.html`, standalone `ddma/beats.html`) carry the same three hardcoded links.

### Finding

The workspace address is defined in three places instead of one. Changing it (a different host, a different port) means editing three files in two repos, and they can drift apart. The link itself works (it opens the landing page and reuses the tab via the named target), so this is a duplication/maintainability fix, not a behaviour fix.

### Fix

1. Create ONE shared definition of the Workspace home link — label, href, and named target — and use it in all three apps (cockpit, curator, Beats Studio). The href must resolve to the workspace landing page (port 8088 on the same host) without hardcoding the full absolute URL in each app file. A small shared snippet or component that each app includes is the expected shape; pick the mechanism that fits how these three pages already share code.
2. Keep the named target `deepdive-workspace` on the link, so the tab is reused when already open.
3. Keep the visible label and behaviour identical: a "🏠 Workspace" link that opens the landing page.
4. After the change, the workspace URL must appear in exactly ONE place (the shared definition). Grep the three app files for `127.0.0.1:8088` — none of them may contain it any more.
5. Fan out the change to the standalone repos the same way the other fixes fan out (cockpit → `mdIngest/ui/cockpit.html`; curator + Beats → standalone `ddma`).

### Verify

1. The workspace URL (`127.0.0.1:8088`) appears in exactly one place in the repo (the shared definition). Grep confirms zero occurrences in `ingest/cockpit.html`, `ddma/curator.html`, and `ddma/beats.html`.
2. All three apps still show the "🏠 Workspace" link with the named target `deepdive-workspace`.
3. Clicking the link in each app opens the landing page on :8088 (or reuses the already-open workspace tab). No new tab per click.
4. The fan-out copies match (cockpit identical in mdIngest, curator + Beats identical in standalone ddma).
5. Report PASS/FAIL per verify step, then STOP with a full summary.

---

## B2 — Issue 99: Workspace code assumes Google Drive — default to a plain local folder

### Where

Verified at deepDive head `a6ec71d9` / mdIngest head `d879ab1` / ddma head `cf26ab2`:

- `mdIngest/ui/server.py` `get_dd_hub_root()` (:728–748): candidates include `Path(r"G:\My Drive\dd_hub")` (:738) and `Path("/mnt/gdrive/dd_hub")` (:739); when unset it warns and defaults to `G:\My Drive\dd_hub` (:747–748).
- `mdIngest/ui/server.py` audio discovery: hardcoded `G:\My Drive\agy_inputs` fallback (:771–777) and `G:/My Drive/pickup_longform` (:827).
- `mdIngest/ui/server.py` Drive export: `export_podcast_to_gdrive()` (:2067, destination :2095) and `export_video_to_gdrive()` (:2235, default `G:/My Drive/Podcast_Video_Pickup` :2238), wired to `/api/podcast/export_gdrive` (:5288) and `/api/podcast/export_gdrive_video` (:5298); Drive-named settings `GDRIVE_PICKUP_PATH` / `GDRIVE_VIDEO_PICKUP_PATH` (:171–174).
- `ddma/scratch/run_curator.py` `resolve_dd_hub_root()` (:141–162): candidates `r"G:\My Drive\dd_hub"`, `"/mnt/gdrive/dd_hub"`, `"/workspace/dd_hub"` (:155); warns and defaults to `G:\My Drive\dd_hub` (:161–162); also `G:\My Drive\agy_inputs` at :4898.
- `settings.template.json` is already neutral (`dd_hub_root` is a `/path/to/dd_hub` placeholder) — do not change it.

### Finding

The README now says the workspace is any local folder the user picks (the dd root hub, `DD_HUB_ROOT`) and Drive/rclone is the user's choice — but the code still defaults to, and falls back to, Google Drive paths. A new user who picks a plain local folder hits Drive defaults the code assumes.

### Fix

1. `get_dd_hub_root()` (`ui/server.py:728–748`) and `resolve_dd_hub_root()` (`run_curator.py:141–162`) must NOT default to a Google Drive path. Default to a plain local folder (or require explicit configuration and fail with a clear message naming `DD_HUB_ROOT` when none is set). Remove `G:\My Drive\dd_hub` and `/mnt/gdrive/dd_hub` from the candidate lists and from the fallback default.
2. Replace the hardcoded Drive fallbacks with workspace-relative paths under `DD_HUB_ROOT`: the `agy_inputs` fallback (`ui/server.py:771–777`, `run_curator.py:4898`) and the `pickup_longform` fallback (`ui/server.py:827`) must resolve inside the workspace, not under `G:\My Drive`.
3. The Drive export functions (`export_podcast_to_gdrive`, `export_video_to_gdrive`, and their API routes) stay as an opt-in feature for users who configure a Drive pickup path, but they must NOT be the default: the default export destination is the workspace audio/video folder. Do not remove the export feature; make Drive opt-in, not assumed.
4. Fan out to the standalone repos (server.py → `mdIngest/ui/server.py`; run_curator.py → standalone `ddma`).

### Verify

1. With `DD_HUB_ROOT` unset and no Drive folder present, the code does NOT default to or reference any `G:\My Drive` / `/mnt/gdrive` path — it uses a plain local folder or fails with a clear message naming `DD_HUB_ROOT`.
2. Grep finds zero `My Drive` / `G:/My Drive` / `/mnt/gdrive` references in the workspace-resolution and audio-discovery code paths (the opt-in Drive export functions and their settings keys are the only exception, and they are not the default).
3. The audio/pickup fallbacks resolve inside `DD_HUB_ROOT`.
4. Creating a new episode in the Curator with a plain local workspace still works and writes to the workspace.
5. The fan-out copies match (server.py identical in mdIngest, run_curator.py identical in standalone ddma).
6. Report PASS/FAIL per verify step, then STOP with a full summary.

---

## B3 — Issue 100: Workspace button does nothing useful when the cockpit server is down

### Where

The Curator's top-bar Workspace button, `ddma/curator.html:1539` (verified at deepDive head `a6ec71d9`, unchanged by Batch 7):

```html
<a href="http://127.0.0.1:8088/" target="deepdive-workspace" id="topWorkspaceBtn" ... title="Open the Workspace home page (landing page)">🏠 Workspace</a>
```

It is a bare link. No check, no launch, no error message. Precedent for launching a sibling server: the cockpit's "Launch Beats Studio" button POSTs to `/api/beats/launch` (`mdIngest/ui/server.py:5075`).

### Finding

If only the ddma server (Curator :8000) is running and the cockpit (:8088) is not, clicking Workspace opens a tab that fails with a browser connection error. The user cannot be expected to start the cockpit first — the button must handle the down case.

### Fix

In order of preference:

1. Best: when the button is clicked, check whether the cockpit (:8088) responds. If it does, open it (current behaviour). If it does not, start the cockpit first (via a launch endpoint on the Curator server, following the `/api/beats/launch` precedent) and then open it once it responds.
2. Minimum (if starting the cockpit from the Curator is not feasible): detect that :8088 is down and show a clear message in the Curator that the workspace server is not running, with instructions on how to start it — do NOT open a dead tab silently.

Do NOT change the button's label or its behaviour when the cockpit is already running.

### Verify

1. With only the Curator running and the cockpit down, click Workspace — either the cockpit starts and the landing page opens, or a clear message appears stating the workspace server is not running with instructions on how to start it. No bare browser connection-error tab.
2. With the cockpit already running, clicking Workspace routes straight to the landing page (unchanged behaviour).
3. The fan-out copy matches (curator.html identical in standalone ddma).
4. Report PASS/FAIL per verify step, then STOP with a full summary.

---

## B4 — Issue 101: Published plan copy lags on rendered duration and published flag

### Where

- The Publish flow, `/publish-clip` handler in `ddma/scratch/run_curator.py:4121`. Step (e), the scoped git add + commit + push (~:4234), adds ONLY the clip mp4 (`src/ddma/docs/episodes/<ep>/clips/<master>`) and the two `episodes.json` manifests (`ddma/docs/episodes.json`, `src/ddma/docs/episodes.json`). The published plan copy (`src/ddma/docs/episodes/<ep>/plan.json`) is NOT in the add list.
- The plan save sync that mirrors the plan to the published copy, `run_curator.py:1832` (`shutil.copy2` to `docs/episodes/<ep>/plan.json` and the `../src/ddma/docs/` mirror).
- Verified live 2026-11-19 for clip 249-18: the published plan copy (`src/ddma/docs/episodes/249/plan.json`) has `locked: True` and the Mosaic run id, but `rendered_duration` is None (the workbench plan has 73.72) and there is no `published` flag. The published copy is a lighter schema (11 keys vs the workbench copy's 23), so the gap is specifically the two fields the distribution side needs.

### Finding

Publish commits the clip and the manifests but never writes the clip's `rendered_duration` or a `published` flag into the published plan copy, and the plan copy is not part of the scoped commit. So the published plan lags behind the workbench plan on exactly the fields that say how long the rendered clip is and whether it is published.

### Fix

1. In the Publish flow, after a clip is published, write the clip's `rendered_duration` and set `published: true` into the published plan copy (`src/ddma/docs/episodes/<ep>/plan.json`).
2. Include that published plan copy in the scoped git add/commit (step (e)), keeping the scope tight: the clip mp4, the published plan copy, and the two `episodes.json` manifests only. Do NOT widen the commit to any other file.
3. Do NOT change the Publish flow's other behaviour (clip upload, manifest update, push).

### Verify

1. After publishing a clip, the published plan copy (`src/ddma/docs/episodes/<ep>/plan.json`) shows that clip's `rendered_duration` and `published: true`.
2. The Publish commit includes the published plan copy alongside the clip and the two manifests — and no other file.
3. Re-publishing an already-published clip stays idempotent (no-op commit, as today).
4. The fan-out copy matches (run_curator.py identical in standalone ddma).
5. Report PASS/FAIL per verify step, then STOP with a full summary.

---

## Guardrails

- Do NOT change any other file beyond what each item names. Do NOT touch the security items, the server code beyond the named handlers, or any other repo.
- Do NOT hardcode any episode number, API key, or credential.
- Do NOT change the caption editing, the revert button, the settings modal, or the 1-Prompt Setup code block (except where an item explicitly names a change).
- If a verify step is ambiguous, list the candidates and STOP — do not guess.
- Report PASS/FAIL per verify step, then STOP with a full summary.
