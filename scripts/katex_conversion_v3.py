import re

def replace_images_with_katex_v3(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Precise mapping
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

    # 1. Handle inlined images ![label](data:...)
    def uri_replacer(match):
        label = match.group(1)
        if label in katex_map:
            return katex_map[label]
        return match.group(0)

    # Regex to match ![imageN](anything)
    content = re.sub(r'!\[(image\d+)\]\([^)]+\)', uri_replacer, content)
    
    # 2. Handle reference style ![label][label] or ![][label] or ![label]
    for label, math in katex_map.items():
        content = content.replace(f"![{label}][{label}]", math)
        content = content.replace(f"![][{label}]", math)
        # Use regex with word boundary for ![image1] but not ![image10]
        # Use lambda for replacement to avoid escape issues
        pattern = r'!\[\b' + re.escape(label) + r'\b\]'
        content = re.sub(pattern, lambda m, val=math: val, content)

    # 3. Handle cases where image name might be duplicated in text like ![image2][image2]
    # (The previous steps might have left some artifacts if the input was messy)
    for label, math in katex_map.items():
        content = content.replace(f"{math}[{label}]", math)

    # 4. Remove definitions at bottom
    content = re.sub(r'^\[image\d+\]:.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n{3,}', '\n\n', content).strip() + "\n"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed KaTeX mapping (V3) in {file_path}")

if __name__ == "__main__":
    replace_images_with_katex_v3("src/bitToIt.md")
