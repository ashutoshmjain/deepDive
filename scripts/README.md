# Scripts Directory

This directory contains the automation tools for the `deepDive` project. The "fix markdown" routine is a two-tier process designed to ensure all articles adhere to the project's technical and aesthetic standards.

---

## The "Fix Markdown" Workflow

The workflow is divided into **Deterministic Automation** (handled by the script) and **Intelligent Orchestration** (handled by the AI agent).

### Tier 1: Execution Engine (`universal_markdown_fixer.py`)
This Python script handles the rules-based formatting that must be consistent across every file. It is the "frozen" standard for processing all markdown content in this repository.

#### Key Features:
1.  **The "Master Key" Strategy:**
    - **Episode Identification:** Automatically extracts the episode number from the filename (e.g., `225.md`) or the title. This index serves as the master key linking the text, the cover image, and the podcast show.
    - **Consistent File Naming:** 
        - **Articles:** `src/<number>.md`
        - **Images:** `src/img/<number>.png`
        - **Videos:** `src/vid/<number>-<descriptive-name>.mp4` (e.g., `234-intro.mp4`).
    - **Title Formatting:** Strictly enforces the `# Index : Title` format (e.g., `# 225 : Title`).
2.  **Asset Integration:** 
    - **Cover Images:** Automatically links the correct image from `src/img/` based on the episode index (e.g., `225.png`).
    - **Podcast Snippet:** Injects a centered HTML snippet with links to the "Deep Dive with Gemini" podcast on all major platforms.
3.  **Navigation Management (`SUMMARY.md`):**
    - **Unlimited Recents:** Pins all numbered posts strictly to the `# Recent ..` section to maintain a chronological podcast index.
    - **Thematic Categories:** Maps unnumbered/legacy files to thematic categories while ensuring numbered posts are never moved.
4.  **Technical Fixes (KaTeX & Currency):**
    - **Absolute KaTeX:** Replaces image placeholders with project-standard Absolute KaTeX symbols.
    - **Currency Sanitization:** Replaces `$` with `USD` to prevent `mdbook-katex` rendering failures.
5.  **Wallet Integration:** Inserts the `shutosha@primal.net` lightning widget to support the value-for-value model.
6.  **Citation Engine:** Sequential re-numbering of footnotes and normalization of the "References" section.

---

### Tier 2: Agent Orchestration (The Intelligence)
While the script handles the structure, the AI agent (Gemini CLI) provides the "intelligence" and is pre-authorized via the project's automation policy (`.gemini/policies/automation.toml`).

#### Agent Responsibilities:
1.  **Deep Sanitization:** Strips invisible Unicode characters using `perl` to prevent KaTeX parsing failures.
2.  **Paragraph Optimization:** Breaks up large "walls of text" into digestible paragraphs for mobile readability.
3.  **Research & Validation:** Fetches missing citation URLs and verifies the build with `mdbook build`.
4.  **Source Control:** Finalizes the task by staging, committing, and pushing to the repository.

---

## The Evolutionary Development Cycle

To reach the goal of autonomous publishing with minimal intelligence, the toolchain follows an iterative testing loop for every new episode:

1.  **Data Intake:** User provides numbered `.md` and `.png` files to the `src/` directory.
2.  **Execution:** Run the script: `python3 scripts/universal_markdown_fixer.py src/<number>.md`.
3.  **Manual Supplement:** If the script misses citations, mangles currency, or breaks KaTeX, the agent fixes the article manually to ensure a perfect publication.
4.  **Publication:** The verified article is committed and pushed to the remote repository for use in the podcast.
5.  **Root Cause Analysis (RCA):** The agent identifies exactly why the script failed or underperformed.
6.  **Refactoring:** The script is updated to handle the edge case automatically in the next run.
7.  **Loop:** The cycle repeats with the next dataset, continuously shrinking the "manual supplement" phase.

---

## Progressive Web App (PWA) & Offline Support

The project transforms the `mdbook` into a standalone, installable application, optimized for a fast, "app-like" experience.

### 1. Simplified Installation
To keep the reading experience clean and "tracker-free," we have removed intrusive installation popups. Instead, installation instructions are integrated directly into the landing page for all platforms (iOS, Android, and Desktop).

**Benefits of Installation:**
- **Offline Access:** Read the entire book without an internet connection.
- **Performance:** Faster loading times via localized caching.
- **Home Screen Integration:** A clean icon for instant access.

### 2. Live Content Updates
- **Update Notifications:** The Service Worker detects new publications and displays a "✨ New Content Available!" notification.
- **Instant Refresh:** Users can update the app instantly without a manual page reload.

### 3. Reading Persistence
- **Auto-Resume:** The app tracks progress in `localStorage`, automatically redirecting users to their last-read article for a seamless across-session experience.

### 4. Technical Stack
- **Workbox:** Manages precaching and service worker lifecycle.
- **Navigation Fallback:** Ensures the PWA remains functional even when offline by routing to `index.html`.

---

### Usage

To process a new or updated file, run the following command from the project root:

```bash
python3 scripts/universal_markdown_fixer.py src/225.md
```

The script will automatically detect the index, fix the formatting, and update the `SUMMARY.md`.
