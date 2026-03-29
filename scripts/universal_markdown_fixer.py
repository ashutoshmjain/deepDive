import re
import os
import subprocess

def get_recent_files(n=3):
    """Returns the n most recently added markdown files in src/ using git."""
    try:
        cmd = "git log --name-only --diff-filter=A --format='%at' src/*.md"
        output = subprocess.check_output(cmd, shell=True, text=True)
        
        files_with_time = []
        current_time = None
        for line in output.split('\n'):
            line = line.strip()
            if not line: continue
            if line.isdigit():
                current_time = int(line)
            elif line.startswith('src/') and line.endswith('.md'):
                if current_time:
                    files_with_time.append((line, current_time))
        
        files_with_time.sort(key=lambda x: x[1], reverse=True)
        unique_files = []
        seen = set()
        for f, t in files_with_time:
            if f not in seen:
                unique_files.append(f)
                seen.add(f)
            if len(unique_files) >= n:
                break
        return unique_files
    except Exception as e:
        print(f"Error getting recent files: {e}")
        return []

def extract_title(file_path):
    """Extracts the H1 title from a markdown file."""
    if not os.path.exists(file_path):
        return os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^#\s+(?:\*\*)?(.*?)(?:\*\*)?$', line.strip())
            if m:
                return m.group(1).strip()
    return os.path.basename(file_path)

def update_summary(target_file_path):
    summary_path = 'src/SUMMARY.md'
    if not os.path.exists(summary_path):
        return

    with open(summary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    target_filename = os.path.basename(target_file_path)
    recent_files = get_recent_files(3)
    
    # 1. Remove the target file and any current 'Recent' files from thematic categories
    # to prevent mdbook "duplicate link" errors.
    recent_filenames = [os.path.basename(f) for f in recent_files]
    
    new_lines = []
    in_recent_section = False
    for line in lines:
        if line.startswith('# Recent ..'):
            in_recent_section = True
            new_lines.append(line)
            continue
        elif line.startswith('# '):
            in_recent_section = False
        
        if not in_recent_section:
            # Check if this line contains a link to any of our recent files
            is_duplicate = False
            for r_fn in recent_filenames:
                if f"./{r_fn}" in line and not line.strip().startswith('#'):
                    is_duplicate = True
                    break
            if is_duplicate:
                continue
        
        new_lines.append(line)

    # 2. Re-construct the 'Recent ..' section with proper titles
    final_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        final_lines.append(line)
        if line.startswith('# Recent ..'):
            for rf in recent_files:
                title = extract_title(rf)
                rf_base = os.path.basename(rf)
                final_lines.append(f"- [{title}](././{rf_base})\n")
            
            # Skip old recent entries
            i += 1
            while i < len(new_lines) and (new_lines[i].strip().startswith('-') or not new_lines[i].strip()):
                if i < len(new_lines) and new_lines[i].startswith('# '):
                    break
                i += 1
            continue
        i += 1

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Headings Cleanup (Remove bolding from H1/H2)
    content = re.sub(r'^#\s+\*\*(.*?)\*\*', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'^##\s+\*\*(.*?)\*\*', r'## \1', content, flags=re.MULTILINE)

    # 2. Cover Image & Podcast Links
    image_name = os.path.basename(file_path).replace('.md', '.png')
    image_path = f"./img/{image_name}"
    
    podcast_links = """<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>"""
    
    if "![cover image]" not in content:
        # Insert after H1
        content = re.sub(r'(^# .*?\n)', rf'\1\n![cover image]({image_path})\n\n{podcast_links}\n\n', content, count=1)

    # 3. KaTeX & Currency
    def curr_repl(m):
        return f"{m.group(1)} USD"
    content = re.sub(r'(?<!\[)(?<!/)\$([\d\.,]+(?: billion| million| trillion)?)', curr_repl, content)
    content = content.replace('$', '\\$')

    # 4. Citations to Footnotes
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
            old_id = int(m.group(1))
            if old_id not in used_cites:
                used_cites[old_id] = next_id
                next_id += 1
            return f"[^{used_cites[old_id]}]"
        
        content = re.sub(r'(?<=[a-zA-Z0-9.])\s*(\d+)(?=\s|$|\n|\.)', cite_repl, content)
        
        ref_sec = "\n\n## References\n\n"
        for old, new in sorted(used_cites.items(), key=lambda x: x[1]):
            if old <= len(citations):
                cite = citations[old-1]
                cite = re.sub(r'\\([_.-])', r'\1', cite)
                ref_sec += f"[^{new}]: {cite}\n\n"
        content += ref_sec

    # 5. Cleanups
    content = content.replace("Truncated", "")
    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target = sys.argv[1]
        fix_markdown(target)
        update_summary(target)
        print(f"Successfully processed {target}")
