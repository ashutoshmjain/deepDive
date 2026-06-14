with open("src/SUMMARY.md", "r") as f: summary = f.read()
with open("src/SUMMARY.md.backup_before_taxonomy", "r") as f: backup = f.read()

import re

# Get thematic part from backup (everything after the old recent section)
backup_parts = backup.split("# The Bitcoin Standard & Sovereign Assets")
if len(backup_parts) == 2:
    thematic_content = "# The Bitcoin Standard & Sovereign Assets" + backup_parts[1]
    
    # Indent it all for the new structure (4 spaces for headers, 8 for items)
    lines = thematic_content.split("\n")
    mod_lines = []
    for line in lines:
        if line.startswith("# "):
            mod_lines.append("    - [" + line[2:].strip() + "]()")
        elif line.startswith("- ["):
            mod_lines.append("        " + line)
        else:
            mod_lines.append("    " + line)
    
    new_thematic = "\n".join(mod_lines)
    
    # Append to the end of new summary
    summary += "\n" + new_thematic
    
with open("src/SUMMARY.md", "w") as f: f.write(summary)
