# Longform Video Podcast Playbook & Architecture Blueprint

**Document Owner**: Ashutosh & Antigravity  
**Location**: `deepDive/LONGFORM_VIDEO_PLAYBOOK.md`  
**Reference Implementation**: Episode 248 (*"What Exactly is AI Autonomy?"* — 54.24 mins, 390 Bespoke Manim Scenes)  
**Show Brand**: **Slopcast** / **Deep Dive Podcast** (`SATOSHA` & `SATOSHI`)

---

## 1. Executive Summary & Core Philosophy

The **Longform Video Podcast Pipeline** transforms a 50–60 minute NotebookLM / Deep Dive master podcast audio track into a broadcast-grade `1920×1080` (`16:9`) animated video master (`podcast_<ep>.mp4`).

Instead of static waveform screens or distracting stock footage, the pipeline generates **350–400 bespoke, monochrome `740×740` vector animations** (~7.5 seconds per micro-beat) using **Manim Community Edition (ManimCE)**. These scenes are authored once during Longform production, stored as lightweight Python source code (`< 700 KB` per episode) in the `ddma` repository on GitHub, and later **reused as the visual building blocks for short-form Reels/Shorts (`248-1` .. `248-23`)**.

### Golden Principle: Reliability Over Rush
> **We have ample wall-clock time; we have zero tolerance for pipeline crashes.**  
> Every architectural choice prioritizes **staying far below the 131,072 input token ceiling** and **avoiding Windows file-locking collisions** caused by excessive parallel processes writing to shared directories.

---

## 2. Plain-English Explainer: What is Manim & How Does This Pipeline Work?

If you have never written a line of Manim code, here is how to think of the system:

1. **What is Manim?**
   - **Manim** (Mathematical Animation Engine, originally created by 3Blue1Brown) is a Python library where animations are written as **code instructions** rather than drawn by hand in Adobe After Effects.
   - For example, instead of dragging a circle with a mouse, a Python script says: *"Draw a pure white circle, draw a plug disconnecting from a wall socket, and slide it left over 2.5 seconds."*
   - Manim reads that Python script and outputs a crisp, tiny `.mp4` video clip (`740×740` pixels, ~80 KB per 7.5-second scene).

2. **How Does Spoken Audio Become 390 Animations?**
   - **Step 1 (Audio & Word Timestamps)**: Whisper (`transcription.json`) knows the exact millisecond every word is spoken across the 54-minute podcast, and `plan.json` slices the episode into ~23 topical chapters (Clips 1–23).
   - **Step 2 (Micro-Beat Slicing)**: Our Python script (`batch_archetype_pipeline.py`) slices each chapter into **~7.5-second spoken "micro-beats"** (~15–20 beats per chapter, ~390 beats across the full 54-minute show).
   - **Step 3 (Gemini Code Authoring)**: For each chapter, the script sends those 15–20 spoken sentences to the **Gemini Flash Lite API** (`gemini-3.5-flash-lite`) with a strict visual prompt: *"Write 15–20 simple, literal white-on-black Manim Python classes that figuratively illustrate these exact spoken words."*
   - **Step 4 (Manim Compilation)**: Our compiler (`compile_all_archetypes.py`) runs Manim on each Python class (`clip_01_gemini_scenes.py` .. `clip_23_gemini_scenes.py`) to produce 390 individual `740×740` `.mp4` files on your local disk (`media/videos/`).
   - **Step 5 (Master Compositing)**: Our compositor (`render_longform_parallel.py`) creates the `1920×1080` widescreen canvas, places the `SATOSHA — 🎙️ — SATOSHI` host strip and word-by-word yellow/white karaoke captions at the top, and pastes each `740×740` Manim animation in the center at its exact timestamp, muxing the -16 LUFS master audio into the final `121 MB` MP4.

---

## 3. Complete Responsibility Matrix (Who Does What?)

