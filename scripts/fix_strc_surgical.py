import re

def final_surgical_fix(content):
    # 1. Header, Image, Podcast links
    title = "MicroStrategy’s \\$STRC: The 5.37 Sharpe Ratio Benchmark"
    cover_image = "![STRC Sharp Ratio](img/strcSharpRatio.png)"
    podcast_links = '<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>'
    
    # Clean duplicates
    content = re.sub(r'^# .*\n', '', content)
    content = re.sub(r'^!\[STRC Sharp Ratio\].*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^<center>.*</center>\n', '', content, flags=re.MULTILINE)
    
    # 2. KaTeX
    content = content.replace("![][image1]", "$$S = \\frac{R_p - R_f}{\\sigma_p}$$")
    content = content.replace("![][image2]", "$R_p$")
    content = content.replace("![][image3]", "$R_f$")
    content = content.replace("![][image4]", "$\\sigma_p$")

    # 3. Tickers & Currency
    content = content.replace("$STRC", "\\$STRC")
    content = content.replace("$MSTR", "\\$MSTR")
    content = content.replace("$MNAV", "\\$MNAV")
    def curr(m): return f"{m.group(1)} USD"
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?:\s*(?:billion|million|trillion))?)', curr, content)

    # 4. Citations in Text
    replacements = {
        '\\ [1]': ' [^1]',
        ' [2]': ' [^2]',
        ' [4]': ' [^3]',
        ' [3]': ' [^4]',
        ' [5]': ' [^5]',
        ' [6]': ' [^6]',
        ' [7]': ' [^7]',
        ' [8]': ' [^8]',
        ' [11]': ' [^9]',
        ' [12]': ' [^10]',
        ' [13]': ' [^11]',
        ' [14]': ' [^12]',
        ' [15]': ' [^13]',
        ' [16]': ' [^14]',
        ' [17]': ' [^15]',
        ' [18]': ' [^16]'
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    # 5. Works Cited Section
    works_cited_start = content.find("#### **Works cited**")
    if works_cited_start != -1:
        text_before = content[:works_cited_start]
        works_cited_raw = content[works_cited_start:]
        
        # Manually fix the entries to ensure they are [^N]: format
        # Regex to find N. and replace with [^NewN]:
        # Mapping: 1->1, 2->2, 4->3, 3->4, 5->5, 6->6, 7->7, 8->8, 11->9, 12->10, 13->11, 14->12, 15->13, 16->14, 17->15, 18->16
        
        lines = works_cited_raw.split('\n')
        new_lines = []
        mapping = {
            '1': '1', '2': '2', '4': '3', '3': '4', '5': '5', '6': '6', '7': '7', '8': '8',
            '11': '9', '12': '10', '13': '11', '14': '12', '15': '13', '16': '14', '17': '15', '18': '16'
        }
        
        for line in lines:
            if line.strip().startswith('####'):
                new_lines.append(line)
                continue
            match = re.match(r'(\d+)\.\s+(.*)', line.strip())
            if match:
                old_num = match.group(1)
                if old_num in mapping:
                    new_lines.append(f"[^{mapping[old_num]}]: {match.group(2)}")
            elif line.strip() == '':
                new_lines.append(line)
        
        # Sort them? mdbook doesn't care, but let's try to keep them neat
        # (Skip sorting for now to avoid complexity, mdbook will handle it)
        content = text_before + '\n'.join(new_lines)

    # 6. Final Header
    content = f"# {title}\n\n{cover_image}\n\n{podcast_links}\n\n" + content.strip()
    return content

# Restore original
import subprocess
subprocess.run(["git", "checkout", "src/strcSharpRatio.md"])

with open('src/strcSharpRatio.md', 'r') as f:
    content = f.read()

fixed = final_surgical_fix(content)
with open('src/strcSharpRatio.md', 'w') as f:
    f.write(fixed)
