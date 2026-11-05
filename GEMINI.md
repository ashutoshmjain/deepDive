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

## Primary Workbench & Fan-Out Push Invariant

1. **`deepDive` is the Active Development Workbench**:
   - Because `start_ingest.bat` launches `python ingest/server.py` and executes `ddma/ddma.py` directly inside `deepDive`, **all active code changes, bug fixes, UI styling, and testing must be done directly in `deepDive`**:
     - UI & Server fixes $\rightarrow$ [`deepDive/ingest/`](file:///c:/Users/ashut/OneDrive/Desktop/github/deepDive/ingest/) (`server.py`, `cockpit.html`, `settings.json`)
     - Engine & animation fixes $\rightarrow$ [`deepDive/ddma/`](file:///c:/Users/ashut/OneDrive/Desktop/github/deepDive/ddma/) (`ddma.py`, `archetype_studio.py`, etc.)
   - This guarantees that what you test on `localhost:8088` is immediately what is running.

2. **The "Push All" Fan-Out Protocol**:
   Whenever instructed to commit and push per our push strategy:
   - **Step 1: Fan-Out Mirroring**: Copy the tested code from `deepDive` outward into the standalone repos:
     - `deepDive/ingest/*` $\longrightarrow$ `mdIngest/ui/*`
     - `deepDive/ddma/ddma.py` $\longrightarrow$ `ddma/ddma.py`
   - **Step 2: Pre-Push Media Verification**: Verify that `mdIngest` and `ddma` contain ONLY code and templates -- **NEVER binary media** (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`).
   - **Step 3: Tri-Repo Commit & Push**:
     - Commit and push `deepDive` to its GitHub remote (preserves local workbench + publication articles/media).
     - Commit and push `mdIngest` to its GitHub remote (clean upstream UI/server tool).
     - Commit and push `ddma` to its GitHub remote (clean upstream CLI tool).

## Pre-Push Verification Checklist
- Before committing and pushing in `ddma` or `mdIngest`, always verify that NO binary media files (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`) are staged.
- Only code, templates, and JSON metadata are allowed in `ddma` and `mdIngest`.
- Always mirror changes made in `deepDive` out to `mdIngest` and `ddma` before finalizing pushes.

## Ephemeral Media & Build Artifacts (`media/` Directory)
- **Role**: ManimCE's local intermediate compilation cache and render scratchpad (`media/videos/clip_XX_gemini_scenes/740p15/*.mp4`, `media/texts/*.svg`, `media/images/`).
- **Strict Non-Commit Invariant**: The `media/` directory is an ephemeral build target (analogous to `node_modules/`, `__pycache__/`, or `target/` in Rust). **NEVER commit or push `media/` to GitHub**.
- **Cloud vs. Local Agent Parity**:
  - The source of truth stored in Git is purely the Python archetype code (`ddma/archetypes/*.py`, `< 700 KB` per episode).
  - Cloud Antigravity environments do NOT expect or require a pre-existing `media/` directory.
  - When rendering in the cloud or locally, running `compile_all_archetypes.py` or `archetype_studio.py` generates the `media/` directory on-demand.
  - **Google Drive Inputs & Handoff**:
  - **Incoming Raw Assets**: `G:\My Drive\agy_inputs/<ep>/` (e.g., `agy_inputs/249/` containing the raw `audio.mp3`/`audio.m4a`, `payload.py`, and research scripts).
  - **Master Exports**: Final longform deliverables stream directly to `G:\My Drive\pickup_longform/` (`podcast_<ep>.mp4`, `podcast_<ep>_thumbnail.jpg`), leaving intermediate `media/` chunks completely disposable.

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

### Tripartite Base Audio Pattern & Zero-Trim Plan Structuring
- **NotebookLM Ingestion Standard**: The base master audio follows a deterministic 3-part spoken structure for every clip:
  1. **Punchline Hook (10–20s)**: Spoken thesis statement, announcing the clip number and title.
  2. **Core Deliberation (~2 mins)**: In-depth conversational discussion between Satosha and Satoshi.
  3. **Outro Teaser (10–20s)**: Spoken bridge stating what to look for in the next clip.
- **Automated Card Casting**:
  - Because the transcript explicitly speaks the Clip Number, Title, and Next Teaser, Gemini automatically casts:
    - **Intro Card**: `title`, `hook_quote`, dynamic PIL/Mosaic card layout.
    - **Outro Card**: `coming_up_title`, `bridge_question`, teaser prompt.
- **Zero Manual Audio Trimming**: DDMA uses `faster-whisper large-v3-turbo` word timestamps to snap directly to Gemini's extracted phrase boundaries.
- **Deterministic Music Sting Invariant**:
  - **Mid-Sting (between Punchline and Deliberation)**: Alternates between `Bluesy Vibes` and `Howling` (5.5s, 0.5s crossfade).
  - **Outro-Sting (after Teaser)**: Always `deepDive-conclusion.mp3` (5.5s).

### Clip-Level Visual Purity (No Intra-Clip Mixing)
- **Engine Purity**: Clips NEVER mix engines internally. Each clip is authored **100% in Mosaic OR 100% in Manim**.
- **Active Master Routing**: In `plan.json`, each clip designates its `visual_source`: `"mosaic"` or `"manim"`. The Longform Compositor dynamically picks up whichever master is active.

### Dual-Track Assembly Protocol: Short Reels vs. Longform Video
1. **Track A: Short Reels (`clips/<ep>-<num>.mp4` • 740×740 / 9:16 for Social)**:
   - **Full Standalone Package**: `[Intro Card] -> [Punchline] -> [Mid-Sting: Bluesy/Howling] -> [Deliberation] -> [Teaser] -> [Outro Card] -> [Outro-Sting: deepDive-conclusion]`.
   - Pure, self-contained promotional reels for TikTok, Shorts, and Instagram.
2. **Track B: Longform Video Podcast (`podcast_<ep>.mp4` • 1920×1080 Widescreen Master)**:
   - **Seamless Flow-Through Rules**:
     - ✂️ **STRIP all Intro Cards & Outro Cards**: Keeps video kinetic without graphic billboard interruptions every 2 minutes.
     - ✂️ **STRIP Outro Stings (`deepDive-conclusion`) BETWEEN clips**: Avoids stopping/concluding the conversation every 2 minutes.
     - 🎵 **KEEP `deepDive-conclusion` on Clip 1 ONLY**: Functions as the Master Show Opener transition into the episode.
     - 🎵 **KEEP Mid-Stings (`Bluesy Vibes` / `Howling`)**: Preserved between punchline and deliberation across all chapters for periodic musical pacing (~every 2 minutes).
     - **Visual Deck**: Plays the Active Master (`visual_source`: Mosaic or Manim) in the central 740×740 canvas.

## Unified Canvas Visual Standards: Longform Podcast vs. DDMA Short Reels

All video production -- whether 1920×1080 widescreen master podcasts or 740×740 / 9:16 short social reels -- shares a unified visual grammar, layout hierarchy, and caption engine. Voice diarization has been retired in favor of a clean, static host header with an active animated microphone.

### 1. Shared Visual Invariants (Common to Both Formats)
- **Host Header Strip**:
  - Display: Static **`SATOSHA  --  🎙️  --  SATOSHI`** centered directly above the captions.
  - **Dynamic Blinking Microphone**: The central microphone icon pulses/blinks dynamically during active speech, eliminating the need for voice diarization or host switching.
- **Word-Level Karaoke Captions**:
  - High-visibility yellow & white typography rendered via Whisper word timestamps.
  - Active spoken word highlights in **Yellow** (`#FFD700` / `#FFF066`), while upcoming words remain in **White** (`#FFFFFF`).
  - Text wraps cleanly within safe zones; zero text clipping.
- **Background & Canvas Styling**:
  - Pure Glossy Black (`#000000` / `RGB(0, 0, 0)`) across all canvas borders and backgrounds.
  - High-contrast, mobile-legible vector lines (bold strokes, 4px–14px, solid white on pure black).
- **Central Visual Deck (740×740)**:
  - Both formats feature the central square `740×740` visual engine playing the active master: **100% Mosaic OR 100% Manim** (no intra-clip mixing).
  - Figurative, "super dumb" cartoon storytelling and clean diagrams without small data clutter or academic tables.
- **Bottom Footer Bar Strip**:
  - Located directly below the central 740×740 visual deck across both formats.
  - **Left Side**:
    - **Manim**: Displays the **Archetype Name** (e.g., `Archetype: KineticVector`).
    - **Mosaic**: Displays **`Mosaic`**.
    - **STRICT INVARIANT: NO ARCHETYPE TITLE EVER**: Never display chapter titles, scene titles, or descriptive text clutter in the footer.
  - **Right Side**:
    - Displays **`deepDive podcast`** for both Manim and Mosaic.
  - **Styling**: Sleek, low-contrast minimalist font (`#64748b` muted slate gray) with a subtle horizontal delimiter line (`y ≈ cur_box_y + 680`).

### 2. Format Comparison & Contrast Matrix

| Visual Element | Track A: DDMA Short Reels (`clips/<ep>-<num>.mp4`) | Track B: Longform Video Master (`podcast_<ep>.mp4`) |
| :--- | :--- | :--- |
| **Canvas Resolution & Aspect Ratio** | **`740×740`** (Square Deck) or **`1080×1920`** (`9:16` Vertical for TikTok / Shorts / Reels) | **`1920×1080`** (`16:9` Widescreen HD Master for YouTube, Spotify, Cockpit) |
| **Pillar Placement** | **Pillar 3: Reels** (Fast, punchy, self-contained promotional shorts) | **Pillar 2: Podcast** (Broadcast episodic deep dive) |
| **Intro Billboard Card** | **Included**: 3–5s Title Card with spoken title & hook quote | **Stripped**: Never show intro graphic cards between chapters |
| **Outro Billboard Card** | **Included**: 3–5s "Coming Up in Next Part" teaser card | **Stripped**: Never show outro bridge cards between chapters |
| **Mid-Sting (Bluesy / Howling)** | **Included**: 5.5s transition between Punchline and Deliberation | **Included**: Preserved across all chapters for periodic musical pacing (~every 2m) |
| **Outro Sting (`deepDive-conclusion`)** | **Included**: 5.5s closing musical sting at the end of every clip | **Stripped between chapters**; **Preserved on Clip 1 ONLY** as the Master Show Opener |
| **Host Header & Karaoke** | Centered in upper canvas safe zone above 740×740 visual square | Centered in upper widescreen strip (`y: 60-120`) above 740×740 central visual square |
| **Micro-Beat Pacing** | Self-contained single-chapter arc (~2 to 2.5 minutes total) | Continuous seamless playback (~350–400 micro-beats across 50–60 minutes) |
| **Patching & Authoring** | Authored in DDMA Studio / Mosaic Workspace | In-place chapter patching via Cockpit **Beat Studio** under the Podcast tab |

### 3. "Super Dumb & Figurative" Cartoon Standard (Manim & Mosaic)
- **Literal Figurative Cartoons**: Scenes must be immediately recognizable cartoons illustrating the spoken dialogue (e.g., a literal brass faucet dripping water into a mug, an airplane flying through clouds, a forklift stacking crates, a prism splitting light).
- **NO DATA CLUTTER**: Never stuff animations with number tables, tiny telemetry cards, or dense academic text. Pure, bold, kinetic cartoon storytelling.
- **Lines & Styling**: Bold, thick lines (4px–14px), solid white on pure black `#000000`, zero background clutter.

### 4. Coherent Black & White Typography & Color Hierarchy (Every Visual Element)

The entire production strictly follows a **Monochrome Noir with Functional Yellow Accent** hierarchy. Random primary colors, gradients, and pastel clutter are permanently prohibited across all visual layers:

| Visual Element | Typography & Font Family | Foreground Color | Background / Stroke / Delimiter | Sizing & Safe Zone Rules |
| :--- | :--- | :--- | :--- | :--- |
| **Canvas Background** | N/A | N/A | **Pure Glossy Black (`#000000`)** | Full 1920×1080 & 740×740 surfaces; zero background texture or noise. |
| **Host Header Strip** | Clean Bold Sans-Serif (Arial Bold / Inter), Uppercase | **Stark White (`#FFFFFF`)**; Delimiter `--` in Muted Slate (`#64748b`) | None (Floats on pure black) | Centered directly above karaoke captions; dynamic white microphone pulses on speech. |
| **Word-Level Captions** | Heavy Sans-Serif (Arial Bold / DejaVu Sans Bold) | **Spoken Word**: Yellow (`#FFD700` / `#FFF066`)<br>**Upcoming Words**: White (`#FFFFFF`) | None (Zero stroke outline / zero dark box) | 32px–40px equivalent; centered, generous line-height (1.3×); strict safe-margin clamping. |
| **Central Visual Deck (Manim)** | Monospace (`DejaVuSansMono`) or Minimalist Sans | **Pure White (`#FFFFFF`)** for all vector lines, figures, and Math/KaTeX | Vector lines: 4px–14px bold solid white; Fills: `#000000` or `#0e1420` | Minimum 28px–36px for labels; zero tiny telemetry text or table clutter. |
| **Central Visual Deck (Mosaic)** | Bold Geometric Sans-Serif (Inter / Helvetica Neue) | **Pure White (`#FFFFFF`)** for headings, metrics, and diagrams | Stark black containers with subtle 1px slate borders (`#334155`) | High-contrast mobile legibility; no low-contrast gray-on-gray text. |
| **Intro Billboard Cards** | Bold Punchy Sans-Serif | **Title**: Stark White (`#FFFFFF`)<br>**Hook Quote**: Muted Silver (`#E2E8F0`) | Pure Black (`#000000`) with 1px subtle divider (`#334155`) | 48px–56px title scale; max 3–5 words per line; strictly centered. |
| **Outro Teaser Cards** | Bold Sans-Serif / Monospace | **Teaser Banner**: Stark White (`#FFFFFF`)<br>**Question**: Silver (`#CBD5E1`) | Pure Black (`#000000`) | 40px–48px scale; clear hierarchy between bridge label and question. |
| **Bottom Footer Bar Strip** | Minimalist Clean Monospace (`DejaVuSansMono`) | **Muted Slate Gray (`#64748b`)** on Left & Right | 1px horizontal delimiter line (`#1e293b` / `#334155`) at `y ≈ cur_box_y + 680` | Low-contrast (14px–16px); never distracts from visual deck; **STRICTLY NO TITLES**. |

## Token Budget & Context Hygiene Rules (131K Input Token Ceiling)
To prevent `HTTP 400: The input token count exceeds the maximum number of tokens allowed 131072`:
1. **Never Read Raw `transcript.jsonl` via `read_file`**:
   - When recovering context from a prior trajectory, NEVER call `read_file` on `transcript.jsonl` (which dumps 46KB / ~12,000 tokens per call). Always use a compact Python script to extract only the last 5–10 step summaries (`< 1 KB` stdout).
2. **Surgical Inspection & Batch Patching Across Generated Files**:
   - Never read entire multi-hundred-line generated Manim scripts (`clip_*_gemini_scenes.py`) into chat context. Use targeted Python regex/AST scripts to inspect only failing classes or lines and apply consolidated fixes in `manim_compat.py` or batch scripts.
3. **Summary-Only CLI Output**:
   - Compiler and compositor scripts (`compile_all_archetypes.py`, `render_longform_parallel.py`) must keep stdout concise (summary lines only) and route verbose tracebacks to log files.
4. **Strictly One Background Task at a Time**:
   - Never launch overlapping background compilation/render commands; wait for the active background task to finish so duplicate `<SYSTEM_MESSAGE>` log dumps do not collide in context.
5. **Subagent Delegation & `/compact`**:
   - Delegate repetitive multi-file debugging or generation loops to a subagent (`invoke_subagent`) so its work stays in an isolated context window, and recommend `/compact` before transitioning between major pipeline phases.




