import re

summary_path = 'src/SUMMARY.md'
with open(summary_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Definitions of where things belong
restorations = {
    "# The AI Revolution & Machine Intelligence": [
        "- [Can AI Get Rich Superfast?](./Can-AI-get-rich-superfast.md)",
        "- [Google's Quest for Physical AI](./intrinsicGoogle.md)"
    ],
    "# Digital Credit & The STRC Bridge": [
        "- [STRC: Corporate Stablecoin Triumph](./STRC_update.md)"
    ],
    "# Social, Culture & Digital Sovereignty": [
        "- [2025: Tangible Value, Digital Horizons](./GlobalStrategicRetrospective2025.md)"
    ]
}

for section, links in restorations.items():
    if section in content:
        for link in links:
            # Only add if not already there
            filename = re.search(r'\(\./([^)]+)\)', link).group(1)
            if filename not in content:
                # Insert at the top of the section (just after the header line)
                header_pos = content.find(section)
                newline_pos = content.find("\n", header_pos) + 1
                content = content[:newline_pos] + link + "\n" + content[newline_pos:]

with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored missing files to SUMMARY.md")
