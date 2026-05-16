# mdBook UI Extension Plan: The Asset Ingestion Bridge

## Objective
Evolve the deepDive publishing workflow by creating a "Dropzone UI" that handles asset ingestion and logistics. Instead of a standalone web app, this will be built as an **mdbook extension**, seamlessly integrating with the existing `mdbook` ecosystem.

## Architectural Shift: The mdbook Extension Model
- **Configuration:** Instead of a standalone `publish_config.json`, all configuration (source folders, asset destinations, script paths) will be embedded directly inside `book.toml` under a custom table (e.g., `[preprocessor.ui-bridge]` or a custom backend).
- **Technology Stack:** **Rust**. Since `mdbook` is written in Rust, writing the extension in Rust ensures native compatibility, easy installation (via `cargo`), and the ability to hook directly into mdbook's build lifecycle.
  - *Backend:* A lightweight embedded Rust web server (e.g., using `axum` or `actix-web`) that serves the UI and listens for file uploads, running on a port like `3001` alongside `mdbook serve`.
  - *Frontend:* Vanilla HTML/JS/CSS served by the Rust backend. Keep it incredibly simple—just a drag-and-drop zone and a few buttons.

## The Roadmap: Baby Steps

### Baby Step 1: The "Dropzone" & Auto-Renamer
- **Goal:** Eliminate the manual moving and renaming of files from the `Downloads` folder.
- **UI:** A simple web page with a text input for "Episode Number" and a drag-and-drop area.
- **Logic:** 
  - User types the episode number (e.g., `239`).
  - User drags the raw markdown (from Google Docs) and the raw cover image (from NotebookLM).
  - The Rust backend receives the files, renames them to match the Master Key (`239.md`, `239.png`), and saves them to `src/` and `src/img/` as configured in `book.toml`.

### Baby Step 2: One-Click Orchestration
- **Goal:** Trigger the three-tier publication scripts without using the CLI.
- **UI:** A "Process Episode" button appears after files are dropped.
- **Logic:** Clicking the button sends an API request to the Rust backend, which then executes the existing Python scripts (`fix_markdown.py`, `fix_pics.py`) via system shell calls, and runs `mdbook build` to validate. 

### Baby Step 3: The "Mosaic Video" Updater
- **Goal:** Seamlessly inject late-arriving infographic videos into existing episodes.
- **UI:** The same Dropzone UI. User enters the Episode Number and drags the MP4 file.
- **Logic:** The Rust backend renames the video (e.g., `239-clip.mp4`), moves it to `vid/`, and appends the `[vid: ...]` tag to the bottom of the existing markdown file, then runs `fix_vids.py`.

## Next Actions
- Review this document to confirm the Rust/mdbook extension approach.
- Define the `[preprocessor.ui-bridge]` schema for `book.toml`.
- Initialize the Rust crate for the mdbook extension.
