import re
import os

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Main Heading and Cover Image
    title = "# Bit to It: The Informational Universe"
    cover_image = "![cover image](./img/bitToIt.png)"
    podcast_links = """<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>"""

    # Check if title already exists
    if not content.startswith("# "):
        content = f"{title}\n\n{cover_image}\n\n{podcast_links}\n\n{content}"
    else:
        # If title exists, insert cover image and podcast links after it
        content = re.sub(r'^# .*\n', f"{title}\n\n{cover_image}\n\n{podcast_links}\n\n", content)

    # 2. Fix citations in text (convert number to [^number])
    # Matches a number at the end of a sentence or phrase, but not part of a value
    # e.g., "cosmos.1" -> "cosmos.[^1]"
    # Avoid matching things like "300 K" or "2026"
    content = re.sub(r'(?<=[a-zA-Z”"\'\)\]\.])(\d+)(?=[^0-9a-zA-Z]|$)', r'[^\1]', content)
    # Special case for citations like "doctrine,2" -> "doctrine,[^2]"
    content = re.sub(r'(?<=[a-zA-Z”"\'\)\]\.][\.,;])(\d+)(?=[^0-9a-zA-Z]|$)', r'[^\1]', content)

    # 3. Fix Works cited section
    works_cited_match = re.search(r'#### \*\*Works cited\*\*(.*)', content, re.DOTALL)
    if works_cited_match:
        works_cited_text = works_cited_match.group(1)
        # Convert "1. Text" to "[^1]: Text"
        works_cited_fixed = re.sub(r'(\d+)\.\s+(.*)', r'[^\1]: \2', works_cited_text)
        # Ensure URLs are properly formatted (sometimes backslashes are added)
        works_cited_fixed = works_cited_fixed.replace('\\_', '_').replace('\\.', '.')
        content = content.replace(works_cited_text, works_cited_fixed)

    # 4. Final Readability: break into more paragraphs if needed
    # (Simplified: just ensure double newlines between sections and paragraphs)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Ensure math delimiters/ampersands are handled
    # (No $ found, so mostly ampersands)
    # Wait, ampersands in text should be replaced if not in code/math
    # But let's be careful.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_markdown("src/bitToIt.md")
