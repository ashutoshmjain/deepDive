import re

def format_works_cited(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    works_cited_start_pattern = r"## Works cited"
    works_cited_start_match = re.search(works_cited_start_pattern, content)

    if works_cited_start_match:
        before_works_cited = content[:works_cited_start_match.end()]
        works_cited_raw = content[works_cited_start_match.end():]

        # Remove backslashes from URLs first
        works_cited_raw = re.sub(r'\\([_.-])', r'\1', works_cited_raw)
        
        # Split by citation number and re-attach numbers, ensuring blank lines
        parts = re.split(r'(\d+\.\s+)', works_cited_raw)
        reconstructed_citations = []
        
        # The first part might be empty if the split starts with a number.
        # If it's not empty, it's leading text before the first citation.
        start_idx = 1 if parts[0].strip() == "" else 0

        for i in range(start_idx, len(parts), 2):
            if i + 1 < len(parts):
                # Combine the number (parts[i]) with the text (parts[i+1])
                citation_entry = parts[i] + parts[i+1].strip()
                reconstructed_citations.append(citation_entry)
            elif parts[i].strip(): # Handle the last part if it's just text after a number
                 reconstructed_citations.append(parts[i].strip())

        works_cited_formatted = "\n\n".join(reconstructed_citations)
        new_content = before_works_cited + "\n\n" + works_cited_formatted.strip()

        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"File {file_path} modified successfully."
        else:
            return f"No changes were made to {file_path}."
    return "'Works cited' section not found."

file_path = "src/the-embedded-value-layer.md"
print(format_works_cited(file_path))
