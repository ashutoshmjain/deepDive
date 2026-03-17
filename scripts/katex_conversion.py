import re

def replace_images_with_katex(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of image labels to KaTeX strings
    katex_map = {
        "image1": r"$\Delta Q = k_B T \ln 2$",
        "image2": r"$1.5 \times 10^{-52}$",
        "image3": r"$\Delta E = k_B T \ln 2$",
        "image4": r"$c^2$",
        "image5": r"$\Delta E$",
        "image6": r"$2.87 \times 10^{-21}$",
        "image7": r"$\Delta m$",
        "image8": r"$S$",
        "image9": r"$k_B \ln 2$",
        "image10": r"$\lambda$",
        "image11": r"$50 \mu m$",
        "image12": r"$\Lambda$",
        "image13": r"$\bar{\Lambda}$",
        "image14": r"$P$",
        "image15": r"$\Lambda$",
        "image16": r"$\sqrt{s}$",
        "image17": r"$J$",
        "image18": r"$\rho$",
        "image19": r"$$G_{\mu\nu} + S_{\mu\nu} = \kappa (T_{\mu\nu} + M_{\mu\nu}) + \Lambda g_{\mu\nu}$$",
        "image20": r"$G_{\mu\nu}$",
        "image21": r"$S_{\mu\nu}$",
        "image22": r"$T_{\mu\nu}$",
        "image23": r"$M_{\mu\nu}$",
        "image24": r"$\Lambda$",
        "image25": r"$E_s = m_s c_s^2$",
        "image26": r"$c_s$",
    }

    # 1. Replace image references in tables and text
    # Matches ![imageN](data:...) or ![imageN][imageN] or ![][imageN]
    for label, math in katex_map.items():
        # Handle the reference-style and inlined-style patterns
        content = re.sub(r'!\[image\d+\]\((data:[^)]+)\)', lambda m: math if label in m.group(0) else m.group(0), content)
        content = content.replace(f"![{label}][{label}]", math)
        content = content.replace(f"![][{label}]", math)
        content = content.replace(f"![{label}]", math)

    # 2. Remove the base64 image definitions at the bottom
    content = re.sub(r'^\[image\d+\]:.*$', '', content, flags=re.MULTILINE)
    
    # 3. Final cleanup: remove extra newlines at the end
    content = re.sub(r'\n{3,}', '\n\n', content).strip() + "\n"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully replaced all images with KaTeX in {file_path}")

if __name__ == "__main__":
    replace_images_with_katex("src/bitToIt.md")
