import re

def update_summary(summary_path, new_file, new_title, file_to_restore, restore_title, restore_category):
    with open(summary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_recent = False
    recent_count = 0
    
    # Define the recent section lines
    recent_entry = f"- [{new_title}](././{new_file})\n"
    
    # 1. Update Recent Section
    # Find the Recent section
    for i, line in enumerate(lines):
        if line.startswith("# Recent .."):
            in_recent = True
            new_lines.append(line)
            # Add the newest entry at the top of recent
            new_lines.append(recent_entry)
            continue
        
        if in_recent:
            if line.startswith("- "):
                recent_count += 1
                if recent_count < 3:
                    new_lines.append(line)
                # If it's the 3rd one, we omit it (it's the one we're restoring)
                continue
            elif line.strip() == "":
                new_lines.append(line)
                continue
            else:
                in_recent = False
        
        new_lines.append(line)

    # 2. Restore file to thematic category
    # Find the category section
    restored_content = []
    restored_found = False
    restore_line = f"- [{restore_title}](./{file_to_restore})\n"
    
    final_lines = []
    for line in new_lines:
        final_lines.append(line)
        if line.startswith(f"# {restore_category}"):
            final_lines.append(restore_line)
            restored_found = True

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    print(f"Updated {summary_path}")

if __name__ == "__main__":
    update_summary(
        "src/SUMMARY.md",
        "bitToIt.md",
        "Bit to It: Informational Cosmos",
        "strcRetirement.md",
        "STRC: Digital Bridge for Legacy",
        "Digital Credit & The STRC Bridge"
    )
