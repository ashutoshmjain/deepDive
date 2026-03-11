
import os
import re

snippet = """<center><span style="font-size: 1.2em; font-weight: bold;">Listen on:</span></center>
<a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a>"""

src_dir = "/home/amj/deepDive/src"
exclude_files = ["SUMMARY.md", "cover.md", "how.md"]

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    content = "".join(lines)
    if "Listen on:" in content:
        # print(f"Skipping {file_path}: already contains 'Listen on:'")
        return

    # Find first header or first non-empty line
    header_idx = -1
    for idx, line in enumerate(lines):
        if line.strip().startswith("#"):
            header_idx = idx
            break
    
    # Check for image after potential header or at start
    image_idx = -1
    search_start = header_idx + 1 if header_idx != -1 else 0
    # Look ahead up to 5 lines for an image
    for idx in range(search_start, min(search_start + 5, len(lines))):
        line = lines[idx].strip()
        if line.startswith("![") or line.startswith("![]"):
            image_idx = idx
            break
        elif line == "" or line.startswith("#"):
            continue
        else:
            # Found text before image, stop looking
            break

    insertion_idx = -1
    if image_idx != -1:
        insertion_idx = image_idx
    elif header_idx != -1:
        insertion_idx = header_idx
    else:
        # No header or image found in first few lines, insert at top
        insertion_idx = -1 # Will insert before line 0

    # Construct new content
    new_lines = []
    if insertion_idx == -1:
        new_lines.append(snippet + "\n\n")
        new_lines.extend(lines)
    else:
        new_lines = lines[:insertion_idx + 1]
        
        # Add spacing before snippet if not already there
        if new_lines[-1].strip() != "":
             new_lines.append("\n")
        
        new_lines.append(snippet + "\n\n")
        
        # Add rest of the file, skipping leading empty lines
        rest = lines[insertion_idx + 1:]
        while rest and rest[0].strip() == "":
            rest.pop(0)
        
        new_lines.extend(rest)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Updated {file_path}")

for filename in os.listdir(src_dir):
    if filename.endswith(".md") and filename not in exclude_files:
        process_file(os.path.join(src_dir, filename))
