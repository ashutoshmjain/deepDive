import re
import os
import subprocess
import sys

# Thematic categories mapping
CATEGORIES = {
    "bitcoin": "# The Bitcoin Standard & Sovereign Assets",
    "btc": "# The Bitcoin Standard & Sovereign Assets",
    "sbr": "# The Bitcoin Standard & Sovereign Assets",
    "ai": "# The AI Revolution & Machine Intelligence",
    "google": "# The AI Revolution & Machine Intelligence",
    "agent": "# The AI Revolution & Machine Intelligence",
    "robot": "# The AI Revolution & Machine Intelligence",
    "llm": "# The AI Revolution & Machine Intelligence",
    "strc": "# Digital Credit & The STRC Bridge",
    "credit": "# Digital Credit & The STRC Bridge",
    "capital": "# Economics, Capital & The Global Shift",
    "dollar": "# Economics, Capital & The Global Shift",
    "gdp": "# Economics, Capital & The Global Shift",
    "sovereign": "# Economics, Capital & The Global Shift",
    "home": "# Economics, Capital & The Global Shift",
    "dream": "# Economics, Capital & The Global Shift",
    "quantum": "# Philosophy, Science & The Nature of Reality",
    "physics": "# Philosophy, Science & The Nature of Reality",
    "thought": "# Philosophy, Science & The Nature of Reality",
    "meaning": "# Philosophy, Science & The Nature of Reality",
    "nostr": "# Social, Culture & Digital Sovereignty",
    "vim": "# Social, Culture & Digital Sovereignty",
    "lata": "# Social, Culture & Digital Sovereignty",
    "cryptograph": "# Philosophy, Science & The Nature of Reality"
}

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
    "![][image13]": r"$l^\mu$",
    "![][image14]": r"$(SU(3) \times SU(2) \times U(1)) / \mathbb{Z}_6$",
    "![][image15]": r"$\mathbb{Z}_6$",
    "![][image16]": r"$N_g = 3$",
    "![][image17]": r"$N_g = 3$",
    "![][image18]": r"$L_P^2$",
    "![][image19]": r"$\alpha_s$",
    "![][image20]": r"$Q$",
    "![][image21]": r"$\alpha^{n}$",
    "![][image22]": r"$n=0$",
    "![][image23]": r"$y \sim 1$",
    "![][image24]": r"$n=1$",
    "![][image25]": r"$y \sim \alpha$",
    "![][image26]": r"$n=1$",
    "![][image27]": r"$y \sim \alpha$",
    "![][image28]": r"$n=2$",
    "![][image29]": r"$y \sim \alpha^2$",
    "![][image30]": r"$n=3$",
    "![][image31]": r"$y \sim \alpha^3$",
    "![][image32]": r"$2/3$",
    "![][image33]": r"$S_3$",
    "![][image34]": r"$1/r$",
    "![][image35]": r"$a_0$",
    "![][image36]": r"$10^{34}$",
    "![][image37]": r"$10-50$"
}

PODCAST_LINKS = """<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>"""

LIGHTNING_WIDGET = """
---

### Tips and Donations

If you enjoyed this deep dive, consider supporting the project with a tip in **Sats**. It's a simple, global way to support independent research.

<lightning-widget
  name="Thanks for supporting the publication"
  accent="#f9ce00"
  to="shutosha@primal.net"
  image="https://nostrcheck.me/media/5af0794606a15b5641e25aa23d04af4cb0d7d5e68b11cacb47e56a4698fca8c4/49ff6d00cb5bc819cd19f77783d4815fbd46a5b99b6fbdead1eaecfab798187b.webp"
/>
<script src="https://embed.twentyuno.net/js/app.js"></script>

To send Sats, you'll need a [lightning wallet](https://lightningaddress.com/). 

---
"""

