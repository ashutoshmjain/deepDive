import re
import os
import unicodedata

# Configuration
FULL_FIDELITY_FILE = "src/241-full-fidelity.md.tmp"
TARGET_FILE = "src/241.md"

# Math Mapping
MATH_MAP = {
    "image1": r"\mathbb{R}",
    "image2": r"ab = ba",
    "image3": r"\mathbb{C}",
    "image4": r"i",
    "image5": r"ab = ba",
    "image6": r"(ab)c = a(bc)",
    "image7": r"a",
    "image8": r"b",
    "image9": r"\mathbb{H}",
    "image10": r"i, j, k",
    "image11": r"ij = k",
    "image12": r"ji = -k",
    "image13": r"ab \neq ba",
    "image14": r"ab \neq ba",
    "image15": r"A",
    "image16": r"B",
    "image17": r"(ab)c = a(bc)",
    "image18": r"a, b, c",
    "image19": r"\mathbb{O}",
    "image20": r"(ab)c \neq a(bc)",
    "image21": r"a > b",
    "image22": r"\mathbb{S}",
    "image23": r"kT \ln 2",
    "image24": r"k_B",
    "image25": r"T"
}

def hydrate():
    if not os.path.exists(FULL_FIDELITY_FILE):
        print(f"Error: {FULL_FIDELITY_FILE} not found.")
        return

    with open(FULL_FIDELITY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 0. Cleanup
    content = unicodedata.normalize('NFKD', content)
    content = re.sub(r'[\u0300-\u036f\u2000-\u200f\ufeff\u0332]', '', content)
    content = content.replace("\xa0", " ")

    # 0.1 Convert currency $ to USD (to avoid KaTeX conflicts)
    # Match $ followed by a number or [^ (citation)
    content = re.sub(r"\$(\d+)", r"\1 USD", content)
    content = re.sub(r"\$\[\^", r"USD [^", content)

    # 1. Strip Google Docs header/junk
    start_match = re.search(r"The Cayley-Dickson progression", content)
    if start_match:
        body = content[start_match.start():]
    else:
        body = content

    # 2. Handle Citations
    def citation_replacer(match):
        prefix = match.group(1) or ""
        cit_num = int(match.group(2))
        if 1 <= cit_num <= 65:
            return f"{prefix}[^{cit_num}]"
        return match.group(0)

    body = re.sub(r"([\.?!,\]\)\$\)])\s*(\d+)(?!\.)", citation_replacer, body)
    body = re.sub(r"([a-zA-Z])(\d+)(?=\s|$|\n)", citation_replacer, body)

    # 3. Replace Image Placeholders with KaTeX
    for img_id, latex in MATH_MAP.items():
        placeholder = f"![]" + f"[{img_id}]"
        body = body.replace(placeholder, f"${latex}$")

    # 4. Clean up URL escapes
    body = re.sub(r"\\_", "_", body)
    body = re.sub(r"\\-", "-", body)
    
    # 5. Format Bibliography
    works_cited_start = re.search(r"Works cited", body, re.IGNORECASE)
    if works_cited_start:
        before_refs = body[:works_cited_start.start()]
        refs_raw = body[works_cited_start.end():]
        
        refs_dict = {}
        parts = re.split(r"(?:\n|^)(\d+)\.\s+", refs_raw)
        for i in range(1, len(parts), 2):
            num = parts[i].strip()
            text = parts[i+1].strip()
            if text:
                text = " ".join(text.split())
                refs_dict[num] = text
        
        refs_cleaned = []
        for num in sorted(refs_dict.keys(), key=int):
            refs_cleaned.append(f"[^{num}]: {refs_dict[num]}")
        
        body = before_refs + "#### **Works Cited**\n\n" + "\n\n".join(refs_cleaned)

    # 6. Re-inject Header
    header = r"""# 241 : What exactly is Immutability?

<!-- VIDEO_STRIP_START -->
<div class="video-single-container" style="display: flex; justify-content: center; width: 100%; margin: 20px 0;">
  <div style="width: 100%; max-width: 10000px; position: relative; border-radius: 12px; overflow: hidden; background: #000; aspect-ratio: 16/9; display: flex; flex-direction: column; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
    <video src="vid/241-Intro.mp4" style="width: 100%; height: 100%; object-fit: contain;" playsinline loop preload="auto" muted autoplay></video>
    <button class="vid-toggle" onclick="window.oph_play_toggle(this)" style="position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.8); color: white; border: 2px solid white; border-radius: 50%; width: 50px; height: 50px; cursor: pointer; font-size: 24px; z-index: 100; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1.0)'">🔇</button>
  </div>
</div>

<script>
window.oph_play_toggle = function(btn) {
  const parent = btn.parentElement;
  const vid = parent.querySelector('video');
  const container = btn.closest('.video-carousel-container, .video-single-container');
  
  if (vid.muted || vid.paused) {
    if (container) {
      container.querySelectorAll('video').forEach(v => {
        if (v !== vid) {
          v.pause();
          v.muted = true;
          const otherBtn = v.parentElement.querySelector('.vid-toggle');
          if (otherBtn) otherBtn.innerText = '🔇';
        }
      });
    }
    vid.muted = false;
    vid.volume = 1.0;
    vid.play().then(() => { btn.innerText = '🔊'; }).catch(e => console.error('Play failed:', e));
  } else {
    vid.pause();
    vid.muted = true;
    btn.innerText = '🔇';
  }
};

(function() {
  const init = () => {
    const vids = document.querySelectorAll('.video-carousel-container video, .video-single-container video');
    vids.forEach(v => { 
      v.muted = true; 
      v.play().catch(() => {}); 
    });
  };
  if (document.readyState === 'complete') { init(); }
  else { window.addEventListener('load', init); }
})();
</script>
<!-- VIDEO_STRIP_END -->

<p align="center">
<i><b>Note to Readers:</b> This document has been updated to <b>Full Fidelity</b>. It now contains the complete depth of research, exhaustive citations, and absolute KaTeX mathematical proofs.</i>
</p>

***

"""
    final_content = header + body

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Successfully hydrated {TARGET_FILE}")

if __name__ == "__main__":
    hydrate()
