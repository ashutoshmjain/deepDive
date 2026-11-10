---
trigger: model_decision
description: "Canvas, typography, and cartoon standards for short reels and longform video — read when rendering, styling, or reviewing clip visuals."
---


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
| **Clip Numbering** | **`0`-Based (`<ep>-0`, `<ep>-1`, ...)**: `Clip 0` = Prologue; `Clip 1+` matches spoken `"Clip 1"`, `"Clip 2"` | Continuous chapter timeline across `Clip 0`..`Clip N` |
| **Intro Billboard Card** | **Included (1.5s)**: `Clip 0` shows `EPISODE <num>` + Episode Title; `Clip 1+` shows `EPISODE <num> • PART <num>` + **≤ 3-word Title** on pure `#000000` | **Stripped**: Replaced by `deepDive-strong.mp3` (`16.71s`) after `Clip 0` hook + stripped redundant spoken welcome |
| **Outro Billboard Card** | **Included (5.0s)**: Ultra-concise **≤ 5-word** curiosity question/exclamation on pure `#000000` with delayed-echo host sign-off | **Stripped**: Never show outro bridge cards between chapters |
| **Mid / Inter-Clip Stings (`Bluesy` / `Howling`)** | **Intra-Clip (after Hook)**: 5.5s sting (`0.2s` gap, `2.0s` fade-out, `1.0s` full-volume speech entry) | **Inter-Clip (between every clip)**: 5.5s alternating `Bluesy Vibes` / `Howling` at the end of every clip before the next `"Clip N"` starts |
| **Outro Sting (`deepDive-conclusion`)** | **Included**: 5.5s in Mosaic body + 5.0s delayed-echo repeat over Outro Card | **Finale Only (`5.5s`)**: Played at the very end of the episode (`"I am Satosha, and I am Satoshi"` + ~4s music) |
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
| **Intro Billboard Cards** | Bold Punchy Sans-Serif (Segoe UI Bold / Arial Bold) | **Header (`EPISODE <n>` / `PART <n>`)**: Silver (`#B4B4B4`)<br>**Title**: Stark White (`#FFFFFF`) | **Pure Glossy Black (`#000000`)** with 2px subtle bottom rule (`#505050`); **zero blurred frame bleed or gray box** | `Clip 0`: `EPISODE <n>` + Episode Title (no Part #). `Clip 1+`: `EPISODE <n> • PART <n>` + **max 3-word Title**. |
| **Outro Teaser Cards** | Bold Sans-Serif (Segoe UI Bold / Arial Bold) | **Curiosity Question**: Stark White (`#FFFFFF`) | **Pure Glossy Black (`#000000`)**; zero background bleed | **Strictly max 5 words** (e.g., `"What is 8D Totality !"`). Never repeat spoken `"Coming up in..."`. |
| **Bottom Footer Bar Strip** | Minimalist Clean Monospace (`DejaVuSansMono`) | **Muted Slate Gray (`#64748b`)** on Left & Right | 1px horizontal delimiter line (`#1e293b` / `#334155`) at `y ≈ cur_box_y + 680` | Low-contrast (14px–16px); never distracts from visual deck; **STRICTLY NO TITLES**. |
