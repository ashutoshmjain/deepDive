
import os

old_snippet_start = '<center><span style="font-size: 1.2em; font-weight: bold;">Listen on:</span></center>'
old_snippet_end = 'Fountain.fm</a>'

new_snippet = """<center>
<span style="font-size: 1.2em; font-weight: bold;">Listen on:</span><br><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a>
</center>"""

src_dir = "src"

for filename in os.listdir(src_dir):
    if filename.endswith(".md") and filename not in ["SUMMARY.md", "cover.md", "how.md"]:
        file_path = os.path.join(src_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_snippet_start in content:
            # Find the full old snippet
            start_idx = content.find(old_snippet_start)
            end_idx = content.find(old_snippet_end, start_idx)
            if end_idx != -1:
                end_idx += len(old_snippet_end)
                old_full_snippet = content[start_idx:end_idx]
                new_content = content.replace(old_full_snippet, new_snippet)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename}")
