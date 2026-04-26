import re

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'r') as f:
    content = f.read()

# 1. Add Unicode stripping into the fix_markdown function (if not already there)
if "content.replace(chr(0x0332), '')" not in content:
    unicode_fix = "    # 0. Strip invisible characters\n    content = content.replace(chr(0x0332), '')"
    content = content.replace('def fix_markdown(file_path, new_title=None, new_episode=None):', 
                             'def fix_markdown(file_path, new_title=None, new_episode=None):\n' + unicode_fix)

# 2. Improve footnote detection in fix_footnotes (catch trailing digits)
# First locate the function and replace its start
old_sub = r"body = re.sub(r'(?<!\w)\[(\d+)\](?!\^)', r'[^\1]', body)"
new_sub = r"""    # 1. Convert markers: [n] or trailing digits like .12 or word12 to [^n]
    body = re.sub(r'(?<=[a-zA-Z\.\,])(\d+)(?!\^|\d| USD)', r'[^\1]', body)
    body = re.sub(r'(?<!\w)\[(\d+)\](?!\^)', r'[^\1]', body)"""

if old_sub in content:
    content = content.replace(old_sub, new_sub)

# 3. Fix Currency Regex to avoid fractions like 2/3
old_curr = r"content = re.sub(r'(?<!\w)\$(?!\^)([\d\.,]+)\s*(k|m|b|t|million|billion|trillion)?\b', curr_repl, content, flags=re.IGNORECASE)"
new_curr = r"content = re.sub(r'(?<![\w/])\$(?!\^)([\d\.,]+)\s*(k|m|b|t|million|billion|trillion)?\b', curr_repl, content, flags=re.IGNORECASE)"

if old_curr in content:
    content = content.replace(old_curr, new_curr)

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'w') as f:
    f.write(content)
