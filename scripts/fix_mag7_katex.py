import re

def fix_mag7(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of image labels to KaTeX strings for mag7split.md
    katex_map = {
        "image1": r"USD 73.0 Billion",
        "image2": r"$$V = \frac{R}{1 + \alpha}$$",
        "image3": r"$\alpha$",
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
    fix_mag7("src/mag7split.md")
