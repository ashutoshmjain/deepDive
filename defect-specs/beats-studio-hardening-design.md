# Beats Studio Hardening — Design Document (Spec B)

**Status:** Design only (no code changes).  
**Base state:** Post-Spec B1 (`deepDive` `8835c8c7`, `mdIngest` `3e275e1`).  
**Scope:** Realizes the user's 2026-11-20 architectural decisions on top of B1's per-episode beats directory (`DD_HUB_ROOT/episodes/<ep>/beats/`), read-path purity, byte-stable plan saves, and static navigation whitelist.

---

## 1. Decisions Summary Table (D1–D7)

| ID | Topic | Recommendation | Alternatives Considered | Decision Waiting on User |
|----|-------|----------------|------------------------|--------------------------|
| **D1** | Storage Map & Canonical Copies | Hub-first (`DD_HUB_ROOT/episodes/<ep>/beats/`) for per-episode beats/meta/renders; `ddma/personal_beats/` (excluded from `mdIngest` via `.gitignore` + `check_fanout.py` skip) for personal beats; `dd_hub/episodes/<ep>/plan.json` canonical, `ddma/projects/<ep>/plan.json` & `ddma/docs/episodes/<ep>/plan.json` derived caches. | (a) Keep working plans in `ddma/projects/<ep>/plan.json` as co-canonical; (b) Store personal beats in `dd_hub` only without repo backup. | Approve canonical status of `dd_hub/episodes/<ep>/plan.json` and `ddma/personal_beats/` deepDive-only placement. |
| **D2** | Personal Beats | Save unit = self-contained JSON + Python bundle (`class_code`, `title`, `tags`, `archetype_id`, `target_duration`, `spoken_text`, `provenance`). Instantiate by inserting/replacing a beat in the episode's O2 `clip_XX_gemini_scenes.py` + `clip_XX_meta.json`, adapting `duration` proportionally and marking the clip's storyboard cache as `custom_edited`. | (a) Reference beats by pointer into source episode (fragile across episode edits); (b) Store only prompt directive and re-synthesize via Gemini on instantiate (slow, non-deterministic). | Confirm save unit fields and whether duration adaptation on instantiate should scale `self.wait()` or re-time evenly across the clip. |
| **D3** | Beats Studio Layout | Realize 3-column workspace below top episode bar: Left = Clip/Chapter list (`#lf-chapter-strip` + engine badge); Middle = Clip-level audio/video player + Beat Scrubber & Editor below; Right = Personal Beats drawer (save/browse/instantiate). Keep Workspace, cockpit, and Cutroom links via `workspace-link.js` (Docs already removed in B1). | (a) Keep 16:9 full-episode player dominant at top; (b) Tabbed view switching between Timeline and Personal Beats. | Approve 3-pane layout proportions, clip-level vs full-master playback toggle, and keeping `cockpit` + `Cutroom` alongside `Workspace` in the top bar. |
| **D4** | Template Cache (`generated_archetypes.json`) | **Present options only (user decides):** Recommend **(c) mdIngest ships a small generic starter set (e.g. 3–5 clean primitives)** while `deepDive` retains the full 22-template library, OR **(a) keep mirrored** if starter size (~22) is acceptable. | (a) Stays mirrored in both repos as today; (b) `deepDive`-only, `mdIngest` ships `{}`; (c) `mdIngest` ships 3–5 generic starter templates. | **User must choose (a), (b), or (c)** for `ddma/generated_archetypes.json` in `mdIngest`. |
| **D5** | Per-Clip Engine Choice | Standardize on `visual_source: "mosaic" \| "manim"` on each clip entry in `plan.json` (default `"mosaic"` for new clips; `"manim"` only when explicitly selected or storyboarded). Retriggering either engine updates `visual_source` and re-runs assembly via `get_longform_all_chapter_mappings()`. | (a) Introduce a separate `engine` field alongside `visual_source` (risks drift); (b) Default all longform chapters to `"manim"`. | Confirm reusing `visual_source` (`"mosaic" \| "manim"`) rather than adding a redundant `engine` key, and confirm `"mosaic"` as default. |
| **D6** | Episode 250 Proving Run | 10-clip subset (5 Mosaic baseline, 5 Manim beats) with explicit producer time logging, blind/rubric explanatory-quality check, and hard exit gate: **NOT WORTH IT** if producer time > 2× Mosaic baseline or Manim failure rate > 20%, triggering clean fallback to Mosaic-only longform. | (a) Full 23-clip Manim run on ep 250 (high upfront cost before gate); (b) Purely qualitative judgment without time/failure thresholds. | Approve 5+5 clip split on ep 250 and quantitative WORTH IT / NOT WORTH IT thresholds. |
| **D7** | Risks & Unknowns | Enforce strict read/write separation at API boundary (GETs never mutate tracked files or plan state; explicit POSTs only), cache Gemini storyboards per clip, and bound Manim render concurrency. | Rely on ad-hoc per-handler fixes. | None (architectural invariant; informs implementation specs). |

