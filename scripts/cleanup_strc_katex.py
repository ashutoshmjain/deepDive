import re

def final_katex_cleanup(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize Ticker escaping to a single backslash
    # The logs showed things like \\\\ which are likely the culprit
    content = re.sub(r'\\+\$STRC', r'\\$STRC', content)
    content = re.sub(r'\\+\$MSTR', r'\\$MSTR', content)
    content = re.sub(r'\\+\$MNAV', r'\\$MNAV', content)
    
    # Also handle raw $STRC just in case
    content = re.sub(r'(?<!\\)\$STRC', r'\\$STRC', content)
    content = re.sub(r'(?<!\\)\$MSTR', r'\\$MSTR', content)
    content = re.sub(r'(?<!\\)\$MNAV', r'\\$MNAV', content)

    # 2. Fix the specific table errors from the logs
    # Error: Can't use function '\)' in math mode
    content = content.replace(r'End of 2026\)', 'End of 2026)')
    
    # Error: Undefined control sequence: \-
    content = content.replace(r'\-0.67', '-0.67')
    
    # 3. Currency: Ensure $ is replaced by USD or escaped
    # Pattern: $ followed by digits
    def currency_fix(match):
        return f"{match.group(1)} USD"
    # Matches $100 but not escaped \$100
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?: billion| million| trillion)?)', currency_fix, content)

    # 4. Fix footnote 11 reference (Strive Inc allocation)
    # The log says footnote 11 is defined but not referenced.
    # Looking at the text, there's a mention of "Strive Inc. recently allocated 50 million USD... [^11]"
    # Wait, if it's not referenced, maybe the script messed up the numbering.
    # I'll check the text for [^11]
    if '[^11]' not in content:
        # Try to find where it should be (Strive Inc)
        content = content.replace('allocated 50 million USD', 'allocated 50 million USD [^11]')

    # 5. Ampersands in text (memory says replace with 'and' if problematic)
    # S&P 500 -> S and P 500
    content = content.replace('S&P', 'S and P')

    # 6. Ensure KaTeX block is clean
    # The block is $$S = \frac{R_p - R_f}{\sigma_p}$$
    # Ensure no weird characters are inside
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

final_katex_cleanup('src/strcSharpRatio.md')
