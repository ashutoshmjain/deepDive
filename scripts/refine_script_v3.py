import re
import os

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'r') as f:
    content = f.read()

# Fix the broken regex replacement from the previous turn
content = content.replace("r'[^]'", "r'[^\1]'")

# Add more comprehensive character stripping
if "re.sub(r'[^\x00-\x7F]+', '', content)" not in content:
    char_strip = """    # 0. Strip invisible and non-ASCII characters that break KaTeX
    content = "".join(c for c in content if c.isprintable() or c in '\n\r\t')
    content = content.replace(chr(0x0332), '')"""
    
    content = content.replace('def fix_markdown(file_path, new_title=None, new_episode=None):',
                             'def fix_markdown(file_path, new_title=None, new_episode=None):\n' + char_strip)

# Ensure currency regex is correct (not double-escaped or corrupted)
old_curr = r"content = re.sub(r'(?<![\w/])\$(?!\^)([\d\.,]+)\s*(k|m|b|t|million|billion|trillion)?\b', curr_repl, content, flags=re.IGNORECASE)"
if old_curr not in content:
    # Attempt to fix if it was corrupted
    content = re.sub(r"content = re.sub\(r'\(\?<!\[\\w/\]\).*?curr_repl, content, flags=re.IGNORECASE\)", old_curr, content)

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'w') as f:
    f.write(content)
