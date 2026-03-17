import re

def fix_qm2(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of image labels to KaTeX strings for QM2-verification.md
    katex_map = {
        "image1": r"$W$",
        "image2": r"$Z$",
        "image3": r"$Z^0$",
        "image4": r"$\nu$",
        "image5": r"$T_3$",
        "image6": r"$Y_W$",
        "image7": r"$$Q = T_3 + \frac{Y_W}{2}$$",
        "image8": r"$Q$",
        "image9": r"$T_3$",
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
    fix_qm2("src/QM2-verification.md")
