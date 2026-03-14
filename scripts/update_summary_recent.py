import re
import os
import glob

summary_path = 'src/SUMMARY.md'
src_dir = 'src'

# Files to exclude from recent list
exclude = ['SUMMARY.md', 'cover.md', 'how.md']

# Get 3 most recently modified markdown files
files = glob.glob(os.path.join(src_dir, '*.md'))
files = [f for f in files if os.path.basename(f) not in exclude]
files.sort(key=os.path.getmtime, reverse=True)
recent_files = files[:3]

with open(summary_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the titles for these files in the current summary
recent_links = []
for file_path in recent_files:
    filename = os.path.basename(file_path)
    # Match [Title](./filename.md)
    pattern = rf'\[([^\]]+)\]\(\./{re.escape(filename)}\)'
    match = re.search(pattern, content)
    if match:
        title = match.group(1)
        recent_links.append(f"- [{title}](./{filename})")

if recent_links:
    recent_section = "# Recent ..\n" + "\n".join(recent_links) + "\n\n"
    
    # Insert after initial links
    # Look for [Around and About](./how.md)
    insertion_point = content.find("[Around and About](./how.md)")
    if insertion_point != -1:
        end_of_line = content.find("\n", insertion_point) + 1
        # Skip an extra newline if present
        if content[end_of_line] == '\n':
            end_of_line += 1
        
        new_content = content[:end_of_line] + "\n" + recent_section + content[end_of_line:]
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUMMARY.md updated with 'Recent ..' section.")
