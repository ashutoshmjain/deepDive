# Batch 10 Addendum — B6: the rename's follow-through (tests, UI strings, two README lines, the checker asymmetry)

This addendum runs **on top of the uncommitted Batch 10 changes** already in the working trees of the local deepDive and mdIngest clones. Five small fixes, in order. It exists because the Batch 10 executor correctly reported these instead of fixing them out of scope.

## Guardrails — they bind this addendum exactly as they bound the batch

- **A1. Protect the work in progress.** Do NOT `git pull`, `git reset`, `git stash`, or `git checkout` in either clone — the uncommitted Batch 10 edits in the working trees must survive untouched. Do not touch the standalone ddma clone at all.
- **A2. STOP before any commit or push.** Local edits, local mirror, local checks, report, stop — same as the batch.
- **A3. No scope extension.** Anything else you notice gets reported, not fixed. If a named string is not found where this addendum says it is, stop that fix, report what you found, and continue with the next fix only if it does not depend on the failed one.
- **A4. Branding rule.** Only the display strings named below change. Identifiers, comments, docstrings, log tags, endpoint paths, storage keys, and the `ddma/` folder name stay byte-identical.
- **A5. Protected content.** No `settings.json`, no episode content, no media — same as the batch.
- **A6. Parity.** Shared files (`ingest/server.py`, `ingest/tests/cockpit_e2e.js`, `ingest/README.md`) are edited in the deepDive clone and mirrored to the mdIngest clone, byte-identical. `mdIngest/README.md` and `deepDive/ddma/README.md` each live in only one repo and are edited where they live.
- **A7. Final report.** Per fix: PASS or FAIL with the Verify evidence, the e2e result, the checker result, and the changed-files list per repo.

## Fix (a) — The e2e suite asserts a string the rename changed

**Where:** `ingest/tests/cockpit_e2e.js` (:270, :284).

**Finding:** the suite asserts the landing launcher's success text `✓ DDMA ready: ` — the rename changed that string in `ingest/landing.html` to `✓ Cutroom ready: `, so the suite now fails on its own assertions.

**Fix:** replace both occurrences of `✓ DDMA ready: ` with `✓ Cutroom ready: ` in the test file (the `startsWith` check and the exact-text check). Nothing else in the file changes — its remaining "DDMA" mentions are test names and comments (internal).

**Verify:** start the servers locally (cockpit :8088, mdbook :3000, Curator :8000, Beats :8001) and run the e2e suite from `ingest/tests` using that folder's own `package.json` setup. Report the pass/fail counts. If the environment cannot run the suite (for example, no usable Chrome for Puppeteer), say so explicitly in the report — do not skip this step silently.

## Fix (b) — server.py progress and message strings the user actually sees

**Where:** `ingest/server.py` — the three strings below.

**Finding:** these are progress/message values the cockpit UI displays; the rest of the file's "DDMA" hits are comments, docstrings, and log tags (internal, they stay).

**Fix:**

- `"Auto-structuring podcast stings & seeding DDMA clips..."` → `"Auto-structuring podcast stings & seeding Cutroom clips..."`
- `"Auto-transcription, podcast stings & DDMA clips ready!"` → `"Auto-transcription, podcast stings & Cutroom clips ready!"`
- `f"DDMA Project {project_id} ready and launched on {curator_target_url}"` → `f"Cutroom Project {project_id} ready and launched on {curator_target_url}"`

If you find any other string in `ingest/server.py` that is returned to the browser as a progress, message, or error value and names DDMA, apply the same rename and list it in the report; if you find none, say so.

**Verify:** `grep -n "DDMA"` in `ingest/server.py` → attach the hit list; every remaining hit is a comment, a docstring, or a log tag. The cockpit page still loads (HTTP 200).

## Fix (c) — Two README lines the batch's scopes just missed

**Where:** `mdIngest/README.md` (the sentence above the setup-prompt block) and `ingest/README.md` (:7).

**Fix:**

- In `mdIngest/README.md`: "(mdIngest + DDMA)" → "(mdIngest + Cutroom)". (The occurrence inside the prompt block was already replaced by the batch; this is the one outside it.)
- In `ingest/README.md`: "mdIngest + DDMA + Beats Studio" → "mdIngest + Cutroom + Beats Studio".

**Verify:** `grep -n "DDMA"` in both files → zero.

## Fix (d) — The fan-out checker's 47-file asymmetry (a Batch 9 leftover)

**Where:** local clones only — copy from the mdIngest clone into the deepDive clone: `ddma/archetypes/ep248/` (46 files) and `ddma/settings.template.json`.

**Finding:** the merged mdIngest inherited these files from the archived ddma repository's head during the merge; the deepDive workbench never had them, so `check_fanout.py` exits 1 even though every batch change is in sync. The files are code (`.py`), metadata (`.json`), and a placeholders-only template — no media, no secrets, no `settings.json`.

**Fix:** copy the 46 `ep248` files and `ddma/settings.template.json` from the mdIngest clone to the identical paths in the deepDive clone, byte-identical. This is a one-off reverse mirror for these paths only; the normal fan-out direction is unchanged. Change nothing else in either tree.

**Verify:** (1) the copied set contains only `.py` and `.json` files plus the template — no media, no `settings.json`. (2) `python scripts/check_fanout.py` now exits 0. If it still exits non-zero, list the files it names in the report and STOP — do not chase any further divergence.

## Fix (e) — The ddma folder's own README still carries the old product name

**Where:** `deepDive/ddma/README.md` — this file exists only in deepDive; do not create it in mdIngest.

**Finding:** its title and opening lines present the product as "DeepDive Media Automator (DDMA)". The rest of the file is a legacy technical document written under the old codename; a full rewrite is a separate future task and is NOT part of this fix.

**Fix:** in the title line and the opening product description (the first three lines), replace "DeepDive Media Automator (DDMA)" with "Cutroom" and any standalone "DDMA" in those lines with "Cutroom". Nothing else in the file changes; folder and path references (`ddma/`) stay as they are.

**Verify:** the first three lines of `deepDive/ddma/README.md` contain no "DDMA" and no "DeepDive Media Automator"; the file is otherwise untouched (diff limited to those lines).
