import re
import os
import glob

summary_path = 'src/SUMMARY.md'
src_dir = 'src'
exclude = ['SUMMARY.md', 'cover.md', 'how.md']

# 1. Get 3 most recently modified markdown files
files = glob.glob(os.path.join(src_dir, '*.md'))
files = [f for f in files if os.path.basename(f) not in exclude]
files.sort(key=os.path.getmtime, reverse=True)
recent_files = [os.path.basename(f) for f in files[:3]]

with open(summary_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 2. Extract all existing links and their categories to rebuild the file
# We'll preserve the structure but remove the 3 recent files from their old spots
new_lines = []
recent_links = []
found_recent_header = False
in_recent_section = False

# First pass: Find titles for the recent files and remove them from everywhere else
file_to_title = {}
# Regex to find [Title](./filename.md)
link_re = re.compile(r'\[([^\]]+)\]\(\./([^)]+)\)')

# We need to preserve the "Recent .." header if it exists, but we'll rebuild its content
cleaned_lines = []
for line in lines:
    if "# Recent .." in line:
        found_recent_header = True
        in_recent_section = True
        cleaned_lines.append(line)
        continue
    
    match = link_re.search(line)
    if match:
        title, filename = match.groups()
        if filename in recent_files:
            file_to_title[filename] = title
            if not in_recent_section:
                continue # Remove from original category
        elif in_recent_section:
            continue # Remove old recent links
    
    if in_recent_section and line.startswith('# ') and "# Recent .." not in line:
        in_recent_section = False
    
    cleaned_lines.append(line)

# 3. Re-insert the 3 recent links into the "Recent .." section
final_lines = []
in_recent = False
recent_added = False

# Ensure recent files are ordered by recency
ordered_recent_links = []
for fname in recent_files:
    if fname in file_to_title:
        ordered_recent_links.append(f"- [{file_to_title[fname]}](./{fname})\n")

for line in cleaned_lines:
    final_lines.append(line)
    if "# Recent .." in line:
        final_lines.extend(ordered_recent_links)
        final_lines.append("\n")
        recent_added = True

# If header wasn't found, add it after intro
if not found_recent_header:
    # Reset and do a fresh insert
    final_lines = []
    inserted = False
    for line in cleaned_lines:
        final_lines.append(line)
        if "[Around and About](./how.md)" in line and not inserted:
            final_lines.append("\n# Recent ..\n")
            final_lines.extend(ordered_recent_links)
            final_lines.append("\n")
            inserted = True

with open(summary_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("SUMMARY.md fixed: Recent files moved to top, duplicates removed.")
