# A4 follow-up — E2E suite still 11/21 after the self-spawn fix

## Scope and head

- Repo: deepDive, head `0d52bb8a` (master).
- This is a FOLLOW-UP to Batch 4 item A4. The A4 code changes are in and committed (`0d52bb8a`): `cockpit_e2e.js` spawns its own server on a test port (default 18088, `TEST_URL` override skips spawn), `puppeteer` / `puppeteer-core` are pinned to exact 24.43.1, and `.github/workflows/e2e.yml` exists on disk (NOT pushed — it needs a workflow-scope token; that push is a separate credential step, NOT part of this spec).
- The suite still does not fully pass. The Batch 4 run reported 11 passed, 10 failed. This spec fixes the failures — or proves they are environmental and reports that instead of forcing a fix.

## Where

- `ingest/tests/cockpit_e2e.js` — the suite. Batch 4 made it spawn `python ingest/server.py` on a test port in the test setup.
- Failure 1 (1 test): a named-target tab-reuse failure, same Chromium family as the recorded Batch-1 ITEM 4 FAIL. The failing test's tabs point at hardcoded `:8088` instead of the spawned test port.
- Failure 2 (9 tests): `Runtime.callFunctionOn` timed out — CDP timeouts, the exact signature of the pre-existing baseline. The Batch 4 report attributes these to browser-side state (leaked tabs from the workspace-link test the likely trigger). The spawned server answered in 2 ms mid-cascade and 3 later tests passed, so the app serves correctly; the wedge is browser-side.

## Finding

Two distinct failure modes remain after the self-spawn fix. Failure 1 looks like a real test bug (hardcoded `:8088` in a test that should target the spawned port). Failure 2 looks environmental (leaked browser tabs / CDP state), but that attribution is the Batch 4 agent's inference — it was not proven by isolation.

## Fix

1. **Failure 1 — hardcoded `:8088` tab target.** Find the named-target tab-reuse test that points its tabs at hardcoded `:8088`. Change it to target the spawned test port (the same port / `TEST_URL` the rest of the suite uses). Do NOT change what the test asserts — only where its tabs point. Re-run that single test and confirm it passes.
2. **Failure 2 — CDP timeouts / leaked tabs.** First ISOLATE, then fix:
   - Run the workspace-link test ALONE (the suspected trigger) and confirm whether it leaks tabs (check for open pages/tabs left behind after it finishes).
   - Run the 9 CDP-timing-out tests ALONE (without the workspace-link test having run first) and confirm whether they pass in isolation.
   - If they pass in isolation and fail only after the workspace-link test, the cause is leaked state: add explicit tab/page cleanup (close pages the test opened) to the workspace-link test, and/or isolate it so its tabs cannot leak into later tests.
   - If they fail in isolation too, the cause is NOT leaked tabs — report the actual error and STOP on this item rather than guessing a fix.
3. Do NOT change the app code (`ingest/server.py`) for either failure unless the isolation proves the app is at fault. Do NOT change the puppeteer versions (already pinned). Do NOT touch `.github/workflows/e2e.yml` (it is not pushed yet; the push is a credential step, not a code step).

## Guardrails

- No Mosaic runs. No keys in git. No commit/push (fan-out is a separate human step).
- If a failure's cause cannot be established by isolation, report it as UNPROVEN rather than inventing a fix. Do not refactor the suite beyond what these two items name.

## Verify

1. Run the full E2E suite from a clean state with no server running (it spawns its own). Report the pass/fail tally.
2. Failure 1's test passes (no longer points at hardcoded `:8088`).
3. The 9 CDP-timeout tests pass — or, if they still fail, the isolation result is reported (pass-in-isolation vs fail-in-isolation) with the evidence, and the item is marked UNPROVEN rather than PASS.
4. Report PASS/FAIL (or UNPROVEN with evidence) per item, then STOP with a full summary.
