import re
import os

FILE_PATH = "src/241.md"

def finalize_layout():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Platform Snippets
    visual_links = r"""<center><a href="https://www.tiktok.com/@shutoshabot" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">▶ TikTok ◀</a><a href="https://www.instagram.com/shutoshabot/" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">◈ Instagram ◈</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">⫸ YouTube ⫷</a></center>"""

    audio_links = r"""<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>"""

    wallet_widget = r"""
<lightning-widget
  name='Thanks for supporting the publication'
  accent='#f9ce00'
  to='shutosha@primal.net'
  image='https://nostrcheck.me/media/5af0794606a15b5641e25aa23d04af4cb0d7d5e68b11cacb47e56a4698fca8c4/49ff6d00cb5bc819cd19f77783d4815fbd46a5b99b6fbdead1eaecfab798187b.webp'
/>
<script src='https://embed.twentyuno.net/js/app.js'></script>
"""

    # 2. Extraction
    # Video Strip
    strip_match = re.search(r"<!-- VIDEO_STRIP_START -->.*?<!-- VIDEO_STRIP_END -->", content, re.DOTALL)
    video_strip = strip_match.group(0) if strip_match else ""

    # Works Cited (Bibliography)
    works_cited_match = re.search(r"#### \*\*Works Cited\*\*.*$", content, re.DOTALL)
    works_cited_body = works_cited_match.group(0) if works_cited_match else ""

    # Locate the core research body
    # It starts after the first horizontal rule or after the title if no rule
    # In our case, let's find the start of the text after the H1 and any initial metadata
    # The text usually starts with "The concept of immutability..."
    body_start_match = re.search(r"\n\nThe concept of immutability", content)
    if body_start_match:
        body_start_index = body_start_match.start()
    else:
        # Fallback to after first H1
        h1_match = re.search(r"^# .*\n", content)
        body_start_index = h1_match.end() if h1_match else 0

    # The body ends before the first "---" associated with Tips or before Works Cited
    tips_match = re.search(r"\n---.*?\n### Tips and Donations", content, re.DOTALL)
    body_end_index = tips_match.start() if tips_match else (content.find("#### **Works Cited**") if "#### **Works Cited**" in content else len(content))

    research_body = content[body_start_index:body_end_index].strip()

    # 3. Final Assembly
    final_output = "# 241 : What exactly is Immutability?\n\n"
    final_output += video_strip + "\n"
    final_output += visual_links + "\n\n"
    
    final_output += """<p align="center">
<i><b>Note to Readers:</b> This document has been updated to <b>Full Fidelity</b>. It now contains the complete depth of research, exhaustive citations, and absolute KaTeX mathematical proofs delivered via the <b>Lossless Tunnel</b> protocol.</i>
</p>\n\n"""

    final_output += "***\n\n"
    final_output += research_body + "\n\n"
    
    final_output += "---\n\n"
    final_output += "### Tips and Donations\n\n"
    final_output += "If you enjoyed this research, consider supporting the project with a tip in **Sats**. It's a simple, global way to support independent research.\n"
    final_output += wallet_widget + "\n"
    final_output += audio_links + "\n\n"
    final_output += "To send Sats, you'll need a [lightning wallet](https://lightningaddress.com/).\n\n"
    final_output += "---\n\n"
    
    final_output += works_cited_body

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(final_output)

    print("Successfully reorganized Episode 241 layout (V2 - High Fidelity Fix).")

if __name__ == "__main__":
    finalize_layout()
