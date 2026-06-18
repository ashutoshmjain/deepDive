# deepDive Project Rules

## **Summary Management Guideline**
AI agents MUST follow the subtree-specific governance rules defined in the "Instructions to AI Agents" section found at the bottom of the following navigational nodes:
1. `src/mempool.md` (mempool catchment)
2. `src/template.md` (active block template)
3. `src/chain.md` (master chain & immutable ledger)
4. `src/genesis.md` (foundational thematic research)
5. `src/SUMMARY.md` (master hierarchy & tree structure)

**Core Mandate:** Before performing any edit within a specific folder of the sidebar, the agent must read the corresponding navigational markdown file to understand the content rules and editing constraints for that specific "link in the chain".

## **Hardened Testing Workflow**
1.  **Snapshot:** Record current state.
2.  **Trial 1:** Execute core change.
3.  **Refine:** Adjust based on build results.
4.  **Trial 2:** Final automated pass.
5.  **Manual:** Provide local link for user verification.

## **Visual Standards**
- **Casing:** All taxonomy links and headers should be lowercase/minimal ("smalls").
- **Tree Structure:** Strictly enforce the 3-layered 4-space hierarchy in `SUMMARY.md`:
  - 0 spaces: Root nodes (`chain`, `template`, `mempool`).
  - 4 spaces: Sub-chains (`block 1`, `genesis`).
  - 8 spaces: Transactions (`episodes`, `pillars`).
  - 12 spaces: Thematic depth (articles under pillars).
- **Media:** Relocate all transparent project assets to `src/img/`.

## **Automation Policy**
- Use `md-publish` for all summary regenerations.
- Re-prime `SUMMARY.md` from a clean header if tree corruption occurs.
