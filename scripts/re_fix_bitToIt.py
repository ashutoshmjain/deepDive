import re
import os

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Re-read original content if possible to undo the bad replacements
    # (Or I can just fix the common bad ones)
    content = content.replace('[^1844532251]', '1844532251')
    content = content.replace('base[^64]', 'base64')
    
    # Fix image references that were broken: image[^1], image[^2], etc.
    content = re.sub(r'image\[\^(\d+)\]', r'image\1', content)
    # Fix URLs that might have been broken: e.g. fall[^06]/cos[^576]
    content = re.sub(r'\[\^(\d+)\]', r'\1', content) # Temp revert all [^n] to n
    
    # Now apply a SAFER citation replacement
    # 1. First, preserve things we DON'T want to change
    # (Not needed if we use a better regex)
    
    # 2. Better Regex for citations: 
    # Must be 1 or 2 digits.
    # Must be preceded by a period, quote, or letter.
    # Must NOT be preceded by "image", "id", "GeV", "K", "base", "v", "S", "cos", "fall", "PMC", "10.", "v", "335673226_", etc.
    # Actually, a simpler way: only match if it's at the end of a word and followed by space or newline or end of file.
    
    # Let's use a list of known citations from the "Works cited" section
    citations = re.findall(r'#### \*\*Works cited\*\*\n\n(?:\[\^(\d+)\]:.*\n?)+', content)
    # Wait, the above might not work if Works cited is already [^n].
    # Let's find all numbers in the Works cited section.
    works_cited_section = re.search(r'#### \*\*Works cited\*\*(.*)', content, re.DOTALL)
    if works_cited_section:
        cite_nums = re.findall(r'(\d+):', works_cited_section.group(1))
        if not cite_nums: # Try the dot format
             cite_nums = re.findall(r'(\d+)\.', works_cited_section.group(1))
        
        # Sort cite_nums descending to avoid partial matches (e.g., 21 before 2)
        cite_nums = sorted(list(set(cite_nums)), key=lambda x: int(x), reverse=True)
        
        for num in cite_nums:
            # Match number preceded by punctuation or letter, and followed by space/newline/punctuation
            # but NOT preceded by letters that indicate it's part of a word/id
            # Negative lookbehind for common prefixes
            pattern = r'(?<!image)(?<!id)(?<!base)(?<!GeV)(?<!K)(?<!v)(?<!S)(?<!cos)(?<!fall)(?<!PMC)(?<!arXiv:)(?<!\d)(?<!\.)' + num + r'(?![0-9])'
            content = re.sub(pattern, r'[^' + num + r']', content)

    # Re-fix the Works cited section formatting
    content = re.sub(r'#### \*\*Works cited\*\*\n\n', r'#### **Works cited**\n\n', content)
    # Ensure it's [^n]: format
    lines = content.split('\n')
    new_lines = []
    in_works_cited = False
    for line in lines:
        if "#### **Works cited**" in line:
            in_works_cited = True
            new_lines.append(line)
            continue
        if in_works_cited:
            # Convert "n. Text" or "n: Text" or "[^n] Text" to "[^n]: Text"
            line = re.sub(r'^\[?\^?(\d+)\]?[\.:\s]+(.*)', r'[^\1]: \2', line)
        new_lines.append(line)
    content = '\n'.join(new_lines)

    # 3. Final cleanup of base64 and other accidental replacements
    content = content.replace('base[^64]', 'base64')
    content = content.replace('image[^', 'image')
    content = content.replace('image', 'image') # Just in case
    
    # Let's be very specific about image definitions at the bottom
    content = re.sub(r'\[image(\d+)\]:', r'[image\1]:', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Re-Fixed {file_path}")

if __name__ == "__main__":
    fix_markdown("src/bitToIt.md")
