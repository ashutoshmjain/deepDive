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

**Agent's Operational Role:**
- **Execution & Validation:** Run `mdbook serve` / `mdbook build` to identify rendering errors.
- **Evolutionary Development:** Continuously improve `universal_markdown_fixer.py` to automate the "Master Key" logic (parsing index from filename, auto-linking assets).
- **Manual Supplement:** Perform web searches to fix or find missing URLs and footnotes.

## **Operational Standards**

### **1. Filename Convention (The Master Key)**
- **Markdown Files:** Must be named strictly by their episode number (e.g., `src/225.md`).
- **Image Files:** Must be named strictly by their episode number (e.g., `src/img/225.png`).
- This shared index links the file, the cover image, and the podcast episode together.

### **2. Title Formatting**
- Every new page must start with its index number and a colon in the H1 header (e.g., `# 225 : Title`). The title text should be descriptive but concise (max 5 words).

### **3. SUMMARY.md Organization**
- **Numbered Posts:** (e.g., `225 : ...`) must remain **strictly** in the `# Recent ..` section. They should NOT be moved to thematic categories.
- **Recent Section:** This section is **UNLIMITED** and will grow as new numbered episodes are added to maintain a chronological podcast index.
- **Path Aliasing:** Use the path-aliasing hack `././filename.md` for all items in the `# Recent ..` section to avoid `mdbook` duplicate errors.

### **4. Technical Rendering (KaTeX)**
- Mathematical formulas and scientific symbols must be rendered using **Absolute KaTeX** code instead of embedded images.
- All math blocks and inline symbols must be correctly formatted for `mdbook-katex`.
