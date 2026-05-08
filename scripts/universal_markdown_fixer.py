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

EPISODE_230_MAP = {
    "![][image1]": r"$mNAV < 1$"
}

def check_root():
    if not os.path.exists('book.toml'):
        sys.exit(1)

def extract_title(file_path):
    if not os.path.exists(file_path): return os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match H1 or H2 as the title
            m = re.match(r'^#{1,2}\s+(?:\d+\s*[:\-]\s*)?(.*?)$', line.strip())
            if m: return m.group(1).strip().replace('**', '')
    return os.path.basename(file_path)

def extract_episode(filename, title):
    m = re.match(r'^(\d+)\.md$', filename)
    if m:
        val = int(m.group(1))
        if val < 1000: return str(val)
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

    new_lines = ["# Summary\n", "\n", "- [Deep Dive with Gemini](./cover.md)\n", "\n", "# Recent ..\n"]
    numbered = sorted([f for f in file_to_info if file_to_info[f]["ep"]], key=lambda x: int(file_to_info[x]["ep"]), reverse=True)
    for f in numbered:
        new_lines.append(f"- [{file_to_info[f]['ep']} : {file_to_info[f]['title']}](././{f})\n")
    
    categories = {}
    current_cat = None
    for line in lines:
        if line.startswith("# ") and "Summary" not in line and "Recent .." not in line:
            current_cat = line.strip()
            if current_cat not in categories: categories[current_cat] = []
        elif line.strip().startswith("- [") and current_cat:
            m = re.search(r'\[(.*?)\]\(\.\/(.*?)\)', line)
            if m:
                fname = m.group(2).replace("./", "")
                if fname in file_to_info and not file_to_info[fname]["ep"]:
                    if line.strip() not in categories[current_cat]:
                        categories[current_cat].append(line.strip())

    for cat in ["# The Bitcoin Standard & Sovereign Assets", "# The AI Revolution & Machine Intelligence", 
                "# Digital Credit & The STRC Bridge", "# Economics, Capital & The Global Shift", 
                "# Philosophy, Science & The Nature of Reality", "# Social, Culture & Digital Sovereignty"]:
        if cat in categories and categories[cat]:
            new_lines.append(f"\n{cat}\n")
            for item in categories[cat]:
                new_lines.append(f"{item}\n")
            del categories[cat]
            
    for cat, items in categories.items():
        if items:
            new_lines.append(f"\n{cat}\n")
            for item in items:
                new_lines.append(f"{item}\n")

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("".join(new_lines))

def fix_footnotes(content):
    parts = re.split(r'(#### \*\*Works cited\*\*|#### \*\*References\*\*)', content, flags=re.IGNORECASE)
    if len(parts) < 3: return content
    
    header = parts[1]
    refs_raw = parts[2]
    body = parts[0]
    
    # IMPROVED PARSING: Handle 1., 1 , and [^1]:
    ref_map = {}
    # [^1]: ...
    ref_lines = re.findall(r'^\[\^(\d+)\]:\s*(.*)$', refs_raw, re.MULTILINE)
    # 1. ...
    ref_lines += re.findall(r'^(\d+)\.\s*(.*)$', refs_raw, re.MULTILINE)
    # 1 ...
    ref_lines += re.findall(r'^(\d+)\s+([^\d].*)$', refs_raw, re.MULTILINE)

    for num, text in ref_lines:
        if num not in ref_map: ref_map[num] = text.strip()
    
    if not ref_map: return content

    # 1. Convert plain citations to [^N]
    # Handle both punctuation-prefixed and space-prefixed numbers
    def replacer(match):
        pre = match.group(1)
        punct = match.group(2)
        nums_str = match.group(3)
        # Avoid matching version numbers or currency decimals
        if punct == '.' and pre and pre.isdigit(): return match.group(0)
        if punct == ':' and pre and pre.isdigit(): return match.group(0)
        
        parts = re.split(r'[\s,]+', nums_str)
        valid_footnotes = []
        for p in parts:
            if not p: continue
            if p in ref_map: valid_footnotes.append(f"[^{p}]")
            else: return match.group(0)
        return f"{pre}{punct}{''.join(valid_footnotes)}"

    # Match numbers after punctuation
    body = re.sub(r'(.?)([.,;")\]])(\d+(?:[\s,]+\d+)*)(?![.\d])', replacer, body)
    # Match numbers after space ONLY if followed by punctuation or end of sentence
    body = re.sub(r'(.?)( )(\d+(?:[\s,]+\d+)*)(?=[.,;":!?]|$)', replacer, body)
    
    def table_repl(match):
        pre, num, post = match.groups()
        if num in ref_map: return f"{pre}[^{num}]{post}"
        return match.group(0)
    body = re.sub(r'(\|[^|]*?\s+)(\d+)(\s*\|)', table_repl, body)

    # 2. IDENTIFY USED FOOTNOTES
    used_numbers = re.findall(r'\[\^(\d+)\]', body)
    unique_used = sorted(list(set(used_numbers)), key=int)
    
    # 3. RE-NUMBER SEQUENTIALLY
    num_map = {old: str(i+1) for i, old in enumerate(unique_used)}
    
    def final_repl(match):
        old_num = match.group(1)
        return f"[^{num_map[old_num]}]"
    
    body = re.sub(r'\[\^(\d+)\]', final_repl, body)

    new_refs = [f"\n\n{header}\n"]
    for old_num in unique_used:
        new_refs.append(f"[^{num_map[old_num]}]: {ref_map[old_num]}\n")
    
    return body + "".join(new_refs)