---

## 2. Verified System Mechanics (Code Citations)

Every claim below was verified against the post-B1 `deepDive` codebase:

- **Local transcription:** `ingest/server.py:966` (`run_faster_whisper_transcription`) and `ddma/ddma.py:1728` (`get_faster_whisper_model`) run `faster-whisper` (`WhisperModel`) locally once per episode at word-level granularity; audio is not sent to Gemini.
- **Per-clip storyboarding:** `ddma/manim_infographic_engine.py:68` (`generate_pedagogical_storyboard`) takes clip caption chunks and `body_duration`, produces scene specs via Gemini, and caches them on the clip (`t_clip["infographic_scenes"]` and `get_storyboard_filepath` in `ddma/scratch/run_curator.py:4644-4666`).
- **Template cache + JIT auto-coder:** `ddma/generated_archetypes.json` contains **22** parameterized templates (`tin_can_intercom`, `coal_locomotive_burner`, etc.). On a cache miss or beat edit, `ddma/archetype_studio.py:604-669` (`update_single_scene_with_ai`) calls Gemini (`PRIMARY_MODELS` at `ddma/archetype_studio.py:19-23`) with local fallback `synthesize_figurative_manim_class` (`ddma/archetype_studio.py:446`).
- **Beat editing (post-B1):** `ddma/archetype_studio.py:625-780` (`update_single_scene_with_ai`) rewrites one `Scene` class (default `duration=7.5`) in the per-episode O2 file `_episode_beats_dir(ep)/clip_XX_gemini_scenes.py`, compiles it via `compile_single_scene` (`ddma/archetype_studio.py:395`) at `740,740` @ `15` fps into `<O2>/media/videos/clip_XX_gemini_scenes/740p15/<Class>.mp4`, and updates `<O2>/clip_XX_meta.json`.
- **Per-episode O2 storage & read-purity (post-B1):** `ddma/archetype_studio.py:31-72` resolves `_episode_beats_dir(ep)` to `DD_HUB_ROOT/episodes/<ep>/beats/` (fallback `ddma/cache/beats/<ep>/`, git-ignored in both repos). `ddma/archetypes/` is read-only fallback reference material; no GET in `ddma/beats_server.py:171-265` writes inside the tracked repo tree.
- **Plan saves (post-B1):** `ddma/scratch/run_curator.py:287-337` (`save_plan`) writes hub-first to `dd_hub/episodes/<ep>/plan.json` + `plan.meta.json` (with `plan_rev` optimistic concurrency), then local `ddma/projects/episode_<ep>/plan.json`, `ddma/plan.json`, and `ddma/docs/episodes/<ep>/plan.json`. `_preserve_number_types` (`ddma/scratch/run_curator.py:184-203`) prevents JS `JSON.stringify` `0.0 -> 0` diff churn.

---

## 3. D1 — Storage Map

