# Project-Specific Permissions & Automation

> **MANDATE:** Operational actions (Git, Scripts, Cleanup, Markdown) are **pre-authorized** via the project's automation policy (`.gemini/policies/automation.toml`). The agent MUST read this file at the start of every session to align with the current toolchain standards but should NOT interrupt the user for verbal approval for these specific tasks.

## **Overarching Goal: The Universal Markdown Fixer & Publishing Toolchain**
The primary mission of this workspace is the iterative development of `scripts/universal_markdown_fixer.py` and associated automation. The goal is to create a robust, standalone **toolchain** that anyone can use to automate the manual labor of publishing an `mdbook`:
1.  **Fix KaTeX/LaTeX Issues:** Ensuring mathematical formulas render perfectly in `mdbook`.
2.  **Automate Asset Integration:** Inserting cover images and podcast links based on filename patterns.
3.  **Synchronize SUMMARY.md:** Maintaining a permanent, growing `# Recent ..` section for all numbered episodes to match podcast indexing, ensuring the website and show are perfectly aligned. Thematic categories are preserved for legacy/unnumbered content.
4.  **Wallet Integration:** Automating the insertion of Lightning widgets (`shutosha@primal.net`) and donation links for Satoshi-based support.

### **Long-Term Vision: End-to-End Publishing Automation**
While focusing on the core foundations above, the ultimate, long-term vision for this workspace is to deeply integrate `mdbook` with Gemini to create a fully autonomous publishing pipeline.

**Core Principle of Collaborative Intelligence:**
We intelligently automate what we regularly do. Our software automation reflects real, lived objectives because we are the **first and power users** of the tools we build.

**The "Master Key" Strategy:**
To simplify synchronization between the website, repository, and podcast shows, the **Episode Number** (e.g., `225`) is the master key for all assets.

**Roles & Responsibilities:**
- **User's Role:** Provide production-grade data (i.e., `<number>.md` and `<number>.png` files) to the repository.
- **Agent's Operational Role:** 
  - **Execution & Testing:** Run the `universal_markdown_fixer.py` script on the provided data. If the script fails, report the errors to the user and wait for explicit instructions on whether to fix it manually or adjust the script.
  - **Validation:** Run `mdbook build` to identify any rendering errors after formatting.
  - **Documentation:** Every key development decision or architectural shift must be immediately documented in the `README.md`.
  - **System Synchronization:** At the end of every session, the agent MUST verify that the `README.md`, `scripts/universal_markdown_fixer.py`, and `GEMINI.md` are in perfect logical sync.
  - **Evolutionary Development Cycle:** This project follows a strict iterative loop to bring the automation to a production-grade level:
    1. **Data Intake:** User provides production-grade data (numbered `.md` and `.png` files).
    2. **Execution:** Agent runs the `universal_markdown_fixer.py` script.
    3. **Manual Supplement:** If the script fails or corrupts data (e.g., footnotes, links, currency), the agent MUST go the "extra mile" to fix the episode manually.
    4. **Publication:** Push the verified, fixed episode to the remote repository.
    5. **Root Cause Analysis (RCA):** Agent performs an RCA on why the script failed.
    6. **Refactoring:** Agent refactors the script to incorporate the fix, ensuring the failure does not recur in the next iteration.
    7. **Wait:** Agent waits for the next data set to test the improved script.
  - **Manual Supplement:** Perform web searches to fix or find missing URLs and footnotes.

## **Operational Standards**

### **1. Filename Convention (The Master Key)**
- **Markdown Files:** Must be named strictly by their episode number (e.g., `src/225.md`).
- **Image Files:** Must be named strictly by their episode number (e.g., `src/img/225.png`).
- **Video Files:** Must be named by their episode number followed by a sequence (e.g., `src/vid/233-1.mp4`, `src/vid/233-2.mp4`). This allows for multiple infographic videos per episode.
- This shared index links the file, the cover image, the podcast episode, and all supplemental video clips together.

### **2. 'Update Video' Workflow**
- When the user says "update video", the agent must:
  1. Identify the video files in `src/vid/` matching the episode number.
  2. Locate the corresponding markdown file in `src/`.
  3. Integrate the video(s) into the markdown file using the appropriate HTML5 or Markdown video tags (ensuring proper placement, typically near relevant conceptual headers).

### **2. Title Formatting**
- Every new page must start with its index number and a colon in the H1 header (e.g., `# 225 : Title`). The title text should be descriptive but concise (max 5 words).

### **3. SUMMARY.md Organization**
- **Numbered Posts:** (e.g., `225 : ...`) must remain **strictly** in the `# Recent ..` section. They should NOT be moved to thematic categories.
- **Recent Section:** This section is **UNLIMITED** and will grow as new numbered episodes are added to maintain a chronological podcast index.

### **4. Technical Rendering (KaTeX)**
- Mathematical formulas and scientific symbols must be rendered using **Absolute KaTeX** code instead of embedded images.
- All math blocks and inline symbols must be correctly formatted for `mdbook-katex`.

## **The Hardened Testing Workflow (Tester Role)**
To minimize manual "intelligence" and maximize script robustess, the agent MUST follow this protocol for every new data intake:
1.  **Snapshot:** Create backups of the new `.md` and `.png` files (e.g., `230.md.bak`).
2.  **Trial 1:** Run `universal_markdown_fixer.py`.
3.  **Validation:** Run `mdbook serve` and check for errors/warnings (KaTeX, footnotes, etc.).
4.  **RCA & Refine:** If errors exist, perform Root Cause Analysis, fix the **script**, and revert the data to the backup.
5.  **Trial 2:** Run the updated script on the clean backup.
6.  **Manual Supplement:** Only if Trial 2 still has minor issues, the agent may use "intelligence" for surgical manual fixes (e.g., web-fetching missing URLs).
7.  **Review Offer:** Offer the user a `localhost:3000` link/check to confirm the build.
8.  **Finality:** Upon approval, commit and push the **hardened script**, the new data, and the updated `SUMMARY.md`.
