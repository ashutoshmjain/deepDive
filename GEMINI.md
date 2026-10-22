# Antigravity Workspace Guidelines & Push Rules

## Repository Roles & Strict Media Boundaries

1. **`ddma` (Pure Code / Tool Repository)**:
   - Contains ONLY Python engine code, configuration, scripts, and lightweight metadata (JSON).
   - **STRICT RULE**: NEVER commit or push binary media assets (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`, clips, stings) to `ddma`.
   - All generated clips remain in local working scratch directories or are published exclusively to `deepDive`.

2. **`mdIngest` (Pure Code / Web UI Repository)**:
   - Contains ONLY ingestion logic, server code, and UI components (`cockpit.html`, etc.).
   - **STRICT RULE**: NEVER commit or push audio/video media files or binary assets to `mdIngest`.

3. **`deepDive` (Publication Repository)**:
   - The ONLY repository designated for published episode articles (`src/<num>.md`) and curated episode publication media (`src/ddma/docs/episodes/<num>/clips/*.mp4`).

## Pre-Push Verification Checklist
- Before committing and pushing in `ddma` or `mdIngest`, always verify that NO binary media files (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`) are staged.
- Only code, templates, and JSON metadata are allowed in `ddma` and `mdIngest`.

## Architectural Philosophy: The "Research to Reels" Pipeline

The system is structured as a 3-pillar content progression with dedicated distribution channels at each stage:

```
[ Level 1: Global Pillars ]
  1. 🔬 Research                 2. 🎙️ Podcast                  3. 🎬 Reels (formerly Media)
       │                              │                              │
[ Level 2: Channels & Tools ]         │                              │
  ├── Web Channel (mdBook)       ├── Audio Master & Social      └── Visual & Audio (DDMA)
  │   • KaTeX math & proofs      │   • NotebookLM Audio Ingest      • 740×740 square video deck
  │   • Interactive models       │   • Word-Timed Transcript Cuts   • Sound check & audio stings
  │   • Local mdserve (port 3000)│   • Gemini Music Review & Stings • Mosaic timeline integration
  │   • Remote push to web       │   • FFmpeg Loudnorm (-16 LUFS)
  │   • deepdive.shutri.com      │   • Google Drive → meta-muse
  │                              │   • Spotify for Creators & Nostr
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

