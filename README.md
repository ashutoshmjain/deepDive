# DeepDive with Gemini: Research & Automation

**[Live Site: deepdive.shutri.com](https://deepdive.shutri.com)**

This repository contains the research, show notes, and automated publishing toolchain for the **Deep Dive with Gemini** podcast. We explore the intersection of ancient philosophy, modern finance, and machine intelligence.

---

## 🚀 High-Fidelity Publishing Toolchain

DeepDive research is published using the **[mdIngest](https://github.com/ashutoshmjain/mdIngest)** toolchain. This "Research-to-Publish" workflow ensures 100% fidelity between the research session and the final production-grade article.

### The Workflow
1.  **Research:** Conducted in high-fidelity LLM sessions using a specialized research protocol.
2.  **Packaging:** Research is exported as a self-extracting payload using the **[Master Ingestion Prompt](https://github.com/ashutoshmjain/mdIngest#the-master-packaging-prompt)**.
3.  **Ingestion:** The **[md-publish](https://github.com/ashutoshmjain/mdIngest)** utility (installed globally) sanitizes the text, hardens KaTeX formulas, re-indexes citations, and synchronizes assets.
4.  **Enrichment:** Automated insertion of cover images, cinematic video scrolls, and Lightning wallet widgets.

---

## 🎨 Philosophy: Video-as-Cover

We are moving away from the "static image and text" standard of the last century. In this project, **static cover photos are obsolete**. Instead, we prioritize high-fidelity video overview infographics (created with tools like **[Mosaic.so](https://mosaic.so)**) to introduce each research episode. This "Video-as-Cover" approach allows researchers to provide an engaging, cinematic introduction that bridges the gap between rigorous academic depth and modern short-form media.

---

## 🔑 The "Master Key" Strategy
To ensure perfect synchronization between the website, repository, and podcast shows, the **Episode Number** (e.g., `225`) is the master key for all assets.
1.  **Articles:** Strictly named `src/225.md`.
2.  **Videos:** The primary visual asset. Named by episode number plus a descriptive suffix (e.g., `src/vid/234-intro.mp4`).
3.  **Images:** Archived only. Named `src/img/225.png`. They are NOT injected into the publication and serve only as a repository-level record.
4.  **Titles:** Automatically formatted as `# 225 : Title` (max 5 words).
5.  **Navigation:** Numbered episodes are pinned to the `# Recent ..` section of `SUMMARY.md`.

---

## 📱 Progressive Web App (PWA)
The deepDive platform is a high-performance PWA powered by **mdBook v0.5.3** and **Workbox**:
- **Offline Access:** Full precaching of all articles and core assets.
- **Reading Persistence:** Automatically resumes from the last-read article.
- **Optimized UI:** Custom high-fidelity theme with Font Awesome 6 integration.
- **Fast Updates:** One-click update notifications for new content.

---

## 🛠️ Technical Stack
- **Engine:** [mdBook](https://rust-lang.github.io/mdBook/) (v0.5.3)
- **Math:** [mdbook-katex](https://github.com/luser/mdbook-katex) (v0.10.0-alpha)
- **Ingestion:** [md-publish](https://github.com/ashutoshmjain/mdIngest) (v0.1.0)
- **PWA:** Google Workbox & Service Workers
- **Automation:** GitHub Actions (Automated build & deploy)

---

## 📜 Recent Development Decisions (Changelog)
- **June 09, 2026:** **Global Toolchain Alignment.** Standardized the environment on global `mdbook v0.5.3` and `md-publish`. Hardened the GitHub Actions workflow to surgically disable preprocessors for CI stability.
- **May 09, 2026:** Formalized the **Descriptive Video Naming Convention**. Transitioned to descriptive suffixes (e.g., `234-intro.mp4`) to improve asset visualization.
- **May 03, 2026:** Hardened `universal_markdown_fixer.py` for consistent H1 formatting and asset injection.
- **Apr 30, 2026:** Implemented refined footnote orchestration to handle mixed citation styles.
- **Apr 26, 2026:** Achieved perfect one-to-one mapping between `src/` and `SUMMARY.md`.
- **Apr 22, 2026:** Fixed `mdbook-katex` rendering conflicts by auto-sanitizing escaped special characters within reference blocks.

---

For detailed ingestion instructions, visit the **[mdIngest Repository](https://github.com/ashutoshmjain/mdIngest)**.