| Artifact Type | `deepDive` Location | `mdIngest` Location | `dd_hub` Workspace (`episodes/<N>/`) | Local-Only / Ignored | Mirroring & Exclusion Mechanism |
|---------------|---------------------|---------------------|---------------------------------------|----------------------|---------------------------------|
| **Engine code** (`archetype_studio.py`, `beats_server.py`, `manim_infographic_engine.py`, `longform_video_engine.py`, `render_longform_parallel.py`) | `ddma/*.py` | `ddma/*.py` | — | — | Mirrored byte-identical by `scripts/check_fanout.py:37-41` (`mirror_tree_files("ddma")`). |
| **Beats Studio UI** (`beats.html`, `workspace-link.js`) | `ddma/beats.html`, `ddma/workspace-link.js` | `ddma/beats.html`, `ddma/workspace-link.js` | — | — | Mirrored byte-identical by `scripts/check_fanout.py`. |
| **Per-episode scene code & beat meta** (`clip_XX_gemini_scenes.py`, `clip_XX_meta.json`) | Read-only starter reference in `ddma/archetypes/` | Read-only starter reference in `ddma/archetypes/` | **Primary (O2):** `episodes/<N>/beats/` | Fallback when `DD_HUB_ROOT` unset: `ddma/cache/beats/<N>/` (git-ignored) | Post-B1 `_episode_beats_dir(ep)` (`archetype_studio.py:42`). Never written to `ddma/archetypes/` at runtime. |
| **Template cache** (`generated_archetypes.json`) | `ddma/generated_archetypes.json` | Pending D4 user decision (currently mirrored) | — | — | Currently mirrored via `check_fanout.py`. If D4 chooses (b) or (c), add `generated_archetypes.json` to `SKIP_FILES` in `check_fanout.py` or maintain separate `mdIngest` template. |
| **Personal beats** (user-saved individual beats) | `ddma/personal_beats/<beat_id>.json` + `.py` (or index `index.json`) | **Never present** | Optional vault/hub backup: `dd_hub/personal_beats/` | — | **Excluded from `mdIngest`:** `check_fanout.py:25-39` enumerates pairs from `MDINGEST / "ddma"` (`mirror_tree_files("ddma")`), NOT from `deepDive`. Because `ddma/personal_beats/` does not exist in `mdIngest`, `check_fanout.py` ignores it; add `ddma/personal_beats/` to `mdIngest/.gitignore` and a guard in `check_fanout.py` (`SKIP_DIRS` / explicit assertion that `personal_beats` never enters `mdIngest`). |
| **Rendered beat MP4s** (`740p15/*.mp4`) | Legacy read-only fallback: `media/videos/` | Never committed (`*.mp4` ignored) | **Primary (O2):** `episodes/<N>/beats/media/videos/clip_XX_gemini_scenes/740p15/` | `ddma/cache/beats/<N>/media/` when hub unset | Written by `compile_single_scene` (`archetype_studio.py:395`), resolved by `_resolve_beat_mp4_path` (`archetype_studio.py:67`). |
| **Per-clip engine choice** (`visual_source: "mosaic" \| "manim"`) | Cached in `ddma/projects/episode_<N>/plan.json` | Never present | **Canonical:** `episodes/<N>/plan.json` | — | Consumed by `get_longform_all_chapter_mappings` (`archetype_studio.py:1182-1201`). |
| **Working plan copies** (`plan.json`) | **Derived caches:** `ddma/projects/episode_<N>/plan.json`, `ddma/plan.json`, `ddma/docs/episodes/<N>/plan.json`, `src/ddma/docs/episodes/<N>/plan.json` | Never present | **Canonical:** `episodes/<N>/plan.json` + `plan.meta.json` | — | `save_plan` (`run_curator.py:287`) writes hub first with `plan_rev` check, then updates derived local caches; fresh clones trust `dd_hub` first via `load_plan` (`run_curator.py:240-285`). |

---

## 4. D2 — Personal Beats

- **Save unit:** A self-contained directory or pair under `ddma/personal_beats/` (mirrored/backed up to `dd_hub/personal_beats/` if configured):
  - Metadata JSON (`<slug>_<short_hash>.json`): `id`, `title`, `tags` (list of strings), `archetype_id` (optional), `target_duration` (float seconds), `spoken_text` (string), `class_name` (original), `provenance` (`{"ep": "248", "clip_num": 1, "beat_index": 3, "saved_at": "<ISO8601>"}`), and `py_file` (`<slug>_<short_hash>.py`).
  - Scene Python file (`<slug>_<short_hash>.py`): standalone `class <SceneName>(Scene):` block plus any local helper shims needed so it has zero cross-episode dependencies.
- **Save flow (from Beats Studio):**
  1. Producer selects a beat in the Middle Pane and clicks **Save to Personal Beats** (prompts for `title` and comma-separated `tags`).
  2. `POST /api/beats/personal/save` sends `{ep, clip_num, beat_index, class_name, title, tags}`.
  3. Server reads the beat's live `Scene` code from `_resolve_clip_py_path(clip_num, ep)` and metadata from `_resolve_clip_meta_path(clip_num, ep)`, writes the self-contained bundle to `ddma/personal_beats/` (and `dd_hub/personal_beats/` if reachable), and returns the saved item.
- **Browse flow:**
  - `GET /api/beats/personal/list?q=<filter>` returns all saved personal beats (title, tags, `target_duration`, `provenance`, preview code snippet). Rendered in the Right Pane with tag/text search.
