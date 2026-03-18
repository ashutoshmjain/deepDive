import re

def final_fix_absolute(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, restore everything to a clean state
    # Replace all \\$ and \$ with $
    content = content.replace(r'\\\\$', '$')
    content = content.replace(r'\\$', '$')
    content = content.replace(r'\$', '$')
    
    # 2. Re-apply escaping ONLY where needed for mdbook-katex
    # Tickers: STRC, MSTR, MNAV. We use \\$ to show $
    # Tickers are usually followed by space, punctuation, or end of line.
    content = content.replace('$STRC', r'\\$STRC')
    content = content.replace('$MSTR', r'\\$MSTR')
    content = content.replace('$MNAV', r'\\$MNAV')
    
    # 3. Currency: Replace ALL other $ with USD
    def curr_fix(m):
        return f"{m.group(1)} USD"
    # Match $ followed by digits
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?: billion| million| trillion)?)', curr_fix, content)
    
    # Also handle the $ before tickers if they weren't matched
    content = re.sub(r'(?<!\\)\$STRC', r'\\$STRC', content)
    content = re.sub(r'(?<!\\)\$MSTR', r'\\$MSTR', content)
    content = re.sub(r'(?<!\\)\$MNAV', r'\\$MNAV', content)

    # 4. Math Blocks: Restore Absolute KaTeX
    # Currently it might have \$S or similar. Let's fix the block.
    # The block starts with $$S and ends with p$$
    # Or just use the known block
    content = re.sub(r'\\+\$+\$S = \\frac', r'$$S = \\frac', content)
    content = re.sub(r'\\sigma_p\\+\$+\$', r'\\sigma_p$$', content)
    
    # Inline math
    content = content.replace(r'\\$R_p\\$', r'$R_p$')
    content = content.replace(r'\\$R_f\\$', r'$R_f$')
    content = content.replace(r'\\$\sigma_p\\$', r'$\sigma_p$')

    # 5. Fix URLs (ensure no \ in them)
    def url_fix(m):
        return m.group(0).replace('\\', '')
    content = re.sub(r'https?://\S+', url_fix, content)

    # 6. Ensure Footnote 11
    if '[^11]' not in content:
        content = content.replace('allocated 50 million USD', 'allocated 50 million USD [^11]')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

final_fix_absolute('src/strcSharpRatio.md')
