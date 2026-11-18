# Simplify the clip text dialog to captions-only

## Where

- `ddma/curator.html` — the clip text modal `#clipTextModalOverlay` at :1667.
  - Header :1670–1676: title `clipTextModalTitle` (:1672), subtitle `clipTextModalSubtitle` (:1673), close `closeClipTextModalBtn` (:1675).
  - Section 1 (script) :1680–1696: label "1. Spoken Script & Social Caption", word count `clipTextWordCount`, buttons `openExternalEditorBtn` (Vim/Notepad, :1688), `syncFromDiskBtn` (Sync Disk, :1689), `smartFormatClipTextBtn` (:1690), `aiPolishClipTextBtn` (:1691), `resetClipTextBtn` (:1692), `copyClipTextBtn` (:1693), textarea `clipTextInput` (:1696).
  - Section 2 (captions) :1699–1712: label "2. Burned Video Captions (3–6 words • ≤34 chars • lowercase • chained)" (:1702), stats `clipCaptionChunksStats` (:1706), `realignCaptionsFromScriptBtn` (Auto-Align, :1707), `whisperResyncCaptionsBtn` (Whisper Sync, :1708), `copyAssFileBtn` (Copy .ASS, :1709), textarea `clipCaptionChunksInput` (:1712).
  - Spec note box :1715–1717 (the 1080×1920 Vertical Render Spec paragraph).
  - Footer :1720–1724: `cancelClipTextBtn` (:1722), `saveClipTextBtn` (:1723, "Save Captions & Persist").
- `ddma/curator.html` — JS for the modal:
  - `updateCaptionChunksStats()` at :2745 (event count, max length, over-34 warning).
  - `requestServerAlignedCaptions()` at :2768 (server align call; `forceWhisper` flag).
  - `openClipTextModal()` at :2794 (populates script + caption boxes; sets `_initialModalTextVal`).
  - DOMContentLoaded listeners :2853–3180 (close, cancel, save, copy, reset, script input, chunks input, realign, whisper, copyAss, smartFormat, aiPolish, external editor, sync disk).
  - Save handler at :3131–3180 (reads script text, computes `topScriptEdited`, auto-aligns when the script changed and the chunks were not hand-edited, else parses chunks from the textarea, then `savePlanToServer()`).
  - `parseChunksFromTextarea()` at :2673 (parses `start -> end | text` lines, READS timestamps from the textarea, rewrites end times to enforce chaining), `formatChunksForTextarea()` at :2668.
  - Mosaic "Edit Clip Text" button at :1915 (`mosaicEditClipTextShortcutBtn`) + handler at :3036–3047, and the `returnToMosaicAfterTextSave` flag/flow at :2554, :2843–2844, :3143, :3175.

## Finding

The dialog was built when the script text doubled as social-media post copy. That job moved to the distribution agent, so the entire top pane (script editor + 6 buttons) is now unused. The user only ever edits caption TEXT; timestamps must never change. Three defects in the current dialog:

1. It is crowded: two panes, 9 buttons, a stats line, and a spec note — for a job that is one box + Save.
2. `parseChunksFromTextarea()` (:2673) READS timestamps from the textarea and rewrites them (it parses `start`/`end` and mutates end times to enforce chaining). A typo in a timestamp silently changes timing. The user wants timestamps locked — text-only edits.
3. The Whisper small.en Sync button (:1708) re-runs faster-whisper on the clip audio for fresh word timestamps. That is a re-transcription, which breaks the one-transcription rule (Issue 56: ONE transcription, done at the podcast stage; clips never re-transcribe). The captions already come from the base transcription; Auto-Align re-chunks from the existing timestamps. Whisper Sync is redundant.
4. The Mosaic modal's "Edit Clip Text" button (:1915) opens this dialog to edit the script. With the script editor gone, that button has nothing to open. (The Mosaic prompt itself stays directly editable in its own textarea, `mosaicPromptTextarea` at :1918.)

## Fix

Replace the dialog with a single captions box. Text-only edits; timestamps are never read from the textarea and never written.

