---
trigger: model_decision
description: "dd_hub folder layout, platform routing and pickup rules, and the three clip consumers — read when the task touches distribution, publishing, the player, episode pages, or the dd_hub vault."
---


## Distribution Strategy

This section defines the single source of truth for asset storage, folder hierarchy, and platform routing across **all Creative Agents** (Local Windows Workbench, Antigravity Cloud VM, Headless GCP Docker) and the **Distribution Agent (`meta-muse` / Muse)**.

### 1. Unified Google Drive Hub (`G:\My Drive\dd_hub\` / `DD_HUB_ROOT`)

All input payloads, longform masters, mobile review reels, and intermediate episode state reside under a single Google Drive root (`dd_hub`), resolved via `DD_HUB_ROOT` (defaults to `G:\My Drive\dd_hub` on Windows, `/mnt/gdrive/dd_hub` in Docker, or `/workspace/dd_hub` in Cloud VM):

```text
dd_hub/
├── inputs/                                  # 📥 RAW EPISODE DROP ZONE
│   └── <ep>/                                # Created per new episode (e.g., inputs/249/)
│       ├── <ep>.m4a                         # Raw continuous NotebookLM master audio
│       └── payload.py                       # Research text, equations, quotes, citations
│
├── audio/                                   # 🎧 LONGFORM AUDIO OUTBOX (For Muse + Pixel Mobile)
│   ├── podcast_<ep>.mp3                     # -16 LUFS Master Audio (<ep> built into filename)
│   ├── podcast_<ep>_cover.jpg               # 1600×1600 square cover art
│   └── podcast_<ep>_meta.json               # Distribution manifest for Muse
│
├── video/                                   # 📺 LONGFORM VIDEO OUTBOX (For Muse + Pixel Mobile)
│   ├── podcast_<ep>.mp4                     # 1920×1080 Widescreen HD Master (<ep> built into filename)
│   ├── podcast_<ep>_thumbnail.jpg           # 1920×1080 widescreen thumbnail
│   └── podcast_<ep>_video_meta.json         # Video distribution manifest for Muse
│
├── mosaics/                                 # 📱 PIXEL MOBILE REVIEW & MANUAL UPLOAD (Mosaic Reels)
│   ├── <ep>-0.mp4                           # Full compiled 9:16 Mosaic reel (<ep>-<clip>.mp4)
│   └── <ep>-1.mp4
│
├── manims/                                  # 📱 PIXEL MOBILE REVIEW & MANUAL UPLOAD (Manim Reels)
│   ├── <ep>-0.mp4                           # Full compiled 9:16 Manim reel (<ep>-<clip>.mp4)
│   └── <ep>-1.mp4
│
└── episodes/                                # 🧠 STUDIO BACKEND VAULT (Creative Agents Only)
    └── <ep>/                                # Intermediate state synced across Local, VM & GCP Docker
        ├── transcription.json               # Whisper word-level timestamps (transcribe once, reuse everywhere)
        ├── podcast_edit.json                # Stripped welcome cut + 22 canonical music stings
        ├── plan.json                        # Clip boundaries, 3-word titles, 5-word bridges, visual_source
        ├── bodies_740/                      # Cached 740×740 visual bodies (mosaic_body_<n>.mp4, manim_body_<n>.mp4)
        └── archetypes/                      # Generated Python Manim scripts (clip_<nn>_gemini_scenes.py)
```

### 2. Platform Routing & Pickup Rules for Distribution Agent (`meta-muse` / Muse)

