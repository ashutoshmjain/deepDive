# Scripts Directory

This directory contains the automation tools for the `deepDive` project. The "fix markdown" routine is a two-tier process designed to ensure all articles adhere to the project's technical and aesthetic standards.

---

## The "Fix Markdown" Workflow

The workflow is divided into **Deterministic Automation** (handled by the script) and **Intelligent Orchestration** (handled by the AI agent).

### Tier 1: Execution Engine (`universal_markdown_fixer.py`)
This Python script handles the rules-based formatting that must be consistent across every file. It is the "frozen" standard for processing all markdown content in this repository.

#### Key Features:
1.  **Title Management:** 
    - **Validation:** Ensures the H1 title is exactly 5 words (warns if not).
    - **Auto-Generation:** If a file lacks an H1 title, the script automatically generates one from the filename or a provided `--title` argument.
2.  **Cover & Social Snippets:** 
    - Automatically identifies and inserts a cover image after the main heading.
    - Injects a centered HTML snippet with links to the "Deep Dive with Gemini" podcast on Spotify, Apple Podcasts, YouTube Music, YouTube, and Fountain.fm.
3.  **Lightning Wallet Widget:** Inserts the `shutosha@primal.net` lightning widget before the "References" or "notes and other stuff" section to support the value-for-value model.
4.  **Technical Fixes (KaTeX & Currency):**
    - **KaTeX Mapping:** Automatically replaces image placeholders (e.g., `![][image1]`) with project-standard Absolute KaTeX symbols (e.g., `$F$`, `$\mathcal{R}$`, `$\Phi$`).
    - **Currency:** Replaces `$` used for currency with `USD` (e.g., `$10B` becomes `10B USD`) to prevent rendering errors.
    - **Escaping:** Escapes literal `$` symbols as `\\$` so `mdbook-katex` treats them as text.
    - **Headers:** Standardizes H1 and H2 headers by removing unnecessary bolding.
5.  **Citation & Footnote Engine:** 
    - **Smarter Regex:** Uses an advanced regex boundary check to re-number footnotes without corrupting decimal numbers (like chapter/verse references `13.30`).
    - **Mapping:** Re-numbers all footnotes sequentially (1, 2, 3...) and ensures the "References" section is a perfectly formatted, numbered list.
    - **Cleanup:** Removes "Truncated" placeholders and normalizes whitespace throughout the document.
6.  **Navigation Management (`SUMMARY.md`):**
    - **Missing File Detection:** Scans the `src/` folder for any `.md` files not currently listed in `SUMMARY.md` and automatically adds them to the project structure.
    - **Dynamic Sorting:** Automatically updates the **"Recent .."** section to list the three most recently added files (based on git addition date).
    - **Thematic Categories:** Moves older files to their appropriate thematic categories (Bitcoin, AI, Economics, Philosophy, Social) using keyword mapping.
    - **Completeness Crosscheck:** Performs a final verification to ensure no `src/` files are orphaned.

---

### Tier 2: Agent Orchestration (The Intelligence)
While the script handles the structure, the AI agent (Gemini CLI) provides the "intelligence" required to prepare the content for the engine and verify the results.

#### Agent Responsibilities:
1.  **Deep Sanitization:** Strips invisible Unicode characters (like `\u0332`) using shell tools (e.g., `perl`) before running the script to prevent KaTeX parsing failures.
2.  **Research & Citations:** Uses web-search and fetch tools to find missing titles, dates, and URLs for raw citations, ensuring the "References" section is complete and accurate.
3.  **Readability & Tone:** Analyzes the text to break up large "walls of text" into shorter, more digestible paragraphs, optimizing the reading experience for mobile and web.
4.  **Final Validation:** 
    - Runs `npm run build:pwa` (instead of standard `mdbook build`) to update the Service Worker and inspect the output.
    - Specifically checks for `ParseError: KaTeX` or `Warning: persistent link` errors in the build log.
5.  **Source Control:** Finalizes the task by staging changes (`git add .`), crafting a descriptive commit message, and pushing to the repository.

---

## Progressive Web App (PWA) & Offline Support

The project includes a fully automated PWA pipeline that allows the book to be installed on mobile/desktop and read entirely offline.

### 1. Infrastructure (`/pwa`)
- **`manifest.json`**: Defines the app's identity (DeepDive), icons, and standalone display mode.
- **`sw-src.js`**: The service worker source file. It uses Workbox to precache the entire book and provides a navigation fallback to `index.html` for offline robustness.
- **`sw-register.js`**: A lightweight client-side script that registers the generated service worker.

### 2. Workbox Integration
The build uses `workbox-cli` in `injectManifest` mode.
- **`workbox-config.js`**: Configured to scan the `book/` directory and precache all HTML, JS, and CSS files.
- **Automatic Updates**: Every time a new article is added, the service worker's revision manifest is updated, triggering an automatic background update for users.

### 3. Theme Customization (`/theme`)
To ensure the PWA is persistent across `mdbook build` runs, the theme is customized:
- **`index.hbs`**: Modified to link the manifest and registration script in the `<head>`.
- **Reading Persistence**: A specialized JavaScript snippet in `index.hbs` tracks the user's progress. It saves the URL of the current article to `localStorage` and automatically redirects the user back to their last-read page if they reopen the app at the homepage.

### 4. Build Pipeline
The standard `mdbook build` is wrapped in a PWA-aware pipeline (`npm run build:pwa`):
1.  **Build**: Runs the standard `mdbook build`.
2.  **Copy**: Moves `manifest.json`, `sw-register.js`, and icons into the `/book` folder.
3.  **Inject**: Runs `workbox injectManifest` to generate the final `sw.js` in the output directory.

---

### Usage

To process a new or updated file, run the following command from the project root:

```bash
python3 scripts/universal_markdown_fixer.py src/your-file-name.md --title "Your Five Word Catchy Title"
```

The AI agent will automatically handle the pre-processing and post-verification steps when you say "fix markdown."
