import subprocess
import re
import os

summary_path = 'src/SUMMARY.md'
exclude = ['SUMMARY.md', 'cover.md', 'how.md']

# Mapping of files to their "Home" categories to ensure they return correctly
HOME_CATEGORIES = {
    "cantillonAI.md": "# The AI Revolution & Machine Intelligence",
    "strcRetirement.md": "# Digital Credit & The STRC Bridge",
    "strcPE.md": "# Digital Credit & The STRC Bridge",
    "intrinsicGoogle.md": "# The AI Revolution & Machine Intelligence",
    "STRC_update.md": "# Digital Credit & The STRC Bridge",
    "Can-AI-get-rich-superfast.md": "# The AI Revolution & Machine Intelligence",
    "GlobalStrategicRetrospective2025.md": "# Social, Culture & Digital Sovereignty"
}

def get_added_files_from_git():
    cmd = ['git', 'log', '--diff-filter=A', '--name-only', '--format=', '--', 'src/*.md']
    result = subprocess.run(cmd, capture_output=True, text=True)
    recent_files = []
    seen = set()
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith('src/'):
            continue
        filename = os.path.basename(line)
        if filename in exclude:
            continue
        if filename not in seen:
            recent_files.append(filename)
            seen.add(filename)
        if len(recent_files) == 3:
            break
    return recent_files

def update_summary():
    recent_files = get_added_files_from_git()
    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Identify titles for ALL files currently in the summary
    file_to_title = {}
    link_re = re.compile(r'\[([^\]]+)\]\(\./([^)]+)\)')
    for match in link_re.finditer(content):
        title, filename = match.groups()
        # Clean up aliased paths if any
        filename = filename.replace('./', '')
        file_to_title[filename] = title

    # 2. Remove "Recent .." section entirely
    content = re.sub(r'# Recent \.\.\n.*?(?=\n#|\Z)', '', content, flags=re.DOTALL)

    # 3. Clean up any existing links to the 3 recent files (remove duplicates)
    for fname in recent_files:
        # Match standard or aliased paths
        pattern = rf'- \[.*\]\(\.\/(\.\/)?{re.escape(fname)}\)\n'
        content = re.sub(pattern, '', content)

    # 4. Restore any file that WAS recent but is NO LONGER recent to its home
    # We look at our known mapping or fallback to where it was
    all_md_files = [os.path.basename(f) for f in subprocess.run(['ls', 'src/'], capture_output=True, text=True).stdout.splitlines() if f.endswith('.md') and f not in exclude]
    
    for fname in all_md_files:
        if fname not in recent_files:
            # If it's not in the summary at all, put it back
            if f"({fname})" not in content and f"(./{fname})" not in content:
                category = HOME_CATEGORIES.get(fname, "# Social, Culture & Digital Sovereignty") # Fallback
                title = file_to_title.get(fname, fname.replace('.md', ''))
                link = f"- [{title}](./{fname})"
                
                pos = content.find(category)
                if pos != -1:
                    newline_pos = content.find("\n", pos) + 1
                    content = content[:newline_pos] + link + "\n" + content[newline_pos:]

    # 5. Create the new "Recent .." section with standard paths
    ordered_links = []
    for fname in recent_files:
        title = file_to_title.get(fname, fname.replace('.md', ''))
        ordered_links.append(f"- [{title}](./{fname})")
    
    recent_section = "# Recent ..\n" + "\n".join(ordered_links) + "\n\n"

    # 6. Insert Recent section after intro
    intro_end = content.find("[Around and About](./how.md)")
    if intro_end != -1:
        insertion_point = content.find("\n", intro_end) + 1
        if content[insertion_point:insertion_point+1] == '\n':
             insertion_point += 1
        content = content[:insertion_point] + recent_section + content[insertion_point:]

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

update_summary()
print("SUMMARY.md updated: Recent files moved to top, duplicates removed.")
