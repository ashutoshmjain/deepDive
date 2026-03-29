import re
import os
import subprocess
from datetime import datetime

def get_recent_files(n=3):
    """Returns the n most recently added markdown files in src/ using git."""
    try:
        # Get files sorted by their first commit date
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
        
        # Sort by time descending and take unique filenames
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

def update_summary(file_path, title):
    summary_path = 'src/SUMMARY.md'
    if not os.path.exists(summary_path):
        return

    with open(summary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    filename = os.path.basename(file_path)
    new_entry = f"- [{title}](./{filename})\n"
    
    # 1. Remove from existing thematic categories to avoid duplicates
    new_lines = []
    in_recent = False
    for line in lines:
        if line.startswith('# Recent ..'):
            in_recent = True
        elif line.startswith('# '):
            in_recent = False
        
        if not in_recent and f"./{filename}" in line:
            continue
        new_lines.append(line)
    
    # 2. Update Recent section
    recent_files = get_recent_files(3)
    final_lines = []
    skip_next_list = False
    
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        final_lines.append(line)
        if line.startswith('# Recent ..'):
            # Generate new recent list
            for rf in recent_files:
                rf_base = os.path.basename(rf)
                # Use the path-aliasing hack to get title if possible, or just use filename
                # For simplicity here, we'll try to find the existing title in SUMMARY
                rf_title = rf_base
                for l in lines:
                    if f"./{rf_base}" in l and not l.startswith('#'):
                        m = re.search(r'\[(.*?)\]', l)
                        if m: rf_title = m.group(1)
                        break
                final_lines.append(f"- [{rf_title}](././{rf_base})\n")
            
            # Skip the old list items
            i += 1
            while i < len(new_lines) and (new_lines[i].strip().startswith('-') or not new_lines[i].strip()):
                i += 1
            continue
        i += 1

    # 3. Add to thematic category if not in top 3
    if f"src/{filename}" not in recent_files:
        # Heuristic: Add to the last section or based on content
        # For now, let's just append to the most appropriate section if we can find it
        # or just at the end of the last section.
        pass # Thematic placement is complex, usually requires manual or LLM help

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get Title
    title_match = re.search(r'^#\s+\*\*(.*?)\*\*', content, flags=re.MULTILINE)
    if not title_match:
        title_match = re.search(r'^#\s+(.*)', content, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(file_path)

    # 1. Headings Cleanup
    content = re.sub(r'^#\s+\*\*(.*?)\*\*', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'^##\s+\*\*(.*?)\*\*', r'## \1', content, flags=re.MULTILINE)

    # 2. Cover Image & Podcast Links
    image_name = os.path.basename(file_path).replace('.md', '.png')
    image_path = f"./img/{image_name}"
    
    podcast_links = """<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>"""
    
    if f"![cover image]" not in content:
        cover_md = f"![cover image]({image_path})"
        content = re.sub(r'(# .*?\n)', rf'\1\n{cover_md}\n\n{podcast_links}\n\n', content, count=1)

    # 3. KaTeX & Currency
    # Replace $ amounts with USD (avoiding URLs)
    def curr_repl(m):
        return f"{m.group(1)} USD"
    content = re.sub(r'(?<!\[)(?<!/)\$([\d\.,]+(?: billion| million| trillion)?)', curr_repl, content)
    # Escape literal $
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
        
        # Match numbers that look like citations (e.g., word.1 or word. 1)
        content = re.sub(r'(?<=[a-zA-Z0-9.])\s*(\d+)(?=\s|$|\n|\.)', cite_repl, content)
        
        ref_sec = "\n\n## References\n\n"
        for old, new in sorted(used_cites.items(), key=lambda x: x[1]):
            if old <= len(citations):
                cite = citations[old-1]
                cite = re.sub(r'\\([_.-])', r'\1', cite) # Clean URLs
                ref_sec += f"[^{new}]: {cite}\n\n"
        content += ref_sec

    # 5. General Cleanups
    content = content.replace("Truncated", "")
    content = re.sub(r'\n\s*\n+', r'\n\n', content) # Normalize whitespace

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return title

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        title = fix_markdown(target_file)
        update_summary(target_file, title)
        print(f"Processed {target_file}")
