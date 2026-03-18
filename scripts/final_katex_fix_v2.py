import re

def fixed_final_katex(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up the messy ticker escaping
    # We want $STRC to show up. In mdbook-katex, \\$ becomes $
    # Currently it has \\$\$STRC or similar.
    content = re.sub(r'\\+\$+\$STRC', r'\\\\$STRC', content)
    content = re.sub(r'\\+\$+\$MSTR', r'\\\\$MSTR', content)
    content = re.sub(r'\\+\$+\$MNAV', r'\\\\$MNAV', content)
    
    # Also handle simpler cases
    content = re.sub(r'(?<!\\)\$STRC', r'\\\\$STRC', content)
    content = re.sub(r'(?<!\\)\$MSTR', r'\\\\$MSTR', content)
    content = re.sub(r'(?<!\\)\$MNAV', r'\\\\$MNAV', content)
    
    # Fix the ones that already had a single backslash
    content = content.replace(r'\STRC', r'\\\\$STRC')
    content = content.replace(r'\MSTR', r'\\\\$MSTR')
    content = content.replace(r'\MNAV', r'\\\\$MNAV')
    
    # Cleanup duplicates from the above replacements
    content = content.replace(r'\\\\\\\\$STRC', r'\\\\$STRC')
    content = content.replace(r'\\\\\\\\$MSTR', r'\\\\$MSTR')
    content = content.replace(r'\\\\\\\\$MNAV', r'\\\\$MNAV')

    # 2. Fix the missing links in citations
    # Ensure URL formatting is clean and not eaten by KaTeX
    # Pattern: [text](url)
    # The links are already there in raw markdown, but they might be broken by the $ signs earlier.
    
    # 3. Currency: Replace ALL stray $ with USD
    # This is the most robust way to stop KaTeX from breaking the whole page.
    def curr_fix(m):
        return f"{m.group(1)} USD"
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?: billion| million| trillion)?)', curr_fix, content)

    # 4. Final verification of the KaTeX block
    content = content.replace(r'$$S = \frac{R_p - R_f}{\sigma_p}$$', '$$S = \\frac{R_p - R_f}{\\sigma_p}$$')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

fixed_final_katex('src/strcSharpRatio.md')
