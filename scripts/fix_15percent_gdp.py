import re
import sys

def fix_markdown(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Fix headings: Ensure blank lines around headings
    # Add newline before headings if missing
    content = re.sub(r'([^\n])\n(#+ )', r'\1\n\n\2', content)
    # Add newline after headings if missing
    content = re.sub(r'(#+ .*?)\n([^\n])', r'\1\n\n\2', content)

    # Replace $ with USD for currency
    content = re.sub(r'\$(\d)', r'USD \1', content)

    # Remove "Truncated"
    content = content.replace("Truncated", "")

    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_markdown("src/pathTo15percentGDP.md")