| Actor | Role | Concrete Responsibilities | What They NEVER Do |
| :--- | :--- | :--- | :--- |
| **1. You (The Producer / "Non-Technical Reviewer")** | Creative Director & Gatekeeper | • Record/ingest the episode in `mdIngest` Cockpit, mine it to a numbered Episode (`248.md`), and finalize the audio cuts/stings (`podcast_edit.json`).<br>• Trigger the Longform build by telling Antigravity: *"Generate and render the longform video for Episode X."*<br>• **Spot-Check Review**: Watch 2–3 minutes of the rendered video (e.g., the 0:30 welcome sting transition and a random mid-episode mark) to verify visual balance, caption readability, and thumbnail appeal.<br>• Approve export to `G:\My Drive\pickup_longform\`. | • You **never** write or debug Manim Python code.<br>• You **never** manually stitch video chunks or run FFmpeg commands.<br>• You **never** manually copy metadata JSONs. |
| **2. Application Code (`ddma` & `mdIngest` Python Scripts)** | Deterministic Workhorse | • **`batch_archetype_pipeline.py`**: Slices transcript into 7.5s beats and calls the Gemini API directly over HTTPS (outside Antigravity's chat context) to write `clip_XX_gemini_scenes.py`.<br>• **`manim_compat.py`**: Automatically intercepts and fixes 95% of LLM Manim hallucinations (wrong keyword arguments, missing easing constants, bad arrow radii).<br>• **`compile_all_archetypes.py`**: Compiles all 390 scenes into `740×740` MP4s with isolated temp directories and writes errors to a log file.<br>• **`render_longform_parallel.py`**: Composites the 1920×1080 video + karaoke captions + audio and exports to Google Drive. | • Application scripts **never** dump thousands of lines of raw code or FFmpeg progress bars into Antigravity's chat window. |
| **3. Gemini API (`gemini-3.5-flash-lite`)** | Scene Code Generator | • Receives 15–20 micro-beats per API call and outputs 15–20 Manim `Scene` subclasses (`Scene01_01` .. `Scene23_17`).<br>• Follows the **"Super Dumb & Literal"** monochrome white-on-black visual prompt. | • Does not consume Antigravity IDE chat tokens (runs via direct REST API key in `ddma/settings.json`). |
| **4. Antigravity (AI Pair Programmer)** | Orchestrator, Debugger & QA | • Launches the batch scripts **one background task at a time**.<br>• Inspects only the short summary log if 5–10 scenes out of 390 fail compilation, patches `manim_compat.py` surgically, and re-runs the failed scenes.<br>• Generates the full-bleed `1920×1080` architectural thumbnail and populates `pickup_longform` manifests.<br>• Commits the clean `.py` archetype library to `ddma` on GitHub. | • **NEVER** reads raw `transcript.jsonl` logs.<br>• **NEVER** reads full 800-line `clip_XX_gemini_scenes.py` files into chat.<br>• **NEVER** runs overlapping background tasks. |
| **5. Distribution Agent (`meta-muse` / Brownie)** | Automated Publisher | • Watches `G:\My Drive\pickup_longform\` for `podcast_<ep>.mp4`, `podcast_<ep>_thumbnail.jpg`, and `podcast_<ep>_video_meta.json`.<br>• Publishes to YouTube (`@shutoshabot`, playlist `"slopcast"`), Spotify for Creators (`"Slopcast"`), and TikTok Web/Desktop. | • Never touches local Git repositories or intermediate Manim files. |

---

## 4. Visual Style Guide, Typography & Pixel Geometry

### 4.1 Master Canvas & Encoding Specifications
- **Master Resolution**: `1920 × 1080` pixels (`16:9` widescreen HD)
- **Frame Rate**: `25 fps` (master composite) / `15 fps` (post-sting Manim micro-beats) / `30 fps` (pre-sting intro scene)
- **Background Color**: Pure Glossy Black (`#000000` / `RGB(0, 0, 0)`) across both the `1920×1080` master canvas and the `740×740` Manim canvas so the square box blends seamlessly with zero visible border.
- **Video Codec**: `libx264`, `-preset ultrafast` (chunk pass) $\rightarrow$ stream-copied via FFmpeg concat demuxer, `-crf 22`, `-pix_fmt yuv420p`
- **Audio Codec**: `aac`, `192 kbps`, mastered at `-16 LUFS` stereo (`podcast_<ep>.mp3`)

