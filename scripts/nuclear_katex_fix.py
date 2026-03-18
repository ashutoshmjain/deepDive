import re

def nuclear_katex_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, preserve the ACTUAL KaTeX block
    math_block = r'$$S = \frac{R_p - R_f}{\sigma_p}$$'
    placeholder = "ACTUAL_MATH_BLOCK_HERE"
    content = content.replace(math_block, placeholder)
    
    # Preserve inline math symbols
    content = content.replace('$R_p$', 'PLACEHOLDER_RP')
    content = content.replace('$R_f$', 'PLACEHOLDER_RF')
    content = content.replace('$\sigma_p$', 'PLACEHOLDER_SIGMA')

    # 2. Now, DELETE all dollar signs from the entire document
    # This is the only way to stop mdbook-katex from hallucinating math blocks
    content = content.replace(r'\\$', '')
    content = content.replace(r'\$', '')
    content = content.replace('$', '')

    # 3. Restore the symbols where needed WITHOUT the dollar sign
    # Or use a different marker if desired, but just the name is safest.
    content = content.replace('STRC', 'STRC') # already there
    
    # 4. Restore the actual math block
    content = content.replace(placeholder, math_block)
    content = content.replace('PLACEHOLDER_RP', '$R_p$')
    content = content.replace('PLACEHOLDER_RF', '$R_f$')
    content = content.replace('PLACEHOLDER_SIGMA', '$\sigma_p$')

    # 5. Fix URLs (ensure no \ in them)
    def url_fix(m):
        return m.group(0).replace('\\', '')
    content = re.sub(r'https?://\S+', url_fix, content)

    # 6. Fix Footnote 14 (The log says it's unreferenced)
    # Let's check the text for it.
    if '[^14]' not in content:
        content = content.replace('approximately 1 billion USD', 'approximately 1 billion USD [^14]')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

nuclear_katex_fix('src/strcSharpRatio.md')
