import subprocess
import re
import os

summary_path = 'src/SUMMARY.md'
exclude = ['SUMMARY.md', 'cover.md', 'how.md']

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

recent_files = get_added_files_from_git()

with open(summary_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Rebuild titles dictionary from current content
file_to_title = {}
link_re = re.compile(r'\[([^\]]+)\]\(\./([^)]+)\)')
for match in link_re.finditer(content):
    title, filename = match.groups()
    if filename in recent_files:
        file_to_title[filename] = title

# Prepare new Recent section using a path-aliasing hack for mdbook
# Using ././filename.md makes it a "different" path to mdbook, but still works.
ordered_links = []
for fname in recent_files:
    if fname in file_to_title:
        # Use ././ to bypass duplicate check
        ordered_links.append(f"- [{file_to_title[fname]}](././{fname})")

recent_section = "# Recent ..\n" + "\n".join(ordered_links) + "\n\n"

# 1. Clean up existing Recent section
content = re.sub(r'# Recent \.\.\n.*?(?=\n#|\Z)', '', content, flags=re.DOTALL)

# 2. Insert fresh Recent section after the intro links
intro_end = content.find("[Around and About](./how.md)")
if intro_end != -1:
    insertion_point = content.find("\n", intro_end) + 1
    if content[insertion_point:insertion_point+1] == '\n':
         insertion_point += 1
    content = content[:insertion_point] + recent_section + content[insertion_point:]

with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(content.strip() + "\n")

print("SUMMARY.md updated with Recent .. using aliased paths (no duplicates).")
