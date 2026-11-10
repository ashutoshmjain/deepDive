# DeepDive Pipeline Failure Contract & Error Handling Invariants

**Document Owner**: Ashutosh & Antigravity  
**Location**: `deepDive/FAILURE_CONTRACT.md`  

---

## 1. Core Principle: Fail Loud, Never Swallow

In headless and Docker container operations, human operators cannot inspect a GUI to notice that a job stalled or failed silently. Every pipeline step must either succeed completely or fail loudly with clear telemetry.

### Non-Negotiable Invariants

1. **No Silent Swallowing on Write Paths**:
   - Every file write, cache save, metadata sync, or plan mutation must catch exceptions and either bubble them up or log them loudly with full error context.
   - Bare `except:` or `except Exception: pass` on file I/O or state mutations is strictly forbidden.

2. **Async Operations Contract (HTTP 202 / Job Polling)**:
   - Any long-running or external API operation (e.g. `/export-to-mosaic`, Manim compilation) must NEVER return HTTP 200 with an empty body while spawning background threads that fail untracked.
   - The endpoint must return an initial tracking payload containing:
     - `success`: `true`
     - `job_id`: Unique identifier (e.g., `<project_id>_<clip_num>`)
     - `status_url`: Endpoint to query status (e.g., `/get-mosaic-status?id=<project_id>&num=<clip_num>`)
   - The status endpoint must return explicit states: `"starting"`, `"running"`, `"completed"`, or `"failed"`, with `error` populated if failed.

3. **Gating & Lock Refusals (HTTP 400 / 403 / 500)**:
   - When a precondition fails (e.g., clip is unlocked, zero clips found for combination, missing canonical audio source), the server must return an explicit HTTP error code (400, 403, or 500) with a JSON error payload explaining the exact failure reason.

4. **Canonical Audio Integrity**:
   - DDMA and Curator must refuse to cut clips or run whisper alignment from assembled podcast files (`podcast_<ep>.mp3`). If only a mastered podcast MP3 is present, the pipeline must raise an error requiring the continuous raw audio (`.m4a` / `.wav`).
