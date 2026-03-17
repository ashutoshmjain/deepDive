# Project-Specific Permissions & Automation

The following actions are **pre-authorized** by the user for this workspace. When starting a session, the agent should confirm if the current task involves these operations and proceed assertively:

## 1. Git Operations
- **Staging:** `git add .` or `git add <file>` is permitted for all task-related changes.
- **Committing:** `git commit -m "<message>"` is permitted once a task is validated.
- **Pushing:** `git push origin master` (or current branch) is permitted after successful commits.

## 2. Script Execution & Cleanup
- **Python Scripts:** Creating and executing scripts in the `scripts/` directory to automate markdown fixes, KaTeX conversions, or `SUMMARY.md` updates.
- **Cleanup:** Deleting temporary files (e.g., `*.txt`, `tmp_*`) created during investigation or comparison.

## 3. Documentation & Markdown
- **Markdown Fixes:** Full-file rewrites to fix formatting, citations, and KaTeX rendering.
- **SUMMARY.md:** Automatically updating the "Recent .." section and moving files between thematic categories.
- **KaTeX:** Always replacing mathematical images with Absolute KaTeX code.

## 4. System Verification
- Running `mdbook build` and `mdbook serve` to validate changes and check for warnings.

---
*Note: While these are pre-authorized, the CLI security architecture may still present a confirmation prompt. The user intends for these to be treated as "Trivial/Routine" approvals.*
