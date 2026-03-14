import re

summary_path = 'src/SUMMARY.md'
with open(summary_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Restore cantillonAI.md to AI section
ai_section = "# The AI Revolution & Machine Intelligence"
ai_link = "- [Agentic AI: The Wealth Catalyst](./cantillonAI.md)"
if ai_link not in content:
    pos = content.find(ai_section)
    if pos != -1:
        newline_pos = content.find("\n", pos) + 1
        content = content[:newline_pos] + ai_link + "\n" + content[newline_pos:]

# Restore STRC links to Digital Credit section
credit_section = "# Digital Credit & The STRC Bridge"
credit_links = [
    "- [STRC: Digital Bridge for Legacy](./strcRetirement.md)",
    "- [STRC: Superior Digital Credit Yield](./strcPE.md)"
]
pos = content.find(credit_section)
if pos != -1:
    newline_pos = content.find("\n", pos) + 1
    for link in reversed(credit_links): # Insert in order
        if link not in content:
            content = content[:newline_pos] + link + "\n" + content[newline_pos:]

with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored all recent articles to their thematic categories.")