def fix_markdown(file_path, title_override=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 0. STRIP INVISIBLE CHARS AND NON-ASCII
    content = content.replace('\u0332', '')
    content = "".join(c for c in content if ord(c) >= 32 or c in '\n\r\t')
    content = "".join(c for c in content if ord(c) < 128)
    
    # 1. CLEANUP URLS (Remove backslashes before special chars)
    content = re.sub(r'(\\)([_.-])', r'\2', content)

    filename = os.path.basename(file_path)
    ep_num = extract_episode(filename, "")
    
    # 2. KATEX PROTECTION
    math_blocks = []
    def save_math(match):
        math_blocks.append(match.group(0))
        return f"__MATH_BLOCK_{len(math_blocks)-1}__"
    
    # Catch both $$ ... $$ and $ ... $
    content = re.sub(r'\$\$.*?\$\$', save_math, content, flags=re.DOTALL)
    content = re.sub(r'\$.*?\$', save_math, content)
    
    # 3. EPISODE SPECIFIC MAPS (Placeholder replacements)
    cur_map = KATEX_MAP
    if ep_num == "229": cur_map = EPISODE_229_MAP
    elif ep_num == "230": cur_map = EPISODE_230_MAP
    for placeholder, symbol in cur_map.items():
        content = content.replace(placeholder, symbol)

    # 4. PRUNE FOOTNOTES
    content = fix_footnotes(content)
    
    # 5. TITLE AND ASSET INTEGRATION
    lines = content.split('\n')
    title = ""
    for i, line in enumerate(lines):
        m = re.match(r'^(#{1,2})\s+(?:\d+\s*[:\-]\s*)?(.*?)$', line.strip())
        if m:
            if title_override:
                # Use override exactly if provided, just ensure it starts with "EP : "
                if not re.match(r'^\d+\s*[:\-]', title_override):
                    full_title = f"{ep_num} : {title_override}"
                else:
                    full_title = title_override
                # For the image alt text, strip the number
                title = re.sub(r'^\d+\s*[:\-]\s*', '', full_title).strip()
            else:
                raw_title = m.group(2).strip().replace('**', '')
                words = raw_title.split()
                limit = 5
                while limit > 1 and words[limit-1].lower() in ['the', 'of', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'with', 'about', 'to']:
                    limit -= 1
                title = " ".join(words[:limit])
                full_title = f"{ep_num} : {title}"
            
            lines[i] = f"# {full_title}"
            
            image_path = f"img/{ep_num}.png"
            new_lines = [lines[i], "", f"![{title}]({image_path})", "", PODCAST_LINKS, ""]
            
            j = i + 1
            while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith('![') or '<center>' in lines[j]):
                j += 1
            lines = new_lines + lines[j:]
            break

    content = '\n'.join(lines)
    
    # 6. CURRENCY AND DOLLAR SIGNS (Applied to non-math blocks)
    # Convert $100 to 100 USD
    content = re.sub(r'\$([\d\.,]+)\s*(million|billion|trillion|k|m|b|t)?(?=[^0-9\^]|$)', r'\1 \2 USD ', content, flags=re.IGNORECASE)
    content = content.replace('  ', ' ')
    # Escape remaining literal dollar signs
    content = content.replace('$', r'\$')
    
    # 7. RESTORE MATH
    for idx, block in enumerate(math_blocks):
        content = content.replace(f"__MATH_BLOCK_{idx}__", block)

    if "lightning-widget" not in content:
        content = content.strip() + "\n" + LIGHTNING_WIDGET

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    check_root()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--title', help="Override title")
    args = parser.parse_args()
    if os.path.exists(args.file):
        fix_markdown(args.file, title_override=args.title)
        update_summary(args.file)
