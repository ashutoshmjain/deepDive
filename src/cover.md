# Deep Dive with Gemini

<center>

<a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a>

</center>

This is a **Clean Internet** publication: universally accessible, anonymous, and clutter-free. No trackers, no cookies, no ads. We conduct deep research into technology, finance, and philosophy, refined in our [open-source repository](https://github.com/ashutoshmjain/deepDive).


<!-- VIDEO_STRIP_START -->

<center><h3>Info Graphics feed from <a href="https://mosaic.so" target="_blank" style="text-decoration: none; color: inherit; border-bottom: 1px solid #555;">Mosaic.SO</a></h3></center>

<center><a href="https://www.tiktok.com/@shutoshabot" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">TikTok</a><a href="https://www.instagram.com/shutoshabot/" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Instagram</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37q8rU8HKTLhdLPZQadcvx-K" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://open.spotify.com/show/07r9EZMLpFC7qwZwxsJ5P9" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Spotify</a></center>

<div class="video-carousel-container" style="display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 15px; padding: 20px 0; scroll-behavior: smooth;">
  <div style="flex: 0 0 60%; scroll-snap-align: center; position: relative; border-radius: 12px; overflow: hidden; background: #000; aspect-ratio: 1/1; display: flex; flex-direction: column;">
    <video src="vid/cover-cleanInternet.mp4" style="width: 100%; height: 85%; object-fit: contain;" playsinline loop preload="auto" muted autoplay></video>
    <div style="height: 15%; background: #1a1a1a; color: #ccc; display: flex; align-items: center; justify-content: center; font-family: monospace; font-size: 12px; border-top: 1px solid #333;">cover-cleanInternet</div>
    <button class="vid-toggle" onclick="window.oph_play_toggle(this)" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: white; border: 2px solid white; border-radius: 50%; width: 45px; height: 45px; cursor: pointer; font-size: 22px; z-index: 100;">🔇</button>
  </div>
  <div style="flex: 0 0 60%; scroll-snap-align: center; position: relative; border-radius: 12px; overflow: hidden; background: #000; aspect-ratio: 1/1; display: flex; flex-direction: column;">
    <video src="vid/cover-collaborativeIntel.mp4" style="width: 100%; height: 85%; object-fit: contain;" playsinline loop preload="auto" muted autoplay></video>
    <div style="height: 15%; background: #1a1a1a; color: #ccc; display: flex; align-items: center; justify-content: center; font-family: monospace; font-size: 12px; border-top: 1px solid #333;">cover-collaborativeIntel</div>
    <button class="vid-toggle" onclick="window.oph_play_toggle(this)" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: white; border: 2px solid white; border-radius: 50%; width: 45px; height: 45px; cursor: pointer; font-size: 22px; z-index: 100;">🔇</button>
  </div>
</div>
<script>
  window.oph_play_toggle = window.oph_play_toggle || function(btn) {
    const parent = btn.parentElement;
    const vid = parent.querySelector('video');
    const container = btn.closest('.video-carousel-container');
    if (vid.paused || vid.muted) {
      container.querySelectorAll('video').forEach(v => { v.pause(); v.muted = true; v.parentElement.querySelector('.vid-toggle').innerText = '🔇'; });
      vid.muted = false; vid.volume = 1.0;
      vid.play().then(() => { btn.innerText = '🔊'; }).catch(e => console.error(e));
    } else {
      vid.pause(); vid.muted = true; btn.innerText = '🔇';
    }
  };
  (function() {
    const init = () => {
      const vids = document.querySelectorAll('.video-carousel-container video');
      vids.forEach(v => { 
        v.muted = true; 
        v.play().catch(() => {}); 
      });
    };
    setTimeout(init, 500);
  })();
</script>
<!-- VIDEO_STRIP_END -->



### Quick Start
- **Navigation:** Toggle the <i class="fa fa-bars"></i> sidebar for chapters, or use <i class="fa fa-search"></i> to search.
- **Install as App:** Enjoy **offline access**, faster loading, and a clean home-screen icon.
  - **iOS:** Share <i class="fa fa-share-square-o"></i> → **Add to Home Screen**.
  - **Android:** Menu <i class="fa fa-ellipsis-v"></i> → **Install App**.
  - **Desktop:** Click the **Install** icon in your address bar.

### The Process
- **Research:** Synthesizing listener inputs with high-fidelity AI-driven deep searches.
- **Publish:** Iteratively refined papers are published here for open-source review.
- **Listen:** Research is transformed into concise, high-quality audio episodes. Infographic shorts are created using [Mosaic Motion](https://motion.so).

---

<center>

![deepDive](./deepDive.png)

_An integrated exploration of intelligence - that sticks :-)_

</center>

---

<center>

Licensed under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)

</center>
