import re

file_path = "src/cantillonAI.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find footnotes with raw URLs and wrap the URL in markdown link syntax
def make_clickable(match):
    prefix = match.group(1)
    url = match.group(2)
    return f"{prefix}[{url}]({url})"

new_content = re.sub(r'(\[\^\d+\]:\s+)(https?://\S+)', make_clickable, content)

if new_content != content:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Links updated successfully.")
else:
    print("No changes needed or pattern not matched.")
