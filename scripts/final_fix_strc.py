import re

def final_fix(content):
    # Remove duplicated headers/images/podcast links
    # Pattern to find the start of the actual content
    # The actual content starts with "The global financial landscape in 2026..."
    content_start = content.find("The global financial landscape in 2026")
    if content_start != -1:
        actual_content = content[content_start:]
    else:
        actual_content = content # Fallback

    title = "MicroStrategy’s \\$STRC: The 5.37 Sharpe Ratio Benchmark"
    cover_image = "![STRC Sharp Ratio](img/strcSharpRatio.png)"
    podcast_links = '<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>'
    
    new_content = f"# {title}\n\n{cover_image}\n\n{podcast_links}\n\n{actual_content}"
    
    # Fix triple backslashes or other escaping artifacts
    new_content = new_content.replace('\\\\\\$MSTR', '\\$MSTR')
    new_content = new_content.replace('\\\\$MSTR', '\\$MSTR')
    
    # Ensure tables don't have extra blank lines between rows
    # The previous run added blank lines between every line
    lines = new_content.split('\n')
    fixed_lines = []
    in_table = False
    for i, line in enumerate(lines):
        if line.strip().startswith('|'):
            in_table = True
            if line.strip() == '': continue # Skip empty lines in table
            fixed_lines.append(line)
        elif in_table and line.strip() == '' and i+1 < len(lines) and lines[i+1].strip().startswith('|'):
            # Skip blank lines between table rows
            continue
        else:
            in_table = False
            fixed_lines.append(line)
            
    return '\n'.join(fixed_lines)

with open('src/strcSharpRatio.md', 'r') as f:
    content = f.read()

fixed_content = final_fix(content)

with open('src/strcSharpRatio.md', 'w') as f:
    f.write(fixed_content)
