import re

summary_path = 'src/SUMMARY.md'
recent_files = ['./cantillonAI.md', './intrinsicGoogle.md', './STRC_update.md']

with open(summary_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Completely remove the existing "Recent .." section and its duplicates
content = re.sub(r'# Recent \.\.\n.*?(?=\n#|\Z)', '', content, flags=re.DOTALL)

# 2. Remove the specific files from their original categories
# We'll do this by matching the exact markdown link lines
for fname in recent_files:
    # Match the whole line including the bullet point and newline
    pattern = rf'- \[.*\]\({re.escape(fname)}\)\n'
    content = re.sub(pattern, '', content)

# 3. Define the fresh "Recent .." section
recent_section = """
# Recent ..
- [Agentic AI: The Wealth Catalyst](./cantillonAI.md)
- [Google's Quest for Physical AI](./intrinsicGoogle.md)
- [STRC: Corporate Stablecoin Triumph](./STRC_update.md)
"""

# 4. Insert the fresh section after the intro links
intro_end = content.find("[Around and About](./how.md)")
if intro_end != -1:
    insertion_point = content.find("\n", intro_end) + 1
    # Check if there's a blank line after the insertion point
    if content[insertion_point:insertion_point+1] == '\n':
         insertion_point += 1
    content = content[:insertion_point] + recent_section + content[insertion_point:]

with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(content.strip() + "\n")

print("SUMMARY.md manually fixed and cleaned up.")
