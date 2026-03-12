
import os

old_snippet_part = '<span style="font-size: 1.2em; font-weight: bold;">Listen on:</span><br>'
src_dir = "src"

for filename in os.listdir(src_dir):
    if filename.endswith(".md"):
        file_path = os.path.join(src_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_snippet_part in content:
            new_content = content.replace(old_snippet_part, "")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
