# Scripts Directory

This directory contains the automation tools for the `deepDive` project. The "fix markdown" routine is a two-tier process designed to ensure all articles adhere to the project's technical and aesthetic standards.

---

## The "Fix Markdown" Workflow

The workflow is divided into **Deterministic Automation** (handled by the script) and **Intelligent Orchestration** (handled by the AI agent).

### Tier 1: Execution Engine (`universal_markdown_fixer.py`)
This Python script handles the rules-based formatting that must be consistent across every file. It is the "frozen" standard for processing all markdown content in this repository.

#### Key Features:
1.  **Title Validation:** Ensures the H1 title is exactly 5 words (warns if not).
2.  **Cover & Social Snippets:** 
    - Automatically identifies and inserts a cover image after the main heading.
    - Injects a centered HTML snippet with links to the "Deep Dive with Gemini" podcast on Spotify, Apple Podcasts, YouTube Music, YouTube, and Fountain.fm.
3.  **Lightning Wallet Widget:** Inserts the `shutosha@primal.net` lightning widget before the "References" or "notes and other stuff" section to support the value-for-value model.
4.  **Technical Fixes (KaTeX & Currency):**
    - Replaces `$` used for currency with `USD` (e.g., `$10B` becomes `10B USD`) to prevent rendering errors.
    - Escapes literal `$` symbols as `\\$` so `mdbook-katex` treats them as text.
    - Standardizes H1 and H2 headers by removing unnecessary bolding.
5.  **Citation & Footnote Engine:** 
    - Re-numbers all footnotes sequentially (1, 2, 3...) and ensures the "References" section is a perfectly formatted, numbered list.
    - Removes "Truncated" placeholders and normalizes whitespace throughout the document.
6.  **Navigation Management (`SUMMARY.md`):**
    - Automatically updates the **"Recent .."** section to list the three most recently added files (based on git addition date).
    - Moves older files to their appropriate thematic categories (Bitcoin, AI, Economics, Philosophy, Social) using keyword mapping.
    - Ensures `cover.md` and `how.md` are preserved at the top of the summary.
    - Performs a **Completeness Crosscheck** to ensure no `src/` files are orphaned.

---

### Tier 2: Agent Orchestration (The Intelligence)
While the script handles the structure, the AI agent (Gemini CLI) provides the "intelligence" required to prepare the content for the engine and verify the results.

#### Agent Responsibilities:
1.  **Deep Sanitization:** Strips invisible Unicode characters (like `\u0332`) using shell tools (e.g., `perl`) before running the script to prevent KaTeX parsing failures.
2.  **Research & Citations:** Uses web-search and fetch tools to find missing titles, dates, and URLs for raw citations, ensuring the "References" section is complete and accurate.
3.  **Readability & Tone:** Analyzes the text to break up large "walls of text" into shorter, more digestible paragraphs, optimizing the reading experience for mobile and web.
4.  **Final Validation:** 
    - Runs `mdbook build` and `mdbook serve` to inspect the output.
    - Specifically checks for `ParseError: KaTeX` or `Warning: persistent link` errors in the build log.
5.  **Source Control:** Finalizes the task by staging changes (`git add .`), crafting a descriptive commit message, and pushing to the repository.

---

### Usage

To process a new or updated file, run the following command from the project root:

```bash
python3 scripts/universal_markdown_fixer.py src/your-file-name.md
```

The AI agent will automatically handle the pre-processing and post-verification steps when you say "fix markdown."
