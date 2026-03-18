import re

def absolute_katex_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. First, preserve the ACTUAL KaTeX block
    # We'll replace it with a placeholder
    math_block_pattern = r'\$\$S = \\frac\{R_p - R_f\}\{\\sigma_p\}\$\$'
    placeholder = "PLACEHOLDER_MATH_BLOCK"
    content = content.replace(r'$$S = \frac{R_p - R_f}{\sigma_p}$$', placeholder)
    
    # Also preserve inline math if any
    # $R_p$ $R_f$ $\sigma_p$
    content = content.replace('$R_p$', 'PLACEHOLDER_RP')
    content = content.replace('$R_f$', 'PLACEHOLDER_RF')
    content = content.replace('$\sigma_p$', 'PLACEHOLDER_SIGMA')

    # 2. Now replace ALL other dollar signs
    # Tickers: $STRC -> STRC dollars or just STRC
    # Let's use "USD" for currency and just the ticker name for tickers
    content = content.replace('$STRC', 'STRC')
    content = content.replace('$MSTR', 'MSTR')
    content = content.replace('$MNAV', 'MNAV')
    
    # 3. Ampersands in HTML or text
    # The podcast links have &si= and &si=
    # mdbook-katex might be trying to parse them.
    # Let's escape them in the HTML
    content = content.replace('&si=', '&amp;si=')
    # S&P -> S and P
    content = content.replace('S&P', 'S and P')

    # 4. The # in color codes
    # background-color: #2E2E2E
    # mdbook-katex might be seeing this as a start of a header if it thinks it's in math mode.
    # Since we removed other $, this might be fixed.

    # 5. Restore placeholders
    content = content.replace(placeholder, r'$$S = \frac{R_p - R_f}{\sigma_p}$$')
    content = content.replace('PLACEHOLDER_RP', '$R_p$')
    content = content.replace('PLACEHOLDER_RF', '$R_f$')
    content = content.replace('PLACEHOLDER_SIGMA', '$\sigma_p$')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

absolute_katex_fix('src/strcSharpRatio.md')
