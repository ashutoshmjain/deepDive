import re

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'r') as f:
    content = f.read()

# 1. Robust character stripping
char_strip_old = """    # 0. Strip invisible and non-ASCII characters that break KaTeX
    content = "".join(c for c in content if c.isprintable() or c in '\n\r\t')
    content = content.replace(chr(0x0332), '')"""

char_strip_new = """    # 0. Strip invisible characters robustly
    content = "".join(c for c in content if ord(c) >= 32 or c in '\n\r\t')"""

if char_strip_old in content:
    content = content.replace(char_strip_old, char_strip_new)
else:
    content = content.replace('def fix_markdown(file_path, new_title=None, new_episode=None):',
                             'def fix_markdown(file_path, new_title=None, new_episode=None):\n' + char_strip_new)

# 2. Fix the footnote regex to be more surgical
old_fn_logic = """    # 1. Convert markers: [n] or trailing digits like .12 or word12 to [^n]
    body = re.sub(r'(?<=[a-zA-Z\.\,])(\d+)(?!\^|\d| USD)', r'[^\1]', body)
    body = re.sub(r'(?<!\w)\[(\d+)\](?!\^)', r'[^\1]', body)"""

new_fn_logic = r"""    # 1. Convert markers: [n] or trailing digits like .12 to [^n]
    # Handle [n] first
    body = re.sub(r'(?<!\w)\[(\d+)\](?!\^)', r'[^\1]', body)
    # Handle trailing digits (only after punctuation or at ends of sentences)
    # This prevents hitting V100 or H100
    body = re.sub(r'(?<!\d)(?<=[\.\,])(\d+)(?!\^|\d| USD)', r'[^\1]', body)
    # Special case: citations at end of words in this specific file style
    if "229" in filename:
         body = re.sub(r'(?<=[a-zA-Z])(\d+)(?!\^|\d| USD|w|W|v|V|h|H|s|S)', r'[^\1]', body)"""

if old_fn_logic in content:
    content = content.replace(old_fn_logic, new_fn_logic)

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'w') as f:
    f.write(content)