| Asset Type | Pickup Location | Target Platforms & Routing Rule |
| :--- | :--- | :--- |
| **1. Research Article & Interactive Math** | **GitHub (`deepDive` repo)**:<br>`src/<ep>.md` | Published via `mdBook` + `KaTeX` to **`deepDive.shutri.com/<ep>.html`** and syndicated as long-form prose to **Nostr (NIP-23)**. |
| **2. Longform Audio Podcast (`podcast_<ep>.mp3`)** | **Google Drive**:<br>`dd_hub/audio/podcast_<ep>.mp3`<br>+ `podcast_<ep>_meta.json` | Picked up by **Muse** and uploaded **ONLY to Spotify ("deepDive" show)**. From Spotify, it is automatically syndicated via RSS to **Apple Podcasts, Fountain.fm, and all Podcast 2.0 clients**. |
| **3. Longform Video Podcast (`podcast_<ep>.mp4`)** | **Google Drive**:<br>`dd_hub/video/podcast_<ep>.mp4`<br>+ `podcast_<ep>_video_meta.json` | Picked up by **Muse** and published to **YouTube**, **TikTok**, and **Spotify ("slopcast" show)** *(plus **Instagram** once long-form video support is enabled)*. |
| **4. Short Reels — Automated Distribution (`<ep>-<clip>.mp4`)** | **GitHub (`deepDive` repo)**:<br>`src/ddma/docs/episodes/<ep>/clips/<ep>-<clip>.mp4` | **Muse**, **`deepdive.shutri.com`** (episode carousel + DDMA player), and **`shutri.com`** (reference-implementation showcase linking the player) ALL pick up the **Active Master** reel from **GitHub Pages** (`deepDive/src/ddma/docs/episodes/<ep>/clips/`). Whichever engine (`mosaic` or `manim`) is marked as `visual_source` in `plan.json` is pushed here. A clip is not live until all three can fetch it (see the "Clips are the key product" section in `GEMINI.md`). |
| **5. Short Reels — Mobile Review & Manual Fallback** | **Google Drive**:<br>`dd_hub/mosaics/<ep>-<clip>.mp4`<br>`dd_hub/manims/<ep>-<clip>.mp4` | Exposed as 1-tap Google Drive shortcuts on Pixel mobile for on-the-go review, side-by-side Manim vs. Mosaic comparison, and manual platform uploads if automated distribution ever fails. **Muse ignores `mosaics/` and `manims/`**. |

### 3. Ephemeral Manim `media/` Rules Across Local, VM, and GCP Docker
- **Strict Non-Commit & Non-Drive Invariant**: ManimCE's local compilation cache (`media/videos/...`, `media/texts/*.svg`, `media/Tex/*.svg`) generates thousands of tiny files. **NEVER commit `media/` to GitHub** and **NEVER place `media/` on Google Drive**.
- **Execution Environment Split**:
  - **Antigravity Cloud VM**: Handles ingestion, Whisper alignment, Gemini audio/clip planning, Mosaic API rendering, and archetype Python code generation (`archetypes/*.py`). Does not run Manim binary rendering.
  - **Local Windows & Headless GCP Docker**: Render Manim inside local ephemeral storage (`deepDive/ddma/media/` locally or `/tmp/media` in Docker), cache the stitched `740×740` silent body into `dd_hub/episodes/<ep>/bodies_740/`, export the full `9:16` vertical reel to `dd_hub/manims/<ep>-<clip>.mp4`, and (when selected as Active Master) push to `deepDive/src/ddma/docs/episodes/<ep>/clips/<ep>-<clip>.mp4`.

### Why Web Belongs Under Research
- Standard social platforms (LinkedIn, Nostr, Substack) are not inherently designed for publishing academic research -- they fail at compiling and rendering complex LaTeX formulas, KaTeX matrices, and mathematical proofs.
- The **Web channel** powered by `mdBook` + `KaTeX` is the designated medium for Research because it preserves mathematical rigor, citation backlinks, and interactive SVG/code models losslessly.
- Therefore, **`mdserve (local)`** and **`Push (Remote)`** live under the **Research** pillar.

### Why Audio & Distribution Belong Under Podcast
- Long-form audio direct from NotebookLM provides the conversational baseline for the entire episode.
- The **Podcast pillar** manages non-destructive editing (`podcast_edit.json`): word-level text search & deletions, Gemini-guided music sting placement, and -16 LUFS podcast mastering.
- The rendered podcast and metadata are exported to Google Drive for pickup by **meta-muse**, which drives distribution to **Spotify for Creators**, while retaining Nostr (NIP-23) long-form prose publishing.

### Why DDMA Belongs Under Reels
- The **Reels pillar** turns research and narrative concepts into visual short-form video clips (740×740 / 9:16) for TikTok, Instagram Reels, and YouTube Shorts.
- Tooling lives in DDMA Studio and the responsive clips inspection deck.
