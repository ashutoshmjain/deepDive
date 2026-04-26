import re
import os

EPISODE_229_MAP_CODE = """
# Specific mappings for Episode 229 (Energy-Intelligence Equivalence)
EPISODE_229_MAP = {
    "![][image1]": r"$E = mc^2$",
    "![][image2]": r"$10-15$",
    "![][image3]": r"$100$",
    "![][image4]": r"$500-1000$",
    "![][image5]": r"$I$",
    "![][image6]": r"$\\eta$",
    "![][image7]": r"$E$",
    "![][image8]": r"$\\Delta S$",
    "![][image9]": r"$$I = \\eta \\frac{\\Delta S \\cdot k_B T}{E}$$",
    "![][image10]": r"$\\Delta S$",
    "![][image11]": r"$T$",
    "![][image12]": r"$W \\ge k_B T \\ln 2$",
    "![][image13]": r"$$T = \\kappa E$$",
    "![][image14]": r"$\\kappa$",
    "![][image15]": r"$E$",
    "![][image16]": r"$2E/\\pi\\hbar$",
    "![][image17]": r"$E = mc^2$",
    "![][image18]": r"$10^{50}$",
    "![][image19]": r"$L$",
    "![][image20]": r"$C$",
    "![][image21]": r"$N$",
    "![][image22]": r"$1/C^\\alpha$",
    "![][image23]": r"$1/N^\\beta$",
    "![][image24]": r"$1/D^\\gamma$",
    "![][image25]": r"$\\rho_s$",
    "![][image26]": r"$P_s$",
    "![][image27]": r"$\\mathcal{M}$",
    "![][image28]": r"$G_{\\mu\\nu}$",
    "![][image29]": r"$$G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = \\kappa T_{\\mu\\nu}$$",
    "![][image30]": r"$a$",
    "![][image31]": r"$\\Phi$",
    "![][image32]": r"$4 \\times 10^{26}$",
    "![][image33]": r"$$I \\propto \\frac{\\Delta S}{E}$$"
}
"""

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'r') as f:
    content = f.read()

# Add EPISODE_229_MAP after KATEX_MAP
content = content.replace('    "![][image37]": r"0-50$"\n}', '    "![][image37]": r"0-50$"\n}\n' + EPISODE_229_MAP_CODE)

# Update fix_markdown to use the correct map
old_placeholder_loop = """    # 2. KaTeX Placeholder Replacement
    for placeholder, latex in KATEX_MAP.items():
        content = content.replace(placeholder, latex)"""

new_placeholder_loop = """    # 2. KaTeX Placeholder Replacement
    current_map = KATEX_MAP
    if "229" in filename:
        current_map = EPISODE_229_MAP
        
    for placeholder, latex in current_map.items():
        content = content.replace(placeholder, latex)"""

content = content.replace(old_placeholder_loop, new_placeholder_loop)

with open('/home/amj/github/deepDive/scripts/universal_markdown_fixer.py', 'w') as f:
    f.write(content)