- **Instantiate flow:**
  1. Producer picks a target clip & beat position (replace beat *k* or insert after beat *k*) in the Middle Pane and clicks **Insert / Apply** on a Personal Beat card in the Right Pane.
  2. `POST /api/beats/personal/instantiate` copies/renames the saved `Scene` class into the target episode's O2 file (`_episode_beats_dir(ep)/clip_XX_gemini_scenes.py`) as `Scene<clip>_<idx>_<suffix>`.
  3. **Duration mismatch handling:** Scale `self.wait(...)` (or append/trim trailing `self.wait(delta)` so the visual persists) to match the target beat's `duration` (e.g., `eff_body_dur / n_scenes` in `ensure_clip_meta`, `archetype_studio.py:194`), rather than distorting animation `run_time`s below 0.3s. Recompile that single scene into O2 `media/`.
  4. **Storyboard cache interaction:** Mark the beat entry in O2 `clip_XX_meta.json` with `"source": "personal_beat"` and `"personal_beat_id": "<id>"`, and set `t_clip["storyboard_custom_edited"] = True` (or preserve O2 `clip_XX_gemini_scenes.py` precedence) so automatic storyboard regeneration does not silently overwrite producer-placed personal beats.

---

## 5. D3 — Beats Studio Layout

Realizing user decision 5 (`deepDive/defect-specs/deepdive-spec-b-beats-studio-hardening.md:73-76`):

- **Top Bar (`header.app-topbar`):**
  - Left: Brand wordmark (`SHUTRI BEATS`), Episode Selector (`#beats-ep` + `Load` button -> `GET /api/beats/index?ep=<ep>`).
  - Right (post-B1): `Workspace` (`data-workspace-home`), `cockpit` (`data-workspace-home data-workspace-page="cockpit.html"`), `Cutroom` (`data-cutroom-home data-cutroom-page="curator.html"`). Docs link is removed (B1).
- **3-Pane Workspace Grid:**
  - **Left Pane — Clips / Chapters (`#lf-chapter-strip`):**
    - Lists all clips (`Part 0..N`) from `GET /api/beats/index?ep=<ep>`.
    - Each clip row/pill shows: clip number, title, duration, beat count, and engine badge (`Mosaic` vs `Manim` from `visual_source`).
    - Actions: Click to select active clip (`selectLfChapter` -> `GET /api/beats/beats?ep=<ep>&clip_num=<c>`); per-clip engine toggle (`Mosaic` / `Manim` -> new `POST /api/beats/set_engine`, D5).
  - **Middle Pane — Audio Segment, Clip Video Playback & Beat Editor:**
    - *Upper Middle:* Clip-level video/audio playback to check flow — toggle between **Clip Preview** (short clip MP4 or audio segment from `dd_hub/episodes/<ep>/`) and **Longform Master** (`/api/beats/video?ep=<ep>` seeked to `chapter_start..chapter_end`), plus the existing `740×740` isolated beat preview (`#lf-beat-preview-overlay`, `/api/beats/beat_video?ep=<ep>&clip_num=<c>&class_name=<cls>`), `Mosaic Retrigger (explicit)` (`POST /api/beats/mosaic_retry`), and `Patch Active Chapter (~8s)` (`POST /api/beats/patch`).
    - *Lower Middle:* Micro-beat scrubber (`#lf-beat-pill-strip`), spoken dialogue card (`#lf-beat-spoken-text`), producer directive editor (`#lf-beat-directive-input` -> `POST /api/beats/update_beat`), collapsible Manim Python editor (`#lf-beat-code-textarea`), and **Save to Personal Beats** button (`POST /api/beats/personal/save`, D2).
  - **Right Pane — Personal Beats Selection:**
    - Search/tag filter input + scrollable list of saved Personal Beats (`GET /api/beats/personal/list`).
    - Each card shows title, tags, `target_duration`, provenance (`ep/clip/beat`), and **Apply to Beat** / **Insert After** (`POST /api/beats/personal/instantiate`).
    - Note: In `mdIngest` (where `personal_beats/` is empty/absent), the Right Pane renders an empty-state message ("No personal beats saved yet — save any beat from the editor") with zero shipped library items.
- **Obsolete in current `beats.html`:**
  - Hardcoded `"23 Parts"` / `"54:14"` placeholder labels (`beats.html:50, 78`) — must populate dynamically from `lfTimelineIndex`.
  - `"Updates Shared Longform + Cutroom Short Library"` label (`beats.html:132`) — update to reflect per-episode O2 storage (`episodes/<ep>/beats/`).
