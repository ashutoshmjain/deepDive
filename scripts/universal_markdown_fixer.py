import re
import os
import subprocess
import sys

# Thematic categories mapping (only for unnumbered/legacy posts)
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
        print("ERROR: Script must be run from the project root.")
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

def extract_episode(filename, title):
    # Priority 1: Filename (Master Key)
    m = re.match(r'^(\d+)\.md$', filename)
    if m: return m.group(1)
    # Priority 2: Title
    m = re.match(r'^(\d+)\s*[:\-]', title)
    if m: return m.group(1)
    return None

def categorize_file(filename):
    filename_lower = filename.lower()
    for kw, cat in CATEGORIES.items():
        if kw in filename_lower:
            return cat
    return "# Social, Culture & Digital Sovereignty"

def verify_completeness():
    """Verifies that all src/ markdown files (except internal ones) are linked in SUMMARY.md."""
    src_files = [f for f in os.listdir('src') if f.endswith('.md')]
    ignore_files = ['SUMMARY.md', 'cover.md']
    target_files = set([f for f in src_files if f not in ignore_files])
    summary_path = 'src/SUMMARY.md'
    if not os.path.exists(summary_path): return "SUMMARY.md not found."
    with open(summary_path, 'r', encoding='utf-8') as f:
        summary_content = f.read()
    # Matches both standard ./filename.md and legacy ././filename.md
    mapped_files = set(re.findall(r'\[.*?\]\(\.\/(?:\.\/)?(.*?)\)', summary_content))
    missing = target_files - mapped_files
    if not missing: return "SUCCESS: All src/ files are correctly mapped in SUMMARY.md."
    else: return f"WARNING: Missing files in SUMMARY.md: {', '.join(sorted(missing))}"

def update_summary(target_file_path):
    """Synchronizes SUMMARY.md with the current src/ directory, managing 'Recent ..' and thematic sections."""
    summary_path = 'src/SUMMARY.md'
    if not os.path.exists(summary_path): return

    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    file_dates = get_file_dates()
    file_to_info = {} # filename -> [title, category, date, is_numbered]
    
    all_src_files = [f for f in os.listdir('src') if f.endswith('.md') and f not in ['SUMMARY.md', 'cover.md']]
    for fname in all_src_files:
        title = extract_title(os.path.join('src', fname))
        episode = extract_episode(fname, title)
        file_to_info[fname] = [title, None, file_dates.get(fname, 0), episode is not None]

    # Parse existing structure to find which category each file was in
    sections_order = []
    current_category = None
    for line in content.split('\n'):
        if line.startswith('# '):
            current_category = line.strip()
            if current_category not in sections_order:
                sections_order.append(current_category)
        elif line.strip().startswith('- ['):
            # Matches standard and aliased paths for transition
            m = re.search(r'\[(.*?)\]\(\.\/(?:\.\/)?(.*?)\)', line)
            if m:
                _, fname = m.groups()
                if fname in file_to_info:
                    # If it's a thematic category, record it. 
                    if "Recent .." not in current_category:
                        file_to_info[fname][1] = current_category

    essential_sections = ["# Recent ..", "# The Bitcoin Standard & Sovereign Assets", "# The AI Revolution & Machine Intelligence", "# Digital Credit & The STRC Bridge", "# Economics, Capital & The Global Shift", "# Philosophy, Science & The Nature of Reality", "# Social, Culture & Digital Sovereignty"]
    for es in essential_sections:
        if es not in sections_order:
            sections_order.append(es)

    # Master Key Rule: All numbered files MUST be in "Recent .."
    recent_filenames = [f for f, info in file_to_info.items() if info[3]]
    
    def get_sort_key(fname):
        title = file_to_info[fname][0]
        episode = extract_episode(fname, title)
        if episode:
            return (int(episode), file_to_info[fname][2])
        return (0, file_to_info[fname][2])

    recent_filenames.sort(key=get_sort_key, reverse=True)

    # Map unnumbered files to thematic categories if not already mapped
    for fname, info in file_to_info.items():
        if not info[3] and info[1] is None:
            info[1] = categorize_file(fname)

    new_content = ["# Summary", "", "- [Deep Dive with Gemini](./cover.md)", ""]
    for sec in sections_order:
        if sec in ["# Summary", "# About the Project"]: continue
        new_content.append(sec)
        
        if sec == "# Recent ..":
            for rf_base in recent_filenames:
                title = file_to_info[rf_base][0]
                # Use standard paths (removing path-aliasing hack)
                new_content.append(f"- [{title}](./{rf_base})")
        else:
            cat_files = []
            for fname, info in file_to_info.items():
                # Only put unnumbered files in thematic categories
                if info[1] == sec and not info[3]:
                    cat_files.append({'title': info[0], 'fname': fname, 'date': info[2]})
            cat_files.sort(key=lambda x: x['date'], reverse=True)
            for f in cat_files:
                new_content.append(f"- [{f['title']}](./{f['fname']})")
        new_content.append("")

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_content).strip() + '\n')

