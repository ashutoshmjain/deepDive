import re

def final_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Restore the podcast links
    podcast_links = """<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>"""
    
    # Replace everything between <center> and </center> at the top
    content = re.sub(r'<center>.*?</center>', podcast_links, content, count=1, flags=re.DOTALL)

    # 2. Fix broken technical terms
    # Fix image references: image[^1] -> image1
    content = re.sub(r'image\[\^(\d+)\]', r'image\1', content)
    # Fix base64: base[^64] -> base64
    content = content.replace('base[^64]', 'base64')
    # Fix other common ones in this file
    content = content.replace('fall[^06]', 'fall06')
    content = content.replace('cos[^576]', 'cos576')
    content = content.replace('bennett[^03]', 'bennett03')
    content = content.replace('v[^1]', 'v1')
    content = content.replace('PMC[^4891656]', 'PMC4891656')
    content = content.replace('PMC[^7451207]', 'PMC7451207')
    content = content.replace('PMC[^11625225]', 'PMC11625225')
    content = content.replace('PMC[^11048803]', 'PMC11048803')
    content = content.replace('WATER.[^2022].S[^10]', 'WATER.2022.S10')
    content = content.replace('id[^1]', 'id1')
    content = content.replace('id[^4]', 'id4')
    content = content.replace('id[^5]', 'id5')
    content = content.replace('id[^6]', 'id6')
    content = content.replace('id[^7]', 'id7')
    content = content.replace('id[^8]', 'id8')
    content = content.replace('id[^9]', 'id9')
    content = content.replace('0cebe[^5563607]', '0cebe5563607')
    content = content.replace('[^15104]', '15104')
    content = content.replace('[^06537]', '06537')
    
    # 3. Fix the citations in text that were NOT changed (if any)
    # Actually, the previous script might have missed some or changed them correctly.
    # Let's check for "cosmos.1" pattern.
    content = re.sub(r'([a-zA-Z”"\'\)\]\.])(\d{1,2})(?=[^0-9a-zA-Z]|$)', r'\1[^\2]', content)
    # But wait, this will match "March 16" -> "March [^16]". 
    # I'll fix known date patterns back.
    content = content.replace('March [^16]', 'March 16')
    content = content.replace('March [^17]', 'March 17')
    content = content.replace('March [^14]', 'March 14')
    content = content.replace('March [^13]', 'March 13')
    content = content.replace('March [^10]', 'March 10')
    content = content.replace('March [^07]', 'March 07')
    content = content.replace('Chapter [^4]', 'Chapter 4')

    # 4. Ensure Works cited is clean
    # The [^n]: Text pattern is good.
    
    # Final check on image labels at the bottom
    content = re.sub(r'\[image(\d+)\]:', r'[image\1]:', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Final Fix applied to {file_path}")

if __name__ == "__main__":
    final_fix("src/bitToIt.md")
