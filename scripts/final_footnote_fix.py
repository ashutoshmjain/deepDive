import re

def final_footnote_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the double footnote definitions like [^17][^20]:
    content = re.sub(r'\[\^(\d+)\]\[\^(\d+)\]:', r'[^\2]:', content)
    
    # Also ensure no [^n][^m] in text if not intended (but here it was intended)
    # Wait, the previous grep showed:
    # [^17][^20]: ...
    # This was originally [^20]:
    
    # Let's just re-run a clean fix on the Works cited section
    lines = content.split('\n')
    new_lines = []
    in_works_cited = False
    for line in lines:
        if "#### **Works cited**" in line:
            in_works_cited = True
            new_lines.append(line)
            continue
        if in_works_cited:
            # Fix any line starting with multiple footnotes or bad formatting
            # e.g. [^17][^20]: -> [^20]:
            match = re.match(r'^(\[\^\d+\])+[:\s]+(.*)', line)
            if match:
                # Extract the LAST footnote number if multiple
                nums = re.findall(r'\d+', line.split(':')[0])
                last_num = nums[-1]
                new_lines.append(f"[^{last_num}]: {match.group(2)}")
                continue
        new_lines.append(line)
    
    content = '\n'.join(new_lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed footnote definitions in {file_path}")

final_footnote_fix("src/bitToIt.md")