### 4.2 Exact Vertical & Horizontal Pixel Map (`1920 × 1080`)

```
+-----------------------------------------------------------------------------------+ (0, 0)
|                                                                                   |
|                          SATOSHA  ────── 🎙️ ──────  SATOSHI                       | y = 60 px (Host Strip)
|                                                                                   |
|            of what it actually takes for a system to sustain itself.              | y = 105..175 px (Karaoke Captions)
|                                                                                   |
|                   +-------------------------------------------+                   | y = 110 px (Post-Sting Box Top)
|                   |      (Upper Manim Canvas kept empty       |                   |   [y = 220 px for Pre-Sting 0..29.68s]
|                   |       so captions never collide)          |                   |
|                   |                                           |                   |
|                   |     +-------------------------------+     |                   | y = 443 px (Manim y = +0.4)
|                   |     |                               |     |                   |
|                   |     |   FIGURATIVE MONOCHROME       |     |                   |
|                   |     |   WHITE-ON-BLACK ANIMATION    |     |                   |
|                   |     |   (Centered x=960, 740x740)   |     |                   |
|                   |     |                               |     |                   |
|                   |     +-------------------------------+     |                   | y = 711 px (Manim y = -2.5)
|                   |                                           |                   |
|                   |   [y=622..672 inside box: BLANK / NO TITLE]                   | (No Archetype Title!)
|                   |   ─────────────────────────────────────   |                   | y = 789 px (Thin Footer Line, Manim y=-3.35)
|                   |   CATEGORY LABEL    DEEP DIVE • EP. 248   |                   | y = 801..811 px (Tiny Meta Labels)
|                   +-------------------------------------------+                   | y = 850 px (Post-Sting Box Bottom)
|                                                                                   |
|                      (230 px of clean black breathing room)                       |
+-----------------------------------------------------------------------------------+ (1920, 1080)
                     x = 590 px                                  x = 1330 px
```

### 4.3 Component Placement & Coordinates
1. **Top Host Strip (`y = 60 px`, centered at `x = 960 px`)**:
   - Left Host (`x = 860`, right-aligned): `SATOSHA` (Male voice — diarization key `"satoshi"` maps to display **`SATOSHA`**).
   - Right Host (`x = 1060`, left-aligned): `SATOSHI` (Female voice — diarization key `"satosha"` maps to display **`SATOSHI`**).
   - Center Icon (`x = 960, y = 60`): Vector studio microphone pulsing white `(255, 255, 255)` / slate `(51, 65, 85)` every `0.8s`, flanked by two `60 px` slate horizontal divider lines (`x = 875..935` and `x = 985..1045`, `RGB(71, 85, 105)`).
2. **Spoken Karaoke Subtitles (`y = 105..175 px`, centered horizontally)**:
   - Single-line segments (`total_width <= 1700 px`) render at `y = 115 px`.
   - Two-line segments (`total_width > 1700 px`) split evenly and render at `y = 105 px` (Line 1) and `y = 152 px` (Line 2).
   - **3-State Word Coloring**:
     - **Currently Spoken Word**: Vibrant Gold `RGB(255, 214, 10)` (`#FFD60A`)
     - **Already Spoken Words**: Pure White `RGB(255, 255, 255)` (`#FFFFFF`)
     - **Upcoming Words in Segment**: Muted Gray `RGB(115, 115, 115)` (`#737373`)
