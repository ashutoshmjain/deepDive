# Batch 11 — Install-prompt stitches from the post-merge new-user test (Issues 110)

**Executor:** any coding agent (Muse / Antigravity CLI) with the repos cloned
locally. Work in the local clones of `deepDive` and `mdIngest`. Never touch the
archived standalone `ddma` clone.

**Why:** on 2026-11-19 a fresh-clone new-user test followed the install prompt in
the mdIngest README literally, end to end. The install works — every server came
up — but four places in the prompt text itself failed a literal reader. This batch
fixes the prompt text. No code changes.

## Guardrails

- **G1 — Order:** work B1 → B5 in order.
- **G2 — Stop before commit/push.** Make the edits locally, run the Verify
  section, and report. Commits happen only on a separate fan-out instruction.
- **G3 — Report, don't fix.** Anything else you notice is reported in the G5
  report, never changed.
- **G4 — Exact edits only.** Each item names the file, the exact current text,
  and its replacement. Change nothing else — no reflow, no rewording.
- **G5 — Report format:** per item PASS/FAIL with the grep evidence from the
  Verify section, then the checker result.

## The background the executor needs

- The README's 12-step prompt is the product being fixed: a new user (or their
  agent) follows it word for word. Every fix below makes a literal reading work.
- `mdIngest/README.md` is **not** a mirrored file — deepDive's README is a
  different document. Edit the README in mdIngest only.
- The one deepDive edit (B5) is a word correction in a spec file that exists
  only in deepDive.

## B1 — Step 3: `python` does not exist on stock Ubuntu/WSL (mdIngest/README.md)

Current text (step 3):

> Create the virtual environment if it does not exist (`python -m venv .venv`), activate it,

Replace with:

> Create the virtual environment if it does not exist (`python3 -m venv .venv` — on Windows: `py -3 -m venv .venv`), activate it,

The rest of step 3 is unchanged. (Step 1 already verifies with
`python3 --version`; step 3 was the inconsistent one.)

## B2 — Step 2: tell the reader to enter the clone (mdIngest/README.md)

Current text (the whole step):

> 2. Fork mdIngest and clone your fork into this workspace: `gh repo fork ashutoshmjain/mdIngest --clone`. All paths below are relative to the repo root.

Replace with:

> 2. Fork mdIngest and clone your fork into this workspace: `gh repo fork ashutoshmjain/mdIngest --clone`, then `cd mdIngest`. All paths below are relative to the repo root, and every command below runs from there.

## B3 — Step 9: nobody ever starts `mdbook serve` (mdIngest/README.md)

Current text (the whole step):

> 9. Launch the mdIngest Publishing Cockpit server (`python ingest/server.py` from the repo root, using the venv) on http://localhost:8088 and verify that http://localhost:3000 is accessible via `mdbook serve`.

Replace with:

> 9. Launch the mdIngest Publishing Cockpit server (`python ingest/server.py` from the repo root, using the venv) on http://localhost:8088. In a second terminal, from the repo root, start the book preview — `mdbook serve --hostname 0.0.0.0 -p 3000` — and verify http://localhost:3000 responds.

## B4 — Steps 12 + the after-setup paragraph: there are four servers (mdIngest/README.md)

In step 12, replace:

> and all three servers respond (cockpit :8088, Curator :8000, Beats :8001).

with:

> and all four servers respond (cockpit :8088, book preview :3000, Curator :8000, Beats :8001).

In the "After setup" paragraph below the steps, replace:

> it mounts the Drive workspace if needed and starts all three servers

with:

> it mounts the Drive workspace if needed and starts all four servers

## B5 — One word in the Batch 10 spec's summary (deepDive only)

In `defect-specs/deepdive-prompt-batch10.md`, in the Execution summary, replace:

> zero remaining hits for the old Cutroom name

with:

> zero remaining hits for the old DDMA name

(Cutroom is the new name; the sentence is about the old one.)

## Verify

1. In mdIngest/README.md: `python -m venv` → 0 hits; `py -3 -m venv` → 1 hit;
   `cd mdIngest` → present in step 2; `mdbook serve --hostname 0.0.0.0 -p 3000`
   → present in step 9; `all three servers` → 0 hits in the whole file;
   `all four servers` → 2 hits.
2. In deepDive's `defect-specs/deepdive-prompt-batch10.md`: `old DDMA name`
   → 1 hit; `old Cutroom name` → 0 hits.
3. From the deepDive clone: `python3 scripts/check_fanout.py` exits 0.
4. `git diff` in each clone shows only the lines this spec names.
