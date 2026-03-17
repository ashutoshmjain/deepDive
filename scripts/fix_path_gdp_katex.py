import re

def fix_path_gdp(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of image labels to KaTeX strings for pathTo15percentGDP.md
    katex_map = {
        "image1": r"$\Delta V = \int \text{Credit} \cdot dt$",
        "image2": r"$e^{rt}$",
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
    fix_path_gdp("src/pathTo15percentGDP.md")
