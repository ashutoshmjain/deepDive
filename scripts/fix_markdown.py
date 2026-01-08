import re
import os

def fix_markdown_formatting(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    original_content = content

    # --- Dollar Sign Replacements ---
    # Replace dollar amounts with "USD" to avoid KaTeX rendering issues.
    content = re.sub(r'\$(\d+(\.\d+)?)\s*billion', r'USD \1 billion', content)
    content = re.sub(r'\$(\d+(\.\d+)?)\s*million', r'USD \1 million', content)
    content = re.sub(r'\$(\d+)', r'USD \1', content)
    
    # --- Heading Replacements ---
    # Ensure blank lines around main headings (level 1)
    content = re.sub(r'(\n|^)([IVX]+\. [^\n:]+):([^\n]*)', r'\n# \2:\3\n\n', content, flags=re.MULTILINE)
    content = re.sub(r'(\n|^)([IVX]+\. [^\n:]+)([^\n]*)', r'\n# \2\3\n\n', content, flags=re.MULTILINE)

    # Ensure blank lines around sub-headings (level 2)
    content = re.sub(r'(\n|^)(\d+\.\d+ [^\n]+)', r'\n## \2\n\n', content, flags=re.MULTILINE)

    # Clean up multiple blank lines introduced by previous replacements
    content = re.sub(r'\n\s*\n+', r'\n\n', content)


    # --- Works Cited Formatting ---
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
                reconstructed_citations.append(citation_entry)
            elif parts[i].strip():
                    reconstructed_citations.append(parts[i].strip())

        works_cited_formatted = "\n\n".join(reconstructed_citations)
        new_content = before_works_cited + "\n\n" + works_cited_formatted.strip()
        content = new_content

    # Final cleanup of multiple blank lines
    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    # Write the modified content back to the file only if it has changed
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"File {file_path} modified successfully.")
    else:
        print(f"No changes were made to {file_path}.")

fix_markdown_formatting("src/corporate-treasury-report.md")