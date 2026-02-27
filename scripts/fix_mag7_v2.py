import re
import os

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Restoration fixes: Correct accidental bracket placement from previous script
    # dates, prices, quarters, etc.
    content = re.sub(r'20\s*\[(\d{2})\]', r'20\1', content)
    content = re.sub(r'Q\s*\[(\d)\]', r'Q\1', content)
    content = re.sub(r'USD\s*68\s*\[1\]', r'USD 68.1', content)
    content = re.sub(r'USD\s*65\s*\[7\]', r'USD 65.7', content)
    content = re.sub(r'USD\s*62\s*\[3\]', r'USD 62.3', content)
    content = re.sub(r'USD\s*2\s*\[8\]', r'USD 2.8', content)
    content = re.sub(r'USD\s*1\s*\[62\]', r'USD 1.62', content)
    content = re.sub(r'USD\s*2\s*\[00\]', r'USD 200', content)
    content = re.sub(r'USD\s*71–7\s*\[2\]', r'USD 71-72', content)
    content = re.sub(r'3\s*\[0\]', r'3.0', content)
    content = re.sub(r'USD\s*4\s*\[00\]', r'USD 400', content)
    content = re.sub(r'USD\s*6\s*\[25\]', r'USD 625', content)
    content = re.sub(r'USD\s*1\s*\[25\]', r'USD 1.25', content)
    content = re.sub(r'USD\s*2\s*\[31\]', r'USD 2.31', content)
    content = re.sub(r'USD\s*0\s*\[52\]', r'USD 0.52', content)
    content = re.sub(r'1\s*\[5\]', r'[15]', content)
    content = re.sub(r'Q\s*\[4\]', r'Q4', content)
    content = re.sub(r'Q\s*\[1\]', r'Q1', content)
    
    # Fix the citations properly (space before [N])
    content = re.sub(r'(\w)\[(\d{1,2})\]', r'\1 [\2]', content)
    content = re.sub(r'(\.)\[(\d{1,2})\]', r'\1 [\2]', content)
    content = re.sub(r'(\s)\[(\d{1,2})\]', r' [\2]', content) # cleanup spaces
    
    # Fix image labels that might have been bracketed
    content = re.sub(r'image\s*\[(\d)\]', r'image\1', content)
    
    # Final cleanup of multiple blank lines
    content = re.sub(r'\n\s*\n+', r'\n\n', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_markdown('src/mag7split.md')