3. **Welcome Sting Title Card (`t = 29.68s .. 39.68s`, or episode-specific sting window)**:
   - Full-screen borderless podcast title card centered at `(960, 560)`:
     - `D E E P   D I V E   P O D C A S T` (`y = 390`)
     - `E P I S O D E   <NUM>` (`y = 450`)
     - Main Episode Title in `52pt Bold` (`y = 525`)
     - Subtitle in `26pt Regular` (`y = 615`)
     - `HOSTED BY SATOSHA & SATOSHI` (`y = 705`)
     - `deepdive.shutri.com/<NUM>.html` (`y = 760`)
4. **740×740 Manim Square Viewport (`box_x = 590 px`)**:
   - **Pre-Sting Intro (`t < 29.68s`)**: Placed at `cur_box_y = 220 px` (`y = 220..960`).
   - **Post-Sting Body (`t > 39.68s`)**: Elevated to `cur_box_y = 110 px` (`y = 110..850`) because all post-sting Manim scenes leave their upper half (`y in [0.4, 4.0]` in Manim coordinates) completely blank for captions. Elevating `cur_box_y` to `110 px` centers the actual vector drawing (`Manim y in [-2.5, +0.4]`) right around `y = 443..711 px` on the `1080p` screen, leaving `230 px` of balanced black space below the footer.
5. **Strict Prohibition on Archetype Titles (Permanent Rule)**:
   - **NO bold scene/archetype titles** at the top or bottom of the `740×740` canvas (`y = -2.95` / pixel rows `622..672` are permanently disabled in `manim_compat.py` and masked in `render_longform_parallel.py` and `archetype_studio.py`). They cause cognitive overload and pull the visual weight of the box downward.
   - **Subtle Footer Retained**: Only the thin `1.5 px` horizontal line (`Manim y = -3.35`, opacity `0.40`, pixel row `679..680`) and tiny `10pt` metadata labels (`CATEGORY LABEL` on the left, `DEEP DIVE PODCAST • EP. <NUM>` on the right, opacity `0.65`, pixel rows `691..701`) are kept.
6. **Zero-Empty-Screen Persistence Rule (Permanent Invariant)**:
   - **The screen must NEVER stay empty (blank black)** because an animation finished early or faded out before the spoken beat ended.
   - **No Terminal `FadeOut` on Main Illustrations**: Manim `Scene` classes must **NEVER** end with `self.play(FadeOut(...))` on the primary visual objects. Instead, every scene must end with `self.wait(...)` holding its final visual state on screen.
   - **Last-Frame Hold (`tpad=stop_mode=clone`)**: Whenever a beat's spoken audio duration is longer than the compiled Manim animation, the stitcher (`archetype_studio.py` and `render_longform_parallel.py`) clones and holds the final visible illustration frame continuously until the next beat begins speaking.
7. **Vertical Centering in 9:16 Short Clips (`1080 × 1920`)**:
   - In DDMA Shorts (`archetype_studio.py`), the illustration zone (`y = 110..622` of the `740×740` frame) is shifted upward by `110 px` while keeping the footer (`y = 672..740`) anchored at the bottom, centering the graphic midway between the upper captions line and the bottom footer line.

### 4.4 Typography Table

| Element | Font Family | Weight | Size | Color (`RGB` / Hex) |
| :--- | :--- | :--- | :--- | :--- |
| **Host Names (`SATOSHA` / `SATOSHI`)** | Arial / Segoe UI (`arialbd.ttf`) | Bold | `22 px` | `RGB(226, 232, 240)` (`#E2E8F0`) |
| **Karaoke Captions** | Arial / Segoe UI (`arialbd.ttf`) | Bold | `36 px` | Gold `#FFD60A` / White `#FFFFFF` / Gray `#737373` |
| **Welcome Sting Main Title** | Arial (`arialbd.ttf`) | Bold | `52 px` | Pure White `#FFFFFF` |
| **Welcome Sting Subtitle** | Arial (`arial.ttf`) | Regular | `26 px` | `RGB(200, 210, 225)` |
| **Manim Diagram Labels (Internal)** | Arial | Bold / Normal | `14–18 pt` | Pure White `#FFFFFF` |
| **Manim Footer Meta Labels** | Arial | Bold (L) / Normal (R) | `10 pt` | Pure White `#FFFFFF` @ `65%` opacity |

