# Scripts Directory

This directory contains the automation tools for the `deepDive` project. The primary tool is `universal_markdown_fixer.py`, which is the "frozen" standard for processing all markdown content in this repository.

## Universal Markdown Fixer (`universal_markdown_fixer.py`)

### Purpose
The `universal_markdown_fixer.py` is a comprehensive automation script designed to ensure all markdown files in the `src/` directory adhere to the project's specific aesthetic, structural, and technical standards. It automates the transition from raw research drafts to polished, `mdbook`-compatible articles.

### Key Features

#### 1. Content Enhancement
- **Cover Image Injection:** Automatically identifies and inserts a cover image after the main heading. It looks for a `.png` file in `src/img/` matching the markdown filename.
- **Podcast Integration:** Injects a centered HTML snippet providing links to the "Deep Dive with Gemini" podcast on Spotify, Apple Podcasts, YouTube Music, YouTube, and Fountain.fm.
- **Heading Standardization:** Cleans up H1 and H2 headers by removing unnecessary bolding and ensuring consistent spacing.

#### 2. Technical Fixes
- **Citation to Footnote Conversion:** Parses the "Works cited" section and re-indexes all in-text citations into proper Markdown footnotes (`[^N]`). This ensures interactive navigation within the book.
- **KaTeX & Currency Compatibility:** 
    - Replaces `$` symbols used for currency with `USD` (e.g., `$10B` becomes `10B USD`) to prevent KaTeX rendering errors.
    - Escapes literal `$` symbols as `\\$` to ensure the `mdbook-katex` plugin treats them as text rather than math delimiters.
- **Cleanup:** Removes "Truncated" placeholders and normalizes whitespace throughout the document.

#### 3. Navigation Management (`SUMMARY.md`)
- **Recent Section Update:** Automatically adds the processed file to the `# Recent ..` section at the top of `SUMMARY.md`.
- **Path-Aliasing Hack:** Employs the `././filename.md` trick for the top three most recent files to allow them to be listed in the "Recent" section without triggering `mdbook`'s duplicate file warnings.
- **Automatic Restoration:** When a file is bumped out of the "Recent" section (top 3), the script automatically restores it to its appropriate thematic category based on a pre-defined keyword mapping.
- **Title Extraction:** Uses the actual H1 header from the markdown file as the link text in the summary, ensuring the navigation matches the article title exactly.

#### 4. Automated Verification
- **Completeness Crosscheck:** As a final step, the script tallies every `.md` file in the `src/` folder and compares it against the entries in `SUMMARY.md`. It provides a `SUCCESS` or `WARNING` report to ensure no content is orphaned from the navigation.

### Usage

To process a new or updated file, run the following command from the project root:

```bash
python3 scripts/universal_markdown_fixer.py src/your-file-name.md
```

### Configuration
The script contains a `CATEGORIES` dictionary that maps keywords to their respective sections in `SUMMARY.md`. Update this mapping to handle new thematic areas or specific filing preferences.

---
*Note: This script is pre-authorized for routine Git and file operations in the `deepDive` workspace.*
