# deepDive Batch 2 — APPROVED items only (2 items)

Heads: deepDive `a174cd39`, ddma `9527fea5`, mdIngest `ab96554b`. All file:line references verified at deepDive `a174cd39`.

This is the approved subset of Batch 2. The other 5 items were triaged out by the user (2026-11-16): the do_GET allowlist and path traversal were skipped (the code is open source — "open" is the key word); the open bind is BY DESIGN (the app runs on an old PC and is accessed from anywhere on the LAN — do NOT change it); the editor/shell/settings and POST-size-cap items are deferred as security recommendations until the app has at least 100 users. Only the two items below are approved.

## How to run this batch

- Work through the items in order, 1 to 2.
- After each item, run its Verify steps and report PASS/FAIL for that item, then continue to the next item. Do NOT stop after a FAIL — report it and continue.
- After ITEM 2, STOP and report the full PASS/FAIL summary for both items.
- Step 0 (before ITEM 1): pull the local ddma and mdIngest repos (`git pull` in each) to confirm they are current. If a pull fails or shows a divergence, STOP and report it — do not proceed on a stale base.
- Guardrails (apply to every item unless the item says otherwise):
  - deepDive only. Do not edit the standalone ddma or mdIngest repos directly. Mirroring to them (fan-out) is a separate human step — do not do it, EXCEPT where ITEM 1 explicitly says to mirror the JSON file (see ITEM 1).
  - No Mosaic runs. Do not trigger any new Mosaic API run (no new cost). Downloading an already-completed render is free and is NOT a run.
  - No keys in git. Never commit settings.json or any API key. Never write a key value into a file, a test, or a report.
  - No commit/push — EXCEPT ITEM 1, whose fix is to commit and push two files (see ITEM 1). For ITEM 2, leave the changes uncommitted in the working tree.
  - Do not touch other clips, other episodes, or unrelated code. Each item is scoped to its own files.
  - Run the existing test suites for the files you touch and report the results. Do not weaken a failing test to make it pass — report it red.
  - Never publish a fixture clip for real. For any verify step that would push to GitHub, use an already-published clip (e.g. 249-11) or intercept the POST — never a real push of a test clip.

## ITEM 1 of 2 — the missing factory-defaults file + gold prompt in GEMINI.md

Where: `ddma/scratch/mosaic_factory_defaults.json` — MISSING (404 on deepDive `a174cd39` and on ddma `9527fea5`, in both repos). `ddma/scratch/run_curator.py` — `get_factory_mosaic_prompt()` at :1313 (reads the JSON file, falls back to the hardcoded gold literal at :1330–1355); served as `factory_mosaic_prompt` at :5549. `GEMINI.md:77` references the JSON file, but the gold prompt text is NOT in GEMINI.md (zero matches for "MOTION DESIGN INSTRUCTIONS").

Finding: the factory-default mechanism is in code (TEST 20 restores what it overwrites; Reset returns the factory prompt, not the stored value), but the tracked backup file it reads was never committed — it is 404 on the remote in both repos, so a fresh clone has no backup file and relies solely on the hardcoded literal. And GEMINI.md, which is always tracked and committed, does not carry the gold prompt text as the human-readable backup. The gold prompt text belongs in GEMINI.md IN ADDITION to the JSON file (the JSON is the machine-readable copy the code reads; GEMINI.md is the canonical human-readable backup).

Fix: (1) Get the JSON file onto the remote. First check whether `ddma/scratch/mosaic_factory_defaults.json` exists on the local disk (it was force-added during the earlier rework but never committed — check `git status` and `git ls-files`). If it exists locally, force-add it (`git add -f`, since `scratch/` is git-ignored), commit it, and push it to deepDive master, then mirror it to the standalone ddma repo (`scratch/`) and push there too. If it does NOT exist locally, regenerate it from the hardcoded gold literal in `get_factory_mosaic_prompt()` (`run_curator.py:1313`) — the JSON is `{"mosaic_default_prompt": "<the full gold text below>"}` — then force-add, commit, push, and mirror as above. (2) Add the full gold prompt text below to `GEMINI.md` as the canonical human-readable backup, in a clearly marked section next to the Factory Defaults Backup line (:77), so the prompt survives even if the JSON file is lost. Commit and push the GEMINI.md change to deepDive master. (3) This ITEM is the exception to the no-commit rule in the batch header: its fix IS to commit and push. Commit the JSON file + the GEMINI.md change, push to deepDive master, and mirror the JSON file to standalone ddma and push there.

The gold prompt text (copy exactly — this is the hardcoded literal at `run_curator.py:1330–1355`):