### 4.5 Thumbnail Style Guide (`podcast_<ep>_thumbnail.jpg`)
- **Dimensions**: Full-bleed `1920 × 1080` JPEG (`quality=95`), filling the entire 16:9 frame edge-to-edge (with a `36 px` architectural blueprint frame and corner registration ticks).
- **Left Column (`x = 100..990`)**:
  - High-contrast Gold `SLOPCAST` pill badge (`#FFD60A` fill, black bold text) + `EPISODE <NUM> • <MIN> MIN` badge.
  - Giant two-line Hero Headline (`62pt` lead-in + `108pt` core question/title).
  - Gold accent bar + all-caps thesis subhead (`30pt` Gold).
  - Three numbered (`01`, `02`, `03`) architectural contrast cards summarizing the episode's 3 core takeaways.
- **Right Column (`x = 1080..1840`)**:
  - Full-height (`r = 355 px`) **System Architecture / Autopoietic Loop Diagram** with bold white/gold geometric nodes and a central focal emblem (`₿` / core mechanism).

---

## 5. Lessons Learned: Preventing Token Ceiling & Windows File-Lock Errors

During our first Episode 248 run, we hit two major roadblocks. Here is why they happened and the permanent engineering defenses now in place:

### Lesson 1: Why Did We Hit `HTTP 400: Input Token Count Exceeds 131072`?
1. **Root Cause A — Reading Raw `transcript.jsonl`**: When recovering session state, calling `read_file` on `.system_generated/logs/transcript.jsonl` dumped 46 KB (~12,000 tokens) per call directly into the prompt window.
2. **Root Cause B — Reading Generated Manim Files in Chat**: 23 files × 700 lines = ~16,000 lines of Python code. Reading full `clip_XX_gemini_scenes.py` files into chat rapidly filled the 131K context window.
3. **Root Cause C — Verbose Compiler Stdout & Overlapping Background Tasks**: Running multiple background tasks simultaneously caused duplicate `<SYSTEM_MESSAGE>` log dumps with long Manim progress bars and tracebacks.

#### Permanent Defenses Against Token Ceiling:
- **Guardrail 1**: Never call `read_file` on `transcript.jsonl`. Use a 5-line Python snippet to print only the last 5 step summaries (`< 1 KB`).
- **Guardrail 2**: `compile_all_archetypes.py` routes all Manim stderr/tracebacks to `compile_errors_summary.log` and prints only 1-line summaries per clip to stdout.
- **Guardrail 3**: Never read entire `clip_XX_gemini_scenes.py` files in chat. Inspect failing lines with a targeted Python regex/AST script and patch `ddma/archetypes/manim_compat.py` globally so one fix heals all 23 files at once.
- **Guardrail 4**: Run **strictly ONE background task at a time** and wait for it to finish before starting the next. Recommend `/compact` between Phase 1 (Scene Generation/Compilation) and Phase 2 (Master Compositing).

---

### Lesson 2: Why Did Windows File-Locking (`PermissionError: [WinError 32]`) & OOM Crashes Happen?
1. **Root Cause A — Parallel Manim Processes Sharing `media/Tex` and `media/texts`**:
   - When Manim renders `Text()` or `MathTex()`, it writes temporary `.svg` files into `media/texts/<hash>.svg`. When 8 Manim processes compiled scenes from the same file or shared the same `media/texts/` folder simultaneously on Windows, NTFS locked the `.svg` or `partial_movie_file_list.txt` files, causing random `PermissionError: [WinError 32] The process cannot access the file because it is being used by another process`.
2. **Root Cause B — Pre-Decoding All 390 MP4s Into RAM Before `ProcessPoolExecutor`**:
   - Pre-loading 390 decoded RGB frame arrays in the main process and passing them to 4 spawned Windows worker processes duplicated multi-gigabyte dictionaries across `pickle` IPC pipes, triggering `MemoryError` / broken pipe crashes.

