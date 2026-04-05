import re
import os
import subprocess

# Thematic categories mapping - Expanded for better matching
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
    "![][image1]": "$F$",
    "![][image2]": "$\\mathcal{R}$",
    "![][image3]": "$\\Phi$"
}

def get_file_dates():
    """Returns a dict of filename -> initial addition timestamp using git log."""
    try:
        # Use diff-filter=A to get the first time a file was added
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
    except Exception as e:
        return {}

def get_recent_files(n=3):
    try:
        dates = get_file_dates()
        # Convert to list of (filename, date) and sort
        sorted_files = sorted(dates.items(), key=lambda x: x[1], reverse=True)
        return [os.path.join('src', f[0]) for f in sorted_files[:n]]
    except Exception as e:
        return []

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
    
    # Pre-populate with ALL src files to catch missing ones
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
                    if "Recent .." not in current_category:
                        file_to_info[fname][1] = current_category

    # Ensure essential categories exist in order
    essential_sections = ["# Recent ..", "# The Bitcoin Standard & Sovereign Assets", "# The AI Revolution & Machine Intelligence", "# Digital Credit & The STRC Bridge", "# Economics, Capital & The Global Shift", "# Philosophy, Science & The Nature of Reality", "# Social, Culture & Digital Sovereignty"]
    for es in essential_sections:
        if es not in sections_order:
            sections_order.append(es)

    recent_files = get_recent_files(3)
    recent_filenames = [os.path.basename(f) for f in recent_files]

    report = []
    for fname in file_to_info:
        if fname in recent_filenames: continue
        if file_to_info[fname][1] is None:
            new_cat = categorize_file(fname)
            file_to_info[fname][1] = new_cat
            report.append(f"Mapped {fname} to {new_cat}")

    new_content = [
        "# Summary",
        ""
    ]
    for sec in sections_order:
        if sec in ["# Summary", "# About the Project"]: continue
        new_content.append(sec)
        
        if sec == "# Recent ..":
            for rf in recent_files:
                rf_base = os.path.basename(rf)
                title = extract_title(rf)
                new_content.append(f"- [{title}](./{rf_base})")
        else:
            cat_files = []
            for fname, info in file_to_info.items():
                if info[1] == sec and fname not in recent_filenames:
                    cat_files.append({'title': info[0], 'fname': fname, 'date': info[2]})
            
            # SORT CHRONOLOGICALLY (NEWEST FIRST)
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

def fix_markdown(file_path, new_title=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure H1 exists
    if not re.search(r'^#\s+', content, re.MULTILINE):
        title_to_use = new_title or os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()
        content = f"# {title_to_use}\n\n" + content
    
    # Update H1 if title provided
    if new_title:
        if len(new_title.split()) > 5:
            print(f"WARNING: Provided title '{new_title}' exceeds 5 words!")
        content = re.sub(r'^#\s+.*$', f'# {new_title}', content, count=1, flags=re.MULTILINE)

    # Clean up bolding in headers
    content = re.sub(r'^#\s+\*\*(.*?)\*\*', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'^##\s+\*\*(.*?)\*\*', r'## \1', content, flags=re.MULTILINE)
    
    # KaTeX replacements
    for placeholder, symbol in KATEX_MAP.items():
        content = content.replace(placeholder, symbol)

    # Insert or Update cover image and podcast links
    image_name = os.path.basename(file_path).replace('.md', '.png')
    image_path = f"./img/{image_name}"
    podcast_links = """<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>"""
    
    if "![cover image]" in content:
        # Update existing cover image link to match filename
        content = re.sub(r'!\[cover image\]\(.*?\)', f'![cover image]({image_path})', content)
    elif image_name not in content:
        # Insert new cover image link
        content = re.sub(r'(^# .*?\n)', rf'\1\n![cover image]({image_path})\n\n{podcast_links}\n\n', content, count=1)
    
    # Currency conversion
    def curr_repl(m): return f"{m.group(1)} USD"
    content = re.sub(r'(?<!\[)(?<!/)\$([\d\.,]+(?: billion| million| trillion)?)', curr_repl, content)
    content = content.replace('$', '\\$')
    
    # Footnote re-numbering and formatting
    works_cited_match = re.search(r'#### \*\*Works cited\*\*(.*)', content, re.DOTALL)
    if works_cited_match:
        wc_text = works_cited_match.group(1).strip()
        content = content[:works_cited_match.start()].strip()
        citations = []
        for line in wc_text.split('\n'):
            m = re.match(r'^(\d+)\.\s+(.*)', line.strip())
            if m: citations.append(m.group(2).strip())
        
        used_cites = {}
        next_id = 1
        def cite_repl(m):
            nonlocal next_id
            try:
                old_id = int(m.group(1))
                if old_id > 50: return m.group(0) # Likely not a citation if > 50
                if old_id not in used_cites:
                    used_cites[old_id] = next_id
                    next_id += 1
                return f"[^{used_cites[old_id]}]"
            except:
                return m.group(0)

        # Fix: Better regex for citations - avoid decimals and check boundary/parenthesis
        content = re.sub(r'(?<=[a-zA-Z\.\)])\s*(\d{1,2})(?![0-9])', cite_repl, content)
        
        ref_sec = "\n\n## References\n\n"
        for old, new in sorted(used_cites.items(), key=lambda x: x[1]):
            if old <= len(citations):
                cite = citations[old-1]
                cite = re.sub(r'\\([_.-])', r'\1', cite)
                ref_sec += f"[^{new}]: {cite}\n\n"
        content += ref_sec
    
    # Cleanup
    content = content.replace("Truncated", "")
    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    # Lightning Widget
    lightning_widget = """
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
    if "shutosha@primal.net" not in content and "SUMMARY.md" not in file_path:
        if "## References" in content:
            content = content.replace("## References", lightning_widget + "\n\n## References")
        else:
            content = content.strip() + "\n" + lightning_widget

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Universal Markdown Fixer')
    parser.add_argument('file', help='The markdown file to process')
    parser.add_argument('--title', help='Optional: A new 5-word title for the article', default=None)
    args = parser.parse_args()

    target = args.file
    fix_markdown(target, args.title)
    report = update_summary(target)
    
    print(f"Successfully processed {target}")
    if report:
        print("\nRestoration Report:")
        for r in report: print(f"- {r}")
    
    final_title = extract_title(target)
    if len(final_title.split()) > 5:
        print(f"\nCRITICAL WARNING: The title '{final_title}' still exceeds 5 words!")
    else:
        print(f"\nConfirmed Title: '{final_title}' ({len(final_title.split())} words)")
    
    print("\nAutomated Crosscheck:")
    print(verify_completeness())
