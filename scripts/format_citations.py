import re

def format_works_cited(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    works_cited_start_pattern = r"### Works cited"
    works_cited_start_match = re.search(works_cited_start_pattern, content)

    if works_cited_start_match:
        before_works_cited = content[:works_cited_start_match.end()]
        works_cited_raw = content[works_cited_start_match.end():]

        # Split by citation number and re-attach numbers
        # This regex will split but keep the numbering for reconstruction
        parts = re.split(r'(\d+\.\s+)', works_cited_raw)
        
        reconstructed_citations = []
        # The split might result in an empty string at the beginning if the match is at the start
        # of the searched string, so we adjust the starting index.
        start_idx = 1 if parts[0].strip() == "" else 0

        for i in range(start_idx, len(parts), 2):
            if i + 1 < len(parts):
                # Reconstruct the citation entry: number + content, then strip trailing spaces
                citation_entry = (parts[i] + parts[i+1]).strip()
                reconstructed_citations.append(citation_entry)
            elif parts[i].strip(): # Handle the last part if it's not a number and not empty
                 reconstructed_citations.append(parts[i].strip())

        # Join with double newlines for blank lines between entries
        works_cited_formatted = "\n\n".join(reconstructed_citations)
        
        # Remove any leading blank lines that might be created before the first citation
        new_content = before_works_cited + "\n\n" + works_cited_formatted.strip()

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return "Works cited section formatted successfully."
    return "'Works cited' section not found."

file_path = "src/meaningOfMeaning-2.md"
print(format_works_cited(file_path))