1. Remove Section 1 (script) from the modal HTML (:1680–1696): the label, the word count, all 6 buttons (Vim/Notepad, Sync Disk, Smart Format, AI Polish, Reset, Copy Text), and the `clipTextInput` textarea.
2. In Section 2: remove the stats span (:1706), the Auto-Align button (:1707), the Whisper Sync button (:1708), and the Copy .ASS button (:1709). Keep only the caption textarea (:1712). Simplify the label to "Burned Video Captions" (drop the "2." and the "3–6 words • ≤34 chars • lowercase • chained" parenthetical — no length limit is enforced or warned about; nobody cares if a word is curtailed).
3. Remove the spec note box (:1715–1717).
4. Update the modal title (:1672) to "CLIP N: Burned Captions" and the subtitle (:1673) to caption-only text (drop the script / ASS / 34-char mention).
5. Footer: keep Cancel (:1722) and Save (:1723, label "Save"). Add a Revert button that restores the textarea to the last SAVED caption chunks (re-format `clip.caption_chunks` via `formatChunksForTextarea`), discarding unsaved edits. Revert restores the last saved state, NOT the raw Whisper transcript (the old Reset behaviour is gone with the script pane).
6. JS — `openClipTextModal()` (:2794): populate ONLY the caption textarea from `clip.caption_chunks`. Remove the script population, the `_initialModalTextVal` tracking, and the `_captionChunksManuallyEdited` flag (no auto-align anymore).
7. JS — Save handler (:3131): replace the script / auto-align logic with a text-only save:
   - Read the textarea lines.
   - For each line i, take the text after the first `|` (if a line has no `|`, the whole line is the text). Normalize it exactly as the current parser does (collapse whitespace to single spaces, trim, lowercase).
   - Pair that text with the ORIGINAL `clip.caption_chunks[i]` start/end, by line position. Timestamps from the textarea are IGNORED entirely — never parsed, never written.
   - Lines beyond the original chunk count are ignored. If there are fewer lines than chunks, the missing chunks keep their original text.
   - Set `clip.caption_chunks` to the updated chunks and call `savePlanToServer()`.
   - Do NOT call `requestServerAlignedCaptions`. Do NOT touch `clip.text` (the stored script text stays as-is; the captions are what get burned).
8. JS — remove the listeners for the removed buttons (Vim/Notepad, Sync Disk, Smart Format, AI Polish, Reset, Copy Text, Auto-Align, Whisper Sync, Copy .ASS). Remove `updateCaptionChunksStats()` (:2745) and `requestServerAlignedCaptions()` (:2768) ONLY if verified to have no other callers (they are used only by this dialog — confirm before deleting).
9. JS — remove the Mosaic "Edit Clip Text" button (:1915) and its handler (:3036–3047), and the `returnToMosaicAfterTextSave` flag/flow (:2554, :2843–2844, :3143, :3175). Reason: it exists only to open the script editor. The Mosaic prompt stays directly editable in its own textarea.
10. Do NOT delete shared helpers (`getClipSpokenText` :2568, `smartFormatTranscript` :2594, `formatChunksForTextarea` :2668, `parseChunksFromTextarea` :2673) — the Save path no longer calls `parseChunksFromTextarea`, but leave the functions in place. Dead-code removal is out of scope; keep the change minimal and safe.

## Verify

1. Open the clip 14 dialog: ONE box (captions) only. Title "CLIP 14: Burned Captions". Buttons Save / Revert / Cancel (+ the X close). No script pane, no stats line, no spec note, no Auto-Align / Whisper / Copy .ASS buttons.
2. Edit a caption text line (change a word), Save, reopen: the new text is there, and the start/end timestamps are IDENTICAL to before (compare against the pre-edit plan).
3. Deliberately change a TIMESTAMP in the textarea (edit a start time), Save, reopen: the timestamp is UNCHANGED (the textarea timestamp was ignored) and only the text changed.
4. Edit a caption text, click Revert WITHOUT saving: the textarea returns to the last saved text.
5. Edit a caption text, click Cancel: nothing is saved (reopen shows the original text).
6. The Mosaic modal no longer has the "Edit Clip Text" button; the Mosaic prompt textarea is still directly editable.
7. Compile clip 14 (or an already-published clip, e.g. 249-8) and confirm the burned captions match the edited text and the caption timing is unchanged (compare the compiled video's caption timing / ASS against the plan).
8. Run the existing test suites and report the counts (`test_compile_scope.py`, `test_canonical_audio_compile.py`, `test_plan_clip0_title.py`, `test_mosaic_mux_integrity.py`, `test_curator.js` — do NOT run TEST 20 without first confirming its `finally` restore at `test_curator.js:1108` is intact).
9. Do NOT publish any clip as part of this verify. Do NOT trigger a Mosaic run. Do NOT commit or push (fan-out is a separate human step).

## Guardrails

- deepDive only (`ddma/curator.html`). No Mosaic runs. No keys in git. No commit/push (fan-out is a separate human step).
- Scoped change only: the clip text modal in `curator.html` + the Mosaic "Edit Clip Text" button that opens it. Do not refactor, do not touch the compile, the plan generation, the Mosaic modal's prompt textarea, or any other dialog.
- Report PASS/FAIL per verify step, then STOP with a full summary.
