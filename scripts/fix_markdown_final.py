import re

def fix_markdown_final(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the specific heading issue
    content = content.replace('#\# Part II: Top Ten Trends in Business', '## Part II: Top Ten Trends in Business')

    # Fix bolding in all headings
    content = re.sub(r'^(#+) \*\*(.*)\*\*$', r'\1 \2', content, flags=re.MULTILINE)

    # Remove duplicate citations
    content = re.sub(r'(\[\d+(?:, \d+)*\])(?:, \1)+', r'\1', content)

    # General cleanup of extra spaces before citations
    content = re.sub(r'\s+(\[\d+(?:, \d+)*\])', r'\1', content)
    
    # Fix broken markdown link
    content = content.replace('(/#part-ii-top-ten-trends-in-business)  ', '')

    # Format "Works cited" section
    works_cited_heading = "#### Works cited"
    if works_cited_heading in content:
        before_works_cited, works_cited_raw = content.split(works_cited_heading, 1)
        
        # Strip leading/trailing whitespace from the raw citations block
        works_cited_raw = works_cited_raw.strip()

        # Split by the number, keeping the delimiter
        # This handles cases where there is no space after the dot
        parts = re.split(r'(\d+\.)', works_cited_raw)
        
        reconstructed_citations = []
        # Start from the first actual citation content
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                # Combine the number with the citation text
                citation_text = (parts[i] + parts[i+1]).strip()
                # Clean up URLs by removing escaped characters
                citation_text = re.sub(r'\\([_.-])', r'\1', citation_text)
                reconstructed_citations.append(citation_text)

        # Join with double newlines
        works_cited_formatted = "\n\n".join(reconstructed_citations)
        
        # Rebuild the final content
        new_content = before_works_cited + works_cited_heading + "\n\n" + works_cited_formatted

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Markdown fixed successfully.")
    else:
        print("'Works cited' section not found.")


fix_markdown_final('src/GlobalStrategicRetrospective2025.md')
