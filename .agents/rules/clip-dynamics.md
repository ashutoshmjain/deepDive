---
trigger: model_decision
description: "Clip numbering, intro/outro card invariants, and the tripartite spoken pattern — read when planning, numbering, titling, or bridging clips."
---


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
