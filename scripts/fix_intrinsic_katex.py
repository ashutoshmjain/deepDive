import re

def fix_intrinsic(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of image labels to KaTeX strings for intrinsicGoogle.md
    katex_map = {
        "image1": r"$(x, y, z)$",
        "image2": r"$\theta$",
        "image3": r"$x$",
        "image4": r"$x = f(\theta)$",
        "image5": r"$\theta = f^{-1}(x)$",
        "image6": r"$R(s, a)$",
        "image7": r"$s$",
        "image8": r"$a$",
        "image9": r"$\pi$",
        "image10": r"$\pi^*$",
        "image11": r"$$J(\pi) = \mathbb{E}_{\tau \sim \pi} \left[ \sum_{t=0}^{\infty} \gamma^t R(s_t, a_t) \right]$$",
        "image12": r"$\gamma$",
        "image13": r"$\tau$",
        "image14": r"$\xi$",
        "image15": r"$\mathcal{D}$",
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
    fix_intrinsic("src/intrinsicGoogle.md")
