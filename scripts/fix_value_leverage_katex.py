import re

def fix_value_leverage(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of image labels to KaTeX strings for valueLeverage.md
    katex_map = {
        "image1": r"$\text{Value} = \text{Gold} + \text{Bitcoin}$",
        "image2": r"$\text{Leverage} = \text{Fiat} \times \text{Credit}$",
        "image3": r"$M$",
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
    fix_value_leverage("src/valueLeverage.md")
