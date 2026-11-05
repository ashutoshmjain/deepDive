# Antigravity Workspace Guidelines & Push Rules

## Repository Roles & Strict Media Boundaries

1. **`ddma` (Pure Code / Tool Repository)**:
   - Contains ONLY Python engine code, configuration, scripts, and lightweight metadata (JSON).
   - **STRICT RULE**: NEVER commit or push binary media assets (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`, clips, stings) to `ddma`.
   - All generated clips remain in local working scratch directories or are published exclusively to `deepDive`.

2. **`mdIngest` (Pure Code / Web UI Repository)**:
   - Contains ONLY ingestion logic, server code, and UI components (`cockpit.html`, etc.).
   - **STRICT RULE**: NEVER commit or push audio/video media files or binary assets to `mdIngest`.

3. **`deepDive` (Local Studio Workbench & Publication Repository)**:
   - **Dual Role**:
     a. **Unified Local Runtime**: On local machines, `deepDive` acts as the active "monorepo" execution workbench (`start_ingest.bat` launches `python ingest/server.py` and calls `ddma/ddma.py` inside `deepDive`).
     b. **Publication Repository**: Designated repository for published episode articles (`src/<num>.md`) and curated episode publication media (`src/ddma/docs/episodes/<num>/clips/*.mp4`).

## Dual-Sync Invariant (Keeping Upstream & Local Studio in Lockstep)
- **Automatic Code Mirroring**:
  Whenever code, server endpoints, or UI features are modified in standalone tool repositories, they **MUST always be synchronized into `deepDive`**:
  - `mdIngest/ui/*` $\longleftrightarrow$ `deepDive/ingest/*` (`server.py`, `cockpit.html`, `settings.json`)
  - `ddma/ddma.py` $\longleftrightarrow$ `deepDive/ddma/ddma.py`
- **Dual-Push Rule**:
  - Code changes are committed and pushed to their standalone repositories (`mdIngest`, `ddma`) to maintain clean, media-free upstream tools.
  - The mirrored code is **also committed and pushed to `deepDive`** on GitHub so the local launcher (`start_ingest.bat`) and local working environment are fully preserved and always up to date.

## Pre-Push Verification Checklist
- Before committing and pushing in `ddma` or `mdIngest`, always verify that NO binary media files (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`) are staged.
- Only code, templates, and JSON metadata are allowed in `ddma` and `mdIngest`.
- Before closing any tool or UI feature update, verify that code parity is maintained across `mdIngest` $\longleftrightarrow$ `deepDive/ingest` and `ddma` $\longleftrightarrow$ `deepDive/ddma`.

## Architectural Philosophy: The "Research to Reels" Pipeline

The system is structured as a 3-pillar content progression with dedicated distribution channels at each stage:

```
[ Level 1: Global Pillars ]
  1. 🔬 Research                 2. 🎙️ Podcast (Audio & Longform Video)   3. 🎬 Reels (Shorts & Clips)
       │                                        │                                       │
[ Level 2: Channels & Tools ]                   │                                       │
  ├── Web Channel (mdBook)                 ├── Audio & Longform Video Studio        └── Visual & Audio (DDMA)
  │   • KaTeX math & proofs                │   • NotebookLM Audio Ingest                • 740×740 square video deck
  │   • Interactive models                 │   • Word-Timed Transcript Cuts             • Sound check & audio stings
  │   • Local mdserve (port 3000)          │   • Gemini Music Review & Stings           • Mosaic timeline integration
  │   • Remote push to web                 │   • FFmpeg Loudnorm (-16 LUFS)             • TikTok / Shorts / Reels
  │   • deepdive.shutri.com                │   • Longform Video Podcast (1920×1080)
  │                                        │   • Beat-by-Beat Timeline & Archetype Studio
  │                                        │   • Google Drive pickup_longform → meta-muse
  │                                        │   • Spotify for Creators, YouTube & Nostr
```

### Why Web Belongs Under Research
- Standard social platforms (LinkedIn, Nostr, Substack) are not inherently designed for publishing academic research—they fail at compiling and rendering complex LaTeX formulas, KaTeX matrices, and mathematical proofs.
- The **Web channel** powered by `mdBook` + `KaTeX` is the designated medium for Research because it preserves mathematical rigor, citation backlinks, and interactive SVG/code models losslessly.
- Therefore, **`mdserve (local)`** and **`Push (Remote)`** live under the **Research** pillar.

### Why Audio & Distribution Belong Under Podcast
- Long-form audio direct from NotebookLM provides the conversational baseline for the entire episode.
- The **Podcast pillar** manages non-destructive editing (`podcast_edit.json`): word-level text search & deletions, Gemini-guided music sting placement, and -16 LUFS podcast mastering.
- The rendered podcast and metadata are exported to Google Drive for pickup by **meta-muse**, which drives distribution to **Spotify for Creators**, while retaining Nostr (NIP-23) long-form prose publishing.

### Why DDMA Belongs Under Reels
- The **Reels pillar** turns research and narrative concepts into visual short-form video clips (740×740 / 9:16) for TikTok, Instagram Reels, and YouTube Shorts.
- Tooling lives in DDMA Studio and the responsive clips inspection deck.

## Longform Video Podcast Architecture & Playbook (Under Podcast Tab)

> [!IMPORTANT]
> **Courses Retired**: Standalone course modules have been retired in favor of **broadcast-grade Longform Video Podcasts (`podcast_<ep>.mp4`)**, fully integrated under the **Podcast tab** in the Cockpit. Detailed blueprint lives in [`deepDive/LONGFORM_VIDEO_PLAYBOOK.md`](file:///c:/Users/ashut/OneDrive/Desktop/github/deepDive/LONGFORM_VIDEO_PLAYBOOK.md).

### Core Architectural Tenets:
1. **Master Specs**:
   - Master Resolution: `1920×1080` (`16:9` widescreen HD, glossy black `#000000`).
   - Host Header Strip: `SATOSHA — 🎙️ — SATOSHI` with yellow/white word-level karaoke captions.
   - Central Visual Canvas: Monochrome `740×740` ManimCE vector animations centered on screen.
2. **Micro-Beat Pacing (~7.5s per scene)**:
   - Slices each ~2-minute chapter into **~15–20 micro-beats** (~350–400 bespoke scenes across a 50–60 min show).
   - Authoring is handled deterministically via `batch_archetype_pipeline.py` using `gemini-3.5-flash-lite`.
3. **"Super Dumb & Figurative" Visual Standard**:
   - **Literal Figurative Cartoons**: Scenes must be immediately recognizable cartoons illustrating the spoken dialogue (e.g., a literal brass faucet dripping water into a mug, an airplane flying through clouds, a forklift stacking crates).
   - **NO DATA CLUTTER**: Never stuff animations with number tables, tiny telemetry cards, or dense academic text. Pure, bold, kinetic cartoon storytelling.
   - **Lines & Styling**: Bold, thick lines (4px–14px), solid white on pure black `#000000`, zero background clutter.
4. **Cockpit Beat Studio & In-Place Patching**:
   - The Cockpit's **Podcast Tab** includes the **Horizontal-Split Longform Beat-by-Beat Timeline**.
   - Allows previewing any single beat's video, regenerating scene code via AI prompt, and **1-click patching** the modified chapter into the Master MP4 in seconds without re-rendering the whole 50-minute episode.
5. **Asset Recycling**:
   - The ~390 Manim scenes authored for Longform Video become the reusable visual building blocks for short-form Reels/Shorts in DDMA.

## Host Identity & Voice Diarization Rules (Permanent Invariant)
- **Host Genders**:
  - **Satosha is MALE** (deep male voice).
  - **Satoshi is FEMALE** (female voice).
- **Voice Diarization Mapping**:
  - Diarization segment `"satoshi"` (male voice) $\implies$ Display **`SATOSHA`**.
  - Diarization segment `"satosha"` (female voice) $\implies$ Display **`SATOSHI`**.
- This mapping is permanent and applies everywhere across DDMA, Infographics, and Podcasts.