#### Permanent Defenses Against Windows File Locks & Memory Crashes:
- **Defense 1 — File-Level Sequential or Isolated `--media_dir` Compilation**:
  - Never run two Manim processes against the **same** `clip_XX_gemini_scenes.py` file concurrently.
  - Compile clip files with at most **2–3 workers across different clip files** (or sequentially overnight since time is abundant), and always pass `-q l` / `--fps 15` with isolated output folders.
- **Defense 2 — Single-Scene LRU Frame Cache Inside Each Compositor Worker**:
  - In `render_longform_parallel.py`, workers receive only lightweight file path strings (`scene_intervals`). Each worker keeps **only 1 Manim MP4 decoded in RAM at a time** (`cached_mp4_path` / `cached_frames`), using `< 50 MB` of RAM per worker.
- **Defense 3 — Unique Per-Chunk Output Filenames**:
  - Each of the 4 parallel compositor workers writes exclusively to its own `temp_chunks/chunk_0X.mp4` with `stderr=subprocess.DEVNULL` (preventing OS pipe buffer deadlocks). The main process touches the chunks only after `pool.map()` has completely exited and closed all file handles.

---

## 6. Distribution Strategy & Platform Specifications

| Platform | Target Account / Show | Upload Limit | Supported for 54-Min Master? | Action / Configuration |
| :--- | :--- | :--- | :--- | :--- |
| **YouTube** | `https://www.youtube.com/@shutoshabot` | 12 hours / 256 GB | **YES** | Upload `podcast_<ep>.mp4` + `podcast_<ep>_thumbnail.jpg` and add to playlist **`"slopcast"`**. |
| **Spotify for Creators (Video)** | Show: **`Slopcast`** (`07r9EZMLpFC7qwZwxsJ5P9`)<br>`https://creators.spotify.com/home/show/07r9EZMLpFC7qwZwxsJ5P9` | 12 hours / 50 GB | **YES** | Upload `podcast_<ep>.mp4` as a Video Episode on Spotify for Creators under **Slopcast**. |
| **TikTok (Long-Form)** | `https://www.tiktok.com/@shutoshabot` | **60 minutes** / 10 GB *(Web/Desktop upload only; mobile app is capped at 10m)* | **YES (via Web/Desktop)** | Upload `podcast_<ep>.mp4` via **TikTok Web/Desktop uploader** (`54:14` and `121 MB` fits cleanly under the 60-min / 10 GB desktop limit). |
| **Instagram** | `https://www.instagram.com/shutoshabot/` | **20 mins** (Reels) / **10 mins** (Standard Feed) | **NO** *(for 54m master)* | **Disabled (`enabled: false`)** in `longform_meta.json`. Instagram is served by the short-form Reels clips (`248-1` .. `248-23`). |

---

## 7. Configuration Management: Where Everything Lives (GitHub vs. Google Drive vs. Local)

To prevent repository bloat and keep a single source of truth, every file has a strict home:

