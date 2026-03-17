import re

def fix_tables_and_images(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dictionary of image labels to their data URIs
    image_defs = re.findall(r'^\[(image\d+)\]:\s*<(data:[^>]+)>', content, re.MULTILINE)
    image_map = {label: uri for label, uri in image_defs}

    def inline_replacer(match):
        label = match.group(1)
        if label in image_map:
            return f"![{label}]({image_map[label]})"
        return match.group(0)

    # 1. Inline images in tables
    # First, identify the tables
    table_pattern = re.compile(r'(\|.*\|(?:\n\|.*\|)+)', re.MULTILINE)
    
    def table_fixer(match):
        table_text = match.group(1)
        # Replace ![][imageN] with ![imageN](data:...)
        fixed_table = re.sub(r'!\[\]\[(image\d+)\]', inline_replacer, table_text)
        return fixed_table

    content = table_pattern.sub(table_fixer, content)

    # 2. Fix other image references in text to use standard ![imageN] syntax
    # (Optional, but let's do it for consistency if it helps)
    content = re.sub(r'!\[\]\[(image\d+)\]', r'![\1][\1]', content)

    # 3. Clean up the image definitions at the bottom
    # Some parsers might not like the < > around data URIs
    content = re.sub(r'^\[(image\d+)\]:\s*<(data:[^>]+)>', r'[\1]: \2', content, flags=re.MULTILINE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed tables and images in {file_path}")

fix_tables_and_images("src/bitToIt.md")