def check_root():
    if not os.path.exists('src') or not os.path.exists('scripts'):
        print("ERROR: Script must be run from the project root (the directory containing 'src/' and 'scripts/').")
        sys.exit(1)

def get_file_dates():
    try:
        cmd = "git log --name-only --diff-filter=A --format='%at' src/*.md"
        output = subprocess.check_output(cmd, shell=True, text=True)
        file_dates = {}
        current_time = None
        for line in output.split('\n'):
            line = line.strip()
            if not line: continue
            if line.isdigit():
                current_time = int(line)
            elif line.startswith('src/') and line.endswith('.md'):
                fname = os.path.basename(line)
                if fname not in file_dates:
                    file_dates[fname] = current_time
        return file_dates
    except Exception:
        return {}

def extract_title(file_path):
    if not os.path.exists(file_path):
        return os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^#\s+(?:\*\*)?(.*?)(?:\*\*)?$', line.strip())
            if m:
                return m.group(1).strip()
    return os.path.basename(file_path)

def categorize_file(filename):
    filename_lower = filename.lower()
    for kw, cat in CATEGORIES.items():
        if kw in filename_lower:
            return cat
    return "# Social, Culture & Digital Sovereignty"

def verify_completeness():
    src_files = [f for f in os.listdir('src') if f.endswith('.md')]
    ignore_files = ['SUMMARY.md', 'cover.md', 'how.md']
    target_files = set([f for f in src_files if f not in ignore_files])
    summary_path = 'src/SUMMARY.md'
    if not os.path.exists(summary_path): return "SUMMARY.md not found."
    with open(summary_path, 'r', encoding='utf-8') as f:
        summary_content = f.read()
    mapped_files = set(re.findall(r'\[.*?\]\(\.\/(\.\/)?(.*?)\)', summary_content))
    mapped_filenames = set([m[1] for m in mapped_files])
    missing = target_files - mapped_filenames
    if not missing: return "SUCCESS: All src/ files are correctly mapped in SUMMARY.md."
    else: return f"WARNING: Missing files in SUMMARY.md: {', '.join(sorted(missing))}"

def update_summary(target_file_path):
    summary_path = 'src/SUMMARY.md'
    if not os.path.exists(summary_path): return

    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    file_dates = get_file_dates()
    file_to_info = {} # filename -> [title, category, date]
    sections_order = []
    current_category = None
    existing_recent = set()
    
    all_src_files = [f for f in os.listdir('src') if f.endswith('.md') and f not in ['SUMMARY.md', 'cover.md', 'how.md']]
    for fname in all_src_files:
        title = extract_title(os.path.join('src', fname))
        file_to_info[fname] = [title, None, file_dates.get(fname, 0)]

    for line in content.split('\n'):
        if line.startswith('# '):
            current_category = line.strip()
            if current_category not in sections_order:
                sections_order.append(current_category)
        elif line.strip().startswith('- ['):
            m = re.search(r'\[(.*?)\]\(\.\/(\.\/)?(.*?)\)', line)
            if m:
                _, _, fname = m.groups()
                if fname in file_to_info:
                    if "Recent .." in current_category:
                        existing_recent.add(fname)
                    else:
                        file_to_info[fname][1] = current_category

    essential_sections = ["# Recent ..", "# The Bitcoin Standard & Sovereign Assets", "# The AI Revolution & Machine Intelligence", "# Digital Credit & The STRC Bridge", "# Economics, Capital & The Global Shift", "# Philosophy, Science & The Nature of Reality", "# Social, Culture & Digital Sovereignty"]
    for es in essential_sections:
        if es not in sections_order:
            sections_order.append(es)

    # Any file not already in a thematic category stays or goes into "Recent .."
    target_filename = os.path.basename(target_file_path)
    recent_filenames = list(existing_recent)
    if target_filename not in recent_filenames and target_filename in file_to_info and file_to_info[target_filename][1] is None:
        recent_filenames.append(target_filename)
    
    def get_sort_key(fname):
        title = file_to_info[fname][0]
        # Try to extract leading episode number
        m = re.match(r'^(\d+)', title)
        if m:
            return (int(m.group(1)), file_to_info[fname][2])
        return (0, file_to_info[fname][2])

    # Sort recent files by episode number (desc), then date (desc)
    recent_filenames.sort(key=get_sort_key, reverse=True)

    report = []
    for fname in file_to_info:
        if fname in recent_filenames: continue
        if file_to_info[fname][1] is None:
            new_cat = categorize_file(fname)
            file_to_info[fname][1] = new_cat
            report.append(f"Mapped {fname} to {new_cat}")

    new_content = ["# Summary", ""]
    for sec in sections_order:
        if sec in ["# Summary", "# About the Project"]: continue
        new_content.append(sec)
        
        if sec == "# Recent ..":
            for rf_base in recent_filenames:
                title = file_to_info[rf_base][0]
                new_content.append(f"- [{title}](./{rf_base})")
        else:
            cat_files = []
            for fname, info in file_to_info.items():
                if info[1] == sec and fname not in recent_filenames:
                    cat_files.append({'title': info[0], 'fname': fname, 'date': info[2]})
            cat_files.sort(key=lambda x: x['date'], reverse=True)
            for f in cat_files:
                new_content.append(f"- [{f['title']}](./{f['fname']})")
        new_content.append("")

    new_content.append("# About the Project")
    new_content.append("- [Deep Dive with Gemini](./cover.md)")
    new_content.append("- [How to read this book](./how.md)")

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_content).strip() + '\n')
    
    return report

