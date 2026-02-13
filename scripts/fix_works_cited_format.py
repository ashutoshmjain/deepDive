import re

def format_works_cited(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    works_cited_start_pattern = r"#### \*\*Works cited\*\*"
    works_cited_start_match = re.search(works_cited_start_pattern, content)

    if works_cited_start_match:
        before_works_cited = content[:works_cited_start_match.end()]
        works_cited_raw = content[works_cited_start_match.end():]

        # Split by citation number and re-attach numbers
        parts = re.split(r'(\d+\.\s+)', works_cited_raw)
        reconstructed_citations = []
        start_idx = 1 if parts[0].strip() == "" else 0

        for i in range(start_idx, len(parts), 2):
            if i + 1 < len(parts):
                citation_entry = parts[i] + parts[i+1].strip()
                # Remove backslashes from URLs
                citation_entry = re.sub(r'\\([_.-])', r'\1', citation_entry)
                reconstructed_citations.append(citation_entry)
            elif parts[i].strip():
                 reconstructed_citations.append(parts[i].strip())

        works_cited_formatted = "\n\n".join(reconstructed_citations)
        new_content = before_works_cited + "\n\n" + works_cited_formatted.strip()

        # Re-encode the entire file to strip any remaining hidden characters.
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return "Works cited section formatted successfully."
    return "'Works cited' section not found."

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(format_works_cited(sys.argv[1]))
    else:
        print("Please provide a file path.")
