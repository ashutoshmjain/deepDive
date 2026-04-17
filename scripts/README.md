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
    - **Title Formatting:** Strictly enforces the `# Index : Title` format (e.g., `# 225 : Title`).
2.  **Asset Integration:** 
    - **Cover Images:** Automatically links the correct image from `src/img/` based on the episode index (e.g., `225.png`).
    - **Podcast Snippet:** Injects a centered HTML snippet with links to the "Deep Dive with Gemini" podcast on all major platforms.
3.  **Navigation Management (`SUMMARY.md`):**
    - **Unlimited Recents:** Pins all numbered posts strictly to the `# Recent ..` section to maintain a chronological podcast index.
    - **Path-Aliasing Hack:** Automatically applies the `././filename.md` prefix to Recent items to prevent `mdbook` duplicate errors.
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

## Progressive Web App (PWA) & Offline Support

The project includes a robust PWA pipeline that transforms the `mdbook` into a standalone, installable application.

### 1. Smart Installation Experience
- **Android/Chrome:** Captures the `beforeinstallprompt` event to show a custom "✨ Install deepDive App" button.
- **iOS/Safari:** Detects iPhone/iPad users and provides a custom hint on how to "Add to Home Screen" using the share menu.
- **Dismissal Logic:** Remembers user choice for 24 hours to avoid being intrusive.

### 2. Live Content Updates
- **New Content Notifications:** The Service Worker listens for updates. When a new article is published, users receive a "✨ New Content Available! Update Now" notification.
- **Skip Waiting:** Clicking the notification forces the new Service Worker to take control and reloads the page instantly.

### 3. Reading Persistence
- **Auto-Resume:** A custom script in `index.hbs` tracks the user's progress in `localStorage`. If the app is reopened at the homepage, it automatically redirects the user to their last-read article.

### 4. Offline Robustness
- **Workbox Integration:** Uses `injectManifest` to precache the entire book.
- **Navigation Fallback:** Provides a seamless experience even without an internet connection by falling back to `index.html`.

---

### Usage

To process a new or updated file, run the following command from the project root:

```bash
python3 scripts/universal_markdown_fixer.py src/225.md
```

The script will automatically detect the index, fix the formatting, and update the `SUMMARY.md`.
