import re

def fix_citations_standard(content):
    # 1. Parse existing Works Cited
    # Look for both "#### **Works cited**" and the older numbering or list format
    works_cited_marker = "#### **Works cited**"
    works_cited_start = content.find(works_cited_marker)
    if works_cited_start == -1:
        print("Marker not found")
        return content

    text_before = content[:works_cited_start]
    works_cited_raw = content[works_cited_start:]

    # Parse entries: can be "1. text" or "[^1]: text" or "1 [3] text" (from my previous mess)
    # Let's just find anything that looks like a citation entry
    # Pattern: Digit(s) followed by dot/bracket/colon
    # Or just use the known URLs to find them
    entries = re.split(r'\n(?=\d+\.\s+|\[\^\d+\]:)', works_cited_raw)
    citations_dict = {}
    for entry in entries:
        match = re.search(r'(?:\[\^|(?:\n|^))(\d+)[\]\.]\s*(.*)', entry, re.DOTALL)
        if match:
            num = match.group(1)
            text = match.group(2).strip()
            citations_dict[num] = text

    # 2. Find all citations in text
    # They might be [N] or [^N] or even \ [N]
    found_citations = []
    def text_citation_subber(match):
        num = match.group(1)
        # We need to find this num in our dict. 
        # But wait, my previous script might have renumbered them.
        # Let's just collect all unique ones.
        if num not in found_citations:
            found_citations.append(num)
        new_idx = found_citations.index(num) + 1
        return f"[^{new_idx}]"

    # Match [N] or [^N] or \ [N] or \ [^N]
    # Also handle the 1 [3]% mess if it's still there
    text_fixed = re.sub(r'\\?\s?\[\^?(\d+)\]', text_citation_subber, text_before)

    # 3. Rebuild Works Cited
    new_works_cited = "#### **Works cited**\n\n"
    for i, old_num in enumerate(found_citations):
        # If we can't find the text, use a placeholder
        text = citations_dict.get(old_num, "Source details not found.")
        new_works_cited += f"[^{i+1}]: {text}\n\n"

    return text_fixed + new_works_cited

with open('src/strcSharpRatio.md', 'r') as f:
    content = f.read()

fixed_content = fix_citations_standard(content)

# Final cleanup of common artifacts
fixed_content = fixed_content.replace('\\ [^', ' [^')
fixed_content = re.sub(r'(\d+)\s+\[\^(\d+)\]%', r'\1.\2%', fixed_content) # Fix "1 [3]%" -> "1.3%"

with open('src/strcSharpRatio.md', 'w') as f:
    f.write(fixed_content)
