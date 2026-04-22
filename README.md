# DeepDive with Gemini: Research & Automation

This repository contains the research, show notes, and publishing toolchain for the **Deep Dive with Gemini** podcast.

---

## 🟢 System Sync Status: **LOCKED**
- **GEMINI.md:** Updated with "Master Key" strategy and updated Agent Role.
- **Automation Script:** `universal_markdown_fixer.py` correctly implements filename-to-index parsing and path-aliasing.
- **Documentation:** Root and scripts READMEs are current.
- **Last Verification:** April 17, 2026.

---

## 🔑 The "Master Key" Strategy
To ensure perfect synchronization between the website, repository, and podcast shows, the **Episode Number** (e.g., `225`) is the master key for all assets.
1.  **Filenames:** `src/225.md` and `src/img/225.png`.
2.  **Titles:** Automatically formatted as `# 225 : Title`.
3.  **Navigation:** Numbered episodes are pinned to the `# Recent ..` section of `SUMMARY.md` indefinitely.

---

## 📱 Progressive Web App (PWA) Status: **ACTIVE**
The deepDive platform is a fully installable PWA with:
- **Offline Reading:** Full precaching of all articles.
- **Smart Install Prompts:** Custom UI for Android/iOS.
- **Live Content Alerts:** Notifications for new episode releases.
- **Reading Persistence:** Auto-resumes from the last-read article.

---

## 🛠️ The Automation Toolchain

The project is powered by a two-tier "Fix Markdown" routine:
1.  **The Script (`scripts/universal_markdown_fixer.py`):** Handles deterministic formatting, asset linking, KaTeX rendering, and `SUMMARY.md` synchronization.
2.  **The Agent (Gemini CLI):** Handles intelligent sanitization, readability optimization, and final validation. Pre-authorized via `.gemini/policies/automation.toml`.

---

## 📜 Recent Development Decisions (Changelog)
- **Apr 22, 2026:** Implemented **Numerical Context Awareness** in `universal_markdown_fixer.py` to prevent corruption of version numbers (e.g., `v1.0`) and decimal metrics (e.g., `4.6`) during sequential footnote re-numbering.
- **Apr 22, 2026:** Fixed `mdbook-katex` rendering conflicts by auto-sanitizing escaped special characters (`\-`, `\&`) within the reference blocks.
- **Apr 17, 2026:** Established "Episode Number as Master Key" strategy.
- **Apr 17, 2026:** Transitioned `SUMMARY.md` to an unlimited, chronological Recent section for numbered episodes.
- **Apr 17, 2026:** Implemented project-level automation policies to bypass manual CLI prompts.
- **Apr 17, 2026:** Formalized the Agent's role in documentation and system synchronization.

---

For detailed technical documentation, see the [Scripts README](./scripts/README.md).
