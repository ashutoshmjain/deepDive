import re

def absolute_final_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the \STRC issue
    # The user sees \STRC, which means the markdown has \STRC or \$STRC and it's literal.
    # We want $STRC to show up. In mdbook-katex, we MUST escape $ as \\$
    # If the file has \STRC, replace it.
    content = content.replace(r'\STRC', r'\\$STRC')
    content = content.replace(r'\MSTR', r'\\$MSTR')
    content = content.replace(r'\MNAV', r'\\$MNAV')
    
    # Also handle the header and any other stray ones
    # Match STRC not preceded by \
    content = re.sub(r'(?<!\\)STRC', r'\\$STRC', content)
    content = re.sub(r'(?<!\\)MSTR', r'\\$MSTR', content)
    content = re.sub(r'(?<!\\)MNAV', r'\\$MNAV', content)
    
    # Cleanup duplicates like \\$STRC becoming \\$\\$STRC
    content = content.replace(r'\\$\\$STRC', r'\\$STRC')
    content = content.replace(r'\\$\\$MSTR', r'\\$MSTR')
    content = content.replace(r'\\$\\$MNAV', r'\\$MNAV')

    # 2. Fix the missing links in citations
    # The raw markdown has [https://...](https://...)
    # mdbook-katex sometimes eats brackets if it thinks it's in math mode.
    # Ensure the citations section is NOT seen as math.
    # Also, standardise the ampersand in the URLs
    content = content.replace('&amp;si=', '&si=') # Restore original for URLs
    
    # 3. Currency: Ensure no stray $ are left
    # Pattern: $ followed by digits
    def curr_fix(m):
        return f"{m.group(1)} USD"
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?: billion| million| trillion)?)', curr_fix, content)

    # 4. Math blocks: Keep them Absolute KaTeX
    # Preserve the one we have
    content = content.replace(r'$$S = \frac{R_p - R_f}{\sigma_p}$$', '$$S = \\frac{R_p - R_f}{\\sigma_p}$$')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

absolute_final_fix('src/strcSharpRatio.md')