def fix_markdown(file_path, new_title=None, episode=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Deep Sanitization: Remove invisible characters and fix broken links
    content = content.replace('\u0332', '')
    # Remove footnote markers from within URLs
    content = re.sub(r'(href=".*?)\[\^\d+\]', r'\1', content)
    
    # 2. H1 Handling
    current_h1_match = re.search(r'^#\s+(.*)$', content, re.MULTILINE)
    if current_h1_match:
        current_full_title = current_h1_match.group(1).strip()
    else:
        current_full_title = os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()
        content = f"# {current_full_title}\n\n" + content

    ep_match = re.match(r'^(\d+)\s*[:\-]\s*(.*)$', current_full_title)
    if ep_match:
        curr_ep, curr_title = ep_match.groups()
    else:
        curr_ep, curr_title = None, current_full_title

    final_ep = episode or curr_ep
    final_title_text = new_title or curr_title

    if final_ep:
        final_h1 = f"# {final_ep} : {final_title_text}"
    else:
        final_h1 = f"# {final_title_text}"

    content = re.sub(r'^#\s+.*$', final_h1, content, count=1, flags=re.MULTILINE)

    # 3. Component Cleaning
    content = re.sub(r'^#\s+\*\*(.*?)\*\*', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'^##\s+\*\*(.*?)\*\*', r'## \1', content, flags=re.MULTILINE)
    
    for placeholder, symbol in KATEX_MAP.items():
        content = content.replace(placeholder, symbol)

    content = re.sub(r'<center>\s*<a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE".*?</center>', '', content, flags=re.DOTALL)
    
    image_name = os.path.basename(file_path).replace('.md', '.png')
    image_path = f"./img/{image_name}"
    
    if "![cover image]" in content:
        content = re.sub(r'!\[cover image\]\(.*?\)', f'![cover image]({image_path})', content)
        content = re.sub(r'(!\[cover image\].*?\n)', rf'\1\n{PODCAST_LINKS}\n\n', content, count=1)
    else:
        content = re.sub(r'(^# .*?\n)', rf'\1\n![cover image]({image_path})\n\n{PODCAST_LINKS}\n\n', content, count=1)

    # 4. Currency Conversion - MASKING KaTeX
    katex_blocks = []
    def mask_katex(m):
        katex_blocks.append(m.group(0))
        return f"__KATEX_BLOCK_{len(katex_blocks)-1}__"

    content = re.sub(r'\$\$.*?\$\$', mask_katex, content, flags=re.DOTALL)
    content = re.sub(r'\$.*?\$', mask_katex, content)

    def curr_repl(m):
        val_str = m.group(1).replace(',', '')
        suffix = m.group(2).lower() if m.group(2) else ""
        multiplier = 1
        if suffix == 'k': multiplier = 1_000
        elif suffix == 'm' or 'million' in suffix: multiplier = 1_000_000
        elif suffix == 'b' or 'billion' in suffix: multiplier = 1_000_000_000
        elif suffix == 't' or 'trillion' in suffix: multiplier = 1_000_000_000_000
        try:
            num = float(val_str) * multiplier
            formatted = f"{int(num):,}" if num == int(num) else f"{num:,}"
            return f"{formatted} USD"
        except: return f"{m.group(1)}{suffix} USD"

    content = re.sub(r'(?<!\w)\$(?!\^)([\d\.,]+)\s*(k|m|b|t|million|billion|trillion)?\b', curr_repl, content, flags=re.IGNORECASE)
    
    for i, block in enumerate(katex_blocks):
        content = content.replace(f"__KATEX_BLOCK_{i}__", block)

    # 5. Footnote Re-numbering - SAFE VERSION
    works_cited_match = re.search(r'#### \*\*Works cited\*\*(.*)', content, re.DOTALL)
    if works_cited_match:
        wc_text = works_cited_match.group(1).strip()
        content = content[:works_cited_match.start()].strip()
        citations = []
        for line in wc_text.split('\n'):
            m = re.match(r'^\[\^(\d+)\]:\s+(.*)', line.strip())
            if not m: m = re.match(r'^(\d+)\.\s+(.*)', line.strip())
            if m: citations.append(m.group(2).strip())
        
        # We DO NOT auto-convert plain numbers to footnotes anymore.
        # We only re-number existing [^n] markers.

        used_cites = {}
        next_id = 1
        def cite_repl(m):
            nonlocal next_id
            try:
                old_id = int(m.group(1))
                if old_id not in used_cites:
                    used_cites[old_id] = next_id
                    next_id += 1
                return f"[^{used_cites[old_id]}]"
            except: return m.group(0)

        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('#'): new_lines.append(line)
            else: new_lines.append(re.sub(r'\[\^(\d+)\]', cite_repl, line))
        content = '\n'.join(new_lines)
        
        ref_sec = "\n\n## References\n\n"
        for old, new in sorted(used_cites.items(), key=lambda x: x[1]):
            if 0 < old <= len(citations):
                cite = citations[old-1]
                cite = re.sub(r'\\([_.-])', r'\1', cite)
                ref_sec += f"[^{new}]: {cite}\n\n"
        content += ref_sec
    
    content = content.replace("Truncated", "")
    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    if "shutosha@primal.net" not in content and "SUMMARY.md" not in file_path:
        if "## References" in content:
            content = content.replace("## References", LIGHTNING_WIDGET + "\n\n## References")
        else:
            content = content.strip() + "\n" + LIGHTNING_WIDGET

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    check_root()
    import argparse
    parser = argparse.ArgumentParser(description='Universal Markdown Fixer')
    parser.add_argument('file', help='The markdown file to process')
    parser.add_argument('--title', help='Optional: A new title for the article', default=None)
    parser.add_argument('--episode', help='Optional: The episode number (e.g., 220)', default=None)
    args = parser.parse_args()

    target = args.file
    if not os.path.exists(target):
        sys.exit(1)

    fix_markdown(target, args.title, args.episode)
    update_summary(target)
    print(f"\nSuccessfully processed {target}")
    final_full_title = extract_title(target)
    print(f"\nFinal Title: '{final_full_title}'")
    print(verify_completeness())
