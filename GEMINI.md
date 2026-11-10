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
     - Engine & animation fixes $\rightarrow$ [`deepDive/ddma/`](file:///c:/Users/ashut/OneDrive/Desktop/github/deepDive/ddma/) (`ddma.py`, `curator.html`, `scratch/run_curator.py`, `scratch/review_episode_bridges.py`, `archetype_studio.py`, etc.)
   - This guarantees that what you test on `localhost:8088` and `localhost:8000` is immediately what is running.

2. **The "Push All" Fan-Out Protocol**:
   Whenever instructed to commit and push per our push strategy:
   - **Step 1: Fan-Out Mirroring**: Copy the tested code from `deepDive` outward into the standalone repos:
     - `deepDive/ingest/*` $\longrightarrow$ `mdIngest/ui/*`
     - `deepDive/ddma/ddma.py`, `curator.html`, `settings.json`, `scratch/run_curator.py`, `scratch/review_episode_bridges.py` $\longrightarrow$ `ddma/`
   - **Step 2: Pre-Push Media Verification**: Verify that `mdIngest` and `ddma` contain ONLY code and templates -- **NEVER binary media** (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`).
   - **Step 3: Tri-Repo Commit & Push**:
     - Commit and push `deepDive` to its GitHub remote (preserves local workbench + publication articles/media).
     - Commit and push `mdIngest` to its GitHub remote (clean upstream UI/server tool).
     - Commit and push `ddma` to its GitHub remote (clean upstream CLI tool).

3. **Active Master Clips Publication & Distribution Invariant**:
   - **Local Staging vs. Remote Distribution**:
     - Whenever an active master clip is compiled in DDMA (`ddma compile-clip` or Curator `/set-active-master`), it is automatically staged to:
       a. `deepDive/src/ddma/docs/episodes/<ep>/clips/<ep>-<clip>.mp4` (via `resolve_deepdive_publication_clips_dir()`, anchored on `Path(__file__).resolve()`).
       b. `dd_hub/mosaics/<ep>-<clip>.mp4` (or `manims/`) for 1-tap mobile review.
     - **CRITICAL DISTRIBUTION RULE**: Google Drive (`dd_hub/mosaics/` and `manims/`) serves ONLY as a personal mobile review outbox and manual fallback. **`deepdive.shutri.com` and the automated distribution agent (`meta-muse` / Muse) ALWAYS pick up the Active Master reel directly from GitHub (`deepDive/src/ddma/docs/episodes/<ep>/clips/`)**.
     - An active clip is **NOT considered published or live on the web until it is committed and pushed to GitHub in `deepDive`**.
   - **Pre-Push Markdown Carousel Synchronization**:
     - Before committing and pushing `deepDive`, `sync_episode_clips_and_markdown(ep)` MUST be executed (either automatically triggered by Cockpit's "Push (Remote)" button at `/api/git/push` or run as part of the push checklist).
     - This automatically scans all canonical clips (`<ep>-*.mp4`) in both `deepDive/ddma/clips/` and `deepDive/src/ddma/docs/episodes/<ep>/clips/`, stages them into `src/ddma/docs/episodes/<ep>/clips/`, and regenerates the `<!-- VIDEO_STRIP_START -->` ... `<!-- VIDEO_STRIP_END -->` carousel in `src/<ep>.md` so the live mdBook article embeds the full clip deck.
   - **Idempotent Overwrite on Re-Run**:
     - Re-running Mosaic or Manim on an active clip automatically overwrites the local staged master in `deepDive/src/ddma/docs/episodes/<ep>/clips/<ep>-<clip>.mp4` and `dd_hub/mosaics/<ep>-<clip>.mp4`.
     - Upon the next Push, Git seamlessly commits and pushes the updated binary video replacing the previous version on GitHub, updating `deepdive.shutri.com` and Muse without changing URL schemes or breaking links.
   - **Strict Pure-Code Boundaries on Standalone Repos**:
     - `deepDive` is the **ONLY** repository permitted to stage and push active binary clips (`src/ddma/docs/episodes/<ep>/clips/*.mp4`).
     - `ddma` and `mdIngest` must **NEVER** contain or stage binary `.mp4` assets during the Fan-Out push.

## Pre-Push Verification Checklist
- Before committing and pushing in `ddma` or `mdIngest`, always verify that NO binary media files (`*.mp4`, `*.mp3`, `*.wav`, `*.m4a`) are staged.
- Only code, templates, and JSON metadata are allowed in `ddma` and `mdIngest`.
- Always mirror changes made in `deepDive` out to `mdIngest` and `ddma` before finalizing pushes.
- For active episode clips: verify that `sync_episode_clips_and_markdown(ep)` has staged all active master clips (`<ep>-<clip>.mp4`) into `deepDive/src/ddma/docs/episodes/<ep>/clips/` and regenerated the `src/<ep>.md` video strip before committing `deepDive`.

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
| **4. Short Reels — Automated Distribution (`<ep>-<clip>.mp4`)** | **GitHub (`deepDive` repo)**:<br>`src/ddma/docs/episodes/<ep>/clips/<ep>-<clip>.mp4` | **Muse** and **`deepDive.shutri.com`** ALWAYS pick up the **Active Master** reel directly from **GitHub** (`deepDive/src/ddma/docs/episodes/<ep>/clips/`). Whichever engine (`mosaic` or `manim`) is marked as `visual_source` in `plan.json` is pushed here. |
| **5. Short Reels — Mobile Review & Manual Fallback** | **Google Drive**:<br>`dd_hub/mosaics/<ep>-<clip>.mp4`<br>`dd_hub/manims/<ep>-<clip>.mp4` | Exposed as 1-tap Google Drive shortcuts on Pixel mobile for on-the-go review, side-by-side Manim vs. Mosaic comparison, and manual platform uploads if automated distribution ever fails. **Muse ignores `mosaics/` and `manims/`**. |

### 3. Ephemeral Manim `media/` Rules Across Local, VM, and GCP Docker
- **Strict Non-Commit & Non-Drive Invariant**: ManimCE's local compilation cache (`media/videos/...`, `media/texts/*.svg`, `media/Tex/*.svg`) generates thousands of tiny files. **NEVER commit `media/` to GitHub** and **NEVER place `media/` on Google Drive**.
- **Execution Environment Split**:
  - **Antigravity Cloud VM**: Handles ingestion, Whisper alignment, Gemini audio/clip planning, Mosaic API rendering, and archetype Python code generation (`archetypes/*.py`). Does not run Manim binary rendering.
  - **Local Windows & Headless GCP Docker**: Render Manim inside local ephemeral storage (`deepDive/ddma/media/` locally or `/tmp/media` in Docker), cache the stitched `740×740` silent body into `dd_hub/episodes/<ep>/bodies_740/`, export the full `9:16` vertical reel to `dd_hub/manims/<ep>-<clip>.mp4`, and (when selected as Active Master) push to `deepDive/src/ddma/docs/episodes/<ep>/clips/<ep>-<clip>.mp4`.

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
- **NotebookLM Ingestion Standard**: The user provides a Python script (`payload.py`) for text/research and a single continuous 20–60 minute master audio file structured clip-wise with a deterministic 3-part spoken pattern for every clip:
  1. **Punchline Hook (10–20s)**: Spoken thesis statement, announcing the clip number and title.
  2. **Core Deliberation (~2 mins)**: In-depth conversational discussion between Satosha and Satoshi.
  3. **Outro Teaser (10–20s)**: Spoken bridge stating what to look for in the next clip.
- **Zero Manual Audio Trimming**: DDMA uses `faster-whisper large-v3-turbo` word timestamps + `resolve_acoustic_word_end` (16kHz PCM RMS energy tail scanning) to snap directly to spoken cue boundaries (`"Clip 1"`, `"Clip 2"`, etc.) or Gemini's extracted phrase boundaries without cutting trailing sibilants.
- **Deterministic Music Sting Invariant**:
  - **Mid-Sting (between Punchline and Deliberation)**: Alternates between `Bluesy Vibes` and `Howling` (`duration: 5.5s`, `silence_before: 0.2s`, `fade_out: 2.0s`, `crossfade: 1.0s`).
  - **Outro-Sting (after Teaser)**: Always `deepDive-conclusion.mp3` (`duration: 5.5s`, `silence_before: 0.2s`, `fade_out: 2.0s`, `crossfade: 0.0s`).

## Clip Dynamics (Zero-Review Automated Clip Production Standard)

To achieve zero-touch automated clip production without manual review cycles, all clip numbering, Intro Title Cards, Outro Bridge Cards, and Gemini casting prompts strictly obey the following 4 invariants:

1. **Pure `#000000` Intro & Outro Canvas (Zero Background Frame Bleed)**:
   - Intro and Outro cards MUST always render on a **pure solid `#000000` black canvas** (`RGB(0, 0, 0)`).
   - **STRICT PROHIBITION**: Never extract or blur frames from `clips/*-{clip_num}.mp4` as background images, and never draw translucent gray boxes (`(18, 18, 18, 200)`). Extracting wildcard clip frames causes cross-episode title card bleed (e.g., Episode 248's title card bleeding behind Episode 249).
   - The Intro Card text rendered in the video preview (`🎬 Intro`) must always match the editable `Intro Card Title Text` field in DDMA Studio 1-to-1.

2. **0-Based Clip Numbering (`<ep>-0`, `<ep>-1`, ...) Aligned with Spoken Audio**:
   - Clips in `plan.json` and DDMA Studio are numbered starting from **`<ep>-0` (`Clip 0`)**:
     - **`Clip 0` (`<ep>-0`)**: The Episode Prologue / Cold Open (spoken before the hosts announce `"Clip 1"`).
     - **`Clip 1` (`<ep>-1`), `Clip 2` (`<ep>-2`), ...**: Strictly aligned with the spoken transcript cues (`"Clip one"`, `"Clip two"`, etc.).
   - **UI Memory Invariant**: `curator.html` and backend endpoints (`/get-clip-intro`, `/get-clip-outro`, `/compile-clip`, etc.) MUST preserve `0`-based clip numbering (`clip.num = 0, 1, 2, ...`) and NEVER re-index `Clip 0` to `1` in DOM memory. This guarantees that when the hosts say `"Clip 1"`, the card badge is `<ep>-1` and the title card says `PART 1`.

3. **Concise Intro Cards (Max 3 Words for Part Titles; No Part Number on `Clip 0`)**:
   - **For `Clip 0` (`<ep>-0`, Episode Prologue)**:
     - Top Header: **`EPISODE <number>`** (strictly **NO `PART` number**).
     - Main Title: **Episode Title** (e.g., `"What Exactly Is Reality?"`).
   - **For `Clip 1+` (`<ep>-1`, `<ep>-2`, ...)**:
     - Top Header: **`EPISODE <number> • PART <number>`** (where `<number>` matches the spoken clip number).
     - Main Title: **STRICTLY MAXIMUM 3 WORDS** designed to capture immediate attention -- typically the scientific concept, the scientist's name, or the core idea (e.g., `"8D Totality"`, `"Sensory Split"`, `"Division Algebras"`, `"Scalar Observer"`, `"Quaternions"`).

4. **Ultra-Concise Outro Bridge Cards (Max 5 Words)**:
   - Because the hosts already speak `"Coming up in the next clip..."` aloud during the final 10–20s Outro Teaser audio segment, the visual Outro Bridge Card (`bridge_text`) must NEVER repeat `"Coming up in Clip X..."` or display a long storyline sentence.
   - Instead, `bridge_text` must be a punchy **MAXIMUM 5-WORD** question or exclamation that hooks curiosity for the next concept (e.g., `"What is 8D Totality !"`, `"Why Four Division Algebras ?"`, `"How Do Quaternions Work ?"`).
   - All Gemini API prompts (`cast_tripartite_plan_with_gemini`, `get_gemini_default_prompt`, `get_gemini_episode_default_prompt`, `review_episode_bridges`) enforce `0`-based numbering, max 3-word Intro titles, and max 5-word Outro bridge prompts automatically.

## Clip Stitching & Acoustic Transition Rules (3-Stage Assembly Invariant)

Every DDMA social reel (`clips/<ep>-<num>.mp4`) is assembled in **3 deterministic stages** to guarantee crisp spoken word completion, zero voice attenuation over music stings, zero graphic bleed on Intro/Outro cards, and the signature delayed-echo host sign-off:

```
STAGE 1: Audio Body Assembly (`ddma.py cut` / `compile_segments`) — Sent to Mosaic
──────────────────────────────────────────────────────────────────────────────────
  [Seg 1: Punchline Hook Audio (10–20s)]
     • Start timestamp backed up via `resolve_acoustic_word_start` (16kHz PCM RMS
       onset scan + 30ms pre-attack cushion) so initial consonants ("Clip") are 100% spoken.
     • End timestamp & Seg 3 start resolved jointly via `resolve_segment_boundary`
       (minimum-RMS silence valley clamp) so trailing sibilants ("senses") are 100%
       spoken with strictly ZERO overlap or word repetition into Seg 3.
     • Followed by `0.2s` clean silence gap (`silence_before: 0.2s`).
          │
          ▼
  [Seg 2: Mid-Sting — Alternating Bluesy Vibes / Howling (5.5s)]
     • Plays at 100% volume for 3.5s, then fades out over 2.0s (`fade_out: 2.0s`).
     • Crossfades `1.0s` (`crossfade: 1.0s`) into Seg 3.
          │
          ▼
  [Seg 3: Core Deliberation + Spoken "Coming Up" Teaser Audio (~100–130s)]
     • Enters at `4.5s` of Seg 2 (after 1.0s of music fade-out) at 100% FULL VOLUME
       (strictly ZERO `afade=in` on human speech so every word is audible).
     • Start timestamp prioritized at/after the silence valley (`resolve_segment_boundary`)
       so the first word of Seg 3 belongs exclusively to Seg 3.
     • End timestamp extended via `resolve_segment_boundary` + `0.2s` silence gap.
          │
          ▼
  [Seg 4: Outro Conclusion Sting — deepDive-conclusion.mp3 (5.5s)]
     • Included in the Body MP3 sent to Mosaic by design so Mosaic renders closing
       motion graphics over the spoken host sign-off ("I am Satosha, and I am
       Satoshi" + conclusion music).

STAGE 2: Mosaic / Manim Body Render (`740×740`)
──────────────────────────────────────────────────────────────────────────────────
  • Stage 1 Body MP3 is muxed onto a 740×740 black canvas WITHOUT Intro or Outro
    cards and sent to Mosaic (so Mosaic graphics never overlay the billboard cards).

STAGE 3: Final Master Packaging (`ddma.py compile-clip` • `1080×1920` Vertical)
──────────────────────────────────────────────────────────────────────────────────
  • [Intro Card (1.5s, Pure #000000, dedicated soft title-card audio)] -> Hard
    concat into [Mosaic/Manim Body Video]
  • [Outro Bridge Card (5.0s, Pure #000000)] -> Stitched at the end with a 1.0s
    crossfade, repeating the final 5.0s of `deepDive-conclusion.mp3` ("I am Satosha,
    and I am Satoshi") to create a deliberate delayed-echo host signature over the
    pure black curiosity question card.
```

### Detailed Acoustic & Stitching Rules:
1. **Automated Word-Onset Attack & Sibilant-Tail Completion (`resolve_acoustic_word_start` & `resolve_acoustic_word_end`)**:
   - **Initial Consonant Attack (`resolve_acoustic_word_start`)**: Whisper word timestamps (`word["start"]`) frequently anchor to the voiced vowel core of a syllable, starting 50ms–130ms *after* initial unvoiced plosives or consonant clusters (`"Cl-"` in `"Clip"`, `"P"`, `"T"`, `"S"`, `"Th-"`). `resolve_acoustic_word_start` scans backward in 10ms frames across the 16kHz PCM waveform from `raw_start` into the preceding breath pause (`[max(0, raw_start - 0.35s, prev_word_end + 0.04s), raw_start]`) until RMS energy drops into background silence (`rms <= 0.0020`, `-54 dBFS`) and adds a `30ms` pre-attack cushion.
   - **Trailing Sibilant Decay (`resolve_acoustic_word_end`)**: Whisper word ends (`word["end"]`) frequently stop 80ms–200ms before trailing unvoiced sibilants/plosives (`"-es"` in `"senses"`, `"-t"`, `"-k"`, `"-s"`) finish decaying. `resolve_acoustic_word_end` inspects the 16kHz PCM waveform forward into the breath pause (`[raw_end, min(raw_end + 0.32s, next_word_start - 0.04s)]`), extending the cut until acoustic RMS energy drops below `-54 dBFS` (`rms <= 0.0020`) + `30ms` decay cushion (minimum `120ms` safety cushion).
   - Zero-duration Whisper cue artifacts (`start == end` on the next clip's `"Clip"` marker) are strictly excluded (`w["start"] < next_st - 0.02`) so the next clip's `"Clip N"` announcement never bleeds into the end of the current clip.
2. **Joint Acoustic Valley & Mutual-Exclusion Resolver (`resolve_segment_boundary`)**:
   - When two spoken sentences are separated by a tight conversational breath pause (e.g., `< 250ms` between Segment 1's last word `w1` and Segment 3's first word `w2`, or even `0.00s` in Whisper's JSON when a transition word like `"That"`, `"So"`, or `"Now"` immediately follows punctuation), extending `w1_end` forward and `w2_start` backward independently can cross the breath pause and cause the boundary word (`w2`) to repeat at the end of Segment 1 and the start of Segment 3.
   - **`resolve_segment_boundary(raw_w1_end, raw_w2_start, audio_path)`** eliminates boundary word repetition through a 3-step mutual-exclusion contract:
     1. **16kHz Minimum-RMS Silence Valley Scan**: Scans the PCM waveform across `[raw_w1_end - 0.02s, max(raw_w2_start + 0.02s, raw_w1_end + 0.32s)]` in `5ms` steps to pinpoint the exact acoustic silence valley (`valley_t`) separating the two words.
     2. **Second-Segment Word Priority (`w2_start`)**: Resolves `w2_start` first and clamps it at or after `valley_t` (`w2_start >= valley_t`), guaranteeing that the opening transition word of the second audio segment belongs **100% to Segment 3**.
     3. **Strict Non-Overlapping Clamp on First Segment (`w1_end`)**: Resolves `w1_end` with `next_word_start=w2_start` and strictly clamps `w1_end <= valley_t <= w2_start`. Furthermore, `ddma.py cut` honors pre-resolved segment boundaries without re-extending them, making segment overlap mathematically impossible.
3. **2.0s Music Fade-Out + 1.0s Full-Volume Speech Entry (Zero Speech Fade-In)**:
   - The Mid-Sting (`5.5s`) plays at full volume (`1.0`) from `0.0s -> 3.5s` and fades out over the final `2.0s` (`3.5s -> 5.5s`).
   - The succeeding speech segment (`Core Deliberation + Teaser`) enters `1.0s` before the music ends (at `4.5s`, when the music is already 50% attenuated) at **100% FULL VOLUME (`adelay` only, strictly NO `afade=t=in` on human speech)**.
4. **Dedicated Intro Card Audio Separation**:
   - The `1.5s` Intro Card uses a dedicated soft intro chime (`title-card-music.mp3` / `deepDive-soft-ok.mp3`) and NEVER steals the first `1.5s` of the clip's Mid-Sting (`Bluesy Vibes` / `Howling`).
5. **Delayed-Echo Host Signature on the Outro Card (By Design)**:
   - `deepDive-conclusion.mp3` (`"I am Satosha, and I am Satoshi"` + conclusion music) is baked into the end of the Stage 1 Body MP3 so Mosaic generates closing motion graphics over it.
   - When `compile-clip` stitches the `5.0s` Outro Bridge Card at the end of the body (`1.0s` crossfade), it intentionally replays the final `5.0s` (`deepDive-conclusion.mp3`), creating a delayed-echo repetition of the host names (`"I am Satosha, and I am Satoshi"`) over the pure `#000000` Outro Card. **Never strip `deepDive-conclusion.mp3` from the short reel body or suppress this echo.**

### Clip-Level Visual Purity (No Intra-Clip Mixing)
- **Engine Purity**: Clips NEVER mix engines internally. Each clip is authored **100% in Mosaic OR 100% in Manim**.
- **Active Master Routing**: In `plan.json`, each clip designates its `visual_source`: `"mosaic"` or `"manim"`. The Longform Compositor dynamically picks up whichever master is active.

### Dual-Track Assembly Protocol: Short Reels vs. Longform Audio/Video Podcast
1. **Track A: Short Reels (`clips/<ep>-<num>.mp4` • 740×740 / 9:16 for Social)**:
   - **Full Standalone Package**: `[Intro Card (1.5s)] -> [Punchline] -> [Mid-Sting: Bluesy/Howling (5.5s, 2.0s fade, 1.0s full-vol speech xfade)] -> [Deliberation + Teaser] -> [Outro-Sting in Body: deepDive-conclusion (5.5s)] -> [Outro Card + Echo Conclusion (5.0s)]`.
   - Pure, self-contained promotional reels for TikTok, Shorts, and Instagram.
2. **Track B: Longform Audio & Video Podcast (`podcast_<ep>.mp3` & `podcast_<ep>.mp4` • 1920×1080 Widescreen Master)**:
   - **Canonical Spoken-Cue Music Sting & Cut Rules (`review_podcast_with_gemini` / `podcast_edit.json`)**:
     - ✂️ **STRIP Redundant Spoken Welcome (`"Welcome to the deep dive"` / `"Today we are going on a massive deep dive"`)**: Automatically cut in `podcast_edit.json` (`cuts`) right at the start of `Clip 0` because `deepDive-strong.mp3` delivers the elaborate spoken show welcome.
     - 🎺 **Opener Sting (`deepDive-strong.mp3` • `16.71s`) in Opening Clip (`Clip 0`)**: Embedded right after the opening punchline hook in `Clip 0` (speaks `"Welcome to deepDive, I am Satosha, and I am Satoshi"` followed by ~10s of music, `0.2s` pre-gap, `2.0s` fade-out, `1.0s` full-volume speech entry).
     - 🎷🎸 **Inter-Clip Stings (`Bluesy Vibes` / `Howling` • `5.5s`) Between Every Clip**: Placed at the **end of every clip and right before the next clip starts** (immediately preceding the spoken `"Clip 1"`, `"Clip 2"`, ..., `"Clip N"` announcements), alternating `Bluesy Vibes` and `Howling` (`0.2s` pre-gap, `2.0s` fade-out, `1.0s` full-volume speech entry).
     - 🎹 **Finale Sting (`deepDive-conclusion.mp3` • `5.5s`) at the Very End**: Placed at the very end of the final clip right after the hosts' final words (speaks `"I am Satosha, and I am Satoshi"` followed by ~4s of closing music, fading out over the final `2.0s`).
     - ✂️ **STRIP all Intro Cards & Outro Cards on Video**: Keeps 1920×1080 video kinetic without graphic billboard interruptions between chapters.
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
