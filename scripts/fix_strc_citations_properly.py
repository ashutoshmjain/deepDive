import re

def fix_citations_final(content):
    # Restore original content first
    import subprocess
    subprocess.run(["git", "checkout", "src/strcSharpRatio.md"])
    with open('src/strcSharpRatio.md', 'r') as f:
        content = f.read()

    # 1. Header, Image, Podcast
    title = "MicroStrategy’s \\$STRC: The 5.37 Sharpe Ratio Benchmark"
    cover_image = "![STRC Sharp Ratio](img/strcSharpRatio.png)"
    podcast_links = '<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>'
    
    if not content.startswith("# "):
        content = f"# {title}\n\n{cover_image}\n\n{podcast_links}\n\n" + content

    # 2. KaTeX Image Replacements
    content = content.replace("![][image1]", "$$S = \\frac{R_p - R_f}{\\sigma_p}$$")
    content = content.replace("![][image2]", "$R_p$")
    content = content.replace("![][image3]", "$R_f$")
    content = content.replace("![][image4]", "$\\sigma_p$")

    # 3. Currency and Tickers
    content = content.replace("$STRC", "\\$STRC")
    content = content.replace("$MSTR", "\\$MSTR")
    content = content.replace("$MNAV", "\\$MNAV")
    
    def currency_replacer(match):
        return f"{match.group(1)} USD"
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?:\s*(?:billion|million|trillion))?)', currency_replacer, content)

    # 4. Citations & Footnotes
    works_cited_marker = "#### **Works cited**"
    works_cited_start = content.find(works_cited_marker)
    if works_cited_start != -1:
        text_before = content[:works_cited_start]
        works_cited_raw = content[works_cited_start:]
        
        # Parse numbered list entries: "1. text"
        citation_lines = re.findall(r'(\d+)\.\s+(.*)', works_cited_raw)
        citations_dict = {num: text.strip() for num, text in citation_lines}
        
        found_citations = []
        def citation_subber(match):
            # Match is either ".N" or " [N]"
            # We extracted the groups from regex
            punct = match.group(1)
            num = match.group(2)
            if num in citations_dict:
                if num not in found_citations:
                    found_citations.append(num)
                new_num = found_citations.index(num) + 1
                if punct == '.':
                    return f"[^{new_num}]"
                else:
                    return f" [^{new_num}]"
            return match.group(0)

        # Match .N (where preceded by word char) or [N] (preceded by space)
        # Use a more explicit regex
        # 1. Period immediately followed by digits (Wikipedia style)
        text_fixed = re.sub(r'(?<=\w)\.(\d+)(?!\d)', lambda m: citation_subber(type('M', (object,), {'group': lambda _, i: '.' if i==1 else m.group(1)})()), text_before)
        # 2. Space followed by [N]
        text_fixed = re.sub(r'\s\[(\d+)\]', lambda m: citation_subber(type('M', (object,), {'group': lambda _, i: ' ' if i==1 else m.group(1)})()), text_fixed)
        
        # Build new Works Cited section in [^N]: format
        new_works_cited = "#### **Works cited**\n\n"
        for i, old_num in enumerate(found_citations):
            new_works_cited += f"[^{i+1}]: {citations_dict[old_num]}\n\n"
            
        content = text_fixed + new_works_cited

    # 5. Clean up image leftovers
    content = re.sub(r'\[image\d+\]: <data:image/.*?>', '', content, flags=re.DOTALL)
    
    # 6. Final Cleanups
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

with open('src/strcSharpRatio.md', 'r') as f:
    content = f.read()

fixed_content = fix_citations_final(content)

with open('src/strcSharpRatio.md', 'w') as f:
    f.write(fixed_content)
