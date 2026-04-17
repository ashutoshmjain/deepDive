# Project-Specific Permissions & Automation

> **MANDATE:** Operational actions (Git, Scripts, Cleanup, Markdown) are **pre-authorized** via the project's automation policy (`.gemini/policies/automation.toml`). The agent MUST read this file at the start of every session to align with the current toolchain standards but should NOT interrupt the user for verbal approval for these specific tasks.

## **Overarching Goal: The Universal Markdown Fixer & Publishing Toolchain**
The primary mission of this workspace is the iterative development of `scripts/universal_markdown_fixer.py` and associated automation. The goal is to create a robust, standalone **toolchain** that anyone can use to automate the manual labor of publishing an `mdbook`:
1.  **Fix KaTeX/LaTeX Issues:** Ensuring mathematical formulas render perfectly in `mdbook`.
2.  **Automate Asset Integration:** Inserting cover images and podcast links based on filename patterns.
3.  **Synchronize SUMMARY.md:** Maintaining a permanent, growing `# Recent ..` section for all numbered episodes to match podcast indexing, ensuring the website and show are perfectly aligned. Thematic categories are preserved for legacy/unnumbered content.
4.  **Wallet Integration:** Automating the insertion of Lightning widgets (`shutosha@primal.net`) and donation links for Satoshi-based support.

### **Long-Term Vision: End-to-End Publishing Automation**
While focusing on the core foundations above, the ultimate, long-term vision for this workspace is to deeply integrate `mdbook` with Gemini to create a fully autonomous publishing pipeline:
1.  **Prompt to Publish:** A user provides a prompt; the system builds the narrative, generates an image, and publishes the article to the web via `mdbook`.
2.  **Audio Generation:** The system automatically creates an audio prompt, uses NotebookLM to generate an audio file, and publishes it to Spotify as a podcast.
3.  **Video Promotion:** The system utilizes tools like motion.so to automatically generate one-minute promotional videos for the published content.
4.  **The Goal:** An end-to-end, zero-touch solution for researching, writing, and distributing multi-modal content (text, audio, video).

**Architectural Principle:**
This vision will be realized through **multi-agent orchestration**. The core philosophy is to achieve integration through the *minimal* use of LLM "intelligence" and *maximum* automation using deterministic command-line tools and scripts. AI should be reserved for cognitive tasks (generation, research, routing), while scripts handle formatting, publishing, and API interactions.

**Core Principle of Collaborative Intelligence:**
We intelligently automate what we regularly do. We do not aspire to build "popular apps" in the abstract; instead, we focus on solving our own immediate pain points—specifically the creation of the *Deep Dive with Gemini* podcast. Our software automation reflects real, lived objectives because we are the **first and power users** of the tools we build. This development is slow, steady, and deliberate.

**Agent's Operational Role:**
- **Execution & Validation:** Run `mdbook serve` / `mdbook build` to identify rendering errors.
- **Manual Supplement:** Perform web searches to fix or find missing URLs and footnotes.
- **Evolutionary Development:** Continuously improve the script based on manual interventions (e.g., updating regex, adding category keywords, fixing logic failures).
- **Future Milestone:** Once the core objectives are perfected, investigate automating footnote fixing and URL searching within the script.

## **Operational Standards**

### **1. Title Formatting**
- Every new page must start with its index number and a colon in the H1 header (e.g., `# 224 : Title`).

### **2. SUMMARY.md Organization**
- **Numbered Posts:** (e.g., `224 : ...`) must remain **strictly** in the `# Recent ..` section. They should NOT be moved to thematic categories.
- **Recent Section:** This section is **UNLIMITED** and will grow as new numbered episodes are added to maintain the podcast index.
- **Path Aliasing:** Use the path-aliasing hack `././filename.md` for all items in the `# Recent ..` section to avoid `mdbook` duplicate errors.

### **3. Technical Rendering (KaTeX)**
- Mathematical formulas and scientific symbols must be rendered using **Absolute KaTeX** code instead of embedded images.
- All math blocks and inline symbols must be correctly formatted for `mdbook-katex`.