def fix_footnotes(content):
    # Find the "Works cited" or "Research" section
    works_cited_match = re.search(r'#### \*\*(Works cited|Research)\*\*', content, re.IGNORECASE)
    if not works_cited_match:
        return content
    
    body = content[:works_cited_match.start()]
    references_block = content[works_cited_match.start():]
    
    # Sanitize references_block for KaTeX-unfriendly escapes
    references_block = references_block.replace(r'\\-', '-').replace(r'\-', '-')
    references_block = references_block.replace(r'\&', '&').replace(r'\_', '_')

    # 1. Convert all [n] style markers in body to [^n] BEFORE usage check
    body = re.sub(r'(?<!\w)\[(\d+)\](?!\^)', r'[^\1]', body)
    
    # 2. Add spaces between consecutive markers to fix mdbook rendering
    body = re.sub(r'(\[\^\d+\])(\[\^\d+\])', r'\1 \2', body)

    # 3. Extract reference definitions: {num: text}
    ref_defs = {}
    lines = references_block.split('\n')
    for line in lines:
        match = re.match(r'^(?:\[\^(\d+)\]:|\s*(\d+)\.)\s+(.*)', line.strip())
        if match:
            num = match.group(1) or match.group(2)
            text = match.group(3)
            ref_defs[num] = text

    # 4. Find all used [^n] markers in body (order of appearance)
    found_markers = re.findall(r'\[\^(\d+)\]', body)
    unique_markers_ordered = []
    for m in found_markers:
        if m not in unique_markers_ordered:
            unique_markers_ordered.append(m)
    
    # 5. Create mapping for sequential re-numbering
    # We include EVERY reference from ref_defs to prevent data loss
    all_refs_to_keep = list(unique_markers_ordered)
    for num in sorted(ref_defs.keys(), key=int):
        if num not in all_refs_to_keep:
            all_refs_to_keep.append(num)
            
    mapping = {old: str(i+1) for i, old in enumerate(all_refs_to_keep)}
    
    # 6. Replace markers in body with new sequential numbers
    def marker_repl(match):
        old_num = match.group(1)
        return f"[[TEMP_{mapping[old_num]}]]"
    
    body = re.sub(r'\[\^(\d+)\]', marker_repl, body)
    body = body.replace("[[TEMP_", "[^").replace("]]", "]")

    # 7. Rebuild the Research section (sequential, preserving all unique entries)
    header_text = works_cited_match.group(1)
    new_references = f"#### **{header_text}**\n\n"
    for old_num in all_refs_to_keep:
        if old_num in ref_defs:
            new_num = mapping[old_num]
            new_references += f"[^{new_num}]: {ref_defs[old_num]}\n\n"
    
    return body.strip() + "\n\n" + new_references.strip()

