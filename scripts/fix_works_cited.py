import re

def fix_works_cited(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content

    # Find the "Works cited" section
    works_cited_start_pattern = r"#### **Works cited**"
    works_cited_start_match = re.search(works_cited_start_pattern, content)

    if works_cited_start_match:
        before_works_cited = content[:works_cited_start_match.end()]
        works_cited_raw = content[works_cited_start_match.end():]

        # Replace escaped hyphens in URLs
        works_cited_raw = works_cited_raw.replace('\\-', '-')

        # Also, remove any stray backslashes from URLs that might be causing issues
        works_cited_raw = re.sub(r'\\([_.-])', r'\1', works_cited_raw)
        
        # Ensure there are blank lines between each citation
        parts = re.split(r'(\d+\\.\s+)', works_cited_raw)
        reconstructed_citations = []
        start_idx = 1 if parts[0].strip() == "" else 0

        for i in range(start_idx, len(parts), 2):
            if i + 1 < len(parts):
                citation_entry = parts[i] + parts[i+1].strip()
                reconstructed_citations.append(citation_entry)
            elif parts[i].strip():
                 reconstructed_citations.append(parts[i].strip())

        works_cited_formatted = "\n\n".join(reconstructed_citations)

        new_content = before_works_cited + "\n\n" + works_cited_formatted.strip()

        # Final cleanup of multiple blank lines
        new_content = re.sub(r'\n\s*\n+', r'\n\n', new_content)
        new_content = new_content.strip() + "\n"

        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"File {file_path} modified successfully."
        else:
            return f"No changes were made to {file_path}."
    else:
        return "'Works cited' section not found."

file_to_fix = 'src/corporate-treasury-report.md'
result = fix_works_cited(file_to_fix)
print(result)