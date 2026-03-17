import re

def fix_qm1(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of image labels to KaTeX strings for QM1-Uniqueness.md
    katex_map = {
        "image1": r"$e^-$",
        "image2": r"$\pm 1$",
        "image3": r"$U(1)$",
        "image4": r"$S^1$",
        "image5": r"$q$",
        "image6": r"$SU(3)$",
        "image7": r"$p^+$",
        "image8": r"$n^0$",
        "image9": r"$\Delta m > 0$",
        "image10": r"$W$",
        "image11": r"$Z$",
        "image12": r"$W^+$",
        "image13": r"$W^-$",
        "image14": r"$\beta^-$",
        "image15": r"$\beta^+$",
        "image16": r"$Z^0$",
        "image17": r"$P$",
        "image18": r"$10^{-25}$",
    }

    # Replacement logic
    for label, math in katex_map.items():
        content = content.replace(f"![][{label}]", math)
        content = content.replace(f"![{label}]", math)

    # Remove the base64 image definitions at the bottom
    content = re.sub(r'^\[image\d+\]:.*$', '', content, flags=re.MULTILINE)
    
    # Final cleanup
    content = re.sub(r'\n{3,}', '\n\n', content).strip() + "\n"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed KaTeX in {file_path}")

if __name__ == "__main__":
    fix_qm1("src/QM1-Uniqueness.md")
