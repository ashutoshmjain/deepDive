# Project-Specific Permissions & Automation

> **MANDATE:** Operational actions (Git, Scripts, Cleanup, Markdown) are **pre-authorized** via the project's automation policy (`.gemini/policies/automation.toml`). The agent MUST read this file at the start of every session to align with the current toolchain standards but should NOT interrupt the user for verbal approval for these specific tasks.

## **Overarching Goal: The Publication Toolchain**
The primary mission of this workspace is the iterative development of the automated publication toolchain. The goal is to automate the manual labor of publishing an `mdbook`:
1.  **Fix KaTeX/LaTeX Issues:** Ensuring mathematical formulas render perfectly in `mdbook`.
2.  **Automate Asset Integration:** Inserting cover images, podcast links, and videos based on filename patterns.
3.  **Synchronize SUMMARY.md:** Maintaining a chronological `# Recent ..` section for all numbered episodes.
4.  **Wallet Integration:** Automating the insertion of Lightning widgets (`shutosha@primal.net`).

### **Long-Term Vision: End-to-End Publishing Automation**
We intelligently automate what we regularly do. Our software automation reflects real, lived objectives because we are the **first and power users** of the tools we build.

**The "Master Key" Strategy:**
To simplify synchronization between the website, repository, and podcast shows, the **Episode Number** (e.g., `225`) is the master key for all assets. 
- **Targeted Processing:** All asset operations (Markdown, Pics, Vids) MUST be surgical. The agent is prohibited from performing global "discovery" searches. If an asset is named `XXX`, it belongs ONLY to `src/XXX.md`.
- **Zero-Sweep Rule:** Do not "sweep" or "fix" files outside the target Episode Number unless explicitly directed to perform repository-wide maintenance. This minimizes the user's testing burden.

## **The Publication Protocol**

The "fix markdown" routine is a modular three-tier process:
1.  **Text Tier (`fix_markdown.py`):** Handles sanitization, KaTeX/Currency, footnotes, and wallet.
2.  **Layout Tier (`fix_pics.py`):** Handles H1 titles, cover image injection, podcast links, and `SUMMARY.md` indexing.
3.  **Media Tier (`fix_vids.py`):** Expands `[vid: filename.mp4]` markers into cinematic infographic HTML blocks.

### **Command Triggers & Protocols**
When the user gives these specific commands, the agent must execute the corresponding script(s), run `mdbook build` to validate, and report status:

- **"Fix Markdown [Number]":** Triggers Tier 1 (`fix_markdown.py`). Focuses on content integrity.
- **"Fix Pics [Number]":** Triggers Tier 2 (`fix_pics.py`). Focuses on cover art and site index.
- **"Fix Vids [Number]":** Triggers Tier 3 (`fix_vids.py`). Focuses on expanding video placeholders.
- **"Process Episode [Number]":** The **Master Orchestrator**. Runs all three tiers in sequence, validates with `mdbook build`, and prepares for push.

### **Agent Responsibilities during Orchestration**
1.  **Intelligent Sanitization:** Before running scripts, the agent must check for and strip invisible Unicode characters.
2.  **Semantic Media Placement:** The agent is responsible for reading the text and identifying the best location to insert `[vid: ...]` markers or additional images.
3.  **Build Validation:** Every automated run MUST be followed by `mdbook build`.
4.  **Finality:** Upon approval, commit and push the updated assets and `SUMMARY.md`.

## **Operational Standards**

### **1. Filename Convention (The Master Key)**
- **Markdown Files:** Must be named strictly by their episode number (e.g., `src/225.md`).
- **Image Files:** Must be named strictly by their episode number (e.g., `src/img/225.png`).
- **Video Files:** Must be named by their episode number followed by a descriptive suffix (e.g., `src/vid/234-intro.mp4`). This helps with visualization and avoids memory bottlenecks.

### **2. Title Formatting**
- Every new page must start with its index number and a colon in the H1 header (e.g., `# 225 : Title`). The title text should be descriptive but concise (max 5 words).

### **3. SUMMARY.md Organization**
- **Numbered Posts:** Must remain **strictly** in the `# Recent ..` section. They should NOT be moved to thematic categories.

## **The Hardened Testing Workflow**
To minimize manual "intelligence" and maximize script robustness:
1.  **Snapshot:** Create backups of the new `.md` files (e.g., `230.md.bak`).
2.  **Execution:** Run the relevant `fix_*.py` script.
3.  **Validation:** Run `mdbook build` and check for errors.
4.  **RCA & Refine:** If errors exist, fix the **script**, and revert the data to the backup.
5.  **Manual Supplement:** Only for surgical manual fixes (e.g., web-fetching missing URLs).
6.  **Finality:** Commit and push the **hardened scripts**, the new data, and the updated `SUMMARY.md`.