def fix_markdown(file_path, new_title=None, episode=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(file_path)
    
    # 1. Title and Episode Extraction (Master Key Logic)
    current_h1_match = re.search(r'^#\s+(.*)$', content, re.MULTILINE)
    current_full_title = current_h1_match.group(1).strip() if current_h1_match else filename.replace('.md', '').title()
    
    final_ep = episode or extract_episode(filename, current_full_title)
    
    # Clean current title from existing index if any
    title_text = new_title or current_full_title
    title_text = re.sub(r'^\d+\s*[:\-]\s*', '', title_text).strip()
    title_text = title_text.replace('**', '') # Remove bolding for title length check
    
    # Enforce 5-word limit for title
    words = title_text.split()
    if len(words) > 5:
        title_text = ' '.join(words[:5])
    
    if final_ep:
        final_h1 = f"# {final_ep} : {title_text}"
        image_name = f"{final_ep}.png"
    else:
        final_h1 = f"# {title_text}"
        image_name = filename.replace('.md', '.png')

    # Update H1
    if current_h1_match:
        content = re.sub(r'^#\s+.*$', final_h1, content, count=1, flags=re.MULTILINE)
    else:
        content = f"{final_h1}\n\n" + content

    # 2. Image Path (Master Key)
    image_path = f"./img/{image_name}"
    
    # 3. Component Cleaning & Podcast Links
    content = content.replace('\u0332', '')
    for placeholder, symbol in KATEX_MAP.items():
        content = content.replace(placeholder, symbol)

    # Remove existing podcast center blocks to avoid duplicates
    content = re.sub(r'<center>\s*<a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE".*?</center>', '', content, flags=re.DOTALL)
    
    if "![cover image]" in content:
        content = re.sub(r'!\[cover image\]\(.*?\)', f'![cover image]({image_path})', content)
        content = re.sub(r'(!\[cover image\].*?\n)', rf'\1\n{PODCAST_LINKS}\n\n', content, count=1)
    else:
        content = re.sub(r'(^# .*?\n)', rf'\1\n![cover image]({image_path})\n\n{PODCAST_LINKS}\n\n', content, count=1)

    # 4. Currency Sanitization (prevents KaTeX parsing errors)
    def curr_repl(m):
        """Replaces $ with USD suffix while preserving original number text."""
        val_text = m.group(1)
        suffix = m.group(2) if m.group(2) else ""
        return f"{val_text}{suffix} USD"

    content = re.sub(r'(?<!\w)\$(?!\^)([\d\.,]+)\s*(k|m|b|t|million|billion|trillion)?\b', curr_repl, content, flags=re.IGNORECASE)
    
    # 5. Footnotes, Cleanup and Wallet Placement
    content = fix_footnotes(content)
    content = content.replace("Truncated", "")
    
    # Ensure wallet is appropriately placed (above citations if they exist)
    # 1. Remove any existing wallet widget blocks
    content = re.sub(r'\n---\n\n### Tips and Donations.*?\n---\n', '', content, flags=re.DOTALL)
    content = content.replace(LIGHTNING_WIDGET, "") # Fallback for exact match
    
    # 2. Insert or Append Widget (except for SUMMARY.md)
    if "SUMMARY.md" not in filename:
        bib_match = re.search(r'#### \*\*Works cited\*\*', content, re.IGNORECASE)
        if bib_match:
            # Insert before bibliography header
            pos = bib_match.start()
            content = content[:pos].strip() + "\n" + LIGHTNING_WIDGET + "\n" + content[pos:]
        else:
            # Append to bottom for files without citations
            content = content.strip() + "\n" + LIGHTNING_WIDGET

    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    check_root()
    import argparse
    parser = argparse.ArgumentParser(description='Universal Markdown Fixer')
    parser.add_argument('file', help='The markdown file to process')
    parser.add_argument('--title', help='Optional: New title', default=None)
    parser.add_argument('--episode', help='Optional: Episode number', default=None)
    args = parser.parse_args()

    if os.path.exists(args.file):
        fix_markdown(args.file, args.title, args.episode)
        update_summary(args.file)
        print(f"\nSuccessfully processed {args.file}")
        print(verify_completeness())
