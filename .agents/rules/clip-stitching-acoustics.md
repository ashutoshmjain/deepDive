---
trigger: model_decision
description: "3-stage clip assembly, acoustic word-boundary resolvers, and the short-reel vs longform dual-track rules — read when cutting, muxing, compiling, or verifying clip audio."
---


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
