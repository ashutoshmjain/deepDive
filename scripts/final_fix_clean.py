import re

def final_fix_clean(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Standardize tickers - Use ONLY one backslash if mdbook handles it, 
    # but based on the logs, mdbook-katex thinks anything between $ is math.
    # So we MUST escape all $.
    # If the user sees \$STRC, it means the escape is being rendered literally.
    # In many markdown renderers, \$ shows as $. 
    # But mdbook-katex might be different.
    
    # Let's try replacing all $ with just the name as a test, 
    # but the user wants the $ symbol.
    # The safest way to get $ in mdbook-katex is \\$ (rendered as $)
    
    content = content.replace(r'\\$\$', r'\\$')
    content = content.replace(r'\\$', r'\\\\$')
    # If it was just $, escape it
    content = re.sub(r'(?<!\\)\$', r'\\\\$', content)
    
    # Cleanup double escapes
    content = content.replace(r'\\\\\\\\$', r'\\\\$')
    
    # 2. IMPORTANT: Restore the KaTeX blocks
    # The math block should NOT be escaped
    content = content.replace(r'\\\\$\\$S', r'$$S')
    content = content.replace(r'p\\\\$', r'p$$')
    # Inline math
    content = content.replace(r'\\\\$R_p\\\\$', r'$R_p$')
    content = content.replace(r'\\\\$R_f\\\\$', r'$R_f$')
    content = content.replace(r'\\\\$\sigma_p\\\\$', r'$\sigma_p$')

    # 3. Restore URLs (remove backslashes from URLs)
    def url_fix(m):
        return m.group(0).replace(r'\\$', '$')
    content = re.sub(r'https?://\S+', url_fix, content)

    # 4. Fix Footnote 11
    if '[^11]' not in content:
        content = content.replace('allocated 50 million USD', 'allocated 50 million USD [^11]')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

final_fix_clean('src/strcSharpRatio.md')