```
MOTION DESIGN INSTRUCTIONS (YOUTUBE SHORTS - around 150 to 180 seconds long)

- Cover the entire timeline of the video with Dan Koe-style motion graphics. Visual coverage must be active and persistent from 0:00 to the very last second with ZERO blank frames.

- Maintain uniform graphic density across all segments.

- Plan 10 to 12 continuous segments of roughly ~ 15 seconds each, perfectly mapped to the clip length. Each segment renders a dynamic diagrammatic graphic with changing visual steps and text reveals.

- Assume background video is a blank black glossy screen (#000000). Keep persistent visuals (animations, conceptual geometry, or text) throughout. Segments must hand off to each other seamlessly like a relay race.

--------------------------------------------------
PACING & ANIMATION RULES
--------------------------------------------------
- No static holds beyond 6 seconds. Introduce visual changes or step reveals every 2-4 seconds.
- Use only basic transforms: opacity, position, scale. Keep animations single-property per element.
- Prefer step-based reveals over continuous complex motion. Avoid preset/template animations.
- No gaps in infographic coverage. Zero external asset dependencies.
```

Verify: (1) `https://raw.githubusercontent.com/ashutoshmjain/deepDive/<new-head>/ddma/scratch/mosaic_factory_defaults.json` returns 200 and its `mosaic_default_prompt` equals the gold text above. (2) Same check for the ddma repo (`https://raw.githubusercontent.com/ashutoshmjain/ddma/<new-head>/scratch/mosaic_factory_defaults.json`). (3) GEMINI.md on the remote contains "MOTION DESIGN INSTRUCTIONS (YOUTUBE SHORTS". (4) `get_factory_mosaic_prompt()` returns the gold text when the JSON file is present, and still falls back to the hardcoded literal if the file is deleted — do not break the fallback. (5) The existing test suite passes — report the count. (Do NOT run TEST 20 against the live prompt without confirming its finally-restore is intact — it is at `test_curator.js:1108` — and confirm it before running.) Report PASS/FAIL, then continue.

## ITEM 2 of 2 — Publish hub recovery would fetch the draft, not the master

Where: `ddma/scratch/run_curator.py` — `/publish-clip` at :4259, step (b) at :4288–4294: if the local master is missing or ≤10000 bytes, it copies `hub_master = working_asset_hub_path(ep_num, master_name)` to local ("Recovering finished master from hub primary store"). `ddma/ddma.py` — `compile_clip` at :2215, output at :2754–2755: `out_filename = f"{base_name}.mp4"`, `out_path = os.path.join(out_dir, out_filename)` — local only, never calls `resolve_working_asset_output` (which `cut` uses at :1323 and `mux_clip` uses at :1589). The hub copy of `{ep}-{num}.mp4` is the mux draft (written by `mux_clip`), not the finished master.

Finding: `/publish-clip` step (b) expects the hub to hold a finished master ("local cache, else hub primary, else compile"). But `compile_clip` never writes the master to the hub — the hub `{ep}-{num}.mp4` is the pre-compile mux draft (740×740, no intro/outro/captions). So if Publish ever takes the hub path (local master missing), it copies the draft and publishes the draft as if it were the master. The bug is latent — it has not fired yet, because Publish normally finds the local master or compiles — but the recovery path is wrong.

Fix: Make `compile_clip` write the finished master hub-first, using `resolve_working_asset_output` (the same helper `cut` and `mux_clip` use), so the hub copy of `{ep}-{num}.mp4` IS the finished master. The local `clips/` copy stays as the cache (the helper returns both paths). After the fix, the hub and local copies of the master agree, and Publish's hub recovery fetches the real master. Do NOT change the mux draft's hub write (`mux_clip` still writes the draft hub-first; `compile_clip` overwrites the hub copy with the master afterwards — that is the intended final state). Do NOT change the Publish step (b) logic — it becomes correct once the hub holds the master.

Verify: (1) Compile a clip that has its mosaic render and audio slice already in the hub (e.g. 249-8, which was recompiled cleanly before) and confirm the hub copy of `{ep}-{num}.mp4` is byte-identical to the local master (same size, same duration, 1080×1920). (2) Confirm the hub copy is the master (1080×1920, correct duration, has intro/outro/captions) and NOT the 740×740 draft. (3) Confirm no other clip's hub file changed. (4) The existing test suite passes — report the count. Do NOT publish a fixture clip for real — this verify step checks the hub/local master agreement only, no push. STOP after this item and report the full PASS/FAIL summary for both items.