- **New endpoints needed (not yet implemented):**
  - `GET /api/beats/personal/list`, `POST /api/beats/personal/save`, `POST /api/beats/personal/instantiate`
  - `POST /api/beats/set_engine` (updates `visual_source` in `plan.json` via `save_plan`)
  - `GET /api/beats/clip_media?ep=<ep>&clip_num=<c>` (serves clip-level audio/video segment for middle-pane flow check)

---

## 6. D4 — Template Cache Disposition (`ddma/generated_archetypes.json`)

User decision required. Currently `ddma/generated_archetypes.json` (22 templates) is mirrored identically in `deepDive` and `mdIngest`.

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **(a) Stay mirrored as today** | Keep all 22 templates in both `deepDive` and `mdIngest`. | Zero fan-out change; new `mdIngest` users get instant local-first hits for common metaphors without Gemini calls. | Ships `deepDive`-flavored templates (`tin_can_intercom`, etc.) in the clean upstream repo; blurs "capability-only" boundary. |
| **(b) `deepDive`-only (`mdIngest` ships `{}`)** | Remove templates from `mdIngest/ddma/generated_archetypes.json` (ship `{}`). | Cleanest separation of engine vs. production material. | Every first-time `mdIngest` user hits Gemini JIT on 100% of beats; slower and costs API quota on first run. |
| **(c) `mdIngest` ships small generic starter set (3–5 templates)** | Keep 22 in `deepDive`; ship 3–5 generic diagrammatic templates (e.g., timeline, comparison split, flow diagram) in `mdIngest`. | Proves local-first cache-hit path out of the box for new users without shipping `deepDive`-specific metaphors. | Requires splitting `generated_archetypes.json` out of byte-identical `check_fanout.py` mirroring (add to `SKIP_FILES` or separate `starter_archetypes.json`). |

**Recommendation:** **(c)** if maintaining a separate 3–5 item starter file is acceptable, otherwise **(a)** if simplicity of byte-identical fan-out outweighs template purity. **Waiting on user choice: (a), (b), or (c).**

---

## 7. D5 — Per-Clip Engine Choice

- **Field & values:** Reuse existing `visual_source` on each clip object in `plan.json` (`"mosaic" | "manim"`), avoiding a duplicate `engine` key.
- **Who sets it & default:**
  - Default for newly planned clips: `"mosaic"` (reliable, fast, zero Manim render risk).
  - Set to `"manim"` explicitly by the producer via Beats Studio (`POST /api/beats/set_engine`) or Curator (`run_curator.py:4671-4672` when Manim infographic is compiled).
- **Retrigger path:**
  - *Mosaic -> Manim:* Producer switches clip to `manim` in Beats Studio (or triggers Manim compile in Cutroom), which runs storyboard + `compile_single_scene` into O2 `episodes/<ep>/beats/` and sets `visual_source = "manim"` via `save_plan`.
  - *Manim -> Mosaic:* Producer clicks `Mosaic Retrigger (explicit)` (`beats.html:611`, `POST /api/beats/mosaic_retry` -> Curator `/export-to-mosaic`), which starts a Mosaic run and sets `visual_source = "mosaic"` on completion.
- **Longform assembly consumption:** `get_longform_all_chapter_mappings` (`archetype_studio.py:1194-1198`) and `get_longform_scene_intervals` (`archetype_studio.py:1236-1266`) already branch on `clip.get("visual_source") == "mosaic"`: if `"mosaic"` and `resolve_mosaic_body()` finds the run/compiled MP4, it slices the Mosaic body by the beat windows; otherwise it renders the Manim beat MP4s from O2 `media/`.

---

## 8. D6 — Episode 250 Proving Run

- **Entry criteria:**
  1. Spec B1 deployed and verified (clean git status after Beats Studio reads/edits).
  2. Episode 250 transcribed (`transcription.json`), planned (`plan.json`), and edited (`podcast_edit.json`) in `dd_hub`.
  3. At least 10 clips identified (5 Mosaic-suited, 5 explanation-heavy where Mosaic feels too coarse).
- **Run shape:**
  - Select **10 clips** from Episode 250: **5 clips** produced with `visual_source: "mosaic"` (control baseline) and **5 clips** produced with `visual_source: "manim"` (beats treatment: storyboard + O2 beat editing + `render_longform_parallel.py --patch`).
  - Log wall-clock producer time per clip (from storyboard/generation through final acceptable preview) and Gemini/Manim failure count.
