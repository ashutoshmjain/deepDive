import re

file_path = "src/cantillonAI.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern to find corrupted nested links and simplify them
def simplify_link(match):
    # match.group(1) is the footnote marker e.g., [^1]: 
    # match.group(2) is the URL (it might contain escaped backslashes)
    marker = match.group(1)
    url = match.group(2)
    # Remove any markdown-escaped backslashes from the URL if they exist
    url = url.replace('\\_', '_').replace('\\.', '.')
    return f"{marker}[{url}]({url})"

# This regex matches the corrupted pattern: [^X]: [url](url](url](url)
# We want to catch the first URL and ignore the rest of the garbage.
# The pattern stops at the first ] that is followed by ( or just ends the line.
corrupted_pattern = r'(\[\^\d+\]:\s+)\[(https?://[^\]\s]+)\]\(https?://[^)]+\)'
new_content = re.sub(corrupted_pattern, simplify_link, content)

# If the regex above is too specific, let's try a broader one that just fixes any [URL](URL...
broad_pattern = r'(\[\^\d+\]:\s+)\[(https?://[^\]]+)\]\((https?://[^)]+)\)'
def broad_simplify(match):
    marker = match.group(1)
    url1 = match.group(2)
    # The URL might have been nested multiple times, so url1 might look like "url](url](url"
    actual_url = url1.split('](')[0]
    actual_url = actual_url.replace('\\_', '_').replace('\\.', '.')
    return f"{marker}[{actual_url}]({actual_url})"

new_content = re.sub(broad_pattern, broad_simplify, new_content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Links cleaned up successfully.")
