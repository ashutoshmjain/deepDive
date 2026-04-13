# Project-Specific Permissions & Automation

> **MANDATE:** At the start of every session in the `deepDive` project, the agent MUST read this file and ask the user for "blanket verbal approval" for the pre-authorized routine actions listed below (Git, Scripts, Cleanup, Markdown) to minimize interruptions.

## **Overarching Goal: The Universal Markdown Fixer & Publishing Toolchain**
The primary mission of this workspace is the iterative development of `scripts/universal_markdown_fixer.py` and associated automation. The goal is to create a robust, standalone **toolchain** that anyone can use to automate the manual labor of publishing an `mdbook`:
1.  **Fix KaTeX/LaTeX Issues:** Ensuring mathematical formulas render perfectly in `mdbook`.
2.  **Automate Asset Integration:** Inserting cover images and podcast links based on filename patterns.
3.  **Synchronize SUMMARY.md:** Automatically generating catchy titles and placing files in thematic categories based on pre-assigned logic.
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

## 1. Git Operations
- **Staging:** `git add .` or `git add <file>` is permitted for all task-related changes.
- **Committing:** `git commit -m "<message>"` is permitted once a task is validated.
- **Pushing:** `git push origin master` (or current branch) is permitted after successful commits.

## 2. Script Execution & Cleanup
- **Tools:** `python3`, `perl`, `ls`, `sed`, `grep`, `cp`, `mv`, and `rm` are pre-authorized for all automation, text-processing, discovery, and file management tasks.
- **Python Scripts:** Creating and executing scripts in the `scripts/` directory to automate markdown fixes, KaTeX conversions, or `SUMMARY.md` updates.
- **Cleanup:** Deleting temporary files (e.g., `*.txt`, `tmp_*`) created during investigation or comparison.

## 3. Documentation & Markdown
- **Markdown Fixes:** Full-file rewrites to fix formatting, citations, and KaTeX rendering.
- **SUMMARY.md:** Automatically updating the "Recent .." section and moving files between thematic categories.
- **KaTeX:** Always replacing mathematical images with Absolute KaTeX code.

## 4. System Verification
- Running `npm run build:pwa` to validate changes and update the Service Worker.
- Running `npm run serve:pwa` (or `mdbook serve`) to check rendering.

---
*Note: While these are pre-authorized, the CLI security architecture may still present a confirmation prompt. The user intends for these to be treated as "Trivial/Routine" approvals.*