```
c:\Users\ashut\OneDrive\Desktop\github\
│
├── deepDive/                                  [GITHUB REPO: Publication & Content Engine]
│   ├── LONGFORM_VIDEO_PLAYBOOK.md             • This master playbook (Tracked in Git)
│   ├── src/<ep>.md                            • Published research article + embedded short-form video strip (Tracked)
│   └── src/ddma/docs/episodes/<ep>/
│       ├── transcription.json                 • Whisper word-level timestamps (Tracked)
│       ├── podcast_edit.json                  • Non-destructive cuts & sting placements (Tracked)
│       ├── plan.json                          • 23-part chapter boundaries & captions (Tracked)
│       ├── cover.webp                         • Episode square cover art (Tracked)
│       ├── clips/248-1.mp4 .. 248-5.mp4       • Curated short-form Reels for web carousel (Tracked)
│       ├── podcast_248.mp3                    • Master audio (IGNORED by .gitignore)
│       └── podcast_248.mp4                    • Master longform video (IGNORED by .gitignore)
│
├── ddma/                                      [GITHUB REPO: Pure Code & Archetype Scene Library]
│   ├── archetypes/                            • SINGLE SOURCE OF TRUTH FOR SCENE CODE (~695 KB total, Tracked in Git!)
│   │   ├── manim_compat.py                    • ManimCE compatibility shims & footer helper
│   │   ├── chapter_01_scenes_strict.py        • Pre-sting intro scene
│   │   ├── clip_01_gemini_scenes.py .. clip_23_gemini_scenes.py  • All 389 Manim Scene classes
│   │   └── clip_02_meta.json .. clip_23_meta.json                • Beat timing & class mappings
│   ├── generated_archetypes.json              • Reusable archetype catalog (Tracked in Git)
│   ├── batch_archetype_pipeline.py            • Gemini Flash Lite scene generator script (Tracked)
│   ├── compile_all_archetypes.py              • Safe Manim batch compiler (Tracked)
│   ├── render_longform_parallel.py            • 1080p parallel compositor (Tracked)
│   └── clips/248-longform-master.mp4          • Local working render output (IGNORED by .gitignore)
│
├── mdIngest/                                  [GITHUB REPO: Pure Code & Cockpit Web UI]
│   └── ui/
│       ├── server.py                          • Backend server & Google Drive export endpoints (Tracked)
│       └── cockpit.html                       • Cockpit UI defaulting video export to G:/My Drive/pickup_longform (Tracked)
│
└── media/videos/                              [LOCAL SCRATCH CACHE ONLY — Not a Git Repo]
    └── clip_01_gemini_scenes/740p15/*.mp4     • 390 compiled 740x740 Manim MP4 building blocks (~31 MB total)
                                                 (Kept locally for fast re-compositing & Shorts reuse; partial_movie_files purged)

G:\My Drive\                                   [GOOGLE DRIVE: Distribution Agent Pickup Handoff]
├── pickup_longform/                           • LONGFORM VIDEO PICKUP FOLDER
│   ├── podcast_248.mp4                        • 121.09 MB 1080p Longform Master Video
│   ├── podcast_248_thumbnail.jpg              • Full-bleed 1920x1080 Slopcast Architectural Thumbnail
│   ├── podcast_248_video_meta.json            • Complete platform/playlist distribution manifest
│   ├── video_meta.json                        • Mirror manifest for agent compatibility
│   └── longform_meta.json                     • Mirror manifest for agent compatibility
│
├── Podcast_Pickup/                            • AUDIO PODCAST PICKUP FOLDER (Spotify Audio)
│   ├── podcast_248.mp3
│   └── podcast_248_meta.json
│
└── Course_Pickup/                             • ANIMATED COURSES PICKUP FOLDER (Modules 1..6)
```

---

## 8. Financials: Token Usage, API Costs & Storage Requirements

### 8.1 Gemini API Cost (Scene Generation via `batch_archetype_pipeline.py`)
Because `batch_archetype_pipeline.py` calls **`gemini-3.5-flash-lite`** directly over REST (one request per clip × 23 clips):
- **Input Tokens**: ~1,200 tokens per clip × 23 clips = **~27,600 input tokens total**
- **Output Tokens**: ~3,500 tokens of Python code per clip × 23 clips = **~80,500 output tokens total**
- **Total Gemini API Financial Cost per 54-Min Episode**: **~$0.03 – $0.06 USD** (virtually free!).

### 8.2 Antigravity IDE Context Window Budget (131,072 Input Token Limit)
When following the clean playbook (running batch scripts in the background and reading only summary logs):
- **Phase 1 (Generate & Compile 390 Scenes)**: ~15,000 – 25,000 context tokens (including patching 5–10 failing scenes via `manim_compat.py`).
- **Phase 2 (Composite Master Video, Generate Thumbnail & Export to Drive)**: ~10,000 – 15,000 context tokens.
- **Total Session Context Footprint**: **~30,000 – 40,000 tokens** (staying well below 35% of the 131,072 ceiling, with zero `HTTP 400` errors).

