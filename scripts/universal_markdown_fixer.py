import re
import os
import subprocess
import sys

CATEGORIES = {
    "bitcoin": "# The Bitcoin Standard & Sovereign Assets",
    "btc": "# The Bitcoin Standard & Sovereign Assets",
    "sbr": "# The Bitcoin Standard & Sovereign Assets",
}

PODCAST_LINKS = '<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>'

LIGHTNING_WIDGET = """
---

### Tips and Donations

If you enjoyed this deep dive, consider supporting the project with a tip in **Sats**. It's a simple, global way to support independent research.

<lightning-widget
  name='Thanks for supporting the publication'
  accent='#f9ce00'
  to='shutosha@primal.net'
  image='https://nostrcheck.me/media/5af0794606a15b5641e25aa23d04af4cb0d7d5e68b11cacb47e56a4698fca8c4/49ff6d00cb5bc819cd19f77783d4815fbd46a5b99b6fbdead1eaecfab798187b.webp'
/>
<script src='https://embed.twentyuno.net/js/app.js'></script>

To send Sats, you'll need a [lightning wallet](https://lightningaddress.com/). 

---
"""

KATEX_MAP = {
    "![][image1]": r"$\mathcal{P} = (\mathcal{S}, \mathcal{A}, \rho, \mathcal{R})$",
    "![][image2]": r"$\mathcal{S}$",
    "![][image3]": r"$\mathcal{A}$",
    "![][image4]": r"$\rho$",
    "![][image5]": r"$\mathcal{R}$",
    "![][image6]": r"$G_N$",
    "![][image7]": r"$SU(3) \times SU(2) \times U(1)$",
    "![][image8]": r"$S^2$",
    "![][image9]": r"$SL(2, \mathbb{C})$",
    "![][image10]": r"$SO(3,1)$",
    "![][image11]": r"$10^{120}$",
    "![][image12]": r"$T_{\mu\nu} l^\mu l^\nu = 0$",
}

EPISODE_229_MAP = {
    "![][image1]": r"$E = mc^2$",
    "![][image2]": r"$10-15$",
    "![][image3]": r"$100$",
    "![][image4]": r"$500-1000$",
    "![][image5]": r"$I$",
    "![][image6]": r"$\eta$",
    "![][image7]": r"$E$",
    "![][image8]": r"$\Delta S$",
    "![][image9]": r"$$I = \eta \frac{\Delta S \cdot k_B T}{E}$$",
    "![][image10]": r"$\Delta S$",
    "![][image11]": r"$T$",
    "![][image12]": r"$W \ge k_B T \ln 2$",
    "![][image13]": r"$$T = \kappa E$$",
    "![][image14]": r"$\kappa$",
    "![][image15]": r"$E$",
    "![][image16]": r"$2E/\pi\hbar$",
    "![][image17]": r"$E = mc^2$",
    "![][image18]": r"$10^{50}$",
    "![][image19]": r"$L$",
    "![][image20]": r"$C$",
    "![][image21]": r"$N$",
    "![][image22]": r"$1/C^\alpha$",
    "![][image23]": r"$1/N^\beta$",
    "![][image24]": r"$1/D^\gamma$",
    "![][image25]": r"$\rho_s$",
    "![][image26]": r"$P_s$",
    "![][image27]": r"$\mathcal{M}$",
    "![][image28]": r"$G_{\mu\nu}$",
    "![][image29]": r"$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \kappa T_{\mu\nu}$$",
    "![][image30]": r"$a$",
    "![][image31]": r"$\Phi$",
    "![][image32]": r"$4 \times 10^{26}$",
    "![][image33]": r"$$I \propto \frac{\Delta S}{E}$$"
}

def check_root():
    if not os.path.exists('book.toml'):
        sys.exit(1)

def extract_title(file_path):
    if not os.path.exists(file_path): return os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^#\s+(?:\d+\s*[:\-]\s*)?(?:\*\*)?(.*?)(?:\*\*)?$', line.strip())
            if m: return m.group(1).strip()
    return os.path.basename(file_path)

def extract_episode(filename, title):
    m = re.match(r'^(\d+)\.md$', filename)
    if m: return m.group(1)
    m = re.match(r'^(\d+)\s*[:\-]', title)
    if m: return m.group(1)
    return None

def update_summary(target_file_path):
    summary_path = 'src/SUMMARY.md'
    if not os.path.exists(summary_path): return
    with open(summary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    all_src_files = [f for f in os.listdir('src') if f.endswith('.md') and f not in ['SUMMARY.md', 'cover.md']]
    file_to_info = {}
    for fname in all_src_files:
        title = extract_title(os.path.join('src', fname))
        ep = extract_episode(fname, title)
        file_to_info[fname] = {"title": title, "ep": ep}

    # Rebuild SUMMARY.md
    new_lines = ["# Summary\\n", "\n", "- [Deep Dive with Gemini](./cover.md)\\n", "\n", "# Recent ..\\n"]
    
    # 1. Numbered Episodes (Growing Recent Section)
    numbered = sorted([f for f in file_to_info if file_to_info[f]["ep"]], key=lambda x: int(file_to_info[x]["ep"]), reverse=True)
    for f in numbered:
        new_lines.append(f"- [{file_to_info[f]['ep']} : {file_to_info[f]['title']}](././{f})\\n")
    
    # 2. Add thematic categories (excluding numbered episodes)
    # We parse the existing SUMMARY.md to keep unnumbered ones in their places
    categories = {} # category_name -> [lines]
    current_cat = None
    for line in lines:
        if line.startswith("# ") and "Summary" not in line and "Recent .." not in line:
            current_cat = line.strip()
            categories[current_cat] = []
        elif line.strip().startswith("- [") and current_cat:
            m = re.search(r'\[(.*?)\]\(\.\/(.*?)\)', line)
            if m:
                fname = m.group(2).replace("./", "")
                if fname in file_to_info and not file_to_info[fname]["ep"]:
                    categories[current_cat].append(line.strip())

    for cat, items in categories.items():
        if items:
            new_lines.append(f"\\n{cat}\\n")
            for item in items:
                new_lines.append(f"{item}\\n")

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("".join(new_lines).replace("\\n", "\n"))

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 0. Strip invisible
    content = "".join(c for c in content if ord(c) >= 32 or c in '\n\r\t')
    content = "".join(c for c in content if ord(c) < 128)
    
    filename = os.path.basename(file_path)
    cur_map = EPISODE_229_MAP if "229" in filename else KATEX_MAP
    for placeholder, symbol in cur_map.items():
        content = content.replace(placeholder, symbol)

    # Currency (Only outside $)
    def curr_repl(text):
        parts = re.split(r'(\$.*?\$)', text, flags=re.DOTALL)
        for i in range(len(parts)):
            if not parts[i].startswith('$'):
                parts[i] = re.sub(r'(?<![\w/])\$(?!\^)([\d\.,]+)\s*(k|m|b|t|million|billion|trillion)?\b', 
                                 r'\1\2 USD', parts[i], flags=re.IGNORECASE)
        return ''.join(parts)
    content = curr_repl(content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    check_root()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    if os.path.exists(args.file):
        fix_markdown(args.file)
        update_summary(args.file)