- **Exit criteria:**
  - **WORTH IT** (continue investing in Beats Studio):
    1. Producer time per Manim clip ≤ **1.5×** Mosaic baseline (or ≤ 15 min/clip).
    2. Explanatory-quality rubric: on blind side-by-side playback of the 5 Manim chapters vs. 5 Mosaic chapters, producer/reviewer rates Manim clearly superior for conceptual clarity on ≥ **4/5** chapters.
    3. Compilation/synthesis failure rate ≤ **10%** of beats (≤ 1 retry needed per 10 beats).
  - **NOT WORTH IT** (exit ramp):
    1. Producer time > **2.0×** Mosaic baseline, OR explanatory quality wins on < **3/5** chapters, OR Manim/Gemini failure rate > **20%**.
- **Concrete fallback if NOT WORTH IT:**
  - Keep `visual_source: "mosaic"` as the permanent default for all longform chapters and short reels.
  - Freeze `beats_server.py`, `beats.html`, and `archetype_studio.py` as-is (functional for legacy ep 248 and manual inspection, no further feature specs).
  - Do not build Personal Beats (D2) or the 3-pane redesign (D3); close Spec B's implementation queue after the proving run.

---

## 9. D7 — Risks and Unknowns

1. **Read side-effects & plan-save churn (generalized beyond B1):**
   - *Post-B1 baseline:* GETs in `beats_server.py` never write to tracked repo files, and `_preserve_number_types` in `run_curator.py` prevents `0.0 -> 0` diff churn on `/save-plan`.
   - *Remaining risk:* `ensure_clip_meta` (`archetype_studio.py:139`) still writes `clip_XX_meta.json` to O2 (`DD_HUB_ROOT/episodes/<ep>/beats/`) during `GET /api/beats/index` and `GET /api/beats/beats`. While outside git, concurrent GETs could race on O2 meta files, and non-`/save-plan` writers (`ddma.py:214` `save_plan_file`, `run_curator.py:4676`) still write derived plan copies without `_preserve_number_types`.
   - *Hardening rule:* Move `_preserve_number_types` into `save_plan` / `save_plan_file` directly, and make `ensure_clip_meta` pure in-memory on GETs (only persisting `clip_XX_meta.json` on explicit POSTs or a dedicated `POST /api/beats/materialize` endpoint).
2. **Gemini cost & latency at longform scale:**
   - Storyboarding 23 clips = 23 Gemini calls; regenerating beats at ~12–18 beats/clip = up to ~350 beats. Caching storyboards per clip (`storyboard_custom_edited` flag) and local-first template hits (`generated_archetypes.json`) bound cost; rate-limit retries with exponential backoff are needed if batch-generating a full episode.
3. **Manim render time & environment parity:**
   - Single beat render is ~3s locally when `manim` is installed, but WSL/clean-room environments without `manim` cannot compile beats (`No module named manim`). Full-episode re-renders of 350+ beats take ~15–20 minutes even when parallelized; incremental `--patch <clip>` (`beats_server.py:322`) must remain the primary inner loop.

---

## 10. Implementation-Spec Outline (Dependency Order)

1. **Spec B2 — Read-Pure Materialization & Shared Plan-Save Normalization:** Make `ensure_clip_meta` pure in-memory on GETs (explicit POST materialize) and move `_preserve_number_types` into `save_plan` + `save_plan_file`.
2. **Spec B3 — Per-Clip Engine Toggle & Clip-Level Playback:** Add `POST /api/beats/set_engine` (`visual_source`) and `GET /api/beats/clip_media`, and wire dynamic chapter/duration headers in `beats.html`.
3. **Spec B4 — Episode 250 Proving Run (Gate):** Execute the 5+5 Mosaic-vs-Manim proving run on Episode 250 and evaluate WORTH IT vs. NOT WORTH IT before building D2/D3.
4. **Spec B5 — Personal Beats Storage & API (gated on B4 WORTH IT):** Implement `ddma/personal_beats/` schema, `check_fanout.py` exclusion, and `/api/beats/personal/{list,save,instantiate}` endpoints.
5. **Spec B6 — Beats Studio 3-Pane Layout (gated on B4 WORTH IT):** Realize the 3-pane UI in `beats.html` (clips left, audio/video + beat editor middle, personal beats right) and apply the D4 `generated_archetypes.json` disposition.