### 8.3 Disk & Cloud Storage Footprint (Per 54-Minute Episode)

| Asset Category | Storage Location | Size (Before Cleanup) | Size (After Cleanup) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Manim Python Source & Meta (`ddma/archetypes/`)** | GitHub (`ddma`) | `695 KB` | **`695 KB` (`0.68 MB`)** | Permanent reusable vector code library in Git. |
| **390 Compiled `740×740` Manim MP4s (`media/videos/`)** | Local Disk Only | `81.25 MB` | **`31.10 MB`** | Deleting `partial_movie_files/` frees ~50 MB while keeping all 390 `.mp4` building blocks. |
| **Temporary Compositor Chunks (`temp_chunks/`)** | Local Disk Only | `44.38 MB` | **`0 MB` (Deleted)** | Auto-deleted after FFmpeg concat demuxer finishes. |
| **Final 1080p Longform Master (`podcast_<ep>.mp4`)** | Google Drive (`pickup_longform`) | `121.09 MB` | **`121.09 MB`** | High-efficiency H.264 monochrome vector compression (~2.2 MB per minute of 1080p video!). |
| **16:9 Architectural Thumbnail (`podcast_<ep>_thumbnail.jpg`)** | Google Drive (`pickup_longform`) | `310 KB` | **`310 KB` (`0.3 MB`)** | Full-bleed `1920×1080` JPEG. |

---

## 9. Step-by-Step Standard Operating Procedure (SOP) for the Next Episode

When Episode 249 is ready for its Longform Video Master, we follow this exact 6-step checklist:

1. **Pre-Flight Check (1 min)**:
   - Verify `podcast_<ep>.mp3`, `transcription.json`, `podcast_edit.json`, and `plan.json` exist in `deepDive/src/ddma/docs/episodes/<ep>/`.
2. **Step 1 — Batch Scene Code Generation (~4 mins wall time)**:
   - Run `python ddma/batch_archetype_pipeline.py --ep <ep>` as a **single** background task.
   - Generates `clip_01_gemini_scenes.py` .. `clip_XX_gemini_scenes.py` (with **no archetype titles**, pure white-on-black figurative visuals).
3. **Step 2 — Batch Manim Compilation (~15–20 mins wall time)**:
   - Run `python ddma/compile_all_archetypes.py` with low concurrency (`MAX_WORKERS = 2`) to prevent Windows NTFS SVG/partial-file locks.
   - If any scenes fail in `compile_errors_summary.log`, patch `ddma/archetypes/manim_compat.py` and re-run only the missing scenes until `100%` of scenes are verified on disk.
4. **Step 3 — Parallel 1080p Master Compositing (~7 mins wall time)**:
   - Run `python ddma/render_longform_parallel.py` (4 CPU workers, single-scene LRU RAM cache, unique `chunk_01.mp4`..`chunk_08.mp4` files).
5. **Step 4 — Human Spot-Check & Full-Bleed Thumbnail**:
   - Generate the full-bleed `1920×1080` Slopcast architectural thumbnail (`podcast_<ep>_thumbnail.jpg`).
   - You spot-check the welcome sting transition (`~0:30`) and post-sting framing (`~1:00`).
6. **Step 5 — Export to `G:\My Drive\pickup_longform\`, Cleanup & Git Push**:
   - Copy `podcast_<ep>.mp4`, `podcast_<ep>_thumbnail.jpg`, and `podcast_<ep>_video_meta.json` to `G:\My Drive\pickup_longform\`.
   - Purge `partial_movie_files/` and `temp_chunks/`.
   - Commit and push the `< 1 MB` `.py` scene library in `ddma/archetypes/` to GitHub.
