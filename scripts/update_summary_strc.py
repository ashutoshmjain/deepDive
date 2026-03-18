import re

def update_summary(summary_path, new_file_info):
    with open(summary_path, 'r') as f:
        content = f.read()

    # Define thematic categories and where files should go when restored
    restoration_map = {
        'bitToIt.md': ('Philosophy, Science & The Nature of Reality', '[Bit to It: Informational Cosmos](./bitToIt.md)'),
        'cloningVsSexualReproduction.md': ('The AI Revolution & Machine Intelligence', '[Sexual Reproduction: Genetic Lottery](./cloningVsSexualReproduction.md)'),
        'cantillonAI.md': ('The AI Revolution & Machine Intelligence', '[Agentic AI: The Wealth Catalyst](./cantillonAI.md)'),
        'strcSharpRatio.md': ('Digital Credit & The STRC Bridge', '[STRC: The 5.37 Sharpe Benchmark](./strcSharpRatio.md)')
    }

    # 1. Identify current Recent items
    recent_section_match = re.search(r'# Recent \.\.\n(.*?)\n\n', content, re.DOTALL)
    if recent_section_match:
        current_recent_lines = recent_section_match.group(1).strip().split('\n')
        current_recent_files = [re.search(r'\./\./(.*?\.md)', line).group(1) for line in current_recent_lines if '././' in line]
    else:
        current_recent_files = []

    # 2. Identify new Recent items (top 3)
    # We'll just hardcode them based on current state + the new one
    # Newest: strcSharpRatio.md
    # 2nd: bitToIt.md
    # 3rd: cloningVsSexualReproduction.md
    # Item to restore: cantillonAI.md
    new_recent_files = ['strcSharpRatio.md', 'bitToIt.md', 'cloningVsSexualReproduction.md']
    to_restore = [f for f in current_recent_files if f not in new_recent_files]

    # 3. Restore older items to their categories
    for f_name in to_restore:
        if f_name in restoration_map:
            cat_name, entry = restoration_map[f_name]
            # Find category and insert entry at top of its list
            cat_pattern = rf'# {cat_name}\n'
            if re.search(cat_pattern, content):
                content = re.sub(cat_pattern, f'# {cat_name}\n- {entry}\n', content)

    # 4. Update Recent section
    new_recent_text = "# Recent ..\n"
    for f_name in new_recent_files:
        if f_name in restoration_map:
            _, entry = restoration_map[f_name]
            # Convert to recent format ././filename.md
            recent_entry = entry.replace('./', '././')
            new_recent_text += f"- {recent_entry}\n"
    
    if recent_section_match:
        content = content.replace(recent_section_match.group(0), new_recent_text + "\n")

    # 5. Remove new Recent items from their thematic categories (to avoid duplicates)
    for f_name in new_recent_files:
        if f_name in restoration_map:
            _, entry = restoration_map[f_name]
            # Escape entry for regex
            entry_regex = re.escape(f"- {entry}")
            content = re.sub(entry_regex + r'\n?', '', content)

    return content

summary_path = 'src/SUMMARY.md'
updated_content = update_summary(summary_path, None)

with open(summary_path, 'w') as f:
    f.write(updated_content)
