import re

def fix_markdown(content):
    # 1. KaTeX Image Replacements (DO THIS FIRST before changing text)
    content = content.replace("![][image1]", "$$S = \\frac{R_p - R_f}{\\sigma_p}$$")
    content = content.replace("![][image2]", "$R_p$")
    content = content.replace("![][image3]", "$R_f$")
    content = content.replace("![][image4]", "$\\sigma_p$")

    # 2. Main Heading & Cover Image & Podcast Links
    # Remove existing titles if any (to be safe)
    content = re.sub(r'^# .*\n', '', content)
    title = "MicroStrategy’s \\$STRC: The 5.37 Sharpe Ratio Benchmark"
    cover_image = "![STRC Sharp Ratio](img/strcSharpRatio.png)"
    podcast_links = '<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>'
    content = f"# {title}\n\n{cover_image}\n\n{podcast_links}\n\n" + content

    # 3. Currency and Tickers
    # Replace tickers first: $STRC -> \$STRC
    content = content.replace("$STRC", "\\$STRC")
    content = content.replace("$MSTR", "\\$MSTR")
    content = content.replace("$MNAV", "\\$MNAV")
    
    # Currency: $100 -> 100 USD
    # Avoid matching math or already escaped stuff
    # Use a lookahead to ensure we are not escaping math
    def currency_replacer(match):
        val = match.group(1)
        # Convert M to million if present
        val = val.replace('M', ' million')
        return f"{val} USD"
    
    # Match $ followed by numbers, but NOT preceded by \ (which would be our escaped tickers)
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?:[M]|\s*(?:billion|million|trillion))?)', currency_replacer, content)

    # 4. Citations & Footnotes
    # Extract references
    works_cited_start = content.find("#### **Works cited**")
    if works_cited_start != -1:
        text_before = content[:works_cited_start]
        works_cited_raw = content[works_cited_start:]
        
        # Parse citations from raw
        citation_lines = re.findall(r'(\d+)\.\s+(.*)', works_cited_raw)
        citations_dict = {num: text for num, text in citation_lines}
        
        # Find all citations in text
        # Original pattern was like ".1" or ".14". We must avoid decimals like "1.5%"
        # A citation usually follows a space or end of word and is NOT followed by a digit
        found_citations = []
        def citation_subber(match):
            # The match is like ".1"
            original_num = match.group(1)
            if original_num in citations_dict:
                if original_num not in found_citations:
                    found_citations.append(original_num)
                new_num = found_citations.index(original_num) + 1
                return f" [{new_num}]"
            return match.group(0)

        # Regex: period followed by digits, NOT preceded by a digit (decimal check), NOT followed by a digit
        # Example: "2026.1" should match ".1", but "1.5" should not match ".5"
        # We use a negative lookbehind for digits
        text_fixed = re.sub(r'(?<!\d)\.(\d+)(?!\d)', citation_subber, text_before)
        
        # Build new Works Cited section
        new_works_cited = "#### **Works cited**\n\n"
        for i, old_num in enumerate(found_citations):
            new_works_cited += f"{i+1}. {citations_dict[old_num]}\n\n"
            
        content = text_fixed + new_works_cited

    # 5. Clean up image leftovers
    content = re.sub(r'\[image\d+\]: <data:image/.*?>', '', content, flags=re.DOTALL)
    
    # 6. Final Readability
    # Fix multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content

# Read original file (I'll need to re-read it because I messed it up)
# Wait, I'll use git checkout to restore it first if I can, or just fix it.
# I'll just fix the mess I made.
with open('src/strcSharpRatio.md', 'r') as f:
    content = f.read()

# Fix the specific mess from previous run:
content = content.replace('\\\\\\$STRC', '$STRC')
content = content.replace('\\\\$STRC', '$STRC')
content = content.replace('\\$STRC', '$STRC')
content = content.replace('1 [3]%', '1.5%') # Hardcoded fix for the common error
content = content.replace('56 [2]', '56.4') # Hardcoded fix for the common error
content = content.replace('3 [2]%', '3.4%') # Hardcoded fix for the common error
content = content.replace('0 [9]', '0.12') # Hardcoded fix for the common error
content = content.replace('0 [10]', '0.11') # Hardcoded fix for the common error

fixed_content = fix_markdown(content)

with open('src/strcSharpRatio.md', 'w') as f:
    f.write(fixed_content)
