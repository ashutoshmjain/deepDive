import subprocess
import re
import os

summary_path = 'src/SUMMARY.md'
exclude = ['SUMMARY.md', 'cover.md', 'how.md']

def get_added_files_from_git():
    # Get filenames based on when they were ADDED to the repo
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
print(f"Recent files (newest additions): {recent_files}")

if not recent_files:
    print("No added files found in git history.")
    exit()

with open(summary_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Rebuild titles dictionary from current content
file_to_title = {}
link_re = re.compile(r'\[([^\]]+)\]\(\./([^)]+)\)')
for match in link_re.finditer(content):
    title, filename = match.groups()
    if filename in recent_files:
        file_to_title[filename] = title

# Clean up existing Recent section
content = re.sub(r'# Recent \.\.\n.*?(?=\n#|\Z)', '', content, flags=re.DOTALL)

# Remove bullets for these files from elsewhere to avoid mdbook duplicates
for fname in recent_files:
    pattern = rf'- \[.*\]\(\./{re.escape(fname)}\)\n'
    content = re.sub(pattern, '', content)

# Prepare new Recent section
ordered_links = []
for fname in recent_files:
    if fname in file_to_title:
        ordered_links.append(f"- [{file_to_title[fname]}](./{fname})")

recent_section = "# Recent ..\n" + "\n".join(ordered_links) + "\n\n"

# Insert after intro
intro_end = content.find("[Around and About](./how.md)")
if intro_end != -1:
    insertion_point = content.find("\n", intro_end) + 1
    if content[insertion_point:insertion_point+1] == '\n':
         insertion_point += 1
    content = content[:insertion_point] + recent_section + content[insertion_point:]

with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(content.strip() + "\n")

print("SUMMARY.md updated using git addition history.")
