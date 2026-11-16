# DeepDive with Gemini: Research & Automation

**[Live Site: deepdive.shutri.com](https://deepdive.shutri.com)**

This repository is the **reference implementation** of a full media creation and distribution pipeline — research becomes an article, the article becomes a podcast, the podcast becomes clips and longform video, and the personal AI assistant Meta Muse distributes it all. See it live at [deepdive.shutri.com](https://deepdive.shutri.com).

---

## Creation: mdIngest + DDMA

Creation is handled through two open-source utilities:

* **[mdIngest](https://github.com/ashutoshmjain/mdIngest)** — publishes math-heavy research to the web, using mdBook as the core engine. It implements an opinionated framework for promoting research: drafts start in the mempool, move into the template, and are sealed into blocks. It transcribes the audio for each research paper (henceforth called an *episode*) and turns it into a deepDive podcast using NotebookLM deepDive audio.
* **[DDMA](https://github.com/ashutoshmjain/ddma)** — cuts the podcast into fully editable clips, uses Mosaic for motion graphics, and finally compiles the clips into longform video.

---

## Distribution: Meta Muse (personal AI assistant)

Distribution is handled through the personal AI assistant **Meta Muse** — Muse is the distribution layer. Once a clip or podcast episode is finished, Muse publishes it across platforms: clips go to Nostr first (video-first, with a SHA-256 hash proving the video), then to Instagram Reels, YouTube Shorts, and TikTok; X and LinkedIn go out as link posts (X carries the YouTube Short link, LinkedIn carries the Instagram reel link), posted automatically once those links exist. The audio podcast goes to Spotify only (its RSS feed syndicates Apple Podcasts, YouTube Music, Fountain, and Podcast 2.0). Nothing posts without the human's per-item approval — Muse prepares and verifies each post, the human approves it, and only then does it go out.

---

## The loop: back into the publication

The reels created by DDMA and the podcast links are baked back into the research web publication at [deepdive.shutri.com](https://deepdive.shutri.com) — each episode page carries its clips and its Listen links. Reels are distributed to Instagram, YouTube Shorts, TikTok, and Nostr; longform video goes to YouTube, TikTok, and Spotify Slopcast.

If you want to build and run a similar pipeline, look at the publication to understand the framework and the distribution, then use the open-source utilities to set up your own research publications. These utilities are being built in the open — feel free to clone them and vibecode them to meet your needs.

---

## 🐛 Bug tracking

We do **not** manage issues on GitHub. Bugs and fixes for deepDive, DDMA, mdIngest, and the portfolio app are tracked in the [Bug Tracker Space](https://muse.ai/s/bug-tracker-ixe6daxhoezyxy/g1O341vEl5aXYIzWFP1db5l-xunGJAxBRSwSJccC110) — a read-only list of all bugs with their status.

---

Licensed under [CC0 1.0 Universal](LICENSE). Built in the open, provided as-is with no warranty.
